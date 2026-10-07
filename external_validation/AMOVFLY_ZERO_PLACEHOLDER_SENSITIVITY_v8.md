# AMOVFLY exact-zero waypoint sensitivity v8

**Classification:** **POST-OUTCOME SENSITIVITY ONLY**  
**Confirmatory result:** unchanged

The successful confirmatory design object (SHA `a5b241f9d17be696652f30968bb1b8a0d2138087674ac371866b606e8362696b`) is read as immutable input. The exact `(0,0)` exclusion changes only the diagnostic outcome definition.

## Diagnostic population

- mean `Y10`: **0.982242987**
- `F10` rate: **0.459143969**
- mean `Y2`: **0.081689297**

## Frozen-design replay sensitivity

| Quantity | Result |
|---|---:|
| KTES−SRS profile-error mean difference | -0.000410683 |
| 95% CI | [-0.000637940, -0.000183427] |
| KTES critical-domain error | 0.033420459 |
| SRS critical-domain error | 0.064682900 |
| Split15 critical-domain error | 0.079275314 |
| KTES−better-comparator domain error | -0.031262441 |
| KTES difficult-case hit | 1.000000 |
| Split15 difficult-case hit | 1.000000 |
| All five numerical gates | PASS |

## Interpretation

This sensitivity was specified after telemetry outcome access. It tests robustness of the method comparison to the identified placeholder, but it is not a repaired confirmatory endpoint and must not replace the original AMOVFLY result.
