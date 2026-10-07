# KTES v8.3 — Reference Format Audit

**Status:** PASS for generic IEEE preparation; final target-journal validation still required.

## Actions completed

- retained the 17-reference numbered order used by the frozen manuscript;
- normalized verified author diacritics in the manuscript and BibTeX source where applicable: Tillé, Grafström, Lundström, Särndal, Schölkopf;
- retained DOI `10.1093/biomet/91.4.893` for the cube method;
- retained DOI `10.1111/j.1541-0420.2011.01699.x` for the local pivotal paper;
- added publisher DOI metadata for the two NIPS 19 chapters:
  - `10.7551/mitpress/7503.003.0069`;
  - `10.7551/mitpress/7503.003.0080`;
- retained IEEE DOI `10.1109/24.589960` for the small-binomial reliability paper;
- created `references_v8_3.bib` with 17 entries;
- offline BibTeX validation returned **0 issues**.

## Items intentionally not over-normalized

- Journal names remain in readable full form in the Markdown manuscript. The exact target IEEE template/bibliography style may abbreviate them automatically.
- The GitHub dataset reference remains a repository citation with frozen commit and access date because no separate archival DOI is asserted in the frozen evidence source.
- `et al.` in reference [7] is retained from the frozen manuscript; the final bibliography engine should expand the complete author list if the source BibTeX is later upgraded.

## Gate conclusion

No reference issue presently changes a scientific claim. Remaining work is bibliography-engine/template normalization after the target periodical is selected.
