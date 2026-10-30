# Data dictionary and grouping

All paths below are relative to the package. JSON order is preserved where it determines deterministic bootstrap choices.

| Path | Fields / semantics | Important boundary |
|---|---|---|
| `data/outcomes/priority.json`, `prefill.json` | `config_id` = workload instance; `cell_id` = controlled condition; `seed` = generation seed; `intervention_id` = fixed base/donor pair; `module_type`; base/treatment ANWG and difference | 10 independent workloads per condition, repeated pairs within workload |
| `data/outcomes/*_four_arm.json` | Same grouping plus four paired ANWG endpoints and `interaction` | `first` and `second` order does not change the interaction; stored endpoint names are preserved |
| `data/diagnostics/priority.json`, `prefill.json` | Matched configuration/intervention IDs; decision/order/key/queue diagnostic fractions or prefill action/request-change fractions; counts where historically saved; median absolute completion-time change | Aggregate diagnostic summaries, not per-request sequences; time changes here are simulated outcome summaries |
| `data/diagnostics/erasure_windows.json` | Window ID, source stratum, three repeated seeds, three `cells` containing pair, numerator, denominator | Count cells sum seeds; cannot recover individual seed trajectories from this projection |
| `data/diagnostics/public_replay.json` | Source, window index, rate, candidate/action/pressure/request-change ratios | Source/window is the resampling key; rate is dependent repeated treatment of that input window |
| `data/outcomes/kv.json` | Configuration, module/pair names; regime or elevated-axis count; shared stream index/seed; control/corrected treatment outcome and gain | Missing regime means use elevated-axis count; fixed conditions remain in the same stream block |
| `data/diagnostics/kv_compatibility.json` | Base/donor/module, historical flag, classification, evidence, required validation and use restriction | `INVALID`/`INCONCLUSIVE` cannot be upgraded by analysis success |
| `data/outcomes/metrics.csv` | Campaign/configuration, opaque workload/intervention/evaluation IDs, module/policy names, whole input-file SHA-256; five base/treatment/benefit-oriented differences and state | Whole-file hash is lineage, not a per-request cache/hash sequence; no source row location is disclosed |
| `data/reference/` | Frozen Stage 2A/2A2 numerical summaries and interpretation notes | Comparison targets, never bootstrapped as new observations |
| `data/figure_data/` | Frozen historic figure anchors; source paths and zero p-value fields removed | Some anchors have only aggregate support; use corrected outcome-generated erasure/KV figures |
| `provenance/` | Source commit, input hashes, explicit projections; claim status and algorithm origins | A source hash does not attest the simulator code actually executed |

`config_id` and source names are intentional reproducibility metadata, not paths or confidential service identifiers. Policy names denote project implementations/adaptations; they do not certify faithful native algorithms. Source-window indices identify selected experimental blocks without original record identities or row ranges.

The historical figure-data key `invariant` is retained only for correspondence with the frozen artifact; it means `ALL_NEAR_NULL`, not invariance under all metrics or equivalence. New figures use “All near null.”
