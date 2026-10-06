from __future__ import annotations
import numpy as np
from scipy.stats import t
from .estimators import ALPHA,_satterthwaite
from .spread_estimators import gs_variance


def pwr_variance(residual,pi,pcond):
    residual=np.asarray(residual,float);pi=np.asarray(pi,float);pcond=np.asarray(pcond,float)
    m=pi<1-1e-10
    if not np.any(m): return 0.0
    r=residual[m]; q=pi[m]; pc=pcond[m]
    return float(np.sum((1-q)*(pc*r/q)**2))


def evaluate_hajek(pop,pred_y,pred_b,sel,y,b,pi_full,alloc,method,coords,balance_error=np.nan):
    masses=[];ey=[];eb=[];vy=[];vb=[];ess=[]
    for g,ng in enumerate(np.asarray(alloc,int)):
        pool=np.flatnonzero(pop.strata==g); sg=sel[pop.strata[sel]==g]
        if len(sg)!=ng: raise RuntimeError(f'stratum {g}: expected {ng}, got {len(sg)}')
        mass=float(pop.p[pool].sum());masses.append(mass)
        pca=pop.p[pool]/mass; cy=float(pca@pred_y[pool]);cb=float(pca@pred_b[pool])
        pcs=pop.p[sg]/mass; pi=pi_full[sg]; wy=pcs/pi
        ry=y[sg]-pred_y[sg];rb=b[sg]-pred_b[sg]
        den=float(wy.sum()); hy=float(np.sum(wy*ry)/den);hb=float(np.sum(wy*rb)/den)
        ey.append(cy+hy);eb.append(cb+hb)
        # linearized ratio residuals around Hajek correction; use max(GS,PWR)
        ly=ry-hy;lb=rb-hb
        vyg=gs_variance(ly,pi,pcs,coords[sg])/(den*den)
        vbg=gs_variance(lb,pi,pcs,coords[sg])/(den*den)
        vyp=pwr_variance(ly,pi,pcs)/(den*den);vbp=pwr_variance(lb,pi,pcs)/(den*den)
        vy.append(max(vyg if np.isfinite(vyg) else 0.0,vyp));vb.append(max(vbg if np.isfinite(vbg) else 0.0,vbp))
        ess.append(float(den*den/max(np.sum(wy*wy),1e-15)))
    masses=np.asarray(masses);ey=np.asarray(ey);eb=np.asarray(eb);vy=np.asarray(vy);vb=np.asarray(vb);ess=np.asarray(ess)
    prof=float(masses@ey); fail=float(masses@eb)
    compy=masses*masses*vy;compb=masses*masses*vb
    sey=float(np.sqrt(np.sum(compy)));seb=float(np.sqrt(np.sum(compb)))
    dfs=np.maximum(1.0,ess-1);dfy=_satterthwaite(compy,dfs);dfb=_satterthwaite(compb,dfs)
    qy=t.ppf(.975,dfy);qb=t.ppf(.975,dfb)
    covy=int(abs(prof-pop.true_mean)<=qy*sey);covb=int(abs(fail-pop.true_fail_prob)<=qb*seb)
    tails=ey[1:];tse=np.sqrt(vy[1:]);true_tail=pop.true_tail_means
    covtail=[]
    for j in range(len(tails)):
        q=t.ppf(.975,max(1,ess[j+1]-1));covtail.append(int(abs(tails[j]-true_tail[j])<=q*tse[j]))
    a=ALPHA/6;qy1=t.ppf(1-a,dfy);qb1=t.ppf(1-a,dfb)
    lm=prof-qy1*sey;um=prof+qy1*sey;lf=fail-qb1*seb;uf=fail+qb1*seb
    lt=[];ut=[]
    for j in range(len(tails)):
        q=t.ppf(1-a,max(1,ess[j+1]-1));lt.append(tails[j]-q*tse[j]);ut.append(tails[j]+q*tse[j])
    lt=np.asarray(lt);ut=np.asarray(ut)
    accept=(lm>=pop.threshold_mean) and (uf<=pop.threshold_fail) and bool(np.all(lt>=pop.tail_requirements))
    reject=(um<pop.threshold_mean) or (lf>pop.threshold_fail) or bool(np.any(ut<pop.tail_requirements))
    status=1 if accept and not reject else (0 if reject and not accept else -1);true=int(pop.true_accept)
    w=pop.p[sel]/pi_full[sel]
    return {'method':method,'est_mean':prof,'mean_abs_error':abs(prof-pop.true_mean),'mean_coverage':covy,
            'est_fail':fail,'fail_abs_error':abs(fail-pop.true_fail_prob),'fail_coverage':covb,
            'critical_tail_mae':float(np.mean(np.abs(tails-true_tail))),'tail_coverage':float(np.mean(covtail)),
            'status':status,'true_accept':true,'definitive_correct':int(status!=-1 and status==true),'abstain':int(status==-1),
            'false_accept':int(status==1 and true==0),'false_reject':int(status==0 and true==1),'balance_error':balance_error,
            'weight_ess':float((w.sum()**2)/max(np.sum(w*w),1e-15)),'min_pi':float(np.min(pi_full[sel])),'max_weight':float(np.max(w))}
