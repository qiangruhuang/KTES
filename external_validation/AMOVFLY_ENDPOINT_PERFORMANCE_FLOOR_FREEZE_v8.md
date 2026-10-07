# AMOVFLY engineering endpoint and performance-floor freeze v8

**Status:** **FROZEN_BEFORE_TELEMETRY_OUTCOME_ACCESS**  
**Dataset:** AMOVFLY, pinned source commit `67069ed00ddbebd62b71aa9bb1272415e9b15ff8`  
**Primary finite population:** 257 autonomous-flight ready-data units defined by `AMOVFLY_PATH_ONLY_INVENTORY_v8.md`  
**Design:** `AMOVFLY_DESIGN_FREEZE_v8.md`  
**Telemetry outcome access at freeze:** **CLOSED**

## 1. Why the endpoint is waypoint attainment, not cross-track error

The AMOVFLY source README identifies `real_lat`/`real_long` as the actual trajectory and `aim_lat`/`aim_long` as the reference coordinates republished from MAVROS `current_waypoint`. A current waypoint is a point target, not a time-synchronized reference trajectory. Therefore the replacement validation will not label the pointwise actual-to-aim distance as cross-track error.

The primary engineering construct is **waypoint attainment**: whether the actual trajectory enters a prespecified horizontal acceptance radius around each consecutively active current waypoint.

## 2. External performance floor

The primary radius is frozen at **10 m** before AMOVFLY telemetry is opened.

Reason: current PX4 documentation defines `NAV_ACC_RAD` as the waypoint acceptance radius and lists a default value of **10.0 m**. This is used only as an external engineering reference threshold. The AMOVFLY repository does not publish the actual flight-controller parameter used for each recorded flight, so 10 m must not be described as the historical onboard configuration.

External source anchor:
- PX4 Parameter Reference, `NAV_ACC_RAD`, default 10.0 m: https://docs.px4.io/main/en/advanced_config/parameter_reference.html
- PX4 mission documentation: acceptance radius is the circle within which a waypoint is considered reached: https://docs.px4.io/main/en/flying/missions.html

A stricter **2 m** radius is frozen as a secondary sensitivity analysis only, motivated by the current ArduPilot multicopter waypoint-radius default. It cannot replace or alter the 10 m primary gate after outcomes are opened.

Secondary source anchor:
- ArduPilot `WP_RADIUS_M` implementation/default: https://firmware.ardupilot.org/coverage/AC_WPNav/AC_WPNav.cpp.gcov.html

## 3. Frozen per-flight outcome construction

Required ready-data columns are `real_lat`, `real_long`, `aim_lat`, and `aim_long`. Column-name matching is exact after trimming whitespace. If the required schema is absent for any frozen finite-population unit, the execution fails closed; the unit is not silently removed.

For flight `i`:

1. A valid waypoint row has finite `aim_lat` and `aim_long` within geographic latitude/longitude ranges.
2. The waypoint key is `(round(aim_lat, 7), round(aim_long, 7))`. A **waypoint episode** is a maximal consecutive run with the same waypoint key.
3. For every waypoint episode `j`, compute great-circle horizontal distance from every valid actual position row in that episode to its active waypoint using Earth mean radius 6,371,008.8 m.
4. Let `d_ij` be the minimum valid horizontal distance in episode `j`. If an episode has a valid waypoint but no valid actual-position row, set `d_ij = +infinity`, so that episode is conservatively counted as not attained.
5. If a flight contains no valid waypoint episode, stop the external-validation execution with `OUTCOME_SCHEMA_UNIT_FAILURE`; do not redefine the finite population.

Primary per-flight bounded performance outcome:

`Y_i(10m) = mean_j I(d_ij <= 10 m)`.

Thus `Y_i` is the proportion of commanded waypoint episodes attained within the frozen reference radius; higher is better and `0 <= Y_i <= 1`.

Primary flight-level engineering failure indicator:

`F_i(10m) = I(any_j d_ij > 10 m) = I(Y_i < 1)`.

Prespecified secondary sensitivity:

`Y_i(2m) = mean_j I(d_ij <= 2 m)` and `F_i(2m) = I(Y_i(2m) < 1)`.

Additional descriptive diagnostics, which do not change the gate, are the number of waypoint episodes and the median, 90th percentile, and maximum of finite `d_ij` values.

## 4. Frozen target estimands

The benchmark profile remains equal-weight over the 257 frozen autonomous-flight units.

Primary population estimand:

`mu_Y = (1/257) * sum_i Y_i(10m)`.

Primary failure-rate estimand:

`mu_F = (1/257) * sum_i F_i(10m)`.

Pre-specified critical domains for bounded-performance estimation are:
- scenario: FAFS, FAVS, VAFS, VAVS;
- UAV identity: G, R, Y.

The difficult-case evaluation set has exactly `ceil(0.10 * 257) = 26` units. After the complete frozen population outcomes are computed, units are ordered by `(Y_i(10m), unit_id)` ascending and the first 26 are used. `unit_id` is the outcome-blind Git-blob identity and is frozen solely as the deterministic tie-break. The difficult-case set is never used by the sampler.

## 5. Frozen estimator/comparator evaluation

The already frozen sampling design is unchanged:
- c-pKTES-Hedge: 3 certainty sentinels + 37 positive-pi probability units;
- stratified SRS: same 6/23/6/5 scenario allocation;
- Split15+Audit25: frozen pre-outcome adapter recorded in `AMOVFLY_DESIGN_FREEZE_v8.md`.

Use the same replay seed block `20261001 ... 20261500` and the same recovered R5 estimator/UQ implementation. No method constant, sentinel rule, inclusion probability, feature, stratum, allocation, endpoint, or threshold may be changed after telemetry outcomes are opened.

## 6. External-validation guardrails

Because the primary outcome is bounded on the same [0,1] scale as the Phase2A SA outcome, the Phase2A numerical guardrails are carried forward unchanged rather than creating new thresholds after dataset selection:

1. no inclusion-probability failure and no non-certainty unit with `pi <= 0`;
2. c-pKTES probability-remainder ESS median >= 18.5 and 5th percentile >= 12;
3. profile error is not materially worse than stratified SRS: paired mean `profile_error_KTES - profile_error_SRS <= 0.01`;
4. mean absolute critical-domain error is not worse than the better comparator by more than 0.02;
5. difficult-case hit rate is not lower than Split15+Audit25 by more than 10 percentage points.

The failure-rate estimation error, UQ coverage, 2 m sensitivity outcome, episode-distance diagnostics, and method-specific estimates are reported but do not create additional post hoc pass/fail rules.

## 7. Interpretation boundary

A supportive result would show that the frozen probability-preserving KTES logic transports to a second real autonomous-flight finite population under an independently fixed waypoint-attainment criterion. It would not establish that 10 m was AMOVFLY's actual configured waypoint radius, certify an aircraft for operations, or establish a universal UAV navigation requirement.

After this file is committed, the design-object SHA and this endpoint contract together authorize telemetry outcome extraction. Any schema failure must be reported rather than repaired using observed performance values.
