# Approval summary — BLOCKED, not an execution request

Plan version: `week4-real-016-v2-live-smoke-proposal-1`

- Case: `W4-REAL-016`, exact revised input bound in plan.json.
- Policy: `attributed-report-readiness-v2`, no fallback.
- Model candidate: `gpt-4.1-mini-2025-04-14` (deprecated; scheduled shutdown 2027-01-14; account access unverified).
- Proposed maxima: USD $0.25; five calls; 65,536 reserved input and 1,536 total completion tokens per call; concurrency one; zero retries; worker timeout 120 seconds; HTTP phase timeout 20 seconds.
- Conditional five-call reservation: $0.143360 at published rates with no cache hits assumed.
- External tracing/export OFF; sanitized local durable spans/usage retained; no diagnostic tools.
- Execution authorization: **false**. Trace-export authorization: **false**. Approval identity/time: **unset**.

Blockers: V2 live path absent; current CLI rejects this version; proposed input bound rejected by current config; default service tier/token envelope unbound; account access and concrete dynamic schema acceptance unverified. No compatible live command exists. Do not execute the old runner or substitute policy/model.

Implementation work would change hashes, requiring a new proposal and explicit authorization for its exact version/hashes before any paid call. This document does not reauthorize the earlier smoke plan. No human semantic grade has been filled.

Bindings:

- plan.json SHA-256: `9f7dd83f6a8552d564f050bc79d068c6ecdebc9290a36b7132d4213eb2775bca`
- exact input SHA-256: `30ece2362f9b8623b12568cc6726215d407604fcc92b3cae2c1e4c3c0f29410c`
- source archive SHA-256: `dbc8ea81f66eba30c74cba89b08ab1c1ceee230886825f4f4f0acca429916d9f`
- configuration SHA-256: `ecdadaaec1d692007dd30b00b262b1dc7067e741e9b6671bd5daa0d09503223f`
- source-files digest: `b559b1e65acd6ad6e772b34e3ede3c8493bf9d70568a02d30a81705868c4d16f`
- V2 policy-files digest: `95110de68fcb97e932a4e8f9ebcf9e5de0f9e16c2af870f1e1e543ceb65037bc`
- readable report SHA-256: `aa67e74471b01e0dc34ad8e98c189dea71f78f2c2c4ca1bf296cb29b9d162b2d`

[Machine plan](plan.json) · [Full readable report](../../../../docs/week4-smoke-plan-real-016-v2-1.md) · [Blank worksheet](review-worksheet.json)
