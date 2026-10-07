# AMOVFLY waypoint semantic audit v8

**Classification:** **POST-OUTCOME DIAGNOSTIC ONLY**  
**Frozen confirmatory result:** unchanged

## Finding

- Frozen population: 257 flights, 13849 waypoint episodes.
- Flights containing at least one exact `(0,0)` aim waypoint episode: **257**.
- Exact `(0,0)` episodes: **378**.
- Episodes with minimum actual-to-aim distance >100 km: **378**.
- Of those extreme episodes, exact `(0,0)` episodes account for **378**; non-zero targets account for **0**.
- Fraction of >100 km episodes explained by exact zero: **1.0**.

## Frozen literal endpoint

- mean `Y10`: **0.946105233**.
- `F10` rate: **1.000000000**.

## Diagnostic exact-zero exclusion

Excluding exact `(0,0)` episodes only, without changing any other episode rule:

- mean `Y10`: **0.982242987**;
- `F10` rate: **0.459143969**;
- mean per-flight change in `Y10`: **0.036137754**;
- flights whose `Y10` changes: **257 / 257**.

## Research-integrity interpretation

This audit was defined after the frozen telemetry outcome was opened. It is therefore a semantic diagnostic, not a repaired confirmatory endpoint. The frozen AMOVFLY external-validation result must remain reported exactly as executed. The literal failure indicator `F10=I(any waypoint episode exceeds 10 m)` is uninformative under the frozen parsing rule because every flight contains at least one exact `(0,0)` placeholder episode. The primary bounded `Y10` endpoint is also shifted upward by about 0.036 on average when those placeholders are excluded diagnostically.

The appropriate response is to narrow the engineering interpretation and report a separately labelled post-outcome sensitivity using the unchanged frozen design. That sensitivity may assess robustness of the method comparison, but it cannot replace the original endpoint or be relabelled as independent confirmation.