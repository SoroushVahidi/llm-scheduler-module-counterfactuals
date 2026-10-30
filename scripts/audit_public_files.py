#!/usr/bin/env python3
"""Scoped release-content checks. Scan results supplement schema/provenance review."""
import csv,json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATTERNS={
 'credential':re.compile(r'gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----|sk-[A-Za-z0-9]{24,}'),
 'private_path':re.compile(r'/(?:home|Users|mmfs1|scratch)/[^\s"\x27]+'),
 'personal_email':re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
 'confidential_history':re.compile(r'PEVA\x2dD\x2d|under\s+review\s+as|editorial\s+portal|author\s+correspondence',re.I)}
FORBIDDEN_FIELDS={'source_row_range','input_length','output_length','input_lens','output_lens','hash_ids','prompt','prompts','timestamp','request_id','session_id','hostname','manifest_path','source_rps','mean_input_tokens','mean_output_tokens'}
def fields(x):
 if isinstance(x,dict):
  yield from x
  for v in x.values():yield from fields(v)
 elif isinstance(x,list):
  for v in x:yield from fields(v)
def main():
 manifest=json.loads((ROOT/'provenance/content_manifest.json').read_text())
 with (ROOT/'provenance/public_file_audit.csv').open() as f:audit={r['path']:r for r in csv.DictReader(f)}
 paths=[r['path'] for r in manifest['files']]+['provenance/content_manifest.json']
 assert set(paths)==set(audit),'file audit must cover every package file'
 for rel in paths:
  p=ROOT/rel;assert p.is_file() and not p.is_symlink(),rel
  assert not any(x in {'.git','.env','__pycache__'} for x in p.relative_to(ROOT).parts),rel
  s=p.read_text()
  for kind,pattern in PATTERNS.items():assert not pattern.search(s),(rel,kind)
  assert audit[rel]['decision']=='INCLUDE' and audit[rel]['license'] in {'MIT','CC-BY-4.0','license-text'},rel
  if rel.startswith('data/recovered/') and p.suffix=='.json':assert not (set(fields(json.loads(s))) & FORBIDDEN_FIELDS),rel
 for name in ['LICENSE','LICENSE-DATA','THIRD_PARTY_NOTICES.md']:assert (ROOT/name).stat().st_size>500
 print(f'PASS: {len(paths)} files; scoped credentials, paths, personal-data, editorial-history, restricted-field, attribution/license and symlink checks')
if __name__=='__main__':main()
