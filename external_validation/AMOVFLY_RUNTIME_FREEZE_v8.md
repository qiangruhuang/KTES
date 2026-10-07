# AMOVFLY design-runtime freeze v8

**Status:** **FROZEN BEFORE TELEMETRY OUTCOME ACCESS**

The AMOVFLY pre-outcome design object with SHA256 `a5b241f9d17be696652f30968bb1b8a0d2138087674ac371866b606e8362696b` was generated and independently rebuilt locally under the following numerical runtime:

- Python 3.13.5
- NumPy 2.3.5
- pandas 2.2.3
- SciPy 1.17.0
- requests 2.32.5

This runtime is now part of the execution provenance for the frozen external-validation design.

## Why this freeze was necessary

The first GitHub Actions execution used Python 3.12.14 / NumPy 2.3.3 / pandas 2.3.3 / SciPy 1.16.2 / requests 2.32.5. It stopped at the design-object SHA check before the schema gate and before any AMOVFLY telemetry value was opened.

A diagnostic rerun preserved the rebuilt design object and again stopped before the schema gate. Comparison with the frozen object showed:

- identical source finite-population frame SHA;
- identical bandwidth;
- identical standardization means and standard deviations;
- identical three certainty sentinel identities;
- identical Split15 deterministic identities and audit allocation;
- but non-identical c-pKTES first-order inclusion probabilities for the 254 non-sentinel units, with maximum absolute difference approximately 0.01084, attributable to numerical-runtime-dependent random-anchor novelty calculations at N=257.

Because the inclusion probabilities are part of the frozen probability design, this discrepancy is substantive for exact reproducibility and must not be accepted through a loose numerical tolerance.

## Execution rule

The confirmatory AMOVFLY run must use the runtime above and must reproduce the complete frozen design object byte-for-byte before the schema gate is allowed to run. If the design SHA still differs, execution stops fail-closed and telemetry remains unopened.

No method constant, seed, sentinel identity, covariate definition, endpoint, threshold, comparator, allocation, or guardrail is changed by this runtime freeze. This is a reproducibility lock on the already-frozen design realization.
