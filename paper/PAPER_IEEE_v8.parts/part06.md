
### F. Limitations

First, the R5 confirmation is simulation-based. Although it uses 1000 independent finite populations and multiple discrepancy regimes, its data-generating mechanisms remain controlled constructions.

Second, the edge-hit advantage over Split15 is not statistically significant. The evidence supports compatibility with Split15-level discovery while improving inference, not dominance in boundary discovery.

Third, Anti-UAV410 is a task-effectiveness benchmark rather than operational weapon-system T&E. Its success establishes structural transport of the sampling design, not mission-level safety certification.

Fourth, the Anti-UAV410 result requires an execution clarification for the exact Split15 adapter and finite-domain estimator. It must not be presented as a pristine preregistered result.

Fifth, IDF-DS did not reach a performance comparison because the public source could not instantiate the frozen preoutcome design frame. The study therefore contributes a source-structure limitation rather than evidence for or against c-pKTES-Hedge performance.

Sixth, the AMOVFLY literal failure endpoint is invalid for failure-rate qualification because of the `(0,0)` placeholder mechanism. The post-outcome sensitivity cannot be promoted to a repaired confirmation.

Seventh, the model-assisted estimator relies on the external availability and quality of auxiliary predictions when they are used. The probability residual correction reduces dependence on those predictions but does not make severe model misspecification irrelevant.

Eighth, the present work does not establish distribution-free safety calibration under arbitrary domain shift. The R3 calibration is frozen and empirically audited within the development/confirmation architecture.

### G. Next independent gate

The next study should not further tune Anti-UAV410 or AMOVFLY. It should use a **new independently frozen engineering dataset and endpoint contract** with:

1. unit-linked preoutcome mission/configuration/environment covariates available before outcome access;
2. endpoint semantics verified independently of the observed performance distribution;
3. the c-pKTES-Hedge design object written and hashed before outcome opening;
4. the same frozen `rho`, `lambda`, sentinel count, estimator, and UQ constants;
5. prespecified population, critical-domain, difficult-case, and weight-stability guardrails.

A negative result should narrow the transportability claim rather than trigger retuning on the same external data.

---

## VIII. Conclusion

This study addresses a specific small-budget T&E conflict: probability sampling is needed for population inference, while active targeting is needed to expose difficult and emergent conditions. c-pKTES-Hedge resolves part of that conflict by embedding three outcome-blind certainty sentinels inside a probability design whose remaining 37 live tests retain known positive inclusion probabilities.

In an independent 1000-population confirmation at n=40, the final design achieves edge discovery comparable to a 15-deterministic-plus-audit baseline at the precision supported by the paired interval while producing lower profile, failure, and critical-tail error and more definitive-correct decisions. This is the primary controlled evidence for the method.

The external evidence is intentionally less tidy. Anti-UAV410 passes every numerical guardrail but includes an execution clarification and retains a small profile-error disadvantage relative to SRS. IDF-DS is stopped before outcome access because the public source cannot support the frozen preoutcome design frame. AMOVFLY passes its numerical comparison gate but its literal waypoint endpoint is semantically contaminated by systematic `(0,0)` placeholders; a post-outcome sensitivity preserves the method-comparison result but cannot replace the confirmation.

These outcomes support a broader methodological conclusion. **External validity for test-allocation methods is a joint property of the sampling design, the source structure, the endpoint semantics, and the realized execution artifact.** A probability-preserving active sampler can improve the inference–edge trade-off under severe live-test budgets, but credible deployment of that sampler requires fail-closed governance before and after the numerical experiment.

---

## References

[1] J.-C. Deville and Y. Tille, “Efficient balanced sampling: The cube method,” *Biometrika*, vol. 91, no. 4, pp. 893–912, 2004, doi: 10.1093/biomet/91.4.893.

[2] A. Grafstrom, N. L. P. Lundstrom, and L. Schelin, “Spatially balanced sampling through the pivotal method,” *Biometrics*, vol. 68, no. 2, pp. 514–520, 2012, doi: 10.1111/j.1541-0420.2011.01699.x.

[3] L. Kish, *Survey Sampling*. New York, NY, USA: Wiley, 1965.

[4] C.-E. Sarndal, B. Swensson, and J. Wretman, *Model Assisted Survey Sampling*. New York, NY, USA: Springer, 1992.

[5] D. G. Horvitz and D. J. Thompson, “A generalization of sampling without replacement from a finite universe,” *Journal of the American Statistical Association*, vol. 47, no. 260, pp. 663–685, 1952.

[6] C. Qian, J. Xu, X. Xing, and F. Guo, “Test case sampling optimization for safety validation of automated driving systems,” *Nature Communications*, vol. 17, art. 3114, 2026, doi: 10.1038/s41467-026-69675-8.

[7] H. Zhao *et al.*, “Accelerated evaluation of automated vehicles safety in lane-change scenarios based on importance sampling techniques,” *IEEE Transactions on Intelligent Transportation Systems*, vol. 18, no. 3, pp. 595–607, 2017.

[8] N. Kalra and S. M. Paddock, “Driving to safety: How many miles of driving would it take to demonstrate autonomous vehicle reliability?” *Transportation Research Part A*, vol. 94, pp. 182–193, 2016.

[9] A. Gretton, K. M. Borgwardt, M. Rasch, B. Scholkopf, and A. J. Smola, “A kernel method for the two-sample-problem,” in *Advances in Neural Information Processing Systems 19*, 2007, pp. 513–520.

[10] J. Huang, A. J. Smola, A. Gretton, K. M. Borgwardt, and B. Scholkopf, “Correcting sample selection bias by unlabeled data,” in *Advances in Neural Information Processing Systems 19*, 2007, pp. 601–608.

[11] B. Huang, J. Li, J. Chen, G. Wang, J. Zhao, and T. Xu, “Anti-UAV410: A thermal infrared benchmark and customized scheme for tracking drones in the wild,” *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 46, no. 5, pp. 2852–2865, 2024, doi: 10.1109/TPAMI.2023.3335338.

[12] C. Garcia-Gascon, J. Bas-Bolufer, P. Castello-Pedrero, and J. A. Garcia-Manrique, “An open benchmark dataset for machine learning and intelligent trajectory optimization in fixed-wing unmanned aerial systems,” *Scientific Data*, vol. 13, art. 364, 2026, doi: 10.1038/s41597-026-06716-3.

[13] C. Garcia-Gascon, “Fixed-Wing UAS Telemetry Benchmark (IDF_DS): 240 Flights for ML and Intelligent Trajectory Optimization,” Zenodo, 2025, doi: 10.5281/zenodo.16992975.

[14] YujiaoHu, “AMOVFLY-Dataset: Dataset associated with ‘AMOVFLY: Enabling Advanced UAV Modeling with the Comprehensive Flight Status Dataset’,” GitHub repository, frozen source commit `67069ed00ddbebd62b71aa9bb1272415e9b15ff8`, accessed Oct. 2026.

[15] National Research Council, *Statistical Methods for Testing and Evaluating Defense Systems: Interim Report*. Washington, DC, USA: National Academies Press, 1995.

[16] C. J. Willits, D. C. Dietz, and A. H. Moore, “Series-system reliability estimation using very small binomial samples,” *IEEE Transactions on Reliability*, vol. 46, no. 2, pp. 296–302, 1997, doi: 10.1109/24.589960.

[17] J. Jeon and S. Ahn, “Bayesian methods for reliability demonstration test for finite population using lot and sequential sampling,” *Sustainability*, vol. 10, no. 10, art. 3671, 2018, doi: 10.3390/su10103671.

---

## Appendix A. Frozen Evidence Identities

### A.1 R5 controlled confirmation

Frozen Phase 1.2R primary method:

- live `n=40`;
- certainty sentinels = 3;
- probability remainder = 37;
- novelty/compound mix = 80/20;
- `rho=0.20`;
- `lambda=3`;
- estimator = stratum-wise Hajek model-assisted residual correction;
- UQ = `max(GS,PWR)` with R3-frozen calibration;
- failure absolute 95% calibration = `0.137719714266479`;
- safety-upper absolute calibration = `0.19767009190382911`.

