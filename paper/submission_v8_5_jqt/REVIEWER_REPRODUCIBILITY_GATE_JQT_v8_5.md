# JQT v8.5 Reviewer Reproducibility Gate

**Date:** 10 October 2026  
**Scientific evidence:** unchanged / frozen  
**Purpose:** reviewer-package integrity and anonymity only

## Decision

**PASS — COMPLETE BLINDED REVIEWER REPRODUCIBILITY ARCHIVE BUILT AND VERIFIED.**

The canonical reviewer archive is:

`JQT_REVIEWER_REPRODUCIBILITY_v8_5.zip`

SHA-256:

`77c55df8fdc39f46bffa1890a7c48445c1ee3316f3e6841fea8db190962354d0`

## Contents

The archive contains the two evidence layers required for review:

1. **Controlled confirmation**
   - R5 confirmation driver and chunk/finalization scripts;
   - recovered/frozen Phase 1.2R method dependencies;
   - R5 raw, paired, scenario, uncertainty, false-accept, and trade-off result tables.

2. **External validation**
   - Anti-UAV410 frozen design frame, State Accuracy input, realized design object, replay code/results, confidence-interval evidence, and execution clarification;
   - IDF-DS preoutcome source contract and source-gate stop record;
   - AMOVFLY design/endpoint freezes, replay result, endpoint-semantic audit, post-outcome sensitivity, provenance audit, and execution scripts;
   - frozen Phase 2 method/protocol records.

## Integrity audit

A single root checksum manifest covers all substantive files.

- checksum entries: **65**
- checksum verification: **65/65 PASS**
- checksum manifest self-reference: **absent**
- missing manifest targets: **0**
- digest mismatches: **0**

The previously generated Phase 2 evidence subarchive was independently rebuilt in GitHub Actions run `38017133001` after correcting a self-referential checksum-manifest defect. The verified Phase 2 subarchive contents matched the corresponding external-validation files in the complete reviewer archive byte-for-byte before the complete archive manifest was regenerated.

## Anonymity audit

The complete archive was scanned for the frozen identity-token set covering repository owner identifiers, author email patterns, public owner-specific GitHub links, and local user paths.

- identity scan: **0 hits**
- author names/affiliations/ORCIDs intentionally absent
- public identity-bearing project links intentionally absent

The archive itself is reviewer-safe under this scan. The **public GitHub or GitHub Actions URL is not reviewer-safe**, because the hosting location reveals repository ownership. The ZIP must therefore be distributed through an anonymous reviewer-access service or uploaded as an anonymous supplementary file if permitted by the journal portal.

## Relationship to the Phase 2 evidence artifact

GitHub Actions run `38017133001` generated the verified Phase 2 evidence subarchive:

- workflow result: **SUCCESS**
- outer artifact digest: `a7aefd32b8e25a2d103ea198cc5ff1f48aa43074ed0969f4a28317785171d053`
- inner Phase 2 reviewer ZIP digest: `e2862086c725599410308c200f25de9dad87f102779cb56311632f0918045f34`
- internal manifest: **35/35 PASS**
- identity scan: **0 hits**

This 89 KB artifact is a validated component of the complete 465 KB reviewer reproducibility package, not the final reviewer package by itself.

## Remaining action

No further reproducibility construction is required. The remaining action is logistical: place `JQT_REVIEWER_REPRODUCIBILITY_v8_5.zip` in an anonymous reviewer-facing location and insert that access reference into the submission system if requested.
