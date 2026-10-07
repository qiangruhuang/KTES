# AMOVFLY external engineering validation result v8

**Numerical result gate:** **PASS**  
**Final classification:** **NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION**

Population truth under the frozen literal 10 m waypoint-attainment rule: mean Y=0.946105; flight failure rate=1.000000. Strict 2 m sensitivity mean Y=0.079256.

## Confirmatory guardrails

| Gate | Result |
|---|---|
| G1 positive pi / no sampling failure | PASS |
| G2 probability-remainder ESS | PASS |
| G3 profile error vs SRS <= +0.01 | PASS; paired mean diff -0.000759, 95% CI [-0.001164, -0.000353] |
| G4 critical-domain error <= better comparator +0.02 | PASS; delta -0.032437 |
| G5 difficult-hit >= Split15 -0.10 | PASS; delta 0.000000 |

The primary endpoint, 10 m external reference radius, 2 m sensitivity, population, design, comparators and numerical guardrails were frozen before telemetry outcome values were opened. The 10 m threshold is an external PX4-default reference and is not claimed to be AMOVFLY's historical configured acceptance radius.

## Post-outcome semantic limitation

A subsequent read-only semantic audit identified exact `(0,0)` `aim_lat/aim_long` episodes in all 257 flights. All 378 episodes with minimum actual-to-aim distance greater than 100 km were exactly these `(0,0)` episodes; no non-zero target generated a >100 km episode. Under the frozen literal parser, those placeholders make `F10=I(any episode >10m)` degenerate (`F10=1` for every flight) and shift the bounded primary `Y10` endpoint materially.

Excluding exact `(0,0)` episodes only as a **post-outcome diagnostic** changes population mean `Y10` from 0.946105 to 0.982243 and `F10` from 1.000 to 0.459. This diagnostic does not alter or repair the confirmatory endpoint.

## Frozen-design robustness sensitivity

A separately labelled post-outcome sensitivity loaded the exact immutable confirmatory design object (`SHA-256 a5b241f9d17be696652f30968bb1b8a0d2138087674ac371866b606e8362696b`) rather than regenerating inclusion probabilities. After excluding exact `(0,0)` episodes only, all five numerical comparison gates remained satisfied:

- KTES−SRS profile-error difference: **−0.000410683**, 95% CI **[−0.000637940, −0.000183427]**;
- KTES critical-domain error: **0.033420459** vs SRS **0.064682900** and Split15 **0.079275314**;
- difficult-case hit: KTES **1.000**, Split15 **1.000**.

This supports robustness of the **method-comparison conclusion** to the identified placeholder. It does not convert the diagnostic endpoint into an independent confirmation and does not rescue failure-probability inference from the original degenerate `F10` result.

## Claim boundary

AMOVFLY supports the claim that the frozen KTES probability-preserving design retained favorable sampling/inference comparisons on an independent real-flight dataset under the executed numerical gate. It does **not** support a clean claim that the frozen literal waypoint endpoint is an uncontaminated engineering performance measure, and it does **not** support failure-rate qualification from `F10`.

See:

- `AMOVFLY_WAYPOINT_SEMANTIC_AUDIT_v8.md`;
- `AMOVFLY_ZERO_PLACEHOLDER_SENSITIVITY_v8.md`;
- `AMOVFLY_NUMERICAL_REPRODUCIBILITY_AUDIT_v8.md`;
- `results/AMOVFLY_EVIDENCE_MANIFEST_v8.json`.
