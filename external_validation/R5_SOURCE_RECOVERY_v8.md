# R5 source recovery and behavioral identity audit v8

**Date:** 2026-10-06  
**Result:** **PASS — frozen implementation lineage recovered.**

The Phase 2A provenance blocker is closed. The 2026-09-29 handoff archive contains the original R5 confirmation runner, chunk runner, UQ runner, `r5_designs.py`, and `r5_estimators.py`, together with an internal SHA-256 manifest. Required lower-level Local Cube, kernel, variance and estimator dependencies were recovered from the frozen Phase 1.2R2 package rather than reimplemented from prose.

## Archive identities

- Handoff archive SHA-256: `232aed9a74de3884f72916c2859e9004dd6b8624cbf20a28d6e9775f99f78fe2` (405,815 bytes).
- Phase 1.2R2 archive SHA-256: `38bc660d88d79c19d42884e59b86e578b19a43eea5bf4835e815f250abe83cc1` (9,460,049 bytes).
- Recovered vendor archive SHA-256: `be3c1c4e917db41235a3f4d9889a826bc15a756b6c2e050b57690030c4d6921e` (17,030 bytes).

The R5 files match the handoff package SHA-256 manifest, including:

- `r5_designs.py`: `1c62fb55dc7b9156148d6ee369ce5ce5148be9d19c257b30325bb3875f3b91ed`
- `r5_estimators.py`: `c32407ce52d2c933a3aadb7d0103d6da14799012ef20ce8aefffa845ab538736`
- `run_r5_pps_confirm.py`: `ad20c3c180f20a97c90e80cc5513e29e2de764c0b49382810c4b1202c7c55e3f`
- `run_r5_pps_confirm_chunk.py`: `9e0fe542304ab6c3bf0fe71a527238aa864dd436b7e0399fff62b728fda09bf2`
- `run_r5_uq_audit_chunk.py`: `c6b0ed6c6eaf65c39a32b79d8c47831b80ae27bd7a309163cda665426f24dcdf`

## Behavioral regression

The recovered R2 dependencies and R5 overlay were assembled without edits and rerun for MC indices 0–9 across all five historical scenarios using the frozen seed `20261115`. The regenerated 150 method rows were compared against the archived `r5_confirm_raw.csv`.

- keys identical: yes;
- numeric cells checked: 3,450;
- maximum absolute numerical difference: `7.105427357601002e-15`;
- mismatches above `1e-12`: 0.

This establishes deterministic behavioral identity for the audited subset and is sufficient to remove the previous claim that the R5 executable source was unavailable.

## Consequence for Phase 2A

The 500 paired replay may now use the recovered sampling engine. External adaptation is restricted to mapping the already frozen Anti-UAV410 outcome-blind features, four size strata, n=40 allocation, NRR sentinel portfolio, `rho=.20`, `lambda=3`, minimum probability fraction `.35`, and replay seeds. No source-level method change is permitted.
