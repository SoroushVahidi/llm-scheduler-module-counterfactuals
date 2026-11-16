# Provenance records

`claim_matrix.json/csv` is the current v0.2.0 coverage matrix. `stage4c_claim_matrix.json` is the frozen unpublished baseline: its candidate flags, old missing-source entries and quartile uncertainty are historical, superseded by the current matrix. `claim_register.json` and `projection_lineage.json` retain original v0.1.0 references. Snapshot, execution and containing commits are not interchangeable. Private commit IDs are source references, not public repositories or download promises.

`recovered_sources.json` records field allowlists and exact source hashes. `prospective_raw_hashes.json` and `trajectory_source_hashes.json` describe saved artifacts outside Git; no execution or containing commit is invented. `stage4c_sources.json` preserves earlier receipt qualifications. Source hashes do not reconstruct excluded raw payloads or establish serving-engine pairing.

`content_manifest.json` checks every file in the published v0.2.0 package except itself. `public_file_audit.csv` records the disposition and license of every file shipped in that release; fingerprints are in the content manifest to avoid recursive hashes. These are immutable release records, not manifests for later documentation revisions. Use the [version-specific validation instructions](../docs/validation.md#choose-the-version-being-checked).
