"""The saved-table loader must close files even when CSV iteration fails."""
import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    'stage4c_resource_test', Path(__file__).resolve().parents[1] / 'scripts/reproduce_stage4c.py')
stage4c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage4c)


class ResourceHandling(unittest.TestCase):
    def test_csv_closed_after_success(self):
        stream = io.StringIO('group,count\na,2\n')
        with patch.object(Path, 'open', return_value=stream):
            self.assertEqual(stage4c.rows('fixture.csv'), [{'group': 'a', 'count': '2'}])
        self.assertTrue(stream.closed)

    def test_csv_closed_after_iteration_error(self):
        stream = io.StringIO('group,count\na,2\n')

        def broken_reader(_):
            yield {'group': 'a', 'count': '2'}
            raise ValueError('deliberate reader failure')

        with patch.object(Path, 'open', return_value=stream), patch.object(
                stage4c.csv, 'DictReader', side_effect=broken_reader):
            with self.assertRaisesRegex(ValueError, 'deliberate reader failure'):
                stage4c.rows('fixture.csv')
        self.assertTrue(stream.closed)
