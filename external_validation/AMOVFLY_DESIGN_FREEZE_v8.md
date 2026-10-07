# AMOVFLY frozen pre-outcome design object v8

**Status:** **FROZEN_PREOUTCOME_DESIGN**  
**Telemetry outcome access:** **CLOSED**

Finite population: N=257 autonomous-flight units after byte-identical alias collapse. Strata/allocation: FAFS 33/6, FAVS 165/23, VAFS 32/6, VAVS 27/5.

The recovered R5 seed lineage is inherited exactly: BASE=20261115, RFF=20261170, novelty-anchor seed=20261192. No seed is selected from AMOVFLY outcomes.

The three NRR certainty sentinels are:
- `VAVS/VAVS/UavR_P400VarAVarS8_6.csv` (unit `readyblob:ff228d4d4c59843e9add5006c070168a49620f4c`)
- `VAFS/VAFS/UavY_P400VarAS4_5.csv` (unit `readyblob:2b9304fc26cdc28abef48703f39d345dbd0e055a`)
- `FAVS/FAVS/UavG_P200A40VarS2_3.csv` (unit `readyblob:d521107a13b0eae6ff335ee8b34f3ba1aff5df9d`)

All 254 non-sentinel units retain positive first-order inclusion probability. The probability remainder contains 37 selected units per replay.

## Outcome-blind 500-replay audit

- sampling failures: 0
- probability-remainder ESS median: 35.224436
- probability-remainder ESS 5th percentile: 34.992990
- minimum selected positive pi: 0.097308
- median Local-Cube balance error: 0.272734

## Comparator freeze

Stratified SRS uses the same 6/23/6/5 allocation. Split15+Audit25 inherits the already-used Phase2A numerical adapter: 3 deterministic geometry points per stratum plus 3 global geometry points; the remaining 25 audit slots use largest-remainder allocation with minimum two per stratum over the non-deterministic remainder. Its audit allocation is [4, 13, 4, 4].

No flight performance value, `Flight_info.csv` row, raw telemetry value, or ready-data CSV value was read to construct this object. The next gate is the independent engineering endpoint/performance-floor freeze; telemetry must remain closed until that gate is persisted and hashed.

## Integrity anchors

- AMOVFLY path-frame SHA256: `92a6d63eb75a0eee58e9d310da9b140517e2dffd2c6f48986fd21b40c8b12c85`
- path-only CI artifact SHA256 digest: `8c88b8b39f1360d48f3c1864f52e8292066bf7f21f9ac5c1e8e16c07fe669d47`
- local full design-object SHA256: `a5b241f9d17be696652f30968bb1b8a0d2138087674ac371866b606e8362696b`
- design-side 500-replay CSV SHA256: `c3d0433523eadb943a6aa6ff4a9867273d1e36826fe479f75281089fa8c666ec`
