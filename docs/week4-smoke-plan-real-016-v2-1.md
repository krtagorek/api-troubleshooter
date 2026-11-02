# Case 016 / V2 live development smoke proposal 1

**BLOCKED — not ready for execution approval. Prepared only; no smoke executed.**
This is a new versioned proposal, not an amendment or authorization of
`data/week4/smoke-plan.json`. Execution and trace-export authorization are false;
approval identity/time and every human grade remain unset.

## Approval summary

| Item | Proposed value |
| --- | --- |
| Case | One exposed development input, `W4-REAL-016`, revised projection `report-evidence-v2-1` |
| Policy | Explicit `attributed-report-readiness-v2`; no V1/inherited-policy fallback |
| Provider/model | OpenAI `gpt-4.1-mini-2025-04-14`; documented but deprecated, account access unverified |
| Limits | Concurrency 1; at most 5 model calls; zero SDK/workflow retries or model fallback |
| Tokens | At most 65,536 reserved input tokens and 1,536 total completion tokens per call; combined proposed context 67,072 |
| Timeouts | Proposed worker-process timeout 120 seconds; network-phase timeout 20 seconds |
| Budget | Proposed ceiling **USD $0.25**; five full reservations **$0.143360**, conditional on the stated bounds and default-tier rates |
| Tracing/tools | External tracing/export OFF; sanitized local durable spans and usage records retained; no diagnostic tools |
| Authorization | `execution_authorized=false`, `trace_export_authorized=false`; identity/time unset |

The [machine-readable plan](../data/week4/smoke-proposals/real-016-v2-1/plan.json)
binds current source files, V2 policy files, dependency locks, exact input, source
archive, configuration, deterministic assessment, pricing record and previews by
SHA-256. Its [artifact manifest](../data/week4/smoke-proposals/real-016-v2-1/artifact-hashes.json)
binds the final proposal files, including the plan itself. No private values are
included.

**No supported V2 live command currently exists.** Do not pass this proposal to
the earlier live command or run the mechanical comparison script as a live runner.
Clearing implementation blockers requires separately authorized work and changes
the source hashes: prepare a fresh plan version and obtain explicit paid-run
authorization tied to that supported version and its exact hashes. Approval of
this blocked proposal cannot authorize different code, a fallback policy, or the
earlier smoke plan. No wider evaluation budget or thresholds are approved here.

## Specific blockers

1. **V2 live integration is absent.** `evaluation/week4/smoke.py` imports the
   inherited `graph.workflow.build_workflow` directly. Its worker has no V2
   selection or scoped analyst-advisory integration. The V2 comparison path uses
   deterministic mock transport, not live-provider reservations.
2. **The current loader does not support this proposal format.** The existing
   path is `live_cli.load_plan → smoke.run_smoke → supervise(inference_worker) →
   inherited graph → LiveModel/Journal`. It accepts only `week4-smoke-plan-1`.
   Its command shape includes `--execute-live`; that is **not a compatible command
   for this plan**. The new plan deliberately records `execution.command=null`.
3. **The proposed input bound is not supported.** Current `LiveConfig` caps
   `input_cap` at 32,768. Data-only validation rejects the proposed 65,536 with
   `Invalid input cap`. A size-only reconstruction of the historical mock analyst
   request is 36,300 bytes plus 4,096 allowance = **40,396**, exceeding the existing
   guard. This motivates the proposed larger reservation without dropping required
   provenance. It does not predict a future live payload. No cap or runner was
   changed in this task.
4. **Tier and exact input metering are unresolved.** The provider omits
   `service_tier`, and the journal does not validate the returned tier. The
   official API says omission uses project-configured `auto`; explicit `default`
   selects standard pricing. The existing complete-request byte-length plus
   4,096 check is an operational proxy, not verified pre-dispatch provider-token
   metering. Thus this proposal's capped arithmetic is not a currently enforceable
   invoice guarantee. [Official Chat Completions reference](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create).
5. **Account and concrete schema acceptance remain unverified.** No authenticated
   discovery or schema submission was performed. Privately confirm dedicated
   project access, billing currency/tariff/default processing and applicable limits;
   do not infer access from a public catalog or a ChatGPT subscription. Recheck
   model status/prices before any future run. Any incompatible model, schema or
   account must block rather than trigger substitution.

No runner redesign or runtime behavior change was made to address these blockers.

## Provider facts and conservative calculation

The fetched official model page documents Chat Completions, Structured Outputs,
the exact snapshot, a 1,047,576-token context window, 32,768 maximum output tokens,
and operation without a reasoning step. Its listed text rates are **USD per
1,000,000 tokens: input $0.40, cached input $0.10, output $1.60**.
[Official model page](https://developers.openai.com/api/docs/models/gpt-4.1-mini).

The snapshot is deprecated, with API shutdown scheduled for **2027-01-14**.
That is documented lifecycle information, not a guarantee of access for a new
dedicated project. No newer model is silently substituted.
[Official deprecations](https://developers.openai.com/api/docs/deprecations).

Source retrieval date: **2026-10-29 UTC** (local planning date 2026-10-28 America/Chicago).
The [pricing/source record](../data/week4/smoke-proposals/real-016-v2-1/official-docs.json)
is a local transcription of fetched official facts, not an invented page snapshot,
raw-page hash or authenticated account quote. The official Structured Outputs
guide supports strict JSON Schema for compatible models, but public support
does not prove acceptance of every dynamically assembled schema.
[Official Structured Outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs).

With no cache hits or tool/Batch discounts assumed:

```text
Per-call reservation = (65,536 × $0.40 + 1,536 × $1.60) / 1,000,000
                     = $0.028672
Five full calls     = $0.143360
Proposed ceiling    = $0.250000
Headroom            = $0.106640
```

The conditional bounded scenario fits $0.25; **the current implementation cannot
enforce this proposal**, so this is not a ready-to-approve spending permission.
Different tariffs, account adjustments or unverified token envelopes invalidate
the calculation. Increasing the ceiling alone would not repair the blockers.

The completion cap covers total generated tokens, including reasoning where
applicable; count billed `completion_tokens` once rather than adding reasoning
again. The proposed model is documented as non-reasoning, and the current journal
does not preserve a separate reasoning breakdown. Never assume unknown total
usage is zero. [Official completion-token definition](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create).

## Sanitized evidence and request preview

- [Exact sanitized case copy](../data/week4/smoke-proposals/real-016-v2-1/sanitized-input.json):
  byte-identical to the versioned projection. Unicode header, exception, reported
  502 provenance, unknown response-body semantics and neutral operation goal are
  preserved; sanitization makes no change.
- [Deterministic attribution assessment](../data/week4/smoke-proposals/real-016-v2-1/attribution-assessment.json):
  source anchors resolve and the full-catalog selection scenario permits qualified
  analysis only, with definitive confirmation false. This is **not a future model
  selection**. Omitted peers, ambiguity, invalid references, refusals or incomplete
  outputs may hold or stop before analyst entry.
- [Initial request preview](../data/week4/smoke-proposals/real-016-v2-1/first-request-preview.json):
  known messages checked against the current classifier prompt, sanitized input
  and deterministic catalog. It includes the proposed model/output cap and current
  adapter's strict wire schema/API parameters. It was not sent or SDK-dispatched.
  The omitted tier is marked explicitly, not silently filled with the desired tier.
- [Later request templates](../data/week4/smoke-proposals/real-016-v2-1/later-request-templates.json):
  symbolic, non-runnable templates. Classification, selected evidence/completeness,
  hypotheses, diagnosis, proposed fix, selected-handle enums and V2 analyst advisory
  depend on prior validated outputs and cannot all be known in advance. No mock
  answers were installed as future outputs. Resolution/validator stages may never
  execute. Existing strict schema, grounding and publication checks remain binding.

The source archive remains a **partial selected-excerpt transcription** and a
**reporter-associated reproduction**, not an authenticated request correlation or
independent reproduction. Locations and hashes bind content; they do not establish
truth. Editorial summary and verbatim excerpts retain distinct kinds. Expected
diagnoses, review decisions, later resolutions and rubrics remain outside the
typed inference copy and request payload fields. The review worksheet is separate
and must never be included in model requests.

## Reservation, accounting and termination semantics

The existing Week 4 journal uses a fresh create-only, append-only/fsynced local
file with locked reservation operations. It reserves full per-call input/output
cost before an attempted dispatch and rejects additional reservations when call
or money limits are exhausted. Unsettled calls or limit violations stop further
dispatch. Each request is marked attempted once; raw provider input/output/cache
counts and resolved model are persisted before structured parsing.

Known metering survives refusals and parsing failures. Missing/invalid metering,
model mismatch or interruption retains uncertain reservations; it does not release
them as zero-cost work or automatically retry. The cached-count hook currently
defaults an absent cached-token detail to zero, conservatively pricing all input
as uncached; that convention is not proof of zero actual cache hits. Actual input
and output totals remain unknown when absent. The journal prices usage at supplied
rates, not an independently reconciled provider invoice.

The worker is supervised in its own POSIX session, with terminate/kill/reap and
process-group cleanup verification. The 120-second process timeout is not a
promise of five completed calls. The 20-second HTTP timeout applies to network
phases, not a separate hard per-call wall deadline. Parent reconciliation and
filesystem writes lie outside the worker process timer. **Local termination does
not cancel remote computation or billing**; interrupted attempts remain uncertain
until reconciled. Local root/node/model spans correspond only to executed work;
no fabricated children for deterministic checks or skipped stages.

No external trace operation is proposed. Export delivery cannot trigger another
inference attempt, and the old trace-only path must not be invoked for this plan.

## Credentials and tracing

Required dedicated private variable: **`WEEK4_OPENAI_API_KEY` only**. Do not put
its value in chat, the plan or command arguments. Do not reuse original project
credentials or automatically load credential files. A future dedicated project
must have account access confirmed privately; nothing was provisioned here.

**No LangSmith credential or project is required with exports disabled.** The
existing checks require `WEEK4_LANGSMITH_API_KEY`/project only when export is
requested. Omit all `WEEK4_LANGSMITH_*` settings in the proposed clean execution
environment. Local durable tracing remains enabled while remote export stays off.

The current worker clears non-allowlisted environment, sets `LANGSMITH_TRACING`
and `LANGCHAIN_TRACING_V2` false, disables durable/diagnostic application flags,
and points SDK-profile lookup to a nonexistent file in the new run directory.
The provider disables environment proxies/redirects and uses a fixed official
origin. It wraps calls in disabled ambient tracing contexts. The allowlist still
permits optional Week 4 tracing variables, so the proposed clean shell should omit
them rather than assuming the worker scrubs those values.

Named ambient tracing/export flags and endpoint-variable **presence** were checked:
all inspected settings were unset. No secret values, credential files or private
configuration were read. The local builder cleared its own inherited environment
before imports, blocked socket/DNS/client constructors, and initialized no SDK
clients. These checks do not attest every future parent environment; recheck it
before any explicitly authorized supported run.

## Human review and offline verification

The [blank worksheet](../data/week4/smoke-proposals/real-016-v2-1/review-worksheet.json)
covers evidence selection/grounding, header-encoding diagnosis, reporter attribution
and uncertainty, safe suggestions, fabricated remediation, and actual route,
calls, usage, cost and latency. Identity/time and semantic grades remain blank.
Graceful hold and analyst entry do not count as diagnostic success.

[Verification](../data/week4/smoke-proposals/real-016-v2-1/verification.json)
is local/static/data-only, with OS networking denied and Python socket/DNS/client
guards. No graph, agent, model, smoke worker or supervisor was invoked. It checks
sanitization, source-anchor resolution, input/template isolation, installed lock
versions, current loader/worker code, cost arithmetic and expected configuration
rejection. Runtime/network/SDK-client tests were unnecessary and not run.

All **328 inherited files**, **50 protected assets**, **880 pre-existing files**,
and **10 active prior sealed manifests / 407 artifact entries** remain unchanged.
The earlier smoke plan and superseded preservation metadata are preserved; the
baseline manifest was not regenerated. No runtime source file was modified.
The only network exception used was public official-document retrieval. No paid
model call, authenticated API call, incident request, external trace, installation,
service, database, Docker, commit, remote or original-project change occurred.
