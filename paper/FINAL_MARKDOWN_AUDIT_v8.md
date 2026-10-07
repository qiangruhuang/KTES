# KTES v8 Final Markdown Audit

**Date:** 2026-10-07  
**Target:** `PAPER_IEEE_v8.md`  
**Decision:** PASS FOR MARKDOWN RESEARCH FREEZE

## Checks completed

1. **Method identity:** PASS. v8 is built around c-pKTES-Hedge; the v7 `M=50 / n=10 / eta=0.6` predecessor is not presented as the Phase 2 method.
2. **Development/confirmation separation:** PASS. R5 confirmation is explicitly independent of R1–R5 tuning; R3 calibration is frozen before confirmation.
3. **Anti-UAV evidence hierarchy:** PASS. Directly frozen noninferiority/ESS/support results are distinguished from comparator-sensitive execution clarifications.
4. **IDF-DS handling:** PASS. Source-structure block is preserved as a preoutcome eligibility result, not a performance result.
5. **AMOVFLY endpoint integrity:** PASS WITH LIMITATION. Original numerical result, semantic defect, and post-outcome sensitivity are all retained side by side.
6. **Reproducibility claim:** PASS. The low-level cause of inclusion-probability drift is stated as unresolved; immutable realized design object is required.
7. **Safety/UQ wording:** PASS. No distribution-free or broad operational-certification claim is made.
8. **Edge-discovery claim:** PASS. The 81.2% vs 77.9% result is not described as statistically established superiority.
9. **Legacy-method scan:** PASS. No `M=50`, `n=10`, or `eta=0.6` remains in the v8 manuscript body.
10. **Citation closure:** PASS. References [1]–[17] are all used in text; KTCS first-author identity corrected to C. Qian.
11. **Document-generation gate:** CLOSED. Markdown is ready for user review; DOCX/PDF requires explicit approval.

## Residual limitations that must remain visible

- R5 remains controlled/simulation evidence.
- Anti-UAV410 has execution clarification and SRS has lower profile error.
- IDF-DS provides no performance estimate.
- AMOVFLY's literal endpoint is semantically contaminated.
- AMOVFLY post-outcome sensitivity is not independent confirmation.
- exact numerical backend responsible for AMOVFLY design-regeneration drift is not isolated.
- two independent external real-data comparisons do not imply general field certification.

## Research decision

No additional experiment is required to close the current v8 Markdown research cycle. The scientifically appropriate next step is manuscript/figure refinement and external peer review. Any further engineering validation should be independently preregistered with endpoint-clean semantics rather than using AMOVFLY outcome knowledge to construct a new confirmation.
