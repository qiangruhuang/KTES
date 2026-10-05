# Phase 2A frozen sampling-engine provenance gate v8

**Date:** 2026-10-05  
**Status:** **OPEN / FAIL-CLOSED**

Phase 2A cannot execute the 500 paired sampling replays until the executable implementation used for the frozen Phase 1.2R-5 confirmation is recovered or byte-level equivalence to an archived implementation is established.

## Required historical implementation

The 2026-09-29 project handoff identifies the relevant implementation paths as:

- `src/run_r5_pps_confirm.py`
- `src/run_r5_pps_confirm_chunk.py`
- `src/run_r5_uq_audit_chunk.py`
- `src/phase12r/r5_designs.py`
- `src/phase12r/r5_estimators.py`

These are the authoritative implementation lineage for the frozen c-pKTES-Hedge sampling engine.

## Recovery audit performed

The Library artifact `KTES_revision_v7_package.zip` was successfully materialized and audited on 2026-10-05. Its size is 2,496,655 bytes and SHA-256 is `e09d37322f2ffd8e1e447da7b6ac1ad6b531590a4b655b1f91e49a0bacdf5bcc`. The archive contains 44 entries, including the v7 manuscript, audit, handoff, and `replication_v7/ktes_demo` code, but contains none of the five frozen R5 implementation files above and no `phase12r` directory.

The older `replication_v7/ktes_demo/ktes.py` is present (SHA-256 `81ca5e6a9c09892f6b5b9a2140eed461f47a0f3d25ec6c1b6065c36177023ebd`) but is not accepted as a substitute because its provenance does not establish identity with the R5 c-pKTES-Hedge engine.

Exact-name searches of the connected Drive for `r5_designs.py`, `KTES_Phase1_2R5`, and `KTES` returned no R5 source artifact. The currently accessible 2026-09-29 handoff archive cannot be raw-materialized through the available Library path.

## Why prose reconstruction is prohibited

The frozen contract fixes the high-level portfolio, rho, lambda, probability floor, compound-tail mixture, and Local Cube requirement, but does not uniquely determine the numerical kernel-novelty operator, normalization details, tie handling, probability construction, or exact balanced-sampling implementation. Recreating those decisions from prose after external outcomes have become visible would introduce an unregistered implementation degree of freedom.

## Closure criteria

This gate closes only if one of the following is obtained:

1. the five historical R5 files from the original Phase 1.2R-5 execution workspace, with recorded SHA-256 hashes; or
2. an archived implementation whose byte identity or deterministic output identity against the frozen R5 confirmation fixtures can be demonstrated.

Until then, the Phase 2A finite-population frame and primary outcomes may be frozen, but sentinel assignment, inclusion probabilities, Local Cube draws, and the 500 paired replay result must not be reported as executed.
