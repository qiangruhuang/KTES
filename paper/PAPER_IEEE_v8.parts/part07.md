The R5 confirmation contains 1000 independent finite populations, 200 under each of five discrepancy scenarios.

### A.2 Anti-UAV410

Primary external-validation evidence:

- `external_validation/PHASE2A_500_REPLAY_RESULT_v8.md`;
- `external_validation/PHASE2A_CI_EVIDENCE_v8.md`;
- `external_validation/PHASE2A_DESIGN_OBJECT_v8.json`;
- `data/anti_uav410_test_design_frame_v8.csv`;
- `data/anti_uav410_siamfc_SA_i_v8.csv`.

Classification: `PASS_WITH_EXECUTION_CLARIFICATION`.

### A.3 IDF-DS

Primary source-gate evidence:

- `external_validation/PHASE2B_PREOUTCOME_FREEZE_v8.md`;
- `external_validation/PHASE2B_SOURCE_GATE_v8.md`.

Classification: `BLOCKED_SOURCE_STRUCTURE` before telemetry outcome opening.

### A.4 AMOVFLY

Primary engineering evidence:

- `external_validation/AMOVFLY_DESIGN_FREEZE_v8.md`;
- `external_validation/AMOVFLY_ENDPOINT_PERFORMANCE_FLOOR_FREEZE_v8.md`;
- `external_validation/AMOVFLY_EXTERNAL_VALIDATION_RESULT_v8.md`;
- `external_validation/AMOVFLY_WAYPOINT_SEMANTIC_AUDIT_v8.md`;
- `external_validation/AMOVFLY_ZERO_PLACEHOLDER_SENSITIVITY_v8.md`;
- `external_validation/AMOVFLY_NUMERICAL_REPRODUCIBILITY_AUDIT_v8.md`.

Classification: `NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION`.

### A.5 Reproducibility rule

For downstream analysis, a realized unequal-probability design is identified by its immutable, hashed design object. Recalculation from source code, package versions, and seeds is not accepted as the same design unless the design-object hash matches exactly.
