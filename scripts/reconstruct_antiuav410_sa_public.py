#!/usr/bin/env python3
"""Reconstruct SiamFC sequence SA from public Anti-UAV410 box annotations.

This is an equivalence-audit path. It treats an all-zero public GT box as target absent
and otherwise mirrors the official Evaluation_for_SA.py frame score. The output must
not be promoted to the frozen Phase2A primary endpoint until the equivalence audit is
accepted.
"""
from __future__ import annotations
import argparse,csv,json,math
from pathlib import Path


def iou(a,b):
    a=list(map(float,a)); b=list(map(float,b))
    x0=max(a[0],b[0]); y0=max(a[1],b[1]); x1=min(a[0]+a[2],b[0]+b[2]); y1=min(a[1]+a[3],b[1]+b[3])
    if x1-x0<=0 or y1-y0<=0:return 0.0
    inter=(x1-x0)*(y1-y0); den=a[2]*a[3]+b[2]*b[3]-inter
    return inter/den if den>0 else 0.0


def load_rows(p:Path):
    text=p.read_text(encoding='utf-8').strip()
    if not text:return []
    try:
        obj=json.loads(text)
        if isinstance(obj,dict) and 'res' in obj: obj=obj['res']
        if isinstance(obj,list): return [list(x) if isinstance(x,(list,tuple)) else [x] for x in obj]
    except json.JSONDecodeError: pass
    rows=[]
    for line in text.splitlines():
        line=line.strip()
        if line: rows.append([float(x) for x in line.replace(',',' ').split()])
    return rows


def is_zero_gt(x):
    return len(x)==4 and all(abs(float(v))<1e-12 for v in x)


def absent_pred(x):
    return len(x) in (0,1)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--official-repo',type=Path,required=True)
    ap.add_argument('--pred-dir',type=Path,required=True)
    ap.add_argument('--frame-csv',type=Path,required=True)
    ap.add_argument('--output-csv',type=Path,required=True)
    ap.add_argument('--audit-json',type=Path,required=True)
    a=ap.parse_args()
    frame=list(csv.DictReader(a.frame_csv.open(encoding='utf-8')))
    if len(frame)!=120: raise SystemExit(f'frozen frame has {len(frame)} rows, expected 120')
    out=[]; total_frames=zero_frames=pred_absent_frames=0; mismatches=[]; bad_gt=[]; pred_widths={}; zero_by_ov={'0':0,'1':0}; zero_seq_by_ov={'0':set(),'1':set()}
    for r in frame:
        name=r['sequence_name']; gp=a.official_repo/'annos/test'/(name+'.txt'); pp=a.pred_dir/(name+'.txt')
        if not gp.exists() or not pp.exists(): raise SystemExit(f'missing {name}: gt={gp.exists()} pred={pp.exists()}')
        gt=load_rows(gp); pred=load_rows(pp)
        if len(gt)!=len(pred): mismatches.append({'sequence_name':name,'gt_n':len(gt),'pred_n':len(pred)})
        vals=[]; z=0; pa=0
        for j,(g,p) in enumerate(zip(gt,pred)):
            pred_widths[str(len(p))]=pred_widths.get(str(len(p)),0)+1
            if len(g)!=4: bad_gt.append({'sequence_name':name,'frame':j,'gt':g}); continue
            if is_zero_gt(g):
                z+=1; score=1.0 if absent_pred(p) else 0.0
            else:
                score=iou(p,g) if len(p)==4 else 0.0
            pa+=int(absent_pred(p)); vals.append(score)
        if not vals: raise SystemExit(f'no evaluable frames: {name}')
        sa=sum(vals)/len(vals); total_frames+=len(vals); zero_frames+=z; pred_absent_frames+=pa
        ov='1' if str(r['OV'])=='1' else '0'; zero_by_ov[ov]+=z
        if z: zero_seq_by_ov[ov].add(name)
        out.append({'sequence_name':name,'SA_reconstructed':format(sa,'.15g'),'n_scored_frames':len(vals),'n_zero_gt_absent':z,'n_absent_predictions':pa,'OV':r['OV'],'size_stratum':r['size_stratum']})
    a.output_csv.parent.mkdir(parents=True,exist_ok=True)
    with a.output_csv.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=out[0].keys(),lineterminator='\n'); w.writeheader(); w.writerows(out)
    audit={
      'schema_version':'KTES-P2A-SA-RECON-AUDIT-v8.1','population_n':len(out),'sequence_name_match':True,
      'all_sequence_lengths_match':not mismatches,'length_mismatches':mismatches,'bad_gt_rows':bad_gt,
      'prediction_row_width_counts':pred_widths,'total_scored_frames':total_frames,'zero_gt_frames':zero_frames,
      'zero_gt_fraction':zero_frames/total_frames,'predicted_absent_frames':pred_absent_frames,
      'zero_gt_frames_by_sequence_OV':zero_by_ov,
      'sequences_with_zero_gt_by_sequence_OV':{k:len(v) for k,v in zero_seq_by_ov.items()},
      'equal_sequence_mean_SA_reconstructed':sum(float(x['SA_reconstructed']) for x in out)/len(out),
      'status':'RECONSTRUCTED_CANDIDATE_NOT_YET_PROMOTED_TO_FROZEN_PRIMARY_ENDPOINT',
      'assumption_requiring_equivalence_evidence':'all-zero public annos/test GT box denotes target absent in IR_label.json'
    }
    a.audit_json.write_text(json.dumps(audit,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(audit,indent=2,sort_keys=True))
if __name__=='__main__': main()
