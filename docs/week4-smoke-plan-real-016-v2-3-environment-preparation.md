# Week 4 proposal 3 — environment preparation

The exact documented setup commands completed successfully after installation/download approval:

```sh
.venv-week4-py311/bin/python -m venv .venv-week4-locked
uv --cache-dir .cache/week4-uv pip sync --python .venv-week4-locked/bin/python --require-hashes evaluation/week4/requirements.lock
.venv-week4-locked/bin/python -m evaluation.week4.dependencies
```

The new isolated environment contains all 88 locked packages with Python 3.11.16. The fresh sync enforced archive hashes and exited 0. No packages or lock files were changed in the older environment; only the dedicated new environment and project-local download cache were installed. The existing configuration tests briefly use their preexisting Week 4 test scratch directory, which they clean up.

All 14 existing configuration-only controls passed in the new environment under OS network denial. Proposal code/dependency/configuration/input/archive bindings passed. All 328 inherited baseline files and 50 reviewed assets match; prior sealed results and proposals match. The previously disclosed Finder .DS_Store discrepancy remains outside bound content and is preserved. No baseline manifest was regenerated.

Installation changed **no proposal-bound code or dependency hashes**. Package versions match, and the sealed proposal was not rebound. The existing preflight still emits a fixed historical “installation not performed” string, and the version helper does not itself attest archive integrity. Raw output is preserved; the successful fresh --require-hashes installation receipt establishes archive integrity for this environment. No code was changed to hide the old message.

Status: **ENVIRONMENT PREPARED; PRIVATE KEY / FINAL RUN APPROVAL OUTSTANDING**.

The dedicated WEEK4_OPENAI_API_KEY was absent in the inspected execution environment. Presence was checked by variable-name membership only. No secret value was fetched, printed, saved, or tested. A private terminal export does not automatically populate this agent's execution environment. Configure it privately in the actual execution environment and recheck presence without displaying its value. Existing private instructions remain in [final-approval setup](week4-smoke-plan-real-016-v2-3-final-approval.md). Do not put a key in .env.example or project artifacts.

Use **.venv-week4-locked/bin/python** for subsequent authorized checks or execution; the parent supervisor uses the current interpreter for its child. No smoke command was run during setup.

Exact proposed run, still unauthorized:

- real-016-v2-3, plan SHA-256 `69e756641250cd698921804cb4dbde0757c6c9e84fa75c04821c29e8b7446acb`.
- Immutable authorization identity `a996d40dd93440d58ed722e2eb9999d98d40a9165d676300db6ac5b1aa8322b4`.
- W4-REAL-016; attributed-report-readiness-v2.
- gpt-4.1-mini-2025-04-14; default tier; no fallback.
- Maximum $2.25; at most five calls; concurrency one; zero retries. Conservative five-call reservation $2.107440.
- External tracing, exports, and incident tools OFF.
- Account access and real provider behavior remain unverified.
- execution_authorized=false, trace_export_authorized=false; approval identity/time/binding unset.

[Installation, dependency check, raw preflight, 14-test output, and final assessment](../reports/week4/smoke016-v2-3-environment-preparation-1/result.json) are fresh records. No model calls, authenticated discovery, trace exports, incident requests, services, databases, commits or remotes occurred. Actual cost and semantic accuracy remain null.
