# KTES v8 Claim–Evidence–Boundary Audit

**Date:** 2026-10-07  
**Scope:** `PAPER_IEEE_v8.md` first research draft  
**Decision:** major story is defensible; several claims require explicit evidence-tier labels before submission packaging.

## 1. Executive audit

The v8 story is materially stronger than a direct extension of v7 because the final algorithm and the external-validation algorithm are now identical: c-pKTES-Hedge. The evidence chain is coherent if and only if the paper distinguishes:

1. **R1–R5 method development**;
2. **independent R5 controlled confirmation**;
3. **Anti-UAV410 structural external validation with execution clarification**;
4. **IDF-DS preoutcome source-structure block**;
5. **AMOVFLY numerical confirmation with endpoint-semantic limitation**;
6. **post-outcome AMOVFLY sensitivity**;
7. **execution reproducibility audit**.

The paper must not collapse these seven evidence classes into a single “validated” label.

## 2. Major claim audit

| Claim | Evidence | Classification | Allowed wording | Prohibited overclaim |
|---|---|---|---|---|
| c-pKTES-Hedge preserves edge discovery while improving inference at n=40 | 1000-population R5 independent confirmation | Confirmatory controlled evidence | Edge hit is statistically compatible with Split15 while profile/failure/tail MAE and definitive-correct improve | “significantly improves edge discovery” |
| Certainty units can coexist with probability inference | frozen 3 certainty + 37 positive-pi design; R5 and external replays | Method/mechanism evidence | certainty units with pi=1 are legitimate design units and do not force undefined selection probabilities for the remainder | “deterministic cases are automatically representative” |
| Anti-UAV410 passes numerical gates | 500 paired replay CI evidence | External numerical evidence | all numerical guardrails pass; profile non-inferiority and ESS are directly frozen; comparator-sensitive gates require execution clarification | “pristine preregistered PASS” |
| KTES is uniformly better than SRS on Anti-UAV410 | contradicted by profile error | Negative evidence | KTES profile error is +0.00404 worse than SRS but within +0.01 bound; critical-domain error is lower | any uniform-superiority statement |
| IDF-DS externally fails KTES | no performance result | Source-eligibility evidence | study is blocked before outcome opening because frozen preoutcome design frame cannot be instantiated from public release | “KTES fails on IDF-DS” |
| AMOVFLY passes engineering validation | numerical gate passes but endpoint is contaminated | Limited external evidence | numerical sampling/inference comparison passes under frozen literal endpoint, then claim is narrowed by endpoint-semantic audit | “clean engineering validation success” |
| post-outcome exact-zero exclusion confirms KTES | same dataset and post-outcome endpoint change | Sensitivity only | method-comparison conclusion is robust to identified placeholder exclusion under immutable design | “independent confirmation” or “repaired primary endpoint” |
| failure-rate qualification is supported on AMOVFLY | F10=1 for all flights | Invalid endpoint for this claim | no failure-rate qualification claim | any F10 safety/failure qualification statement |
| design is reproducible from source+seed+versions | contradicted by later runner | Reproducibility boundary | immutable realized design object is required downstream unless regenerated hash matches | “seeded execution is sufficient reproducibility” |

## 3. Abstract audit

### Pass

- The abstract gives the correct n=40 architecture.
- R5 edge-hit wording correctly avoids significance overclaim.
- Anti-UAV explicitly preserves the unfavourable profile-error comparison.
- IDF-DS is described as a preoutcome block, not failure.
- AMOVFLY uses the exact final classification.
- Post-outcome sensitivity is not promoted to confirmation.

### Required tightening

The phrase “External validation is deliberately fail-closed” is acceptable, but the Abstract should make clear that Anti-UAV's full five-gate status includes an execution clarification for the Split15 adapter / domain estimator. The current wording already names the classification; no additional numerical detail is required.

The phrase “all frozen numerical comparison gates pass” for AMOVFLY must remain adjacent to the semantic limitation. Do not separate them into different abstract paragraphs in a way that lets the numerical pass read as the final engineering conclusion.

## 4. Introduction audit

### Strongest conceptual contribution

The most defensible novelty statement is not a new cube-sampling theorem. It is the **T&E-specific composition and evidence architecture**:

- certainty sentinels;
- positive-pi active remainder;
- outcome-blind novelty/compound-tail enrichment;
- Local Cube;
- Hajek model-assisted correction;
- three-state safety decision;
- frozen external-validation governance.

The Introduction should explicitly avoid claiming novelty for Cube, pivotal, Hajek, ESS, or model-assisted estimation individually.

### Potential reviewer objection

A reviewer may ask whether “certainty units with pi=1” is just standard survey sampling terminology. The response is yes; this component is standard. The contribution is using that identity to reconcile small-budget active edge coverage with probability-preserving T&E inference and then validating the resulting design under the frozen evidence chain.

## 5. Methods audit

### Frozen method identity

The manuscript correctly uses the Phase1.2R final method rather than the v7 M=50/n=10/eta=0.6 predecessor.

### UQ constants should be explicit

For full reproducibility, the manuscript should include the R3-frozen safety constants:

- failure absolute 95% calibration: `0.137719714266479`;
- safety upper calibration: `0.19767009190382911`.

These constants are evidence identities, not tunable hyperparameters in Phase 2.

### Probability-remainder pi=1 cap

The Phase2A design contains one non-sentinel remainder unit naturally capped at pi=1 by the frozen `_capped_inclusion` algorithm. The manuscript should note that “37 probability-remainder units” means design identity, not that every remainder `pi_i` is strictly less than one after capping. The current Methods wording already allows this; retain it.

## 6. Anti-UAV410 audit

### Numerically clean components

The following results are directly interpretable under the frozen c-pKTES method:

- no nonpositive inclusion-probability failure;
- probability-remainder ESS median 33.12;
- probability-remainder ESS p05 32.60;
- profile-error difference vs stratified SRS +0.00404;
- profile-error non-inferiority threshold +0.01.

### Comparator-sensitive components

The exact numerical Split15 15+25 adapter and finite-domain critical-domain estimator were clarified after `SA_i` recovery. Therefore:

- critical-domain guardrail;
- difficult-case comparison against Split15

must carry the execution-clarification label wherever used as confirmatory evidence.

Recommended main-text wording:

> “All five numerical guardrails were satisfied under the disclosed execution adapter; the profile/ESS components are directly tied to the frozen c-pKTES design, whereas the two comparator-sensitive guardrails inherit the documented post-recovery execution clarification.”

## 7. IDF-DS audit

The source block is methodologically useful but should not consume excessive Results space. Its function in the paper is to demonstrate a preoutcome eligibility rule:

> a dataset can be rich in telemetry yet unusable for confirmatory sampling design if unit-level design covariates are unavailable before outcome opening.

The paper should avoid implying that the Scientific Data paper is incorrect. The correct statement is that the **public archive structure available to the frozen protocol did not instantiate the assumed per-flight structure**, despite the article's description. This may reflect version/release organization rather than an error in the paper.

## 8. AMOVFLY audit

### Confirmatory numerical claim

The numerical comparison is real and should not be deleted after the semantic problem is found. The frozen literal endpoint was specified before telemetry outcomes were opened, and all five numerical gates passed.

### Final engineering claim

The final classification is weaker because the literal endpoint is contaminated by systematic waypoint placeholders. The paper should use “engineering-facing external dataset” rather than “clean engineering confirmation.”

### Sensitivity claim

The exact-zero sensitivity is unusually informative because it consumes the original immutable design object rather than recomputing pi. It shows that the method-comparison ranking is robust to the identified placeholder exclusion. It still remains post outcome.

## 9. Reproducibility audit

This is a potentially publishable methodological lesson rather than an embarrassment to hide.

The later runner reproduced:

- standardization means/SDs;
- kernel bandwidth;
- code hashes;
- seed lineage;
- certainty sentinels;

but changed 254/257 first-order inclusion probabilities and an example Local-Cube sample. Maximum absolute pi difference was 0.0108411663.

The fail-closed response—refusing tolerance relaxation and loading the original hashed design object—is scientifically stronger than silently accepting a “close” regeneration.

Recommended reproducibility principle:

> “For confirmatory unequal-probability designs, the realized first-order probability vector is an immutable analysis input unless a regenerated design matches the frozen design-object hash exactly.”

## 10. Adversarial reviewer questions and answers

### Q1. Is c-pKTES-Hedge genuinely new, or just unequal-probability sampling plus Cube?

**Answer:** The paper should not claim a new general sampling theorem. Its contribution is a task-specific active/probability composition for small-budget T&E, the frozen inference/UQ architecture, and the controlled-to-external evidence chain. This is a systems/statistical-method contribution.

### Q2. Why is Anti-UAV called a pass if SRS has lower profile error?

**Answer:** The gate is non-inferiority, not superiority. The observed +0.00404 KTES-SRS difference is below the prespecified +0.01 tolerance, while critical-domain error is lower and weight stability remains strong. The paper must state this plainly.

### Q3. Does the post-outcome Split15 clarification invalidate Phase2A?

**Answer:** It prevents a pristine preregistration label. It does not affect frozen c-pKTES constants, endpoint, frame, strata, allocation, seed block, or the primary SRS/ESS comparison. The correct classification is PASS_WITH_EXECUTION_CLARIFICATION.

### Q4. Does the AMOVFLY endpoint problem invalidate the whole external experiment?

**Answer:** It invalidates clean interpretation of the literal endpoint as an uncontaminated engineering performance/failure measure. It does not erase the executed sampling comparison. The sensitivity shows comparison robustness but remains post outcome. The final classification must retain the semantic limitation.

### Q5. Why include IDF-DS if there is no result?

**Answer:** Because it demonstrates the source-eligibility component of external validation and documents a scientifically correct fail-closed stop before outcome leakage. It should be concise in the main paper and detailed in supplement/repository evidence.

### Q6. If pi cannot be regenerated exactly, how can the study be reproducible?

**Answer:** Reproducibility is achieved by freezing the realized design object itself, analogously to freezing a trained model artifact. The paper should make that object part of the confirmatory data package.

## 11. Required revisions to PAPER_IEEE_v8 before submission review

1. Add the two R3 frozen UQ constants to Methods / Appendix.
2. Add one sentence in Anti-UAV Results separating directly frozen guardrails from comparator-sensitive clarified guardrails.
3. Use “engineering-facing external dataset” consistently for AMOVFLY.
4. Retain IDF-DS as `BLOCKED_SOURCE_STRUCTURE`, not a failed external validation.
5. Add an explicit sentence that Cube / local pivotal / Hajek components are established methods and that novelty is in their T&E-specific composition and evidence protocol.
6. Keep the realized-design-object requirement in both Discussion and Reproducibility Appendix.
7. Do not restore v7 M=50/n=10/eta=0.6 results as v8 headline evidence.

## 12. Gate decision

**Research logic:** PASS after listed revisions.  
**Method–evidence identity:** PASS.  
**External-validity wording:** PASS WITH REQUIRED QUALIFIERS.  
**Endpoint integrity:** AMOVFLY limitation must remain prominent.  
**DOCX/PDF readiness:** **NOT YET**. Complete revisions and one final adversarial manuscript audit first.
