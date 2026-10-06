#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import t
from phase12r.active_designs import kernel_novelty
from phase12r.kernel import median_bandwidth, rbf_cross, rff_features, standardize
from phase12r.r5_designs import certainty_portfolio_blended_pps_local_cube
from phase12r.r5_estimators import pwr_variance
from phase12r.spread_estimators import gs_variance
from phase12r.estimators import _satterthwaite

N=120; LIVE=40; SEEDS=np.arange(20261001,20261501,dtype=int)
BASE=20261115; RFF=BASE+55; NOV=BASE+77
RHO=.20; LAM=3.; MINF=.35; PORT='NRR'
KFEAT=['TC','OV','SV','FM','OC','DBC','Tiny','Small','Medium','Normal','log_length_ln']
AFEAT=['TC','OV','SV','FM','OC','DBC','Tiny','Small']; DOM=['TC','OV','SV','FM','OC','DBC']
STRATA=['Tiny','Small','Medium','Normal']; SMAP={s:i for i,s in enumerate(STRATA)}

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def largest(counts,total,min_per=2):
    c=np.asarray(counts,int); base=np.where(c>0,np.minimum(min_per,c),0)
    if base.sum()>total: raise ValueError('minimum allocation exceeds total')
    rem=total-int(base.sum()); cap=c-base
    if rem>cap.sum(): raise ValueError('requested sample exceeds population')
    if rem==0:return base
    q=rem*cap/cap.sum(); ex=np.floor(q).astype(int); left=rem-int(ex.sum())
    order=np.lexsort((np.arange(len(c)),-(q-ex)))
    for g in order[:left]: ex[g]+=1
    out=base+ex
    if out.sum()!=total or np.any(out>c): raise RuntimeError('allocation construction failed')
    return out

def srs(strata,alloc,rng,eligible=None):
    if eligible is None: eligible=np.ones(len(strata),bool)
    sel=[]; pi=np.zeros(len(strata),float)
    for g,ng in enumerate(np.asarray(alloc,int)):
        pool=np.flatnonzero((strata==g)&eligible)
        if ng>len(pool): raise RuntimeError(f'stratum {g}: allocation exceeds eligible pool')
        if ng:
            pi[pool]=ng/len(pool); sel.extend(rng.choice(pool,size=ng,replace=False).tolist())
    return np.asarray(sel,int),pi

def split15(Xs,strata,h):
    sel=[]
    def pick(pool,k):
        nonlocal sel
        pool=np.setdiff1d(np.asarray(pool,int),np.asarray(sel,int),assume_unique=False)
        for _ in range(k):
            if not len(pool): break
            if not sel: score=np.linalg.norm(Xs[pool]-Xs[pool].mean(0),axis=1)
            else: score=1-rbf_cross(Xs[pool],Xs[np.asarray(sel)],h).mean(1)
            i=int(pool[np.argmax(score)]); sel.append(i); pool=pool[pool!=i]
    for g in range(4): pick(np.flatnonzero(strata==g),3)
    pick(np.arange(len(strata)),3)
    out=np.asarray(sel,int)
    if len(out)!=15 or len(np.unique(out))!=15: raise RuntimeError('split deterministic size failure')
    return out

def load_frame(path):
    f=pd.read_csv(path)
    if len(f)!=N or f.sequence_name.duplicated().any(): raise ValueError('bad frozen frame identity')
    miss=[c for c in KFEAT+AFEAT+['size_stratum','frozen_aux_risk'] if c not in f.columns]
    if miss: raise ValueError(f'missing frame columns: {miss}')
    st=f.size_stratum.map(SMAP).to_numpy()
    if np.any(pd.isna(st)): raise ValueError('unmapped stratum')
    st=st.astype(int); counts=np.bincount(st,minlength=4); alloc=largest(counts,40,2)
    if tuple(counts)!=(33,54,29,4) or tuple(alloc)!=(11,17,10,2): raise ValueError('frozen strata/allocation mismatch')
    Xraw=f[KFEAT].to_numpy(float); Xs,_,_=standardize(Xraw); h=median_bandwidth(Xs,seed=BASE)
    phi=rff_features(Xs,h,n_features=8,seed=RFF); p=np.full(N,1/N,float)
    nov=kernel_novelty(Xs,p,h,seed=NOV); Xadv=f[AFEAT].to_numpy(float); risk=f.frozen_aux_risk.to_numpy(float)
    return f,st,counts,alloc,Xs,Xadv,p,h,phi,nov,risk

def design(frame_path):
    f,st,counts,alloc,Xs,Xadv,p,h,phi,nov,risk=load_frame(frame_path)
    sel,pi,_,cert,_=certainty_portfolio_blended_pps_local_cube(Xs,phi,Xadv,p,st,alloc,nov,risk,PORT,np.random.default_rng(int(SEEDS[0])),rho=RHO,lam=LAM,min_fraction=MINF)
    if len(cert)!=3 or len(sel)!=LIVE or np.any(pi<=0) or abs(pi.sum()-LIVE)>1e-8: raise RuntimeError('c-pKTES design contract failure')
    non=np.setdiff1d(np.arange(N),cert)
    det=split15(Xs,st,h); eligible=np.ones(N,bool); eligible[det]=False
    rem=np.array([np.sum((st==g)&eligible) for g in range(4)],int); aa=largest(rem,25,2)
    pis=np.zeros(N); pis[det]=1
    for g,ng in enumerate(aa):
        pool=np.flatnonzero((st==g)&eligible); pis[pool]=ng/len(pool)
    obj={'schema_version':'KTES-P2A-DESIGN-OBJECT-v8.4','finite_population_n':N,'live_n':LIVE,
         'frozen_protocol':'KTES_Phase2_External_Validation_Protocol_v1.0','replay_seed_block':[int(SEEDS[0]),int(SEEDS[-1])],
         'kernel_features':KFEAT,'adverse_features':AFEAT,'strata_order':STRATA,'stratum_counts':counts.tolist(),'allocation_n40':alloc.tolist(),'bandwidth':float(h),'rff_n_features':8,
         'seed_lineage':{'historical_base_r5_seed':BASE,'rff_seed':RFF,'novelty_seed':NOV},
         'cpktes_immutable':{'portfolio':PORT,'rho':RHO,'lambda':LAM,'min_probability_fraction':MINF,'certainty_n':3,'probability_remainder_n':37},
         'sentinel_indices':[int(x) for x in cert],'sentinel_sequences':f.iloc[cert].sequence_name.tolist(),
         'capped_non_sentinel_pi1_indices':[int(x) for x in non[np.isclose(pi[non],1.,atol=1e-12)]],
         'capped_non_sentinel_pi1_sequences':f.iloc[non[np.isclose(pi[non],1.,atol=1e-12)]].sequence_name.tolist(),
         'cpktes_pi_by_sequence':{str(r.sequence_name):float(pi[i]) for i,r in f.iterrows()},
         'split_deterministic_indices':[int(x) for x in det],'split_deterministic_sequences':f.iloc[det].sequence_name.tolist(),'split_audit_allocation_n25':aa.tolist(),
         'split_pi_by_sequence':{str(r.sequence_name):float(pis[i]) for i,r in f.iterrows()},
         'external_adapter_mapping':{'split15':'Historical deterministic_ktes15 3x4+3 geometry rule mapped outcome-blind to the four Phase2A size strata; 25 audit units use largest-remainder allocation with minimum 2 over the remaining population. This numerical adapter was instantiated after SA_i recovery but before replay results; it is an execution clarification, not pristine preregistration.'},
         'outcome_fields_read_for_design':[]}
    return obj

def load_y(path,f):
    s=pd.read_csv(path)
    if len(s)!=N or s.sequence_name.duplicated().any(): raise ValueError('bad SA artifact')
    m=f[['sequence_name']].merge(s[['sequence_name','SA_i']],on='sequence_name',how='left',validate='one_to_one')
    if m.SA_i.isna().any(): raise ValueError('missing SA_i')
    return m.SA_i.to_numpy(float)

def profile(p,st,sel,y,pi,coords):
    masses=[]; ests=[]; vars=[]; esses=[]
    for g in range(4):
        pool=np.flatnonzero(st==g); sg=sel[st[sel]==g]
        if len(sg)==0: raise RuntimeError(f'no selected unit in stratum {g}')
        mass=float(p[pool].sum()); pcs=p[sg]/mass; q=pi[sg]; w=pcs/q; den=float(w.sum()); est=float(np.sum(w*y[sg])/den); r=y[sg]-est
        vg=gs_variance(r,q,pcs,coords[sg])/(den*den); vp=pwr_variance(r,q,pcs)/(den*den)
        masses.append(mass);ests.append(est);vars.append(max(vg if np.isfinite(vg) else 0.,vp));esses.append(den*den/max(np.sum(w*w),1e-15))
    ma=np.asarray(masses); va=np.asarray(vars); ea=np.asarray(esses); est=float(ma@np.asarray(ests)); truth=float(p@y)
    comp=ma*ma*va; se=float(np.sqrt(comp.sum())); df=_satterthwaite(comp,np.maximum(1.,ea-1)); q=t.ppf(.975,df)
    wg=p[sel]/pi[sel]
    return est,abs(est-truth),int(abs(est-truth)<=q*se),float(wg.sum()**2/max(np.sum(wg*wg),1e-15)),float(np.min(pi[sel])),float(np.max(wg/wg.sum()))

def domain_stats(p,mask,sel,y,pi,coords):
    pool=np.flatnonzero(mask); mass=float(p[pool].sum()); truth=float(np.sum(p[pool]*y[pool])/mass); sg=sel[mask[sel]]
    if len(sg)==0: return 0.,truth,0,0.
    pc=p[sg]/mass; q=pi[sg]; est=float(np.sum(pc*y[sg]/q)); w=pc/q; ess=float(w.sum()**2/max(np.sum(w*w),1e-15))
    if len(sg)<2:return est,truth,int(math.isclose(est,truth,rel_tol=0,abs_tol=1e-15)),ess
    vg=gs_variance(y[sg],q,pc,coords[sg]); vp=pwr_variance(y[sg],q,pc); var=max(vg if np.isfinite(vg) else 0.,vp); tq=t.ppf(.975,max(1.,ess-1))
    return est,truth,int(abs(est-truth)<=tq*math.sqrt(max(var,0.))),ess

def subset_ess(p,idx,pi):
    w=p[idx]/pi[idx]; return float(w.sum()**2/max(np.sum(w*w),1e-15)) if len(idx) else 0.

def sample(method,seed,f,st,alloc,Xs,Xadv,p,phi,nov,risk,obj):
    rng=np.random.default_rng(int(seed))
    if method=='c-pKTES-Hedge':
        sel,pi,bal,cert,_=certainty_portfolio_blended_pps_local_cube(Xs,phi,Xadv,p,st,alloc,nov,risk,PORT,rng,rho=RHO,lam=LAM,min_fraction=MINF)
        if not np.array_equal(np.sort(cert),np.sort(np.asarray(obj['sentinel_indices'],int))): raise RuntimeError('sentinel identity changed')
        rem=np.setdiff1d(sel,cert,assume_unique=False)
        if len(sel)!=40 or len(np.unique(sel))!=40 or len(rem)!=37 or np.any(pi<=0): raise RuntimeError('c-pKTES sampling contract failure')
        return sel,pi,float(bal),rem
    if method=='Stratified-SRS':
        sel,pi=srs(st,alloc,rng); return sel,pi,np.nan,sel
    det=np.asarray(obj['split_deterministic_indices'],int); elig=np.ones(N,bool); elig[det]=False; aa=np.asarray(obj['split_audit_allocation_n25'],int); aud,_=srs(st,aa,rng,elig)
    pi=np.asarray([float(obj['split_pi_by_sequence'][str(n)]) for n in f.sequence_name]); sel=np.r_[det,aud]
    if len(sel)!=40 or len(np.unique(sel))!=40 or np.any(pi<=0): raise RuntimeError('split sampling contract failure')
    return sel,pi,np.nan,aud

def method_row(method,seed,f,st,alloc,Xs,Xadv,p,phi,nov,risk,obj,y,diff):
    sel,pi,bal,prob=sample(method,seed,f,st,alloc,Xs,Xadv,p,phi,nov,risk,obj)
    pe,p_err,cov,ess,mp,mw=profile(p,st,sel,y,pi,Xs); de=[];dc=[]
    for c in DOM:
        e,tr,cv,es=domain_stats(p,f[c].to_numpy(int).astype(bool),sel,y,pi,Xs); de.append(abs(e-tr));dc.append(cv)
    return {'seed':int(seed),'method':method,'n_selected':len(sel),'profile_estimate':pe,'profile_error':p_err,'critical_domain_error':float(np.mean(de)),'difficult_case_hit':int(any(int(i) in diff for i in sel)),'ess_all':ess,'ess_probability_component':subset_ess(p,prob,pi),'probability_component_n':len(prob),'min_pi_selected':mp,'max_normalized_weight':mw,'profile_uq_covered':cov,'domain_uq_coverage_mean':float(np.mean(dc)),'balance_error':bal}

def pair(a,b):
    d=np.asarray(a,float)-np.asarray(b,float); m=float(d.mean()); se=float(d.std(ddof=1)/math.sqrt(len(d))); return {'n':len(d),'mean_diff':m,'ci_lo':m-1.96*se,'ci_hi':m+1.96*se,'median_diff':float(np.median(d))}

def evaluate(frame_path,sa_path,design_path,out):
    out.mkdir(parents=True,exist_ok=True); f,st,_,alloc,Xs,Xadv,p,_,phi,nov,risk=load_frame(frame_path); y=load_y(sa_path,f)
    order=np.argsort(y,kind='mergesort'); cutoff=float(y[order[11]])
    if math.isclose(float(y[order[12]]),cutoff,rel_tol=0,abs_tol=1e-15): raise RuntimeError('bottom10 cutoff tie')
    diff={int(x) for x in order[:12]}; obj=json.loads(design_path.read_text()); sent=np.asarray(obj['sentinel_indices'],int); non=np.setdiff1d(np.arange(N),sent)
    pik=np.asarray([float(obj['cpktes_pi_by_sequence'][str(n)]) for n in f.sequence_name]); rows=[]; failures=[]
    for seed in SEEDS:
        for m in ['c-pKTES-Hedge','Stratified-SRS','Split15+Audit25']:
            try: rows.append(method_row(m,seed,f,st,alloc,Xs,Xadv,p,phi,nov,risk,obj,y,diff))
            except Exception as e: failures.append({'seed':int(seed),'method':m,'error':repr(e)})
    raw=pd.DataFrame(rows).sort_values(['seed','method']).reset_index(drop=True); raw.to_csv(out/'phase2a_500_replay_raw_v8.csv',index=False)
    if len(raw)!=1500:
        (out/'phase2a_replay_failures_v8.json').write_text(json.dumps(failures,indent=2)+'\n'); raise RuntimeError(f'replay rows {len(raw)} != 1500')
    ss=[]
    for m,d in raw.groupby('method'):
        ss.append({'method':m,'n_replays':len(d),'profile_error_mean':d.profile_error.mean(),'profile_error_median':d.profile_error.median(),'critical_domain_error_mean':d.critical_domain_error.mean(),'critical_domain_error_median':d.critical_domain_error.median(),'difficult_case_hit_rate':d.difficult_case_hit.mean(),'ess_all_median':d.ess_all.median(),'ess_all_p05':d.ess_all.quantile(.05),'ess_probability_component_median':d.ess_probability_component.median(),'ess_probability_component_p05':d.ess_probability_component.quantile(.05),'probability_component_n':int(d.probability_component_n.iloc[0]),'min_pi_selected_min':d.min_pi_selected.min(),'max_normalized_weight_p95':d.max_normalized_weight.quantile(.95),'profile_uq_coverage':d.profile_uq_covered.mean(),'domain_uq_coverage_mean':d.domain_uq_coverage_mean.mean()})
    sm=pd.DataFrame(ss).sort_values('method'); sm.to_csv(out/'phase2a_500_replay_summary_v8.csv',index=False); piv={m:raw[raw.method==m].sort_values('seed').reset_index(drop=True) for m in raw.method.unique()}; prs=[]
    for metric in ['profile_error','critical_domain_error','difficult_case_hit','ess_probability_component']:
        for comp in ['Stratified-SRS','Split15+Audit25']: prs.append({'comparison':f'c-pKTES-Hedge - {comp}','metric':metric,**pair(piv['c-pKTES-Hedge'][metric],piv[comp][metric])})
    pdx=pd.DataFrame(prs); pdx.to_csv(out/'phase2a_500_replay_paired_v8.csv',index=False); s=sm.set_index('method'); k=s.loc['c-pKTES-Hedge']; better=min([('Stratified-SRS',s.loc['Stratified-SRS','critical_domain_error_mean']),('Split15+Audit25',s.loc['Split15+Audit25','critical_domain_error_mean'])],key=lambda x:x[1]); pdiff=float(k.profile_error_mean-s.loc['Stratified-SRS','profile_error_mean']); cdiff=float(k.critical_domain_error_mean-better[1]); hdiff=float(k.difficult_case_hit_rate-s.loc['Split15+Audit25','difficult_case_hit_rate'])
    G={'positive_pi_and_no_sampling_failure':{'value':len(failures)==0 and bool(np.all(pik[non]>0)),'pass':len(failures)==0 and bool(np.all(pik[non]>0))},'ktes_probability_remainder_ess_median_ge_18_5':{'value':float(k.ess_probability_component_median),'threshold':18.5,'pass':bool(k.ess_probability_component_median>=18.5)},'ktes_probability_remainder_ess_p05_ge_12':{'value':float(k.ess_probability_component_p05),'threshold':12.,'pass':bool(k.ess_probability_component_p05>=12)},'profile_error_not_worse_than_srs_by_gt_0_01':{'ktes_minus_srs':pdiff,'threshold_max':.01,'pass':pdiff<=.01},'critical_domain_error_not_worse_than_better_baseline_by_gt_0_02':{'better_baseline':better[0],'ktes_minus_better':cdiff,'threshold_max':.02,'pass':cdiff<=.02,'preregistration_note':'Comparator-sensitive: split adapter clarified after SA_i recovery.'},'difficult_hit_not_below_split_by_gt_0_10':{'ktes_minus_split':hdiff,'threshold_min':-.10,'pass':hdiff>=-.10,'preregistration_note':'Comparator-sensitive: split adapter clarified after SA_i recovery.'}}
    ok=all(v['pass'] for v in G.values()); truths={c:float(y[f[c].to_numpy(int).astype(bool)].mean()) for c in DOM}; gate={'schema_version':'KTES-P2A-RESULT-GATE-v8.4','status':'PASS_WITH_EXECUTION_CLARIFICATION' if ok else 'FAIL','all_numeric_guardrails_pass':ok,'design_object_sha256':sha(design_path),'frame_sha256':sha(frame_path),'sa_sha256':sha(sa_path),'truth_profile_mean_SA':float(p@y),'bottom10_cutoff_SA':cutoff,'bottom10_n':12,'challenge_domain_truths':truths,'critical_domain_estimator':'Horvitz-Thompson finite-domain mean with known outcome-blind domain denominator','replays':500,'guardrails':G,'split_adapter_note':obj['external_adapter_mapping']['split15'],'interpretation':'Frozen c-pKTES and SRS are evaluated without outcome-driven retuning. Split-dependent guardrails use a disclosed post-SA_i execution clarification and are not a pristine preregistered comparison.'}
    (out/'phase2a_result_gate_v8.json').write_text(json.dumps(gate,indent=2,sort_keys=True)+'\n'); lines=['# Phase 2A 500-paired-replay result v8','',f"**Gate status:** **{gate['status']}**",'','## Method summaries','',sm.to_markdown(index=False),'','## Paired comparisons','',pdx.to_markdown(index=False),'','## Frozen guardrails','']+[f"- `{q}`: **{'PASS' if v['pass'] else 'FAIL'}** — {json.dumps(v,ensure_ascii=False)}" for q,v in G.items()]+['','## Execution-order disclosure','',obj['external_adapter_mapping']['split15'],'','The c-pKTES constants, endpoint, frame covariates, strata, allocation and guardrail thresholds were not retuned after outcome recovery.','', '## Interpretation boundary','','This gate evaluates structural transfer of the frozen probability-preserving sampling logic on a real task-effectiveness benchmark. It does not establish live-weapon validity, deployment-frequency representativeness, or mission-level safety certification.']
    (out/'PHASE2A_500_REPLAY_RESULT_v8.md').write_text('\n'.join(lines)+'\n'); print(sm.to_string(index=False)); print('\nGATE',gate['status']);print(json.dumps(G,indent=2))

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True); a=sub.add_parser('freeze');a.add_argument('--frame',type=Path,required=True);a.add_argument('--output',type=Path,required=True);a=sub.add_parser('evaluate');a.add_argument('--frame',type=Path,required=True);a.add_argument('--sa',type=Path,required=True);a.add_argument('--design',type=Path,required=True);a.add_argument('--out-dir',type=Path,required=True);x=ap.parse_args()
    if x.cmd=='freeze':
        o=design(x.frame);x.output.parent.mkdir(parents=True,exist_ok=True);x.output.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n');print(json.dumps({'sha256':sha(x.output),'sentinel_sequences':o['sentinel_sequences'],'capped_non_sentinel_pi1_sequences':o['capped_non_sentinel_pi1_sequences'],'split_audit_allocation_n25':o['split_audit_allocation_n25']},indent=2))
    else:evaluate(x.frame,x.sa,x.design,x.out_dir)
if __name__=='__main__':main()
