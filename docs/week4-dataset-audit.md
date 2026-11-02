# Week 4 candidate audit — offline draft

2026-10-28. No golden dataset exists yet. This audit reads local public source and artifacts only; inherited historical claims are not reproduced results. No external public site, private archive, database or original project was accessed.

## Assets and provenance

`data/week4/candidate-inventory.csv` contains 200 incident candidates and 15 separate fixture/artifact records. Fixture records are leads, not 15 additional independent incidents. Every row remains NOT_REVIEWED; scenario tags are provisional collection roles, not human labels. An HTTP error can be a happy diagnostic task: “happy” means sufficient evidence for a supported diagnosis and safe next step, not HTTP 200.

| Source | Static finding | Limitation |
|---|---|---|
| `data/generate_incidents.py`, `data/incidents/` | 120 programmatically generated records, 80 development/40 test; fixed seed 314159; 24 status/cause templates | Generator cause strings are unreviewed hypotheses; repeated templates; inherited README reports 34 normalized cross-split groups |
| `data/benchmark_v2/scenarios.py`, `build.py`, committed manifest and audit | 80 programmatically generated records, 40/40; 16 families, five variants each; seed 1324001; 24 complete/16 ambiguous per split | Family-disjoint split is structural only; same synthetic specification; initial/pre-final audits describe older drafts, not extra candidates |
| V2 `semantic_rubric.json` | Independent semantic review design, status NOT_REVIEWED | No current reviewed answers or reviewer authority |
| `tests/fixtures/inc0025_investigator.json`, `inc0110_investigator.json`, V2 classifier/investigator fixtures | Previously used model-output regression artifacts over synthetic incidents | Observed agent failures are not real-world API incidents or new incident inputs; provenance does not make their answers correct |
| `tests/fixtures/publication/README.rst` and JSON projections/templates | Sanitized synthetic state/output projections and preparation templates; deliberate negative safety strings | Mixed authorship; template review flags confer no human approval; no standalone incident established |
| `manual_issuer_hold.json`, `manual_issuer_final_hold.json` | Origin metadata describes sanitized persisted application states, original provider wording unavailable | Observation of a workflow state does not establish a real incident; input authenticity, capture chain and independent source remain unknown |
| Public repository evaluation documentation | Historical prior-use and failure descriptions | Reports/receipts/reviews excluded; planned single-case dispatch is not proof that dispatch happened |

No verified real observed incident input is available in the audited set. Human-authored simulation content is visible in generator scenario specifications, but generated variants are classified programmatically generated. No standalone simulation is promoted to a reviewed case. No incident generator inspected calls an LLM. Model-authored *output* fixtures do not establish LLM-authored *input* cases; mixed/unknown fixture provenance remains unresolved. External LLM assistance in authoring specifications cannot be ruled out by absence of model calls in Python. Obtain an author declaration before certifying the LLM-generation fraction. Unknown sources cannot be counted as proven non-LLM.

## Prior-use and contamination

`evaluation/README.md` explicitly describes failed pilot outputs INC-0110 and INC-0025 and subsequent regression use. `evaluation/EVIDENCE_REFERENCES.md` records V2-02-01 classifier failure and compatibility replay; `V2_SINGLE_VERIFICATION.md` and `V2_LIVE_HANDLES.md` describe further preparation, not new dispatch authorization. Exclude these from independent reserved evidence. All jwks-stale-cache variants share that exposed family. V1 equivalents across splits share mechanisms; moving an ID does not remove leakage. Development records are development-exposed even if exact execution is unknown. Remaining test IDs have unknown history, never “untouched.” This planning audit has inspected the catalog itself; future reservation requires explicit exposure disclosure.

Needed history: authorized case-ID/run manifest crosswalk, prompt/routing development records, selected subset membership, dates and code versions, replay/fixture derivation map and owner attestation on family exposure. Request a minimal redacted summary; do not reconstruct excluded ledgers or private human reviews.

## Recommended collection target

Freeze only after review: **40 cases = 20 happy + 12 edge + 6 known-failure + 2 adversarial**. These are mutually exclusive primary strata; secondary tags may overlap. Suggested sourcing target:

| Stratum | Count | Collection proposal |
|---|---:|---|
| Happy | 20 | 12 distinct authorized real incident episodes + 8 independently reviewed programmatic cases |
| Edge | 12 | 6 distinct authorized real episodes + 6 reviewed simulations/programmatic cases with missing or conflicting discriminating evidence |
| Known-failure | 6 | 4 distinct real episodes with documented prior agent failure + 2 inherited regression-derived complete inputs, explicitly reused |
| Adversarial | 2 | New human-authored complete incident inputs containing instruction injection or credential solicitation bait, no real secrets |

Thus target 22 real, 16 programmatic/simulated and 2 human-authored adversarial cases, zero intentionally LLM-generated. This is a collection proposal, not existing evidence or a claim the 22 incidents exist. A real incident counts once; paraphrases, alternate captures and mutations remain the same episode/family. The current source pool can supply many draft synthetic candidates but cannot credibly fill reviewed real-preferred sourcing, six evidenced failures, or two complete adversarial cases. It does **not yet meet** assignment sourcing/review requirements. Below 20% means at most 7 of 40 LLM-generated cases (8 is exactly 20%); target zero and resolve unknown authorship before freezing. If real evidence cannot be supplied, obtain an explicit assignment ruling permitting a synthetic-heavy benchmark and disclose its limitations; do not silently substitute.

For real episodes, request owner permission/license, sanitized original input and capture chain, episode ID and deduplication key, relevant API documentation/version and incident chronology, verified mechanism/resolution evidence, observed outcomes and prior agent exposure. For USGS specifically request owner-selected sanitized request/response pair, endpoint/method/parameters, capture time, relevant official contract/version, expected versus actual behavior and evidence of outcome. A status code or public contract alone cannot verify a cause. Private reports and USGS captures are outside this task; nothing was copied or reconstructed.

For each draft, reviewer checks schema, redaction, independence, sufficient versus ambiguous evidence, allowed alternatives, supporting/counterevidence, prohibited claims/actions, legitimate hold and applicable stages. Use one genuine human reviewer initially; independent second review is optional, with disagreements adjudicated if performed. Leave reviewer identity, timestamps and confirmations blank until actual review. Review the expected answer against evidence, not generator intent. Remove or correct unsupported expectations in a new draft version. Maintain drafts under `data/week4/drafts/` in a future phase; a separate versioned `golden/` artifact contains approved inference inputs and evaluator-only expected behaviors, hashes and genuine review records. Neither directory is created or populated by this planning task.

## Verification

Read-only SHA-256 and byte-size verification matched all **328** inherited manifest entries, including application files, inherited datasets and README.week3.md. Manifest SHA-256: `0ad4421d9342b780996b70de8b72d9d0cab1b771e6f37fd82dd4c5ccbf42b62f`. Verification was against this copy's manifest, without accessing the original directory. New planning documents and inventory are outside manifest scope. This is file integrity evidence, not application testing or semantic dataset validation.
