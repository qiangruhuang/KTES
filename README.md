# KTES — Kernel-based Test-condition Sampling for Evaluation

Canonical research repository for the KTES project.

## Current state: v8 external-validation evidence closed for review

- **Phase 1 / v7 controlled evidence:** frozen after adversarial-review repair.
- **Phase 2 method contract:** frozen; no rho/lambda/sentinel/UQ retuning on external outcomes.
- **Phase 2A Anti-UAV410:** **COMPLETE — PASS_WITH_EXECUTION_CLARIFICATION**.
- **Phase 2B IDF-DS:** **BLOCKED_SOURCE_STRUCTURE** before telemetry outcome opening; the public release cannot instantiate the frozen flight-level outcome-blind design frame.
- **Replacement engineering validation — AMOVFLY:** confirmatory numerical gate **PASS**, with a material **endpoint-semantic limitation** discovered post outcome.
- **AMOVFLY exact-zero sensitivity:** **POST_OUTCOME_SENSITIVITY ONLY**; the method-comparison conclusion remains robust when exact `(0,0)` waypoint placeholders are diagnostically excluded.

The defensible current conclusion is therefore:

> The frozen c-pKTES-Hedge design transports beyond controlled simulation to two independent real-data settings at the level of probability-preserving sampling/inference comparisons, but the strength of engineering claims is dataset- and endpoint-dependent. Anti-UAV410 carries an execution-order clarification; IDF-DS is blocked by public-source structure; AMOVFLY passes its frozen numerical comparison gate but its literal waypoint endpoint is contaminated by systematic `(0,0)` placeholder episodes.

## Phase 2A — Anti-UAV410

The frozen pilot uses the official Anti-UAV410 test split (`N=120`), SiamFC per-sequence State Accuracy (`SA_i`), `n=40` selected sequences and 500 paired design replays (`20261001..20261500`).

| Method | Profile error | Critical-domain error | Difficult-case hit | Probability-component ESS median |
|---|---:|---:|---:|---:|
| c-pKTES-Hedge | 0.03007 | **0.04893** | 1.000 | 33.12 |
| Stratified-SRS | **0.02603** | 0.05911 | 0.996 | 39.71 |
| Split15+Audit25 | 0.03049 | 0.06109 | 1.000 | 24.27 |

All numerical guardrails pass. c-pKTES-Hedge is not uniformly superior: its profile error is higher than SRS by `+0.00404` (95% CI `0.00137` to `0.00671`) but remains inside the frozen `+0.01` non-inferiority bound. Its critical-domain error is lower.

The result remains **PASS_WITH_EXECUTION_CLARIFICATION**, not a pristine preregistered PASS, because the exact numerical Split15 adapter and finite-domain critical-domain estimator required explicit execution clarification after `SA_i` recovery. No frozen c-pKTES-Hedge constant or gate threshold was retuned.

## Phase 2B — IDF-DS source gate

The pre-outcome protocol required unit-linked mission/configuration information before telemetry values could enter the analysis. Audit of the public IDF-DS release found archive-level mission plans but not the required per-flight mission/configuration structure. Realized GPS paths, wind, speeds, states, power or other telemetry were not promoted into the sampling frame to rescue the study.

IDF-DS is therefore **BLOCKED_SOURCE_STRUCTURE**, not a method-performance failure. It remains a documented external-data limitation.

## AMOVFLY — independent real-flight validation

AMOVFLY was frozen as a new independent engineering dataset before telemetry outcomes were opened.

Frozen identities:

- source: `YujiaoHu/AMOVFLY-Dataset` at commit `67069ed00ddbebd62b71aa9bb1272415e9b15ff8`;
- finite population: `N=257` unique autonomous ready-data flight blobs;
- strata: FAFS 33 / FAVS 165 / VAFS 32 / VAVS 27;
- `n=40` allocation: 6 / 23 / 6 / 5;
- path-only frame SHA-256: `92a6d63eb75a0eee58e9d310da9b140517e2dffd2c6f48986fd21b40c8b12c85`;
- realized design-object SHA-256: `a5b241f9d17be696652f30968bb1b8a0d2138087674ac371866b606e8362696b`;
- primary frozen literal endpoint: proportion of waypoint episodes attaining an external 10 m reference radius;
- confirmatory run: GitHub Actions `37564463826`.

### Confirmatory numerical result

| Method | Profile error Y10 | Critical-domain error Y10 | Difficult-case hit | Probability ESS median |
|---|---:|---:|---:|---:|
| c-pKTES-Hedge | 0.003784 | **0.033764** | 1.000 | 35.224 |
| Stratified-SRS | 0.004543 | 0.066201 | 1.000 | 39.276 |
| Split15+Audit25 | **0.003637** | 0.080011 | 1.000 | 23.019 |

All five frozen numerical gates pass. For the profile endpoint, KTES−SRS paired error difference is `−0.0007586` (95% CI `−0.0011638` to `−0.0003534`). Critical-domain error is also lower for KTES than either comparator.

### Endpoint-semantic audit

The frozen literal parser produced `Y10=0.946105` and `F10=1.000` for the population. A post-outcome read-only audit then found:

- all **257/257** flights contain at least one exact `(0,0)` aim-waypoint episode;
- **378** exact-zero episodes occur in total;
- exactly **378** episodes have minimum actual-to-aim distance >100 km;
- all 378 extreme episodes are exact `(0,0)` episodes; no non-zero target produces a >100 km episode.

Thus the literal `F10=I(any episode >10 m)` endpoint is degenerate and cannot support failure-rate qualification. The bounded `Y10` endpoint is also materially shifted by the placeholder semantics.

This does not erase the executed confirmatory result, but it changes the defensible classification to:

**NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION**.

### Post-outcome robustness sensitivity

A separately labelled sensitivity excludes exact `(0,0)` episodes only. It reads the original confirmatory design object as immutable input; it does not regenerate inclusion probabilities or modify sentinels/comparators.

Diagnostic population after exact-zero exclusion:

- `Y10=0.982243`;
- `F10=0.459144`;
- `Y2=0.081689`.

Under the unchanged frozen design and replay seeds:

- KTES−SRS profile-error difference: `−0.0004107`, 95% CI `−0.0006379` to `−0.0001834`;
- KTES critical-domain error: `0.033420` vs SRS `0.064683` vs Split15 `0.079275`;
- KTES and Split15 difficult-case hit: `1.000`;
- all five numerical sensitivity gates remain satisfied.

This supports robustness of the **method-comparison conclusion** only. It is post outcome and cannot replace the confirmatory endpoint.

## Numerical reproducibility finding

A later hosted-runner attempt to regenerate the AMOVFLY design from the same source code, declared Python/NumPy/SciPy versions, frame, constants and seeds failed the exact design-object SHA guard before sensitivity outcomes were computed.

The regenerated object preserved standardization, bandwidth, seed lineage and sentinels, but `254/257` first-order inclusion probabilities differed by more than `1e-12` (maximum absolute difference `0.0108412`), and the example Local-Cube sample changed. No tolerance was relaxed.

Downstream analysis now follows the stricter rule: **the hashed realized design object is an immutable research input**. Package-version pinning plus seeds alone is not treated as sufficient identity for the realized unequal-probability design.

## Evidence map

Core external-validation documents:

- `external_validation/PHASE2A_500_REPLAY_RESULT_v8.md`
- `external_validation/PHASE2A_EXECUTION_AUDIT_v8.md`
- `external_validation/PHASE2B_PREOUTCOME_FREEZE_v8.md`
- `external_validation/PHASE2B_SOURCE_GATE_v8.md`
- `external_validation/AMOVFLY_DESIGN_FREEZE_v8.md`
- `external_validation/AMOVFLY_ENDPOINT_PERFORMANCE_FLOOR_FREEZE_v8.md`
- `external_validation/AMOVFLY_RUNTIME_FREEZE_v8.md`
- `external_validation/AMOVFLY_EXTERNAL_VALIDATION_RESULT_v8.md`
- `external_validation/AMOVFLY_WAYPOINT_SEMANTIC_AUDIT_v8.md`
- `external_validation/AMOVFLY_ZERO_PLACEHOLDER_SENSITIVITY_v8.md`
- `external_validation/AMOVFLY_NUMERICAL_REPRODUCIBILITY_AUDIT_v8.md`

Machine-readable evidence:

- `results/amovfly_external_validation_result_v8.json`
- `results/amovfly_500_replay_summary_v8.csv`
- `results/amovfly_waypoint_semantic_audit_v8.json`
- `results/amovfly_zero_placeholder_sensitivity_v8.json`
- `results/amovfly_zero_placeholder_sensitivity_summary_v8.csv`
- `results/AMOVFLY_EVIDENCE_MANIFEST_v8.json`

Frozen Phase 1 manuscript/revision material remains under `paper/`; v8 external-validation evidence does not retroactively alter the frozen v7 manuscript.

## Research integrity rule

Phase 2A is closed and must retain its less favorable profile-error result relative to SRS. Anti-UAV410 may not be retuned and relabelled as external confirmation.

IDF-DS remains a documented source-structure block. It may not be rescued by deriving the frozen design from telemetry outcomes.

AMOVFLY's original confirmatory result, post-outcome semantic audit and post-outcome sensitivity must be reported side by side. The exact-zero exclusion cannot be silently promoted to the primary endpoint. The degenerate literal failure endpoint cannot support failure-probability or safety-qualification claims. Future engineering confirmation should use a new independently frozen dataset/endpoint contract rather than repairing AMOVFLY on the same outcomes and calling it new confirmation.
