
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
