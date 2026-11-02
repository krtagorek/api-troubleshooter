# Case 016 V2 smoke proposal 3 — funded, not authorized

This is a preparation-only proposal for one development case, W4-REAL-016. No smoke, workflow, model client, authenticated discovery, incident request, or external trace export was executed. Execution and trace-export authorization are false; approval identity, time, and binding remain null. Human review grades remain blank. Account access is unverified.

The [machine-readable plan](../data/week4/smoke-proposals/real-016-v2-3/plan.json) is PREPARED_FUNDED_NOT_AUTHORIZED. Its SHA-256 is `69e756641250cd698921804cb4dbde0757c6c9e84fa75c04821c29e8b7446acb`; its immutable authorization identity is `a996d40dd93440d58ed722e2eb9999d98d40a9165d676300db6ac5b1aa8322b4`. These hashes describe this proposal, not an approval.

## Model and public documentation

Official documentation checked on 2026-10-29 UTC lists `gpt-4.1-mini-2025-04-14`, Chat Completions and structured-output support, a 1,047,576-token context window, and a 32,768-token maximum output. The proposal retains that existing snapshot and explicit `service_tier=default`; there is no alias, tier, model, or policy fallback. [Official model documentation](https://developers.openai.com/api/docs/models/gpt-4.1-mini).

The model is deprecated, with shutdown scheduled for January 14, 2027; it is not retired on the retrieval date. The documented replacement is gpt-6-luna. No replacement is needed for this near-term compatibility smoke. After this window, prepare a separately checked replacement proposal rather than silently substituting it. Proposal 3 enforces a last UTC execution date of January 13, 2027; a date supplied by a modified plan cannot extend this window. Public listing does not establish this account's access. [Official deprecations](https://developers.openai.com/api/docs/deprecations).

Strict structured outputs remain enabled with the inherited dynamic schema. Public feature compatibility does not prove that every concrete emitted schema will be accepted by the provider. The completion cap includes any non-visible/reasoning tokens once; service tier is explicitly default rather than omitted/auto. [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [Chat Completions parameters](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create).

## Conservative funding and execution limits

Listed text rates are USD $0.40 per million input tokens and $1.60 per million output tokens; cached input is listed at $0.10, but **no cache savings are assumed**. [Official rates](https://developers.openai.com/api/docs/models/gpt-4.1-mini).

| Reservation | Calculation | USD |
| --- | --- | ---: |
| Input per call | 1,047,576 × 0.40 / 1,000,000 | 0.4190304 |
| Output per call | 1,536 × 1.60 / 1,000,000 | 0.0024576 |
| Full per call | Input + output | 0.421488 |
| Five calls | 5 × 0.421488 | 2.107440 |
| Proposed ceiling | Hard run ceiling | 2.250000 |
| Headroom | Ceiling − five reservations | 0.142560 |

The input reservation is the entire documented context window, a conservative upper bound, **not an exact token count or character estimate**. The separate enforced 65,536-byte bound applies to the complete serialized provider request, including system prompt, schemas, advisory, catalog, and growing workflow state. Oversized requests fail before reservation/dispatch. This byte limit is not used as a token conversion.

One case, concurrency 1, at most five model calls, zero SDK/workflow retries, 1,536 maximum completion tokens per call, 120-second worker deadline, and 20-second HTTP phase timeout remain unchanged. The worker deadline controls total case execution; an HTTP phase timeout alone is not an end-to-end latency limit. Durable reservations precede attempts; unknown/interrupted/ambiguous usage retains reservations and prevents further dispatch. Unexpected model/tier receipts fail safely. Prior timeout, request-size, reconciliation, and tracing-isolation controls were not modified.

## Exact input and request-preview limitations

The [exact sanitized input](../data/week4/smoke-proposals/real-016-v2-3/sanitized-input.json) is byte-identical to V2-1 and proposal 2: SHA-256 `30ece2362f9b8623b12568cc6726215d407604fcc92b3cae2c1e4c3c0f29410c`. Its local archive digest is `dbc8ea81f66eba30c74cba89b08ab1c1ceee230886825f4f4f0acca429916d9f`. Unicode, the exact outgoing-header exception, reported 502, and remediation uncertainty are preserved.

The [initial request preview](../data/week4/smoke-proposals/real-016-v2-3/first-request-preview.json) includes the known system/user/schema/API parameter content, with a 15,395-byte preview body. It was not sent. HTTP authentication/SDK-generated headers and actual response are absent. The [later request templates](../data/week4/smoke-proposals/real-016-v2-3/later-request-templates.json) cannot predict future validated outputs, selections, route, advisory, or state growth; they are templates, not fabricated future requests or calls. Every actual request would be bounded again at dispatch.

The archive is a partial original-excerpt transcription. V2 distinguishes original anchors, attributed editorial summary, reporter-associated reproduction, and authenticated correlation; the latter remains false. Binding proves identity, not truth. Evaluator diagnoses, source resolutions, labels, and review decisions stay outside inference. Existing readiness, grounding, validation, authorization, and publication behavior is unchanged. Analyst entry would not establish diagnostic completion or semantic accuracy.

## Week 4-only configuration change

Only `evaluation/week4/live_config.py`, `live_cli.py`, and `smoke.py` change runtime behavior. A named proposal-3 budget profile permits $2.25 only with V2. The default profile remains $0.25; older plan versions cannot borrow the new profile. No previous experiment configuration or model selection is rewritten.

The proposal-3 loader validates source/dependency, configuration, input bytes, component and archive hashes, exact case/profile identity, tracing-off policy, lifecycle window, and full five-call funding. Live entry additionally requires explicit authorization bound to immutable proposal contents; missing authorization is rejected before credential lookup or SDK construction. A direct high-ceiling live entry requires that same bound plan. The binding detects mismatched proposal content; it is not an identity service or a substitute for the user's explicit future authorization.

All V2 external tracing remains disabled, including ambient exports. No incident tools are enabled. The preparation helper `scripts/week4_prepare_smoke016_v2_plan3.py` creates data and validates configuration only; it does not invoke a workflow or smoke runner.

## Offline verification and preservation

14 focused tests passed under OS network denial plus application guards. They cover five-call funding, old $0.25 defaults, old-version rejection, missing authorization, direct-entry rejection, changed input/config/code/archive bindings, model/tier/policy mismatch, lifecycle extension rejection, exhausted call/money reservations, uncertain reservations, and immutable-approval mismatch. Journal receipts in these tests are synthetic accounting fixtures, not provider attempts, spending, or model-quality evidence.

No SDK construction, socket/DNS attempt, subprocess/incident command, smoke, or model execution occurred during preparation. The prior 42-test provider report remains historical evidence for full-request rejection, mocked provider errors, timeout cleanup, and receipt behavior; these transport tests were not rerun or relabeled as this proposal's execution.

Preservation details and reproducible commands are recorded in [fresh verification results](../reports/week4/smoke-proposal3-verification-1/result.json). The 328 inherited files are compared against the existing manifest, never regenerated; preexisting reviewed assets, policy files, proposals, and sealed runs are compared against the pre-change snapshot. New proposal files are sealed with their own artifact hashes.

## Private prerequisites before any future authorized run

1. Resolve or explicitly accept dependency provenance: Python 3.11.16 and all 88 installed pins match the locks, but installed distribution archive integrity was not reverified. A future authorized hash-checked installation into an isolated environment may change bindings and require a new proposal. No installation occurred here.
2. Recheck lifecycle, applicable default-tier pricing, and model availability immediately before authorization. Changed rates, model, dependencies, code, or configuration require a fresh bound proposal. Keep older sealed plans intact.
3. Privately supply only the dedicated `WEEK4_OPENAI_API_KEY`; its value was not read. Do not reuse original credentials. No LangSmith credentials are required. Account/model permissions, quota, billing, and applicable tariff remain unverified until a future authorized run; do not perform authenticated discovery as part of this preparation.
4. Separately authorize exactly one bounded paid run and the exact immutable identity. Preserve this sealed master; any authorized copy must contain genuine approval identity/time and matching binding. No identity or time has been supplied by this task. Trace export must remain false.
5. Use a fresh immutable output directory with the existing supervised entry, process cleanup, request bounds, reservation journal, and usage reconciliation intact. Never rerun paid inference to repair tracing/accounting uncertainty. Leave human review blank until actually performed.

A future authorized smoke could establish account access, acceptance of concrete requests/schemas, response-tier/usage receipts, and bounded workflow mechanics for that case. It cannot establish general diagnostic quality. Actual cost and semantic accuracy remain null.

Reproducible verification (not smoke execution):

```sh
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-py311/bin/python -m unittest tests.week4.test_smoke_proposal3 tests.week4.test_supervised_v2_provider.ProviderControls.test_unknown_policy_model_bound_and_tier_are_not_substituted tests.week4.test_supervised_v2_provider.ProviderControls.test_new_plan_loader_selects_v2_and_rejects_configuration_tampering -v
```

The preparation helper is create-once and now intentionally refuses the existing proposal directory. Do not rerun it by deleting or overwriting the sealed output.
