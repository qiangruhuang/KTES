# Blinded Reproducibility Material — Submission Manifest

This file defines the material that should be provided anonymously to editors/reviewers during double-anonymized review. The public project repository should not be linked from the blinded manuscript.

## A. Final method implementation

- c-pKTES-Hedge sampling design implementation
- Local Cube / local pivotal dependencies used by the frozen implementation
- Hájek model-assisted estimator implementation
- uncertainty / decision implementation
- environment or dependency specification sufficient to execute the frozen workflow

## B. Controlled confirmation

- R5 independent-confirmation driver
- the 1000-population confirmation result table
- paired confidence-interval output
- frozen R3 uncertainty calibration constants and confirmation diagnostics

## C. Anti-UAV410 external study

- 120-sequence outcome-blind design frame
- per-sequence State Accuracy input
- realized c-pKTES-Hedge design object
- 500-replay execution script
- replay summary, confidence-interval evidence, and ESS output
- execution-clarification note

## D. IDF-DS source gate

- preoutcome source-structure protocol
- source eligibility audit
- source-gate decision record showing that outcome evaluation stopped before telemetry-based rescue

## E. AMOVFLY external study

- frozen 257-flight analysis frame
- realized sampling-design object
- primary numerical comparison result
- waypoint endpoint-semantic audit
- post-outcome exact-zero diagnostic sensitivity, clearly labelled non-confirmatory
- realized-design regeneration / provenance audit

## F. Review-package anonymization

Before upload:

- remove author names, emails, affiliations, ORCIDs, GitHub usernames, local machine paths, and repository-owner metadata;
- preserve scientific file hashes and design-object hashes when they do not identify authors;
- use neutral package/file names;
- do not include commit links that reveal repository ownership;
- retain a private crosswalk between blinded filenames and the canonical public repository for post-acceptance release.
