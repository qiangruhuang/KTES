# Supplementary Information — c-pKTES-Hedge v8.3

**Relationship to main manuscript:** this supplement contains material compressed out of `PAPER_IEEE_v8_3.md`. It does not introduce a new method, rerun an endpoint, or change an evidence classification.

---

## S1. Method development and freeze history

The small-N design was developed through five explicit stages. **R1** compared an all-probability design with a split design containing 15 deterministic KTES points and a smaller probability audit; the all-probability design improved profile and critical-tail inference but had lower edge discovery. **R2** introduced novelty-driven unequal inclusion probabilities and local spreading; edge hit increased but remained below the deterministic split design in some regimes. **R3** introduced three risk-aware certainty sentinels; pooled edge discovery matched the split baseline, but simulator-blind hidden-bias conditions exposed a weakness because all sentinels inherited the auxiliary risk model. **R4** hedged the certainty portfolio with one pure-novelty guard and two risk-aware sentinels. **R5** moved the additional hedge into the probability remainder through a 20% compound adverse-tail component and froze `rho=0.20` before confirmation.

The final Phase 2 method is therefore the output of an explicit development sequence. No Phase 2 external dataset is used to continue the R1–R5 search.

---

## S2. Frozen estimator and uncertainty construction

The final design uses 3 certainty sentinels and 37 probability-remainder units at `n=40`. The certainty units satisfy `pi=1`. The frozen probability-remainder score is

\[
z_i=0.80N_i+0.20C_i,
\]

with within-stratum tilt

\[
\pi_i\propto \exp\{3(z_i-\bar z_g)\}.
\]

Local Cube sampling is applied under the fixed stratum allocation. The model-assisted residual correction within stratum `g` is

\[
\widehat R_{g,H}
=
\frac{\sum_{i\in s_g}(p_{i\mid g}/\pi_i)(Y_i-m_i)}
{\sum_{i\in s_g}p_{i\mid g}/\pi_i},
\]

with overall estimator

\[
\widehat\theta_Y
=
\sum_g P(G_g)
\left[
E_{p_g}\{m(X)\}+\widehat R_{g,H}
\right].
\]

The frozen uncertainty diagnostic is

\[
\widehat V=\max(\widehat V_{GS},\widehat V_{PWR}).
\]

R3-frozen calibration constants reused unchanged in R5 and Phase 2 are `0.137719714266479` for the two-sided failure diagnostic and `0.19767009190382911` for the safety-facing upper calibration. These are empirical calibration constants within the development/confirmation architecture and are not asserted to be distribution-free under arbitrary shift.

The legal decisions are Accept, Reject, and Inconclusive.

---

## S3. R5 independent confirmation detail

The frozen R5 design was confirmed on 1000 independent finite populations: 200 for each of `good`, `global_bias`, `tail_bias`, `hidden_bias`, and `mixed`. Every population was evaluated with paired c-pKTES-Hedge, reconstructed R4, and Split15 designs at `n=40`.

**TABLE S1.** Primary R5 comparison

| Metric | c-pKTES-Hedge | Split15 | Paired difference | 95% CI |
|---|---:|---:|---:|---:|
| Edge hit | 0.812 | 0.779 | +0.033 | -0.0013 to +0.0673 |
| Profile MAE | 0.006824 | 0.008348 | -0.001525 | -0.002025 to -0.001024 |
| Failure MAE | 0.051746 | 0.060399 | -0.008653 | -0.012595 to -0.004711 |
| Critical-tail MAE | 0.016811 | 0.020958 | -0.004147 | -0.004798 to -0.003497 |
| Definitive correct | 0.173 | 0.089 | +0.084 | +0.0555 to +0.1125 |
| Abstain | 0.826 | 0.911 | -0.085 | -0.1135 to -0.0565 |

Under `hidden_bias`, edge hit is 0.770 for c-pKTES-Hedge and 0.795 for Split15; the paired difference is -2.5 percentage points with 95% CI -10.17 to +5.17 percentage points. Across 945 true-Reject populations, zero false accepts are observed. This is a property of the frozen confirmation distribution, not proof of zero true false-accept probability.

The R3 calibration raises failure marginal coverage from 94.9% to 99.0% and safety upper-bound coverage from 97.1% to 99.9%. Definitive-correct and abstention rates are unchanged in this confirmation because other constraints dominate the campaigns whose failure bounds widen.

---

## S4. Anti-UAV410 Phase 2A

Phase 2A uses the official Anti-UAV410 120-sequence test split and frozen SiamFC system under test. The primary outcome is per-sequence State Accuracy `SA_i`. Outcome-blind covariates are six challenge indicators, four target-size indicators, and log sequence length. Size strata contain 33 Tiny, 54 Small, 29 Medium, and 4 Normal sequences, with frozen allocation 11/17/10/2. The replay protocol uses 500 paired replays with seed block 20261001–20261500.

**TABLE S2.** Anti-UAV410 comparator results

| Method | Profile error mean | Critical-domain error mean | Difficult-case hit | Probability-component ESS median |
|---|---:|---:|---:|---:|
| c-pKTES-Hedge | 0.03007 | 0.04893 | 1.000 | 33.12 |
| Stratified-SRS | 0.02603 | 0.05911 | 0.996 | 39.71 |
| Split15+Audit25 | 0.03049 | 0.06109 | 1.000 | 24.27 |

The c-pKTES-minus-SRS profile-error difference is `+0.00404` with 95% CI `0.00137` to `0.00671`, inside the frozen `+0.01` non-inferiority bound. The critical-domain-error difference versus SRS is `-0.01018` with 95% CI `-0.01230` to `-0.00806`. The probability-remainder ESS median is 33.12 and its fifth percentile 32.60, above frozen thresholds 18.5 and 12. No non-certainty inclusion-probability failure occurs.

The directly frozen c-pKTES/SRS components cover positive-inclusion support, probability-remainder ESS, and the +0.01 profile-error non-inferiority gate. The exact 15+25 Split15 adapter and finite-domain critical-domain estimator required execution clarification after `SA_i` recovery. Therefore the final evidence class is **PASS_WITH_EXECUTION_CLARIFICATION**, not a pristine preregistered pass.

Primary evidence files include `external_validation/PHASE2A_500_REPLAY_RESULT_v8.md`, `external_validation/PHASE2A_CI_EVIDENCE_v8.md`, `external_validation/PHASE2A_DESIGN_OBJECT_v8.json`, `data/anti_uav410_test_design_frame_v8.csv`, and `data/anti_uav410_siamfc_SA_i_v8.csv`.

---

## S5. IDF-DS source gate

The preregistered Phase 2B protocol required flight-linked preoutcome mission/configuration/environment information before telemetry outcomes were opened. Structural audit of the public release found archive-level mission plans but no per-flight `mission.txt` and `parameters.csv` structure at the required resolution. The SpeedyBee processed release exposes 111 lap identifiers rather than the intended 120 flight units.

The only identified mission plan is an archive-level constant shared across the two architecture archives. Realized GPS paths, speed, altitude, turn rate, wind histories, flight duration, flight modes, failsafe states, actuator, power, airspeed, sensor histories, and post-flight quality measures are prohibited as rescue covariates because they are realized telemetry rather than preoutcome design information.

The study therefore terminates as **BLOCKED_SOURCE_STRUCTURE — INSUFFICIENT PREOUTCOME COVARIATE RESOLUTION** before telemetry outcome opening. This is not a c-pKTES-Hedge performance failure.

Primary evidence files include `external_validation/PHASE2B_PREOUTCOME_FREEZE_v8.md` and `external_validation/PHASE2B_SOURCE_GATE_v8.md`.

---

## S6. AMOVFLY preoutcome design and confirmatory run

The confirmatory finite population contains 257 unique autonomous ready-data flight blobs across four scenario strata: FAFS 33, FAVS 165, VAFS 32, and VAVS 27. The frozen `n=40` allocation is 6/23/6/5. The literal primary endpoint is the proportion of waypoint episodes attaining an external 10 m reference radius. The 10 m value is an external reference threshold and is not asserted to be the historical configured AMOVFLY acceptance radius.

**TABLE S3.** AMOVFLY confirmatory numerical results

| Method | Profile error Y10 | Critical-domain error Y10 | Difficult-case hit | Probability ESS median |
|---|---:|---:|---:|---:|
| c-pKTES-Hedge | 0.003784 | 0.033764 | 1.000 | 35.224 |
| Stratified-SRS | 0.004543 | 0.066201 | 1.000 | 39.276 |
| Split15+Audit25 | 0.003637 | 0.080011 | 1.000 | 23.019 |

All five frozen numerical gates pass. The KTES-minus-SRS profile-error difference is `-0.0007586` with 95% CI `-0.0011638` to `-0.0003534`. Critical-domain error is also lower for KTES than either comparator.

The frozen realized design-object SHA-256 is `a5b241f9d17be696652f30968bb1b8a0d2138087674ac371866b606e8362696b`.

---

## S7. AMOVFLY endpoint-semantic audit

Under the frozen literal parser, the population mean is `Y10=0.946105` and the flight-level failure indicator `F10=I(any waypoint episode >10 m)` equals one for every flight.

A post-outcome read-only semantic audit finds:

- 257/257 flights contain at least one exact `(0,0)` `aim_lat/aim_long` episode;
- 378 exact-zero episodes occur in total;
- exactly 378 episodes have minimum actual-to-aim distance greater than 100 km;
- every >100 km episode is an exact-zero episode;
- no non-zero target produces a >100 km episode.

The literal `F10` endpoint is therefore degenerate and cannot support failure-rate qualification. The bounded `Y10` endpoint is materially influenced by the placeholder semantics. The confirmatory result is retained rather than silently repaired. The final classification is **NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION**.

---

## S8. Post-outcome diagnostic sensitivity

A separately labelled sensitivity excludes exact `(0,0)` episodes while loading the immutable confirmatory design object rather than regenerating inclusion probabilities.

After exclusion, population `Y10` is 0.982243 and `F10` is 0.459144. Under the unchanged frozen design and replay seeds, the KTES-minus-SRS profile-error difference is `-0.0004107` with 95% CI `-0.0006379` to `-0.0001834`. Critical-domain error is 0.03342 for KTES versus 0.06468 for SRS and 0.07928 for Split15. All five numerical comparison gates remain satisfied.

This sensitivity supports robustness of the **method-comparison conclusion** to the identified placeholder. Because the exclusion rule is post outcome, it does not replace the primary confirmatory endpoint and does not rescue the original failure-rate interpretation.

---

## S9. Realized-design reproducibility audit

A later hosted-runner attempt to regenerate the AMOVFLY design from the same source code, declared Python/NumPy/SciPy/Pandas versions, input frame, constants, and seeds fails the exact design-object hash check. Standardization statistics, kernel bandwidth, source hashes, seed lineage, and certainty sentinels match, but 254 of 257 first-order inclusion probabilities differ by more than `1e-12`. The maximum absolute difference is 0.0108412, and an example Local-Cube selected set changes.

No tolerance is relaxed. The low-level numerical backend responsible for the drift is not isolated. Downstream sensitivity analysis therefore consumes the immutable realized design object from the successful confirmatory run.

The reproducibility rule is: for floating-point unequal-probability designs, the realized vector of first-order inclusion probabilities and deterministic design identities is part of the research object; source code, package versions, and random seeds alone are not accepted as equivalent identity unless the design-object hash matches exactly.

---

## S10. Evidence manifest and reproducibility checklist

For every major result, the repository should retain, where applicable:

- source identity and source commit/hash;
- preoutcome frame identity;
- realized design-object hash;
- source-code hash;
- replay seed block;
- result-table hash;
- CI run/artifact identity;
- evidence class and claim boundary.

The key evidence classes remain:

**TABLE S4. Evidence-class manifest.**

| Evidence set | Final evidence class |
|---|---|
| R5 controlled confirmation | Confirmatory controlled evidence |
| Anti-UAV410 | `PASS_WITH_EXECUTION_CLARIFICATION` |
| IDF-DS | `BLOCKED_SOURCE_STRUCTURE` |
| AMOVFLY | `NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION` |

Primary AMOVFLY evidence files include `external_validation/AMOVFLY_DESIGN_FREEZE_v8.md`, `external_validation/AMOVFLY_ENDPOINT_PERFORMANCE_FLOOR_FREEZE_v8.md`, `external_validation/AMOVFLY_EXTERNAL_VALIDATION_RESULT_v8.md`, `external_validation/AMOVFLY_WAYPOINT_SEMANTIC_AUDIT_v8.md`, `external_validation/AMOVFLY_ZERO_PLACEHOLDER_SENSITIVITY_v8.md`, and `external_validation/AMOVFLY_NUMERICAL_REPRODUCIBILITY_AUDIT_v8.md`.
