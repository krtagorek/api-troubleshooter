# Week 4 Loom walkthrough — suggested 4–5 minutes

Record the workbook, this report and saved artifacts. Keep the open private .env tab and any credentials out of the recording. Do not launch tasks or rerun the agent. Suggested timing is optional; the brief requires a short walkthrough, not a fixed duration.

## 0:00–0:35 — Use case and outcome

Show the opening of [the evaluation report](week4-evaluation-report.md).

“I evaluated my Week 3 API Troubleshooter, which uses several agents to classify an incident, select evidence, analyze causes, propose read-only diagnostic steps and validate the output. The user needs a supported explanation or useful clarification. A plausible internal diagnosis is insufficient if the saved response is unhelpful or unsupported. I chose the own-use-case spreadsheet track with local traces; external LangSmith exports were deferred.”

## 0:35–1:10 — Dataset and rubric

Show workbook Review, Inputs and Rubric.

“There are 30 identical frozen cases in both runs. Twenty-four come from public incident reports, one is an explicitly qualified third-party mock-upstream reproduction, and five consume the conservative artificial allowance. Five out of thirty is 16.67 percent. The mix is 12 happy, 15 edge, two difficult and one adversarial, skewed toward partial evidence. Cases were development-exposed and some share families, so this is not an independent holdout. I reviewed expected behavior and scored saved outputs from zero to three; two is a pass. Exact review times are unknown.”

“The five metrics are correctness, uncertainty, grounding, latency and cost. Grounding includes human claim-support review, not only valid references. Holds and execution errors remain in the denominator.”

## 1:10–1:55 — Baseline failure

Open saved baseline W4-REAL-016 result or its section in the paired packet; distinguish saved questions from internal reasoning.

“The baseline attempted all 30 cases: 27 held before analyst entry, two had later publication holds, and one failed during resolution output validation. Case 016 preserved a non-ASCII header and reported exception but omitted attribution dependencies. Its hold does not prove that all source evidence was absent. Overall correctness had zero passes; uncertainty and grounding each had four. All baseline final reports were null; UI delivery was not verified.”

## 1:55–2:40 — Three targeted changes

Show the report's three-change table and the existing advisory source if useful.

“First, I reused V2 attribution and dependency work to distinguish omitted selection from unavailable evidence. Second, I added safe, specific clarification and partial-content guidance through existing fields, preserving holds and validators. Third, I added read-only wording guidance compatible with the unchanged resolution validator. These are three functional targets; policy version numbers are not separate improvements.”

“Offline controls checked valid and forged evidence, missing dependencies, failures and limits. Those scripted tests establish mechanics, not model quality. The historical resolution-wording failure case did not reach resolution in the final live run, so that targeted fix was not validated live.”

## 2:40–3:40 — Measured outcomes and regressions

Show workbook metrics and the final score table. Optionally show V2-03-01's saved final report alongside its safety finding.

“The final run made 65 calls and cost 7.31 cents. Correctness rose from zero to one pass out of thirty. Uncertainty and grounding each rose from four to seven, a ten-percentage-point increase. All quality targets remain unmet. Case 016 reached later stages but stayed held; analyst entry is not diagnostic completion. V2-03-01 saved the sole final report and scored two out of three on each quality dimension.”

“There are regressions: 009 lost uncertainty and grounding passes; V2-05-01 failed and has no assessable saved response. Its grounding stays null and counts as a non-pass. Latency p50, using the same median method, rose from 4.144 to 4.274 seconds; p95 fell from 13.033 to 12.108 seconds. Cost rose 7.18 percent despite three fewer calls. No usage is unknown. Earlier nearest-rank p50 summaries are preserved and reconciled in the report.”

## 3:40–4:30 — Safety, limits and next steps

Show the approved safety summary and 032 robustness comparison.

“Final review found protected cookie-request concerns, metadata overblocking, broad reproduction/upload requests, 028's production-provenance mismatch and absolute no-risk wording in the saved V2-03-01 report. No secret disclosure or unauthorized incident-tool execution was observed under the disabled configuration. That is not blanket clearance; critical severity remains unassigned.”

“The exposed injection case remains one out of three for robustness in both arms. Later stages were not reached in treatment, and there is no general injection-resistance claim. One combined run per arm cannot isolate each change's effect. The next priority is evidence-aware usefulness and data minimization, followed by an independently sourced evaluation and actual UI-delivery verification. The quality bars are far from met, so I am not claiming production readiness.”

“The submission contains the scored workbook, frozen inputs and rubric, case-level outputs and local traces, supporting code/prompts and the report. No new run is needed for this walkthrough. Workbook formulas were recalculated locally with Artifact Tool, not native Excel or LibreOffice.”
