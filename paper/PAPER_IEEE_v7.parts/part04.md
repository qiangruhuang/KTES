
### G. Complexity

With the coverage module deleted, selection costs $O(M)$ for within-stratum sampling; the simplex QP (4) is solved by SLSQP at $O(m_\ell^3)$ per stratum; the adaptive search re-solves at most $|\{\tau_k\}|$ times. The QP needs the $m_\ell\times m_\ell$ kernel $K_{ZZ}$ and the $m_\ell\times|\mathcal{P}_\ell|$ reference kernel, both millisecond-scale at $M=50$; the dominant cost of the retained IP module (KTES-IP arm) is the entropy-regularized k-means, $O(\mathrm{iter}\cdot k\cdot N)$ per selection. The k-means clustering and iterative weight optimization of the parent framework are otherwise gone.

---

## V. Experimental Protocol

### A. Datasets and ground truth

Three public benchmarks and one physics surface, spanning scale, dimensionality, and noise:

**TABLE II.** Datasets. $P^*$ is the $\pi$-weighted pool mean; for the three benchmarks $\pi$ is uniform over the pool.

| Dataset | $N$ | $d$ | Response | Ground truth | Note |
|---|---|---|---|---|---|
| AI4I 2020 (UCI 601) [25] | 10000 | 8 | machine failure | 5-fold OOF logistic-regression probability | failure 3.39% |
| Steel Plates (UCI 198) [26] | 1941 | 33 | defect | same | OOF AUC 1.000, near-deterministic |
| SECOM (UCI 179) [27] | 1567 | 446 | pass/fail | same | real high-dimensional, OOF AUC 0.653 |
| Multi-env ballistic surface | 2000 | 10 | hit | physics model (10) | Section IV-F |

The benchmark "ground truth" is the out-of-fold (OOF) cross-validated predicted probability over the full pool, which avoids leakage from the label itself (the five label-decomposition columns of AI4I are dropped). These are therefore *semi-synthetic* surfaces, a limitation stated in Section VII-C: the analytic metrics inherit this truth as exact, so an additional truth-estimation error term is unaccounted; Section VI-H quantifies the consequence by regenerating the truth with a different learner. The ballistic pool is sampled from the operational scenario, so pool $=\pi$ for it by construction.

### B. Fairness protocol and metrics

Two rules are binding; the project violated each once during internal audit and obtained a wrong conclusion both times, which is why they are stated as rules.

> **Rule 1 (fairness).** When comparing randomized methods, *all* methods must re-select on the *same* random seeds. Randomizing only some methods compares their single realization against a 50-realization average of the baseline and inflates the novel method (measured inflation here: a factor of 2).
>
> **Rule 2 (sample size).** Replications must be sufficient. On AI4I, SRS's mean absolute relative design error is 0.0967 at REP = 10 but 0.1421 at REP = 50; the two support opposite conclusions because the per-seed spread of SRS is large (sd 0.125).

*Metrics.* With $\mathbb{E}[\hat P]=\sum_m\lambda_m p_{(m)}$ from (8), define the *relative design error* of one selection seed and its mean over seeds,

$$
\mathrm{RE}(s)=\frac{\big|\mathbb{E}_s[\hat P]-P^*\big|}{P^*},
\qquad
\mathrm{MARE}=\frac1S\sum_{s=1}^{S}\mathrm{RE}(s),
\tag{12}
$$

and the analytic RMSE $\sqrt{(\mathbb{E}_s[\hat P]-P^*)^2+\mathrm{Var}[\hat P]}$. Both are *analytic*: they contain no shot noise, because the expectation is taken over the known ground-truth responses. MARE is an MAE-type loss over design seeds; it mixes signed design bias with design variance. This matters for interpretation: on the three benchmarks, $\pi$ is the pool mean and SRS is marginally design-unbiased, so its MARE (0.1421 on AI4I) is entirely selection variability, not bias in the statistical sense. We report MARE because it is the quantity a practitioner's selection procedure experiences; the signed bias of SRS is approximately zero on the benchmarks by construction, and the phase diagram of Section VI-D is where genuine pool bias is induced and measured. All frozen KTES headline experiments use the exact-budget quota correction of Algorithm 1 ($\sum_\ell m_\ell=M$), so KTES and SRS each operate on exactly $M=50$ selected conditions. Legacy IP ablations are identified separately when they do not use the frozen protocol. Coverage is estimated by Monte Carlo shot resampling, with $R=300$ resamples per design seed averaged over 50 design seeds in the main tables, and $R=3000$ on a single fixed design in the calibration study of Section VI-E. All comparisons report *both* the mean and the paired per-seed win rate (fraction of the $S$ seeds on which a method's RE is lower).

### C. Baselines and a fairness caveat about them

SRS is the primary baseline; SRS-IS (random selection with post-hoc importance weights) is used in the source-pool shift experiments of Section VI-G to isolate a direct reweighting alternative. LHS (nearest-neighbor mapping of a Latin hypercube sample onto the pool) and greedy maximin-distance (GMM) designs optimize geometric spread. Empirically their relative design errors are 3.0$\times$ and 7.5$\times$ that of SRS on AI4I, far worse than a competent design of this class should be for response-surface purposes, which is expected here because the estimand is not a response surface: their objectives are misaligned with weighted estimation by construction (Section II-C). We therefore treat LHS and GMM as protocol calibration rather than headline comparisons, and we do not claim "dominance" over them. The baselines that probe KTES's nearest neighbours are already present under the Table I nomenclature: the "stratified SRS with target stratum weights" comparator is KTES-U (post-stratification weighting with $\pi$-proportional quotas), and the "SRS with kernel/calibration balancing weights under the same ESS floor" comparator is KTES-R (uniform random selection plus MMD alignment under the identical $\eta$ constraint). KLIEP-style direct density-ratio weighting differs from KTES-R only in how the ratio is estimated, and we claim no novelty for the weighting step itself (Section II-B); KTES-R is therefore the operative kernel-balancing baseline, and Section VI-G reports where it wins.

---

## VI. Results

Unless stated otherwise: $M=50$, $n=10$, main seed 42, all methods re-select on the same seeds per replication (Rule 1), analytic metrics, $P^*$ defined on the target distribution.

### A. Main comparison

**Table III** fixes the exact budget at $M=50$, $n=10$, $\eta=0.6$, and REP = 50 paired selection seeds.

**TABLE III.** Frozen-protocol main comparison. MARE is mean $\pm$ sd across 50 paired selection seeds. Signed error is the mean signed relative design error. $\mathrm{cov}_f$ and $\mathrm{cov}_{BK}$ are design-averaged empirical coverages of the plug-in Wald and Bayes-Kish constructions over the same 50 designs with $R=300$ shot resamples per design.

| Dataset | SRS MARE | KTES MARE | Reduction | Signed (SRS / KTES) | RMSE (SRS / KTES) | Win rate | $N_{\mathrm{eff}}$ (KTES) | $\mathrm{cov}_f$ (SRS / KTES) | $\mathrm{cov}_{BK}$ (SRS / KTES) |
|---|---|---:|---:|---|---|---:|---:|---|---|
| AI4I 2020 | 0.1421 $\pm$ 0.1248 | **0.0713 $\pm$ 0.0671** | 49.8% | +0.017 / $-0.004$ | 0.00973 / 0.00992 | 66% | 32.2 | 0.857 / 0.890 | 0.896 / 0.951 |
| Steel Plates | 0.0573 $\pm$ 0.0424 | **0.0259 $\pm$ 0.0288** | 54.8% | $-0.007$ / $-0.018$ | 0.03929 / 0.02228 | 68% | 31.1 | 0.267 / 0.645 | 0.658 / 0.939 |
| SECOM | 0.0363 $\pm$ 0.0245 | **0.0216 $\pm$ 0.0157** | 40.5% | +0.005 / $-0.008$ | 0.01143 / 0.01373 | 66% | 32.2 | 0.921 / 0.918 | 0.946 / 0.954 |
| Ballistic surface | 0.0851 $\pm$ 0.0663 | **0.0440 $\pm$ 0.0350** | 48.4% | +0.021 / +0.000 | 0.00519 / 0.00598 | 72% | 35.4 | 0.868 / 0.864 | 0.951 / 0.951 |

The mean paired KTES$-$SRS differences are $-0.0708$ (95% CI $[-0.1133,-0.0284]$) on AI4I, $-0.0314$ $[-0.0475,-0.0153]$ on Steel Plates, $-0.0147$ $[-0.0228,-0.0067]$ on SECOM, and $-0.0412$ $[-0.0615,-0.0209]$ on the ballistic surface. Because SRS has heavy-tailed seedwise error, we also report bootstrap intervals for the paired median: $-0.0555$ $[-0.1042,-0.0089]$, $-0.0251$ $[-0.0478,-0.0089]$, $-0.0113$ $[-0.0236,-0.0017]$, and $-0.0284$ $[-0.0631,-0.0061]$, respectively. Both summaries favour KTES in all four cases, but win rates remain 66–72%, so the method is not uniformly better on every realized design.

For the three public benchmarks, SRS is marginally design-unbiased because the benchmark pool is the target population. Their MARE reductions therefore measure **selection-variability control**, not correction of a population-selection bias. The coverage columns are empirical properties of the stated constructions, not inferential guarantees; in particular, the interval model omits design error as discussed in Sections VI-E and VI-G.

### B. Ablation: selection and weighting are separable, and only weighting is load-bearing

**Table IV** is the orthogonal four-cell decomposition on AI4I (20 seeds, analytic metrics): selection $\in$ {random, IP-coverage} $\times$ weighting $\in$ {uniform, unconstrained $\lambda$ ($\tau=0$)}.

**TABLE IV.** Four-cell ablation on AI4I (20 seeds, $\tau=0$ for $\lambda$ arms).

| Selection | Weighting | MARE | Analytic RMSE | $N_{\mathrm{eff}}$ |
|---|---|---|---|---|
| Random | uniform | 0.1252 $\pm$ 0.0915 | 0.00918 | 50.0 |
| Random | $\lambda$ | **0.0605** $\pm$ 0.0645 | 0.01284 | 19.6 |
| IP-coverage | uniform | 0.1840 $\pm$ 0.1214 | 0.01056 | 50.0 |
| IP-coverage | $\lambda$ | **0.0613** $\pm$ 0.0482 | 0.01279 | 18.6 |

- *IP coverage can be deleted.* With uniform weights, coverage-ordered selection (0.1840) is *worse* than random selection (0.1252). With $\lambda$ (unconstrained), the two are statistically indistinguishable at this sample size (0.0613 vs 0.0605); an equivalence test at 50 seeds is future work. The four-dataset replication (REP = 50) refines this: IP-coverage is better by mean on three datasets (0.0964 vs 0.1064 on AI4I, 0.0468 vs 0.0508 on Steel Plates, 0.0308 vs 0.0321 on SECOM) but all three paired differences are indistinguishable from zero, while on the scenario-weighted surface random-within-strata is significantly better (0.0549 vs 0.0836; paired difference $-0.029$ $[-0.050,-0.009]$). Deletion therefore costs nothing detectable and helps where it matters most.
- *Weighting is load-bearing.* Pure stratification with uniform weights (KTES-U) is worse than SRS on two of four datasets by mean (Steel Plates 0.0654 vs 0.0573; ballistic 0.0952 vs 0.0851) and better on the other two (AI4I 0.1242 vs 0.1421; SECOM 0.0320 vs 0.0363). Alignment weights, not coverage or quotas, carry the performance.
- *The variance price and its recovery.* Unconstrained $\lambda$ costs 40% RMSE and drops $N_{\mathrm{eff}}$ from 50 to about 19; the frozen constrained version of Section IV-D yields RMSE ratios of 0.57–1.20 relative to SRS (Table V), with mean $N_{\mathrm{eff}}$ of 31–35 conditions.

### C. Adaptive concentration vs fixed $\tau$

**Table V** compares fixed $\tau=0.03$ with ESS-constrained searches. The frozen headline value is $\eta=0.6$, selected by the cross-dataset majority of a 25/25 development/evaluation seed split.
