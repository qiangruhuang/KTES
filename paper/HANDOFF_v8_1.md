# KTES v8.1 Submission-Presentation Handoff

## Current state

The research-method layer remains frozen at v8. The submission-presentation gate has now been audited separately and classified:

**PASS WITH REQUIRED PRESENTATION RESTRUCTURING**.

No new experiment, retuning or endpoint change was performed.

## Newly frozen presentation assets

- `FIGURE_TABLE_BLUEPRINT_v8.md`
- `SUPPLEMENT_STRUCTURE_v8.md`
- `PRESENTATION_GATE_AUDIT_v8.md`
- `figures/FIG1_METHOD_ARCHITECTURE_v8.svg`
- `figures/FIG2_R5_CONFIRMATION_v8.svg`
- `figures/FIG3_EXTERNAL_EVIDENCE_v8.svg`
- `figures/FIG4_VALIDITY_GATES_v8.svg`
- `scripts/build_v8_submission_figures.py`

## Canonical figure execution

The repository figure builder is now fail-closed through GitHub Actions.

- workflow: `Rebuild v8 submission figures`;
- run: `37582703568`;
- trigger commit: `1ee820ce136af9448df943e9ac411cf4651a3b25`;
- canonical generated-figure commit: `857ba09` (`paper: rebuild canonical v8 submission figures`);
- validation: all four SVG files were regenerated from `scripts/build_v8_submission_figures.py`, confirmed non-empty, and parsed successfully as XML before commit.

The committed SVGs should therefore be treated as generated presentation artifacts, not hand-edited sources. Future figure revisions must be made in the builder and regenerated through the same workflow.

## Main-paper visual storyline

1. **Method:** 3 outcome-blind certainty sentinels + 37 positive-π probability-remainder units.
2. **Controlled confirmation:** edge discovery remains statistically compatible with Split15 while inferential errors improve.
3. **External evidence:** Anti-UAV, IDF-DS and AMOVFLY yield different evidence classes for legitimate reasons.
4. **Validity synthesis:** source structure, endpoint semantics and realized design provenance are separate gates before an engineering claim is allowed.

## Next manuscript action

Create a submission-compressed Markdown revision from `PAPER_IEEE_v8.md` that:

- inserts the four frozen figure assets;
- reduces the main paper to three tables;
- moves execution manifests, detailed external comparator tables and sensitivity mechanics to Supplementary Information;
- preserves every adverse result and evidence label exactly.

Do not modify the frozen method or rerun outcomes during this editing step.
