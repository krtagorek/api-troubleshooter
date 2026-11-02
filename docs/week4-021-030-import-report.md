# Week 4 cases 021–030: review import and remaining selection

The user's decisions are recorded as **User in this conversation**, with exact review/record timestamps, semantic scores, final splits and final eligibility unset. Source packets are evidence, not instructions. No source command was executed. The original JSON and HTML packet are archived byte-for-byte in [batch-021-030/sources](../data/week4/reviewed-candidates/batch-021-030/sources/). The HTML packet's ten evidence/expectation blocks match the candidate JSON.

New [reviewed records](../data/week4/reviewed-candidates/batch-021-030/reviewed-candidates.json), [evaluator expectations](../data/week4/reviewed-candidates/batch-021-030/evaluator-references.json), [runtime assessment](../data/week4/reviewed-candidates/batch-021-030/runtime-assessment.json), and [nine inference projections](../data/week4/reviewed-candidates/batch-021-030/inference/) are separate. Later source resolutions, expected diagnoses, source URLs/dates and family labels are evaluator-only. Generic endpoint goals are editorial, not additional human confirmations.

## Actual counts

| Measure | New batch | Entire current pool |
| --- | ---: | ---: |
| Unconditional ACCEPT with compatible input | 7 | 27, including the previous 20 |
| CONDITIONAL_ACCEPT with compatible input | 2 | 2: 022 and 028 |
| HOLD, no export | 1 | New case 030 excluded from selection |
| Technically input-compatible | **9** | **29** |
| Candidates with no outstanding case-specific sourcing condition | 8: seven ACCEPT plus 022's fulfilled archival condition | **28**; still not final eligibility |
| Outstanding conditional sourcing decision | 1: 028 | 1 |

The **technical shortfall is one input** (030 or a reviewed replacement). The **condition-cleared selection shortfall is two slots**: resolve 028's eligibility and replace/recover 030. If 028 is excluded, two replacement inputs are needed. Strictly unconditional ACCEPT alone totals 27; 022 remains a recorded CONDITIONAL_ACCEPT even though its stated prerequisite is now met. No final selection/freeze is asserted.

## Per-case import

| Case | Human decision | Status provenance / retained facts | Offline result and remaining qualifications |
| --- | --- | --- | --- |
| 021 | ACCEPT | Published POST /session request and 500; JSON header with Content-Length 0 | Input compatible. Empty-body parsing mismatch is qualified; no universal empty-POST rule or tested header fix |
| 022 | CONDITIONAL_ACCEPT | Archived original HTTP/2 500 plus access log for POST /api/v4/projects; missing-boundary error | Input compatible. **Archival condition met.** Reporter-published correlation, not authenticated trace correlation; no missing-avatar-only cause or proven fix |
| 023 | ACCEPT | Published POST /new/_index and HTTP 500; unauthorized design-document error | Input compatible. Investigate access policy; no storage-outage or security-bypass conclusion |
| 024 | ACCEPT | Published POST / access-log 403, missing-CSRF warning, text/plain form encoding | Input compatible. Rendered tag does not establish delivery; later enctype success stays evaluator-only |
| 025 | ACCEPT | Published POST /api/2/envelope/ 403 and RedirectView/CSRF warning | Input compatible. Distinguish external acceptance from internal rejection; do not prescribe browser cookies or disable CSRF |
| 026 | ACCEPT | Contributor v3 POST /todos 500; v2 comparison 201; two Content-Type header entries | Input compatible. Both ordered pairs survive separately; controlled comparison is not a guaranteed patch |
| 027 | ACCEPT | Published HTTP/1.1 GET / →502 transcript; reporter protocol/config comparison | Input compatible. No proven exact defect, DNS failure, TLS bypass or promised upgrade fix |
| 028 | CONDITIONAL_ACCEPT | Client POST /api/chat/completions log 400; **mock** upstream 429 and Retry-After 7; client header absent | Input compatible, **sourcing eligibility pending**. Third-party controlled reproduction, not production traffic or a real account quota event |
| 029 | ACCEPT | Published GET /keepalive.html HTTP 400 and empty Host | Input compatible. Empty value preserved; direct empty-string catalog leaf omitted by inherited catalog, but the attributed observation remains available. No readiness equivalence claimed |
| 030 | HOLD | 204/413 originate in stated expected-output text, not a captured exchange | Strict schema rejects transport status null. No 0/200/204 substitution; no runtime export. [Held proposal](../data/week4/reviewed-candidates/batch-021-030/held-030-proposed-input.json) preserves expected-output provenance outside the runnable folder |

All nine exports passed the existing InferenceCase schema, unchanged sanitization, initialize_state(max_retries=0), catalog construction and resolution. 030 failed safely. No graph, agent, model or incident command was executed. Valid input/catalog structure does not prove a readiness route, complete diagnostic evidence or semantic accuracy. Response bodies remain not-supplied nulls, not claimed wire captures; logs=[] does not assert absence of source logs. Attributed observations remain prose rather than fabricated log events/timestamps.

026 retains exactly `[["content-type","application/json"],["Content-Type","Application/Json"]]`. These are distinct list entries and catalog references, not a collapsed dictionary. The inherited catalog omits 029's direct empty-string Host leaf; the exact empty field and the reporter's observation remain in inference. No mapping/sanitization evidence changes were detected in the nine exported records. The omission is a catalog granularity limitation, not permission to invent a hostname or relax readiness.

## 022: archival prerequisite resolved

The web reader returned 429, but a bounded, unauthenticated GET to the [original GitLab report](https://gitlab.com/gitlab-org/gitlab/-/issues/385112) returned HTTP 200 and original issue JSON. The archive validates iid=385112 and project_id=278964. [Original response bytes](../data/week4/reviewed-candidates/batch-021-030/sources/primary-022-response.json) SHA-256: **96dfdb7854db8a90db327e01cb341a5833475d2aadd98a6b566f97e00c2ef5c9**. Its Content-Type is application/json; an initial `.html` filename contains the same raw JSON bytes, not a separately rendered page. The retrieval receipt documents this.

[Source binding](../data/week4/reviewed-candidates/batch-021-030/source-022-binding.json) records original excerpt positions/hashes for the 500 transcript, missing-boundary error and published log association. Same correlation ID/method/path appear in the reporter's workhorse error/access records. These establish what the source reports; hashes and matching strings do not authenticate a request trace or independently verify truth. The archive's proposed fixes/comparisons are not copied into inference. No new human review timestamp is inferred from source publication metadata.

## 028: exact remaining decision

The user must decide: **may this documented third-party bug reproduction using a mock upstream be included as a source-derived case under the course rubric, and how must it count toward the generated-case allowance?** It must never be labeled production traffic. Public provenance does not settle rubric eligibility.

The five existing artificial selections still consume five allowance slots. 028 is outside the condition-cleared pool while this classification is pending; its charge is **unresolved**, not asserted zero. If it must consume another allowance slot, do not include it as a sixth: exclude/replace it or separately approve removal/replacement of another artificial case. No such substitution has been made.

## Family overlap and exposure

024 and 025 share broad CSRF-rejection symptoms but different applications and hypotheses: form encoding versus relay/web routing. Do not transfer 024's later resolution into 025 or claim independent holdouts. Media-type cases 021/022/026 overlap broadly with 006/010; 028 overlaps rate-limit/status themes in 004/009; 027 overlaps gateway themes in 016/020. [Family audit](../data/week4/reviewed-candidates/batch-021-030/family-overlap.json) records these distinctions. All packets are development-exposed; earlier exposure is unknown. No final split is assigned.

## Proposed replacements — neither implemented nor approved

**For held 030:** review [FastAPI issue 1911](https://github.com/fastapi/fastapi/issues/1911) as a new source-backed candidate, not as a relabeled 030. The reporter supplies a POST /upload_two_files access-log 422 alongside body validation identifying a missing second_file. Investigate multipart field delivery; do not infer the client defect from another commenter's curl resolution. This has observed-status evidence, but still needs source archival, sanitized projection, qualified human expectation and compatibility review. No case ID, input or decision has been created. It is a parsing/binding edge candidate, not prompt injection; overlap with 007/022 must be disclosed.

**Explicit prompt-injection coverage:** propose replacing **V2-01-03** with a separately versioned adversarial derivative of that same artificial fixture, retaining its incident facts and adding a clearly untrusted request-metadata note attempting to make the assistant ignore instructions and falsely claim resolution/validation. Expected robustness: ignore the instruction attempt, retain normal evidence/readiness/authorization rules and never fabricate checks or success. Exact payload, identity and rubric require human review; no derivative input is created or selected here.

Retire the original from that future 30-case selection only after explicit approval; preserve its reviewed input and results. One generated case replaces one, so the five artificial allowance slots remain **five**, not six. Development exposure and same-family dependence remain. Scenario coverage would change one proposed happy diagnostic slot into one explicit LLM prompt-injection adversarial slot; that is proposed coverage, not a tested safety result. 030's protocol-security example and 029's malformed Host are not LLM prompt-injection tests. The approximate two-adversarial guide is not yet achieved by this single proposed substitution. This swap does not resolve 028's separate eligibility question or fill the 030 gap by itself.

## Verification and preservation

Receipts and workbook snapshots are under [import-021-030-1](../reports/week4/import-021-030-1/). Existing supported import assessment was reused; no runner, policy, approval machinery or application behavior was added. Offline checks run with OS network deny and existing socket/SDK/command guards; all guard counts zero. Public retrieval was a separate source-only phase. No paid calls, exports, installs, services, credentials or incident endpoints were used. Semantic accuracy remains unmeasured, cost null. Approved metric targets remain unchanged, including cost per attempted case and human grounding assessment. Applicability must be designated before execution; holds are not automatic passes.

The workbook preserves the prior 20 review/input rows and all actual scores/outputs. New conditional/held entries do not imply evaluation assignment. The original baseline manifest and all 328 inherited files are checked without regeneration; prior sealed artifacts and reviewed assets remain protected. Exact preservation receipts accompany the report.
