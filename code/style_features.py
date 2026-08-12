# -*- coding: utf-8 -*-
"""Writing-style variable construction: the S2/S3 columns (original rules, 2026-08-05 run).

Reproduces the S2 and S3 columns of the analysis dataset for all 1,929 loans
to floating-point precision (< 1e-14).

Input : plan_text — the master file's descriptiveRepaymentPlanBody after
        whitespace normalization (re.sub(r'\s+', ' ', x).strip())
Output: S2 (informal orthographic marker rate, per 100 characters)
        S3 (positive-emotion vocabulary rate, per 1,000 characters)

The byte-exact archived original with Korean comments is preserved in the
git history of this file (commit 17ae97d). The raw plan texts are not
distributed in this repository (personal information), so this script cannot
be re-run publicly; it is the authoritative specification behind the S2/S3
columns of data/analysis_v3_public.csv. Reconstruction check (2026-08-12):
applying these rules to the original texts reproduces the distributed S2/S3
columns exactly (max abs. error 4.4e-16 / 7.1e-15); descriptives match
Appendix D (S2 mean .1909, 74.3% zeros; S3 mean 2.6440, 57.8% zeros;
r(S2,S3) = .043). Known limitations disclosed in Appendix D: informal-marker
matches are dominated by punctuation runs (ellipses), and the stem '웃'
produces partial-string false positives (48/1,724 = 2.8% of matches).
"""
import re, pandas as pd

# -- S2: informal-orthography pattern (author-defined; no spell-checker used) --
#    Repeated-jamo affective markers + excessive punctuation.
#    Spelling and spacing errors are NOT counted.
INFORMAL = r'(ㅠ+|ㅜ+|ㅎㅎ+|ㅋ+|\^\^|~{2,}|\.{3,}|!{2,}|\?{2,})'

# -- S3: positive-vocabulary list (author-defined, 20 stems; no existing sentiment lexicon) --
POSITIVE = ['감사','고맙','희망','행복','기쁘','좋은','좋습니다','믿음','믿어','사랑',
            '축복','웃','따뜻','소중','응원','보답','은혜','기회','새출발','꿈']

def normalize(x):
    """Master-file raw text -> analysis text. This normalization is why the
    denominator is 1-3% smaller than plan_len for some texts."""
    return re.sub(r'\s+', ' ', str(x)).strip()

def style_features(text_series):
    t = text_series.fillna('')
    denom = t.str.len().clip(lower=30)          # character count incl. spaces, floored at 30
    n_informal = t.apply(lambda s: len(re.findall(INFORMAL, s)))          # non-overlapping match count
    n_positive = t.apply(lambda s: sum(s.count(w) for w in POSITIVE))     # sum of substring frequencies
    return pd.DataFrame({'S2': n_informal/denom*100,      # x100
                         'S3': n_positive/denom*1000})    # x1000

if __name__ == '__main__':
    df = pd.read_csv('analysis_v3.csv')
    print(style_features(df.plan_text).describe())
