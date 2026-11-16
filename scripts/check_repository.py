#!/usr/bin/env python3
"""Offline checks for this post-v0.2.0 checkout; never reseals the published release."""
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SHA256 = 'f2f3cb44be4710b9320bda0e41739ab219ccce23b74fd34589999eb5bfec8cff'
# The only released executable changed: context-managed CSV reading, no math change.
ADAPTER_SHA256 = '1b5fcd36084adcdfc6dd6c837bfc4e0d5703ddb437262f4353abb705c7fc5337'
EDITABLE_DOCUMENTS = {
    'README.md', 'THIRD_PARTY_NOTICES.md', 'docs/claim_coverage.md',
    'docs/denominator_correction.md', 'docs/reproduction_scope.md',
    'docs/statistical_design.md', 'docs/validation.md', 'provenance/README.md',
}
ADDITIONS = {
    '.gitignore', 'docs/README.md', 'docs/integrity_review.md',
    'scripts/check_repository.py', 'tests/test_repository_hygiene.py',
    'tests/test_resource_handling.py',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    """Include unignored working files and *all* tracked files, even force-added output."""
    paths = set()
    for directory, folders, files in os.walk(root, followlinks=False):
        here = Path(directory)
        for folder in folders[:]:
            p = here / folder
            rel = p.relative_to(root).as_posix()
            if folder in {'.git', '__pycache__'} or rel in {'.venv', 'output'}:
                folders.remove(folder)
            elif p.is_symlink():
                paths.add(rel)
                folders.remove(folder)
        paths.update((here / name).relative_to(root).as_posix() for name in files
                     if name != '.git' and not name.endswith(('.pyc', '.pyo')))
    if (root / '.git').exists():
        tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode()
        paths.update(filter(None, tracked.split('\0')))
    return sorted(paths)


def expand_braces(value):
    match = re.search(r'\{([^{}]+)\}', value)
    if not match:
        return [value]
    return [x for part in match[1].split(',')
            for x in expand_braces(value[:match.start()] + part + value[match.end():])]


def check_claims(root):
    with (root / 'provenance/claim_matrix.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 48 and {r['claim_id'] for r in rows} ==
            {f'C{i:02}' for i in range(1, 49)}, 'claim matrix: missing or duplicate family')
    require(sum(r['v020_coverage'] == 'R' for r in rows) == 36,
            'claim matrix: frozen coverage changed')
    require(next(r for r in rows if r['claim_id'] == 'C11')['v020_coverage'] == 'F',
            'claim matrix: C11 release assessment changed')
    mirror = json.loads((root / 'provenance/claim_matrix.json').read_text())
    require({r['claim_id']: r for r in rows} == {r['claim_id']: r for r in mirror},
            'claim matrix: CSV/JSON differ')
    references = 0
    for row in rows:
        for group in filter(None, row['public_artifact'].split(';')):
            for target in expand_braces(group.strip()):
                name, _, anchor = target.partition('#')
                p = (root / name).resolve()
                require(p.is_relative_to(root) and p.is_file(),
                        f"claim {row['claim_id']}: missing public artifact")
                if anchor:
                    ids = {r['claim_id'] for r in json.loads(p.read_text())['claims']}
                    require(anchor in ids, f"claim {row['claim_id']}: missing register entry")
                references += 1
        commands = re.findall(r'\bpython\s+([\w/]+\.py)', row['reconstruction_command'])
        if row['v020_coverage'] == 'R':
            require(bool(commands), f"claim {row['claim_id']}: missing command")
        for command in commands:
            require((root / command).is_file(), f"claim {row['claim_id']}: missing script")
    return references


def heading_ids(text):
    result, counts = set(), {}
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        slug = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
        n = counts.get(slug, 0)
        result.add(slug if n == 0 else f'{slug}-{n}')
        counts[slug] = n + 1
    return result


def check_links(root, paths):
    count = 0
    for name in paths:
        if not name.endswith('.md'):
            continue
        p = root / name
        text = re.sub(r'```.*?```', '', p.read_text(), flags=re.S)
        for link in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
            parts = urlsplit(link.strip('<>'))
            if parts.scheme or parts.netloc:
                continue
            target = (p.parent / unquote(parts.path)).resolve() if parts.path else p
            require(target.is_relative_to(root) and target.exists(), f'{name}: broken relative link')
            if parts.fragment and target.suffix == '.md':
                require(unquote(parts.fragment) in heading_ids(target.read_text()),
                        f'{name}: broken heading link')
            count += 1
    return count


def check(root=ROOT):
    root = root.resolve()
    manifest = root / 'provenance/content_manifest.json'
    require(not manifest.is_symlink() and digest(manifest) == MANIFEST_SHA256,
            'frozen release manifest changed')
    records = json.loads(manifest.read_text())['files']
    expected = {r['path'] for r in records} | {'provenance/content_manifest.json'} | ADDITIONS
    paths = inventory(root)
    require(set(paths) == expected,
            'unexpected or missing files: ' + ', '.join(sorted(set(paths) ^ expected)))
    for name in paths:
        p = root / name
        require(not p.is_symlink() and p.is_file(), f'{name}: symlink or non-file')
        require(not p.stat().st_mode & 0o111, f'{name}: unexpected executable permission')
    for row in records:
        name = row['path']
        if name in EDITABLE_DOCUMENTS:
            continue
        want = ADAPTER_SHA256 if name == 'scripts/reproduce_stage4c.py' else row['sha256']
        require(digest(root / name) == want, f'{name}: protected content changed')
    patterns = runpy.run_path(str(root / 'scripts/audit_public_files.py'))['PATTERNS']
    for name in paths:
        try:
            text = (root / name).read_text()
        except UnicodeDecodeError:
            raise ValueError(f'{name}: unexpected binary file') from None
        for kind, pattern in patterns.items():
            require(not pattern.search(text), f'{name}: sensitive-content category {kind}')
    references = check_claims(root)
    links = check_links(root, paths)
    return dict(status='PASS', files=len(paths), frozen_manifest='unchanged',
                claim_families=48, reconstructible_families=36,
                public_artifact_references=references, relative_links=links)


if __name__ == '__main__':
    try:
        print(json.dumps(check(), indent=2))
    except (ValueError, OSError, KeyError) as error:
        raise SystemExit('FAIL: ' + str(error))
