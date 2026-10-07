#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,math,sys
from pathlib import Path
import numpy as np,pandas as pd
from scipy.stats import t
N=257;STRATA=['FAFS','FAVS','VAFS','VAVS'];UAVG=['G','R','Y'];SMAP={s:i for i,s in enumerate(STRATA)}
ALLOC=np.array([6,23,6,5],int);SEEDS=np.arange(20261001,20261501,dtype=int)
BASE=20261115;RFF=20261170;NOV=20261192;RHO=.20;LAM=3.;MINF=.35;PORT='NRR'
FRAME_SHA='92a6d63eb75a0eee58e9d310da9b140517e2dffd2c6f48986fd21b40c8b12c85';DESIGN_SHA='a5b241f9d17be696652f30968bb1b8a0d2138087674ac371866b606e8362696b';ART_DIGEST='8c88b8b39f1360d48f3c1864f52e8292066bf7f21f9ac5c1e8e16c07fe669d47'
REQ=['real_lat','real_long','aim_lat','aim_long'];EARTH=6371008.8

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def largest(counts,total,min_per=2):
 c=np.asarray(counts,int);base=np.where(c>0,np.minimum(min_per,c),0);rem=total-int(base.sum());cap=c-base;q=rem*cap/cap.sum();ex=np.floor(q).astype(int);left=rem-int(ex.sum());order=np.lexsort((np.arange(len(c)),-(q-ex)))
 for g in order[:left]:ex[g]+=1
 out=base+ex
 if out.sum()!=total or np.any(out>c):raise RuntimeError('allocation failure')
 return out

def load_engine(vendor):
 sys.path.insert(0,str(vendor));from phase12r.active_designs import kernel_novelty;from phase12r.kernel import standardize,median_bandwidth,rff_features,rbf_cross;from phase12r.r5_designs import certainty_portfolio_blended_pps_local_cube;from phase12r.r5_estimators import pwr_variance;from phase12r.spread_estimators import gs_variance;from phase12r.estimators import _satterthwaite
 return kernel_novelty,standardize,median_bandwidth,rff_features,rbf_cross,certainty_portfolio_blended_pps_local_cube,pwr_variance,gs_variance,_satterthwaite

def split15(Xs,st,h,rbf_cross):
 sel=[]
 def pick(pool,k):
  nonlocal sel;pool=np.setdiff1d(np.asarray(pool,int),np.asarray(sel,int),assume_unique=False)
  for _ in range(k):
   if not len(pool):break
   score=np.linalg.norm(Xs[pool]-Xs[pool].mean(0),axis=1) if not sel else 1-rbf_cross(Xs[pool],Xs[np.asarray(sel)],h).mean(1);i=int(pool[np.argmax(score)]);sel.append(i);pool=pool[pool!=i]
 for g in range(4):pick(np.flatnonzero(st==g),3)
 pick(np.arange(len(st)),3);out=np.asarray(sel,int)
 if len(out)!=15 or len(np.unique(out))!=15:raise RuntimeError('split15 failure')
 return out

def prepare_design(frame,vendor,out):
 eng=load_engine(vendor);kernel_novelty,standardize,median_bandwidth,rff_features,rbf_cross,cpktes,*_=eng;f=pd.read_csv(frame)
 if len(f)!=N or f.unit_id.duplicated().any() or sha(frame)!=FRAME_SHA:raise RuntimeError('frozen frame identity mismatch')
 st=f.scenario.map(SMAP).to_numpy(int);counts=np.bincount(st,minlength=4)
 if tuple(counts)!=(33,165,32,27) or not np.array_equal(ALLOC,largest(counts,40,2)):raise RuntimeError('strata/allocation mismatch')
 sc=np.column_stack([(f.scenario==s).astype(float) for s in STRATA]);uv=np.column_stack([(f.uav==u).astype(float) for u in UAVG]);alt=f.altitude_parameter.to_numpy(float);obs=alt[np.isfinite(alt)];alt_center=float(obs.mean());alt_coord=np.where(np.isfinite(alt),alt,alt_center)
 Xraw=np.column_stack([sc,uv,f.payload_parameter.to_numpy(float),alt_coord,f.altitude_parameter_available.astype(float).to_numpy(),f.speed_parameter.to_numpy(float),f.altitude_variable.astype(float).to_numpy(),f.speed_variable.astype(float).to_numpy()]);kcols=[f'scenario_{s}' for s in STRATA]+[f'uav_{u}' for u in UAVG]+['payload_parameter','altitude_parameter_centerfill','altitude_parameter_available','speed_parameter','altitude_variable','speed_variable']
 Xs,mu,sd=standardize(Xraw);Xadv=f[['payload_severity','altitude_variable','speed_variable']].astype(float).to_numpy();p=np.full(N,1/N,float);h=median_bandwidth(Xs,seed=BASE);phi=rff_features(Xs,h,n_features=8,seed=RFF);nov=kernel_novelty(Xs,p,h,seed=NOV);risk=f.frozen_aux_risk.to_numpy(float)
 sel,pi,bal,cert,_=cpktes(Xs,phi,Xadv,p,st,ALLOC,nov,risk,PORT,np.random.default_rng(int(SEEDS[0])),rho=RHO,lam=LAM,min_fraction=MINF);det=split15(Xs,st,h,rbf_cross);elig=np.ones(N,bool);elig[det]=False;rem=np.array([np.sum((st==g)&elig) for g in range(4)]);aa=largest(rem,25,2);spi=np.zeros(N);spi[det]=1
 for g,ng in enumerate(aa):
  pool=np.flatnonzero((st==g)&elig);spi[pool]=ng/len(pool)
 src=vendor/'phase12r';obj={'schema_version':'KTES-AMOVFLY-DESIGN-OBJECT-v8.1','status':'FROZEN_PREOUTCOME_DESIGN','outcome_values_opened':False,'source':{'repository':'YujiaoHu/AMOVFLY-Dataset','commit':'67069ed00ddbebd62b71aa9bb1272415e9b15ff8','frame_sha256':FRAME_SHA,'ci_artifact_digest_sha256':ART_DIGEST,'population_n':N},'finite_population':{'unit':'one unique ready-data Git blob in autonomous scenarios; byte-identical aliases collapsed','excluded':['Random manual-control scenario','Multi-UAV records without frozen one-flight-one-outcome map'],'equal_profile_weight':1/N},'strata_order':STRATA,'stratum_counts':counts.tolist(),'allocation_n40':ALLOC.tolist(),'kernel_geometry':{'columns':kcols,'altitude_structural_missing_rule':f'center-fill using outcome-blind available-altitude mean {alt_center:.15g} plus availability indicator; no telemetry imputation','standardize_function':'recovered R5 phase12r.kernel.standardize','standardization_mu':[float(x) for x in mu],'standardization_sd':[float(x) for x in sd],'bandwidth':float(h),'rff_n_features':8},'seed_lineage':{'historical_base_r5_seed':BASE,'rff_seed':RFF,'novelty_anchor_seed':NOV,'replay_seed_block':[int(SEEDS[0]),int(SEEDS[-1])]},'adverse_tail':{'columns':['payload_severity','altitude_variable','speed_variable'],'compound_rule':'recovered R5 product of top-3 weighted marginal adverse quantiles'},'auxiliary_risk':{'column':'frozen_aux_risk','formula':'0.5*variability_severity + 0.5*payload_severity'},'cpktes':{'portfolio':PORT,'rho':RHO,'lambda':LAM,'min_probability_fraction':MINF,'certainty_n':3,'probability_remainder_n':37,'sentinel_indices':[int(x) for x in cert],'sentinel_unit_ids':f.iloc[cert].unit_id.tolist(),'sentinel_paths':f.iloc[cert].canonical_ready_path.tolist(),'pi_by_unit_id':{str(f.iloc[i].unit_id):float(pi[i]) for i in range(N)},'design_example_seed':int(SEEDS[0]),'design_example_selected_unit_ids':f.iloc[sel].unit_id.tolist(),'design_example_balance_error':float(bal)},'comparators':{'stratified_srs':{'allocation':ALLOC.tolist()},'split15_audit25':{'status':'FROZEN_PREOUTCOME_ADAPTER','deterministic_rule':'Phase2A inherited 3 per stratum maximin/kernel-geometry + 3 global maximin/kernel-geometry','deterministic_indices':[int(x) for x in det],'deterministic_unit_ids':f.iloc[det].unit_id.tolist(),'audit_allocation_n25':aa.tolist(),'pi_by_unit_id':{str(f.iloc[i].unit_id):float(spi[i]) for i in range(N)}}},'design_side_replay_audit':{'n_replays':500,'sampling_failures':0,'probability_remainder_ess_median':35.22443572573489,'probability_remainder_ess_p05':34.99299027627282,'minimum_selected_positive_pi':0.0973081911914407,'maximum_selected_pi':0.2553116790583898,'balance_error_median':0.27273353717800797},'source_code_sha256':{'r5_designs.py':sha(src/'r5_designs.py'),'active_designs.py':sha(src/'active_designs.py'),'kernel.py':sha(src/'kernel.py')}}
 dp=out/'AMOVFLY_DESIGN_OBJECT_REBUILT_v8.json';dp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
 if sha(dp)!=DESIGN_SHA:raise RuntimeError(f'design object hash mismatch {sha(dp)} != {DESIGN_SHA}')
 return f,st,p,Xs,Xadv,phi,nov,risk,obj,eng

def schema_gate(f,root,out):
 rows=[];bad=[]
 for _,r in f.iterrows():
  p=root/str(r.canonical_ready_path)
  if not p.is_file():bad.append((r.unit_id,'missing_file',str(p)));continue
  try:cols=[str(c).strip() for c in pd.read_csv(p,nrows=0).columns]
  except Exception as e:bad.append((r.unit_id,'header_read',repr(e)));continue
  miss=[c for c in REQ if c not in cols];rows.append({'unit_id':r.unit_id,'path':r.canonical_ready_path,'n_columns':len(cols),'required_present':not miss,'missing_required':'|'.join(miss)})
  if miss:bad.append((r.unit_id,'missing_columns','|'.join(miss)))
 pd.DataFrame(rows).to_csv(out/'amovfly_outcome_schema_audit_v8.csv',index=False);(out/'amovfly_outcome_schema_failures_v8.json').write_text(json.dumps(bad,indent=2)+'\n')
 if bad:raise RuntimeError(f'OUTCOME_SCHEMA_GATE_FAIL n={len(bad)}; no telemetry values opened')

def hav(lat,lon,alat,alon):
 lat=np.radians(lat);lon=np.radians(lon);a1=math.radians(alat);a2=math.radians(alon);dlat=lat-a1;dlon=lon-a2;a=np.sin(dlat/2)**2+np.cos(lat)*math.cos(a1)*np.sin(dlon/2)**2;return 2*EARTH*np.arcsin(np.sqrt(np.clip(a,0,1)))
def flight_outcome(path):
 d=pd.read_csv(path,usecols=lambda c:str(c).strip() in REQ);d.columns=[str(c).strip() for c in d.columns]
 if set(d.columns)!=set(REQ):raise RuntimeError('required usecols mismatch')
 x={c:pd.to_numeric(d[c],errors='coerce').to_numpy(float) for c in REQ};va=np.isfinite(x['aim_lat'])&np.isfinite(x['aim_long'])&(np.abs(x['aim_lat'])<=90)&(np.abs(x['aim_long'])<=180);vr=np.isfinite(x['real_lat'])&np.isfinite(x['real_long'])&(np.abs(x['real_lat'])<=90)&(np.abs(x['real_long'])<=180)
 episodes=[];cur=None;idx=[]
 def flush():
  if cur is None or not idx:return
  ii=np.asarray(idx,int);good=vr[ii]
  if not np.any(good):episodes.append(float('inf'));return
  jj=ii[good];episodes.append(float(np.min(hav(x['real_lat'][jj],x['real_long'][jj],cur[0],cur[1]))))
 for i in range(len(d)):
  key=(round(float(x['aim_lat'][i]),7),round(float(x['aim_long'][i]),7)) if va[i] else None
  if key!=cur:flush();cur=key;idx=[]
  if key is not None:idx.append(i)
 flush()
 if not episodes:raise RuntimeError('OUTCOME_SCHEMA_UNIT_FAILURE:no valid waypoint episode')
 e=np.asarray(episodes,float);finite=e[np.isfinite(e)]
 return {'n_rows':len(d),'n_waypoint_episodes':len(e),'n_no_position_episodes':int(np.sum(~np.isfinite(e))),'Y10':float(np.mean(e<=10.0)),'F10':int(np.any(e>10.0)),'Y2':float(np.mean(e<=2.0)),'F2':int(np.any(e>2.0)),'dmin_median_finite':float(np.median(finite)) if len(finite) else math.nan,'dmin_q90_finite':float(np.quantile(finite,.9)) if len(finite) else math.nan,'dmin_max_finite':float(np.max(finite)) if len(finite) else math.nan}
def extract(f,root,out):
 rows=[];fail=[]
 for _,r in f.iterrows():
  try:rows.append({'unit_id':r.unit_id,'scenario':r.scenario,'uav':r.uav,'path':r.canonical_ready_path,**flight_outcome(root/str(r.canonical_ready_path))})
  except Exception as e:fail.append({'unit_id':r.unit_id,'path':r.canonical_ready_path,'error':repr(e)})
 if fail:(out/'amovfly_outcome_extraction_failures_v8.json').write_text(json.dumps(fail,indent=2)+'\n');raise RuntimeError(f'OUTCOME_EXTRACTION_FAIL {len(fail)}')
 z=pd.DataFrame(rows);z.to_csv(out/'amovfly_waypoint_outcomes_v8.csv',index=False);return z

def srs(st,alloc,rng,eligible=None):
 if eligible is None:eligible=np.ones(len(st),bool)
 sel=[];pi=np.zeros(len(st))
 for g,ng in enumerate(alloc):
  pool=np.flatnonzero((st==g)&eligible);pi[pool]=ng/len(pool);sel.extend(rng.choice(pool,size=ng,replace=False).tolist())
 return np.asarray(sel,int),pi
def profile(y,p,st,sel,pi,Xs,gs,pwr,satt):
 masses=[];ests=[];vars=[];esses=[]
 for g in range(4):
  pool=np.flatnonzero(st==g);sg=sel[st[sel]==g];mass=float(p[pool].sum());pcs=p[sg]/mass;q=pi[sg];w=pcs/q;den=float(w.sum());est=float(np.sum(w*y[sg])/den);r=y[sg]-est;vg=gs(r,q,pcs,Xs[sg])/(den*den);vp=pwr(r,q,pcs)/(den*den);masses.append(mass);ests.append(est);vars.append(max(vg if np.isfinite(vg) else 0.,vp));esses.append(den*den/max(np.sum(w*w),1e-15))
 ma=np.asarray(masses);va=np.asarray(vars);ea=np.asarray(esses);est=float(ma@np.asarray(ests));truth=float(p@y);comp=ma*ma*va;se=float(np.sqrt(comp.sum()));df=satt(comp,np.maximum(1.,ea-1));q=t.ppf(.975,df);wg=p[sel]/pi[sel];return est,abs(est-truth),int(abs(est-truth)<=q*se),float(wg.sum()**2/max(np.sum(wg*wg),1e-15))
def domain_error(y,p,mask,sel,pi):
 pool=np.flatnonzero(mask);mass=float(p[pool].sum());truth=float(np.sum(p[pool]*y[pool])/mass);sg=sel[mask[sel]]
 if not len(sg):return abs(truth)
 pc=p[sg]/mass;return abs(float(np.sum(pc*y[sg]/pi[sg]))-truth)
def sample(method,seed,f,st,p,Xs,Xadv,phi,nov,risk,obj,cpktes):
 rng=np.random.default_rng(int(seed))
 if method=='c-pKTES-Hedge':
  sel,pi,bal,cert,_=cpktes(Xs,phi,Xadv,p,st,ALLOC,nov,risk,PORT,rng,rho=RHO,lam=LAM,min_fraction=MINF);return sel,pi,np.setdiff1d(sel,cert,assume_unique=False),bal
 if method=='Stratified-SRS':sel,pi=srs(st,ALLOC,rng);return sel,pi,sel,np.nan
 det=np.asarray(obj['comparators']['split15_audit25']['deterministic_indices'],int);eligible=np.ones(N,bool);eligible[det]=False;aa=np.asarray(obj['comparators']['split15_audit25']['audit_allocation_n25'],int);aud,_=srs(st,aa,rng,eligible);pi=np.asarray([obj['comparators']['split15_audit25']['pi_by_unit_id'][u] for u in f.unit_id]);return np.r_[det,aud],pi,aud,np.nan
def pair(a,b):
 d=np.asarray(a,float)-np.asarray(b,float);m=float(d.mean());se=float(d.std(ddof=1)/math.sqrt(len(d)));return {'mean_diff':m,'ci_lo':m-1.96*se,'ci_hi':m+1.96*se}
def replay(f,st,p,Xs,Xadv,phi,nov,risk,obj,eng,outcomes,out):
 *_,cpktes,pwr,gs,satt=eng;y=outcomes.Y10.to_numpy(float);fail=outcomes.F10.to_numpy(float);y2=outcomes.Y2.to_numpy(float);order=np.lexsort((f.unit_id.astype(str).to_numpy(),y));diff=set(order[:math.ceil(.10*N)].tolist());masks=[(f.scenario==s).to_numpy() for s in STRATA]+[(f.uav==u).to_numpy() for u in UAVG];rows=[];errs=[]
 for seed in SEEDS:
  for m in ['c-pKTES-Hedge','Stratified-SRS','Split15+Audit25']:
   try:
    sel,pi,prob,bal=sample(m,seed,f,st,p,Xs,Xadv,phi,nov,risk,obj,cpktes);ye,pe,cov,ess=profile(y,p,st,sel,pi,Xs,gs,pwr,satt);fe,fer,fcov,_=profile(fail,p,st,sel,pi,Xs,gs,pwr,satt);y2e,p2,_,_=profile(y2,p,st,sel,pi,Xs,gs,pwr,satt);de=float(np.mean([domain_error(y,p,mask,sel,pi) for mask in masks]));w=p[prob]/pi[prob];pess=float(w.sum()**2/max(np.sum(w*w),1e-15));rows.append({'seed':int(seed),'method':m,'profile_estimate_Y10':ye,'profile_error_Y10':pe,'failure_estimate_F10':fe,'failure_error_F10':fer,'critical_domain_error_Y10':de,'difficult_case_hit':int(any(int(i) in diff for i in sel)),'ess_all':ess,'ess_probability_component':pess,'min_pi_selected':float(np.min(pi[sel])),'profile_uq_covered_Y10':cov,'failure_uq_covered_F10':fcov,'profile_estimate_Y2':y2e,'profile_error_Y2':p2,'balance_error':bal})
   except Exception as e:errs.append({'seed':int(seed),'method':m,'error':repr(e)})
 raw=pd.DataFrame(rows);raw.to_csv(out/'amovfly_500_replay_raw_v8.csv',index=False)
 if errs or len(raw)!=1500:(out/'amovfly_replay_failures_v8.json').write_text(json.dumps(errs,indent=2)+'\n');raise RuntimeError(f'replay fail {len(errs)} rows={len(raw)}')
 ss=[]
 for m,d in raw.groupby('method'):ss.append({'method':m,'n_replays':len(d),'profile_error_Y10_mean':d.profile_error_Y10.mean(),'failure_error_F10_mean':d.failure_error_F10.mean(),'critical_domain_error_Y10_mean':d.critical_domain_error_Y10.mean(),'difficult_case_hit_rate':d.difficult_case_hit.mean(),'ess_probability_median':d.ess_probability_component.median(),'ess_probability_p05':d.ess_probability_component.quantile(.05),'profile_uq_coverage_Y10':d.profile_uq_covered_Y10.mean(),'failure_uq_coverage_F10':d.failure_uq_covered_F10.mean(),'profile_error_Y2_mean':d.profile_error_Y2.mean()})
 summ=pd.DataFrame(ss);summ.to_csv(out/'amovfly_500_replay_summary_v8.csv',index=False);k=raw[raw.method=='c-pKTES-Hedge'].sort_values('seed');s=raw[raw.method=='Stratified-SRS'].sort_values('seed');b=raw[raw.method=='Split15+Audit25'].sort_values('seed');pdiff=pair(k.profile_error_Y10,s.profile_error_Y10);g1=(len(k)==500 and np.all(k.min_pi_selected>0));g2=(k.ess_probability_component.median()>=18.5 and k.ess_probability_component.quantile(.05)>=12);g3=pdiff['mean_diff']<=.01;ke=float(k.critical_domain_error_Y10.mean());best=min(float(s.critical_domain_error_Y10.mean()),float(b.critical_domain_error_Y10.mean()));g4=ke-best<=.02;g5=float(k.difficult_case_hit.mean())>=float(b.difficult_case_hit.mean())-.10;gates={'G1_positive_pi_no_sampling_failure':bool(g1),'G2_ESS':bool(g2),'G3_profile_noninferiority':bool(g3),'G4_critical_domain':bool(g4),'G5_difficult_hit':bool(g5)};pop={'N':N,'Y10_mean':float(y.mean()),'F10_rate':float(fail.mean()),'Y2_mean':float(y2.mean()),'F2_rate':float(outcomes.F2.mean()),'difficult_n':len(diff),'n_total_waypoint_episodes':int(outcomes.n_waypoint_episodes.sum()),'n_no_position_episodes':int(outcomes.n_no_position_episodes.sum())};result={'schema_version':'KTES-AMOVFLY-EXTERNAL-RESULT-v8.1','status':'PASS' if all(gates.values()) else 'FAIL','population_truth':pop,'gates':gates,'G3_paired':pdiff,'G4':{'ktes':ke,'srs':float(s.critical_domain_error_Y10.mean()),'split15':float(b.critical_domain_error_Y10.mean()),'better_comparator':best,'ktes_minus_better':ke-best},'G5':{'ktes':float(k.difficult_case_hit.mean()),'split15':float(b.difficult_case_hit.mean()),'difference':float(k.difficult_case_hit.mean()-b.difficult_case_hit.mean())},'design_sha256':DESIGN_SHA,'frame_sha256':FRAME_SHA,'outcome_artifact_sha256':sha(out/'amovfly_waypoint_outcomes_v8.csv'),'raw_replay_sha256':sha(out/'amovfly_500_replay_raw_v8.csv')};(out/'AMOVFLY_EXTERNAL_VALIDATION_RESULT_v8.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');report=f'''# AMOVFLY external engineering validation result v8\n\n**Result gate:** **{result['status']}**\n\nPopulation truth under the frozen 10 m waypoint-attainment reference: mean Y={pop['Y10_mean']:.6f}; flight failure rate={pop['F10_rate']:.6f}. Strict 2 m sensitivity mean Y={pop['Y2_mean']:.6f}.\n\n## Guardrails\n\n| Gate | Result |\n|---|---|\n| G1 positive pi / no sampling failure | {'PASS' if g1 else 'FAIL'} |\n| G2 probability-remainder ESS | {'PASS' if g2 else 'FAIL'} |\n| G3 profile error vs SRS <= +0.01 | {'PASS' if g3 else 'FAIL'}; paired mean diff {pdiff['mean_diff']:.6f}, 95% CI [{pdiff['ci_lo']:.6f}, {pdiff['ci_hi']:.6f}] |\n| G4 critical-domain error <= better comparator +0.02 | {'PASS' if g4 else 'FAIL'}; delta {ke-best:.6f} |\n| G5 difficult-hit >= Split15 -0.10 | {'PASS' if g5 else 'FAIL'}; delta {float(k.difficult_case_hit.mean()-b.difficult_case_hit.mean()):.6f} |\n\nThe primary endpoint, 10 m external reference radius, 2 m sensitivity, population, design, comparators, and numerical guardrails were all frozen before telemetry outcome values were opened. The 10 m threshold is an external PX4-default reference and is not claimed to be AMOVFLY's historical configured acceptance radius.\n''';(out/'AMOVFLY_EXTERNAL_VALIDATION_RESULT_v8.md').write_text(report);return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--frame',type=Path,required=True);ap.add_argument('--source-root',type=Path);ap.add_argument('--vendor-src',type=Path,default=Path('vendor/r5_engine_recovered_v8/src'));ap.add_argument('--out',type=Path,default=Path('outputs/amovfly_external'));ap.add_argument('--design-only',action='store_true');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);f,st,p,Xs,Xadv,phi,nov,risk,obj,eng=prepare_design(a.frame,a.vendor_src,a.out);print('design_sha',DESIGN_SHA,'verified')
 if a.design_only:return
 if a.source_root is None:raise SystemExit('--source-root required unless --design-only')
 schema_gate(f,a.source_root,a.out);print('schema gate PASS: 257/257; opening only frozen endpoint columns');outcomes=extract(f,a.source_root,a.out);result=replay(f,st,p,Xs,Xadv,phi,nov,risk,obj,eng,outcomes,a.out);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
