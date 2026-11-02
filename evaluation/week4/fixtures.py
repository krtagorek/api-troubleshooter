"""Scripted mock outputs, not semantic labels or model-quality evidence."""
import json
from pathlib import Path


def development_cases():
    return json.loads((Path(__file__).parent/'fixtures/development.json').read_text())


def mock_reply(request):
    envelope = json.loads(request['messages'][1]['content'].split('\n', 1)[1])
    schema = request['response_format']['json_schema']['name']
    if schema == 'ClassifierOutput':
        output = {'classification': {'category': 'unknown', 'confidence': 0,
                                    'reasoning': 'Offline scripted response, no diagnostic claim.'}}
    elif schema == 'LiveLogInvestigatorOutput':
        output = {'evidence_contract': envelope['evidence_contract'],
                  'evidence_snapshot': envelope['evidence_snapshot'],
                  'selected_evidence_handles': [], 'completeness': 'missing', 'diagnostic_gaps': []}
    elif schema == 'RootCauseAnalystOutput':
        output = {'hypotheses': [], 'diagnosis': {'status': 'inconclusive',
            'summary': 'Offline scripted inconclusive response; no semantic judgment.',
            'confidence': 0, 'uncertainty': ['No verification was performed.']}}
    else:
        raise ValueError('Unexpected mock stage')
    return {'output': output}


def full_path_reply(request):
    """Exercise later boundaries with scripted responses; no semantic claim."""
    schema = request['response_format']['json_schema']['name']
    envelope = json.loads(request['messages'][1]['content'].split('\n', 1)[1])
    if schema == 'LiveLogInvestigatorOutput':
        answer = mock_reply(request)
        answer['output'].update(selected_evidence_handles=[e['handle'] for e in envelope['evidence_catalog']],
                                completeness='complete')
        return answer
    refs = [e['evidence_id'] for e in envelope.get('evidence', {}).get('items', [])]
    contract = {key: envelope[key] for key in ('evidence_contract', 'evidence_snapshot') if key in envelope}
    if schema == 'RootCauseAnalystOutput':
        return {'output': {**contract, 'hypotheses': [{'hypothesis_id': 'mock-h1',
            'description': 'Scripted fixture hypothesis for boundary coverage only.', 'confidence': 0.2,
            'supporting_evidence_ids': refs}], 'diagnosis': {'status': 'tentative',
            'summary': 'Scripted fixture hypothesis remains unverified.', 'selected_hypothesis_id': 'mock-h1',
            'confidence': 0.2, 'uncertainty': ['Offline test data; not a quality judgment.'],
            'discriminating_evidence_ids': refs, 'diagnostic_checks': ['Review sanitized comparison observations.']}}}
    if schema == 'ResolutionGeneratorOutput':
        return {'output': {**contract, 'proposed_fix': {'plan_kind': 'diagnostic',
            'summary': 'Review sanitized evidence with the responsible owner.',
            'steps': ['Inspect sanitized comparison observations with the responsible owner.'],
            'verification_steps': ['Review evidence completeness; no execution occurred.'],
            'requires_human_approval': True, 'evidence_ids': refs}}}
    if schema == 'ValidatorOutput':
        return {'output': {'validation': {'status': 'NOT_TESTED', 'checks': [],
                          'issues': ['Offline scripted review only.'], 'retry_recommended': False}}}
    return mock_reply(request)
