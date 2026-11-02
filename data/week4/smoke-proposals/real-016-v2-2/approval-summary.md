# Proposal 2 — BLOCKED, not an execution request

Case: W4-REAL-016, unchanged versioned source projection. Policy: attributed-report-readiness-v2. Model: gpt-4.1-mini-2025-04-14. Tier: explicit default. No fallback, retries, diagnostic tools or external tracing. Local durable traces and usage remain enabled.

The complete request byte cap is 65,536. The conservative input reservation is the model's full 1,047,576-token context, not a byte/character token estimate. Completion cap is 1,536 total tokens. Maximum calls: five; concurrency one; worker timeout 120 seconds; HTTP phase timeout 20 seconds.

Real listed-rate reservations: $0.421488 per call, $2.107440 for five. The unchanged $0.25 hard stop rejects the FIRST dispatch. $2.11 is only a candidate rounded minimum, neither implemented nor authorized. A narrower justified counting bound or separately authorized ceiling change is still required. Account access remains unverified.

Execution authorization: false. Trace-export authorization: false. Approval identity/time: unset. No live smoke occurred; all semantic review fields remain blank.

Plan SHA-256: 9e5c4c017a6020d9fb8cb243edb8ec04e1f53ad9877f472ecb055448e9b7403c
Configuration canonical SHA-256: 3b8b70d513015ce6a0625ecf282765d446e3d8ae67f138f06d3285ad505245c0
Input bytes SHA-256: 30ece2362f9b8623b12568cc6726215d407604fcc92b3cae2c1e4c3c0f29410c
Archive SHA-256: dbc8ea81f66eba30c74cba89b08ab1c1ceee230886825f4f4f0acca429916d9f

[Machine plan](plan.json) · [Implementation report](../../../../docs/week4-supervised-v2-provider-verification.md) · [Blank worksheet](review-worksheet.json)
