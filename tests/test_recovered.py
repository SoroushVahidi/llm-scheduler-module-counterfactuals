"""Independent observation arithmetic, grouping guards, and frozen-baseline comparisons."""
import importlib.util,sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import reconstruct as m
class Recovered(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=m.reconstruct()
 def test_priority_probe_population(self):
  p=self.r['C03']['pdo_p1_generic_opportunity'];self.assertEqual(p['n_instances'],10);m.near(p['candidate'],.3519178293803816);m.near(p['rank'],.27237390582441356)
 def test_historical_quartiles_not_default_interpolation(self):
  self.assertEqual(m._percentile([0,1,2,3],.25),0)
  self.assertEqual(self.r['C10']['n'],72)
  m.near(self.r['C10']['quartiles'],[.9666666666666667,.9978494623655914])
 def test_standalone_fairness_instance_mean(self):
  self.assertEqual(self.r['C16']['n_instances'],5)
  m.near(self.r['C16']['mean_ci'],[-.011872288247500465,-.03274948122995659,0])
 def test_all_heldout_primary_tests_match_original_family(self):
  m.near(self.r['heldout']['multiplicity']['bh_q_values'],[.013993003498250875,.866,.27586206896551724,.27586206896551724])
  self.assertEqual(self.r['heldout']['priority_fairness']['seed_same_sign_count'],1)
 def test_controlled_permutation_and_bh_families(self):
  c=self.r['C07'];m.near(c['priority']['contrast_p'][0],1/2001)
  self.assertEqual(c['priority']['single_families']['pdo_p1_generic_opportunity']['q05'],16)
  self.assertEqual(c['priority']['single_families']['pdo_p1_generic_opportunity']['q10'],17)
  m.near(c['prefill']['contrast_q'],[2/2001,1])
 def test_saved_four_arm_contrasts(self):
  self.assertEqual(self.r['C23']['zero'],63)
  self.assertEqual(len(self.r['C33']),24)
  self.assertTrue(all(v['mean']>0 and v['n']==410 for v in self.r['C33'].values()))
 def test_trajectory_denominator_discrepancy_is_explicit(self):
  c=self.r['C11_trajectory'];self.assertEqual(c['unknown'],232011);self.assertEqual(c['actionable'],364302);self.assertEqual(c['overrides'],356577)
  m.near(c['unknown_over_actionable'],.6368644695884184)
  m.near(c['unknown_over_overrides'],.6506617084108061)
 def test_four_arm_corruption_is_rejected(self):
  d=m.frame('replay_four_arm');d.loc[0,'both_reward']+=.01
  with self.assertRaises(AssertionError):m.arms(d)
 def test_prospective_units_seed_collapse_and_frozen_interval(self):
  p=self.r['prospective'];self.assertEqual(p['seed_rows'],2100);self.assertEqual(p['rate_cells'],420);self.assertEqual(p['H1']['n_windows'],140)
  m.near(p['H1']['delta_r_95ci'],[-.0197308571607414,.18389660134613597])
  self.assertEqual({v['n_windows'] for v in p['by_source'].values()},{20})
  m.near(p['stage_funnel']['pooled']['actionable_override_rate'],.8249233096954524)
 def test_duplicate_seed_cannot_inflate_window_sample(self):
  import pandas as pd
  d=m.frame('prospective_seed_counts');d=pd.concat([d,d.iloc[[0]]])
  with self.assertRaises(ValueError):m.prospective_counts(d)
 def test_corrupt_partition_rejected(self):
  d=m.frame('prospective_seed_counts');d.loc[0,'n_actionable']+=1
  with self.assertRaises(ValueError):m.prospective_counts(d)
if __name__=='__main__':unittest.main()
