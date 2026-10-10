# Blinded Reproducibility Material — Submission Manifest

This file defines the material provided anonymously to editors/reviewers during double-anonymized review. The public project repository must not be linked from the blinded manuscript.

## A. Final method implementation

- c-pKTES-Hedge sampling design implementation
- Local Cube / local pivotal dependencies used by the frozen implementation
- Hájek model-assisted estimator implementation
- uncertainty / decision implementation
- environment or dependency specification sufficient to execute the frozen workflow

## B. Controlled confirmation

- R5 independent-confirmation driver and chunk/finalization scripts
- frozen/recovered Phase 1.2R method dependencies
- 1000-population raw/summary/scenario/paired result tables
- frozen R3 uncertainty calibration constants and uncertainty/false-accept diagnostics

## C. Anti-UAV410 external study

- 120-sequence outcome-blind design frame
- per-sequence State Accuracy input
- realized c-pKTES-Hedge design object
- 500-replay execution script
- replay summary, paired replay output, confidence-interval evidence, and ESS-supporting output
- execution-clarification note

## D. IDF-DS source gate

- preoutcome source-structure protocol
- source eligibility audit
- source-gate decision record showing that outcome evaluation stopped before telemetry-based rescue

## E. AMOVFLY external study

- frozen design and endpoint records
- primary numerical comparison result
- waypoint endpoint-semantic audit
- post-outcome exact-zero diagnostic sensitivity, clearly labelled non-confirmatory
- realized-design regeneration / provenance audit
- scripts and summary outputs needed to inspect the frozen external study

## F. Review-package anonymization

The complete bundle must:

- remove author names, emails, affiliations, ORCIDs, GitHub usernames, local machine paths, and repository-owner metadata;
- preserve scientific values, design hashes, endpoint definitions, result values, and public third-party dataset identifiers;
- use neutral package/file names;
- omit identity-bearing commit/repository links from reviewer-facing files;
- retain a private author-side crosswalk between blinded filenames and the canonical public repository for post-acceptance release.

## G. Canonical complete reviewer archive

The canonical reviewer-facing archive is:

`JQT_REVIEWER_REPRODUCIBILITY_v8_5.zip`

SHA-256:

`77c55df8fdc39f46bffa1890a7c48445c1ee3316f3e6841fea8db190962354d0`

Final integrity audit:

- controlled R5 confirmation content present: **PASS**
- Anti-UAV410 content present: **PASS**
- IDF-DS source-gate content present: **PASS**
- AMOVFLY content present: **PASS**
- checksum manifest entries: **65**
- checksum verification: **65/65 PASS**
- missing checksum targets: **0**
- checksum mismatches: **0**
- checksum-manifest self-reference: **absent**
- identity scan: **0 hits** under the frozen review-anonymity token rules

## H. Phase 2 evidence builder provenance

The Phase 2 evidence component was independently rebuilt after a packaging audit identified a self-referential checksum manifest in an earlier archive.

- GitHub Actions run: `38017133001` — **SUCCESS**
- builder correction commit: `721fa91d5bbc255fb9dfeb93a3b99cb0cc279cd0`
- outer workflow-artifact digest: `a7aefd32b8e25a2d103ea198cc5ff1f48aa43074ed0969f4a28317785171d053`
- inner Phase 2 reviewer ZIP digest: `e2862086c725599410308c200f25de9dad87f102779cb56311632f0918045f34`
- Phase 2 checksum verification: **35/35 PASS**
- Phase 2 identity scan: **0 hits**

The Phase 2 component was byte-compared against the external-validation layer of the complete reviewer archive before the complete root checksum manifest was regenerated.

## I. Remaining review-access action

The technical archive-construction gate is closed. The remaining action is distribution only: the authors must place `JQT_REVIEWER_REPRODUCIBILITY_v8_5.zip` in an anonymous reviewer-access channel or upload it as an anonymous supplementary file if the live journal portal permits this.

The archive itself passed the anonymity scan, but the identity-bearing public GitHub/GitHub Actions hosting URL must not be used as the reviewer-facing link.
