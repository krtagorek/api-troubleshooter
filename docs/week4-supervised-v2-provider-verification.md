# Supervised V2 provider integration and proposal 2

Implemented the bounded Week 4 integration and verified it offline. **The
case-016 paid smoke remains blocked by conservative funding requirements and
unverified account access.** No model, policy or service tier was substituted,
and the existing $0.25 software ceiling was not raised.

New [proposal 2](../data/week4/smoke-proposals/real-016-v2-2/plan.json) is bound to
the changed source/configuration hashes and the unchanged revised case input and
source archive. Both authorization flags remain false; approval identity/time
and human grades remain unset. The sealed earlier proposal is unchanged and is
not reauthorized by this work.

## Changes outside the inherited baseline

- `evaluation/week4/smoke.py`: explicit validated `evidence_policy` selects V2
  through the existing supervised worker and inherited factories. Its provider
  is wrapped with the existing V2 analyst-advisory adapter; no new agent or
  evidence mechanism is introduced. Unknown policies are rejected. V2 remote
  exports are rejected before dispatch. Inference environment isolation now also
  drops tracing credentials/endpoints and disables legacy tracing and OTel flags.
- `live_config.py`: pins V2 to the selected snapshot and a documented full-context
  input reservation; separates the 65,536-byte complete-request limit from token
  accounting. Only explicit `service_tier=default` is supported. Existing money,
  output, call-count and timeout ceilings remain unchanged.
- `live_provider.py`: prepares the complete sanitized provider body, including
  current system messages, strict response schema, V2 advisory and growing state,
  **on every invocation**. Oversize rejection occurs before reservation or SDK
  construction. The SDK request hook rechecks the actual serialized body against
  the prepared object and byte cap before marking an attempt. Prepared and actual
  body hashes are recorded distinctly. A byte limit is not called a token count.
- `accounting.py`: retains received counts before semantic parsing and adds strict
  V2 model/tier, total-token consistency and cache-count checks. Missing or
  ambiguous metering retains reservations and blocks subsequent dispatch. Optional
  reasoning detail is recorded; total completion tokens are priced once.
- `live_cli.py`: accepts the new proposal version, validates explicit V2/tracing-off
  identity, source/configuration/case/archive bindings and full funding. Execution
  still requires explicit authorization and the live flag. Unfunded plans fail
  before creating an execution directory or client.
- `sdk_fixtures.py`: adds an unknown/partial/inconclusive mechanical transport
  scenario and explicit returned tier, solely for offline verification.

All modifications are Week 4-only. The 328 inherited files, prompts, grounding,
redaction, routing/publication/authorization policies and reviewed V1/V2 evidence
assets remain unchanged. The legacy Week 4 path remains explicitly separate;
V2 never falls back to its byte proxy or to another model/tier.

## Why the reservation changed

The previous 65,536-token reservation was not established by the byte-plus-4,096
proxy. Local tokenization of text alone would not prove the provider's complete
Chat/schema framing. Official documentation describes an input-count endpoint
for **Responses**; no equivalent exact count for this Chat Completions request
was established here. Treating a Responses count as a Chat count would require
additional justification or a separately scoped API change.
[Official token-counting documentation](https://developers.openai.com/api/docs/guides/token-counting).

V2 now reserves the selected model's **entire documented context window,
1,047,576 tokens**, for each call, independently of its much smaller wire size.
This is a deliberately loose upper-bound assumption for accepted requests under
the documented model contract, not an exact count or character estimate. It
covers unknown provider-side framing without inventing a fixed overhead. The
65,536-byte local request cap separately limits transport resources and growing
state; it does not reduce the full-context reservation.
[Official model context and rates](https://developers.openai.com/api/docs/models/gpt-4.1-mini).

At the publicly listed USD-per-million input/output rates of $0.40/$1.60, without
assuming cached input:

```text
Per-call reservation = (1,047,576 × 0.40 + 1,536 × 1.60) / 1,000,000
                     = $0.421488
Five full calls      = $2.107440
Current hard stop    = $0.250000
```

**$0.25 is enforced as a stop, but is not a viable smoke ceiling under this
bound.** Even the first reservation is refused; tests verify zero dispatches at
the real listed rates. $2.11 is recorded only as a rounded candidate minimum for
five full reservations, not as an implemented or authorized ceiling. Raising the
hard stop, selecting another model or changing/counting another API is outside
this increment. A narrower justified bound or explicitly authorized budget work
would require a fresh configuration/source binding and proposal.

The input bound relies on the provider honoring its documented model context;
returned violations are recorded and stop further calls. Local software cannot
promise an invoice against a provider contract violation. The selected snapshot
remains deprecated; actual account access and lifecycle must be rechecked before
any future paid proposal is approved.

## Metering, tier, traces and timeout behavior

Requests explicitly send `service_tier=default`, `max_completion_tokens`, strict
JSON Schema, `stream=false`, `store=false`, fixed official provider origin and
zero SDK retries. Redirects and environment proxies remain disabled. Actual
returned V2 tier must also be `default`; missing/unexpected tiers retain uncertain
reservations and stop. There is no automatic retry or alternative tier.
[Official Chat Completions parameters](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create).

V2 requires integer input/output/cache counts and a consistent total. Unknown
cache usage is no longer silently recorded as zero in V2. Non-visible/reasoning
tokens are already included in completion totals and are not billed twice.
Known usage survives parsing failures. Missing metering, mismatched model/tier,
provider/network errors and interrupted calls fail safely; uncertainty does not
become zero spending. Durable locked/fsynced reservations still precede attempts,
and unsettled calls, call exhaustion or insufficient funds prohibit another
dispatch. An oversize preflight has no reservation and no attempted model call.

The existing POSIX process supervisor still terminates/kills/reaps the worker and
verifies process-group cleanup. The overall worker timeout and HTTP phase timeouts
have different boundaries. Killing a local process does **not** cancel remote
work or prove billing cancellation; an interrupted attempt retains its reservation.

V2 export flags are rejected; no LangSmith credential is required. The inference
child drops tracing credentials/endpoints, disables ambient LangSmith/LangChain
and OTel export flags, and uses disabled SDK tracing contexts. Sanitized durable
local spans and provider usage remain. Only executed/attempted boundaries appear
as model spans after reconciliation; no children are invented for deterministic
checks or budget/size rejection. The separate legacy trace-recovery capability
was not invoked or authorized.

## Focused offline verification

**42 tests passed**: 11 new provider/integration controls, 27 existing provenance
and workflow-parity controls, and four existing mocked-SDK parsing/accounting/
interruption/timeout regressions. [Sealed verification record](../reports/week4/supervised-v2-provider-verification-1/result.json).

| Check | Observed result |
| --- | --- |
| Explicit V2 through supervised worker and SDK MockTransport | Classifier, investigator and inherited analyst completed; three mock dispatches; held/inconclusive; zero errors. V2 advisory version/qualification was present. |
| Complete body oversized, including schema even with tiny visible text | Rejected before reservation, SDK construction or mock dispatch; zero attempts. |
| Budget exhaustion or call limit | Further dispatch prevented. Real-rate/full-context configuration at $0.25 dispatched zero requests. |
| Known usage, cached input and reasoning detail | Cost reconciled with completion tokens counted once; known usage persisted before parsing rejection. |
| Missing usage/cache count, inconsistent total, missing/unexpected tier | Reservation retained; unknown priced total remains null; subsequent call refused. |
| Network timeout and provider error | One mock attempt, no retry; safe failure and further-dispatch prohibition. |
| Process timeout/interruption | Cleanup verified; attempted call remains uncertain and reserved. |
| Policy/model/bound/tier substitution or plan configuration tampering | Rejected. New-format funded synthetic plan selected V2. |
| Ambient tracing/export settings | Removed/disabled; V2 export request rejected. No external exports. |
| Existing reference/ambiguity/conflict/coverage and insufficient-evidence controls | Passed unchanged; baseline/V1/V2 policy assets preserved. |

Tests ran under OS `deny network*`, with additional socket/DNS guards. New SDK
tests permit initialization **only with an in-process MockTransport and a fixed
non-credential fixture string**. No live SDK transport or private credential was
used; LangSmith client initialization was blocked. Existing selected SDK tests
also used only fixture transports. These were isolated offline verification
scenarios, not execution of a live smoke plan. No diagnostic answers or source
resolutions supplied the mock responses.

The supervised test uses arbitrary **test-only rates** to exercise later nodes;
they are not proposed prices or spending evidence. The real-rate no-dispatch test
is separate. Analyst entry is branch coverage, not diagnostic success, appropriate
clarification, golden readiness or semantic accuracy. Semantic accuracy and real
cost remain null/not measured.

## New proposal and prerequisites

[Proposal 2](../data/week4/smoke-proposals/real-016-v2-2/plan.json) contains the
supported policy/tier/configuration, source/dependency/input/archive hashes, exact
sanitized input, updated request previews, conditional attribution assessment and
blank human worksheet. The loader rejects this real-price plan with the expected
funding error. `execution_authorized=false`, `trace_export_authorized=false`, and
approval fields remain unset. No sealed proposal was edited.

Remaining prerequisites are precise:

1. Resolve funding versus conservative input counting through a separately scoped
   change; the $0.25 ceiling cannot fund this selected model with this reservation.
2. Privately verify dedicated account/model access, current default-tier pricing,
   model lifecycle and billing controls. No authenticated discovery occurred.
3. Prepare fresh bindings after any such change, then obtain explicit user paid-run
   authorization for that plan/version and hashes. Account verification alone does
   not override the funding blocker.

A future authorized smoke would establish whether this account accepts the
specific strict schemas and returns the expected model/tier/metering, and would
record its actual selection, route, latency and charges. It would not independently
reproduce the public incident, authenticate reporter correlation or establish
semantic quality without genuine human review. Only a dedicated
`WEEK4_OPENAI_API_KEY` would be needed; no tracing credential is required.

## Preservation and reproduction

**328/328 baseline files and 50/50 protected reviewed assets match** the existing
manifest/preflight. All **851 snapshotted protected files**, including V1/V2 policy
files, earlier proposals, docs and prior results, are unchanged. Ten prior active
sealed result manifests / 407 artifact entries match; the earlier sealed smoke
proposal also matches its own manifest. Permitted Week 4 runtime source changes
make earlier source bindings historical, not a license to refresh them in place.
The baseline manifest was not regenerated.

Reproduce the focused new controls (no credentials/installations required):

```sh
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-py311/bin/python -m unittest tests.week4.test_supervised_v2_provider -v
```

The complete test selection and code assertions are recorded in the verification
artifacts and test sources. The macOS network-deny sandbox required an exception
to the enclosing workspace sandbox; no network capability was enabled for tests.
Public official-document retrieval was the only network exception used. No live
model, authenticated/incident request, external trace, installation, service,
database, Docker, commit, remote or original-project change occurred.
