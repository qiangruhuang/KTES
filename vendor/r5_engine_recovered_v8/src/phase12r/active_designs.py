from __future__ import annotations
import numpy as np
from scipy.spatial import cKDTree
from .cube import cube_sample
from .kernel import rbf_cross


def kernel_novelty(Xs, p, h, power=2.0, max_anchors=160, seed=0):
    """Outcome-free rarity/novelty score from approximate weighted RBF density.

    Operational-profile anchors make this O(N*A) rather than O(N^2). The rank
    transform makes the score robust to density scale. No outcome or hidden-edge
    labels are used.
    """
    Xs=np.asarray(Xs,float); p=np.asarray(p,float); p=p/p.sum()
    if len(Xs) <= max_anchors:
        anchors=np.arange(len(Xs)); w=p.copy()
    else:
        rng=np.random.default_rng(seed)
        anchors=rng.choice(len(Xs),size=max_anchors,replace=False,p=p)
        # Sampling anchors from p means an unweighted average estimates P K(x,X).
        w=np.full(len(anchors),1/len(anchors),float)
    density = rbf_cross(Xs, Xs[anchors], h) @ w
    order = np.argsort(np.argsort(density))  # low density -> low rank
    novelty = 1.0 - (order + 0.5) / len(density)
    return np.clip(novelty, 1e-6, 1.0) ** float(power)


def _capped_inclusion(base_scores, n, min_fraction=0.45):
    """Convert positive scores to first-order inclusion probabilities summing to n.

    A positive floor preserves inference eligibility for every unit. Iterative
    capping handles pi_i > 1 without changing the requested expected sample size.
    """
    s = np.asarray(base_scores, float)
    N = len(s)
    if not (0 < n <= N):
        raise ValueError("invalid sample size")
    equal = n / N
    floor = min_fraction * equal
    # Allocate the remaining expected count proportional to scores.
    rem = n - N * floor
    q = s / s.sum()
    pi = np.full(N, floor) + rem * q
    # Water-fill caps at 1.
    free = np.ones(N, dtype=bool)
    for _ in range(N + 2):
        over = free & (pi > 1.0)
        if not np.any(over):
            break
        pi[over] = 1.0
        free[over] = False
        target = n - pi[~free].sum()
        if target <= 0 or not np.any(free):
            break
        floor_free = floor
        base = np.full(np.sum(free), floor_free)
        residual = target - base.sum()
        sf = s[free]
        if residual < 0:
            base[:] = target / len(base)
            residual = 0
        pi[free] = base + residual * sf / sf.sum()
    # Small numerical correction over non-certainty units.
    diff = n - pi.sum()
    idx = np.flatnonzero(pi < 1 - 1e-12)
    if len(idx):
        pi[idx] += diff / len(idx)
    if np.any(pi <= 0) or np.any(pi > 1 + 1e-8) or abs(pi.sum() - n) > 1e-6:
        raise RuntimeError("failed to construct inclusion probabilities")
    return np.clip(pi, 1e-12, 1.0)


def novelty_inclusion_probabilities(strata, alloc, novelty, eta=0.45, min_fraction=0.45):
    """Unequal pi within each stratum, mixing profile-uniform and novelty targeting."""
    full = np.zeros(len(strata), float)
    for g, ng in enumerate(np.asarray(alloc, int)):
        pool = np.flatnonzero(strata == g)
        if ng <= 0:
            continue
        # eta=0 -> equal probabilities. eta>0 tilts toward high novelty.
        nov = np.asarray(novelty[pool], float)
        score = (1.0 - eta) * np.ones(len(pool)) + eta * nov / max(nov.mean(), 1e-12)
        full[pool] = _capped_inclusion(score, int(ng), min_fraction=min_fraction)
    return full


def stratified_unequal_cube(Xphi, strata, alloc, pi_full, rng):
    """Cube sample with unequal first-order pi and kernel-feature balance."""
    selected = []
    balerr = []
    for g, ng in enumerate(np.asarray(alloc, int)):
        pool = np.flatnonzero(strata == g)
        pi = np.asarray(pi_full[pool], float)
        if abs(pi.sum() - ng) > 1e-6:
            raise ValueError("stratum inclusion probabilities do not sum to allocation")
        d = min(Xphi.shape[1], max(1, int(ng) - 2))
        Z = Xphi[pool, :d].copy()
        sd = Z.std(0)
        sd = np.where(sd < 1e-10, 1.0, sd)
        Z = (Z - Z.mean(0)) / sd
        B = np.column_stack([np.ones(len(pool)), Z / pi[:, None]])
        loc = cube_sample(pi, B, rng)
        selected.extend(pool[loc].tolist())
        # HT balance diagnostic on standardized kernel features.
        ht = (Z[loc] / pi[loc, None]).sum(0)
        total = Z.sum(0)
        balerr.append(float(np.linalg.norm((ht - total) / len(pool))))
    return np.asarray(selected, int), float(np.mean(balerr))


def _pivotal_pair_update(p, i, j, rng, tol=1e-12):
    a, b = float(p[i]), float(p[j])
    s = a + b
    if s < 1.0 - tol:
        if s <= tol:
            p[i] = p[j] = 0.0
        elif rng.random() < a / s:
            p[i], p[j] = s, 0.0
        else:
            p[i], p[j] = 0.0, s
    elif s > 1.0 + tol:
        prob_i_one = (1.0 - b) / (2.0 - s)
        if rng.random() < prob_i_one:
            p[i], p[j] = 1.0, s - 1.0
        else:
            p[i], p[j] = s - 1.0, 1.0
    else:
        if rng.random() < a / s:
            p[i], p[j] = 1.0, 0.0
        else:
            p[i], p[j] = 0.0, 1.0
    p[i] = 0.0 if p[i] < tol else (1.0 if p[i] > 1.0 - tol else p[i])
    p[j] = 0.0 if p[j] < tol else (1.0 if p[j] > 1.0 - tol else p[j])


def local_pivotal_sample(pi, coords, rng, k_neighbors=32):
    """Approximate local pivotal sampling preserving first-order inclusion probabilities.

    Pair updates are exact pivotal updates. Locality is induced by pairing a random
    active unit with its nearest still-active neighbor from a precomputed kNN list;
    a direct fallback is used when the local list is exhausted.
    """
    pi = np.asarray(pi, float)
    p = pi.copy()
    coords = np.asarray(coords, float)
    N = len(p)
    k = min(max(2, int(k_neighbors) + 1), N)
    tree = cKDTree(coords)
    _, neigh = tree.query(coords, k=k)
    if k == 1:
        neigh = neigh[:, None]
    while True:
        active = np.flatnonzero((p > 1e-10) & (p < 1 - 1e-10))
        if len(active) <= 1:
            break
        i = int(rng.choice(active))
        aset = set(active.tolist())
        j = None
        for cand in np.atleast_1d(neigh[i])[1:]:
            c = int(cand)
            if c in aset and c != i:
                j = c
                break
        if j is None:
            others = active[active != i]
            d2 = np.sum((coords[others] - coords[i]) ** 2, axis=1)
            j = int(others[np.argmin(d2)])
        _pivotal_pair_update(p, i, j, rng)
    if np.any((p > 1e-8) & (p < 1 - 1e-8)):
        i = int(np.flatnonzero((p > 1e-8) & (p < 1 - 1e-8))[0])
        p[i] = float(rng.random() < p[i])
    s = np.flatnonzero(p > 0.5)
    target = int(round(pi.sum()))
    if len(s) != target:
        # Should be extremely rare; use randomized rounding only as numerical fallback.
        order = np.argsort(-p)
        s = order[:target]
    return np.sort(s)


def stratified_local_pivotal(coords, strata, alloc, pi_full, rng):
    selected = []
    for g, ng in enumerate(np.asarray(alloc, int)):
        pool = np.flatnonzero(strata == g)
        loc = local_pivotal_sample(pi_full[pool], coords[pool], rng)
        if len(loc) != int(ng):
            raise RuntimeError("local pivotal sample size mismatch")
        selected.extend(pool[loc].tolist())
    return np.asarray(selected, int)

from .cube import _step as _cube_step

def local_cube_sample(pi, spread_coords, balance, rng, k_neighbors=64, tol=1e-10):
    """Local cube: prescribed first-order pi, auxiliary balance, and local repulsion.

    At each flight step the cube null-space update is applied to q+1 nearby active
    units, where q is the number of balancing variables. This preserves the cube
    balance equations while making nearby units compete for inclusion.
    """
    p=np.asarray(pi,float).copy(); C=np.asarray(spread_coords,float); B=np.asarray(balance,float)
    if B.ndim==1: B=B[:,None]
    q=B.shape[1]
    N=len(p)
    k=min(N,max(q+2,int(k_neighbors)))
    tree=cKDTree(C)
    _, neigh=tree.query(C,k=k)
    if k==1: neigh=neigh[:,None]
    guard=0
    while True:
        active=np.flatnonzero((p>tol)&(p<1-tol))
        if len(active)<=q: break
        pivot=int(rng.choice(active)); aset=set(active.tolist())
        cluster=[pivot]
        for cand in np.atleast_1d(neigh[pivot])[1:]:
            cc=int(cand)
            if cc in aset and cc!=pivot:
                cluster.append(cc)
                if len(cluster)==q+1: break
        if len(cluster)<q+1:
            rem=np.asarray([a for a in active if a not in cluster],int)
            if len(rem):
                d2=np.sum((C[rem]-C[pivot])**2,axis=1)
                need=q+1-len(cluster)
                cluster.extend(rem[np.argsort(d2)[:need]].tolist())
        idx=np.asarray(cluster,int)
        if len(idx)<q+1: break
        M=B[idx].T
        _,_,vh=np.linalg.svd(M,full_matrices=True)
        u=vh[-1]
        if np.linalg.norm(u)<1e-12:
            guard+=1
            if guard>100: break
            continue
        _cube_step(p,idx,u,rng)
        guard=0
    # Local pivotal landing on remaining fractional units; pair nearby residuals.
    while True:
        active=np.flatnonzero((p>tol)&(p<1-tol))
        if len(active)<=1: break
        i=int(rng.choice(active)); others=active[active!=i]
        d2=np.sum((C[others]-C[i])**2,axis=1); j=int(others[np.argmin(d2)])
        _pivotal_pair_update(p,i,j,rng,tol=tol)
    if np.any((p>1e-8)&(p<1-1e-8)):
        i=int(np.flatnonzero((p>1e-8)&(p<1-1e-8))[0]); p[i]=float(rng.random()<p[i])
    s=np.flatnonzero(p>.5); target=int(round(np.sum(pi)))
    if len(s)!=target:
        s=np.argsort(-p)[:target]
    return np.sort(s)


def stratified_local_cube(Xspread, Xphi, strata, alloc, pi_full, rng):
    selected=[]; balerr=[]
    for g,ng in enumerate(np.asarray(alloc,int)):
        pool=np.flatnonzero(strata==g); pi=np.asarray(pi_full[pool],float)
        if abs(pi.sum()-ng)>1e-6: raise ValueError('pi sum mismatch')
        d=min(Xphi.shape[1],max(1,int(ng)-2))
        Z=Xphi[pool,:d].copy(); sd=Z.std(0); sd=np.where(sd<1e-10,1,sd); Z=(Z-Z.mean(0))/sd
        # For cube balancing with unequal pi, use auxiliary x_i/pi_i so that
        # sum_{sample} x_i/pi_i targets the population auxiliary total.
        B=np.column_stack([np.ones(len(pool)), Z/pi[:,None]])
        loc=local_cube_sample(pi,Xspread[pool],B,rng)
        if len(loc)!=int(ng): raise RuntimeError('local cube size mismatch')
        selected.extend(pool[loc].tolist())
        ht=(Z[loc]/pi[loc,None]).sum(0); total=Z.sum(0)
        balerr.append(float(np.linalg.norm((ht-total)/len(pool))))
    return np.asarray(selected,int),float(np.mean(balerr))

def novelty_inclusion_probabilities_exp(strata, alloc, novelty, lam=3.0, min_fraction=0.35):
    """Exponential novelty PPS tilt with a positive probability floor."""
    full=np.zeros(len(strata),float)
    for g,ng in enumerate(np.asarray(alloc,int)):
        pool=np.flatnonzero(strata==g)
        if ng<=0: continue
        z=np.asarray(novelty[pool],float)
        score=np.exp(float(lam)*(z-z.mean()))
        full[pool]=_capped_inclusion(score,int(ng),min_fraction=min_fraction)
    return full

def deterministic_novelty_sentinels(Xs, novelty, m=3, h=None, novelty_weight=0.55):
    """Outcome-blind certainty sentinels: novelty + maximin kernel-space coverage."""
    Xs=np.asarray(Xs,float); novelty=np.asarray(novelty,float)
    if m<=0: return np.empty(0,dtype=int)
    # Rank-normalize novelty to [0,1].
    nr=np.argsort(np.argsort(novelty))/(len(novelty)-1 if len(novelty)>1 else 1)
    # novelty is already high for rare units; ranking above preserves direction.
    selected=[]
    for k in range(int(m)):
        if not selected:
            score=nr.copy()
        else:
            d=np.sqrt(((Xs[:,None,:]-Xs[np.asarray(selected)][None,:,:])**2).sum(2)).min(1)
            dr=np.argsort(np.argsort(d))/(len(d)-1 if len(d)>1 else 1)
            score=novelty_weight*nr+(1-novelty_weight)*dr
        if selected: score[np.asarray(selected)]=-np.inf
        selected.append(int(np.argmax(score)))
    return np.asarray(selected,int)


def certainty_augmented_local_cube(Xspread,Xphi,strata,alloc,novelty,rng,m_certainty=3,lam=3.0,min_fraction=.35):
    """Select m outcome-blind certainty sentinels (pi=1) plus local-cube probability remainder."""
    cert=deterministic_novelty_sentinels(Xspread,novelty,m=m_certainty)
    pi_full=np.zeros(len(strata),float); pi_full[cert]=1.0; selected=cert.tolist(); balerr=[]
    for g,ng in enumerate(np.asarray(alloc,int)):
        pool_all=np.flatnonzero(strata==g); c=np.intersect1d(pool_all,cert,assume_unique=False); nr=int(ng)-len(c)
        pool=np.setdiff1d(pool_all,cert,assume_unique=False)
        if nr<0: raise RuntimeError('too many certainty units in a stratum')
        if nr==0: continue
        z=np.asarray(novelty[pool],float); score=np.exp(float(lam)*(z-z.mean()))
        pi=_capped_inclusion(score,nr,min_fraction=min_fraction); pi_full[pool]=pi
        d=min(Xphi.shape[1],max(1,nr-2)); Z=Xphi[pool,:d].copy(); sd=Z.std(0); sd=np.where(sd<1e-10,1,sd); Z=(Z-Z.mean(0))/sd
        B=np.column_stack([np.ones(len(pool)),Z/pi[:,None]])
        loc=local_cube_sample(pi,Xspread[pool],B,rng)
        selected.extend(pool[loc].tolist())
        ht=(Z[loc]/pi[loc,None]).sum(0); total=Z.sum(0); balerr.append(float(np.linalg.norm((ht-total)/len(pool))))
    sel=np.asarray(selected,int)
    if len(sel)!=int(np.sum(alloc)): raise RuntimeError(f'certainty-augmented size mismatch {len(sel)}')
    return sel,pi_full,float(np.mean(balerr) if balerr else 0.0),cert
