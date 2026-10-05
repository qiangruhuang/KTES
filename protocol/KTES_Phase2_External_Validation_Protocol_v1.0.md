# KTES Phase 2 External Validation Protocol v1.0

**Status:** PRE-REGISTERED / FROZEN FOR EXECUTION  
**Date:** 2026-09-29  
**Method under validation:** c-pKTES-Hedge  
**Frozen contract SHA-256:** `8b038633b4238ff1e2411a452731033c097fdbff6632634bc6edc1ab5b09e5e9`

## 1. Purpose

Phase 1.2R is closed. Phase 2 evaluates transportability of the already frozen design. It does not reopen R1–R5 and does not develop a new sentinel mechanism.

The external-validation sequence is fixed:

1. **Phase 2A — Anti-UAV410 task-effectiveness pilot**: structural validation of the inference–tail–difficult-case trade-off on an independent real-world tracking benchmark.
2. **Phase 2B — IDF-DS performance-floor / mission-profile validation**: engineering validation on real fixed-wing autonomous-flight telemetry.

A negative result is an external-validity boundary. The same external outcomes cannot be used to retune the method and then be reused as confirmation.

## 2. Immutable method contract

The following values are unchanged from R5/R3:

- live-test budget: **n = 40**;
- certainty units: **3**, all outcome-blind and with \(\pi=1\);
- frozen certainty portfolio: **NRR = 1 pure-novelty + 2 risk-aware sentinels**; each risk-aware sentinel uses 50% ranked novelty + 50% ranked auxiliary predicted failure;
- probability remainder: **37 units**, all with known positive inclusion probability;
- probability score: **80% kernel novelty + 20% compound adverse-tail score**;
- \(\rho=0.20\), \(\lambda=3\), existing minimum-probability floor retained;
- spreading/balance: **Local Cube**;
- compound-tail score: product of the three largest operational-profile marginal adverse quantiles;
- estimator: **stratum-wise Hájek model-assisted residual correction**;
- design UQ: **max(GS, PWR)**;
- R3 frozen calibration: failure abs95 = **0.137719714266479**; safety upper = **0.19767009190382911**;
- decision architecture: **Accept / Reject / Inconclusive**.

No quantity in this list may be selected again using Anti-UAV410 or IDF-DS outcomes.

## 3. Phase 2A — Anti-UAV410 task-effectiveness pilot

### 3.1 External-validation role

Anti-UAV410 is used as a **task-effectiveness structural validation**, not as a claim that a tracking benchmark is equivalent to live OT&E. The dataset contains 410 thermal-infrared sequences and more than 438,000 annotated bounding boxes, with official train/validation/test partitions of 200/90/120 sequences. The official benchmark exposes six challenge attributes—Thermal Crossover, Out-of-View, Scale Variation, Fast Motion, Occlusion, Dynamic Background Clutter—and four target-size attributes—Tiny, Small, Medium, Normal.

The pilot asks one question:

> With the Phase 1.2R design frozen, can 40 selected test conditions preserve population-level task-effectiveness inference while enriching genuinely difficult sequences without unstable inclusion weights?

### 3.2 Finite population and unit of analysis

Primary finite population: **the official Anti-UAV410 test split (N=120 sequences)**.

- unit \(i\): one video sequence;
- primary benchmark-profile weight: \(p_i=1/120\);
- terminology: this is **benchmark-profile inference**, not empirical operational-frequency inference, because Anti-UAV410 does not supply deployment-frequency weights.

Using the official test split preserves a clear external holdout. Train/validation data may be used only for non-target auxiliary model development if that recipe is fixed before test outcomes are opened; the c-pKTES parameters remain unchanged.

### 3.3 System outcome

The default pilot system under test is the official repository's **SiamFC default tracker**, because the benchmark provides a direct reproducible execution path for it and it is not introduced as an Anti-UAV410-specific retrained method.

Primary per-sequence outcome:

\[
Y_i = SA_i,
\]

where \(SA\) is the Anti-UAV state-accuracy metric that combines localization overlap and target presence/absence handling.

Secondary descriptive outputs: Success AUC and 20-pixel precision when available from the same frozen tracker run. They do not alter sampling or the primary gate.

### 3.4 Outcome-blind design covariates

Only information available before opening SiamFC task-effectiveness outcomes may enter selection.

Primary covariate source: sequence-level official attribute annotations. The frame-level `IR_label.json` annotations are not required for the primary design because the official repository notes that they are incomplete.

Kernel/spreading feature vector uses:

- six challenge indicators: TC, OV, SV, FM, OC, DBC;
- four size indicators: Tiny, Small, Medium, Normal;
- log sequence length if available before outcome scoring.

Adverse orientation for the compound-tail score uses only variables for which “higher = more adverse” is unambiguous:

- TC, OV, SV, FM, OC, DBC;
- Tiny and Small target indicators.

`Medium` and `Normal` remain kernel geometry features but are not treated as adverse-tail coordinates.

### 3.5 Frozen auxiliary risk map

For Phase 2A, the auxiliary predicted-failure input is deliberately simple and outcome-blind:

\[
\widehat r_i = \tfrac12\,\overline A_i + \tfrac12\,S_i,
\]

where \(\overline A_i\) is the mean of the six challenge indicators and \(S_i\) is a fixed size-severity score (Tiny=1, Small=2/3, Medium=1/3, Normal=0; use the most adverse active size category).

This is a structural analogue of wall-to-wall auxiliary risk, not a claim that it is a calibrated M&S model. It is used because it can be computed without tracker outcome leakage. The risk map is not tuned on the test outcomes.

For model-assisted estimation of continuous \(SA\), the primary Phase 2A pilot uses a constant auxiliary mean within each sampling stratum. This intentionally conservative choice prevents test-outcome leakage. IDF-DS is reserved for the stronger telemetry/surrogate model-assisted validation.

### 3.6 Strata and allocation

Strata are defined by the most adverse official target-size class active for the sequence: Tiny > Small > Medium > Normal. This yields mutually exclusive, outcome-blind strata.

The n=40 allocation is determined **before outcomes** by largest-remainder proportional allocation to stratum population size, with a minimum of 2 per non-empty stratum when feasible. This allocation rule is fixed; no outcome-based reallocation is permitted.

### 3.7 Frozen c-pKTES-Hedge selection

Within the above finite population:

1. compute kernel novelty from the outcome-blind feature matrix;
2. select 3 certainty sentinels with the frozen NRR portfolio;
3. compute the compound adverse-tail score using the frozen top-3 marginal-quantile product;
4. for each non-certainty unit set
   \[
   z_i=0.80N_i+0.20C_i;
   \]
5. use \(\lambda=3\) and the existing inclusion-probability floor to obtain positive \(\pi_i\);
6. use Local Cube for spreading/balance while preserving prescribed inclusion probabilities;
7. evaluate the frozen stratum-wise Hájek residual correction and max(GS,PWR) UQ.

### 3.8 Comparators

Only two comparators are retained:

- **Stratified probability sampling**, n=40, with the same outcome-blind strata and allocation rule.
- **Split-style baseline**, 15 deterministic geometry/difficulty points + 25 probability-audit points. The deterministic component is fixed from pre-test covariates only; the audit component uses the same strata. The split-style result is interpreted as a baseline family comparison, not as a re-development target.

No additional adaptive or learned sampler is introduced in Phase 2A.

### 3.9 External outcomes used only after design freeze

After the design object (features, strata, allocation, \(\pi_i\), sentinel indices, random seeds) is written to disk and hashed, tracker outcomes may be opened for evaluation.

The difficult-case evaluation set is defined as the **bottom 10% of full-population sequence SA**. It is an evaluation label only and is never used by the sampler.

### 3.10 Primary evaluation metrics

For each design replay:

1. **Profile error:** \(|\widehat\mu_{SA}-\mu_{SA}|\).
2. **Critical-domain error:** mean absolute error of SA over the six challenge domains TC/OV/SV/FM/OC/DBC.
3. **Difficult-case hit:** at least one selected sequence belongs to the bottom-10% SA set.
4. **Weight stability:** Hájek weight ESS, minimum selected \(\pi\), maximum normalized weight.
5. **Design-UQ coverage:** whether the nominal interval covers the known finite-population mean SA and the six domain means.

The Phase 2A primary result is the **paired distribution of these metrics under a fixed finite population and pre-registered design randomization**. It does not claim independent operational campaigns.

### 3.11 Replay plan

Use **500 paired design replays** with a fixed seed block `20261001 ... 20261500`. Every replay uses the same frozen feature engineering and method constants; only sampling randomness changes.

Report paired mean differences and 95% CIs for profile error, critical-domain error, difficult-case hit and ESS. Do not select the method based on p-values.

### 3.12 Phase 2A success / stop rules

Phase 2A is considered structurally supportive when all of the following hold:

- no inclusion-probability failure and no non-certainty unit with \(\pi_i\le0\);
- median weight ESS is not lower than **50% of the 37-unit probability remainder** (ESS ≥18.5) and the 5th percentile is ≥12;
- profile error is not materially worse than stratified probability sampling (paired mean difference ≤0.01 SA units);
- critical-domain error is not materially worse than the better of the two baselines by >0.02 SA units;
- difficult-case hit is not lower than the split-style baseline by more than **10 percentage points**.

These are **external-validation guardrails**, not new tuning targets. If any gate fails, record the failure and its mechanism. Do not retune \(\rho\), \(\lambda\), sentinel count, estimator or UQ constants on Anti-UAV410.

### 3.13 Interpretation boundary

A pass supports transportability of the probability-preserving sampling logic to a real task-effectiveness benchmark. It does not establish live-weapon-system validity, mission-level safety certification or empirical deployment-frequency representativeness.

## 4. Phase 2B — IDF-DS engineering validation (queued, not yet executed)

IDF-DS contains 240 real autonomous fixed-wing flights, 120 with SpeedyBee F405/INAV and 120 with Holybro Pixhawk 6X + Jetson Orin NX/PX4, totalling more than 32 hours. Logs include IMU, GNSS, airspeed, barometric altitude, actuators, flight modes, battery/power data and mission files.

Phase 2B will start only after the Phase 2A result is locked. Its role is more directly engineering-facing:

- finite-population unit: one autonomous flight;
- primary strata: the two avionics architectures (20/20 n=40 allocation unless an outcome-blind mission-file eligibility rule requires exclusion before sampling);
- operational covariates: mission geometry, requested speed/altitude, wind estimates, route complexity, platform configuration and pre-outcome telemetry metadata;
- performance-floor candidates: trajectory tracking, airspeed margin and energy/mission completion metrics;
- the published Ranger 2400 stall-speed value (~9 m/s) may provide an externally specified airspeed floor, but the exact Phase 2B failure rule must be frozen from engineering semantics before opening flight outcomes;
- the R5 sampling constants and R3 UQ constants remain unchanged.

No Phase 2B threshold will be selected using observed failure rates.

## 5. Reporting rule

Phase 2 reporting separates three evidence levels:

- **confirmed Phase 1.2R simulation evidence**;
- **Phase 2A structural external-validation evidence**;
- **Phase 2B engineering external-validation evidence**.

Results must be reported even if they are negative. A failed gate narrows the method's applicability; it does not authorize reusing the same external dataset as a development set while retaining an “external validation” claim.

## 6. Source anchors

- Huang B, Li J, Chen J, et al. *Anti-UAV410: A Thermal Infrared Benchmark and Customized Scheme for Tracking Drones in the Wild*. IEEE TPAMI. DOI: 10.1109/TPAMI.2023.3335338.
- Official Anti-UAV410 benchmark repository: `HwangBo94/Anti-UAV410`.
- García-Gascón C, Bas-Bolufer J, Castelló-Pedrero P, García-Manrique JA. *An open benchmark dataset for machine learning and intelligent trajectory optimization in fixed-wing unmanned aerial systems*. Scientific Data. 2026;13:364. DOI: 10.1038/s41597-026-06716-3.
- IDF-DS data record: Zenodo DOI 10.5281/zenodo.16992975.
