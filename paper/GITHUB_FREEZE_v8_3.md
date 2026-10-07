# KTES v8.3 GitHub Freeze Provenance

## Status

The v8.3 journal-format layer is frozen as a presentation-only transformation of the previously frozen scientific evidence. No new experiment, retuning, endpoint redefinition, or evidence-class change was introduced.

## Canonical figure gate

- Figure builder gate introduced at commit `3ce74f86f6e61d151cb3cc44b312984c844f5b2b`.
- First run `37656697979` failed closed because the builder wrote to the wrong output directory; no canonical v8.3 figures were committed.
- Path correction commit: `7f0e26f93fb3c86c382ae62da6d189d49c608660`.
- Second run `37657076830` passed figure generation and font checks but exposed a CI bug: `git diff --quiet` ignored newly generated untracked figures, so the workflow did not commit them.
- Commit-condition correction: `fb2e71eb73c5af8a9bed300009cb00307e848f4b`.
- Final canonical figure run: `37657191603`.
- Canonical figure commit: `2a71600eaddc2d6273f2f8f3ad0013191eaf85b9`.
- All four SVG vector masters parse as XML and retain minimum rendered text size of approximately 9.23 pt at IEEE 7.16-in two-column width.

## Canonical text-materialization gate

The v8.3 manuscript, Supplementary Information, BibTeX source, format audits, handoff, manifest, and structural-audit script are transported as a compressed byte-pack with per-file SHA-256 verification.

- First materialization run `37657966833` failed closed because `part01.b64` was truncated during connector upload (9,948 bytes instead of 15,812); no canonical text assets were committed.
- The intact `part02.b64` was retained.
- Restored `part01.b64` blob SHA: `9b82a35ea3471fd69e27734d59ccb7d721de71d1`.
- Restoration commit: `ea831fd419ce492861fad6e8c6246884b7502f9f`.
- Successful materialization run: `37658623957`.
- Canonical text commit: `b9e5e4bd6bdf929511b8df3e3ba69b885667afc6`.
- All 12 canonical text assets passed their frozen SHA-256 checks before and after writing.

Key frozen text hashes:
- `paper/PAPER_IEEE_v8_3.md`: `c90b1c20b9e605db8e30da1a70250ec0ea9eaf57cfcccddca1bd0f4b13f5a7e1`
- `paper/SUPPLEMENTARY_INFORMATION_v8_3.md`: `38d2dd47b56e26605fb77853490969485eee4a04f60682c90ba0ab27612de6da`
- `paper/references_v8_3.bib`: `ba4367a0233ef569643b9dacd96b6381370fdaaeb660657d53857033d035b40a`

## Independent final submission audit

- Audit workflow commit / audited repository state: `9372551a22146e276e45dba2fdf7e222cf3461db`.
- Audit run: `37658719995`.
- Result: **39/39 PASS**.

The audit verifies four v8.3 figure paths with no stale v8 paths; three main tables; Supplementary Sections S1-S10 and Tables S1-S4; exact external evidence classes; required adverse/limiting numerical results; no R5 edge-superiority claim; no IDF-DS performance result; the AMOVFLY placeholder limitation and immutable realized-design requirement; all figure/table references before presentation; all four figures at >=9 pt at two-column width; and 17 manuscript references matched by 17 BibTeX entries.

## Claim boundary

The science remains frozen. v8.3 is ready for generic IEEE journal layout preparation, but a literal page-by-page compiled-PDF gate must wait until the exact target IEEE periodical/template is frozen. SVG files remain reproducible vector masters; final journal figure export should use the target periodical's accepted vector/raster format after that template decision.
