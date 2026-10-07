# KTES v8 Adversarial Review

**Date:** 2026-10-07  
**Target:** `PAPER_IEEE_v8.md` after first Claim–Evidence revision  
**Reviewer posture:** skeptical IEEE reviewer; priority is fatal logic, evidence leakage, method identity, and reproducibility rather than prose style.

## Recommendation

**Major revision, but the paper is now research-coherent.**

The manuscript has a credible central contribution and a stronger evidence architecture than the frozen v7 predecessor. The largest prior defect—treating the v7 target-alignment algorithm and the Phase2 c-pKTES-Hedge algorithm as if they were one method—has been removed. The remaining issues are mostly positioning, presentation hierarchy, and reproducibility disclosure rather than missing core experiments.

## 1. Strongest aspect

The strongest contribution is the explicit reconciliation of two small-budget T&E objectives:

- active difficult-condition enrichment;
- probability-preserving population inference.

The use of certainty units (`pi=1`) plus a positive-pi probability remainder is conceptually clean. The paper also benefits from reporting external-validation failures/limitations that many manuscripts would hide: Anti-UAV execution clarification, IDF-DS source ineligibility, AMOVFLY endpoint contamination, and realized-design numerical drift.

This evidence discipline is publishable if the paper avoids overselling the statistical novelty of the component algorithms.

## 2. Potential fatal objection: “This is a composition, not a new sampling theorem”

### Reviewer concern

Cube sampling, unequal first-order inclusion probabilities, certainty units, Hajek correction, model-assisted estimation, and spatially balanced sampling are established. A reviewer could reject the paper if it is framed as a new general sampling algorithm.

### Current manuscript status

The revised Methods now explicitly states that these components are established and that the contribution is their T&E-specific composition with an outcome-blind active score, certainty portfolio, frozen safety layer, and external-validation governance.

### Required response

Keep the title and Abstract focused on **test allocation** rather than “new sampling theory.” In the Introduction, retain the wording “small-N sampling-and-inference architecture” rather than “novel estimator.”

**Status: controlled.**

## 3. Potential fatal objection: R5 development leakage into confirmation

### Reviewer concern

R1–R5 contains multiple design iterations. The reviewer may ask whether the 1000-population confirmation reused development populations or tuned `rho`, `lambda`, sentinels, or UQ constants on the confirmation set.

### Evidence

The project handoff explicitly freezes:

- `rho=0.20`;
- `lambda=3`;
- 3 sentinels;
- 37 probability-remainder units;
- Hajek estimator;
- `max(GS,PWR)`;
- R3 calibration;
- confirmation seed 20261115.

R5 confirmation uses 1000 independent finite populations over five scenarios.

### Required manuscript reinforcement

Add one short sentence in Section V-B that the R5 confirmation population seeds were not used in R1–R5 development and that the R3 calibration was developed before R5 confirmation. Do not add new experiments.

**Status: minor textual reinforcement required.**

## 4. Anti-UAV410: pass label can be misunderstood

### Reviewer concern

SRS has better profile error, yet the study says PASS.

### Evidence

The frozen success rule is non-inferiority: KTES-SRS profile-error difference must be <= +0.01. Observed difference is +0.00404 with 95% CI [0.00137, 0.00671]. Critical-domain error is lower for KTES.

### Assessment

The manuscript now reports the unfavourable profile result prominently. This is good. The label `PASS_WITH_EXECUTION_CLARIFICATION` remains acceptable only if “PASS” is consistently tied to the preregistered gate rather than interpreted as superiority.

### Required wording rule

Whenever the label first appears, write “passes the frozen numerical guardrails” rather than “validates superiority.”

**Status: controlled.**

## 5. Anti-UAV execution clarification weakens two guardrails

### Reviewer concern

The exact Split15 15+25 adapter and finite-domain estimator were instantiated after `SA_i` recovery. This could be viewed as post-outcome protocol completion.

### Evidence

The c-pKTES constants, endpoint, frame, strata, allocation, seed block, and thresholds were not altered. The affected elements are comparator-sensitive components.

### Assessment

The manuscript correctly separates directly frozen c-pKTES/SRS/ESS results from comparator-sensitive guardrails. This should be mirrored in the supplement and figure/table captions.

### Recommendation

In the main paper, use Anti-UAV primarily as evidence for:

1. no weight collapse;
2. profile-error non-inferiority to SRS;
3. external-domain sampling feasibility.

Treat the Split15 difficult-hit result and exact critical-domain comparator ordering as secondary evidence with the disclosed clarification.

**Status: acceptable with explicit hierarchy.**

## 6. IDF-DS: useful governance evidence, but do not overspend main-text space

### Reviewer concern

A dataset with no method-performance result can look like failed scope expansion.

### Assessment

The source gate is useful because it demonstrates a fail-closed rule before outcome leakage. However, detailed ZIP member counts and archive forensic details belong in supplementary evidence, not the main narrative.

### Recommendation

Keep the main paper to one compact Results subsection and move structural inventory details to repository/supplement.

**Status: no new experiment needed.**

## 7. AMOVFLY: endpoint-semantic limitation is the central external-validity challenge

### Reviewer concern

If the primary engineering endpoint is contaminated, can AMOVFLY still be called confirmatory evidence?

### Assessment

The sampling comparison was confirmatory under a frozen literal endpoint, but the engineering interpretation was later invalidated/narrowed. The current classification—`NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION`—is defensible because it preserves both facts.

The strongest safe claim is:

> The frozen sampling design retained favorable numerical comparisons on an independent real-flight finite population, but the literal endpoint cannot support clean performance/failure qualification.

The paper must not call the post-outcome exact-zero exclusion a corrected confirmation.

**Status: controlled.**

## 8. AMOVFLY failure-rate result must be de-emphasized

### Reviewer concern

`F10=1` for every flight is degenerate because of placeholder episodes. Reporting failure-UQ metrics around this endpoint could distract or mislead.

### Recommendation

Do not headline any AMOVFLY failure-rate comparison in the main paper. Report the degeneracy and state that failure-rate qualification is unsupported. Keep detailed failure calculations in repository evidence only.

**Status: current manuscript follows this recommendation.**

## 9. Reproducibility drift is serious but manageable

### Reviewer concern

Same source, versions, inputs, and seeds produced materially different `pi_i` values. The reviewer may interpret this as non-reproducible software.

### Evidence

The later audit found 254/257 `pi_i` differences >1e-12, max absolute difference 0.0108412, while means/SDs, bandwidth, source hashes, seed lineage, and sentinels matched.

### Assessment

The fail-closed response is appropriate: downstream work uses the immutable confirmatory design object. However, the paper should not imply that the root numerical cause is understood.

### Required wording

State explicitly: “the low-level numerical backend responsible for the drift was not isolated.” The research contribution is the provenance response, not a solved numerical-analysis problem.

**Status: one sentence should be added to Discussion/Reproducibility.**

## 10. Safety calibration claim boundary

### Reviewer concern

R3 calibration may look like distribution-free certification.

### Evidence

The project handoff says calibration interpretation depends on exchangeability/accredited-domain assumptions and must not be claimed robust to arbitrary domain shift.

### Recommendation

Add one sentence in Methods or Limitations:

> “The frozen calibration is empirical within the development/confirmation architecture and is not asserted to be distribution-free under arbitrary simulator-to-reality shift.”

**Status: wording needed.**

## 11. Missing external confirmation after AMOVFLY limitation?

### Reviewer concern

A skeptical reviewer may demand another clean engineering dataset because AMOVFLY has endpoint contamination and IDF-DS is blocked.

### Assessment

A new external dataset would strengthen the paper, but it is not scientifically justified to keep adding datasets solely to obtain a clean positive result. The present paper can be publishable if framed as an evidence-bounded methods paper whose external program discovers both transport and validity boundaries.

The current Discussion correctly proposes a **future independent endpoint-clean confirmation** rather than repairing AMOVFLY.

**Status: no additional experiment required for the current research gate.**

## 12. Tables and figures needed for eventual submission

The Markdown paper is logically complete but not yet visually optimized. The eventual IEEE package should prioritize four main figures/tables:

1. **Figure 1:** design architecture—3 certainty sentinels + 37 positive-pi remainder + Local Cube + Hajek correction + three-state decision.
2. **Figure 2:** R1–R5 development-to-confirmation funnel, emphasizing the freeze boundary before R5 confirmation and Phase2.
3. **Figure 3:** external evidence map with three outcomes: Anti-UAV PASS_WITH_EXECUTION_CLARIFICATION; IDF-DS BLOCKED_SOURCE_STRUCTURE; AMOVFLY NUMERICAL PASS + ENDPOINT-SEMANTIC LIMITATION.
4. **Table 1:** one compact cross-evidence table showing R5, Anti-UAV, AMOVFLY profile/critical-domain/edge metrics and evidence class.

Do not add decorative plots that do not answer the main question.

## 13. Required edits before “submission-draft” label

1. State R5 confirmation seeds/populations were not part of development.
2. Add explicit non-distribution-free calibration limitation.
3. State that the low-level source of AMOVFLY numerical drift remains unidentified.
4. Keep Anti-UAV comparator-sensitive results hierarchically secondary.
5. Preserve all three external-validation classifications exactly.
6. Add a compact evidence-level table to the main paper before final typesetting.
7. Do one final citation audit for Anti-UAV410, IDF-DS, Cube, local pivotal, and AMOVFLY repository identity.

## 14. Final adversarial decision

**Novelty framing:** acceptable if treated as T&E systems/statistical composition.  
**Method identity:** pass.  
**Development/confirmation separation:** pass with one textual reinforcement.  
**External evidence:** strong for an evidence-bounded paper; not sufficient for broad field-certification claims.  
**Research integrity:** strong; negative/blocked/limited results are preserved.  
**Need for new experiments before next review:** no.  
**Ready for final Markdown revision:** yes.  
**Ready for DOCX/PDF:** no.
