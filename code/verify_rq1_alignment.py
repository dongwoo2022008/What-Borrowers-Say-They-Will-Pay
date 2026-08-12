#!/usr/bin/env python3
"""RQ1 confirmatory test — full reproduction from the repository data.

Reproduces (manuscript Section 5.1, Table 4, Appendix C):
  91 loans / 854 paid installments
  loan-level mean share within +/-3 days of the stated day = 36.6%
  permutation null mean = 24.3% (2,000 reassignments of stated days, seed 42)
  one-sided p = (b + 1) / (B + 1) = 1/2001 = .0005  (Phipson & Smyth, 2010)
  window robustness vs the uniform 30-day benchmark (Appendix C, Table C1)

Run from the repository root:  python code/verify_rq1_alignment.py
"""
import numpy as np
import pandas as pd

d = pd.read_csv('data/analysis_v3_public.csv')
p = pd.read_csv('data/panel_long.csv')

p = p[p['actual_date'].notna()].copy()
p['aday'] = pd.to_datetime(p['actual_date'], errors='coerce').dt.day

def circ(a, b, period=30):
    x = np.abs(a - b)
    return np.minimum(x, period - x)

g = d[d['day_v3'].notna()]
daymap = dict(zip(g['loan_id'], g['day_v3']))
m = p[p['loan_id'].isin(g['loan_id'])].copy()
m['d'] = circ(m['aday'], m['loan_id'].map(daymap))

loan_share = m.groupby('loan_id')['d'].apply(lambda s: (s <= 3).mean())
obs = loan_share.mean()
print(f"loans: {m['loan_id'].nunique()}  paid installments: {len(m)}")
print(f"observed loan-level mean share within +/-3 days: {100*obs:.1f}%")

rng = np.random.default_rng(42)
ids = loan_share.index.to_numpy()
days = np.array([daymap[i] for i in ids], dtype=float)
pdays = {lid: grp['aday'].to_numpy() for lid, grp in m.groupby('loan_id')}
B = 2000
nulls = np.empty(B)
for b in range(B):
    perm = rng.permutation(days)
    nulls[b] = np.mean([ (circ(pdays[l], sd) <= 3).mean()
                         for l, sd in zip(ids, perm) ])
exceed = int((nulls >= obs).sum())
print(f"permutation null mean: {100*nulls.mean():.1f}%  95% range [{100*np.percentile(nulls,2.5):.1f}, {100*np.percentile(nulls,97.5):.1f}]")
print(f"p = ({exceed}+1)/({B}+1) = {(exceed+1)/(B+1):.4f}")

print("\nWindow robustness (observed vs uniform (2k+1)/30):")
for k in (1, 3, 5, 7):
    s = m.groupby('loan_id')['d'].apply(lambda x: (x <= k).mean()).mean()
    print(f"  +/-{k} day(s): {100*s:.1f}% vs {100*(2*k+1)/30:.1f}%")
