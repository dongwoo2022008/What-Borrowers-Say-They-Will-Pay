#!/usr/bin/env python3
"""Figure 4 - distribution of circular distance between actual payment day and
stated repayment day, rebuilt from the raw panel.

Reason for the rebuild: the previous PNG carried a baked-in title reading
"Figure 1. Alignment between stated repayment dates and actual payment timing",
while the manuscript caption below it reads "Figure 4". It also carried the old
"p < .0005" and described 36.6% as an installment share. In-image titles are
dropped here so the caption is the single source of numbering.

Palette is unchanged from the previous version (the paper's other colour
figures are Figure 5 and Figure G1); only the text is corrected.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd, numpy as np

D = 'data/analysis_v3_public.csv'
PN = 'data/panel_long.csv'
OUT = 'figures/Figure_4.png'

d = pd.read_csv(D)
p = pd.read_csv(PN)
day = dict(zip(d['loan_id'], d['day_v3']))
ids = d.loc[d['day_v3'].notna(), 'loan_id']
q = p[p['loan_id'].isin(ids) & p['actual_date'].notna()].copy()
q['aday'] = pd.to_datetime(q['actual_date']).dt.day
x = np.abs(q['aday'].to_numpy() - q['loan_id'].map(day).to_numpy())
dist = np.minimum(x, 30 - x)
n_inst, n_loan = len(q), q['loan_id'].nunique()

share = pd.Series(dist).value_counts(normalize=True).sort_index() * 100
share = share.reindex(range(16), fill_value=0.0)

# loan-level mean share within +/-3, the confirmatory statistic
loan_share = q.assign(d=dist).groupby('loan_id')['d'].apply(lambda s: (s <= 3).mean())
main = 100 * loan_share.mean()

# uniform 30-day per-distance benchmark: 1/30 at d = 0 and d = 15, 2/30 otherwise
unif = np.array([100 / 30 if k in (0, 15) else 200 / 30 for k in range(16)])

DARK, LIGHT, RULE = '#4d4d4d', '#c9c9c9', '#1a1a1a'
fig, ax = plt.subplots(figsize=(9.6, 5.2), dpi=150)
ax.bar(range(16), share.to_numpy(),
       color=[DARK if k <= 3 else LIGHT for k in range(16)], width=0.86, zorder=2)
ax.step(np.arange(-0.5, 16.0), np.append(unif, unif[-1]), where='post',
        color=RULE, lw=2.0, ls=(0, (5, 3)), zorder=3)

ax.set_xlabel('Circular distance between actual payment day and stated repayment day (days)',
              fontsize=11.5)
ax.set_ylabel('Share of installments (%)', fontsize=11.5)
ax.set_xticks(range(16)); ax.set_xlim(-0.7, 15.7)
ax.tick_params(labelsize=10.5)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.yaxis.grid(True, color='#e6e6e6', zorder=0); ax.set_axisbelow(True)

ax.annotate(f'Within ±3 days of the stated day:\nloan-level mean share {main:.1f}% vs. 24.3%\nunder the permutation null (p = .0005)',
            xy=(2.55, share.iloc[2] + 2.2), xytext=(4.3, 11.4), fontsize=11,
            color='#222222', va='center',
            arrowprops=dict(arrowstyle='-', color=RULE, lw=1.2))
ax.text(9.0, unif[9] + 0.55, 'Uniform-calendar benchmark', fontsize=11, color='#7a8590')

fig.savefig(OUT, dpi=1000, bbox_inches='tight', pad_inches=0.10, facecolor='white')
from PIL import Image
im = Image.open(OUT)
print(f'{n_loan} loans, {n_inst} paid installments | loan-level mean within +/-3 = {main:.2f}%')
print('pooled shares d=0..3:', [round(v, 1) for v in share.iloc[:4]])
print('written', im.size, round(im.size[0] / im.size[1], 4))
