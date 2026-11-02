# Week 4: bounded plan for three reviewed improvements

**Plan only. No implementation or improvement execution is authorized by this document.** The original baseline, frozen assignment-30-v1 inputs and approved rubric remain the comparison artifacts. See the [final baseline scorecard](week4-baseline-final-scorecard.md).

## Scope and measured starting point

There are three functional targets, not one improvement per policy version. Existing attributed-report V2 and selection-dependency work together serve target 1. Targets 2 and 3 address separate observed response/publication and resolution-wording failures. Accounting, adapters, tracing and dataset management do not count as substantive diagnostic improvements.

The reviewed baseline has 27 holds before analyst entry (26 unsupported-pattern reasons; one missing-comparison-peer reason), two later safety/publication holds, and one resolution-output failure. All 30 correctness scores are below the pass threshold; uncertainty and grounding each have four threshold passes. A necessary safety hold is not itself proof that readiness should be relaxed.

Keep all changes outside the 328 inherited files. Retain original factories, graph topology, strict provider schema, redaction, grounding, authorization, publication decisions, retries=0 and at most five model calls/case. No case-ID rules, evaluator references, expected answers, later resolutions, new mechanism extraction, automatic evidence selection, new runner, ledger or approval system. Frozen numeric/string/provenance discrepancies are not repaired in this work.

## 1. Evidence-aware analysis/clarification handoff

**Observed scope: 27 cases; potential analyst expansion is narrower.** Reuse the existing V2 ASCII-header rule and `attributed_selection_v1` dependency advisory. It can qualify 016 only when the model actually selects valid original anchors and reporter-association dependencies; it does not authenticate request correlation or make every report eligible for analysis. For the other unsupported-pattern cases, improve the existing investigator's case-specific missing-evidence questions using only inference material and the actual readiness/coverage reason. Do not manufacture a diagnosis to avoid a hold.

Proposed boundary: existing Week 4 investigator/provider advisory and explicit V2 workflow composition. Preserve the baseline branch and inherited readiness. Keep selected facts, unselected available facts, source-attribution limitations and genuinely unavailable facts distinguishable. A missing dependency must identify its actual reference/role where resolvable; a model assertion of completeness cannot supply it. No new paid stage or automatic addition is introduced. Existing inherited augmentation remains characterized, including its redaction restriction.

Acceptance tests after separately authorized implementation:

- **016 positive:** selected emoji, exact ASCII exception and all valid original reporter-association anchors qualify analysis under existing V2, with definitive_confirmation=false. Compare baseline on identical bytes. No confirmed repair/outage/correlation claims.
- **016 recorded live selection:** still holds because required attribution dependencies are absent; advisory explains missing references without selecting them. Only intended investigator/advisory request fields differ.
- **Negative controls:** fabricated quote, missing bridge, stale/cross-case/evaluator reference, unrelated attempt, contradictory/ambiguous evidence, instruction-bearing source and missing comparison peer remain held. Source hashes bind excerpts; they do not establish truth.
- **006/007/011/012 clarification regressions:** retain historical media-type comparison, binding signature, missing-header attribution and parse-error scope. Ask relevant sanitized facts without assuming raw credentials, a corrected payload or a confirmed cause. These cases do not gain readiness merely because useful prose exists.
- **008/020/V2-04-01 ambiguity:** preserve repository separation, separate transfers/attempts and GET versus logged delete. Request association/operation clarification rather than assert one cause.
- **V2-05-01:** preserve the numeric input and original redaction. Its omitted comparison must remain visible; do not repair binding by weakening validation or reintroducing a redacted observation. Any need for a representation change is a separately reported blocker.

## 2. Safe useful partial reporting

**Observed scope: two later holds, plus request-wording regressions elsewhere.** Improve request wording and the already-existing user-facing clarification field. Use precise sanitized nonsecret issuer/audience/expiry metadata and verifier decisions; never request raw tokens, full Authorization values or cookies. Sanitized nonsecret claims are not reusable credentials. Broad logs/body/header requests must explicitly require sanitization/minimization. Write reproductions must specify existing-state checks and controlled nonproduction reproduction before any repeat operation.

Proposed boundary: Week 4 scoped model-request instructions and, only if necessary, a wrapper of the existing request_user_input node within the established V2 composition. Preserve node/edge topology. Keep the inherited publication decision and final_report withheld whenever it denies publication. Use pending_user_questions for bounded safe, case-specific clarification rather than converting an unsafe/internal diagnosis into an authorized report. Any observation mentioned in that clarification must resolve to the selected snapshot and retain its uncertainty. Do not silently remove safety markers to make a report eligible.

Acceptance tests:

- **032 and V2-03-01:** with valid selected evidence and NOT_TESTED validation, produce a saved case-specific safe question about issuer comparison or workload/resource attributes. Do not credit internal analysis as delivered output. Keep final_report=null whenever the unchanged publication decision holds. Human review, not a route flag, determines usefulness.
- **008 unsafe request:** a raw authentication-token/Authorization-header solicitation remains blocked. Never restore that text to saved clarification; keep the prevention finding visible.
- **Sanitized metadata controls:** distinguish actual raw credential requests from sanitized nonsecret claims. Test actual policy transformations rather than assume the latter always passes current heuristics. If safe wording cannot be achieved without changing inherited safety/publication logic, report that blocker instead of bypassing it.
- **005/013/026/031 and other recorded raw-data requests:** explicit exclusion of secret values/private payloads; scope to minimal sanitized headers/structure. No supposed safety pass from withholding alone.
- **014/018:** no blind repeated POST/write. Require state/duplicate checks and a safe controlled reproduction plan; never execute it.
- **032 R1–R4:** preserve resistance to injected false-resolution/validation instructions and action boundaries; improve R3 useful scoped content. Never count analyst entry as robustness or diagnostic success. No claim of general robustness from one exposed development case.

## 3. Read-only resolution wording compatibility

**Observed scope: V2-15-01.** Add a scoped Week 4 resolution-request advisory. Ask for read-only imperative steps such as inspect/compare/review, with uncertain mechanism descriptions outside action steps. Require the model to avoid all existing prohibited verbs in every action list checked by the inherited resolution/publication validators, including descriptive subordinate clauses. Do not strip or rewrite a received response to force validation, retry the call, or weaken the regex/action boundary.

Acceptance tests:

- The exact recorded rejected response still raises `AgentOutputError`; the historical failure is not erased. Its detailed message remains identified as a deterministic post-run reproduction, not an original captured message.
- A mocked strict-schema response with bounded read-only comparison steps and selected evidence references passes existing resolution validation. A tentative diagnosis still cannot receive a remediation plan.
- Actual deploy/restart/disable/delete/modify/update/reconfigure/rotate/change instructions remain rejected, as do forged/unselected evidence IDs and unsupported execution/success claims.
- Request-level parity: only the scoped resolution advisory changes; classifier/investigator inputs, provider settings and input bytes do not change because of target 3. No fallback, second model call or additional retry is introduced.
- No claim that prompt wording guarantees future provider compliance. A new invalid response remains a retained failed case with its actual usage.

## Implementation limits and verification sequence

Expected existing Week 4 touch points: `attributed_selection_v1.py`, `attributed_report_v2/workflow.py`, and existing `smoke.py`/configuration wiring only where explicit opt-in composition requires it. Put a scoped resolution proxy in the existing Week 4 composition layer rather than copying an agent. Extend existing tests under `tests/week4`; do not edit inherited `agents/`, `graph/`, `tools/`, models, prompts or UI. Do not create another readiness mechanism or framework.

1. Implement one target at a time only after explicit implementation authorization. Characterize request diffs and baseline topology/behavior before each edit. If existing interfaces require inherited changes or wider provenance rules, stop and report the specific blocker.
2. Run network-blocked mocked checks through the existing supervised provider path: focused controls above, `test_attributed_report_v2`, `test_supervised_selection_pair`, `test_supervised_v2_provider`, and `test_case_manifest`. Preserve failed-case continuation, uncertain reservations, timeout cleanup and no trace-triggered repeat inference. Scripted request/branch coverage is not model quality.
3. Reconcile actual executed boundaries/calls and verify labels remain outside inference. Check frozen input/reference/rubric hashes, all 328 inherited files, original baseline artifacts, and baseline/treatment input-byte parity. Report behavior/request differences rather than count architecture work as a feature.
4. Prepare one separately bound, unauthorized final treatment proposal for the existing 30-case manifest path. Recheck model lifecycle, pricing, dependencies and code bindings before requesting execution approval. The existing runner supports the full manifest; do not add subset-runner infrastructure for intermediate measurements.

## Comparison and results presentation

Reuse the sealed baseline; do not rerun it. The simplest paid comparison, if separately authorized, is one final cumulative treatment run on the same 30 frozen inputs, same model snapshot/default tier and limits: at most 150 additional calls, concurrency 1, zero retries, incident tools/exports OFF. No such spending is authorized now. Current recorded rates/reservations are historical assumptions until reverified for a future bound proposal.

Use offline request/branch ablations to characterize each target. Compare final versus baseline case-level rubric scores, missingness, safety observations, outcome groups, latency and receipt-priced cost. Show each of the three functional targets' affected examples and observed before/after behavior, acknowledging overlap and joint effects. Do not claim isolated per-change semantic causality from the final combined run or infer semantics from scripted coverage. If the course reviewer requires paid intermediate semantic arms, report the need and seek separate scope/budget authorization through the existing full-manifest path; do not quietly add runs or infrastructure.

Deliver the updated spreadsheet, a compact baseline/final metric table with all assigned denominators, the three observed failure clusters, representative successes/regressions, retained holds/errors, total/mean cost and usage uncertainty, and a Loom walkthrough. Disclose all development exposure, family overlap, five artificial slots, approximate-mix deviation and unverified UI delivery. No implementation, new policy version or execution is performed by preparing this plan.
