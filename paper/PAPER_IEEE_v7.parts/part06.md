
| Dataset | Method | $0.85P^*$ | $1.15P^*$ |
|---|---|---|---|
| AI4I | SRS | 0.10 / 0.00 / 0.90 | 0.16 / 0.04 / 0.80 |
|  | KTES | 0.10 / 0.00 / 0.90 | 0.08 / 0.00 / 0.92 |
| Steel | SRS | 0.86 / 0.00 / 0.14 | 0.90 / 0.00 / 0.10 |
|  | KTES | **0.92 / 0.00 / 0.08** | **1.00 / 0.00 / 0.00** |
| SECOM | SRS | 0.08 / 0.02 / 0.90 | 0.08 / 0.02 / 0.90 |
|  | KTES | 0.12 / 0.00 / 0.88 | 0.10 / 0.00 / 0.90 |
| Ballistic | SRS | 0.12 / 0.00 / 0.88 | 0.02 / 0.02 / 0.96 |
|  | KTES | 0.04 / 0.02 / 0.94 | 0.04 / 0.04 / 0.92 |

Only Steel Plates is routinely decisive at this shot budget. AI4I, SECOM, and ballistic cases remain predominantly inconclusive, and KTES is not uniformly more decisive than SRS; on the ballistic surface it can also make more wrong calls at the tested thresholds. The estimation gain in Table III therefore **does not establish a qualification-decision gain**. This negative result closes the logical gap between the estimand and the T&E endpoint and identifies shot budget / decision design, rather than further point-estimator tuning, as the next decision-level problem.

---

## VII. Discussion

### A. What the evidence supports

KTES should be read as a support-aware design and synthesis framework for a known target scenario, not as a universally superior sampler. The frozen exact-budget results show a reproducible reduction in selection-seed MARE relative to SRS on the four controlled surfaces, and the outer-pool experiment shows that this advantage against naive SRS persists across independently generated source pools when the target strata remain represented. The fail-closed support result is equally important: when a rare target stratum disappears from the candidate source, the correct action is to acquire or generate additional candidate conditions, not to force a weighted estimate.

The nearest alternative depends on the data-generating regime. Direct importance weighting is competitive and can be superior, as on AI4I under positive shift, while KTES is better in several other supported cells. The evidence therefore supports method comparison conditioned on support, target-reference availability, and dataset geometry rather than a one-dimensional rule based on the sign of pool bias.

### B. Relation to KTCS and novelty boundary

KTCS optimizes coverage and representativeness because coverage is part of its test-set objective. For a weighted-mean estimand, the IP-coverage ordering is not load-bearing in the controlled ablation and is removed from the recommended pipeline. Kernel alignment, stratification, calibration weighting, and Kish ESS are established ideas; novelty is not claimed for those components in isolation. The contribution is their T&E-specific organization around a declared target estimand, exact resource budget, explicit target reference, support failure semantics, ESS-constrained weighting, source-pool-level validation, and separation of estimation accuracy from qualification decisions.

### C. Limitations

1) *Semi-synthetic benchmark truth.* The three public-data response surfaces are model-generated OOF probabilities. Random-forest regeneration preserves the gain on AI4I and Steel but reverses it on SECOM, so benchmark conclusions depend on the truth generator.
2) *No independent engineering validation.* The ballistic case is a physics-based demonstration calibrated from second-hand hit-rate material and engineering assumptions. It supports controlled mechanism tests, not field-effectiveness claims. No absolute hit probability is interpreted as an operational value.
3) *Support checking is stratum-level.* Requiring at least $m_{\min}$ candidate points in every target-positive stratum prevents the most obvious positivity failure but does not prove within-stratum overlap in high-dimensional continuous space.
4) *Target-reference availability is an assumption.* Bias correction in Section VI-G uses an unlabeled reference frame under $\pi$. If an operational target sample/grid or a defensible density-ratio estimate is unavailable, target alignment is not identified.
5) *Intervals are conditional engineering constructions.* The effective-count Beta interval is not the conjugate posterior of the heterogeneous Bernoulli model. Its 0.951 AI4I coverage is a single-design calibration; biased-pool coverage varies with signed design error. The model-assisted design-variance term is a sensitivity correction and can fail when bias dominates.
6) *Decision power is limited at the frozen shot budget.* At $n=10$, three of four surfaces are predominantly inconclusive around $\pm15\%$ thresholds. Lower MARE does not guarantee more correct accept/reject decisions.
7) *Outer-pool Monte Carlo is modest.* The source-pool experiment uses 20 pools and two selection seeds per pool. It is sufficient to reveal support failures and overturn the earlier direction-only rule, but not to map all pool-generation mechanisms.
8) *Hyperparameter evidence is limited to the reported grid.* The held-out split supports $\eta=0.6$ as a common frozen value; a nested study over strata, kernel bandwidth, $m_{\min}$, and budget remains outside the present scope.
9) *Pre-test gain proxies are exploratory.* Under the frozen protocol, correlations of gain with $\sigma_\varrho$, score AUC distance, and their interaction are 0.086, 0.340, and 0.217. They are not validated decision rules.

### D. Next validation gate

The next study should be an **independent engineering validation** with a pre-specified operational target distribution and candidate-source mechanism. The frozen algorithm, $M$, $n$, $\eta$, support rule, primary MARE endpoint, and threshold-decision endpoint should be locked before observing the engineering outcomes. The principal question is no longer whether another synthetic surface can be added, but whether the support-aware target-alignment workflow transfers when the target reference, candidate pool, and outcome process are generated independently of the method-development data.

---

## VIII. Conclusion

KTES reorganizes stratification, kernel alignment, and ESS control around a scenario-weighted T&E estimand with an exact condition budget and explicit support semantics. Under the frozen $M=50$, $n=10$, $\eta=0.6$ protocol, it reduces MARE relative to SRS by 40.5–54.8% on four controlled surfaces, with 66–72% per-seed win rates; paired mean and median-bootstrap intervals favour KTES in all four comparisons. These public-benchmark gains primarily reflect reduced selection variability, and one benchmark reverses under a non-smooth alternative truth generator.

The stronger source-pool experiment changes the applicability conclusion. KTES outperforms naive SRS when target support is adequate, but severe under-representation frequently becomes a fail-closed support problem rather than a recoverable weighting problem. Relative performance against direct importance weighting is dataset-dependent, so no universal direction-based method rule is supported. The Kish-scaled interval is useful as a conditional calibrated construction, while the model-assisted design term remains a sensitivity analysis. At the qualification endpoint, lower estimation error does not uniformly increase decision power at $n=10$.

The resulting evidence supports a narrower but stronger claim: KTES is a defensible **support-aware target-alignment workflow** for controlled scenario-weighted estimation when a target reference exists and candidate support is adequate. Independent engineering validation, pre-specified before outcome inspection, is the remaining gate for a field-transportability claim.

---

## References

[1] Central Military Commission. Regulations on Equipment Test and Evaluation of the PLA (军队装备试验鉴定规定), effective 2022-02-10. Public source: Ministry of National Defense website, https://www.mod.gov.cn/gfbw/qwfb/4904888.html.

[2] Q. Chen, J. Xu, X. Xing, and F. Guo, "Test case sampling optimization for safety validation of automated driving systems," *Nature Communications*, vol. 17, art. 3114, 2026, doi: 10.1038/s41467-026-69675-8. (Preprint: F. Guo et al., doi: 10.21203/rs.3.rs-6130565/v1.)

[3] ISO, *ISO 21448:2022 Road Vehicles -- Safety of the Intended Functionality*, Geneva, 2022.

[4] ISO, *ISO 34502:2022 Road Vehicles -- Test Scenarios for Automated Driving Systems -- Scenario-Based Safety Evaluation Framework*, Geneva, 2022.

[5] P. Li, Q. Dong, H. Yuan, W. Hu, W. Sun, Y. Gu, and C. Dong, "High-coverage cut-in scenario library generation for automated driving simulation testing" (面向自动驾驶仿真测试的高覆盖切入场景库生成方法), *China Journal of Highway and Transport*, vol. 37, no. 7, pp. 237-249, 2024, doi: 10.19721/j.cnki.1001-7372.2024.07.019.

[6] A. Gretton, K. M. Borgwardt, M. Rasch, B. Schölkopf, and A. J. Smola, "A kernel method for the two-sample-problem," in *Advances in Neural Information Processing Systems 19*, MIT Press, 2007, pp. 513-520. (Journal version: *J. Mach. Learn. Res.*, vol. 13, pp. 723-773, 2012.)

[7] J. Huang, A. J. Smola, A. Gretton, K. M. Borgwardt, and B. Schölkopf, "Correcting sample selection bias by unlabeled data," in *Advances in Neural Information Processing Systems 19*, MIT Press, 2007, pp. 601-608.

[8] M. Sugiyama, T. Suzuki, S. Nakajima, H. Kashima, P. von Bünau, and M. Kawanabe, "Direct importance estimation for covariate shift adaptation," *Ann. Inst. Stat. Math.*, vol. 60, pp. 699-746, 2008, doi: 10.1007/s10463-008-0197-x.

[9] L. Kish, *Survey Sampling*. New York, NY, USA: Wiley, 1965.

[10] M. D. McKay, R. J. Beckman, and W. J. Conover, "A comparison of three methods for selecting values of input variables in the analysis of output from a computer code," *Technometrics*, vol. 21, no. 2, pp. 239-245, 1979, doi: 10.2307/1268522.

[11] M. E. Johnson, L. M. Moore, and D. Ylvisaker, "Minimax and maximin distance designs," *J. Statist. Planning Inference*, vol. 26, no. 2, pp. 131-148, 1990, doi: 10.1016/0378-3758(90)90122-B.

[12] C. J. Clopper and E. S. Pearson, "The use of confidence or fiducial limits illustrated in the case of the binomial," *Biometrika*, vol. 26, pp. 404-413, 1934, doi: 10.1093/biomet/26.4.404.

[13] E. B. Wilson, "Probable inference, the law of succession, and statistical inference," *J. Amer. Statist. Assoc.*, vol. 22, pp. 209-212, 1927, doi: 10.1080/01621459.1927.10502953.

[14] L. D. Brown, T. T. Cai, and A. DasGupta, "Interval estimation for a binomial proportion," *Statist. Sci.*, vol. 16, no. 2, pp. 101-133, 2001, doi: 10.1214/ss/1009213286.

[15] TE-BTBA-001-2021, Equipment Test and Evaluation Procedures and Requirements (装备试验鉴定程序和要求), sec. 5.4.3-5.4.4, 2021.

[16] TE-BTBA-006-2021, Guide to Equipment Fielding Approval (装备列装定型工作指南), sec. 5.3.8-5.4, 2021.
