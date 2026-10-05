# KTES v8 — External Engineering Validation Result Gate

Date: 2026-10-05  
Status: **BLOCKED — primary external-validation outcome is absent from the supplied JSON**  
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

Evidence identity:

- SHA-256: `7861cded4d79dfd37ce251e8167f81ce145ea8f9ed68d8dd1f4b252ca33d82a0`
- size: `19,063,146` bytes
- tracker blocks: `56`
- `SiamFC` present: yes
- `SiamFC.seq_wise` records: `120`
- sequence-level keys: `precision_curve`, `precision_score`, `speed_fps`, `success_curve`, `success_rate`, `success_score`
- sequence-level `SA`/`state_accuracy`: **absent**

Secondary SiamFC outputs in the file are:

- overall Success AUC: `0.3463100482261262`
- 20-pixel precision: `0.5317451076183254`
- success rate at IoU=0.5: `0.45729244949889203`

These are valid secondary descriptive results but cannot substitute for the frozen primary endpoint.

## 3. Why the result gate cannot yet be closed

The frozen evaluation requires per-sequence `SA_i` to construct:

- the full-population mean `mu_SA`;
- six challenge-domain SA means;
- the bottom-10% difficult-case set;
- per-replay profile and domain estimation errors;
- difficult-case-hit comparisons.

The Anti-UAV410 code path computes State Accuracy separately from the Success/Precision report stored in `performance.json`. Therefore `SA_i` cannot be reconstructed from the supplied JSON alone.

Replacing `SA_i` by Success AUC after observing outcomes would change the pre-registered primary endpoint and invalidate the external-validation claim. No such substitution is made.

## 4. Minimum additional artifact needed

Either of the following is sufficient:

- a sequence-level export with exactly the 120 frozen test-sequence names and their `SA_i` values; or
- the corresponding 120 SiamFC tracker-result files plus official Anti-UAV410 test annotations needed to run the official State Accuracy evaluator.

Outcome-blind official sequence attributes may still be used for the frozen design because they were pre-specified as design covariates.

## 5. Academic interpretation

The Phase 2A protocol remains valid and frozen. The current external-result status is **BLOCKED**, not PASS and not FAIL. Phase 1/v7 controlled evidence remains unchanged. No field-transportability claim is added until the pre-registered primary gate is actually evaluated.
