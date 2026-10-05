# KTES v7 Consistency Audit

The audit checks the Markdown manuscript against the frozen machine-readable evidence.

## Checks

- PASS — No bibliography placeholders
- PASS — Frozen headline MARE range present
- PASS — Frozen win-rate range present
- PASS — Deprecated 38–47 headline absent
- PASS — Deprecated 64–74 headline absent
- PASS — Weak-proxy correlations present
- PASS — Support-failure rates present
- PASS — Threshold endpoint section present
- PASS — Independent engineering gate present
- PASS — Contract exact budget
- PASS — Contract uniform reference
- PASS — Contract fail closed
- PASS — All four paired mean CIs favour KTES
- PASS — All four median bootstrap CIs favour KTES
- PASS — Outer support failure AI4I -1 = 95%
- PASS — Outer support failure Steel -1 = 40%
- PASS — Outer support failure SECOM -1 = 95%
- PASS — SECOM RF truth reverses (red_rf=-18.350%)

Overall: **PASS** (18/18 checks).

## Frozen evidence SHA-256 manifest

| File | SHA-256 |
|---|---|
| `ktes.py` | `81ca5e6a9c09892f6b5b9a2140eed461f47a0f3d25ec6c1b6065c36177023ebd` |
| `validate_contracts.py` | `5dd4b9847cf8b93600f305d6c88a7c10e79e2f9f84d755c365b3e1837bffad6c` |
| `validate_v2_adaptive.py` | `ef4c8e1b5bf324ad74b61e8cde3445eb2108deb8499df696bff486e0b96c3455` |
| `heldout_eta.py` | `af63bf3a1f72c05de56e5ff516649dcbe43c1a3109194cbc21a02c1b7a5d175f` |
| `headline_stats.py` | `6546e41a7ae31a820892c0a16e054632ef768393eedd947a13ebebcf7a23a635` |
| `calibrate_intervals.py` | `b3a7a1106d7286f06fc48af41c2052738212f10f08d240c17b739d91ea1ba04b` |
| `scan_phase_diagram_frozen.py` | `9bb6fd7359bf4fc84cc58ec9b697dae032c3d95bb76649a772e9ca0e1f2a523a` |
| `validate_pool_outer.py` | `f7e597463e6d852189751a39069950b288ea2acc1ace491d670cbc386a76d3b0` |
| `coverage_vs_bias.py` | `5d8c0fa8754aded53e5ba32fb3c014db68d4e7dfbe3e3810d99c0581ce4c4709` |
| `truth_sensitivity.py` | `8621eb98c66ba8241e66a4f7b0d1c8583df97dfa4f8c58ffd554b1987cc8a4de` |
| `validate_threshold_decision.py` | `2e06ece1e006134169e68fa232b8171cc3790bcefb34fdec9597a85916c891f5` |
| `validate_contracts_results.json` | `de71e95dcefff445a7f244b44f79713d2863a7528471f331fcab79eba50d08f2` |
| `validate_v2_adaptive_results.json` | `7f9a82b067316b180786e5486d8f472404ea6d8c513009774dfae6b532ec92ba` |
| `heldout_eta_results.json` | `bed8906768f8785905da341f9140aae088f4dcb49fe430444e2e4b7c2cf0bf03` |
| `headline_paired_stats.json` | `99b9363721b6fb88519525b6db00173b566fad7409c49da0c51a05d86a8a3ec7` |
| `calibrate_intervals_results.json` | `3ad5468159ed1b305e2eb68d246eab4edb0dac4ee408e8ba8c7b2a15f50f1766` |
| `scan_phase_diagram_frozen_results.json` | `77b8dfe6c0db3448ebbedae8c2af1419b7d1abeef68a536cc67c663a32d104b0` |
| `pool_outer_results.json` | `5df446ceb2cfb48384feffbaeb98a6c80a20748d52093bf052c7d2fefe4f2edd` |
| `coverage_vs_bias_results.json` | `afa09838d6589cd09da195ee6d7118a2c490f2b26a135b81153fb20f58aac453` |
| `truth_sensitivity_results.json` | `8522521828a4a3a48100da96fc05464d80ffb7749ab33fdb3b89d387a35c26ce` |
| `threshold_decision_results.json` | `11e7ef8c8b1ba8a6ec39c11ef32a0d7c818efb47e7c5e442f04453c013bf2133` |
