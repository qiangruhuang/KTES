# PAPER_IEEE_v8 lossless source split

The v8 Markdown manuscript is split only to make connector-level repository transfer auditable. The seven files are consecutive original line ranges; no content transformation is applied.

Frozen reconstructed identity:

- bytes: `49485`
- SHA-256: `710702c979036957cc00ad5b385965802331175d9d1d71d2f1573ca5c81e4bc1`
- lines: `639`

Part identities:

| Part | Lines | Bytes | SHA-256 |
|---|---:|---:|---|
| part01.md | 100 | 13532 | `43fe40b99ccbda4d633d718bb525a53f6ed5b5f91cdd578e9784d8e9ad18655b` |
| part02.md | 100 | 2889 | `b6c4e61546d4aa28a4b56b48502be0d980108da4d2c944a17c4532d58c05c0b4` |
| part03.md | 100 | 5112 | `f0be2abb3977531f2208206fc6bdec26b97d10769aa62a97569058e889ebca97` |
| part04.md | 100 | 8731 | `bb4d4ef8cb9bba6a4608e8ab9567f48058b22101e326b9a6e1088ad0ce9e54f3` |
| part05.md | 100 | 9343 | `30e43f2f580b446d75657fd1cfd9cd4265c91f9a6c51c7edd45a654987f3942c` |
| part06.md | 100 | 8351 | `abc10bbb112b4a685b864d942bdd1798dfa5ff274d0a6c4924b426db0dc12d6c` |
| part07.md | 39 | 1527 | `f8921e7c2b8f1557d341dc28c3ee1c4f1c54f1d3ba6679d6db9eb6212be2b14b` |

Rebuild from repository root:

```bash
python scripts/rebuild_paper_ieee_v8.py
```

The rebuild fails closed unless both byte count and SHA-256 match the frozen manuscript.
