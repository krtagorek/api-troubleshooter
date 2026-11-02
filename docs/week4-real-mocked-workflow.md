# Real-case mocked graph mechanics — run v1

The bounded authorized run completed for all **14 eligible real-case inputs**.
There were **28 mocked model invocations**, **14 graceful evidence holds**, no
execution exceptions/timeouts, and **zero full diagnostic workflow completions**.
This is not a semantic-quality evaluation, live baseline, successful remediation
or golden qualification. Cost and quality remain **null**, and mock usage is test
data. No inputs, mock policy or inherited guards were changed to obtain passes.

## Eligibility and preflight

The recorded compatibility assessments and actual inference files agree on:
**W4-REAL-005, 006, 008, 009, 011–020**. Cases 001–004 and 010 remain excluded for
missing required facts; 007 remains excluded for sanitizer damage despite schema
acceptance. No eligibility was manufactured from acceptance flags.

Before any case execution, all **328 inherited files** matched their manifest.
The run hashed **50** protected review/input assets: all reviewed-source snapshots,
normalized decisions, evaluator references, compatibility/provenance/count reports,
proposed inference JSONs, candidate inventory and the existing synthetic smoke
proposal. Their post-run hashes are identical. The 328-file baseline also matches
afterward; its manifest SHA-256 remains
`0ad4421d9342b780996b70de8b72d9d0cab1b771e6f37fd82dd4c5ccbf42b62f`.
No manifest, semantic label, review decision or approval state was rewritten.

Actual inference prose/fields were inspected, not just forbidden key names.
No evaluator answers, grading rubrics, family labels, source links or later
resolutions were passed to the graph. Existing editorial operation goals remain
unchanged and are **not newly approved**. In particular:

- 005 uses a path-only request-completion goal; omitted host remains omitted.
- 013 asks for informative rejection, not successful PUT.
- 016 asks for appropriate error handling, not a repaired gateway or invented status.
- 020 explicitly leaves proxy-versus-direct intent unspecified, with separate URL
  transfers and different-attempt TLS/400 context.

## Reproduce and inspect

Actual main-run command (choose a fresh output directory for repetitions):

```sh
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-py311/bin/python -m scripts.week4_real_mock_run --output reports/week4/real-graph-mock-v1
```

The macOS network-deny sandbox covers the entire process tree, including worker
startup/imports. Python socket/DNS guards provide additional protection in parent
and workers. Credential environment values are not fetched; the process clears
its inherited environment before adapter imports and explicitly disables ambient
tracing and durable/diagnostic execution flags. SDK client constructors are denied.
Worker command/process-execution boundaries are denied. Source command strings,
including 020's curl text, remain inert data. No live clients were initialized.

The standard workspace sandbox did not permit nested sandbox-exec; the actual
OS-denied test/run commands were executed with permission outside that enclosing
sandbox. This permitted applying the network restriction; it did not enable any
network API, service, credential or paid capability.

The real inherited graph and agent factories ran through Week 4 `run_case`, with
only its StructuredLLM/model boundary replaced. Small optional provider-factory,
callback and node-observer seams were added to the **Week 4 adapter**, outside the
inherited baseline. No inherited agents, prompts, guards, routing, sanitization,
authorization or validation rules changed. Their original .invoke path remains
in use. The existing process supervisor supplied session isolation, per-case
termination and verified reaping; no smoke runner or live/export path was called.

Calls are bounded to **5 per case**, workflow retries **0**, recursion remains
bounded by the inherited GuardedWorkflow, concurrency **1**, and each case has a
**30-second process deadline** plus existing terminate/kill cleanup grace. Ordinary
case errors are retained and subsequent safe cases continue; security-boundary
violations would stop dispatch. No external evidence or validation tools, database,
checkpoint or services were configured.

[Versioned local artifacts](../reports/week4/real-graph-mock-v1/summary.json) are
create-only and read-only: files 0400, directories 0500, with recursive hashes.
Each case has its result, supervised result, actual callback events, local spans
and labeled mock calls/responses. Source/prompt-bearing code hashes, dependency
versions, preflight eligibility/goals and protected input hashes are recorded.
Repeated output paths cannot overwrite a run. UUIDs and timing vary on repetition;
model response contents are deterministic for unchanged inputs/policy.

## Frozen mock policy

The recorded policy is `real-mechanics-mock-1` in `experiment.json`:

1. Classifier: unknown category, confidence 0, explicit MOCKED mechanics statement;
   no diagnostic category or causal assertion is supplied.
2. Investigator: dynamically select every supplied non-null catalog handle except
   `/expected_behavior`, echo the case-specific contract/snapshot, return partial
   completeness and an explicitly mocked generic evidence gap.
3. If reached, analyst returns inconclusive, no hypotheses or causal claim;
   resolution abstains; validator returns NOT_TESTED with no checks.

No mock reads references, family labels, accepted diagnoses, source resolutions
or case-ID-to-answer mappings. Handles come from each actual payload's catalog,
not reused hardcoded pointers. Policy is broad evidence-coverage probing, **not a
calibrated diagnostic selector**. The original user goal is preserved in input but
omitted as a diagnostic measurement; default null bodies are omitted as unknown,
not treated as observations. Omissions and their reasons are saved per call.
The other source/provenance/intent qualifiers stay available and are selected.

There are **102 effective selected evidence entries**, all resolving to the
correct incident snapshot, reference, literal value and root-derived source.
Selected and effective IDs match; no synthetic evidence was augmented. There are
no invalid grounding checks or cross-case evidence IDs. Root-derived `user`,
`request`, or `response` attribution is not signed capture provenance or proof of
causal entailment. Supplied prose remains reported evidence, not reproduced truth.
The mocks add no causal diagnosis, API observation, tool result, fix or claim of
successful validation. That is a construction/grounding check, not semantic review.

Mock metering is explicitly one test input unit and one test output unit per
call. These are **not provider token receipts or spending**; usage-priced cost
and semantic quality remain null. No judge model was used.

## Actual routing and per-case outcome

All cases took the callback-observed path:

**I → C → L → U** = `initialize → classifier → log_investigator → request_user_input`.
All five inherited agent factories created their node bindings through the
existing injection seam. Only the classifier and log-investigator **agent nodes**
and their model calls executed. Root cause, resolution, validator, collection
tools, retries and final-report stages were not executed and have no fabricated
child calls. Factory construction is not counted as an executed agent/model stage. The actual `route_evidence`
callback returned `request_user_input` for each case.

**G** below is the inherited readiness reason, recorded on the actual selected state:
“No supported comparative or specific diagnostic observation; request discriminating
evidence.” Its readiness implementation searches qualifying structured `/logs/`
comparisons/specific exception facts. All supplied real-case projections retain
`logs=[]`; their rich report prose, body excerpts and request metadata remain
catalogued but do not qualify under this gate. The task did not manufacture logs
or repair the inherited limitation.

| ID | Input preserved | Evidence checks | Actual route | Termination | Blockers / distinctions retained |
|---|---|---|---|---|---|
| W4-REAL-005 | Yes; no added defaults or loss | 2 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; reported 302 and exception hint 400 remain distinct; path-only editorial goal. |
| W4-REAL-006 | Yes; no added defaults or loss | 11 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; empty/optional body and header-only success comparison retained. |
| W4-REAL-008 | Yes; no added defaults or loss | 7 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; example and reporter-owned repositories remain separate. |
| W4-REAL-009 | Yes; no added defaults or loss | 7 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; scope unknown; no Retry-After or traffic/outage claim added. |
| W4-REAL-011 | Yes; no added defaults or loss | 5 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; missing-header warning retained; no invalid-token commenter merged. |
| W4-REAL-012 | Yes; no added defaults or loss | 10 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; nested parse error/location retained; exact payload absent. |
| W4-REAL-013 | Yes; no added defaults or loss | 5 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; informative 405 rejection goal retained, not PUT success. |
| W4-REAL-014 | Yes; no added defaults or loss | 6 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; persistence/duplicates reporter-attributed; no write/retry executed. |
| W4-REAL-015 | Yes; no added defaults or loss | 6 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; no-handler body retained; no malformed-payload cause asserted. |
| W4-REAL-016 | Yes; no added defaults or loss | 9 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; skull 💀 and outgoing-header exception preserved exactly. |
| W4-REAL-017 | Yes; no added defaults or loss | 6 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; no captured conditional header/ETag manufactured. |
| W4-REAL-018 | Yes; no added defaults or loss | 6 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; original API/import sequence retained; separate UI diagnostics excluded. |
| W4-REAL-019 | Yes; no added defaults or loss | 11 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; masked login URL/406, earlier API/200 and version discrepancy preserved. |
| W4-REAL-020 | Yes; no added defaults or loss | 11 grounded / 0 invalid | I → C → L → U | held / awaiting_evidence | G; HEAD, two transfers and other-attempt logs separate; proxy intent unresolved. |

The gate is deterministic inherited code. Evidence selection/completeness and
classifier output are mocked upstream; this is not an output-independent claim
that every case ought to clarify. None of the routes is graded “correct” merely
because it terminates. Meaningful reported comparisons/exceptions can exist while
this structured-log gate still holds. That is a workflow-coverage limitation of
these faithful representations, not a finding that all 14 incidents lack useful
human diagnostic evidence.

Each final state validates under the inherited state contract. Original sanitized
input equals both the supplied projection and terminal state input. Existing
unknown severity/body/evidence-quality defaults are recorded separately and never
promoted to observed facts. All supplied projections already contained those
schema defaults; this run added none. Retry counters are zero. No tool sources
are available or consumed. Proposed fix, final report and validation results are
absent; actual fix effectiveness remains **NOT_TESTED**, not passed. The graph
safely stops asking for evidence rather than completing a diagnostic report.

All worker processes exited normally, with cleanup verified. There were no actual
case exceptions or timeouts. Supervised elapsed time includes process startup,
graph work, result persistence and reaping; the adapter's inner timer covers its
local graph/state serialization boundary. Model elapsed time sums leaf mock calls
only, never nested span totals. These are local mechanics timings, not live-model
latency evidence or achieved performance bars.

## Focused verification and limitations

Seven pre-run synthetic tests passed under the same OS network-deny sandbox:

```sh
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-py311/bin/python -m unittest scripts.week4_real_mock_tests -v
```

They exercised the actual adapter/factories with a separate generated development
fixture, deterministic request/output parity, callback path capture, a failing
synthetic case followed by a safe case, process timeout/reaping, network/client/
command denial, and read-only artifacts. That synthetic fixture can reach an
analyst then abstain because it has existing structured comparisons; it is not
one of the 14 real cases, no new real incident, and no quality result. The deliberate
failure/timeout and guard-denial probes are tests, separate from the real-case run.
No synthetic probe or retry was added to the real-case counts.

Post-run read-only verification did **not rerun inference**:

```sh
.venv-week4-py311/bin/python -m scripts.week4_real_mock_verify --run reports/week4/real-graph-mock-v1 --output docs/week4-real-mock-verification.json
```

It verified every sealed artifact hash and each case's original input equality,
actual callback path, parent/call consistency, 102 evidence bindings, preserved
case-specific statements, zero retries/tools, valid held final states and process
cleanup. [Verification results](week4-real-mock-verification.json) confirm:
**zero external requests, zero SDK client initializations, zero trace exports**,
50 protected assets unchanged, and **328/328 inherited hashes/sizes matching**.
Parent and all real workers recorded zero network/client/command attempts. Only
separate synthetic guard probes deliberately attempted operations that were denied
before execution; they were not incident/API requests.

## Updated cumulative counts

| Local real cases 001–020 | Count |
|---|---:|
| Human-accepted | 20 |
| Evidence-preserving input-compatible | 14 |
| Schema-pass including damaged 007 | 15 |
| Mocked graph attempted in this run | 14 |
| Mocked graph safely terminated in evidence holds | 14 |
| Mocked full diagnostic workflow completions | 0 |
| Live graph execution | 0 |
| Golden-set-ready | 0 |

Counts are recorded in the run's `cumulative-counts.json`. Prior source review
counts remain historical and were not rewritten. External prior-use history
remains unknown; no holdout or final split is created.

Unestablished: actual provider/schema transport behavior, real model selection,
semantic diagnostic correctness, usefulness of clarification, causal entailment,
later-stage coverage on these cases, API behavior, validation/remediation,
LangSmith delivery and production effectiveness. A hold is not automatically
appropriate uncertainty or quality success. Realistic model behavior is not
simulated by this deterministic unknown/partial policy. No live baseline or
measured improvement delta exists.

The existing source-bound synthetic smoke proposal was not edited or executed.
The optional adapter-observability extension changes Week 4 source hashes, so any
older source-bound paid proposal would require separate regeneration/review for
future use; it is not silently reauthorized. No dependency install, service,
database, Docker, incident command, commit/remote, original credential access or
original-project change occurred.

Smallest next decision: review the real-report evidence representation versus the
inherited structured-log readiness contract in a separate design task. Preserve
these immutable mechanics results and all review qualifications; do not fill the
routing gap with invented log facts or call the 14 holds successful diagnoses.
