# Phase 2A execution audit v8

**Audit date:** 2026-10-05  
**Overall state:** **FAIL-CLOSED / NOT YET EXECUTABLE AS A FULL 500-REPLAY CONFIRMATION**

## Audit results

1. **Protocol integrity — PASS.** The 2026-09-29 Phase 2 protocol and immutable contract remain unchanged.
2. **External frame identity — PASS.** The official test population contains 120 sequence-level attribute records and is pinned to Anti-UAV410 commit `8a8eb04d976e9386b7c9c3ada5c85e5086013d52`.
3. **Outcome-blind frame construction — PASS.** The frame is based only on official attributes and frame counts; no tracker outcome enters feature construction.
4. **Strata/allocation — PASS.** Population counts are 33/54/29/4 for Tiny/Small/Medium/Normal and the frozen n=40 allocation is 11/17/10/2.
5. **Primary-outcome availability — FAIL-CLOSED.** The supplied SiamFC `performance.json` has 120 sequences but no sequence-level State Accuracy.
6. **Sampling-engine provenance — FAIL-CLOSED.** The historical handoff names the frozen R5 implementation files, but the executable source is absent from the accessible snapshot. Reimplementing kernel novelty or Local Cube from prose would constitute an unregistered implementation change.
7. **Parameter retuning — PASS.** No rho/lambda/sentinel/UQ/endpoint/guardrail change has been made.
8. **Endpoint substitution — PASS.** Success AUC and precision have not been substituted for State Accuracy.

## Consequence

The design frame is frozen, but the 500 paired replays must not be reported as executed until two independent requirements are satisfied: (i) the frozen R5 sampling-engine source is recovered and its provenance recorded; and (ii) the 120 sequence-level `SA_i` values are obtained from the official SA semantics. This status is neither a Phase 2A pass nor a Phase 2A fail.

## Recovery paths already fixed

For `SA_i`, the official `Evaluation_for_SA.py` semantics are now mirrored by `scripts/extract_antiuav410_sa.py`. It requires the Anti-UAV410 test `IR_label.json` files and the 120 SiamFC prediction files and emits a sequence-keyed SA table. The official repository also publishes a Google Drive archive of paper tracking results; acquisition of the SiamFC raw predictions from that archive remains an evidence-recovery task, not a protocol change.

For the sampling engine, the required historical files are `run_r5_pps_confirm.py`, `run_r5_pps_confirm_chunk.py`, `phase12r/r5_designs.py`, and `phase12r/r5_estimators.py`. Until recovered, execution remains fail-closed.
