# Phase 2A design freeze v8

**Originally frozen:** 2026-10-05  
**Updated after provenance recovery:** 2026-10-06  
**Protocol:** KTES Phase 2 External Validation Protocol v1.0  
**Status:** **FRAME FROZEN; R5 DESIGN OBJECT INSTANTIATED FROM RECOVERED HISTORICAL SOURCE**

## Frozen finite-population frame

The Phase 2A finite population is the official Anti-UAV410 test split, N=120 sequences. The outcome-blind design frame was reconstructed only from the official repository pinned at commit `8a8eb04d976e9386b7c9c3ada5c85e5086013d52`. No SiamFC performance field or State Accuracy value enters the frame construction.

The feature schema follows the frozen protocol: TC, OV, SV, FM, OC, DBC, Tiny, Small, Medium, Normal, and log sequence length. The auxiliary risk score remains

\[
\widehat r_i=\tfrac12\overline A_i+\tfrac12 S_i,
\]

with Tiny=1, Small=2/3, Medium=1/3, Normal=0 and the most adverse active size class used for stratification.

Frozen stratum counts are Tiny 33, Small 54, Medium 29, Normal 4. The frozen n=40 largest-remainder/minimum-2 allocation is Tiny 11, Small 17, Medium 10, Normal 2. Frame SHA-256 is `c360494499e2cc9d09c62876bd3c45ab9f5be6982174b172224d12e62e6c9f69`.

## Immutable c-pKTES-Hedge contract

The Phase 1.2R-5 contract remains unchanged:

- three NRR certainty sentinels: one pure-novelty + two risk-aware;
- 37-unit probability remainder;
- 80% kernel novelty + 20% compound adverse-tail score;
- rho=.20, lambda=3.0, minimum-probability fraction=.35;
- Local Cube spreading/balance;
- stratum-wise Hájek model-assisted residual correction;
- max(GS,PWR) UQ with frozen R3 calibration constants.

The historical R5 runtime was subsequently recovered from the 2026-09-29 handoff and passed source-hash and historical behavior regression checks. No prose reconstruction is used for the KTES sampling engine.

## Instantiated design object

The hash-verified historical engine instantiates the following fixed outcome-blind design characteristics:

- design object SHA-256: `2a686908e42a1134578c07eecce9ca3be8336ff08c37c8d3622ff2a2855184dc`;
- historical base R5 seed: `20261115`;
- fixed RFF seed: `20261170`;
- novelty seed: `20261192`;
- replay randomization seeds: `20261001..20261500`;
- certainty sentinels:
  - `20190926_111509_1_9`;
  - `3700000000002_162623_1`;
  - `new6_train_newfix`.

The frozen inclusion-probability construction naturally caps one non-sentinel remainder unit, `20190925_124000_1_10`, at `pi=1`. It remains part of the probability-remainder design identity; it is not reclassified as a fourth manually chosen certainty sentinel.

## Split-style comparator execution clarification

The original Phase 2 protocol fixed the baseline family as 15 deterministic geometry/difficulty units plus 25 probability-audit units but did not uniquely specify its four-size-stratum numerical adapter. The executed outcome-blind adapter inherits the historical deterministic `3×4+3` geometry structure: 3 deterministic points in each Phase 2A size stratum plus 3 global points, followed by a disjoint 25-unit probability audit. The resulting audit allocation after deterministic removal is Tiny/Small/Medium/Normal `7/11/6/1`.

This exact numerical adapter was instantiated after `SA_i` had been recovered, although it never reads `SA_i`. It is therefore an execution clarification rather than a pristine preregistered component. Split-dependent claims retain that limitation.

## Outcome-access chronology

The Phase 2 protocol was frozen on 2026-09-29. The supplied `performance.json` was inspected later and exposed secondary sequence-level Success/Precision outputs but not the primary `SA_i`. The primary State Accuracy vector was subsequently recovered. The R5 source was recovered only after primary outcomes existed, so sentinel indices and inclusion probabilities were instantiated chronologically after outcome availability even though the sampling code and inputs are outcome-blind and historically frozen.

No Phase 2A outcome was used to alter c-pKTES rho, lambda, sentinel portfolio/count, inclusion-probability floor, feature frame, strata, allocation, seed block, primary endpoint or guardrail thresholds. This chronology is why the final Phase 2A result is reported as `PASS_WITH_EXECUTION_CLARIFICATION` rather than a pristine preregistered PASS.
