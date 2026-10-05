[17] TE-BTBA-009-2021, General Requirements for Data Acceptance in Equipment Test and Evaluation (装备试验鉴定数据采信通用要求), Equipment Development Department, CMC, 2021.

[18] C. J. Willits, D. C. Dietz, and A. H. Moore, "Series-system reliability estimation using very small binomial samples," *IEEE Trans. Rel.*, vol. 46, no. 2, pp. 296-302, 1997, doi: 10.1109/24.589960.

[19] J. Jeon and S. Ahn, "Bayesian methods for reliability demonstration test for finite population using lot and sequential sampling," *Sustainability*, vol. 10, no. 10, art. 3671, 2018, doi: 10.3390/su10103671.

[20] D. Li, M. Ruan, and K. You, "Research on test scheme of weapon system reliability qualification based on reliability growth" (基于可靠性增长的武器系统可靠性鉴定试验方案研究), *Acta Armamentarii*, vol. 38, no. 9, pp. 1815-1821, 2017.

[21] S. Zhang, S. Fan, and J. Zhang, "Bayesian assessment for product reliability using pass-fail data" (成败型产品可靠性的Bayes评估), *Acta Armamentarii*, vol. 22, no. 2, pp. 238-240, 2001.

[22] T. Zhou, C. Hu, and X. Ye, "Bayes method for reliability assessment of missile weapon systems" (导弹武器系统可靠性评估的Bayes方法), *Tactical Missile Technology*, no. 1, pp. 20-23, 2005.

[23] L. Kang, S. Dong, and N. Guo, "Armament test evaluation and load calculation based on Bayesian assessment" (武器装备试验的Bayes评估及容量计算), *Journal of Air Force Engineering University*, no. 6, pp. 30-33, 2003.

[24] Y. Xing, *Reliability and Maintainability Index Verification for Weapon System with Small Sample Size* (小子样条件下武器装备可靠性与维修性指标验证方法), M.S. thesis, National University of Defense Technology, Changsha, China, 2005.

[25] AI4I 2020 Predictive Maintenance Dataset, UCI ML Repository, ID 601, doi: 10.24432/C5HS5C.

[26] Steel Plates Faults Dataset, UCI ML Repository, ID 198, doi: 10.24432/C5J30W.

[27] SECOM Dataset, UCI ML Repository, ID 179, doi: 10.24432/C5KS39.

[28] US Army, *FM 23-10 Sniper Training*, Table 3-1 (environmental impact-point offsets).

[29] A. Salt and D. Rowland, "Small-arms hit-probability data," ISMOR 2016. Second-hand compilation, row-level source annotation; original 83-point table not obtained (Section VII-C).

[30] H. Zhao, B. Peng et al., "Accelerated evaluation of automated vehicles safety in lane-change scenarios based on importance sampling techniques," *IEEE Trans. Intell. Transp. Syst.*, vol. 18, no. 3, pp. 595-607, 2017.

[31] N. Kalra and S. M. Paddock, "Driving to safety: How many miles of driving would it take to demonstrate autonomous vehicle reliability?" *Transportation Research Part A*, vol. 94, pp. 182-193, 2016.

[32] M. R. Elliott and R. Valliant, "Inference for nonprobability samples," *Statist. Sci.*, vol. 32, no. 2, pp. 249-264, 2017.

[33] J.-C. Deville and C.-E. Särndal, "Calibration estimators in survey sampling," *J. Amer. Statist. Assoc.*, vol. 87, no. 419, pp. 376-382, 1992.

[34] Y. Chen, P. Li, and C. Wu, "Doubly robust inference with nonprobability survey samples," *J. Amer. Statist. Assoc.*, vol. 115, no. 532, pp. 2011-2021, 2020, doi: 10.1080/01621459.2019.1677241.

[35] D. Sanz-Alonso and R. Wang, "A Bayesian perspective on importance sampling: Required sample size and ESS," *Entropy*, vol. 23, no. 1, art. 22, 2021.

[36] M. R. Spencer, "An approximate design effect for unequal weighting when measurements may correlate with selection probabilities," *Survey Methodology*, vol. 26, no. 2, 2000.

[37] National Research Council, *Statistical Methods for Testing and Evaluating Defense Systems: Interim Report*, ch. 2, "Use of experimental design in operational testing," National Academies Press, 1995.

---

## Appendix A. Reproducibility

The v7 evidence freeze is generated from the offline replication package. The primary commands are:

```bash
python validate_contracts.py                 # exact budget, reference contract, fail-closed support
python validate_v2_adaptive.py 50            # frozen headline grid and coverage
python heldout_eta.py                         # 25/25 eta selection audit
python headline_stats.py                      # paired mean/median uncertainty
python calibrate_intervals.py                 # single-design interval calibration
python scan_phase_diagram_frozen.py           # frozen 5x7 synthetic phase diagram
python validate_pool_outer.py                 # 20-source-pool outer Monte Carlo
python coverage_vs_bias.py 3000               # coverage under induced shift
python truth_sensitivity.py                   # logistic vs random-forest truth
python validate_threshold_decision.py         # accept/reject/inconclusive endpoint
```

The ablation scripts (`analyze_ai4i_failure.py`, `validate_ktes_v2.py`) remain part of the package for the coverage-deletion result. Legacy `scan_pool_bias.py`, `scan_phase_diagram_v2.py`, and the old fixed-pool `validate_biased_pool_results.json` are retained for provenance but are **not** sources for v7 headline claims. Machine-readable v7 evidence is stored in `validate_contracts_results.json`, `validate_v2_adaptive_results.json`, `heldout_eta_results.json`, `headline_paired_stats.json`, `calibrate_intervals_results.json`, `scan_phase_diagram_frozen_results.json`, `pool_outer_results.json`, `coverage_vs_bias_results.json`, `truth_sensitivity_results.json`, and `threshold_decision_results.json`.

Selection seeds for the main paired runs are 9000 onward; shot resampling uses the 30000-series RNG as specified in the scripts. The outer-pool analysis isolates each dataset-shift cell in a fresh process to avoid cumulative SLSQP/BLAS stalls observed on some builds; this changes neither seeds nor mathematics.
