# KTES v7 Handoff

## Frozen state

The adversarial-review repair cycle is complete at the controlled-research level. The current source of truth is `PAPER_IEEE.md`, supported by `RESEARCH_REVISION_v7.md`, `SUPPLEMENTARY_RESULTS_v7.md`, and the curated `replication_v7/` subset.

Frozen method:

- exact \(M=50\) conditions;
- \(n=10\) trials/condition;
- random within-stratum selection;
- target-reference kernel alignment;
- frozen \(\eta=0.6\);
- fail-closed support check with \(m_{min}=2\);
- conditional Bayes-Kish interval as the primary pseudo-posterior construction.

## Main revised conclusions

1. Frozen KTES lowers MARE by 40.5–54.8% versus SRS on the four controlled surfaces; paired mean and median-bootstrap CIs favour KTES in all four.
2. The public benchmark effect is selection-variability control and is response-surface dependent; SECOM reverses under RF truth.
3. Source-pool support failure is a first-order applicability boundary. Severe negative shift fails support in 95% of AI4I/SECOM pools and 40% of Steel pools.
4. KTES versus post-hoc importance weighting is dataset-dependent; the old direction-only method rule is retired.
5. The pre-test gain proxies are weak after freezing the actual protocol and are no longer used as a go/no-go rule.
6. Bayes-Kish is a conditional calibrated engineering construction, not a general Bayesian coverage result.
7. Lower MARE does not imply stronger qualification decisions at \(n=10\); most low-probability cases are inconclusive.

## Deprecated evidence

Do not use the legacy single-pool biased table, old phase diagram, or old pool-bias scan for headline claims. They remain only for provenance.

## Remaining gate

The next substantive study is an independent engineering validation with a pre-specified target mission profile, externally generated candidate pool, frozen algorithm and thresholds, and equal-budget comparison to SRS and direct reweighting. No further synthetic benchmark should be added before this gate.

## Document gate

This handoff remains in Markdown. DOCX/PDF generation should begin only after the user reviews and explicitly approves the v7 research content.
