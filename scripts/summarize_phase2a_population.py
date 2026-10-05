#!/usr/bin/env python3
"""Summarize frozen Phase2A full-population outcomes without sampling execution."""
from __future__ import annotations
import argparse,csv,hashlib,json,math,statistics
from pathlib import Path
CHALLENGES=['TC','OV','SV','FM','OC','DBC']
SIZES=['Tiny','Small','Medium','Normal']

def sha256(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()
def qlinear(xs,p):
    ys=sorted(xs); h=(len(ys)-1)*p; lo=math.floor(h); hi=math.ceil(h)
    return ys[lo] if lo==hi else ys[lo]+(h-lo)*(ys[hi]-ys[lo])
def mean_for(rows,key=None,val=None):
    z=[r['SA_i'] for r in rows if key is None or r[key]==val]; return sum(z)/len(z),len(z)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--frame',type=Path,required=True); ap.add_argument('--sa',type=Path,required=True); ap.add_argument('--json-out',type=Path,required=True); ap.add_argument('--md-out',type=Path,required=True); a=ap.parse_args()
    fr={r['sequence_name']:r for r in csv.DictReader(a.frame.open(encoding='utf-8'))}; sr={r['sequence_name']:r for r in csv.DictReader(a.sa.open(encoding='utf-8'))}
    if len(fr)!=120 or len(sr)!=120 or set(fr)!=set(sr): raise SystemExit('frame/SA must match 120 unique sequences')
    rows=[]
    for n in sorted(fr):
        x=dict(fr[n]); x['SA_i']=float(sr[n]['SA_i']); rows.append(x)
    sa=[r['SA_i'] for r in rows]; sorted_rows=sorted(rows,key=lambda r:(r['SA_i'],r['sequence_name']))
    k=12; difficult=sorted_rows[:k]; cutoff=difficult[-1]['SA_i']; below=sum(x<cutoff for x in sa); at=sum(abs(x-cutoff)<1e-15 for x in sa)
    domains={c:{'n':sum(int(r[c])==1 for r in rows),'mean_SA':sum(r['SA_i'] for r in rows if int(r[c])==1)/sum(int(r[c])==1 for r in rows)} for c in CHALLENGES}
    sizes={s:{'n':sum(r['size_stratum']==s for r in rows),'mean_SA':sum(r['SA_i'] for r in rows if r['size_stratum']==s)/sum(r['size_stratum']==s for r in rows)} for s in SIZES}
    out={'schema_version':'KTES-P2A-POPULATION-OUTCOMES-v8.1','population_n':120,'primary_endpoint':'sequence-level State Accuracy','profile_mean_SA':sum(sa)/120,'median_SA':statistics.median(sa),'sd_SA_sample':statistics.stdev(sa),'quantiles':{'q05':qlinear(sa,.05),'q10':qlinear(sa,.10),'q25':qlinear(sa,.25),'q75':qlinear(sa,.75),'q90':qlinear(sa,.90),'q95':qlinear(sa,.95)},'challenge_domains':domains,'size_strata':sizes,'difficult_bottom_10pct':{'k':k,'cutoff_SA':cutoff,'n_strictly_below_cutoff':below,'n_equal_cutoff':at,'tie_at_cutoff':at>1,'members':[{'sequence_name':r['sequence_name'],'SA_i':r['SA_i'],'size_stratum':r['size_stratum'],'active_challenges':[c for c in CHALLENGES if int(r[c])==1]} for r in difficult]},'frame_sha256':sha256(a.frame),'sa_sha256':sha256(a.sa),'sampling_engine_used':False}
    a.json_out.parent.mkdir(parents=True,exist_ok=True); a.json_out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    lines=['# Phase 2A full-population outcome freeze v8','',f'**N:** 120 sequences  ','**Primary endpoint:** sequence-level Anti-UAV410 State Accuracy  ',f'**Population mean SA:** {out["profile_mean_SA"]:.6f}  ',f'**Median SA:** {out["median_SA"]:.6f}  ',f'**Sample SD:** {out["sd_SA_sample"]:.6f}  ','','## Frozen challenge-domain truths','', '| Domain | N | Mean SA |','|---|---:|---:|']
    for c in CHALLENGES: lines.append(f'| {c} | {domains[c]["n"]} | {domains[c]["mean_SA"]:.6f} |')
    lines += ['','## Frozen size-stratum truths','', '| Stratum | N | Mean SA |','|---|---:|---:|']
    for s in SIZES: lines.append(f'| {s} | {sizes[s]["n"]} | {sizes[s]["mean_SA"]:.6f} |')
    lines += ['','## Difficult-case set','',f'The pre-registered bottom 10% set contains 12 sequences. The 12th-order cutoff is SA={cutoff:.6f}; tie at cutoff: **{str(at>1).lower()}**.','', '| Rank | Sequence | SA | Size | Active challenges |','|---:|---|---:|---|---|']
    for i,r in enumerate(difficult,1): lines.append(f'| {i} | `{r["sequence_name"]}` | {r["SA_i"]:.6f} | {r["size_stratum"]} | {", ".join(c for c in CHALLENGES if int(r[c])==1) or "none"} |')
    lines += ['','This file freezes population truths only. No KTES, SRS, split-style sampling draw, inclusion probability, estimator, or design-UQ calculation is executed here.']
    a.md_out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'profile_mean_SA':out['profile_mean_SA'],'median_SA':out['median_SA'],'difficult_cutoff':cutoff,'tie_at_cutoff':at>1},indent=2))
if __name__=='__main__': main()
