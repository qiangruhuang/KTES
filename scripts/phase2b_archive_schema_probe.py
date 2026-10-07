#!/usr/bin/env python3
"""Central-directory-only schema probe for the IDF-DS Zenodo archives.

No ZIP member contents are opened. This probe exists to reconcile the published
Data Records description with the actual public archive member names before any
Phase 2B outcome-bearing payload is accessed.
"""
from __future__ import annotations
import argparse, json, re, hashlib
from collections import Counter
from pathlib import Path, PurePosixPath
from remotezip import RemoteZip

RECORD_ID='16992976'
SOURCES={
 'SpeedyBee_INAV': f'https://zenodo.org/records/{RECORD_ID}/files/Speedybee%20DataSet.zip?download=1',
 'Pixhawk_Jetson_PX4': f'https://zenodo.org/records/{RECORD_ID}/files/Holybro%20Pixhawk.zip?download=1',
}
KEYWORDS=('mission','waypoint','wp','parameter','param','config','gps','kml','flight','log','blackbox','ulg')

def ext(name):
    s=PurePosixPath(name).suffix.lower()
    return s if s else '<none>'

def top(name):
    p=PurePosixPath(name).parts
    return p[0] if p else ''

def sha(x:bytes): return hashlib.sha256(x).hexdigest()

def probe(label,url):
    with RemoteZip(url) as rz:
        infos=[i for i in rz.infolist() if not i.is_dir()]
        names=sorted(str(PurePosixPath(i.filename)) for i in infos)
        lows=[n.lower() for n in names]
        ext_counts=Counter(ext(n) for n in names)
        top_counts=Counter(top(n) for n in names)
        basename_counts=Counter(PurePosixPath(n).name.lower() for n in names)
        keyword_hits={}
        for k in KEYWORDS:
            hit=[n for n,l in zip(names,lows) if k in PurePosixPath(l).name or f'/{k}' in l or l.startswith(k)]
            keyword_hits[k]={'count':len(hit),'examples':hit[:30]}
        candidates=[n for n in names if ext(n) in {'.txt','.csv','.json','.waypoints','.mission','.plan','.params','.param'}]
        return {
          'architecture':label,'archive_url':url,'member_count':len(names),
          'telemetry_values_opened':False,'zip_member_contents_opened':False,
          'extension_counts':dict(ext_counts.most_common()),
          'top_level_counts':dict(top_counts.most_common(50)),
          'common_basenames':dict(basename_counts.most_common(50)),
          'keyword_hits':keyword_hits,
          'candidate_structural_name_count':len(candidates),
          'candidate_structural_name_examples':candidates[:100],
          'first_100_member_names':names[:100],
          'last_50_member_names':names[-50:],
          'member_name_list_sha256':sha(('\n'.join(names)+'\n').encode()),
        }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,default=Path('outputs/phase2b_schema_probe')); a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    data=[probe(k,v) for k,v in SOURCES.items()]
    p=a.out/'phase2b_archive_schema_probe_v8.json'; p.write_text(json.dumps({'schema_version':'KTES-P2B-ARCHIVE-SCHEMA-PROBE-v8.1','zenodo_record':RECORD_ID,'probes':data},indent=2,sort_keys=True)+'\n')
    lines=['# Phase 2B public-archive schema probe v8','',
      'This probe uses ZIP central-directory metadata only. No ZIP member contents or telemetry values are opened.','',
      '| Architecture | members | top extensions | mission hits | parameter hits | waypoint hits | candidate structural names |','|---|---:|---|---:|---:|---:|---:|']
    for d in data:
      ex=', '.join(f'{k}:{v}' for k,v in list(d['extension_counts'].items())[:5])
      lines.append(f"| {d['architecture']} | {d['member_count']} | {ex} | {d['keyword_hits']['mission']['count']} | {d['keyword_hits']['parameter']['count']} | {d['keyword_hits']['waypoint']['count']} | {d['candidate_structural_name_count']} |")
    lines += ['', '## Gate rule','',
      'The Phase 2B pre-outcome protocol requires mission plans and static parameters before telemetry outcomes are opened. If the public archive does not expose semantically equivalent structural files, the gate remains **BLOCKED_SOURCE_STRUCTURE**. Outcome-bearing telemetry must not be opened merely to reconstruct a design frame that was supposed to be pre-outcome.','']
    m=a.out/'PHASE2B_ARCHIVE_SCHEMA_PROBE_v8.md'; m.write_text('\n'.join(lines))
    print(p,sha(p.read_bytes())); print(m,sha(m.read_bytes()))
if __name__=='__main__': main()
