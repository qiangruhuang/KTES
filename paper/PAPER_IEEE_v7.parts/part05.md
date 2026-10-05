
**TABLE V.** MARE by regularizer under the exact-budget regime (REP = 50). Realized $\tau$ and local $N_{\mathrm{eff}}/m$ are means under the frozen $\eta=0.6$ configuration.

| Dataset | SRS | $\tau=0.03$ | $\eta=0.6$ (frozen) | $\eta=0.7$ | $\eta=0.8$ | Realized $\tau$ | $N_{\mathrm{eff}}/m$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| AI4I | 0.1421 | 0.1092 | **0.0713** | 0.0739 | 0.0865 | 0.000595 | 0.744 |
| Steel Plates | 0.0573 | 0.0411 | **0.0259** | 0.0314 | 0.0378 | 0.001450 | 0.794 |
| SECOM | 0.0363 | 0.0264 | **0.0216** | 0.0231 | 0.0250 | 0.000038 | 0.803 |
| Ballistic | 0.0851 | 0.0503 | **0.0440** | 0.0447 | 0.0485 | 0.000232 | 0.817 |

On development seeds the per-dataset optimum is $\eta=0.6$ for Steel Plates, SECOM, and ballistic and $\eta=0.7$ for AI4I. On held-out evaluation seeds, replacing 0.6 by 0.7 changes MARE by 0.0000 (AI4I), +0.0072 $\pm$ 0.0032 (Steel), +0.0016 $\pm$ 0.0009 (SECOM), and +0.0018 $\pm$ 0.0025 (ballistic), where positive values mean 0.7 is worse. This supports a single frozen $\eta=0.6$ configuration without claiming a universal optimum.

### D. Frozen phase diagram and limits of pre-test diagnostics

To test score fidelity and pool shift under the same frozen protocol as Table III, we rerun the angular-error surface on a $5\times7$ grid over score fidelity $\alpha\in\{0,0.25,0.5,0.75,1\}$ and pool-bias intensity $\beta\in\{-1.5,-1,-0.5,0,0.5,1,1.5\}$. Each cell uses $M=50$, $\eta=0.6$, exact quotas, fail-closed support checks, and 10 paired seeds. All 35 cells retain adequate stratum support in this controlled surface.

**TABLE VI.** Frozen-protocol relative MARE reduction of KTES vs SRS (%). This is a secondary synthetic diagnostic (10 seeds per cell), not a confidence-bound table.

| $\alpha\backslash\beta$ | $-1.5$ | $-1.0$ | $-0.5$ | $0.0$ | $+0.5$ | $+1.0$ | $+1.5$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | +47.6 | +82.1 | +20.6 | +46.8 | +37.9 | +52.4 | +58.0 |
| 0.25 | +60.4 | +68.7 | +71.2 | +46.8 | +58.0 | +70.0 | +64.3 |
| 0.50 | +71.2 | +76.0 | +75.6 | +46.8 | +74.1 | +76.4 | +66.2 |
| 0.75 | +83.2 | +86.5 | +83.2 | +46.8 | +84.1 | +81.3 | +57.5 |
| 1.00 | +73.7 | +80.2 | +83.4 | +46.8 | +72.9 | +70.4 | +50.3 |

The surface confirms that the frozen method can remain effective across a wide range of controlled shifts, but it **does not validate the earlier proposed field rule**. Across the 35 cells, correlation of gain with log-importance-ratio spread is only $r=0.086$, with $|\mathrm{AUC}(s,y)-0.5|$ it is $r=0.340$, and with their interaction it is $r=0.217$. These associations are too weak and surface-dependent to justify a quantitative pre-test predictor of KTES gain. We therefore retain $\sigma_\varrho$ and score fidelity only as descriptive diagnostics and do not use them as a go/no-go rule. The support audit in Section VI-G is the stronger operational applicability check.

### E. Conditional interval calibration

We evaluate seven interval constructions on AI4I ($P^*=0.0338$) using one fixed frozen KTES design (seed 42, $N_{\mathrm{eff}}=34.17$ conditions) and one SRS design, with $R=3000$ shot-level resamples.

**TABLE VII.** Empirical coverage at nominal 95% on the single fixed AI4I design.

| Construction | KTES | SRS |
|---|---:|---:|
| Wald, plug-in variance | 0.899 | 0.647 |
| Wald, Jeffreys variance | 0.990 | 0.912 |
| Wald, logit scale | 0.926 | 0.763 |
| Beta, pseudo-count $=n$, uniform prior | 1.000 | 1.000 |
| Beta, pseudo-count $=n$, Jeffreys prior | 1.000 | 1.000 |
| **Effective-count Beta, Kish $n_{\mathrm{eff}}$** | **0.951** | 0.764 |
| Wald, Kish | 0.927 | 0.651 |

The nominal-$n$ pseudo-posteriors are prior-dominated and over-conservative. The Kish scaling brings the frozen KTES construction close to nominal on this one design, while SRS remains under-covered because the selected design is displaced from $P^*$. This result supports the interval as a **conditional engineering calibration** for the stated regime; it does not establish unconditional 95% coverage. Section VI-G tests the same mechanism under induced pool shift and separates variance correction from residual signed bias.

### F. Physical case: angular error, environments, and the sight table

The two empirical data chains underlying this subsection are shown in Fig. 3 (proving-ground single-shot hit probabilities; combat and peace-training hit rates, with wartime points connected and peace-training points left unlinked).

*Step 1, back-inferred angular error.* Inverting (10) at $k_{\mathrm{env}}=1$ against Salt wartime hit rates gives, for standing targets, $\sigma_\theta(50\,\mathrm{m})=22.97$ mrad falling to $\sigma_\theta(500\,\mathrm{m})=7.97$ mrad (ratio 0.35; from 100 m, 16.70 to 7.97, ratio 0.48; the two ratios refer to different baselines and must not be interchanged). That near-range angular error is systematically *larger* reproduces the proximity effect reported by Salt as a *self-consistency check* of the inversion (the same data drive both sides), not as independent validation; and $\sigma_\theta$ is an *equivalent* total that absorbs shooter factors. The prone-posture inversion is non-monotone in mid-range (250-350 m), indicating instability at those small probabilities; the standing chain is used downstream. Fig. 4(a) plots both inversions.

*Step 2, environment amplification.* Inverting $k_{\mathrm{env}}$ from target hit-rate levels relative to plain gives plain 1.000, plateau 1.157, hot-humid 1.067, cold 1.086. Because these targets were themselves engineering assumptions (reductions of 25%, 12%, 15%), $k_{\mathrm{env}}$ inherits that assumption; the sensitivity scan of the environment model is part of the replication package. *Range dependence.* In the probability range this pilot occupies ($p\approx2\times10^{-3}$ to $6\times10^{-2}$), (10) gives $p_{\mathrm{env}}/p_{\mathrm{plain}}\approx k_{\mathrm{env}}^{-2}$, numerically constant over 50-800 m (computed ratios: plateau 0.755 to 0.748, hot-humid 0.883 to 0.879, cold 0.853 to 0.849). Fig. 4(b)-(c) shows the resulting surface and this ratio directly. The angular-error model is therefore *empirically indistinguishable* from a multiplicative model in this regime; its advantage is interpretability and the ballistic/crew decomposition (11), not measured range-dependent discrimination.

*Step 3, what the sight table can and cannot explain.* Applying FM 23-10 impact-point offsets [28] (altitude 5000 ft $\approx$ 1.6 MOA, 10 $^\circ$C $\approx$ 1 MOA, 20% RH $\approx$ 1 MOA; Fig. 5(a)): plateau (4500 m, $-5\,^\circ$C, RH 30%) totals 5.04 MOA, hot-humid (35 $^\circ$C, RH 90%) 2.83 MOA, cold ($-30\,^\circ$C, RH 60%) 4.53 MOA. The offset-to-dispersion ratio is only 0.088-0.184, and the ballistic term explains 0.97% (plateau), 0.31% (hot-humid), 0.78% (cold) of the hit-rate reduction, against the 25%/12%/15% the engineering factors assert (Fig. 5(b)). Reverse-engineering those factors would require 21.8-33.1 MOA of impact shift, five to eight times the sight-table values. **Conclusion:** the modeled ballistic component does <b>not</b> explain the asserted reductions; the residual is not accounted for by the sight-table term, and crew effectiveness is a plausible but uncalibrated contributor. We therefore do not claim that crew effectiveness is the dominant share as a measured fact. The environment effect must still be decomposed as in (11), no absolute hit-probability from this surface may be quoted, and Figs. 3-5 are demonstration material for the physical case: the method comparisons of Sections VI-A-VI-G do not depend on them. Method comparisons on the surface are insensitive to the decomposition because it rescales responses without touching the pool structure or $\pi$.

### G. Source-pool shift, support failures, and outer-pool uncertainty

The benchmark main table holds pool $=$ target, so it cannot establish bias correction. We therefore generate biased candidate pools from the full reference distribution using $p_{\mathrm{pool}}\propto\pi e^{\beta s}$ with $\beta\in\{-1,0,+1\}$. The target estimand and unlabeled target-reference frame remain fixed under $\pi$. Crucially, inference is performed across **20 independently generated source pools** per dataset-shift cell, with two paired selection seeds within each pool; the source pool, not the selection seed, is the inferential unit. KTES uses the same exact-budget $\eta=0.6$ protocol and fails closed whenever a target-positive stratum has fewer than two candidate conditions.

**TABLE VIII.** Outer-pool MARE and paired source-pool differences. KTES MARE is conditional on pools that pass the support check; when fewer than two pools pass, no CI is reported.

| Dataset | $\beta$ | Support-fail rate | SRS | SRS-IS | KTES* | KTES$-$SRS [95% CI] | KTES$-$SRS-IS [95% CI] |
|---|---:|---:|---:|---:|---:|---|---|
| AI4I | $-1$ | **95%** | 0.485 | 0.321 | 0.080 | $-0.340$ (1 supported pool) | $-0.184$ (1 supported pool) |
| AI4I | 0 | 0% | 0.148 | 0.148 | 0.078 | $-0.070$ $[-0.120,-0.020]$ | $-0.070$ $[-0.120,-0.020]$ |
| AI4I | $+1$ | 0% | 0.997 | **0.138** | 0.311 | $-0.686$ $[-0.803,-0.569]$ | **+0.173** $[+0.091,+0.255]$ |
| Steel | $-1$ | **40%** | 0.153 | 0.176 | 0.058 | $-0.099$ $[-0.143,-0.054]$ | $-0.119$ $[-0.159,-0.079]$ |
| Steel | 0 | 0% | 0.075 | 0.075 | 0.027 | $-0.047$ $[-0.071,-0.024]$ | $-0.047$ $[-0.071,-0.024]$ |
| Steel | $+1$ | 0% | 0.174 | 0.173 | **0.079** | $-0.095$ $[-0.121,-0.070]$ | $-0.094$ $[-0.140,-0.049]$ |
| SECOM | $-1$ | **95%** | 0.042 | 0.098 | 0.020 | $-0.032$ (1 supported pool) | $-0.042$ (1 supported pool) |
| SECOM | 0 | 0% | 0.038 | 0.038 | 0.026 | $-0.013$ $[-0.024,-0.001]$ | $-0.013$ $[-0.024,-0.001]$ |
| SECOM | $+1$ | 0% | 0.049 | 0.037 | **0.022** | $-0.027$ $[-0.040,-0.014]$ | $-0.015$ $[-0.025,-0.004]$ |
| Ballistic | $-1$ | 0% | 0.571 | 0.143 | **0.099** | $-0.472$ $[-0.540,-0.403]$ | $-0.044$ $[-0.113,+0.025]$ |
| Ballistic | 0 | 0% | 0.097 | 0.097 | **0.048** | $-0.049$ $[-0.073,-0.024]$ | $-0.049$ $[-0.073,-0.024]$ |
| Ballistic | $+1$ | 0% | 0.518 | 0.208 | **0.140** | $-0.378$ $[-0.410,-0.346]$ | $-0.069$ $[-0.128,-0.009]$ |

The load-bearing finding is **support-aware rather than direction-only**. When support is adequate, KTES is lower-error than naive SRS in every cell for which a source-pool CI can be estimated. Severe negative shift, however, removes the minimum rare-stratum support in 95% of AI4I and SECOM pools and 40% of Steel pools. Those cells are not evidence that weighting can recover missing conditions; they are evidence that the design should stop and request supplemental candidates. Among supported pools, KTES versus SRS-IS is dataset-dependent: SRS-IS is clearly better for AI4I at $\beta=+1$, KTES is better for Steel, SECOM, and ballistic at $\beta=+1$, and the ballistic $\beta=-1$ difference is not significant. The previous simple rule “KTES for under-representation, importance weighting for over-representation” is therefore rejected by the stronger outer-pool experiment.

*Coverage under induced shift.* On the angular-error surface, Bayes-Kish coverage for SRS falls from 0.946 at $\beta=0$ to 0.606 at $-1.5$ and 0.771 at $+1.5$. Frozen KTES gives 0.957 at $\beta=0$, 0.954 at $-1.5$, 0.967 at $-1$, 0.901 at $+1$, and 0.868 at $+1.5$. A model-assisted re-selection term $\hat\tau_d^2$, estimated from a kernel-ridge surrogate and $B=10$ cost-free redesigns, raises KTES coverage to 0.982, 0.981, and 0.965 for $\beta=-1.5,-1,-0.5$, respectively, but falls to 0.880 and 0.833 at $\beta=+1,+1.5$. The correction therefore addresses part of the **design-variance** component under one shift regime; it does not repair signed bias and is retained as a sensitivity analysis rather than a primary interval guarantee.

### H. Truth-generator sensitivity

The public benchmark metrics treat a 5-fold OOF logistic-regression probability surface as ground truth. To test dependence on response-surface smoothness, we regenerate the benchmark truth with a 300-tree random forest and recompute SRS and frozen KTES on the same 30 selection seeds. On AI4I the MARE reduction changes from 40.6% (logistic truth) to 32.7% (random-forest truth); on Steel Plates it changes from 57.0% to 46.5%. On SECOM, however, the reduction changes from +48.0% to **$-18.3\%$**, so KTES becomes worse than SRS under the alternative truth generator. The benchmark advantage is therefore conditional on the learned response surface; the public-data rows cannot be read as universal evidence for kernel alignment. The source-pool experiments and the physics surface provide complementary but still controlled evidence rather than a substitute for independent engineering validation.

### I. Threshold-decision endpoint

The motivating T&E decision is whether $P^*$ exceeds a qualification threshold, not merely whether MARE is small. We therefore connect each selected design to the Bayes-Kish interval and classify a complete $n=10$ experiment as **accept** if the lower bound exceeds $t$, **reject** if the upper bound is below $t$, and **inconclusive** otherwise. Thresholds are $t=cP^*$ with $c\in\{0.70,0.85,1.00,1.15,1.30\}$; $c=1$ is treated as a boundary with no artificial “correct side.” Table IX shows the practically informative $\pm15\%$ thresholds.

**TABLE IX.** Decision rates at $t=0.85P^*$ and $1.15P^*$, 50 complete experiments per method. Entries are correct / wrong / inconclusive.
