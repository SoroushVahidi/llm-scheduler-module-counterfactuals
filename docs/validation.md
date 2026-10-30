# Validation

Run the complete command sequence in README.md and `python scripts/audit_public_files.py`. The portable suite contains28 tests:13 retained v0.1.0,4 Stage4C,11 added observation/statistical/corruption checks. Comparisons retain the frozen Stage4C reference files. No new scientific experiments are part of validation.

The release is checked in a freshly extracted archive and a clean checkout, using only package files and installed dependencies. Restricted-runtime validation uses Linux Landlock to deny access to private research directories and seccomp to deny socket/connect calls; an explicit denial probe is run before scientific reconstruction. Dependencies are installed before network denial. Hash checks, all28 tests, original figure artist checks, original/Stage4C/recovered reconstruction, supplementary arithmetic and public-file scans must pass.

All v0.1.0 observation files, source analysis modules and original portable tests are byte-identical. The Stage4C observation/reference projections and pilot analyses are unchanged. The quartile note is clarified from historical source code. Additional observations change coverage, not the frozen experimental results. The sole discovered manuscript discrepancy is the separately documented C11 denominator wording; both historical and correctly denominated calculations are preserved.

Numerical tolerances: integers exact; new rounded canonical values absolute2e-9;420 prospective count-derived rate cells match the archived Parquet at absolute1e-14. Prospective bootstrap B=2000 and seeds match the historical analyzer. New tests reject altered arm endpoints, duplicate seed cells and inconsistent count partitions. Existing tests also reject altered pilot completions/diagnoses. Passing equality-flag arithmetic is never called independent real-engine pairing validation.

Package and asset checksums identify bytes. They do not certify historical execution, upstream trace redistribution rights or native algorithm fidelity. Downloadable validation receipts report actual executed commands and exit codes; public-access verification is performed after publication.
