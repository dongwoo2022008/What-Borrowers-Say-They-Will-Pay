#!/usr/bin/env python3
"""Cash-flow placebo (manuscript Section 5.1, Table 4 note) — reproduction.

Group A (date-stating): specific repayment timing stated AND a calendar day
extracted (day_v3) -> 91 loans / 854 paid installments.
Group B (placebo): NO specific repayment timing (P3v3 < 4) but a payday
disclosed in the plan text -> 36 loans / 326 paid installments.

The payday was extracted from the borrower-written plan text with a
deterministic rule-based pattern (no LLM involvement); because the raw texts
contain personal information and are excluded from this repository, the
extracted day is provided as the `salday` column of analysis_v3_public.csv.
The extraction pattern itself is documented in code/salary_day_pattern.py.

Nulls are GROUP-SPECIFIC permutation nulls: reference days are reassigned
across loans WITHIN each group (1,000 draws, seed 7). The two nulls differ
(24.3% vs 22.8%) because the marginal distributions of reference days differ;
the comparison of interest is each group's excess over its own null
(+12.3 vs +13.7 percentage points), not the raw alignment rates.

Run from the repository root:  python code/verify_placebo.py
"""
import numpy as np
import pandas as pd

d = pd.read_csv('data/analysis_v3_public.csv')
pan = pd.read_csv('data/panel_long.csv')
pan = pan[pan['actual_date'].notna()].copy()
pan['aday'] = pd.to_datetime(pan['actual_date'], errors='coerce').dt.day

def circ(a, b, period=30):
    x = np.abs(a - b)
    return np.minimum(x, period - x)

gA = d[(d['P3v3'] >= 4) & d['day_v3'].notna()]
gB = d[(d['P3v3'] < 4) & d['salday'].notna()]

for lab, g, col in [('A date-stating', gA, 'day_v3'), ('B payday-only placebo', gB, 'salday')]:
    daymap = dict(zip(g['loan_id'], g[col]))
    m = pan[pan['loan_id'].isin(g['loan_id'])].copy()
    m['d'] = circ(m['aday'], m['loan_id'].map(daymap))
    share = m.groupby('loan_id')['d'].apply(lambda s: (s <= 3).mean())
    obs = share.mean()
    rng = np.random.default_rng(7)
    ids = share.index.to_numpy()
    days = np.array([daymap[i] for i in ids], dtype=float)
    pdays = {lid: grp['aday'].to_numpy() for lid, grp in m.groupby('loan_id')}
    out = []
    for _ in range(1000):
        perm = rng.permutation(days)
        out.append(np.mean([ (circ(pdays[l], sd) <= 3).mean()
                             for l, sd in zip(ids, perm) ]))
    null = float(np.mean(out))
    print(f"{lab}: {m['loan_id'].nunique()} loans / {len(m)} installments | "
          f"observed {100*obs:.1f}% | group permutation null {100*null:.1f}% | "
          f"excess {100*(obs-null):+.1f}pp")
print("\nNote: reported values (36.6/24.3/+12.3 and 36.5/22.8/+13.7) come from the")
print("archived 2026-08-05 run; small third-digit differences are Monte Carlo noise.")
