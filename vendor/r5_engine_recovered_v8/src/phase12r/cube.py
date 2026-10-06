from __future__ import annotations
import numpy as np

def _step(p,idx,u,rng,tol=1e-12):
    v=p[idx]
    pos=u>tol; neg=u<-tol
    plus=[]; minus=[]
    if np.any(pos):
        plus.extend(((1-v[pos])/u[pos]).tolist()); minus.extend((v[pos]/u[pos]).tolist())
    if np.any(neg):
        plus.extend((v[neg]/(-u[neg])).tolist()); minus.extend(((1-v[neg])/(-u[neg])).tolist())
    lp=min(plus) if plus else 0.0; lm=min(minus) if minus else 0.0
    if lp<=tol and lm<=tol: return False
    if lm<=tol: take_plus=True
    elif lp<=tol: take_plus=False
    else: take_plus=(rng.random()<lm/(lp+lm))
    v=v+(lp*u if take_plus else -lm*u)
    v=np.where(v<1e-10,0,v); v=np.where(v>1-1e-10,1,v)
    p[idx]=np.clip(v,0,1)
    return True

def cube_sample(pi,balance,rng):
    """Approximate cube sampler: exact flight balance, pivotal landing; preserves first-order expectations."""
    p=np.asarray(pi,float).copy(); B=np.asarray(balance,float)
    if B.ndim==1: B=B[:,None]
    q=B.shape[1]
    while True:
        active=np.flatnonzero((p>1e-10)&(p<1-1e-10))
        if len(active)<=q: break
        idx=rng.choice(active,size=q+1,replace=False)
        M=B[idx].T
        # Null direction of q x (q+1) matrix.
        _,_,vh=np.linalg.svd(M,full_matrices=True)
        u=vh[-1]
        if np.linalg.norm(u)<1e-12:
            continue
        _step(p,idx,u,rng)
    # Pivotal landing preserves sample-size balance exactly when ones are in B.
    while True:
        active=np.flatnonzero((p>1e-10)&(p<1-1e-10))
        if len(active)<=1: break
        idx=active[:2]
        _step(p,idx,np.array([1.0,-1.0]),rng)
    if np.any((p>1e-8)&(p<1-1e-8)):
        i=np.flatnonzero((p>1e-8)&(p<1-1e-8))[0]
        p[i]=float(rng.random()<p[i])
    s=np.flatnonzero(p>.5)
    target=int(round(np.sum(pi)))
    if len(s)!=target:
        # Numerical fallback; should be rare. Keep nearest rounded probabilities.
        s=np.argsort(-p)[:target]
    return np.sort(s)

def stratified_cube_sample(Xphi,strata,alloc,rng):
    """Equal-first-order-probability cube sampling within each mutually exclusive stratum."""
    selected=[]; pi_full=np.zeros(len(strata)); balerr=[]
    for g,ng in enumerate(alloc):
        pool=np.flatnonzero(strata==g); Ng=len(pool)
        if ng<=0: continue
        if ng>Ng: raise ValueError("allocation exceeds stratum size")
        pi=np.full(Ng,ng/Ng,float); pi_full[pool]=pi
        # Number of kernel balance features adapted to small stratum sample size.
        d=min(Xphi.shape[1],max(1,ng-2))
        Z=Xphi[pool,:d].copy()
        sd=Z.std(0); sd=np.where(sd<1e-10,1,sd)
        Z=(Z-Z.mean(0))/sd
        B=np.column_stack([np.ones(Ng),Z])
        loc=cube_sample(pi,B,rng)
        selected.extend(pool[loc].tolist())
        balerr.append(float(np.linalg.norm(Z[loc].mean(0)-Z.mean(0))))
    return np.asarray(selected,dtype=int),pi_full,float(np.mean(balerr))
