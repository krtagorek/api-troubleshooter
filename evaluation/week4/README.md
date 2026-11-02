# Week 4 evaluation adapter

The in-process mock runner remains available. A separate single-case supervisor
now implements the supported OpenAI live-provider SDK and explicit sanitized
LangSmith Client instrumentation, verified only with mocked transports. **Paid
calls and external exports remain unauthorized.** No golden dataset, semantic
reference labels, historical ledger or automatic approval system was created.

See [the smoke/setup plan](../../docs/week4-smoke-plan.md) for exact private setup,
locked installation, unresolved model/pricing fields and future commands. The
new live integration is `python -m evaluation.week4.live_cli`; its `plan` action
is offline. Execution and trace actions require explicit flags and future
permission. The machine proposal is `data/week4/smoke-plan.json`.

The CLI accepts only the two built-in exposed development fixtures:

```sh
.venv-week4-py311/bin/python -m evaluation.week4 --experiment offline-dev-1 --output reports/week4/offline-dev-1
```

Output must be inside this project. Each run creates a new directory and writes
files exclusively; existing directories cannot be resumed or overwritten. A
fresh run UUID distinguishes repeated experiments; root/child IDs are stable
within that run. Completed artifacts and their directory are made read-only (0400/0500). The
SHA-256 artifact inventory detects later edits; an owner can still explicitly
change permissions, so this is not filesystem WORM protection. `experiment.json`
binds source/prompt-bearing module hashes, packages, dataset version and config.
Each assigned case gets a result and an unfilled review worksheet. Executed cases
also get local spans and mock usage receipts. Interrupted runs retain available
artifacts and must use a new directory; absence of final artifact hashes signals
an incomplete run. This is not a paid dispatch ledger.

`InferenceCase` is a strict runtime input boundary. It rejects evaluator-only keys
recursively before inherited sanitization can silently remove them. Unknown
incident fields are rejected. Only an `Incident` reaches `initialize_state`.
`EvaluatorReference` is a separate post-inference type, never a runner parameter.
Key checks cannot detect an answer paraphrased inside ordinary incident prose:
source/label review is still required. Do not populate expected answer notes or
human review fields without authentic review. `grading.py` provides structural
trace/usage checks, exact evidence checks, assigned denominators and a blank
worksheet; none establishes semantic diagnostic correctness.

`runner.py` invokes `build_workflow` with **all five inherited factories** via
`agents=` and `llm=`. No inherited code or behavior is patched. Zero workflow
retries, no checkpoint/database, external tools or diagnostic contracts. Holds
are inherited route decisions, not reviewed legitimacy judgments. Stage coverage
records actual agent-factory boundaries; it does not claim instrumentation of
internal graph control/routing nodes. Partial validated state is retained after
ordinary errors. Input errors and unattempted rows use the same result schema,
with null timing/usage where no workflow ran. Counts include every assigned case.

`MockModel` uses real ChatOpenAI schema serialization and parsing over a mandatory
`httpx.MockTransport`. It explicitly supplies a dummy key and dummy origin,
disables environment proxies, SDK retries, cache and ambient LangSmith tracing.
This mock path has no switch to a live transport; the separate supervised smoke path uses `LiveModel`. Root → agent-node → actual model-attempt
spans are explicit local records. Skipped stages and deterministic work have no
fabricated model/tool spans. No tools are configured, so no tool calls or spans
occur. The inherited validator actually calls the model and then enforces
NOT_TESTED; both this attempted call and any swallowed model error are retained.

Schema rejection, refusal, grounding/agent rejection, mock timeout and application
errors remain failures and subsequent safe cases continue. Label/isolation
failures, case/call/byte ceilings and missing/invalid received usage stop dispatch;
remaining rows are unattempted. Simulated pre-response failures have known-zero
mock usage; this is **not** a policy to assign zero to real failed requests. A
future live adapter must retain reservations or stop on unknown usage. Failed
local sink delivery is recorded without rerunning inference or stopping safe
cases. Local records are retained even if delivery fails.

Latency is measured with a monotonic clock from case execution through local
state serialization; file-write and sink-delivery overhead are outside this
initial timer. Model elapsed sum counts only leaf call receipts; do not add node
and root durations to it. Batch p50/p95 use nearest-rank attempted-case timings,
with their denominator shown. MockTransport callbacks are synchronous test code;
SDK timeouts do not preempt a hanging callback. The separate `smoke.py` runner now enforces process-level timeouts and durable
reservations; this paragraph describes only the original in-process mock path. No cost bar or model-quality bar can be assessed from these results.

## Fixtures and portable verification

`fixtures/development.json` contains two inference-only copies of the first two
inherited V2 development records (issuer-canonicalization family), wrapped with
W4-DEV IDs. They are exposed, programmatically generated development material,
not new independent incidents. No labels were copied. `mock_reply` and
`full_path_reply` are scripted model-output fixtures for boundary coverage, not
expected semantic answers. The first induces an evidence hold; the second
exercises all five real factories with an explicitly unverified hypothesis.

Tests use unittest, without loading inherited pytest conftest, private-history
harnesses or database fixtures. A socket-connect deny guard is active for every
test. They write temporary artifacts only beneath the project's ignored local
virtual environment. Inspected invocation:

```sh
.venv-week4-py311/bin/python -m unittest evaluation.week4.tests.test_offline -v
```

The isolated Python 3.11 environment was created locally; preinstalled third-party
distributions were copied from a local disposable environment. No network install,
original environment file or credentials were used. Package versions are recorded
in run metadata; this environment is not asserted to match the hash-locked baseline
installation. Future reproducibility should sync the lock in a new environment
under separately approved network access if required.

## Supervised SDK integration and verification

`LiveModel` uses supported `OpenAI.chat.completions.create` with strict schemas,
official origin, explicit dedicated key, no automatic retries, no fallback,
non-streamed responses and unchanged inherited prompts/validation. An HTTP response
hook fsyncs actual usage before SDK/output parsing; unknown usage is never zero.
The new `Journal` atomically reserves money/call capacity before dispatch and
records each request attempt separately. Crashes/unknown calls retain reservations;
observed overruns are recorded and block further dispatch. This journal is fresh
Week 4 accounting, with no private/legacy history reconstruction.

`smoke.py` spawns a POSIX session for the case, terminates/kills on timeout and
verifies reaping/session cleanup. It snapshots only actual root/agent/model
boundaries. No tools are configured and skipped stages have no fabricated calls.
Only model spans linked to actual attempted requests survive reconciliation.
Case elapsed time starts before spawn and ends after reaping, durable terminal
journal and reconciliation, before report/export writes. Trace delivery has a
separate process timeout and timer. Timed-out provider work may still incur
remote charges; its reservation remains uncertain, and no automatic retry occurs.

`langsmith_sink.py` uses supported Client create/read methods with explicit
sanitized projections, disabled ambient/batch/OTel instrumentation, no environment
proxy/redirects, and SDK retries disabled. Every expected span is retrieved and
matched against local root/parent/run/case IDs, content, usage, errors and times.
Numeric usage is sent only on model children, avoiding nested usage double counts.
Because inherited redaction strips keys containing “token”, a safe numeric
`usage_counts` metadata projection uses “units”; supported top-level numeric
LangSmith usage fields also retain actual counts. No inherited redaction rule
was weakened. Trace-only export/retrieval uses saved spans and cannot invoke a
model. Remote visibility/backend behavior still needs the future approved smoke.

Additional portable verification (both suites have external sockets blocked;
spawned offline workers enforce their own deny guard):

```sh
.venv-week4-py311/bin/python -m evaluation.week4.dependencies
.venv-week4-py311/bin/python -m unittest evaluation.week4.tests.test_offline evaluation.week4.tests.test_live_sdk -v
```

All model names/rates in SDK fixtures are explicitly test-only. Version checking
now confirms Python 3.11.16 and all 88 inherited pins; archive hash verification
requires a fresh lock-based sync as documented in the smoke plan. No dependency
was added/upgraded and no network install was run.

Remaining private prerequisites: install from the hash lock, verify a compatible
available snapshot and current rates, inspect the development input, configure
new dedicated provider/tracing project credentials and trace privacy/residency,
fill the private plan, and separately authorize exactly one <=5-call / <=$0.25
smoke plus exports. Human review fields stay blank until performed. See the smoke
plan for exact variables and commands. No database or application service is needed.
