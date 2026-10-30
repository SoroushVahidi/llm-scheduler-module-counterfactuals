"""MIT project statistical primitives, adapted for the portable outcome release.
Origins: Stage 2A / Stage 2A2; no historical simulation implementation included.
Changed: removed raw/private inputs and command-line side effects. Mathematics unchanged.
"""
import collections, hashlib, math, random, statistics
import numpy as np
B=10000
SEED=20261029
def stable_seed(label):
    return int.from_bytes(hashlib.sha256(f'{SEED}|{label}'.encode()).digest()[:8], 'big')

def interval(values):
    s = sorted(v for v in values if v is not None)
    def q(p):
        x = (len(s)-1)*p; i = int(x)
        return s[i] + (s[min(i+1,len(s)-1)]-s[i])*(x-i)
    return [q(.025), q(.975)] if s else None

def estimands(cells):
    positive = [c for c in cells if c['denominator'] > 0]
    n = sum(c['denominator'] for c in positive)
    return (sum(c['numerator'] for c in positive)/n if n else None,
            statistics.mean(c['numerator']/c['denominator'] for c in positive) if positive else None)

def draw_windows(groups, rng):
    # Each group contains complete windows, never individual pair-window cells.
    return [w for key in sorted(groups) for w in rng.choices(groups[key], k=len(groups[key]))]

def erasure_bootstrap(windows, stratified=True, b=B, hierarchical=False):
    groups = collections.defaultdict(list)
    for w in windows: groups[w['source'] if stratified else 'all'].append(w)
    rng = random.Random(stable_seed('erasure-hierarchical' if hierarchical else 'erasure-stratified' if stratified else 'erasure-unstratified'))
    draws = []
    for _ in range(b):
        if hierarchical:
            sampled = [w for source in rng.choices(sorted(groups), k=len(groups)) for w in rng.choices(groups[source], k=len(groups[source]))]
        else:
            sampled = draw_windows(groups,rng)
        draws.append(estimands([c for w in sampled for c in w['cells']]))
    return {'pooled_event_weighted_ci95':interval([x[0] for x in draws]),
            'equal_positive_cell_ci95':interval([x[1] for x in draws]),
            'undefined_draws':sum(x[0] is None for x in draws), 'B':b}

def kv_summary(rs,label):
    # Average over a fixed design inside each shared seed-stream block.
    blocks=collections.defaultdict(list)
    for r in rs: blocks[r['heldout_stream_index']].append(r['gain_v1_corrected'])
    assert len(blocks)==10 and len({len(v) for v in blocks.values()})==1
    vals=[statistics.mean(blocks[k]) for k in sorted(blocks)]
    rng=random.Random(stable_seed('kv|'+label))
    boots=[statistics.mean(rng.choices(vals,k=len(vals))) for _ in range(B)]
    return dict(mean=statistics.mean(vals),ci95=interval(boots),n_seed_streams=len(vals),n_observations=len(rs),n_pairs=len({r['intervention_id'] for r in rs}),seed_stream_means=vals)

def seed(label):return int.from_bytes(hashlib.sha256(('20261029|stage2a2|'+label).encode()).digest()[:8],'big')

def classify(effects):
    if not all(math.isfinite(v) for v in effects):raise ValueError('missing/nonfinite effect')
    pos=any(v>1e-12 for v in effects);neg=any(v< -1e-12 for v in effects);zero=any(abs(v)<=1e-12 for v in effects)
    return 'SIGN_SENSITIVE' if pos and neg else 'DETECTION_SENSITIVE' if (pos or neg) and zero else 'NON_NULL_SAME_DIRECTION' if pos or neg else 'ALL_NEAR_NULL'

def corr(x,y):
    x=np.asarray(x,float);y=np.asarray(y,float)
    if len(x)<3 or np.ptp(x)==0 or np.ptp(y)==0:return None
    return float(np.corrcoef(x,y)[0,1])

def calculate(rows,center=False,which='priority'):
    if which=='priority':x=[r['candidate'] for r in rows];y=[r['priority_divergence'] for r in rows]
    elif which=='prefill_pressure':x=[r['prefill_pressure'] for r in rows];y=[r['prefill_divergence'] for r in rows]
    else:x=[r['prefill_divergence'] for r in rows];y=[r['prefill_request_change'] for r in rows]
    if center:
        groups=collections.defaultdict(list)
        for i,r in enumerate(rows):groups[r['source']].append(i)
        for indices in groups.values():
            mx=sum(x[i] for i in indices)/len(indices);my=sum(y[i] for i in indices)/len(indices)
            for i in indices:x[i]-=mx;y[i]-=my
    return corr(x,y)

def draw_blocks(groups,rng):
    return [block for source in sorted(groups) for block in rng.choices(groups[source],k=len(groups[source]))]
