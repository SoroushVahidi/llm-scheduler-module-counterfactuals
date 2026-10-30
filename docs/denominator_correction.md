# Explicit denominator discrepancy: C11

The reviewed manuscript says approximately 63.7% of overrides are unclassifiable. The historical saved calculation is 232,011 unknown classifications / 364,302 actionable trajectory steps = **63.68644696%**. There are 7,725 final-divergent steps and 356,577 overrides, so unknown / overrides is **65.06617084%**.

Both values are computed from 168 pair-window files (56 windows × 3 pairs), each containing three saved seeds. The public file retains counts only; input states, IDs and event times are excluded. The extraction sums stored event classification labels; it does not rerun the classifier or certify the underlying state comparison. All three per-pair count totals independently match the archived analysis. Local stage counts retain zero unknown labels.

The historical number has not been replaced. The release reports both denominators and assigns no full claim-as-written coverage to C11. Suggested manuscript correction, for author review only: “The trajectory comparison leaves approximately 63.7% of actionable steps unclassifiable (65.1% among overrides).” No manuscript or PDF was modified.
