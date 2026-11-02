# API Troubleshooter

An evaluation-driven extension of my Week 3 multi-agent API troubleshooting app. Week 4 tests whether it provides useful, grounded explanations and safe diagnostic next steps on 30 reviewed cases.

**Status: portfolio/research project, not production-ready.** Evaluation found excessive abstention, brittle evidence handling and safety overblocking. Failures and regressions are included.

## Evaluation and submission

- [Complete evaluation report](docs/week4-evaluation-report.md): methodology, three changes, measured impact, monitoring proposal and limitations.
- [Scored workbook](outputs/week4-completion-30/week4-evaluation.xlsx) (download to view).
- [Frozen dataset](data/week4/datasets/assignment-30-v1/manifest.json).
- [Paired baseline/final evidence](reports/week4/baseline-treatment-grading-2/README.md).
- [Final paired scorecard](docs/week4-paired-final-scorecard.md).
- [Submission checklist](docs/week4-submission-checklist.md).

| Metric | Baseline | Final treatment |
|---|---:|---:|
| Diagnostic correctness | 0/30 | 1/30 |
| Appropriate uncertainty | 4/30 | 7/30 |
| Grounding | 4/30 | 7/30 |
| Median case latency | 4.144s | 4.274s |
| p95 case latency | 13.033s | 12.108s |
| Total usage-priced cost | $0.0681888 | $0.0730880 |

One live run per arm used identical frozen inputs and `gpt-4.1-mini-2025-04-14`. Human scores assess saved response content; UI delivery was not verified. All quality targets remain unmet. Combined results do not isolate each change's contribution. The original resolution-wording failure path was not reached in the final live run, so that fix has offline evidence only.

The dataset includes 24 public-report cases, one controlled reproduction with a mock upstream, and five artificial cases. Public reports are attributed evidence, not independently authenticated production captures. Development exposure, family overlap, scenario imbalance and one adversarial case limit generalization. Third-party reports retain their original rights; the project license does not relicense them.

The application uses React/TypeScript, FastAPI, five LangGraph agent factories and PostgreSQL. Week 4 adds local tracing, reviewed references, evidence attribution and supervised provider accounting. Incident tools and external trace exports were disabled during the submitted runs. Installed environments, caches, credentials and submission ZIPs are excluded from Git. Selected submission evidence is explicitly committed under `reports/`; other reports remain local.

## Setup and historical preparation notes

Use the setup commands below with isolated databases, ports and volumes. The [Week 4 adapter README](evaluation/week4/README.md) documents evaluation entry points. Copy `.env.example` to a private `.env`; never commit it. Live evaluation requires a dedicated `WEEK4_OPENAI_API_KEY` and explicitly approved, bounded plan. Recheck model availability/prices before future execution. Cloning this repo does not authorize paid calls.

**The remainder of this README is the original preparation record.** Statements below about no executions, missing dependencies or a fresh repository describe that earlier milestone, not the completed evaluation or current publication. [The evaluation report](docs/week4-evaluation-report.md) is the source of current results. Historical tests are not claimed as rerun during publication.

Week 4 GenAI cohort project: systematic evaluation of the inherited Week 3 AI API Integration Troubleshooter. This is an independent source copy, not a new implementation or an evaluated improvement. No models, services, databases or tests were run during preparation.

The inherited application is React/TypeScript + FastAPI + five LangGraph agents, with PostgreSQL jobs, checkpoints, SSE and grounded tentative reports. Original package/API/database identifiers remain unchanged. See [Week 3 README](README.week3.md) for inherited instructions; those instructions are historical and are NOT permission to reuse the original environment.

## Safe setup status

Static inspection confirms Python 3.11, uv/hash-locked requirements.lock, npm/package-lock.json and Node ^22.12.0 or >=24.0.0. Dependencies are not installed in this copy. Future installation commands, not executed during preparation:

```bash
uv venv --python 3.11 .venv
uv pip sync --python .venv/bin/python --require-hashes requirements.lock
cd frontend
npm ci
```

Copy `.env.example` to a private `.env` only when ready to configure this project. All credentials and connection URLs are blank; original credentials were not copied. Provision NEW isolated database, checkpoint and test targets before running migrations or services. Migrations 0001–0008 are inherited; checkpoint setup is separate. Nothing is automatically migrated here.

Do not run inherited Docker/startup commands blindly: Compose defaults to host port 5432 and a project-scoped volume, the Vite proxy points to 127.0.0.1:8000, and frontend/browser test ports can collide with Week 3. Use a distinct Compose project name, new volume, verified unused ports and isolated database names. The hard-coded health check and test DB initializer also need review before changing the inherited default DB name. Vite proxy reconfiguration is deferred; stop or isolate the old backend before using the inherited proxy. Shell environment variables can override a private dotenv file; use a clean shell and never inherit the original database, model or tracing credentials.

No worker deterministic-mode switch is assumed. Starting the ordinary worker with model credentials can incur charges; manual UI execution has no universal evaluation spend cap. Keep durable execution and diagnostic contracts disabled. No paid execution or tracing export is approved.

## Evaluation work

See [initial assessment](docs/week4-initial-assessment.md), [Week 4 scope](docs/week4-scope.md), and [source provenance](docs/source-provenance.md). Frozen synthetic V1/V2 inputs and evaluator-only labels are inherited unchanged. They are NOT a newly reviewed golden dataset or guaranteed untouched holdout. Labels, rubrics and human-only reviews must stay out of inference inputs.

Private historical reports and human reviews were excluded. Tests marked `private_audit` intentionally require authentic excluded archives; do not fabricate them or describe their skips as verification. Portable synthetic fixtures are retained. Other maintainer acceptance scripts may require original-local/private prerequisites; inspect before execution.

MIT project license and THIRD_PARTY_NOTICES.txt are retained verbatim. Dependency license limitations remain documented; no installed dependencies or build bundles are distributed. This repository has a fresh main branch with no commit or remote.
