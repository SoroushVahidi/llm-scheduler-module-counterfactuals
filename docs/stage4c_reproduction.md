# Saved-output reconstruction and reviewer access

From a clean extracted package root, install the pinned dependencies in
`requirements.txt`, then run:

```bash
python scripts/verify_manifest.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/reproduce.py --output output
python scripts/figures.py --results output/results.json --output output/figures
python scripts/reproduce_stage4c.py --output output/stage4c
python scripts/supplementary_counts.py --output output/supplementary
python analysis/reconstruct.py --output output/recovered
```

All runtime inputs are inside the package. No credentials, private directories,
cluster accounts, GPUs, model weights or network are required at runtime.
These commands reanalyze saved observations only. Do not call private pilot
runners or simulator scripts to validate this package.

| Manuscript item (label stable across pagination) | Regenerated output |
|---|---|
| Main Fig2 priority; Fig3 prefill; Fig4 interactions | `output/figures/` plots plus checked artist/anchor values; selected numerical views, not identical publisher artwork |
| FigS1 seed strips | `output/supplementary/interaction_seeds.pdf` and `counts.json` |
| FigS3 priority forest, FigS4 KV, FigS5 metrics | original release figure views and `output/results.json` per-pair/population/module tables; full journal layout not reproduced |
| Original erasure sensitivity, KV populations, replay ranges | `output/results.json` and `selected_tables.csv` |
| Pilot table | `output/stage4c/pilot.csv`; both original analyzers rerun on saved records; separate arithmetic/schedule oracle checks112 primitives |
| Erasure extension table | `output/stage4c/erasure_extension.csv` |
| Dynamic fidelity table and six fairness candidates | `output/stage4c/dynamic_fidelity.csv`, `fairness_candidates.csv` |
| Prefill fidelity table | `output/stage4c/prefill_fidelity.csv`; retain overlapping views separately |
| Pairing table | `output/stage4c/real_engine_pairing_audit_assertions.csv`; counts of retained assertions only |
| Later real-engine contrasts | `output/stage4c/real_engine_contrasts.csv` |
| Metric family table | `output/results.json` → metrics.by_module |
| Per-source prospective correlation / predictive tables | `output/recovered/results.json` prospective.by_source; prediction table remains frozen per-model scores |
| Policy/interfaces, controlled design, lineage, campaign catalog | Documentary design/inventory tables, not newly calculated experiments; see coverage matrix for empirical claims |

Fig1 is a conceptual diagram, not an empirical calculation. FigS2 numerical stage shares and ambiguity counts are regenerated in `output/recovered/results.json`; the original journal artwork is not reproduced. See the explicit C11 denominator discrepancy. Original
figure anchors are frozen references; checking a saved anchor is not computing
it from observations. `supplementary_counts.py` uses only v0.1.0 data and can be
copied into that release for the additional descriptive arithmetic and seed
strip; it requires no new observations. The baseline coverage percentage counts
data-sufficient calculations with this disclosed adapter, not a claim that the
adapter was already in v0.1.0.

Reviewer access: use the public versioned release archive and SHA256SUMS. All required runtime inputs are included. Private source commit identifiers are provenance references, not promises of public access. The archive contains no manuscripts, private communications or editorial history.
