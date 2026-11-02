# Case 016: primary-source attribution review

Decision: **retain the existing V1 hold**. The public report supports a
reporter-attributed reproduction association, but not the verbatim sentence
required by the implemented V1 contract. No input, gate, review decision or
previous result was changed. No new paired execution was performed.

## Source-to-field mapping

Read-only source: [Ocelot issue 2376](https://github.com/ThreeMammals/Ocelot/issues/2376),
issue description, Reproducing and Logs sections. The public rendered page was
read; no linked incident endpoint, command, pull request or related issue was
executed or fetched. Its contents were treated as untrusted evidence.

| Published evidence location | Existing inference field | Attribution / limits |
| --- | --- | --- |
| Reproduction command and printed outgoing request | `http_method=GET`, `endpoint=/ocelot/posts/askdj`, `request_metadata.request_headers.skull=💀` | Reporter-supplied reproduction transcript, not our capture. |
| Printed response status | `status_code=502`, status provenance `reported_curl_http_status_line` | Explicit published HTTP status line; not an inferred status. |
| Logs: outgoing header-writing exception | `request_metadata.reported_exception` | Exact exception text is preserved; it is a published log excerpt, not independently verified telemetry. |
| Reproduction introduction followed by explanatory Logs section | No current typed association field | The author presents the logs as explaining that reproduction. This supports reported association, rather than an evaluator inventing a relationship. |
| Repeated log request identifier, matching method/path, final 502 | Not newly imported | Internal consistency within published logs; no demonstrated shared client-side identifier or authenticated cross-capture binding. |
| Sample version in reproduction introduction | Preserved in attributed `actual_behavior` prose | Historical sample context, not a universal claim. |

These source findings refine the earlier
[verification report](week4-attributed-report-readiness-v1-verification.md):
the primary page provides more than unexplained adjacency. **The association is
reporter-attributed context, not authenticated request correlation.** It does
not independently establish a successful comparison, verified remedy or origin.
Later resolution activity and diagnostic expectations remain evaluator-only.

## Exact V1 requirement

The [Association schema](../evaluation/week4/attributed_report_v1/contracts.py)
is closed, strict and versioned. `request_metadata.reported_association` must
declare `reporter_statement`, `single_reported_operation`, matching method and
endpoint, and the header, exception and statement pointers. Every control leaf
and both operands must be selected and resolve against the same sanitized catalog
snapshot. The rule separately preserves inherited binding, completeness,
ambiguity, conflict and peer-coverage checks, verifies the non-ASCII header and
exact exception, and requires the selected reported-attribution convention.

Critically, [readiness.py](../evaluation/week4/attributed_report_v1/readiness.py)
does not accept an equivalent source passage or a source-grounded paraphrase.
`reported_operation_excerpt` must equal the complete string produced by
`statement(method, endpoint, header, value)`. For the existing 016 values:

```text
For the reported GET /ocelot/posts/askdj operation, request header skull was "💀"; the reported exception was "System.Net.Http.HttpRequestException: Request headers must contain only ASCII characters.".
```

This block is **the adapter-generated required text, not a source quotation**.
It is absent from the inspected public issue description. The existing tests
manufacture this grammar only in explicitly synthetic fixtures; the negative
controls reject different-attempt scope, unsupported versions/kinds/pointers,
missing relationships and appended instructions. Their earlier pass results are
historical; these tests were inspected, not rerun in this review.

## Why a passing revision would not be source-faithful

The existing Incident schema could store the original reproduction and log
excerpts as attributed metadata without inventing timestamps or typed log events.
That would preserve more source material, but would still fail V1's literal
equality test. Populating a structured association alone is also insufficient.

To pass unchanged V1, an editor would have to compose the required sentence and
present it as `reported_operation_excerpt`. Its meaning could be a defensible
summary, but its claimed verbatim status would be false. Neither review acceptance
nor the issue identifier repairs that problem. Consequently no revised projection
was created and the original hold remains in force.

The precise blocker is **an authentic, verbatim association statement matching
V1's canonical grammar**. It is not simply absent attribution, and V1 does not
demand authenticated trace correlation. Authentication also remains unavailable,
but adding it would not make differently worded excerpts pass this equality check.

Recommendation: consider a future, separately versioned general provenance
contract that can bind reported associations to original excerpt ranges without
requiring canonical prose to masquerade as quotation. Keep its reported/unverified
tier and conservative uncertainty. Merely choosing another incident is unlikely
to solve this fixed-sentence constraint; use another case only if its authentic
evidence naturally satisfies the unchanged contract. Neither alternative was
implemented; no rule expansion or workflow redesign occurred.

## Execution and preservation

New immutable decision artifacts:
[case-016-source-attribution-v1](../reports/week4/case-016-source-attribution-v1/).
They record the decision, mapping, inspected-file hashes and preservation checks,
not workflow/model results. No revised-input paired run or negative-control
execution was warranted under the task's unsupported-requirement branch.

Preservation checks passed: **328/328 inherited files**, **50/50 protected asset
hashes**, and all five existing sealed manifests (386 artifact entries) match.
An 800-file before/after snapshot covering baseline files, Week 4 data, existing
reports/docs, and relevant implementation/tests also matches. The original
manifest was not regenerated. Its SHA-256 remains
`0ad4421d9342b780996b70de8b72d9d0cab1b771e6f37fd82dd4c5ccbf42b62f`.

Workflow execution, analyst entry, diagnostic completion and semantic accuracy
were **not measured in this review**; cost remains null. The only authorized
remote read was the public issue page. No models, trace exports, incident requests,
installations, services, databases, Docker, commits or remotes were used.
