# KTES Project Handoff v8

**Date:** 2026-10-07  
**Canonical repository:** `qiangruhuang/KTES`  
**Research state:** v8 external-validation evidence closed for manuscript review

## Source of truth

The v8 source of truth is the new c-pKTES-Hedge manuscript and the frozen Phase 1.2R / Phase 2 evidence. The frozen v7 target-alignment manuscript is predecessor evidence and must not be merged into v8 as if it were the same algorithm.

Primary manuscript files:

- `paper/PAPER_IEEE_v8.md`
- `paper/MANUSCRIPT_ARCHITECTURE_DECISION_v8.md`
- `paper/CLAIM_EVIDENCE_AUDIT_v8.md`
- `paper/ADVERSARIAL_REVIEW_v8.md`
- `paper/CITATION_AUDIT_v8.md`
- `paper/RESEARCH_REVISION_v8.md`

## Frozen method

c-pKTES-Hedge at n=40 = 3 outcome-blind certainty sentinels + 37 positive-pi probability-remainder tests; 80% kernel novelty + 20% compound adverse-tail score; rho=.20; lambda=3; Local Cube; stratum-wise Hajek model-assisted residual correction; max(GS,PWR) UQ; frozen R3 calibration; Accept/Reject/Inconclusive.

Do not add new sentinels, retune constants, or use external outcomes to redesign the method.

## Evidence state

### R5 controlled confirmation

Closed. Main controlled result: edge discovery comparable to Split15 at supported precision, with lower profile/failure/tail error and higher definitive-correct rate. Hidden-bias boundary remains visible.

### Anti-UAV410

Closed: **PASS_WITH_EXECUTION_CLARIFICATION**. All numerical guardrails pass. KTES profile error is modestly worse than SRS but within the frozen +0.01 noninferiority bound; critical-domain error is lower. Split15/domain-estimator details required post-SA execution clarification.

### IDF-DS

Closed at source gate: **BLOCKED_SOURCE_STRUCTURE** before telemetry-outcome opening. Do not use realized telemetry to retrofit preoutcome covariates.

### AMOVFLY

Closed: **NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION**. Numerical comparison gates pass, but exact `(0,0)` waypoint placeholders contaminate the literal endpoint. Exact-zero exclusion is post-outcome sensitivity only.

### Reproducibility

Use the hashed realized unequal-probability design object as immutable input. Do not regenerate `pi_i` and silently accept numerical closeness if the design hash differs.

## Manuscript claim boundary

Allowed:

- probability-preserving active enrichment is viable under severe small-N T&E budgets;
- R5 improves inference metrics while retaining comparable edge discovery;
- design logic transported to two independent real-data settings at the sampling-comparison level;
- external validity depends on source structure, endpoint semantics, and provenance.

Prohibited:

- edge-discovery superiority from the R5 paired result;
- universal superiority to SRS;
- live-weapon or mission-level safety certification;
- clean failure-rate qualification from AMOVFLY F10;
- treating IDF-DS as a performance failure;
- promoting post-outcome AMOVFLY sensitivity to confirmation;
- treating v7 target-alignment KTES and c-pKTES-Hedge as one method.

## Next action

The current task is manuscript review/figure design, not new method development. If another external engineering validation is pursued, it must use a new independently frozen dataset and endpoint contract.

DOCX/PDF remains gated pending explicit user approval.
