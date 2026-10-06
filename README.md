# KTES — Kernel-based Test-condition Sampling for Evaluation

Canonical research repository for the KTES project.

## Current state: v8 external engineering validation

- **Phase 1 / v7 controlled evidence:** frozen after adversarial-review repair.
- **Phase 2 external engineering validation protocol:** pre-registered and frozen.
- **Phase 2A Anti-UAV410 design frame and primary State Accuracy outcome:** frozen for all 120 official test sequences.
- **Frozen Phase 1.2R-5 sampling-engine provenance:** recovered, hash-verified and behavior-regression verified.
- **Phase 2A 500 paired replay gate:** **COMPLETE — PASS_WITH_EXECUTION_CLARIFICATION**.
- **Phase 2B IDF-DS:** may enter pre-outcome engineering-contract freeze; outcome opening remains prohibited until the exact engineering endpoint/failure rule and column map are frozen.

No rho/lambda/sentinel/UQ retuning, endpoint substitution or post-outcome redesign of c-pKTES-Hedge has been performed.

## Phase 2A result

The frozen pilot uses Anti-UAV410 test split `N=120`, SiamFC State Accuracy (`SA_i`), n=40 selected sequences and 500 paired design replays (`20261001..20261500`).

Mean results:

| Method | Profile error | Critical-domain error | Difficult-case hit | Probability-component ESS median |
|---|---:|---:|---:|---:|
| c-pKTES-Hedge | 0.03007 | **0.04893** | 1.000 | 33.12 |
| Stratified-SRS | **0.02603** | 0.05911 | 0.996 | 39.71 |
| Split15+Audit25 | 0.03049 | 0.06109 | 1.000 | 24.27 |

All numerical external-validation guardrails pass. c-pKTES-Hedge is **not** uniformly superior: its profile error is higher than SRS by `+0.00404` (95% CI `0.00137` to `0.00671`), but this remains inside the frozen `+0.01` non-inferiority bound. Its six-domain critical error is lower than SRS by `−0.01018` (95% CI `−0.01230` to `−0.00806`).

The result is classified **PASS_WITH_EXECUTION_CLARIFICATION**, rather than pristine preregistered PASS, because the exact numerical Split15 adapter and the finite-domain critical-domain estimator required explicit execution clarification after `SA_i` recovery. Those clarifications do not modify the c-pKTES-Hedge selection constants or any gate threshold.

## Frozen evidence identities

Outcome-blind design frame:

- N: `120`
- SHA-256: `c360494499e2cc9d09c62876bd3c45ab9f5be6982174b172224d12e62e6c9f69`
- size strata: Tiny 33 / Small 54 / Medium 29 / Normal 4
- n=40 allocation: 11 / 17 / 10 / 2

Primary State Accuracy outcome:

- `data/anti_uav410_siamfc_SA_i_v8.csv`
- SHA-256: `4049ca9c83128e2a2c8e244c30597a95431f1489efb2f69cda536c8e4873a886`
- population mean SA: `0.351505497767269`
- median SA: `0.251659259263625`
- bottom-10% cutoff: `0.0281723445330009`, no tie

Phase 2A design object:

- SHA-256: `2a686908e42a1134578c07eecce9ca3be8336ff08c37c8d3622ff2a2855184dc`
- certainty sentinels: `20190926_111509_1_9`, `3700000000002_162623_1`, `new6_train_newfix`
- one non-sentinel probability-remainder unit is naturally capped to `pi=1` by the frozen inclusion-probability algorithm; it remains part of the 37-unit probability-remainder identity for ESS evaluation.

## Independent CI execution

GitHub Actions run `37422551437` at commit `44357d40de298d4a3b19e6dfe629d43464865a88` independently verified the historical R5 runtime SHA-256 values, frozen external-input hashes, design instantiation and all 500 paired replays. The CI artifact was downloaded and rehashed independently; all core output hashes matched the runner log exactly.

See `external_validation/PHASE2A_CI_EVIDENCE_v8.md` for the execution and hash manifest.

## Repository layout

- `paper/` — frozen v7 manuscript/revision/supplement/audit/handoff.
- `protocol/` — Phase 2 external-validation protocol and immutable contract.
- `vendor/r5_engine_recovered_v8/` — recovered hash-verified historical Phase 1.2R runtime used for Phase 2A.
- `external_validation/PHASE2A_DESIGN_FREEZE_v8.md` — outcome-blind frame/allocation freeze and chronology.
- `external_validation/SA_RECOVERY_v8.md` — State Accuracy recovery/reconciliation audit.
- `external_validation/PHASE2A_POPULATION_OUTCOMES_v8.md` — frozen population truths.
- `external_validation/SAMPLING_ENGINE_PROVENANCE_GATE_v8.md` — closed R5 provenance gate.
- `external_validation/PHASE2A_EXECUTION_AUDIT_v8.md` — final Phase 2A execution audit.
- `external_validation/PHASE2A_500_REPLAY_RESULT_v8.md` — 500-replay primary result.
- `external_validation/phase2a_result_gate_v8.json` — machine-readable gate decision.
- `external_validation/PHASE2A_CI_EVIDENCE_v8.md` — independent CI execution evidence.
- `results/phase2a_500_replay_summary_v8.csv` and `results/phase2a_500_replay_paired_v8.csv` — frozen result tables.
- `scripts/` — deterministic evidence recovery, auditing and replay code.

## Research integrity rule

Phase 2A is now closed. Its results must be reported even where they are less favorable to KTES, particularly the higher profile error relative to SRS. Anti-UAV410 may not now be used to retune the frozen method and then be relabeled as external confirmation.

The next study step is Phase 2B pre-outcome contract freeze. The IDF-DS engineering dataset should not be opened for outcome analysis until the finite-population eligibility rule, primary engineering performance floor, exact failure semantics, covariate/column map, strata and analysis endpoints are frozen from engineering meaning rather than observed failure rates.
