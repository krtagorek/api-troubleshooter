# One development smoke — prepared, not authorized or executed

Implementation and offline tests only are authorized. The proposed maximum is
**$0.25**, one case, at most five model calls, concurrency one, zero SDK/workflow
retries, no fallback, no diagnostic tools, no database/checkpoint or service.
The overall $10 envelope and evaluation thresholds remain proposed. No rates or
model selection have been verified or populated by this implementation.

`data/week4/smoke-plan.json` is an offline, unresolved machine-readable proposal.
It binds the exact inference-only W4-DEV-1 input and source/dependency hashes.
The input is a copy of the inherited V2 issuer-canonicalization development
variant, not a real incident or independent reserved example. No evaluator labels
are attached. A genuine human should inspect the sanitized input and resulting
output; reviewer, timestamp and confirmation fields stay blank until that occurs.
No golden dataset is frozen by this smoke proposal.

## Reproducible setup inside this new project

No dependencies were added or upgraded. `evaluation/week4/requirements.lock`
includes the inherited complete hash-locked `requirements.lock`; the adjacent
`requirements.in` lists direct imports. Both HTTPX generations are deliberately
retained: inherited LangChain uses httpx while the pinned OpenAI 3.35.1 SDK uses
httpx2. LangSmith uses its supported requests session. All are already locked.
The target is Python **3.11.16**, macOS ARM64 (the inherited lock's tested platform).
The process supervisor requires POSIX sessions/signals; Windows is unsupported.

All 88 installed pins and Python match the lock in the existing Week 4 test
venv. Installed versions were checked, not rehashed/reinstalled distribution
archives. To create a clean hash-verified installation privately:

```sh
.venv-week4-py311/bin/python -m venv .venv-week4-locked
uv --cache-dir .cache/week4-uv pip sync --python .venv-week4-locked/bin/python --require-hashes evaluation/week4/requirements.lock
.venv-week4-locked/bin/python -m evaluation.week4.dependencies
.venv-week4-locked/bin/python -m unittest evaluation.week4.tests.test_offline evaluation.week4.tests.test_live_sdk -v
```

The sync command was **not executed** here. It may require network permission
when distribution archives are not locally cached; it writes only the new
project environment/cache. Do not sync or activate the original Week 3 environment.
No original credentials/configuration are needed for these checks.

## Model and pricing decisions you must complete

Choose an available, explicit model snapshot that supports Chat Completions,
strict JSON Schema, temperature 0 and `max_completion_tokens`. Verify the current
model capabilities and your project access. An alias or default is not a verified
snapshot; incompatibility must block the smoke, not silently change parameters
or models. No availability call is performed during planning.

Verify official current input/output USD-per-million rates for that snapshot,
and its cached-input rate if caching can occur. Fill the private plan's `model`,
`input_per_million`, `output_per_million`, `cached_input_per_million` where
applicable, `pricing_source` and actual `pricing_verified_at`. These are provided
verification records, not automatic proof of pricing/account access. Never copy
the arbitrary test-only fixture rates. Missing cached-input pricing with reported
cached usage retains the reservation and stops rather than inventing a cost.

The complete request is rejected if its byte length plus 4,096 allowance exceeds
the configured input reservation (default 32,768); output cap is 1,536. Check that
five full worst-case reservations fit $0.25 at the verified rates. The journal
reserves worst-case cost before each attempted dispatch. Refuse dispatch if money
or call limits cannot accommodate it. Byte/framing bounds and provider-side
controls are conservative operational protection, not an absolute invoice
promise; observed overruns are recorded honestly and stop execution.

Official implementation references:
[OpenAI Python SDK](https://developers.openai.com/api/reference/python),
[Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs),
and [LangSmith manual tracing guidance](https://docs.langchain.com/langsmith/trace-with-api).
These establish interfaces, not current pricing or this account's availability.

## Private variables and projects

Use a new dedicated provider project/key and new LangSmith project/key. No
resources are provisioned by this code. Configure project spend controls/alerts
where available and choose trace access/retention deliberately. Keep secrets
private; do not place them in the plan, command arguments, reports or chat.

In a new project-only `.env.week4` (already ignored), set:

- `WEEK4_OPENAI_API_KEY`: new provider project credential.
- `WEEK4_LANGSMITH_API_KEY`: new tracing credential.
- `WEEK4_LANGSMITH_PROJECT`: exact new project name, e.g. `api-troubleshooter-week4-eval`.
- `WEEK4_LANGSMITH_PROJECT_ID`: project UUID, recommended and required by SDK retrieval on SmithDB-only deployments.
- `WEEK4_LANGSMITH_WORKSPACE_ID`: workspace UUID if required by your key/account.

The file is not read automatically. Load only this file in a clean shell when
ready; the child discards ordinary OPENAI/LANGSMITH/DB settings and disables
ambient tracing. It explicitly points SDK profile loading at a nonexistent file
inside the new run directory; it never reuses a personal/original SDK profile.
The provider endpoint is fixed to official HTTPS. LangSmith defaults to US;
select a supported regional allowlisted endpoint with `--langsmith-endpoint`
only after confirming project residency. Environment proxies and redirects are
disabled. No external diagnostic tool or application service is started.

## Prepare privately; execute only after explicit authorization

If source/dependency hashes have changed, prepare a fresh unresolved proposal:

```sh
.venv-week4-locked/bin/python -m evaluation.week4.live_cli plan --output data/week4/smoke-plan-next.json
```

Copy the current proposal to an ignored private file, fill only verified model/
pricing settings, inspect the input/redaction and caps, and retain source/case
hashes. Regenerate a new proposal after code or input changes. For example:

```sh
mkdir -p reports/week4
cp data/week4/smoke-plan.json reports/week4/smoke-plan-private.json
```

The following is a **future command, not executed or approved by this task**.
Run only after separately authorizing this exact paid case and trace export:

```sh
set -a
source .env.week4
set +a
.venv-week4-locked/bin/python -m evaluation.week4.live_cli run --plan reports/week4/smoke-plan-private.json --output reports/week4/live-smoke-001 --execute-live --export-traces
```

No extra paid connectivity call is needed. The case's 120-second process timeout
includes spawn/imports/inference and durable child output; supervisor termination
and reaping add at most the documented cleanup grace, subject to OS scheduling.
The primary timer starts before process launch and ends after verified reaping,
fsynced terminal journal and local reconciliation. Final report writes and trace
export are excluded. Trace export runs in a separate process with a 30-second
limit and its own duration. Model timings count leaf attempts only; never add
nested span durations to them. The old in-process mock runner retains its
separately documented timer and is not live latency evidence.

Review `result.json`, `journal.jsonl`, `spans.json`, `review.json`,
`trace-status.json` and `artifact-hashes.json`. Only model spans with actual
request-attempt records are exported. Started spans interrupted by termination
are closed as interrupted; skipped stages do not acquire children. Known usage
is journaled before output parsing; unknown or interrupted calls keep their full
reservations, cost stays incomplete, and no further dispatch occurs. Do not
reset a journal or assume a new output directory reconciles uncertain spend.

SDK trace delivery is synchronous, without automatic inference retry or ambient
instrumentation. Retrieval compares every expected UUID, parent/root/case/run
link, input/output projection, timing, error and numeric usage. Eventual remote
visibility or backend-specific configuration can require later trace-only work.
A failed trace export is never grounds to rerun inference. Future explicitly
authorized trace-only commands use only saved spans and a separate new directory:

```sh
.venv-week4-locked/bin/python -m evaluation.week4.live_cli trace-only --source reports/week4/live-smoke-001 --output reports/week4/trace-check-001 --retrieve-traces
.venv-week4-locked/bin/python -m evaluation.week4.live_cli trace-only --source reports/week4/live-smoke-001 --output reports/week4/trace-delivery-001 --export-traces
```

Re-delivery reuses IDs and must verify any existing records; it cannot repeat a
model call. Human causal review is still required; neither trace completeness nor
a supported tentative report proves a diagnosis or tested fix. NOT_TESTED remains
NOT_TESTED. One smoke does not establish benchmark accuracy or production quality.
