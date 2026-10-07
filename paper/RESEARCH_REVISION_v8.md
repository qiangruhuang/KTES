# KTES Research Revision v8

**Date:** 2026-10-07  
**Status:** EXTERNAL-VALIDATION EVIDENCE CLOSED FOR MANUSCRIPT REVIEW  
**Canonical method:** c-pKTES-Hedge

## 1. Why v8 is a new manuscript architecture

The frozen v7 paper studied a predecessor target-alignment KTES design (`M=50`, `n=10`, `eta=0.6`). Phase 1.2R subsequently converged to a materially different small-budget design, c-pKTES-Hedge. Because Phase 2 validates c-pKTES-Hedge rather than the v7 algorithm, v8 is not an append-only update to v7. The v7 manuscript remains immutable predecessor evidence; v8 is organized around the Phase 1.2R method and its controlled-to-external evidence chain.

## 2. Frozen final method

At the primary live-test budget `n=40`:

- 3 outcome-blind certainty sentinels have `pi=1`;
- 37 units form the positive-inclusion-probability remainder;
- sentinel portfolio: 1 pure-novelty + 2 risk-aware;
- remainder score: 80% kernel novelty + 20% compound adverse-tail score;
- `rho=0.20`, `lambda=3`, frozen probability-floor implementation;
- Local Cube spreading/balance;
- stratum-wise Hajek model-assisted residual correction;
- UQ: `max(GS,PWR)`;
- R3 frozen absolute failure calibration `0.137719714266479`;
- R3 frozen safety-upper calibration `0.19767009190382911`;
- decision: Accept / Reject / Inconclusive.

No Phase 2 outcome was used to retune these constants.

## 3. Controlled confirmation

R5 confirmation used 1000 independent finite populations, 200 in each of five discrepancy regimes. c-pKTES-Hedge versus Split15 achieved:

- edge hit 81.2% vs 77.9%; paired +3.3 percentage points, 95% CI crossing zero;
- profile MAE 0.006824 vs 0.008348;
- failure MAE 0.051746 vs 0.060399;
- critical-tail MAE 0.016811 vs 0.020958;
- definitive-correct 17.3% vs 8.9%.

The edge result supports comparability, not statistically established superiority. Hidden-bias edge discovery remains a visible boundary. Zero observed false accepts among 945 true-Reject populations is not interpreted as zero true false-accept probability.

## 4. Phase 2A Anti-UAV410

The primary finite population is the official 120-sequence test split; the primary outcome is per-sequence SiamFC State Accuracy. The frozen design uses size strata Tiny/Small/Medium/Normal = 33/54/29/4 and n=40 allocation 11/17/10/2.

Across 500 paired replays:

- c-pKTES profile error 0.03007 vs SRS 0.02603;
- KTES-SRS profile difference +0.00404, 95% CI [0.00137, 0.00671], inside the frozen +0.01 noninferiority bound;
- c-pKTES critical-domain error 0.04893 vs SRS 0.05911;
- difficult-case hit 1.000 vs SRS 0.996;
- probability-remainder ESS median 33.12, p05 32.60.

All numerical guardrails pass. Exact Split15 numerical adaptation and the finite-domain estimator required clarification after `SA_i` recovery. Final classification: **PASS_WITH_EXECUTION_CLARIFICATION**.

## 5. Phase 2B IDF-DS

The source gate was evaluated before telemetry-outcome access. The public archives did not instantiate the preregistered unit-linked per-flight mission/configuration structure required for the outcome-blind design frame. Realized telemetry was not used to rescue the design.

Final classification: **BLOCKED_SOURCE_STRUCTURE**, not performance PASS or FAIL.

## 6. Independent engineering-facing validation: AMOVFLY

The frozen finite population contains 257 ready-data flights in four scenario strata, with n=40 allocation 6/23/6/5. The literal confirmatory 10 m waypoint-attainment endpoint passed all five numerical method-comparison gates:

- KTES profile error 0.003784 vs SRS 0.004543;
- KTES-SRS paired difference -0.0007586, 95% CI [-0.0011638, -0.0003534];
- KTES critical-domain error 0.033764 vs SRS 0.066201;
- difficult-case hit 1.000.

A post-outcome semantic audit then found exact `(0,0)` aim-waypoint placeholders in all 257 flights. All 378 >100 km target-distance episodes were exact-zero episodes. Therefore the literal failure endpoint is degenerate and the bounded Y10 endpoint is materially affected.

Final classification: **NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION**.

The exact-zero exclusion sensitivity preserves the method-comparison ranking under the original immutable design object but remains post outcome and cannot replace the confirmatory endpoint.

## 7. Realized-design reproducibility rule

A later hosted-runner regeneration reproduced declared source/runtime metadata, standardization, bandwidth, seed lineage, and sentinels but changed 254/257 first-order inclusion probabilities; maximum absolute `pi_i` difference was 0.0108412. The low-level cause was not isolated.

No tolerance was relaxed. Downstream work must consume the exact hashed realized design object. For unequal-probability confirmatory designs, source code + package versions + seeds are not sufficient identity unless the regenerated design-object hash matches exactly.

## 8. Manuscript claim now supported

The supported story is:

> Under severe live-test budgets, a small certainty-sentinel portfolio can coexist with a positive-inclusion-probability remainder and preserve a usable population-inference basis while retaining active pressure toward difficult conditions. External validity, however, is jointly constrained by sampling design, preoutcome source structure, endpoint semantics, and realized execution provenance.

This does not support claims of live-weapon certification, deployment-frequency representativeness, distribution-free safety guarantees, or universal superiority to probability sampling.

## 9. Current manuscript state

`PAPER_IEEE_v8.md` has been re-architected around c-pKTES-Hedge. The following audits are complete:

- method/evidence architecture decision;
- Claim–Evidence audit;
- adversarial reviewer audit;
- citation identity and in-text closure audit;
- legacy-method/overclaim string scan.

No additional experiment is required for the present Markdown research gate. A future independent endpoint-clean engineering dataset would strengthen external confirmation but should be a new frozen study, not a repair of AMOVFLY.

## 10. Artifact gate

The research deliverable remains Markdown. DOCX/PDF generation remains closed until explicit user approval after review of the v8 Markdown manuscript.
