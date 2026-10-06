# Phase 2B pre-outcome freeze v8

**Freeze date:** 2026-10-06  
**Dataset:** IDF-DS / Fixed-Wing UAS Telemetry Benchmark  
**Status:** **PRE-OUTCOME FROZEN FOR STRUCTURAL/SCHEMA AUDIT — FLIGHT-LEVEL TELEMETRY OUTCOMES MUST REMAIN CLOSED**

## 1. Purpose and relationship to Phase 2A

Phase 2A is locked as `PASS_WITH_EXECUTION_CLARIFICATION`. Phase 2B is a separate engineering-facing external validation of the already frozen Phase 1.2R-5 method. It must not be used to retune `rho`, `lambda`, certainty-sentinel count/type, the inclusion-probability floor, the Hájek estimator, Local Cube, or the R3 calibration constants.

The Phase 2B question is:

> With a fixed live-test budget of 40 flights, can frozen c-pKTES-Hedge preserve finite-population inference for a real fixed-wing mission-performance outcome while maintaining useful coverage of difficult flights and stable probability weights?

Phase 2B is not an architecture superiority study and is not a flight-safety certification exercise.

## 2. Public-source facts frozen before outcome access

The source-of-record paper and Zenodo release establish the following facts before flight-level outcome extraction:

- IDF-DS contains 240 autonomous fixed-wing flights and more than 32 hours of flight data.
- The release contains 120 SpeedyBee F405 / INAV flights and 120 Holybro Pixhawk 6X + Jetson Orin NX / PX4 flights.
- Each flight folder contains a controller log, `parameters.csv`, `mission.txt`, and an extracted GPS path; the Zenodo release also provides grouped and ungrouped telemetry representations.
- The same Volantex Ranger 2400 airframe family is used, with different avionics masses/configurations.
- The paper reports a cruise-speed range of 14–17 m/s and an approximate Ranger 2400 stall speed of 9 m/s.
- The SpeedyBee airspeed sensor is optional, whereas the Pixhawk configuration uses a DroneCAN pitot tube. Consequently, a 9 m/s indicated-airspeed floor is not a valid common primary endpoint across both architectures.
- Environmental wind, temperature and humidity were recorded for context. The paper's demonstrated wind estimate is derived from aircraft airspeed, groundspeed and attitude; such telemetry-derived wind is an outcome-derived quantity and is not permitted as a sampling covariate.
- The published mission descriptions include a 17-waypoint zigzag trajectory of approximately 5.4 km per lap and a 54-waypoint circuit of 3,906 m; the latter has a mission-profile average groundspeed of about 15 m/s.

The paper contains wording indicating repeated predefined trajectories under both control architectures but also describes configuration-specific mission examples. Therefore the exact architecture × mission cross-tab is treated as **unknown until reconstructed from `mission.txt` only**. No causal claim comparing PX4 with INAV is permitted unless common mission support is demonstrated from pre-outcome mission metadata.

## 3. Finite population, unit and estimand

The intended finite population is all 240 released flights.

- unit: one autonomous flight;
- intended profile weight: equal weight, `p_i = 1 / N_eligible`;
- primary strata: `SpeedyBee_INAV` and `Pixhawk_Jetson_PX4`;
- intended live-test allocation: 20 / 20 at `n=40`.

### 3.1 Outcome-blind eligibility

A flight is structurally eligible if, before reading any telemetry values:

1. its architecture identity is known;
2. `mission.txt` is present and parseable;
3. at least one raw telemetry/log representation is present and its schema is capable of yielding GNSS position and mission/flight-mode state;
4. the file set is not duplicate-identical to another flight identity.

Only file existence, names, sizes, hashes, headers/topic names, mission plans and static parameter names/values may be used at this gate. GPS trajectories, sensor values, flight-mode timelines, failsafe events, energy traces, airspeed values and other flight outcomes must remain unopened.

If either architecture has fewer than 20 structurally eligible flights, execution fails closed; the 40-flight budget is not redistributed after inspecting outcomes. If eligibility changes `N` from 240, the changed finite-population estimand must be reported explicitly.

## 4. Outcome-blind Phase 2B design frame

### 4.1 Mandatory mission-geometry features

The following features are computed only from `mission.txt` after deterministic coordinate conversion:

1. `waypoint_count`;
2. `planned_horizontal_length_m`;
3. `median_nonzero_leg_length_m`;
4. `planned_altitude_range_m`;
5. `planned_altitude_median_m`;
6. `total_abs_turn_rad_per_km`;
7. `max_abs_turn_deg`;
8. `fraction_turns_ge_45deg`;
9. explicit planned/commanded speed in m/s, if encoded by the mission format.

Mission loops/JUMP instructions, when present, are expanded according to the mission-file semantics before these quantities are calculated. Takeoff and landing items are retained for mission-completion semantics but excluded from route-complexity turn calculations.

### 4.2 Static configuration features

A small semantic cross-platform map may add only these preflight concepts:

- configured cruise/trim speed;
- configured maximum bank angle;
- configured waypoint/turn-control scale.

A concept is included in the common kernel matrix only if an official firmware definition exists for both architectures and the corresponding static parameter is structurally available in at least 95% of each stratum. This availability check may inspect parameter names and missingness only; it may not use telemetry outcomes. If a common semantic mapping cannot be established, the concept is omitted globally rather than imputed from flight outcomes.

### 4.3 Environmental context

A wind/temperature/humidity variable may enter the design frame only if it exists as an independent contextual or preflight record not calculated from aircraft telemetry. Wind reconstructed from airspeed, groundspeed, attitude, GPS or any post-flight sensor stream is prohibited from sentinel selection, novelty scoring and inclusion-probability construction.

### 4.4 Feature processing

- architecture defines the two sampling strata and is not interpreted as a causal exposure;
- continuous features use the same frozen standardization and kernel code recovered for R5;
- no feature is screened using the flight-performance outcomes;
- constant or structurally unavailable common features are removed by a deterministic schema-only rule;
- kernel/RFF/novelty implementation and historical fixed seed lineage are inherited from the recovered R5 engine rather than reimplemented from prose.

## 5. Frozen sampling design

The Phase 1.2R-5 method remains unchanged:

- `n=40`;
- 3 outcome-blind certainty sentinels with portfolio `NRR`;
- 37 known positive-inclusion-probability remainder units;
- `rho=0.20`;
- `lambda=3.0`;
- minimum-probability fraction `0.35`;
- score = 80% kernel novelty + 20% compound adverse-tail score;
- Local Cube spreading/balance;
- stratum-wise Hájek model-assisted residual correction;
- `max(GS,PWR)` design UQ;
- R3 failure calibration constants retained without re-estimation.

The intended allocation is exactly 20 SpeedyBee / 20 Pixhawk-Jetson. Certainty units count against the allocation of their own stratum.

For finite-population replay evaluation after outcomes are opened, the fixed 500-seed block `20261001 ... 20261500` is reused. Reusing the existing Phase 2A block avoids selecting a new randomization schedule after seeing Phase 2B results.

## 6. Primary engineering outcome

### 6.1 Flight-level route-tracking error

For flight `i`, define the horizontal cross-track distance `d_i(t)` as the geodesic/local-tangent-plane distance from the observed GNSS position to the planned horizontal mission polyline during the autonomous waypoint-tracking segment.

The common, dimensionless tracking error is

\[
E_i = \frac{Q_{0.95}\{d_i(t)\}}{\operatorname{median}(\text{non-zero planned leg lengths}_i)}.
\]

The primary task-effectiveness score is

\[
Y_i = \exp(-E_i),
\]

so that larger values are better and `0 < Y_i <= 1`. The normalization is determined entirely by the mission plan and makes the score comparable across missions of different geometric scale. The 95th percentile targets sustained adverse tracking while limiting sensitivity to single-sample GNSS spikes.

The waypoint-tracking segment begins after the planned takeoff phase enters autonomous route execution and ends at the planned landing/terminal mission transition. Platform-specific state/topic names may differ, but their mapping to this semantic segment must be coded and hashed before any telemetry values are evaluated. If a platform cannot support this mapping from documented flight-mode/mission state, Phase 2B blocks rather than substituting a post hoc segment definition.

### 6.2 Population target

The primary estimand is the equal-weight finite-population mean

\[
\mu_Y = N_{eligible}^{-1}\sum_i Y_i.
\]

c-pKTES, stratified SRS and any retained split-style sensitivity design are evaluated against the known finite-population truth after all outcomes are opened.

## 7. Frozen engineering failure indicator

The binary failure endpoint is mission-execution failure rather than an arbitrary airspeed cutoff:

`F_i = 1` if at least one of the following occurs during the intended autonomous mission:

1. the mission does not reach its documented terminal mission state;
2. a recorded system failsafe/abort produces an unplanned RTH, hold, landing or termination;
3. the log terminates before the planned terminal state without a documented normal landing/disarm completion.

Planned RTH/landing mission items are not failures. Manual RC override is counted as a failure only when the log/status semantics identify it as an intervention replacing the intended autonomous mission execution, not when it is a planned operational mode transition.

The platform-specific mapping of PX4 and INAV states to these three semantic conditions must be specified from firmware documentation and hash-frozen before reading state values. No failure definition may be changed after the observed failure rate is known.

For failure probability, the same frozen stratum-wise Hájek residual structure is used with `F_i` in place of the continuous outcome. The R3 calibration constants are carried forward as a fixed sensitivity/safety diagnostic. Because their exchangeability assumption was developed in synthetic campaigns, Phase 2B will report their empirical finite-population replay coverage and will not claim distribution-free safety certification.

## 8. Secondary outcomes fixed before telemetry access

These are secondary and cannot change the primary gate.

1. **Raw route tracking:** `Q95` cross-track error in metres and median cross-track error.
2. **Mission completion ratio:** fraction of the planned route/mission sequence completed before the terminal state.
3. **Energy intensity:** Wh per flown kilometre over the autonomous segment when voltage/current data are structurally valid.
4. **IAS margin diagnostic:** only for flights with a documented, valid indicated-airspeed sensor. Report `Q05(IAS) - 9 m/s` and time fraction below 9 m/s during the autonomous cruise/waypoint segment. The paper's approximate 9 m/s stall speed is used only as an airframe-level secondary reference; it is not substituted by groundspeed and is not the common primary failure floor.
5. **Environmental sensitivity:** independent recorded weather may be used for stratified description; telemetry-derived wind remains outcome-side information only.

## 9. Difficult-flight and critical-domain evaluation

After the full outcome vector is opened, define the difficult set as the bottom 10% of full-population `Y_i`. This is an evaluation label only and is never supplied to the sampler.

Primary critical domains are the two architecture strata. If pre-outcome `mission.txt` hashing identifies multiple recurring mission signatures with at least 10 eligible flights each, architecture × mission-signature cells are added as prespecified secondary domains. No domain is created from observed `Y_i` or `F_i`.

## 10. Comparators

### 10.1 Primary comparator

**Stratified SRS**, n=40, exactly 20 / 20 across the two architecture strata.

### 10.2 Split-style sensitivity comparator

The split-style family is secondary in Phase 2B. If retained, its numerical adapter must be frozen before outcomes:

- 15 deterministic outcome-blind geometry/configuration points;
- 25 probability-audit points;
- total architecture allocation remains 20 / 20;
- deterministic slots are allocated 8 / 7 across the fixed stratum order `SpeedyBee_INAV`, `Pixhawk_Jetson_PX4`;
- audit slots are therefore 12 / 13;
- within each stratum, deterministic selection uses the recovered historical maximin/kernel-geometry rule only;
- audit selection is SRS without replacement from the non-deterministic remainder.

This rule is fixed here before Phase 2B telemetry outcomes are opened. It is a Phase 2B execution adapter, not a claim that the exact two-stratum 8/7 mapping existed in Phase 1.

## 11. Phase 2B replay metrics and gates

The primary structural-transfer gates reuse the bounded-score scale established for Phase 2A:

1. no sampling failure and every non-certainty unit retains positive inclusion probability;
2. probability-remainder ESS median >= 18.5 and 5th percentile >= 12;
3. paired mean profile-error difference `MAE(c-pKTES) - MAE(stratified SRS) <= 0.01` on `Y_i`;
4. critical-domain MAE is not worse than the better retained baseline by more than 0.02 on the bounded `Y_i` scale;
5. difficult-flight hit rate is not lower than the split-style sensitivity baseline by more than 10 percentage points, if the split-style adapter passes its own pre-outcome freeze; otherwise compare difficult-hit descriptively against stratified SRS and mark gate 5 not evaluable rather than inventing a replacement comparator.

Failure-probability MAE, uncalibrated design-UQ coverage and R3-calibrated coverage are mandatory secondary inference diagnostics. They do not override a failed primary structural-transfer gate.

## 12. Execution chronology and fail-closed rules

The following order is mandatory:

1. freeze this document;
2. inventory the IDF-DS archive using filenames, hashes, sizes and schemas only;
3. construct the 240-flight structural eligibility table;
4. parse `mission.txt` and static `parameters.csv` only;
5. build and hash the outcome-blind design frame;
6. freeze the PX4/INAV state-semantic adapter for waypoint segment and mission-execution failure;
7. instantiate and hash the c-pKTES design object, inclusion probabilities, sentinel identities and comparator objects;
8. only then open GNSS trajectories, state timelines, airspeed, battery/power and other flight-level telemetry values;
9. compute all flight-level outcomes;
10. run the frozen 500 paired replays and report the complete gate, including negative results.

If any definition cannot be implemented from the documented fields, execution stops. The same telemetry may not be used to redesign the endpoint and then be relabelled as independent external confirmation.

## 13. Interpretation boundary fixed in advance

A supportive Phase 2B result would show that the probability-preserving sampling/inference logic transfers from controlled simulation and Anti-UAV410 to a real engineering telemetry benchmark. It would not establish:

- causal superiority of PX4 over INAV or vice versa;
- operational deployment-frequency representativeness;
- aircraft certification or airworthiness;
- a validated stall boundary for every Ranger 2400 configuration;
- live-weapon or mission-safety certification.

Architecture effects are especially restricted because mission geometry, acquisition period, avionics mass and controller architecture may be partially or fully confounded in the released benchmark.

## 14. Source anchors reviewed before freeze

1. García-Gascón C, Bas-Bolufer J, Castelló-Pedrero P, García-Manrique JA. *An open benchmark dataset for machine learning and intelligent trajectory optimization in fixed-wing unmanned aerial systems*. Scientific Data. 2026;13:364. DOI: `10.1038/s41597-026-06716-3`.
2. García Gascón C. *Fixed-Wing UAS Telemetry Benchmark (IDF_DS): 240 Flights for ML and Intelligent Trajectory Optimization*. Zenodo v1.0. DOI concept record: `10.5281/zenodo.16992975`; version record: `10.5281/zenodo.16992976`.
3. PX4 documentation: fixed-wing Mission mode / waypoint-switch semantics and controller documentation for mission setpoints and TECS.
4. INAV documentation/source: `nav_wp_radius`, fixed-wing waypoint tracking/turn smoothing, mission waypoint semantics, and INAV 6.1 release documentation.
5. Internal frozen sources: `protocol/KTES_Phase2_Frozen_Contract_v1.0.json`, `protocol/KTES_Phase2_External_Validation_Protocol_v1.0.md`, recovered R5 engine and Phase 2A CI evidence.

No flight-level IDF-DS telemetry outcome vector was inspected to choose the definitions in this freeze.