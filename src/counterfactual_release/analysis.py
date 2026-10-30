"""Outcome-only reconstruction. All inference preserves paired workload/window blocks.
New release adapters; inherited formulas/seeds are documented in provenance.
"""
import collections, csv, json, random, statistics
from pathlib import Path
import numpy as np
from .primitives import (B, stable_seed, interval, estimands, erasure_bootstrap,
                         kv_summary, seed, classify, calculate, draw_blocks)
ROOT=Path(__file__).resolve().parents[2]
def load(path):return json.loads((ROOT/path).read_text())
def means_by(rows,field,key='config_id'):
    groups=collections.defaultdict(list)
    for r in rows:groups[r[key]].append(float(r[field]))
    return [statistics.mean(groups[k]) for k in sorted(groups)]
def mean_ci(values,random_seed,b=2000):
    values=np.asarray(values,float)
    if not len(values) or not np.all(np.isfinite(values)):raise ValueError('finite nonempty values required')
    rng=np.random.default_rng(random_seed)
    draws=np.mean(values[rng.integers(0,len(values),(b,len(values)))],axis=1)
    mean=float(np.mean(values));hits=int(np.sum(draws<=0 if mean>=0 else draws>=0))
    return dict(mean=mean,ci95=[float(x) for x in np.quantile(draws,[.025,.975])],
                n_units=len(values),B=b,tail_hits=hits,
                historical_tail_fraction=min(1.,2*hits/b),
                plus_one_tail_sensitivity=min(1.,2*(hits+1)/(b+1)))
def bh(ps):
    order=sorted(range(len(ps)),key=lambda i:ps[i]);q=[1.]*len(ps);last=1.
    for rank in range(len(ps),0,-1):
        i=order[rank-1];last=min(last,ps[i]*len(ps)/rank);q[i]=last
    return q

def controlled(kind):
    rows=load('data/outcomes/'+kind+'.json');diags=load('data/diagnostics/'+kind+'.json')
    arms=load('data/outcomes/'+kind+'_four_arm.json')
    rs=1231191560 if kind=='priority' else 1827463921
    cells={}
    for cell in sorted({r['cell_id'] for r in rows}):
        sub=[r for r in rows if r['cell_id']==cell];dg=[r for r in diags if r['cell_id']==cell]
        out={'delta_anwg':mean_ci(means_by(sub,'delta_anwg'),rs),
             'n_pairs':len({r['intervention_id'] for r in sub}),
             'n_seeds':len({r['seed'] for r in sub}), 'n_rows':len(sub)}
        keys=['decision_divergence_rate'] if kind=='priority' else ['prefill_action_divergence_fraction','fraction_requests_completion_time_changed','median_abs_completion_time_diff']
        for k in keys:out[k]=mean_ci(means_by(dg,k),rs)
        forest=[]
        for iid in sorted({r['intervention_id'] for r in sub}):
            pair=[r for r in sub if r['intervention_id']==iid]
            forest.append(dict(intervention_id=iid,base=pair[0]['base_policy'],donor=pair[0]['donor_policy'],**mean_ci(means_by(pair,'delta_anwg'),rs)))
        for r,q in zip(forest,bh([r['plus_one_tail_sensitivity'] for r in forest])):r['plus_one_bh_q']=q
        out['pairs']=forest;cells[cell]=out
    # Serialized canonical values carry 10-decimal rounding. Four-arm contrast tolerance reflects this only.
    for a in arms:
        contrast=a['both_reward']-a['first_reward']-a['second_reward']+a['base_reward']
        if abs(contrast-a['interaction'])>3e-10:raise AssertionError('four-arm mismatch')
    return dict(cells=cells,interaction=mean_ci(means_by(arms,'interaction'),rs),
                unit='workload instance; all fixed pairs retained jointly; 10 independent generation seeds per condition',
                rounding='canonical observations serialized to 10 decimal places; reference agreement tolerance 2e-9')

def erasure():
    windows=load('data/diagnostics/erasure_windows.json');cells=[c for w in windows for c in w['cells']]
    assert all(0<=c['numerator']<=c['denominator'] for c in cells)
    p,m=estimands(cells)
    return dict(numerator=sum(c['numerator'] for c in cells),denominator=sum(c['denominator'] for c in cells),
        pooled_event_weighted=p,equal_positive_cell_mean=m,
        counts=dict(windows=len(windows),sources=len({w['source'] for w in windows}),pairs=len({c['pair'] for c in cells}),cells=len(cells),positive_cells=sum(c['denominator']>0 for c in cells),zero_cells=sum(c['denominator']==0 for c in cells),positive_windows=sum(any(c['denominator'] for c in w['cells']) for w in windows)),
        primary=erasure_bootstrap(windows),unstratified_sensitivity=erasure_bootstrap(windows,False),source_hierarchical_sensitivity=erasure_bootstrap(windows,hierarchical=True))

def kv():
    rows=load('data/outcomes/kv.json')
    assert len({(r['config_id'],r['intervention_id']) for r in rows})==len(rows)
    assert all(abs(r['reward_v1_corrected']-r['reward_base']-r['gain_v1_corrected'])<2e-10 for r in rows)
    pops={'six_clean_slot_exploratory':[r for r in rows if r['module_type']=='kv_guard'],
          'mixed_thirteen_historical_sensitivity':rows,
          'one_unflagged_pair_sensitivity':[r for r in rows if r['module_type']=='kv_guard' and r['base_policy']=='aging_priority']}
    result={}
    for name,pop in pops.items():
        groups=collections.defaultdict(list)
        for r in pop:groups['regime:'+r['regime'] if r['regime'] else 'axes:'+str(int(r['n_elevated_axes']))].append(r)
        result[name]={key:kv_summary(rs,name+'|'+key) for key,rs in {'overall':pop,**groups}.items()}
    return result

def replay_groups(rows):
    windows={}
    for r in rows:windows.setdefault((r['source'],r['window_index']),[]).append(r)
    groups=collections.defaultdict(list)
    for (source,_),block in windows.items():
        if len(block)!=3 or {r['rate'] for r in block}!={.5,1.,2.}:raise ValueError('each upstream window must retain all three rates')
        groups[source].append(block)
    return groups

def replay():
    rows=load('data/diagnostics/public_replay.json');groups=replay_groups(rows);out={}
    for name,which,center in [('priority_pooled','priority',False),('priority_source_centered','priority',True),('prefill_pressure_action','prefill_pressure',False),('prefill_action_request','prefill_request',False)]:
        rng=random.Random(seed(name));values=[];undefined=0
        for _ in range(B):
            v=calculate([r for block in draw_blocks(groups,rng) for r in block],center,which)
            if v is None:undefined+=1
            else:values.append(v)
        out[name]=dict(estimate=calculate(rows,center,which),conditional_percentile_range95=[float(v) for v in np.quantile(values,[.025,.975])],undefined_draws=undefined,seed=seed(name))
    return out

def metrics():
    with (ROOT/'data/outcomes/metrics.csv').open() as f:rows=list(csv.DictReader(f))
    ids=set();counts=collections.Counter();by_module=collections.defaultdict(collections.Counter)
    for r in rows:
        key=(r['workload_id'],r['intervention_id']);assert key not in ids;ids.add(key);effects=[]
        for m in ['anwg','mean_soft_credit','wcg','wmt','wnt']:
            diff=float(r['intervention_'+m])-float(r['base_'+m]);diff= -diff if m in ('wmt','wnt') else diff
            assert abs(diff-float(r['effect_'+m]))<1e-14
            effects.append(diff)
        state=classify(effects);assert state==r['state'];counts[state]+=1;by_module[r['module_type']][state]+=1
    return dict(n_cells=len(rows),counts=dict(counts),by_module={k:dict(v) for k,v in by_module.items()})

def compare(actual,expected,tol=2e-12):
    if isinstance(expected,dict):
        for k,v in expected.items():compare(actual[k],v,tol)
    elif isinstance(expected,list):
        assert len(actual)==len(expected)
        for a,e in zip(actual,expected):compare(a,e,tol)
    elif isinstance(expected,(int,float)):
        assert abs(actual-expected)<=tol,(actual,expected)
    else:assert actual==expected,(actual,expected)

def verify(result):
    e=load('data/reference/erasure.json');compare(result['erasure'],{k:e[k] for k in result['erasure']})
    compare(result['kv'],load('data/reference/kv.json')['populations'])
    compare(result['replay'],load('data/reference/public_replay.json')['statistics'])
    assert result['metrics']['counts']=={'ALL_NEAR_NULL':3028,'DETECTION_SENSITIVE':655,'SIGN_SENSITIVE':257}
    for kind in ['priority','prefill']:
        r=result[kind];ref=load('data/reference/'+kind+'.json');old=load('data/reference/controlled_statistics.json')[kind]
        for key,s in ref.items():
            if key=='interaction':g=r['interaction'];target=s['mean_interaction']
            else:g=r['cells'][s['cell_id']]['delta_anwg'];target=s['mean_delta_anwg']
            compare([g['mean'],*g['ci95']],[target,s['ci_low'],s['ci_high']],2e-9)
            if key!='interaction':
                for field,mean,ci in [('fraction_requests_completion_time_changed','fraction_requests_completion_time_changed_mean','fraction_requests_completion_time_changed_ci'),('median_abs_completion_time_diff','median_abs_completion_time_diff_mean','median_abs_completion_time_diff_ci')]:
                    if mean in s:compare([r['cells'][s['cell_id']][field]['mean'],*r['cells'][s['cell_id']][field]['ci95']],[s[mean],*s[ci]],2e-9)
        cell=next(v for k,v in r['cells'].items() if ('p1_' if kind=='priority' else 'f1_') in k)
        assert sum(v['plus_one_bh_q']<.1 for v in cell['pairs'])==old['plus_one_fdr_count']
        frozen={x['intervention_id']:x for x in old['per_intervention']}
        for p in cell['pairs']:
            assert p['tail_hits']==frozen[p['intervention_id']]['tail_hits']
    return dict(status='PASS',scope='outcome reconstruction only',comparison_tolerance=2e-12,canonical_rounding_tolerance=2e-9)

def run(output):
    result={k:f() for k,f in [('priority',lambda:controlled('priority')),('prefill',lambda:controlled('prefill')),('erasure',erasure),('kv',kv),('replay',replay),('metrics',metrics)]}
    result['verification']=verify(result)
    output.mkdir(parents=True,exist_ok=True)
    (output/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    # A rectangular table makes selected results accessible without executing plotting code.
    with (output/'selected_tables.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['analysis','estimate','lower95','upper95','unit'])
        for k in ['priority','prefill']:
            v=result[k]['interaction'];w.writerow([k+'_interaction',v['mean'],*v['ci95'],'10 workload instances'])
        for k,ci in [('pooled_event_weighted','pooled_event_weighted_ci95'),('equal_positive_cell_mean','equal_positive_cell_ci95')]:
            w.writerow([k,result['erasure'][k],*result['erasure']['primary'][ci],'source-stratified whole windows'])
        for k,v in result['replay'].items():w.writerow([k,v['estimate'],*v['conditional_percentile_range95'],'conditional source-window sensitivity'])
    return result
