"""Fresh paired mechanical comparison, offline transports only; never a smoke."""
import argparse
from pathlib import Path
import json
import os
from time import monotonic
from uuid import uuid4
from scripts import week4_real_mock_run as common

ROOT = common.ROOT


def protected():
    """Read project copies only; never access baseline source_directory."""
    common.verify_baseline()
    sealed = ROOT/'reports/week4/real-graph-mock-v1'
    hashes = json.loads((sealed/'artifact-hashes.json').read_text())
    if any(common.sha((sealed/p).read_bytes()) != h for p,h in hashes.items()):
        raise RuntimeError('Historical sealed hash mismatch')
    expected = json.loads((sealed/'preflight.json').read_text())['asset_hashes']
    if common.fingerprint() != expected:
        raise RuntimeError('Protected reviewed asset hash mismatch')
    paths = {*(ROOT/'data/week4').rglob('*'), ROOT/'docs/source-baseline-manifest.json'}
    for name in ('offline-verification-1','offline-verification-final','real-graph-mock-v1',
                 'attributed-report-readiness-v1-paired-1'):
        paths.update((ROOT/'reports/week4'/name).rglob('*'))
    paths = sorted(paths)
    return {str(p.relative_to(ROOT)):common.sha(p.read_bytes()) for p in paths if p.is_file()}


def worker(raw, directory, namespace, arm):
    os.setsid()
    common.clear_environment()
    with common.offline_guard(worker=True) as guard:
        from evaluation.week4.runner import run_case
        from evaluation.week4.contracts import InferenceCase
        from evaluation.week4.tracing import FakeTracingSink
        from evaluation.week4.grading import structural_checks, grounding_checks
        from evaluation.week4.attributed_report_v1.readiness import assess
        from evaluation.week4.attributed_report_v1.workflow import build_workflow, AnalystAdvisory
        from tools.diagnostic_sufficiency import readiness
        from dataclasses import asdict
        capture = {}; gates = []; events = common.recorder()
        def provider_factory(trace):
            model = common.DeterministicModel(trace)
            capture['provider'] = AnalystAdvisory(model) if arm == 'v1' else model
            return capture['provider']
        def observer(name, state):
            if name == 'log_investigator':
                gates.append({'legacy':asdict(readiness(state['sanitized_inputs'],state['evidence'])),
                              'v1':assess(state['sanitized_inputs'],state['evidence']).model_dump(mode='json'),
                              'selected':state['evidence'].model_dump(mode='json')})
        result,spans,calls,fatal = run_case(InferenceCase.model_validate(raw), namespace+':'+arm,
            None, FakeTracingSink(), provider_factory=provider_factory,
            callbacks=[events], node_observer=observer,
            workflow_factory=build_workflow if arm == 'v1' else None)
        row = result.model_dump(mode='json')
        from evaluation.week4.contracts import check_inference
        for call in calls:
            payload = json.loads(call['messages'][-1]['content'].split('\n',1)[1])
            check_inference(payload['incident'])
        row.update(arm=arm, actual_ordered_graph_path=events.path,
            actual_router_returns=events.decisions, gate_observations=gates,
            advisory_changes=getattr(capture['provider'],'advisories',[]),
            advisory_scope_checks=getattr(capture['provider'],'scope_checks',[]),
            span_structure=structural_checks(result,spans,calls), grounding=grounding_checks(result),
            input_preserved=raw['incident']==events.graph_input==row['output']['sanitized_inputs'],
            fatal_error=type(fatal).__name__ if fatal else None, security=dict(guard),
            semantic_accuracy=None, cost_usd=None)
        if fatal or any(guard.values()):
            row['terminal_status'] = 'security_stop'
        directory = Path(directory)
        common.write(directory/'result.json',row)
        common.write(directory/'spans.json',spans)
        common.write(directory/'model-calls.json',calls)
        common.write(directory/'graph-events.json',events.events)


def compare_pair(baseline, treatment, b_calls, t_calls):
    return {
        'pre_analyst_requests_equal': [c['messages'] for c in b_calls[:2]] == [c['messages'] for c in t_calls[:2]],
        'pre_analyst_outputs_equal': [c['response'] for c in b_calls[:2]] == [c['response'] for c in t_calls[:2]],
        'selections_equal': baseline['gate_observations'][0]['selected'] == treatment['gate_observations'][0]['selected'],
        'inputs_preserved': baseline['input_preserved'] and treatment['input_preserved'],
    }


def run(output):
    common.clear_environment()
    with common.offline_guard() as parent_guard:
        from evaluation.week4.smoke import supervise
        from evaluation.week4.dependencies import verify_lock
        before = protected()
        pre,inputs = common.preflight()
        dependencies = verify_lock()
        out = Path(output).resolve()
        if not out.is_relative_to(ROOT):
            raise ValueError('Output must stay in new project')
        out.mkdir(parents=True,exist_ok=False,mode=0o700)
        common.write(out/'preflight.json',pre)
        sources = sorted((ROOT/'evaluation/week4').rglob('*.py')) + [
            Path(__file__).resolve(), ROOT/'scripts/week4_real_mock_run.py']
        common.write(out/'experiment.json',{
            'version':'attributed-report-readiness-v1-paired-1', 'config':common.CONFIG,
            'dependencies':dependencies, 'input_revisions':'existing bytes unchanged; both arms',
            'input_file_hashes':{ident:common.sha((ROOT/path).read_bytes()) for ident,path in pre['input_paths'].items()},
            'source_hashes':{str(p.relative_to(ROOT)):common.sha(p.read_bytes()) for p in sources},
            'network':'OS deny network* plus Python socket/DNS/SDK/command guards',
            'latency_boundary':'Case elapsed_seconds: immediately before node-wrapper setup, graph construction/invoke through terminal serialization; excludes provider creation, initial state setup and local trace delivery. Supervisor: spawn through reaping. Model elapsed: sum of actual mock-call receipts only. No remote export.',
            'semantic_accuracy':None,'cost_usd':None})
        namespace = str(uuid4()); rows=[]; stop=False
        for ident in common.EXPECTED:
            pair = {}; calls = {}
            for arm in ('baseline','v1'):
                directory = out/arm/ident; directory.mkdir(parents=True,mode=0o700)
                if stop:
                    row={'case_id':ident,'arm':arm,'terminal_status':'unattempted_security_stop','errors':['batch_stopped']}
                else:
                    started=monotonic()
                    control=supervise(worker,(inputs[ident],str(directory),namespace,arm),common.CONFIG['case_timeout_seconds'])
                    path=directory/'result.json'
                    row=json.loads(path.read_text()) if path.exists() else {
                        'case_id':ident,'arm':arm,'terminal_status':control['terminal'],'errors':[control['terminal']]}
                    row['supervisor']=control;row['supervised_elapsed_seconds']=monotonic()-started
                    stop=(row['terminal_status']=='security_stop' or any(parent_guard.values())
                          or not control['cleanup_verified'])
                common.write(directory/'supervised-result.json',row)
                pair[arm]=row
                cp=directory/'model-calls.json';calls[arm]=json.loads(cp.read_text()) if cp.exists() else []
            parity=compare_pair(pair['baseline'],pair['v1'],calls['baseline'],calls['v1']) if all(
                p.get('gate_observations') for p in pair.values()) else {'not_checked':'case failed before gate'}
            rows.append({'case_id':ident, 'parity':parity, 'arms':{arm:{
                'route':row.get('actual_ordered_graph_path'),
                'readiness':(row.get('gate_observations') or [{}])[0].get('legacy' if arm=='baseline' else 'v1'),
                'analyst_entries':(row.get('actual_ordered_graph_path') or []).count('root_cause_analyst'),
                'executed_calls':len(calls[arm]), 'terminal_status':row['terminal_status'],
                'errors':row.get('errors',[]), 'advisory_changes':len(row.get('advisory_changes',[]))}
                for arm,row in pair.items()}})
        after=protected()
        common.write(out/'summary.json',{'assigned_real_cases':14,'synthetic_cases':0,'pairs':rows,
            'model_calls':sum(a['executed_calls'] for p in rows for a in p['arms'].values()),
            'protected_hashes_unchanged':before==after, 'protected_file_count':len(before),
            'baseline':common.verify_baseline(), 'parent_security':dict(parent_guard),
            'semantic_accuracy':None,'cost_usd':None,'external_requests':0,'trace_exports':0,
            'limitations':'Reported association absent: no input revisions invented; analyst entry is not diagnostic completion or quality.'})
        common.write(out/'protected-hashes.json',before)
        common.finalize(out)
        if before!=after or any(parent_guard.values()):
            raise RuntimeError('Protected/isolation boundary failed')
        if any(not all(p['parity'].values()) or 'not_checked' in p['parity'] for p in rows):
            raise RuntimeError('Paired parity failed; inspect preserved results')
        return rows

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    rows=run(args.output)
    print(json.dumps({'pairs':len(rows),'calls':sum(a['executed_calls'] for p in rows for a in p['arms'].values())}))
