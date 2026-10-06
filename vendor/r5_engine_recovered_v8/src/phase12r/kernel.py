from __future__ import annotations
import numpy as np
from scipy.spatial.distance import pdist

def standardize(X):
    X=np.asarray(X,float); mu=X.mean(0); sd=X.std(0)
    sd=np.where(sd<1e-12,1,sd)
    return (X-mu)/sd,mu,sd

def median_bandwidth(X,max_points=600,seed=0):
    rng=np.random.default_rng(seed); X=np.asarray(X,float)
    if len(X)>max_points: X=X[rng.choice(len(X),max_points,replace=False)]
    d=pdist(X); d=d[d>0]
    return float(np.median(d)) if len(d) else 1.0

def rbf_cross(A,B,h):
    A=np.asarray(A,float);B=np.asarray(B,float)
    d2=((A[:,None,:]-B[None,:,:])**2).sum(2)
    return np.exp(-d2/(2*h*h))

def rff_features(X,h,n_features=8,seed=0):
    rng=np.random.default_rng(seed); X=np.asarray(X,float)
    W=rng.normal(size=(X.shape[1],n_features))/max(h,1e-8)
    b=rng.uniform(0,2*np.pi,size=n_features)
    return np.sqrt(2/n_features)*np.cos(X@W+b)
