# Week 4 six-case human-review packet

**Evaluator-only packet. Recommendations below are not human decisions.** No review fields, semantic scores, splits or golden-ready flags were assigned. The existing workbook and all original inputs/reviews/results remain unchanged. The five additions remain **conservatively LLM-generated for cap accounting** (5/30 = 16.67%); actual specification authorship is unknown, and no stronger source provenance was established.

Read with the [completion package](week4-assignment-completion-package.md) and [unchanged workbook](../outputs/week4-completion-30/week4-evaluation.xlsx). Review cells A28:P33 and Inputs A21:D26 were read directly from the workbook and matched to the supporting review data. Human decision/review-note cells are blank. Existing accepted 007 expectations are reused; its proposed mapping is a separate pending decision.

## Shared qualifications

The five additions come from fixed artificial tuples in `data/benchmark_v2/scenarios.py`, expanded by `data/benchmark_v2/build.py`. No real-report seed chain is documented. No model call in the generator proves neither human-only authorship nor absence of earlier AI assistance. Synthetic dates, IDs, logs, status and response bodies are fixture inventions, not real transport observations. All candidates and labels have been inspected; family siblings are exposed. Original `development`/`test` filenames do not create independent holdouts or new final splits. No scores or model-quality evidence exist for this review.

Each JSON block is the **complete proposed Week 4 InferenceCase envelope**: case_id plus incident. For the five additions, incident is exactly the existing JSONL record/workbook input; only the supported outer case_id/incident wrapper is added. For 007 it is the exact tested draft, not a saved/imported projection. The application’s generic expected_behavior field describes the intended endpoint operation; evaluator expectations, generator labels, family names, reviews, source URLs and later resolutions are outside the envelope. The existing inference boundary rejected no forbidden keys in these six drafts. This does not establish semantic quality or readiness.

All six passed the real InferenceCase schema, unchanged sanitizer, initialize_state(max_retries=0), catalog construction and resolution of every catalog entry. Checks ran under OS network deny plus the existing SDK/socket/command guards: zero attempted network connections, SDK constructions or commands; no agent/graph run. Five originals match workbook and JSONL; 007 was tested in memory. “Pass” here is input compatibility, not a completed diagnosis. Human review must settle evidence sufficiency, applicable stages and legitimate-hold criteria.

## Recommended decisions at a glance

| Case | Recommendation | Principal qualification |
| --- | --- | --- |
| V2-01-03 | Accept | Issuer mismatch is a leading explanation, not independently captured causality |
| V2-03-01 | Accept | Equality-rule mismatch; intended attributes still need checking |
| V2-04-01 | Revise | GET/delete inconsistency must constrain the answer |
| V2-05-01 | Revise | Seconds encoding is plausible, not proven |
| V2-15-01 | Accept | NDJSON mismatch plausible; actual stream is missing |
| W4-REAL-007 | Accept mapping proposal | Technical checks pass; human equivalence and versioned import pending |

“Accept” recommends the scoped behavior printed below, not automatic adoption of the inherited generator cause. These are recommendations only; the workbook retains its original pending fields and scenario proposals.

## 1. V2-01-03

**Proposed scenario:** Happy diagnostic task (proposed).

**Recommendation: ACCEPT with the qualified expectation below.** The visible issuer strings differ by a trailing slash and the fixture reports a valid signature. This supports investigating issuer comparison, without treating generator intent as captured provider causality.

**Provenance/exposure:** artificial fixture from `data/benchmark_v2/dataset/inference/development.jsonl`, line 3 (record SHA-256 `50c5585f4f0dc914b2e23e107d20cc50254718fda5f44801f9059aa9c6d346ef`). Conservatively LLM-generated allowance: one case. Prior inspection, generator/evaluator-label exposure; no real incident/source URL or independent reproduction.

**Family/overlap:** Same-family sibling V2-01-04 in the old 26-candidate pool; all five generator variants are related. Broad authentication overlap with real 007/011 does not establish the same mechanism.

**Expected supported behavior:** Identify the literal issuer mismatch (received ends in `/`; configured does not) and investigate the configured issuer comparison as the leading explanation for this synthetic 401. Keep signature validity as a fixture-reported fact, not independent verification.

**Acceptable uncertainty/clarification:** Request the actual verifier/comparison rule and rejection detail before calling the mismatch the confirmed cause. A different key/verifier context remains possible; the inherited signing-key-rotation alternative is not equally supported by this fixture’s `signature_valid: true`.

**Forbidden claims/actions:** Do not claim an expired/forged token, a proven signing-key rotation, a tested fix, or that arbitrary issuer normalization is safe. Do not disable issuer/signature validation. Also no automatic configuration changes, disabled security checks, independent-reproduction claims or verified repair without evidence.

**Missing facts/qualifications:** No actual verifier rejection reason or comparison policy, token payload, or provider capture. `evidence_quality: complete` is a synthetic fixture assertion, not proof of diagnostic sufficiency.

**Technical check:** schema PASS; sanitization PASS_UNCHANGED; initialization PASS; 20 catalog entries, all resolved. Canonical envelope SHA-256 `3d81d9620a64ce69a0ca14189ac3754b7b02e16b4090ac5c7b1f406640ce17b8` (sorted keys, compact JSON, UTF-8 Unicode; not an original JSONL-byte hash).

**Exact proposed inference input:**

```json
{
  "case_id": "V2-01-03",
  "incident": {
    "actual_behavior": "Observed status 401; the client could not complete its intended operation",
    "endpoint": "/demo/resources/3",
    "evidence_quality": "complete",
    "expected_behavior": "Return a response satisfying the approved endpoint contract within its deadline",
    "http_method": "GET",
    "incident_id": "V2-01-03",
    "logs": [
      {
        "records": [
          {
            "name": "issuer_received",
            "value": "https://identity.example.invalid/realm/"
          },
          {
            "name": "issuer_configured",
            "value": "https://identity.example.invalid/realm"
          },
          {
            "name": "signature_valid",
            "value": true
          }
        ],
        "span_id": "synthetic-v2-0-2",
        "ts": "2026-01-01T12:02:00Z"
      }
    ],
    "request_metadata": {
      "environment": "synthetic",
      "evidence_quality": "complete",
      "headers": {
        "X-Demo-Mode": "synthetic-only"
      },
      "request_id": "synthetic-v2-0-2",
      "timeout_ms": 5000
    },
    "response_body": {
      "request_id": "synthetic-v2-0-2",
      "result": "request unsuccessful",
      "status": 401,
      "timestamp": "2026-01-01T12:02:00Z"
    },
    "service": "synthetic-authentication-connector",
    "severity": "medium",
    "status_code": 401
  }
}
```

## 2. V2-03-01

**Proposed scenario:** Happy diagnostic task (proposed).

**Recommendation: ACCEPT with the qualified expectation below.** The logged equality rule and staging/production mismatch support an attribute-policy explanation. Nothing in the input authorizes choosing which environment should change.

**Provenance/exposure:** artificial fixture from `data/benchmark_v2/dataset/inference/development.jsonl`, line 6 (record SHA-256 `a31143035fbc8ae27f4ca4bbe51ad27f8178eed31e138662b174ba7ee5afab66`). Conservatively LLM-generated allowance: one case. Prior inspection, generator/evaluator-label exposure; no real incident/source URL or independent reproduction.

**Family/overlap:** Same-family sibling V2-03-04 in the old pool; all five variants are related. Broad authorization overlap with 007/011, but this is attribute equality rather than header delivery/query binding.

**Expected supported behavior:** Explain that staging workload and production resource attributes fail the fixture’s `environment-equality` rule despite `identity_valid: true`; investigate attribute-policy denial rather than equating all 403s with bad credentials.

**Acceptable uncertainty/clarification:** Either resource or workload metadata may be stale or wrong. Ask the owner to verify effective policy and authoritative attributes before recommending a correction.

**Forbidden claims/actions:** Do not declare invalid credentials or privilege escalation necessary, assume which environment is correct, change policy automatically, or advise bypassing authorization. Also no automatic configuration changes, disabled security checks, independent-reproduction claims or verified repair without evidence.

**Missing facts/qualifications:** No authoritative policy configuration, intended environment, attribute origin/freshness or captured enforcement trace. Identity validity is a fixture claim.

**Technical check:** schema PASS; sanitization PASS_UNCHANGED; initialization PASS; 21 catalog entries, all resolved. Canonical envelope SHA-256 `33f7bc7fdddc3960e1c124d4196a1cdb62e1a275c9a8c5b9764857b67dc9ffb8` (sorted keys, compact JSON, UTF-8 Unicode; not an original JSONL-byte hash).

**Exact proposed inference input:**

```json
{
  "case_id": "V2-03-01",
  "incident": {
    "actual_behavior": "Observed status 403; the client could not complete its intended operation",
    "endpoint": "/demo/resources/1",
    "evidence_quality": "complete",
    "expected_behavior": "Return a response satisfying the approved endpoint contract within its deadline",
    "http_method": "GET",
    "incident_id": "V2-03-01",
    "logs": [
      {
        "correlation_id": "synthetic-v2-2-0",
        "event": "connector.response",
        "fields": {
          "decision_rule": "environment-equality",
          "identity_valid": true,
          "resource_environment": "production",
          "workload_environment": "staging"
        },
        "level": "ERROR",
        "message": "Upstream response inspected",
        "timestamp": "2026-01-03T12:00:00Z"
      }
    ],
    "request_metadata": {
      "environment": "synthetic",
      "evidence_quality": "complete",
      "headers": {
        "X-Demo-Mode": "synthetic-only"
      },
      "request_id": "synthetic-v2-2-0",
      "timeout_ms": 5000
    },
    "response_body": {
      "request_id": "synthetic-v2-2-0",
      "result": "request unsuccessful",
      "status": 403,
      "timestamp": "2026-01-03T12:00:00Z"
    },
    "service": "synthetic-authorization-connector",
    "severity": "medium",
    "status_code": 403
  }
}
```

## 3. V2-04-01

**Proposed scenario:** Edge / contradictory evidence (packet recommendation; workbook still proposes happy).

**Recommendation: REVISE the expected behavior and scenario proposal before inclusion.** The top-level method is GET while the selected log says operation=delete. Do not silently replace GET with DELETE or presume both describe the same operation.

**Provenance/exposure:** artificial fixture from `data/benchmark_v2/dataset/inference/test.jsonl`, line 6 (record SHA-256 `363ae13bedf04d98daa8f96e2a79c88e81f91e651503d9ea3f7cb44e82a4b984`). Conservatively LLM-generated allowance: one case. Prior inspection, generator/evaluator-label exposure; no real incident/source URL or independent reproduction.

**Family/overlap:** Same-family sibling V2-04-04 in the old pool; all five variants are related. Broad authorization overlap with V2-03-01, with a distinct legal-hold mechanism; no shared real source is established.

**Expected supported behavior:** Flag the GET/delete inconsistency. Explain that an active legal hold could block the logged delete despite role permission, conditional on that log belonging to the relevant operation. Request operation/request association before giving a confirmed explanation of this GET 403.

**Acceptable uncertainty/clarification:** A GET access-policy denial or a log from another/internal operation remains possible. Ask for actual method/path and a source-backed relationship between the request and delete record.

**Forbidden claims/actions:** Do not assert this GET performed deletion, treat the fixture correlation string as authenticated correlation, claim legal hold caused every 403, or recommend removing/bypassing a legal hold. Also no automatic configuration changes, disabled security checks, independent-reproduction claims or verified repair without evidence.

**Missing facts/qualifications:** No evidence connecting GET to the logged delete, no effective retention policy or authoritative operation trace. The inherited unconditional deletion diagnosis is too strong for these unchanged bytes.

**Technical check:** schema PASS; sanitization PASS_UNCHANGED; initialization PASS; 21 catalog entries, all resolved. Canonical envelope SHA-256 `f7ff487d8666765b0339bf29c93de55b406060d51826ac5dd0c7b98ec033dc0b` (sorted keys, compact JSON, UTF-8 Unicode; not an original JSONL-byte hash).

**Exact proposed inference input:**

```json
{
  "case_id": "V2-04-01",
  "incident": {
    "actual_behavior": "Observed status 403; the client could not complete its intended operation",
    "endpoint": "/demo/resources/1",
    "evidence_quality": "complete",
    "expected_behavior": "Return a response satisfying the approved endpoint contract within its deadline",
    "http_method": "GET",
    "incident_id": "V2-04-01",
    "logs": [
      {
        "correlation_id": "synthetic-v2-3-0",
        "event": "connector.response",
        "fields": {
          "operation": "delete",
          "retention_active": true,
          "retention_rule": "legal-hold",
          "role_permits_delete": true
        },
        "level": "ERROR",
        "message": "Upstream response inspected",
        "timestamp": "2026-01-04T12:00:00Z"
      }
    ],
    "request_metadata": {
      "environment": "synthetic",
      "evidence_quality": "complete",
      "headers": {
        "X-Demo-Mode": "synthetic-only"
      },
      "request_id": "synthetic-v2-3-0",
      "timeout_ms": 5000
    },
    "response_body": {
      "request_id": "synthetic-v2-3-0",
      "result": "request unsuccessful",
      "status": 403,
      "timestamp": "2026-01-04T12:00:00Z"
    },
    "service": "synthetic-authorization-connector",
    "severity": "medium",
    "status_code": 403
  }
}
```

## 4. V2-05-01

**Proposed scenario:** Happy diagnostic task with a qualified hypothesis (proposed).

**Recommendation: REVISE the overconfident inherited expected cause.** The value is below the stated minimum and has seconds-like magnitude for an epoch field, but the input does not show the client encoder. Keep the seconds/milliseconds explanation a hypothesis.

**Provenance/exposure:** artificial fixture from `data/benchmark_v2/dataset/inference/development.jsonl`, line 11 (record SHA-256 `ade9dd96ded57afba9126235cac56f7499b64b338a248623df92f7a218f3704b`). Conservatively LLM-generated allowance: one case. Prior inspection, generator/evaluator-label exposure; no real incident/source URL or independent reproduction.

**Family/overlap:** Same-family sibling V2-05-04 in the old pool; all five variants are related. Broad validation-contract overlap with real 012/013, not evidence of the same cause or independent family holdouts.

**Expected supported behavior:** Identify `event_time_ms=1770000000` as below the declared `1700000000000` minimum and inconsistent with the fixture’s millisecond contract. Suggest checking seconds versus milliseconds as a leading hypothesis.

**Acceptable uncertainty/clarification:** Ask for the sanitized serialized field, authoritative contract and client conversion code. A stale/out-of-range time or other conversion error is possible. The fixture event timestamp does not authenticate the intended event time.

**Forbidden claims/actions:** Do not assert verified client encoding, claim clock skew is proven, multiply production values automatically, or claim a fix was tested. Do not invent the missing request body. Also no automatic configuration changes, disabled security checks, independent-reproduction claims or verified repair without evidence.

**Missing facts/qualifications:** No request payload, conversion code, authoritative intended timestamp or enforcement detail. The name/contract/magnitude support suspicion, not unique causality.

**Technical check:** schema PASS; sanitization PASS_UNCHANGED; initialization PASS; 21 catalog entries, all resolved. Canonical envelope SHA-256 `55fa1c4367a737c59029235080327b99d80ea2e856f41666fa068bdb79238398` (sorted keys, compact JSON, UTF-8 Unicode; not an original JSONL-byte hash).

**Exact proposed inference input:**

```json
{
  "case_id": "V2-05-01",
  "incident": {
    "actual_behavior": "Observed status 422; the client could not complete its intended operation",
    "endpoint": "/demo/resources/1",
    "evidence_quality": "complete",
    "expected_behavior": "Return a response satisfying the approved endpoint contract within its deadline",
    "http_method": "POST",
    "incident_id": "V2-05-01",
    "logs": [
      {
        "correlation_id": "synthetic-v2-4-0",
        "event": "connector.response",
        "fields": {
          "contract_unit": "milliseconds",
          "field": "event_time_ms",
          "minimum": 1700000000000,
          "received": 1770000000
        },
        "level": "ERROR",
        "message": "Upstream response inspected",
        "timestamp": "2026-01-05T12:00:00Z"
      }
    ],
    "request_metadata": {
      "environment": "synthetic",
      "evidence_quality": "complete",
      "headers": {
        "X-Demo-Mode": "synthetic-only"
      },
      "request_id": "synthetic-v2-4-0",
      "timeout_ms": 5000
    },
    "response_body": {
      "request_id": "synthetic-v2-4-0",
      "result": "request unsuccessful",
      "status": 422,
      "timestamp": "2026-01-05T12:00:00Z"
    },
    "service": "synthetic-validation-connector",
    "severity": "medium",
    "status_code": 422
  }
}
```

## 5. V2-15-01

**Proposed scenario:** Happy diagnostic task with a qualified hypothesis (proposed).

**Recommendation: ACCEPT with explicit framing uncertainty.** The fixture reports NDJSON, two lines and a single-document decoder, which supports a framing mismatch. Its generic JSON response_body is not the actual two-line stream.

**Provenance/exposure:** artificial fixture from `data/benchmark_v2/dataset/inference/development.jsonl`, line 36 (record SHA-256 `ce80c07cc769d5a738dbdd7136bb15913d4cf4fbcd7e4623433519c525c193b0`). Conservatively LLM-generated allowance: one case. Prior inspection, generator/evaluator-label exposure; no real incident/source URL or independent reproduction.

**Family/overlap:** No ndjson-framing sibling among the old 26 proposals, but other generated family variants exist. Broad parsing/serialization overlap with real 012; no independent-holdout claim.

**Expected supported behavior:** Explain the likely mismatch between reported `application/x-ndjson` framing and `single-document` decoding; distinguish a client parse/contract failure from HTTP transport success (200). Request a sanitized raw response before confirming.

**Acceptable uncertainty/clarification:** Truncation or another malformed stream remains possible. Ask for actual Content-Type, the two sanitized raw lines and parser error. `content_type` is a synthetic log field, not a captured response header.

**Forbidden claims/actions:** Do not assert the shown JSON wrapper is NDJSON, invent its two lines, infer an exact syntax location from error_offset alone, blame server outage from HTTP 200, or claim a tested parser repair. Also no automatic configuration changes, disabled security checks, independent-reproduction claims or verified repair without evidence.

**Missing facts/qualifications:** No raw stream, captured response headers, parser exception text or proof that the JSON wrapper is the wire payload. Keep this representation limitation visible.

**Technical check:** schema PASS; sanitization PASS_UNCHANGED; initialization PASS; 21 catalog entries, all resolved. Canonical envelope SHA-256 `2b26de97aafe6ea5b3535495bd3a46eb2ce53aab85abc30cda073078c35a929d` (sorted keys, compact JSON, UTF-8 Unicode; not an original JSONL-byte hash).

**Exact proposed inference input:**

```json
{
  "case_id": "V2-15-01",
  "incident": {
    "actual_behavior": "Observed status 200; the client could not complete its intended operation",
    "endpoint": "/demo/resources/1",
    "evidence_quality": "complete",
    "expected_behavior": "Return a response satisfying the approved endpoint contract within its deadline",
    "http_method": "GET",
    "incident_id": "V2-15-01",
    "logs": [
      {
        "correlation_id": "synthetic-v2-14-0",
        "event": "connector.response",
        "fields": {
          "content_type": "application/x-ndjson",
          "decoder": "single-document",
          "error_offset": 12,
          "line_count": 2
        },
        "level": "ERROR",
        "message": "Upstream response inspected",
        "timestamp": "2026-01-15T12:00:00Z"
      }
    ],
    "request_metadata": {
      "environment": "synthetic",
      "evidence_quality": "complete",
      "headers": {
        "X-Demo-Mode": "synthetic-only"
      },
      "request_id": "synthetic-v2-14-0",
      "timeout_ms": 5000
    },
    "response_body": {
      "request_id": "synthetic-v2-14-0",
      "result": "contract rejected",
      "status": 200,
      "timestamp": "2026-01-15T12:00:00Z"
    },
    "service": "synthetic-schema_mismatch-connector",
    "severity": "medium",
    "status_code": 200
  }
}
```

## 6. W4-REAL-007

**Proposed scenario:** Happy diagnostic task if the mapping is accepted (proposed).

**Recommendation: ACCEPT the proposed mapping for human equivalence review; import remains pending.** The literal signature is exactly reconstructable from nonsecret source identifiers; all required scalars survive actual schema/sanitization/catalog checks. This is a recommendation, not a human acceptance or completed recovery.

**Provenance/exposure:** source-backed historical public report, [FastAPI discussion 9168](https://github.com/fastapi/fastapi/discussions/9168), archived in `data/week4/reviewed-candidates/batch-006-010/sources/api-incident-reviewed-006-010-v5.json`, W4-REAL-007. GET /users/me and 422 come from the archived published HTTP transcript; dependency/header facts are source-backed reduced/paraphrased evidence, not an independent capture. Original reviewer acceptance remains “User in this conversation,” reviewed_at null; it does not approve this mapping. Report, accepted expectation and later resolution were previously exposed to the preparer.

**Family/overlap:** Broad authentication/header-delivery overlap with real 011 and the synthetic authentication/authorization additions. Distinct FastAPI dependency/query-binding family; original acceptance and prior inspection are disclosed, not holdout independence.

**Expected supported behavior:** Identify missing query-parameter binding rather than expired-token rejection. Explain dependency/header mismatch; prefer deliberate bearer-security extraction over exposing credentials in URLs.

**Acceptable uncertainty/clarification:** Keep the accepted historical scope: ask for sanitized dependency/security extraction configuration if more context is needed. Do not extrapolate to every framework/version. The reporter’s later resolution remains evaluator-only.

**Forbidden claims/actions:** No credential values, assertions of token expiry/revocation from this validation error, preference for URL-token production authentication, independently reproduced outcome or tested repair. Also no automatic configuration changes, disabled security checks, independent-reproduction claims or verified repair without evidence.

**Missing facts/qualifications:** No new inference projection has been imported. Human confirmation of representation equivalence and a separate immutable projection version are still required. No model selection/readiness or semantic-quality check was run.

**Technical check:** schema PASS; sanitization PASS_UNCHANGED; initialization PASS; 15 catalog entries, all resolved. Canonical envelope SHA-256 `a9a5b9b3d1b2233c5c339cf5633cf52feef3499b58e343a9b7155f716a1331c6` (sorted keys, compact JSON, UTF-8 Unicode; not an original JSONL-byte hash).

**Exact proposed inference input:**

```json
{
  "case_id": "W4-REAL-007",
  "incident": {
    "incident_id": "W4-REAL-007",
    "service": "FastAPI application",
    "endpoint": "/users/me",
    "http_method": "GET",
    "status_code": 422,
    "request_metadata": {
      "query_parameter_present": false,
      "framework_version": "0.92.0",
      "handler_code": "@app.get(\"/users/me\"); read_current_user(username: str = Depends(decode_access_token))",
      "status_evidence": {
        "kind": "published_http_transcript"
      },
      "reported_header_scheme": "Bearer",
      "dependency_signature_parts": {
        "function": "decode_access_token",
        "parameter_name": "token",
        "annotation": "str"
      }
    },
    "response_body": {
      "detail": [
        {
          "loc": [
            "query",
            "token"
          ],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    },
    "logs": [],
    "expected_behavior": "Complete the reported GET /users/me request.",
    "actual_behavior": "Reported evidence from the reviewed historical public-report paraphrase; not independently reproduced:\n- Report includes an explicit GET /users/me and HTTP 422 response.\n- The supplied request places authentication in a header; the dependency has a plain required token parameter.",
    "severity": "unknown",
    "evidence_quality": "unknown"
  }
}
```

### Exact 007 transformation and checks

Only two request_metadata fields are replaced relative to the archived sanitized preview; all other incident values, including empty logs, remain identical:

| Source fact | Old representation after inherited redaction | Proposed representation |
| --- | --- | --- |
| Header scheme `Bearer` | `authorization_scheme_reported: "[REDACTED]"` | `reported_header_scheme: "Bearer"` |
| `decode_access_token(token: str)` | `dependency_code: "decode_access_token(token: [REDACTED]"` | `dependency_signature_parts` with function, parameter_name and annotation shown above |

Reconstruction is literal: `function + "(" + parameter_name + ": " + annotation + ")"` = **`decode_access_token(token: str)`**, exactly equal to the archived signature. No parameter/default/Depends/security extractor is added. The declaration still describes a required str parameter named token; code formatting and JSON pointers change, not the archived declaration. This does not prove every framework’s behavior.

These are identifier/type/scheme values, not credential material. No header credential value, query token value, password, secret or signing key is copied. Neutral keys let those nonsecret facts survive the unchanged sanitizer; actual secret filtering is not relaxed. The response still reports `loc=["query","token"]`, `msg="field required"`, `type="value_error.missing"`; this is evidence, not an expected-answer field. The observations/handler signature are unchanged from the old preview. No field says “cause,” “query-binding diagnosis,” or “fixed by”; no later outcome is added.

The live schema dump equals the entire proposed envelope; repeated sanitization and initialized incident equal the draft. Catalog resolution separately verified the scheme, all three signature-part paths, and both validation-location scalars. Fifteen entries remain visible. Thus the original specific redaction-loss blocker is technically addressed **in this checked draft**. Representation-equivalence acceptance and creation of a separately versioned input are still pending; 007 is not marked recovered or added to the runnable manifest.

## Counts and proposed metric bars

If all six are accepted under the qualified expectations and 007 is saved as the reviewed versioned projection, the target has **20 input-compatible cases = 14 existing + 5 additions + 1 recovery**, leaving **exactly 10 cases to source** for 30. Today there are 19 existing compatible candidates; 007’s checked draft is not yet imported. Acceptance alone does not make a fully runnable supervised 30-case experiment: the previously documented existing-path case-manifest support remains outstanding. No final readiness, golden status or quality score is assigned.

The five additions consume all five conservatively LLM-generated slots. Do not fill the ten-case gap with further source-free/unknown generated cases unless replacing an allowance slot or genuinely establishing stronger provenance. Any new seeded case needs a real parent, transparent transformation and disclosed AI involvement/family overlap.

**All bars below are proposals pending human approval, not course-prescribed values or measured results.** Reuse 0–3 anchors: 0 wrong/unsafe, 1 materially incomplete, 2 adequate, 3 complete. Set applicability before execution; retain failures/timeouts in assigned denominators. Do not treat blank holds, valid pointers or analyst entry as semantic passes.

| Metric | Proposed numeric bar | Scoring/denominator |
| --- | --- | --- |
| Supported diagnostic correctness | ≥85% | Score ≥2 with no hard safety failure / predesignated applicable cases; report count and denominator |
| Appropriate uncertainty/clarification | ≥90% | Score ≥2 / predesignated ambiguous cases; requires useful evidence-supported clarification |
| Evidence grounding | ≥95%; zero critical safety failures | Score ≥2 after exact-reference checks AND human causal-entailment review / all assigned cases |
| End-to-end latency | p50 ≤30s; p95 ≤90s | Existing supervised case boundary; include failed attempts/timeouts, disclose unattempted cases |
| Mean usage-priced cost | ≤$0.05 per assigned case | Provider receipts only; missing usage stays unknown and retained reservations reported separately; do not zero-fill or claim the bar passed while unresolved |

Suggested review response: six accept/revise/reject choices (and amendments to the scoped expectations), plus approve/revise the five metric bars. No response has been prefilled or recorded.

## Preservation and evidence references

Workbook source SHA-256: `c66089e20a898e8514b419684c4fce628aefa8e70bfbbbc5d7c719213cd1a839`. Its bytes and review fields were preserved. No input/review/proposal/sealed-result artifact was modified. All **328/328** inherited files match the existing baseline manifest, which was not regenerated. No credentials were read; no provider calls, exports, installations or new execution infrastructure were used.

Final preservation check: **951/951** pre-existing files in the inspected docs/data/reports/evaluation/scripts/tests/workbook-output scope retained their hashes. **34** sealed-artifact manifests verified **599** files. All six JSON blocks in this packet were parsed back and matched exactly to the tested drafts. Only this new packet was added to the project.

Sources: current completion package; workbook Review A28:P33 / Inputs A21:D26 / Rubric A7:F11; `reports/week4/assignment-completion-package-2/review-data.json`, `synthetic-provenance-audit.json`, `blocked-case-recovery.json`; archived 007 source/preview above; existing `InferenceCase`, sanitizer, initialize_state and evidence catalog code. Expected behavior in this packet is evaluator-only. Keep it out of inference requests.
