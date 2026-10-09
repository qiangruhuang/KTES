# JQT v8.5 Pre-Submission Adversarial Review

**Reviewer posture:** skeptical statistical-methods reviewer for *Journal of Quality Technology*  
**Decision simulation:** **MINOR REVISION / SEND TO REVIEW AFTER ADMINISTRATIVE COMPLETION**

## 1. Reviewer-first impression

The paper now presents a recognizable JQT problem rather than a project audit: under a hard physical-test budget, the design must discover difficult conditions without abandoning population inference. The 3-certainty-plus-37-probability architecture is easy to identify, the comparator is same-budget, and the independent confirmation is separated from method development.

The strongest paper-level contribution is not a new theorem for balanced sampling. It is the integration of active difficult-condition pressure, positive first-order inclusion probabilities, model-assisted residual correction, conservative uncertainty, and explicit execution provenance into one small-budget quality/reliability test-allocation architecture.

## 2. Likely reviewer attacks

### A. “The statistical ingredients are established; where is the novelty?”

**Risk:** High but controlled.

Cube/local pivotal sampling, unequal inclusion probabilities, Hájek correction, model-assisted estimation, and kernel measures are established.

**Current response:** The manuscript explicitly credits those foundations and claims novelty at the architecture/problem level. The R1–R5 sequence explains why a simple probability design, risk-only certainty design, and split deterministic/audit design do not solve the same small-budget trade-off.

**Required discipline:** Do not change the title/abstract to imply a new sampling theorem.

### B. “Why should three certainty units be enough?”

**Risk:** Moderate.

The design does not prove that three is universally optimal. The evidence shows that the frozen 3+37 architecture improves inference relative to Split15 while retaining aggregate edge discovery at the supported precision.

**Current response:** Correctly bounded. Hidden-bias results remain visible.

**Required discipline:** Keep “three sentinels” as the confirmed architecture, not a universal optimum.

### C. “Is the comparator fair?”

**Risk:** Moderate-low.

Both R5 methods use n=40. Split15 explicitly represents 15 deterministic difficult-case tests plus a 25-test probability audit. This is the comparison relevant to the paper's resource-allocation question.

**Residual concern:** Reviewer may request more exact Split15 construction detail. That detail should remain available in the blinded reproducibility package/Supplement.

### D. “The probability floor was underspecified.”

**Risk:** Previously real; now closed.

The submission manuscript now reports the frozen implementation parameter `min_probability_fraction=0.35`, recovered from the realized design object. No result changed.

### E. “The external validation is messy.”

**Risk:** Moderate, but this is not a reason for rejection if positioned correctly.

Anti-UAV410 contains a profile-error disadvantage but passes the prespecified non-inferiority tolerance and improves critical-domain error. IDF-DS stops before performance evaluation because the preoutcome frame cannot be instantiated. AMOVFLY has favorable numerical comparison but contaminated literal endpoint semantics.

**Current response:** The manuscript does not convert these into a universal validation claim. They are used to identify transport conditions for an active probability design.

**Required discipline:** Do not market all three as equivalent successful external validations.

### F. “AMOVFLY's endpoint problem invalidates the external evidence.”

**Risk:** Moderate.

It invalidates clean literal failure-rate qualification, not the existence of the executed numerical sample-allocation comparison. The paper keeps both facts visible and leaves the exact-zero exclusion as post-outcome diagnostic sensitivity.

**Current response:** Scientifically defensible.

### G. “How reproducible is the method if the inclusion probabilities drift on another runner?”

**Risk:** Moderate, but potentially a strength for JQT.

The paper reports the drift rather than hiding it and makes the realized design object part of the research identity. This is directly relevant to reproducible unequal-probability sampling.

**Current response:** Strong, provided the blinded review archive contains the exact realized design object.

### H. “Why is this a quality-technology paper rather than a defense/UAV paper?”

**Risk:** Low after v8.4 expansion.

The problem is framed as resource-constrained quality/reliability test allocation. Defense/UAV datasets are applications, not the definition of the method. JQT explicitly includes government and military operations in scope.

### I. “Does the AI-use statement create an editorial issue?”

**Risk:** Manageable.

Taylor & Francis requires disclosure. The statement limits AI use to editorial restructuring of existing author-provided text, language refinement, consistency/reference-format checks, and coding assistance, with human verification and responsibility. It does not claim AI generated the research design, data, analyses, or conclusions.

**Required author action:** Keep the pre-AI / earlier manuscript versions and project audit trail available in case the editor requests clarification.

## 3. Claim ceiling

The strongest defensible claim is:

> A small certainty portfolio can be embedded within a positive-inclusion-probability design to improve the controlled inference–discovery trade-off at n=40, while external transport depends on preoutcome source structure, endpoint semantics, and preservation of the realized design object.

The evidence does **not** establish:
- universal superiority to SRS or Split15;
- statistically significant R5 edge-discovery superiority;
- optimality of three sentinels;
- distribution-free uncertainty validity under arbitrary shift;
- live weapon-system certification;
- a clean AMOVFLY failure-rate qualification result.

## 4. Recommendation

No new experiment is required for first submission to JQT.

Before upload, complete only:
- author/title-page metadata;
- anonymous reproducibility archive;
- literal ScholarOne formatting checks.

**Simulated recommendation: MINOR REVISION / SUITABLE FOR EXTERNAL PEER REVIEW.**
