# JQT v8.5 Submission Readiness Gate

**Target journal:** *Journal of Quality Technology*  
**Article type:** Regular Research  
**Gate date:** 10 October 2026  
**Overall status:** **SCIENTIFIC/TEXTUAL SUBMISSION GATE PASS; AUTHOR-METADATA ACTIONS REMAIN**

## 1. Current JQT requirements verified

Checked against the current Taylor & Francis JQT pages and Taylor & Francis editorial policies on 10 October 2026.

- JQT publishes Regular Research articles developing and evaluating innovative analytical solutions to real industry, government, and societal quality/reliability problems.
- JQT explicitly includes practical applicability in military and government operations within scope.
- JQT uses **double-anonymized peer review**.
- JQT encourages demonstration on real data and code sharing for reproducibility.
- Recent JQT articles include separate disclosure, data-availability, funding, and generative-AI-use statements.
- Taylor & Francis requires generative-AI use to be disclosed with the tool/version, purpose, and author responsibility.
- Recent JQT publication style uses author–year citations; the v8.5 manuscript has therefore been converted from the inherited IEEE numeric style.

Sources checked:
- https://www.tandfonline.com/journals/ujqt20
- https://www.tandfonline.com/journals/ujqt20/about-this-journal
- https://taylorandfrancis.com/our-policies/ai-policy/
- https://authorservices.taylorandfrancis.com/editorial-policies/using-ai-in-your-research-and-manuscript-preparations/

The public JQT page does not expose every ScholarOne validation rule in machine-readable form. Exact upload-system constraints should therefore be rechecked literally at the final upload screen.

## 2. Completed manuscript gates

| Gate | Status | Evidence |
|---|---|---|
| Journal scope | PASS | Statistical/computational test-allocation method for quality/reliability under small budgets; government/military applicability explicitly within JQT scope |
| Article type | PASS | Regular Research is the correct category |
| Scientific evidence freeze | PASS | No new experiment, retuning, endpoint change, or evidence-class change in v8.5 |
| Main manuscript depth | PASS | ~6,700 word-like tokens before References; method, confirmation, external evidence, discussion all retained |
| Abstract | PASS | ~207 words, unstructured |
| Double anonymity | PASS | No author names, affiliations, public-repository owner, local paths, or internal version labels in blinded manuscript/Supplement |
| References | PASS | JQT-style author–year in-text citations and alphabetized author–year reference list |
| Figures / tables | PASS | 4 figures, 3 main tables, cited in order |
| Supplement | PASS | 10-section blinded Supplement with four supplementary tables |
| Reproducibility parameter | PASS | `min_probability_fraction=0.35` restored from frozen realized design object |
| Data/code statement | PASS | Anonymous review-stage wording in blinded manuscript |
| Generative-AI disclosure | PASS | Tool/version, permitted editorial/coding uses, verification, and human responsibility stated |
| Cover letter | PASS WITH AUTHOR CONFIRMATION | Scientific rationale complete; originality/concurrent-submission assertion left for human confirmation |
| Title page | TEMPLATE COMPLETE | All non-author fields prepared; author-owned metadata intentionally left blank |
| Automated submission audit | PASS | 50/50 checks |

## 3. Mandatory author actions before clicking Submit

These fields were deliberately not inferred from repository ownership or prior profile information.

1. Fill the final author order, affiliations, corresponding author, and ORCID iDs on `TITLE_PAGE_JQT_v8_5.md`.
2. Fill Funding, competing interests, Acknowledgments, and CRediT author contributions.
3. Confirm the cover-letter statement that the manuscript is original, not published previously, not under consideration elsewhere, and approved by all authors.
4. Prepare the blinded reproducibility archive defined in `BLINDED_REPRODUCIBILITY_MANIFEST_v8_5.md`, or upload equivalent anonymous supplementary code/data files through the submission system.
5. Remove author names, emails, affiliations, usernames, local paths, and public repository links from that blinded archive before upload.
6. At the ScholarOne upload screen, recheck any live word-limit, file-type, or figure-resolution rule that is not exposed on the public journal page.

## 4. Recommended upload set

**For reviewers**
- `MANUSCRIPT_JQT_v8_5_BLINDED`
- `SUPPLEMENTARY_INFORMATION_JQT_v8_5_BLINDED`
- four neutral-name figure files (`figure1`–`figure4`) if the system requests separate figures
- blinded reproducibility archive / anonymous supplementary code

**For editorial office only**
- `TITLE_PAGE_JQT_v8_5`
- `COVER_LETTER_JQT_v8_5`

The public project repository should not be linked in reviewer-facing files during double-anonymized review.

## 5. Gate decision

The manuscript itself is ready to move from manuscript development to literal submission packaging. No scientific reason remains to reopen the experiments for JQT submission.

**Decision: PASS FOR JQT SUBMISSION PACKAGING, conditional only on author-owned metadata and creation of the anonymous review archive.**
