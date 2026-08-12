# -*- coding: utf-8 -*-
"""
S2·S3 문체 변수 산출 스크립트 (원본 규칙, 2026-08-05 실행분)
analysis_v3.csv의 S2·S3 열을 전수 1,929건에서 부동소수점 오차(<1e-14) 내로 재현함.

입력 : plan_text — 마스터 파일 descriptiveRepaymentPlanBody 를
       공백 정규화한 텍스트  (re.sub(r'\s+',' ', x).strip())
출력 : S2 (비표준 표기 비율, per 100자) · S3 (긍정 어휘 비율, per 1000자)
"""
import re, pandas as pd

# ── S2: 비표준 표기 패턴 (자체 정의. 맞춤법 검사기 미사용) ──
#   자모 반복형 정서 표기 + 과잉 문장부호. 맞춤법·띄어쓰기 오류는 세지 않는다.
INFORMAL = r'(ㅠ+|ㅜ+|ㅎㅎ+|ㅋ+|\^\^|~{2,}|\.{3,}|!{2,}|\?{2,})'

# ── S3: 긍정 어휘 목록 (자체 정의 20어. 기존 감성사전 미사용) ──
POSITIVE = ['감사','고맙','희망','행복','기쁘','좋은','좋습니다','믿음','믿어','사랑',
            '축복','웃','따뜻','소중','응원','보답','은혜','기회','새출발','꿈']

def normalize(x):
    """마스터 원문 → 분석용 텍스트. 이 정규화 때문에 분모가 plan_len보다 1~3% 작다."""
    return re.sub(r'\s+', ' ', str(x)).strip()

def style_features(text_series):
    t = text_series.fillna('')
    denom = t.str.len().clip(lower=30)          # 글자 수(공백 포함), 하한 30
    n_informal = t.apply(lambda s: len(re.findall(INFORMAL, s)))          # 중복 없는 매치 수
    n_positive = t.apply(lambda s: sum(s.count(w) for w in POSITIVE))     # 부분문자열 빈도 합
    return pd.DataFrame({'S2': n_informal/denom*100,      # ×100
                         'S3': n_positive/denom*1000})    # ×1000

if __name__ == '__main__':
    df = pd.read_csv('analysis_v3.csv')
    print(style_features(df.plan_text).describe())

# ---------------------------------------------------------------------------
# Verification note (this repository). The raw plan texts are not distributed
# here (personal information), so this script cannot be re-run publicly; it is
# the archived original specification behind the S2/S3 columns of
# data/analysis_v3_public.csv. Reconstruction check (2026-08-12): applying
# these rules to the original texts reproduces the distributed S2/S3 columns
# for all 1,929 loans (max abs. error 4.4e-16 / 7.1e-15); descriptives match
# Appendix D (S2 mean .1909, 74.3% zeros; S3 mean 2.6440, 57.8% zeros;
# r = .043). Known limitations disclosed in Appendix D: informal-marker
# matches are dominated by punctuation runs (ellipses), and the stem '웃'
# produces partial-string false positives (48/1,724 = 2.8% of matches).
# ---------------------------------------------------------------------------
