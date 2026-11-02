# Week 4 attributed selection dependencies v1

Implemented **attributed-selection-dependencies-v1** as a separate opt-in Week 4 composition in [attributed_selection_v1.py](../evaluation/week4/attributed_selection_v1.py). No preexisting implementation, input, review, proposal, or sealed result was edited. No live calls, exports, incident requests, installations, or commits occurred.

## Finding from the sealed live smoke

The investigator returned `selected_evidence_handles = [E41, E43, E47, E01]`, `completeness = complete`, and no diagnostic gaps. The inherited investigator resolved these to the exact reported exception, the emoji header, reported status, and actual-behavior narrative. Its trusted coverage assessment downgraded completeness to partial. V2 then held with **Missing selected reported/unverified attribution**; the analyst was never entered.

The unchanged V2 contract requires the selected exception/header operands, the exact `/request_metadata/observation_representation` attribution scalar, and **every scalar catalog leaf** under `/request_metadata/report_attribution_v2/`. V2 also resolves and checks the archived relationship, original anchors, operation operands, snapshot binding, and inherited coverage/conflict/ambiguity/completeness checks. Listing these dependencies is not proof they are true.

There are **39 required references** for this input. The exception/header operands E41/E43 were selected; all **37 attribution dependencies** were omitted:

| Handles | Exact reference or expansion |
| --- | --- |
| E03 | `/request_metadata/observation_representation` |
| E05–E09 | `/request_metadata/report_attribution_v2/anchors/bridge/{block,end,kind,literal,start}`, respectively |
| E10–E14 | `/request_metadata/report_attribution_v2/anchors/exception/{block,end,kind,literal,start}`, respectively |
| E15–E19 | `/request_metadata/report_attribution_v2/anchors/header/{block,end,kind,literal,start}`, respectively |
| E20–E24 | `/request_metadata/report_attribution_v2/anchors/request/{block,end,kind,literal,start}`, respectively |
| E25–E29 | `/request_metadata/report_attribution_v2/anchors/status/{block,end,kind,literal,start}`, respectively |
| E30 | `/request_metadata/report_attribution_v2/authenticated_request_correlation` |
| E31 | `/request_metadata/report_attribution_v2/endpoint` |
| E32 | `/request_metadata/report_attribution_v2/exception_pointer` |
| E33 | `/request_metadata/report_attribution_v2/header_pointer` |
| E34 | `/request_metadata/report_attribution_v2/kind` |
| E35 | `/request_metadata/report_attribution_v2/method` |
| E36 | `/request_metadata/report_attribution_v2/relationship` |
| E37 | `/request_metadata/report_attribution_v2/source_sha256` |
| E38 | `/request_metadata/report_attribution_v2/summary` |
| E39 | `/request_metadata/report_attribution_v2/summary_kind` |
| E40 | `/request_metadata/report_attribution_v2/version` |

The [machine-readable inventory](../reports/week4/attributed-selection-dependencies-v1-2/required-and-omitted.json) lists each full path individually. Handles apply only to this snapshot. The implementation derives current handles from current catalog paths; these numbers and the incident ID are not rules.

Originally, all these facts were present in the incident JSON and flat catalog. The inherited system prompt described selecting evidence, considering comparison peers, and not inventing observations, but did not expose the V2 attribution dependency group. The generic inherited coverage heuristic recognizes telemetry/comparison candidates, not this report-attribution group. The observed omission therefore does not establish that the source lacks attribution. It establishes that this live selection omitted attribution which the gate requires. It also does not establish that an advisory will make another live model select correctly.

## Versioned change and exact request difference

The new `SelectionAdvisory` proxy affects **LiveLogInvestigatorOutput only**. It verifies the input catalog/contract/snapshot and appends one fixed-format user-payload field:

```json
{
  "selection_dependency_advisory": {
    "version": "attributed-selection-dependencies-v1",
    "evidence_contract": "evidence-handles-v1",
    "evidence_snapshot": "<existing snapshot>",
    "instruction": "<fixed selection/uncertainty guidance>",
    "groups": [{
      "rule": "reported-ascii-header-rejection",
      "operands": ["<current header and exact exception handles/references>"],
      "required_all": ["<current attribution and packet-leaf handles/references>"],
      "provenance_ceiling": "reporter-associated reproduction; not authenticated request correlation"
    }],
    "issues": []
  }
}
```

The complete exact added object, not this abbreviated example, is in the [final request diff](../reports/week4/attributed-selection-dependencies-v1-2/request-diff.json). The [original request](../reports/week4/attributed-selection-dependencies-v1-2/investigator-request-before.json) reconstructs the sealed prepared-request hash `c05daf6a7f897afbad4613b0aea6e810779167576615b0c2367d9b7594dd77f3`. The [revised provider-normalized request](../reports/week4/attributed-selection-dependencies-v1-2/investigator-request-after.json) is an offline preview, not a dispatched request.

System prompt, output schema and schema enums, existing user-payload values, model, tier, output cap, and other provider parameters are unchanged. The added field is the only semantic request difference. Provider-normalized request size increases from **17,112 to 22,025 bytes** (+4,913), below the existing 65,536-byte limit. This byte count is not a token count. Later workflow requests and total provider usage cannot be predicted from this preview.

Earlier sealed v1-1 artifacts describe the first advisory draft; its after-request preview precedes provider JSON/redaction normalization. The separate wire-preview-2 artifacts correct that preview. Final v1-2 artifacts use the completed no-auto-addition composition and already include provider normalization. Earlier drafts remain unchanged; final v1-2 artifacts are authoritative for this implementation.

The advisory contains fixed guidance and catalog handles/paths, not excerpts promoted into instructions. It is derived only from the closed typed V2 packet and the same narrow non-ASCII-header/exact-exception pattern. It adds no new mechanism, diagnostic answer, source resolution, evaluator label, or case-ID instruction. Outside this scope, the proxy passes the request through unchanged.

The new `create_investigator` reuses the inherited factory, then appends an explicit deterministic missing-dependency gap when required selections or fields are absent. It never adds evidence or forces completeness. Within the attributed advisory scope, it retains only the model's explicitly selected, snapshot-bound IDs: any comparison candidates copied by the inherited factory's internal augmentation are excluded and reported as omitted. The unchanged readiness coverage checks can then hold for those omitted peers. A synthetic unselected-telemetry control verifies this behavior. Outside this narrow scope, the inherited path is unchanged. No original selected fact is removed or new fact selected by the advisory.

The new `build_workflow(llm=..., observer=...)` composes that investigator with the inherited factories, existing V2 graph, and existing scoped analyst advisory. Topology parity is verified. No inherited globals are monkeypatched, no routing logic is copied, and all readiness, binding, archive, grounding, publication, authorization, and validation policies remain unchanged.

## Offline outcomes

All model outputs below are scripted controls. One existing real projection was replayed under two fixed selection policies; these are not four new incidents or independent evaluations.

| Scripted selection | Existing V2 | V2 + selection v1 |
| --- | --- | --- |
| Recorded live handles | Classifier → investigator → hold; 2 mocked calls; no analyst | Same route/calls/hold; explicit missing-dependency gap added |
| Explicit valid dependency handles | Classifier → investigator → analyst → awaiting evidence; 3 mocked calls | Same route/calls/outcome; qualified analysis only |

The analyst mock is explicitly inconclusive with no causal diagnosis, hypotheses, or remediation. Analyst entry is not diagnostic completion, appropriate clarification, golden readiness, or model-quality improvement.

**32 tests passed:** eight new selection controls, twelve existing V2 controls, ten V1 controls, and two existing V2 workflow regressions. Controls verify every attribution-peer omission independently holds and is reported; missing records/anchors, stale hashes, forged quotations/relationships/IDs, cross-case references, unrelated attempts, evaluator references, provenance promotion, instruction-bearing evidence, ambiguity, conflicts, coverage, and legacy/insufficient paths remain rejected or held. The unchanged original-anchor control specifically separates identical literals from unrelated attempt scopes.

The replay tests assert no attribution or telemetry auto-addition in the opted-in scope, no completeness promotion, identical classifier requests, exactly one added investigator user field, unchanged schema/options/system messages, and topology parity. Neither advice nor a scripted claim of complete can bypass V2. [Test log and comparison artifacts](../reports/week4/attributed-selection-dependencies-v1-2/result.json).

Semantic accuracy, model-quality delta, and new real cost remain **null/not measured**. There were zero new live requests or trace exports. Scripted branch coverage cannot establish whether a live model understands or follows the advisory. The recorded classifier's causal language remains a model assertion, not authenticated correlation.

## Preservation and future comparison

All **942 preexisting protected files** match the before snapshot, including all **328 inherited baseline files**, existing V1/V2 implementations, reviewed inputs/reviews, proposals, and sealed results. Every active sealed artifact manifest also verifies. The baseline manifest was not regenerated.

Adding a Week 4 module changes the current source-file inventory. Consequently, the old proposal remains byte-for-byte preserved but its loader should reject a replay against the enlarged inventory. No proposal was silently rebound. The prior one-run approval was consumed and does not authorize another call.

The [future live comparison proposal](../reports/week4/attributed-selection-dependencies-v1-2/future-live-comparison-proposal.json) is **unauthorized and not executable**, with blank approval fields, tracing OFF, a bound input/archive/source inventory, and no approved comparison budget. The new selection composition is not wired into the supervised live-provider path in this task. That separately reviewed integration, fresh model/pricing checks, a funded two-arm budget and newly bound executable proposal, and explicit authorization remain prerequisites.

For a fair future comparison, run fresh V2 and treatment arms on identical input bytes, model snapshot/tier, schema, dependencies, limits, and selections policy; only the advisory and deterministic dependency reporting may differ. Do not compare treatment against the historical live smoke as if they were a contemporaneous paired experiment. Keep ordinary failures and holds in denominators, report actual selected handles and branches, and make no isolated causal or semantic-quality claim from one case.

Reproduce offline checks with existing dependencies:

```sh
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' .venv-week4-locked/bin/python -m unittest tests.week4.test_attributed_selection_v1 tests.week4.test_attributed_report_v2 tests.week4.test_attributed_report_v1 tests.week4.test_attributed_report_v2_regressions -v
```

The create-only artifact builder is `scripts/week4_attributed_selection_verify.py`; it intentionally refuses the already sealed output directory. Do not delete historical artifacts to rerun it. The exact final provider-normalized preview is the v1-2 artifact described above; earlier previews are retained as draft mechanics evidence.
