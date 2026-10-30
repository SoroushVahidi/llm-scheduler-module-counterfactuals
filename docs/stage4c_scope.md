# Stage4C additions retained in v0.2.0

This release extends v0.1.0 (`484aba68a02709006e6b824d6734cfeb69ecd056`), anchored to the reviewed
25-page manuscript commit `a93e5c0b8d69f39ead656b5c808d82e3f958922f`. The final release is v0.2.0.

Coverage is the unweighted fraction of 48 explicitly enumerated principal
empirical claim families in `provenance/claim_matrix.json` whose named
numerical finding can be recalculated from included observations, counts or
ratios with the listed commands. Repeated prose/abstract claims count once;
methods, hypothetical examples, literature and administrative status do not
count. A family containing an unsupported component gets no partial credit.
R means saved-output numerical reconstruction; F means frozen/partial evidence;
M means no adequate public supporting artifact. A frozen answer or a hash of
withheld inputs is not numerical reconstruction. These are claim-family
coverage percentages, not percentages of paper pages, raw data or validity.

v0.1.0: 14/48 = 29.17%.
Unpublished Stage4C baseline: 23/48 = 47.92%.
v0.2.0: 36/48 = 75.00%. Original-execution reproduction
for these experimental families is **0/48** in this package; no simulator or
model execution environment is distributed. Native serving-engine validity
is not established by any coverage percentage.

Added observations: the seven original synthetic pilot fixtures and both saved
batches; 126 erasure seed-unit counts; 10,773 fidelity unit counters; 756 prefill
units with 15 overlapping view/stratum rows each; ten priority-retry arm-group
means; and 15 v3 pair-level latency differences. No trajectories are regenerated.
The pilot's synthetic observations are the original pilot, not replacement
demonstrations for trace-derived experiments.

Pairing JSON contains historical audit assertions plus result hashes. Counting
false flags is possible; independently comparing withheld input vectors is
not. Retry flags were privately compared again in Stage4C; v3 flags come from
the preserved Stage4A remote audit. The positive latency contrasts remain
saved numerical observations and do not restore identical-input causality.
Do not pool their different estimands, hardware, models or treatments.

Dynamic/pre-fill state equality, determinism and isolation were checked against
saved raw records privately; public counters permit aggregation, not rerunning
those state checks. No unseen-workload guarantee or native Scorpio/vLLM/Sarathi
fidelity follows. Six fairness-context mismatches and all excluded candidates
remain visible.

Current coverage and unresolved families are documented in [claim_coverage.md](claim_coverage.md). Recovered observations resolve held-out inference, controlled multiplicity, prospective per-window/source correlations, standalone fairness and the historical quartile definition. C11 remains partial due to the documented denominator discrepancy. Raw third-party inputs and private Git history are excluded. No DOI is assigned.
