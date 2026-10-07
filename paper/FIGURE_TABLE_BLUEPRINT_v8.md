# KTES v8 Submission Figure and Table Blueprint

**Status:** submission-presentation design freeze candidate  
**Scope:** presentation only; no method retuning, no new experiment, no endpoint redefinition  
**Evidence source:** frozen v8 manuscript and closed Phase 1.2R / Phase 2 evidence

## 1. Presentation objective

The submission should make one argument visually clear before a reviewer reads the full Methods:

> Under a severe live-test budget, c-pKTES-Hedge preserves a probability-sampling basis while actively enriching edge conditions; its controlled confirmation supports the inferential trade-off, while the external evidence shows that numerical performance, source admissibility, endpoint validity, and realized-design provenance must be judged separately.

The current v8 manuscript contains enough evidence, but the four in-text result tables distribute the story across too many numerical blocks. The submission version should use **four main figures and three main tables**, with detailed execution evidence moved to Supplementary Information.

## 2. Main figures

### Figure 1 — Method architecture: probability-preserving active test allocation

**Question answered:** What is c-pKTES-Hedge and why is it different from both simple probability sampling and a deterministic edge block?

**Visual structure:**
1. finite operational population with outcome-blind covariates;
2. three certainty sentinels selected without outcomes;
3. 37-unit positive-π probability remainder;
4. remainder score = 80% kernel novelty + 20% compound adverse-tail score;
5. Local Cube selection under the fixed stratum allocation;
6. Hájek model-assisted residual estimation and frozen UQ;
7. Accept / Reject / Inconclusive decision.

**Mandatory annotations:** `n=40`, `3 + 37`, `rho=0.20`, `lambda=3`, positive inclusion-probability floor, immutable realized design object.

**Do not show:** R1–R4 historical variants in the main figure. Their development path belongs in Supplementary Fig. S1.

### Figure 2 — R5 controlled confirmation: the discovery–inference trade-off

**Question answered:** Did the frozen method preserve difficult-condition discovery while improving inferential accuracy?

**Visual structure:**
- left block: edge hit and decision outcomes;
- right block: profile, failure, and critical-tail MAE;
- every row displays c-pKTES-Hedge and Split15 side by side plus the paired difference and 95% CI where available.

**Frozen numbers:**
- edge hit: 0.812 vs 0.779; paired +0.033, 95% CI [-0.0013, +0.0673];
- profile MAE: 0.006824 vs 0.008348; difference -0.001525, 95% CI [-0.002025, -0.001024];
- failure MAE: 0.051746 vs 0.060399; difference -0.008653, 95% CI [-0.012595, -0.004711];
- critical-tail MAE: 0.016811 vs 0.020958; difference -0.004147, 95% CI [-0.004798, -0.003497];
- definitive correct: 0.173 vs 0.089; difference +0.084, 95% CI [+0.0555, +0.1125];
- abstain: 0.826 vs 0.911; difference -0.085, 95% CI [-0.1135, -0.0565].

**Visual claim:** edge discovery is statistically compatible with Split15 at the reported precision, whereas the main inferential-error metrics improve. The figure must not visually imply significant edge-hit superiority.

### Figure 3 — Layered external validation: three datasets, three different conclusions

**Question answered:** What actually transported outside the controlled confirmation?

**Rows:** Anti-UAV410, IDF-DS, AMOVFLY.

**Columns / visual lanes:**
- source admissibility;
- frozen-design execution;
- numerical method comparison;
- endpoint / semantic validity;
- final evidence class.

**Required content:**
- Anti-UAV410: profile-error difference vs SRS +0.00404, 95% CI [0.00137, 0.00671], inside the +0.01 non-inferiority bound; lower critical-domain error; `PASS_WITH_EXECUTION_CLARIFICATION`.
- IDF-DS: no telemetry outcome opened; flight-level preoutcome design frame not recoverable; `BLOCKED_SOURCE_STRUCTURE`.
- AMOVFLY: KTES−SRS profile-error difference -0.0007586, 95% CI [-0.0011638, -0.0003534]; numerical gates pass; exact `(0,0)` waypoint placeholders contaminate the literal endpoint; `NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION`.

This is the figure that should carry the paper's external-validity message. It should not be replaced by three separate performance plots.

### Figure 4 — Evidence validity is a gated chain, not a single accuracy number

**Question answered:** Why can a numerical pass still fail to support an unrestricted engineering claim?

**Gates:**
1. admissible preoutcome source structure;
2. frozen design identity;
3. valid endpoint semantics;
4. immutable realized design provenance;
5. numerical performance and uncertainty;
6. claim classification.

**Case overlays:**
- IDF-DS stops at Gate 1;
- Anti-UAV410 passes the core frozen method gate but carries a comparator execution clarification;
- AMOVFLY passes the numerical gate but receives an endpoint-semantic limitation;
- the later hosted-runner reproduction attempt motivates Gate 4 because 254/257 inclusion probabilities drifted by >1e-12 despite matching high-level runtime metadata.

**Role in paper:** this is not decorative governance. It is the conceptual synthesis of the external evidence.

## 3. Main tables

### Table I — Frozen c-pKTES-Hedge contract

Keep one compact methods table in the main paper:

| Component | Frozen specification |
|---|---|
| Live-test budget | n=40 |
| Certainty sentinels | 3, outcome-blind |
| Probability remainder | 37 positive-π units |
| Remainder score | 80% kernel novelty + 20% compound adverse-tail |
| Tail parameters | rho=0.20, lambda=3 |
| Selection | Local Cube under fixed stratum allocation |
| Estimator | stratum-wise Hájek model-assisted residual correction |
| UQ | max(GS, PWR), frozen R3 calibration |
| Decision | Accept / Reject / Inconclusive |
| Reproducibility identity | source/runtime metadata + hashed realized design object |

This table replaces repeated prose scattered across Methods and Appendix.

### Table II — R5 independent confirmation

Retain the present R5 result table almost unchanged. It is the principal quantitative table and should remain in the main paper.

### Table III — External evidence classification

Merge the current Anti-UAV, IDF-DS, AMOVFLY and cross-evidence tables into one evidence-class table. Include only the metric needed to understand the gate result; move full comparator metrics to Supplementary Tables S4–S6.

Recommended columns: dataset; preoutcome source gate; primary numerical comparison; key validity boundary; final evidence class.

## 4. Material to move out of the main paper

Move the following from the main text to Supplementary Information while keeping concise summary sentences in Results:

- full Anti-UAV comparator table and all ESS quantiles;
- full AMOVFLY comparator table;
- the exact list of 257-flight placeholder audit counts beyond the two decisive facts (`257/257` affected; `378/378` >100 km episodes are exact-zero episodes);
- detailed design-object SHA and hosted-runner field-drift diagnostics;
- R1–R4 development chronology beyond one paragraph;
- individual CI run IDs, artifact IDs, and file hashes.

These are essential audit evidence but not main-story evidence.

## 5. Main-text figure order

1. Fig. 1 immediately after the method overview in Section IV.
2. Fig. 2 at the beginning of Section VI.A.
3. Fig. 3 after the three external-validation subsections.
4. Fig. 4 at the start of Discussion, replacing part of the current verbal synthesis.

The visual sequence becomes: **method → controlled evidence → external evidence → validity principle**.

## 6. Presentation freeze rule

No figure may use a post-outcome sensitivity as if it were confirmatory evidence. No graphical rescaling may hide the less favorable Anti-UAV profile-error result. No figure may label AMOVFLY as an unrestricted engineering validation pass. IDF-DS must appear as a source-structure stop, not as a missing or negative KTES result.
