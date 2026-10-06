# Phase 2A 500-paired-replay result v8

**Gate status:** **PASS_WITH_EXECUTION_CLARIFICATION**

## Method summaries

| method          |   n_replays |   profile_error_mean |   profile_error_median |   critical_domain_error_mean |   critical_domain_error_median |   difficult_case_hit_rate |   ess_all_median |   ess_all_p05 |   ess_probability_component_median |   ess_probability_component_p05 |   probability_component_n |   min_pi_selected_min |   max_normalized_weight_p95 |   profile_uq_coverage |   domain_uq_coverage_mean |
|:----------------|------------:|---------------------:|-----------------------:|-----------------------------:|-------------------------------:|--------------------------:|-----------------:|--------------:|-----------------------------------:|--------------------------------:|--------------------------:|----------------------:|----------------------------:|----------------------:|--------------------------:|
| Split15+Audit25 |         500 |            0.0304875 |              0.0246688 |                    0.0610944 |                      0.0600203 |                     1     |          30.6863 |       30.6863 |                            24.27   |                         24.27   |                        25 |              0.215686 |                   0.0386364 |                 0.962 |                  0.901667 |
| Stratified-SRS  |         500 |            0.0260294 |              0.0208684 |                    0.0591125 |                      0.0580649 |                     0.996 |          39.71   |       39.71   |                            39.71   |                         39.71   |                        40 |              0.314815 |                   0.0264706 |                 0.974 |                  0.935333 |
| c-pKTES-Hedge   |         500 |            0.0300689 |              0.0271298 |                    0.0489346 |                      0.0478004 |                     1     |          34.5922 |       34.0655 |                            33.1218 |                         32.5987 |                        37 |              0.179379 |                   0.0469651 |                 0.964 |                  0.943667 |

## Paired comparisons

| comparison                      | metric                    |   n |    mean_diff |       ci_lo |       ci_hi |   median_diff |
|:--------------------------------|:--------------------------|----:|-------------:|------------:|------------:|--------------:|
| c-pKTES-Hedge - Stratified-SRS  | profile_error             | 500 |  0.00403957  |  0.00136838 |  0.00671075 |   0.00437964  |
| c-pKTES-Hedge - Split15+Audit25 | profile_error             | 500 | -0.000418608 | -0.00324923 |  0.00241201 |  -0.000904161 |
| c-pKTES-Hedge - Stratified-SRS  | critical_domain_error     | 500 | -0.0101779   | -0.0123005  | -0.00805534 |  -0.00892534  |
| c-pKTES-Hedge - Split15+Audit25 | critical_domain_error     | 500 | -0.0121597   | -0.0142625  | -0.010057   |  -0.010876    |
| c-pKTES-Hedge - Stratified-SRS  | difficult_case_hit        | 500 |  0.004       | -0.00153816 |  0.00953816 |   0           |
| c-pKTES-Hedge - Split15+Audit25 | difficult_case_hit        | 500 |  0           |  0          |  0          |   0           |
| c-pKTES-Hedge - Stratified-SRS  | ess_probability_component | 500 | -6.58372     | -6.6125     | -6.55494    |  -6.58815     |
| c-pKTES-Hedge - Split15+Audit25 | ess_probability_component | 500 |  8.85622     |  8.82744    |  8.885      |   8.85179     |

## Frozen guardrails

- `positive_pi_and_no_sampling_failure`: **PASS** — {"value": true, "pass": true}
- `ktes_probability_remainder_ess_median_ge_18_5`: **PASS** — {"value": 33.12181234684833, "threshold": 18.5, "pass": true}
- `ktes_probability_remainder_ess_p05_ge_12`: **PASS** — {"value": 32.598666450606956, "threshold": 12.0, "pass": true}
- `profile_error_not_worse_than_srs_by_gt_0_01`: **PASS** — {"ktes_minus_srs": 0.004039565979218843, "threshold_max": 0.01, "pass": true}
- `critical_domain_error_not_worse_than_better_baseline_by_gt_0_02`: **PASS** — {"better_baseline": "Stratified-SRS", "ktes_minus_better": -0.010177897751266395, "threshold_max": 0.02, "pass": true, "preregistration_note": "Comparator-sensitive: split adapter clarified after SA_i recovery."}
- `difficult_hit_not_below_split_by_gt_0_10`: **PASS** — {"ktes_minus_split": 0.0, "threshold_min": -0.1, "pass": true, "preregistration_note": "Comparator-sensitive: split adapter clarified after SA_i recovery."}

## Execution-order disclosure

Historical deterministic_ktes15 3x4+3 geometry rule mapped outcome-blind to the four Phase2A size strata; 25 audit units use largest-remainder allocation with minimum 2 over the remaining population. This numerical adapter was instantiated after SA_i recovery but before replay results; it is an execution clarification, not pristine preregistration.

The c-pKTES constants, endpoint, frame covariates, strata, allocation and guardrail thresholds were not retuned after outcome recovery.

## Interpretation boundary

This gate evaluates structural transfer of the frozen probability-preserving sampling logic on a real task-effectiveness benchmark. It does not establish live-weapon validity, deployment-frequency representativeness, or mission-level safety certification.
