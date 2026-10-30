"""Independent arithmetic/schedule oracle; no simulator or analyzer imports."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def verify(fixtures, payload):
    assert [x['case_id'] for x in fixtures] == [x['case_id'] for x in payload['records']]
    checks=0
    for fixture,row in zip(fixtures,payload['records']):
        requests={r['request_id']:r for r in fixture['requests']}
        cap=fixture['capacity']
        for arm,rule in [('base','fifo'),('donor',fixture['donor'])]:
            schedule=fixture['expected'][arm]
            actual={str(r['id']):dict(admission=r['admission'],completion=r['completion']) for r in row[arm]['completed']}
            assert actual==schedule, (fixture['case_id'],arm,'schedule')
            for rec in row[arm]['completed']:
                assert rec['met'] == (rec['completion'] <= requests[rec['id']]['slo_deadline'])
            for rid, rec in schedule.items():
                assert rec['completion']==rec['admission']+requests[int(rid)]['actual_output_tokens']
            successful=sum(s['completion']<=requests[int(i)]['slo_deadline'] for i,s in schedule.items())
            assert row[arm]['metrics']['arrival_normalized_weighted_goodput']==successful/len(requests)
            for entry in row[arm]['applied']:
                t=entry['time']
                expected=sorted(int(i) for i,s in schedule.items() if s['admission']==t)
                assert entry['admitted']==expected, (fixture['case_id'],arm,t,'actual admissions')
                assert sorted(entry['action']['admit'].get('0',[]))==expected
                checks+=1
        base=fixture['expected']['base']
        for e in row['base']['events']:
            t=e['snapshot']['time']
            waiting=[i for i,r in requests.items() if r['arrival_time']<=t and base[str(i)]['admission']>=t]
            active=[int(i) for i,s in base.items() if s['admission']<t<s['completion']]
            assert sorted(r['request_id'] for r in e['snapshot']['waiting_queue'])==sorted(waiting)
            assert sorted(e['snapshot']['gpu_states'][0]['active_request_ids'])==sorted(active)
            assert len(active)<=cap
            for prefix,rule in [('base','fifo'),('donor',fixture['donor'])]:
                def key(i):
                    r=requests[i]
                    return (r['slo_deadline'],r['arrival_time'],i) if rule=='edf' else (r['arrival_time'],i)
                order=sorted(waiting,key=key)
                # Large KV/batch budgets make slots the only placement constraint.
                assert e[prefix+'_rank']==order
                assert e[prefix+'_action']['admit'].get('0',[])==order[:cap-len(active)]
                assert all(not value for key,value in e[prefix+'_action'].items() if key!='admit')
                checks+=1
        assert row['B']==row['C'], (fixture['case_id'],'baseline disagreement')
        for k,v in fixture['expected']['counts'].items():
            assert row['B'][k]==v, (fixture['case_id'],k)
        n=fixture['expected']['counts']['disagreement']
        z=fixture['expected']['counts']['erased']
        assert row['B']['erasure_fraction']==(z/n if n else None)
        changed=sorted(int(i) for i in base if base[i]['completion']!=fixture['expected']['donor'][i]['completion'])
        assert row['B']['changed_requests']==changed
        assert row['B']['unmatched_requests']==[]
        assert row['B']['request_denominator']==len(requests)
        assert row['B']['decisions']==len(row['base']['events'])
        assert row['B']['local_action_differences']==n-z
        expected_delta=sum(s['completion']<=requests[int(i)]['slo_deadline'] for i,s in fixture['expected']['donor'].items())/len(requests)-sum(s['completion']<=requests[int(i)]['slo_deadline'] for i,s in base.items())/len(requests)
        assert row['B']['delta_anwg']==expected_delta
        assert row['observer_neutrality'] is True
    return dict(status='PASS',cases=len(fixtures),primitive_event_checks=checks,
                ground_truth='pre-execution admission/completion schedules plus independent integer-capacity/service arithmetic',
                independence_limit='separate code path, same research agent; not independent-team validation')
