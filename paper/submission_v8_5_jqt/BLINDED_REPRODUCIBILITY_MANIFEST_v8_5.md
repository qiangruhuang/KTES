# Blinded Reproducibility Material — Submission Manifest

This file defines the material provided anonymously to editors/reviewers during double-anonymized review. The public project repository must not be linked from the blinded manuscript.

## A. Final method implementation

- c-pKTES-Hedge sampling design implementation
- Local Cube / local pivotal dependencies used by the frozen implementation
- Hájek model-assisted estimator implementation
- uncertainty / decision implementation
- environment or dependency specification sufficient to execute the frozen workflow

## B. Controlled confirmation

- R5 independent-confirmation driver / frozen method lineage
- frozen R3 uncertainty calibration constants and confirmation diagnostics
- provenance record for the recovered R5 implementation

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

The builder must:

- remove author names, emails, affiliations, ORCIDs, GitHub usernames, local machine paths, and repository-owner metadata;
- preserve scientific values, design hashes, endpoint definitions, result values, and public third-party dataset identifiers;
- use neutral package/file names;
- omit identity-bearing commit/repository links from reviewer-facing files;
- retain a private author-side crosswalk between blinded filenames and the canonical public repository for post-acceptance release.

## G. Verified v8.5 build

The blinded reviewer-evidence archive is now **built and technically verified**.

- GitHub Actions workflow run: `38017133001` — **SUCCESS**
- builder correction commit: `721fa91d5bbc255fb9dfeb93a3b99cb0cc279cd0`
- outer workflow-artifact digest: `a7aefd32b8e25a2d103ea198cc5ff1f48aa43074ed0969f4a28317785171d053`
- reviewer-facing inner ZIP: `JQT_REVIEWER_EVIDENCE_EXTERNAL_v8_5.zip`
- reviewer-facing ZIP SHA-256: `e2862086c725599410308c200f25de9dad87f102779cb56311632f0918045f34`
- identity-leak scan: **PASS / 0 hits** under the frozen identity-token rules
- checksum manifest: **35/35 PASS**
- checksum manifest self-reference: **absent by construction**

The technical archive-construction gate is therefore closed. The remaining review-access task is **distribution**, not bundle creation: the authors must place the verified ZIP in an anonymous reviewer-access channel or upload it as an anonymous supplementary file if the live journal portal permits this. The identity-bearing public GitHub Actions URL itself must not be used as the reviewer-facing link.
