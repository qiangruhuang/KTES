# KTES v8 — External Engineering Validation Result Gate

**Updated:** 2026-10-06  
**Phase 2A status:** **PASS_WITH_EXECUTION_CLARIFICATION**  
**Protocol status:** frozen; no post-outcome retuning or endpoint substitution performed.

## 1. Frozen Phase 2A gate

The Phase 2A pilot evaluates the official Anti-UAV410 test split (`N=120`) with the official SiamFC default tracker, primary per-sequence State Accuracy outcome `Y_i=SA_i`, n=40 selected sequences and 500 paired design replays using seeds `20261001..20261500`.

The frozen c-pKTES-Hedge design retains 3 NRR certainty sentinels plus a 37-unit probability remainder, rho=.20, lambda=3, minimum-probability fraction=.35, 80/20 novelty–compound-tail PPS, Local Cube spreading, stratum-wise Hájek profile estimation and the frozen R3 UQ machinery.

## 2. Frozen evidence identities

Outcome-blind frame:

- N `120`;
- SHA-256 `c360494499e2cc9d09c62876bd3c45ab9f5be6982174b172224d12e62e6c9f69`;
- Tiny/Small/Medium/Normal counts `33/54/29/4`;
- n=40 allocation `11/17/10/2`.

Primary State Accuracy artifact:

- `data/anti_uav410_siamfc_SA_i_v8.csv`;
- N `120`;
- SHA-256 `4049ca9c83128e2a2c8e244c30597a95431f1489efb2f69cda536c8e4873a886`;
- population mean SA `0.351505497767269`;
- bottom-10% difficult set `n=12`, cutoff `0.0281723445330009`, no tie.

The supplied `performance.json` remains secondary evidence only. It does not contain sequence-level State Accuracy and was not substituted for the primary endpoint.

## 3. Sampling-engine provenance — CLOSED

The earlier fail-closed source-provenance blocker is resolved. The original Phase 1.2R-5 source lineage was recovered from the 2026-09-29 handoff and linked to the historical Phase 1.2R dependency modules. Hash records are stored in `data/r5_source_recovery_manifest_v8.json` and the exact Phase 2A runtime source is committed under `vendor/r5_engine_recovered_v8/` with SHA-256 checks.

A historical behavior regression compared the recovered implementation with the frozen R5 confirmation fixture over 50 tasks, 150 method rows and 3,450 numeric cells. Maximum absolute difference was `7.105427357601002e-15` against tolerance `1e-12`.

## 4. Independent 500-replay execution — CLOSED

GitHub Actions run `37422551437`, job `112134913235`, at commit `44357d40de298d4a3b19e6dfe629d43464865a88` independently completed all fail-closed checks and 500 paired replays. The design-object SHA-256 is `2a686908e42a1134578c07eecce9ca3be8336ff08c37c8d3622ff2a2855184dc`.

The CI artifact was independently downloaded and rehashed. Core output hashes match the runner log exactly; see `external_validation/PHASE2A_CI_EVIDENCE_v8.md`.

## 5. Phase 2A results

Mean performance across 500 replays:

| Method | Profile error | Critical-domain error | Difficult-case hit | Probability-component ESS median |
|---|---:|---:|---:|---:|
| c-pKTES-Hedge | 0.03007 | **0.04893** | 1.000 | 33.12 |
| Stratified-SRS | **0.02603** | 0.05911 | 0.996 | 39.71 |
| Split15+Audit25 | 0.03049 | 0.06109 | 1.000 | 24.27 |

Paired c-pKTES-Hedge minus SRS profile error is `+0.00404` (95% CI `0.00137` to `0.00671`). This means c-pKTES-Hedge is worse on the profile-error endpoint in this benchmark, but the difference remains below the preregistered non-inferiority bound of `+0.01`.

Paired critical-domain error versus SRS is `−0.01018` (95% CI `−0.01230` to `−0.00806`), favoring c-pKTES-Hedge. Difficult-case hit is 100% for c-pKTES-Hedge and Split15+Audit25 and 99.6% for SRS.

## 6. Guardrail decision

All numerical guardrails pass:

1. no sampling failure and all non-sentinel units retain positive inclusion probability — **PASS**;
2. 37-unit KTES remainder ESS median `33.12 >= 18.5`, p05 `32.60 >= 12` — **PASS**;
3. profile-error difference KTES−SRS `+0.00404 <= +0.01` — **PASS**;
4. critical-domain-error difference versus the better baseline (SRS) `−0.01018 <= +0.02` — **PASS**;
5. difficult-case-hit difference KTES−Split15 `0.00 >= −0.10` — **PASS**.

Machine-readable gate: `external_validation/phase2a_result_gate_v8.json`.

## 7. Why the result is PASS_WITH_EXECUTION_CLARIFICATION

Two pre-registered concepts were not numerically unique enough for an unqualified PASS label:

- **Split-style comparator:** the protocol fixed `15 deterministic geometry/difficulty + 25 probability-audit` but not the exact four-stratum mapping. The executed outcome-blind adapter uses the historical 3×4+3 geometry rule and allocates the disjoint audit remainder `7/11/6/1` after deterministic removal. This was instantiated after `SA_i` recovery but before replay results.
- **Critical-domain estimator:** the protocol fixed six challenge-domain error but did not specify the finite-domain estimator when a rare domain receives zero sampled sequences. The final implementation uses the Horvitz-Thompson finite-domain mean with known outcome-blind domain denominator, which remains defined for every replay.

These are execution clarifications rather than changes to c-pKTES-Hedge. No selection constant, primary endpoint, stratum/allocation rule, seed block or gate threshold was changed.

## 8. Academic interpretation

Phase 2A provides external structural support for the frozen probability-preserving sampling logic under the prespecified guardrails, but it does **not** show uniform superiority: SRS has lower profile-estimation error, while c-pKTES-Hedge has lower critical-domain error and retains high difficult-case coverage with acceptable weight stability.

The claim boundary remains narrow. Phase 2A does not establish deployment-frequency representativeness, live-weapon validity or mission-level safety certification. The next allowed step is Phase 2B pre-outcome engineering-contract freeze for IDF-DS; Phase 2A must not be retuned and reused as a new development set.
