# KTES v8.3 — Virtual Page-Flow Audit

**Important:** this is a layout simulation, not a literal compiled-PDF page audit. A true page-by-page visual inspection is deferred until the exact IEEE periodical template is frozen and PDF generation is explicitly approved.

## Reading-order objective

A reviewer should encounter evidence in the following order:

1. problem and narrow claim;
2. probability-preserving design identity;
3. independent controlled confirmation;
4. layered external evidence;
5. validity/provenance interpretation;
6. limitations and next independent gate.

## Candidate two-column flow

### Opening spread

Title, abstract, Introduction, and Related Work should remain text dominant. No large figure is placed before the method is defined. This prevents the visual story from preceding the inferential contract.

### Method spread

Problem Formulation and c-pKTES-Hedge lead into Table I and Fig. 1. Table I carries exact frozen contract values; Fig. 1 carries architecture. The figure is intentionally full width because one-column scaling would violate the typography gate.

### Controlled-evidence spread

Evidence Protocol transitions directly to Results A. Fig. 2 is the first major result visual and should appear before or adjacent to Table II. The figure shows paired direction/uncertainty; Table II carries exact absolute values. This division avoids duplicating a full numeric table inside the graphic.

### External-evidence spread

Fig. 3 precedes Table III. The figure communicates that the three datasets terminate at different evidence states; Table III supplies the exact numerical result and machine-readable evidence class. Detailed Anti-UAV/AMOVFLY comparator tables remain in Supplement.

### Discussion spread

Fig. 4 opens or anchors Discussion. It should not be moved into Methods because it is an inference from the external evidence chain, not part of the sampling algorithm.

### Closing material

Limitations, next independent gate, Conclusion, and References should not be interrupted by a new result float. If Fig. 4 drifts to the closing page in the final template, shorten float queues rather than moving scientific results into the Discussion.

## Float-congestion risks

The manuscript contains four full-width figures and two clearly full-width main tables. Generic IEEE two-column LaTeX may defer `figure*`/`table*` floats to page tops. Risks:

- Fig. 2 and Table II may compete for the same top-float area.
- Fig. 3 and Table III may similarly queue.
- forcing exact positions can create large white gaps or reorder evidence.

Mitigation:

- allow one result table to move to the next top float if necessary;
- keep captions concise;
- keep Table I one column when legible;
- do not add new main-text tables;
- do not split Table III into multiple dataset-specific tables.

## Information-density audit

PASS after v8.3 figure redesign:

- no figure contains body text below ~9.23 pt at 7.16-in width;
- figure numbers/titles are no longer duplicated inside the artwork;
- Fig. 2 uses interval geometry instead of repeating Table II values;
- Fig. 3 uses three evidence cards instead of a six-column mini-table;
- Fig. 4 uses a gate chain with four short evidence lanes.

## Expected exact-review trigger

A literal page-by-page gate becomes mandatory only after the target journal/template is frozen. At that point inspect every page for:

- float order and orphan captions;
- column breaks through equations;
- table text below readable size;
- captions separated from graphics;
- reference spill/overfull boxes;
- excess white space caused by star-float queues;
- whether evidence-class labels wrap ambiguously.
