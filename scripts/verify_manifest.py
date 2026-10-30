#!/usr/bin/env python3
"""Verify every immutable snapshot file. Generated output/ and .venv/ are outside its scope."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'provenance/content_manifest.json').read_text())
for row in manifest['files']:
 p=root/row['path'];assert p.is_file() and not p.is_symlink(),row['path']
 assert len(p.read_bytes())==row['bytes'],row['path']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['path']
print('PASS:',len(manifest['files']),'hashed files; manifest excludes only itself to avoid recursion')
