# KTES Research Revision v7 — Evidence Freeze After Adversarial Review

Date: 2026-10-05  
Scope: methodological correction and evidence re-analysis using the uploaded pre-revision code/data package.  
Status: research-content stage; no DOCX/PDF generated.

## 1. Frozen research question

The study evaluates whether a small set of test conditions can support a defensible estimate of a prescribed scenario-weighted effectiveness quantity

\[
P^*=\mathbb E_{x\sim\pi}[p(x)]
\]

when candidate test conditions may be distributed differently from the operational target distribution. The revised method is treated as a **support-aware target-alignment workflow for T&E**, not as a novel kernel-weighting algorithm.

The frozen primary comparison is KTES versus simple random sampling (SRS) under:

- exactly \(M=50\) selected conditions for every method;
- \(n=10\) Bernoulli trials per selected condition;
- random selection within target-defined strata;
- kernel alignment to an unlabeled target-reference distribution;
- adaptive weight regularization with frozen \(\eta=0.6\);
- fail-closed support checking for target-positive strata;
- 50 paired selection seeds for the main comparison.

## 2. Corrections made to the research protocol

### 2.1 Candidate pool and target reference are now distinct objects

The original implementation and manuscript mixed two meanings of the alignment reference: the candidate pool and the operational target distribution. The revised contract separates:

- **candidate pool \(\mathcal P\)**: conditions that can actually be selected for testing;
- **target reference \(\mathcal R\sim\pi\)**: unlabeled scenario conditions or a finite scenario grid describing the operational target distribution.

Within stratum \(\ell\), selected points are aligned to the target-reference measure \((R_\ell,\pi_\ell)\). When pool = target, the pool itself is a valid target reference and the within-stratum reference is uniform. The core `ktes_v2_select` interface now also supports an explicit per-stratum `ref_X` together with `ref_weights`.

### 2.2 Exact condition budget

The previous rounding rule could yield more than 50 selected conditions. The frozen algorithm now uses deterministic quota correction until

\[
\sum_\ell m_\ell=M=50.
\]

The implementation is described as an **exact-budget quota correction**; the earlier “largest-remainder” label was removed because the code did not implement the classical largest-remainder algorithm.

### 2.3 Support failures are fail-closed

A target-positive stratum with fewer than \(m_{\min}=2\) candidate conditions is no longer skipped and renormalized. It raises `SupportViolationError`. Renormalizing surviving strata would redefine the estimand rather than estimate the original \(P^*\).

This produces an important methodological distinction:

- under-representation with positive support can be addressed by design and reweighting;
- missing support is an identification failure and requires additional candidate generation/testing.

The current test is stratum-level and therefore does not prove full high-dimensional positivity within a stratum.

### 2.4 Regularization frozen before headline evaluation

The held-out 25/25 seed split gives a per-dataset development choice of \(\eta=0.6\) for Steel, SECOM, and ballistic and \(\eta=0.7\) for AI4I. The cross-dataset majority rule freezes \(\eta=0.6\) for all headline analyses.

Evaluation-seed MARE differences for \(\eta=0.7-0.6\) are:

| Dataset | Evaluation MARE at selected \(\eta\) | Evaluation MARE at 0.7 | Difference |
|---|---:|---:|---:|
| AI4I | 0.0688 | 0.0688 | 0.0000 |
| Steel | 0.0308 | 0.0380 | +0.0072 ± 0.0032 |
| SECOM | 0.0232 | 0.0247 | +0.0016 ± 0.0009 |
| Ballistic | 0.0435 | 0.0453 | +0.0018 ± 0.0025 |

A nested optimization over all design parameters is not claimed.

## 3. Contract verification

`validate_contracts.py` was rerun after the code correction.

| Check | Result |
|---|---|
| exact budget \(M=50\) | PASS |
| default uniform reference = explicit uniform reference | PASS |
| fail-closed support violation | PASS |

Observed frozen quotas are 48/2 for AI4I, Steel, and SECOM and 41/4/3/2 for the ballistic environment strata. The maximum numerical difference between default and explicitly supplied uniform-reference alignment weights is \(4.01\times10^{-11}\).

## 4. Frozen primary results

### 4.1 Estimation error

| Dataset | SRS MARE | KTES MARE | Reduction | Win rate | Mean paired KTES−SRS [95% CI] | Median paired difference [bootstrap 95% CI] |
|---|---:|---:|---:|---:|---|---|
| AI4I | 0.1421 | 0.0713 | 49.8% | 66% | −0.0708 [−0.1133, −0.0284] | −0.0555 [−0.1042, −0.0089] |
| Steel | 0.0573 | 0.0259 | 54.8% | 68% | −0.0314 [−0.0475, −0.0153] | −0.0251 [−0.0478, −0.0089] |
| SECOM | 0.0363 | 0.0216 | 40.5% | 66% | −0.0147 [−0.0228, −0.0067] | −0.0113 [−0.0236, −0.0017] |
| Ballistic | 0.0851 | 0.0440 | 48.4% | 72% | −0.0412 [−0.0615, −0.0209] | −0.0284 [−0.0631, −0.0061] |

Both paired-mean and paired-median summaries favour KTES in all four frozen comparisons. The per-seed win rates remain only 66–72%, so the result does not mean that KTES wins every realized design.

For the three public benchmark rows, pool = target. SRS is therefore marginally design-unbiased, and the MARE reduction measures **selection variability**, not population-bias correction.

### 4.2 RMSE and ESS

| Dataset | RMSE SRS | RMSE KTES | KTES/SRS | KTES mean \(N_{eff}\) |
|---|---:|---:|---:|---:|
| AI4I | 0.00973 | 0.00992 | 1.02 | 32.2 |
| Steel | 0.03929 | 0.02228 | 0.57 | 31.1 |
| SECOM | 0.01143 | 0.01373 | 1.20 | 32.2 |
| Ballistic | 0.00519 | 0.00598 | 1.15 | 35.4 |

The ESS constraint controls the variance cost of alignment but does not eliminate it. This replaces the earlier blanket claim that the variance penalty was “recovered” across all datasets.

## 5. Interval evidence

### 5.1 Fixed-design calibration

On one fixed AI4I design (3000 shot resamples), empirical 95% coverage is:

| Construction | KTES | SRS |
|---|---:|---:|
| Wald plug-in | 0.899 | 0.647 |
| Wald + Jeffreys variance | 0.990 | 0.912 |
| logit-Wald | 0.926 | 0.763 |
| nominal-\(n\) Beta, uniform prior | 1.000 | 1.000 |
| nominal-\(n\) Beta, Jeffreys prior | 1.000 | 1.000 |
| Bayes-Kish | 0.951 | 0.764 |
| Wald-Kish | 0.927 | 0.651 |

The Bayes-Kish result supports a **conditional empirical calibration** on this design. It is not a Bayesian conjugate posterior for heterogeneous Bernoulli conditions and is not an unconditional 95% guarantee.

### 5.2 Coverage under induced pool shift

For KTES, Bayes-Kish coverage across the angular-error shift experiment is 0.954, 0.967, 0.969, 0.957, 0.935, 0.901, and 0.868 from \(\beta=-1.5\) to +1.5. The model-assisted design-variance correction raises coverage to 0.982/0.981/0.965 for \(\beta=-1.5/-1/-0.5\), but yields 0.880 and 0.833 at +1/+1.5.

The revised conclusion is therefore:

> the design term can improve coverage when omitted design variance dominates; it cannot repair signed bias and is retained as a sensitivity correction rather than a primary interval guarantee.

## 6. Source-pool uncertainty and support audit

The earlier biased-pool analysis drew each candidate pool once and varied only selection seeds. The revised experiment uses 20 independent source pools per dataset-shift cell and two paired selection seeds within each pool. Inference is across source pools.

| Dataset | \(\beta\) | Support-fail rate | SRS MARE | SRS-IS | KTES* | KTES−SRS [95% CI] | KTES−SRS-IS [95% CI] |
|---|---:|---:|---:|---:|---:|---|---|
| AI4I | −1 | 95% | 0.485 | 0.321 | 0.080 | −0.340 (1 supported pool) | −0.184 (1 supported pool) |
| AI4I | 0 | 0% | 0.148 | 0.148 | 0.078 | −0.070 [−0.120, −0.020] | −0.070 [−0.120, −0.020] |
| AI4I | +1 | 0% | 0.997 | **0.138** | 0.311 | −0.686 [−0.803, −0.569] | **+0.173 [+0.091, +0.255]** |
| Steel | −1 | 40% | 0.153 | 0.176 | 0.058 | −0.099 [−0.143, −0.054] | −0.119 [−0.159, −0.079] |
| Steel | 0 | 0% | 0.075 | 0.075 | 0.027 | −0.047 [−0.071, −0.024] | −0.047 [−0.071, −0.024] |
| Steel | +1 | 0% | 0.174 | 0.173 | **0.079** | −0.095 [−0.121, −0.070] | −0.094 [−0.140, −0.049] |
| SECOM | −1 | 95% | 0.042 | 0.098 | 0.020 | −0.032 (1 supported pool) | −0.042 (1 supported pool) |
| SECOM | 0 | 0% | 0.038 | 0.038 | 0.026 | −0.013 [−0.024, −0.001] | −0.013 [−0.024, −0.001] |
| SECOM | +1 | 0% | 0.049 | 0.037 | **0.022** | −0.027 [−0.040, −0.014] | −0.015 [−0.025, −0.004] |
| Ballistic | −1 | 0% | 0.571 | 0.143 | **0.099** | −0.472 [−0.540, −0.403] | −0.044 [−0.113, +0.025] |
| Ballistic | 0 | 0% | 0.097 | 0.097 | **0.048** | −0.049 [−0.073, −0.024] | −0.049 [−0.073, −0.024] |
| Ballistic | +1 | 0% | 0.518 | 0.208 | **0.140** | −0.378 [−0.410, −0.346] | −0.069 [−0.128, −0.009] |

\*KTES MARE is conditional on pools that pass the support check.

Two previous claims are invalidated:

1. Severe under-representation is not always a regime in which KTES can safely “correct” the pool. In AI4I and SECOM it usually removes the minimum rare-stratum support entirely and therefore triggers fail-closed.
2. The rule “KTES for under-representation, SRS-IS for over-representation” is not supported. AI4I +1 favours SRS-IS, whereas Steel, SECOM, and ballistic +1 favour KTES.

The defensible rule is support-first: verify target support, then compare target-alignment and direct reweighting under the actual candidate-source mechanism.

## 7. Frozen phase diagram and pre-test diagnostics

The phase diagram was rerun with the frozen exact-budget \(\eta=0.6\) protocol on 35 \((\alpha,\beta)\) cells, 10 seeds per cell. KTES MARE is lower than SRS in all 35 controlled cells; the \(\beta=0\) gain is 46.8% on this particular surface.

The proposed field proxies, however, do not survive the protocol freeze strongly:

- \(r(\mathrm{gain},\sigma_{\log\rho})=0.086\);
- \(r(\mathrm{gain},|\mathrm{AUC}-0.5|)=0.340\);
- interaction correlation = 0.217.

These values are too weak to support a quantitative pre-test gain predictor. The proxies are retained only as exploratory descriptors. Support checking is the operationally stronger applicability gate.

## 8. Truth-generator sensitivity

| Dataset | Logistic-truth reduction | Random-forest-truth reduction |
|---|---:|---:|
| AI4I | 40.6% | 32.7% |
| Steel | 57.0% | 46.5% |
| SECOM | 48.0% | **−18.3%** |

SECOM reverses under the non-smooth truth generator. The public benchmark evidence is therefore conditional on the response surface and cannot establish universal transportability of kernel alignment.

## 9. Qualification-threshold endpoint

A complete test is classified as:

- accept if the Bayes-Kish lower bound is above threshold \(t\);
- reject if the upper bound is below \(t\);
- inconclusive otherwise.

For thresholds at ±15% of \(P^*\):

| Dataset | Method | \(0.85P^*\): correct / wrong / inconclusive | \(1.15P^*\): correct / wrong / inconclusive |
|---|---|---|---|
| AI4I | SRS | 0.10 / 0.00 / 0.90 | 0.16 / 0.04 / 0.80 |
|  | KTES | 0.10 / 0.00 / 0.90 | 0.08 / 0.00 / 0.92 |
| Steel | SRS | 0.86 / 0.00 / 0.14 | 0.90 / 0.00 / 0.10 |
|  | KTES | **0.92 / 0.00 / 0.08** | **1.00 / 0.00 / 0.00** |
| SECOM | SRS | 0.08 / 0.02 / 0.90 | 0.08 / 0.02 / 0.90 |
|  | KTES | 0.12 / 0.00 / 0.88 | 0.10 / 0.00 / 0.90 |
| Ballistic | SRS | 0.12 / 0.00 / 0.88 | 0.02 / 0.02 / 0.96 |
|  | KTES | 0.04 / 0.02 / 0.94 | 0.04 / 0.04 / 0.92 |

This closes a major logic gap in the original paper. Lower MARE does **not** imply better qualification decisions at the frozen shot budget. Only Steel is routinely decisive. The other three surfaces are mostly inconclusive, and ballistic KTES can make more wrong decisions at the tested thresholds.

The next decision-level question is therefore sample/shot allocation around a pre-specified acceptance threshold, not further optimization of the point estimator within the current \(n=10\) setting.

## 10. Revised academic conclusions

The evidence supports the following statements:

1. Under an exact \(M=50\), frozen \(\eta=0.6\) controlled protocol, KTES reduces seedwise MARE relative to SRS on all four development/evaluation surfaces.
2. On pool=target public benchmarks, that reduction is selection-variability control rather than bias correction.
3. Candidate support is a first-order applicability condition. Missing target strata cannot be repaired by reweighting and should stop the analysis.
4. When support is adequate, KTES is consistently better than naive SRS in the tested outer-pool cells, but its advantage over direct importance weighting is dataset-dependent.
5. Kish-scaled intervals have useful empirical calibration in some regimes but remain conditional engineering constructions.
6. The model-assisted design-variance term can improve coverage when variance dominates but cannot cure signed bias.
7. The earlier proposed field-computable gain proxies are too weak under the frozen protocol to serve as a decision rule.
8. Reduced estimation error does not automatically improve qualification decisions at \(n=10\).
9. The public benchmark result is response-surface dependent; SECOM reverses under a random-forest truth generator.

## 11. Claims explicitly withdrawn or deprecated

The following old claims should no longer appear in the manuscript or presentation:

- “KTES reduces MARE by 38–47% with win rates 64–74%.”  
  Replaced by frozen-protocol 40.5–54.8% and 66–72%.
- “The paired advantage is statistically significant only on AI4I.”  
  Replaced by paired mean and median-bootstrap intervals below zero on all four frozen comparisons.
- “A +26.9% stratification floor and strong AUC/interaction proxies predict gain.”  
  The frozen surface gives a different surface-specific baseline and weak proxy correlations; no predictive field rule is supported.
- “Use KTES for under-representation and importance weighting for over-representation.”  
  Outer-pool evidence shows this is dataset-dependent, and severe under-representation often fails support before weighting is meaningful.
- “The design-error correction restores nominal coverage.”  
  Replaced by a regime-dependent sensitivity-correction statement.
- “Crew effectiveness explains the dominant residual environment effect.”  
  The physical case only establishes that the modeled sight-table ballistic component does not explain the assumed reductions; crew effects remain uncalibrated.

## 12. Validation performed

Completed checks in the current environment:

- `python -m py_compile` on all modified/audited analysis scripts: PASS.
- `python validate_contracts.py`: PASS for exact budget, reference equivalence, and fail-closed support.
- `python headline_stats.py`: reproduces all four frozen headline comparisons and paired intervals.
- Full current JSON outputs exist for adaptive main results, held-out \(\eta\), interval calibration, coverage-vs-bias, threshold decisions, truth sensitivity, outer-pool analysis, and frozen phase diagram.

The old single-pool `validate_biased_pool_results.json`, `scan_pool_bias.py`, and `scan_phase_diagram_v2.py` are retained for provenance only and are **not** v7 headline evidence.

## 13. Remaining research gate

No additional synthetic benchmark is required to make the current internal logic coherent. The remaining major validity gate is a genuinely independent engineering dataset or pre-specified external case in which:

1. the target mission distribution is defined before outcome inspection;
2. the candidate-source mechanism is external to method development;
3. \(M\), \(n\), \(\eta=0.6\), stratum definition, support rule, MARE endpoint, and qualification threshold endpoint are frozen in advance;
4. support failures are reported as failures rather than excluded silently;
5. KTES, SRS, and a direct reweighting baseline are compared under the same budget.

Until that gate is passed, the manuscript should claim controlled methodological validation, not field transportability.
