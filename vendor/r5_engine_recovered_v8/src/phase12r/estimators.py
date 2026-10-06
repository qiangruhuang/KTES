from __future__ import annotations
import numpy as np
from scipy.stats import norm,t
from .kernel import rbf_cross

ALPHA=.05

def krr_correction(Xs,train,residual,h,ridge=.08,labels=None):
    train=np.asarray(train,dtype=int); residual=np.asarray(residual,float)
    if labels is None:
        Xa=Xs; Xt=Xs[train]
    else:
        # Known task-domain indicators are legitimate auxiliary variables.
        G=np.eye(5)[labels]
        Xa=np.column_stack([Xs,1.5*G]); Xt=Xa[train]
    Ktt=rbf_cross(Xt,Xt,h)+ridge*np.eye(len(train))
    alpha=np.linalg.solve(Ktt,residual)
    return rbf_cross(Xa,Xt,h)@alpha

def _stratum_ma(pop,pred_y,pred_b,sel,y,b,alloc):
    masses=[]; ey=[]; eb=[]; vy=[]; vb=[]; tail_hw=[]
    for g,ng in enumerate(alloc):
        pool=np.flatnonzero(pop.strata==g); sg=sel[pop.strata[sel]==g]
        if len(sg)!=ng: raise RuntimeError(f"stratum {g}: expected {ng}, got {len(sg)}")
        pg=pop.p[pool]/pop.p[pool].sum(); masses.append(pop.p[pool].sum())
        center_y=float(pg@pred_y[pool]); center_b=float(pg@pred_b[pool])
        ry=y[sg]-pred_y[sg]; rb=b[sg]-pred_b[sg]
        ey.append(center_y+float(np.mean(ry))); eb.append(center_b+float(np.mean(rb)))
        fpc=max(0.0,1-len(sg)/len(pool))
        vy.append(float(np.var(ry,ddof=1)/len(sg)*fpc) if len(sg)>1 else np.nan)
        vb.append(float(np.var(rb,ddof=1)/len(sg)*fpc) if len(sg)>1 else np.nan)
    return np.asarray(masses),np.asarray(ey),np.asarray(eb),np.asarray(vy),np.asarray(vb)

def _satterthwaite(v,df):
    v=np.asarray(v,float); df=np.asarray(df,float)
    num=np.sum(v)**2; den=np.sum(np.where(df>0,v*v/df,0))
    return float(num/den) if den>0 else 1e6

def evaluate_ma(pop,pred_y,pred_b,sel,y,b,alloc,method,balance_error=np.nan):
    masses,ey,eb,vy,vb=_stratum_ma(pop,pred_y,pred_b,sel,y,b,alloc)
    prof=float(masses@ey); fail=float(masses@eb)
    comp_y=masses*masses*vy; comp_b=masses*masses*vb
    se_y=float(np.sqrt(np.sum(comp_y))); se_b=float(np.sqrt(np.sum(comp_b)))
    dfs=np.asarray(alloc)-1
    df_y=_satterthwaite(comp_y,dfs); df_b=_satterthwaite(comp_b,dfs)
    # Marginal 95% intervals for diagnostics.
    qy=t.ppf(.975,df_y); qb=t.ppf(.975,df_b)
    cov_y=int(abs(prof-pop.true_mean)<=qy*se_y)
    cov_b=int(abs(fail-pop.true_fail_prob)<=qb*se_b)
    tails=ey[1:]; tail_se=np.sqrt(vy[1:]); true_tail=pop.true_tail_means
    cov_tail=[]
    for j,ng in enumerate(np.asarray(alloc)[1:]):
        q=t.ppf(.975,max(1,int(ng)-1)); cov_tail.append(int(abs(tails[j]-true_tail[j])<=q*tail_se[j]))

    # Familywise one-sided three-state decision, 6 constraints.
    a=ALPHA/6
    qy1=t.ppf(1-a,df_y); qb1=t.ppf(1-a,df_b)
    lower_mean=prof-qy1*se_y; upper_mean=prof+qy1*se_y
    lower_fail=fail-qb1*se_b; upper_fail=fail+qb1*se_b
    lower_tail=[]; upper_tail=[]
    for j,ng in enumerate(np.asarray(alloc)[1:]):
        q=t.ppf(1-a,max(1,int(ng)-1))
        lower_tail.append(tails[j]-q*tail_se[j]); upper_tail.append(tails[j]+q*tail_se[j])
    lower_tail=np.asarray(lower_tail); upper_tail=np.asarray(upper_tail)
    accept=(lower_mean>=pop.threshold_mean) and (upper_fail<=pop.threshold_fail) and bool(np.all(lower_tail>=pop.tail_requirements))
    reject=(upper_mean<pop.threshold_mean) or (lower_fail>pop.threshold_fail) or bool(np.any(upper_tail<pop.tail_requirements))
    status=1 if accept and not reject else (0 if reject and not accept else -1)
    true=int(pop.true_accept)
    return {
        'method':method,'est_mean':prof,'mean_abs_error':abs(prof-pop.true_mean),'mean_coverage':cov_y,
        'est_fail':fail,'fail_abs_error':abs(fail-pop.true_fail_prob),'fail_coverage':cov_b,
        'critical_tail_mae':float(np.mean(np.abs(tails-true_tail))),
        'tail_coverage':float(np.mean(cov_tail)),'status':status,'true_accept':true,
        'definitive_correct':int(status!=-1 and status==true),'abstain':int(status==-1),
        'false_accept':int(status==1 and true==0),'false_reject':int(status==0 and true==1),
        'balance_error':balance_error,
    }
