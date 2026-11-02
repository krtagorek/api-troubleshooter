# Frozen assignment set and existing-supervisor extension verification

**Status:** frozen reviewed set assignment-30-v1, **30 unique cases and five artificial allowance slots; zero outstanding substantive dataset/applicability decisions**. Reviewer approvals are User in this conversation, exact times unset. Inputs/references/rubric/applicability/provenance/scenarios are bound in [manifest.json](../data/week4/datasets/assignment-30-v1/manifest.json), SHA-256 `c105de5632777304e876176f74e5dcf1a0ae0442058ff28e37edbfbb9cb75b32`. Dataset freeze is not golden-result readiness or diagnostic completion.

Approved W4-DRAFT-031-v1 replaces held 030; approved W4-DRAFT-032-v1 replaces V2-01-03 one-for-one. Originals, reviews and 030's HOLD remain preserved outside selection. 028 is an approved source-derived third-party controlled mock-upstream reproduction, authorship unknown, not production traffic; no additional generated charge. Its difficult/failure scenario denotes a reported application problem, not our observed agent failure. 022's archive condition is fulfilled; historical decision unchanged. All eleven scenario completions are approved. No semantic scores or final development/reserved splits were invented.

Approved mix **12/15/2/1** (happy/edge/difficult/adversarial) versus approximate guide **15/9/4/2**, deviation **−3/+6/−2/−1**. Source cases are exposed and family-correlated; no independent-holdout claim. The frozen reference scope, not later source resolutions, governs human grading.

## Implementation boundary

Only the existing Week 4 path is extended. contracts.py verifies frozen file/external bindings, distinct IDs/counts and separated inference/evaluator records. live_config.py permits a manifest-specific bounded configuration with original or existing V2 workflow; old $0.25 and case-016 configurations stay unchanged. live_provider.py and accounting.py select strict provider safety from the full-context accounting mode, so both arms use identical byte limits, tier/usage validation, output cap and reservation rules. No inherited prompts/graphs/grounding/redaction/authorization/publication file changes.

smoke.py extends its existing run_smoke supervisor to a sequential manifest. Before each case, actual preceding sealed journals are reconciled against aggregate limits. Case resource-admission records are explicitly not provider-call records; there is no second usage ledger. Actual calls/usage remain in the existing per-case Journal. Local roots/node/model spans reflect actual boundaries; skipped model stages get no fabricated calls. Ordinary fully metered failures remain in rows and allow safe continuation; security/resource/accounting uncertainty stops dispatch, retaining unattempted rows and reservations. A corrupt journal retains an unknown liability bound with attempted counts unknown, not invented five-call receipts. Process timeout/cleanup, retries=0, provider integration and local tracing are reused.

live_cli.py adds run-manifest and reuses the existing bound authorization check; dataset review cannot authorize paid execution. Manifest/input/config/code/dependency changes reject the proposal. Authorization is arm-specific; no later improved run is implied. No new runner file, agent, remote transport, policy or approval system was added.

## Focused offline tests

**28 tests passed** in the [saved log](../reports/week4/assignment-freeze-1/tests.txt). Command (inspected first; no original databases/services):

```text
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-locked/bin/python -m unittest tests.week4.test_case_manifest tests.week4.test_supervised_v2_provider tests.week4.test_supervised_selection_pair -v
```

Checks cover all 30 input schemas, unchanged sanitization, initialization/catalog binding; 120 nested evaluator-field rejections; input/reference/rubric/applicability/provenance/scenario tampering; duplicate IDs; original baseline versus explicit V2 common configuration; initial request/input parity; actual shared request boundaries; model spans versus actual SDK mock requests; known parsing failure retained then safe continuation; usage loss/interrupt/timeout retention and verified cleanup; corrupted journal without invented attempts; money/call exhaustion before dispatch; unsupported model/tier and old-default preservation; unauthorized or changed plans rejected. Existing provider and selection-advisory regressions pass.

Only SDK MockTransport/fake metering is used. New test output is not spending or model-quality evidence. No private key/presence check, authenticated discovery, paid model, incident command/service, install or trace export occurred. Both graph arms use real inherited factories via existing injection. No evaluator answers produce model responses.

## Actual scripted routes and limitations

Baseline: **30 retained, 63 model calls, 29 held, one failed; three analyst entries**. V2+selection advisory control: **30 retained, 63 calls, 29 held, one failed; four analyst entries**. Every case has verified child cleanup. Initial classifier requests are identical across all pairs; shared actual investigator boundaries differ only by the existing scoped advisory. Different/failed boundaries are recorded, not invented to force matching call counts.

**Known preserved failure: V2-05-01.** Numeric received=1770000000 remains intact in the input. The inherited sanitizer redacts its catalog observation string as [REDACTED]. Baseline investigator selection then fails binding (ValueError); the existing selection-advisory wrapper fails earlier (AgentOutputError) in the treatment. This is a mechanics limitation, not hidden input mutation, a passed case or semantic accuracy evidence. Both failures remain visible; subsequent safe cases still run. No source evidence, inherited redaction or grounding check was weakened. Fixing this existing interaction is outside the manifest-extension scope; it may inform a future separately scoped targeted change, without claiming an observed model-quality gain here.

Additional analyst entry for 016 is scripted boundary coverage with an inconclusive mock, not a diagnosis, appropriate clarification, verified repair or golden readiness. Actual agent failure clusters must be derived from a real authorized baseline and human grading; 028's source failure label and these mock routes do not substitute for them. **Semantic accuracy and actual cost remain null.**

| Selected case | Baseline calls / outcome / analyst | V2 control calls / outcome / analyst |
| --- | --- | --- |
| W4-REAL-005 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-006 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-008 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-009 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-011 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-012 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-013 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-014 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-015 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-016 | 2 / held / not entered | 3 / held / entered |
| W4-REAL-017 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-018 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-019 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-020 | 2 / held / not entered | 2 / held / not entered |
| W4-DRAFT-032-v1 | 3 / held / entered | 3 / held / entered |
| V2-03-01 | 3 / held / entered | 3 / held / entered |
| V2-04-01 | 2 / held / not entered | 2 / held / not entered |
| V2-05-01 | 2 / failed / not entered | 1 / failed / not entered |
| V2-15-01 | 3 / held / entered | 3 / held / entered |
| W4-REAL-007 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-021 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-022 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-023 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-024 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-025 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-026 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-027 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-028 | 2 / held / not entered | 2 / held / not entered |
| W4-REAL-029 | 2 / held / not entered | 2 / held / not entered |
| W4-DRAFT-031-v1 | 2 / held / not entered | 2 / held / not entered |

## Unauthorized baseline proposal

[Machine plan](../data/week4/execution-proposals/assignment-baseline-1/plan.json), SHA-256 `dcd2076c86747bc8b57196f0f29b93ecc2e6895f2a49786df609b547e4e1955b`; [readable proposal](week4-assignment-baseline-proposal-1.md). Original graph, gpt-4.1-mini-2025-04-14/default, strict complete request bound, full-context reservations, output 1536, call 20s/case 120s, concurrency one, maximum five calls/case/150 total, zero retries. **$63.223200** conservative ceiling; **$0.36–$0.72** illustrative usage assumptions separately labeled, not guaranteed or authorized spend. Local traces only; incident tools/exports OFF. Pricing/lifecycle sources are linked in the proposal.

Loader preflight passes; paid authorization is rejected as required. Approval identity/time unset; execution_authorized=false and trace_export_authorized=false. Private key and account/model access for the future environment remain unverified. Prior hash-locked installation attestation and current installed-version check are bound; no installation/re-audit was performed. Later code/model/rate/input changes need a new proposal; prior sealed smoke/pair configurations are not silently rebound.

## Preservation and remaining work

All 328 inherited hashes and the existing baseline manifest are checked, never regenerated. All previous sealed artifacts, source inputs/reviews/packets and exclusions are preserved. Active working guides and workbook are updated; their exact prior bytes are archived. Current source changes are limited to six Week 4 adapter/supervision files plus one new focused test module. Preservation receipt records the exact changed-file allowlist and prior sealed-manifest counts.

No substantive review decisions remain for this frozen set. Remaining operational prerequisites are explicit **baseline-only** authorization, private key/account/model availability and final bound preflight. The known V2-05-01 failure is retained as an evaluation outcome, not concealed as compatibility success beyond the input boundary. At least one additional substantive functional change remains needed after actual baseline failure analysis; infrastructure work does not count toward the course's three/four changes. Later improved execution and human grading/report/Loom work remain separately required.
