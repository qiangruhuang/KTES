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
