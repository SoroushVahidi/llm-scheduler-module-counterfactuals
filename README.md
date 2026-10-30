# Module Counterfactuals for Attributing LLM Serving Scheduler Effects

**Research code and data v0.1.0 — released 2026-10-30 (UTC).** [Repository](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals) · [Versioned release](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/releases/tag/v0.1.0). This package reconstructs selected manuscript analyses from project-generated outcomes. It contains neither the development repository's history nor a runnable serving simulator. Soroush Vahidi is the recorded research author; the manuscript is not represented as accepted or published. No archive DOI has been assigned.

## Research question

An aggregate scheduler score cannot tell us whether a component had an opportunity to act, whether its recommendation survived downstream composition, or whether individual requests changed despite an aggregate null. This study combines typed module substitutions, paired full trajectories, same-state interventions and downstream disagreement-erasure diagnostics. Factorial comparisons expose interactions between modules. Pairing and common random numbers are established techniques; the contribution is the combined diagnostic procedure and its explicit separation of these questions. Instrumented alternatives can recover some of the same information.

A full-trajectory treatment replaces a declared module and follows the resulting trajectory using the paired workload. A same-state comparison asks what a different recommendation would do at one fixed state. Local erasure does **not** establish equivalence of long-horizon trajectories or live production systems.

## What is included

| Projection | Observations and grouping | Supported calculation |
|---|---|---|
| Controlled priority | 840 outcomes: 28 fixed pairs × 10 workload seeds × 3 conditions; 840 diagnostic summaries | Paired ANWG changes, per-workload means, pointwise intervals, finite-bootstrap tail sensitivity |
| Controlled prefill | 120 outcomes: 4 fixed pairs × 10 seeds × 3 conditions; 120 diagnostic summaries | Aggregate nulls alongside request completion-time changes |
| Four-arm interactions | 10 paired four-arm observations per module experiment | Both − first − second + base; priority × fairness and prefill × fairness |
| Local erasure | 168 pair-window cells inside 56 windows, 7 sources; each cell sums 3 repeated simulation seeds | Event-weighted fraction, equal-positive-cell mean, whole-window bootstrap |
| Public replay diagnostics | 21 source windows × 3 dependent rates = 63 instances | Four correlations and corrected source-window conditional resampling |
| Metric sensitivity | 3,940 matched cells, 5 paired endpoint values each | Benefit-oriented tolerance classifications |
| Exploratory KV | 5,330 observations, 13 historical rows; six declared-slot pairs form 2,460 observations; one unflagged pair forms 410 | Paired changes and intervals clustered on 10 shared seed streams |
| Figure anchors | Five historical plotted-number datasets, with private paths removed | Selected numerical comparisons; new release plots also use corrected erasure/KV calculations |

IDs are experimental grouping keys, not original production request/session identifiers. Frozen references are kept separately from observations. Do not concatenate overlapping campaign projections into a new independent sample: the metric panel deliberately reuses outcomes represented elsewhere.

## Reproduce without private access

Tested with CPython **3.12.3**, NumPy **2.3.5**, Matplotlib **3.10.9**. CPU-only; no API, model weights, scheduler service, GPU or network is used after dependency installation. Run from the extracted package root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/verify_manifest.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python scripts/reproduce.py --output output
PYTHONDONTWRITEBYTECODE=1 python scripts/figures.py --results output/results.json --output output/figures
```

The reconstruction writes `results.json` and `selected_tables.csv`; it checks frozen reference values before reporting PASS. Figure generation writes PDF/PNG figures and `plotted_values.json`, checking actual artist coordinates and selected manuscript anchors. These are outcome-reconstruction commands, not new experiments. Full percentile calculations use 10,000 draws for erasure, replay and KV; controlled comparisons use their original 2,000 draws. Runtime depends on the machine. See [statistical design](docs/statistical_design.md), [data dictionary](docs/data_dictionary.md), [provenance](docs/provenance.md) and [supported scope](docs/reproduction_scope.md).

## What the evidence supports

- Local erasure: **338,241 / 340,548 = 99.3226%** pooled event-weighted; **96.0806%** equal-positive-cell mean. Their distinct post-hoc ranges are approximately **[98.7983%, 99.5835%]** and **[93.2348%, 98.0106%]**, respectively. There are **72 positive and 96 zero-denominator cells**. Only **3 of 38** benchmark-eligible pairs were selected for this experiment.
- Priority activation can affect aggregate outcomes in the controlled design. Prefill can change individual completion times while observed aggregate ANWG remains zero. Observed zeros are not equivalence tests.
- Interactions depend on the design: the controlled priority/fairness contrast is negative; prefill/fairness shows subadditive degradation. Held-out and source-dependent transfer is weaker or inconclusive; the package does not generalize controlled results to all workloads.
- Replay uses **21**, not 63, source-window units. The 1,512 distinct source records and 4,536 appearances are certified historical input counts, not independently reconstructable identities in this sanitized package. Corrected ranges are conditional sensitivity calculations over deliberately selected windows, not calibrated population-confidence claims.
- Metric classifications are **3,028 all-near-null / 655 detection-sensitive / 257 sign-sensitive** using tolerance 1e-12 and benefit orientation. These are neither statistical significance nor practical-value categories.

## Essential limitations

The source workloads were production-derived; priorities, SLOs, treatments and outcomes were assigned or simulated. This is model-conditional attribution, not a live-production causal evaluation. Stage/order descriptions are implementation-specific and cannot attest every historical executed version.

**KV semantics remain unresolved:** five interpretations as native Scorpio modules are INVALID; five reserve interventions are INCONCLUSIVE. A reserve alias is not the native Scorpio decode filter. Six declared-slot pairs are exploratory, and the unflagged single pair is a sensitivity population, not a certificate of native algorithm fidelity. Numerical reconstruction does not repair those limitations.

A prospective opportunity result remains inconclusive. Predictive AUROC 1.0 had only one independent test group and is exploratory, not validated generalization. There is **no valid real-vLLM confirmatory treatment-effect estimate**. Unsuccessful infrastructure attempts are not validation.

Raw or reconstructive Azure, BurstGPT and Mooncake traces, prompts/session identifiers, source row ranges, timing/token/cache sequences, private source snapshots, historical logs, legacy missing Parquets and publisher assets are excluded. Historical diagnostic denominators are incomplete; replay ratios cannot support newly invented event-count inference. Exact filtered BurstGPT file bytes and some execution/state attestations are unavailable. See [missing-input scope](docs/reproduction_scope.md).

## Attribution, related research and citation

Project code is MIT. Eligible project-generated outcome projections are CC BY 4.0; see `LICENSE-DATA` and [third-party notices](THIRD_PARTY_NOTICES.md). Neither license grants rights to third-party raw traces. All source attributions and differences between historical and current implementations are documented in [provenance](docs/provenance.md).

The related manuscript *When Does LLM-Serving Scheduler Adaptation Matter? Action Opportunity and Causal Headroom in Production-Derived Replay* studies whole-policy opportunity and one-step latency headroom. It shares infrastructure and some Azure/BurstGPT records with this study. These are not independent source datasets. Its editorial status is not asserted. This package studies component boundaries, erasure, paired consequences and interactions. An earlier synthetic credit benchmark is separately available at [module-intervention-credit](https://huggingface.co/datasets/SoroushVahidi/module-intervention-credit), recorded revision `84430648ed5d564b29b4f9465efb27ad29921cf8`; it is not a substitute for these projections.

Use `CITATION.cff` for the author/title/version. Cite [v0.1.0](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/releases/tag/v0.1.0), which provides the release archive and SHA-256 checksum. The source, [outcome data](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/tree/v0.1.0/data/outcomes), [diagnostics](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/tree/v0.1.0/data/diagnostics) and [reproduction scope](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/blob/v0.1.0/docs/reproduction_scope.md) are public. No DOI has been assigned.
