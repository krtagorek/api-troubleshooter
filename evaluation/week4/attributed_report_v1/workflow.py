"""Opt-in composition: reuse inherited graph definitions, replace one branch.

The locked LangGraph builder representation is used explicitly and characterized
by topology parity tests. No inherited globals or existing runnable are mutated.
No tools, persistence, signed semantics, or live-provider activation are exposed.
"""
from collections import defaultdict
from copy import copy
import json
from langchain_core.messages import HumanMessage
from graph.guard import GuardedWorkflow
from graph.workflow import build_workflow as baseline_workflow
from graph.routing import next_evidence_source
from models.evidence import EvidenceCollection
from .readiness import assess


def route_evidence_v1(state):
    decision = assess(state['sanitized_inputs'], state['evidence'])
    if decision.qualified_analysis:
        return 'root_cause_analyst'
    # Never fall back to the historical non-catalog-ID sufficiency shortcut.
    return 'collect_evidence' if next_evidence_source(state) else 'request_user_input'


def build_workflow(*, agents, trusted_semantics_enabled=False):
    if trusted_semantics_enabled is not False:
        raise ValueError('V1 cannot confer signed semantic authority')
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
    builder.add_conditional_edges('log_investigator', route_evidence_v1, previous.ends)
    return GuardedWorkflow(builder.compile())


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
