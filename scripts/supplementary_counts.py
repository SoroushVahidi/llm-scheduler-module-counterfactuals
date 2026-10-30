#!/usr/bin/env python3
"""Additional arithmetic on v0.1.0 observations; no scientific executions."""
import argparse,json,statistics
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('output/supplementary'));a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 out={}
 cells=[c for w in load('data/diagnostics/erasure_windows.json') for c in w['cells'] if c['denominator']]
 rates=[c['numerator']/c['denominator'] for c in cells]
 out['original_erasure_heterogeneity']=dict(linear_quantiles=np.quantile(rates,[0,.25,.5,.75,1]).tolist(),lower_order_quartiles=np.quantile(rates,[.25,.75],method='lower').tolist(),note='Historical code uses sorted[floor(q*(n-1))]; see analysis/historical_quartile.py and provenance/recovered_sources.json. Linear interpolation is a different convention.',zero_rate_denominators=[c['denominator'] for c in cells if c['numerator']==0])
 rr=load('data/diagnostics/public_replay.json');sources=sorted({r['source'] for r in rr})
 out['replay_by_source']={s:float(np.corrcoef([r['candidate'] for r in rr if r['source']==s],[r['priority_divergence'] for r in rr if r['source']==s])[0,1]) for s in sources}
 out['replay_between_source']=float(np.corrcoef([statistics.mean(r['candidate'] for r in rr if r['source']==s) for s in sources],[statistics.mean(r['priority_divergence'] for r in rr if r['source']==s) for s in sources])[0,1])
 arms=load('data/outcomes/prefill_four_arm.json')
 out['prefill_isolated']={key:statistics.mean(r[key]-r['base_reward'] for r in arms) for key in ['first_reward','second_reward','both_reward']}
 assert round(out['replay_between_source'],3)==-.467
 assert round(out['prefill_isolated']['first_reward'],4)==-.0442
 assert round(out['prefill_isolated']['second_reward'],4)==-.0289
 fig,ax=plt.subplots(figsize=(7,3));artists=[]
 for i,kind in enumerate(['priority','prefill']):
  v=[r['interaction'] for r in load('data/outcomes/'+kind+'_four_arm.json')]
  artist=ax.scatter(v,[i]*len(v));assert np.allclose(artist.get_offsets()[:,0],v);artists.append(v)
 ax.axvline(0,color='gray');ax.set_yticks([0,1],['Priority × fairness','Prefill × fairness']);ax.set_xlabel('Four-arm ANWG interaction (ten paired seeds per campaign)');fig.tight_layout();fig.savefig(a.output/'interaction_seeds.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 out['seed_strip_values']=artists
 (a.output/'counts.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print('PASS: supplementary arithmetic and seed-strip coordinates from v0.1.0 observations')
if __name__=='__main__':main()
