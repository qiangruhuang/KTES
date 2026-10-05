#!/usr/bin/env python3
"""Reproduce Anti-UAV410 sequence-level State Accuracy from official semantics."""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

def iou(a,b):
    a=list(map(float,a)); b=list(map(float,b)); x1=max(a[0],b[0]); y1=max(a[1],b[1]); x2=min(a[0]+a[2],b[0]+b[2]); y2=min(a[1]+a[3],b[1]+b[3])
    if x2-x1<=0 or y2-y1<=0:return 0.0
    inter=(x2-x1)*(y2-y1); return inter/(a[2]*a[3]+b[2]*b[3]-inter)

def load_pred(p):
    text=p.read_text(encoding='utf-8').strip()
    try:
        obj=json.loads(text); return obj['res'] if isinstance(obj,dict) and 'res' in obj else obj
    except json.JSONDecodeError:
        rows=[]
        for line in text.splitlines():
            line=line.strip()
            if not line: continue
            rows.append([float(x) for x in line.replace(',',' ').split()])
        return rows

def sa(pred,label):
    vals=[]
    for pr,gt,exists in zip(pred,label['gt_rect'],label['exist']):
        if not exists: vals.append(1.0 if len(pr) in (0,1) else 0.0); continue
        if len(gt)<4 or sum(gt)==0: continue
        vals.append(iou(pr,gt) if len(pr)==4 else 0.0)
    if not vals: raise ValueError('no evaluable frames')
    return sum(vals)/len(vals),len(vals)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--dataset-root',type=Path,required=True); ap.add_argument('--pred-dir',type=Path,required=True); ap.add_argument('--frame-csv',type=Path,required=True); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--split',default='test')
    a=ap.parse_args(); expected=[r['sequence_name'] for r in csv.DictReader(a.frame_csv.open())]; rows=[]
    for name in expected:
        lp=a.dataset_root/a.split/name/'IR_label.json'; pp=a.pred_dir/(name+'.txt')
        if not lp.exists() or not pp.exists(): raise SystemExit(f'missing input for {name}: label={lp.exists()} pred={pp.exists()}')
        label=json.loads(lp.read_text(encoding='utf-8')); pred=load_pred(pp); score,n=sa(pred,label)
        rows.append({'sequence_name':name,'SA_i':format(score,'.15g'),'n_evaluable_frames':n,'n_pred_frames':len(pred),'n_label_frames':len(label['exist'])})
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator='\n'); w.writeheader(); w.writerows(rows)
    print(f'N={len(rows)} overall_mean_SA={sum(float(r["SA_i"]) for r in rows)/len(rows):.12f}')
if __name__=='__main__': main()
