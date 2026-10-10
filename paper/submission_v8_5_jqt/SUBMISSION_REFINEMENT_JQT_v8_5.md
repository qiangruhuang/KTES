# JQT v8.5 Submission Refinement Record

**Date:** 10 October 2026  
**Target:** *Journal of Quality Technology*, Regular Research  
**Scientific evidence:** frozen; no experiment, endpoint, comparator, threshold, evidence class, or claim ceiling reopened.

## Final reviewer-facing refinements

1. The keyword set was reduced to five JQT-facing terms:
   - active sampling
   - finite-population inference
   - reliability evaluation
   - small-sample qualification
   - test allocation
2. A dedicated `Advice to practitioners` subsection was added to the Discussion. It states when the method is appropriate, what must be frozen before testing, how weight stability should be checked, when a source/endpoint gate should stop execution, and why the realized inclusion-probability object must be archived.
3. The former `Boundaries and next test` subsection was renumbered to 5.7 without changing its scientific content.
4. The full manuscript template is mechanically synchronized with the canonical blinded body.

## GitHub fail-closed gates

- Practitioner refinement workflow run `38013875889`: **SUCCESS**.
- Full-template assembly workflow run `38013888085`: **SUCCESS**.
- Blinded reviewer-evidence workflow:
  - run `38013936611`: failed before execution because of workflow syntax; no reviewer artifact was produced;
  - run `38013974867`: assembled evidence but failed identity-leak scanning; no reviewer artifact was produced;
  - run `38014053578`: **SUCCESS** after identity-only redaction in reviewer copies. Scientific numbers, hashes, endpoints, and third-party dataset identifiers were preserved.
- Initial canonical export run `38014260128`: manuscript content checks passed, but local independent inspection found that `SHA256SUMS.txt` had included itself.
- Corrected export workflow run `38014400041`: **SUCCESS**, including internal `sha256sum -c SHA256SUMS.txt`.

## Canonical manuscript state

- Blinded manuscript: approximately **6,913 word-like tokens before References**.
- Abstract: **207 word-like tokens**.
- Keywords: **5**.
- Main figures: **4**.
- Main tables: **3**.
- Blinded manuscript SHA-256: `9b6d7680687df5f48e28836a59883903804ea24432868f8bf1f91e76285b5deb`
- Full-template SHA-256: `9af77bd2370975e295f2803f254a70e6a771243bdcd4370532e37e7686acfdd8`
- Canonical submission ZIP SHA-256: `30adf436e603b9aa135f78a267c07e3eb9fd5013bd5f7ad65b4922c7bcc1c2fd`

## Anonymous reviewer reproducibility package

A separate reviewer-only reproducibility archive was constructed from the frozen R5 handoff lineage plus the identity-redacted Phase 2 evidence artifact.

- File count: **67**
- Size: **475,125 bytes**
- SHA-256: `fe4a54c7bba69dc384ef2d99c2cba531fe019c783b60ee8e08ed3129eb17fbb5`
- Identity scan: **PASS**
- The archive is intentionally **not committed to the public GitHub repository**, because doing so would expose repository ownership during double-anonymized review.

The archive contains the controlled R5 confirmation code/results and the Phase 2 method, Anti-UAV410, IDF-DS, and AMOVFLY design/result/audit materials needed for reviewer inspection. Raw third-party benchmark archives are not redistributed.

## Scientific claim ceiling

Unchanged. The submission does not claim:

- statistically significant R5 edge-discovery superiority;
- universal superiority to SRS or Split15;
- optimality of three sentinels;
- distribution-free uncertainty validity under arbitrary shift;
- a method-performance result from IDF-DS;
- clean AMOVFLY failure-rate qualification;
- live weapon-system certification.

The reviewer-facing manuscript retains the R5 edge interval crossing zero, Anti-UAV profile-error disadvantage, hidden-bias boundary, IDF-DS source stop, AMOVFLY endpoint-semantic defect, and realized-`pi_i` regeneration drift.

## Remaining author-owned inputs

Before literal portal submission, the authors must still provide/confirm:

1. final author order and names;
2. affiliations and corresponding-author information;
3. ORCID iDs;
4. funding and grant numbers;
5. competing-interest disclosure;
6. acknowledgments;
7. CRediT roles;
8. all-author approval and confirmation that the manuscript is not under consideration elsewhere;
9. any ScholarOne/Taylor & Francis portal-only fields and live validation rules.

**Gate decision:** `UPLOAD-READY EXCEPT AUTHOR-OWNED METADATA AND LIVE PORTAL FIELDS`.
