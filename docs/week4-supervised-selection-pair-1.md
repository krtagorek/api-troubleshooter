# Supervised V2 selection-dependency pair — proposal 1

**Prepared, not executed.** Both arm plans have execution_authorized=false, trace_export_authorized=false, and unset approval identity/time/binding. No paid calls, authenticated discovery, exports, installations, services, or commits occurred. Offline model/provider transport checks are scripted test data, not spending or quality evidence.

The [machine-readable paired proposal](../data/week4/smoke-proposals/real-016-v2-selection-pair-1/plan.json) binds two fresh arms, the unchanged W4-REAL-016 V2-1 input, original provenance archive, current code/lock inventory, verified pricing, and configurations. Its SHA-256 is `c06dbe27004d63ca65acf2cbdaa7442d92eb42ab515963018cac79cbf1c90b24`.

| Arm | Selection policy | Plan SHA-256 |
| --- | --- | --- |
| [Baseline plan](../data/week4/smoke-proposals/real-016-v2-selection-pair-1/baseline-plan.json) | off; existing V2 | `8437eda9b5ab35bd433ca4386002ab493683196776c19e80f5d46e286c150f6e` |
| [Treatment plan](../data/week4/smoke-proposals/real-016-v2-selection-pair-1/treatment-plan.json) | attributed-selection-dependencies-v1 over the same V2 | `c04d4528ae238a57ef7685d3f5f2c536bcc63c88ffbdd67fab1b696e6c289628` |

The only configuration difference between arms is selection_policy. Both use gpt-4.1-mini-2025-04-14, default tier, concurrency one, zero SDK/workflow retries, no fallback, five calls maximum per arm, 1,536 maximum completion tokens per call, 65,536 complete-request bytes, a 120-second case deadline and 20-second HTTP phase timeout. External tracing and incident tools remain OFF. Maximum total calls: ten.

## Integration

The existing path remains **live_cli → run_smoke → supervise → inference_worker → LiveModel + Journal**. No second runner, accounting ledger, or provenance contract was introduced.

- LiveConfig gains an explicit selection_policy, defaulting to off. Unknown policies and selection treatment without V2 reject; older plan versions cannot enable treatment.
- The existing worker substitutes only the log-investigator factory when the treatment flag is present. All other inherited factories, V2 branch, scoped analyst advisory, prompts, provider request schema/options and policies are reused.
- The original selection-dependency v1 implementation is unchanged. It selects no evidence and does not force completeness. In its narrow attributed scope, it retains only explicitly selected IDs and reports missing dependencies/omitted telemetry. This case's baseline path also adds no unselected facts; that is verified offline. Baseline preserves existing behavior elsewhere.
- Both arms record local, deterministic selection measurements after the investigator. Measurements cannot change state, routing, readiness or grounding.
- Each arm retains its existing durable journal, reservation-before-dispatch, usage reconciliation, unknown-charge retention, process timeout and cleanup. Request-size checks include system/schema/advisory and growing state on every actual call.
- New paired-arm plan validation binds the manifest, same input/source/configuration identity, role, and fixed create-only output directory. The treatment requires a completed, sealed, matching baseline with verified cleanup, no errors, no uncertain charges and no limit violations. An unsafe baseline stops the comparison rather than allowing further paid dispatch.
- Atomic output-directory creation prevents repeating an arm. Treatment cannot overlap baseline because baseline's terminal sealed artifacts are required first. Two bounded $2.25 journals give a combined $4.50 cap without another journal. Do not delete claimed output directories to retry.

Changed existing Week 4 files: live_config.py, live_cli.py and smoke.py. New modules: paired_selection_plan_v1.py and selection_metrics_v1.py. No inherited file, original V1/V2 readiness implementation, selection v1 implementation, reviewed asset, or prior sealed result changed.

## Verified pricing and conservative combined budget

Official public documentation was fetched on **2026-10-29**. The snapshot remains listed, with Chat Completions/structured-output support, a 1,047,576-token context and 32,768-token model output ceiling. Listed USD rates per million text tokens remain **$0.40 input, $0.10 cached input, $1.60 output**. [Official model/pricing documentation](https://developers.openai.com/api/docs/models/gpt-4.1-mini).

The model is deprecated, with shutdown scheduled for January 14, 2027. Both executable arm plans enforce a last UTC execution date of January 13, 2027. There is no automatic replacement. [Official lifecycle notice](https://developers.openai.com/api/docs/deprecations).

| Reservation | USD |
| --- | ---: |
| Full per call: (1,047,576 × 0.40 + 1,536 × 1.60) / 1,000,000 | 0.421488 |
| Five calls per arm | 2.107440 |
| Ten calls across both arms | **4.214880** |
| Proposed cap per arm | 2.250000 |
| Proposed combined cap | **4.500000** |
| Combined headroom | 0.285120 |

No cache savings are assumed. The entire documented context is reserved as a conservative input bound, **not an exact token count or character estimate**. Reported cached usage may reduce reconciled cost only after valid receipts; missing or ambiguous usage retains reservations. Provider-priced estimates are not independent invoice attestation. The old $0.25 default and all older plan bytes remain intact.

## Exact request differences

For identical prior validated outputs, the investigator user JSON gains exactly **selection_dependency_advisory**. The existing system message, every existing payload value, evidence catalog/snapshot, response schema, enums, model, tier and provider settings remain unchanged. The [bound exact diff](../data/week4/smoke-proposals/real-016-v2-selection-pair-1/investigator-example-diff.json) and [baseline](../data/week4/smoke-proposals/real-016-v2-selection-pair-1/baseline-investigator-example.json)/[treatment](../data/week4/smoke-proposals/real-016-v2-selection-pair-1/treatment-investigator-example.json) provider-normalized examples show 17,112 → 22,025 bytes (+4,913), below the existing cap.

Those exact examples condition on the prior sealed classifier output; they are not predictions of the next classifier response. The actual supervised MockTransport captures independently verify the difference in [recorded-selection controls](../reports/week4/supervised-selection-pair-verification-1/recorded/) and [valid-dependency controls](../reports/week4/supervised-selection-pair-verification-1/dependencies/). Classifier requests match byte-equivalent JSON content, investigator requests differ only by the advisory, and downstream analyst requests match when scripted selections/outputs match.

Two independent live arms can produce different classifier or investigator outputs despite identical requests and temperature zero. Such downstream request differences must be recorded as consequences, not hidden or asserted to be advisory-only differences. The treatment can also add explicit local missing-dependency gaps; no missing evidence is synthesized. There is no promise of identical future routes, schemas conditioned on selection, token use, or latency. Original excerpts remain unverified reporter attribution, not authenticated correlation.

## Offline verification

**51 focused tests passed** under OS network denial, covering existing supervised provider/budget/error/timeout behavior, old $0.25 defaults, new authorization and paired-plan checks, selection v1, and V2 provenance/negative controls. Mock SDK construction only permits HTTPX MockTransport and an explicit offline fixture key; LangSmith/export and socket access are blocked.

| Scripted selection, identical across arms | Baseline | Treatment |
| --- | --- | --- |
| Recorded live handles E41/E43/E47/E01 | Required coverage 2/39; two calls; analyst not reached; held | Same coverage/calls/hold; explicit missing-dependency gap |
| Explicit required attribution selection | Required coverage 39/39; three calls; analyst entered; held with inconclusive diagnosis | Same coverage/calls/outcome |

Valid-reference binding passes in these controls; it does not confer sufficient evidence. Definitive confirmation remains false. Neither arm yields diagnostic success. Synthetic usage is 11 input + 7 output tokens per mocked call and is reconciled as test accounting only. Mock timings include real process overhead but do not measure live provider latency. Actual live tokens/cost/latency and semantic accuracy remain null.

The tests also reject tampered combined ceilings/configs/inputs, unsupported policies, a treatment borrowed by an older plan, wrong-arm approval bindings, missing authorization, repeated outputs, and treatment before safe baseline reconciliation. Existing regressions cover oversized complete requests, reservation exhaustion, missing/ambiguous usage, unexpected tiers, provider errors, zero retry and timeout cleanup.

[Verification and preservation results](../reports/week4/supervised-selection-pair-verification-1/result.json): all **328 inherited files** match the original baseline manifest; all existing inputs/reviews/proposals/sealed results and 996 other preexisting files match the before snapshot. Exactly the three authorized Week 4 runtime files changed. The baseline manifest was not regenerated. Current source hashes differ from older plans, which therefore cannot be silently replayed or rebound.

## Planned measurements and human review

The [bound measurement specification](../data/week4/smoke-proposals/real-016-v2-selection-pair-1/planned-measurements.json) defines:

| Measurement | Record |
| --- | --- |
| Required-reference coverage | Selected required references / full 39-reference requirement for this snapshot, with exact missing handles/paths and issues |
| Valid selection | Actual snapshot-bound catalog references/scalars; validity is separate from coverage and qualification |
| Analyst entry and route | Actual stage start/completion and ordered stage journal events; skipped stages have no fabricated calls |
| Terminal outcome | Held/completed/failure/timeout/interruption, errors and cleanup; blocked/unattempted treatment retained in the two-arm denominator |
| Tokens | Provider-received input/output/cache/reasoning counts for actual attempts; unknown stays null |
| Cost | Durable reconciled usage at bound rates, plus retained uncertain reservations; no hidden retries |
| Latency | Existing case boundary before process spawn through reaping, terminal fsync/reconciliation; excludes report/export. Model latency sums ended attempted calls once, never root + node + model spans |
| Semantic quality | Genuine human review of evidence grounding, uncertainty and appropriate clarification; worksheet remains blank |

Analyst entry is **not** diagnostic completion or success. Structural/selection coverage is not semantic quality. One development case cannot establish isolated causality or broad quality improvement. The historical single live smoke remains historical evidence, not a fresh paired baseline.

## Remaining prerequisites

There is no identified integration blocker after offline verification. Paid execution remains blocked by **new explicit approval of this paired proposal and both exact arm bindings**. The earlier single-run approval was consumed and grants no authority here.

Before any future authorized execution, recheck source/input/configuration hashes, model lifecycle/pricing and the dedicated private WEEK4_OPENAI_API_KEY in the actual execution environment. No key value or presence was inspected during this task. No authenticated account discovery occurred; the prior successful case does not guarantee future account permissions, quota, rate limits, receipts or concrete schema acceptance.

The hash-locked Week 4 environment is already installed; all 88 versions and Python 3.11.16 match. This proposal binds the earlier successful archive-verification receipt. No dependency installation occurred. Any changed environment/code/configuration requires a fresh proposal rather than editing these sealed files.

When separately authorized, use the **existing live_cli run** entry for each authorized arm copy, baseline first, with each fixed bound output path. There is no paired runner. Arm authorization must match its immutable identity in verification.json, and trace_export_authorized must remain false. Do not run an old launch helper or reuse the spent one-case plan.

Reproduce offline checks:

```sh
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-locked/bin/python -m unittest tests.week4.test_supervised_selection_pair tests.week4.test_supervised_v2_provider tests.week4.test_smoke_proposal3 tests.week4.test_attributed_selection_v1 tests.week4.test_attributed_report_v2 -v
```

The data-only preparation helper is scripts/week4_prepare_selection_pair.py. It is create-once and intentionally refuses the sealed proposal directory; never delete or overwrite historical outputs to rerun it.
