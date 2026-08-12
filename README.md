# What Borrowers Say They Will Pay: Repayment Plans and Execution among Financially Excluded Borrowers

Verification repository for the manuscript. It contains the processed datasets, frozen analysis protocols, annotation codebooks, validation records, and verification code needed to reproduce the paper's confirmatory results, descriptive tables, and data figures — starting from processed (de-texted) data rather than raw borrower records.

**Data ethics note.** The borrower-authored application texts and raw platform records contain personal and financial information about individual borrowers and are **not** distributed here. Every variable derived from the texts (LLM annotations, rule-based extractions, the placebo payday variable) is included, so all quantitative results can be verified without access to the texts. Loan identifiers are platform listing codes with no personal names. The raw texts are available from the author upon reasonable request, subject to applicable data-protection requirements.

## Repository structure

```
data/
  analysis_v3_public.csv   Loan-level analysis file (1,929 loans, 91 variables).
                           = the paper's analysis dataset with the raw plan_text
                           column removed and the derived `salday` column
                           (rule-based payday extraction) added.
  panel_long.csv           Installment panel (19,755 rows, analytic sample): scheduled/actual
                           dates, payment status, delay, amounts.
  loan_level_pcg.csv       Loan-level plan-capacity-gap (PCG) file for the
                           RQ2 equivalence (TOST) analysis.
  annot_v3.csv             Frozen-codebook (v3) LLM annotation output
                           (labels only).
protocols/
  PROTOCOL_final2.md       Frozen confirmatory protocol (2026-08-05): RQ1
                           alignment test and delinquency-initiation hazard,
                           margins fixed before execution.
  CODEBOOK_v2.md           Annotation codebook, first version (development).
  CODEBOOK_v3.md           Frozen annotation codebook used for all v3
                           measures (this is also the LLM prompt).
validation/
  llm_key.csv              Original full-corpus LLM annotation (key labels).
  llm_rerun_2026-08.csv    Fresh-context LLM re-annotation of the 120
                           Phase B cases (run-to-run stability check).
  pb_map_final.csv         Phase B case -> loan_id mapping.
  phaseA_human_g3.csv      Phase A blind human coding (60 cases).
  phaseA_g3_merged.csv     Phase A human coding merged with machine labels.
code/
  verify_rq1_alignment.py  RQ1 confirmatory test: 91/854, 36.6% vs 24.3%
                           permutation null, p = .0005; window robustness.
  verify_placebo.py        Cash-flow placebo: group-specific permutation
                           nulls (A: 91 loans; B: 36 payday-only loans).
  salary_day_pattern.py    The deterministic rule-based payday extraction
                           pattern behind `salday` (no LLM involvement).
  placebo_cashflow_original_2026-08-05.py
                           Archived original placebo code (references the
                           undistributed plan_text; kept for provenance).
  style_features.py        Construction rules for the two writing-style
                           proxies (the S2/S3 columns): informal orthographic
                           markers and positive-emotion vocabulary.
  verify_descriptives.py   Sample construction, trajectory counts, Table 7.
  verify_validation_agreement.py
                           LLM run-to-run stability (P2 linear wkappa .935,
                           binary timing kappa .750).
  make_fig4_alignment.py   Figure 4 from data/ (alignment distribution).
  make_fig5_trajectories.py Figure 5 from data/ (trajectory map + branching).
  make_figG1_severity.py   Figure G1 from data/ (delay-severity map).
figures/
  Figure_1.png ... Figure_5.png, Figure_G1.png   Manuscript figures.
```

## Verification map

| Manuscript result | Data | Script | Expected output |
|---|---|---|---|
| §5.1 / Table 4: 36.6% vs 24.3%, p = .0005 (91 loans / 854 installments) | analysis_v3_public + panel_long | `verify_rq1_alignment.py` | matches to Monte Carlo precision |
| Table C1 window robustness (±1/3/5/7: 23.4/36.6/48.2/58.2 vs uniform) | same | `verify_rq1_alignment.py` | exact |
| §5.1 / Table 4 placebo: B group 36/326, 36.5% vs 22.8% (+13.7pp) | analysis_v3_public (`salday`) + panel_long | `verify_placebo.py` | matches to Monte Carlo precision |
| Placebo funnel 1,929 → 66 extracted → 36 no-timing | analysis_v3_public | `verify_descriptives.py` | exact |
| §3 / §5.3 sample and trajectory counts (1,873; 701/771/401; 791/381/496) | analysis_v3_public | `verify_descriptives.py` | exact |
| Table 7 descriptives (166, −10.4pp; 386, −2.6pp) | analysis_v3_public | `verify_descriptives.py` | exact |
| App. E run-to-run stability (wκ = .935, κ = .750, 93.3%) | validation/ | `verify_validation_agreement.py` | exact |
| Figures 4, 5, G1 | data/ | `make_fig*.py` | pixel-identical up to rendering |
| RQ2 nested LPM / TOST and RQ3 discrete-time hazards (Tables 5–6) | analysis_v3_public, loan_level_pcg, panel_long | specifications in the manuscript (§4.3–4.4) and PROTOCOL_final2.md | re-estimable from the distributed variables |

Permutation results are Monte Carlo; the archived 2026-08-05 runs are authoritative for the third digit. The confirmatory p-value uses the Phipson–Smyth correction (b+1)/(B+1).

## Environment

Python ≥ 3.10 with `pandas` and `numpy` (figure scripts additionally need `matplotlib` and `Pillow`). Run all scripts from the repository root.

## Notes on measurement provenance

The two rule-based measures that carry the paper's confirmatory results (the stated repayment day behind the alignment sample, and the repayment-date disclosure indicator behind the delinquency-initiation hazard) require no semantic judgment. Semantic measures were produced by a large language model applying the frozen codebook (protocols/CODEBOOK_v3.md) and validated against independent blinded human coding; the validation label files are in `validation/`.
