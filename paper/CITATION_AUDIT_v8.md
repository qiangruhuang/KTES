# KTES v8 Citation Audit

**Date:** 2026-10-07  
**Scope:** `PAPER_IEEE_v8.md`  
**Status:** PASS after one bibliographic correction

## 1. Audit objective

This audit verifies that the v8 manuscript uses its reference list in the body, that key method and external-data identities match authoritative publication records, and that no unpublished AMOVFLY manuscript is represented as peer-reviewed evidence.

## 2. Correction made

The first author of *Test case sampling optimization for safety validation of automated driving systems* is **Chen Qian**, cited in Western bibliographic order as **C. Qian**, not `Q. Chen`. Reference [6] was corrected accordingly.

Verified record:

- C. Qian, J. Xu, X. Xing, and F. Guo, *Nature Communications*, vol. 17, art. 3114, 2026, doi: `10.1038/s41467-026-69675-8`.

## 3. Key identity checks

- **Cube method:** J.-C. Deville and Y. Tille, *Biometrika*, 91(4), 893–912 (2004), doi `10.1093/biomet/91.4.893`.
- **Local pivotal sampling:** A. Grafstrom, N. L. P. Lundstrom, and L. Schelin, *Biometrics*, 68(2), 514–520 (2012), doi `10.1111/j.1541-0420.2011.01699.x`.
- **Horvitz–Thompson:** D. G. Horvitz and D. J. Thompson, *JASA*, 47(260), 663–685 (1952).
- **Anti-UAV410:** B. Huang et al., *IEEE TPAMI*, 46(5), 2852–2865 (2024), doi `10.1109/TPAMI.2023.3335338`; first published online 22 Nov 2023.
- **IDF-DS descriptor:** C. Garcia-Gascon et al., *Scientific Data*, 13, 364 (2026), doi `10.1038/s41597-026-06716-3`.
- **Finite-population reliability demonstration:** J. Jeon and S. Ahn, *Sustainability*, 10(10), 3671 (2018), doi `10.3390/su10103671`.
- **AMOVFLY:** cited only as the frozen `YujiaoHu/AMOVFLY-Dataset` repository at commit `67069ed00ddbebd62b71aa9bb1272415e9b15ff8`; the associated manuscript is not represented as a published peer-reviewed source.

## 4. In-text reference closure

All references [1]–[17] are now cited at least once in the manuscript body. Method citations are attached to the relevant established components rather than to c-pKTES-Hedge as if those components were newly invented.

The external dataset citations are placed in the evidence-protocol subsections:

- Anti-UAV410 → [11];
- IDF-DS → [12], [13];
- AMOVFLY → [14].

## 5. Claim-boundary check

The citation pass does not change the evidence hierarchy:

- the v7 target-alignment KTES algorithm is not cited as identical to c-pKTES-Hedge;
- Anti-UAV410 remains `PASS_WITH_EXECUTION_CLARIFICATION`;
- IDF-DS remains `BLOCKED_SOURCE_STRUCTURE`;
- AMOVFLY remains `NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION`;
- post-outcome exact-zero exclusion remains sensitivity evidence only.

## 6. Decision

**Citation identity:** PASS.  
**In-text citation closure:** PASS.  
**Modern external-source identity:** PASS.  
**Unpublished-source overstatement:** NONE FOUND.  
**Remaining citation blocker before Markdown freeze:** NONE.
