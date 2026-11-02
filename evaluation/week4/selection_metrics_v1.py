"""Local selection measurements only; cannot select evidence or change gates."""
from .attributed_selection_v1 import dependency_advisory, missing_dependencies
from .attributed_report_v2.readiness import assess


def measure(incident, evidence):
    advisory = dependency_advisory(incident)
    required = {e['reference']:e for g in advisory['groups']
                for e in g['operands'] + g['required_all']}
    missing = missing_dependencies(incident, evidence)
    decision = assess(incident, evidence)
    omitted = {e['reference'] for e in missing['missing']}
    return {'version':'selection-measurements-v1','snapshot':advisory['evidence_snapshot'],
            'required_reference_count':len(required),
            'selected_required_reference_count':len(required)-len(omitted),
            'missing_dependencies':missing['missing'],'dependency_issues':missing['issues'],
            'required_reference_coverage_complete':bool(required) and not omitted and not missing['issues'],
            'selected_reference_count':len(evidence.items),'valid_selected_references':True,
            'completeness_after_checks':evidence.completeness,
            'qualified_analysis':decision.qualified_analysis,'readiness_reason':decision.reason,
            'definitive_confirmation':False,'semantic_accuracy':None}
