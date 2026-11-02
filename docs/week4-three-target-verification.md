# Three reviewed Week 4 targets — implementation and offline verification

Implemented as an explicit opt-in of the existing V2 composition and supervised manifest path. **No paid calls, exports or baseline rerun.** Frozen data, approved grading and the sealed live baseline remain unchanged.

## Request and behavior changes

| Target | Exact boundary change | Preserved boundaries |
| --- | --- | --- |
| Evidence-aware handoff | `reviewed_targets=true` requires manifest budget profile + V2 + existing selection advisory. Investigator system message appends HANDOFF_ADVISORY after WEEK4_REVIEWED_ADVISORY; the existing selection_dependency_advisory user-payload addition remains narrow to actual groups/issues. Final evidence is restricted to explicitly returned handles; inherited extra peers are filtered before downstream use. | No new mechanism, no automatically selected downstream evidence, no source prose extraction, no modified baseline factory or readiness rules. Supplied/unselected inventory does not confer sufficiency. |
| Safe partial content | Analyst appends SAFE_METADATA system guidance; investigator/resolution include the same metadata/reproduction restrictions. The existing request_user_input node is wrapped in the copied V2 definition; inherited hold/publication decision runs first. Saved questions preserve safety markers, require minimal sanitized data, distinguish unselected dependencies from not-supplied typed fields, mention selected comparison roles/references and prohibit blind repeat writes. | final_report and stop reason remain inherited; no withheld diagnosis is republished. Questions are not asserted to reach a UI. No case-ID instructions or evaluator content. |
| Resolution wording | Only the resolution system message receives RESOLUTION_ADVISORY plus metadata restrictions; the fixed-state user payload is unchanged. Read-only action lists must avoid the unchanged forbidden words even in descriptive clauses. | Same schema/action/reference validators. No response rewriting, extra call, fallback or retry. Exact historical bad response still rejected. |

The original inherited system text remains the prefix. Classifier and validator model messages are unchanged by the new proxy. The existing AnalystAdvisory still supplies V2-specific readiness metadata only where its actual narrow rule qualifies. Full literal request examples are in [request-differences.json](../reports/week4/three-target-offline-1/request-differences.json); the authoritative instruction constants are in evaluation/week4/attributed_report_v2/workflow.py.

### Selection versus absence

clarification_context records selected references, available_but_unselected_dependencies, other_available_unselected_references (not asserted required), dependency issues, not_supplied_fields and existing readiness reason. All selected references must resolve to the current incident snapshot. A null response_body is labeled not supplied, not a captured null exchange; empty typed logs do not erase attributed excerpts in other fields. Unselected inventory is not silently collected or marked unavailable. Source attribution remains user/reporter supplied and not independently authenticated; definitive_confirmation stays false.

### Saved content versus actual delivery

The actual evaluation contract is the existing case result output: output.pending_user_questions and output.final_report, with local output/trace artifacts. run-manifest prints a batch accounting/status summary, not those narratives. The inherited frontend renders a persisted report (frontend/src/pages/incidents.tsx:42); this task ran no UI, API or worker service. New context explicitly labels saved clarification and UI delivery unverified. No UI-delivery or publication-success claim is made.

## Focused controls and regressions

**50 tests passed** on final code under `/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)'`, using the existing locked environment. No dependency installation. Exact log: [tests-final.txt](../reports/week4/three-target-offline-1/tests-final.txt).

- Valid selected original anchors qualify the existing V2 rule with definitive=false; recorded 016 live selection still holds and reports omitted dependencies.
- Fabricated quotations, missing anchors/peers, stale/cross-case/evaluator references, unrelated attempts, unsupported association, ambiguity/conflicts and instruction-bearing source retain rejection/holds through the existing V2 tests.
- 006/007/011/012 and 008/020/V2-04-01 remain held under unchanged nonqualifying evidence; clarification is reference-specific and does not invent a cause. Explicit-selection control proves inherited additions do not escape into treatment evidence.
- Saved 032 and V2-03-01 later-hold states retain diagnostic_output_safety_review_required, final_report=null and safety markers, while gaining selected issuer/attribute comparison questions. This is a saved-state control, not a new semantically successful trajectory.
- Raw token/header solicitation stays blocked. Sanitized nonsecret issuer metadata is tested separately. 014/018 saved-state questions include existing-state/duplicate checks and approval in controlled nonproduction; no incident request is executed.
- The exact recorded V2-15-01 response still raises AgentOutputError. A separately scripted positive read-only response passes existing validation; all prohibited action verbs, remediation for tentative diagnosis, and forged/unselected references remain rejected. This characterizes compatibility, not future model compliance.
- Original graph topology and baseline-off request behavior, strict provider request size, budget/calls, usage-before-parse receipts, missing usage, provider/tier errors, timeout cleanup, uncertain reservations, safe failure continuation and no unauthorized dispatch pass relevant regressions.
- Existing test_case_manifest previously wrote a paired mock summary into the sealed freeze report; its write now targets its temporary test directory. This is a test-artifact correction, not application behavior or a historical-result edit.

Command (no live calls):

```sh
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-locked/bin/python -m unittest tests.week4.test_reviewed_targets tests.week4.test_attributed_report_v2 tests.week4.test_supervised_selection_pair tests.week4.test_supervised_v2_provider tests.week4.test_case_manifest -v
```

## Fresh 30-case treatment mechanics

Final immutable result directory: [treatment-mechanics-2](../reports/week4/three-target-offline-1/treatment-mechanics-2/). The earlier development run remains separate. Both use the unchanged v2_mechanics/common inconclusive mock policy. Only supported SDK MockTransport with the fixture key is permitted; sockets are OS-blocked and LangSmith client construction is blocked. No live transport or private credential is used.

**30 assigned/attempted, zero unattempted; 63 actual mock provider calls; 29 held and one failed.** 25 held before analyst entry, four held after an inconclusive analyst, and V2-05-01 failed in the investigator before that model boundary (one classifier call). No resolution/validator calls occurred in this 30-case common-policy run; do not fabricate them from the separate controls. All 30 process cleanups were verified; model-span count equals actual attempts, trace export not requested, and actual test usage receipts reconcile without double counting. Mock usage/cost is test data; real treatment spending and quality are not measured.

| Case | Actual stages (C classifier / I investigator / A analyst) | Calls | Outcome / error |
| --- | --- | ---: | --- |
| W4-REAL-005 | C → I | 2 | held |
| W4-REAL-006 | C → I | 2 | held |
| W4-REAL-008 | C → I | 2 | held |
| W4-REAL-009 | C → I | 2 | held |
| W4-REAL-011 | C → I | 2 | held |
| W4-REAL-012 | C → I | 2 | held |
| W4-REAL-013 | C → I | 2 | held |
| W4-REAL-014 | C → I | 2 | held |
| W4-REAL-015 | C → I | 2 | held |
| W4-REAL-016 | C → I → A | 3 | held |
| W4-REAL-017 | C → I | 2 | held |
| W4-REAL-018 | C → I | 2 | held |
| W4-REAL-019 | C → I | 2 | held |
| W4-REAL-020 | C → I | 2 | held |
| W4-DRAFT-032-v1 | C → I → A | 3 | held |
| V2-03-01 | C → I → A | 3 | held |
| V2-04-01 | C → I | 2 | held |
| V2-05-01 | C → I failed | 1 | failed / AgentOutputError |
| V2-15-01 | C → I → A | 3 | held |
| W4-REAL-007 | C → I | 2 | held |
| W4-REAL-021 | C → I | 2 | held |
| W4-REAL-022 | C → I | 2 | held |
| W4-REAL-023 | C → I | 2 | held |
| W4-REAL-024 | C → I | 2 | held |
| W4-REAL-025 | C → I | 2 | held |
| W4-REAL-026 | C → I | 2 | held |
| W4-REAL-027 | C → I | 2 | held |
| W4-REAL-028 | C → I | 2 | held |
| W4-REAL-029 | C → I | 2 | held |
| W4-DRAFT-031-v1 | C → I | 2 | held |

Full per-case readiness reasons, missing dependency inventories, saved questions and errors: [treatment-mechanics-summary-2.json](../reports/week4/three-target-offline-1/treatment-mechanics-summary-2.json). They are actual recorded mechanics, not case scores or diagnostic completion.

Reproduce the mocked manifest through the existing path with a **fresh** project-local output (never rerun over sealed directories):

```python
from pathlib import Path
from unittest.mock import patch
from scripts.week4_real_mock_run import clear_environment
from tests.week4.test_case_manifest import mock_worker
from evaluation.week4 import smoke
clear_environment()
with patch.object(smoke, "inference_worker", new=mock_worker):
    smoke.run_manifest(Path("reports/week4/three-target-offline-1/plan-improved.json"),
        Path("reports/week4/three-target-offline-1/treatment-reproduction-FRESH"),
        mode="offline_test", scenario="v2_mechanics")
```

Run this only under the same OS network-deny sandbox and current locked dependencies. This is a thin invocation of the existing supervisor, not another runner. The bound plan intentionally rejects after future runtime changes.

## Baseline parity and remaining blockers

All 30 input identities and **complete initial classifier provider-request hashes** equal the sealed live baseline, not merely a character estimate. All non-policy provider settings are equal. See [input-request-parity.json](../reports/week4/three-target-offline-1/input-request-parity.json). Later live/mock request streams naturally depend on different model outputs; equality is asserted only at the initial shared boundary and in explicit fixed-state schema controls. No false full-stream parity claim or paid baseline rerun.

**Retained blocker:** V2-05-01 numeric observation redaction makes the explicit investigator catalog/snapshot check reject before transport. The failed row remains and subsequent safe cases continue. No representation repair, validator relaxation or input change is included. Other report-only cases remain outside the existing narrow rule. Raw instruction/credential text cannot make readiness true.

Prompt wording may still produce invalid or unhelpful live outputs. Publication may still hold; safe questions are not diagnostic completion. No UI delivery was verified. The combined future comparison cannot isolate per-change semantic effects. Human grading and actual receipt reconciliation remain necessary after separately authorized execution.

## Preservation and future proposal

Runtime edits are limited to five existing Week 4 files; two test files changed/added. No inherited prompts, graph/routing/readiness/grounding/redaction/authorization/publication validators were edited. The explicit baseline branch remains unchanged in behavior; source bindings for historical launch plans are intentionally not refreshed. All 328 inherited files, frozen assignment-30-v1 assets, reviewed judgments, workbook bytes, original proposals and sealed live baseline/results are preserved. Detailed checks and hashes: [preservation-checks.json](../reports/week4/three-target-offline-1/preservation-checks.json).

[Final-treatment proposal](week4-assignment-final-treatment-proposal-1.md): same 30 frozen cases/rubric, gpt-4.1-mini-2025-04-14/default, max $63.223200, 150 calls, five/case, zero retries, concurrency 1, local tracing, exports/tools OFF. execution_authorized=false, approval fields unset. Model is documented deprecated until 2027-01-14; public rates/lifecycle were refreshed without authenticated discovery. Account/key availability is not established here. No paid command or export was executed.
