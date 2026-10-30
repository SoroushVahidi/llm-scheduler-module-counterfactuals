#!/usr/bin/env python3
"""Reconstruct saved-output summaries; no simulator, model, or network calls."""
import argparse, csv, json, math, random, statistics, sys
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/stage4c'))
from pilot_analyses import instrumented_ablation, diagnostic_protocol
from pilot_verify_pilot import verify

def load(name): return json.loads((ROOT/name).read_text())
def rows(name): return list(csv.DictReader((ROOT/'data/stage4c'/name).open()))
def near(a,b,tol=1e-10):
 if not math.isclose(a,b,rel_tol=0,abs_tol=tol):raise AssertionError((a,b))
def bounds(v,seed=424243):
 rng=random.Random(seed);n=len(v)
 means=sorted(sum(v[rng.randrange(n)] for _ in range(n))/n for _ in range(10000))
 return means[250],means[9750]

def reconstruct():
 ref=load('data/reference/stage4c.json');out={}
 p,q=[load('data/stage4c/'+x+'.json') for x in ['pilot','pilot_repeat']]
 f=load('data/stage4c/fixtures.json')
 oracle=verify(f,p);verify(f,q);assert p['records']==q['records']
 for r in p['records']:
  assert instrumented_ablation(r)==diagnostic_protocol(r)==r['B']==r['C']
 out['pilot']=dict(oracle=oracle,cases=[dict(case=r['case_id'],**r['B']) for r in p['records']],cost={k:p['cost'][k]+q['cost'][k] for k in ['trajectory_executions','local_branch_evaluations']})
 assert out['pilot']['cost']=={'trajectory_executions':56,'local_branch_evaluations':224}
 groups=defaultdict(list)
 for r in rows('erasure_units.csv'):groups[r['family'],r['window']].append(r)
 assert len(groups)==42
 cells=[]
 for (family,window),rr in sorted(groups.items()):
  assert {int(r['seed']) for r in rr}=={910101,910102,910103} and len(rr)==3
  vals={(int(r['actionable']),int(r['erased'])) for r in rr};assert len(vals)==1
  n,e=vals.pop();assert 0<=e<=n
  cells.append(dict(family=family,window=window,actionable=n,erased=e,rate=e/n if n else None))
 out['erasure_extension']={}
 for family in ['admission','kv_guard']:
  rr=[r for r in cells if r['family']==family];rates=[r['rate'] for r in rr if r['rate'] is not None]
  n=sum(r['actionable'] for r in rr);e=sum(r['erased'] for r in rr)
  o=dict(cells=len(rr),positive_cells=len(rates),zero_cells=len(rr)-len(rates),actionable=n,erased=e,pooled_rate=e/n,positive_cell_mean=statistics.mean(rates),saved_mean_cell_interval=list(bounds(rates)))
  want=ref['erasure_extension']['families'][family]
  for k,v in o.items():
   if isinstance(v,list):
    for a,b in zip(v,want[k]):near(a,b)
   else:near(v,want[k])
  out['erasure_extension'][family]=o
 groups=defaultdict(list);dd=rows('dynamic_units.csv')
 assert len(dd)==10773 and len({r['unit'] for r in dd})==10773
 for r in dd:groups[r['family']].append(r);groups['all'].append(r)
 out['dynamic_fidelity']={}
 for family,rr in groups.items():
  n=sum(int(r['reachable']) for r in rr);e=sum(int(r['agree']) for r in rr)
  rates=[int(r['agree'])/int(r['reachable']) for r in rr if int(r['reachable'])]
  o=dict(units=len(rr),positive_units=len(rates),zero_units=len(rr)-len(rates),agree=e,reachable=n,pooled=e/n,mean_positive_unit=statistics.mean(rates))
  for k,v in o.items():near(v,ref['dynamic_fidelity'][family][k])
  out['dynamic_fidelity'][family]=o
 assert sum(int(r['states']) for r in dd)==689472
 bycandidate=defaultdict(list)
 for r in dd:bycandidate[r['candidate']].append(r)
 out['fairness_candidates']={k:dict(units=len(rr),agree=sum(int(r['agree']) for r in rr),reachable=sum(int(r['reachable']) for r in rr)) for k,rr in bycandidate.items() if rr[0]['family']=='fairness_aging'}
 assert len(out['fairness_candidates'])==6 and all(x['agree']<x['reachable'] for x in out['fairness_candidates'].values())
 groups=defaultdict(list);pp=rows('prefill_units.csv');assert len({r['unit'] for r in pp})==756
 for r in pp:groups[r['view'],r['stratum']].append(r)
 out['prefill_fidelity']={}
 for (view,stratum),rr in groups.items():
  assert len(rr)==756 and len({r['unit'] for r in rr})==756
  o=dict(states=sum(int(r['states']) for r in rr),agree=sum(int(r['agree']) for r in rr),positive_units=sum(int(r['states'])>0 for r in rr))
  assert o==ref['prefill_fidelity']['views'][view][stratum]
  out['prefill_fidelity'].setdefault(view,{})[stratum]=o
 # Equality flags remain assertions; only count their saved values here.
 out['real_engine_pairing_audit_assertions']={}
 for campaign in ['v3','priority']:
  rr=load('data/stage4c/'+campaign+'_pair_audit.json')
  out['real_engine_pairing_audit_assertions'][campaign]=dict(pairs=len(rr),arms=2*len(rr),equal_vectors=sum(r['input_vector_equal'] for r in rr),equal_multisets=sum(r['input_multiset_equal'] for r in rr),equal_output_vectors=sum(r['output_vector_equal'] for r in rr))
  assert all(not r['input_vector_equal'] and not r['input_multiset_equal'] and r['output_vector_equal'] for r in rr)
 v3=load('data/stage4c/v3_pair_audit.json');v3by={r['pair'].split('__')[1:][0]+'_'+r['pair'].split('_')[-1]:r['absolute_mean_ttft_difference_ms'] for r in v3}
 cv=[v3by['high_'+str(s)]-v3by['low_'+str(s)] for s in range(993001,993006)]
 pp={(r['regime'],int(r['seed'])):float(r['control_high_priority_ttft_ms'])-float(r['treatment_high_priority_ttft_ms']) for r in rows('priority_arm_means.csv')}
 cp=[pp['HIGH',s]-pp['LOW',s] for s in range(995001,995006)]
 rr=load('data/reference/stage4c_real_engine.json')
 near(statistics.mean(cv),rr['v3_mean']);near(statistics.mean(cp),rr['priority']['mean_C_ms'])
 out['real_engine_contrasts']={}
 for campaign,values in [('v3',cv),('priority',cp)]:
  rng=random.Random(424242);means=sorted(sum(values[rng.randrange(5)] for _ in range(5))/5 for _ in range(10000))
  lower=means[499 if campaign=='v3' else 500];want=rr['v3_lower'] if campaign=='v3' else rr['priority']['bootstrap_one_sided_95_lower']
  near(lower,want)
  out['real_engine_contrasts'][campaign]=dict(per_seed=values,mean_ms=statistics.mean(values),positive_seeds=sum(x>0 for x in values),one_sided_lower_ms=lower,interpretation='Saved arithmetic only; identical-input causal pairing unestablished')
 out['verification']='PASS: saved-output arithmetic and synthetic oracle; no experimental execution'
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('output/stage4c'));a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 out=reconstruct();(a.output/'results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 # Machine-readable tables are regenerated directly from computed results.
 for key in ['erasure_extension','dynamic_fidelity','real_engine_pairing_audit_assertions','real_engine_contrasts','fairness_candidates']:
  with (a.output/(key+'.csv')).open('w') as f:
   rr=[dict(group=k,**v) for k,v in out[key].items()];w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
 with (a.output/'pilot.csv').open('w') as f:
  rr=out['pilot']['cases'];w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
 with (a.output/'prefill_fidelity.csv').open('w') as f:
  rr=[dict(view=v,stratum=s,**d) for v,ss in out['prefill_fidelity'].items() for s,d in ss.items()];w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
 print(out['verification'])
if __name__=='__main__':main()
