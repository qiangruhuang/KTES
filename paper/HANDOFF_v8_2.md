# KTES v8.2 Submission-Compressed Manuscript Handoff

## State

v8.2 is a presentation-only revision of frozen `PAPER_IEEE_v8.md`. It introduces no new experiment, retuning, endpoint change, or evidence-class change.

## Canonical v8.2 files

- `paper/PAPER_IEEE_v8_2.md`
- `paper/SUPPLEMENTARY_INFORMATION_v8_2.md`
- `paper/FOUR_WAY_CONSISTENCY_AUDIT_v8_2.md`
- `paper/ADVERSARIAL_REVIEW_v8_2.md`
- `paper/HANDOFF_v8_2.md`
- `paper/figures/FIG1_METHOD_ARCHITECTURE_v8.svg`
- `paper/figures/FIG2_R5_CONFIRMATION_v8.svg`
- `paper/figures/FIG3_EXTERNAL_EVIDENCE_v8.svg`
- `paper/figures/FIG4_VALIDITY_GATES_v8.svg`

## GitHub freeze state

- deterministic figure-builder correction commit: `3153df48e4ef1684f12da8b8be4dae6751a59b6a`;
- figure rebuild CI run: `37601908428`, conclusion `success`;
- canonical Fig. 3 now includes both frozen profile-error 95% CIs and the exact AMOVFLY evidence class containing `CONFIRMATORY`;
- v8.2 main-manuscript commit: `3c8afcd3691ae553f84ed61844243dca9f2b3a7a`.

## Main-paper structure

- four main figures;
- three main tables;
- compressed method/evidence protocol;
- one controlled-confirmation results section;
- one integrated layered-external-evidence section;
- discussion organized around validity gates rather than dataset-by-dataset repetition.

## Supplement structure

S1–S10 retain development history, estimator/UQ details, R5 detail, Anti-UAV comparator/ESS evidence, IDF-DS source gate, AMOVFLY confirmatory table, endpoint-semantic audit, post-outcome sensitivity, realized-design reproducibility audit, and evidence manifest.

## Mandatory claim boundaries

Do not change the following labels or interpretations in journal formatting:

- R5 edge-hit superiority is **not** established because its paired CI crosses zero.
- Anti-UAV410: `PASS_WITH_EXECUTION_CLARIFICATION`.
- IDF-DS: `BLOCKED_SOURCE_STRUCTURE`; no performance result.
- AMOVFLY: `NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION`.
- exact-zero AMOVFLY exclusion: post-outcome diagnostic sensitivity only.
- realized design object: immutable confirmatory research input when downstream inference depends on `pi_i`.

## v8.2 audit outcome

- Four-way consistency: **PASS AFTER ONE PRESENTATION-ONLY CORRECTION**.
- Adversarial review: **MINOR REVISION / FORMAT-READY AFTER NON-SCIENTIFIC CLEANUP**.
- New experiments required: **none**.
