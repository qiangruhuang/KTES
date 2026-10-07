# KTES v8.2 Submission-Level Adversarial Review

**Review target:** `PAPER_IEEE_v8_2.md` + `SUPPLEMENTARY_INFORMATION_v8_2.md` + four frozen submission figures  
**Review stance:** skeptical methods reviewer evaluating statistical identity, external-validity claims, and presentation integrity  
**Recommendation:** **MINOR REVISION / FORMAT-READY AFTER NON-SCIENTIFIC CLEANUP**

## 1. Central story

The compressed manuscript now has one coherent story: under a 40-test budget, c-pKTES-Hedge embeds a small certainty-sentinel portfolio inside a probability design so that difficult-condition enrichment does not destroy the probability basis for population inference. The controlled R5 confirmation is the primary performance evidence; Anti-UAV410, IDF-DS, and AMOVFLY are external evidence gates with intentionally different conclusions.

This is substantially clearer than a manuscript organized around four separate result tables and long execution prose.

## 2. Major reviewer attacks and disposition

### Attack 1 — “The method is a bundle of known survey-sampling tools.”

**Disposition: addressed.** The manuscript no longer implies novelty for Local Cube or Hajek estimation. The contribution is framed as the T&E-specific architecture: outcome-blind certainty sentinels + positive-π active remainder + finite-population correction + fail-closed evidence governance under severe budget.

### Attack 2 — “The edge-discovery result is being oversold.”

**Disposition: addressed.** Fig. 2, Table II, Abstract, Results, Discussion, and Conclusion all preserve that the paired edge-hit interval crosses zero. The claim is compatibility/no detected disadvantage at the reported precision, not superiority.

### Attack 3 — “External validation is cherry-picked because Anti-UAV is partly worse.”

**Disposition: addressed.** The main paper explicitly retains Anti-UAV's +0.00404 profile-error disadvantage versus SRS and shows it in Fig. 3 and Table III. This strengthens rather than weakens the external-validity argument.

### Attack 4 — “IDF-DS contributes no method evidence and should be removed.”

**Disposition: reject the attack, but keep wording disciplined.** IDF-DS is not presented as performance validation. It is evidence for the preregistered source-eligibility gate: the study stops before telemetry opening because the required preoutcome design frame cannot be instantiated without contaminating independence.

### Attack 5 — “AMOVFLY is invalid; therefore the external claim collapses.”

**Disposition: addressed by claim restriction.** AMOVFLY remains a numerical comparison under the executed design but not a clean engineering-endpoint validation. The exact-zero sensitivity is in Supplement and is explicitly post outcome. Anti-UAV supplies an independent task-effectiveness transfer result, so AMOVFLY is not the sole external evidence.

### Attack 6 — “If the design cannot be regenerated exactly, reproducibility is inadequate.”

**Disposition: addressed by a stronger provenance rule.** The paper does not accept approximate regeneration as equivalent. The realized inclusion-probability vector and deterministic identities are frozen as an immutable design object. Fig. 4 makes this a methodological requirement rather than hiding it as an implementation anomaly.

## 3. Residual scientific risks

### R1. Controlled confirmation is still simulation-based

This remains the most important limitation. The manuscript states it directly and does not claim field certification.

### R2. Anti-UAV execution clarification weakens preregistration purity

The evidence class is correctly downgraded. The main paper should not replace the exact label with a generic “external PASS” during later journal editing.

### R3. AMOVFLY endpoint contamination limits engineering interpretation

The Supplement contains enough detail to prevent the post-outcome exact-zero exclusion from being mistaken for the primary analysis. Any later graphical abstract must preserve this distinction.

### R4. The frozen uncertainty calibration remains empirical

The manuscript correctly avoids a distribution-free claim. Do not shorten this caveat out of the journal-formatted Methods or Limitations.

## 4. Presentation risks

### P1. Fig. 3 class wording

**Fixed during this review.** The prior shortened AMOVFLY class omitted `CONFIRMATORY`; v8.2 restores the exact evidence class and adds the required 95% CIs.

### P2. Three tables are sufficient

The present allocation is appropriate: method contract, R5 confirmation, external evidence classification. Restoring separate Anti-UAV or AMOVFLY main tables would fragment the story again.

### P3. Supplement must remain audit-complete

The Supplement now carries comparator metrics, ESS thresholds, source-gate details, semantic-audit counts, post-outcome sensitivity, and realized-design drift. These items should not be dropped during typesetting merely because they are no longer in the main narrative.

## 5. Claim ceiling after v8.2

The strongest defensible manuscript-level claim is:

> c-pKTES-Hedge provides a probability-preserving way to actively enrich a 40-test campaign and improves the controlled inference–discovery trade-off relative to the frozen Split15 comparator; its external use is supported at the level of sampling/inference transport, but engineering-validity strength remains conditional on preoutcome source structure, endpoint semantics, and realized-design provenance.

Claims that remain unsupported include:

- universal superiority in difficult-condition discovery;
- replacement of large-scale qualification campaigns by 40 tests;
- distribution-free safety guarantees;
- operational weapon-system certification from Anti-UAV410;
- failure-rate qualification from AMOVFLY `F10`;
- a clean pristine-preregistered label for Anti-UAV Phase 2A.

## 6. Recommendation

**MINOR REVISION / FORMAT-READY AFTER NON-SCIENTIFIC CLEANUP.**

No new experiment is required by this review. Remaining work is limited to journal-specific formatting, figure typography/vector export checks, reference-style normalization, and any external reviewer-requested clarification. The frozen method and outcomes should remain closed.
