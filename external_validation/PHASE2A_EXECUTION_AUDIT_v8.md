# Phase 2A execution audit v8

**Audit date:** 2026-10-05  
**Overall state:** **PRIMARY OUTCOME + POPULATION TRUTHS FROZEN; 500-REPLAY EXECUTION FAIL-CLOSED ON R5 SOURCE PROVENANCE**

## Audit results

1. **Protocol integrity — PASS.** The 2026-09-29 Phase 2 protocol and immutable contract remain unchanged.
2. **External frame identity — PASS.** The official Anti-UAV410 test population contains 120 sequence-level attribute records and is pinned to commit `8a8eb04d976e9386b7c9c3ada5c85e5086013d52`.
3. **Outcome-blind frame construction — PASS.** The design frame uses only official attributes and sequence lengths. Frame SHA-256: `c360494499e2cc9d09c62876bd3c45ab9f5be6982174b172224d12e62e6c9f69`.
4. **Strata/allocation — PASS.** Tiny/Small/Medium/Normal population counts are 33/54/29/4 and the frozen n=40 allocation is 11/17/10/2.
5. **SiamFC raw prediction recovery — PASS.** The official paper tracking-result archive contains 410 SiamFC result files, including all 120 frozen test sequences; archive SHA-256 `79b70e0e56c212bfb19223a22b007ad61e2cb18bf127c16319982f6c61cf6cea`.
6. **Target-existence recovery and reconciliation — PASS.** All 120 sequences and 129,691 frames were recovered. Across target-present frames there are zero visible localization-coordinate conflicts and zero visible zero/nonzero conflicts between the recovered labels and pinned official box annotations. Eight target-absent frames retain nonzero exported boxes, but this is semantically irrelevant because the official State Accuracy evaluator ignores the GT box when `exist=false`.
7. **Primary-outcome availability — PASS.** Exactly 120 `SA_i` values were generated under the official State Accuracy semantics. SA artifact SHA-256: `4049ca9c83128e2a2c8e244c30597a95431f1489efb2f69cda536c8e4873a886`.
8. **Population-truth freeze — PASS.** Population mean SA is `0.351505497767269`, median `0.251659259263625`; the bottom-10% difficult set has exactly 12 sequences with cutoff `0.0281723445330009` and no cutoff tie. Six challenge-domain and four size-stratum truths are frozen in `data/anti_uav410_population_outcomes_v8.json`.
9. **Sampling-engine provenance — FAIL-CLOSED.** The historical handoff names the frozen R5 implementation files, but the executable source is absent from the accessible project snapshot. Reimplementing kernel novelty, inclusion probabilities, or Local Cube from prose would constitute an unregistered implementation change.
10. **Parameter retuning — PASS.** No rho/lambda/sentinel/UQ/endpoint/guardrail change has been made.
11. **Endpoint substitution — PASS.** Success AUC and precision remain secondary only and were not substituted for State Accuracy.

## Remaining blocker

The 500 paired replays must not be reported as executed until the original frozen Phase 1.2R-5 sampling-engine implementation is recovered or deterministic identity to an archived implementation is demonstrated.

Required implementation lineage:

- `src/run_r5_pps_confirm.py`
- `src/run_r5_pps_confirm_chunk.py`
- `src/run_r5_uq_audit_chunk.py`
- `src/phase12r/r5_designs.py`
- `src/phase12r/r5_estimators.py`

The provenance checker `scripts/audit_r5_source_provenance.py` is already committed and fails closed if any required source is absent.

## Current interpretation

Phase 2A is no longer blocked by external outcomes: the complete primary outcome vector and all population truths required for replay scoring are frozen. It remains neither PASS nor FAIL because the pre-registered KTES/SRS/split-style replay comparison has not yet been executed with the frozen R5 engine.