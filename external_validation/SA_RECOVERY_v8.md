# Phase 2A State Accuracy recovery note

The supplied `performance.json` cannot yield the frozen primary endpoint because its SiamFC sequence records contain Success/Precision summaries rather than per-frame predictions or sequence State Accuracy.

The official Anti-UAV410 `Evaluation_for_SA.py` defines sequence SA by iterating over prediction, ground-truth box, and target-existence status per frame. For target-absent frames a missing/one-element prediction scores 1 and a box prediction scores 0; for target-present frames a four-coordinate prediction scores its IoU with ground truth, otherwise 0; invalid present-target ground-truth records are skipped. Sequence SA is the mean over evaluable frames.

`scripts/extract_antiuav410_sa.py` mirrors these semantics without changing the Phase 2A endpoint. The minimum evidence package is therefore:

- `test/<sequence>/IR_label.json` for all 120 official test sequences; and
- SiamFC `<sequence>.txt` prediction files for the identical 120 sequence names.

The extracted table must have exactly 120 unique names matching the frozen design frame before the 500-replay evaluator is allowed to run.
