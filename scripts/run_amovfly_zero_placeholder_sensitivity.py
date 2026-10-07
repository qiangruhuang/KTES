#!/usr/bin/env python3
"""Post-outcome AMOVFLY sensitivity using the immutable confirmatory design object.

The exact-(0,0) exclusion was defined after outcome access. This script therefore
cannot create a replacement confirmatory result. It reads the successful
confirmatory design object as immutable input, preserving its pi_i, certainty
sentinels, split comparator, seeds and guardrails, and changes only the diagnostic
outcome definition.
"""
from __future__ import annotations

import argparse,json,math,sys
from pathlib import Path
import numpy as np
import pandas as pd

import run_amovfly_external_validation as base
from audit_amovfly_waypoint_semantics import episode_rows


def load_frozen_design(frame_path:Path,design_path:Path,vendor:Path):
    if base.sha(frame_path)!=base.FRAME_SHA: raise RuntimeError('frozen frame hash mismatch')
    if base.sha(design_path)!=base.DESIGN_SHA: raise RuntimeError('frozen design-object hash mismatch')
    f=pd.read_csv(frame_path); obj=json.loads(design_path.read_text())
    if len(f)!=base.N or f.unit_id.duplicated().any(): raise RuntimeError('finite-population mismatch')
    if obj.get('outcome_values_opened') is not False or obj.get('status')!='FROZEN_PREOUTCOME_DESIGN': raise RuntimeError('design-object provenance mismatch')
    st=f.scenario.map(base.SMAP).to_numpy(int); p=np.full(base.N,1/base.N,float)
    kg=obj['kernel_geometry']; mu=np.asarray(kg['standardization_mu'],float); sd=np.asarray(kg['standardization_sd'],float)
    alt=f.altitude_parameter.to_numpy(float); alt_coord=np.where(np.isfinite(alt),alt,float(mu[8]))
    sc=np.column_stack([(f.scenario==s).astype(float) for s in base.STRATA]); uv=np.column_stack([(f.uav==u).astype(float) for u in base.UAVG])
    Xraw=np.column_stack([sc,uv,f.payload_parameter.to_numpy(float),alt_coord,f.altitude_parameter_available.astype(float).to_numpy(),f.speed_parameter.to_numpy(float),f.altitude_variable.astype(float).to_numpy(),f.speed_variable.astype(float).to_numpy()])
    Xs=(Xraw-mu)/sd
    sys.path.insert(0,str(vendor))
    from phase12r.kernel import rff_features
    from phase12r.active_designs import local_cube_sample
    from phase12r.r5_estimators import pwr_variance
    from phase12r.spread_estimators import gs_variance
    from phase12r.estimators import _satterthwaite
    phi=rff_features(Xs,float(kg['bandwidth']),n_features=int(kg['rff_n_features']),seed=int(obj['seed_lineage']['rff_seed']))
    cpi=np.asarray([obj['cpktes']['pi_by_unit_id'][str(u)] for u in f.unit_id],float)
    spi=np.asarray([obj['comparators']['split15_audit25']['pi_by_unit_id'][str(u)] for u in f.unit_id],float)
    cert=np.asarray(obj['cpktes']['sentinel_indices'],int); det=np.asarray(obj['comparators']['split15_audit25']['deterministic_indices'],int)
    aa=np.asarray(obj['comparators']['split15_audit25']['audit_allocation_n25'],int)
    if not np.allclose(cpi[cert],1.0): raise RuntimeError('frozen certainty pi mismatch')
    for g,ng in enumerate(base.ALLOC):
        if abs(cpi[st==g].sum()-ng)>1e-10: raise RuntimeError(f'frozen KTES pi stratum sum mismatch {g}')
    return f,st,p,Xs,phi,cpi,spi,cert,det,aa,obj,(local_cube_sample,pwr_variance,gs_variance,_satterthwaite)


def clean_outcomes(frame:pd.DataFrame,root:Path):
    rows=[]
    for _,r in frame.iterrows():
        ep=pd.DataFrame(episode_rows(root/str(r.canonical_ready_path),str(r.unit_id),str(r.scenario),str(r.uav)))
        ep=ep.loc[~ep.exact_zero_waypoint]
        if ep.empty: raise RuntimeError(f'all episodes exact zero: {r.unit_id}')
        d=ep.dmin_m.to_numpy(float)
        rows.append({'unit_id':r.unit_id,'scenario':r.scenario,'uav':r.uav,'Y10':float(np.mean(d<=10.0)),'F10':int(np.any(d>10.0)),'Y2':float(np.mean(d<=2.0)),'F2':int(np.any(d>2.0)),'n_waypoint_episodes':len(d),'n_no_position_episodes':int(np.sum(~np.isfinite(d)))})
    z=pd.DataFrame(rows)
    if z.unit_id.tolist()!=frame.unit_id.tolist(): raise RuntimeError('outcome order mismatch')
    return z


def sample_frozen(method,seed,f,st,Xs,phi,cpi,spi,cert,det,aa,local_cube):
    rng=np.random.default_rng(int(seed))
    if method=='Stratified-SRS':
        sel,pi=base.srs(st,base.ALLOC,rng); return sel,pi,sel,np.nan
    if method=='Split15+Audit25':
        eligible=np.ones(base.N,bool);eligible[det]=False;aud=[]
        for g,ng in enumerate(aa):
            pool=np.flatnonzero((st==g)&eligible);aud.extend(rng.choice(pool,size=int(ng),replace=False).tolist())
        aud=np.asarray(aud,int);return np.r_[det,aud],spi,aud,np.nan
    selected=cert.tolist(); bal=[]
    for g,ng in enumerate(base.ALLOC):
        pool_all=np.flatnonzero(st==g); c=np.intersect1d(pool_all,cert,assume_unique=False);nr=int(ng)-len(c);pool=np.setdiff1d(pool_all,cert,assume_unique=False)
        if nr==0: continue
        pi=cpi[pool]
        if abs(pi.sum()-nr)>1e-10: raise RuntimeError('frozen remainder pi sum mismatch')
        d=min(phi.shape[1],max(1,nr-2));Z=phi[pool,:d].copy();s=Z.std(0);s=np.where(s<1e-10,1,s);Z=(Z-Z.mean(0))/s;B=np.column_stack([np.ones(len(pool)),Z/pi[:,None]])
        loc=local_cube(pi,Xs[pool],B,rng)
        if len(loc)!=nr: raise RuntimeError('local cube size mismatch')
        selected.extend(pool[loc].tolist());bal.append(float(np.linalg.norm(((Z[loc]/pi[loc,None]).sum(0)-Z.sum(0))/len(pool))))
    sel=np.asarray(selected,int);prob=np.setdiff1d(sel,cert,assume_unique=False)
    if len(sel)!=40: raise RuntimeError('KTES size mismatch')
    return sel,cpi,prob,float(np.mean(bal))


def paired(a,b):
    d=np.asarray(a,float)-np.asarray(b,float);m=float(d.mean());se=float(d.std(ddof=1)/math.sqrt(len(d)));return {'mean_diff':m,'ci_lo':m-1.96*se,'ci_hi':m+1.96*se}


def replay(f,st,p,Xs,phi,cpi,spi,cert,det,aa,obj,eng,outcomes,out):
    local_cube,pwr,gs,satt=eng;y=outcomes.Y10.to_numpy(float);f10=outcomes.F10.to_numpy(float);y2=outcomes.Y2.to_numpy(float);order=np.lexsort((f.unit_id.astype(str).to_numpy(),y));difficult=set(order[:math.ceil(.10*base.N)].tolist());masks=[(f.scenario==s).to_numpy() for s in base.STRATA]+[(f.uav==u).to_numpy() for u in base.UAVG];rows=[];fails=[]
    for seed in base.SEEDS:
        for method in ['c-pKTES-Hedge','Stratified-SRS','Split15+Audit25']:
            try:
                sel,pi,prob,bal=sample_frozen(method,seed,f,st,Xs,phi,cpi,spi,cert,det,aa,local_cube);est,pe,cov,ess=base.profile(y,p,st,sel,pi,Xs,gs,pwr,satt);_,fe,fcov,_=base.profile(f10,p,st,sel,pi,Xs,gs,pwr,satt);_,p2,_,_=base.profile(y2,p,st,sel,pi,Xs,gs,pwr,satt);de=float(np.mean([base.domain_error(y,p,m,sel,pi) for m in masks]));w=p[prob]/pi[prob];pess=float(w.sum()**2/max(np.sum(w*w),1e-15));rows.append({'seed':int(seed),'method':method,'profile_estimate_Y10':est,'profile_error_Y10':pe,'failure_error_F10':fe,'critical_domain_error_Y10':de,'difficult_case_hit':int(any(int(i) in difficult for i in sel)),'ess_all':ess,'ess_probability_component':pess,'min_pi_selected':float(np.min(pi[sel])),'profile_uq_covered_Y10':cov,'failure_uq_covered_F10':fcov,'profile_error_Y2':p2,'balance_error':bal})
            except Exception as e:fails.append({'seed':int(seed),'method':method,'error':repr(e)})
    raw=pd.DataFrame(rows);rp=out/'amovfly_zero_placeholder_sensitivity_500_replay_raw_v8.csv';raw.to_csv(rp,index=False)
    if fails or len(raw)!=1500:(out/'amovfly_zero_placeholder_sensitivity_failures_v8.json').write_text(json.dumps(fails,indent=2)+'\n');raise RuntimeError(f'replay failures={len(fails)} rows={len(raw)}')
    ss=[]
    for m,d in raw.groupby('method'):ss.append({'method':m,'n_replays':len(d),'profile_error_Y10_mean':d.profile_error_Y10.mean(),'critical_domain_error_Y10_mean':d.critical_domain_error_Y10.mean(),'difficult_case_hit_rate':d.difficult_case_hit.mean(),'ess_probability_median':d.ess_probability_component.median(),'ess_probability_p05':d.ess_probability_component.quantile(.05),'profile_uq_coverage_Y10':d.profile_uq_covered_Y10.mean(),'failure_error_F10_mean':d.failure_error_F10.mean(),'failure_uq_coverage_F10':d.failure_uq_covered_F10.mean(),'profile_error_Y2_mean':d.profile_error_Y2.mean()})
    pd.DataFrame(ss).to_csv(out/'amovfly_zero_placeholder_sensitivity_summary_v8.csv',index=False)
    k=raw[raw.method=='c-pKTES-Hedge'].sort_values('seed');s=raw[raw.method=='Stratified-SRS'].sort_values('seed');b=raw[raw.method=='Split15+Audit25'].sort_values('seed');g3=paired(k.profile_error_Y10,s.profile_error_Y10);kd=float(k.critical_domain_error_Y10.mean());sd=float(s.critical_domain_error_Y10.mean());bd=float(b.critical_domain_error_Y10.mean());best=min(sd,bd);kh=float(k.difficult_case_hit.mean());bh=float(b.difficult_case_hit.mean());gates={'G1_positive_pi_no_sampling_failure':bool(np.all(k.min_pi_selected>0)),'G2_ESS':bool(k.ess_probability_component.median()>=18.5 and k.ess_probability_component.quantile(.05)>=12),'G3_profile_noninferiority':bool(g3['mean_diff']<=.01),'G4_critical_domain':bool(kd-best<=.02),'G5_difficult_hit':bool(kh-bh>=-.10)}
    res={'schema_version':'KTES-AMOVFLY-ZERO-PLACEHOLDER-SENSITIVITY-v8.2','classification':'POST_OUTCOME_SENSITIVITY_ONLY','confirmatory_result_replaced':False,'frozen_design_object_sha256':base.DESIGN_SHA,'frame_sha256':base.FRAME_SHA,'sampling_note':'Exact frozen pi/sentinels/split adapter loaded from successful confirmatory artifact; Local Cube randomization replayed under the same algorithm and seed block.','population_truth':{'N':base.N,'Y10_mean':float(outcomes.Y10.mean()),'F10_rate':float(outcomes.F10.mean()),'Y2_mean':float(outcomes.Y2.mean()),'F2_rate':float(outcomes.F2.mean()),'difficult_n':len(difficult)},'gates_under_sensitivity_definition':gates,'all_five_sensitivity_gates_pass':bool(all(gates.values())),'G3_paired':g3,'G4':{'ktes':kd,'srs':sd,'split15':bd,'better_comparator':best,'ktes_minus_better':kd-best},'G5':{'ktes':kh,'split15':bh,'difference':kh-bh},'raw_replay_sha256':base.sha(rp),'interpretation':'Diagnostic robustness analysis only; cannot replace the frozen confirmatory endpoint.'};(out/'AMOVFLY_ZERO_PLACEHOLDER_SENSITIVITY_v8.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
    md=f"""# AMOVFLY exact-zero waypoint sensitivity v8\n\n**Classification:** **POST-OUTCOME SENSITIVITY ONLY**  \n**Confirmatory result:** unchanged\n\nThe successful confirmatory design object (SHA `{base.DESIGN_SHA}`) is read as immutable input. The exact `(0,0)` exclusion changes only the diagnostic outcome definition.\n\n## Diagnostic population\n\n- mean `Y10`: **{res['population_truth']['Y10_mean']:.9f}**\n- `F10` rate: **{res['population_truth']['F10_rate']:.9f}**\n- mean `Y2`: **{res['population_truth']['Y2_mean']:.9f}**\n\n## Frozen-design replay sensitivity\n\n| Quantity | Result |\n|---|---:|\n| KTES−SRS profile-error mean difference | {g3['mean_diff']:.9f} |\n| 95% CI | [{g3['ci_lo']:.9f}, {g3['ci_hi']:.9f}] |\n| KTES critical-domain error | {kd:.9f} |\n| SRS critical-domain error | {sd:.9f} |\n| Split15 critical-domain error | {bd:.9f} |\n| KTES−better-comparator domain error | {kd-best:.9f} |\n| KTES difficult-case hit | {kh:.6f} |\n| Split15 difficult-case hit | {bh:.6f} |\n| All five numerical gates | {'PASS' if all(gates.values()) else 'FAIL'} |\n\n## Interpretation\n\nThis sensitivity was specified after telemetry outcome access. It tests robustness of the method comparison to the identified placeholder, but it is not a repaired confirmatory endpoint and must not replace the original AMOVFLY result.\n""";(out/'AMOVFLY_ZERO_PLACEHOLDER_SENSITIVITY_v8.md').write_text(md);print(json.dumps(res,indent=2,sort_keys=True))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--frame',type=Path,required=True);ap.add_argument('--frozen-design',type=Path,required=True);ap.add_argument('--source-root',type=Path,required=True);ap.add_argument('--vendor-src',type=Path,default=Path('vendor/r5_engine_recovered_v8/src'));ap.add_argument('--out',type=Path,default=Path('outputs/amovfly_zero_sensitivity'));a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);f,st,p,Xs,phi,cpi,spi,cert,det,aa,obj,eng=load_frozen_design(a.frame,a.frozen_design,a.vendor_src);z=clean_outcomes(f,a.source_root);z.to_csv(a.out/'amovfly_zero_placeholder_sensitivity_outcomes_v8.csv',index=False);replay(f,st,p,Xs,phi,cpi,spi,cert,det,aa,obj,eng,z,a.out)
if __name__=='__main__':main()
