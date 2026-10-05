# KTES v7 Supplementary Results — Frozen Evidence Tables

This supplement records the numerical evidence used by `PAPER_IEEE.md` and `RESEARCH_REVISION_v7.md`. It is intentionally limited to the post-review frozen protocol and excludes legacy exploratory scans from headline inference.

## S1. Frozen main configuration

- selected conditions: \(M=50\), exact for KTES and SRS;
- trials per condition: \(n=10\);
- KTES ESS target: \(\eta=0.6\);
- main paired selection seeds: 50;
- candidate-support floor: \(m_{\min}=2\) for every target-positive stratum;
- support failure: fail closed;
- benchmark target reference: benchmark population itself;
- induced-shift target reference: full unlabeled reference frame under \(\pi\).

## S2. Main paired statistics

| Dataset | MARE SRS | MARE KTES | Reduction | Win | Mean difference [95% CI] | Wilcoxon p | Sign p | Median [bootstrap 95% CI] |
|---|---:|---:|---:|---:|---|---:|---:|---|
| AI4I | 0.142126 | 0.071304 | 49.83% | 0.66 | −0.070822 [−0.113281, −0.028362] | 0.00261 | 0.03284 | −0.055544 [−0.104240, −0.008890] |
| Steel | 0.057255 | 0.025857 | 54.84% | 0.68 | −0.031398 [−0.047527, −0.015269] | 0.000178 | 0.01535 | −0.025147 [−0.047794, −0.008902] |
| SECOM | 0.036338 | 0.021619 | 40.51% | 0.66 | −0.014720 [−0.022771, −0.006668] | 0.000915 | 0.03284 | −0.011312 [−0.023555, −0.001742] |
| Ballistic | 0.085135 | 0.043971 | 48.35% | 0.72 | −0.041164 [−0.061451, −0.020878] | 0.000311 | 0.00260 | −0.028378 [−0.063139, −0.006127] |

## S3. Frozen adaptive-weight behaviour

| Dataset | mean activated \(\tau\) | realized local \(N_{eff}/m\) | global KTES \(N_{eff}\) | KTES/SRS RMSE |
|---|---:|---:|---:|---:|
| AI4I | 0.000595 | 0.74395 | 32.15 | 1.019 |
| Steel | 0.001450 | 0.79355 | 31.11 | 0.567 |
| SECOM | 0.000038 | 0.80285 | 32.23 | 1.202 |
| Ballistic | 0.000232 | 0.81727 | 35.39 | 1.153 |

## S4. Contract tests

`validate_contracts_results.json` reports:

- `exact_budget = true`;
- `uniform_reference_contract = true`;
- `support_fail_closed = true`.

Default vs explicit-uniform target-reference maximum \(|\Delta\lambda|\):

- AI4I: \(1.22\times10^{-11}\);
- Steel: \(3.66\times10^{-13}\);
- SECOM: \(8.23\times10^{-14}\);
- Ballistic: \(4.01\times10^{-11}\).

## S5. Conditional interval calibration

AI4I, one fixed design, \(R=3000\):

| Interval | KTES | SRS |
|---|---:|---:|
| Wald plug-in | 0.8993 | 0.6470 |
| Wald Jeffreys | 0.9900 | 0.9123 |
| logit Wald | 0.9260 | 0.7633 |
| Beta nominal count, uniform prior | 1.0000 | 1.0000 |
| Beta nominal count, Jeffreys prior | 1.0000 | 1.0000 |
| Bayes-Kish | 0.9507 | 0.7637 |
| Wald-Kish | 0.9270 | 0.6510 |

## S6. Coverage versus induced shift

| \(\beta\) | SRS Bayes-Kish | KTES Bayes-Kish | KTES design-aware sensitivity |
|---:|---:|---:|---:|
| −1.5 | 0.606 | 0.954 | 0.982 |
| −1.0 | 0.759 | 0.967 | 0.981 |
| −0.5 | 0.868 | 0.969 | 0.965 |
| 0 | 0.946 | 0.957 | 0.957 |
| +0.5 | 0.950 | 0.935 | 0.926 |
| +1.0 | 0.884 | 0.901 | 0.880 |
| +1.5 | 0.771 | 0.868 | 0.833 |

The model-assisted term is not a monotone improvement and is not a coverage guarantee.

## S7. Frozen phase diagram

Relative KTES MARE reduction versus SRS (%), 10 paired seeds/cell:

| \(\alpha\backslash\beta\) | −1.5 | −1.0 | −0.5 | 0 | +0.5 | +1.0 | +1.5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 47.6 | 82.1 | 20.6 | 46.8 | 37.9 | 52.4 | 58.0 |
| 0.25 | 60.4 | 68.7 | 71.2 | 46.8 | 58.0 | 70.0 | 64.3 |
| 0.50 | 71.2 | 76.0 | 75.6 | 46.8 | 74.1 | 76.4 | 66.2 |
| 0.75 | 83.2 | 86.5 | 83.2 | 46.8 | 84.1 | 81.3 | 57.5 |
| 1.00 | 73.7 | 80.2 | 83.4 | 46.8 | 72.9 | 70.4 | 50.3 |

Exploratory correlations with gain:

- \(\sigma_{\log\rho}\): 0.086;
- \(|AUC-0.5|\): 0.340;
- interaction: 0.217.

## S8. Truth-generator sensitivity

| Dataset | SRS LR | KTES LR | LR reduction | SRS RF | KTES RF | RF reduction |
|---|---:|---:|---:|---:|---:|---:|
| AI4I | 0.1318 | 0.0783 | 40.6% | 0.4076 | 0.2742 | 32.7% |
| Steel | 0.0580 | 0.0250 | 57.0% | 0.0533 | 0.0285 | 46.5% |
| SECOM | 0.0377 | 0.0196 | 48.0% | 0.0621 | 0.0735 | −18.3% |

## S9. Source-pool support-failure rates

At \(\beta=-1\):

- AI4I: 19/20 pools fail the minimum support contract;
- Steel: 8/20 fail;
- SECOM: 19/20 fail;
- ballistic: 0/20 fail.

For cells with adequate support and at least two valid pools, KTES−SRS source-pool CIs are negative in all reported cells. KTES−SRS-IS is not sign-consistent across datasets.

## S10. Threshold decisions

At \(t=0.85P^*\) and \(1.15P^*\), the low-probability AI4I, SECOM, and ballistic experiments are mostly inconclusive at \(n=10\). Steel is the only dataset with high correct-decision frequency. No universal decision-level advantage is claimed for KTES.
