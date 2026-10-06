# Phase 2A frozen sampling-engine provenance gate v8

**Updated:** 2026-10-06  
**Status:** **CLOSED / PASS**

The provenance gate that previously blocked the 500 paired Phase 2A replays is closed. The original Phase 1.2R-5 implementation lineage was recovered from the 2026-09-29 KTES handoff materials and linked to the earlier Phase 1.2R2 dependency source rather than reconstructed from the external-validation outcomes.

## Recovered historical implementation

The recovered R5 lineage includes the authoritative files named in the handoff:

- `src/run_r5_pps_confirm.py` — SHA-256 `ad20c3c180f20a97c90e80cc5513e29e2de764c0b49382810c4b1202c7c55e3f`;
- `src/run_r5_pps_confirm_chunk.py` — `9e0fe542304ab6c3bf0fe71a527238aa864dd436b7e0399fff62b728fda09bf2`;
- `src/run_r5_uq_audit_chunk.py` — `c6b0ed6c6eaf65c39a32b79d8c47831b80ae27bd7a309163cda665426f24dcdf`;
- `src/phase12r/r5_designs.py` — `1c62fb55dc7b9156148d6ee369ce5ce5148be9d19c257b30325bb3875f3b91ed`;
- `src/phase12r/r5_estimators.py` — `c32407ce52d2c933a3aadb7d0103d6da14799012ef20ce8aefffa845ab538736`.

The R5 files depend on earlier Phase 1.2R modules. The exact runtime dependencies used by Phase 2A are committed under `vendor/r5_engine_recovered_v8/src/phase12r/` with `vendor/r5_engine_recovered_v8/SHA256SUMS.txt`. The CI workflow fails before replay execution if any committed runtime byte differs from its historical SHA-256.

The broader source-recovery inventory and archive provenance are recorded in `data/r5_source_recovery_manifest_v8.json`.

## Historical behavior regression

Source presence alone was not accepted as sufficient. The recovered implementation was rerun against frozen R5 confirmation fixtures before Phase 2A execution:

- 50 historical tasks across 5 scenarios and MC indices 0–9;
- 150 method rows;
- 3,450 numeric cells checked;
- maximum absolute difference `7.105427357601002e-15`;
- acceptance tolerance `1e-12`;
- row/key identity: PASS.

This demonstrates deterministic behavioral identity at substantially tighter tolerance than any Phase 2A reporting precision.

## Independent Phase 2A execution

GitHub Actions independently executed the frozen Phase 2A analysis at commit `44357d40de298d4a3b19e6dfe629d43464865a88`, run `37422551437`. The job verified the recovered runtime hashes, compiled the replay adapter, verified the frozen frame and `SA_i` hashes, instantiated the design object, completed all 500 paired replays, hashed the evidence and uploaded the artifact. Every step passed.

The resulting Phase 2A classification is `PASS_WITH_EXECUTION_CLARIFICATION`; see `external_validation/PHASE2A_CI_EVIDENCE_v8.md` and `external_validation/PHASE2A_500_REPLAY_RESULT_v8.md`.

## Research-integrity conclusion

The sampling engine used for Phase 2A is not a prose-based post-outcome reconstruction. The historical source lineage, byte hashes and behavior regression are all documented. No Phase 2A outcome was used to retune rho, lambda, sentinel count or portfolio, inclusion-probability floor, Local Cube rule, estimator family, R3 UQ constants, primary endpoint, sample budget or guardrail thresholds.
