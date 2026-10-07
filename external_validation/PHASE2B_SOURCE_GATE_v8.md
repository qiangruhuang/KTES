# Phase 2B IDF-DS source-structure gate v8

**Audit date:** 2026-10-07  
**Frozen protocol:** `external_validation/PHASE2B_PREOUTCOME_FREEZE_v8.md`  
**Gate status:** **BLOCKED_SOURCE_STRUCTURE — INSUFFICIENT PREOUTCOME COVARIATE RESOLUTION**  
**Outcome access:** **CLOSED; no flight-level telemetry values were opened for this gate**

## 1. Why this gate was required

Phase 2B was preregistered to construct a flight-level outcome-blind design frame from `mission.txt`, static `parameters.csv`, and any independently recorded preflight environmental context before opening GNSS, flight-state, airspeed, power, or other telemetry values. Those variables are needed to define kernel geometry, novelty, compound-tail scoring, certainty sentinels, and positive inclusion probabilities without outcome leakage.

The Scientific Data article describes 240 flights, split 120/120 between SpeedyBee-INAV and Pixhawk-Jetson-PX4, and describes a per-flight folder organization containing mission and parameter files. The public Zenodo archives were therefore audited directly before any outcome extraction.

## 2. Outcome-blind public-archive audit

Three independent GitHub Actions audits were executed against Zenodo record `16992976` using HTTP range reads.

1. **Structural inventory**, run `37556443990`, artifact `11455650072`, artifact digest `sha256:e3e45a4cc6f71f725a86ec39f09012755b845729c5de72cf6b9b5a1996963058`.
2. **Central-directory schema probe**, run `37556600205`, artifact `11454473489`, artifact digest `sha256:957d908f5e0c35d3e4fd71e8331526e081d46d09c9d21e41e5e1b073013be6c6`.
3. **Source reconciliation**, run `37556831613`, artifact `11454518707`, artifact digest `sha256:c692e786934ce5dc8ee43e1a637c47009a65c9d0ee8fa64169606387d44d6ad2`.

The first two audits use ZIP central-directory metadata only. The reconciliation additionally reads the archive-level QGroundControl `.plan` file, which is a mission plan and therefore an allowed pre-outcome source. No processed telemetry CSV, GPS path, ULog, INAV raw log, state, airspeed, power, or sensor value was opened.

## 3. Actual release structure

| Property | SpeedyBee-INAV archive | Pixhawk-Jetson-PX4 archive |
|---|---:|---:|
| ZIP members | 252 | 17,226 |
| Processed unit IDs identifiable from names | 111 (`Lap001..Lap111`) | 120 (`vuelo_1..120` / `lap_1..120`) |
| Raw log members | 26 `LOG*.TXT` | 13 `.ulg` |
| Per-flight `mission.txt` | 0 | 0 |
| Per-flight `parameters.csv` | 0 | 0 |
| Archive-level `.plan` files | 1 | 1 |
| Independent weather/metadata-like files identifiable by name | 0 | 0 |

The public archive organization therefore does not match the per-flight `mission.txt` / `parameters.csv` structure assumed by the frozen Phase 2B protocol. In particular, the SpeedyBee public processed release exposes 111 lap IDs rather than 120 flight-level processed units.

## 4. Mission-plan reconciliation

Both archives contain `Readme/cheste_QGroundControl.plan`. The files are byte-identical:

- SHA-256: `e5b62ca7b94947ec1c746245c7e096df84f38d1ff9719d62f3058cd116f3bb76`;
- mission items: 55;
- command composition: 53 command-16 items, one command-177 item, one command-21 item;
- geometry signature SHA-256: `9d0dd1746415f50d1b545d60df82fe812eceb55f0635c1a7ebd5b1fa1b8c6232`.

Thus the only released mission plan detected is an archive-level constant, and it is identical across the two architecture archives. It cannot supply flight-level or within-stratum mission-condition heterogeneity.

## 5. Why Phase 2B cannot proceed as preregistered

The frozen c-pKTES-Hedge design requires unit-level outcome-blind covariates before outcomes are opened. With only architecture labels and one shared mission plan, the release provides no defensible flight-level engineering condition vector for within-stratum kernel novelty, adverse-tail scoring, or sentinel selection.

The following potential substitutions are prohibited because they are realized flight outcomes rather than pre-outcome conditions:

- processed GPS trajectories or path geometry;
- realised speed, altitude, turn rate, wind, or route-tracking behaviour;
- flight duration or log size as a proxy for mission difficulty;
- flight-mode, failsafe, actuator, power, airspeed, or sensor histories;
- post-flight quality measures derived from those streams.

Flight/lap identifiers and acquisition order are labels, not engineering condition covariates, and are not introduced as a rescue feature.

Accordingly, constructing a new design frame from the released telemetry would convert IDF-DS from external validation data into development data. That would violate the Phase 2 contract.

## 6. Decision

Phase 2B is **not a performance FAIL** and **not a PASS**. It is **BLOCKED_SOURCE_STRUCTURE** before outcome opening.

This preserves the independence of the external dataset and leaves the Phase 2A result unchanged. Phase 2A remains `PASS_WITH_EXECUTION_CLARIFICATION`; no Phase 2A constant is retuned.

Phase 2B may resume only if an independently sourced, unit-linked preflight metadata package becomes available that can be matched to the intended flight population before outcome extraction. At minimum it must establish flight identity and supply defensible per-flight pre-outcome mission/configuration/environment covariates. Its identity and hashes must be frozen before telemetry values are opened.

If such metadata cannot be obtained, the scientifically correct endpoint is to report IDF-DS as an external-data limitation and, only under a new preregistered protocol, consider a different engineering dataset. The existing IDF-DS outcome streams must not be used to redesign KTES and then relabeled as independent confirmation.

## 7. Evidence identities

- `PHASE2B_STRUCTURAL_INVENTORY_v8.md`: SHA-256 `529a79767be21637a370a7cbed07d80224187778f40dae0861e52f9cb3a6d2f8`
- `phase2b_structural_inventory_manifest_v8.json`: SHA-256 `e44f89ea4751f66f5da2b3b2f8b7fd02a09b1893a011b692fc7714494143de77`
- `PHASE2B_ARCHIVE_SCHEMA_PROBE_v8.md`: SHA-256 `ceebf3af6274e1d18b36a3bebc9ce37579a02867ce9c1b8ffc6832704bf82e08`
- `phase2b_archive_schema_probe_v8.json`: SHA-256 `59881d4c41a8bfdc99ed7552d92d127415f308109f113202f5cba287d9d6c6cc`
- `PHASE2B_SOURCE_RECONCILIATION_v8.md`: SHA-256 `bd54d39aeddbb74e83943af7c9975d40d6828600ff388d8da370359bb6801930`
- `phase2b_source_reconciliation_v8.json`: SHA-256 `f7c5a9f2c279f3086ddc921d555a40d4f4807e51fdc0e1382c82339ba3529a0a`

These hashes were independently recomputed from the downloaded CI artifacts.
