# Five reviewed real-report candidates — import record

Imported the five decisions explicitly confirmed by **User in this conversation**.
This is content/scope review of development candidates, not independent incident
reproduction, model-output grading, a frozen golden set, reserved evidence,
publication approval or paid-execution authorization.

## Source identity and times

Structured source: `/Users/tagore/Documents/Codex/2026-10-25/w/outputs/api-incident-reviewed-v2.json`.
Byte-identical destination: `data/week4/reviewed-candidates/real-incidents-v2.json`.

- JSON SHA-256: `f3eb5764d834b6a65e4a54dfad61426fdeb08adc41bbe73e5ed703b8e826af28` (13388 bytes).
- HTML companion SHA-256: `220502c787d8b3789fed4a7d9051dbe156e2911ee8d54f74719e0033cd6f1e74` (6051 bytes).
- Actual import processing time: `2026-10-28T23:43:37.572925+00:00`.
- Source processing/recorded time, preserved: `2026-10-28T23:39:03Z`.
- Exact individual review/confirmation times: **unknown**. `reviewed_at` and
  `confirmation_at` remain null; import time is never substituted for them.

[Import provenance](../data/week4/reviewed-candidates/import-provenance.json)
records both source hashes, the exact authorized decisions and the distinction
between timestamps. The original JSON and HTML were read only; no source content
was modified. HTML was parsed as text, never rendered/executed or followed to
public URLs. All five IDs, decisions, source links, accepted expectations, review
qualifications and inference observations match between the local files. This
is a local consistency check, not independent verification of the public reports.

## Decisions retained

| Case | Confirmed decision | Qualification preserved | Original runtime status |
|---|---|---|---|
| W4-REAL-001 | ACCEPT_WITH_REVISIONS | Reporter's successful `data.`-prefixed comparison is present; not every expansion field is required | RUNTIME_MAPPING_PENDING |
| W4-REAL-002 | ACCEPT | TLS mechanism supported; underlying defect unconfirmed; no disabling verification | RUNTIME_MAPPING_PENDING |
| W4-REAL-003 | ACCEPT | Qualified version/acceleration hypothesis; no definitive credential/checksum diagnosis | RUNTIME_MAPPING_PENDING |
| W4-REAL-004 | ACCEPT | Ambiguous evidence; secondary limiting stays a hypothesis | RUNTIME_MAPPING_PENDING |
| W4-REAL-005 | ACCEPT | Generic transport-edge scope accepted; observed 302 differs from exception hint 400 | RUNTIME_VALIDATION_PENDING |

Every original `runtime_ready: false`, `semantic_scores: null`,
`execution_authorized: false`, `trace_export_authorized: false`, reviewer string,
null `reviewed_at` and recorded-at value was preserved. No new reviewer identity,
semantic rating, causal confirmation, remediation result or approval was created.
The reporter comparison in case 001 is legitimate source evidence even though it
is informative about the expected diagnosis; it is not removed as answer leakage.
Contributor/maintainer interpretations remain in evaluator records, not promoted
to independently captured measurements.

## Artifacts and separation

- `real-incidents-v2.json`: exact mixed source archive, **not an inference file**.
- `evaluator-references.json`: evaluator-only decisions, accepted expectations,
  URLs, source display headings, dates, families, scopes and grading prose.
- `runtime-assessment.json`: evaluator-only field maps, blockers and actual check
  outcomes; this does not modify the source's runtime flags.
- `inference/W4-REAL-005.json`: the sole proposed complete typed input. It contains
  no review/expected-diagnosis/source-URL/family fields. Cases 001–004 have no
  inference artifacts because missing runtime facts cannot be invented.
- `contract-test-results.json`: **14 wholly synthetic negative schema checks**,
  with safe genuine Pydantic errors. The invented fixture is never merged into a
  real candidate. No real candidate was filled with test values.
- `inventory-update.json`: append-by-ID audit of the existing inventory.

The case-005 projection is a proposed editorial mapping, not an additional human
confirmation. `/` is the observed path in `GET /`; no omitted host is reconstructed.
The neutral `expected_behavior` is an editorial operation-completion requirement,
not the accepted diagnostic answer. The exact observed GET/302 and quoted hint
400 remain separate. See [the runtime assessment](week4-runtime-compatibility.md)
for the provenance and routing limitations of this representation.

## Inventory update and exposure

Appended exactly W4-REAL-001 through W4-REAL-005 by explicit case-ID matching:
**215 original rows + 5 = 220 unique IDs**. The prior 215 rows were preserved
byte-for-byte as the existing file prefix. Its SHA-256 remains
`f81d1d279b809b429e1f0400d901558281a810a0578fe65d78dca6d26b55ed0c`.
The resulting inventory SHA-256 is
`e636f576e250162a477b937e5eb139430e2106cd4e921f1542f9be596cc19b42`.
No column change was needed: `review_status` holds the exact confirmed content
review decision; runtime compatibility is described separately in `limitations`
and the assessment artifact. `inherited_split=not_assigned` avoids claiming that
these new development candidates were in inherited benchmark splits. Case 005
has the confirmed provisional transport-edge role; strata for 001–004 stay
UNASSIGNED rather than fabricating golden composition labels.

These are public third-party incident reports with AI-curated paraphrases and
expectations, expressly human reviewed. They are not independently reproduced
real captures and not fabricated synthetic incidents. AI curation does not by
itself resolve an assignment's LLM-authorship accounting rule; disclose it when
adjudicating sourcing. They are development-exposed; exact prior agent execution
is unknown, not proven absent. Public redistribution rights remain unadjudicated.
No original private report, capture or credential was accessed, and nothing was
published. The existing synthetic smoke proposal was not repurposed or changed.

## Verification and smallest next action

Eight portable tests pass, including 14 synthetic negative contract checks;
source identity and HTML consistency; null review times; case-005 schema,
redaction stability, initialization and catalog; separation; no fabricated host,
status or log events; inventory preservation and differing-destination rejection.
The tests deny sockets and import no agent graph/provider SDK. A second import
verified identical destinations without changing the original import timestamp.

All **328 inherited files** match SHA-256 and byte size in the existing baseline
manifest. That manifest was not regenerated. No application/inherited fixture,
contract, sanitizer, grounding/routing/authorization rule, original project,
database or service was changed. No graph/model execution, external requests,
tracing exports, dependencies, commits/remotes or spending occurred.

Smallest next action: review the editorial case-005 projection and choose whether
it is an input/clarification example or should await authentic structured evidence;
collect the genuinely missing method/path/status observations for 001–004 where
they exist. TLS failure may have no HTTP response at all. Do not manufacture a
status to make case 002 fit. The options and comparability consequences are in
the runtime report; no option is implemented by this import.
