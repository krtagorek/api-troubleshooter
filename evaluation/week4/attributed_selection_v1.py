"""Opt-in selection-dependency advisory, layered over unchanged V2 gates.

No evaluator data, case IDs, source prose extraction, or evidence augmentation.
"""
import json
from pydantic import ValidationError
from langchain_core.messages import HumanMessage
from models.incident import Incident
from models.evidence import EvidenceGap
from tools.evidence_catalog import handle_catalog, resolve_handles
from agents.common import checked_update
from agents.log_investigator import create_agent as inherited_investigator
from evaluation.week4.attributed_report_v1.contracts import EXCEPTION
from evaluation.week4.attributed_report_v1.readiness import HEADER
from evaluation.week4.attributed_report_v2.contracts import Attribution

VERSION = 'attributed-selection-dependencies-v1'
ATTRIBUTION = '/request_metadata/observation_representation'
PACKET = '/request_metadata/report_attribution_v2/'
INSTRUCTION = (
    'Dependency handles are existing catalog evidence, not new observations or a diagnosis. '
    'If relying on the reported ASCII-header rejection pair, review and select its attribution '
    'and original-excerpt dependencies together. Select only evidence you actually reviewed. '
    'If dependencies are missing, invalid, irrelevant, or unsupported, retain uncertainty and '
    'report diagnostic_gaps; do not claim completeness. Selection does not authenticate '
    'correlation or establish a cause. Existing readiness checks decide qualification.'
)


def dependency_advisory(incident):
    incident = Incident.model_validate(incident)
    catalog = handle_catalog(incident)
    rows = catalog['evidence_catalog']
    by_path = {e['reference']: e for e in rows}
    result = dict(version=VERSION, evidence_contract=catalog['evidence_contract'],
                  evidence_snapshot=catalog['evidence_snapshot'], instruction=INSTRUCTION,
                  groups=[], issues=[])
    md = incident.request_metadata
    if 'report_attribution_v2' not in md:
        return result
    try:
        packet = Attribution.model_validate(md['report_attribution_v2'])
    except ValidationError:
        result['issues'].append('Invalid typed V2 attribution record; no dependency group established.')
        return result
    if set(packet.anchors) != {'request', 'header', 'status', 'exception', 'bridge'}:
        result['issues'].append('Required original-excerpt anchor roles are incomplete or invalid.')
        return result
    header = by_path.get(packet.header_pointer)
    exception = by_path.get(packet.exception_pointer)
    if (header is None or exception is None or not HEADER.fullmatch(header['reference'])
            or header['value_type'] != 'str' or not any(ord(c) > 127 for c in header['observation'])
            or exception['observation'] != EXCEPTION):
        result['issues'].append('No matching typed non-ASCII header/exact reported exception pair.')
        return result
    # Exact scalar paths/handles only. Never copy archive text or editorial prose
    # into instructions. The unchanged V2 assessor validates the actual archive.
    dependencies = [e for e in rows if e['reference'] == ATTRIBUTION or e['reference'].startswith(PACKET)]
    if ATTRIBUTION not in by_path:
        result['issues'].append('Required reported/unverified attribution field is absent.')
    result['groups'].append({
        'rule': 'reported-ascii-header-rejection',
        'operands': [{'handle': e['handle'], 'reference': e['reference']} for e in (header, exception)],
        'required_all': [{'handle': e['handle'], 'reference': e['reference']} for e in dependencies],
        'provenance_ceiling': 'reporter-associated reproduction; not authenticated request correlation',
    })
    return result


def missing_dependencies(incident, evidence):
    """Report omissions only; never resolve by adding facts or changing readiness."""
    advisory = dependency_advisory(incident)
    catalog = handle_catalog(incident)
    # Bind selected IDs and references to this snapshot through trusted resolution.
    from tools.evidence_catalog import resolve_evidence
    selected = set()
    for item in evidence.items:
        entry = resolve_evidence(incident, item.evidence_id)
        if entry.reference != item.reference or entry.observation != item.observation:
            raise ValueError('Selected evidence differs from snapshot')
        selected.add(entry.reference)
    missing = [e for group in advisory['groups'] for e in group['operands'] + group['required_all']
               if e['reference'] not in selected]
    return dict(version=VERSION, evidence_snapshot=catalog['evidence_snapshot'],
                missing=missing, issues=advisory['issues'])


class SelectionAdvisory:
    """Only investigator user payload gains one named advisory; no output edits."""
    def __init__(self, provider, *, explicit_selection_only=False):
        self.provider = provider
        self.requests = []
        self.explicit_selected_ids = None
        self.explicit_selection_only = explicit_selection_only

    def __getattr__(self, name):
        return getattr(self.provider, name)

    def with_structured_output(self, schema, **options):
        actual = self.provider.with_structured_output(schema, **options)
        if schema.__name__ != 'LiveLogInvestigatorOutput':
            return actual
        owner = self
        class Structured:
            def invoke(self, messages):
                payload = json.loads(messages[-1].content.split('\n', 1)[1])
                expected = handle_catalog(payload['incident'])
                if any(payload[k] != expected[k] for k in expected):
                    raise ValueError('Investigator catalog/snapshot mismatch')
                advice = dependency_advisory(payload['incident'])
                # No behavior/request change for incidents outside the narrow scope.
                if not advice['groups'] and not advice['issues'] and not owner.explicit_selection_only:
                    return actual.invoke(messages)
                outgoing = messages
                if advice['groups'] or advice['issues']:
                    revised = {**payload, 'selection_dependency_advisory': advice}
                    outgoing = [*messages[:-1], HumanMessage(content='UNTRUSTED_EVIDENCE_JSON\n' + json.dumps(revised))]
                    owner.requests.append({'before': payload, 'after': revised,
                                           'system_unchanged': outgoing[:-1] == messages[:-1]})
                output = actual.invoke(outgoing)
                # Preserve the model's exact selection for the opt-in node; do
                # not allow inherited telemetry augmentation to add facts here.
                selected = resolve_handles(payload['incident'], output.selected_evidence_handles,
                    output.evidence_contract, output.evidence_snapshot)
                owner.explicit_selected_ids = {entry.evidence_id for entry in selected}
                return output
        return Structured()


def create_investigator(*, llm, explicit_selection_only=False):
    proxy = SelectionAdvisory(llm, explicit_selection_only=explicit_selection_only)
    inherited = inherited_investigator(llm=proxy)
    def node(state):
        proxy.explicit_selected_ids = None
        update = inherited(state)
        evidence = update['evidence']
        if proxy.explicit_selected_ids is not None:
            extras = [e for e in evidence.items if e.evidence_id not in proxy.explicit_selected_ids]
            if extras:
                evidence = evidence.model_copy(update={
                    'items': [e for e in evidence.items if e.evidence_id in proxy.explicit_selected_ids],
                    'missing': [*evidence.missing, EvidenceGap(
                        description='Unselected catalog comparison candidates were not automatically included: ' +
                            ', '.join(e.reference for e in extras),
                        required_to_resolve='Review omitted comparison evidence and select it explicitly if supported.')],
                })
        report = missing_dependencies(state['sanitized_inputs'], evidence)
        if report['missing'] or report['issues']:
            paths = ', '.join(e['handle'] + '=' + e['reference'] for e in report['missing'])
            gap = EvidenceGap(description='V2 attribution selection dependencies missing: ' + (paths or '; '.join(report['issues'])),
                required_to_resolve='Review the referenced attributed evidence; select only supported dependencies, or retain the evidence hold.')
            evidence = evidence.model_copy(update={'missing': [*evidence.missing, gap]})
            return checked_update(state, {**update, 'evidence': evidence})
        return checked_update(state, {**update, 'evidence': evidence})
    return node


def build_workflow(*, llm, observer=None):
    """Explicit injection composition; reuse the exact V2 graph and factories."""
    from evaluation.week4.attributed_report_v2.workflow import build_workflow as v2
    from evaluation.week4.attributed_report_v2.workflow import AnalystAdvisory
    from evaluation.week4.runner import FACTORIES
    provider = AnalystAdvisory(llm)
    def wrap(name, factory):
        actual = factory(llm=provider)
        def node(state):
            update = actual(state)
            if observer is not None:
                observer(name, {**state, **update})
            return update
        return node
    factories = {**FACTORIES, 'log_investigator': create_investigator}
    return v2(agents={name: wrap(name, factory) for name, factory in factories.items()},
              trusted_semantics_enabled=False)
