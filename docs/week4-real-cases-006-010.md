# Human-reviewed cases 006–010 — import and offline compatibility

All five decisions are **ACCEPTED**, attributed exactly to **User in this
conversation**. Cases 006–009 preserve the v5 acceptances; case 010's new
acceptance and transport-status correction come from the current explicit user
request. Exact review/confirmation times and scores remain null. No independent
reproduction, verified outage, remediation result or additional approval is claimed.

[Corrected review records](../data/week4/reviewed-candidates/batch-006-010/reviewed-candidates.json)
retain the reviewed evidence and qualifications. Original v1/v5 files were copied
byte-for-byte into `batch-006-010/sources/` and left unchanged outside the project.
The derived review record deliberately corrects the erroneous 010 status placement;
it is not represented as a byte-identical v5 copy. Cases 001–005 and their decisions,
provenance, input files and prior import times remain unchanged.

## Five-case result

| Case | Human acceptance / original pending boundary | Status provenance | Missing evidence | Runtime checks and remaining blockers |
|---|---|---|---|---|
| 006 | ACCEPTED, supported media-type diagnosis; mapping pending | Published HTTP transcript: 415; body also reports 415 | Independent reproduction, current-version behavior and fresh runtime evaluation absent | **PASS input/initialization/catalog**, no sanitization changes; inference exported. Empty body, absent Content-Type, handler consumes condition and reportedly successful JSON-header comparison preserved. No claim about every Spring version. |
| 007 | ACCEPTED, supported parameter-binding diagnosis; mapping pending | Published HTTP transcript: 422; validation body identifies required `query` / `token` | Credential values intentionally absent; later reporter resolution excluded from inference; faithful sanitizer-compatible signature representation unresolved | **PASS schema/initialization/catalog, BLOCKED evidence preservation**. Inherited sanitizer damages the dependency signature and removes the reported authorization scheme. No runnable inference export; only evaluator-side sanitized preview. |
| 008 | ACCEPTED, ambiguous evidence; mapping pending | Reporter-stated 404; not upgraded to a captured status line | Response body, exact reporter-owned requests, credentials/permission scope and resource-specific evidence unavailable | **PASS input/initialization/catalog**, no sanitization changes; inference exported. Shown example and unnamed reporter-owned repositories stay distinct; later resolution stays evaluator-only. No common cause for every 404 asserted. |
| 009 | ACCEPTED, supported rate-limit response, scope/cause unresolved; mapping pending | Reporter-stated 429 echoed in error body, not captured status line | Actual headers including Retry-After, quota/scope, request traffic and cause unknown | **PASS input/initialization/catalog**, no sanitization changes; inference exported. No Retry-After value, limit, excessive-user-traffic claim or outage invented. |
| 010 | ACCEPTED, ambiguous media-type rejection; validation pending | Error-body status string **"415" only**; actual transport HTTP status unknown | Wire status, actual Content-Type, boundary and sanitized payload structure absent | **FAIL current input schema / BLOCKED runtime import**. Reviewed `status_code=null`; body string retained in response body and status-evidence metadata. Genuine rejection: `incident.status_code`, `int_type`, "Input should be a valid integer". Initialization/catalog not checked. No 0, 200 or 415 substitute. |

Acceptance, input compatibility, and evaluation eligibility are separate fields in
[runtime-assessment.json](../data/week4/reviewed-candidates/batch-006-010/runtime-assessment.json).
No case is golden-set-ready: even the three input-compatible proposals need
mapping/benchmark review, eligibility/family decisions and actual authorized
runtime evaluation. No final splits or semantic ratings were assigned. The source
proposed happy/edge labels are retained only as evaluator proposals, not accepted
final strata.

## Evidence, mapping and redaction

The input files are under `batch-006-010/inference/`: **006, 008 and 009 only**.
They use the same `InferenceCase`, `Incident`, inherited sanitizer,
`initialize_state` and scalar/handle catalog boundaries as 001–005. No schema,
prompt, routing, grounding, redaction, authorization or publication rule changed.
No artificial log events, request IDs/timestamps, HTTP headers, raw payloads or
observed outcomes were created. Empty log lists remain empty. Unknown severity
and evidence-quality values are existing runtime defaults, not editorial ratings.

The `expected_behavior` strings describe neutral requested operations, not accepted
diagnostic answers. These editorial mapping choices are not newly human-confirmed.
Reported observations remain attributed historical public-report paraphrases, not
independently captured measurements. Case 006's successful header comparison is
legitimate reported evidence rather than an added evaluator answer. Case 008's
example endpoint stays attached only to the example request; separate owned-repo
reports are not rewritten as observations of that same resource.

All accepted expectations, source URLs/dates, family labels, proposed strata,
review decisions, grading qualifications and later source resolutions are kept in
[evaluator-only references](../data/week4/reviewed-candidates/batch-006-010/evaluator-references.json),
not runtime inputs. In particular, 007's later query-based success and 008's later
resolution never enter the inference projection/preview. URL credentials are not
recommended as production authentication. Case 010's expectation requests actual
request/response evidence; missing boundary, invalid UUID and Postman defects
remain unproven hypotheses, confined to evaluator qualifications.

Case 007 exposes two real inherited sanitizer transformations:

| Source field | Reviewed diagnostic content | After inherited sanitization |
|---|---|---|
| `request_metadata.authorization_scheme_reported` | `Bearer` (scheme name, no credential value) | `[REDACTED]` |
| `request_metadata.dependency_code` | `decode_access_token(token: str)` | `decode_access_token(token: [REDACTED]` |

The required-query validation error `loc=["query", "token"]`, message/type,
handler signature and reporter observations survive. The exact dependency
signature does not. The original is preserved in the corrected reviewed evidence
and immutable source copies. No sanitizer bypass, re-encoding trick, replacement
credential or claim of diagnostic equivalence was introduced. A sanitized preview
is evaluator-only and is **not** in the inference directory. Resolve a genuinely
credential-free, source-faithful representation in a separately reviewed mapping,
using the same version for baseline and improved evaluation, or keep the case
blocked. Preserving human acceptance does not require forcing runtime eligibility.

For 010, the reviewed evidence follows the existing missing-value convention used
by cases 001–003: `status_code=null`. It retains `response_body.errors[0].status`
as the string `"415"`, plus explicit `request_metadata.status_evidence` with
body status and unknown transport status. The strict runtime cannot accept null;
that constraint is preserved. The original erroneous integer 415 remains visible
only in the byte-identical archived drafts and explicit correction history.

## Related families and exposure

[family-overlap.json](../data/week4/reviewed-candidates/batch-006-010/family-overlap.json)
flags:

- **006 / 010:** media-type rejection family. A historical empty-body/header
  comparison and an ambiguous multipart failure are different reports, but not
  independent media-type holdout evidence. Their status provenance also differs.
- **004 / 009:** broad rate-limiting/response-ambiguity family. GitHub 403 secondary
  limiting is a hypothesis; Spotify reporter/body 429 supports the response
  category while scope/cause remain unresolved. Do not transfer labels between them.
- **004 / 008:** broader GitHub access/response-ambiguity exposure, with distinct
  resources/symptoms and no proven common mechanism.

The linked Spring duplicate #21955 is not an additional independent incident.
These flags are a bounded overlap inspection, not a full semantic audit of all
inherited generated families. All five cases are development-exposed; prior
model-run history is unknown. No independent holdout or final split is assigned.
Public redistribution rights remain unadjudicated; importing does not publish.

## Provenance and preserved history

Actual import processing time: `2026-10-29T02:22:28.877591+00:00` (UTC). This is **not** a review,
confirmation or source-event timestamp. Source files provide no exact human
review times for this batch; nulls are retained rather than inferred from file
versions, collection dates, or import time.

- v1 draft SHA-256: `c56e7aff05e0b0aede6b4df79691482798de07b32b09f1808ad709998b0e203f`.
- v5 review SHA-256: `682f0b0e1564f79528cb86a7e3048ffafdf9f51e67253dfd1d8561446f50a5df`.

[Import provenance](../data/week4/reviewed-candidates/batch-006-010/import-provenance.json)
records the current-user authority for 010, prior v5 acceptances and the explicit
415-to-null correction with retained body status. The inventory was extended by
exact IDs 006–010 to **225 unique rows**; its earlier **220-row byte prefix** still
hashes to `e636f576e250162a477b937e5eb139430e2106cd4e921f1542f9be596cc19b42`.
Earlier review decisions were not overwritten. The older importer's historical
inventory check/test now validates its original prefix rather than incorrectly
requiring that later batches never append records. Its old import report and
source copy remain untouched; repeated old/new imports verify identity, not
replace differing data or reassign import times.

## Offline verification and next action

Inspected command, using the existing isolated environment with sockets denied:

```sh
.venv-week4-py311/bin/python -m unittest scripts.week4_reviewed_compatibility_tests scripts.week4_reviewed_batch2_tests -v
```

**18 tests passed**: 001–005 regressions, new review/source checks, status correction,
required diagnostic evidence, disclosed redaction losses, source-resolution/label
separation, body-versus-wire status, family flags, append-only inventory and all
328 baseline SHA-256/byte-size checks. The earlier synthetic negative schema probes
remain clearly test-only. No agent graph or provider SDK was imported by these
checks and no models or tools were executed. Exact source-copy identity and
idempotent import behavior were verified separately.

All **328 inherited baseline files match**; the manifest was not regenerated.
The existing synthetic smoke plan and its source bindings were not changed or
executed. No API requests, external tracing, dependency installation, application
services, databases, Docker, commits, remotes, original-project access/change or
spending authorization occurred.

Smallest next actions: review the three faithful editorial input mappings;
resolve 007's signature-preservation blocker without weakening the sanitizer;
obtain authentic transport status and actual media-type/payload evidence for 010,
or retain it as accepted out-of-contract/clarification material. A future nullable
transport contract would require explicit versioning and comparable baseline/
improved inputs; it is not implemented here. None of those decisions is a golden
freeze or permission for paid execution.
