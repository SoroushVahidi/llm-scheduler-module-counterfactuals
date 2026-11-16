# Reproducibility and integrity review — 16 November 2026

This review concerns the evolving checkout after the v0.2.0 release. It adds
checks for the current repository without changing the published release,
scientific observations, statistical implementations or coverage classifications.
The baseline was documentation commit `e73356484880c9fd0bbeacb0db6a215413573f4f`.

## What was verified

The attached v0.2.0 archive was downloaded from its public release page, verified
against the asset's SHA-256, and compared byte-for-byte with all 103 files in the
v0.2.0 Git tag. Its original verifier accepted all 102 manifest entries.
The checksum manifest itself is excluded from that recursive inventory.

A fresh CPython 3.12.3 virtual environment installed the pinned requirements;
`pip check` reported no incompatible requirements. The five documented
reconstruction commands ran in separate processes using only public files and
installed dependencies. Linux Landlock denied access outside the package and
runtime locations, and seccomp denied network sockets. Explicit file-access
and socket-denial probes passed before each command. No private checkout,
credential, serving engine, model weights or GPU was required. This checks the
public reconstruction workflow, not the original simulation or native execution.

## Claim-to-evidence assessment

The CSV and JSON matrices agree on all 48 identifiers: **36 reconstructible,
10 partial and 2 unavailable**. Public artifact references and command paths
resolve. Source inspection traced the reconstructed families to these inputs:

| Families | Recomputed evidence and statistical unit |
|---|---|
| C01–C05, C07 | Controlled outcomes/probes; interventions are averaged within workload before inference over ten workload seeds. |
| C08–C10, C12–C13 | Original/extension erasure counts; distinguish pooled event fractions from means over positive-denominator cells. Whole windows are resampled, retaining dependent pairs/seeds. |
| C14–C16 | Four-arm interaction contrasts and standalone fairness outcomes; context and signs retain their original interpretation. |
| C17–C20 | Held-out observations joined by workload; fixed intervention repetitions are aggregated before the declared inference. |
| C21–C23 | Replay ratios and four-arm outcomes; 63 rate instances belong to 21 upstream windows, not 63 independent windows. |
| C25–C27 | Prospective per-seed counts; five seed ratios per cell, with 140 unit-rate windows used for primary inference and source-family blocks retained. |
| C28–C29 | Paired endpoint columns and deterministic metric classification; 3,940 cells, not independent experimental replications. |
| C31–C33 | Exploratory KV outcomes and interactions; population distinctions and ten shared seed-stream blocks retained. |
| C35–C37 | Saved fidelity counters and candidate inventories; arithmetic agreement is reconstructible, native semantic validity is not established. |
| C38–C39 | Seven original synthetic pilot fixtures, saved records/repeat, both analyzers and independent oracle. Saved execution accounting does not recreate the historical executions. |
| C42–C43 | Recorded real-engine arm/pair summaries; numerical contrasts and resampling are reproducible, identical-input causality is not established. |

These mappings support the **declared saved-output** coverage. They do not award
credit for original execution, missing inputs or validation of native algorithms.
Representative exclusions were also checked:

- C06 has a frozen structural-pressure anchor, not the required original
  per-instance probes. A different diagnostic population cannot substitute.
- C11's counts reconstruct both `232011/364302` (63.6864% of actionable steps)
  and `232011/356577` (65.0662% among overrides). Its historical partial status
  remains unchanged despite later manuscript clarification.
- C24/C47 require restricted input-identity mappings; counts and hashes cannot
  independently establish disjointness or overlap.
- C30/C48 concern historical recovery/execution lineage beyond public file hashes.
- C34/C44 lack the executable native contracts or input vectors required for
  independent validity/pairing checks. Saved equality flags are assertions.
- C40/C41/C46 lack full logs, calibration observations or a complete execution
  archive; C45 lacks individual predictions needed to reconstruct model scores.

Calculations read outcome/count projections first; frozen summaries serve as
comparison targets. Reading a recorded answer does not count as reconstruction.
Independent arithmetic checks confirmed the erasure totals and grouping,
workload-averaged prefill request-change fraction, C11 denominators, and metric
category counts. No reported estimate, interval, seed, margin or classification
was changed.

## Conservative repairs and regression checks

1. `scripts/reproduce_stage4c.py` opened CSV files without an explicit close.
   This genuine resource-management defect was reproduced. The loader now uses
   a context manager; tests check closure on both successful reading and an
   iteration exception. No analysis expression or CSV interpretation changed.
2. The old public-content scanner covers only the frozen manifest. It cannot
   cover later additions by itself. The additional offline
   [checkout guard](../scripts/check_repository.py) checks the current file
   inventory, sensitive-content patterns, relative links/anchors, claim targets,
   permissions, and immutable released scientific content. Documentation changes
   and the checksum-pinned loader repair are explicitly scoped exceptions.
3. A narrow `.gitignore` excludes the local virtual environment, Python caches,
   and documented `output/` directory. It does not ignore scientific data trees.
   The guard still rejects unreviewed files force-added from ignored directories.

The suite now has **39 passing tests**: the original 28, two resource-closure
tests, and nine checkout-integrity mutation tests. Missing observations, changed
reference files, invalid claim targets, bad anchors, unreviewed files, symlinks
and credential-shaped content are rejected. The suite ran with ResourceWarnings
promoted to errors; no resource warnings remained. All **36 generated files**, including numerical tables, JSON results and figures,
matched the validated released implementation byte-for-byte.

Use [validation.md](validation.md) for the two distinct validation paths:
`verify_manifest.py` on the exact release, and `check_repository.py` on this
checkout. Historical manifests, file-level audits, tags and release assets were
not regenerated or changed. The original release verifier intentionally rejects
later edited documentation and the repaired loader.

## Security, dependencies and external access

All current repository files were reviewed with the content guard. No credential,
restricted trace payload, private manuscript, machine-specific runtime path or
unexpected binary/symlink was found. Existing project-owned synthetic pilot
request fields are intentional fixtures, not third-party production identities.
Large JSON/CSV files are scientific observations or provenance and are retained.
All source files use ordinary non-executable permissions; commands invoke Python.
License terms and the restriction on redistributing upstream traces are unchanged.

Thirteen important external URLs were checked: twelve returned successful
responses, including both release pages and the Azure, BurstGPT, Mooncake and
CC BY sources. The BurstGPT DOI redirects to an ACM page returning an automated
access block (HTTP 403). Crossref independently resolves the DOI and matching
title, so this was not classified as a broken citation.

OSV returned no advisory matches for the twelve runtime package versions in the
fresh environment, including all three direct pinned dependencies. This is a
point-in-time advisory lookup, not a guarantee of vulnerability absence. The
three direct dependencies are pinned; transitive dependencies are not fully
locked. Installation and execution were checked on Linux/CPython 3.12.3, not
claimed across every platform. Scans and isolation tests have a bounded scope;
they do not certify all possible privacy inferences or historical execution.

The public release still supports saved-output numerical reconstruction, not
complete original-experiment reproduction, native instrumentation neutrality,
or native module-intervention validity. Those scientific limits remain intact.
