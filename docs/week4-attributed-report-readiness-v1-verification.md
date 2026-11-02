# Week 4 attributed report readiness V1: implementation and offline verification

Implemented as an explicit Week 4 opt-in. **No real case gained analyst entry.**
The current inputs do not contain the explicit, resolvable same-operation
association required by this conservative first increment. The rule works on
clearly synthetic positive evidence and preserves clarification holds on the
unchanged real projections. These are mechanics results, not diagnostic quality,
appropriate-clarification judgments, golden readiness, or evaluation eligibility.

## Association decision made before implementation

[The proposal](week4-attributed-report-readiness-v1-proposal.md) requires an
association supported by inference evidence, not review acceptance or case ID.
The current [016 input](../data/week4/reviewed-candidates/batch-016-020/inference/W4-REAL-016.json)
contains:

- A literal non-ASCII request header and the exact reported exception.
- `observation_representation`: attributed public-report excerpts/paraphrases,
  not independent reproduction.
- A historical prose description listing the request and exception together.

The local candidate source snapshot likewise groups them in one incident's
`inference_evidence`. That supports describing them as reported observations,
but neither grouping nor adjacency explicitly establishes a single-operation
relationship. There is no structured association or literal relational statement
that V1 can resolve. The source is a curated excerpt/paraphrase, not an
independently authenticated request/exception capture. Its review proposal,
expected behavior, family, resolution and acceptance were not used to fill this
gap. No source URL was fetched.

Therefore **016 remains held**. No revised real input was generated. The remaining
13 cases do not contain the selected exact exception/non-ASCII-header pattern.
Existing reviewed assets and input bytes are unchanged in both arms.

## Implementation boundaries

New package [attributed_report_v1](../evaluation/week4/attributed_report_v1/):

- [contracts.py](../evaluation/week4/attributed_report_v1/contracts.py): frozen,
  extra-forbidden typed association, literal anchors and assessment. Assessment
  includes policy version, sanitized catalog snapshot, legacy decision, selected
  IDs, pointers, exact spans, reported/unverified provenance and limitations.
- [readiness.py](../evaluation/week4/attributed_report_v1/readiness.py): calls
  inherited readiness first. Every earlier binding, completeness, ambiguity,
  duplicate, coverage and conflict hold is final. Only the inherited final
  no-pattern outcome can enter the new rule. Legacy qualifying catalog evidence
  keeps its original behavior. The new rule requires the selected exact exception,
  a selected string header with a non-ASCII code point, selected attribution and
  a selected, literal same-operation relationship. Case-insensitive conflicting
  header values hold. `definitive_confirmation` is always false.
- [workflow.py](../evaluation/week4/attributed_report_v1/workflow.py): creates the
  inherited graph using its existing agent injection, copies its definition
  containers into a separate locked-SDK builder and replaces only the investigator
  evidence branch. All node functions, other branch functions and edges are
  reused. No inherited globals are monkeypatched; no new agent is implemented.
  A failed modern binding never falls back through the historical non-catalog-ID
  compatibility shortcut. Signed semantics, evidence tools, validation tools and
  persistence are not enabled by this composition.
- `AnalystAdvisory` scopes its provider proxy to `RootCauseAnalystOutput`. It
  rebinds the supplied handles/snapshot, recomputes readiness, and replaces only
  `analysis_readiness` for a qualifying V1 report. System prompt, Incident,
  classification, evidence, strict output schema and inherited post-validation
  remain intact. The old advisory remains nested in the new one. No child call or
  span is invented for deterministic assessment.

The sole existing-file change is an optional `workflow_factory=None` seam in
[the Week 4 runner](../evaluation/week4/runner.py); the default is the inherited
builder. This file is outside the 328-file baseline. Original prompts, inherited
routing, publication, redaction, grounding, authorization and validation code are
unchanged. The V1 branch only grants entry to qualified analysis. It does not
change downstream report eligibility; the legacy publication guard still applies.

### Deliberately restrictive association contract

This implementation does not infer association from arbitrary prose. For the new
report route, `request_metadata.reported_association` must conform to the closed
`Association` schema. It declares the version, `reporter_statement` kind,
`single_reported_operation` scope, matching method/endpoint, header pointer,
exception pointer and statement pointer. All of its leaves must be selected and
snapshot-bound. The statement must resolve at
`/request_metadata/reported_operation_excerpt` and match the bounded literal
relationship grammar implemented by `statement()` exactly, including the actual
header value and exact exception. Appended instructions, another operation,
unknown scope/version, evaluator pointers, missing peers and altered literals
hold. The attribution representation must also be selected and match the
reported/unverified convention.

This grammar is intentionally narrower than arbitrary natural-language source
reports. The synthetic fixture constructs such a statement and is explicitly
marked synthetic. **Do not generate that statement from co-occurring real facts
and present it as a source excerpt to obtain a pass.** A future authentic input
would need a source-supported literal relationship under this contract. If its
original wording cannot fit this narrow grammar faithfully, keep it held and
propose a separately versioned extraction/association change. No generalized
prose extractor or additional mechanism rule is implemented here.

The record is an unverified reported relationship, never authenticated trace
correlation. Hashes establish content binding, not truth, origin or ownership.
A malicious reporter could fabricate consistent source facts; V1 confers no
source authentication or execution authority. Existing untrusted-data system
instructions, strict schemas and downstream checks remain necessary.

## Final paired comparison

Fresh final immutable results:
[attributed-report-readiness-v1-paired-2](../reports/week4/attributed-report-readiness-v1-paired-2/),
with [summary](../reports/week4/attributed-report-readiness-v1-paired-2/summary.json),
[experiment](../reports/week4/attributed-report-readiness-v1-paired-2/experiment.json),
[hash manifest](../reports/week4/attributed-report-readiness-v1-paired-2/artifact-hashes.json),
and baseline/V1 per-case result, supervised result, model-call, span and graph-event
files. Files have mode 0400; directories 0500; writes are create-only.

For **every row below**, both actual routes were:
`initialize → classifier → log_investigator → request_user_input`.
Both arms had **zero analyst entries, two executed mock calls, held termination,
and zero errors**. No case was silently dropped.

Reason keys (full decisions are preserved per case):

- **G**, baseline: “No supported comparative or specific diagnostic observation;
  request discriminating evidence”.
- **P**, V1: “No selected exact reported ASCII exception/non-ASCII header pair”.
- **A**, V1: “Missing or invalid explicit same-operation report association”.

| Case | Baseline reason | V1 reason | Analyst entries B/V1 | Calls B/V1 | Terminal B/V1 | Errors B/V1 |
| --- | --- | --- | --- | --- | --- | --- |
| 005 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 006 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 008 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 009 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 011 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 012 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 013 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 014 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 015 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 016 | G | A | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 017 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 018 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 019 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |
| 020 | G | P | 0 / 0 | 2 / 2 | held / held | 0 / 0 |

There are 14 assigned real inputs and 28 arm executions, with 56 mock calls,
56 mock input tokens and 56 mock output tokens. These receipts are test data.
**Semantic accuracy = null/not measured; monetary cost = null/not measured.**
There were no paid calls, external requests or trace exports. The inconclusive
terminal diagnosis on these held cases is created by the inherited clarification
node, not an analyst/model call. Local spans cover only the case, two executed
agent boundaries and two executed model boundaries; no tools or skipped stages.

Both arms used identical current input bytes, the same dependency lock and all
88 matching installed pins (Python 3.11.16), and unchanged
`real-mechanics-mock-1`. Limits remained five model calls, zero workflow retries,
30-second supervised case timeout, concurrency one, no external tools/tracing.
All 14 pre-analyst request messages, responses and selections match across arms;
inputs are preserved. The final baseline arm also matches the historical sealed
baseline's request messages, outputs and routes. Only arm-specific thread IDs
are normalized when comparing full terminal states across new arms.

No real analyst advisory was changed because no real case qualified. The
intended advisory difference was verified on the synthetic positive: same
pre-analyst requests, one additional actual analyst call, only the readiness
payload changed, old advisory retained, reported/unverified limitations and
`definitive_confirmation=false`. The common analyst mock still returned
inconclusive; inherited clarification followed. That is branch coverage, not a
successful diagnosis.

An earlier fresh [paired-1 run](../reports/week4/attributed-report-readiness-v1-paired-1/)
is retained unchanged. It has the same 14-pair routes, parity and 56 mock-call
result. Its experiment text overincluded local trace delivery in the case latency
description. Paired-2 corrects that metadata and is the final reported run. Do not
pool these repeated inputs into a 28-case dataset; the two recorded comparisons
total 112 mock calls, with unit-control calls separate.

### Timing boundaries

`CaseResult.elapsed_seconds` begins immediately before node-wrapper setup and
includes graph construction/invocation, observer work, error handling and terminal
serialization. It excludes provider creation, initial state setup and local sink
delivery. `model_elapsed_seconds` is the sum of actual mock receipt durations,
not node/root durations added together. Supervisor elapsed includes spawn through
verified reaping and parent overhead. These are local mechanics measurements, not
provider latency or performance benchmarks. All reconciliations passed.

## Focused control outcomes

[Rule controls](../tests/week4/test_attributed_report_v1.py) and
[composition controls](../tests/week4/test_attributed_report_comparison.py):
**13 tests passed**. One explicitly identified test checks current 016's missing
association; synthetic controls are separate from the 14-case comparison.

| Control | Actual result |
| --- | --- |
| Synthetic exact exception, Unicode header, selected literal relationship and attribution | V1 qualifies with resolvable snapshot-bound anchors; baseline holds. |
| Real inherited workflow on synthetic positive | Baseline 2 calls; V1 3 calls and analyst entry; V1 ends held/inconclusive, no validation or report. |
| Missing exception/header/association/attribution/statement; ASCII header; unrelated exception; wrong field | All hold. |
| Wrong method/endpoint, separate-attempt scope, unsupported version, wrong pointers, evaluator kind | All hold. |
| Appended instructions in exception/statement, prose asserting sufficiency, extra `analysis_ready` field | All hold; no command or tool execution. |
| Forged, stale or cross-case IDs, altered observation/source/pointer, duplicate IDs | All hold. Forged legacy IDs cannot use the compatibility fallback. |
| Missing selected operand/association peer or legacy diagnostic log peer | Holds. |
| Ambiguous observation; unknown/missing/conflicting completeness | Holds. |
| Conflicting correlated log values, reversed bounds, case-insensitive header conflict | Holds; legacy conflict holds are not overridden. |
| Synthetic model asserts competing supported causes without discriminating evidence | Inherited post-validation forces inconclusive, no selected hypothesis, confidence zero. |
| Topology parity | Same nodes, destinations and conditional edges; only the investigator branch implementation differs. Signed-semantic activation rejected. |
| Legacy qualifying telemetry fixture | Same baseline/V1 requests, mock responses and executed path; no advisory replacement. |
| Span/usage/timing checks on synthetic execution | Reconcile; no invented model/tool children. |

The [existing runner suite](../scripts/week4_real_mock_tests.py) also passed
**7/7 tests**, including failure-then-subsequent-case, timeout termination with
verified cleanup, deterministic parity, span parentage, immutable finalization
and guards blocking sockets/SDK constructors/commands. Those guard probes are
intentional local denied attempts, not network requests or client initialization.
The actual paired workers and parent recorded zero boundary attempts.

## Protected artifacts and remaining limitations

[Independent read-only verification](week4-attributed-report-readiness-v1-verification.json)
passed: 328/328 inherited baseline files, 50/50 pre-existing protected asset hashes,
74/74 historical real-run artifact hashes, all other prior offline run files,
and the retained first paired run are unchanged. The final run protects 297
existing data/report/manifest files and verifies 144 sealed final artifacts.
The current implementation source hashes match final experiment metadata. The
baseline manifest was not regenerated; its SHA-256 remains
`0ad4421d9342b780996b70de8b72d9d0cab1b771e6f37fd82dd4c5ccbf42b62f`.

The primary unresolved blocker is source-supported explicit same-operation
association. No human review of a new association or policy interpretation is
fabricated. Existing acceptance is neither evidence of reproduction nor approval
of a newly synthesized relationship. More permissive extraction, further mechanism
rules, real-provider behavior and publication changes remain outside this increment.
The builder-copy integration depends on the pinned LangGraph representation;
upgrades require renewed topology/behavior characterization. All cases remain
previously exposed development evidence; no independence, final split, golden
qualification or model-quality gain is asserted.

## Reproduce

Use the existing isolated environment; no installation or credential setup is
needed. These commands run only the inspected portable modules and stdlib
verification path. The macOS OS sandbox denies networking for parent and children;
Python socket/DNS, SDK-constructor and worker-command guards provide additional
boundaries. Credential environment is cleared before adapter imports, ambient
LangSmith tracing is disabled, and only local fake-sink spans are recorded.
The enclosing workspace sandbox required permission to apply the macOS sandbox;
that exception did not enable network traffic.

```sh
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-py311/bin/python -m unittest tests.week4.test_attributed_report_v1 tests.week4.test_attributed_report_comparison -v
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-py311/bin/python -m unittest scripts.week4_real_mock_tests -v
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-py311/bin/python -m scripts.week4_attributed_report_compare --output reports/week4/attributed-report-readiness-v1-paired-3
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-py311/bin/python -m scripts.week4_attributed_report_verify --run reports/week4/attributed-report-readiness-v1-paired-2 --output docs/week4-attributed-report-readiness-v1-verification-repeat.json
```

Choose new output paths on each repetition. Never modify sealed directories to
resume a run. No live model, trace-export, smoke, database, application service,
Docker, commit, remote operation or original-project access occurred.
