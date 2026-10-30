#!/usr/bin/env python3
"""Reconstruct additional claims from saved observations, without scientific execution."""
import argparse,json,sys
from pathlib import Path
import numpy as np
import pandas as pd
from historical_statistics import (ci_mean_instances,bootstrap_two_sided_p,permutation_p_instances,bh_qvalues,priority_generalization,prefill_generalization,priority_fairness_generalization,kv_guard_generalization)
from historical_quartile import _percentile
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/name).read_text())
def frame(name):return pd.DataFrame(load('data/recovered/'+name+'.json'))
def near(a,b,tol=2e-9):
 if not np.allclose(a,b,atol=tol,rtol=0,equal_nan=True):raise AssertionError(f'{a!r} != {b!r}; tolerance {tol}')
def arms(df,suffix=''):
 result=df['both_reward'+suffix]-df['first_reward'+suffix]-df['second_reward'+suffix]+df['base_reward']
 near(result,df['interaction_v1_corrected' if suffix else 'interaction'])
 return result

def compare_numeric(actual,reference,path=''):
 """Compare calculated named outputs to frozen references; references are never inputs."""
 if isinstance(actual,dict):
  for k,v in actual.items():
   if k in reference:compare_numeric(v,reference[k],path+'/'+k)
 elif isinstance(actual,list):
  if isinstance(reference,list):
   assert len(actual)==len(reference),path
   for i,(a,b) in enumerate(zip(actual,reference)):compare_numeric(a,b,path+f'/{i}')
 elif isinstance(actual,(int,float)) and not isinstance(actual,bool):
  try:near(actual,reference)
  except AssertionError as e:raise AssertionError(path+': '+str(e)) from e

def prospective_counts(df):
 """First average seed ratios, then use one source-window at 1x as inference unit."""
 keys=['config_id','source_key','window_role','replay_rate_multiplier']
 if df.duplicated(keys+['seed']).any():raise ValueError('duplicate seed cell')
 if set(df.groupby(keys).size())!={5}:raise ValueError('expected five saved seeds per cell')
 if (df['n_decisions']<=0).any():raise ValueError('nonpositive decision denominator')
 for key in ['n_structural_ge2','n_actionable','n_final_action_divergent']:
  if ((df[key]<0)|(df[key]>df['n_decisions'])).any():raise ValueError('invalid count')
 if not (df.n_actionable==df.n_actionable_and_final_divergent+df.n_actionable_but_final_same).all():raise ValueError('actionable counts do not partition')
 d=df.copy()
 for num,den,name in [('n_structural_ge2','n_decisions','structural_opportunity_rate'),('n_actionable','n_decisions','actionable_opportunity_rate'),('n_final_action_divergent','n_decisions','final_action_divergence_rate'),('n_actionable','n_structural_ge2','actionable_given_structural_rate'),('n_actionable_but_final_same','n_actionable','actionable_override_rate')]:d[name]=d[num]/d[den].replace(0,np.nan)
 cols=['structural_opportunity_rate','actionable_opportunity_rate','final_action_divergence_rate','actionable_given_structural_rate','actionable_override_rate']
 w=d.groupby(keys,sort=True)[cols].mean().reset_index()
 family={'burstgpt_v2_without_fails_1':'burstgpt','azure_llm_2023_code':'azure_2023','azure_llm_2023_conversation':'azure_2023','azure_llm_2024_code':'azure_2024','azure_llm_2024_conversation':'azure_2024','mooncake_fast25_conversation':'mooncake','mooncake_fast25_toolagent':'mooncake'}
 w['source_family']=w.source_key.map(family)
 if w.source_family.isna().any():raise ValueError('unmapped source')
 primary=w[np.isclose(w.replay_rate_multiplier,1)].copy()
 if primary.duplicated(['source_key','window_role']).any():raise ValueError('duplicate source window')
 return w,primary

def corr(d,x):return float(np.corrcoef(d[x],d.final_action_divergence_rate)[0,1])
def prospective(df):
 w,p=prospective_counts(df);assert len(w)==420 and len(p)==140
 columns=['structural_opportunity_rate','actionable_opportunity_rate','final_action_divergence_rate']
 blocks=[g[columns].to_numpy() for _,g in p.groupby('source_family')]
 rng=np.random.default_rng(4108260827);ds=[]
 for _ in range(2000):
  x=np.concatenate([g[rng.integers(0,len(g),len(g))] for g in blocks]);r=np.corrcoef(x.T);ds.append(r[1,2]-r[0,2])
 rs=corr(p,columns[0]);ra=corr(p,columns[1]);ci=np.percentile(ds,[2.5,97.5]).tolist()
 centered=p.copy()
 for c in columns:centered[c]=p[c]-p.groupby('source_family')[c].transform('mean')
 h1=dict(r_structural_1x=rs,r_actionable_1x=ra,delta_r_1x=ra-rs,delta_r_95ci=ci,n_windows=len(p),bootstrap_b=2000)
 h2=dict(source_centered_r_structural=corr(centered,columns[0]),source_centered_r_actionable=corr(centered,columns[1]));h2['source_centered_delta_r']=h2['source_centered_r_actionable']-h2['source_centered_r_structural']
 by_source={k:dict(n_windows=len(g),r_structural=corr(g,columns[0]),r_actionable=corr(g,columns[1])) for k,g in p.groupby('source_key')}
 funnel={k:dict(n_windows=len(g),**{c:float(g[c].mean()) for c in columns+['actionable_given_structural_rate','actionable_override_rate']}) for k,g in [('pooled',p),*list(p.groupby('source_family'))]}
 moon=p[p.source_family=='mooncake'];h4=dict(combined_r_structural=corr(moon,columns[0]),combined_r_actionable=corr(moon,columns[1]))
 reference=load('data/stage4c/prospective_summary.json')
 for key,value in [('H1',h1),('H2',h2),('H4_mooncake',h4)]:compare_numeric(value,reference[key],key)
 return dict(H1=h1,H2=h2,H4_mooncake=h4,by_source=by_source,stage_funnel=funnel,seed_rows=len(df),rate_cells=len(w))

def controlled_tests():
 out={}
 for kind,seed,low,high,divcol in [('priority',1231191560,'pdo_p0_pressure_no_opportunity','pdo_p1_generic_opportunity','decision_divergence_rate'),('prefill',1827463921,'fdo_f0_inactive_control','fdo_f1_high_pressure_opportunity','prefill_action_divergence_fraction')]:
  d=pd.DataFrame(load('data/diagnostics/'+kind+'.json'));o=pd.DataFrame(load('data/outcomes/'+kind+'.json'))
  ps=[]
  for table,col in [(d,divcol),(o,'delta_anwg')]:
   groups=[table[table.cell_id==c].groupby('config_id')[col].apply(lambda s:float(np.mean(np.abs(s)))).to_numpy() for c in [low,high]]
   ps.append(permutation_p_instances(*groups,seed=seed,b=2000))
  counts={}
  for c in [low,high]:
   vals=[]
   for _,g in o[o.cell_id==c].groupby('intervention_id'):
    v=g.groupby('config_id').delta_anwg.mean().to_numpy();vals.append(bootstrap_two_sided_p(v,seed=seed,b=2000))
   qs=np.array(bh_qvalues(vals));counts[c]=dict(n_tests=len(qs),q05=int(sum(qs<.05)),q10=int(sum(qs<.10)))
  out[kind]=dict(contrast_p=ps,contrast_q=bh_qvalues(ps),single_families=counts)
 return out

def reconstruct():
 out={}
 p=frame('priority_probes');out['C03']={c:dict(n_instances=len(g),candidate=float(g.candidate_set_ge2_fraction.mean()),rank=float(g.priority_rank_disagreement_fraction.mean())) for c,g in p.groupby('cell_id')}
 rates=sorted(c['numerator']/c['denominator'] for w in load('data/diagnostics/erasure_windows.json') for c in w['cells'] if c['denominator'])
 out['C10']=dict(n=len(rates),median=float(np.median(rates)),quartiles=[_percentile(rates,q) for q in [.25,.75]],range=[min(rates),max(rates)],method='sorted[floor(q*(n-1))], historical code')
 f=frame('fairness');near(f.reward_intervention-f.reward_base,f.delta_anwg)
 v=f[f.cell_id=='v2_fair_act'].groupby('config_id').delta_anwg.mean().to_numpy();out['C16']=dict(n_instances=len(v),mean_ci=ci_mean_instances(v,seed=20270225,b=2000))
 singles=frame('heldout_singles');near(singles.reward_intervention-singles.reward_base,singles.delta_anwg);near(abs(singles.delta_anwg),singles.abs_delta_anwg)
 pairs=frame('heldout_pairwise');arms(pairs);div=frame('heldout_divergence');pp=frame('heldout_priority_probes');fp=frame('heldout_prefill_probes')
 h=dict(priority=priority_generalization(singles,div,pp),priority_fairness=priority_fairness_generalization(pairs,pp),kv_guard=kv_guard_generalization(singles),prefill=prefill_generalization(singles,div,fp))
 ps=[h['priority']['low_vs_higher_opportunity_divergence_permutation_p'],h['priority_fairness']['interaction']['bootstrap_p'],h['kv_guard']['low_vs_higher_pressure_abs_delta_permutation_p'],h['prefill']['active_vs_inactive_divergence_permutation_p']]
 qs=bh_qvalues(ps);h['priority_fairness']['interaction']['bh_q']=qs[1];h['multiplicity']=dict(raw_p_values=ps,bh_q_values=qs)
 compare_numeric(h,load('data/reference/recovered_heldout.json'))
 out['heldout']=h
 replay=frame('replay_four_arm');ri=arms(replay);out['C23']=dict(n=len(ri),zero=int(sum(abs(ri)<1e-12)),max_abs=float(max(abs(ri))))
 kv=frame('kv_pairwise');ki=arms(kv,'_v1');kv=kv.assign(reconstructed_interaction=ki)
 out['C33']={k:dict(n=len(g),mean=float(g.reconstructed_interaction.mean()),n_streams=int(g.heldout_stream_index.nunique())) for k,g in kv.groupby('pairwise_id')}
 out['prospective']=prospective(frame('prospective_seed_counts'))
 out['C07']=controlled_tests()
 local=load('data/recovered/local_stage_counts.json');out['C11_partial_local_only']={}
 for pair in sorted({r['pair_id'] for r in local}):
  rows=[r for r in local if r['pair_id']==pair];cs={k:sum(r['cause_counts'][k] for r in rows) for k in rows[0]['cause_counts']};den=sum(r['local_overrides'] for r in rows);assert sum(cs.values())==den
  out['C11_partial_local_only'][pair]=dict(n_seed_cells=len(rows),overrides=den,cause_counts=cs,cause_shares={k:v/den for k,v in cs.items()})
 trajectory=load('data/recovered/trajectory_stage_counts.json')
 from collections import Counter
 counts=Counter()
 for row in trajectory:counts.update(row['counts'])
 actionable=counts['actionable'];final=counts['final_divergent'];unknown=counts['cause_UNKNOWN_AMBIGUOUS']
 out['C11_trajectory']=dict(n_pair_windows=len(trajectory),actionable=actionable,overrides=actionable-final,unknown=unknown,unknown_over_actionable=unknown/actionable,unknown_over_overrides=unknown/(actionable-final),cause_counts=dict(counts),denominator_discrepancy='Manuscript says overrides for 63.7%; saved calculation divides by all actionable steps. No full claim-as-written credit.')
 near(unknown/actionable,load('data/stage4c/original_erasure_taxonomy_summary.json')['ambiguity_reduction']['trajectory_unknown_ambiguous_rate'])
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('output/recovered'));a=ap.parse_args();r=reconstruct();a.output.mkdir(parents=True,exist_ok=True)
 (a.output/'results.json').write_text(json.dumps(r,indent=2,sort_keys=True,allow_nan=True)+'\n')
 print('PASS: additional saved-observation reconstructions; no experimental execution')
if __name__=='__main__':main()
