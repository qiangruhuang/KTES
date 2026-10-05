# KTES — Kernel-based Test-condition Sampling for Evaluation

Canonical research repository for the KTES project.

## Current state: v8 external engineering validation

- **Phase 1 / v7 controlled evidence:** frozen after adversarial-review repair.
- **Phase 2 external engineering validation protocol:** pre-registered and frozen.
- **Phase 2A outcome-blind design frame:** frozen from the pinned official Anti-UAV410 test split.
- **Phase 2A primary State Accuracy endpoint:** recovered and frozen for all 120 SiamFC test sequences.
- **Full-population outcome truths:** frozen, including six challenge-domain means and the 12-sequence bottom-10% difficult set.
- **500 paired replay gate:** **NOT YET EXECUTED / FAIL-CLOSED** because the original Phase 1.2R-5 sampling-engine source provenance has not yet been recovered.
- No endpoint substitution, post-outcome retuning, or redesign has been performed.

The frozen Phase 2A protocol defines Anti-UAV410 test split `N=120`, frozen SiamFC system outcome, `n=40` selected sequences, and 500 paired design replays. The primary endpoint is per-sequence State Accuracy (`SA_i`). Success AUC and 20-pixel precision remain secondary descriptive outputs only.

## Key frozen v8 evidence

Outcome-blind design frame:

- N: `120`
- frame SHA-256: `c360494499e2cc9d09c62876bd3c45ab9f5be6982174b172224d12e62e6c9f69`
- size strata: Tiny 33 / Small 54 / Medium 29 / Normal 4
- frozen n=40 allocation: 11 / 17 / 10 / 2

Primary outcome:

- `data/anti_uav410_siamfc_SA_i_v8.csv`
- N: `120`
- SHA-256: `4049ca9c83128e2a2c8e244c30597a95431f1489efb2f69cda536c8e4873a886`
- population mean SA: `0.351505497767269`
- median SA: `0.251659259263625`
- bottom-10% cutoff: `0.0281723445330009`, no cutoff tie

The original supplied `performance.json` remains preserved only by hash/manifest because it does not contain sequence-level State Accuracy. The primary outcome was recovered from the public SiamFC raw tracking-result archive plus per-frame target-existence metadata under the official Anti-UAV410 SA semantics.

## Repository layout

- `paper/` — frozen v7 manuscript/revision/supplement/audit/handoff.
- `protocol/` — Phase 2 external-validation protocol and immutable contract.
- `external_validation/PHASE2A_DESIGN_FREEZE_v8.md` — frozen outcome-blind frame and allocation.
- `external_validation/SA_RECOVERY_v8.md` — primary State Accuracy evidence recovery and reconciliation audit.
- `external_validation/PHASE2A_POPULATION_OUTCOMES_v8.md` — frozen population truths.
- `external_validation/PHASE2A_EXECUTION_AUDIT_v8.md` — current execution-readiness audit.
- `external_validation/SAMPLING_ENGINE_PROVENANCE_GATE_v8.md` — remaining fail-closed R5 implementation gate.
- `external_validation/RESULT_GATE_v8.md` — current external-validation result-gate state.
- `scripts/` — deterministic evidence, frame, SA, population-summary, and provenance auditing scripts.
- `data/` — derived manifests and frozen external-validation data products; large raw archives are not duplicated in Git.

## Remaining P0 requirement

Before the 500 paired replays can be executed, recover the original frozen Phase 1.2R-5 implementation lineage:

- `src/run_r5_pps_confirm.py`
- `src/run_r5_pps_confirm_chunk.py`
- `src/run_r5_uq_audit_chunk.py`
- `src/phase12r/r5_designs.py`
- `src/phase12r/r5_estimators.py`

`scripts/audit_r5_source_provenance.py` fails closed if any required source is absent. A prose-based reimplementation after viewing external outcomes is not accepted as the frozen engine.

## Research integrity rule

External outcomes may not be used to re-select c-pKTES-Hedge/R3/R5 constants and then be reused as confirmation. A failed external gate is reported as an external-validity boundary. Current Phase 2A status is neither PASS nor FAIL: the outcome evidence is frozen, but the pre-registered replay comparison awaits the original sampling engine.