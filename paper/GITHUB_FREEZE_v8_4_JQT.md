# KTES v8.4 JQT GitHub Freeze Provenance

## State

The JQT-targeted manuscript layer is frozen on branch `paper/jqt-v8.4`. The scientific evidence remains the previously frozen v8.3 evidence; v8.4 changes manuscript architecture, exposition, and target-journal positioning only.

## Expanded manuscript

- Canonical path: `paper/PAPER_JQT_v8_4.md`
- Main-text word-like count before References: 6590
- Abstract word-like count: 207
- SHA-256: `1a4fec05538eb2ab74d7884b2b0f38d96b09d2de3088c935d46beb2d973b3d2c`
- Automated scientific/narrative freeze audit: **23/23 PASS**
- GitHub Actions run: `37960841017`
- Materialize step: PASS
- Audit step: PASS
- Canonical manuscript commit: `a4e31330963b4334da0deb1abfea6f952135a9d6`

The first large-payload transfer failed closed because connector transport altered payload bytes. No canonical manuscript was overwritten. The successful run used smaller chunks; each chunk was verified against the expected Git blob identity before the fail-closed materializer reconstructed the manuscript and checked the full SHA-256.

## Support assets

The Supplementary Information and BibTeX source are materialized through an isolated support workflow that is not permitted to overwrite the expanded manuscript.

- `paper/SUPPLEMENTARY_INFORMATION_JQT_v8_4.md`
  - SHA-256: `4b0e5d273375d2c37b90010124dad0917f3ecfe979db97addeb4e5f6df898dce`
- `paper/references_JQT_v8_4.bib`
  - SHA-256: `ef28eb9e6b9788a271dc932a4614c102f9e656b66e911a8aff000a0b455116d1`
- Support materialization commit: `fde63df016d4e261a5d40b526de9c24c0df72f89`

## Writing and journal records

The branch also contains:

- `paper/JQT_TARGET_JOURNAL_DECISION_v8_4.md`
- `paper/WRITING_REVISION_AUDIT_v8_4.md`
- `paper/JQT_EXPANDED_FREEZE_AUDIT_v8_4.md`
- `paper/HANDOFF_v8_4_JQT.md`

## Claim boundary

Do not change without reopening the scientific gate:

- no R5 edge-hit superiority claim;
- Anti-UAV410 retains its adverse profile-error result and `PASS_WITH_EXECUTION_CLARIFICATION`;
- IDF-DS remains `BLOCKED_SOURCE_STRUCTURE` and has no method-performance result;
- AMOVFLY remains `NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION`;
- exact-zero exclusion remains post-outcome diagnostic sensitivity;
- exact realized design objects remain required for `pi_i`-dependent downstream inference;
- no universal superiority or live weapon-system certification claim.

## Next packaging gate

The research/manuscript-content gate is closed. Remaining work is submission packaging: double-anonymization, blinded code/data access, author metadata and declarations, JQT/Taylor & Francis style conversion, and literal rendered-document inspection. No new experiment is required for manuscript length or journal fit.
