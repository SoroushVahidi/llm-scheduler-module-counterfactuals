# Module Counterfactuals for Attributing LLM Serving Scheduler Effects

[Release v0.2.0](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/releases/tag/v0.2.0) provides code and eligible project-generated observations for reconstructing saved numerical analyses. **36/48 claim families (75.00%)** are reconstructible, compared with 14/48 in v0.1.0 and 23/48 in the unpublished Stage4C candidate. The [complete coverage matrix](provenance/claim_matrix.csv) gives commands, units, provenance and limitations for every family. Frozen summaries and partially supported claims receive no credit.

This is model-conditional research on scheduler module substitutions, opportunities to act, downstream disagreement erasure, request consequences and interactions. Saved-output reconstruction does not reproduce the original experiment executions or establish native serving-engine validity. No GPU, model service, credentials or private repository access is needed. No DOI has been assigned.

## Run the complete reconstruction

Tested with CPython 3.12.3. Install dependencies before disconnecting from the network, then run from the repository or extracted archive root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/verify_manifest.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/reproduce.py --output output
python scripts/figures.py --results output/results.json --output output/figures
python scripts/reproduce_stage4c.py --output output/stage4c
python scripts/supplementary_counts.py --output output/supplementary
python analysis/reconstruct.py --output output/recovered
```

These commands analyze saved records and generate numerical tables, checked figure views and JSON results. They do not simulate new trajectories or run model inference. The existing v0.1.0 data, scientific analysis and portable tests remain intact. See [table/figure instructions](docs/stage4c_reproduction.md), [statistical design](docs/statistical_design.md), [new data dictionary](docs/recovered_data_dictionary.md), and [validation](docs/validation.md).

## Included evidence

| Directory | Contents |
|---|---|
| `data/outcomes`, `data/diagnostics`, `data/figure_data` | Original controlled priority/prefill, four-arm, erasure, replay, metric and exploratory KV projections; historical figure anchors are references |
| `data/stage4c` | Original synthetic equal-information pilot, erasure-extension counts, dynamic/prefill fidelity counters, fairness mismatches, real-engine summaries and limited pairing assertions |
| `data/recovered` | Controlled priority probes, standalone fairness outcomes, held-out observations, replay/KV four-arm outcomes, prospective per-seed counts, local and trajectory stage counts |
| `analysis`, `scripts`, `src` | Portable statistical reconstruction and original pilot oracle; no experimental runners |
| `data/reference` | Frozen comparison targets, clearly separate from reconstruction inputs |
| `tests` | Numerical, grouping, integrity and deliberate-corruption checks |
| `provenance` | All 48 claims, field/source records, SHA-256 manifests and file-level redistribution review |
| `docs` | Experimental units, methods, limitations, figure/table mapping and release notes |

Experimental grouping IDs identify research units, not production requests. Do not pool overlapping projections as independent observations. Seed averages, source windows, repeated replay rates and fixed intervention families have distinct roles documented in the dictionaries.

## Findings and limitations

The historical quartile convention is now established from source code: the sorted observation at `floor(q*(n−1))`. Standalone fairness and prospective source mappings are recovered. The prospective correlation improvement remains inconclusive: Δr = 0.054504, bootstrap interval [−0.019731, 0.183897].

**A denominator discrepancy is explicitly preserved:** the manuscript's 63.7% unclassifiable trajectory figure divides by all actionable steps. Among overrides it is 65.1%. [Both calculations and the suggested wording correction](docs/denominator_correction.md) are provided; the manuscript has not been changed and this family receives no full coverage credit.

There is **no independently verified identical-input real-vLLM causal estimate** in this package. Matching trace hashes, seed flags or request counts cannot prove that the server received identical input vectors. The preserved audits report mismatches for 15 v3 and 10 priority-retry pairs; unavailable vectors prevent public rechecking. Historical latency arithmetic remains observable but does not establish causal pairing. KV compatibility labels and fidelity counters likewise do not establish native Scorpio/vLLM/Sarathi correctness.

Raw third-party traces, reconstructive token/time/cache sequences, source row mappings, request/session IDs, private logs, private communications and private Git history are excluded. Some original probe records, prediction vectors and execution attestations remain unavailable. See [all remaining gaps](docs/claim_coverage.md) and [exclusions](docs/exclusions.md). The fixed 48-family coverage denominator does not measure original-execution reproduction, which is 0/48 in this package.

## Licenses and citation

Project code and documentation are [MIT](LICENSE). Eligible project-generated numerical data and factual provenance are [CC BY 4.0](LICENSE-DATA). Preserve [upstream attribution](THIRD_PARTY_NOTICES.md). These licenses do not grant rights to Azure, BurstGPT or Mooncake raw traces. The original synthetic pilot fixtures are actual saved research inputs, not fabricated replacements for unavailable observations.

Cite `CITATION.cff` and the versioned release. [v0.1.0](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/releases/tag/v0.1.0) and its Git history remain available. The package describes research evidence, without asserting journal acceptance or current editorial status.
