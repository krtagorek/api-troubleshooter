# Final submission checklist

Chosen route: **own use case / Week 3 agent, spreadsheet**. External LangSmith evidence and an executed customer-support notebook are not requirements of this chosen route. No LLM judge was used. This checklist does not authorize any execution or publishing.

## Prepared locally

- [x] [Evaluation report](week4-evaluation-report.md): use case, evaluation one-liner, five metrics, approved rubric/pass bars, failure analysis, three functional changes, baseline/final deltas and remaining limitations.
- [x] [Completed workbook](../outputs/week4-completion-30/week4-evaluation.xlsx): 30 labeled cases and both arms' outputs/references, scores, costs/latency and approved final safety/032 judgments. Long content is labeled as a preview, with complete saved artifacts referenced.
- [x] [Frozen assignment-30-v1](../data/week4/datasets/assignment-30-v1/manifest.json): same inputs, expectations, applicability, rubric, scenario and provenance bindings in both arms; no refreeze or inferred labels.
- [x] [Scored case records](../reports/week4/submission-finalization-1/scored-cases.json) and [CSV](../reports/week4/submission-finalization-1/scored-cases.csv), local baseline/final results, traces and receipts; failures/holds retained.
- [x] Supporting original prompts, Week 4 advisories, evaluator/supervisor code and existing offline verification evidence included in the local bundle.
- [x] Final judgments attributed to User in this conversation, exact review time unknown. Quality numbers preserved; grounding null failures retained in assigned denominators; critical severity unassigned, no blanket safety clearance.
- [x] Dataset artificial allowance, family/development exposure, scenario deviation, UI-delivery limit, untested targeted live wording path, unmet quality targets and inability to isolate per-change effects disclosed.
- [x] Workbook formulas recalculated with Artifact Tool, saved values/features and local artifact links checked. **Native Excel/LibreOffice recalculation not performed.** Do not claim otherwise.
- [x] Original 328 files, frozen inputs and sealed baseline/final/earlier attempts preserved. No new experiment, API call, service, installation, code repair, commit or publication performed.
- [x] [Local submission handoff](../outputs/week4-submission-1/README.md) prepared with an explicit file allowlist and content checks. No .env files, credentials, environments, Git metadata or VS Code launch tasks included.

## User actions still required

1. **Record the short Loom** using [the script](week4-loom-script.md). Show saved evidence, not a fresh run. Keep the open .env tab, secrets and unrelated private windows out of frame.
2. **Add the actual Loom URL** to the submission portal or accompanying message after recording. No URL is invented or prefilled here. Review the recording for unintended private content before submitting it.
3. **Upload the bundle** or the workbook/report/supporting materials separately, according to the course portal's accepted formats. If Markdown is not accepted, paste the completed report into the required document format without changing the findings. The bundle preserves project-relative paths; extract it before opening local references.
4. **Confirm the uploaded attachments open** and the Loom link is accessible to the grader. Check the portal's deadline and file-size/format rules; those portal-specific details were not provided or verified.

An optional native spreadsheet opening/recalculation check may be performed privately; it was not performed by this task and is not presented as an additional course requirement. If performed, report the application and actual result. No additional semantic review or paid experiment is required to submit the honest limitations above; critical severity remains explicitly unassigned as approved.
