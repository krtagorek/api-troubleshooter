# Real-016 V2 proposal 3 — final-approval preflight

Status: **OFFLINE PREFLIGHT PASS; EXECUTION SETUP BLOCKED**. Preparation only, checked 2026-10-29 (America/Chicago). No smoke, live client, authenticated discovery, incident request, export, dependency installation, service, commit, or remote operation occurred.

The sealed [plan](../data/week4/smoke-proposals/real-016-v2-3/plan.json), its [approval summary](../data/week4/smoke-proposals/real-016-v2-3/approval-summary.md), and prior [verification results](../reports/week4/smoke-proposal3-verification-1/result.json) were inspected. No bound content changed, so no proposal version was created.

- Proposal: **real-016-v2-3**
- Plan SHA-256: `69e756641250cd698921804cb4dbde0757c6c9e84fa75c04821c29e8b7446acb`
- Immutable authorization identity: `a996d40dd93440d58ed722e2eb9999d98d40a9165d676300db6ac5b1aa8322b4`
- Case/policy: **W4-REAL-016 / attributed-report-readiness-v2**
- Snapshot/tier: **gpt-4.1-mini-2025-04-14 / default**
- Maximum: **$2.25**, five calls, concurrency 1, zero retries, no fallback.
- Five full reservations: **$2.107440**, with **$0.142560** headroom.
- External tracing, exports, incident tools: **OFF**.
- Execution authorization false; approval identity/time/binding null. No human approval inferred.

## Dependency archive integrity — BLOCKED before installation

The supported setup is documented in [the existing setup process](week4-smoke-plan.md). Python 3.11.16 and all 88 installed package versions still match the unchanged locks. This does **not** prove original archive integrity. The fresh `.venv-week4-locked` and project-local `.cache/week4-uv` do not exist. No global/private cache or original environment was examined.

The exact required installation action, reported before any installation, is:

```sh
.venv-week4-py311/bin/python -m venv .venv-week4-locked
uv --cache-dir .cache/week4-uv pip sync --python .venv-week4-locked/bin/python --require-hashes evaluation/week4/requirements.lock
.venv-week4-locked/bin/python -m evaluation.week4.dependencies
```

It writes only the new project environment/cache. Package downloads may require network permission. These commands were **not executed**; permission is needed before proceeding with installation/network access. Hash mismatch, unavailable compatible archives, or missing pinned Python must stop setup rather than select other versions. After successful setup, rerun the existing offline preflight using the locked environment and recheck all proposal bindings. Changed dependency/code/configuration bindings require a new proposal. A hash-checked install proves the accepted distribution archives; it does not retroactively attest how the older test environment was installed.

## Private credential setup — ABSENT in inspected execution environment

No dedicated OpenAI key tool is available in this session. The supported existing environment-variable mechanism was inspected using name membership only (`'WEEK4_OPENAI_API_KEY' in os.environ`), before environment clearing. Result: **absent in this execution environment**. No key value was fetched, no credential file was opened, no key validity was checked, and no authenticated discovery was performed. A different private terminal's environment is not attested by this result.

In a clean private zsh terminal, obtain a dedicated Week 4 key through your provider account and enter it via a masked prompt:

```zsh
unsetopt XTRACE
read -rs 'WEEK4_OPENAI_API_KEY?Dedicated Week 4 API key (hidden): '
printf '\n'
export WEEK4_OPENAI_API_KEY
```

Run these privately; never paste the value into chat, command arguments, source files, plans, shell history, project artifacts, or original-project files. Do not create a project credential file or automatically source an original environment. Do not use `env`, `printenv`, or debug tracing to display secrets. No LangSmith credentials are required. Use a clean shell without ambient tracing variables. Entering the key at the prompt is not a model call or authorization.

A value-free presence check is:

```sh
.venv-week4-py311/bin/python -c 'import os; print("PRESENT" if "WEEK4_OPENAI_API_KEY" in os.environ else "ABSENT")'
```

This checks the variable name only, not nonemptiness, validity, account permissions, or model access. A terminal export does not automatically populate this agent's tool environment. The actual authorized execution process must receive it through private environment injection; do not send the value to the agent in chat. Remove it from the private shell afterward with `unset WEEK4_OPENAI_API_KEY`.

## Public pricing and lifecycle refresh — unchanged

Official pages fetched again on 2026-10-29 retain the snapshot, Chat Completions/structured-output compatibility, 1,047,576-token context, and 32,768-token model output limit. Listed rates remain $0.40 input, $0.10 cached input, and $1.60 output per million tokens. [Official model and pricing documentation](https://developers.openai.com/api/docs/models/gpt-4.1-mini).

The model remains deprecated with removal scheduled for January 14, 2027. The proposal's January 13 UTC cutoff remains appropriate; no replacement or rate change is needed for this preparation. Public availability does not establish this account's access. [Official deprecations](https://developers.openai.com/api/docs/deprecations).

Calculation, with no cache savings: `5 × ((1,047,576 × 0.40 + 1,536 × 1.60) / 1,000,000) = $2.107440`. The full-context input reservation is conservative, not exact token counting; the independent complete-request byte bound remains 65,536. System/schema/advisory/state content is included in that dispatch bound. Maximum completion 1,536, worker timeout 120 seconds, HTTP phase timeout 20 seconds, reservation and reconciliation controls are unchanged.

## Offline preflight and preservation

Fresh [results](../reports/week4/smoke016-v2-3-final-approval-preflight-1/result.json) and [14 passing tests](../reports/week4/smoke016-v2-3-final-approval-preflight-1/unittest.txt) are recorded separately from the sealed proposal. The existing loader passed configuration, source/component/archive/input binding, policy, lifecycle and budget checks. Missing authorization was rejected before credentials or clients. Application guards recorded zero network, SDK-client, and command attempts; OS network denial was enabled.

The exact proposal's 12 sealed artifact entries and prior verification's 3 entries match. All **328 inherited files**, **50 reviewed assets**, **11 prior active sealed manifests / 410 entries**, and older proposals match. The baseline manifest was not regenerated.

The original all-file snapshot audit is **FAIL** for one Finder metadata file: `data/week4/smoke-proposals/.DS_Store`. Old digest `e4a3ee2b26aa996e3ee819a12c09e40651f6f17628a87a7e87e57462ff1fabb6`; current digest `f8eb84ad091805775b216d88737bb13c7ad336b58643a902d94f5b9f72eae9a9`. It was not restored or normalized. All other 866 snapshotted entries match; the metadata file is outside proposal bindings. The fresh report explicitly separates this mismatch from protected-content PASS.

Reproduce the read-only preflight:

```sh
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-py311/bin/python -m scripts.week4_smoke016_v2_3_approval_preflight
```

The preflight script creates no model/client or workflow; it cannot execute the smoke. Account access, actual provider request acceptance, usage receipts, and real behavior remain **unverified**. Semantic accuracy and actual cost remain null.

## Approval request to present after reporting blockers

Do you approve exactly one future W4-REAL-016 development smoke using V2 and gpt-4.1-mini-2025-04-14/default, proposal real-016-v2-3 with the plan SHA-256 above, maximum $2.25/five calls/zero retries, external tracing and incident tools OFF, **only after hash-locked dependency setup and private key presence are verified**? Account access and real provider behavior remain unverified. No execution is authorized by this document; installation permission is separate from paid-run approval.
