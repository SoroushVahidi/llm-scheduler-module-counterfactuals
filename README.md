# Module Counterfactuals for Attributing LLM-Serving Scheduler Effects

**In plain words.** An LLM-serving scheduler is built from modules: admission, batching, preemption and so on. Swapping one module can change what it *recommends* without changing overall throughput, or leave the average unchanged while individual requests get faster or slower. This repository defines an **observation contract** that records, for each module, its opportunity to act, its recommendation, whether the action survived downstream logic, and the request-level and aggregate outcomes. It ships the analysis code, saved simulation outcomes and a validation suite so the reported findings can be rebuilt from the packaged files, with no GPU or network needed.

## Paper

- **Preprint:** S. Vahidi. *Module Counterfactuals for Attributing LLM Serving Scheduler Effects.* Research Square, 2026. [doi:10.21203/rs.3.rs-11569472/v1](https://doi.org/10.21203/rs.3.rs-11569472/v1). Not yet peer-reviewed.

```bibtex
@misc{vahidi2026modulecf,
  author = {Vahidi, Soroush},
  title  = {Module Counterfactuals for Attributing {LLM} Serving Scheduler Effects},
  year   = {2026},
  note   = {Research Square preprint},
  doi    = {10.21203/rs.3.rs-11569472/v1}
}
```

To cite the code, use the software release via [CITATION.cff](CITATION.cff) (release [v0.2.0](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/releases/tag/v0.2.0)). Related public data: [module-intervention-credit](https://huggingface.co/datasets/SoroushVahidi/module-intervention-credit) (single- and pairwise-module substitution counterfactuals, published from the llm-serving-heuristic-evolution program).

Related: [llm-serving-heuristic-evolution](https://github.com/SoroushVahidi/llm-serving-heuristic-evolution) (preprint [doi:10.2139/ssrn.7584825](https://doi.org/10.2139/ssrn.7584825)) · [llm-serving-scheduler-robustness-benchmark](https://github.com/SoroushVahidi/llm-serving-scheduler-robustness-benchmark).

---

> The detailed documentation below is kept from the previous README, with only small factual updates.

How can a scheduler module change its recommendations without changing overall
performance—and how can an unchanged aggregate conceal effects on individual
requests? This repository provides research code and eligible saved observations
for studying these questions in reconstructed LLM-serving schedulers.

The contribution is an **observation contract** that separates a module's
opportunity to act, its recommendation, the action that survives downstream
logic, and the resulting request-level and aggregate outcomes. It complements
whole-scheduler comparisons with explicit intermediate measurements. Equally
instrumented ablation recovered the same diagnoses in seven constructed
comparisons; the contribution is the contract, not diagnostic superiority.

## Research findings

- **Finding A — downstream erasure:** changed recommendations can produce the
  same admitted-request set after downstream scheduling logic.
- **Finding B — request effects under aggregate nulls:** request completion timing
  or service-level objective (SLO) status can change while arrival-normalized
  weighted goodput (ANWG) remains unchanged.
- **Finding C — context-dependent attribution:** effects depend on module
  composition, workload characteristics, and the performance endpoint.

Cloned-state comparisons measure recommendation survival at the **same state**.
Paired complete trajectories measure the consequences of **persistent module
substitution** as states evolve. These are different estimands. The reported
reconstructed experiments are discrete-event simulations; their timing results
are not hardware-performance measurements. See the
[design and interpretation guide](docs/reproduction_scope.md).

## Public artifact and coverage

[Release v0.2.0](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/releases/tag/v0.2.0)
supports **saved-output reconstruction of 36/48 enumerated claim families**.
It contains analysis code, tests, project-generated outcome/count/ratio
projections, selected figure reconstructions, and provenance records. It does
not include the full original simulator/serving environment or restricted raw
traces. This coverage is not complete original-experiment reproduction.

| Resource | Location |
|---|---|
| Statistical analysis code | [src/](src/), [analysis/](analysis/) |
| Reproduction entry points | [scripts/](scripts/) |
| Saved observations and comparison targets | [data/](data/); [data dictionaries](docs/README.md#data-and-provenance) |
| Portable validation suite | [tests/](tests/), [validation instructions](docs/validation.md) |
| Claim-to-evidence mapping | [48-family matrix](provenance/claim_matrix.csv), [coverage and remaining gaps](docs/claim_coverage.md) |

## Quick start

Use the exact release for reproducible results and its original checksum checks.
The commands below select **v0.2.0**, rather than a later documentation revision.
CPython 3.12.3 and the dependencies in `requirements.txt` were used for validation.

```bash
git clone --branch v0.2.0 --depth 1 https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals.git
cd llm-scheduler-module-counterfactuals
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/verify_manifest.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests -v
```

Alternatively, extract the attached v0.2.0 release archive and start with the
virtual-environment command. After dependency installation, reconstruction uses
only packaged files: no GPU, model service, credentials, private repository, or
runtime network access is required. The manifest is frozen to the release;
[validation guidance](docs/validation.md) explains checks on later documentation branches.

## Reproduce numerical results and figures

From the release root, with the environment activated:

```bash
python scripts/reproduce.py --output output
python scripts/figures.py --results output/results.json --output output/figures
python scripts/reproduce_stage4c.py --output output/stage4c
python scripts/supplementary_counts.py --output output/supplementary
python analysis/reconstruct.py --output output/recovered
```

These commands recalculate statistics and tables from saved records. Figure
outputs are checked numerical views, not copies of journal artwork. The
[figure/table reproduction guide](docs/stage4c_reproduction.md) maps each command
to its outputs and manuscript items. The seven-case pilot rechecks saved records
and its oracle; it does not rerun a serving experiment.

## Evidence and interpretation

The [claim matrix](provenance/claim_matrix.csv) identifies each finding's inputs,
experimental units, command, and limitations. Frozen reference answers and
historical assertion flags do not receive independent reconstruction credit.
[Statistical methodology](docs/statistical_design.md) specifies denominators,
resampling units, uncertainty, and multiplicity; overlapping projections must
not be pooled as independent observations.

The public release does **not** establish native scheduler performance or causal
validity. Native-vLLM deterministic input pairing is a separate validation step;
input equality alone does not establish instrumentation neutrality. Later pairing
work, pending instrumentation-neutrality evidence, and native module-substitution
validation are outside this frozen package. Native substitution effects are not
established here.

Remaining gaps include exact input identities, some original probe and prediction
records, and execution attestations. Third-party raw traces and reconstructive
request sequences are excluded. See [reproduction limits](docs/reproduction_scope.md)
and [data exclusions](docs/exclusions.md). The historical 63.7%/65.1% denominator
issue is explained in a [dated clarification](docs/denominator_correction.md);
subsequent manuscript wording does not change the published 36/48 assessment.

## Documentation

The [documentation index](docs/README.md) groups the reproduction instructions,
data dictionaries, statistics, provenance, coverage, limitations, and release
history. Start there for a specific figure, claim, or data field.

## Citation, licenses, and attribution

Cite the version used, using [CITATION.cff](CITATION.cff) and its release URL:

> Vahidi, S. (2026). *Module Counterfactuals for Attributing LLM Serving Scheduler
> Effects: Outcome Reconstruction Package* (Version 0.2.0) [Software and data].
> https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/releases/tag/v0.2.0

No DOI or journal acceptance is claimed. Code and documentation are [MIT](LICENSE);
eligible project-generated numerical data and factual provenance are
[CC BY 4.0](LICENSE-DATA). Retain [third-party attribution](THIRD_PARTY_NOTICES.md);
these licenses do not relicense upstream traces. The earlier
[v0.1.0 release](https://github.com/SoroushVahidi/llm-scheduler-module-counterfactuals/releases/tag/v0.1.0)
remains available with its original identity.
