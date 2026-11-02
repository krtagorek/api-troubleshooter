# Week 4 attributed report readiness V2

Implemented `attributed-report-readiness-v2` outside the inherited baseline.
Original V1, reviewed inputs, human decisions and sealed runs are unchanged.
V2 replaces the generated-sentence requirement with original excerpt anchors and
an explicit archived reporter-attribution relationship. It uses the same narrow
ASCII-header mechanism; no general prose readiness or case-ID rule was added.

## Actual case-016 result

Both arms received identical bytes from the new
[versioned projection](../data/week4/report-evidence-v2-1/inference/W4-REAL-016.json).
The unchanged `real-mechanics-mock-1` policy supplied all model responses.

| Arm | Actual route | Analyst entries | Mock calls | Terminal outcome | Errors |
| --- | --- | --- | --- | --- | --- |
| Original baseline | initialize → classifier → log_investigator → request_user_input | 0 | 2 | held; inconclusive clarification state | 0 |
| Explicit V2 | initialize → classifier → log_investigator → root_cause_analyst → request_user_input | 1 | 3 | held; inconclusive clarification state | 0 |

Baseline reason: no supported comparative or specific diagnostic observation.
V2 reason: original excerpt-bound reporter association permits qualified analysis
only. `definitive_confirmation=false`, provenance `reported_unverified`.

This is **analyst-entry mechanics, not diagnostic success**. The common analyst
mock returns inconclusive with no hypotheses; no final report, proposed fix,
validation execution or verified remediation resulted. Semantic accuracy and
monetary cost remain **null/not measured**. Five total mock calls produced five
mock input and five mock output token units; these are test data, not spending
or real tokenizer receipts. Synthetic controls are separate from this one real
development input and two arm executions.

Fresh immutable [paired artifacts](../reports/week4/attributed-report-readiness-v2-paired-1/)
include [summary](../reports/week4/attributed-report-readiness-v2-paired-1/summary.json),
experiment metadata, full requests/responses, observed node/branch events,
local spans and supervised results. No comparison was made against changed-input
historical results. The historical 14-case runs remain historical mechanics evidence.

## Provenance correction and source mapping

The source relationship was established by the preceding
[source review](week4-case-016-source-attribution-review.md): the issue presents
its request reproduction and an author-introduced explanatory log section.
That supports reported association, not authenticated request correlation.
No new network/source request occurred in this increment.

The new [archive](../data/week4/report-evidence-v2-1/archive/)
contains five separately located, original substrings: method/path, Unicode
header, reported response status, exact exception, and the author's log-section
bridge. They are not spliced into a purported continuous quotation. Locations
identify their published sections; offsets are end-exclusive Unicode character
indices within each archived clip, not invented full-page positions or timestamps.

This is a **partial selected-excerpt transcription from the public page inspected
in the previous review**, not an original raw HTML capture. `raw_capture_sha256`
is null. The new hash binds the local archive bytes; it does not attest a historical
page revision, truth, reporter identity or independent reproduction. Scope labels
and the cross-section relationship are explicit editorial annotations, not
captured request IDs. Full upstream source authenticity remains unverified.

| Representation | V2 meaning and bound |
| --- | --- |
| `verbatim_source_excerpt` | Literal characters resolve to the specified archived block/range. A fabricated quote, wrong range or stale document fails. This establishes binding to the selected-excerpt archive. |
| `attributed_editorial_summary` | Separately marked summary of the source's presentation; never accepted as a source quotation. It must match the archived annotation and cannot substitute for the original anchors. |
| `reporter_associated_reproduction` | Auditable relationship joining the request, response and explanatory log excerpts within one reported reproduction scope. It is not inferred from review acceptance or model confidence. |
| `authenticated_request_correlation` | Explicitly false for this archive and projection. Attempts to promote the lower tiers to authenticated correlation are rejected by the strict contract. No authentication facility is implemented. |

The [projection metadata](../data/week4/report-evidence-v2-1/projection.json)
records old/new input hashes and the source binding. The only added Incident field
is `request_metadata.report_attribution_v2`. Removing it reproduces the complete
original input exactly. Unicode, exception text, reported 502 provenance, unknown
body semantics, neutral operation goal and remediation uncertainty are preserved.
No expected diagnosis, family label, acceptance decision, later resolution or
semantic score enters the archive, relationship packet or model inputs.

## Contract and integration

New [V2 package](../evaluation/week4/attributed_report_v2/):

- `contracts.py` defines closed typed blocks, anchors, relationships, projection
  attribution and readiness assessment with distinct provenance levels.
- `archive.py` resolves bounded local files by content hash, never by fetching a
  URL. The archived relationship is an explicit curated source annotation. It
  is not a model-supplied sufficiency assertion or an authorization permit.
- `readiness.py` retains inherited evidence binding, duplicate, ambiguity,
  completeness, conflict and coverage checks. Only the legacy final no-pattern
  hold may enter the new mechanism rule. Every attribution packet leaf must also
  be selected. Source roles/ranges/scopes resolve against the installed archive;
  method/path, Unicode header, exact exception and reported status must match
  the Incident. Missing, forged, unrelated or unsupported associations hold.
- `workflow.py` uses the existing opt-in composition pattern: independent builder
  containers, unchanged inherited node handlers/edges, one replaced evidence
  branch. This replaces the report-readiness predicate; it adds no approval or
  authorization layer. The scoped provider adapter changes only the analyst's
  readiness advisory, retaining the old advisory and explicit limitations.

The mechanism remains generic: any selected string request header containing a
non-ASCII code point plus the existing exact reported exception, backed by the
required source relationship. It does not match an incident ID, service name,
review acceptance, diagnosis label or arbitrary prose assertion.

Grounding, strict outputs, redaction, competing-hypothesis handling, publication,
authorization and validation policies remain inherited and unchanged. Ordinary
legacy-qualified evidence retains its original route and model requests. A
failed modern reference never falls back through legacy-ID compatibility.

## Verification

**34 tests passed:** 12 V2 anchor/provenance controls, the existing 13 V1 controls,
7 existing mocked-runner regressions, and 2 additional V2 workflow parity tests.
The sealed [32-test transcript](../reports/week4/attributed-report-readiness-v2-controls-1/unittest.txt)
and [additional regression record](../reports/week4/attributed-report-readiness-v2-regressions-1/result.json)
are separate from real-case results.

| Control | Observed result |
| --- | --- |
| Original anchors plus explicit reported relationship | Qualified analysis only; no definitive confirmation. |
| Fabricated quotations, self-supplied archive body, wrong offsets, missing anchors or selected peers | Hold. |
| Missing/corrupt/stale archive, forged or cross-case evidence IDs, evaluator pointers | Hold. |
| Same literals assigned to an unrelated attempt scope | Hold. |
| Unsupported relationship/version, summary disguised as quote, attempted authenticated-correlation promotion | Hold. |
| Appended instructions in quote, prose claiming sufficiency, extra readiness flag | Hold; no instruction can create the required relationship. |
| Literal instruction-bearing synthetic archive without a relationship | Hold; no commands or tools executed. |
| Unknown/missing/conflicting completeness, ambiguous items, inherited contradictory bounds or missing diagnostic peers | Hold. |
| Case-insensitive conflicting header values | Hold. |
| Existing insufficient 008 and missing-contract synthetic control | Hold. Full V2 missing-contract execution matches baseline requests/outputs/route. |
| Legacy qualifying synthetic telemetry | Full V2/baseline requests, responses and route match; no advisory replacement. |
| Topology | Baseline/V2 node and edge shapes match; no new agent or tool boundary. |

[Read-only artifact reconciliation](week4-attributed-report-readiness-v2-verification.json)
passed. Pre-analyst requests, responses and selected evidence match between arms;
both preserve the revised input. The actual V2 analyst call contains only the
intended readiness-advisory change, with its system prompt and other payload
fields unchanged. Real calls/spans reconcile: baseline has two agent/model
boundaries, V2 three; neither has tool spans or fabricated skipped calls.
Model durations and mock usage sum exactly, without adding parent durations.
Case timing includes graph setup/invoke and terminal serialization, excluding
provider creation, initial state setup and local sink delivery. Supervisor timing
includes spawn through verified reaping.

All 88 dependency pins match the existing lock; Python 3.11.16. Both arms used
zero retries, the existing five-call ceiling, 30-second supervised timeout,
concurrency one and the unchanged mock policy. OS networking was denied for the
process tree; Python socket/DNS, SDK-constructor and worker-command guards were
active. Ambient tracing was disabled; only fake-sink local spans were recorded.
The paired parent/workers recorded zero network, client-constructor or command
attempts. Intentional denial probes in existing unit tests did not send requests
or initialize clients.

## Preservation and limitations

[Preservation proof](../reports/week4/attributed-report-readiness-v2-preservation-2/result.json):
**840 pre-existing files unchanged**, including **328/328 inherited baseline
files**, all **50 protected assets**, V1 implementation, reviewed inputs and
reviews. All **six prior sealed manifests / 389 artifact entries** match. The
paired runner also protects 500 data/report/doc/V1 files against mutation.
The baseline manifest was not regenerated; its SHA-256 remains
`0ad4421d9342b780996b70de8b72d9d0cab1b771e6f37fd82dd4c5ccbf42b62f`.
New data and result directories are create-only, sealed with hash manifests,
read-only files and read/execute-only directories.

The first new preservation-metadata manifest accidentally included its own
empty-file digest. That unpublished defective metadata is retained byte-for-byte
under [superseded metadata](week4-attributed-report-readiness-v2-preservation-superseded/),
with its defect recorded in the corrected proof; it is not relied upon. All
current result manifests verify. No prior artifact or execution result was altered.

This is a previously exposed development case and a curated, partial public-report
archive. Content binding does not prove the source account, real-world causal
truth or the editorial association's correctness. A malicious archive curator
could fabricate consistent material; these checks do not solve that threat.
Remediation, origin and independent reproduction remain unverified. No semantic
accuracy, diagnostic success, golden readiness or independent holdout gain is
claimed. The composition depends on the pinned LangGraph builder representation;
upgrades require renewed parity checks.

## Reproduce

No installation or credentials are needed. Use new output paths for repeated
runs. The workspace sandbox required an exception to apply the macOS deny-network
sandbox; this did not enable network traffic.

```sh
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-py311/bin/python -m unittest tests.week4.test_attributed_report_v2 tests.week4.test_attributed_report_v1 tests.week4.test_attributed_report_comparison scripts.week4_real_mock_tests tests.week4.test_attributed_report_v2_regressions -v
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-py311/bin/python -m scripts.week4_attributed_report_v2_compare --input data/week4/report-evidence-v2-1/inference/W4-REAL-016.json --output reports/week4/attributed-report-readiness-v2-paired-2
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-py311/bin/python -m scripts.week4_attributed_report_v2_verify --run reports/week4/attributed-report-readiness-v2-paired-1 --output docs/week4-attributed-report-readiness-v2-verification-repeat.json
```

No live model, external tracing, incident request, service, installation, database,
Docker, commit, remote operation or original-project access occurred.
