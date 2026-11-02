# Assignment final treatment 2 — executed once

Approved proposal SHA-256: `da8f65bfafe5e73edc18abbad70b8b9d482eeb8368bd1b94bb2e648a2996ca5a`. The sealed proposal remains unchanged; authorization is recorded separately in [the execution preflight folder](../reports/week4/assignment-final-treatment-2-authorized-preflight-1/). VS Code changed only its treatment plan/output arguments; the existing selective private loader was unchanged and no proposal-bound artifact was invalidated.

All proposal, dataset, dependency, private credential-presence, public pricing/lifecycle and preservation checks passed before dispatch. No authenticated discovery was performed. The existing supervised manifest path ran once: same frozen assignment-30-v1 inputs, gpt-4.1-mini-2025-04-14/default, V2/dependencies/reviewed targets, five calls/case, 150 total maximum, concurrency 1, zero retries, $63.223200 maximum. Exports and incident tools stayed OFF; local tracing remained enabled. The private key was loaded only into process memory and was never printed, copied, hashed or stored in artifacts.

| Actual measurement | Treatment 2 |
| --- | ---: |
| Assigned / attempted / unattempted | 30 / 30 / 0 |
| Model calls | 65 |
| Usage | 132,472 input + 12,562 output; 145,034 total tokens |
| Receipt-priced cost | $0.0730880 |
| Mean cost per attempted case | $0.00243627 |
| Retained uncertain reservations | $0 |
| Case latency p50 / p95 | 4.272s / 12.108s |
| Outcomes | 28 held / 1 completed workflow / 1 failed |

V2-05-01 retained AgentOutputError before its investigator provider call; subsequent safe cases continued. Case 016 selected the attribution dependencies and reached analyst, resolution and validator, but remained held. V2-03-01 completed its workflow and saved a final_report; this is not a human quality score or verified UI delivery. V2-15-01 held before analyst entry, so avoiding its prior resolution failure does not establish live wording compliance. Baseline and zero-call attempts were not rerun.

[Paired human-grading packet](../reports/week4/baseline-treatment-grading-2/README.md) contains all exact saved outputs/questions, separately identified internal reasoning/model outputs, approved expectations/applicability, routes, selections/dependencies, errors, usage, latency, existing baseline scores and blank treatment scores. [CSV measurements](../reports/week4/baseline-treatment-grading-2/paired-measurements.csv) provide blank treatment grading columns. All quality, safety and 032 robustness judgments remain pending; the cumulative comparison does not isolate per-change causality.

All 30 frozen input bindings and initial classifier request hashes match baseline. Selected-item reference checks: 180 checked, zero invalid; this is not human assessment of claim support. All 30 process cleanups were verified and all case trace exports were not requested. [Post-run audit](../reports/week4/assignment-final-treatment-2-authorized-preflight-1/postrun-preservation.json) verifies 328/328 inherited files and all 153 prior sealed groups (3,227 indexed artifacts), along with unchanged frozen dataset, workbook/reviews, baseline and previous attempts. No behavior or input repairs occurred during execution. The launch now points to an existing sealed output directory and cannot be reused as a fresh authorized run.
