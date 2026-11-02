# Manifest live guard correction — offline verification

The manifest treatment passed manifest authorization/admission, then entered a legacy single-case guard because selection_policy was enabled. That guard accepts only the single-case proposal versions and rejected the manifest before any provider call. The sealed zero-call attempt remains infrastructure evidence, with no treatment scores or quality result.

The only runtime change is in `evaluation/week4/smoke.py`: the legacy guard now additionally requires `manifest_plan is None`. This variable is populated only after the existing manifest plan/configuration, authorization and case-admission checks succeed. Manifest cases retain those checks; single-case paths retain their existing guard. No model request, evidence policy, grounding, publication, authorization requirement, accounting rule or tracing setting changes. [Exact runtime diff](../reports/week4/manifest-live-guard-fix-1/runtime-diff.patch).

## Verification

**55 tests passed** under an OS network-deny sandbox. [Focused log](../reports/week4/manifest-live-guard-fix-1/focused-tests.log), [full regression log](../reports/week4/manifest-live-guard-fix-1/regression-tests.log).

- The actual `live_cli.main → run_manifest → run_smoke → supervisor → inference_worker` path runs in **live mode**, with a synthetic authorized manifest and synthetic key. Only the provider transport is replaced by the supported SDK MockTransport. The treatment reaches provider dispatch and classifier completion; process cleanup is verified. A deliberately restricted aggregate fixture budget then prevents the next case from dispatching. These are scripted mechanics and fixture receipts, not paid usage or semantic evidence.
- Unauthorized plans, changed approval/code/dataset/configuration bindings, unsupported tier, unfunded budget, exports, baseline/treatment mismatch, incorrect output location, changed frozen case bytes and missing admission remain rejected. An unsupported legacy plan still fails its legacy ceiling check.
- The actual existing VS Code selective loader is tested against a **temporary synthetic .env only**. Interpolation remains disabled; only WEEK4_OPENAI_API_KEY is exported, unrelated provider/tracing settings are excluded, ambient tracing is disabled, and fixture values are absent from output. The project private .env was not opened, printed, copied or hashed. Git metadata confirms it is ignored and untracked.
- Relevant existing controls pass: 30-input/evaluator isolation and baseline/treatment input parity; both mocked manifest arms; ordinary failure retention/continuation; request-size and money/call bounds; usage before parse errors; missing/ambiguous usage reservations; unsupported tiers; interruption/timeout cleanup; V2 provenance/selection controls; reviewed-target and validator regressions.

Reproduce offline with the existing dependencies:

```sh
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-locked/bin/python -m unittest tests.week4.test_manifest_live_guard tests.week4.test_reviewed_targets tests.week4.test_attributed_report_v2 tests.week4.test_supervised_selection_pair tests.week4.test_supervised_v2_provider tests.week4.test_case_manifest -v
```

The tests use temporary project-local directories and synthetic authorization, never the approved live output locations or private credentials. No new runner, policy version or approval mechanism was added.

## Preservation and remaining prerequisites

[Preservation checks](../reports/week4/manifest-live-guard-fix-1/preservation-checks.json): **328/328 inherited files**, the unchanged baseline manifest, all **2,278 protected start files**, and **151 prior sealed groups / 3,216 indexed artifacts** pass. Frozen dataset, workbook, reviews, sealed baseline, proposal 1, its authorization copy and zero-call attempt are unchanged. Treatment scores remain blank; no paid calls, authenticated discovery or exports occurred.

[Corrected proposal 2](week4-assignment-final-treatment-proposal-2.md) passes offline configuration/dependency/binding checks and rejects execution authorization. Proposal 1 now correctly fails its stale runtime binding; it was not rebound. The existing VS Code treatment task still names proposal 1 and the already-existing zero-call output directory: **do not relaunch that task**. A future explicitly approved run must use a separately authorized copy of proposal 2 and its fresh output location through the existing path. This task does not modify launch authorization or execute it.

The existing V2-05-01 investigator catalog failure remains retained, without repair. Other live selection/output failures remain possible; current account access was not checked. The 88 installed pins and Python version match the lock, and the prior hash-locked installation receipt is intact; no new installation or installed-file re-audit was performed. Human treatment grading and verified UI delivery remain outstanding after a future authorized run.
