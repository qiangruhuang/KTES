# Phase 2A design freeze v8

**Date:** 2026-10-05  
**Protocol:** KTES Phase 2 External Validation Protocol v1.0  
**Status:** **FRAME FROZEN; SAMPLING-ENGINE INSTANTIATION FAIL-CLOSED PENDING SOURCE-PROVENANCE RECOVERY**

## Frozen finite-population frame

The Phase 2A finite population is the official Anti-UAV410 test split, N=120 sequences. The outcome-blind design frame is reconstructed only from the official repository pinned at commit `8a8eb04d976e9386b7c9c3ada5c85e5086013d52`. No SiamFC performance field or State Accuracy value is read in this reconstruction.

The feature schema follows the pre-registered protocol: TC, OV, SV, FM, OC, DBC, Tiny, Small, Medium, Normal, and log sequence length. Sequence length is obtained from the number of frame annotations in the official `annos/test/<sequence>.txt` file. The auxiliary risk score remains exactly

\[
\widehat r_i=\tfrac12\overline A_i+\tfrac12 S_i,
\]

with Tiny=1, Small=2/3, Medium=1/3, Normal=0 and the most adverse active size class used for stratification.

The frozen stratum counts are Tiny 33, Small 54, Medium 29, Normal 4. Applying the pre-registered n=40 largest-remainder proportional allocation with a minimum of two observations per non-empty stratum gives Tiny 11, Small 17, Medium 10, Normal 2.

## Immutable sampling contract

The Phase 1.2R-5 contract remains unchanged: three certainty sentinels (one pure-novelty and two risk-aware), 37 positive-inclusion-probability units, 80% kernel novelty + 20% compound adverse-tail score, rho=0.20, lambda=3, minimum-probability fraction 0.35, Local Cube spreading/balance, stratum-wise Hájek model-assisted residual correction, max(GS,PWR) UQ, and the frozen R3 calibration constants.

## Fail-closed provenance rule

The project handoff identifies the original executable implementation as `src/phase12r/r5_designs.py` and associated R5 scripts. Those source files are not readable from the currently accessible project snapshot: only their historical paths are recoverable. The textual contract does not uniquely specify the kernel-novelty operator or the exact Local Cube numerical implementation. Consequently, this v8 freeze does **not** create a replacement implementation and does not assign new sentinel indices or inclusion probabilities from a reconstructed algorithm.

This is a reproducibility control, not a methodological revision. The frame, strata, allocation, auxiliary-risk map, seed block (`20261001`–`20261500`), comparator definitions, and all external-validation guardrails are frozen. The remaining sampling-engine object will be instantiated only from the recovered frozen R5 source or a byte-identical archived implementation.

## Outcome-access chronology

The Phase 2 protocol was frozen on 2026-09-29. The supplied `performance.json` was inspected before this design-frame instantiation and exposed sequence-level Success/Precision outputs, but it did not expose the primary `SA_i` endpoint. No method constant, covariate definition, stratum rule, allocation rule, comparator, endpoint, or guardrail was changed after that inspection. This chronology is retained explicitly because Phase 2A should not be described as a pristine pre-outcome design instantiation; rather, it is an instantiation of a protocol that was already frozen before secondary-outcome access.
