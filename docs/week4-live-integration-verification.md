# Week 4 SDK integration — offline verification

Supported provider/LangSmith implementation and offline tests only. No paid model
call or external trace export was made or authorized. No database, Docker,
application service, original credentials, historical dispatcher, private ledger,
commit or remote was used or created. The original Week 3 project/environment
was not accessed or changed.

## Implemented boundaries

- `live_provider.py`: supported OpenAI SDK on the fixed official endpoint, strict
  wire schema with inherited handle constraints, unchanged inherited factories/
  prompts/safety validation, no retries or fallback. A response hook captures
  provider usage in the durable journal before SDK and output/schema parsing.
- `accounting.py`: fresh append-only JSONL journal, exclusive locks, fsync before
  dispatch and after received usage. Separate reservation and request-attempt
  events; money/call caps; partial/unknown usage retains reservations and stops.
  Actual observed overruns remain visible; no fabricated zero usage or invoices.
- `smoke.py`: one real inherited graph in a spawned POSIX session; process timeout,
  terminate/kill/reap and session cleanup verification. Each attempted call has
  stable case/root/span/journal linkage. Interrupted started spans are marked
  interrupted; unattempted model work and skipped stages get no fabricated calls.
- `langsmith_sink.py`: supported Client create/read methods with explicit sanitized
  inputs/outputs and numeric usage; ambient, batch and OTel tracing disabled.
  Post-inference export in a separately bounded process. Retrieval matches every
  expected local UUID, parent/root/run/case link, content, timing, error and usage.
  Trace-only export/retrieval cannot invoke an inference worker.
- `live_cli.py`: offline unresolved plan preparation; future live/export/retrieval
  commands require explicit flags. No new consent registry, signed approval
  system or legacy history requirement was introduced.
- `requirements.lock`, `requirements.in`, `.python-version`, `dependencies.py`
  under `evaluation/week4/`: inherited full hash lock reused unchanged, no added
  or upgraded packages. All 88 installed pins plus Python 3.11.16 verified.

The primary supervised timer includes process startup/imports, graph/model work,
durable child output, termination/reaping, fsynced terminal journal and local
reconciliation. Final report writes and tracing are excluded. Trace duration is
separate. Model elapsed totals sum only ended attempted-call records; interrupted
leaf durations remain incomplete/null, never zero or nested-span double counts.
The old in-process mock timer is separately documented in the adapter README.

## Portable test result

Inspected invocation, no inherited pytest/private-history/database fixtures:

```sh
.venv-week4-py311/bin/python -m unittest evaluation.week4.tests.test_offline evaluation.week4.tests.test_live_sdk -v
```

**31 tests pass.** Parent tests and spawned mock workers block external sockets.
Both real SDKs are exercised through local httpx2/requests test transports.
Coverage includes all five inherited stages; strict output handling; label
isolation; actual root/node/model boundaries; usage and timing; ordinary failure
continuation; parser errors with retained known usage; missing usage; one-attempt
transport errors; child interruption; blocked transport killed by process timeout;
verified cleanup; money/call limits before dispatch; observed overruns; torn
journals; trace failure without inference repetition; trace retrieval mismatch;
trace-only recovery; explicit redaction; and traced/untraced request/output parity
with ambient tracing enabled in the parent. Model names, rates, responses and
usage in these checks are expressly **test data**, not spending/quality evidence.

## Integrity and remaining work

All **328 inherited files** match the baseline manifest by SHA-256 and byte size,
including inherited application files, datasets and dependency lock. Only new
Week 4 implementation/tests/fixtures/lock references and Week 4 documents changed.

[The smoke/setup plan](week4-smoke-plan.md) describes exact private setup and
future commands. `data/week4/smoke-plan.json` binds one exposed synthetic
DEVELOPMENT case, keeps model/rates unresolved, limits calls to <=5 and proposes
$0.25. Human review fields are null; no semantic labels or golden set were made.
The $10 envelope and evaluation bars remain proposed.

Current tests verify installed versions; a fresh --require-hashes sync is prepared
but was not executed. Distribution-archive integrity must be verified on that
fresh installation before live use. Remote account/model/schema availability,
current rates, live transport/trace behavior, regional deployment and eventual
visibility remain unverified until a separately authorized smoke. Provider-side
work may continue after local cancellation, so uncertain reservations are kept;
local timeout cannot promise cancellation of remote billing. File locks/fsync and
process supervision were tested on macOS/Python 3.11, not Windows or power-loss
hardware. Source/case hashes must be regenerated if implementation changes.
