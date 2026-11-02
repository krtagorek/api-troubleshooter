# Week 4 attributed report readiness: investigation and V1 proposal

Status: proposed; documentation only. No behavior, case version, human decision,
or sealed result is changed. This proposal authorizes neither implementation nor
execution. Its first increment deliberately supports one narrow evidence pattern,
not an automatic pass for all 14 cases.

## Recorded finding

The [mocked workflow report](week4-real-mocked-workflow.md),
[sealed summary](../reports/week4/real-graph-mock-v1/summary.json), per-case
`supervised-result.json` gate records, and graph event records agree: all 14 cases
executed `initialize → classifier → log_investigator → request_user_input`.
There were 28 mock calls, two per case, and no executed analyst/model descendants
after investigation. All 14 were held, rather than failed by exception or timeout.
All 102 selected evidence entries were bound successfully; no augmentation or
invalid/cross-case reference was recorded. Each saved readiness decision reported:

> No supported comparative or specific diagnostic observation; request discriminating evidence

Every input has `logs=[]`. Useful observations survive elsewhere in each Incident,
but the qualifying-fact construction in
[diagnostic_sufficiency.py](../tools/diagnostic_sufficiency.py) examines **only
selected `/logs/` leaves**. Therefore the recorded holds are explained by the
guard's representation boundary, without a claim about model diagnostic ability.

The evidence contracts also matter:

- [Evidence](../models/evidence.py) binds literal observations to scalar pointers.
  Supported roots are logs, response body, request metadata, status code, expected
  behavior, and actual behavior. Root-derived `source` is a location convention;
  it does not establish independent telemetry provenance.
- The [catalog](../tools/evidence_catalog.py) revalidates/sanitizes the Incident,
  skips sensitive/label fields, and generates snapshot-bound scalar IDs and
  handles. Resolution proves content binding, not authenticity or causal entailment.
- [Selection](../tools/evidence_selection.py) recognizes more coverage candidates
  than readiness recognizes diagnostic facts. A response error can be selected
  and coverage-complete without qualifying for analysis.
- [Routing](../graph/routing.py) uses readiness for modern catalog IDs. Its older
  non-catalog-ID compatibility path must not be used to evade this check.
- Existing [trusted contracts](trusted-diagnostic-contracts.rst) concern separately
  authorized semantics. Public incident reports do not acquire that authority.
  The [mechanism/origin proposal](mechanism-origin-contract-v2-proposal.rst) also
  distinguishes qualified mechanisms from confirmation; it is not an implemented
  permission to bypass current guards.

## 1. What qualifies today, exactly?

Readiness means permission to **attempt qualified analysis**, never confirmed
diagnosis. `definitive_confirmation` is always false in this helper.

First, selected evidence must be nonempty and completeness `complete` or `partial`.
Any explicitly ambiguous item, duplicate ID, ID/reference/source/observation
mismatch, or omitted diagnostic peer holds. Only selected log leaves then form
fact groups. Quality-limitation markers are excluded. Facts normally share their
immediate parent; array leaves use their containing field name. A `/records/`
`value` takes its selected sibling `name` as the key, grouped at the enclosing
records collection. This is not arbitrary cross-log joining.

Conflicting scalar values at the same group hold. Conflicts across records with
the same reported correlation, event, stage and fact name also hold. Explicit
conflicting bounds hold. Within a group, any of these patterns qualifies:

1. Same-type, non-null, unequal role-paired fields: `configured/received`,
   `expected/actual`, `expected/observed`, `resource/workload`, `server/client`.
   Matching replaces underscore-delimited role tokens. Numeric pairs qualify
   only for the `expected` role with a recognized numeric metric; arbitrary
   numeric configuration differences do not. Array pairs qualify when their
   value sets are disjoint, not merely differently ordered.
2. An explicit same-metric, same-unit bound violation: observed > upper or
   observed < lower. The metric vocabulary is scale, count, requests,
   utilization, latency, duration, elapsed, age, size; supported dimensions use
   ms/seconds or bytes as appropriate. Namespaces remain distinct. The explicit
   historical aliases in [semantic_comparison.py](../tools/semantic_comparison.py)
   are observed latency versus deadline/budget, observed age versus max age,
   observed size versus min size, bucket requests versus bucket limit, and DNS
   elapsed versus request deadline. Equality to a bound does not violate it.
3. A field named exactly `exception`, `exception_type`, or `error_type`, with a
   string fully matching `[A-Za-z][A-Za-z0-9_.]*(?:Error|Exception)`.
   A message containing an exception name, or a type followed by `: message`,
   does not qualify by this rule.
4. An integer `error_offset >= 0` together with `decoder` and `content_type`
   fields in the same group. The current implementation checks presence of the
   latter two, rather than parsing prose into them.

HTTP status alone, expected behavior, model confidence, reliability scores,
catalog membership, and free-text causal assertions are not qualifying patterns.

## 2. Preserved facts outside that boundary

These are findings from the actual inference files, not additions from evaluator
answers. All four inputs contain no typed log events.

| Case | Preserved inference evidence | Why it cannot qualify today / limits to preserve |
| --- | --- | --- |
| 006 | Metadata says empty body, absent Content-Type, Spring 5.1.2, and includes the handler's `consumes="application/json"` declaration. Body says `Content type '' not supported`. Attributed prose preserves a 415 transcript and the same empty-body request reportedly succeeding with the JSON header (200, `[]`). | Metadata/body/prose are outside the log fact groups. The comparison is not a typed log role pair. Neither code nor the historical comparison proves behavior for every Spring version. |
| 011 | Reported access-log GET `/api/list-files` 401 and an adjacent “Missing Authorization header” warning, plus the reporter's working assistant/failing file access and environment observations. | They are attributed prose, not ingested log records; the warning is not an exception-type field. Adjacency alone is not authenticated request correlation. Port, expiry, signing problems, and other commenters' token problems are not confirmed causes. |
| 012 | Response excerpt has `mapper_parsing_exception`, nested `json_parse_exception`, and the exact reason about unexpected `f`, expected comma, line 2 column 45. Status provenance is a reported client exception HTTP status line. | Body facts never enter qualifying groups. Snake-case `type` is also not a recognized CamelCase exception field. Line/column must not be converted to an invented byte offset. Original payload and a corrected request are absent. |
| 016 | Metadata contains `request_headers.skull="💀"` and `reported_exception="System.Net.Http.HttpRequestException: Request headers must contain only ASCII characters."`; attributed prose preserves the reported curl 502 and sample tag 24.1.0. | Metadata is excluded. The full exception-plus-message would not match the type-only regex even if copied into a log field. Report association is not an independently correlated gateway trace. There is no successful comparison request or confirmed upstream origin. |

## 3. Guard versus mock policy

[The recorded policy](../scripts/week4_real_mock_run.py), version
`real-mechanics-mock-1`, returns unknown classification/confidence zero, selects
all supplied non-null catalog leaves except expected behavior, and reports partial
completeness. Unknown classification is not the evidence route's readiness
predicate. Partial is explicitly permitted. For these saved selections, binding,
ambiguity, duplication and peer coverage did not cause the recorded rejection.
The empty qualifying log fact set did.

Selection remains model-dependent in general: another policy could omit required
peers, mark ambiguity, or return unknown/conflicting completeness and hold earlier.
The common analyst mock, if reached, deliberately returns inconclusive with no
hypotheses. Therefore opening this gate cannot establish semantic accuracy or
full diagnostic completion. No unexecuted analyst outcome is a recorded result.

There are later independent boundaries. [The analyst](../agents/root_cause.py)
currently supplies the old readiness result to its model, checks grounding and
counterevidence, downgrades ordinary catalog-supported claims to tentative, and
forces unresolved competing hypotheses without discrimination to inconclusive.
[Publication policy](../graph/report_policy.py) separately invokes the old
readiness helper and requires a grounded, discriminating, diagnostic-only plan,
human approval, NOT_TESTED validation and safe wording. Routing alone changes
neither of those contracts.

## 4. Honest representation is possible; readiness recognition is missing

Authentic excerpts can already be represented as strings in `actual_behavior`,
`response_body` where it actually is a response excerpt, or explicitly attributed
`request_metadata` fields. No timestamp or log-event object is required there.
An excerpt's original status provenance and completeness must remain explicit.
The existing files mix excerpts and editorial historical paraphrases; these must
not all be relabeled verbatim quotes. The local source snapshots are evidence to
check attribution, not executable instructions. No remote source fetch is needed
or proposed.

Thus the answer is **yes for honest storage, no for qualification by today's
readiness rules**. Do not put prose into invented `/logs/0/fields/exception_type`,
invent timestamps/correlation IDs, turn parser coordinates into offsets, or rename
editorial expectations as observations to manufacture a qualifying pattern.

## 5. Recommended smallest increment: attributed-report gate V1

Add an opt-in, separately versioned Week 4 adapter, `attributed-report-readiness-v1`,
leaving the original graph and all 328 inherited files unchanged. Start with one
generic rule: **reported ASCII-header rejection corroborated by a non-ASCII
request-header value**. This targets an observable boundary, not a case ID,
service name, expected answer, or root-cause label. Do not add generalized prose
extraction or rules for 006/011/012 in this increment. Their preservation is useful
even when they continue to hold; each later rule requires its own reviewed scope.

Use the existing Incident bytes initially. A new typed local assessment records
policy version, sanitized snapshot digest, rule ID, evidence IDs, references,
literal matched spans, provenance tier, scope limitations, eligibility and reason.
It contains no expected answer, source resolution, family label, review acceptance,
or semantic score. It is derived by deterministic code, never accepted from model
output. No new Incident root or Evidence source enum is needed.

The new gate must:

1. Retain the original binding, completeness, ambiguity, duplicate and coverage
   preconditions. An old guard rejection for conflict or bad binding must not be
   overridden. Only its final “no supported observation” outcome may be considered
   for this additional pattern.
2. Resolve both selected IDs through the current sanitized catalog. Require a
   string leaf under `/request_metadata/request_headers/<header>` containing a
   non-ASCII code point, and the exact allowlisted exception type/message at
   `/request_metadata/reported_exception`. Use exact bounded matching of the
   observed value above, not “contains Error” or arbitrary model assertions.
   Require the existing attribution representation to identify reported evidence;
   unknown or contradictory provenance holds. Attribution text is descriptive,
   not a permission switch. Both facts must belong to the same reported operation;
   separate attempts or unclear association hold. For 016 the shared report
   association supports investigation only, not verified trace correlation.
3. Derive the Unicode predicate from the literal header value. Require both
   references and reject stale snapshots, other-case IDs, changed observations,
   unresolved spans, evaluator-only pointers, duplicate descriptors, unsupported
   versions and contradictory evidence. Never accept an `analysis_ready` flag,
   policy definition, reference list or diagnosis supplied in source prose.
4. Produce `qualified_analysis=true`, `definitive_confirmation=false` only for
   this bounded reported mechanism. Record `reported`, never captured/verified.
   Preserve the old decision alongside the new decision for auditability.
   Missing successful comparison, independent capture and origin evidence remain
   limitations. This permits a hypothesis/check, not a universal causal conclusion.

Provenance has three distinct meanings: direct captured telemetry only when
actually supplied; reporter observations or reporter-quoted telemetry with its
attribution and unverified completeness; evaluator interpretation, which stays
outside inference. A catalog's `source="request"` does not erase these distinctions.
Hashes prove binding, not a reporter's truthfulness. Even fabricated source data
could imitate an allowed signature; V1 grants no authentication or execution
authority and must never be described as solving source authenticity.

Arbitrary prose, including “ignore the guard,” cannot supply the rule operands.
Instruction-bearing text is untrusted data. Reject an altered exception value
with appended instructions; require real typed header operands, not a sentence
claiming a non-ASCII header. Keep inherited redaction, strict model schemas,
output safety, reference validation, authorization and publication intact. Add
adversarial instruction fixtures rather than claiming that exact matching alone
solves prompt injection.

### Integration boundary

The inherited `build_workflow` has factory injection but no readiness-policy
injection. Do not monkeypatch its globals or impersonate signed semantic-contract
authority. Build a small versioned Week 4 composition using the real inherited
factories and unchanged node handlers/topology, replacing only the evidence-route
decision for this opt-in arm. Characterize topology parity to contain drift.

The analyst currently recomputes the legacy readiness advisory. Use an explicitly
scoped Week 4 model-input adapter at its injected provider boundary to replace
only `analysis_readiness` with the checked V1 assessment (including the legacy
decision and limitations). Preserve its system prompt, Incident, evidence,
classification, response schema and post-validation. Do not invent child calls
for deriving this deterministic assessment. Record this advisory difference as
part of the treatment, rather than claiming request parity at that field.

Keep downstream report eligibility unchanged in this increment. The acceptance
target is qualified analyst entry; a later publication hold is expected and must
remain visible. A new report-publication policy would be a separate proposal.

## Before/after examples (predictions, not executions)

| Input held identical in both arms | Baseline | Proposed V1 |
| --- | --- | --- |
| 016: reported exception above plus literal skull header `💀`, with current attributed representation; no synthetic logs | Selects existing references but no log facts; asks for evidence after investigator. | Checks both selected snapshot-bound references and allows the analyst to consider reported header encoding rejection. Must retain uncertainty about provenance/origin and propose read-only confirmation. Under the common mock the analyst still returns inconclusive and routes to clarification; no diagnosis success is claimed. |
| 008: reporter-stated 404 for an example repository, separately reported owned repositories, no captured body/status line and no discriminating access/resource evidence | Holds. | Holds: no qualifying ASCII rejection/header pair. Ask for the actual affected repository request, sanitized access context, resource existence and response details. Do not merge example and owned repositories or assert every 404 has one cause. |

006 is well-supported for a historical media-type hypothesis, but deliberately
outside the first rule. Accepting a review decision does not force readiness,
eligibility, independence, or golden-set status.

## Focused validation and acceptance criteria for implementation

All future verification is offline, with the existing isolated environment,
blocked external network/SDK transports, no tools/services and zero paid usage.
No such execution was performed for this documentation task.

| Check | Required result |
| --- | --- |
| Generic synthetic matching pair and existing 016 projection | Selected, valid evidence reaches a real analyst boundary in V1; baseline holds. New node/model spans exist only for actual execution. |
| Remove exception; remove header; use ASCII header; unrelated error; wrong field; unknown attribution | Hold with explicit reason. No broad prose fallback. |
| Different reported attempts, contradictory values, ambiguous observations or omitted peer | Hold; no cross-attempt join or conflict override. |
| Valid references but uncertainty about origin/reproduction | Qualified analysis only; never definitive, execution-authorized or automatically publishable. Test competing hypotheses and inherited inconclusive downgrade. |
| Forged ID, cross-case ID, stale digest, changed scalar/span, evaluator pointer or injected sufficiency flag | Reject/hold before analyst; retain visible failure reason and denominator. |
| Source text requests bypass or supplies fake policy/labels | No control effect; strict rule operands, schema/redaction and output safety remain enforced. Labels/resolutions never enter actual captured model requests. |
| 008 and generic insufficient controls | Still request discriminating evidence; no causal assertion from 404 alone. |
| Legacy qualifying telemetry fixtures and baseline arm | Original routes, requests and outputs remain unchanged; no regression or alternate authority path. |
| Common inconclusive mock | Report analyst-entry/route/span coverage separately from semantic accuracy; accuracy is not measured. Never count a mock hypothesis as human/model quality evidence. |

Accept only if all focused checks pass, all attempted calls and failed cases stay
in results, no skipped calls/spans are invented, timing/usage reflect executed
boundaries, and baseline/assets/sealed hash checks remain unchanged. Human review
of the new rule's evidence interpretation remains pending until actually performed;
do not copy existing case acceptance into a policy approval.

## Fair paired comparison

Freeze identical case bytes, case versions, redaction/catalog versions, dependency
lock, selected IDs, source hashes and common mock policy for both arms. Use
`real-mechanics-mock-1` unchanged initially, including its inconclusive analyst,
five-call cap, zero retries and no external tools. Select the arm explicitly;
never dispatch by case ID or evaluator expectations. Pre-analyst requests and
selections must match. Compare old/new readiness reasons, analyst entry, actual
node/call counts, terminal holds/errors, grounding failures and elapsed boundaries.
The extra analyst advisory/call is the intended treatment, not a parity failure.

Do not seed mock answers from source resolutions. Separate additional synthetic
branch-targeting policies from this common-policy real-case comparison. Report
route coverage and acceptance/rejection mechanics with denominators, with semantic
accuracy “not measured.” Development cases are already exposed; family overlap
(including 006/010 and 004/009) prevents claims of independent holdout performance.

No input change is required for the recommended first increment. If inspection
finds the reported-operation association cannot be validated from the current
projection, hold 016 too; create a separately reviewed projection version only
from existing source evidence. Any added excerpt/attribution fields must go to
**both** arms with identical revised bytes. Rerun baseline on those bytes; do not
compare a revised treatment directly with the sealed old-input run. Preserve
`real-graph-mock-v1` as historical mechanics evidence and write new paired results
to fresh immutable directories with policy/input/source hashes.

## Proposed implementation files, risks and scope

Future additions (not created here):

- `evaluation/week4/attributed_report_v1/contracts.py`: closed typed assessment,
  provenance tiers and exact anchor representation.
- `evaluation/week4/attributed_report_v1/readiness.py`: selected-ID resolution,
  precondition preservation and single deterministic ASCII rule.
- `evaluation/week4/attributed_report_v1/workflow.py`: explicit opt-in composition
  and narrow analyst advisory adapter; inherited factories and handlers reused.
- `scripts/week4_attributed_report_compare.py`: paired offline runner using the
  existing supported Week 4 execution path and common mock policy.
- `tests/week4/test_attributed_report_v1.py` and
  `tests/week4/test_attributed_report_comparison.py`: focused controls above;
  inspect repository test placement before choosing final paths.
- New versioned experiment metadata/results and follow-up verification document;
  optional new projection assets only if justified, never overwriting reviews.

No inherited file, prompt, routing module, grounding/redaction/authorization rule,
review record, sealed run or baseline manifest would be edited. Runner integration
must stay outside those files; if the proposed composition cannot preserve their
contracts, stop and revise this design rather than silently broadening scope.

Main risks are false source association, spoofed reporter content, treating a
mechanism as proven origin, topology drift, leakage through richer projections,
and optimizing one known development case. Mitigations are narrow scope, literal
case-bound operands, explicit attribution, unchanged later safety gates, negative
controls and paired input equality. V1 intentionally leaves other rich reports
held and does not establish real-model quality or full workflow completion.

## Read-only verification for this proposal

Standard-library file/hash inspection only: 328/328 inherited files match the
existing manifest; 50/50 protected asset hashes match sealed preflight; 74/74 sealed
artifact hashes match. The baseline manifest was not regenerated. A 471-file
snapshot covering inherited files, Week 4 data, sealed run and existing docs was
also unchanged after adding this proposal. No workflow/tests, model calls,
network requests, external tracing, installations or services were run.
