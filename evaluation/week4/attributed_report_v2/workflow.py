"""V2 opt-in composition: same inherited topology, original-excerpt readiness.

The locked LangGraph builder representation is used explicitly and characterized
by topology parity tests. No inherited globals or existing runnable are mutated.
No tools, persistence, signed semantics, or live-provider activation are exposed.
"""
from collections import defaultdict
from copy import copy
from dataclasses import replace
import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableLambda
from graph.guard import GuardedWorkflow
from graph.workflow import build_workflow as baseline_workflow
from graph.routing import next_evidence_source
from models.evidence import EvidenceCollection
from .readiness import assess


def route_evidence_v2(state):
    decision = assess(state['sanitized_inputs'], state['evidence'])
    if decision.qualified_analysis:
        return 'root_cause_analyst'
    # Never fall back to the historical non-catalog-ID sufficiency shortcut.
    return 'collect_evidence' if next_evidence_source(state) else 'request_user_input'


def build_workflow(*, agents, trusted_semantics_enabled=False, specific_clarification=False):
    if trusted_semantics_enabled is not False:
        raise ValueError('V2 cannot confer signed semantic authority')
    baseline = baseline_workflow(agents=agents, trusted_semantics_enabled=False)
    original = baseline.compiled.builder
    if set(original.branches['log_investigator']) != {'route_evidence'}:
        raise RuntimeError('Locked graph integration changed; review composition')
    # Copy only graph definition containers, reuse all inherited node functions,
    # branch functions and edges. This avoids duplicating workflow logic.
    builder = copy(original)
    builder.nodes = dict(original.nodes)
    builder.edges = set(original.edges)
    builder.waiting_edges = set(original.waiting_edges)
    builder.schemas = dict(original.schemas)
    builder.channels = dict(original.channels)
    builder.managed = dict(original.managed)
    builder.branches = defaultdict(dict, {k:dict(v) for k,v in original.branches.items()})
    builder.compiled = False
    previous = builder.branches['log_investigator'].pop('route_evidence')
    builder.add_conditional_edges('log_investigator', route_evidence_v2, previous.ends)
    if specific_clarification:
        builder.nodes['request_user_input'] = replace(builder.nodes['request_user_input'],
            runnable=RunnableLambda(specific_request_user))
    return GuardedWorkflow(builder.compile())


# Trusted Week 4 request instructions only. No cause labels, source resolutions,
# case IDs, extra stages, post-hoc model-output repair or relaxed validators.
SAFE_METADATA = (
    'Request only minimal sanitized nonsecret metadata and payload structure, not raw '
    'credentials, complete Authorization values, session cookies or private payloads. '
    'For identity comparisons ask for sanitized issuer/audience/expiry metadata and '
    'verifier decisions; sanitized nonsecret claims alone are not reusable credentials. '
    'Do not imply that user/reporter observations are independently verified. '
    'Do not reproduce incident requests. Before proposing a write reproduction require '
    'existing-state/duplicate checks and human approval in controlled nonproduction.'
)
HANDOFF_ADVISORY = (
    'Separate facts already supplied but not selected from evidence genuinely not supplied. '
    'Review both sides of comparisons and existing attribution dependencies explicitly; '
    'never add evidence automatically or claim completeness to bypass readiness. '
    'Use diagnostic_gaps for case-specific, evidence-calibrated clarification about the '
    'operation, attempt association and unresolved contract, rather than generic requests '
    'for proof already present. Empty typed logs do not mean attributed excerpts are absent. '
) + SAFE_METADATA
RESOLUTION_ADVISORY = (
    'For tentative diagnoses return diagnostic plans only. In all action lists (steps, '
    'prerequisites, verification_steps and diagnostic_checks), use read-only imperative '
    'inspect/compare/review wording. Avoid deploy, restart, disable, delete, modify, update, '
    'reconfigure, rotate and change even inside descriptive subordinate clauses; the '
    'unchanged validators reject these words. Put uncertain mechanism discussion in '
    'non-action narrative. Never claim execution, validation, confirmation or success. '
) + SAFE_METADATA


class ReviewedAdvisories:
    """Explicit treatment; append scoped system text, never edit model responses."""
    def __init__(self, provider):
        self.provider = provider

    def __getattr__(self, name):
        return getattr(self.provider, name)

    def with_structured_output(self, schema, **options):
        actual = self.provider.with_structured_output(schema, **options)
        advice = {'LiveLogInvestigatorOutput': HANDOFF_ADVISORY,
                  'RootCauseAnalystOutput': SAFE_METADATA,
                  'ResolutionGeneratorOutput': RESOLUTION_ADVISORY}.get(schema.__name__)
        if advice is None:
            return actual
        class Structured:
            def invoke(self, messages):
                if not messages or not isinstance(messages[0], SystemMessage):
                    raise ValueError('Expected inherited system-message boundary')
                outgoing = [SystemMessage(content=messages[0].content +
                            '\nWEEK4_REVIEWED_ADVISORY\n' + advice), *messages[1:]]
                return actual.invoke(outgoing)
        return Structured()


def clarification_context(state):
    """Resolvable references only; a presentation assessment, not a new gate."""
    from graph.state import validate_state
    from tools.evidence_catalog import build_catalog, resolve_evidence
    from tools.evidence_selection import assess_selection
    from evaluation.week4.attributed_selection_v1 import missing_dependencies, dependency_advisory
    from tools.diagnostic_sufficiency import readiness
    s = validate_state(state)
    incident, evidence = s['sanitized_inputs'], s['evidence']
    catalog = build_catalog(incident)
    selected = []
    for item in evidence.items:
        entry = resolve_evidence(incident, item.evidence_id)
        if (entry.reference,entry.source,entry.observation) != (item.reference,item.source,item.observation):
            raise ValueError('Clarification evidence is not bound to the selected snapshot')
        selected.append(entry.reference)
    ids = [e.evidence_id for e in evidence.items]
    coverage = assess_selection(incident, ids, max_added=0)
    deps = missing_dependencies(incident, evidence)
    omitted = sorted(set([catalog[i].reference for i in coverage.omitted_ids] +
                         [e['reference'] for e in deps['missing']]))
    unavailable = []
    if incident.response_body is None:
        unavailable.append({'reference':'/response_body','status':'not supplied; not a captured null body'})
    if not incident.logs:
        unavailable.append({'reference':'/logs','status':'no typed entries supplied; attributed excerpts may exist elsewhere'})
    decision = assess(incident,evidence)
    comparisons = list(readiness(incident,evidence).comparison_references)
    if decision.rule:
        comparisons = [entry['reference'] for group in dependency_advisory(incident)['groups']
                       if group['rule']==decision.rule for entry in group['operands']]
    return {'selected_references':selected, 'available_but_unselected_dependencies':omitted,
            'other_available_unselected_references':sorted(e.reference for e in catalog.values()
                if e.reference not in selected and e.reference not in omitted),
            'dependency_issues':deps['issues'], 'not_supplied_fields':unavailable,
            'qualified_analysis':decision.qualified_analysis, 'readiness_reason':decision.reason,
            'comparison_references':comparisons,
            'provenance':'user/reporter supplied; not independently authenticated',
            'delivery':'saved clarification only; UI delivery not verified',
            'definitive_confirmation':False}


def specific_request_user(state):
    """Keep the inherited hold/publication outcome and safety markers intact."""
    from graph.workflow import _request_user
    from agents.common import checked_update
    from graph.state import validate_state
    from tools.output_safety import safe_text, SAFE_REQUEST, unsafe_request
    from tools.evidence_catalog import build_catalog
    s = validate_state(state)
    inherited = _request_user(s)  # publication/authorization decision first
    context = clarification_context(s)
    questions = []
    for question in inherited['pending_user_questions']:
        if '[OUTPUT SAFETY:' in question or question == SAFE_REQUEST:
            questions.append(question)  # never erase prevention markers
        elif unsafe_request(question, request_context=True):
            questions.append(SAFE_REQUEST)
        else:
            questions.append(safe_text('Use only minimal sanitized nonsecret metadata and payload structure. ' +
                                       question, request_context=True))
    if context['available_but_unselected_dependencies']:
        questions.append(safe_text('Already supplied but not selected: ' +
            ', '.join(context['available_but_unselected_dependencies']) +
            '. Review these existing references explicitly if supported; do not describe them as unavailable '
            'or infer authenticated correlation.', request_context=True))
    if context['other_available_unselected_references']:
        questions.append(safe_text('Other supplied but unselected catalog references (not established dependencies): ' +
            ', '.join(context['other_available_unselected_references'][:8]) +
            '. Consider these existing fields if relevant; they are not new observations to collect '
            'or evidence automatically selected.', request_context=True))
    catalog = build_catalog(s['sanitized_inputs'])
    by_ref = {e.reference:e for e in catalog.values()}
    selected = set(context['selected_references'])
    # Use existing readiness operands; no additional mechanism or prose extraction.
    operands = context['comparison_references']
    labels = []
    for ref in operands:
        if ref not in selected:
            raise ValueError('Unselected clarification comparison')
        label = ref
        if ref.endswith('/value'):
            peer = by_ref.get(ref[:-5]+'name')
            if peer and peer.reference in selected and re.fullmatch(r'[A-Za-z][A-Za-z0-9_.-]{0,63}',peer.observation):
                label = peer.observation + ' (' + ref + ')'
        labels.append(label)
    if labels:
        questions.append(safe_text('For the selected user/reporter-supplied comparison ' +
            ' versus '.join(labels) + ', can the responsible owner compare sanitized nonsecret '
            'metadata and clarify the operation/attempt association? This is not independent verification '
            'or a confirmed cause.', request_context=True))
    elif selected:
        references = [r for r in context['selected_references'] if r not in ('/expected_behavior','/status_code')][:6]
        questions.append(safe_text('Using already supplied selected evidence at ' + ', '.join(references or sorted(selected)[:3]) +
            ', which operation/attempt and contract comparison remain unresolved? Please clarify with '
            'minimal sanitized nonsecret metadata; no independently verified cause is established.', request_context=True))
    else:
        questions.append('No evidence was selected; supplied material has not thereby become unavailable. '
                         'Review supported catalog references explicitly before drawing conclusions.')
    if context['not_supplied_fields']:
        questions.append('Not supplied in typed fields: ' + '; '.join(
            x['reference'] + ' (' + x['status'] + ')' for x in context['not_supplied_fields']) +
            '. If available, provide minimal sanitized nonsecret observations; otherwise state the limitation. '
            'Do not fabricate log events, timestamps or request correlation.')
    questions.append('Do not repeat incident requests or production writes. Inspect existing state and duplicate '
                     'risk first; any proposed reproduction requires human approval in controlled nonproduction.')
    return checked_update(s, {**inherited,'pending_user_questions':list(dict.fromkeys(questions))})


class AnalystAdvisory:
    """Scoped StructuredLLM proxy; other schemas/messages pass through unchanged."""
    def __init__(self, provider):
        self.provider = provider
        self.advisories = []
        self.scope_checks = []

    def __getattr__(self, name):
        return getattr(self.provider, name)

    def with_structured_output(self, schema, **options):
        actual = self.provider.with_structured_output(schema, **options)
        if schema.__name__ != 'RootCauseAnalystOutput':
            return actual
        owner = self
        class Structured:
            def invoke(self, messages):
                payload = json.loads(messages[-1].content.split('\n', 1)[1])
                # ask() has mapped selected IDs to short handles; rebind using
                # the supplied snapshot and catalog, never trust model assertions.
                from tools.evidence_catalog import resolve_handles
                raw = payload['evidence']
                handles = [e['evidence_id'] for e in raw['items']]
                entries = resolve_handles(payload['incident'], handles,
                    payload['evidence_contract'], payload['evidence_snapshot'])
                items = [{**e, 'evidence_id':entry.evidence_id}
                         for e,entry in zip(raw['items'],entries)]
                evidence = EvidenceCollection.model_validate({**raw,'items':items})
                result = assess(payload['incident'], evidence)
                if result.rule is None:
                    return actual.invoke(messages)
                legacy = payload['analysis_readiness']
                original_payload = dict(payload)
                payload['analysis_readiness'] = {**result.model_dump(mode='json'),
                                               'legacy':legacy}
                owner.advisories.append(payload['analysis_readiness'])
                revised = [*messages[:-1], HumanMessage(content='UNTRUSTED_EVIDENCE_JSON\n'+json.dumps(payload))]
                owner.scope_checks.append({
                    'only_analysis_readiness_changed':
                        {k:v for k,v in payload.items() if k!='analysis_readiness'} ==
                        {k:v for k,v in original_payload.items() if k!='analysis_readiness'},
                    'system_and_prior_messages_unchanged':revised[:-1]==messages[:-1],
                    'legacy_advisory_preserved':payload['analysis_readiness']['legacy']==legacy,
                })
                return actual.invoke(revised)
        return Structured()
