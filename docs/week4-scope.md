# API Troubleshooter — Week 4 scope

Historical preparation scope (current offline implementation status follows below); the following benchmark work is not scored:

- Build a human-reviewed golden dataset of 40 cases with provenance and prior-use adjudication. Preserve an unchanged version for paired baseline/improvement comparisons.
- Separate development, reserved, previously used and related-family cases. Do not call inherited V2 cases untouched without reviewing historical usage.
- Integrate LangSmith tracing with one root run per case and actual model/tool child runs. Preserve redaction; tracing is currently disabled and historical evaluator transport rejects enabled tracing.
- Define quality, behavior, latency and usage-priced cost metrics; distinguish unexercised stages, workflow failures and uncertainty from incorrect diagnoses.
- Analyze the top three observed failures, then authorize 3–4 targeted improvements with measured comparisons. No prompt/routing changes are part of preparation.
- Keep expected answers, labels, rubrics and human review out of runtime model inputs. Keep mocked runs separate from live-model results and do not fabricate reviews.
- Prepare a concise professional demo: failure → authorized change → measured result, with limitations disclosed.

Next gate: agree dataset ownership/use history, review rubric and trace/budget design before implementing evaluators. No paid calls or automatic approvals are authorized.

## Phase 1 offline planning findings — 2026-10-28

Planning deliverables now exist: [evaluation protocol](week4-evaluation-protocol.md), [dataset audit](week4-dataset-audit.md), [candidate inventory](../data/week4/candidate-inventory.csv), and [tracing/isolation design](week4-tracing-design.md). They are drafts, not approved metrics, reviewed labels, a frozen dataset or an implemented runner.

Confirmed by local inspection: 120 V1 and 80 V2 programmatically generated incident records; 15 fixture/projection/template leads do not add independent incidents. No verified real observed incident inputs or newly human-reviewed golden cases established. INC-0025, INC-0110 and V2-02-01 have documented prior failure/replay exposure; jwks-stale-cache family is exposed. Other absent histories remain unknown. V1 cross-split overlap and related V2 variants limit generalization. Fixture model outputs are distinct from LLM-generated incident inputs; specification authorship needs confirmation. Current sources do not yet meet real-preferred, reviewed 40-case sourcing requirements.

The provider guard rejects enabled tracing; existing agent factories and graph injection seams permit a separately reviewed Week 4 adapter without modifying inherited behavior or invoking private dispatchers. New database names alone are insufficient: inherited initializer, healthcheck and frontend proxy need isolated future configuration. Read-only manifest verification matched 328 inherited files, including datasets; see audit for manifest digest.

Unresolved owner decisions: source permission and access to sanitized distinct real episodes (including any USGS evidence), prior-use/family history and specification authorship, human reviewer availability and adjudication ownership, practical development/reserved separation with exposure disclosure, acceptance of proposed rubric/bars, model snapshot and official pricing verification, new trace project/redaction/retention settings, isolated resource availability, and a fresh proposed $10 maximum with separate per-arm authorization. No approval is inferred from these proposals.

Recommended next implementation step: authorize only the separate offline adapter and mock-transport trace-contract checks while collecting/reviewing source evidence. Freeze labels, dataset, baseline and execution plan only after review; select 3–4 changes after baseline failure analysis. Live smoke and formal arms require future explicit approval. This phase ran no tests, services, databases, live models, tracing exports or inherited dispatchers; installed no dependencies, made no commits, and did not access or change the original project.


## Phase 2 offline adapter implementation

Implemented `evaluation/week4/` without changing inherited application files. The
entry point runs two clearly exposed development fixtures through the actual
inherited graph/factories using mandatory mocked SDK transport and a local fake
sink. Runtime inputs reject evaluator-only fields; reference types and genuine
human-review fields remain separate and unfilled. Results, partial validated
state, errors, stage coverage, model usage/timing, root/node/model spans and
structural/grounding checks are recorded in create-only, read-only completed
output directories. No configured tools means no invented tool spans. The
validator's real model attempt is recorded if reached; NOT_TESTED stays explicit.

Protocol revisions: one genuine reviewer initially, optional independent second
review; practical reserved/development separation with disclosed exposure and no
custodian requirement; ordinary case failures continue, while security/isolation,
label leakage, resource exhaustion and unbounded accounting stop dispatch;
cumulative development experiments selected after baseline analysis. Thresholds
and the $10 budget are still proposed and unapproved.

Portable verification runs only the new unittest module with socket connections
denied. See [adapter documentation](../evaluation/week4/README.md) for invocation,
limitations and the exact prerequisites for a future live smoke. Mock token
counts are test data, never real spend or model-quality evidence. No golden
dataset or semantic references have been assigned. An isolated local Python 3.11
environment uses copied preinstalled dependencies, without network installation.
No services, Docker, databases, live calls, remote tracing, private ledger,
original-project access, commit or remote was used in this phase.

## Phase 3 SDK integration prepared; no live execution

The smallest supervised one-case path now uses the supported OpenAI SDK with
strict schemas and received usage journaled before parsing, plus supported
LangSmith Client create/read instrumentation on sanitized explicit spans. New
Week 4 accounting is independent of private historical ledgers. Process-level
case timeout and terminate/kill/reap verification, per-run money/call limits,
unknown-usage reservation retention and trace-only recovery are implemented.
No external diagnostic tools, databases, services or inherited behavior changed.

31 portable tests cover both SDKs using mocked transports with external sockets
blocked. All 88 installed dependency versions and Python 3.11.16 match the reused
full hash lock; no package additions/upgrades or network installation occurred.
A fresh archive-hash-verified sync is documented for private setup. All 328
inherited manifest entries still match. See
[SDK verification](week4-live-integration-verification.md) and
[one-case setup plan](week4-smoke-plan.md).

The machine smoke proposal keeps model selection, verified prices and human
review unresolved. Exact dedicated private variables, account/project setup,
pricing/capability checks and future explicit execution/export flags are
specified in the setup plan. No paid call, external trace export, model-quality
claim, new golden data, commit or remote is authorized by implementation.
