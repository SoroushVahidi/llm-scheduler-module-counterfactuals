"""Three observation contracts. No fixtures, ground-truth labels or simulator imports."""

def aggregate_ablation(record):
    b, d = record['base'], record['donor']
    delta = d['metrics']['arrival_normalized_weighted_goodput'] - b['metrics']['arrival_normalized_weighted_goodput']
    return dict(delta_anwg=delta, aggregate_changed=delta != 0,
                mechanism='not identifiable from primary aggregate contrast alone',
                base_metrics=b['metrics'], donor_metrics=d['metrics'])


def instrumented_ablation(record):
    """Generic relational/set queries, not a sequential funnel classifier."""
    rows = record['base']['events']
    competition = {i for i, r in enumerate(rows) if len(r['snapshot']['waiting_queue']) >= 2}
    mismatch = {i for i, r in enumerate(rows) if r['base_rank'][:1] != r['donor_rank'][:1]}
    equal_actions = {i for i, r in enumerate(rows) if set(r['base_action']['admit'].get('0', [])) == set(r['donor_action']['admit'].get('0', []))}
    b = {r['id']: r for r in record['base']['completed']}
    d = {r['id']: r for r in record['donor']['completed']}
    changed = sorted(i for i in b.keys() & d.keys() if (b[i]['completion'], b[i]['met']) != (d[i]['completion'], d[i]['met']))
    return dict(decisions=len(rows), opportunity=len(competition), disagreement=len(mismatch),
                erased=len(mismatch & equal_actions), local_action_differences=len(rows)-len(equal_actions),
                erasure_fraction=len(mismatch & equal_actions)/len(mismatch) if mismatch else None,
                changed_requests=changed, unmatched_requests=sorted(b.keys() ^ d.keys()),
                request_denominator=record['request_count'],
                delta_anwg=aggregate_ablation(record)['delta_anwg'])


def diagnostic_protocol(record):
    """Explicit stage-by-stage checks; separate local and trajectory estimands."""
    out = dict(decisions=0, opportunity=0, disagreement=0, erased=0, local_action_differences=0)
    for event in record['base']['events']:
        out['decisions'] += 1
        if len(event['snapshot']['waiting_queue']) >= 2:
            out['opportunity'] += 1
        a = event['base_rank'][0] if event['base_rank'] else None
        b = event['donor_rank'][0] if event['donor_rank'] else None
        action_a = sorted(event['base_action']['admit'].get('0', []))
        action_b = sorted(event['donor_action']['admit'].get('0', []))
        if action_a != action_b:
            out['local_action_differences'] += 1
        if a != b:
            out['disagreement'] += 1
            if action_a == action_b:
                out['erased'] += 1
    out['erasure_fraction'] = out['erased']/out['disagreement'] if out['disagreement'] else None
    completions = {r['id']: r for r in record['donor']['completed']}
    changed, unmatched = [], []
    for base in record['base']['completed']:
        donor = completions.pop(base['id'], None)
        if donor is None:
            unmatched.append(base['id'])
        elif base['completion'] != donor['completion'] or base['met'] != donor['met']:
            changed.append(base['id'])
    out.update(changed_requests=sorted(changed), unmatched_requests=sorted(unmatched+list(completions)),
               request_denominator=record['request_count'],
               delta_anwg=record['donor']['metrics']['arrival_normalized_weighted_goodput']-record['base']['metrics']['arrival_normalized_weighted_goodput'])
    return out
