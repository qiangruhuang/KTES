Phase 2 freezes:

- `n=40`;
- three certainty sentinels;
- 37 probability-remainder identities;
- 80/20 novelty/compound mixture;
- `rho=0.20`;
- `lambda=3`;
- probability floor implementation;
- Hajek model-assisted estimator;
- `max(GS,PWR)` variance diagnostic;
- R3 safety calibration;
- Accept/Reject/Inconclusive logic.

If an external source cannot instantiate the preoutcome frame, the study stops rather than substituting outcome-derived covariates. If an endpoint is found to have a post-outcome semantic defect, the original result is retained and the claim is narrowed; a sensitivity analysis cannot be promoted to a new confirmation.

### D. Anti-UAV410 task-effectiveness pilot

Anti-UAV410 is an infrared UAV-tracking benchmark with 410 videos [11]. Phase 2A uses the official 120-sequence test split as a finite population and the default SiamFC tracker as the frozen system under test. The primary outcome is per-sequence State Accuracy `SA_i`. The live-test analogue selects 40 sequences.

Outcome-blind covariates are six official challenge indicators, four target-size indicators, and log sequence length. The mutually exclusive size strata contain 33 Tiny, 54 Small, 29 Medium, and 4 Normal sequences, with frozen allocation 11/17/10/2.

The replay protocol uses 500 paired design replays with seed block 20261001–20261500. Prespecified guardrails cover positive inclusion probabilities, probability-remainder ESS, profile-error non-inferiority to stratified probability sampling, critical-domain error, and difficult-case discovery.

### E. IDF-DS source-structure gate

IDF-DS is a published dataset of 240 autonomous fixed-wing flights using two avionics architectures [12], [13]. The preregistered Phase 2B design required flight-linked preoutcome mission/configuration/environment information before opening telemetry outcomes.

The public archive was therefore audited structurally before telemetry values were opened. The audit found archive-level mission plans but did not recover the required per-flight `mission.txt` and `parameters.csv` structure from the released archives. The SpeedyBee processed release exposed 111 lap identifiers rather than 120 intended flight units. Realized trajectories, speeds, flight durations, and telemetry values were prohibited as rescue covariates.

### F. AMOVFLY replacement engineering validation

AMOVFLY provides real UAV flight process data with flight-scenario labels and preoutcome route/configuration context [14]. A new independent protocol was frozen before telemetry-outcome opening. The confirmatory finite population contains 257 unique autonomous ready-data flight blobs across four scenario strata: FAFS 33, FAVS 165, VAFS 32, and VAVS 27, with `n=40` allocation 6/23/6/5.

The frozen literal primary endpoint is the proportion of waypoint episodes attaining an external 10 m reference radius. The 10 m value is an external reference threshold and is not asserted to be the historical configured AMOVFLY acceptance radius.

The confirmatory design object was hashed before downstream replay. A later post-outcome semantic audit and a separately labelled sensitivity analysis were required because of exact `(0,0)` waypoint placeholders.

---

## VI. Results

### A. R5 independent controlled confirmation

Table I summarizes the primary R5 versus Split15 comparison over 1000 independent finite populations.

**TABLE I. R5 independent confirmation, n=40.**

| Metric | c-pKTES-Hedge | Split15 | Paired difference | 95% CI |
|---|---:|---:|---:|---:|
| Edge hit | **0.812** | 0.779 | +0.033 | -0.0013 to +0.0673 |
| Profile MAE | **0.006824** | 0.008348 | -0.001525 | -0.002025 to -0.001024 |
| Failure MAE | **0.051746** | 0.060399 | -0.008653 | -0.012595 to -0.004711 |
| Critical-tail MAE | **0.016811** | 0.020958 | -0.004147 | -0.004798 to -0.003497 |
| Definitive correct | **0.173** | 0.089 | +0.084 | +0.0555 to +0.1125 |
| Abstain | 0.826 | 0.911 | -0.085 | -0.1135 to -0.0565 |

The edge-hit point estimate is higher for c-pKTES-Hedge, but its paired confidence interval crosses zero. The evidence therefore supports **no detected edge-discovery disadvantage at the reported precision**, not statistically significant superiority.

The stronger result is inferential. Profile, failure, and critical-tail errors are all lower under c-pKTES-Hedge, and definitive-correct decisions increase while abstention falls. This is the trade-off that R5 was designed to achieve: recover much of the active edge pressure of Split15 while retaining probability-preserving population inference.

### B. Hidden-bias boundary and false acceptance

Under `hidden_bias`, edge hit is 0.770 for c-pKTES-Hedge and 0.795 for Split15. The paired difference is -2.5 percentage points with 95% CI -10.17 to +5.17 percentage points. This closes the earlier R3/R4 simulator-blind weakness without establishing dominance over the deterministic split design.

Across 945 true-Reject populations in the R5 confirmation, zero false accepts are observed. This is consistent with low observed false-accept risk under the frozen confirmation distribution but is not interpreted as proof that the true false-accept probability is zero or as a distribution-free operational guarantee.

### C. Frozen safety-UQ audit

The R3 calibration is applied to the same R5 campaigns without changing the point estimator. Failure marginal coverage rises from 94.9% to 99.0%, and safety upper-bound coverage from 97.1% to 99.9%. Definitive-correct and abstention rates are unchanged in this confirmation because other constraints already dominate final status for the campaigns whose failure bounds widen.

This result is evidence about the frozen confirmation set, not a theorem that wider failure bounds are cost-free in every domain.

### D. Anti-UAV410 external validation

Table II gives the 500 paired-replay Phase 2A result.

**TABLE II. Anti-UAV410 Phase 2A, 500 paired replays.**

| Method | Profile error mean | Critical-domain error mean | Difficult-case hit | Probability-component ESS median |
|---|---:|---:|---:|---:|
| c-pKTES-Hedge | 0.03007 | **0.04893** | 1.000 | 33.12 |
| Stratified-SRS | **0.02603** | 0.05911 | 0.996 | 39.71 |
| Split15+Audit25 | 0.03049 | 0.06109 | 1.000 | 24.27 |

c-pKTES-Hedge is **not uniformly better**. Its profile error is higher than stratified SRS by 0.00404, with paired 95% CI 0.00137 to 0.00671. The increase remains inside the frozen +0.01 non-inferiority guardrail. By contrast, critical-domain error is lower than both comparators; the c-pKTES-minus-SRS difference is -0.01018 with 95% CI -0.01230 to -0.00806.

All numerical guardrails pass under the disclosed execution adapter. The directly frozen c-pKTES/SRS components include positive-inclusion support, the probability-remainder ESS diagnostics, and the +0.01 profile-error non-inferiority gate. The critical-domain and Split15 difficult-case guardrails are comparator-sensitive because the exact 15+25 Split15 adapter and finite-domain estimator required execution clarification after `SA_i` recovery. The probability-remainder ESS median is 33.12 and its fifth percentile is 32.60, both well above the frozen thresholds of 18.5 and 12. No non-certainty inclusion-probability failure occurs.

The correct classification is nevertheless **PASS_WITH_EXECUTION_CLARIFICATION**. The exact numerical Split15 adapter and finite-domain critical-domain estimator were instantiated after `SA_i` recovery, although the c-pKTES constants, endpoint, covariates, strata, allocation, seed block, and gate thresholds were unchanged. The result is therefore stronger than an exploratory reanalysis but weaker than a pristine preregistered pass.

### E. IDF-DS stops at the source gate

IDF-DS does not produce a method-performance result. Before opening telemetry outcomes, the source audit finds that the public archives cannot instantiate the preregistered flight-level outcome-blind design frame. The only identified mission plan is an archive-level constant shared across the two architecture archives, and the released structure does not provide the expected flight-specific mission/configuration files at the required resolution.

Using realized GPS paths, speed, flight duration, wind histories, or other telemetry to manufacture a design frame after seeing the release would convert the external dataset into a development source. The study is therefore classified **BLOCKED_SOURCE_STRUCTURE — INSUFFICIENT PREOUTCOME COVARIATE RESOLUTION**.

This is not a KTES performance failure. It is evidence that external validation can legitimately terminate before outcome analysis when the source cannot support the promised sampling design.

### F. AMOVFLY confirmatory numerical result
