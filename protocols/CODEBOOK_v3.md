# Appendix A v3 — Revised Codebook for P3 and P4 (frozen 2026-08-05)

*English translation. The Korean original below is the frozen instrument of record — the Korean text is what was given to the LLM annotator as the prompt. Where translation and original could diverge, the original governs.*

Following the diagnosis from the G3 human validation (κ_P3 = 0.125, κ_P4 = 0.126), only P3 and P4 were revised. The P1, P2, and P5 definitions remain as in v2 (no re-annotation).

## P3 Temporal structure (v3)

**The timing must attach to the act of repayment — not to the timing of income arrival.**

1 = no mention of repayment timing
2 = vague ("as soon as possible", "I will repay when I have room")
3 = repayment timing given relatively or as a range ("I will start repaying in three months", "I will settle it in the second half of the year", "I will repay when the bonus comes")
4 = a repeatable or specific time is designated for the act of repayment
    ("I will repay on the 25th of every month", "I will deposit it right on payday", "repayment completed by January 2020")
5 = two or more such repayment times form a structure
    ("200,000 won on the 25th of every month, early repayment of the balance when the December bonus arrives")

### Exclusion rules (new in v3 — the core of the judgment)
- **Statements that only describe when income arrives are not P3.**
  "My payday is the 25th of every month" (income description) → P3 = 1 if nothing else is said
  "I will repay right on my payday, the 25th" (linked to the act of repayment) → P3 = 4
- **Dates inside explanations of past delinquency are not P3.**
  "The delinquency happened because my payday moved from the 5th to the 10th" → ignored for the P3 judgment
- Dates inside income/expense tables ("received on the 10th of every month") are ignored
- Bare mentions of loan maturity or term ("applying for 12 months") are ignored

## P4 Contingency (v3)

**Expressions of repayment resolve are not P4. The condition "if things go wrong" must be explicit or clearly implied.**

1 = no mention of the possibility of repayment disruption
    ※ General resolve ("I will repay diligently", "I will never be late", "I promise faithful repayment") is always 1
2 = only current hardship described, no provision for disruption
3 = vague determination about what to do if disruption occurs
    ("I will repay no matter what", "even if I have to work myself to the bone", "even if I have to take a part-time job")
4 = one concrete alternative in case of disruption ("if business is bad, I will repay even if I have to pull out my deposit")
5 = alternative + trigger condition ("if sales fall below half, I will repay from the academy's key money")

## Anchor (only for cases with P3 = 4 or 5)

**The question is what the repayment timing is tied to — not what the repayment resource is (resources are P2).**

- income = tied to a recurring income event (repaying on payday, pension payment day, benefit deposit day)
- calendar = a date designated without mention of an income event (repaying on the 10th of every month)
- event = tied to a one-off event (upon receiving severance pay, from a maturing insurance payout)
- none = cannot be determined

Auxiliary: day = the designated day of month (1–31, null if none) · multi = whether multiple times form a structure

## Validation plan
- New LLM output is compared against the existing 60-case human coding (produced blind, fixed)
- Because these 60 cases were also used to diagnose the codebook, the kappa is an optimistic estimate — stated in the paper, with bootstrap CIs alongside
- For P4, the human reference values do not match the new definition → **demoted to an unvalidated exploratory variable in the appendix. Main block = P1, P2, P3b, P5**

---

## Original (Korean) — frozen instrument of record (the LLM prompt)

# 부록 A v3 — P3·P4 개정 코드북 (2026-08-05 동결)

G3 인간 검증(κ_P3=0.125, κ_P4=0.126)의 진단에 따라 P3·P4만 개정. P1·P2·P5 정의는 v2 유지(재주석 없음).

## P3 시간 구조 (v3)

**"상환 행위"에 시점이 붙어야 한다. 소득이 들어오는 시점이 아니다.**

1 = 상환 시점에 대한 언급 없음
2 = 막연 ("빠른 시일 내에", "여유가 생기면 갚겠다")
3 = 상환 시점이 상대적·범위로 제시 ("3개월 후부터 갚겠다", "하반기에 정리하겠다", "보너스 나오면 상환")
4 = 상환 행위에 반복 가능하거나 특정한 시점이 지정
    ("매월 25일에 상환하겠습니다", "급여일에 바로 입금하겠습니다", "2020년 1월까지 상환 완료")
5 = 그런 상환 시점이 둘 이상 구조를 이룸
    ("매월 25일에 20만원씩, 12월 상여 수령 시 잔액 조기상환")

### 배제 규칙 (v3 신설 — 판정의 핵심)
- **소득 유입 시점만 서술한 것은 P3가 아니다.**
  "급여일은 매월 25일입니다" (수입 설명) → 다른 언급 없으면 P3=1
  "급여일인 25일에 바로 상환하겠습니다" (상환 행위에 연결) → P3=4
- **과거 연체에 대한 해명 속의 날짜는 P3가 아니다.**
  "연체는 급여일이 5일에서 10일로 바뀌어서 그랬다" → P3 판정에서 무시
- 수입·지출 내역표 안의 날짜("매월 10일 수령")는 무시
- 대출 만기·기간의 단순 언급("12개월로 신청")은 무시

## P4 조건부성 (v3)

**상환 의지의 표명은 P4가 아니다. '차질이 생기면'이라는 조건이 명시되거나 분명히 함의되어야 한다.**

1 = 상환 차질 가능성에 대한 언급 없음
    ※ 일반적 다짐("열심히 갚겠습니다", "절대 연체하지 않겠습니다", "성실상환 약속드립니다")은 전부 1
2 = 현재의 어려움만 서술, 차질 시 대비는 없음
3 = 차질이 생길 경우에 대한 막연한 각오
    ("무슨 일이 있어도 갚겠다", "몸이 부서져라 일해서라도", "알바를 해서라도")
4 = 차질 시 구체적 대안 1개 ("장사가 안 되면 보증금을 빼서라도 상환")
5 = 대안 + 발동 조건 ("매출이 절반 이하로 떨어지면 학원 권리금으로 상환")

## 앵커 (P3 = 4 또는 5인 건만)

**상환 시점이 무엇에 걸려 있는가를 묻는다. 재원이 무엇인가가 아니다(재원은 P2).**

- income = 반복적 소득 사건에 연동 (급여일·연금지급일·수급비 입금일에 상환)
- calendar = 소득 사건 언급 없이 날짜만 지정 (매월 10일에 상환)
- event = 일회성 사건에 연동 (퇴직금 수령 시, 만기 보험금으로)
- none = 판정 불가

부속: day = 지정된 날짜(1~31, 없으면 null) · multi = 복수 시점 구조 여부

## 검증 계획
- 신규 LLM 출력을 기존 인간 60건 코딩(블라인드 생산, 고정)과 대조
- 이 60건은 코드북 진단에도 사용되었으므로 카파는 낙관적 추정치 — 논문에 명시, 부트스트랩 CI 병기
- P4는 인간 기준값이 새 정의와 불일치 → **미검증 탐색 변수로 부록 강등. 주 블록 = P1·P2·P3b·P5**
