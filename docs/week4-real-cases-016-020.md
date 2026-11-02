# Reviewed cases 016–020 — import and offline input compatibility

All five user decisions are recorded as **ACCEPTED**, with reviewer attribution
**User in this conversation**. The v5 acceptances of 016–019 are retained; 020's
acceptance comes from the current explicit instruction after v5. Exact review,
confirmation and recording times remain null, as do semantic scores. Actual import
processing time `2026-10-29T02:39:34.670532+00:00` (UTC) is separate and is never substituted for
human review or an incident timestamp. No independent reproduction, remediation
confirmation, signatures or additional approval is claimed.

## Counts: acceptance is not runtime or golden readiness

| Scope | Human-accepted | Schema-pass | Evidence-preserving input-compatible | Graph-executed | Golden-ready |
|---|---:|---:|---:|---:|---:|
| This batch 016–020 | 5 | 5 | 5 | 0 | 0 |
| Cumulative local reviewed cases 001–020 | **20** | **15** | **14** | **0** | **0** |

The extra schema-only case is **007**, whose diagnostic signature is damaged by
inherited sanitization; it is excluded from the 14 supported proposals. Cases
001–004 lack required source fields and 010 lacks a transport status. Those six
cases remain blocked, including 007's evidence-preservation blocker. No old
blocker or human decision was overwritten to improve the count. These are local
import/compatibility counts; previous external model usage remains unknown.
The [cumulative count record](../data/week4/reviewed-candidates/batch-016-020/cumulative-counts.json)
records that scope and the exact exclusions.

Input-compatible means the proposed mapping passes the existing schema,
sanitization, initialization and scalar/handle catalogs without diagnostic
content loss. It does not mean graph selection/routing, causal reasoning,
remediation, real endpoint behavior or semantic grading passed. All source
`runtime_ready` flags remain false and review runtime statuses remain pending.
No final stratum or split was assigned.

## Per-case report

| Case | Status/observation provenance and preserved evidence | Editorial runtime operation goal | Unknowns and remaining limitations | Compatibility |
|---|---|---|---|---|
| 016 | Reported curl **GET /ocelot/posts/askdj / 502**, Content-Length 0; exact `skull: 💀`; `System.Net.Http.HttpRequestException: Request headers must contain only ASCII characters.`; sample tag 24.1.0 | Handle the reported GET request with appropriate error handling | No paired successful request or verified remediation. Removing the header is only a proposed diagnostic comparison; no upstream outage or released gateway fix established | PASS schema, unchanged sanitizer, initialization and catalog. Unicode scalar is preserved literally in the catalog |
| 017 | Proxy/backend access-log reports both show **PUT /remote.php/webdav/x27.dat / 412**; original reporter later observes concurrent updates by two clients | Update the requested file respecting write preconditions and overwrite protection | Actual conditional headers/ETags and exact failed precondition absent. Contributor If-Match explanations remain evaluator-only; later other-user failures are separate. No bypass of overwrite protection | PASS schema, unchanged sanitizer, initialization and catalog; conditional-write cause remains a qualified hypothesis |
| 018 | Published server-log report pairs **POST /api/v4/projects/2/issues / 409**; reported creation during import and conflicts after import; “Duplicated issue” and counter suspicion explicitly reporter-attributed | Create the requested issue in the specified project | Exact request payload/counter defect unresolved. Separate UI/import uniqueness diagnostics are not merged into this API trace. Publication date remains null; log dates do not replace it. No DB repair, guessed identifier or blind retry | PASS schema, unchanged sanitizer, initialization and catalog; no server execution or counter verification |
| 019 | Capture excerpt shows **GET /login?return_to=http%3A%2F%2Fx.x.x.239%2Frepositories%2F1 / 406**, labeled 16.7.3; earlier 16.2.1 **GET /api/v3/repositories/1 / 200** comparison | Complete the reported API-driven repository import; exact request chain unspecified | Source prose says **16.7.2** while capture says **16.7.3**; discrepancy preserved, not resolved. Host masking/encoding retained verbatim. No replacement with intended repository endpoint, invented redirects, or later code-level explanation promoted into evidence. Source date remains null | PASS schema, unchanged sanitizer, initialization and catalog; exact import chain/configuration still unknown |
| 020 | First URL transfer: **HEAD / to envoy-egress:8080 / 503**. Separate second URL transfer: **HEAD / to www.google.com / 200**. Exact two-URL command retained as reported text. Earlier TLS WRONG_VERSION_NUMBER/400 context is from a different attempt | Provide a response to the reported HEAD request; proxy-versus-direct intent remains explicitly unspecified | No proof second transfer used a proxy; no correlation of earlier TLS/400 material to this HEAD/503 response. Source `-k` is not a recommendation; no TLS-verification bypass. Intent/goal mapping remains unresolved | PASS schema, unchanged sanitizer, initialization and catalog. **HEAD already supported** by inherited allowlist; no contract change |

The neutral operation goals are explicitly editorial mappings, not new human
confirmations or copies of evaluator diagnoses. Case 020 does not acquire an
invented “proxy Google successfully” goal. Case 016 preserves appropriate error
handling rather than asserting a desired exact status or a repaired upstream.

## Inference/reference separation and evidence preservation

[Normalized review records](../data/week4/reviewed-candidates/batch-016-020/reviewed-candidates.json)
are separate from [evaluator references](../data/week4/reviewed-candidates/batch-016-020/evaluator-references.json)
and the five `inference/W4-REAL-016.json` through `W4-REAL-020.json` files under
`data/week4/reviewed-candidates/batch-016-020/`.

Original v1/v5 source files were copied byte-for-byte to `sources/`. Their raw
evidence is identical between versions. The normalized records update stale
NOT_REVIEWED flags using current authority; archived source flags are not edited.
The one explicit observational addition is 019's prose/capture version discrepancy:
the source proposal and current user identify the prose as 16.7.2, while the
inference excerpt labels capture 16.7.3. Both are preserved with named scopes;
no contributor causal explanation was copied into inference. This authorized
addition is logged in import provenance and is not represented as a captured
measurement or a byte-identical normalized v5 file.

**No diagnostic evidence was lost through sanitization or catalog construction.**
All supplied method/path/status values and attributed observations survive.
The skull remains U+1F480 `💀` in both JSON and the trusted scalar catalog.
The ASCII exception stays verbatim. The source-masked URL text is never decoded,
unmasked or replaced. Reported warning/exception statements stay prose rather
than manufactured timestamped or typed log events. `logs=[]` means no typed log
records were supplied here, not that no source logs existed. Body nulls mean not
transcribed/available, not observed JSON null; that distinction is recorded in
metadata. Existing unknown severity/evidence-quality defaults are not ratings.
No source event time, request ID, header, payload, host, version or outcome was
invented. Local offline-check thread IDs are validation context only, not source
request identifiers, and are absent from the proposed incident inputs.

Case 017 includes the original reporter's own concurrent-update observation,
but no captured `If-Match` header or ETag is invented from contributor advice.
Case 018 retains the reporter's counter suspicion as a suspicion, not a proven
counter defect, and contains no separate UI uniqueness trace or repair commands.
Case 019 preserves the observed login endpoint even though the high-level intent
is repository import. Its successful repository-path comparison remains a
separate historical request, not the observed failing endpoint or a fabricated
redirect hop.

For 020, the supplied command is retained exactly as inert evidence:

```text
curl -v -k http://envoy-egress:8080 -I http://www.google.com
```

**It was not executed and is not recommended practice.** The projection labels
its two URL transfers, lack of established Google proxy use, different-attempt
TLS/400 context and unresolved intent. Earlier logs are not rewritten as correlated
facts of the HEAD/503 exchange. No structured synthetic log events were made to
exercise routing guards. The third reported observation retains its own explicit
different-attempt qualifier. Model behavior on that ambiguity remains untested.

Source URLs/dates, review decisions, families, grading expectations and later
contributor interpretations remain evaluator-only. The actual inference files
were inspected and tested for those fields and answer strings, not only for
schema success. An evaluator-only answer injected into metadata is rejected by
the existing Week 4 boundary. No agent graph, request command or model-input SDK
call was executed to make these checks pass.

## Family/source overlap and eligibility

The overlap report compares exact source URLs with 001–015 and exact family
labels against all **230 prior inventory IDs**; no exact source/family match was
found. That result does not prove independence:

- 016's linked **#2374/#2375** belong to the same Ocelot report family, not extra
  independent incidents. Header/media handling also overlaps broadly with 006/010.
- 017/018/014 share write-conflict/concurrency exposure, but a 412 precondition,
  import-associated 409 and 500/write inconsistency are not one proven cause.
- 019/018 share GitLab importer exposure with different reported operations and
  unresolved defects. The login/access ambiguity also overlaps broadly with 011/008.
- 020 has broader transport/TLS/proxy ambiguity alongside 002/005, not established
  causal equality. Different attempts and separate URL transfers are not additional
  independent incidents or proof of one causal chain.

All are development-exposed AI-curated public reports, not independently
reproduced captures. Previous external usage and full semantic/family independence
remain unverified. Publication/redistribution rights are unadjudicated. No holdout,
final split or golden-set eligibility follows from these imports. Qualified causal
hypotheses and unresolved goals require later review before evaluation freezing.

## Identity, preservation and verification

Actual import processing time: `2026-10-29T02:39:34.670532+00:00` (UTC), not a review time.

- v1 source SHA-256: `1afd93762b41edf0a4777edd80aef8e41fdc0b9cb32b3db5eeb35d578fc9337a`.
- v5 source SHA-256: `b503fdd5ee0f7e5ab2a403f8b05bfbaeeef6a1e88f721098a5d4dab9d2029893`.

[Import provenance](../data/week4/reviewed-candidates/batch-016-020/import-provenance.json)
and [verification](../data/week4/reviewed-candidates/batch-016-020/verification.json)
record source identity, authority for the newly accepted 020, import time,
observational additions and preservation of **33 prior review JSON artifacts**.
All original files and earlier decisions/import times are unchanged. Repeated
import leaves every batch JSON byte and the inventory unchanged, retains import
time, and refuses differing destinations/decisions. Earlier import checks now
bind their original historical prefixes/artifact sets rather than counting later
batches as changes to past decisions.

The inventory now has **235 unique IDs**. Its original 230-row prefix still hashes
to `ba82e186f1fb9ced192f2c7727260864414c6e96d9c121e99eb7e405aa8df537`; new inventory hash is `753d463e4aed3f1fd6e18fc4fc618c723d895ffa4be3b3111f0c2df31751269b`.
Rows were appended by explicit IDs; no old record or accepted decision was replaced.
All new scenario/final-split assignments remain unassigned.

Focused isolated-environment command, with sockets and DNS denied:

```sh
.venv-week4-py311/bin/python -m unittest scripts.week4_reviewed_compatibility_tests scripts.week4_reviewed_batch2_tests scripts.week4_reviewed_batch3_tests scripts.week4_reviewed_batch4_tests -v
```

**39 tests passed**, including earlier-batch regressions, source identity, Unicode,
HEAD allowlist support, exact paths/versions, transfer correlation boundaries,
editorial goals, evidence preservation, reference separation, count discipline,
idempotence and baseline integrity. No model mock was needed; no graph, agent or
provider SDK was imported by these tests. `initialize_state` is input-state
validation, not graph execution. Catalog success does not prove readiness/routing
coverage or semantic diagnostic quality.

**All 328 inherited files match SHA-256 and byte size** in the existing manifest.
The manifest hash is `0ad4421d9342b780996b70de8b72d9d0cab1b771e6f37fd82dd4c5ccbf42b62f` and it was not
regenerated. Inherited contracts, prompts, routing, sanitization and safety rules
were untouched. No live models, tracing, incident/API requests, installations,
services, databases, Docker, commits/remotes, smoke execution, original credentials
or original-project access/change occurred.

Smallest next action: review operation-goal mappings and family roles, particularly
020's unresolved proxy intent and 019's missing request chain/version discrepancy,
without replaying either command or write endpoint. Collect authentic missing
headers/ETags, request context or causal evidence only if available. Keep all
hypotheses qualified and the six earlier runtime blockers intact; no case is
promoted to a frozen golden set by acceptance or ingress success alone.
