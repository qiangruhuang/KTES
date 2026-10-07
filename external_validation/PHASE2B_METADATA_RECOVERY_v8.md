# Phase 2B IDF-DS public metadata recovery audit v8

**Audit date:** 2026-10-07  
**Parent source gate:** `PHASE2B_SOURCE_GATE_v8.md`  
**Status:** **NO QUALIFYING PUBLIC UNIT-LINKED PREOUTCOME METADATA PACKAGE FOUND**  
**Phase 2B gate:** remains **BLOCKED_SOURCE_STRUCTURE**  
**Telemetry outcome access:** remains **CLOSED**

## 1. Purpose

The Phase 2B source gate showed that the public IDF-DS Zenodo archives do not have the per-flight `mission.txt` / `parameters.csv` layout described in the Scientific Data paper. Before treating that mismatch as a terminal data limitation, a targeted public-source recovery audit was performed to determine whether the missing unit-linked preflight metadata had been released elsewhere by the authors or their institutions.

This audit searched only for information that could legitimately have existed before each flight outcome: mission/waypoint plans, controller-configuration snapshots, preflight/environmental metadata, or a unit-level mapping that would link those records to the intended finite population. Telemetry-derived GPS trajectories, realised wind/speed/state histories, post-flight summaries and third-party features reconstructed from telemetry were explicitly excluded as design covariates.

## 2. Public-source search coverage

The search covered five distinct source classes, supplemented by GitHub code search:

1. author-associated project/data pages for César García-Gascón, Javier Bas-Bolufer, Pablo Castelló-Pedrero and Juan Antonio García-Manrique;
2. Zenodo records/versions/related deposits associated with IDF-DS and the original authors;
3. exact-file searches for `cheste_QGroundControl.plan`, `mission.txt`, `parameters.csv`, `flight_001`, `Speedybee DataSet.zip`, and `Holybro Pixhawk.zip`;
4. Universitat Politècnica de València / Instituto IDF project and publication pages;
5. searches for a corrected or later `v1.1` / `v2` IDF-DS release after the 2025-08-29 v1.0 deposit.

The principal first-party/public records reviewed were:

- Zenodo record `16992976`: https://zenodo.org/records/16992976
- concept DOI `10.5281/zenodo.16992975`
- Scientific Data article DOI `10.1038/s41597-026-06716-3`
- PMC full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC12982758/
- Instituto IDF publication/news page: https://institutoidf.com/news/63775a02-8b0d-4147-bc2c-218a6f64ec96
- UPV author/publication pages returned for the original research team.

GitHub code search was also used for the dataset title and exact release/file terminology. Returned repositories were third-party users of the Zenodo dataset, not author-owned companion releases.

## 3. Findings

### 3.1 No later official release was found

The public Zenodo record still identifies the dataset as **Version v1.0**, published 2025-08-29. The targeted search did not identify an author-associated v1.1, v2, correction deposit, supplemental archive, or replacement record containing the missing per-flight structural metadata.

This is a bounded public-source conclusion as of the audit date, not a claim that the authors never retained such files privately.

### 3.2 First-party pages point back to the same Zenodo release

The Scientific Data paper and derivative institutional/publication pages consistently direct users to Zenodo concept DOI `10.5281/zenodo.16992975` / record `16992976`. No separate first-party download for per-flight missions, controller snapshots, weather logs, or a 240-flight mapping was surfaced.

### 3.3 The publication describes metadata that are absent from the public archive

The Scientific Data article explicitly states that each of the two architecture directories contains 120 `flight_XXX` folders and that each flight folder includes a mission plan, controller-parameter snapshot and GPS path. It also states that environmental wind/temperature/humidity information was recorded for context.

Direct ZIP central-directory audits of the current Zenodo v1.0 files do not reproduce that described release structure. Instead, the public archives expose processed/ungrouped telemetry layouts, one archive-level `cheste_QGroundControl.plan` per architecture archive, and no per-flight `parameters.csv` or independent weather/preflight metadata file identifiable from the release structure.

The two detected archive-level `.plan` files are byte-identical and therefore cannot supply flight-level condition variation.

### 3.4 Third-party reconstructed datasets do not solve the design problem

Several third-party projects use or preprocess IDF-DS. Some reconstruct flight-disjoint tables from telemetry and report different usable-flight counts. These sources are useful corroboration that the public release is being interpreted from its processed telemetry layout, but they are not eligible Phase 2B design inputs because their covariates are derived from realised flight data and are not first-party preflight records.

Accordingly, no third-party derived dataset is used to rescue the preregistered sampling frame.

## 4. Recovery decision

No qualifying **public, unit-linked, pre-outcome metadata package** was found in the targeted recovery audit. Therefore the existing status remains:

> **Phase 2B = BLOCKED_SOURCE_STRUCTURE — INSUFFICIENT PREOUTCOME COVARIATE RESOLUTION.**

This is not a c-pKTES-Hedge performance failure. No Phase 2B outcome data have been opened for the sampling design, and the dataset remains uncontaminated as an external outcome source.

## 5. Minimum package that would reopen Phase 2B

Phase 2B may resume without redesign if the original data producers provide a package that was recorded independently of the post-flight outcomes and contains, at minimum:

1. **Unit identity map**
   - intended flight ID for all eligible SpeedyBee and Pixhawk missions;
   - mapping from those flight IDs to the filenames/processed IDs in the public Zenodo release;
   - explanation of the public SpeedyBee `Lap001..Lap111` versus reported 120-flight discrepancy.

2. **Per-unit mission/configuration metadata**
   - the original `mission.txt`, `.plan`, or equivalent waypoint/mission file associated with each flight, if these varied by flight; and/or
   - preflight `parameters.csv` / controller configuration snapshots associated with each flight.

3. **Per-unit independently recorded environment metadata, if available**
   - wind speed/direction, temperature, humidity or other field measurements recorded independently of onboard flight outcomes;
   - timestamps or flight IDs sufficient to join them without examining telemetry performance.

4. **Provenance**
   - creation/acquisition semantics showing that these variables were fixed or observed before/during preflight rather than derived retrospectively from the outcome telemetry;
   - hashes or immutable file identities once received.

The package does **not** need to reproduce every field imagined by the original Phase 2B plan. It needs enough genuine unit-level pre-outcome heterogeneity to instantiate the already frozen kernel/novelty/tail/sentinel design without using outcome-bearing telemetry.

## 6. What remains prohibited

Until such a package is obtained and hash-frozen, the following remain prohibited as Phase 2B selection features:

- realised GPS/path geometry extracted from telemetry;
- realised wind inferred from airspeed/groundspeed;
- realised altitude, speed, duration, turn rate or flight-mode history;
- battery, power, airspeed, sensor, actuator or estimator histories;
- log size/duration as a proxy for flight difficulty;
- post-flight anomaly/quality labels;
- third-party features reconstructed from any of the above.

Using these data to define the sampling design would make IDF-DS a development dataset and would invalidate an independent external-validation claim.

## 7. Research consequence

The evidence chain is now cleanly separated:

- **Phase 1/v7:** controlled evidence frozen;
- **Phase 2A:** completed, `PASS_WITH_EXECUTION_CLARIFICATION`;
- **Phase 2B method contract:** frozen before outcomes;
- **Phase 2B public-source audit:** source structure does not support the frozen outcome-blind flight-level design;
- **Phase 2B metadata recovery:** no qualifying public companion package found as of 2026-10-07;
- **Phase 2B outcomes:** remain unopened for the KTES sampling study.

If no private/original preflight package can be obtained, the scientifically defensible next step is to report IDF-DS as an external-data limitation and preregister a different independent engineering dataset. IDF-DS must not be converted into a development set and then relabelled as confirmation.
