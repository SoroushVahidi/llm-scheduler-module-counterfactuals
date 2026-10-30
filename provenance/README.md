# Provenance records

`claim_matrix.json/csv` is the current v0.2.0 coverage matrix. `stage4c_claim_matrix.json` is the frozen unpublished baseline: its candidate flags, old missing-source entries and quartile uncertainty are historical, superseded by the current matrix. `claim_register.json` and `projection_lineage.json` retain original v0.1.0 references. Snapshot, execution and containing commits are not interchangeable. Private commit IDs are source references, not public repositories or download promises.

`recovered_sources.json` records field allowlists and exact source hashes. `prospective_raw_hashes.json` and `trajectory_source_hashes.json` describe saved artifacts outside Git; no execution or containing commit is invented. `stage4c_sources.json` preserves earlier receipt qualifications. Source hashes do not reconstruct excluded raw payloads or establish serving-engine pairing.

`content_manifest.json` checks every package file except itself. `public_file_audit.csv` records the disposition and license of every shipped file; fingerprints are in the content manifest to avoid recursive hashes.
