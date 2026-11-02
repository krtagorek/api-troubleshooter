# Paired baseline / final-treatment-2 results — treatment grading pending

One approved treatment execution; no retry, repair or baseline rerun. The original proposal and separate authorization are preserved. The previous zero-call attempt remains sealed and is excluded from model-quality comparison. All treatment semantic/safety/robustness fields remain blank.

| Measurement | Sealed baseline | Treatment 2 |
| --- | ---: | ---: |
| Assigned / attempted / unattempted | 30 / 30 / 0 | 30 / 30 / 0 |
| Actual model calls | 68 | 65 |
| Usage-priced total USD | 0.0681888 | 0.0730880 |
| Mean USD per attempted case | 0.00227296 | 0.002436266666666666666666666667 |
| Retained reservations USD | 0 | 0 |
| Supervisor latency p50 / p95 seconds | 4.136 / 13.033 | 4.272 / 12.108 |
| Analyst entries | 3 | 2 |

Treatment: 28 held, one completed workflow (V2-03-01), one failure (V2-05-01). V2-05-01 retains AgentOutputError before its investigator provider call; its classifier receipt remains and later safe cases continued. V2-15-01 changed from a baseline resolution failure to a pre-analyst hold; this does not demonstrate live resolution-wording compliance.

Case 016 selected the attribution dependencies and reached analyst/resolution/validator, but remained held with qualified_evidence_required. V2-03-01 has the one saved final_report; it still requires human grading and does not establish UI delivery. 032 held before analyst entry in treatment, whereas baseline reached later stages. These are observed route/outcome changes, not semantic judgments.

Mechanical grouping: 27 treatment holds before analyst entry, one later hold (016), one pre-analyst failure (V2-05-01), one completed workflow (V2-03-01). Changed terminal outcomes: V2-03-01 held→completed; V2-05-01 held→failed; V2-15-01 failed→held. Changed agent routes: 016, 032 and V2-15-01; an unchanged started-node route can still contain a skipped provider call, as V2-05-01 shows.

All 30 frozen input bindings and initial classifier provider-request hashes match the baseline. Later request streams depend on the intended advisories and actual model outputs; full-stream parity is not claimed. The combined final-versus-baseline comparison cannot isolate per-change semantic causality.

Deterministic selected-item reference binding: baseline 150 checked, treatment 180 checked, zero invalid in each. This is not human grounding assessment of material claims, diagnostic accuracy, or a safety pass. Treatment usage: 132,472 input + 12,562 output = 145,034 tokens, cached input 0. All 65 usage receipts are known; no retained liability. Summary JSON explicitly records missingness for every usage field. Latency is the existing case-supervision boundary over all 30 attempts including failure; report/preflight overhead is excluded.

Baseline approved scores stay correctness 0/30, uncertainty 4/30 and grounding 4/30, with V2-15-01 explicitly unscored for grounding and retained as non-pass. The workbook and all treatment score fields remain unchanged/blank; no automated semantic improvement claim is made.

[Exact paired saved content](paired-responses.md), [complete machine records](paired-cases.json), [measurements and blank treatment grading columns](paired-measurements.csv), [summary / usage](summary.json), [mechanics checks](mechanics-and-binding-checks.json).

| Case | Baseline → treatment outcome | Calls B/T | Cost USD B/T | Latency s B/T |
| --- | --- | ---: | ---: | ---: |
| W4-REAL-005 | held → held | 2/2 | 0.0015072/0.0016388 | 5.869/5.703 |
| W4-REAL-006 | held → held | 2/2 | 0.0016716/0.0017144 | 3.618/4.147 |
| W4-REAL-008 | held → held | 2/2 | 0.0016732/0.001848 | 4.256/4.702 |
| W4-REAL-009 | held → held | 2/2 | 0.0014580/0.0014872 | 4.559/3.676 |
| W4-REAL-011 | held → held | 2/2 | 0.0014860/0.0016416 | 3.449/4.550 |
| W4-REAL-012 | held → held | 2/2 | 0.0018756/0.0019316 | 4.465/4.140 |
| W4-REAL-013 | held → held | 2/2 | 0.0014592/0.0015684 | 3.701/3.871 |
| W4-REAL-014 | held → held | 2/2 | 0.0016512/0.0018648 | 4.114/5.058 |
| W4-REAL-015 | held → held | 2/2 | 0.0015772/0.0016748 | 4.570/3.946 |
| W4-REAL-016 | held → held | 2/5 | 0.0033792/0.0149320 | 3.745/15.451 |
| W4-REAL-017 | held → held | 2/2 | 0.0016188/0.0016644 | 4.403/4.215 |
| W4-REAL-018 | held → held | 2/2 | 0.001646/0.0017664 | 4.153/4.332 |
| W4-REAL-019 | held → held | 2/2 | 0.0021356/0.0021688 | 4.924/4.408 |
| W4-REAL-020 | held → held | 2/2 | 0.0020776/0.0022532 | 3.866/4.211 |
| W4-DRAFT-032-v1 | held → held | 5/2 | 0.0072188/0.0021012 | 13.072/3.769 |
| V2-03-01 | held → completed | 5/5 | 0.0069992/0.0071248 | 13.033/12.108 |
| V2-04-01 | held → held | 2/2 | 0.0020284/0.0021920 | 4.554/4.372 |
| V2-05-01 | held → failed | 2/1 | 0.0019920/0.0009992 | 3.720/2.323 |
| V2-15-01 | failed → held | 4/2 | 0.0056040/0.0020244 | 10.514/3.591 |
| W4-REAL-007 | held → held | 2/2 | 0.0017672/0.0018924 | 4.031/3.728 |
| W4-REAL-021 | held → held | 2/2 | 0.0016368/0.0017656 | 4.227/4.272 |
| W4-REAL-022 | held → held | 2/2 | 0.0016372/0.0018244 | 4.136/4.300 |
| W4-REAL-023 | held → held | 2/2 | 0.0016220/0.0016844 | 3.975/3.844 |
| W4-REAL-024 | held → held | 2/2 | 0.0016632/0.0017596 | 3.840/4.044 |
| W4-REAL-025 | held → held | 2/2 | 0.0016968/0.0017292 | 4.000/4.585 |
| W4-REAL-026 | held → held | 2/2 | 0.0017688/0.0019240 | 4.020/4.782 |
| W4-REAL-027 | held → held | 2/2 | 0.0016988/0.0018812 | 4.179/4.423 |
| W4-REAL-028 | held → held | 2/2 | 0.0017492/0.0019224 | 3.729/4.276 |
| W4-REAL-029 | held → held | 2/2 | 0.0015044/0.0015016 | 3.995/3.651 |
| W4-DRAFT-031-v1 | held → held | 2/2 | 0.0023856/0.0026072 | 4.347/4.850 |
