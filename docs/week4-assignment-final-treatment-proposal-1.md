# Final cumulative treatment proposal 1 — NOT AUTHORIZED

[Machine-readable plan](../data/week4/execution-proposals/assignment-final-treatment-1/plan.json)

**SHA-256: a367001cc86e71c320399f3cc128e0259ef3d8f3ea32384067b61944c6c38dad**

execution_authorized=false; trace_export_authorized=false. Approval identity, time and binding are unset. Implementation/offline verification does not authorize paid execution. This proposes **one final cumulative treatment run only**, reusing the sealed live baseline; no baseline rerun or intermediate/improvement follow-on runs are authorized.

| Setting | Exact proposal |
| --- | --- |
| Dataset | All 30 frozen assignment-30-v1 cases, unchanged order/input bytes/reference/rubric/applicability |
| Dataset manifest SHA-256 | c105de5632777304e876176f74e5dcf1a0ae0442058ff28e37edbfbb9cb75b32 |
| Treatment | Existing attributed-report-readiness-v2; attributed-selection-dependencies-v1; reviewed_targets=true |
| Model / tier | gpt-4.1-mini-2025-04-14 / default; no substitution |
| Provider | Existing supported SDK Chat Completions path; strict structured outputs; temperature 0 |
| Calls | At most five/case, **150 total**, concurrency 1, zero SDK/workflow retries, no fallback |
| Per-call output | max_completion_tokens=1536 |
| Complete request cap | 65,536 serialized UTF-8 bytes, including system/schema/advisories/growing state; recomputed before dispatch |
| Input reservation | Full documented model context, 1,047,576 tokens/call; conservative bound, not an exact token count or character estimate |
| Timeouts | Existing 20s call timeout; 120s process case timeout plus verified terminate/kill cleanup grace |
| Maximum reservation | **$0.421488/call; $2.107440/case; $63.223200/run** |
| Tracing/tools | Existing local spans ON; external exports, ambient instrumentation and incident tools OFF |
| Result path | reports/week4/assignment-final-treatment-live-1 — fresh, not created during preparation |
| Credential | Dedicated WEEK4_OPENAI_API_KEY configured privately in execution process; neither value nor presence checked here |
| Expiry | 2027-01-13; recheck lifecycle/pricing before any authorized execution |

## Public provider verification and funding

The current [official model documentation](https://developers.openai.com/api/docs/models/gpt-4.1-mini) lists this snapshot, Chat Completions, structured outputs, context 1,047,576, and prices per million tokens: **$0.40 input, $0.10 cached input, $1.60 output**. The [official deprecation notice](https://developers.openai.com/api/docs/deprecations) schedules this snapshot's API shutdown for **January 14, 2027**. Public verification is recorded in the bound plan and [provider-verification record](../data/week4/execution-proposals/assignment-final-treatment-1/public-provider-verification.json). Deprecated does not establish private account access; no authenticated discovery occurred.

Uncached worst-case reservation per call = (1,047,576 × $0.40 + 1,536 × $1.60) / 1,000,000 = **$0.421488**. Five calls/case and 30 cases yield **$63.223200**. Reserving full context as input plus maximum output intentionally overbounds real requests; it does not assert that a request of that size would fit alongside output. The independent complete-request byte cap remains enforced. No cache savings are assumed.

The inherited illustrative usage-cost range **$0.36–$0.72** is an assumption, not a guarantee, authorization or treatment forecast: 30 cases at 3 × (8k input + 500 output) through 5 × (8k input + 1k output) tokens/case, uncached rates. The sealed baseline actually cost $0.0681888 in receipt-priced usage; that is historical baseline spending, not predicted treatment cost. Mock token/cost receipts are test data. Treatment actual cost and semantic quality remain null.

Existing per-case durable reservations and global manifest admissions prevent dispatch beyond money/call limits. Missing/ambiguous usage retains reservations, fatal accounting/isolation uncertainty stops the batch, and every unattempted assignment remains recorded. Ordinary safely metered failures stay in results and permit supported continuation. There is no inference retry for trace failure and no export in this proposal.

## Exact intended changes and limitations

1. Existing V2 readiness/dependencies plus scoped investigator guidance; explicit selected evidence only in the reviewed treatment, with supplied/unselected versus not-supplied fields distinguished. The same narrow ASCII-header rule remains; arbitrary prose does not become diagnosis-ready.
2. Scoped nonsecret-metadata guidance and bounded case-specific questions through existing pending_user_questions. Publication holds and safety markers remain. These are **saved evaluation fields, not verified UI delivery**; final_report is not created to bypass a hold.
3. A resolution-request wording advisory compatible with unchanged action/grounding validators. Historical rejected replies still fail; model responses are not repaired or retried.

[Implementation/verification report](week4-three-target-verification.md) includes exact before/after requests, all 30 mock routes/errors, and acceptance-control evidence. The common mock is inconclusive; its 30-case run does not exercise resolution or validation, which have separate saved-response controls. No mock result is diagnostic-quality evidence.

**Known retained case failure:** V2-05-01's numeric catalog observation is redacted before the existing explicit selection snapshot check. The treatment retains the investigator failure before its provider call; one classifier call is recorded in the mock. The input, redaction and validators were not repaired. The case is not excluded from the final 30. Other unsupported report-only cases still hold; a better clarification is not a completed diagnosis.

The combined final-versus-baseline comparison cannot isolate per-change semantic causality. Case-level human grading and safety review are still required after any authorized final run. No general robustness claim is supported by the single exposed adversarial case.

## Approval prerequisites

- Explicit approval of **this exact proposal/hash**, one final treatment only, $63.223200 and 150 calls. The consumed baseline authorization does not apply.
- Private dedicated key in the launching process. Current private account/model access remains unverified; no key was read or authenticated request made.
- Repeat the existing dependency/binding/preservation and pricing/lifecycle preflight before execution. Current 88 pinned versions/Python 3.11.16 match the inherited lock; the bound prior hash-locked installation receipt is verified. No new installation or independent installed-package-file re-audit was performed.
- Preserve fresh output, exports/tools OFF, and the same frozen inputs/rubric. Prior plans remain sealed historical artifacts; their old runtime bindings were not silently refreshed.

The existing future command is `python -m evaluation.week4.live_cli run-manifest --plan <separately-authorized-bound-copy> --output reports/week4/assignment-final-treatment-live-1 --execute-live`. The proposal as prepared rejects execution authorization before dispatch. No future paid command was executed here.
