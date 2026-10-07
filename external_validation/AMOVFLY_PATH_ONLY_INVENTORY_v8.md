# AMOVFLY autonomous-flight pre-outcome path inventory v8

**Gate:** **PASS_AUTONOMOUS_PATH_FRAME**

Only pinned Git-tree metadata were read. No `Flight_info.csv` row and no raw/ready telemetry value was opened.

- source commit: `67069ed00ddbebd62b71aa9bb1272415e9b15ff8`
- unique autonomous ready-blob units: 257
- excluded Random/manual paths: 14
- alias groups collapsed: 6
- unresolved alias conflicts: 0
- path parse failures: 0
- condition parse failures: 0

## Scenario strata and n=40 allocation

| Stratum | N | n |
|---|---:|---:|
| FAFS | 33 | 6 |
| FAVS | 165 | 23 |
| VAFS | 32 | 6 |
| VAVS | 27 | 5 |

## Frozen design-side semantics

Kernel geometry uses scenario/UAV identity, payload, explicitly encoded altitude/speed parameters, structural altitude availability, and altitude/speed variability flags. Missing variable-altitude values are not imputed from telemetry.

Auxiliary risk is `0.5*variability_severity + 0.5*payload_severity`. Speed and altitude magnitudes are not assigned an adverse direction without independent engineering justification.

`Random` is excluded because the source README describes manual control. Multi-UAV records are not added without a separately frozen one-flight-one-outcome map.

A PASS authorizes R5 design-object instantiation only; telemetry outcomes remain closed.
