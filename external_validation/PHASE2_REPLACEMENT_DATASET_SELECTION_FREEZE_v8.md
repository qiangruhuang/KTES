# Phase 2 replacement external-engineering dataset selection freeze v8

**Freeze date:** 2026-10-07  
**Trigger:** IDF-DS Phase 2B `BLOCKED_SOURCE_STRUCTURE` before outcome opening  
**Status:** **FROZEN BEFORE REPLACEMENT-DATASET SEARCH / OUTCOME ACCESS**

## 1. Purpose

IDF-DS cannot currently instantiate the preregistered flight-level outcome-blind KTES design because the public release lacks unit-linked preflight mission/configuration metadata. This document freezes the rules for selecting a replacement independent engineering dataset before candidate outcome values are inspected.

The replacement is not chosen to obtain a favourable KTES result. It is chosen only on source structure, engineering semantics, external independence and executability of the already frozen c-pKTES-Hedge contract.

## 2. Required eligibility criteria

A candidate qualifies only if all of the following are satisfied from documentation, file structure, schemas, mission/configuration files, or other pre-outcome metadata without inspecting unit-level performance outcomes.

1. **Independent external source**
   - not used in Phase 1 method development, tuning, R3 calibration, R5 confirmation, or Phase 2A;
   - public and citable from a stable repository, DOI, or institutional release.

2. **Finite population of repeated engineering trials**
   - one identifiable unit per flight/test/run;
   - preferably `N >= 100`; absolute minimum `N >= 80` unless a stronger engineering justification is frozen before outcomes;
   - enough units remain outside the n=40 live-test analogue to make finite-population sampling meaningful.

3. **Real system preferred**
   - priority 1: real fixed-wing UAS flights;
   - priority 2: other real autonomous/robotic flight trials with comparable mission-condition structure;
   - simulation-only datasets are ineligible for the primary replacement gate and may be used only as a separate lower-tier validation if no real dataset can satisfy the primary criteria.

4. **Unit-linked pre-outcome covariates**
   - at least four defensible condition/configuration variables that vary across units and were specified or observed before the system-performance outcome was realised;
   - examples: mission geometry/waypoints, requested altitude/speed, controller configuration, payload/platform configuration, independently measured preflight weather/environment, commanded disturbance/degradation level;
   - unit IDs must map these variables to the same finite population used for outcome evaluation.

5. **Outcome separation**
   - performance/outcome telemetry or labels must be separable from the pre-outcome design frame;
   - selection features may not require realised GPS paths, realised speed, flight duration, post-flight state histories, energy use, anomaly scores, tracking error, failure labels or other outcome-derived quantities.

6. **Engineering endpoint feasibility**
   - after design freeze, the source must support at least one continuous system-performance endpoint with clear engineering meaning;
   - it must also support a failure/performance-floor definition from external engineering semantics or an independently declared threshold rather than an observed-failure-rate quantile.

7. **Traceable execution**
   - source files, unit mapping and design-frame inputs can be hashed and frozen;
   - missing-data/eligibility rules can be written before outcomes;
   - the frozen c-pKTES-Hedge constants can be applied without algorithm retuning.

## 3. Outcome-blind candidate ranking

Among eligible candidates, ranking uses only the following metadata-side dimensions. No observed performance values enter the ranking.

| Dimension | Weight | Outcome-blind evidence |
|---|---:|---|
| Unit-linked pre-outcome covariate richness | 30% | number, provenance and within-population variation of mission/config/environment variables |
| Finite-population adequacy | 20% | N, unit identity completeness, balance across natural strata |
| Engineering closeness to Phase 2B intent | 20% | real fixed-wing/autonomous flight, mission-level performance relevance |
| Endpoint semantic clarity | 15% | documented command/reference signals and externally interpretable performance/failure semantics, without reading values |
| Reproducibility/provenance | 15% | stable DOI/repository, documented schema, immutable files, mapping completeness |

A candidate must first pass all required eligibility criteria. Weighted ranking is not used to rescue an ineligible dataset.

## 4. Prohibited candidate-selection information

Before a replacement dataset is selected and its design-frame protocol is frozen, the following must not be inspected or used for ranking:

- candidate-specific tracking-error distributions;
- failure/anomaly rates;
- outcome means/variances;
- which units are difficult or extreme according to realised performance;
- KTES/SRS performance on candidate outcomes;
- any quantity computed from realised telemetry solely to make a candidate appear more informative.

Schema/header inspection is allowed when it reveals what variables exist but not their unit-level values.

## 5. Selection outcome

The search must end in one of three states:

1. **ELIGIBLE_REPLACEMENT_SELECTED** — exactly one highest-ranked candidate satisfies all criteria; freeze its finite population, source hashes and pre-outcome design contract before opening outcomes.
2. **MULTIPLE_ELIGIBLE_TIE** — candidates are materially tied on outcome-blind criteria; resolve with a deterministic rule frozen here: prefer real fixed-wing over other UAS, then larger complete N, then stronger immutable provenance.
3. **NO_ELIGIBLE_PUBLIC_REPLACEMENT** — stop the primary engineering external-validation extension rather than weaken the rules after seeing available datasets.

## 6. Method invariants

Replacement-dataset selection does not reopen c-pKTES-Hedge development. The following remain immutable from the Phase 2 contract unless the replacement protocol demonstrates that a quantity is a dataset-specific semantic adapter rather than a method parameter:

- n=40;
- 3 outcome-blind certainty sentinels;
- 37-unit positive-probability remainder;
- 0.80 kernel novelty + 0.20 compound adverse-tail;
- rho=0.20;
- lambda=3;
- minimum-probability fraction=0.35;
- Local Cube spreading/balance;
- stratum-wise Hájek model-assisted residual correction;
- max(GS,PWR) UQ and frozen R3 calibration constants;
- Accept / Reject / Inconclusive decision logic.

Any replacement external result, including an unfavourable result, must be retained.
