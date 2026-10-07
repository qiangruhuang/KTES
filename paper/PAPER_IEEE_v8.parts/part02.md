
Let

\[
U=\{1,\ldots,N\}
\]

be a finite population of candidate test conditions with operational weights

\[
p_i\ge 0,\qquad \sum_{i\in U}p_i=1.
\]

The population is partitioned into an operational core and mandatory critical domains,

\[
G_0,G_1,\ldots,G_R.
\]

Let `Y_i` denote a bounded performance outcome and `B_i` a failure indicator or analogous adverse event where such an endpoint is semantically valid. Example estimands are

\[
\theta_Y=\sum_i p_iY_i,
\qquad
\theta_B=\sum_i p_iB_i,
\]

and critical-domain means

\[
\theta_{Y,g}=E_p[Y\mid i\in G_g].
\]

### B. Live-test budget

The primary live-test budget is

\[
n_L=40.
\]

The problem is to choose a sample `s` of exactly 40 units while satisfying three competing requirements:

1. retain a valid probability-design basis for population inference;
2. enrich the sample toward rare or compound adverse conditions;
3. avoid unstable inverse-probability weights.

### C. Preoutcome information

The design may use only information available before opening the live outcomes. This can include operational covariates, scenario labels, configuration variables, and wall-to-wall simulator or surrogate predictions. Outcome-derived quantities cannot be used to define novelty, sentinels, inclusion probabilities, or strata in a confirmatory external study.

This rule is central to the IDF-DS source gate and to the post-outcome treatment of AMOVFLY waypoint semantics.

---

## IV. c-pKTES-Hedge

### A. Frozen live-test architecture

The final Phase 1.2R design uses

\[
3\text{ certainty units}+37\text{ probability-remainder units}=40\text{ live tests}.
\]

The three certainty units satisfy

\[
\pi_i=1.
\]

They are part of the probability design; they are not treated as convenience observations with undefined selection probability. Every non-certainty inferential unit must satisfy

\[
0<\pi_i<1,
\]

except where the frozen capped-inclusion algorithm naturally caps a probability-remainder unit at one. Such a unit retains probability-remainder identity because it arises from the frozen first-order probability construction rather than from deterministic sentinel assignment.

### B. Outcome-blind sentinel portfolio

The frozen sentinel portfolio is `NRR`:

1. one pure kernel-novelty sentinel;
2. two risk-aware sentinels combining novelty with a preoutcome auxiliary risk score.

Sequential maximin diversification discourages all three certainty slots from collapsing onto the same local region of feature space. No additional sentinel type is introduced in Phase 2.

### C. Probability-remainder hedge

For a non-certainty unit `i`, define kernel novelty `N_i` and a compound adverse-tail score `C_i` computed only from preoutcome operational covariates. The frozen score is

\[
z_i=0.80N_i+0.20C_i.
\]

Within each stratum, first-order probabilities are tilted through

\[
\pi_i\propto \exp\{3(z_i-\bar z_g)\},
