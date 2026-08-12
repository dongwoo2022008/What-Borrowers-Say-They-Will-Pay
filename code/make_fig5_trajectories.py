#!/usr/bin/env python3
"""Figure 5 - repayment trajectories of all resolved loans, rebuilt from data
in grayscale.

Two reasons for the rebuild.

(1) Grayscale. Measured on the previous PNG, the three panel-A categories mapped
to grey 198 (current), 174 (first delinquency) and 79 (after re-delinquency).
The 24-level gap between the first two disappears at print size, where each loan
is one pixel row — so the colour figure also failed on a mono printer. The ramp
here is 232 / 150 / 60, gaps of 82 and 90, and it is ordinal: lighter is better.

(v12.62) Panel B: outcome boxes widened to 0.36 so the repaid/loss line fits;
all branching arrows orthogonal (right-edge -> vertical bus -> left-edge).

(2) Panel B text clipping. The old panel put the final-outcome callouts in
separate boxes overlapping the state boxes, which clipped "Return to current".
The outcome shares are now a third line inside the box they belong to.

Every count is recomputed here rather than carried over. Verified against the
manuscript: 1,873 resolved; 701 (37%) never delinquent, all fully repaid;
1,172 (63%) reach a first delinquency; of those 791 (67.5%) return to current
(repaid 84.6% / loss 15.4%) and 381 (32.5%) do not (repaid 26.8% / loss 73.2%);
496 (62.7%) of returners re-enter delinquency.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow
import matplotlib.patches as mpatches
import pandas as pd, numpy as np

CUR, DEL, RED = 232, 150, 60          # grey levels, light -> dark = better -> worse
NCOL = 400

d = pd.read_csv('data/analysis_v3_public.csv')
r = d[d['outcome'].isin(['repaid', 'charged_off'])].copy()
r['repaid'] = (r['outcome'] == 'repaid').astype(int)
r['dq'] = r['first_delinq_k'].notna()

N = len(r)
g0 = r[~r['dq']]                                   # never delinquent
g1 = r[r['dq'] & (r['repaid'] == 1)].sort_values('first_delinq_frac')
g2 = r[r['dq'] & (r['repaid'] == 0)].sort_values('first_delinq_frac')
GAP = 9

rows = []
def add(df):
    for t in df.itertuples():
        row = np.full(NCOL, CUR, dtype=float)
        n = max(int(t.n_inst), 1)
        def pos(k):
            return int(np.clip((k - 1) / n, 0, 1) * NCOL)
        if not np.isnan(t.first_delinq_k):
            a = pos(t.first_delinq_k)
            b = pos(t.return_to_current_k) if not np.isnan(t.return_to_current_k) else NCOL
            row[a:b] = DEL
            if not np.isnan(t.re_delinq_k):
                row[pos(t.re_delinq_k):] = RED
        rows.append(row)

add(g0); rows += [np.full(NCOL, np.nan)] * GAP
add(g1); rows += [np.full(NCOL, np.nan)] * GAP
add(g2)
M = np.vstack(rows)

fig = plt.figure(figsize=(13.6, 7.0), dpi=150)
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 0.92], wspace=0.30,
                      left=0.055, right=0.985, top=0.93, bottom=0.09)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1])

cmap = plt.get_cmap('gray').copy(); cmap.set_bad('white')
axA.imshow(np.ma.masked_invalid(M), cmap=cmap, vmin=0, vmax=255,
           aspect='auto', interpolation='nearest', extent=[0, 100, len(M), 0])
axA.set_xlabel('Progress through loan term (%)', fontsize=11)
axA.set_ylabel(f'Loans ({N:,}; one row each, sorted by first-delinquency timing)', fontsize=10.5)
axA.set_yticks([0, 250, 500, 750, 1000, 1250, 1500, 1750])
axA.tick_params(labelsize=10)
axA.set_title('A. Repayment trajectories of all resolved loans', fontsize=12,
              fontweight='bold', loc='left', pad=8)
for s in axA.spines.values():
    s.set_linewidth(0.9); s.set_color('#444444')

mids = [len(g0) / 2, len(g0) + GAP + len(g1) / 2, len(g0) + len(g1) + 2 * GAP + len(g2) / 2]
labels = [f'No delinquency,\nfully repaid\n({len(g0)})',
          f'Delinquent,\nfully repaid\n({len(g1)})',
          f'Delinquent,\ncharged off\n({len(g2)})']
for y, lab in zip(mids, labels):
    axA.text(102.5, y, lab, fontsize=9.5, va='center', ha='left', color='#222222')

handles = [mpatches.Patch(facecolor=str(v / 255), edgecolor='#555555', label=l)
           for v, l in [(CUR, 'Current (incl. after return)'),
                        (DEL, 'First delinquency spell'),
                        (RED, 'After re-delinquency')]]
axA.legend(handles=handles, loc='upper right', fontsize=9, framealpha=1,
           edgecolor='#888888').get_frame().set_linewidth(0.8)

# ---------------- Panel B ----------------
axB.set_xlim(0, 1); axB.set_ylim(0, 1); axB.axis('off')
axB.set_title('B. Trajectory branching and final outcomes', fontsize=12,
              fontweight='bold', loc='left', pad=8)

BOX = {}
def box(key, cx, cy, w, h, lines, fill='#f2f2f2'):
    axB.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, lw=1.3,
                            edgecolor='#3a3a3a', facecolor=fill, zorder=2))
    axB.text(cx, cy, '\n'.join(lines), ha='center', va='center', fontsize=9.6,
             color='#111111', linespacing=1.5, zorder=3)
    BOX[key] = (cx, cy, w, h)

def seg(x0, y0, x1, y1):
    axB.plot([x0, x1], [y0, y1], color='#555555', lw=1.4,
             solid_capstyle='round', zorder=1)

def harrow(x0, y, x1):
    axB.annotate('', xy=(x1, y), xytext=(x0, y),
                 arrowprops=dict(arrowstyle='-|>', color='#555555', lw=1.4,
                                 shrinkA=0, shrinkB=1), zorder=1)

def split_right(parent, children, busx):
    """Orthogonal fan-out: parent right edge -> vertical bus -> child left edges."""
    (px, py, pw, ph) = BOX[parent]
    seg(px + pw / 2, py, busx, py)
    ys = [BOX[c][1] for c in children]
    seg(busx, min(ys + [py]), busx, max(ys + [py]))
    for c in children:
        (cx, cy, cw, ch) = BOX[c]
        harrow(busx, cy, cx - cw / 2)

nd, fd = len(g0), len(g1) + len(g2)
ret = r[r['dq'] & r['return_to_current_k'].notna()]
nor = r[r['dq'] & r['return_to_current_k'].isna()]
red = ret['re_delinq_k'].notna().sum()

box('all',  0.12, 0.50, 0.20, 0.14, ['All resolved', f'{N:,}'])
box('nd',   0.44, 0.86, 0.24, 0.14, ['No delinquency', f'{nd} ({100*nd/N:.0f}%)'])
box('fd',   0.44, 0.26, 0.24, 0.14, ['First delinquency', f'{fd:,} ({100*fd/N:.0f}%)'])
box('rep',  0.80, 0.86, 0.24, 0.14, ['Fully repaid', '100%'], fill='#e2e2e2')
box('red',  0.80, 0.60, 0.24, 0.13, ['Re-delinquency', f'{red} ({100*red/len(ret):.1f}%)'])
box('ret',  0.80, 0.36, 0.36, 0.15,
    ['Return to current', f'{len(ret)} ({100*len(ret)/fd:.1f}%)',
     f'repaid {100*ret["repaid"].mean():.1f}% · loss {100*(1-ret["repaid"].mean()):.1f}%'])
box('nor',  0.80, 0.11, 0.36, 0.15,
    ['No return', f'{len(nor)} ({100*len(nor)/fd:.1f}%)',
     f'repaid {100*nor["repaid"].mean():.1f}% · loss {100*(1-nor["repaid"].mean()):.1f}%'])

split_right('all', ['nd', 'fd'], 0.27)   # all -> {no delinquency, first delinquency}
harrow(BOX['nd'][0] + BOX['nd'][2] / 2, 0.86, BOX['rep'][0] - BOX['rep'][2] / 2)
split_right('fd', ['ret', 'nor'], 0.59)  # first delinquency -> {return, no return}
axB.annotate('', xy=(0.80, 0.60 - 0.065), xytext=(0.80, 0.36 + 0.075),
             arrowprops=dict(arrowstyle='-|>', color='#555555', lw=1.4,
                             shrinkA=1, shrinkB=1), zorder=1)

# text-overflow assertion for panel B
fig.canvas.draw()
rend = fig.canvas.get_renderer()
import matplotlib.transforms as mtrans
for t in axB.texts:
    bb = t.get_window_extent(renderer=rend).transformed(axB.transData.inverted())
    x, y = t.get_position()
    hit = [k for k, (cx, cy, w, h) in BOX.items() if abs(cx - x) < 1e-6 and abs(cy - y) < 1e-6]
    if hit:
        cx, cy, w, h = BOX[hit[0]]
        ox = max(0, (bb.width - w) / 2); oy = max(0, (bb.height - h) / 2)
        print(f'box {hit[0]}: text {bb.width:.3f}x{bb.height:.3f} vs box {w}x{h}',
              'OVERFLOW' if (ox > 0 or oy > 0) else 'ok')

OUT = 'figures/Figure_5.png'
fig.savefig(OUT, dpi=600, facecolor='white', bbox_inches='tight', pad_inches=0.10)
from PIL import Image
im = Image.open(OUT)
print(f'resolved {N} | never delinquent {nd} | first delinquency {fd} | '
      f'return {len(ret)} | no return {len(nor)} | re-delinquency {red}')
print('written', im.size, round(im.size[0] / im.size[1], 4))
