\]

subject to the existing positive inclusion-probability floor and exact stratum allocation. The frozen constants are therefore

\[
\rho=0.20,\qquad \lambda=3.
\]

The compound-tail term is deliberately mild. Development experiments with stronger tilts improved some edge metrics but reduced worst-case robustness; `rho=0.20` was frozen before independent confirmation.

### D. Local Cube spreading and balance

Given the prescribed first-order probabilities, Local Cube sampling applies local competition in auxiliary-feature space while maintaining approximate balancing constraints. The design inherits the probability-preserving logic of cube sampling [1] and the spreading motivation of local pivotal methods [2].

The algorithm is used as a design mechanism rather than a claim of exact optimality. Its role is to avoid spending several probability-remainder slots on nearly redundant nearby conditions when equally eligible alternatives exist elsewhere in the operational frame.

### E. Model-assisted Hajek residual correction

Let `m_i` denote a wall-to-wall auxiliary prediction. Within stratum `g`, the residual correction is

\[
\widehat R_{g,H}
=
\frac{\sum_{i\in s_g}(p_{i\mid g}/\pi_i)(Y_i-m_i)}
{\sum_{i\in s_g}p_{i\mid g}/\pi_i}.
\]

The overall estimator is

\[
\widehat\theta_Y
=
\sum_g P(G_g)
\left[
E_{p_g}\{m(X)\}+\widehat R_{g,H}
\right].
\]

The same architecture is used for failure or critical-domain targets when the endpoint is valid. In external studies without a defensible wall-to-wall outcome surrogate, a conservative constant auxiliary mean within stratum reduces the estimator to a probability-weighted Hajek correction without outcome leakage.

### F. Weight diagnostics

For selected probability-remainder units with analysis weights proportional to `p_i/pi_i`, the Kish effective sample size is

\[
N_{\mathrm{eff}}
=
\frac{(\sum_i w_i)^2}{\sum_i w_i^2}.
\]

External validation uses fail-closed ESS guardrails. For the 37-unit probability remainder, the median ESS must be at least 18.5 and its fifth percentile at least 12. No external dataset is allowed to retune the tilt or probability floor to satisfy these thresholds.

### G. Uncertainty and three-state decision

The design variance diagnostic uses

\[
\widehat V=\max(\widehat V_{GS},\widehat V_{PWR}),
\]

where the first term is a spatial/local-difference estimator and the second is a first-order-probability reference construction. Safety-facing failure calibration was frozen in R3 and reused unchanged in R5 and Phase 2. The frozen absolute calibration constants are 0.137719714266479 for the two-sided failure diagnostic and 0.19767009190382911 for the safety-facing upper calibration.

The frozen calibration is empirical within the development/confirmation architecture and is not asserted to be distribution-free under arbitrary simulator-to-reality shift.

The final decision is:

- **Accept** when all safety-facing bounds pass;
- **Reject** when at least one requirement clearly fails;
- **Inconclusive** otherwise.

The objective is controlled evidence, not maximum definitive-decision rate.

---

## V. Evidence Protocol

### A. Phase 1.2R development sequence

The small-N design was developed through five explicit stages.

**R1** compared an all-probability design with a split design containing 15 deterministic KTES points and a smaller probability audit. The all-probability design substantially improved profile and critical-tail inference but had lower edge discovery.

**R2** introduced novelty-driven unequal inclusion probabilities and local spreading. Edge hit increased but remained below the deterministic split design in some regimes.

**R3** introduced three risk-aware certainty sentinels. Pooled edge discovery matched the split baseline, but simulator-blind hidden-bias conditions exposed a weakness because all sentinels inherited the auxiliary risk model.

**R4** hedged the certainty portfolio with one pure-novelty guard and two risk-aware sentinels. Hidden-bias performance improved but remained imperfect.

**R5** moved the additional hedge into the probability remainder through a 20% compound adverse-tail component. Development compared multiple hedge strengths and froze `rho=0.20` before confirmation.

The final Phase 2 method is therefore the output of an explicit development sequence; Phase 2 datasets are not used to continue this search.

### B. Independent R5 confirmation

The frozen R5 design was confirmed on 1000 independent finite populations: 200 populations for each of five discrepancy scenarios (`good`, `global_bias`, `tail_bias`, `hidden_bias`, `mixed`). Every population was evaluated with paired c-pKTES-Hedge, reconstructed R4, and Split15 designs at `n=40`.

The primary confirmation seed was 20261115. Confirmation populations/seeds were not used in the R1–R5 development search, and the R3 safety calibration was developed and frozen before R5 confirmation. The confirmation evaluates profile, failure, critical-tail, edge-hit, definitive-correct, abstention, coverage diagnostics, and false acceptance.

### C. Phase 2 governance contract

