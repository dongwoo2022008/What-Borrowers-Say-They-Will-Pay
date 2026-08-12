# -*- coding: utf-8 -*-
"""Deterministic rule-based payday extraction (no LLM involvement).

This is the exact pattern used to construct the `salday` column of
data/analysis_v3_public.csv from the borrower-written repayment-plan texts.
The raw texts contain personal and financial information and are therefore
not distributed with this repository; applying this pattern to the original
texts yields 66 extractions among 1,929 loans, of which 36 fall in the
no-stated-timing placebo group (P3v3 < 4).
"""
import re
import numpy as np

SALARY_DAY = re.compile(
    r'(?:급여일|월급날|월급일|봉급날)[은이가]?\s*(?:매월|매달)?\s*(\d{1,2})\s*일'
    r'|(?:매월|매달)\s*(\d{1,2})\s*일(?:에)?\s*(?:수령|입금|받|나오|지급)')

def salary_day(text):
    m = SALARY_DAY.search(str(text))
    return int(m.group(1) or m.group(2)) if m else np.nan
