# Probability-Preserving Active Test Allocation Under Severe Live-Test Budgets: c-pKTES-Hedge with Layered External Validation

**Research manuscript v8 — Markdown evidence draft**  
**Evidence status:** Phase 1.2R R5 frozen; Phase 2A closed; IDF-DS source gate closed; AMOVFLY confirmatory numerical gate closed with endpoint-semantic limitation.  
**Document status:** research draft for adversarial review; not yet approved for DOCX/PDF submission packaging.

---

**Abstract**—Operational test and evaluation often has to infer population-level effectiveness and expose difficult operating conditions from only a few dozen live tests. Pure probability sampling protects inference but can miss rare or compound edge conditions, whereas deterministic edge-focused designs improve discovery at the cost of a weaker sampling basis for population estimation. We study a probability-preserving compromise, **c-pKTES-Hedge**, that combines three outcome-blind certainty sentinels with a 37-unit positive-inclusion-probability remainder at a live-test budget of 40. The probability remainder is enriched by kernel novelty and a frozen compound adverse-tail score, spatially spread with Local Cube sampling, and analysed with a stratum-wise Hajek model-assisted residual estimator and conservative design diagnostics. In an independent confirmation over 1000 finite populations spanning five simulator-discrepancy regimes, c-pKTES-Hedge attains 81.2% edge hit versus 77.9% for a 15-deterministic-plus-audit design; the paired edge-hit interval crosses zero, so no superiority claim is made. At the same time, profile, failure, and critical-tail mean absolute errors improve from 0.008348, 0.060399, and 0.020958 to 0.006824, 0.051746, and 0.016811, respectively, and definitive-correct decisions rise from 8.9% to 17.3%. External validation is deliberately fail-closed. On Anti-UAV410, all numerical guardrails pass, although profile error is modestly higher than stratified probability sampling by 0.00404 and the result is classified as **PASS_WITH_EXECUTION_CLARIFICATION**. A planned IDF-DS flight study is stopped before outcome opening because the public release cannot instantiate the preregistered flight-level preoutcome design frame. On AMOVFLY, all frozen numerical comparison gates pass, but a post-outcome semantic audit reveals systematic `(0,0)` waypoint placeholders that make the literal failure endpoint degenerate; the correct classification is therefore **NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION**. A post-outcome sensitivity using the immutable realized design object preserves the method-comparison conclusion but does not repair the primary endpoint. The evidence supports probability-preserving active enrichment as a viable small-budget test-allocation principle while showing that external validity depends jointly on source structure, endpoint semantics, and execution provenance.

**Index Terms**—balanced sampling, finite-population inference, Hajek estimator, Local Cube, operational test and evaluation, probability sampling, small-sample qualification, spatially balanced sampling, test allocation, uncertainty quantification.

---

## I. Introduction

### A. The small-budget T&E conflict

Operational test and evaluation (T&E) is rarely a pure prediction problem. The evaluator must decide where to spend a limited number of real-system trials and then use those trials to infer whether performance requirements are met over an operational population of conditions [15]. In the settings motivating this work, the relevant live-test budget is not hundreds or thousands of conditions but roughly **30–50 real tests**. That scale creates a conflict between two legitimate objectives.

The first objective is **population inference**. If the final decision concerns an operational-profile mean, failure probability, or critical-domain performance, then the real tests should retain a defensible probability-sampling interpretation [3]–[5]. Known inclusion probabilities make weighted finite-population estimation possible and prevent a small set of deliberately chosen difficult cases from being mistaken for a representative population sample.

The second objective is **difficult-condition discovery**. Equal-probability designs can spend too much of a small budget in densely populated central regions and miss rare, compound, or previously unenumerated edge conditions. In many safety- or mission-critical programs, failure to expose such conditions is itself an important test-design failure.

A common practical response is to split the budget: allocate a deterministic block to difficult conditions and reserve the remainder as a probability audit. This protects edge discovery but weakens the probability basis of the full live-test campaign. The alternative—keeping every unit in a simple equal-probability sample—protects inference but may leave too little active pressure toward the boundary.

This paper asks whether that trade-off can be softened without pretending that deterministic simulation runs are equivalent to live probability samples.

### B. Design principle

Our central design principle is simple:

> A small number of deliberately targeted live tests can coexist with population inference if those tests are treated as **certainty units with first-order inclusion probability one**, while the rest of the live campaign remains a positive-inclusion-probability probability sample.

This principle leads to **c-pKTES-Hedge**. At the frozen primary budget of 40 tests, three outcome-blind certainty sentinels have `pi=1`; the other 37 live tests are sampled with known, positive first-order inclusion probabilities. Their inclusion probabilities are tilted toward kernel novelty and compound adverse operational conditions, but retain a probability floor. Local Cube sampling is then used to spread and approximately balance the probability remainder in auxiliary-feature space while preserving the prescribed first-order probabilities.

The design is analysed with a stratum-wise Hajek model-assisted residual correction. Simulation, digital twins, or other model-based predictions enter only as wall-to-wall auxiliary information. Their run count is never converted into a live effective sample size. The final decision remains three-state—Accept, Reject, or Inconclusive—because small live-test campaigns should not be forced to produce definitive decisions when the evidence is weak.

### C. Why the evidence architecture matters

A method intended for T&E can fail in more ways than poor numerical accuracy. The source may not contain the preoutcome covariates needed to instantiate the promised design. An endpoint may be mathematically computable but semantically contaminated. A sampling algorithm may be reproducible in source code yet fail to regenerate the exact realized first-order inclusion probabilities on a different numerical backend. These are not implementation footnotes; they determine whether an external-validity claim is scientifically defensible.

We therefore separate four evidence layers:

1. **method development**, in which R1–R5 design choices are explored;
2. **independent controlled confirmation**, in which the final R5 design is frozen and evaluated on 1000 new finite populations;
3. **external real-data validation**, in which method constants are not retuned;
4. **execution and semantic audits**, which may narrow the claim even when numerical guardrails pass.

### D. Contributions

This study makes four contributions.

**C1 — Probability-preserving active enrichment.** We combine outcome-blind certainty sentinels with a positive-inclusion-probability remainder so that active difficult-condition targeting and finite-population inference remain parts of one sampling design rather than disconnected deterministic and audit samples.

**C2 — A small-N sampling-and-inference architecture.** The final design couples kernel novelty, a frozen compound adverse-tail hedge, a positive inclusion-probability floor, Local Cube spreading, stratum-wise Hajek model-assisted residual correction, conservative design diagnostics, and three-state decisions.

**C3 — Strict development/confirmation separation.** The novelty/compound mixture, tilt strength, sentinel count, estimator, and safety calibration are frozen before the R5 confirmation and are not retuned on Anti-UAV410, IDF-DS, or AMOVFLY.

**C4 — Layered external-validation evidence.** The three external studies end in three different scientifically meaningful states: numerical pass with execution clarification, preoutcome source-structure block, and numerical pass with an endpoint-semantic limitation. This makes the validation discipline part of the contribution rather than treating external validation as a binary performance score.

The resulting claim is deliberately narrower than “40 tests replace a large campaign.” We evaluate whether a probability-preserving active design can improve the **inference–edge-discovery trade-off** at small budget and whether that design logic survives independent data without outcome-driven redesign.

---

## II. Related Work

### A. Scenario-based validation and test allocation

Scenario-based validation is widely used when exhaustive physical testing is infeasible. In automated-driving safety evaluation, test-case sampling, accelerated evaluation, and importance sampling allocate computation or test effort toward rare and safety-relevant events [6]–[8]. These methods motivate the general idea that the test distribution need not equal the operational distribution if the inferential correction is explicit. Kernel-based distribution matching and sample-selection-bias correction provide related tools for representing a target population under nonuniform sampling [9], [10]. Our predecessor KTES study adapted this general logic to a weighted-effectiveness estimand; the present paper does not treat that predecessor design as the same algorithm as c-pKTES-Hedge.

The present study addresses a different and later-stage problem: a severe **live-test-count constraint**. The design objective is no longer only to reduce weighted-mean estimation error; it is to retain probability inference while recovering much of the difficult-condition discovery achieved by an explicitly deterministic edge block.

### B. Unequal-probability and balanced sampling

Unequal-probability sampling provides the natural framework for active enrichment without discarding known selection probabilities [5]. The cube method of Deville and Tille selects approximately balanced samples with equal or unequal inclusion probabilities while targeting auxiliary-total balance [1]. Spatially balanced and local pivotal designs extend the principle by discouraging the simultaneous inclusion of nearby units, improving sample spread in auxiliary or geographic spaces [2].

c-pKTES-Hedge uses these ideas operationally rather than claiming them as new sampling theory. The novelty lies in the T&E-specific composition: outcome-blind active scoring determines first-order inclusion probabilities, a small set of certainty units is retained explicitly, and Local Cube provides spreading/balance while preserving the probability identity of the remainder.

### C. Model-assisted finite-population inference

Model-assisted survey estimation uses a wall-to-wall predictor to reduce residual variance while retaining correction through a probability sample [4]. In our setting, a simulator or surrogate plays the role of auxiliary prediction, not a replacement for real tests. The estimator corrects prediction residuals within strata using the known live-test inclusion probabilities. This distinction is important because a large simulation campaign does not create a large live-test effective sample size.

The Hajek form is used for stability under unequal small-sample weights, while design weighting remains rooted in known first-order inclusion probabilities [3]–[5]. We do not claim exact finite-sample unbiasedness of the ratio correction. Instead, the controlled confirmation and external finite populations are used to evaluate error, coverage diagnostics, and decision behaviour directly.

### D. Small-sample qualification and abstention

Small-sample reliability and qualification problems often face a tension between decision power and false-accept control [16], [17]. A method that always produces a definitive decision can appear operationally efficient while hiding weak evidence. We therefore make **Inconclusive** an explicit legal outcome. Safety-facing calibration is frozen independently and is not retuned to reduce abstention in the confirmation or external studies.

### E. External validation as an evidence process

External validation is often described as applying a frozen model to a new dataset. Sampling designs require a stricter definition. The external source must provide enough **preoutcome unit-level information** to construct the design before the outcome is opened; the outcome must have an engineering or task semantics that can be defended independently of the numerical result; and the realized inclusion probabilities must be preserved as part of the execution record.

The Phase 2 program is organized around these requirements. A source can therefore be blocked before outcome access, or a numerically successful study can have its claim narrowed after a semantic audit.

---

## III. Problem Formulation

### A. Finite population and operational profile

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

Phase 2 freezes:

- `n=40`;
- three certainty sentinels;
- 37 probability-remainder identities;
- 80/20 novelty/compound mixture;
- `rho=0.20`;
- `lambda=3`;
- probability floor implementation;
- Hajek model-assisted estimator;
- `max(GS,PWR)` variance diagnostic;
- R3 safety calibration;
- Accept/Reject/Inconclusive logic.

If an external source cannot instantiate the preoutcome frame, the study stops rather than substituting outcome-derived covariates. If an endpoint is found to have a post-outcome semantic defect, the original result is retained and the claim is narrowed; a sensitivity analysis cannot be promoted to a new confirmation.

### D. Anti-UAV410 task-effectiveness pilot

Anti-UAV410 is an infrared UAV-tracking benchmark with 410 videos [11]. Phase 2A uses the official 120-sequence test split as a finite population and the default SiamFC tracker as the frozen system under test. The primary outcome is per-sequence State Accuracy `SA_i`. The live-test analogue selects 40 sequences.

Outcome-blind covariates are six official challenge indicators, four target-size indicators, and log sequence length. The mutually exclusive size strata contain 33 Tiny, 54 Small, 29 Medium, and 4 Normal sequences, with frozen allocation 11/17/10/2.

The replay protocol uses 500 paired design replays with seed block 20261001–20261500. Prespecified guardrails cover positive inclusion probabilities, probability-remainder ESS, profile-error non-inferiority to stratified probability sampling, critical-domain error, and difficult-case discovery.

### E. IDF-DS source-structure gate

IDF-DS is a published dataset of 240 autonomous fixed-wing flights using two avionics architectures [12], [13]. The preregistered Phase 2B design required flight-linked preoutcome mission/configuration/environment information before opening telemetry outcomes.

The public archive was therefore audited structurally before telemetry values were opened. The audit found archive-level mission plans but did not recover the required per-flight `mission.txt` and `parameters.csv` structure from the released archives. The SpeedyBee processed release exposed 111 lap identifiers rather than 120 intended flight units. Realized trajectories, speeds, flight durations, and telemetry values were prohibited as rescue covariates.

### F. AMOVFLY replacement engineering validation

AMOVFLY provides real UAV flight process data with flight-scenario labels and preoutcome route/configuration context [14]. A new independent protocol was frozen before telemetry-outcome opening. The confirmatory finite population contains 257 unique autonomous ready-data flight blobs across four scenario strata: FAFS 33, FAVS 165, VAFS 32, and VAVS 27, with `n=40` allocation 6/23/6/5.

The frozen literal primary endpoint is the proportion of waypoint episodes attaining an external 10 m reference radius. The 10 m value is an external reference threshold and is not asserted to be the historical configured AMOVFLY acceptance radius.

The confirmatory design object was hashed before downstream replay. A later post-outcome semantic audit and a separately labelled sensitivity analysis were required because of exact `(0,0)` waypoint placeholders.

---

## VI. Results

### A. R5 independent controlled confirmation

Table I summarizes the primary R5 versus Split15 comparison over 1000 independent finite populations.

**TABLE I. R5 independent confirmation, n=40.**

| Metric | c-pKTES-Hedge | Split15 | Paired difference | 95% CI |
|---|---:|---:|---:|---:|
| Edge hit | **0.812** | 0.779 | +0.033 | -0.0013 to +0.0673 |
| Profile MAE | **0.006824** | 0.008348 | -0.001525 | -0.002025 to -0.001024 |
| Failure MAE | **0.051746** | 0.060399 | -0.008653 | -0.012595 to -0.004711 |
| Critical-tail MAE | **0.016811** | 0.020958 | -0.004147 | -0.004798 to -0.003497 |
| Definitive correct | **0.173** | 0.089 | +0.084 | +0.0555 to +0.1125 |
| Abstain | 0.826 | 0.911 | -0.085 | -0.1135 to -0.0565 |

The edge-hit point estimate is higher for c-pKTES-Hedge, but its paired confidence interval crosses zero. The evidence therefore supports **no detected edge-discovery disadvantage at the reported precision**, not statistically significant superiority.

The stronger result is inferential. Profile, failure, and critical-tail errors are all lower under c-pKTES-Hedge, and definitive-correct decisions increase while abstention falls. This is the trade-off that R5 was designed to achieve: recover much of the active edge pressure of Split15 while retaining probability-preserving population inference.

### B. Hidden-bias boundary and false acceptance

Under `hidden_bias`, edge hit is 0.770 for c-pKTES-Hedge and 0.795 for Split15. The paired difference is -2.5 percentage points with 95% CI -10.17 to +5.17 percentage points. This closes the earlier R3/R4 simulator-blind weakness without establishing dominance over the deterministic split design.

Across 945 true-Reject populations in the R5 confirmation, zero false accepts are observed. This is consistent with low observed false-accept risk under the frozen confirmation distribution but is not interpreted as proof that the true false-accept probability is zero or as a distribution-free operational guarantee.

### C. Frozen safety-UQ audit

The R3 calibration is applied to the same R5 campaigns without changing the point estimator. Failure marginal coverage rises from 94.9% to 99.0%, and safety upper-bound coverage from 97.1% to 99.9%. Definitive-correct and abstention rates are unchanged in this confirmation because other constraints already dominate final status for the campaigns whose failure bounds widen.

This result is evidence about the frozen confirmation set, not a theorem that wider failure bounds are cost-free in every domain.

### D. Anti-UAV410 external validation

Table II gives the 500 paired-replay Phase 2A result.

**TABLE II. Anti-UAV410 Phase 2A, 500 paired replays.**

| Method | Profile error mean | Critical-domain error mean | Difficult-case hit | Probability-component ESS median |
|---|---:|---:|---:|---:|
| c-pKTES-Hedge | 0.03007 | **0.04893** | 1.000 | 33.12 |
| Stratified-SRS | **0.02603** | 0.05911 | 0.996 | 39.71 |
| Split15+Audit25 | 0.03049 | 0.06109 | 1.000 | 24.27 |

c-pKTES-Hedge is **not uniformly better**. Its profile error is higher than stratified SRS by 0.00404, with paired 95% CI 0.00137 to 0.00671. The increase remains inside the frozen +0.01 non-inferiority guardrail. By contrast, critical-domain error is lower than both comparators; the c-pKTES-minus-SRS difference is -0.01018 with 95% CI -0.01230 to -0.00806.

All numerical guardrails pass under the disclosed execution adapter. The directly frozen c-pKTES/SRS components include positive-inclusion support, the probability-remainder ESS diagnostics, and the +0.01 profile-error non-inferiority gate. The critical-domain and Split15 difficult-case guardrails are comparator-sensitive because the exact 15+25 Split15 adapter and finite-domain estimator required execution clarification after `SA_i` recovery. The probability-remainder ESS median is 33.12 and its fifth percentile is 32.60, both well above the frozen thresholds of 18.5 and 12. No non-certainty inclusion-probability failure occurs.

The correct classification is nevertheless **PASS_WITH_EXECUTION_CLARIFICATION**. The exact numerical Split15 adapter and finite-domain critical-domain estimator were instantiated after `SA_i` recovery, although the c-pKTES constants, endpoint, covariates, strata, allocation, seed block, and gate thresholds were unchanged. The result is therefore stronger than an exploratory reanalysis but weaker than a pristine preregistered pass.

### E. IDF-DS stops at the source gate

IDF-DS does not produce a method-performance result. Before opening telemetry outcomes, the source audit finds that the public archives cannot instantiate the preregistered flight-level outcome-blind design frame. The only identified mission plan is an archive-level constant shared across the two architecture archives, and the released structure does not provide the expected flight-specific mission/configuration files at the required resolution.

Using realized GPS paths, speed, flight duration, wind histories, or other telemetry to manufacture a design frame after seeing the release would convert the external dataset into a development source. The study is therefore classified **BLOCKED_SOURCE_STRUCTURE — INSUFFICIENT PREOUTCOME COVARIATE RESOLUTION**.

This is not a KTES performance failure. It is evidence that external validation can legitimately terminate before outcome analysis when the source cannot support the promised sampling design.

### F. AMOVFLY confirmatory numerical result

AMOVFLY supplies the strongest engineering-facing external comparison. Table III reports the frozen numerical result for the literal 10 m waypoint-attainment endpoint.

**TABLE III. AMOVFLY confirmatory numerical result.**

| Method | Profile error Y10 | Critical-domain error Y10 | Difficult-case hit | Probability ESS median |
|---|---:|---:|---:|---:|
| c-pKTES-Hedge | 0.003784 | **0.033764** | 1.000 | 35.224 |
| Stratified-SRS | 0.004543 | 0.066201 | 1.000 | 39.276 |
| Split15+Audit25 | **0.003637** | 0.080011 | 1.000 | 23.019 |

All five frozen numerical gates pass. The paired KTES-minus-SRS profile-error difference is -0.0007586 with 95% CI -0.0011638 to -0.0003534. Critical-domain error is also lower for KTES than either comparator.

The numerical result alone would support a confirmatory pass. The endpoint audit changes the interpretation.

### G. AMOVFLY endpoint-semantic limitation

Under the frozen literal parser, the population mean is `Y10=0.946105` and the flight-level failure indicator `F10=I(any waypoint episode >10 m)` equals one for every flight.

A post-outcome read-only semantic audit finds:

- every one of the 257 flights contains at least one exact `(0,0)` `aim_lat/aim_long` episode;
- 378 exact-zero episodes occur in total;
- exactly 378 episodes have minimum actual-to-aim distance greater than 100 km;
- every >100 km episode is an exact-zero episode;
- no non-zero target produces a >100 km episode.

The literal `F10` endpoint is therefore degenerate and cannot support failure-rate qualification. The bounded `Y10` endpoint is also materially influenced by the placeholder semantics.

The confirmatory numerical result is not deleted or silently repaired. Its final classification is

> **NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION.**

### H. Post-outcome frozen-design sensitivity

A separately labelled sensitivity excludes exact `(0,0)` episodes while loading the immutable confirmatory design object rather than regenerating inclusion probabilities.

After the diagnostic exclusion, population `Y10` changes to 0.982243 and `F10` to 0.459144. Under the unchanged frozen design and replay seeds, the KTES-minus-SRS profile-error difference remains favourable at -0.0004107 with 95% CI -0.0006379 to -0.0001834. Critical-domain error is 0.03342 for KTES versus 0.06468 for SRS and 0.07928 for Split15. All five numerical comparison gates remain satisfied.

This supports robustness of the **method-comparison conclusion** to the identified placeholder. Because the exclusion rule is post outcome, it does not replace the primary confirmatory endpoint and does not rescue the original failure-rate interpretation.

### I. Realized-design reproducibility audit

A later hosted-runner attempt to regenerate the AMOVFLY design from the same source code, declared Python/NumPy/SciPy/Pandas versions, input frame, constants, and seeds fails the exact design-object hash check. Standardization statistics, kernel bandwidth, source hashes, seed lineage, and certainty sentinels match, but 254 of 257 first-order inclusion probabilities differ by more than `1e-12`. The maximum absolute difference is 0.0108412, and an example Local-Cube selected set changes.

No tolerance is relaxed. The low-level numerical backend responsible for the drift was not isolated. Downstream sensitivity analysis instead consumes the immutable realized design object from the successful confirmatory run.

This produces an additional practical result:

> for floating-point unequal-probability designs, the realized vector of first-order inclusion probabilities and deterministic design identities is part of the research object; source code, package versions, and random seeds alone may be insufficient execution identity.


### J. Cross-evidence summary

Table IV separates numerical performance from evidence class. The same method can therefore have a favorable numerical comparison without receiving an unrestricted validation label.

**TABLE IV. Cross-evidence summary.**

| Evidence set | Primary role | c-pKTES result | Key boundary | Final evidence class |
|---|---|---|---|---|
| R5, 1000 controlled populations | independent method confirmation | lower profile/failure/tail MAE; edge hit statistically compatible with Split15 | controlled DGPs | Confirmatory controlled evidence |
| Anti-UAV410 | external task-effectiveness transfer | all numerical guardrails satisfied; profile +0.00404 vs SRS within +0.01 bound | Split15/domain-estimator execution clarification | PASS_WITH_EXECUTION_CLARIFICATION |
| IDF-DS | planned engineering source gate | no performance result | preregistered flight-level preoutcome frame not recoverable from public release | BLOCKED_SOURCE_STRUCTURE |
| AMOVFLY | external real-flight sampling comparison | all frozen numerical comparison gates satisfied | systematic `(0,0)` waypoint placeholders contaminate literal endpoint | NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION |

---

## VII. Discussion

### A. What the controlled evidence supports

The R5 confirmation supports c-pKTES-Hedge as a **probability-preserving active test allocation** rather than as a universally optimal sampler. At n=40, the design keeps edge discovery at approximately the Split15 level while improving profile, failure, and critical-tail inference and increasing definitive-correct decisions in the frozen finite-population confirmation.

The important mechanism is not the presence of three deliberately targeted points by itself. It is the preservation of known first-order probabilities for the rest of the campaign. This lets the live tests continue to serve a population-inference role rather than separating the campaign into a large deterministic discovery block and a small audit whose effective sample size is too limited to support the desired estimands.

### B. What transported to external data

Two independent real-data settings support transport of the sampling/inference logic, but neither provides a clean field-certification claim.

Anti-UAV410 shows that the frozen design can move to an unrelated task-effectiveness population without weight collapse. The result is not uniformly favourable—SRS has lower profile error—but the frozen non-inferiority guardrail passes and KTES has lower critical-domain error. This is a useful result precisely because it preserves an unfavourable dimension instead of selecting only metrics that favour the new method.

AMOVFLY provides stronger numerical support: profile error relative to SRS and critical-domain error are both lower. Yet the endpoint-semantic audit prevents us from treating that numerical pass as clean engineering qualification. The external evidence therefore supports the **design comparison**, not the literal interpretation of every executed endpoint.

### C. A source can fail before the algorithm is tested

The IDF-DS study illustrates a different external-validity boundary. The published article describes a rich 240-flight telemetry benchmark, but the public archive structure available to the frozen protocol does not expose the expected unit-linked preflight design information at the required resolution. The scientifically attractive shortcut would be to derive mission difficulty from realized trajectories or telemetry. That shortcut would also invalidate the confirmatory design because the selection frame would then be outcome-derived.

Stopping before outcome opening is therefore a positive research result. It demonstrates that external validation has a **source-eligibility gate**, not merely a numerical performance gate.

### D. Endpoint semantics are part of validity

AMOVFLY demonstrates that a mathematically bounded endpoint can be numerically stable and still be semantically compromised. The exact `(0,0)` waypoint episodes were not random extreme errors; they formed a systematic placeholder mechanism that generated every >100 km target-distance episode. Once discovered, the correct response is not to erase them and rerun the confirmation under a more attractive endpoint. The original result must remain visible, and any repaired definition becomes post-outcome sensitivity evidence.

This distinction matters in engineering T&E because performance thresholds often originate in interface semantics, operational doctrine, or system configuration rather than statistical convenience. A future independent confirmation should freeze an endpoint whose semantics are externally verified before outcome opening.

### E. Realized design objects should be frozen artifacts

The AMOVFLY reproducibility audit exposes a rarely documented issue in unequal-probability numerical sampling. The same source code, versions, seeds, and frame did not regenerate identical first-order probabilities on a later hosted runner. The mechanism was not isolated, but the consequence is clear: when downstream estimators depend on `pi_i`, a numerically close reconstruction is not automatically the same research design.

For confirmatory work, the realized design object should therefore be hashed and archived before outcomes are opened. Downstream analyses should consume that object directly. This requirement is analogous to freezing a trained model artifact rather than relying on a training script and seed to recreate exactly the same floating-point model later.

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

The R5 confirmation contains 1000 independent finite populations, 200 under each of five discrepancy scenarios.

### A.2 Anti-UAV410

Primary external-validation evidence:

- `external_validation/PHASE2A_500_REPLAY_RESULT_v8.md`;
- `external_validation/PHASE2A_CI_EVIDENCE_v8.md`;
- `external_validation/PHASE2A_DESIGN_OBJECT_v8.json`;
- `data/anti_uav410_test_design_frame_v8.csv`;
- `data/anti_uav410_siamfc_SA_i_v8.csv`.

Classification: `PASS_WITH_EXECUTION_CLARIFICATION`.

### A.3 IDF-DS

Primary source-gate evidence:

- `external_validation/PHASE2B_PREOUTCOME_FREEZE_v8.md`;
- `external_validation/PHASE2B_SOURCE_GATE_v8.md`.

Classification: `BLOCKED_SOURCE_STRUCTURE` before telemetry outcome opening.

### A.4 AMOVFLY

Primary engineering evidence:

- `external_validation/AMOVFLY_DESIGN_FREEZE_v8.md`;
- `external_validation/AMOVFLY_ENDPOINT_PERFORMANCE_FLOOR_FREEZE_v8.md`;
- `external_validation/AMOVFLY_EXTERNAL_VALIDATION_RESULT_v8.md`;
- `external_validation/AMOVFLY_WAYPOINT_SEMANTIC_AUDIT_v8.md`;
- `external_validation/AMOVFLY_ZERO_PLACEHOLDER_SENSITIVITY_v8.md`;
- `external_validation/AMOVFLY_NUMERICAL_REPRODUCIBILITY_AUDIT_v8.md`.

Classification: `NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION`.

### A.5 Reproducibility rule

For downstream analysis, a realized unequal-probability design is identified by its immutable, hashed design object. Recalculation from source code, package versions, and seeds is not accepted as the same design unless the design-object hash matches exactly.
