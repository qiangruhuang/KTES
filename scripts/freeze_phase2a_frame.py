#!/usr/bin/env python3
"""Freeze the outcome-blind Phase 2A Anti-UAV410 design frame."""
from __future__ import annotations
import argparse,csv,hashlib,json,math
from pathlib import Path
ATTR_ORDER=["TC","OV","SV","FM","OC","DBC","Tiny","Small","Medium","Normal"]
SIZE_PRIORITY=["Tiny","Small","Medium","Normal"]
SEVERITY={"Tiny":1.0,"Small":2/3,"Medium":1/3,"Normal":0.0}
EXPECTED_N=120; LIVE_N=40; MIN_PER=2
PINNED_COMMIT="8a8eb04d976e9386b7c9c3ada5c85e5086013d52"
def sha256(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def allocation(counts):
    base={s:(MIN_PER if counts[s] else 0) for s in SIZE_PRIORITY}; rem=LIVE_N-sum(base.values()); residual={s:max(0,counts[s]-base[s]) for s in SIZE_PRIORITY}; den=sum(residual.values())
    q={s:(rem*residual[s]/den if den else 0) for s in SIZE_PRIORITY}; extra={s:math.floor(q[s]) for s in SIZE_PRIORITY}; left=rem-sum(extra.values())
    order=sorted(SIZE_PRIORITY,key=lambda s:(-(q[s]-extra[s]),SIZE_PRIORITY.index(s)))
    for s in order[:left]: extra[s]+=1
    out={s:base[s]+extra[s] for s in SIZE_PRIORITY}; assert sum(out.values())==LIVE_N; return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--official-repo',type=Path,required=True); ap.add_argument('--out-dir',type=Path,required=True); a=ap.parse_args(); repo=a.official_repo; out=a.out_dir; out.mkdir(parents=True,exist_ok=True)
    att_dir=repo/'annos/test/att'; gt_dir=repo/'annos/test'; att_files=sorted(att_dir.glob('*.txt')); gt_files={p.stem:p for p in gt_dir.glob('*.txt') if p.parent==gt_dir}
    if len(att_files)!=EXPECTED_N: raise SystemExit(f'attribute files: {len(att_files)} != {EXPECTED_N}')
    names=[p.stem for p in att_files]
    if set(names)!=set(gt_files): raise SystemExit('attribute/annotation sequence-name mismatch')
    rows=[]; counts={s:0 for s in SIZE_PRIORITY}; source=[]
    for p in att_files:
        vals=[int(x) for x in p.read_text().strip().split(',')]
        if len(vals)!=10 or any(v not in (0,1) for v in vals): raise SystemExit(f'bad attribute vector: {p.name}')
        d=dict(zip(ATTR_ORDER,vals)); active=[s for s in SIZE_PRIORITY if d[s]]
        if not active: raise SystemExit(f'no active size class: {p.stem}')
        stratum=active[0]; counts[stratum]+=1; nframes=sum(1 for line in gt_files[p.stem].read_text().splitlines() if line.strip()); challenge=sum(vals[:6])/6; risk=.5*challenge+.5*SEVERITY[stratum]
        rows.append({'sequence_name':p.stem,**d,'sequence_length':nframes,'log_length_ln':math.log(nframes),'size_stratum':stratum,'challenge_mean':challenge,'size_severity':SEVERITY[stratum],'frozen_aux_risk':risk})
        source.append({'sequence_name':p.stem,'attribute_sha256':sha256(p),'annotation_sha256':sha256(gt_files[p.stem]),'sequence_length':nframes})
    alloc=allocation(counts)
    for r in rows: r['stratum_n_population']=counts[r['size_stratum']]; r['stratum_n_allocated']=alloc[r['size_stratum']]
    csv_path=out/'anti_uav410_test_design_frame_v8.csv'; fields=['sequence_name',*ATTR_ORDER,'sequence_length','log_length_ln','size_stratum','challenge_mean','size_severity','frozen_aux_risk','stratum_n_population','stratum_n_allocated']
    with csv_path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(rows)
    manifest={'schema_version':'KTES-P2A-FRAME-v8.2','official_repository':'HwangBo94/Anti-UAV410','official_commit':PINNED_COMMIT,'population_n':EXPECTED_N,'attribute_order':ATTR_ORDER,'stratum_counts':counts,'allocation_n40':alloc,'length_feature_used':True,'outcome_fields_read':False,'source_files':source,'frame_sha256':sha256(csv_path)}
    (out/'anti_uav410_frame_manifest_v8.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:manifest[k] for k in ['population_n','stratum_counts','allocation_n40','frame_sha256']},indent=2))
if __name__=='__main__': main()
