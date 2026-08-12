#!/usr/bin/env python3
"""Sample construction, trajectory counts, and Table 7 descriptives.

Reproduces (manuscript Sections 3, 5.3, Table 7, Figure 5):
  1,929 analytic loans; 1,873 resolved (78.6% fully repaid)
  701 never-delinquent (all repaid) / 771 delinquent-repaid / 401 charged off
  returners 791 (67.5%; repaid 84.6%) vs no-return 381 (repaid 26.8%)
  re-delinquency among returners: 496 (62.7%)
  Table 7: date disclosure 166 (52.4% vs 62.8%, -10.4pp);
           income documentation 386 (59.8% vs 62.5%, -2.6pp)

Run from the repository root:  python code/verify_descriptives.py
"""
import pandas as pd

d = pd.read_csv('data/analysis_v3_public.csv')
print('analytic loans:', len(d))

r = d[d['outcome'].isin(['repaid', 'charged_off'])].copy()
r['repaid'] = (r['outcome'] == 'repaid').astype(int)
r['dq'] = r['first_delinq_k'].notna()
print(f"resolved: {len(r)}  fully repaid: {100*r['repaid'].mean():.1f}%")
g0 = r[~r['dq']]; g1 = r[r['dq'] & (r['repaid'] == 1)]; g2 = r[r['dq'] & (r['repaid'] == 0)]
print(f"never delinquent: {len(g0)} (repaid {100*g0['repaid'].mean():.0f}%)  "
      f"delinquent-repaid: {len(g1)}  charged off: {len(g2)}")

dq = r[r['dq']]
ret = dq[dq['return_to_current_k'].notna()]
nor = dq[dq['return_to_current_k'].isna()]
red = ret['re_delinq_k'].notna().sum()
print(f"returners: {len(ret)} ({100*len(ret)/len(dq):.1f}%; repaid {100*ret['repaid'].mean():.1f}%)  "
      f"no return: {len(nor)} (repaid {100*nor['repaid'].mean():.1f}%)  "
      f"re-delinquency: {red} ({100*red/len(ret):.1f}%)")

print('\nTable 7 (delinquency initiation by disclosure, resolved+ongoing analytic sample):')
for label, col in [('Repayment-date disclosure', 'pay_sched_rx'), ('Income documentation', 'income_doc')]:
    w = d[d[col] == 1]; wo = d[d[col] == 0]
    iw = 100 * w['first_delinq_k'].notna().mean()
    iwo = 100 * wo['first_delinq_k'].notna().mean()
    print(f"  {label}: n={len(w)} ({1000*len(w)/len(d):.0f}/1,000) | "
          f"initiation {iw:.1f}% vs {iwo:.1f}% | gap {iw-iwo:+.1f}pp")

print('\nPlacebo funnel: payday extracted:', int(d['salday'].notna().sum()),
      '| of which no stated timing (P3v3<4):', int(((d['P3v3'] < 4) & d['salday'].notna()).sum()))
