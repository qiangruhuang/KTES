# KTES — Kernel-based Test-condition Sampling for Evaluation

Canonical research repository for the KTES project.

## Current state: v8 external engineering validation

- **Phase 1 / v7 controlled evidence:** frozen after adversarial-review repair.
- **Phase 2 external engineering validation protocol:** pre-registered and frozen.
- **Phase 2A Anti-UAV410 design frame and primary State Accuracy outcome:** frozen for all 120 official test sequences.
- **Frozen Phase 1.2R-5 sampling-engine provenance:** recovered, hash-verified and behavior-regression verified.
- **Phase 2A 500 paired replay gate:** **COMPLETE — PASS_WITH_EXECUTION_CLARIFICATION**.
- **Phase 2B IDF-DS pre-outcome source gate:** **BLOCKED_SOURCE_STRUCTURE**. The public Zenodo release does not expose the per-flight mission/configuration metadata required to instantiate the preregistered outcome-blind KTES design; no flight-level telemetry outcomes have been opened for Phase 2B.

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

## Phase 2B source gate

The frozen Phase 2B protocol required flight-level pre-outcome mission/configuration information before any IDF-DS telemetry values could be opened. Direct range-only audits of Zenodo record `16992976` showed that the released archives do not have the per-flight `mission.txt` / `parameters.csv` structure described in the paper:

- SpeedyBee-INAV: 252 ZIP members, 111 processed `Lap` IDs, 26 raw `LOG*.TXT`, one archive-level `.plan`, no per-flight parameter-like file;
- Pixhawk-Jetson-PX4: 17,226 ZIP members, 120 grouped and 120 ungrouped processed IDs, 13 raw `.ulg`, one archive-level `.plan`, no per-flight parameter-like file;
- the two archive-level `cheste_QGroundControl.plan` files are byte-identical and have the same 55-item geometry signature;
- no independent per-flight weather/condition metadata is identifiable from the archive names.

The only released mission plan is therefore an archive-level constant and cannot define within-stratum novelty, adverse-tail scores or sentinel selection. Realized GPS paths, wind, speeds, flight states, power, airspeed or other telemetry outcomes are not promoted into the design frame to rescue the validation.

Phase 2B is consequently **not a performance FAIL**. It is blocked before outcome opening by insufficient pre-outcome covariate resolution. See `external_validation/PHASE2B_SOURCE_GATE_v8.md`.

## Frozen evidence identities

Outcome-blind Phase 2A design frame:

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

GitHub Actions run `37422551437` at commit `44357d40de298d4a3b19e6dfe629d43464865a88` independently verified the historical R5 runtime SHA-256 values, frozen external-input hashes, design instantiation and all 500 paired Phase 2A replays. The CI artifact was downloaded and rehashed independently; all core output hashes matched the runner log exactly.

Phase 2B source-structure audits were also executed independently in GitHub Actions without opening flight-level telemetry outcomes. The final source-reconciliation run is `37556831613`.

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
- `external_validation/phase2a_result_gate_v8.json` — machine-readable Phase 2A gate decision.
- `external_validation/PHASE2A_CI_EVIDENCE_v8.md` — independent CI execution evidence.
- `external_validation/PHASE2B_PREOUTCOME_FREEZE_v8.md` — immutable pre-outcome Phase 2B contract.
- `external_validation/PHASE2B_SOURCE_GATE_v8.md` — Phase 2B public-source fail-closed audit.
- `results/phase2a_500_replay_summary_v8.csv` and `results/phase2a_500_replay_paired_v8.csv` — frozen Phase 2A result tables.
- `scripts/` — deterministic evidence recovery, auditing, replay and pre-outcome source-audit code.

## Research integrity rule

Phase 2A is closed. Its results must be reported even where they are less favorable to KTES, particularly the higher profile error relative to SRS. Anti-UAV410 may not now be used to retune the frozen method and then be relabeled as external confirmation.

Phase 2B remains outcome-blind and blocked at the public-source gate. It may resume only if a unit-linked preflight metadata package can be independently matched and hash-frozen before telemetry outcome extraction. If such metadata is unavailable, IDF-DS must be reported as an external-data limitation; any replacement engineering validation requires a new preregistered external dataset rather than outcome-driven redesign on IDF-DS.
