# Human-reviewed incidents 011–015 — import and input compatibility

All five authoritative user decisions are recorded as **ACCEPTED**, attributed
exactly to **User in this conversation**. Cases 011–014 retain the v5 acceptances;
015 was accepted after v5 and is recorded from the current explicit instruction.
Exact review/confirmation/recording timestamps and semantic scores remain null.
The actual import processing time `2026-10-29T02:30:56.018274+00:00` is provenance only, never
substituted for human review time. No signatures, independent reproduction,
verified remediation or additional confirmations were invented.

## Counts and result

Counts are for **this five-case import**, not benchmark performance:

| Category | Count | Meaning |
|---|---:|---|
| Human-accepted | 5 | Content/scope decisions only |
| Schema-compatible | 5 | Existing `InferenceCase` / `Incident` accepted the proposed mappings |
| Evidence-preserving input-compatible | 5 | Sanitization unchanged; initialization and scalar/handle catalogs passed |
| Graph-executed | 0 | No graph, agent, provider, model or validation workflow executed |
| Golden-set-ready | 0 | Mapping/eligibility/family review and benchmark preparation remain pending |

The inventory now contains **230 unique IDs**, preserving its entire earlier
225-row byte prefix. Neither accepted review nor passing ingress marks a case
runtime-ready or independently held out. All normalized source `runtime_ready`
flags remain false; original pending human-review runtime statuses are retained.
No final splits or stratum labels were assigned.

## Per-case provenance, mapping and remaining uncertainty

| Case | Accepted qualification and status provenance | Editorial runtime expected_behavior | Missing evidence / remaining blockers | Input result |
|---|---|---|---|---|
| 011 | Supported missing-authorization category, underlying cause unresolved. Published server-access-log report pairs **GET /api/list-files / 401** with adjacent **Missing Authorization header** warning | List the reporter's generated files through the reported GET operation | Original complete request/header capture and missing-header cause unavailable. Changed port 3001, image 0.15 and Linux remain reported context, not causal proof. Do not merge later invalid-token comments; no expiry/signing-secret/port fix confirmed | PASS schema, unchanged sanitization, initialization and catalog; no hard input blocker |
| 012 | Supported JSON-parsing category, exact defect unresolved. Client exception reports **POST /euronews/mytable/1266?pretty=true / HTTP 400** | Submit the intended document to the reported POST operation | Exact original request bytes and a confirmed correction are unavailable. Parent mapper_parsing_exception and nested json_parse_exception, character f/code 102, **line 2 column 45**, remain intact. Later mapping advice/another error is not this request's verified repair | PASS schema, unchanged sanitization, initialization and catalog; no hard input blocker |
| 013 | Supported method-routing category and reported missing-Allow defect. HTTPie **PUT / / 405**; GET-only route and GET / → 200 comparison | Return an **informative rejection** for the reported unsupported PUT request, consistent with its configured route | No full allowed-method list or reproduced upgrade outcome. Preserve actix-web 3.3.2, content-length 0 and “no Allow header shown.” PUT success is not the intended contract | PASS schema, unchanged sanitization, initialization and catalog; no hard input blocker |
| 014 | Reporter write/response inconsistency and duplicate-retry risk, exact server defect unresolved. Curl **POST /api/issues/5a773a8c-85e8-4668-a72e-b7feff2ce14a/children / HTTP 500** | Create the requested child issue and return a response consistent with the write outcome | Persistence after this request and duplicates after repeats remain **reporter statements**, not verified database observations. Exact payload/failure point absent. Evaluator expectation checks existing state before replay and rejects blind retries; no confirmed serialization/transaction/code defect | PASS schema, unchanged sanitization, initialization and catalog; no hard input blocker; no write/replay executed |
| 015 | Supported route/handler rejection, cause unresolved. Curl **POST /_plugins/_sm/policies/snapshot_policy / HTTP 400** and no-handler body | Submit the intended snapshot policy through the reported POST operation | Actual deployed API/plugin support and root cause unresolved. Preserve reported Content-Type application/json, OpenSearch 2.0.1, Graylog 5.0.3 and exact no-handler response. No malformed JSON, absent plugin, licensing, POST-to-PUT change or different snapshot API is a confirmed fix | PASS schema, unchanged sanitization, initialization and catalog; no hard input blocker |

The operation goals are explicitly **editorial mappings**, not quotations or newly
human-confirmed labels. They do not copy evaluator diagnoses. For 013, the current
instruction explicitly identifies informative rejection as the intended operation
contract; the mapping does not require an unsupported write to succeed. For 014,
“check existing state before replay” is an evaluator diagnostic/safety criterion,
not permission to run the endpoint. All actual observations remain source-attributed.

Remaining blockers are to **diagnostic evaluation/eligibility**, not hidden failed
ingress checks: review the editorial mappings, evidence sufficiency and family
assignments; retain unresolved causes rather than converting category support
into a confirmed defect. No mapping has been scored or validated by a model.

## Evidence separation and loss checks

The separate artifact structure is
`data/week4/reviewed-candidates/batch-011-015/`:

- `sources/`: exact v1 and v5 bytes, including stale source NOT_REVIEWED flags.
- [reviewed-candidates.json](../data/week4/reviewed-candidates/batch-011-015/reviewed-candidates.json): normalized authoritative decisions; all five case-level flags reflect acceptance without changing raw archives.
- [evaluator-references.json](../data/week4/reviewed-candidates/batch-011-015/evaluator-references.json): URLs, dates, families, proposed/accepted expectations, review decisions and later contributor interpretations.
- `inference/W4-REAL-011.json` through `W4-REAL-015.json`: five separate proposed typed inputs; none is a smoke plan or approved execution target.
- [runtime-assessment.json](../data/week4/reviewed-candidates/batch-011-015/runtime-assessment.json): per-case checks, editorial-goal flags, unknowns and separate eligibility states.
- `family-overlap.json`, `import-provenance.json`, `inventory-update.json`, `verification.json`: source/family review and reproducible import/check evidence.

**No supplied diagnostic evidence changed through mapping/sanitization.** Every
source observation is retained literally in attributed `actual_behavior` prose;
response-body excerpts remain structurally equal to the supplied source. Required
warnings and exception locations are preserved. Empty `logs=[]` stays empty:
we did not fabricate timestamped/structured log events, even for the reported
server access log and adjacent warning in 011. Catalog provenance for those
quoted statements is **user** evidence, not a signed or independently captured
log. Passing catalogs cannot establish that later structured-log readiness gates
will be exercised; selection/readiness, routing and publication were not run.

Metadata states that any body is a **reported excerpt with completeness unknown**,
not full raw response bytes. Null bodies in 011/013 mean not supplied, not captured
JSON null; catalog null defaults must not be interpreted as observed wire data.
No allowed-method header list, Authorization value, corrected payload, complete
raw headers, host, timestamp, request ID, outcome or severity was invented. The
issue UUID in 014's supplied endpoint is preserved exactly; no request/run ID is
promoted into source evidence. Unknown severity/evidence-quality values are
existing runtime defaults. The generated offline-check thread identifier is only
local validation context and is absent from the proposed incident inputs.

Projection inspection/tests exclude review fields, accepted expectations, source
URLs/dates, family labels and later advice. Inference contains the reporter's
GET comparison, missing-header warning, parser exception and persistence claims
because those are reported observations; it contains no added diagnosis, fix or
claim of independent confirmation. No later token symptom, mapping fix, version
milestone repair, serialization theory or different snapshot API advice was
inserted into an inference input.

## Source/family overlap

The importer compared exact source URLs against 001–010 and exact family labels
against all **225 prior inventory IDs**. No exact prior source URL or family-label
match was found for these five. That does **not** establish semantic independence:

- 011 shares broad authentication/header-delivery exposure with 007 and inherited
  V1's stripped-Authorization family. Query binding and a missing header are not
  thereby the same proven cause.
- 012 has broad request parsing/validation exposure alongside 001, 006 and 010;
  syntax, parameter paths and media negotiation remain different mechanisms.
- 013/015 share broad method/route availability questions but different reported
  behavior and uncertainty.
- 014 shares only broad server-error symptoms with inherited generated examples;
  related source issues **#6529 and #3310** must not become independent incidents
  automatically. Alternate descriptions remain within an episode/family review.

All cases are development-exposed AI-curated public reports, not independently
reproduced captures or verified outages. Earlier model-run history is unknown.
This local comparison is not a full semantic/contamination audit. Final grouping,
splits and redistribution rights remain unresolved; no publication is authorized.

## Import identity and idempotence

Source hashes:

- v1: `7eaf6dcd1169bf11ccbf139cf53b76f2f46a0cb846e68388400783df8cf6773e`.
- v5: `0ff93d69a63a7e98aadbce8c9f5184b079f943e6f12c2837bc329b0730c23c63`.

Draft/v5 inference evidence was checked for identity before normalization. Exact
source copies and previous review artifacts are hash-checked. A second import
must match existing records or fail without overwriting differences; actual
import time remains unchanged on repetition. The entire new JSON tree and
inventory were verified byte-identical after repetition.

**19 prior review JSON artifacts** remain unchanged, including the
001–005 and 006–010 records/decisions and their original import times. The earlier
batch's historical inventory check now accepts an unchanged original prefix plus
later append-only rows, rather than forbidding future batches. No earlier review
record or historical import report was overwritten. The old 225-row prefix has
SHA-256 `d55dde9f418447033216dcc06867d73ac7f5af002f2d8a332e1dfc33fe5cedb6`; the resulting inventory has SHA-256
`ba82e186f1fb9ced192f2c7727260864414c6e96d9c121e99eb7e405aa8df537`.

## Verification

Inspected portable invocation in the existing isolated Week 4 environment:

```sh
.venv-week4-py311/bin/python -m unittest scripts.week4_reviewed_compatibility_tests scripts.week4_reviewed_batch2_tests scripts.week4_reviewed_batch3_tests -v
```

**28 tests passed**, with socket/DNS access denied. They include earlier-import
regressions, new decisions/source identity, all source-specific evidence and
operation goals, excerpt qualifications, label exclusion, exact observed paths,
idempotence, overlap/count discipline and hash preservation. No graph or provider
SDK was imported by the tests; no model mock or agent execution was needed.

**All 328 inherited baseline files match SHA-256 and byte size.** The existing
manifest was not regenerated. Inherited contracts, prompts, routing, sanitization,
grounding, safety/authorization and validation rules were untouched. The original
project and credentials were not accessed. No models, trace exports, incident/API
requests, dependency installation, services, databases, Docker, commits/remotes
or smoke execution occurred. The existing synthetic smoke proposal and its source
bindings remain unchanged.

Smallest next step: review the five editorial operation goals and bounded source/
family roles before considering a frozen dataset. Collect missing causal evidence
only if available; keep unresolved hypotheses explicit. Do not replay the write
endpoint, manufacture data to exercise routing, or infer runtime/quality approval
from these input-only passes.
