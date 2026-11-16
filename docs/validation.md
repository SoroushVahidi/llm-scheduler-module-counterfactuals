# Validation

## Choose the version being checked

For the published artifact, use the exact **v0.2.0 tag or attached release
archive**, as shown in the [quick start](../README.md#quick-start). Run its
manifest verifier, tests and reconstruction commands from that release root.
The manifest covers documentation as well as code and data.

Later documentation branches intentionally differ from those frozen document
hashes. A manifest mismatch on such a branch does not justify changing or
skipping the released integrity check: verify the exact release checkout
instead. The published `content_manifest.json`, file-level audit, release notes,
claim matrices and tags are retained unchanged. Updated documentation is not a
new scientific release, and its validation must separately establish that code,
data, statistics and tests still match v0.2.0.

## Validate the evolving checkout

On the documentation/integrity branch, use the additional offline guard:

```bash
python scripts/check_repository.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests -v
```

This guard checks the current file inventory, relative documentation links,
claim-matrix targets, permissions, and sensitive-content patterns. It verifies
released code, data, tests and reference values against the **unchanged** frozen
manifest, allowing only the explicitly listed documentation edits and the
checksum-pinned CSV resource-management repair. New files must be explicitly
reviewed and listed. Files force-added from ignored output directories are also
checked when Git metadata is available.

The repair closes CSV input streams on both success and failure; calculations
and saved observations are unchanged. The extra tests exercise that behavior
and reject missing observations, altered references, bad links, unreviewed files,
symlinks and credential-shaped text. Checks run locally; no CI service or new
runtime dependency is required. Scans are bounded safeguards, not a guarantee
against every possible disclosure.

The [November 16 integrity review](integrity_review.md) records the independent
coverage review, isolated reproduction and known limitations. The original
`verify_manifest.py` remains the verifier for the exact v0.2.0 release; it is
expected to reject edited documentation and the repaired adapter on this branch.

## Recorded v0.2.0 validation

The following describes validation performed for the published release, including
its restricted-runtime checks. It is not a claim that every later documentation
edit reruns those isolation checks.

Run the complete command sequence in README.md and `python scripts/audit_public_files.py`. The portable suite contains 28 tests: 13 retained v0.1.0, 4 Stage4C, 11 added observation/statistical/corruption checks. Comparisons retain the frozen Stage4C reference files. No new scientific experiments are part of validation.

The release is checked in a freshly extracted archive and a clean checkout, using only package files and installed dependencies. Restricted-runtime validation uses Linux Landlock to deny access to private research directories and seccomp to deny socket/connect calls; an explicit denial probe is run before scientific reconstruction. Dependencies are installed before network denial. Hash checks, all 28 tests, original figure artist checks, original/Stage4C/recovered reconstruction, supplementary arithmetic and public-file scans must pass.

All v0.1.0 observation files, source analysis modules and original portable tests are byte-identical. The Stage4C observation/reference projections and pilot analyses are unchanged. The quartile note is clarified from historical source code. Additional observations change coverage, not the frozen experimental results. The sole discovered manuscript discrepancy is the separately documented C11 denominator wording; both historical and correctly denominated calculations are preserved.

Numerical tolerances: integers exact; new rounded canonical values absolute 2e-9; 420 prospective count-derived rate cells match the archived Parquet at absolute 1e-14. Prospective bootstrap B=2000 and seeds match the historical analyzer. New tests reject altered arm endpoints, duplicate seed cells and inconsistent count partitions. Existing tests also reject altered pilot completions/diagnoses. Passing equality-flag arithmetic is never called independent real-engine pairing validation.

Package and asset checksums identify bytes. They do not certify historical execution, upstream trace redistribution rights or native algorithm fidelity. Downloadable validation receipts report actual executed commands and exit codes; public-access verification is performed after publication.
