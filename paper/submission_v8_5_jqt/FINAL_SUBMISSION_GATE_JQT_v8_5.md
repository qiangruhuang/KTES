# JQT v8.5 Final Submission Gate

**Date:** 10 October 2026  
**Target:** *Journal of Quality Technology*, Regular Research  
**Scientific evidence:** frozen; no experiment, endpoint, comparator, threshold, evidence class, or claim ceiling reopened

## Decision

**TECHNICAL SUBMISSION PACKAGE PASS; AUTHOR-OWNED METADATA AND BLINDED ARCHIVE REMAIN.**

The reviewer-facing scientific manuscript has passed the existing 50/50 submission audit. The final packaging pass additionally closes the artwork-format and full-manuscript-template gaps.

## Canonical reviewer-facing package

- `MANUSCRIPT_JQT_v8_5_BLINDED.md`
- `SUPPLEMENTARY_INFORMATION_JQT_v8_5_BLINDED.md`
- `FIGURE_CAPTIONS_JQT_v8_5.md`
- `figures/figure1.eps` through `figures/figure4.eps`
- blinded reproducibility archive to be instantiated from `BLINDED_REPRODUCIBILITY_MANIFEST_v8_5.md`

## Editorial-office package

- `MANUSCRIPT_JQT_v8_5_FULL_TEMPLATE.md` — mechanically assembled from the title-page template and the canonical blinded body; author fields remain explicit placeholders
- `TITLE_PAGE_JQT_v8_5.md`
- `COVER_LETTER_JQT_v8_5.md`

## Journal-format checks

Current JQT/Taylor & Francis guidance was rechecked on 10 October 2026:

1. JQT uses double-anonymized peer review.
2. A full manuscript with author details and a separate anonymous manuscript are required for double-anonymous workflows.
3. Figures must be separate files and anonymized for review.
4. Taylor & Francis recommends EPS for line art; the four frozen SVG masters were exported to EPS without scientific edits.
5. JQT scope explicitly includes methodological quality/reliability work with practical applicability in military and government operations.

## Artwork gate

- EPS workflow run: `38006438769` — SUCCESS
- EPS canonical commit: `4fc03a303aad2526fba8f62e3fd4416e55cc578f`
- EPS files use neutral reviewer-facing names and passed identity scanning.
- SVG masters remain unchanged as reproducibility/production sources.

## Full-manuscript assembly gate

- Assembly workflow run: `38006704041` — SUCCESS
- Template commit: `516d5fd9e2968053506a22ca6a5071e36f54cb49`
- The assembled template contains the title-page author placeholders plus the exact canonical scientific body.

## AI-use disclosure gate

Taylor & Francis currently permits uses including language refinement and coding assistance, requires transparent disclosure of generative-AI use, and requires human verification and responsibility. It also states that generative AI must not replace core author responsibilities or create an unreviewed first draft.

The current disclosure therefore remains explicit about ChatGPT (OpenAI, GPT-5.6 Sol), editorial/language assistance, consistency/reference-format checks, coding assistance, human verification, and full author responsibility. Before submission, the authors must personally verify that this statement accurately describes their use and retain the earlier manuscript/research record if editorial clarification is requested.

## Scientific claim ceiling rechecked

The submission package does not claim:

- statistically significant R5 edge-discovery superiority;
- universal superiority to SRS or Split15;
- optimality of three sentinels;
- distribution-free uncertainty validity under arbitrary shift;
- a method-performance result from IDF-DS;
- clean AMOVFLY failure-rate qualification;
- live weapon-system certification.

It retains the Anti-UAV profile-error disadvantage, the hidden-bias boundary, the AMOVFLY endpoint-semantic defect, and the realized-`pi_i` regeneration drift.

## Mandatory human inputs before clicking Submit

1. final author order and names;
2. affiliations and corresponding-author details;
3. ORCID iDs;
4. Funding statement and grant numbers;
5. competing-interest disclosure;
6. Acknowledgments;
7. CRediT author-contribution statement;
8. reviewer-safe blinded reproducibility archive/link;
9. confirmation that all authors approve the submission and it is not under consideration elsewhere;
10. literal verification of any live portal-only fields or limits immediately before submission.

No additional scientific analysis is required to satisfy the current JQT first-submission gate.
