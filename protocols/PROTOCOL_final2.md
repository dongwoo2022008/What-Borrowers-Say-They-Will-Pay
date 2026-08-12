# Final Two-Test Pre-Specification Protocol (frozen 2026-08-05 — written before execution)

*English translation. The Korean original below is the frozen document of record.*

The last two legitimate tests of the original narrative ("the propositional content of plans carries incremental information about performance"). Exploring any margin beyond the criteria written in this document is prohibited. If both tests fail, the original narrative is abandoned and Plan B (reframing around the negative results) is adopted.

## Disclosures (honesty)

- For Test 1, one feasibility peek was performed before execution (pooled-installment basis: 36.8% vs. placebo 24.4%). The confirmatory test is pre-specified at the more conservative loan level, and the peek is disclosed in the paper.
- Test 2 (hazard) was not run in any form beforehand.

## Test 1 — Promise–behavior correspondence

- Sample: loans with P3v3 ≥ 4 and a stated promise day (`day`) (91 expected), installments with actual payment dates
- Main statistic: the across-loan mean of each loan's "share of installments paid within ±3 days of the promised day"
- Inference: permutation test reassigning promised days across loans, 2,000 draws (loan level), one-sided p
- **Pass line: p < 0.05**
- Secondary (not used for the pass/fail decision): ±1-day and ±5-day windows; subsample with stated-day-to-due-day distance ≥ 7 days (severing contractual alignment); early-payment installments only; loan-clustered regression of the circular distance between actual and promised days
- Confounding defense: the permutation preserves the marginal distribution of promised days, so the general tendency of payments to cluster on particular calendar days is controlled

## Test 2 — Installment-level discrete-time hazard, three events (RQ3)

- Data: installment panel. GLM with cloglog link
- Events: (1) delinquency initiation (risk set: installments before first delinquency); (2) return to current (risk set: delinquent installments after first delinquency); (3) re-delinquency (risk set: installments after return)
- Content block: **P2 (validated, κ = .735), P3b (v3, validated), pay_sched_rx (rule-based), P1 (κ = .317 — attenuation caveat stated)**
- Baseline model: installment-progress polynomial (cubic) + year FE + ln(amount) + term + interest rate + gender + past performance (with missing indicator) + ln(length)
- Main test: LR test of the four-variable content block at each event, **Holm correction across the three events**
- **Pass line: block p < 0.05 at one or more events after Holm correction**
- SEs: loan-level cluster (robust) reported alongside

## Decision rules

- Both pass → refine and keep the original narrative as "content predicts the structure and timing of repayment"
- Only Test 1 passes → reframe around correspondence (abandon success-prediction claims)
- Only Test 2 passes → reframe around dynamics
- Both fail → **Plan B confirmed. No further exploration.**

---

## Original (Korean) — frozen document of record

# 최종 2검정 사전 지정 프로토콜 (2026-08-05 동결 — 실행 전 작성)

당초 서사("계획의 명제적 내용은 이행에 관한 증분 정보를 담는다")의 마지막 합법적 검정 두 개.
이 문서에 적힌 기준 이외의 추가 마진 탐색은 금지한다. 두 검정 모두 실패 시 당초 서사를 접고 B안(음의 결과 재구성)으로 확정한다.

## 공개 사항 (정직성)
- 검정 1은 실행 전 타당성 점검(feasibility peek)을 1회 수행했다(회차 풀링 기준 36.8% vs 플라시보 24.4%).
  본검정은 더 보수적인 대출 수준 추론으로 사전 지정하며, peek 사실을 논문에 명시한다.
- 검정 2(hazard)는 어떤 형태로도 미리 돌리지 않았다.

## 검정 1 — 약속–행동 대응 (correspondence)
- 표본: P3v3≥4이고 약속 날짜(day) 명시된 대출 (91건 예상), 실제 납부일 보유 회차
- 주 통계량: 대출별 "약속일 ±3일 이내 납부 회차 비율"의 대출 간 평균
- 추론: 약속일을 대출 간 무작위 재배정하는 순열검정 2,000회 (대출 수준), 단측 p
- **합격선: p < 0.05**
- 보조(합격 판정에 불사용): ±1일·±5일 창, 예정일-약속일 거리 ≥7일 하위표본(계약 정렬 배제),
  조기납부 회차 한정, 실제일-약속일 원형거리의 대출 클러스터 회귀
- 교란 방어: 순열이 약속일의 주변분포를 보존하므로 '납부일이 특정 날짜에 몰리는' 일반 경향은 통제됨

## 검정 2 — 회차 수준 이산시간 hazard 3사건 (RQ3)
- 자료: 회차 패널. cloglog 링크 GLM
- 사건: ①연체 개시(위험집합: 첫 연체 전 회차) ②정상 복귀(위험집합: 첫 연체 후 연체 상태 회차)
  ③재연체(위험집합: 복귀 후 회차)
- 내용 블록: **P2(κ=.735 검증), P3b(v3, 검증), pay_sched_rx(규칙 기반), P1(κ=.317 — 감쇠 유보 명시)**
- 기저모형: 회차 진행률(3차 다항) + 연도 FE + ln금액 + 기간 + 이자율 + 성별 + 과거이행(결측지시자) + ln길이
- 주검정: 각 사건에서 내용 블록 4변수의 LR 검정, **3사건 간 Holm 보정**
- **합격선: Holm 보정 후 1개 사건 이상에서 블록 p < 0.05**
- SE: 대출 수준 클러스터(로버스트)로 확인 병기

## 판정 규칙
- 둘 다 합격 → 당초 서사를 "내용은 상환의 구조·시점을 예측한다"로 정련하여 유지
- 검정 1만 합격 → 대응 중심으로 재구성(성패 예측 주장은 포기)
- 검정 2만 합격 → 동태 중심으로 재구성
- 둘 다 불합격 → **B안 확정. 추가 탐색 금지**
