
Under a budget, select exactly $M$ conditions from $\mathcal P$, run $n$ Bernoulli trials per condition, estimate $P^*$, and attach an uncertainty statement. In deployment, $p(\cdot)$ and $P^*$ are unknown. In the controlled evaluation used here, reference response surfaces supply $p(\cdot)$ so that design error can be measured directly.

The design requires an explicit support condition. Partition both the target reference and candidate pool by the same feature-side strata $\mathcal S_\ell$. If the target mass $w_\ell=\Pr_\pi(X\in\mathcal S_\ell)$ is positive but the candidate pool contains fewer than $m_{\min}$ conditions in that stratum, KTES returns a **support violation** and requests additional candidate generation/testing. It does not renormalize the remaining target mass, because doing so changes the estimand. This is a coarse stratified positivity check; it does not prove full within-stratum support in continuous feature space, which remains a limitation.

Three properties distinguish the task from test-set construction [2]: (1) the object is a weighted estimator and can be scored against $P^*$ in controlled validation; (2) rare target strata may require explicit quota protection; and (3) T&E ultimately acts on threshold decisions, so point error, interval behaviour, and accept/reject/inconclusive outcomes are evaluated separately.

---

## IV. The KTES Method

### A. Overview and naming

KTES proceeds in three steps:

$$
\underbrace{\text{stratify}}_{\text{IV-B}}
\;\to\;
\underbrace{\text{select}}_{\text{IV-B}}
\;\to\;
\underbrace{\text{align}}_{\text{IV-C}}
\;\to\;
\underbrace{\text{intervals}}_{\text{IV-E}} .
$$

The estimator is

$$
\hat P \;=\; \sum_{m=1}^{M}\lambda_m\,\hat p_{(m)},
\qquad \hat p_{(m)}=\frac1n\sum_{j=1}^{n} y_{mj},
\tag{2}
$$

with $y_{mj}\in\{0,1\}$ the outcome of trial $j$ on condition $m$ and $\lambda\ge0$, $\sum_m\lambda_m=1$.

Because several ablation variants appear throughout, Table I fixes the naming used everywhere in this paper.

**TABLE I.** Variant naming used throughout this paper.

| Name | Selection | Weights | Stratified? | Role |
|---|---|---|---|---|
| **KTES** (recommended) | random within strata | $\lambda$, adaptive $\tau$ (IV-D) | yes | main method |
| KTES-IP | IP-coverage ordering | $\lambda$, fixed $\tau=0.03$ | yes | parent-framework ablation |
| KTES-U | random within strata | uniform $1/m_\ell$ per stratum | yes | ablation (weighting off) |
| KTES-R | uniform random | $\lambda$ | no | ablation (stratification off) |
| SRS (Uniform) | uniform random | uniform $1/M$ | no | baseline |
| SRS-IS | uniform random | post-hoc importance weights | no | baseline (Fig. 1 only) |
| LHS / GMM | space-filling | uniform | no | baselines (Section V-C) |

The information-potential (IP) coverage step inherited from KTCS re-orders candidates by an entropy-regularized k-means coverage objective before Pareto-indexed sampling; it is retained only inside the KTES-IP ablation arm.

### B. Stratified selection

*Motivation.* Stratification and kernel alignment serve different roles. Stratification reserves candidate capacity for target-relevant strata; alignment controls the weighted distribution represented by the selected points. The IP-coverage ordering inherited from KTCS is therefore not part of the recommended estimator.

*Construction.* Partition the candidate pool into $L$ strata $\{\mathcal P_\ell\}$ using a feature-side criticality score $s(x)$, and define target stratum mass

$$
w_\ell=\sum_{i:r_i\in\mathcal S_\ell}\pi_i,\qquad \sum_{\ell=1}^{L}w_\ell=1.
\tag{3}
$$

Integer quotas start from $\mathrm{round}(w_\ell M)$, are clamped to the minimum-per-stratum floor and available-pool cap, and are then deterministically corrected one unit at a time until $\sum_\ell m_\ell=M$. This is an **exact-budget quota correction**, not a largest-remainder claim. If a target-positive stratum contains fewer than $m_{\min}$ candidate conditions, KTES fails closed. Otherwise $m_\ell$ conditions are sampled uniformly without replacement within each stratum. The score $s(x)$ uses features only, never observed outcomes; in the demonstrations it is tool-wear times torque for AI4I, feature-space distance for Steel Plates and SECOM, and a weighted combination of range, environment, and target size for the ballistic surface.

The frozen protocol selects exactly $M=50$ conditions on every dataset. Contract tests over 10 seeds recover quotas 48/2 for AI4I, Steel, and SECOM and 41/4/3/2 for the four ballistic environment strata, with selected count exactly 50 in every run. Stratification is not claimed to be universally beneficial: its role is quota protection, while the weighting ablations determine whether alignment itself carries the estimation gain.

**ALGORITHM 1.** KTES selection and weighting (frozen protocol).

```text
Input: candidate pool P, target-reference strata R_l and weights pi_l,
       target stratum masses w_l, budget M, ESS ratio eta,
       grid {tau_k}, m_min = 2
1  quotas = exact_budget_quotas(w_l, |P_l|, M, m_min)
2  if any target-positive l has |P_l| < m_min:
3      raise SupportViolation(l)              # fail closed
4  for each stratum l:
5      draw quotas[l] candidate conditions uniformly from P_l
6      for tau_k in increasing order:
7          align selected points to (R_l, pi_l) by Eq. (5)
8          stop at first N_eff(lambda_l) >= eta * quotas[l]
9      append w_l * normalized(lambda_l)
10 return selected conditions and globally normalized lambda
```

### C. Alignment weights

Let $Z_\ell=\{z_m\}$ be the selected conditions in stratum $\ell$, and let $R_\ell=\{r_i:r_i\in\mathcal S_\ell\}$ be the corresponding target-reference conditions. With an RBF kernel $K$, solve

$$
\begin{gathered}
