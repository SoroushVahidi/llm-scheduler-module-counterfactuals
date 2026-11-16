"""Mutation tests for the current-checkout guard, without editing real evidence."""
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('repository_checks', ROOT / 'scripts/check_repository.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class RepositoryHygiene(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in guard.inventory(ROOT):
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, p)

    def test_current_checkout_passes(self):
        self.assertEqual(guard.check(self.root)['reconstructible_families'], 36)

    def test_missing_observation_rejected(self):
        (self.root / 'data/diagnostics/erasure_windows.json').unlink()
        with self.assertRaisesRegex(ValueError, 'missing files'):
            guard.check(self.root)

    def test_changed_reference_rejected(self):
        p = self.root / 'data/reference/erasure.json'
        p.write_text(p.read_text() + '\n')
        with self.assertRaisesRegex(ValueError, 'protected content changed'):
            guard.check(self.root)

    def test_new_unreviewed_data_rejected(self):
        (self.root / 'data/unreviewed.csv').write_text('a,b\n1,2\n')
        with self.assertRaisesRegex(ValueError, 'unexpected or missing files'):
            guard.check(self.root)

    def test_sensitive_content_in_new_document_rejected(self):
        # Synthetic credential shape; no real credential is included.
        p = self.root / 'docs/README.md'
        p.write_text(p.read_text() + '\n' + 'gh' + 'p_' + 'X' * 30)
        with self.assertRaisesRegex(ValueError, 'sensitive-content category credential'):
            guard.check(self.root)

    def test_broken_heading_rejected(self):
        p = self.root / 'docs/README.md'
        p.write_text(p.read_text() + '\n[Missing](validation.md#does-not-exist)\n')
        with self.assertRaisesRegex(ValueError, 'broken heading link'):
            guard.check(self.root)

    def test_claim_artifact_reference_rejected(self):
        p = self.root / 'provenance/claim_matrix.csv'
        with p.open() as stream:
            rows = list(csv.DictReader(stream))
        rows[0]['public_artifact'] = 'data/nonexistent.json'
        with p.open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=rows[0])
            writer.writeheader()
            writer.writerows(rows)
        (self.root / 'provenance/claim_matrix.json').write_text(json.dumps(rows))
        # Test reference validation independently of the earlier immutable-hash gate.
        with self.assertRaisesRegex(ValueError, 'missing public artifact'):
            guard.check_claims(self.root)

    def test_symlink_rejected(self):
        p = self.root / 'docs/README.md'
        p.unlink()
        p.symlink_to(self.root / 'README.md')
        with self.assertRaisesRegex(ValueError, 'symlink or non-file'):
            guard.check(self.root)

    @unittest.skipUnless(shutil.which('git'), 'Git-specific publication guard')
    def test_force_added_ignored_output_rejected(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        p = self.root / 'output/unreviewed.json'
        p.parent.mkdir()
        p.write_text('{}')
        subprocess.run(['git', 'add', '-f', 'output/unreviewed.json'], cwd=self.root, check=True)
        with self.assertRaisesRegex(ValueError, 'unexpected or missing files'):
            guard.check(self.root)
