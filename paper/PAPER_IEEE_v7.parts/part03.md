\min_{\lambda^{(\ell)}}\; \tfrac12(\lambda^{(\ell)})^\top K_{ZZ}\lambda^{(\ell)}-k_b^\top\lambda^{(\ell)}+\tau\|\lambda^{(\ell)}\|_2^2,\\
\text{s.t.}\quad \lambda^{(\ell)}\ge0,\qquad \sum_m\lambda_m^{(\ell)}=1,
\end{gathered}
\tag{4}
$$

where

$$
k_{b,m}=\sum_{i\in R_\ell}\bar\pi_i^{(\ell)}K(z_m,r_i),\qquad
\bar\pi_i^{(\ell)}=\frac{\pi_i}{\sum_{j\in R_\ell}\pi_j}.
\tag{5}
$$

This **reference contract** separates the selectable candidate pool from the unlabeled target distribution. When pool $=$ target (the benchmark main comparisons), the pool itself is the reference and the within-stratum target weights are uniform. When a biased candidate pool is induced in Section VI-G, the frozen evaluation uses the independently defined target-reference frame under $\pi$ and selects only from the biased pool. In operational use, such a reference can be a scenario grid or unlabeled sample generated from the prescribed mission profile; if neither a target reference nor an estimable density ratio is available, target-shift correction is not identified and KTES should not be presented as such. The regularizer $\tau$ limits concentration of $\lambda$.

The implementation contract was checked numerically: on all four datasets, calling the default pool-as-reference path and calling the same uniform target reference explicitly produce alignment weights that differ by at most $4.1\times10^{-11}$; the support-failure path also raises as specified.

### D. Effective-sample-size-constrained adaptive regularization

Weighting has a variance price. Define the Kish effective number of selected conditions

$$
N_{\mathrm{eff}}(\lambda)=\frac{1}{\sum_m\lambda_m^2}\in[1,M].
\tag{6}
$$

The four-cell AI4I ablation shows the basic trade: unconstrained alignment reduces MARE from 0.1252 to 0.0605 but raises analytic RMSE from 0.00918 to 0.01284 as $N_{\mathrm{eff}}$ falls from 50 to about 19. KTES therefore searches an increasing $\tau$ grid for the first solution satisfying

$$
N_{\mathrm{eff}}(\lambda^{(\ell)}(\tau))\ge\eta m_\ell.
\tag{7}
$$

A 25/25 development/evaluation seed split chooses $\eta=0.6$ on Steel Plates, SECOM, and the ballistic surface and $\eta=0.7$ on AI4I; the cross-dataset majority rule therefore freezes $\eta=0.6$ before the headline evaluation. Under this frozen protocol, mean activated $\tau$ ranges from $3.8\times10^{-5}$ (SECOM) to $1.45\times10^{-3}$ (Steel Plates), and the realized local $N_{\mathrm{eff}}/m$ ratios are 0.744–0.817. Relative to SRS, analytic RMSE ratios under the frozen configuration range from 0.57 to 1.20, so the ESS constraint controls but does not eliminate the variance cost of weighting.

### E. Dual-paradigm intervals

*Frequentist.* From (2),

$$
\mathbb{E}[\hat P]=\sum_m\lambda_m p_{(m)},\qquad
\mathrm{Var}[\hat P]=\sum_m \lambda_m^2\,\frac{p_{(m)}(1-p_{(m)})}{n} .
\tag{8}
$$

The Wald plug-in interval $\hat P\pm z_{0.975}\sqrt{\widehat{\mathrm{Var}}}$ degrades when many $\hat p_{(m)}=0$ (the plug-in variance loses those terms), which matters at small $P^*$; remedies include the logit scale and the Kish-scaled variants below.

*Effective-count Beta (pseudo-posterior).* With a Jeffreys-type prior $\mathrm{Beta}(a_0,b_0)=(0.5,0.5)$, the interval used in this paper is

$$
\begin{gathered}
\mathrm{Beta}\Big(a_0+\hat P\,n_{\mathrm{eff}},\;\; b_0+(1-\hat P)\,n_{\mathrm{eff}}\Big),\\[2pt]
n_{\mathrm{eff}}=\frac{n}{\sum_m\lambda_m^2}=n\cdot N_{\mathrm{eff}} .
\end{gathered}
\tag{9}
$$

The *effective observation count is the Kish value*, not the nominal one. On the fixed AI4I calibration design of Section VI-E, a pseudo-count of only $n$ shots is prior-dominated and gives coverage 1.000, whereas Kish scaling gives 0.951 at the nominal 95% level. This is an empirical calibration for that design, not a coverage theorem. We call (9) an *effective-count Beta (pseudo-posterior) interval* rather than a Bayesian credible interval: the fractional pseudo-counts are not the conjugate posterior of the condition-heterogeneous Bernoulli model (8). A hierarchical Beta-Binomial model for between-condition heterogeneity would be more principled but is outside the present method.

*Scope.* Both (8) and (9) propagate *shot noise only*. Design error, the deviation of the selected conditions' weighted response from $\pi$-weighted truth, is not propagated, so the intervals are conditional on the selected design. Section VI-E reports the fixed-design calibration; Table III reports design-averaged empirical coverage across 50 selected designs; Section VI-G evaluates a model-assisted design-variance sensitivity correction under induced shift.

### F. Physics-based response surface for the multi-environment case

The selection and weighting rules are equipment-agnostic. This subsection specifies how the pilot response surface (each condition's ground-truth $p_i$) is generated for the small-arms case, and how environment effects are modeled.

*Two ways to write environment effects.* The engineering habit writes environment as a multiplier on the hit probability, $p_{\mathrm{env}}(r)=p_{\mathrm{base}}(r)\,\eta_{\mathrm{env}}$. This form states the reduction but not its physical source; it cannot be sanity-checked against ballistics and it implicitly assumes the same relative reduction at every range. A more physical form lets the environment act on the *dispersion* of the impact point, with the hit-probability reduction as a geometric consequence:

$$
p=\Big[2\Phi\big(\tfrac{w}{2\sigma}\big)-1\Big]
  \Big[2\Phi\big(\tfrac{h}{2\sigma}\big)-1\Big],
\qquad \sigma=k_{\mathrm{env}}\,\sigma_\theta(r)\,r ,
\tag{10}
$$

with $w,h$ the target dimensions, $\Phi$ the standard normal CDF, $\sigma$ the equivalent standard deviation on the target plane, $\sigma_\theta(r)$ the equivalent angular error, and $k_{\mathrm{env}}\ge1$ the environment's amplification of angular error. The two axes are assumed independent zero-mean Gaussian. We quantify below (Section VI-F) that, in the probability range where this pilot operates, (10) is numerically indistinguishable from a multiplicative model with $\eta_{\mathrm{env}}=k_{\mathrm{env}}^{-2}$; its advantage is physical interpretability and decomposability, not empirical distinguishability.

*Calibration pipeline.* (i) Infer $\sigma_\theta(r)$ per range from measured wartime hit rates by solving (10) at $k_{\mathrm{env}}=1$; (ii) infer $k_{\mathrm{env}}$ per environment from target hit-rate levels relative to plain on a common reference-range set; (iii) evaluate (10) on the environment $\times$ weapon $\times$ posture $\times$ range grid to obtain the pool's ground truth.

*Honest decomposition of environment effects.* Because $k_{\mathrm{env}}$ is inferred from hit-rate reductions, it confounds two mechanisms that must be separated:

$$
\eta_{\mathrm{env}} \;=\;
\underbrace{\eta^{\mathrm{ballistic}}}_{\text{sight table}}
\;\times\;
\underbrace{\eta^{\mathrm{crew}}}_{\text{crew effect}} .
\tag{11}
$$

The ballistic term (altitude, temperature, humidity acting on the trajectory) is computable from published sight tables [28] and is tiny (under 1%, Section VI-F). The crew-effectiveness term (hypoxia, cold strain, heat stress) has no authoritative quantitative standard; it must be calibrated from data or carried as a declared estimate. The decomposition scales the *absolute* response values but leaves the pool structure (features, strata, score) and $\pi$ unchanged, so comparisons between selection methods are unaffected; *no absolute hit-probability value from this surface may be quoted* unless $\eta^{\mathrm{crew}}$ has been calibrated.
