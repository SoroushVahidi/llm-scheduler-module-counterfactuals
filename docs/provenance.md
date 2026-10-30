# Provenance and implementation lineage

Source development commit: `cf2200de16b6f6c0aabeaebc5a73de97f01feac2`. This private source identifier is retained for provenance, not offered as a publicly accessible checkout. `projection_lineage.json` maps the 22 explicit A/B input files to whole-file hashes, logical source IDs and field-removal transformations. The private builder retains exact internal paths; the public package needs none of them. `claim_register.json` distinguishes supported reconstruction from frozen evidence and historical limitations. Hash agreement identifies bytes; it does not attest native algorithm fidelity or the historical executed simulator version.

## Algorithm/source lineage

| Released implementation | Origin/version evidence | Changes and scope |
|---|---|---|
| `primitives.py`: erasure and KV inference | Project-owned MIT Stage 2A reanalysis functions; original script hash recorded in projection lineage | Extracted mathematical functions only; removed raw/private input loaders, repository paths and command side effects; seed and resampling math unchanged |
| `primitives.py`: replay correlation/resampling, metric classifier | Project-owned MIT Stage 2A2 functions; original script hash recorded | Extracted pure functions; removed raw trace/export/private imports; centering and grouping unchanged |
| `analysis.py`: controlled inference and four-arm reconstruction | New project release implementation of mean/percentile bootstrap and BH adjustment, checked against frozen Stage 2A tail counts and original controlled summaries | NumPy seeded generator; original B=2,000; canonical rounding disclosed; no Gate-1 source port copied |
| `figures.py` | New project Matplotlib implementation | Outcome-generated plots and artist-coordinate checks; no publisher style files or journal PDFs; selected original plotted numbers retained as comparison targets |
| Historical scheduler/Scorpio/reserve code | Private simulator lineage; local-erasure register records `b5bc1967adf6210be4cae69549163686f8a6003d` with no fresh execution attestation | Not bundled or claimed independently runnable. Project-maintained reconstructions/adaptations must not be represented as validated native implementations |
| NumPy / Matplotlib | Versions pinned in requirements.txt | External dependencies installed from their distributions, not copied source |

## Workload provenance

| Family | Sources and transformation | What is released |
|---|---|---|
| Controlled priority/prefill/interactions | Project-generated workloads with fixed condition designs and generation seeds | Paired scalar outcomes and summary diagnostics; no private simulator code |
| Local erasure | Seven source strata, eight selected windows each, three paired modules and three repeated seeds | Window-grouped counts, source names and seed IDs; input payload removed |
| Replay | Azure 2023/2024 Code/Conversation, BurstGPT, Mooncake conversation/tool-agent; three deterministic windows per source, replay rates 0.5/1/2 | Ratios with grouping; no per-request timestamps/tokens/hash IDs |
| Metrics | Controlled priority/prefill, held-out generalization, public replay | Five paired simulated endpoints, opaque experiment IDs and source-outcome file hashes |
| Exploratory KV | Fixed held-out synthetic workload conditions across ten shared seed streams | Corrected paired endpoints and design grouping; native interpretation remains invalid/inconclusive |

Upstream references, verified release labels and license caveats are in `THIRD_PARTY_NOTICES.md`. A release label is not a pinned executed code commit. The exact filtered BurstGPT file was not recovered, although selected record mappings established reuse with related research. The private evidence register supplies source input hashes for unavailable historical extensions; no replacement observations were fabricated.

This release was prepared with substantive AI assistance for projection adapters, analysis checking, tests and documentation. Human authors remain responsible for final scientific and publication approval; no independent human verification is asserted by an automated PASS.

Public release v0.1.0 (2026-10-30 UTC) comes from the approved 43-file snapshot at private work commit `38f0689d868e57169dd2fd4832a2de6db175855b`. Its scientific data, analysis code and tests are unchanged. Release-only edits update public URLs, citation/version metadata and author-approved publication status; the content manifest is regenerated. The original development history is not distributed.
