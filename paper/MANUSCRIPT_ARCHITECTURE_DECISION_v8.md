# KTES v8 Manuscript Architecture Decision

**Date:** 2026-10-07  
**Status:** research architecture frozen for v8 drafting  
**Parent evidence:** v7 controlled-estimation manuscript + Phase 1.2R R1–R5 + Phase 2 external-validation evidence

## 1. Decision

The v8 manuscript must **not** be produced by appending the Phase 2 external-validation tables to the frozen v7 manuscript.

The reason is method identity. The v7 manuscript studies a target-alignment KTES workflow under a frozen `M=50, n=10, eta=0.6` protocol with random within-stratum selection and target-reference alignment weights. The Phase 2 external-validation program instead validates the later **c-pKTES-Hedge** design frozen after Phase 1.2R:

- live-test budget `n=40`;
- 3 outcome-blind certainty sentinels (`pi=1`);
- 37 positive-inclusion-probability probability tests;
- 80% kernel novelty + 20% compound adverse-tail score;
- `rho=0.20`, `lambda=3`;
- Local Cube spreading/balance;
- stratum-wise Hajek model-assisted residual correction;
- `max(GS,PWR)` design UQ;
- R3-frozen safety-facing calibration;
- Accept / Reject / Inconclusive decisions.

Treating those two algorithms as one method would create a method-evidence mismatch. The scientifically defensible path is therefore to preserve v7 as a predecessor evidence freeze and create a new v8 manuscript whose primary method is c-pKTES-Hedge.

## 2. New primary research question

The v8 paper should answer:

> Under a hard 30–50 live-test budget, can a probability-preserving active test design enrich difficult and emergent conditions while retaining stable finite-population inference, and does that trade-off transport to independent real-data settings without outcome-driven retuning?

This question is materially different from the v7 weighted-mean alignment question and is the correct target for the R5 and Phase 2 evidence.

## 3. Core storyline

The paper should tell one sequence rather than several parallel algorithm stories.

### 3.1 Problem

Pure probability sampling protects population inference but can miss rare, compound, or previously unenumerated difficult conditions at n around 40. Deterministic edge-focused sampling improves difficult-case discovery but weakens the probability-sampling basis needed for population-level qualification.

### 3.2 Design principle

The proposed solution is not to choose one side of that trade-off. c-pKTES-Hedge embeds a small deterministic-inclusion component **inside** a probability design:

- certainty units have legitimate first-order inclusion probability `pi=1`;
- all remaining inferential units retain known positive `pi_i`;
- active enrichment changes first-order probabilities but does not turn the remainder into convenience sampling;
- Local Cube adds spreading/balance while preserving the prescribed inclusion probabilities.

This gives the paper its conceptual contribution: **active difficult-condition enrichment need not automatically destroy design-based population inference if the enrichment is expressed through a valid inclusion-probability design.**

### 3.3 Controlled evidence

The independent R5 confirmation is the primary method evidence, not the old v7 MARE table.

Across 1000 independent finite populations and five simulator-discrepancy scenarios at n=40:

- edge hit: 81.2% for c-pKTES-Hedge vs 77.9% for Split15;
- paired edge-hit difference: +3.3 percentage points, 95% CI crossing zero, so no claim of significant superiority;
- profile MAE: 0.006824 vs 0.008348;
- failure MAE: 0.051746 vs 0.060399;
- critical-tail MAE: 0.016811 vs 0.020958;
- definitive-correct: 17.3% vs 8.9%;
- false acceptance: 0 observed among 945 true-Reject populations, which is not interpreted as a zero true rate.

The correct controlled-data claim is therefore that R5 preserves edge discovery comparable to Split15 while improving population/failure/tail inference and definitive-correct decisions in the frozen confirmation.

### 3.4 External evidence chain

The external evidence should be presented as **layered validation**, not a single binary success label.

#### Anti-UAV410

- independent task-effectiveness benchmark;
- all numerical guardrails pass;
- KTES profile error is 0.03007 vs 0.02603 for stratified SRS;
- paired KTES-SRS profile-error difference is +0.00404, 95% CI [0.00137, 0.00671], still within the frozen +0.01 non-inferiority bound;
- critical-domain error is lower for KTES: 0.04893 vs 0.05911 SRS and 0.06109 Split15;
- difficult-case hit is 1.000;
- probability-remainder ESS median is 33.12.

Classification must remain **PASS_WITH_EXECUTION_CLARIFICATION**, because the exact Split15 15+25 adapter and finite-domain estimator were numerically instantiated after `SA_i` recovery. This is not a pristine preregistered pass.

#### IDF-DS

IDF-DS is not a failed KTES experiment. The source gate closed before telemetry-outcome opening because the public archives did not provide the preregistered flight-linked preoutcome mission/configuration structure. Using realized trajectories or telemetry to rescue the sampling frame would create outcome leakage.

Classification: **BLOCKED_SOURCE_STRUCTURE**.

This is scientifically valuable negative evidence because it demonstrates that an external-validation protocol can fail before performance analysis when the source cannot support an outcome-blind design frame.

#### AMOVFLY

AMOVFLY provides the strongest engineering-facing external test but also the strongest warning about endpoint semantics.

Frozen confirmatory numerical result:

- KTES profile error Y10: 0.003784;
- SRS: 0.004543;
- Split15: 0.003637;
- KTES-SRS paired difference: -0.0007586, 95% CI [-0.0011638, -0.0003534];
- KTES critical-domain error: 0.033764 vs 0.066201 SRS and 0.080011 Split15;
- difficult-case hit: 1.000;
- all five numerical gates pass.

However, the post-outcome semantic audit found exact `(0,0)` aim-waypoint placeholders in all 257 flights. All 378 >100 km target-distance episodes are exactly those placeholders, making the literal failure endpoint `F10` degenerate at 1.0 and materially shifting the bounded `Y10` endpoint.

The final classification must therefore be:

**NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION.**

A post-outcome exact-zero exclusion sensitivity may be reported only as robustness of the method-comparison conclusion, not as a repaired confirmatory endpoint.

## 4. New contribution structure

The Introduction should state four contributions.

**C1 — Probability-preserving active enrichment.** A small certainty component is combined with a positive-pi probability remainder so that difficult-condition targeting and population inference remain in one design rather than separate deterministic and audit samples.

**C2 — Small-N inference architecture.** The design couples novelty/compound-tail inclusion probabilities, Local Cube spreading, Hajek model-assisted correction, conservative GS/PWR variance diagnostics, and three-state decisions.

**C3 — Development/confirmation separation.** R1–R5 development decisions are separated from a 1000-population independent confirmation and from external datasets on which rho, lambda, sentinel count, estimator and UQ constants are not retuned.

**C4 — Layered external-validity governance.** Anti-UAV410, IDF-DS and AMOVFLY show three distinct external-validation outcomes: numerical pass with execution clarification, preoutcome source-structure block, and numerical pass with endpoint-semantic limitation. The paper therefore contributes a validation discipline as well as a sampling method.

## 5. Claims that v8 may make

1. At n=40 in the independent R5 confirmation, c-pKTES-Hedge matched the edge-discovery performance of Split15 at the level supported by the paired CI while improving profile, failure and critical-tail inference.
2. A small number of certainty units can coexist with a positive-inclusion-probability remainder without invalidating the probability-design identity of the remainder.
3. The frozen method transferred to Anti-UAV410 without weight collapse and passed all prespecified numerical guardrails, although profile error was modestly worse than SRS and the comparator adapter required execution clarification.
4. The same frozen sampling logic retained favorable numerical comparisons on AMOVFLY, but the primary engineering interpretation was weakened by a post-outcome endpoint-semantic defect.
5. External validity is not a scalar property of an algorithm; it depends jointly on source structure, preoutcome covariate availability, endpoint semantics and execution provenance.
6. A hashed realized design object is part of the research object for unequal-probability designs whose floating-point realization cannot be reproduced byte-for-byte from source, versions and seeds alone.

## 6. Claims that v8 must not make

1. “40 tests replace 720 tests.”
2. “R5 significantly improves edge discovery over Split15.”
3. “KTES discovers arbitrary unknown failures.”
4. “0 observed false accepts proves zero false-accept probability.”
5. “Anti-UAV410 proves operational weapon-system validity.”
6. “AMOVFLY proves a valid flight-failure rate under the literal F10 endpoint.”
7. “The post-outcome exact-zero sensitivity repairs or replaces the AMOVFLY confirmation.”
8. “IDF-DS failed KTES.”
9. “Seeds and package versions alone reproduce the realized unequal-probability design.”
10. “The v7 M=50, n=10, eta=0.6 algorithm is the same algorithm externally validated in Phase 2.”

## 7. Proposed v8 paper structure

1. Introduction
2. Related Work
   - small-budget test allocation and scenario validation
   - balanced / unequal-probability / spatial sampling
   - model-assisted survey inference and small-N decisions
   - external-validation governance
3. Problem Formulation
4. c-pKTES-Hedge
   - operational frame and strata
   - certainty sentinels
   - probability remainder and compound-tail hedge
   - Local Cube
   - Hajek model-assisted estimator
   - UQ and three-state decision
5. Evidence Protocol
   - R1–R5 development separation
   - independent R5 confirmation
   - external-validation contract
6. Results
   - R5 confirmation
   - safety-UQ audit
   - Anti-UAV410
   - IDF-DS source gate
   - AMOVFLY confirmation and semantic audit
   - numerical reproducibility audit
7. Discussion
   - inference-edge trade-off
   - what transported and what did not
   - endpoint/source/provenance lessons
   - limitations and next independent confirmation
8. Conclusion
9. Reproducibility Appendix

## 8. Treatment of the v7 manuscript

The v7 manuscript remains an immutable predecessor and should not be overwritten. Its target-alignment experiments can be cited as development context or used in a separate methodological history/supplement, but the v8 main claims should be supported by the R5 and Phase 2 evidence chain.

If journal length is restrictive, the detailed v7 weighted-alignment experiments should stay outside the v8 main paper rather than forcing two different KTES algorithms into one Methods section.

## 9. Review gate before DOCX/PDF

The next artifact is a Markdown v8 manuscript plus a Claim–Evidence audit. DOCX/PDF generation should remain blocked until:

- the v8 method identity is internally consistent;
- every Abstract/Introduction claim maps to R5 or Phase 2 evidence;
- the three external-validation classifications are preserved exactly;
- post-outcome analyses are labelled as such;
- references for Anti-UAV410, IDF-DS, Cube sampling and spatially balanced sampling are verified;
- an adversarial review finds no method-evidence conflation.
