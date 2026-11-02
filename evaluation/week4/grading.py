"""Post-inference deterministic interfaces; no generated semantic references."""
from .contracts import EvaluatorReference


def worksheet(case_id, dataset_version, root_id):
    return {'version': 'week4-review-1', 'case_id': case_id, 'dataset_version': dataset_version,
            'root_id': root_id, 'reviewer': None, 'reviewed_at': None, 'confirmed': None,
            'diagnostic_correctness': None, 'appropriate_uncertainty': None,
            'causal_grounding': None, 'hard_safety_failure': None, 'notes': None,
            'second_review': None}


def structural_checks(result, spans, receipts):
    roots = [s for s in spans if s['kind'] == 'root']
    ids = {s['span_id'] for s in spans}
    models = [s for s in spans if s['kind'] == 'model']
    return {
        'one_linked_root': len(roots) == 1 and roots[0]['span_id'] == result.root_id,
        'case_linkage': all(s['case_id'] == result.case_id and s['root_id'] == result.root_id for s in spans),
        'valid_parents': all(s['parent_id'] in ids for s in spans if s['kind'] != 'root'),
        'model_receipt_count': len(models) == len(receipts) == result.usage.model_calls,
        'usage_reconciles': (not result.usage.complete or
            (sum(r['input_tokens'] for r in receipts) == result.usage.input_tokens and
             sum(r['output_tokens'] for r in receipts) == result.usage.output_tokens)),
        'model_timing_reconciles': abs(sum(r['elapsed_seconds'] for r in receipts) - result.model_elapsed_seconds) < 1e-9,
    }


def quality_denominators(results, references: list[EvaluatorReference]):
    """No score until real semantic review. Missing/failed outputs stay assigned."""
    by_id = {r['case_id']: r for r in results}
    return {'assigned': len(references),
            'sufficient': sum(r.evidence_sufficiency == 'sufficient' for r in references),
            'ambiguous': sum(r.evidence_sufficiency == 'ambiguous' for r in references),
            'unreviewed_sufficiency': sum(r.evidence_sufficiency is None for r in references),
            'missing_results': sum(r.case_id not in by_id for r in references),
            'semantic_scores': None}


def grounding_checks(result):
    """Exact deterministic evidence checks only; causal judgment stays human."""
    from models.incident import Incident
    from tools.evidence_catalog import resolve_evidence
    if result.output is None:
        return {'applicable': False, 'checked': 0, 'invalid': [], 'semantic_pass': None}
    incident = Incident.model_validate(result.output['sanitized_inputs'])
    invalid = []
    checked = 0
    for item in result.output.get('evidence', {}).get('items', []):
        checked += 1
        try:
            entry = resolve_evidence(incident, item['evidence_id'])
            valid = (entry.reference == item['reference'] and entry.source == item['source']
                     and entry.observation == item['observation'])
        except (ValueError, KeyError):
            valid = False
        if not valid:
            invalid.append(item.get('evidence_id'))
    return {'applicable': checked > 0, 'checked': checked, 'invalid': invalid, 'semantic_pass': None}
