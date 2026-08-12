#!/usr/bin/env python3
"""Figure G1 - installment-level delay-severity map, rebuilt from the panel in
grayscale to complete the paper's monochrome figure family.

The severity scale is ordinal (early / on time / 1-7 / 8-30 / 31+ / unpaid),
which is exactly what a sequential ramp encodes: lighter = milder. The colour
original used a blue-yellow-red palette whose blue (early) and light-blue
(on time) bands read identically in mono print.

Grey levels: early 245, on time 218, 1-7 days 175, 8-30 days 130,
31+ days 80, unpaid 25. Groups and within-group ordering reproduce the
original: never-delinquent repaid / delinquent repaid / delinquent charged
off, each sorted by mean delay.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd, numpy as np

NCOL = 400
GREY = {'early': 245, 'ontime': 218, 'late1_7': 175, 'late8_30': 130,
        'late31': 80, 'unpaid': 25}

d = pd.read_csv('data/analysis_v3_public.csv')
p = pd.read_csv('data/panel_long.csv')
r = d[d['outcome'].isin(['완납', '손실'])].copy()
r['repaid'] = (r['outcome'] == '완납').astype(int)
r['dq'] = r['first_delinq_k'].notna()

def cat(row):
    if row['unpaid'] == 1: return GREY['unpaid']
    if row['early'] == 1: return GREY['early']
    if row['ontime'] == 1: return GREY['ontime']
    dl = row['delay']
    if dl <= 7: return GREY['late1_7']
    if dl <= 30: return GREY['late8_30']
    return GREY['late31']

p = p[p['loan_id'].isin(r['loan_id'])].copy()
p['g'] = p.apply(cat, axis=1)
seq = {lid: grp.sort_values('k')['g'].to_numpy() for lid, grp in p.groupby('loan_id')}
mean_delay = p.groupby('loan_id')['delay'].mean()

g0 = r[~r['dq']].assign(md=lambda x: x['loan_id'].map(mean_delay)).sort_values('md')
g1 = r[r['dq'] & (r['repaid'] == 1)].assign(md=lambda x: x['loan_id'].map(mean_delay)).sort_values('md')
g2 = r[r['dq'] & (r['repaid'] == 0)].assign(md=lambda x: x['loan_id'].map(mean_delay)).sort_values('md')
GAP = 9

rows = []
def add(df):
    for lid in df['loan_id']:
        s = seq.get(lid)
        if s is None or len(s) == 0:
            rows.append(np.full(NCOL, 255.0)); continue
        idx = np.minimum((np.arange(NCOL) / NCOL * len(s)).astype(int), len(s) - 1)
        rows.append(s[idx].astype(float))

add(g0); rows += [np.full(NCOL, np.nan)] * GAP
add(g1); rows += [np.full(NCOL, np.nan)] * GAP
add(g2)
M = np.vstack(rows)

fig, ax = plt.subplots(figsize=(10.6, 7.8), dpi=150)
cmap = plt.get_cmap('gray').copy(); cmap.set_bad('white')
ax.imshow(np.ma.masked_invalid(M), cmap=cmap, vmin=0, vmax=255,
          aspect='auto', interpolation='nearest', extent=[0, 100, len(M), 0])
ax.set_xlabel('Progress through loan term (%)', fontsize=12)
ax.set_ylabel('Loans (1,873; sorted by mean delay within group)', fontsize=11.5)
ax.tick_params(labelsize=10.5)
for s in ax.spines.values():
    s.set_linewidth(0.9); s.set_color('#444444')

mids = [len(g0)/2, len(g0)+GAP+len(g1)/2, len(g0)+len(g1)+2*GAP+len(g2)/2]
labels = [f'No delinquency,\nfully repaid ({len(g0)})',
          f'Delinquent,\nfully repaid ({len(g1)})',
          f'Delinquent,\ncharged off ({len(g2)})']
for y, lab in zip(mids, labels):
    ax.text(101.5, y, lab, fontsize=10, va='center', ha='left', color='#222222')

handles = [mpatches.Patch(facecolor=str(v/255), edgecolor='#555555', label=l)
           for l, v in [('Early', GREY['early']), ('On time', GREY['ontime']),
                        ('1–7 days late', GREY['late1_7']), ('8–30 days late', GREY['late8_30']),
                        ('31+ days late', GREY['late31']), ('Unpaid', GREY['unpaid'])]]
leg = ax.legend(handles=handles, loc='upper right', fontsize=9.5, ncol=2,
                framealpha=1, edgecolor='#888888')
leg.get_frame().set_linewidth(0.8)

OUT = 'figures/FigureG1_severity.png'
fig.savefig(OUT, dpi=600, bbox_inches='tight', pad_inches=0.10, facecolor='white')
from PIL import Image
im = Image.open(OUT)
print('groups:', len(g0), len(g1), len(g2), '| total', len(g0)+len(g1)+len(g2))
print('written', im.size, round(im.size[0]/im.size[1], 4))
