# Assignment original-baseline execution proposal 1 — NOT AUTHORIZED

Machine-readable [plan](../data/week4/execution-proposals/assignment-baseline-1/plan.json), SHA-256 **dcd2076c86747bc8b57196f0f29b93ecc2e6895f2a49786df609b547e4e1955b**.
Frozen [assignment-30-v1 manifest](../data/week4/datasets/assignment-30-v1/manifest.json), SHA-256 **c105de5632777304e876176f74e5dcf1a0ae0442058ff28e37edbfbb9cb75b32**.

Dataset approval does not authorize execution. execution_authorized=false; trace_export_authorized=false; approval identity/time/binding unset. **Baseline only:** no later improved/intermediate run is implicitly authorized. No live run was performed by preparation or offline tests.

| Setting | Exact proposal |
| --- | --- |
| Cases | All 30 manifest cases, fixed manifest order; identical files required for any later comparison |
| Arm | Original inherited graph/factories/prompts, evidence_policy=inherited, selection_policy=off |
| Model/API/tier | gpt-4.1-mini-2025-04-14; supported OpenAI SDK Chat Completions; explicit default tier |
| Temperature/output | 0; max_completion_tokens=1536; strict structured output, no fallback |
| Calls | Maximum 5/case, **150/run**; concurrency 1; SDK/workflow retries 0 |
| Complete request cap | 65,536 UTF-8 serialized bytes including system/schema/advisories/state, recomputed at every call; bytes are **not** exact tokens |
| Input reservation | 1,047,576 tokens/call: conservative full documented context; no cache savings assumed |
| Timeouts | Call 20s; process case 120s plus existing terminate/kill cleanup grace; cleanup must verify |
| Money | $2.107440/case; **$63.223200 maximum for baseline** |
| Tools/tracing | Incident/evidence execution tools OFF; exports/ambient tracing OFF; existing local spans ON |
| Credential | Dedicated WEEK4_OPENAI_API_KEY only, configured privately; not inspected here |
| Future result directory | reports/week4/assignment-baseline-live-1; not created/executed during preparation |
| Expiry | Must execute by 2027-01-13; recheck rates/lifecycle before authorization/execution |

## Verified public rates and reservation calculation

Official [GPT-4.1 mini documentation](https://developers.openai.com/api/docs/models/gpt-4.1-mini) lists $0.40 input, $0.10 cached input and $1.60 output per million; 1,047,576 context, structured outputs and Chat Completions. The [deprecation notice](https://developers.openai.com/api/docs/deprecations) schedules removal for January 14, 2027. Public documentation does **not** prove account access. Rates/lifecycle were checked on 2026-10-29; source record is official-pricing.json beside the plan.

Worst-case per call = (1,047,576 × $0.40 + 1,536 × $1.60) / 1,000,000 = **$0.421488**. Five calls = **$2.107440**. Thirty five-call cases = **$63.223200**. Reserving a full context as input plus output is deliberately conservative; it is not a claim that an actual request uses that many input tokens. Complete-request byte rejection remains an independent bound.

**Separately labeled usage-cost assumption: $0.36–$0.72 for the baseline**, not measured, guaranteed or authorized spending. It assumes 30 cases at 3 × (8k input + 500 output) through 5 × (8k input + 1k output) tokens/case. No cache savings. Actual cost/semantic quality remain null. Do not substitute this estimate for the conservative reservation ceiling.

## Existing-path enforcement and accounting

The existing supervised run_smoke path is invoked sequentially by its manifest extension, through the same provider, journal, process supervisor and local spans. Resource-admission files represent **cases**, not invented provider calls. Actual dispatch/usage remains in the original durable per-case journals; aggregate limits reconcile those journals before the next case. Immutable case outputs and a fresh batch output prevent retry/resume. Fully metered ordinary case failures remain in results and allow safe continuation. Security/resource/accounting uncertainty or unverified cleanup stops dispatch; every remaining assigned case gets an explicit unattempted record. Unknown charges retain reservations; corrupt journals retain an explicitly unresolved case-liability bound instead of invented attempts/usage. Trace issues never trigger repeated inference.

Both original-baseline and explicit V2 configurations use identical full-context/request-size/service-tier/receipt accounting; workflow choice is separate. Older $0.25 defaults and sealed experiment configurations are unchanged. This is a configuration/supervision extension, not another readiness policy, agent, ledger or remote transport.

## Known retained mechanics failure

V2-05-01 remains selected. Its numeric epoch value is preserved in the input, but the inherited sanitizer redacts its catalog observation string; investigator processing then fails binding in both SDK-mock arms. This failed row remains visible and later safe cases continue. No guard/redaction relaxation is included in this extension. Input compatibility does not promise full workflow completion or semantic success.

## Remaining operational prerequisites

- Explicit approval of this exact plan hash and **baseline-only $63.223200/150-call** maximum. Dataset decisions do not meet it.
- Private execution environment with WEEK4_OPENAI_API_KEY. Neither key value nor presence was inspected for this proposal. Account/model access and real batch provider behavior remain unverified; no authenticated discovery is authorized.
- Repeat the existing offline loader/dependency checks immediately before execution. The prior hash-locked installation receipt is bound; current 88 versions/Python/locks are checked. No new install occurred. Installed package-file integrity beyond that receipt/version check was not independently re-audited.
- Preserve fresh output path, frozen inputs, disabled exports/tools and model lifecycle window. Future code/rate/input changes require a new bound proposal. Prior smoke/pair proposals remain sealed historical artifacts; their old code bindings are not silently refreshed.

The future supported command is `python -m evaluation.week4.live_cli run-manifest --plan data/week4/execution-proposals/assignment-baseline-1/plan.json --output reports/week4/assignment-baseline-live-1 --execute-live`. It currently rejects the unauthorized plan before dispatch. It was **not run live**. Record any future authorization through the existing bound-plan mechanism; do not repurpose the dataset-review approval.
