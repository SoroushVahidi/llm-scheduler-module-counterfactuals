# Third-party attribution and exclusions

No third-party source code, publisher assets or raw traces are bundled. NumPy and Matplotlib are installed as dependencies under their upstream terms; their code is not relicensed by this package. Code/data licenses here apply only to the project's own contributions.

| Upstream workload | Attribution and authoritative source | Recorded version; status |
|---|---|---|
| Azure LLM Inference 2023 (Code/Conversation) | Patel et al., *Splitwise: Efficient generative LLM inference using phase splitting*, ISCA 2024. [Dataset and citation](https://github.com/Azure/AzurePublicDataset/blob/master/AzureLLMInferenceDataset2023.md) | 2023-11-11 traces. Data CC BY, per dataset instructions and [license](https://github.com/Azure/AzurePublicDataset/blob/master/LICENSE). |
| Azure LLM Inference 2024 (Code/Conversation) | Stojkovic et al., *DynamoLLM: Designing LLM Inference Clusters for Performance and Energy Efficiency*, HPCA 2025. [Dataset and citation](https://github.com/Azure/AzurePublicDataset/blob/master/AzureLLMInferenceDataset2024.md) | 2024-05-10 through 2024-05-19. Data CC BY, per dataset instructions. |
| BurstGPT | Wang et al., *BurstGPT: A Real-World Workload Dataset to Optimize LLM Serving Systems*, KDD 2025, [doi:10.1145/3711896.3737413](https://doi.org/10.1145/3711896.3737413); [source](https://github.com/HPMLL/BurstGPT) | Historical records name v2.0 and `BurstGPT_without_fails_1.csv`; exact filtered bytes are not recovered. Selected record mapping, not full-file identity, was verified. [CC BY 4.0](https://github.com/HPMLL/BurstGPT/blob/main/LICENSE). |
| Mooncake | Qin et al., *Mooncake*, FAST 2025; [FAST25-release](https://github.com/kvcache-ai/Mooncake/tree/main/FAST25-release) | Conversation/tool-agent trace labels; no pinned upstream commit verified here. The repository has Apache-2.0 code terms, but no explicit trace-specific redistribution grant was established. No trace payload or reconstructive descriptor is included. |

Changes from source workloads: research simulations generated new outcomes after deterministic workload selection and synthetic priority/SLO/intervention assignment. This package then selects only aggregate outcomes or grouped diagnostics, removes source record ranges, request/session IDs, timestamps, token lengths, cache/hash sequences and private paths, and preserves statistical grouping. Frozen numbers and new outcome projections are clearly separated. No raw upstream data is licensed by `LICENSE-DATA`.

The Mooncake-derived rows are project-generated outcomes/counts/ratios only; their inclusion is not a legal determination that the upstream trace can be redistributed. For v0.1.0, the author approved publication of its selected project-generated outcomes and stated that he is not aware of restrictions preventing their sharing. No Mooncake trace permission is presumed. Any future exclusion of a source must be documented and revalidated; silently dropping its strata would no longer reconstruct the reported seven-source estimands.

## Stage4C redistribution review (2026-10-30)

Current upstream BurstGPT and Azure license files state CC BY4.0. That does not
recover the historical filtered BurstGPT bytes or establish a complete source
version attestation. Mooncake supplies repository Apache2.0 terms but the trace
release README inspected here does not resolve an explicit data-specific grant.
No upstream raw rows, reconstructive state/length/timing/cache records, private
paths or trace payloads are added. The new CSVs contain only project-generated
counts or latency summaries; the seven pilot fixtures are original synthetic
inputs. Rights to project code/data follow LICENSE and LICENSE-DATA, with source
attribution preserved. This is a scoped redistribution assessment, not an
assertion of permission to release upstream traces. The author authorized publication of the audited eligible v0.2.0 subset. This authorization does not grant rights in third-party trace payloads.
