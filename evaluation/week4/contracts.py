"""Strict inference boundary and evaluator-only records."""
from typing import Literal, Any
from pydantic import BaseModel, ConfigDict, Field, model_validator
from models.incident import Incident

FORBIDDEN = {'root_cause', 'expected_resolution', 'reference', 'references', 'rubric',
             'labels', 'expected_answer', 'reviewer', 'reviewed_at', 'semantic_labels',
             'family_id', 'diagnosis_expectation', 'acceptable_alternatives',
             'dataset_version', 'expected_behavior_notes', 'evidence_sufficiency',
             'applicable_stages', 'evidence_pointers', 'unsafe_actions', 'rubric_version',
             'confirmed', 'review_status', 'accepted_expected_behavior',
             'expected_supported_response', 'scenario_label', 'artificial_allowance',
             'human_review', 'metric_applicability', 'forbidden_unsupported_claims'}

class BoundaryFailure(RuntimeError):
    """Security/label isolation failure: halt batch, never persist unsafe input."""

class ResourceFailure(RuntimeError):
    pass

class AccountingFailure(RuntimeError):
    pass


def load_case_manifest(path):
    """Verify a frozen evaluation set; return inference records separately.

    Evaluator records are integrity-checked but never returned to the workflow.
    """
    import hashlib
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    path = Path(path).resolve()
    if not path.is_relative_to(root):
        raise BoundaryFailure('Dataset must stay in the new project')
    manifest = json.loads(path.read_text())
    if (manifest.get('version') != 'week4-dataset-manifest-1' or
        manifest.get('unresolved_substantive_decisions') != []):
        raise BoundaryFailure('Unfrozen or unresolved dataset')
    def verify(base, relative, expected):
        component = (base / relative).resolve()
        if (Path(relative).is_absolute() or not component.is_relative_to(base) or
            not component.is_file() or hashlib.sha256(component.read_bytes()).hexdigest() != expected):
            raise BoundaryFailure('Dataset component binding mismatch')
        return component
    files = manifest['files']
    for relative, expected in files.items():
        verify(path.parent, relative, expected)
    for relative, expected in manifest['external_bindings'].items():
        if not relative.startswith(('data/week4/', 'docs/')):
            raise BoundaryFailure('Invalid provenance binding')
        verify(root, relative, expected)
    rows = manifest['cases']
    ids = [r['case_id'] for r in rows]
    if (len(ids) != 30 or len(set(ids)) != 30 or manifest['case_count'] != 30 or
        any(type(r['artificial_allowance']) is not int or r['artificial_allowance'] not in (0,1) for r in rows) or
        sum(r['artificial_allowance'] for r in rows) != 5 or manifest['artificial_allowance_count'] != 5):
        raise BoundaryFailure('Invalid selected-set counts')
    for name in ('rubric.json', 'applicability.json', 'provenance.json', 'scenarios.json', 'approval.json'):
        if name not in files:
            raise BoundaryFailure('Missing evaluation binding')
    applicability = json.loads((path.parent/'applicability.json').read_text())
    if applicability['unresolved_decisions'] or set(applicability['cases']) != set(ids):
        raise BoundaryFailure('Unresolved metric applicability')
    inputs = []
    for row in rows:
        if row['input_path'] not in files or row['reference_path'] not in files:
            raise BoundaryFailure('Unbound inference/reference record')
        raw = json.loads((path.parent/row['input_path']).read_text())
        case = InferenceCase.model_validate(raw)
        if case.case_id != row['case_id'] or case.incident.incident_id != case.case_id or case.model_dump(mode='json') != raw:
            raise BoundaryFailure('Input identity or sanitization changed')
        reference = json.loads((path.parent/row['reference_path']).read_text())
        if reference['case_id'] != case.case_id or applicability['cases'][case.case_id]['unresolved']:
            raise BoundaryFailure('Reference/applicability identity mismatch')
        inputs.append(raw)
    return manifest, inputs


def check_inference(value):
    if isinstance(value, dict):
        if FORBIDDEN.intersection(value):
            raise BoundaryFailure('Evaluator-only field at inference boundary')
        for item in value.values():
            check_inference(item)
    elif isinstance(value, list):
        for item in value:
            check_inference(item)

class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

class InferenceCase(Strict):
    case_id: str = Field(min_length=1, pattern=r'^[A-Za-z0-9_-]+$')
    incident: Incident

    @model_validator(mode='before')
    @classmethod
    def isolate(cls, value):
        if isinstance(value, cls):
            value = value.model_dump(mode='json')
        check_inference(value)
        if isinstance(value, dict) and isinstance(value.get('incident'), dict):
            if set(value['incident']) - set(Incident.model_fields):
                raise BoundaryFailure('Unknown incident field')
        return value

class EvaluatorReference(Strict):
    """Never accepted by runner; unreviewed by default, no semantic labels assigned."""
    case_id: str
    dataset_version: str
    expected_behavior_notes: str | None = None
    evidence_sufficiency: Literal['sufficient', 'ambiguous'] | None = None
    applicable_stages: tuple[str, ...] = ()

class Usage(Strict):
    input_tokens: int | None = None
    output_tokens: int | None = None
    model_calls: int = 0
    complete: bool = True
    source: Literal['mock_test_data'] = 'mock_test_data'
    usage_priced_cost_usd: None = None

class CaseResult(Strict):
    case_id: str
    root_id: str | None
    terminal_status: str
    workflow_status: str | None = None
    error: str | None = None
    errors: tuple[str, ...] = ()
    stage_coverage: dict[str, str]
    elapsed_seconds: float | None
    model_elapsed_seconds: float
    usage: Usage | None
    output: dict[str, Any] | None = None
    trace_status: str = 'local'
    mode: Literal['offline_mock'] = 'offline_mock'
    semantic_quality: None = None
