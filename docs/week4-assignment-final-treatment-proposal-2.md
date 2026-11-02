# Final cumulative treatment proposal 2 — NOT AUTHORIZED

[Machine-readable plan](../data/week4/execution-proposals/assignment-final-treatment-2/plan.json)

**SHA-256: da8f65bfafe5e73edc18abbad70b8b9d482eeb8368bd1b94bb2e648a2996ca5a**

execution_authorized=false; trace_export_authorized=false. Approval identity, time and binding are unset. Prior proposal-1 approval does not authorize this changed code binding. No run was executed during preparation.

| Setting | Proposed execution |
| --- | --- |
| Dataset | Same 30 frozen assignment-30-v1 inputs, order, references, rubric and applicability |
| Dataset manifest SHA-256 | c105de5632777304e876176f74e5dcf1a0ae0442058ff28e37edbfbb9cb75b32 |
| Treatment | attributed-report-readiness-v2 + attributed-selection-dependencies-v1 + reviewed_targets=true; unchanged |
| Model / tier | gpt-4.1-mini-2025-04-14 / default; no substitution |
| Calls / concurrency / retries | Five per case; 150 total; concurrency 1; zero retries or fallback |
| Maximum | **$63.223200 total**, $2.107440 per case, $0.421488 reservation per call |
| Complete request bound | 65,536 serialized UTF-8 bytes including system/schema/advisories/state; checked before every dispatch |
| Input / output reservation | 1,047,576 input tokens conservatively reserved; max_completion_tokens=1,536; no cache savings |
| Timeouts | Existing 20s call / 120s process case boundary, with verified cleanup |
| Tracing / tools | Local tracing ON; external exports, ambient tracing and incident tools OFF |
| Fresh result location | reports/week4/assignment-final-treatment-live-2 — not created |
| Expiry | 2027-01-13; repeat public pricing/lifecycle checks before execution |

Only the Week 4 manifest-versus-single-case guard scope changes. Configuration and maximum limits are byte-equivalent as JSON values to proposal 1. The only changed runtime source binding is `evaluation/week4/smoke.py`; the new focused regression is also recorded. [Verification and exact diff](week4-manifest-live-guard-fix-verification.md). Original proposal, authorization and zero-call attempt remain sealed. That attempt made no provider calls and supplies no model-quality evidence. The sealed live baseline will be reused; no baseline rerun or follow-on experiment is included.

The [official model page](https://developers.openai.com/api/docs/models/gpt-4.1-mini) was refreshed on 2026-10-29: the snapshot documents Chat Completions and structured outputs, 1,047,576 context, and per-million-token rates of $0.40 input, $0.10 cached input and $1.60 output. The [official deprecation page](https://developers.openai.com/api/docs/deprecations) retains its January 14, 2027 shutdown. Account-specific access remains unverified; no authenticated discovery occurred. [Bound public verification](../data/week4/execution-proposals/assignment-final-treatment-2/public-provider-verification.json).

Conservative uncached reservation: `(1,047,576 × 0.40 + 1,536 × 1.60) / 1,000,000 = $0.421488`; five calls × 30 cases = **$63.223200**. Full context reserved as input plus output intentionally overbounds feasible requests; it is neither an exact token count nor a character estimate. Existing durable journals, uncertain-usage retention, admission bounds and timeout cleanup remain enforced. Ordinary safe failures remain assigned case outcomes; unsafe/accounting uncertainty stops further dispatch.

The inherited illustrative **$0.36–$0.72 usage-cost range** assumes 30 cases at three × (8k input + 500 output) through five × (8k input + 1k output) tokens/case at uncached rates. It is not a treatment forecast or guarantee. Actual treatment cost and semantic scores remain null. V2-05-01's existing investigator failure remains in scope. Analyst entry is not diagnostic completion; combined final-versus-baseline results cannot isolate per-change semantic causality. Saved questions do not establish UI delivery.

Remaining setup: explicit approval of **this exact proposal/hash**; a separately authorized bound copy through the existing mechanism; private dedicated WEEK4_OPENAI_API_KEY loading through the selective loader; repeated proposal/dataset/dependency/preservation, fresh-output and pricing/lifecycle preflight. Current private account access is unverified. All 88 pins/Python match, and the prior hash-locked installation receipt remains intact; no installation or new installed-file integrity audit occurred. The private project .env was not inspected in preparation.

The existing VS Code task still targets proposal 1 and its sealed result directory. It was deliberately not rebound or relaunched. Only after explicit approval should the existing launch configuration point to the separately authorized proposal-2 copy and the new output path. **No execution, exports, baseline rerun or subsequent improvement runs are authorized by this document.**
