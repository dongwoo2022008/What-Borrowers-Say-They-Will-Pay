# Appendix A v2 — Codebook for the Propositional Content of Repayment Plans (frozen 2026-08-04)

*English translation. The Korean original below is the frozen instrument of record — the Korean text is what was given to the LLM annotator as the prompt. Where translation and original could diverge, the original governs.*

Changes from v1: (1) P4 binarization finalized; (2) G4 gate deleted; (3) P5 conditional-reporting rule; (4) reduced set of variables subject to length residualization.

## Coding target

The `descriptiveRepaymentPlanBody` field of the 1,930 analytic-sample loans. Texts under 30 characters excluded (none applied). Whitespace-normalized, truncated at 2,500 characters.

## The five dimensions

**P1 Specificity** — the degree to which the act of repayment is numerically specified
1 = general resolve only ("I will repay faithfully")
2 = method mentioned but vague ("I will repay from my salary")
3 = amount **or** frequency numerically stated (one of the two)
4 = amount **and** frequency both stated
5 = amount + frequency + linked to income context ("300,000 of my 2.1 million monthly, on the 25th of every month")

**P2 Funding-source identification** — the degree to which the repayment source is specified
1 = none / 2 = vague ("by working hard")
3 = one source specified / 4 = one source + amount / 5 = multiple sources + amounts

**P3 Temporal structure** — the degree to which timing is specified
1 = none / 2 = vague ("as soon as possible")
3 = relative timing ("in three months") / 4 = one specific time ("the 25th of every month") / 5 = multiple-time structure

**P4 Contingency** — mention of provisions for disruption
1 = no mention of disruption / 2 = only hardship mentioned / 3 = vague determination
4 = one concrete alternative / 5 = alternative + trigger condition

**P5 Evidential grounding** — whether the source is a present fact or a future expectation
1 = no grounding / 2 = entirely future expectation / 3 = mostly future / 4 = mostly present / 5 = entirely present fact

Cannot judge = **9**

## Transformation rules for analysis (finalized in v2)

| Variable | Analysis form | Basis |
|---|---|---|
| P1 | ordinal 1–5 (raw scale) | pilot SD 1.59, length correlation +0.165 |
| P2 | ordinal 1–5 | SD 1.17 |
| P3 | ordinal 1–5 | SD 1.41 |
| **P4** | **binary = 1(P4 ≥ 2)** | 66% of the 5-point mass at 1. After binarization: rate 33.8%, within-group variation 45% |
| P5 | ordinal 1–5, **no individual-coefficient interpretation** | definitionally dependent on P2 (r = +0.717). Composite index reported alongside |
| amt_stated | binary (whether a promised amount is stated) | robustness substitute for P1. r(P1) = +0.864 |

- **9 (cannot judge) treated as missing + missing indicator.** Pilot incidence 0%.
- The raw 5-point P4 is preserved → appendix distribution table and robustness checks.
- P5 conditional reporting: the main-text correlation table uses the full sample; the appendix adds correlations conditional on P2 ≥ 3.

## Length-confounding treatment (reduced in v2)

- **P1: no residualization needed.** Length correlation +0.165 — the correlation is simply reported in the text.
- **P2 (+0.360), P3 (+0.330), P4 (+0.439): length-residualized robustness checks required.**
- Style S1 (length) is always included in the M1 baseline model.

## Gates (v2)

| Gate | Criterion | Status |
|---|---|---|
| G1 measurement variation | mode < 60% & SD ≥ 0.9 (P4: post-binarization rate 15–85%) | passed |
| G2 within-borrower variation | within-SD > 0 in 30%+ of repeat-borrower groups | passed |
| G3 human agreement | weighted kappa and directional agreement | in progress |
| ~~G4 promised-amount extraction~~ | **deleted** — r = +0.864 with P1, same construct | discarded |

## Annotation execution specification

- Batches of 70 · 28 batches total · parallel agents
- Output: JSONL, `{"id":..,"P1":..,"P2":..,"P3":..,"P4":..,"P5":..,"amt":..,"freq":..,"src":[..],"ev":".."}`
- Quality checks: one-way ANOVA of batch-mean differences (pilot: p > 0.21 on all dimensions), replication check against the 198-case pilot

---

## Original (Korean) — frozen instrument of record (the LLM prompt)

# 부록 A v2 — 상환계획 명제적 내용 코드북 (2026-08-04 동결)

v1 대비 변경: ①P4 이진화 확정 ②G4 게이트 삭제 ③P5 조건부 보고 규칙 ④길이 잔차화 대상 축소

## 코딩 대상
분석표본 1,930건의 `descriptiveRepaymentPlanBody`. 30자 미만 제외(해당 없음).
공백 정규화 후 2,500자에서 절단.

## 다섯 차원

**P1 구체성** — 상환 행위가 수치로 특정되는 정도
1 = 일반 다짐만("성실히 갚겠습니다")
2 = 방식 언급하나 모호("월급에서 갚겠습니다")
3 = 금액 **또는** 주기 중 하나 수치 명시
4 = 금액 **및** 주기 모두 명시
5 = 금액+주기+소득맥락 연결("월 210만 중 30만을 매월 25일")

**P2 재원 식별** — 상환 재원이 특정되는 정도
1 = 없음 / 2 = 막연("열심히 벌어서")
3 = 재원 1개 특정 / 4 = 재원 1개+금액 / 5 = 복수 재원+금액

**P3 시간 구조** — 시점이 특정되는 정도
1 = 없음 / 2 = 막연("빠른 시일 내")
3 = 상대적 시점("3개월 후") / 4 = 구체적 시점 1개("매월 25일") / 5 = 복수 시점 구조

**P4 조건부성** — 차질 상황 대비 언급
1 = 차질 언급 없음 / 2 = 어려움만 언급 / 3 = 막연한 각오
4 = 구체적 대안 1개 / 5 = 대안+발동조건

**P5 실현 근거** — 재원이 현재 사실인가 미래 기대인가
1 = 근거 없음 / 2 = 전적 미래 기대 / 3 = 미래 우세 / 4 = 현재 우세 / 5 = 전적 현재 사실

판정 불가 = **9**

## 분석 시 변환 규칙 (v2 확정)

| 변수 | 분석 형태 | 근거 |
|---|---|---|
| P1 | 1~5 순서형 (원첩도) | 파일럿 SD 1.59, 길이 상관 +0.165 |
| P2 | 1~5 순서형 | SD 1.17 |
| P3 | 1~5 순서형 | SD 1.41 |
| **P4** | **이진 = 1(P4≥2)** | 5점 중 66%가 1에 집중. 이진화 시 비율 33.8%, 군내변이 45% |
| P5 | 1~5 순서형, **개별 계수 해석 금지** | P2와 정의상 의존(r=+0.717). 합성지표 병기 |
| amt_stated | 이진 (약속액 명시 여부) | P1의 견고성 대체변수. r(P1)=+0.864 |

- **9(판정불가)는 결측 처리 + 결측지시자**. 파일럿 발생률 0%.
- P4 원 5점은 보존 → 부록 분포표 및 견고성 점검.
- P5 조건부 보고: 본문 상관표는 전체, 부록에 P2≥3 조건부 상관 병기.

## 길이 교락 처리 (v2 축소)
- **P1: 잔차화 불필요.** 길이 상관 +0.165 — 상관값만 본문 보고.
- **P2(+0.360)·P3(+0.330)·P4(+0.439): 길이 잔차화 견고성 점검 필수.**
- 문체 S1(길이)은 M1 기저모형에 상시 포함.

## 게이트 (v2)
| 게이트 | 기준 | 상태 |
|---|---|---|
| G1 측정변이 | 최빈<60% & SD≥0.9 (P4는 이진 후 비율 15~85%) | 통과 |
| G2 차입자내 변이 | 반복군의 30%+ 에서 within-SD>0 | 통과 |
| G3 인간 일치 | 가중 카파 및 방향 일치 | 진행 중 |
| ~~G4 약속액 추출~~ | **삭제** — P1과 r=+0.864로 동일 구성개념 | 폐기 |

## 주석 실행 사양
- 배치 70건 · 총 28배치 · 병렬 에이전트
- 출력: JSONL, `{"id":..,"P1":..,"P2":..,"P3":..,"P4":..,"P5":..,"amt":..,"freq":..,"src":[..],"ev":".."}`
- 품질점검: 배치 간 평균 차이 일원분산분석(파일럿 전 차원 p>0.21), 파일럿 198건 재현성 대조
