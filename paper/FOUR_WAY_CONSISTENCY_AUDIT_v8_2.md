# KTES v8.2 Four-Way Consistency Audit

**Scope:** figure ↔ table ↔ prose ↔ claim consistency after submission compression  
**Frozen evidence source:** `PAPER_IEEE_v8.md`, SHA-256 `710702c979036957cc00ad5b385965802331175d9d1d71d2f1573ca5c81e4bc1`  
**Decision:** **PASS AFTER ONE PRESENTATION-ONLY CORRECTION**

## 1. Structural checks

- Main figures: **4/4 present**.
- Main tables: **3/3 present**.
- Detailed Anti-UAV and AMOVFLY comparator tables: moved to Supplement.
- Detailed post-outcome sensitivity: moved to Supplement and explicitly retained as diagnostic rather than confirmation.
- Evidence manifests / hashes: moved to Supplement except for the realized-design provenance rule needed in the main argument.
- No R1–R5 method constant, external endpoint, replay result, or evidence class was changed.

## 2. Four-way evidence matrix

| Claim | Figure | Main table | Main prose | Supplement | Audit result |
|---|---|---|---|---|---|
| `n=40`, 3 certainty + 37 positive-π remainder | Fig. 1 | Table I | Sec. IV | S1–S2 | PASS |
| `rho=0.20`, `lambda=3` frozen before confirmation | Fig. 1 | Table I | Sec. IV–V | S1–S2 | PASS |
| R5 edge hit 0.812 vs 0.779; CI crosses zero | Fig. 2 | Table II | Sec. VI.A | S3 | PASS; no superiority language |
| R5 profile/failure/critical-tail MAE improve | Fig. 2 | Table II | Sec. VI.A | S3 | PASS |
| Anti-UAV profile error is worse than SRS by +0.00404 but inside +0.01 bound | Fig. 3 | Table III | Sec. VI.B | S4 | PASS; adverse result remains visible |
| Anti-UAV evidence class | Fig. 3 | Table III | Sec. VI.B | S4 | PASS: `PASS_WITH_EXECUTION_CLARIFICATION` |
| IDF-DS produces no performance result | Fig. 3/4 | Table III | Sec. VI.B / VII.B | S5 | PASS |
| IDF-DS evidence class | Fig. 3/4 | Table III | Sec. VI.B | S5 | PASS: `BLOCKED_SOURCE_STRUCTURE` |
| AMOVFLY profile comparison favours KTES numerically | Fig. 3 | Table III | Sec. VI.B | S6 | PASS |
| AMOVFLY exact-zero placeholder invalidates unrestricted endpoint claim | Fig. 3/4 | Table III | Sec. VI.B / VII.B | S7–S8 | PASS |
| AMOVFLY evidence class | Fig. 3 | Table III | Sec. VI.B | S7 | PASS: `NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION` |
| Post-outcome exact-zero exclusion is diagnostic only | not promoted to a main performance panel | n/a | Sec. VI.B | S8 | PASS |
| Realized design object is part of confirmatory identity | Fig. 1/4 | Table I | Sec. VI.B / VII.B | S9–S10 | PASS |

## 3. Presentation-only inconsistency found and corrected

The first v8.1 Fig. 3 asset used the shortened AMOVFLY label `NUMERICAL PASS WITH ENDPOINT-SEMANTIC LIMITATION`, whereas the frozen evidence class is `NUMERICAL CONFIRMATORY PASS WITH ENDPOINT-SEMANTIC LIMITATION`. The same figure also omitted the two profile-error 95% confidence intervals required by the frozen figure blueprint.

This was corrected in the deterministic figure builder before v8.2 freeze:

- Anti-UAV: profile Δ vs SRS `+0.00404`, 95% CI `[0.00137, 0.00671]`;
- AMOVFLY: profile Δ vs SRS `-0.0007586`, 95% CI `[-0.0011638, -0.0003534]`;
- AMOVFLY class restored to the exact frozen wording containing `CONFIRMATORY`.

No underlying analysis changed.

## 4. Adverse-evidence preservation check

The compressed main paper still states all five reviewer-critical adverse findings:

1. R5 edge-hit CI crosses zero.
2. Hidden-bias does not establish edge superiority.
3. Anti-UAV profile error is higher than SRS by +0.00404.
4. IDF-DS stops before performance analysis.
5. AMOVFLY's literal failure endpoint is degenerate; the post-outcome sensitivity cannot repair the primary confirmation.

The realized-design regeneration failure is also retained in the main paper because it motivates the provenance gate rather than serving as execution trivia.

## 5. Compression integrity

The source manuscript contains 6,568 word-like tokens by the same local counting rule; the v8.2 main manuscript contains approximately 3,618, a reduction of about 45% while preserving the frozen quantitative claims. Detailed evidence is relocated rather than deleted.

## 6. Final decision

**PASS AFTER ONE PRESENTATION-ONLY CORRECTION.**

The v8.2 manuscript is internally consistent across figure, table, prose, and claim layers. The remaining work is journal formatting and external reviewer feedback, not additional method development or result generation.
