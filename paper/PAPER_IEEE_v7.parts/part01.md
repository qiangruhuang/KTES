# Stratified Kernel-Based Selection of Test Conditions for Scenario-Weighted Effectiveness Estimation in Equipment Test and Evaluation

**Submission draft v2.1 / evidence freeze v7** (Markdown research source; all headline numbers below are tied to the frozen exact-budget, $\eta=0.6$ protocol and the audited JSON outputs in the replication package).

---

**Abstract**—Equipment test and evaluation (T&E) must select a small number of operating conditions from a large candidate pool and estimate a scenario-weighted effectiveness quantity. We adapt the kernel test-case-sampling framework KTCS to this estimation task. The resulting KTES design uses exact-budget stratified quotas, random selection within strata, target-reference kernel alignment, an effective-sample-size (ESS) constraint on the alignment weights, and a fail-closed support check that refuses estimation when a target-positive stratum lacks minimum candidate support. Under the frozen $M=50$, $n=10$, $\eta=0.6$ protocol, KTES lowers mean absolute relative design error by 40.5–54.8% relative to simple random sampling (SRS) across three public benchmark surfaces and one physics surface, with paired win rates of 66–72%; both mean paired 95% intervals and bootstrap median intervals are below zero in all four comparisons. On the public benchmarks this is selection-variability control, not statistical bias correction, and the benchmark truth is semi-synthetic. An outer Monte Carlo over independently resampled source pools shows that KTES reduces error relative to SRS when target support is adequate, but severe under-representation often becomes a support-identification failure rather than a reweighting problem (support violations occur in 95% of AI4I and SECOM pools and 40% of Steel pools at the tested negative-shift setting). Relative performance against post-hoc importance weighting is dataset- and support-dependent, so no directional dominance rule is claimed. A single-design AI4I calibration gives 0.951 empirical coverage for the 95% Kish-scaled pseudo-posterior interval; broader biased-pool experiments show that a model-assisted design-variance term is a sensitivity correction, not an unconditional coverage guarantee. Finally, threshold-decision experiments show that lower estimation error does not uniformly translate into greater accept/reject power at $n=10$. The resulting contribution is a support-aware, evidence-bounded T&E design and synthesis framework rather than a new kernel-weighting algorithm.

**Index Terms**—Covariate shift, effective sample size, importance weighting, interval calibration, kernel methods, small-sample estimation, stratified sampling, test and evaluation.

---

## I. Introduction

### A. Problem

Equipment T&E is the statutory statistical gate between development and fielding. Under the current Chinese military regulation on equipment test and evaluation, the assessment chain comprises five phases: performance testing (性能试验), state assessment (状态鉴定), operational testing (作战试验), fielding approval (列装定型), and in-service evaluation (在役考核) [1]. At every phase the evaluator must answer the same statistical question: *under the prescribed conditions of operational use, does the effectiveness metric meet the threshold?*

Four difficulties make this question hard.

1) *Combinatorial explosion of conditions.* Environment (plain, plateau, hot-humid, cold), range, target posture, and weapon platform jointly exceed $10^3$ combinations, while budgets allow only hundreds to thousands of rounds.

2) *The estimand is a weighted mean.* The operational scenario specifies a distribution $\pi$ over conditions; the quantity to be assessed is $P^*=\mathbb{E}_{x\sim\pi}[p(x)]$, a distribution-weighted expectation, not the hit rate of any single "typical" condition. Throughout the pilot scenarios of this paper we use the illustrative mix plain 82%, plateau 8%, hot-humid 6%, and cold 4%. These are *pilot values for method demonstration* (disclaimer in Section II-E), not the mission profile of any specific fielded system.

3) *The candidate pool is biased.* Historical range data, simulation output, and combat or training records are almost never sampled from $\pi$. Averaging over the pool is therefore systematically off $P^*$.

4) *Data are scarce and heterogeneous.* The per-condition replication $n$ is small, outcomes are Bernoulli, and the success probability itself can be as low as $10^{-2}$, the regime where interval coverage is most fragile.

The problem is thus: *under a budget (choose $M$ conditions, $n$ trials each), select $M$ conditions from the pool so that the estimate of $P^*$ is accurate and its interval conclusion is defensible.*

### B. Why existing practice falls short

Three families of methods are in common use, and each is misaligned with the estimand.

*Simple random sampling (SRS)* is unbiased for the pool, but biased for $P^*$ whenever pool $\neq\pi$, and it provides no quota guarantee for rare but critical strata; individual realizations can omit plateau or cold conditions entirely.

*Stratified sampling* guarantees rare strata are represented, but within-stratum selection rules and the merging of stratum weights usually rest on experience, with no criterion tied to the estimation target.

*Space-filling designs* (Latin hypercube [10], maximin-distance [11], and their descendants) optimize geometric spread in feature space. They serve response-surface modeling and factor screening. For estimating a weighted functional of a possibly biased pool, geometric uniformity guarantees neither weighted unbiasedness nor smaller variance; Our experiments quantify this mismatch (Section VI-A); the comparison is intentionally unfavorable to them, as argued in Section V-C.

More fundamentally, all three families act only on *which points to select* and leave the pool-versus-target shift unaddressed. If the pool is generated by a biased mechanism, no amount of uniform spreading makes its expectation equal $P^*$.

### C. Approach and contributions

We transfer the kernel test-case sampling framework KTCS [2], built for safety validation of automated driving, to a scenario-weighted estimation task and retain only the components supported by controlled evidence.

**C1, retargeted estimand.** KTCS evaluates the representativeness and coverage of a selected test set. KTES instead targets the weighted functional $P^*$, so designs can be compared by estimation error and by downstream qualification decisions.

**C2, structural simplification.** In the orthogonal ablation of Section VI-B, the information-potential (IP) coverage step is unnecessary for weighted-mean estimation, whereas alignment weights are load-bearing. The recommended design therefore uses random selection within strata and retains the alignment step under an ESS constraint.

**C3, exact-budget and support-aware design.** KTES enforces exactly $M$ selected conditions and separates the *candidate pool* from an unlabeled *target-reference set* representing $\pi$. A target-positive stratum with fewer than $m_{\min}$ candidate conditions triggers a support violation rather than renormalization. This distinction is operationally important: under-representation with positive support is potentially correctable; missing support is not identified by reweighting alone.

**C4, inference and decision discipline.** The regularization target is frozen at $\eta=0.6$ from a held-out seed split; uncertainty is reported at both the selection-seed and source-pool levels; the Kish-scaled interval is explicitly a conditional pseudo-posterior construction; and a threshold-decision experiment tests whether lower estimation error translates into more useful accept/reject conclusions.

We frame the contribution as a **task-level recombination with an evidence-mapped boundary**, not as a new kernel-weighting algorithm. Under the frozen exact-budget protocol, KTES reduces MARE by 40.5–54.8% relative to SRS, with paired win rates of 66–72%. All four mean paired 95% intervals and bootstrap median intervals favour KTES, but the semi-synthetic truth surfaces, support failures under severe shift, and weak decision power in low-probability cases delimit what those reductions imply.

---

## II. Related Work

### A. Scenario-based safety validation and test-case sampling

KTCS [2] selects test cases from large-scale naturalistic driving data by two criteria, representativeness (consistency with the real driving distribution) and coverage (capturing high-risk corner cases), and is the direct parent of this work. Its scenario-based evaluation philosophy is codified in ISO 21448 (SOTIF) [3] and ISO 34502 [4]; related Chinese work generates high-coverage scenario libraries from naturalistic data [5]. In the autonomous-vehicle literature, accelerated evaluation by importance sampling reweights skewed test samples to recover naturalistic-distribution performance [30], and rare-event probability estimation quantifies how much testing is needed for statistical acceptance [31]. All of these score the *selected set*; none targets a weighted mean with a known ground truth. Our contribution is to place the same selection machinery under an estimation objective and report what survives (Section VI-B).

### B. Importance weighting, covariate shift, and kernel methods

When the pool distribution differs from the target $\pi$, the standard remedy is importance weighting. Kernel mean matching (KMM) solves for sample weights by matching RKHS means [7]; direct density-ratio estimation includes KLIEP [8]; the maximum mean discrepancy (MMD) provides the underlying two-sample framework [6]. In survey statistics, calibration weighting obtains weights by constrained optimization [33], and inference from nonprobability samples is an active topic [32], [34]. Kish's effective sample size $N_{\mathrm{eff}}=(\sum_i w_i)^2/\sum_i w_i^2$ is the classical measure of variance inflation under unequal weighting [9], and its role in self-normalized importance sampling is quantified in [35]. Our $\lambda$ solves an MMD-alignment problem on the probability simplex. The increment here is to price the *cost* of those weights in Kish effective sample size and to turn that price into a design-time constraint (Section IV-D). We also note the known caveat that design effects are biased when weights correlate with the outcome [36], which is exactly the regime KTES constructs (Section VII-C).

### C. Space-filling designs

Latin hypercube sampling [10] and maximin-distance criteria [11] are foundational tools of computer-experiment design, aimed at response-surface fitting and factor screening. We include them as baselines and show that, for a weighted-mean estimand on a biased pool, geometric spread brings no advantage; the reason is structural: pool bias is an error in the *weighting* dimension, orthogonal to geometric fill.

### D. Small-sample reliability assessment and interval estimation

Interval estimation for binomial proportions has a long literature, from Clopper-Pearson [12] and Wilson [13] to the systematic comparison in [14]. Bayesian assessment for one-shot and count data is also established in reliability engineering. Relevant defense-oriented work includes finite-population reliability demonstration testing [19], reliability-growth-informed qualification plans [20], inheritance-factor Bayes assessment for pass/fail products and missile systems [21], [22], small-sample test-size and risk calculations [23], and multi-source reliability/maintainability verification under small samples [24]. Series-system reliability with very small binomial samples is treated in [18]. These methods primarily address inference or acceptance for a specified test population. KTES addresses the upstream design problem of which conditions to test and how to synthesize them toward a prescribed scenario-weighted estimand; the interval construction in Section IV-E is deliberately presented as a calibrated engineering approximation rather than as a new Bayesian posterior theory.

### E. The T&E process and data acceptance

The five-phase chain and its decision vocabulary are fixed by regulation [1]; state-assessment conclusions and fielding-approval conclusions are specified in [15], [16]; the acceptance of test, simulation, and historical data is governed by [17]. KTES is designed to sit between two nodes of that chain: as a *statistical design tool for condition selection* in performance and operational testing (stratified quotas plus alignment), and as a *weighted-synthesis and interval tool* after data acceptance (dual-paradigm intervals with the Kish correction). Design-of-experiments guidance for operational testing [37] argues for structuring tests across the operating envelope, consistent with our stratification step; however, we are not aware of established practice that combines scenario-weighted estimation with kernel-based condition selection, and we phrase our positioning accordingly. **Pilot-scenario disclaimer.** The multi-environment mix (82/8/6/4) and the environment factors used in the physical case are pilot values set for method demonstration; in operational use they must come from the system's operational-mission documents.

---

## III. Problem Formulation

Let $\mathcal R=\{r_i\}_{i=1}^{N_R}$ denote an unlabeled **target-reference frame** representing the operational scenario, with target weights $\pi_i\ge0$, $\sum_i\pi_i=1$. Let $\mathcal P=\{x_j\}_{j=1}^{N_P}$ denote the **candidate pool** from which test conditions can actually be selected. The two sets coincide on the unbiased benchmark experiments but may differ when the candidate pool is generated by proving-ground practice, simulation, or historical records. Each condition $x$ has an unknown repeated-trial success probability $p(x)$. The target estimand is

$$
P^* \;=\; \sum_{i=1}^{N_R}\pi_i p(r_i).
\tag{1}
$$
