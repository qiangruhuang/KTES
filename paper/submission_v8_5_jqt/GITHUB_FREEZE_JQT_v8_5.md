# KTES v8.5 JQT — GitHub Canonical Freeze

**Freeze date:** 10 October 2026  
**Branch:** `paper/jqt-v8.5`  
**Canonical materialization commit:** `30b2af5305a1f62c54c76a41bb5bfe60301a7225`  
**Materializer workflow run:** `38002786906`  
**Workflow conclusion:** `SUCCESS`

## Fail-closed verification

The successful materializer checked four transport chunks before decoding, then checked every canonical submission file against its frozen SHA-256, copied the four frozen manuscript figures to neutral reviewer-facing filenames, and checked each copied figure against its source.

### Canonical submission files

| File | SHA-256 |
|---|---|
| `MANUSCRIPT_JQT_v8_5_BLINDED.md` | `58cfbd564e5f0d2be703891bdc145cd3a14b4aa2de5ab91417a5c179bf22c6b5` |
| `SUPPLEMENTARY_INFORMATION_JQT_v8_5_BLINDED.md` | `5ad0b62c22990ce728e80459f146187e691fa251b5523cfef05a1e3b4664309b` |
| `TITLE_PAGE_JQT_v8_5.md` | `5960f756ec437296c4de44bad077413a8554b211a517e94eb2288da01ad7ccff` |
| `COVER_LETTER_JQT_v8_5.md` | `744b7a1b9af6909b8b547114255752ce4671f591f0adbc8e3a777d2c03fc94d6` |
| `references_JQT_v8_5.bib` | `ef28eb9e6b9788a271dc932a4614c102f9e656b66e911a8aff000a0b455116d1` |
| `BLINDED_REPRODUCIBILITY_MANIFEST_v8_5.md` | `44e1054d5b955eb1e3ee7756565b72efaa9ccf4369b467e8291977ad7cd545d7` |
| `SUBMISSION_FREEZE_AUDIT_JQT_v8_5.md` | `c4cf5185fa16eb09052c371d9cd78d49c3fb307cc39daae9d4f71856c0aa4442` |
| `SUBMISSION_READINESS_JQT_v8_5.md` | `f3d70271d9109000153e36c8eaedbc871ef8b7a6f9872e6fe821274f4cfd951d` |
| `ADVERSARIAL_REVIEW_JQT_v8_5.md` | `eca506b9722e459fb82ee264600bdc336dfab18ec01dfcf7f472e48cae9b6eec` |
| `HANDOFF_JQT_v8_5.md` | `00982bdc038a7247c5881e19cf04025ce4efac060c85858233c4fff35f0cbcd8` |

### Neutral reviewer-facing figures

| Figure | SHA-256 |
|---|---|
| `figures/figure1.svg` | `ad6889ddac76fc6916ac63f35a68587162bab6a3f764477ebd07c0ef79c8b8fd` |
| `figures/figure2.svg` | `487a994d5a16833aa2172eb48b7e7fc414d5c690a3ed2a1ff7ea62470dcfd407` |
| `figures/figure3.svg` | `a2e36131d8c86c4e2a7160e64fa8d5e02c2a511d680f6343f07241ce17ff76c7` |
| `figures/figure4.svg` | `b9c7ecc33bda7461fba77b4256b4efc7297af2cba4165fe9b692149780a79cae` |

## Submission-gate interpretation

This commit freezes the **scientific/textual JQT v8.5 submission package**. It does not assert that author-owned metadata are complete, and it does not substitute for the anonymous reviewer reproducibility archive.

No scientific result, endpoint, comparator, threshold, evidence class, or claim ceiling was changed during GitHub materialization.

## Non-canonical transport files

Files under `.github/submission_payloads/` and the materializer workflow are transport/provenance infrastructure only. They are not reviewer-facing manuscript components and are not part of the scientific evidence object.
