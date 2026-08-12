#!/usr/bin/env python3
"""Validation-agreement reproduction (manuscript Section 3.5, Table 3, App. E).

Reproduces from the label files in validation/ (no raw texts required) the
LLM run-to-run stability check: the 120 Phase B cases were re-annotated in
fresh contexts (2026-08) and compared with the original full-corpus
annotation (llm_key.csv). Expected: P2 linear weighted kappa ~= .935;
binary timing kappa ~= .750; binary agreement ~= 93%.

The Phase B coder<->coder and LLM<->adjudicated figures in Table 3
(wk = .737 [.65, .82], wk = .777 [.694, .851], k = .559, k = .482) are
computed from the archived adjudication records; the files distributed here
support the stability check and the case-to-loan mapping audit.

Run from the repository root:  python code/verify_validation_agreement.py
"""
import numpy as np
import pandas as pd

def kappa(a, b, weights=None):
    a = list(a); b = list(b)
    cats = sorted(set(a) | set(b))
    idx = {c: i for i, c in enumerate(cats)}
    O = np.zeros((len(cats), len(cats)))
    for x, y in zip(a, b):
        O[idx[x], idx[y]] += 1
    O /= len(a)
    E = np.outer(O.sum(1), O.sum(0))
    if weights == 'linear' and len(cats) > 1:
        k = len(cats)
        W = 1 - np.abs(np.subtract.outer(np.arange(k), np.arange(k))) / (k - 1)
    else:
        W = np.eye(len(cats))
    po = (W * O).sum(); pe = (W * E).sum()
    return (po - pe) / (1 - pe)

key = pd.read_csv('validation/llm_key.csv')          # original full-corpus annotation
rerun = pd.read_csv('validation/llm_rerun_2026-08.csv')  # case, P2, P3 (fresh-context re-annotation)
pbmap = pd.read_csv('validation/pb_map_final.csv')   # case -> loan_id

m = (rerun.rename(columns={'P2': 'P2_rerun', 'P3': 'P3_rerun'})
          .merge(pbmap, on='case')
          .merge(key[['loan_id', 'P2', 'P3_v3']], on='loan_id'))
print('matched cases:', len(m))
print(f"P2 run-to-run linear weighted kappa: {kappa(m['P2_rerun'], m['P2'], 'linear'):.3f}")
b1 = (m['P3_rerun'] >= 4).astype(int)
b2 = (m['P3_v3'] >= 4).astype(int)
print(f"binary timing run-to-run kappa: {kappa(b1, b2):.3f}")
print(f"binary timing agreement: {100*(b1 == b2).mean():.1f}%")
