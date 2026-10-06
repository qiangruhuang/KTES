# Phase 2A CI evidence freeze v8

**Date:** 2026-10-06  
**Repository:** `qiangruhuang/KTES`  
**Execution commit:** `44357d40de298d4a3b19e6dfe629d43464865a88`  
**GitHub Actions run:** `37422551437`  
**Job:** `112134913235`  
**Artifact:** `phase2a-v8-500-replay`, artifact ID `11393801731`

## Independent execution checks

The CI job completed successfully after all of the following fail-closed checks passed:

1. SHA-256 verification of the recovered historical R5 runtime sources;
2. static compilation of `scripts/run_phase2a_500_replays.py`;
3. SHA-256 verification of the frozen Anti-UAV410 design frame and `SA_i` outcome artifact;
4. deterministic Phase 2A design-object instantiation;
5. all 500 paired replays for c-pKTES-Hedge, stratified SRS, and Split15+Audit25;
6. output hashing;
7. artifact upload.

The design object selected the same three frozen NRR certainty sentinels on every replay:

- `20190926_111509_1_9`;
- `3700000000002_162623_1`;
- `new6_train_newfix`.

One non-sentinel probability-remainder unit, `20190925_124000_1_10`, is naturally capped at first-order inclusion probability 1 by the frozen `_capped_inclusion` algorithm. It remains part of the 37-unit probability-remainder design identity and is therefore retained when computing the preregistered remainder ESS.

The disclosed Split15+Audit25 external adapter yields audit allocation `7/11/6/1` across Tiny/Small/Medium/Normal after removing the 15 deterministic units.

## Frozen CI output hashes

- `PHASE2A_500_REPLAY_RESULT_v8.md`: `5011a73dc977eb39ac9372ca57decb811437f27dc6bca4a129e87bfe360e77a7`
- `PHASE2A_DESIGN_OBJECT_v8.json`: `2a686908e42a1134578c07eecce9ca3be8336ff08c37c8d3622ff2a2855184dc`
- `phase2a_500_replay_paired_v8.csv`: `2b5621e5d30ee075fcb209c35f1fd02f12cfbf5980105b5c146e60b9fd8c4190`
- `phase2a_500_replay_raw_v8.csv`: `423b6a96652a8cb1f19adb85762c7d90d4e0ded2ee9286057452460635d3866d`
- `phase2a_500_replay_summary_v8.csv`: `637b0652872b863b28ec471dab4c8c311c0ae2dd6bb0306c114ee19c8eb26813`
- `phase2a_result_gate_v8.json`: `a4a24b60599cdb237538165cee0b958de21ee1556cf393e806fbf08cbd698fc9`

The uploaded artifact ZIP digest is `f765251f44cb3e99adf9344a3dbcef275ab34b389957ea944d7cbca3cb3b6f89`. The downloaded artifact was independently unpacked and all six file hashes above were rechecked against the runner log; all matched exactly.

The raw 1,500-row replay matrix is retained in the CI artifact and is deterministically regenerable from the committed frozen inputs, hash-verified R5 runtime and replay script. The repository commits the primary result, result gate, summary and paired-comparison tables; the raw matrix is referenced by hash rather than duplicated as a generated output.

## Evidence classification

All numerical Phase 2A guardrails pass. The correct classification is **PASS_WITH_EXECUTION_CLARIFICATION**, not a pristine preregistered PASS, because the split-style comparator's exact 15+25 numerical adapter and the finite-domain critical-domain estimator required execution clarification after `SA_i` recovery. Neither clarification changes c-pKTES-Hedge constants, endpoint, feature frame, strata, n=40 allocation, seed block or guardrail thresholds.
