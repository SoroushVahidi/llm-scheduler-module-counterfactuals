"""Readable release figures computed from public outcomes; no publisher assets.
Frozen manuscript figure anchors are separate comparison targets, not replacement observations.
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from .analysis import load,compare

def series(result):
    s={}
    for kind,tag in [('priority','p'),('prefill','f')]:
        s[kind+'_controlled']=[dict(label=k,mean=v['delta_anwg']['mean'],ci=v['delta_anwg']['ci95']) for k,v in result[kind]['cells'].items()]
        active=next(v for k,v in result[kind]['cells'].items() if tag+'1_' in k)
        s[kind+'_forest']=[dict(label=p['intervention_id'],mean=p['mean'],ci=p['ci95']) for p in active['pairs']]
    s['interactions']=[dict(label=k+' × fairness',mean=result[k]['interaction']['mean'],ci=result[k]['interaction']['ci95']) for k in ['priority','prefill']]
    e=result['erasure'];s['erasure']=[dict(label='Event-weighted',mean=e['pooled_event_weighted'],ci=e['primary']['pooled_event_weighted_ci95']),dict(label='Equal positive cell',mean=e['equal_positive_cell_mean'],ci=e['primary']['equal_positive_cell_ci95'])]
    s['replay_conditional']=[dict(label=k.replace('_',' '),mean=v['estimate'],ci=v['conditional_percentile_range95']) for k,v in result['replay'].items()]
    pop=result['kv']['six_clean_slot_exploratory']
    for prefix in ['regime:','axes:']:s['kv_'+prefix[:-1]]=[dict(label=k[len(prefix):],mean=v['mean'],ci=v['ci95']) for k,v in sorted(pop.items()) if k.startswith(prefix)]
    cell=next(v for k,v in result['prefill']['cells'].items() if 'f1_' in k)
    s['prefill_request']=[dict(label='Completion-time change fraction',mean=cell['fraction_requests_completion_time_changed']['mean'],ci=cell['fraction_requests_completion_time_changed']['ci95'])]
    return s

def anchor_checks(result):
    # Independent frozen manuscript numbers: compare against newly calculated estimates/CIs.
    forest=load('data/figure_data/fig4_priority_forest.json')
    active=next(v for k,v in result['priority']['cells'].items() if 'p1_' in k)
    target={v['intervention_id']:v for v in forest['interventions']}
    for v in active['pairs']:
        t=target[v['intervention_id']]
        compare([v['mean'],*v['ci95']],[t['mean_delta_anwg'],t['ci_low'],t['ci_high']],2e-9)
    for k,f in zip(['priority','prefill'],load('data/figure_data/fig6_interactions.json')['pairs']):
        compare([result[k]['interaction']['mean'],*result[k]['interaction']['ci95']],[f['interaction'],*f['interaction_ci']],2e-9)
    f3=load('data/figure_data/fig3_priority_opportunity.json')
    p1=next(v for k,v in result['priority']['cells'].items() if 'p1_' in k)
    compare([p1['delta_anwg']['mean'],*p1['delta_anwg']['ci95']],[f3['performance']['signed_mean_delta_anwg_p1'],*f3['performance']['signed_ci_p1']],2e-9)
    f5=load('data/figure_data/fig5_prefill_chain.json')['panels']
    for tag in ['f0','f1']:
        c=next(v for k,v in result['prefill']['cells'].items() if tag+'_' in k)
        for name,field in [('action_divergence','prefill_action_divergence_fraction'),('delta_anwg','delta_anwg'),('timing_changed_fraction','fraction_requests_completion_time_changed')]:
            compare([c[field]['mean'],*c[field]['ci95']],[f5[name][tag+'_mean'],f5[name][tag+'_ci_low'],f5[name][tag+'_ci_high']],2e-9)
    f9=load('data/figure_data/fig9_metric_sensitivity.json')
    for f in f9['families']:
        c=result['metrics']['by_module'][f['id']]
        for key,state in [('invariant','ALL_NEAR_NULL'),('detection_sensitive','DETECTION_SENSITIVE'),('sign_sensitive','SIGN_SENSITIVE')]:
            assert f[key]==c.get(state,0)
    return dict(priority_forest_pairs=28,interaction_intervals=2,prefill_panel_checks=6,metric_family_checks=12,status='PASS',scope='Selected anchors; opportunity min/max and legacy replication marker retained as frozen evidence only')

def render(results_path,output):
    result=json.loads(Path(results_path).read_text());data=series(result)
    checks=anchor_checks(result);output.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':10,'pdf.fonttype':42,'figure.dpi':140})
    recorded={}
    for name,rows in data.items():
        fig,ax=plt.subplots(figsize=(8,max(2.8,len(rows)*.34+1.4)))
        for i,r in enumerate(rows):
            point,=ax.plot(r['mean'],i,'o',color='#0072B2')
            ci=ax.hlines(i,*r['ci'],color='#0072B2')
            # Inspect actual artist coordinates separately from the serialization path.
            actual=float(point.get_xdata()[0]);bounds=ci.get_segments()[0][:,0].tolist()
            compare([actual,*bounds],[r['mean'],*r['ci']],1e-14)
            recorded.setdefault(name,[]).append(dict(label=r['label'],mean=actual,ci=bounds))
        ax.set_yticks(range(len(rows)),[r['label'] for r in rows]);ax.invert_yaxis()
        if name=='erasure':title='Same-state downstream erasure; 56 clustered windows';xlabel='Erasure fraction; conditional post-hoc interval'
        elif name.startswith('kv'):title='Exploratory KV: six declared-slot pairs (semantics unvalidated)';xlabel='ANWG treatment − control; ten seed-stream blocks'
        elif name.startswith('replay'):title='Replay: 21 upstream windows, 63 dependent rate instances';xlabel='Correlation; conditional resampling range, not population coverage'
        elif name=='prefill_request':title='Prefill: request-level changes despite aggregate ANWG null';xlabel='Request fraction; ten workload instances'
        else:title=name.replace('_',' ').capitalize();xlabel='ANWG treatment − control (interaction: four-arm contrast)'
        ax.set_title(title);ax.set_xlabel(xlabel);ax.grid(axis='x',alpha=.2)
        fig.tight_layout();fig.savefig(output/(name+'.pdf'),metadata={'CreationDate':None,'ModDate':None,'Creator':'Matplotlib','Title':title});fig.savefig(output/(name+'.png'));plt.close(fig)
    counts=result['metrics']['counts'];fig,ax=plt.subplots(figsize=(7,3.5))
    names=['ALL_NEAR_NULL','DETECTION_SENSITIVE','SIGN_SENSITIVE'];bars=ax.bar(['All near null','Detection sensitive','Sign sensitive'],[counts[k] for k in names])
    assert [int(b.get_height()) for b in bars]==[3028,655,257]
    ax.bar_label(bars);ax.set_ylim(0,3500);ax.set_ylabel('Matched metric cells');ax.set_title('Numerical tolerance categories, not significance tests');fig.tight_layout()
    fig.savefig(output/'metrics.pdf',metadata={'CreationDate':None,'ModDate':None});fig.savefig(output/'metrics.png');plt.close(fig)
    (output/'plotted_values.json').write_text(json.dumps(dict(series=recorded,metric_counts=counts,anchor_checks=checks),indent=2,sort_keys=True)+'\n')
    print('PASS: actual artist coordinates and selected frozen manuscript anchors')
