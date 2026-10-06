from __future__ import annotations
import numpy as np
from .active_designs import _capped_inclusion, local_cube_sample


def rank01(x):
    x=np.asarray(x,float)
    if len(x)<=1: return np.zeros_like(x)
    order=np.argsort(np.argsort(x,kind='mergesort'),kind='mergesort')
    return order/(len(x)-1)


def interaction_leverage_score(Xs,p,ridge=0.10,central_penalty=0.45):
    """Outcome-blind leverage of pairwise interactions after removing main effects.

    The score is high when a unit is unusual in the pairwise-interaction feature
    space beyond what is explained by ordinary main-effect leverage. This targets
    compound/semantic edge conditions without using live outcomes or hidden labels.
    """
    X=np.asarray(Xs,float); p=np.asarray(p,float); p=p/p.sum(); n,d=X.shape
    pairs=[(j,k) for j in range(d) for k in range(j+1,d)]
    W=np.column_stack([X[:,j]*X[:,k] for j,k in pairs])
    A=np.column_stack([np.ones(n),X])
    sw=np.sqrt(p)[:,None]
    # weighted projection of interactions onto intercept + main effects
    coef=np.linalg.lstsq(A*sw,W*sw,rcond=None)[0]
    R=W-A@coef
    # weighted standardization
    mu=(p[:,None]*R).sum(0); R=R-mu
    sd=np.sqrt((p[:,None]*R*R).sum(0)); sd=np.where(sd<1e-8,1.0,sd); R=R/sd
    S=(R*p[:,None]).T@R + ridge*np.eye(R.shape[1])
    Sinv=np.linalg.pinv(S,rcond=1e-10)
    lint=np.einsum('ij,jk,ik->i',R,Sinv,R)
    # penalize ordinary main-effect leverage so score emphasizes combinations
    Sm=(X*p[:,None]).T@X + ridge*np.eye(d)
    Sminv=np.linalg.pinv(Sm,rcond=1e-10)
    lmain=np.einsum('ij,jk,ik->i',X,Sminv,X)
    ri=rank01(lint); rm=rank01(lmain)
    score=ri*(1.0-central_penalty*rm)
    return np.clip(score,0,None)


def risk_novelty_score(novelty,pred_fail):
    return 0.5*rank01(novelty)+0.5*rank01(pred_fail)


def _select_by_type(Xs,base_scores,types,diversity_weight=0.35):
    """Sequential outcome-blind certainty selection with maximin diversification."""
    X=np.asarray(Xs,float); selected=[]
    n=len(X)
    for typ in types:
        base=rank01(np.asarray(base_scores[typ],float))
        if selected:
            D=np.sqrt(((X-X[selected][:,None,:].transpose(1,0,2))**2).sum(2)) if False else None
            # simpler pairwise distance to already-selected points
            dist=np.sqrt(((X[:,None,:]-X[np.asarray(selected)][None,:,:])**2).sum(2)).min(1)
            div=rank01(dist)
            score=(1-diversity_weight)*base+diversity_weight*div
            score[np.asarray(selected)]=-np.inf
        else:
            score=base.copy()
        selected.append(int(np.argmax(score)))
    return np.asarray(selected,int)


def select_portfolio(Xs,novelty,pred_fail,interaction,portfolio):
    scores={'N':novelty,'R':risk_novelty_score(novelty,pred_fail),'I':interaction}
    return _select_by_type(Xs,scores,list(portfolio),diversity_weight=.35)


def certainty_portfolio_local_cube(Xspread,Xphi,strata,alloc,novelty,pred_fail,interaction,
                                   portfolio,rng,lam=3.0,min_fraction=.35):
    """Fixed certainty portfolio plus probability-preserving novelty-PPS Local Cube remainder."""
    cert=select_portfolio(Xspread,novelty,pred_fail,interaction,portfolio)
    pi_full=np.zeros(len(strata),float); pi_full[cert]=1.0
    selected=cert.tolist(); balerr=[]
    for g,ng in enumerate(np.asarray(alloc,int)):
        pool_all=np.flatnonzero(strata==g)
        c=np.intersect1d(pool_all,cert,assume_unique=False)
        nr=int(ng)-len(c)
        pool=np.setdiff1d(pool_all,cert,assume_unique=False)
        if nr<0: raise RuntimeError('too many certainty units in stratum')
        if nr==0: continue
        z=np.asarray(novelty[pool],float)
        score=np.exp(float(lam)*(z-z.mean()))
        pi=_capped_inclusion(score,nr,min_fraction=min_fraction); pi_full[pool]=pi
        d=min(Xphi.shape[1],max(1,nr-2))
        Z=Xphi[pool,:d].copy(); sd=Z.std(0); sd=np.where(sd<1e-10,1,sd); Z=(Z-Z.mean(0))/sd
        B=np.column_stack([np.ones(len(pool)),Z/pi[:,None]])
        loc=local_cube_sample(pi,Xspread[pool],B,rng)
        if len(loc)!=nr: raise RuntimeError('local cube size mismatch')
        selected.extend(pool[loc].tolist())
        ht=(Z[loc]/pi[loc,None]).sum(0); total=Z.sum(0)
        balerr.append(float(np.linalg.norm((ht-total)/len(pool))))
    sel=np.asarray(selected,int)
    if len(sel)!=int(np.sum(alloc)): raise RuntimeError(f'size mismatch {len(sel)}')
    if np.any(pi_full<=0):
        # units in strata from which all slots are certainty cannot occur under current allocations;
        # otherwise every non-certainty unit must retain positive inclusion probability.
        bad=np.flatnonzero(pi_full<=0)
        if len(bad): raise RuntimeError('nonpositive inclusion probability')
    return sel,pi_full,float(np.mean(balerr) if balerr else 0.0),cert

def weighted_cdf_columns(X,p):
    X=np.asarray(X,float);p=np.asarray(p,float);p=p/p.sum();n,d=X.shape;Q=np.empty_like(X,float)
    for j in range(d):
        order=np.argsort(X[:,j],kind='mergesort');cw=np.cumsum(p[order]);Q[order,j]=cw-0.5*p[order]
    return Q


def compound_adverse_score(X,p,k=3):
    """Outcome-blind joint-severity score after orienting variables so high=more adverse.

    Product of the k largest operational-profile marginal quantiles. It flags
    conditions that are moderately/highly adverse on several dimensions even
    when no single coordinate is an extreme outlier.
    """
    Q=weighted_cdf_columns(X,p); top=np.sort(Q,axis=1)[:,-int(k):]
    return np.prod(top,axis=1)


def certainty_portfolio_blended_pps_local_cube(Xspread,Xphi,Xraw,pop_p,strata,alloc,novelty,pred_fail,
                                               portfolio,rng,rho=.35,lam=3.0,min_fraction=.35):
    """Certainty portfolio + Local Cube remainder with novelty/compound-tail PPS hedge."""
    comp=compound_adverse_score(Xraw,pop_p,k=3)
    # interaction argument is unused by N/R portfolios but supplied for generic selector
    inter=np.zeros(len(strata))
    cert=select_portfolio(Xspread,novelty,pred_fail,inter,portfolio)
    pi_full=np.zeros(len(strata),float);pi_full[cert]=1.0;selected=cert.tolist();balerr=[]
    comp_r=rank01(comp)
    for g,ng in enumerate(np.asarray(alloc,int)):
        pool_all=np.flatnonzero(strata==g);c=np.intersect1d(pool_all,cert,assume_unique=False);nr=int(ng)-len(c)
        pool=np.setdiff1d(pool_all,cert,assume_unique=False)
        if nr<0: raise RuntimeError('too many certainty units in stratum')
        if nr==0: continue
        z=(1-float(rho))*np.asarray(novelty[pool],float)+float(rho)*comp_r[pool]
        score=np.exp(float(lam)*(z-z.mean()))
        pi=_capped_inclusion(score,nr,min_fraction=min_fraction);pi_full[pool]=pi
        d=min(Xphi.shape[1],max(1,nr-2));Z=Xphi[pool,:d].copy();sd=Z.std(0);sd=np.where(sd<1e-10,1,sd);Z=(Z-Z.mean(0))/sd
        B=np.column_stack([np.ones(len(pool)),Z/pi[:,None]])
        loc=local_cube_sample(pi,Xspread[pool],B,rng)
        if len(loc)!=nr: raise RuntimeError('local cube size mismatch')
        selected.extend(pool[loc].tolist())
        ht=(Z[loc]/pi[loc,None]).sum(0);total=Z.sum(0);balerr.append(float(np.linalg.norm((ht-total)/len(pool))))
    sel=np.asarray(selected,int)
    if len(sel)!=int(np.sum(alloc)): raise RuntimeError(f'size mismatch {len(sel)}')
    if np.any(pi_full<=0): raise RuntimeError('nonpositive inclusion probability')
    return sel,pi_full,float(np.mean(balerr) if balerr else 0.0),cert,comp
