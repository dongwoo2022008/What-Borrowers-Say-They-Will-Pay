# -*- coding: utf-8 -*-
"""Cash-flow placebo test (original code of the 2026-08-05 run).

Basis of the Table 4 note. Reproduction confirmed:
A 36.6/24.3 (+12.3pp) · B 36.5/22.8 (+13.7pp).

Design
  Group A (promisers): specific repayment timing stated (P3_v3 >= 4) with the
      day extracted -> 91 loans / 854 installments
  Group B (placebo)  : no repayment timing stated (P3_v3 < 4), payday
      disclosed in the text -> 36 loans / 326 installments
  Statistic : across-loan mean of each loan's "share of installments paid
      within +/-3 days of the reference day"
      (reference day = promised day for A / payday for B)
  Null      : reference days randomly reassigned across loans WITHIN each
      group, 1,000 draws (computed independently per group)
  * The two nulls differ (24.3 vs 22.8) because the marginal distributions of
    reference days differ across groups; these are group-specific nulls, not
    a shared null. The comparison of interest is the EXCESS over each group's
    own null, not the raw observed rates.

The byte-exact archived original with Korean comments is preserved in the
git history of this file (commit 2a3ace6). The raw plan texts are not
distributed here; the extracted payday is provided as the `salday` column of
data/analysis_v3_public.csv, and code/verify_placebo.py is the publicly
runnable version of this test.
"""
import re, numpy as np, pandas as pd

# Payday extraction pattern (deterministic; no LLM involvement)
SALARY_DAY = re.compile(
    r'(?:급여일|월급날|월급일|봉급날)[은이가]?\s*(?:매월|매달)?\s*(\d{1,2})\s*일'
    r'|(?:매월|매달)\s*(\d{1,2})\s*일(?:에)?\s*(?:수령|입금|받|나오|지급)')

def salary_day(text):
    m = SALARY_DAY.search(str(text))
    return int(m.group(1) or m.group(2)) if m else np.nan

def circ(a, b, period=30):
    """Circular distance on the monthly cycle."""
    x = np.abs(a - b)
    return np.minimum(x, period - x)

def concordance(panel, loans, daycol, window=3):
    m = panel.merge(loans[['loan_id', daycol]], on='loan_id')
    m = m[m.aday.notna()]
    stat = m.assign(hit=circ(m.aday, m[daycol]) <= window).groupby('loan_id').hit.mean().mean()
    return stat, m

def permutation_null(m, days, window=3, B=1000, seed=7):
    rng = np.random.default_rng(seed)
    ids, vals = days.index.values, days.values
    out = []
    for _ in range(B):
        fake = pd.Series(rng.permutation(vals), index=ids)
        fd = m.loan_id.map(fake)
        out.append(m.assign(hit=circ(m.aday, fd) <= window)
                     .groupby('loan_id').hit.mean().mean())
    return np.mean(out), np.percentile(out, 97.5)

if __name__ == '__main__':
    A = pd.read_csv('analysis_v3.csv')          # includes plan_text, P3_v3, day
    pan = pd.read_csv('panel_long.csv')
    pan = pan[pan.actual_date.notna()].copy()
    pan['aday'] = pd.to_datetime(pan.actual_date, errors='coerce').dt.day
    A['salday'] = A.plan_text.apply(salary_day)

    gA = A[(A.P3_v3 >= 4) & A.day.notna()]      # promisers
    gB = A[(A.P3_v3 <  4) & A.salday.notna()]   # placebo: no timing stated + payday disclosed
    for lab, g, col in [('A promisers', gA, 'day'), ('B payday-only', gB, 'salday')]:
        obs, m = concordance(pan, g, col)
        null, hi = permutation_null(m, g.set_index('loan_id')[col])
        print(f"{lab}: {m.loan_id.nunique()} loans/{len(m)} inst. | "
              f"observed {obs:.3f} | null {null:.3f} (97.5% {hi:.3f}) | excess {obs-null:+.3f}")
