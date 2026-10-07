# KTES v8.3 — IEEE Journal-Format Gate

**Scope:** presentation-only transformation of frozen v8.2 evidence.  
**Scientific status:** closed; no new experiment, retuning, endpoint change, or evidence-class change.  
**Gate result:** **PASS FOR GENERIC IEEE JOURNAL LAYOUT PREPARATION; TARGET-JOURNAL TEMPLATE STILL REQUIRED.**

## 1. External formatting basis

The current IEEE Author Center guidance was used only for formatting constraints, not scientific content. The relevant guidance is:

- use the IEEE article template selected for the target periodical;
- typical journal graphic widths are one column (3.5 in / 88.9 mm) or two columns (7.16 in / 182 mm);
- vector graphics are preferred for resizing;
- figure type should reproduce at approximately 9–10 pt at final display size;
- accepted final graphics include PS/EPS/PDF/PNG/TIFF; SVG is therefore retained here as the reproducible vector **source master**, not the final submission format;
- figures and tables should communicate trends versus exact values, respectively.

No target IEEE periodical has yet been frozen, so v8.3 does not invent journal-specific page limits or supplementary-file rules.

## 2. Main-manuscript changes from v8.2

- Abstract compressed from 295 to ~216 words without changing any evidence class or numerical claim.
- Main text remains organized as Introduction–Related Work–Problem–Method–Evidence Protocol–Results–Discussion–Conclusion.
- Table I compressed from 10 rows to 6 rows by grouping method-contract fields.
- Table III compressed from 5 columns to 4 columns.
- All four figures are explicitly introduced in prose before their captions.
- Figure paths now point to the v8.3 IEEE-width-optimized vector masters.
- Reference names with diacritics were normalized where externally verified (e.g., Tillé, Grafström, Lundström, Särndal, Schölkopf).
- DOI metadata was added to the two NIPS book-chapter references [9] and [10].

## 3. Figure gate

All four figures are designed for **two-column full width** because the evidence density would make one-column reproduction unreadable.

| Figure | Intended float | Width | Minimum reproduced text | Gate |
|---|---|---:|---:|---|
| Fig. 1 method architecture | `figure*` | 7.16 in | ~9.23 pt | PASS |
| Fig. 2 R5 paired confirmation | `figure*` | 7.16 in | ~9.23 pt | PASS |
| Fig. 3 layered external evidence | `figure*` | 7.16 in | ~9.23 pt | PASS |
| Fig. 4 validity gates | `figure*` | 7.16 in | ~9.23 pt | PASS |

The v8.3 graphics deliberately remove in-graphic figure numbers and titles; numbering and explanation remain in the manuscript captions. This avoids duplicated title text and increases usable plotting area.

### Final-export rule

The canonical v8.3 SVG files are vector masters. At final submission packaging they should be exported to **PDF or EPS with embedded fonts** (or text converted to outlines) and then checked in the exact target template. No PDF/EPS export is generated in this research turn.

## 4. Table gate

| Table | Intended span | Reason |
|---|---|---|
| Table I — frozen method contract | one column if legible; otherwise `table*` | only two columns after compression |
| Table II — R5 confirmation | `table*` | five numeric columns including CI |
| Table III — external evidence | `table*` | long evidence-class and validity-boundary text |

Supplementary Tables S1–S3 should be full width. Table S4 can be one column or full width depending on target supplementary template.

## 5. Cross-reference gate

PASS:

- Fig. 1 / Table I are introduced before placement.
- Fig. 2 / Table II are introduced before placement.
- Fig. 3 / Table III are introduced before placement.
- Fig. 4 is introduced before placement.
- Supplement Sections S1–S10 and Tables S1–S4 have continuous identifiers.
- Main-text references to Supplement S1, S3, S4–S10 remain valid after compression.

## 6. Claim-preservation gate

The journal-format transformation preserves all mandatory adverse or limiting evidence:

- R5 edge-hit superiority is not claimed; its paired CI crosses zero.
- Anti-UAV410 retains the +0.00404 profile-error disadvantage vs SRS and the exact class `PASS_WITH_EXECUTION_CLARIFICATION`.
- IDF-DS remains `BLOCKED_SOURCE_STRUCTURE` with no performance result.
- AMOVFLY remains `NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION`.
- exact-zero AMOVFLY exclusion remains post-outcome diagnostic sensitivity only.
- immutable realized-design provenance remains a methodological requirement.

## 7. Reference gate

- Main manuscript: 17 numbered references.
- Parallel `references_v8_3.bib`: 17 entries.
- Offline BibTeX syntax/field validation: **0 issues**.
- References [1], [2], [9], [10], and [16] were additionally cross-checked against publisher/IEEE metadata during the v8.3 gate.

## 8. Remaining non-scientific blockers

Before a true submission package can be declared complete:

1. freeze the exact IEEE target periodical and download its current template;
2. map the Markdown into that template;
3. export SVG masters to accepted PDF/EPS graphics with embedded fonts;
4. compile and run a literal page-by-page PDF visual audit;
5. run IEEE LaTeX/reference/PDF validation tools where applicable;
6. insert final author list, affiliations, funding, conflict/data/code statements, and any journal-specific declarations.

None of these items requires reopening the scientific analysis.
