#!/usr/bin/env python3
"""Reconcile actual IDF-DS public archive layout with the Phase2B freeze.

Allowed reads: ZIP central-directory metadata and the archive-level QGroundControl
`.plan` mission reference only. No telemetry CSV, GPS path, ULog or INAV raw log
member content is opened.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from collections import Counter
from pathlib import Path, PurePosixPath
from remotezip import RemoteZip

RID='16992976'
SOURCES={
 'SpeedyBee_INAV':f'https://zenodo.org/records/{RID}/files/Speedybee%20DataSet.zip?download=1',
 'Pixhawk_Jetson_PX4':f'https://zenodo.org/records/{RID}/files/Holybro%20Pixhawk.zip?download=1',
}

def sha(b): return hashlib.sha256(b).hexdigest()

def plan_summary(data:bytes):
    txt=data.decode('utf-8-sig')
    obj=json.loads(txt)
    mission=obj.get('mission',{}) if isinstance(obj,dict) else {}
    items=mission.get('items',[]) if isinstance(mission,dict) else []
    commands=[]; coords=[]
    for it in items:
        if not isinstance(it,dict): continue
        cmd=it.get('command'); commands.append(cmd)
        params=it.get('params')
        if isinstance(params,list) and len(params)>=7:
            try:
                lat=float(params[4]); lon=float(params[5]); alt=float(params[6])
                coords.append((round(lat,7),round(lon,7),round(alt,3)))
            except (TypeError,ValueError): pass
    geom_payload=json.dumps({'commands':commands,'coords':coords},separators=(',',':'),sort_keys=True).encode()
    return {
      'sha256':sha(data),'item_count':len(items),'command_counts':dict(Counter(map(str,commands))),
      'coordinate_item_count':len(coords),'geometry_signature_sha256':sha(geom_payload),
      'planned_home_position_present': bool(mission.get('plannedHomePosition')),
    }

def ids_from_names(names, patterns):
    out=set()
    for n in names:
      for p in patterns:
        m=p.search(n)
        if m:
          out.add(int(m.group(1))); break
    return sorted(out)

def probe(label,url):
  with RemoteZip(url) as rz:
    infos=[i for i in rz.infolist() if not i.is_dir()]
    names=sorted(str(PurePosixPath(i.filename)) for i in infos)
    plans=[n for n in names if PurePosixPath(n).suffix.lower()=='.plan']
    plan_records=[]
    for n in plans:
      with rz.open(n) as f: data=f.read(5_000_001)
      if len(data)>5_000_000: raise RuntimeError('plan too large')
      plan_records.append({'member':n,**plan_summary(data)})
    if label=='SpeedyBee_INAV':
      proc_ids=ids_from_names(names,[re.compile(r'/Lap(\d+)_',re.I), re.compile(r'/Lap(\d+)\.',re.I)])
      grouped_ids=[]
      ungrouped_ids=[]
      raw=[n for n in names if re.search(r'/rawdata/LOG\d+\.TXT$',n,re.I)]
    else:
      grouped_ids=ids_from_names(names,[re.compile(r'/Grouped flights/vuelo_(\d+)_sync\.csv$',re.I)])
      ungrouped_ids=ids_from_names(names,[re.compile(r'/UnGrouped flights/(?:lap_\d+/)?lap_(\d+)(?:/|$)',re.I),re.compile(r'/UnGrouped flights/lap_(\d+)(?:/|$)',re.I)])
      proc_ids=sorted(set(grouped_ids)|set(ungrouped_ids))
      raw=[n for n in names if re.search(r'/rawdata/.+\.ulg$',n,re.I)]
    param_like=[n for n in names if re.search(r'(parameter|parameters|param)(?:_|\.|/)',PurePosixPath(n).name,re.I)]
    metadata_like=[n for n in names if re.search(r'(weather|environment|metadata|meta_data|conditions)',PurePosixPath(n).name,re.I)]
    return {
      'architecture':label,'member_count':len(names),'plan_records':plan_records,
      'processed_unit_ids':proc_ids,'processed_unit_count':len(proc_ids),
      'grouped_unit_ids':grouped_ids,'grouped_unit_count':len(grouped_ids),
      'ungrouped_unit_ids':ungrouped_ids,'ungrouped_unit_count':len(ungrouped_ids),
      'raw_log_member_count':len(raw),'raw_log_member_examples':raw[:30],
      'parameter_like_member_count':len(param_like),'parameter_like_examples':param_like[:30],
      'independent_metadata_like_member_count':len(metadata_like),'independent_metadata_like_examples':metadata_like[:30],
      'telemetry_member_contents_opened':False,'allowed_plan_member_contents_opened':True,
    }

def main():
  ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,default=Path('outputs/phase2b_source_reconciliation')); a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
  probes=[probe(k,v) for k,v in SOURCES.items()]
  plan_sigs=[r['geometry_signature_sha256'] for p in probes for r in p['plan_records']]
  one_shared_each=all(len(p['plan_records'])==1 for p in probes)
  same_geom=len(set(plan_sigs))==1 if plan_sigs else False
  per_unit_structural=any(p['parameter_like_member_count']>0 for p in probes) or any(len(p['plan_records'])>1 for p in probes)
  gate='BLOCKED_INSUFFICIENT_PREOUTCOME_COVARIATE_RESOLUTION' if one_shared_each and not per_unit_structural else 'REQUIRES_FURTHER_STRUCTURAL_AUDIT'
  out={
    'schema_version':'KTES-P2B-SOURCE-RECONCILIATION-v8.1','zenodo_record':RID,'probes':probes,
    'one_archive_level_plan_each':one_shared_each,'shared_plan_geometry_identical_across_architectures':same_geom,
    'per_unit_mission_or_parameter_metadata_detected':per_unit_structural,
    'telemetry_values_opened':False,'gate':gate,
    'interpretation':'Do not substitute GPS/telemetry-derived features for missing per-unit pre-outcome design covariates.'
  }
  j=a.out/'phase2b_source_reconciliation_v8.json'; j.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
  lines=['# Phase 2B source reconciliation v8','',f'**Gate:** **{gate}**','',
    'This reconciliation reads ZIP central-directory metadata and the archive-level `.plan` mission reference only. No telemetry CSV, GPS path, ULog, INAV raw-log, state, airspeed, power, or sensor values are opened.','',
    '| Architecture | processed unit IDs | grouped IDs | ungrouped IDs | raw logs | `.plan` files | parameter-like files |','|---|---:|---:|---:|---:|---:|---:|']
  for p in probes:
    lines.append(f"| {p['architecture']} | {p['processed_unit_count']} | {p['grouped_unit_count']} | {p['ungrouped_unit_count']} | {p['raw_log_member_count']} | {len(p['plan_records'])} | {p['parameter_like_member_count']} |")
  lines += ['',f"Archive-level plan geometry identical across architectures: **{same_geom}**.", '',
    '## Consequence for the frozen Phase 2B design','',
    'The preregistered KTES design requires flight-level outcome-blind covariates so that novelty, adverse-tail scoring, sentinels and positive inclusion probabilities are defined before outcomes. A single archive-level mission plan (and no per-flight static parameter snapshot) cannot provide within-stratum flight-condition heterogeneity. Flight/lap identifiers are labels, not engineering covariates.','',
    'Therefore telemetry-derived GPS paths, wind, realised speeds, state histories or other post-flight quantities must not be promoted into the sampling frame to rescue the design. If no separate preflight/mission metadata release exists, Phase 2B as preregistered is blocked by source structure and should be reported as an external-data limitation rather than redesigned on the same outcomes.','']
  m=a.out/'PHASE2B_SOURCE_RECONCILIATION_v8.md'; m.write_text('\n'.join(lines))
  print(json.dumps({'gate':gate,'same_geometry':same_geom,'counts':[(p['architecture'],p['processed_unit_count']) for p in probes]},indent=2))
  print(j.name,sha(j.read_bytes())); print(m.name,sha(m.read_bytes()))
if __name__=='__main__': main()
