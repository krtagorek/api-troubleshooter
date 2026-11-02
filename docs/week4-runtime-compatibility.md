# Reviewed candidates — offline runtime compatibility

Content review and runtime compatibility are separate. This audit invokes only
input validation, inherited sanitization, state initialization, log parsing of an
empty optional log list, and scalar/handle catalog construction for the supported
proposal. It does not execute an agent graph, model, tool, validation workflow,
provider, trace export, database or service. No inherited behavior was modified.

## Five-case summary

| Case | Human decision | Input compatibility | Primary blockers / qualifications |
|---|---|---|---|
| W4-REAL-001 | ACCEPT_WITH_REVISIONS | BLOCKED | Status, method and path absent. Successful `data.` comparison retained in source; no guessed HTTP 400 or GET. |
| W4-REAL-002 | ACCEPT | BLOCKED | TLS failure has no observed HTTP status; method/path absent. Do not convert it to HTTP 500 or infer POST from SDK creation. |
| W4-REAL-003 | ACCEPT | BLOCKED | No observed status/method/path; `PutObject` is an operation, not a captured endpoint. Keep 1.36.x imprecise. |
| W4-REAL-004 | ACCEPT | BLOCKED | Reported 403 retained; method/path absent. Do not invent POST, `/graphql`, logs or a proven rate-limit cause. |
| W4-REAL-005 | ACCEPT | INPUT_COMPATIBLE_NOT_EXECUTED | GET/302 and path `/` supported; omitted identity preserved. Editorial request-completion goal proposed, not newly human-confirmed. Routing/causal quality untested. |

The original source runtime flags remain unchanged and pending. One proposed
input passed ingress checks; **zero cases were agent-executed or golden-frozen**.
No blocked case was instantiated with invented fillers. The neutral user-goal
mapping is editorial metadata: it is not a claim that a reporter literally wrote
that requirement. If literal reporter requirement wording is required, treat 005
as blocked on that mapping until supplied; do not copy its evaluator diagnosis
into `expected_behavior` to fill the field.

## Contracts and safe rejection evidence

`models/incident.py:Incident` requires nonempty `incident_id`, `service`, `endpoint`,
`expected_behavior`, `actual_behavior`, an allowlisted method and a strict integer
status 100–599. Endpoint is a nonempty **string**, not an absolute-URL requirement;
this permits a reported `/` path without a host. It does not legitimize an invented
nonempty sentinel for an absent path. Optional runtime defaults are empty metadata,
null response body, empty logs, unknown severity and unknown evidence quality.
Unknown severity is not a rating; unknown body is not a captured JSON null.

The Week 4 `InferenceCase` rejects evaluator-only fields before inherited
sanitization, and rejects unknown incident fields. Inherited `incident_from_record`
otherwise allowlists fields, so using it alone would silently omit source fields:
this audit does not feed a whole reviewed source record to initialization.
Catalogs use incident-scoped scalar IDs and trusted root-based provenance; a
resolvable pointer never proves the reported cause or capture provenance.

Wholly synthetic contract inputs verified the actual constraints, with safe errors
recorded in `data/week4/reviewed-candidates/contract-test-results.json`:

| Constraint probe | Genuine rejection type | Relevant cases |
|---|---|---|
| Missing status | `missing` / Field required | 001–003 |
| Null status | `int_type` / Input should be a valid integer | 001–003; no HTTP status for TLS is not a numeric status |
| Missing method | `missing` | 001–004 |
| Null or UNKNOWN method | `literal_error` | 001–004 |
| Missing endpoint | `missing` | 001–004 |
| Null endpoint / empty endpoint | `string_type` / `string_too_short` | 001–004 |
| Missing/null/empty expected_behavior | `missing` / `string_type` / `string_too_short` | User-goal mapping unresolved independently of diagnostic expectations |
| Status 99/600 or string "302" | `greater_than_equal` / `less_than_equal` / `int_type` | Contract bounds only, never values inserted into real cases |

These are 14 negative schema probes within eight tests, not 14 additional real
incidents or model attempts. Synthetic GET/200/path strings exist only in the
clearly named test helper, never in blocked candidate artifacts. We did not
pretend a blocked real mapping was attempted and rejected by the full workflow.

## Field-level maps

Classification means: **observed_report** = statement present in the reviewed
public-report evidence, not an independently observed capture; **derived** =
source-preserving extraction/attributable composition; **editorial_metadata** =
dataset linkage/label or neutral goal; **unknown** = not observed, not filled.
`null` below means no supported value/proposal, never an instruction to coerce a
required field. All seven required fields and all optional defaults are shown.

### W4-REAL-001 — BLOCKED

| Runtime field | Available source observation | Proposed mapping | Classification | Blocker / rationale |
|---|---|---|---|---|
| incident_id (required) | Source case ID W4-REAL-001 | W4-REAL-001 | editorial_metadata | Dataset linkage only; not an observed request/correlation ID. |
| service (required) | Stripe | Stripe | editorial_metadata | Reviewed service label; not independently captured identity. Preserve deliberate omission for 005. |
| endpoint (required) | Charge.list | null / unavailable | unknown | BLOCKED: operation name alone is not an observed path/endpoint. |
| http_method (required) | null / unavailable | null / unavailable | unknown | BLOCKED: no method reported; do not infer from SDK operation. |
| status_code (required) | null / unavailable | null / unavailable | unknown | BLOCKED: missing HTTP status; exception names/TLS failures are not HTTP 400/500. |
| expected_behavior (required) | Reported operation: Charge.list | null / unavailable | editorial_metadata | No explicit user requirement recorded; a neutral operation goal would need editorial mapping. Never copy accepted_expected_behavior. |
| actual_behavior (required) | ["A list request expands application without a data prefix.", "InvalidRequestError identifies application and suggests data.application.", "Reporter states that prefixing the list expansion paths with data. makes the request work."] | null / unavailable | derived | Attributable reports may be joined without causal additions; only 005 has a complete input proposal. |
| request_metadata (optional) | null / unavailable | {} (optional default) | unknown | No request IDs/times/SDK patch versions invented; optional empty default. |
| response_body (optional) | null / unavailable | null / unavailable | unknown | No raw HTTP body supplied; optional null preserved. |
| logs (optional) | [{"source": "reported SDK exception", "message": "This property cannot be expanded (application)."}] | null / unavailable | observed_report | These are attributed exception excerpts, not verified raw telemetry. Empty source list for 004 stays empty. |
| severity (optional) | null / unavailable | unknown | unknown | Runtime unknown default only; no severity rating assigned. |
| evidence_quality (optional) | null / unavailable | unknown | unknown | Runtime unknown default only; accepted review sufficiency is evaluator-only. |

### W4-REAL-002 — BLOCKED

| Runtime field | Available source observation | Proposed mapping | Classification | Blocker / rationale |
|---|---|---|---|---|
| incident_id (required) | Source case ID W4-REAL-002 | W4-REAL-002 | editorial_metadata | Dataset linkage only; not an observed request/correlation ID. |
| service (required) | Stripe | Stripe | editorial_metadata | Reviewed service label; not independently captured identity. Preserve deliberate omission for 005. |
| endpoint (required) | checkout.Session.create_async | null / unavailable | unknown | BLOCKED: operation name alone is not an observed path/endpoint. |
| http_method (required) | null / unavailable | null / unavailable | unknown | BLOCKED: no method reported; do not infer from SDK operation. |
| status_code (required) | null / unavailable | null / unavailable | unknown | BLOCKED: missing HTTP status; exception names/TLS failures are not HTTP 400/500. |
| expected_behavior (required) | Reported operation: checkout.Session.create_async | null / unavailable | editorial_metadata | No explicit user requirement recorded; a neutral operation goal would need editorial mapping. Never copy accepted_expected_behavior. |
| actual_behavior (required) | ["Reporter compares stripe-python 11.4.0 failure with 11.3.0 success under asyncio and HTTPXClient.", "Trace reaches TLS setup; Python versions 3.9.15/3.12.2; macOS/Fedora reported."] | null / unavailable | derived | Attributable reports may be joined without causal additions; only 005 has a complete input proposal. |
| request_metadata (optional) | null / unavailable | {} (optional default) | unknown | No request IDs/times/SDK patch versions invented; optional empty default. |
| response_body (optional) | null / unavailable | null / unavailable | unknown | No raw HTTP body supplied; optional null preserved. |
| logs (optional) | [{"source": "reported client traceback", "message": "httpx.ConnectError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate"}] | null / unavailable | observed_report | These are attributed exception excerpts, not verified raw telemetry. Empty source list for 004 stays empty. |
| severity (optional) | null / unavailable | unknown | unknown | Runtime unknown default only; no severity rating assigned. |
| evidence_quality (optional) | null / unavailable | unknown | unknown | Runtime unknown default only; accepted review sufficiency is evaluator-only. |

### W4-REAL-003 — BLOCKED

| Runtime field | Available source observation | Proposed mapping | Classification | Blocker / rationale |
|---|---|---|---|---|
| incident_id (required) | Source case ID W4-REAL-003 | W4-REAL-003 | editorial_metadata | Dataset linkage only; not an observed request/correlation ID. |
| service (required) | AWS S3 | AWS S3 | editorial_metadata | Reviewed service label; not independently captured identity. Preserve deliberate omission for 005. |
| endpoint (required) | PutObject via upload_file | null / unavailable | unknown | BLOCKED: operation name alone is not an observed path/endpoint. |
| http_method (required) | null / unavailable | null / unavailable | unknown | BLOCKED: no method reported; do not infer from SDK operation. |
| status_code (required) | null / unavailable | null / unavailable | unknown | BLOCKED: missing HTTP status; exception names/TLS failures are not HTTP 400/500. |
| expected_behavior (required) | Reported operation: PutObject via upload_file | null / unavailable | editorial_metadata | No explicit user requirement recorded; a neutral operation goal would need editorial mapping. Never copy accepted_expected_behavior. |
| actual_behavior (required) | ["Reporter uses boto3/botocore 1.36.x with transfer acceleration and s3v4.", "Reporter says disabling acceleration or using boto3 1.35.99 succeeds.", "Environment: Python 3.9.4, Ubuntu 20.04.6."] | null / unavailable | derived | Attributable reports may be joined without causal additions; only 005 has a complete input proposal. |
| request_metadata (optional) | null / unavailable | {} (optional default) | unknown | No request IDs/times/SDK patch versions invented; optional empty default. |
| response_body (optional) | null / unavailable | null / unavailable | unknown | No raw HTTP body supplied; optional null preserved. |
| logs (optional) | [{"source": "reported SDK exception", "message": "SignatureDoesNotMatch"}] | null / unavailable | observed_report | These are attributed exception excerpts, not verified raw telemetry. Empty source list for 004 stays empty. |
| severity (optional) | null / unavailable | unknown | unknown | Runtime unknown default only; no severity rating assigned. |
| evidence_quality (optional) | null / unavailable | unknown | unknown | Runtime unknown default only; accepted review sufficiency is evaluator-only. |

### W4-REAL-004 — BLOCKED

| Runtime field | Available source observation | Proposed mapping | Classification | Blocker / rationale |
|---|---|---|---|---|
| incident_id (required) | Source case ID W4-REAL-004 | W4-REAL-004 | editorial_metadata | Dataset linkage only; not an observed request/correlation ID. |
| service (required) | GitHub GraphQL | GitHub GraphQL | editorial_metadata | Reviewed service label; not independently captured identity. Preserve deliberate omission for 005. |
| endpoint (required) | GraphQL requests using app authentication | null / unavailable | unknown | BLOCKED: operation name alone is not an observed path/endpoint. |
| http_method (required) | null / unavailable | null / unavailable | unknown | BLOCKED: no method reported; do not infer from SDK operation. |
| status_code (required) | 403 | 403 | observed_report | Reported 403 is a symptom, not proof of permission failure or throttling. |
| expected_behavior (required) | Reported operation: GraphQL requests using app authentication | null / unavailable | editorial_metadata | No explicit user requirement recorded; a neutral operation goal would need editorial mapping. Never copy accepted_expected_behavior. |
| actual_behavior (required) | ["Reporter sees bursts lasting seconds, sometimes 20–30 seconds.", "No detailed message reported; reporter says primary quota is not exhausted."] | null / unavailable | derived | Attributable reports may be joined without causal additions; only 005 has a complete input proposal. |
| request_metadata (optional) | null / unavailable | {} (optional default) | unknown | No request IDs/times/SDK patch versions invented; optional empty default. |
| response_body (optional) | null / unavailable | null / unavailable | unknown | No raw HTTP body supplied; optional null preserved. |
| logs (optional) | [] (optional default where proposed) | null / unavailable | observed_report | These are attributed exception excerpts, not verified raw telemetry. Empty source list for 004 stays empty. |
| severity (optional) | null / unavailable | unknown | unknown | Runtime unknown default only; no severity rating assigned. |
| evidence_quality (optional) | null / unavailable | unknown | unknown | Runtime unknown default only; accepted review sufficiency is evaluator-only. |

### W4-REAL-005 — INPUT_COMPATIBLE_NOT_EXECUTED

| Runtime field | Available source observation | Proposed mapping | Classification | Blocker / rationale |
|---|---|---|---|---|
| incident_id (required) | Source case ID W4-REAL-005 | W4-REAL-005 | editorial_metadata | Dataset linkage only; not an observed request/correlation ID. |
| service (required) | HTTP endpoint (identity omitted) | HTTP endpoint (identity omitted) | editorial_metadata | Reviewed service label; not independently captured identity. Preserve deliberate omission for 005. |
| endpoint (required) | GET / | / | derived | Only the path / is explicit in GET /; host remains omitted and no URL is reconstructed. |
| http_method (required) | GET | GET | observed_report | GET explicitly reported. |
| status_code (required) | 302 | 302 | observed_report | Observed/reported 302 only; error_status_hint=400 stays quoted exception text. |
| expected_behavior (required) | Reported operation: GET / | Complete the reported GET / request without a client protocol exception. | editorial_metadata | 005 uses a proposed editorial request-completion goal, not a reporter quotation or new human-confirmed label; accepted diagnostic expectation excluded. |
| actual_behavior (required) | ["Trace records a redirect to HTTPS port 4433 with Transfer-Encoding: chunked.", "A protocol exception follows the redirect response.", "Reporter states curl works."] | Reported observations from the reviewed public-report paraphrase; not independently captured:<br>- Trace records a redirect to HTTPS port 4433 with Transfer-Encoding: chunked.<br>- A protocol exception follows the redirect response.<br>- Reporter states curl works.<br>Quoted reported trace text, not a captured response body:<br>- reported HTTPX trace: h11.RemoteProtocolError; their_state=ERROR; error_status_hint=400<br>No raw response body or endpoint identity is supplied in this reviewed evidence. | derived | Attributable reports may be joined without causal additions; only 005 has a complete input proposal. |
| request_metadata (optional) | null / unavailable | {} (optional default) | unknown | No request IDs/times/SDK patch versions invented; optional empty default. |
| response_body (optional) | null / unavailable | null / unavailable | unknown | No raw HTTP body supplied; optional null preserved. |
| logs (optional) | [{"source": "reported HTTPX trace", "message": "h11.RemoteProtocolError; their_state=ERROR; error_status_hint=400"}] | [] (optional default where proposed) | derived | 005 quotes the existing reported trace in actual_behavior (user source); logs defaults empty, not a claim no trace existed. No synthetic log events. |
| severity (optional) | null / unavailable | unknown | unknown | Runtime unknown default only; no severity rating assigned. |
| evidence_quality (optional) | null / unavailable | unknown | unknown | Runtime unknown default only; accepted review sufficiency is evaluator-only. |

## Case 005 check results and evidence preservation

`inference/W4-REAL-005.json` passes `InferenceCase`/`Incident`, inherited
sanitization, `initialize_state(..., max_retries=0)`, `build_catalog`,
`handle_catalog` and empty-list log parsing. All supplied field values are
unchanged by sanitization. The optional defaults introduced by the existing
schema are reported separately; they are not new observations. No diagnostic
string was lost: GET, 302, HTTPS port 4433, `Transfer-Encoding: chunked`,
`h11.RemoteProtocolError`, `their_state=ERROR`, `error_status_hint=400`, and the
reporter's curl comparison remain literal report content.

There is no HTTP 400 observation: 400 remains in attributed exception prose and
302 is the sole runtime status. The path `/` comes directly from the explicit
operation `GET /`; the service remains exactly `HTTP endpoint (identity omitted)`.
No URL/host/redirect target or request timestamp/ID is created or replayed.
No exact SDK version or severity was invented. Proposed expected behavior merely
asks for the reported operation to complete without a protocol exception; it
contains no chunk-framing diagnosis, recommended fix or evaluator verdict.

The source's existing reported trace excerpt is quoted in `actual_behavior`,
with explicit attribution. It is **not** converted into an artificial log event
or raw response body. Thus the exception remains catalogued as **user** evidence,
without claiming a captured log measurement. Its original structured source
record remains byte-identical in the import. `logs=[]` is the schema default,
not a statement that the original reporter had no trace.

The catalog has four scalar entries: `/actual_behavior`, `/expected_behavior`,
`/status_code`, `/response_body`. The last is the inherited **unknown null default**,
not an observed null body. Metadata/log defaults add no fabricated scalar facts.
Catalog sources are `user` and `response`; these are schema root conventions, not
signed third-party provenance or independent confirmation.

The source's accepted expectation to investigate malformed/missing chunk framing
is evaluator-only. No maintainer hypothesis is inserted into inference prose.
Other cases likewise keep accepted explanations, contributor opinions, source
URLs/display headings, family and grading notes outside runtime inputs. Literal
reporter observations such as the successful `data.` comparison in 001 are
retained as evidence, even if they strongly suggest the reviewed expectation.
Source-faithful evidence is not equivalent to leaking an added evaluator answer.

## Boundaries still not checked

For 001–004: real-case input construction, sanitization loss, initialization,
catalog and graph/model stages are NOT_CHECKED because no supported complete
projection exists. Their validation blockers are established by field inspection
plus the separate synthetic constraints, not execution with guessed fillers.
No redaction rejection is claimed where redaction was never attempted.

For 005: ingress/catalog pass is not full workflow compatibility or causal quality.
No evidence selection, readiness, routing, root-cause, resolution, publication or
validation stage was executed. Static inspection of `diagnostic_sufficiency.py`
shows its qualified-analysis gate searches structured `/logs/` comparisons or
specific exception fields. This conservative projection has no `/logs/` entries;
a user-prose exception cannot be assumed to exercise those routes. We did not
manufacture structured facts to get around that guard. A reported curl success
is not this agent's successful remediation, and absent validation remains untested.
The expected-behavior editorial mapping has not received an additional human
confirmation. The case remains development material, not reserved evidence.

## Options for each blocker; none implemented

| Case / blocker | A — collect source evidence | B — retain for validation/clarification | C — future versioned unknown-aware input | D — replace if impractical |
|---|---|---|---|---|
| 001: missing status/method/path; requirement wording | Ask for an authorized sanitized request/response or contemporaneous explicit method/path/status and operation requirement; retain successful `data.` comparison | Evaluate missing-field ingress rejection; current agent cannot be credited for a clarification it never generated | Allow explicitly unavailable transport fields with attributed reported observations | Use another genuinely distinct documented parameter-validation episode; do not relabel a paraphrase of this incident |
| 002: TLS has no observed HTTP response; missing method/path | Collect method/path and trust/TLS diagnostics if available; do not seek a fictional status or a patched version that was never reported | Retain as an out-of-contract transport/clarification example, separately counted | Model non-HTTP transport failure with absent status, preserving certificate-mechanism/underlying-defect distinction | Replace with a documented HTTP-stage incident only if HTTP-only scope is required; retain this accepted record in inventory |
| 003: absent raw status/method/path and precise 1.36 patch | Request sanitized original response metadata and exact versions where authentic; no signed URLs, credentials, or invented patch numbers | Check ingress missingness separately; no credential/checksum diagnostic score | Permit unavailable fields and explicit version uncertainty; separate reporter comparisons from other commenters | Replace with a complete version-interaction report if authentic missing details cannot be obtained |
| 004: 403 known, method/path/body/headers/pattern absent | Request observed method/path, sanitized response metadata and timing/concurrency/quota evidence, without asserting secondary limiting | Retain ambiguity and missingness for ingress clarification; status alone is not a supported diagnosis | Represent unknown method/path and maintain competing hypotheses in evaluator-only expectations | Use a distinct sufficiently documented ambiguous API report; no automatic POST or `/graphql` substitution |
| 005: proposed editorial goal, no raw framing/capture and no structured qualifying log facts | Review the neutral user-goal mapping; collect authentic sanitized trace/body/framing information if available, while keeping endpoint identity omitted | Keep as input-validation/clarification material; do not claim model-stage coverage from catalog success | Design explicit reported-exception evidence with source attribution and unknown host/body semantics; no synthetic logs or weakened guard | Replace only if actual qualified-analysis coverage is required and honest evidence collection is impractical; generic transport scope acceptance is preserved |

**Comparability consequences:** A changes evidence and therefore case/dataset
version. Collect before benchmark freeze, or rerun both baseline and improved on
the same revised version; it is development-exposed, not newly independent.
B changes the evaluation task/denominator: ingress validation can be scored
separately, but a rejected input is not an attempted agent diagnostic case or a
verified agent trace. C changes the contract/baseline boundary: implement only in
a future separately versioned design and establish comparable baseline/final
inputs under that version. Never apply a mapping workaround only to one arm.
D changes case membership, strata and family coverage; before freeze re-review
and version the selection, after freeze rebaseline the changed benchmark instead
of claiming a paired delta on different cases. Replacements must not manufacture
independent incidents from alternate wording of the same report.

## Recommended next action and unresolved decisions

First review the case-005 editorial requirement/projection and decide its intended
role (ingress/clarification versus later diagnostic coverage); collect source
metadata for 001–004 where it actually exists. No live or mock model is needed
for that decision. For TLS, retaining the accepted case may require option C or
an explicit out-of-contract task, not more aggressive filling of the current
schema. Clarify public redistribution permission and any historical use before
claiming sourcing independence or publishing. Additional human review is optional,
not fabricated. Do not change the inherited contract or repurpose the synthetic
smoke plan as part of this import.

Verification command (isolated existing Week 4 environment, network denied):

```sh
.venv-week4-py311/bin/python -m unittest scripts.week4_reviewed_compatibility_tests -v
```

**8 tests passed**, including 14 synthetic negative constraints and all 328
inherited SHA-256/size checks. Original source JSON/HTML and the synthetic smoke
plan/source bindings remain unchanged. No graph/model/provider SDK was imported
by these tests, no service/database was contacted, no dependencies were installed,
and no tracing, spend, commit, remote or original-project change occurred.
