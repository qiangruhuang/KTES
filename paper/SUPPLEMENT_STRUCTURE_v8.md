# KTES v8 Supplementary Information Structure

**Status:** submission-presentation design freeze candidate  
**Purpose:** move audit depth out of the main narrative without losing reproducibility or adverse evidence

## S1. Method development and freeze history

- R1–R5 development sequence.
- Exact reason for moving from deterministic split to probability-preserving hedge.
- Frozen `rho=0.20`, `lambda=3`, sentinel portfolio and probability floor.
- Supplementary Fig. S1: R1→R5 design evolution.

## S2. Frozen estimator and uncertainty construction

- stratum-wise Hájek model-assisted residual estimator;
- Local Cube implementation identity;
- `max(GS,PWR)` uncertainty diagnostic;
- frozen R3 calibration constants;
- Accept / Reject / Inconclusive logic;
- estimator/UQ claim boundary.

## S3. R5 independent confirmation

- full metrics by discrepancy regime (`good`, `global_bias`, `tail_bias`, `hidden_bias`, `mixed`);
- edge-hit, profile/failure/tail MAE, definitive-correct, abstention, coverage and false acceptance;
- hidden-bias subgroup result;
- safety-UQ audit;
- Supplementary Tables S1–S3.

## S4. Anti-UAV410 Phase 2A

- finite population and 120-sequence frame;
- outcome-blind attributes and size strata;
- frozen allocation 11/17/10/2;
- exact three sentinels;
- positive-π remainder diagnostics;
- all 500 paired replay summaries;
- full SRS and Split15 comparator results;
- execution-order disclosure and why the result is `PASS_WITH_EXECUTION_CLARIFICATION`;
- hashes and CI evidence manifest.

## S5. IDF-DS source gate

- preregistered required preoutcome covariates;
- public archive structure audit;
- 111 SpeedyBee processed IDs vs intended 120;
- shared archive-level mission plan;
- prohibited telemetry-derived rescue features;
- exact `BLOCKED_SOURCE_STRUCTURE` decision rule.

No flight-level telemetry outcome should be analyzed in this supplement unless a future independently sourced preflight metadata package first satisfies the frozen source gate.

## S6. AMOVFLY preoutcome design and confirmatory run

- population construction and four strata;
- n=40 allocation 6/23/6/5;
- path-only design frame identity;
- immutable confirmatory design-object hash;
- full numerical gate results;
- exact primary endpoint definition.

## S7. AMOVFLY endpoint-semantic audit

- exact-zero `(0,0)` episode diagnosis;
- proof that 378/378 >100 km episodes are exact-zero episodes;
- consequence for `F10` degeneracy;
- effect on bounded `Y10`;
- explicit statement that the confirmatory endpoint is not retroactively replaced.

## S8. Post-outcome sensitivity

- exact-zero exclusion only;
- immutable original design object loaded unchanged;
- unchanged replay seeds;
- numerical results;
- strict label: **post-outcome diagnostic sensitivity, not independent confirmation**.

## S9. Realized-design reproducibility audit

- later hosted-runner reconstruction attempt;
- same high-level source/runtime metadata and sentinels;
- 254/257 `pi_i` values differ by >1e-12;
- maximum absolute difference 0.0108412;
- changed example Local-Cube sample;
- fail-closed response and immutable-design-object rule.

## S10. Evidence manifest and reproducibility checklist

For every major result, provide:

- source identity and source commit/hash;
- preoutcome frame hash;
- realized design-object hash where applicable;
- code hash;
- replay seed block;
- result-table hash;
- CI run/artifact identity;
- evidence class and claim boundary.

## Main-paper / supplement boundary

The main paper should answer **what the method is, what the frozen confirmation showed, what transported externally, and why evidence classification matters**. The supplement should answer **exactly how every design and result can be reconstructed and audited**.
