# Phase 2A State Accuracy recovery note

**Status:** **CLOSED / PRIMARY OUTCOME FROZEN**  
**Date:** 2026-10-05

The supplied `performance.json` could not yield the frozen primary endpoint because its SiamFC sequence records contain Success/Precision summaries rather than per-frame predictions or sequence State Accuracy. The endpoint was therefore recovered from independent raw evidence without replacing or redefining State Accuracy.

## Recovery chain

The official Anti-UAV410 `Evaluation_for_SA.py` defines sequence SA by iterating over prediction, ground-truth box, and target-existence state per frame. For target-absent frames a missing/one-element prediction scores 1 and a box prediction scores 0; for target-present frames a four-coordinate prediction scores IoU with ground truth, otherwise 0; invalid present-target ground truth is skipped. Sequence SA is the mean over evaluable frames.

The final v8 chain is:

1. Pin the official repository at commit `8a8eb04d976e9386b7c9c3ada5c85e5086013d52`.
2. Recover the official paper SiamFC raw tracker results from the public tracking-results archive. The archive contains 410 SiamFC `.txt` files; the 120 frozen test-sequence files are selected by exact sequence name. Archive SHA-256: `79b70e0e56c212bfb19223a22b007ad61e2cb18bf127c16319982f6c61cf6cea`.
3. Range-read only the 120 `IR_label.json` metadata files from the public Anti-UAV410 ZIP mirror; no video pixels are required.
4. Use recovered `exist` state together with the pinned official GitHub `annos/test` bounding boxes. The reconciliation gate requires visible localization information to agree exactly.
5. Execute `scripts/extract_antiuav410_sa.py`, which mirrors the official SA scoring semantics.

## Reconciliation audit

All 120 frozen sequences and all 129,691 frames are aligned. For target-present frames:

- visible nonzero-coordinate conflicts: `0`;
- mirror-zero / official-nonzero conflicts: `0`;
- mirror-nonzero / official-zero conflicts: `0`.

Eight target-absent frames retain a nonzero official exported box. These do not affect State Accuracy because the evaluator branches on `exist=false` and does not use the GT box in that branch. The eight frames are retained explicitly in `data/anti_uav410_irlabel_recovery_manifest_v8.json`; they are not silently corrected or dropped.

## Frozen primary endpoint

The final output is `data/anti_uav410_siamfc_SA_i_v8.csv`:

- unique sequences: `120`;
- exact match to the frozen design-frame sequence set: yes;
- SHA-256: `4049ca9c83128e2a2c8e244c30597a95431f1489efb2f69cda536c8e4873a886`;
- equal-sequence population mean SA: `0.351505497767269`.

`data/anti_uav410_siamfc_SA_i_manifest_v8.json` records the primary evidence identity, and `external_validation/PHASE2A_POPULATION_OUTCOMES_v8.md` freezes the population-level truths required for subsequent replay scoring.

## Boundary

Closing this recovery step does **not** constitute a Phase 2A validation pass. It closes only the primary-outcome availability gate. The 500 paired replay remains fail-closed until the original frozen Phase 1.2R-5 sampling engine is recovered and provenance-audited.