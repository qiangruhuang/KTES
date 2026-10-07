# KTES v8.3 — Generic IEEEtran Mapping

This file defines the intended mapping once the exact IEEE periodical is frozen. It is not a journal-specific template.

## Main floats

- Fig. 1: `figure*` at top of page, `width=\textwidth`.
- Table I: prefer one-column `table`; promote to `table*` only if wrapped text reduces readability.
- Fig. 2: `figure*` at top of the R5-results page.
- Table II: `table*`, preferably below the associated result paragraph or on the following top float.
- Fig. 3: `figure*` at top of the layered-external-evidence page.
- Table III: `table*` following Fig. 3; do not place before the figure because the visual evidence-class hierarchy is the primary first-pass display.
- Fig. 4: `figure*` at the start of Discussion or the next available top-of-page float.

Use standard IEEE `\caption{}` + `\label{}` + `\ref{}` mechanics. Avoid hard `[H]` placement and avoid adding a caption package unless required by the selected journal template.

## Recommended labels

- `fig:method`
- `tab:contract`
- `fig:r5`
- `tab:r5`
- `fig:external`
- `tab:external`
- `fig:gates`

Supplement:

- `tab:s-r5`
- `tab:s-antiuav`
- `tab:s-amovfly`
- `tab:s-evidence`

## Graphics source and final export

Canonical research masters are:

- `FIG1_METHOD_ARCHITECTURE_v8_3.svg`
- `FIG2_R5_CONFIRMATION_v8_3.svg`
- `FIG3_EXTERNAL_EVIDENCE_v8_3.svg`
- `FIG4_VALIDITY_GATES_v8_3.svg`

Final template mapping should point to PDF/EPS exports generated from exactly these masters, not to independently redrawn copies.
