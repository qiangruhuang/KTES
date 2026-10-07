# Phase 2 replacement external-engineering candidate audit v8

**Audit date:** 2026-10-07  
**Selection-rule source:** `PHASE2_REPLACEMENT_DATASET_SELECTION_FREEZE_v8.md`  
**Outcome access:** **CLOSED for all candidate datasets during this audit**  
**Decision:** **ELIGIBLE_REPLACEMENT_SELECTED — AMOVFLY**  
**Selection tier:** priority 2 (real autonomous UAV flight; not accepted as verified fixed-wing)

## 1. Decision rule applied

The replacement-data rules were frozen before this candidate search. A dataset must satisfy all seven mandatory criteria before outcome-blind ranking is allowed. Priority is then:

1. real fixed-wing UAS;
2. other real autonomous/robotic flight systems;
3. simulation is ineligible for the primary replacement gate.

The search therefore first attempted to identify a qualifying fixed-wing dataset with at least 80 distinct flight/test units, unit-linked pre-outcome condition/configuration variables, physically separable outcome telemetry, a continuous engineering performance endpoint, and stable public provenance.

No unit-level performance distributions, failure rates, KTES/SRS results, difficult-case labels, or candidate-specific outcome statistics were inspected or used for this selection.

## 2. Priority-1 fixed-wing audit

| Candidate | Real fixed-wing | N gate | >=4 unit-linked pre-outcome covariates | System-performance endpoint | Stable public source | Eligibility decision |
|---|---|---:|---|---|---|---|
| IDF-DS | Yes | 240 reported | **No in current public release** | Yes | Zenodo + Scientific Data | **Blocked source structure**; already audited separately |
| FliPASED flight-test data | Yes | **28** flight tests | Yes | Yes | HUN-REN/SZTAKI research-data repository | **Fail N gate** |
| ALFA fixed-wing fault dataset | Yes | **47** processed autonomous flights | fault/control context exists | Yes | public Figshare/data DOI | **Fail N gate** |
| NASA J-FLiC acoustic/control campaign | Yes | **26** flights in the public 2015 campaign report | test-condition descriptions exist | Yes | NASA NTRS presentation, not an open unit-level flight-data release | **Fail N gate / reusable-data gate** |
| UK LAPSE-RATE | Mixed; four BLUECAT5 fixed-wing among seven UAS | 178 files across mixed platforms | campaign/site/profile metadata exists | **Primary data are atmospheric measurements** | Zenodo + ESSD | **Fail engineering-endpoint criterion** |
| SCALES 2024 | Mixed multirotor/fixed-wing/VTOL | 1064 campaign flights | flight/operator catalog exists | **Primary data are atmospheric measurements** | Zenodo | **Fail engineering-endpoint criterion** |
| Fixed-wing micro-UAV INS/GNSS open data | Yes | only a few released missions | rich mission/sensor metadata | navigation/photogrammetric trajectory products | Zenodo | **Fail N gate** |

### Fixed-wing conclusion

The targeted search did not identify a public priority-1 candidate satisfying all mandatory criteria. This is not a claim that no such dataset can exist; it is the frozen decision for the public candidate set identified before replacement outcome access. The fixed-wing priority therefore does not block evaluation of priority-2 real-flight candidates.

## 3. Priority-2 candidate audit

### 3.1 AMOVFLY

**Primary source:** `YujiaoHu/AMOVFLY-Dataset`  
**Source commit frozen for candidate selection:** `67069ed00ddbebd62b71aa9bb1272415e9b15ff8`  
**Paper:** Lee et al., *AMOVFLY: Enabling Advanced UAV Modeling With the Comprehensive Flight Status Dataset*, IEEE Transactions on Intelligent Transportation Systems, Early Access, 3 September 2026, DOI `10.1109/TITS.2026.3728060`.

The public source reports 270+ real flights (>46 h) across three UAV identities and five reference routes, with fixed/variable altitude and speed scenarios and multi-UAV operations.

The candidate is deliberately **not classified as fixed-wing** for the priority rule. The accessible paper/repository metadata identify heterogeneous AMOVLAB UAV platforms but do not provide sufficient source evidence to assign UavR/UavY/UavG to a fixed-wing airframe. It is therefore conservatively assessed only under priority 2.

#### Pre-outcome design variables available without flight-performance values

The repository documentation and filenames make the following unit-linked variables available before opening the ready/raw telemetry values:

- scenario / `Data Dir` (FAFS, FAVS, VAFS, VAVS, Random; multi-UAV records are separately indexed);
- reference route (five routes are documented);
- UAV identity (`UavR`, `UavY`, `UavG`);
- commanded/configured payload parameter encoded in the file identity;
- commanded/configured altitude parameter encoded in the file identity;
- commanded/configured speed parameter encoded in the file identity;
- battery identity encoded in the raw-flight identity and reported as `BatteryName`;
- flight start date/time;
- nearest-station wind speed (`WindSpeed_station`), pressure (`AirPressure_station`), temperature and weather obtained from the Visual Crossing Weather API.

The source also contains fields that are **not allowed** in the design frame because they are outcome-derived. These are frozen out before any value access:

- `Length(s)`;
- `BatteryCost`;
- `AllPower`;
- `WindSpeed_test`;
- `AirPressure_test`;
- any realised position, speed, acceleration, battery, wind, pressure or power value from ready/raw flight files.

`Flight_info.csv` header was inspected only to verify schema; unit-level rows were not used for selection.

#### Outcome separation and endpoint feasibility

Flight outcome streams are stored separately in raw/ready flight CSVs. The documented telemetry contains both actual trajectory (`real_lat`, `real_long`) and reference waypoint coordinates (`aim_lat`, `aim_long`), plus position, velocity, attitude, battery voltage/current and power. This supports a continuous engineering endpoint such as reference-trajectory tracking error after the design is frozen. Energy/power outcomes are available as secondary engineering endpoints.

The exact primary endpoint and performance-floor threshold are **not chosen in this candidate audit**. They must be declared from engineering semantics or an independent external tolerance before outcome values are opened.

#### Mandatory eligibility result

| Criterion | Result | Basis |
|---|---|---|
| Independent external source | PASS | not used in Phase 1, R3/R5, or Phase 2A |
| Finite repeated engineering population | PASS | 270+ real flights; one identifiable flight file per unit |
| Real system | PASS, priority 2 | real UAV flights; no verified fixed-wing claim used |
| >=4 unit-linked pre-outcome covariates | PASS | route, UAV, payload, altitude, speed, scenario, battery, independent station weather |
| Outcome separation | PASS | pre-outcome identifiers/settings can be whitelisted separately from raw/ready telemetry |
| Engineering endpoint feasibility | PASS | documented reference vs actual trajectory and power streams; threshold still to be frozen |
| Traceable execution | PASS | public GitHub repository + IEEE paper; source commit can be pinned and hashes generated |

**AMOVFLY eligibility: PASS.**

### 3.2 CMU / DJI Matrice 100 package-delivery dataset

The Scientific Data release contains 209 real quadcopter recordings, including 195 parameterized autonomous flights. The attached `parameters.csv` records programmed ground speed, payload and cruise altitude plus date/time and route; processed telemetry is separately provided.

For the homogeneous 195-flight autonomous mission population, the documented varying engineering controls are speed, altitude and payload, while the triangular reference route is essentially common. Date/time are identifiers/context rather than a fourth independently designed engineering condition. The release does not itself provide an independent unit-linked preflight weather table.

Under the already frozen strict rule requiring at least four defensible varying pre-outcome condition/configuration variables, this candidate is **not eligible as currently released**. It is not rescued by deriving wind or other conditions from flight telemetry.

**CMU Matrice-100 eligibility: FAIL criterion 4.**

### 3.3 UAV-SEAD

UAV-SEAD contains 1,396 categorized and 3,196 raw real multirotor PX4 flight logs across diverse hardware/sensor/environment contexts. This easily passes the size and real-system criteria. However, the publicly documented feature richness is primarily contained in ULog/uORB flight streams and the anomaly labels were assigned from post-flight physical/expert evaluation. The public dataset card does not expose a separate unit-level preflight condition/configuration table sufficient to define four or more KTES selection covariates before outcome access.

Using PX4 `sensor_preflight`, hardware-device IDs, mission/setpoint topics, flight states, or anomaly labels from the logs to construct the design frame would require opening the same flight logs that contain the outcome process and would violate the frozen outcome-separation rule.

**UAV-SEAD eligibility: FAIL criteria 4–5 for the present KTES external-validation design.**

### 3.4 LAPSE-RATE and SCALES

Both are large, valuable real UAS campaigns and include fixed-wing aircraft. Their released finite-population products are designed primarily to measure atmospheric thermodynamic/kinematic quantities. The flight itself is the sensor deployment mechanism, rather than the system whose performance is being qualified against a command/reference endpoint.

Reframing atmospheric observations as a UAV engineering performance outcome would alter the pre-specified scientific question. They are therefore not eligible replacement datasets despite their real-flight provenance and, in SCALES, large N.

**LAPSE-RATE/SCALES eligibility: FAIL criterion 6.**

## 4. Outcome-blind ranking of eligible candidates

Only mandatory-eligible candidates may be ranked. In the current audit, AMOVFLY is the only candidate that passes all seven mandatory criteria.

| Dimension | Frozen weight | AMOVFLY assessment | Score contribution |
|---|---:|---|---:|
| Unit-linked pre-outcome covariate richness | 30% | high: route, vehicle, payload, altitude, speed, scenario, battery, station weather | 30 |
| Finite-population adequacy | 20% | 270+ identifiable real flights | 20 |
| Engineering closeness | 20% | real autonomous UAV flight but not accepted as fixed-wing | 14 |
| Endpoint semantic clarity | 15% | reference-vs-actual trajectory and power streams are explicitly documented | 15 |
| Reproducibility/provenance | 15% | IEEE paper + public GitHub; repository lacks archival DOI but commit can be pinned | 12 |
| **Total** | **100%** |  | **91/100** |

The score is used only after mandatory eligibility and did not use observed outcomes.

## 5. Frozen replacement decision

The predeclared selection-state is:

> **ELIGIBLE_REPLACEMENT_SELECTED — AMOVFLY**

Reason:

1. no identified priority-1 fixed-wing candidate satisfies all mandatory frozen criteria;
2. AMOVFLY satisfies all mandatory priority-2 criteria;
3. it is the only currently audited candidate with sufficiently rich unit-linked pre-outcome condition metadata, a large real-flight finite population, physically separable telemetry outcomes and a directly documented reference trajectory.

This decision authorizes only a **dataset-specific pre-outcome protocol and design-frame audit**. It does **not** authorize opening AMOVFLY performance values yet.

## 6. Next gate before any AMOVFLY outcome access

The following must be written and hash-frozen first:

1. exact finite-population eligibility rule and immutable source commit;
2. whitelist of permitted pre-outcome columns/tokens and blacklist of outcome-derived fields;
3. deterministic parser for payload / altitude / speed encoded in filenames;
4. route identity/geometry representation using the pre-existing `Route/` assets only;
5. treatment of multi-UAV paired flights and duplicate/shared-flight identities;
6. natural strata and n=40 allocation;
7. Phase-2-compatible auxiliary risk map, with no outcome-derived predictor;
8. three sentinel identities and all positive inclusion probabilities;
9. comparator design objects and replay seeds;
10. continuous primary endpoint and independent engineering performance-floor semantics;
11. full source/design hashes.

Only after this object is persisted and hashed may raw/ready flight telemetry values be opened.

## 7. Public source anchors

- AMOVFLY repository: https://github.com/YujiaoHu/AMOVFLY-Dataset
- AMOVFLY IEEE paper: https://doi.org/10.1109/TITS.2026.3728060
- CMU Matrice-100 Scientific Data paper: https://doi.org/10.1038/s41597-021-00930-x
- CMU data release: https://doi.org/10.1184/R1/12683453
- FliPASED open flight-test data: https://hdl.handle.net/21.15109/CONCORDA/PU4R32
- NASA J-FLiC public campaign record: https://ntrs.nasa.gov/citations/20160009093
- LAPSE-RATE UK dataset paper: https://doi.org/10.5194/essd-12-1759-2020
- SCALES 2024 release: https://doi.org/10.5281/zenodo.20091327
- UAV-SEAD public dataset card: https://huggingface.co/datasets/aykutkabaoglu/uav-flight-anomaly-dataset
