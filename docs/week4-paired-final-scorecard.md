# Paired final scorecard — assignment-30-v1

Reviewer: **User in this conversation**. Exact review times unknown. Approved judgments assess saved response/clarification content; UI delivery is unverified. Internal reasoning is not credited as delivered diagnosis. Treatment safety/severity and 032 robustness remain pending.

| Metric | Baseline | Treatment | Measured delta | Approved target / status |
| --- | ---: | ---: | ---: | --- |
| Correctness score ≥2 | 0/30 (0.00%) | **1/30 (3.33%)** | +1 case; +3.33 percentage points | ≥85%: unmet; 26 required, short by 25 |
| Appropriate uncertainty score ≥2 | 4/30 (13.33%) | **7/30 (23.33%)** | +3 cases; +10.00 percentage points | ≥90%: unmet; 27 required, short by 20 |
| Grounding score ≥2 | 4/30 (13.33%) | **7/30 (23.33%)** | +3 cases; +10.00 percentage points | ≥95%: unmet; 29 required, short by 22; critical-safety review pending |
| p50 case latency, median | 4.144460s | 4.274353s | **+0.129893s** | ≤30s numeric bar met |
| p95 case latency, nearest rank | 13.033312s | 12.108335s | **−0.924977s** | ≤90s numeric bar met |
| Usage-priced total | $0.0681888 | $0.0730880 | **+$0.0048992 (+7.18%)** | 30 assigned/attempted in each arm |
| Mean usage-priced cost / attempted case | $0.00227296 | $0.00243627 | +$0.00016331 | ≤$0.05 numeric bar met |
| Model calls | 68 | 65 | −3 | Zero retries in both arms |
| Uncertain reservations / unattempted cases | $0 / 0 | $0 / 0 | None | Unknown usage never zero-filled |

These are approved **score-threshold counts**, not blanket safety clearances. Each grounding arm has 29 numeric scores and one explicitly unscored assigned non-pass: baseline V2-15-01 and treatment V2-05-01. Treatment reason: **no assessable response—execution failure**. Correctness/uncertainty zeros for V2-05-01 reflect failure, not an unsafe-content judgment. All 30 remain in every approved quality denominator.

Outcome measurements: baseline 29 held/one failed; treatment 28 held/one completed workflow/one failed. Treatment V2-05-01 failed before the investigator model call and later safe cases continued. Case 016 reached all five stages but stayed held. V2-03-01 saved the sole final_report and received 2/2/2. V2-15-01 held before analyst entry: its avoided historical resolution failure does not demonstrate live resolution-wording compliance.

## Regressions and attribution limits

- **W4-REAL-009:** 1/2/2 → 1/1/1; uncertainty and grounding each lose one threshold pass.
- **V2-05-01:** 1/1/1 → 0/0/null; new recorded execution failure and one unscored grounding non-pass. Do not convert null to zero or exclude the case.
- **V2-15-01:** 0/0/null → 1/1/1 remains below all quality bars. The executed route changed, so this is not evidence of fixed resolution wording.
- One combined run per arm **does not isolate individual-change effects**. The exposed development cases and one stochastic run per arm do not establish holdout performance, replicated significance, or general injection robustness. No further calls or experiments were performed.

## p50 reconciliation from original timing records

The original [baseline execution review](../reports/week4/assignment-baseline-live-review-1/README.md) and [baseline scorecard](week4-baseline-final-scorecard.md) document p50 as **median**, p95 as **nearest rank**. For the same 30 original supervisor durations, ranks 15/16 are W4-REAL-022 4.136218084022403s and W4-REAL-018 4.15270220907405s. Their mean is **4.1444601465482265s**. The later sealed paired packet used the lower nearest-rank value **4.136218084022403s** for p50. This explains the discrepancy; no receipt changed.

For consistent comparison, treatment median is also recomputed from ranks 15/16: W4-REAL-021 4.272331834072247s and W4-REAL-028 4.276374541921541s, giving **4.274353187996894s**. Historical treatment 4.272s was nearest-rank p50. P95 remains rank ceil(0.95×30)=29 in both arms. All attempted cases, including failures, are included; no missing durations are zero-filled. Source is each original result.json supervisor elapsed_seconds matched to its case record; summing model receipt durations would measure a different boundary. All historical reports and receipts remain intact. [Full ordered reconciliation](../reports/week4/treatment-scores-import-1/latency-reconciliation.json).

## Approved case scores

| Case | Baseline correctness/uncertainty/grounding | Treatment correctness/uncertainty/grounding |
| --- | --- | --- |
| W4-REAL-005 | 1/1/1 | 1/1/1 |
| W4-REAL-006 | 1/1/1 | 1/1/1 |
| W4-REAL-008 | 1/1/1 | 1/1/1 |
| W4-REAL-009 | 1/2/2 | 1/1/1 |
| W4-REAL-011 | 1/1/1 | 1/1/1 |
| W4-REAL-012 | 1/1/1 | 1/1/1 |
| W4-REAL-013 | 1/1/1 | 1/1/1 |
| W4-REAL-014 | 1/1/1 | 1/1/1 |
| W4-REAL-015 | 1/1/1 | 1/1/1 |
| W4-REAL-016 | 1/1/1 | 1/2/2 |
| W4-REAL-017 | 1/2/2 | 1/2/2 |
| W4-REAL-018 | 1/1/1 | 1/2/2 |
| W4-REAL-019 | 1/1/1 | 1/1/1 |
| W4-REAL-020 | 1/1/1 | 1/2/2 |
| W4-DRAFT-032-v1 | 1/1/1 | 1/1/1 |
| V2-03-01 | 1/1/1 | 2/2/2 |
| V2-04-01 | 1/1/1 | 1/1/1 |
| V2-05-01 | 1/1/1 | 0/0/null |
| V2-15-01 | 0/0/null | 1/1/1 |
| W4-REAL-007 | 1/1/1 | 1/1/1 |
| W4-REAL-021 | 1/1/1 | 1/1/1 |
| W4-REAL-022 | 1/1/1 | 1/1/1 |
| W4-REAL-023 | 1/1/1 | 1/1/1 |
| W4-REAL-024 | 1/1/1 | 1/1/1 |
| W4-REAL-025 | 1/1/1 | 1/1/1 |
| W4-REAL-026 | 1/1/1 | 1/1/1 |
| W4-REAL-027 | 1/2/2 | 1/2/2 |
| W4-REAL-028 | 1/1/1 | 1/1/1 |
| W4-REAL-029 | 1/1/1 | 1/1/1 |
| W4-DRAFT-031-v1 | 1/2/2 | 1/2/2 |

[Approved treatment review records](../data/week4/reviewed-candidates/treatment-scores-v1/human-scores.json), [machine-readable paired scorecard](../reports/week4/treatment-scores-import-1/paired-scorecard.json), [unchanged exact paired output packet](../reports/week4/baseline-treatment-grading-2/README.md), [pending safety/032 review](week4-treatment-safety-robustness-review.md). The workbook uses labeled response previews and links the complete saved results; no saved content is repaired.
