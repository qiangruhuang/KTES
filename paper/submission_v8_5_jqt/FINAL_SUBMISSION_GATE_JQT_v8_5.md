# JQT v8.5 Final Submission Gate

**Date:** 10 October 2026  
**Target:** *Journal of Quality Technology*, Regular Research  
**Scientific evidence:** frozen; no experiment, endpoint, comparator, threshold, evidence class, or claim ceiling reopened

## Decision

**TECHNICAL SUBMISSION PACKAGE PASS; AUTHOR-OWNED METADATA AND ANONYMOUS REVIEWER-ACCESS LOCATION REMAIN.**

The reviewer-facing scientific manuscript has passed the existing 50/50 submission audit. Artwork, the full-manuscript template, and the complete blinded reviewer-reproducibility package have also passed their technical gates.

## Canonical reviewer-facing package

- `MANUSCRIPT_JQT_v8_5_BLINDED.md`
- `SUPPLEMENTARY_INFORMATION_JQT_v8_5_BLINDED.md`
- `FIGURE_CAPTIONS_JQT_v8_5.md`
- `figures/figure1.eps` through `figures/figure4.eps`
- complete verified reviewer archive `JQT_REVIEWER_REPRODUCIBILITY_v8_5.zip`

The complete reviewer archive contains controlled R5 confirmation code/results plus all three Phase 2 external-study evidence paths. Its SHA-256 is `77c55df8fdc39f46bffa1890a7c48445c1ee3316f3e6841fea8db190962354d0`. A single root checksum manifest covers 65 substantive files and verifies 65/65; identity scan returned zero hits under the frozen scan rules.

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

## Reviewer reproducibility gate

The complete reviewer archive was rebuilt after an independent audit found that the earlier Phase 2 subarchive checksum manifest included itself. The Phase 2 builder was corrected and rerun before final package assembly.

**Verified Phase 2 subarchive**
- reviewer-evidence workflow run: `38017133001` — SUCCESS
- builder correction commit: `721fa91d5bbc255fb9dfeb93a3b99cb0cc279cd0`
- inner Phase 2 ZIP SHA-256: `e2862086c725599410308c200f25de9dad87f102779cb56311632f0918045f34`
- manifest: 35/35 PASS, self-reference absent
- identity scan: 0 hits

**Complete reviewer archive**
- file: `JQT_REVIEWER_REPRODUCIBILITY_v8_5.zip`
- SHA-256: `77c55df8fdc39f46bffa1890a7c48445c1ee3316f3e6841fea8db190962354d0`
- controlled-confirmation content present: PASS
- Anti-UAV410 / IDF-DS / AMOVFLY content present: PASS
- root checksum manifest: 65/65 PASS
- missing targets / mismatches: 0 / 0
- identity scan: 0 hits

The archive itself is reviewer-safe under this audit. Its storage/distribution location must also preserve anonymity, so the public GitHub/GitHub Actions location cannot serve as the reviewer-facing URL.

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
8. anonymous reviewer-access URL or portal location for the already-verified complete reproducibility ZIP;
9. confirmation that all authors approve the submission and it is not under consideration elsewhere;
10. literal verification of any live portal-only fields or limits immediately before submission.

No additional scientific analysis is required to satisfy the current JQT first-submission gate.
