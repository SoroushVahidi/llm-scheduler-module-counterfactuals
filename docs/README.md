# Documentation

Start with the [repository overview](../README.md) and the exact
[v0.2.0 release](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/releases/tag/v0.2.0).
This documentation supports reconstruction from saved observations; no private
manuscript or development checkout is needed to run the public analyses.

## Reproduction and interpretation

| Question | Guide |
|---|---|
| How do I install, verify and run the package? | [Quick start](../README.md#quick-start), [validation](validation.md) |
| Which commands produce a figure or table? | [Reproduction map](stage4c_reproduction.md), [supplement table matrix](supplement_table_matrix.csv) |
| What do cloned states and complete trajectories measure? | [Designs and reproduction scope](reproduction_scope.md) |
| What are the denominators, resampling units and statistical conventions? | [Statistical design](statistical_design.md), [additional observation definitions](recovered_data_dictionary.md) |
| Which findings are supported, partial or unavailable? | [Coverage and gaps](claim_coverage.md), [claim matrix CSV](../provenance/claim_matrix.csv) / [JSON](../provenance/claim_matrix.json) |
| What does the historical 63.7%/65.1% issue mean? | [Denominator clarification and release-time assessment](denominator_correction.md) |

## Data and provenance

| Resource | Contents |
|---|---|
| [Core data dictionary](data_dictionary.md) | Controlled outcomes, diagnostics, erasure, replay, KV and metric projections retained from v0.1.0. |
| [Stage4C dictionary](stage4c_data_dictionary.md) | Pilot, erasure extension, fidelity counters and historical real-engine summaries added in v0.2.0. “Stage4C” is a retained collection name, not a required external workflow. |
| [Recovered-observation dictionary](recovered_data_dictionary.md) | Additional controlled probes, fairness, held-out, prospective and classification counts. |
| [Implementation and workload provenance](provenance.md) | Analysis origins, input transformations and workload attribution. |
| [Provenance index](../provenance/README.md) | Source hashes, claim registers and immutable release manifests. |
| [Exclusions](exclusions.md) | Restricted inputs, unavailable evidence and redistribution boundaries. |

## Version history and citation

- [v0.2.0 release notes](RELEASE_v0.2.0.md) and [extension scope](stage4c_scope.md)
  describe the October 30 release snapshot. Historical manuscript wording and
  coverage decisions are scoped to that snapshot, not later manuscript revisions.
- [v0.1.0](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/releases/tag/v0.1.0)
  remains the earlier outcome-reconstruction release.
- [Citation metadata](../CITATION.cff), [code/documentation license](../LICENSE),
  [data license](../LICENSE-DATA), and [third-party notices](../THIRD_PARTY_NOTICES.md)
  specify attribution and reuse.

Later documentation changes do not replace published archives, expand release
coverage, or change the numerical inputs, analysis code or statistical methods.
