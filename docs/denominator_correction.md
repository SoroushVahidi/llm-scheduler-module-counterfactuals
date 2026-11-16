# C11: trajectory denominators and the historical release assessment

The manuscript snapshot reviewed for the October 30, 2026 v0.2.0 release described approximately 63.7% of overrides as unclassifiable. The historical saved calculation is 232,011 unknown classifications / 364,302 actionable trajectory steps = **63.68644696%**. There are 7,725 final-divergent steps and 356,577 overrides, so unknown / overrides is **65.06617084%**.

Both values are computed from 168 pair-window files (56 windows × 3 pairs), each containing three saved seeds. The public file retains counts only; input states, IDs and event times are excluded. The extraction sums stored event classification labels; it does not rerun the classifier or certify the underlying state comparison. All three per-pair count totals independently match the archived analysis. Local stage counts retain zero unknown labels.

## Release-time assessment

The historical number has not been replaced. The release reports both denominators and assigns no full claim-as-written coverage to C11. Suggested manuscript correction, for author review only: “The trajectory comparison leaves approximately 63.7% of actionable steps unclassifiable (65.1% among overrides).” No manuscript or PDF was modified.

## Later manuscript clarification

The later manuscript explicitly distinguishes approximately **63.7% of actionable
steps** from **65.1% among overrides**. The suggested wording above is therefore
historical, not an outstanding correction to that later text.

This clarification does not retrospectively revise the published release audit:
C11 remains partial in the unchanged [v0.2.0 claim matrix](../provenance/claim_matrix.csv),
and coverage remains **36/48 claim families**. No new observations, execution
attestations, or classifier validation are supplied by a wording change. Both
ratios remain reproducible with `python analysis/reconstruct.py --output output/recovered`.
