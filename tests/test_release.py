import collections,csv,math,random,unittest
from counterfactual_release import analysis as a
from counterfactual_release.primitives import estimands,draw_windows,draw_blocks,stable_seed,seed,classify,calculate,erasure_bootstrap
class PublicReconstructionTests(unittest.TestCase):
    def test_estimands_not_interchangeable(self):
        self.assertEqual(estimands([dict(numerator=9,denominator=10),dict(numerator=0,denominator=1),dict(numerator=0,denominator=0)]),(9/11,.45))
    def test_empty_denominator_is_undefined(self):
        self.assertEqual(estimands([dict(numerator=0,denominator=0)]),(None,None))
    def test_all_empty_bootstrap(self):
        r=erasure_bootstrap([dict(source='a',cells=[dict(numerator=0,denominator=0)])],b=7)
        self.assertEqual(r['undefined_draws'],7);self.assertIsNone(r['pooled_event_weighted_ci95'])
    def test_erasure_cells_never_resampled_alone(self):
        windows=a.load('data/diagnostics/erasure_windows.json');groups=collections.defaultdict(list)
        for w in windows:groups[w['source']].append(w)
        draw=draw_windows(groups,random.Random(2));self.assertEqual(len(draw),56)
        self.assertTrue(all(any(w is original for original in windows) for w in draw))
        self.assertTrue(all(len(w['cells'])==3 and len(w['seeds'])==3 for w in draw))
        self.assertEqual(collections.Counter(w['source'] for w in draw),collections.Counter(w['source'] for w in windows))
    def test_erasure_denominators(self):
        ws=a.load('data/diagnostics/erasure_windows.json');cs=[c for w in ws for c in w['cells']]
        self.assertEqual((len(cs),sum(c['denominator']>0 for c in cs)),(168,72))
        self.assertEqual((sum(c['numerator'] for c in cs),sum(c['denominator'] for c in cs)),(338241,340548))
    def test_portable_seed(self):
        self.assertEqual(seed('priority_pooled'),7145265818209731858)
        self.assertEqual(stable_seed('erasure-stratified'),stable_seed('erasure-stratified'))
    def test_replay_three_rates_stay_together(self):
        rows=a.load('data/diagnostics/public_replay.json');groups=a.replay_groups(rows)
        self.assertEqual((len(groups),sum(map(len,groups.values()))),(7,21))
        draws=draw_blocks(groups,random.Random(13))
        for block in draws:
            self.assertEqual({r['rate'] for r in block},{.5,1.,2.})
            self.assertEqual(len({(r['source'],r['window_index']) for r in block}),1)
        with self.assertRaises(ValueError):a.replay_groups(rows[:-1])
    def test_source_centering_recomputed(self):
        rs=[dict(source=s,candidate=x,priority_divergence=y) for s,x,y in [('a',0,0),('a',2,4),('b',10,6),('b',12,10)]]
        self.assertAlmostEqual(calculate(rs,True),1.)
        self.assertNotAlmostEqual(calculate(rs),1.)
    def test_metric_orientation_categories(self):
        self.assertEqual(classify([0,0,0,0,0]),'ALL_NEAR_NULL')
        self.assertEqual(classify([0,1,0,0,0]),'DETECTION_SENSITIVE')
        self.assertEqual(classify([1,-1,0,0,0]),'SIGN_SENSITIVE')
        self.assertEqual(classify([1]*5),'NON_NULL_SAME_DIRECTION')
        with self.assertRaises(ValueError):classify([math.nan])
        self.assertEqual(a.metrics()['counts'],{'ALL_NEAR_NULL':3028,'DETECTION_SENSITIVE':655,'SIGN_SENSITIVE':257})
    def test_workload_clustering(self):
        rows=[dict(config_id='x',v=0),dict(config_id='x',v=2),dict(config_id='y',v=10)]
        self.assertEqual(a.means_by(rows,'v'),[1,10])
    def test_four_arm_controls_and_nulls(self):
        for kind in ['priority','prefill']:
            d=a.controlled(kind);self.assertEqual(d['interaction']['n_units'],10)
            active=next(v for k,v in d['cells'].items() if ('p1_' if kind=='priority' else 'f1_') in k)
            self.assertEqual(active['delta_anwg']['n_units'],10)
            if kind=='prefill':self.assertEqual(active['delta_anwg']['mean'],0.)
    def test_finite_tail_resolution(self):
        d=a.mean_ci([1]*10,1)
        self.assertEqual(d['historical_tail_fraction'],0)
        self.assertEqual(d['plus_one_tail_sensitivity'],2/2001)
    def test_compatibility_is_not_runtime_acceptance(self):
        rows=a.load('data/diagnostics/kv_compatibility.json')
        self.assertEqual(collections.Counter(r['classification'] for r in rows),{'INVALID':5,'INCONCLUSIVE':5})
        kv=a.load('data/outcomes/kv.json');clean=[r for r in kv if r['module_type']=='kv_guard']
        self.assertEqual((len(kv),len(clean),len([r for r in clean if r['base_policy']=='aging_priority'])),(5330,2460,410))
if __name__=='__main__':unittest.main()
