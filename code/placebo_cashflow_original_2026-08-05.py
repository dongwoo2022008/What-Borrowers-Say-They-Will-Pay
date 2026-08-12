# -*- coding: utf-8 -*-
"""
현금흐름 플라시보 검정 (2026-08-05 실행분 원본 코드)
Table 4 주석 근거. 재현 확인: A 36.6/24.3(+12.3pp) · B 36.5/22.8(+13.7pp)
설계
  A군(약속자)       : 상환 시점을 구체적으로 약속(P3_v3 ≥ 4)하고 그 날짜(day)가 추출된 대출 → 91대출/854회차
  B군(플라시보)     : 상환 시점을 약속하지 않았고(P3_v3 < 4) 텍스트에 급여일만 밝힌 대출 → 36대출/326회차
  통계량            : 대출별 "기준일 ±3일 이내 납부 회차 비율"의 대출 간 평균
                      (A군 기준일 = 약속일 / B군 기준일 = 급여일)
  귀무               : 각 군 내부에서 기준일을 대출 간 무작위 재배정, 1,000회 (군별로 독립 산출)
  ★ 두 군의 귀무값이 다른 이유(24.3 vs 22.8)는 각 군의 기준일 주변분포가 다르기 때문이며,
    공유 귀무가 아니라 군별 귀무이다. 비교 대상은 관측값이 아니라 '귀무 대비 초과분'이다.
"""
import re, numpy as np, pandas as pd
# 급여일 추출 정규식 (LLM 미사용, 결정론적)
SALARY_DAY = re.compile(
    r'(?:급여일|월급날|월급일|봉급날)[은이가]?\s*(?:매월|매달)?\s*(\d{1,2})\s*일'
    r'|(?:매월|매달)\s*(\d{1,2})\s*일(?:에)?\s*(?:수령|입금|받|나오|지급)')
def salary_day(text):
    m = SALARY_DAY.search(str(text))
    return int(m.group(1) or m.group(2)) if m else np.nan
def circ(a, b, period=30):
    """월 주기 원형 거리"""
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
    A = pd.read_csv('analysis_v3.csv')          # plan_text, P3_v3, day 포함
    pan = pd.read_csv('panel_long.csv')
    pan = pan[pan.actual_date.notna()].copy()
    pan['aday'] = pd.to_datetime(pan.actual_date, errors='coerce').dt.day
    A['salday'] = A.plan_text.apply(salary_day)
    gA = A[(A.P3_v3 >= 4) & A.day.notna()]      # 약속자
    gB = A[(A.P3_v3 <  4) & A.salday.notna()]   # 플라시보: 약속 없음 + 급여일 공개
    for lab, g, col in [('A 약속자', gA, 'day'), ('B 급여일만', gB, 'salday')]:
        obs, m = concordance(pan, g, col)
        null, hi = permutation_null(m, g.set_index('loan_id')[col])
        print(f"{lab}: {m.loan_id.nunique()}대출/{len(m)}회차 · "
              f"관측 {obs:.3f} · 귀무 {null:.3f}(97.5% {hi:.3f}) · 초과 {obs-null:+.3f}")
