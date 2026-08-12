# -*- coding: utf-8 -*-
"""Writing-style proxy construction (manuscript Section 3.4.1, Appendix D).

Documents the exact rules behind the two style columns distributed in
data/analysis_v3_public.csv:
  S2 = rate of informal orthographic markers (matches / denominator * 100)
  S3 = rate of positive-emotion vocabulary   (matches / denominator * 1000)

Input is the borrower-written repayment-plan field only (the loan-purpose
field is not used). Cleaning: whitespace runs collapsed to single spaces,
then stripped. Denominator: character count including spaces, floored at 30.

The raw plan texts contain personal information and are not distributed in
this repository, so this script cannot be re-run publicly end-to-end; it is
included as the authoritative specification. Reconstruction from the
documented rules reproduces the distributed S2/S3 columns for all 1,929
loans to floating-point precision (max abs. error 4.4e-16 / 7.1e-15), with
the descriptive statistics reported in Appendix D: S2 mean .1909 (74.3%
zeros), S3 mean 2.6440 (57.8% zeros), r(S2, S3) = .043.

Known limitations (disclosed in Appendix D): about three quarters of the
informal-marker matches are ellipses/punctuation runs rather than
orthographic slang, so S2 is best read as informal punctuation; the
positive-vocabulary stem '웃' produces partial-string false positives (e.g.,
in 워크아웃/이웃) in 48 of 1,724 total matches (2.8%). The two measures are
explicit proxies for writing style, not psychological states.
"""
import re
import numpy as np

INFORMAL = re.compile(r'ㅠ+|ㅜ+|ㅎㅎ+|ㅋ+|\^\^|~{2,}|\.{3,}|!{2,}|\?{2,}')

POSITIVE_STEMS = ['감사', '고맙', '희망', '행복', '기쁘', '좋은', '좋습니다', '믿음', '믿어',
                  '사랑', '축복', '웃', '따뜻', '소중', '응원', '보답', '은혜', '기회', '새출발', '꿈']
POSITIVE = re.compile('|'.join(POSITIVE_STEMS))


def clean(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def style_features(text):
    """Return (informal_marker_rate, positive_vocab_rate) for one plan text."""
    t = clean(text)
    denom = max(len(t), 30)
    return (len(INFORMAL.findall(t)) / denom * 100,
            len(POSITIVE.findall(t)) / denom * 1000)
