# AMOVFLY external engineering validation result v8

**Result gate:** **PASS**

Population truth under the frozen 10 m waypoint-attainment reference: mean Y=0.946105; flight failure rate=1.000000. Strict 2 m sensitivity mean Y=0.079256.

## Guardrails

| Gate | Result |
|---|---|
| G1 positive pi / no sampling failure | PASS |
| G2 probability-remainder ESS | PASS |
| G3 profile error vs SRS <= +0.01 | PASS; paired mean diff -0.000759, 95% CI [-0.001164, -0.000353] |
| G4 critical-domain error <= better comparator +0.02 | PASS; delta -0.032437 |
| G5 difficult-hit >= Split15 -0.10 | PASS; delta 0.000000 |

The primary endpoint, 10 m external reference radius, 2 m sensitivity, population, design, comparators, and numerical guardrails were all frozen before telemetry outcome values were opened. The 10 m threshold is an external PX4-default reference and is not claimed to be AMOVFLY's historical configured acceptance radius.

## Post-outcome semantic limitation

A subsequent read-only semantic audit identified exact `(0,0)` `aim_lat/aim_long` episodes in all 257 flights. All 378 episodes with minimum actual-to-aim distance greater than 100 km were exactly these `(0,0)` episodes. This does not alter the executed confirmatory result above, but it materially limits its engineering interpretation and makes the literal `F10=I(any episode >10m)` endpoint degenerate (`F10=1` for every flight). See `AMOVFLY_WAYPOINT_SEMANTIC_AUDIT_v8.md` and the separately labelled post-outcome sensitivity analysis.