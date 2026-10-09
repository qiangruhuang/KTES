# KTES v8.4 Writing Revision Audit — Expanded JQT Draft

**Source:** frozen `PAPER_IEEE_v8_3.md` / v8.3 evidence package  
**Revised manuscript:** `PAPER_JQT_v8_4.md`  
**Target:** *Journal of Quality Technology* (Regular Research)  
**Scientific state:** frozen; manuscript architecture and exposition only

## 1. Revision objective

The first JQT rewrite compressed the main text too aggressively. The expanded v8.4 restores the methodological and evidential logic required for a full methods paper without reopening any experiment.

The central argument is:

> Under a hard physical-test budget, difficult-case discovery and finite-population inference need not be split into statistically disconnected campaigns. c-pKTES-Hedge embeds a small certainty portfolio inside an unequal-probability design, preserving a large inferential probability remainder while directing tests toward novel and adverse conditions.

## 2. Writing frameworks applied

- **anti-defensive-writing:** the paper is organized around the strongest defensible contribution rather than around a chronology of failures and audits.
- **nature-writing:** the paper follows problem -> exact gap -> method logic -> independent confirmation -> external transport -> bounded implication.
- **nature-polishing:** section jobs, evidence placement, paragraph necessity, claim/evidence/boundary alignment, terminology, and sentence economy were checked before line-level polish.
- **integrity constraint:** evidence that changes the interpretation remains in the main text. R5 edge non-superiority, Anti-UAV profile cost, IDF-DS source stop, AMOVFLY endpoint contamination, and realized-design drift are not hidden.

## 3. Expansion relative to the first JQT draft

The main text is now approximately **6,590 words before References**, with a **207-word abstract**.

The added content is not repeated audit material. It restores:

1. the four-part design conflict motivating the method;
2. the role of certainty sentinels inside a probability design;
3. the rationale for novelty, adverse-tail weighting, probability floors, Local Cube spreading, and Hájek model-assisted correction;
4. the three-state uncertainty/decision logic;
5. an operational six-stage implementation contract;
6. the R1–R5 design evolution and what each stage resolved;
7. the purpose of the independent 1000-population confirmation and its metrics;
8. the exact role of the three external studies;
9. a fuller interpretation of why the method improves the inference-discovery trade-off;
10. JQT-facing practical implications for quality and reliability test planning.

Pure provenance listings, file hashes, detailed post-outcome sensitivity tables, and repeated external audit mechanics remain in Supplementary Information.

## 4. Main-text evidence allocation

| Evidence | Function | Main-text treatment |
|---|---|---|
| R1–R5 development | method rationale | restored as a concise design-evolution subsection |
| R5 1000-population confirmation | primary evidence | full main Results + Table 2/Fig. 2 |
| R5 UQ/decision behavior | necessary support | restored in main Results |
| hidden-bias edge result | claim boundary | retained in main Results |
| Anti-UAV design strata/ESS/non-inferiority | external support | restored in main Results |
| IDF-DS source failure | transport boundary | retained, without treating it as performance failure |
| AMOVFLY numerical comparison | external support | retained |
| AMOVFLY endpoint audit | interpretation-changing boundary | retained |
| exact-zero exclusion sensitivity | robustness only | remains Supplementary / diagnostic |
| realized `pi_i` drift | reproducibility implication | retained and interpreted |
| detailed artifact hashes/run IDs | provenance detail | Supplement/repository only |

## 5. Anti-defensive-writing application

Defensive repetition remains removed. Formal evidence-class labels appear in Table 3, not repeatedly in the Abstract, Discussion, and Conclusion. The manuscript now foregrounds the method's positive contribution before introducing boundaries.

At the same time, no conclusion-changing adverse result was deleted or softened beyond what the evidence permits.

## 6. Nature-writing / polishing application

- Title now states the actual capability and trade-off.
- Abstract contains one central claim, decisive controlled evidence, and one bounded external implication.
- Introduction defines the gap as a methodological conflict, not the absence of c-pKTES-Hedge.
- Methods explain motivation -> mechanism -> inferential role for each component.
- Results use claim-first subsections.
- Discussion synthesizes mechanism, quality/reliability implications, transport conditions, and reproducibility.
- Conclusion does not introduce new limitations or new claims.
- Em-dash prose and marketing language are avoided.

## 7. Frozen-science audit

The expanded manuscript passed **23/23 automated checks**.

Verified items include:

- `n=40`, 3 certainty sentinels, and 37 probability-remainder units;
- `rho=0.20`, `lambda=3`, and both R3 calibration constants;
- all R5 primary numerical results and paired intervals;
- no edge-superiority claim;
- Anti-UAV profile disadvantage and ESS values;
- IDF-DS explicitly has no method-performance result;
- AMOVFLY numerical result and `(0,0)` endpoint defect;
- realized-design drift `254/257`, max difference `0.0108412`;
- all three formal external evidence classes;
- four figures and three main tables;
- all 17 references cited in the main manuscript;
- abstract under 250 words;
- no universal-superiority language or banned self-weakening phrasing.

**Expanded manuscript SHA-256:** `1a4fec05538eb2ab74d7884b2b0f38d96b09d2de3088c935d46beb2d973b3d2c`

## 8. Remaining submission inputs

Only author/submission-specific items remain:

- blinded repository or reviewer archive;
- author list, affiliations, corresponding author and ORCIDs;
- conflict-of-interest statement;
- funding statement;
- literal Taylor & Francis/JQT submission formatting and final rendered inspection.

No new analysis is required for these items.
