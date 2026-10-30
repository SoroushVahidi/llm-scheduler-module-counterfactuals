"""Saved-evidence integrity and deliberately corrupted synthetic-oracle checks."""
import copy, importlib.util, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('stage4c',Path(__file__).resolve().parents[1]/'scripts/reproduce_stage4c.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Stage4C(unittest.TestCase):
 def test_saved_tables_and_original_oracle(self):
  r=m.reconstruct()
  self.assertEqual(r['pilot']['oracle']['primitive_event_checks'],112)
 def test_oracle_rejects_changed_completion(self):
  p=m.load('data/stage4c/pilot.json');p['records'][0]['base']['completed'][0]['completion']+=1
  with self.assertRaises(AssertionError):m.verify(m.load('data/stage4c/fixtures.json'),p)
 def test_oracle_rejects_fabricated_diagnosis(self):
  p=m.load('data/stage4c/pilot.json');p['records'][0]['B']['opportunity']=1
  with self.assertRaises(AssertionError):m.verify(m.load('data/stage4c/fixtures.json'),p)
 def test_fidelity_counts_valid_and_frames_complete(self):
  r=m.rows('dynamic_units.csv')
  self.assertTrue(all(0<=int(x['agree'])<=int(x['reachable'])<=int(x['states']) for x in r))
  from collections import Counter
  self.assertEqual(set(Counter(x['candidate'] for x in r).values()),{189})
  inv=m.load('data/stage4c/dynamic_candidates.json')
  self.assertEqual(len(inv),72)
  self.assertEqual(len({x['candidate'] for x in r}),57)
if __name__=='__main__':unittest.main()
