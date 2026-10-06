# Phase 2A execution audit v8

**Updated:** 2026-10-06  
**Overall state:** **500-REPLAY EXECUTION COMPLETE; ALL NUMERICAL GUARDRAILS PASS; CLASSIFICATION = PASS_WITH_EXECUTION_CLARIFICATION**

## Audit results

1. **Protocol integrity — PASS.** The 2026-09-29 Phase 2 protocol and immutable c-pKTES-Hedge contract remain unchanged.
2. **External frame identity — PASS.** Official Anti-UAV410 test population `N=120`, pinned to repository commit `8a8eb04d976e9386b7c9c3ada5c85e5086013d52`.
3. **Outcome-blind frame — PASS.** Frame SHA-256 `c360494499e2cc9d09c62876bd3c45ab9f5be6982174b172224d12e62e6c9f69`; Tiny/Small/Medium/Normal counts `33/54/29/4`; n=40 allocation `11/17/10/2`.
4. **Primary State Accuracy outcome — PASS.** Exactly 120 `SA_i` values under official Anti-UAV410 State Accuracy semantics; SHA-256 `4049ca9c83128e2a2c8e244c30597a95431f1489efb2f69cda536c8e4873a886`.
5. **Population truth freeze — PASS.** Equal-sequence population mean SA `0.351505497767269`; bottom-10% set contains exactly 12 sequences with cutoff `0.0281723445330009` and no tie.
6. **Frozen R5 source provenance — PASS.** Original R5 source was recovered from the 2026-09-29 handoff lineage. Required files and runtime dependencies have historical SHA-256 records and are committed as hash-verified source under `vendor/r5_engine_recovered_v8/`.
7. **Historical implementation regression — PASS.** Fifty historical tasks, 150 method rows and 3,450 numeric cells were checked against the frozen R5 confirmation fixture; maximum absolute numeric difference was `7.105427357601002e-15` at tolerance `1e-12`.
8. **Design-object instantiation — PASS WITH DISCLOSURE.** Design SHA-256 `2a686908e42a1134578c07eecce9ca3be8336ff08c37c8d3622ff2a2855184dc`. Certainty sentinels are `20190926_111509_1_9`, `3700000000002_162623_1`, and `new6_train_newfix`. One non-sentinel remainder unit (`20190925_124000_1_10`) is naturally capped at `pi=1` by the frozen inclusion-probability construction and remains part of the 37-unit probability-remainder identity.
9. **500 paired replays — PASS.** Seeds `20261001..20261500`; 500 realizations per method and 1,500 method-replay rows completed without sampling failure under the final audited implementation.
10. **Independent CI reproduction — PASS.** GitHub Actions run `37422551437`, job `112134913235`, at commit `44357d40de298d4a3b19e6dfe629d43464865a88` independently passed runtime SHA checks, static compilation, input SHA checks, design freeze, all 500 replays, evidence hashing and artifact upload.
11. **Parameter retuning — PASS.** No change to rho=.20, lambda=3, sentinel portfolio/count, probability floor, Local Cube rule, R3 UQ constants, endpoint, n=40 allocation, replay seed block or guardrail thresholds.
12. **Endpoint substitution — PASS.** Success AUC/precision remain secondary only; primary endpoint is `SA_i`.

## Numerical gate

All preregistered numerical guardrails pass:

- positive inclusion probabilities and no replay sampling failures: **PASS**;
- KTES 37-unit probability-remainder ESS median `33.1218` >= `18.5`: **PASS**;
- KTES remainder ESS 5th percentile `32.5987` >= `12`: **PASS**;
- profile-error difference KTES−SRS `+0.00404` <= non-inferiority bound `+0.01`: **PASS**;
- critical-domain-error difference versus the better baseline (SRS) `−0.01018` <= `+0.02`: **PASS**;
- difficult-case hit difference KTES−Split15 `0.000` >= `−0.10`: **PASS**.

The result should not be simplified to “KTES is better on every endpoint.” KTES has higher mean profile error than stratified SRS (`0.03007` versus `0.02603`), and the paired difference is positive (`+0.00404`, 95% CI `0.00137` to `0.00671`). It passes because the protocol specified a `+0.01` non-inferiority guardrail. In contrast, mean six-domain critical error is lower for KTES (`0.04893`) than SRS (`0.05911`), paired difference `−0.01018` (95% CI `−0.01230` to `−0.00806`). Difficult-case hit is 100% for KTES and Split15 and 99.6% for SRS.

## Execution clarifications that prevent a pristine preregistered-PASS label

### 1. Split15 numerical adapter

The frozen protocol specified `15 deterministic geometry/difficulty + 25 probability-audit` but did not uniquely specify the four-stratum external numerical mapping. The executed adapter inherits the historical deterministic geometry rule as `3 per Phase 2A size stratum + 3 global`, then allocates the disjoint 25-unit probability audit over the remaining population by the frozen largest-remainder/minimum-2 rule. The resulting Tiny/Small/Medium/Normal audit allocation is `7/11/6/1`.

This mapping is outcome-blind, but its exact numerical instantiation occurred after `SA_i` recovery. Therefore Split15-dependent guardrails are retained with an explicit execution-order limitation.

### 2. Critical-domain estimator

The protocol required error over six challenge domains but did not uniquely state how a finite-domain mean should be estimated when a replay contains zero sampled members of a rare challenge domain. A strict replay exposed this possibility for OC. The final implementation uses the design-based Horvitz-Thompson finite-domain mean with the known outcome-blind full-domain denominator. This keeps the domain endpoint defined for every replay and all methods.

This estimator clarification was made after `SA_i` recovery and is therefore disclosed as an execution clarification rather than represented as pristine preregistration.

Neither clarification alters c-pKTES-Hedge selection constants or any frozen gate threshold.

## Evidence freeze

Canonical evidence:

- `external_validation/PHASE2A_500_REPLAY_RESULT_v8.md`;
- `external_validation/phase2a_result_gate_v8.json`;
- `results/phase2a_500_replay_summary_v8.csv`;
- `results/phase2a_500_replay_paired_v8.csv`;
- `external_validation/PHASE2A_CI_EVIDENCE_v8.md`.

The CI-generated raw 1,500-row replay matrix has SHA-256 `423b6a96652a8cb1f19adb85762c7d90d4e0ded2ee9286057452460635d3866d` and is retained in the immutable CI artifact; it can be regenerated deterministically from the committed frozen inputs and analysis workflow.

## Current interpretation

Phase 2A is closed as **PASS_WITH_EXECUTION_CLARIFICATION**. The result supports structural transport of the frozen probability-preserving sampling logic to this real task-effectiveness benchmark under the specified non-inferiority/tail-coverage guardrails. It does not establish superiority on profile estimation, deployment-frequency representativeness, live-weapon validity or mission-level safety certification.

Phase 2B may now move from queued status to **pre-outcome engineering-contract freeze**. No IDF-DS outcome should be opened until its eligibility rule, primary performance floor, exact failure definition and column map are frozen.
