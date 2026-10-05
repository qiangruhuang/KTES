# KTES — Kernel-based Test-condition Sampling for Evaluation

Canonical research repository for the KTES project.

## Current state: v8 external engineering validation

- **Phase 1 / v7 controlled evidence:** frozen after adversarial-review repair.
- **Phase 2 external engineering validation protocol:** pre-registered and frozen.
- **Anti-UAV410 evidence received:** `performance.json` audited.
- **Phase 2A result gate:** **BLOCKED**, not PASS/FAIL, because the supplied JSON does not contain the pre-registered per-sequence State Accuracy (`SA_i`) endpoint.
- No endpoint substitution, post-outcome retuning, or redesign has been performed.

The frozen Phase 2A protocol defines Anti-UAV410 test split `N=120`, frozen SiamFC system outcome, `n=40` selected sequences, and 500 paired design replays. The primary endpoint is per-sequence State Accuracy (`SA_i`). Success AUC and 20-pixel precision are secondary descriptive outputs only.

## Repository layout

- `paper/` — frozen v7 manuscript/revision/supplement/audit/handoff.
- `protocol/` — Phase 2 external-validation protocol and immutable contract.
- `external_validation/RESULT_GATE_v8.md` — current result-gate decision and evidence boundary.
- `scripts/audit_performance_json.py` — deterministic audit of the supplied Anti-UAV410 performance JSON.
- `data/performance_manifest_v8.json` — hash/schema audit for the supplied external result file.
- `REPOSITORY_MANIFEST_v8.json` — SHA-256 inventory of the research snapshot.

## External evidence file

The supplied `performance.json` is not duplicated in Git history. It is identified by:

- size: `19,063,146` bytes
- SHA-256: `7861cded4d79dfd37ce251e8167f81ce145ea8f9ed68d8dd1f4b252ca33d82a0`

The file contains the expected 120 SiamFC `seq_wise` records, but only Success/Precision-derived fields. It does not contain `SA_i`/state-accuracy values, so it cannot close the frozen Phase 2A primary gate.

## Reproduce the evidence audit

```bash
python scripts/audit_performance_json.py /path/to/performance.json
```

Expected current status: `RESULT GATE BLOCKED`.

To close Phase 2A without changing the protocol, provide either:

1. a 120-row sequence-level State Accuracy export for the same frozen SiamFC test run; or
2. the 120 SiamFC tracker-result files plus Anti-UAV410 test annotations required by the official SA evaluator.

## Research integrity rule

External outcomes may not be used to re-select c-pKTES-Hedge/R3/R5 constants and then be reused as confirmation. A failed external gate is reported as an external-validity boundary.
