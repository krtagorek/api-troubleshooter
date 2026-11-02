# API Troubleshooter — Initial assessment

## Directly inspected architecture

`main.py` composes FastAPI; `backend/app.py` supplies versioned incident/registry administration routes, `backend/streaming.py` SSE, and `worker/__main__.py` the independent durable worker. `worker/queue.py` provides jobs/leases. Five agents in `agents/` classify, investigate, analyze causes, propose human-reviewed plans and validate. `graph/state.py`, `routing.py`, `workflow.py` and `report_policy.py` define validated shared state, conditional evidence holds and tentative-report eligibility. NOT_TESTED is not successful validation.

`tools/evidence_catalog.py` binds short handles to an incident snapshot; trusted selection/sufficiency, scalar grounding, counterevidence and output-safety boundaries precede publication. Ordinary uploaded logs are not signed provenance. Diagnostic contracts, signed ingestion and execution-time permits are optional and default OFF; flag activation alone provides no authority. Existing authorization must remain intact.

`persistence/` uses SQLAlchemy async application tables and separate LangGraph checkpoint schema. Alembic contains 0001–0008. `registry/` enforces independent endpoint approval. `frontend/` contains React, Router, Query, authenticated fetch-based SSE and timeline/report views. Config and health readiness do not prove worker/model availability.

## Reusable evaluation inventory

V1 has 120 generated cases (80 development, 40 test) with separate inference/labels. Its inherited evaluation README reports 34 normalized cross-split overlap groups: not independent generalization evidence. V2 has 80 cases (40/40), 16 family-based scenarios and separate labels/rubric/manifest. Counts were checked by reading JSONL files during preparation; semantic quality and prior-use independence were not newly validated. Published synthetic generators and project licensing provide the source provenance; real manual USGS captures were excluded.

`evaluation/` includes dataset/leakage audits, V1 lexical-proxy metrics, V2 versioned scoring/review, budget reservations, provider receipts, single-use dispatch lifecycle, paired arms and human-review tooling. Historical dispatch manifests bind old code and private ledger hashes, not this new project. Do not run inherited paid dispatchers or invent replacement history to unblock them. The original $0.0550552/$2 estimate is historical Week 3 context, not a newly issued Week 4 budget or reproduced ledger.

Agent `ask()` uses structured ChatOpenAI responses, zero SDK retries and safety/grounding validation. Its persisted accepted outputs and node-completed events do not by themselves carry full provider usage receipts. Evaluation provider instrumentation records usage/latency/cost separately. No new one-root-per-case LangSmith integration is established; current evaluator restrictions reject enabled tracing/custom provider origins. This is a design gap for the next phase, not a reason to remove existing safety gates now.

Portable fixtures under tests/fixtures are retained. tests/conftest.py explicitly marks private-history tests and supplies isolated synthetic inputs only to mock-transport tests; this does not reproduce authentic audits. Private-history modules: test_rc_benchmark, test_next_v2_pilot, test_v2_execution, test_selection_comparison, test_v2_single, test_paired_human_review; additional named historical tests are listed in conftest.py. Some acceptance harnesses require fixed ports or original configuration/archive checks. They are not fresh-clone commands. No tests were run, dependencies installed, or databases contacted.

## Verification evidence and limits

The source root is not a Git repository. The clean nested publication repository identifies inherited commit 88563eab8fe871b14f19bf4f1675b2828f25ebc0. Current selected source bytes match that repository; extra local HTTP captures are excluded. Historical documents report 1013 backend tests, 70 Vitest and 13 fixture Chromium passes, with separate disposable PostgreSQL/live-local acceptance. These are historical claims, not current re-execution. Real-model pilot results are distinct from deterministic application acceptance; private original outputs/reviews are not copied and no independent accuracy is claimed.

The existing public licensing documents retain package-level MIT-notice gaps for development-only stackback/uri-js-replace and scroll-bar release metadata limits. Project MIT and verified third-party notices are unchanged; no dependency implementations are vendored. Public evaluator source contains a previously approved pseudonymous reviewer identifier used by legacy guards; no private review records are copied. Do not reinterpret hard-coded legacy identities as production principals or new human confirmation.

## Recommended next phase

Review candidate dataset prior-use/family leakage and choose 40 golden cases without automatically approving labels. Specify a versioned label-isolated runner, explicit root/child tracing contracts, actual token/latency receipts, human rubric and fresh budget/approval boundaries. Then separately authorize offline evaluator/tracing implementation and disposable-environment regression testing. Do not tune on reserved cases or alter inherited behavior before a baseline protocol is frozen.
