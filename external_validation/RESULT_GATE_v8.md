# KTES v8 — External Engineering Validation Result Gate

Date: 2026-10-05  
Status: **PRIMARY-OUTCOME GATE CLOSED; 500-REPLAY EXECUTION STILL FAIL-CLOSED ON FROZEN R5 SOURCE PROVENANCE**  
Protocol status: **frozen; no retuning or endpoint substitution permitted**.

## 1. Frozen Phase 2A gate

The pre-registered Phase 2A pilot uses:

- official Anti-UAV410 **test split, N=120 sequences**;
- frozen system under test: **SiamFC default tracker**;
- primary per-sequence outcome: **State Accuracy**, `Y_i = SA_i`;
- selected test budget: **n=40**;
- **500 paired design replays**, seeds `20261001 ... 20261500`;
- frozen c-pKTES-Hedge/R3/R5 constants.

The structural-support decision requires all five guardrails:

1. no inclusion-probability failure and no non-certainty unit with `pi_i <= 0`;
2. median weight ESS >= 18.5 and 5th-percentile ESS >= 12;
3. profile `SA` error is not materially worse than stratified probability sampling by >0.01 SA units;
4. six-domain critical `SA` error is not materially worse than the better baseline by >0.02 SA units;
5. difficult-case hit is not >10 percentage points below the split-style baseline.

## 2. Supplied `performance.json` audit

The originally supplied JSON remains a valid secondary-outcome artifact but does not itself contain the primary endpoint:

- SHA-256: `7861cded4d79dfd37ce251e8167f81ce145ea8f9ed68d8dd1f4b252ca33d82a0`
- size: `19,063,146` bytes
- `SiamFC.seq_wise` records: `120`
- sequence-level `SA`/`state_accuracy`: absent
- overall Success AUC: `0.3463100482261262`
- 20-pixel precision: `0.5317451076183254`
- success rate at IoU=0.5: `0.45729244949889203`

No secondary metric is substituted for `SA_i`.

## 3. Primary State Accuracy evidence — CLOSED

The missing primary endpoint was recovered without rerunning or retuning SiamFC:

1. the official Anti-UAV410 repository was pinned at commit `8a8eb04d976e9386b7c9c3ada5c85e5086013d52`;
2. the official paper tracking-result archive supplied **410 SiamFC raw prediction files**, from which the identical 120 frozen test sequences were selected; archive SHA-256 is `79b70e0e56c212bfb19223a22b007ad61e2cb18bf127c16319982f6c61cf6cea`;
3. the public Anti-UAV410 ZIP mirror was range-read to recover the 120 per-frame target-existence arrays without downloading video pixels;
4. localization boxes were taken from the pinned official repository and reconciled with recovered target-existence state under the official State Accuracy semantics;
5. `scripts/extract_antiuav410_sa.py` reproduced the official frame-level State Accuracy rule and emitted exactly 120 sequence-level outcomes.

The reconciliation audit found 8 frames with `exist=false` while the exported official box remained nonzero. These do not affect State Accuracy because the official evaluator does not use the GT box on target-absent frames. Across target-present frames there were zero localization-coordinate conflicts and zero visible zero/nonzero conflicts. The reconciliation gate therefore passed.

Frozen primary outcome artifact:

- file: `data/anti_uav410_siamfc_SA_i_v8.csv`
- N: `120`
- SHA-256: `4049ca9c83128e2a2c8e244c30597a95431f1489efb2f69cda536c8e4873a886`
- equal-sequence population mean SA: `0.351505497767269`

## 4. Full-population truth freeze — CLOSED

The primary outcome was joined to the already frozen outcome-blind design frame (frame SHA-256 `c360494499e2cc9d09c62876bd3c45ab9f5be6982174b172224d12e62e6c9f69`). Population truths are frozen in `data/anti_uav410_population_outcomes_v8.json` and `external_validation/PHASE2A_POPULATION_OUTCOMES_v8.md`.

Key values are:

- population mean SA: `0.351505497767269`;
- median SA: `0.251659259263625`;
- bottom-10% difficult-case set: exactly 12 sequences;
- difficult-case cutoff: `SA = 0.0281723445330009`;
- cutoff tie: none.

The six frozen challenge-domain means are also recorded there. No sampling engine was used to create these population truths.

## 5. Remaining execution blocker

The result gate is **not yet a Phase 2A PASS or FAIL** because the 500 paired design replays have not been executed. The only remaining P0 blocker is the executable provenance of the frozen Phase 1.2R-5 sampling engine.

The historical handoff identifies the authoritative implementation lineage as:

- `src/run_r5_pps_confirm.py`
- `src/run_r5_pps_confirm_chunk.py`
- `src/run_r5_uq_audit_chunk.py`
- `src/phase12r/r5_designs.py`
- `src/phase12r/r5_estimators.py`

Those files are not present in the accessible v7 package or connected Drive search. Reimplementing kernel novelty, inclusion-probability construction, or Local Cube from prose after external outcomes are visible would introduce an unregistered implementation degree of freedom. Execution therefore remains fail-closed until the frozen implementation is recovered or deterministic identity to an archived implementation is demonstrated.

## 6. Academic interpretation

Phase 2A has advanced from “missing primary endpoint” to “primary endpoint and population truth fully frozen.” This is a substantive closure of the evidence gap, but it is not evidence that c-pKTES-Hedge passes external validation. The external validation decision remains pending the pre-registered 500 paired replay using the original frozen sampling engine. Phase 1/v7 controlled evidence remains unchanged.