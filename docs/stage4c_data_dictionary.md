# Added data dictionary and units

All CSVs are UTF-8 with header rows. Counts and seeds are integers; rates and
latency means are finite decimal values. Null rates are undefined, never zero.
Experimental grouping keys are project IDs, not production request/session IDs.

| File | Fields and unit | Interpretation |
|---|---|---|
| `fixtures.json` | Seven original cases, generated request integers, arrivals, service lengths, capacity and expected schedules | Entirely synthetic; elementary schedule oracle input |
| `pilot*.json` | `records`: original base/donor events, completions, A/B/C diagnoses; `cost`; allowlisted provenance | Two saved deterministic batches, not 14 independent cases; synthetic state sequences are safe here |
| `erasure_units.csv` | `family,window,seed,actionable,erased` | 126 rows; each pair/window has 3 identical seed counts; collapse to42 cells before inference |
| `dynamic_units.csv` | `unit,candidate,family,window,seed,states,reachable,agree` | 10773 unique units; candidate x window-rate x seed; zero reachability has undefined fraction |
| `dynamic_candidates.json` | candidate ID, family, base/donor, classification, context/semantic notes | 72 inventory candidates;57 tested;15 excluded; exclusions are not perfect agreement |
| `prefill_units.csv` | same unit keys plus `view,stratum,states,agree` | 11340 rows from756 units and15 overlapping view/stratum combinations, never add all rows as independent states |
| `prefill_candidates.json` | Four modeled prefill candidates with context limits | Common post-admission input boundary; identical stateless component |
| `v3_pair_audit.json` | 15 pair IDs; three equality booleans; arm request/failure counts; two raw result SHA256s; absolute mean TTFT difference in ms | Saved pair differences; equality flags are historical assertions; no input length vectors |
| `priority_arm_means.csv` | seed, LOW/HIGH, control/treatment high-priority TTFT means in ms, low-priority TTFT cost in ms | 10 regime/seed rows representing20 arms; low-priority cost is treatment minus control |
| `priority_pair_audit.json` | 10 pairs, equality flags, completion/failure counts, result hashes | Public assertions privately rechecked; raw vectors withheld |
| `prospective_summary.json` | Saved H1/H2/H4/secondary summaries | Frozen evidence only;140 primary unit-rate windows after seed aggregation |
| `predictive_model_scores.json` | Task/model test scores and recorded group-CI metadata | No individual predictions; reselecting best saved scores is not recomputing performance |
| `data/reference/stage4c*.json` | Frozen historical comparison targets | Separate from observation inputs; never fabricated observations |

Erasure intervals resample the18 positive windows within each family, using
Python `random.Random(424243)`, 10000 means and sorted indices250/9750.
They apply to positive-cell means, not pooled events; three zero windows per
family remain reported. Shared windows, rates and deterministic seeds are
dependent. Original erasure retains its own56-window complete-frame bootstrap.

Dynamic pooled agreement is sum(agree)/sum(reachable); positive-unit mean is
the mean of agree/reachable over positive units. Fairness uses the complete
context-dependent ranking comparator. Standard prefill captures64 initial
states/unit; active census caps5000; first64-active is an overlapping subview.

v3: H_s=abs(mean TTFT treatment-high - control-high) minus the analogous low
difference. Retry: H_s=(control-treatment high-priority mean TTFT)_HIGH minus
the analogous LOW benefit. Both average five seed contrasts. Frozen one-sided
bootstrap uses10000 resamples, seed424242: sorted lower index499 for v3 and500
for retry (historical implementations differ). Neither repairs input mismatch.

Additional frozen summaries: `original_erasure_taxonomy_summary.json` retains
original ambiguity and stage classifications; `kv_pairwise_summary.json` retains
historical corrected pairwise summaries. Historical labels such as synergistic
are recorded labels, not endorsed native synergy or an improvement claim.
The erasure IQR convention remains unresolved as described in the scope.
