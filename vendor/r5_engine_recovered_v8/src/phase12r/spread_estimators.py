from __future__ import annotations
import numpy as np
from scipy.stats import t
from scipy.spatial import cKDTree
from .estimators import ALPHA,_satterthwaite


def gs_variance(residual, pi, pcond, coords):
    """Grafstrom-Schelin nearest-neighbour variance estimator for an HT residual total.

    Target residual total is sum_i pcond_i r_i and its HT estimator is
    sum_{i in s} pcond_i r_i / pi_i. The GS estimator only needs first-order pi.
    """
    residual=np.asarray(residual,float); pi=np.asarray(pi,float); pcond=np.asarray(pcond,float)
    coords=np.asarray(coords,float)
    # Certainty units (pi=1) have zero design variance and are excluded from
    # the local-difference variance calculation.
    mask=pi < 1.0-1e-10
    residual=residual[mask]; pi=pi[mask]; pcond=pcond[mask]; coords=coords[mask]
    n=len(residual)
    if n<2: return 0.0 if n==0 else np.nan
    z=pcond*residual/pi
    tree=cKDTree(coords)
    _,idx=tree.query(coords,k=2)
    nn=idx[:,1]
    return float(0.5*np.sum((z-z[nn])**2))


def evaluate_ma_spread(pop,pred_y,pred_b,sel,y,b,pi_full,alloc,method,spread_coords,balance_error=np.nan):
    masses=[]; ey=[]; eb=[]; vy=[]; vb=[]; ess=[]
    for g,ng in enumerate(np.asarray(alloc,int)):
        pool=np.flatnonzero(pop.strata==g); sg=sel[pop.strata[sel]==g]
        if len(sg)!=ng: raise RuntimeError(f'stratum {g}: expected {ng}, got {len(sg)}')
        mass=float(pop.p[pool].sum()); masses.append(mass)
        pcond_all=pop.p[pool]/mass
        cy=float(pcond_all@pred_y[pool]); cb=float(pcond_all@pred_b[pool])
        pcond_s=pop.p[sg]/mass; ry=y[sg]-pred_y[sg]; rb=b[sg]-pred_b[sg]
        hy=float(np.sum(pcond_s*ry/pi_full[sg])); hb=float(np.sum(pcond_s*rb/pi_full[sg]))
        ey.append(cy+hy); eb.append(cb+hb)
        vy.append(gs_variance(ry,pi_full[sg],pcond_s,spread_coords[sg]))
        vb.append(gs_variance(rb,pi_full[sg],pcond_s,spread_coords[sg]))
        w=pcond_s/pi_full[sg]; ess.append(float((w.sum()**2)/max(np.sum(w*w),1e-15)))
    masses=np.asarray(masses);ey=np.asarray(ey);eb=np.asarray(eb);vy=np.asarray(vy);vb=np.asarray(vb);ess=np.asarray(ess)
    prof=float(masses@ey);fail=float(masses@eb)
    comp_y=masses*masses*vy;comp_b=masses*masses*vb
    se_y=float(np.sqrt(np.sum(comp_y)));se_b=float(np.sqrt(np.sum(comp_b)))
    dfs=np.maximum(1.0,ess-1);df_y=_satterthwaite(comp_y,dfs);df_b=_satterthwaite(comp_b,dfs)
    qy=t.ppf(.975,df_y);qb=t.ppf(.975,df_b)
    cov_y=int(abs(prof-pop.true_mean)<=qy*se_y);cov_b=int(abs(fail-pop.true_fail_prob)<=qb*se_b)
    tails=ey[1:];tail_se=np.sqrt(vy[1:]);true_tail=pop.true_tail_means
    cov_tail=[]
    for j in range(len(tails)):
        q=t.ppf(.975,max(1,ess[j+1]-1));cov_tail.append(int(abs(tails[j]-true_tail[j])<=q*tail_se[j]))
    a=ALPHA/6;qy1=t.ppf(1-a,df_y);qb1=t.ppf(1-a,df_b)
    lm=prof-qy1*se_y;um=prof+qy1*se_y;lf=fail-qb1*se_b;uf=fail+qb1*se_b
    lt=[];ut=[]
    for j in range(len(tails)):
        q=t.ppf(1-a,max(1,ess[j+1]-1));lt.append(tails[j]-q*tail_se[j]);ut.append(tails[j]+q*tail_se[j])
    lt=np.asarray(lt);ut=np.asarray(ut)
    accept=(lm>=pop.threshold_mean) and (uf<=pop.threshold_fail) and bool(np.all(lt>=pop.tail_requirements))
    reject=(um<pop.threshold_mean) or (lf>pop.threshold_fail) or bool(np.any(ut<pop.tail_requirements))
    status=1 if accept and not reject else (0 if reject and not accept else -1);true=int(pop.true_accept)
    w=pop.p[sel]/pi_full[sel]
    return {'method':method,'est_mean':prof,'mean_abs_error':abs(prof-pop.true_mean),'mean_coverage':cov_y,
            'est_fail':fail,'fail_abs_error':abs(fail-pop.true_fail_prob),'fail_coverage':cov_b,
            'critical_tail_mae':float(np.mean(np.abs(tails-true_tail))),'tail_coverage':float(np.mean(cov_tail)),
            'status':status,'true_accept':true,'definitive_correct':int(status!=-1 and status==true),'abstain':int(status==-1),
            'false_accept':int(status==1 and true==0),'false_reject':int(status==0 and true==1),'balance_error':balance_error,
            'weight_ess':float((w.sum()**2)/max(np.sum(w*w),1e-15)),'min_pi':float(np.min(pi_full[sel])),'max_weight':float(np.max(w))}
