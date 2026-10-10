# KTES v8.5 JQT — GitHub Submission Provenance

**Freeze date:** 10 October 2026  
**Branch:** `paper/jqt-v8.5`  
**Scientific evidence state:** frozen; no experiment, endpoint, comparator, threshold, evidence class, or claim ceiling reopened

## 1. Initial canonical materialization

The JQT v8.5 text package was first materialized fail-closed on GitHub.

- canonical materialization commit: `30b2af5305a1f62c54c76a41bb5bfe60301a7225`
- materializer workflow run: `38002786906`
- conclusion: **SUCCESS**

The materializer verified the blinded manuscript, Supplement, title-page template, cover letter, BibTeX, submission audits, and neutral-name figure copies against the frozen transport payload before writing them to the branch.

## 2. Artwork and full-template gates

- EPS artwork workflow run: `38006438769` — **SUCCESS**
- EPS canonical commit: `4fc03a303aad2526fba8f62e3fd4416e55cc578f`
- final full-template assembly workflow: `38017648177` — **SUCCESS**

The full manuscript template is mechanically assembled from the canonical blinded scientific body plus the current title-page template. Changes to the title page do not alter the blinded scientific body.

## 3. Final author-side submission-package export

The export workflow was revised to trigger whenever any canonical submission input changes, preventing stale title-page/full-template content from surviving in a previously exported ZIP.

- export workflow correction commit: `10d6c377365d31cea0b8cd8ad4a0867e45f2f5c5`
- final export workflow run: `38017778082` — **SUCCESS**
- outer GitHub artifact digest: `3d2d0211af8a2269fe3a6753e75b187d6cad23a031e155cb69e1fa2bf5170ec9`
- canonical inner `JQT_v8_5_SUBMISSION_PACKAGE.zip` digest: `e294a1293dafcad7bf681eaa652a667a608e311c77b3f4d4b3f3d7d6e06dd2c0`
- package checksum manifest: **11/11 PASS**
- current title page contains complete reviewer-archive digest: **PASS**
- current full template contains complete reviewer-archive digest: **PASS**

This is the canonical author-side submission package before insertion of author-owned metadata.

## 4. Blinded reviewer-evidence correction and verification

An independent audit of the first Phase 2 reviewer-evidence artifact found one packaging defect: `SHA256SUMS.txt` included itself, so its own listed hash could not be stable. No scientific file mismatch was found.

The builder was corrected to exclude the checksum manifest from itself and to execute `sha256sum -c` before archiving.

- correction commit: `721fa91d5bbc255fb9dfeb93a3b99cb0cc279cd0`
- rebuilt Phase 2 reviewer-evidence run: `38017133001` — **SUCCESS**
- outer workflow-artifact digest: `a7aefd32b8e25a2d103ea198cc5ff1f48aa43074ed0969f4a28317785171d053`
- inner Phase 2 ZIP digest: `e2862086c725599410308c200f25de9dad87f102779cb56311632f0918045f34`
- internal manifest: **35/35 PASS**
- identity scan: **0 hits**

The verified Phase 2 files were byte-compared with the external-validation layer of the complete reviewer reproducibility bundle and matched file-for-file.

## 5. Complete reviewer reproducibility archive

The canonical reviewer-facing reproducibility archive is:

`JQT_REVIEWER_REPRODUCIBILITY_v8_5.zip`

SHA-256:

`77c55df8fdc39f46bffa1890a7c48445c1ee3316f3e6841fea8db190962354d0`

It contains:

- controlled R5 confirmation driver, method dependencies, raw/summary/scenario/paired/UQ/false-accept outputs;
- Anti-UAV410 design frame, primary input, realized design object, replay code/results and execution clarification;
- IDF-DS preoutcome contract and source-gate record;
- AMOVFLY design/endpoint records, numerical result, semantic audit, sensitivity and provenance audit;
- frozen Phase 2 protocol/method records.

Final package checks:

- root checksum entries: **65**
- root checksum verification: **65/65 PASS**
- missing targets: **0**
- mismatches: **0**
- checksum-manifest self-reference: **absent**
- reviewer identity scan: **0 hits**

The archive content is anonymous under the frozen scan rules. The public GitHub/GitHub Actions hosting location is still identity-bearing and must not be used as the reviewer-facing access URL.

## 6. Submission-state interpretation

The technical submission package is now complete. Remaining blockers are author-owned or portal-logistical only:

- authors/order, affiliations, corresponding-author details and ORCIDs;
- Funding, competing interests, Acknowledgments and CRediT;
- author approval/originality/concurrent-submission confirmation;
- anonymous hosting or portal upload of the already-verified complete reviewer archive;
- literal verification of live portal-only constraints immediately before submission.

No additional scientific analysis is required for the current JQT first-submission gate.
