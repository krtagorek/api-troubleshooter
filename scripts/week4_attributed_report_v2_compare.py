"""One development-input paired comparison. Mock policy unchanged; no SDK clients."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from time import monotonic
from uuid import uuid4
from scripts import week4_real_mock_run as common
from scripts.week4_attributed_report_compare import compare_pair
ROOT=common.ROOT

def worker(raw, directory, namespace, arm):
    os.setsid()
    common.clear_environment()
    with common.offline_guard(worker=True) as guard:
        from evaluation.week4.runner import run_case
        from evaluation.week4.contracts import InferenceCase
        from evaluation.week4.tracing import FakeTracingSink
        from evaluation.week4.grading import structural_checks, grounding_checks
        from evaluation.week4.attributed_report_v2.readiness import assess
        from evaluation.week4.attributed_report_v2.workflow import build_workflow, AnalystAdvisory
        from tools.diagnostic_sufficiency import readiness
        from dataclasses import asdict
        capture = {}; gates = []; events = common.recorder()
        def provider_factory(trace):
            model = common.DeterministicModel(trace)
            capture['provider'] = AnalystAdvisory(model) if arm == 'v2' else model
            return capture['provider']
        def observer(name, state):
            if name == 'log_investigator':
                gates.append({'legacy':asdict(readiness(state['sanitized_inputs'],state['evidence'])),
                              'v2':assess(state['sanitized_inputs'],state['evidence']).model_dump(mode='json'),
                              'selected':state['evidence'].model_dump(mode='json')})
        result,spans,calls,fatal = run_case(InferenceCase.model_validate(raw), namespace+':'+arm,
            None, FakeTracingSink(), provider_factory=provider_factory,
            callbacks=[events], node_observer=observer,
            workflow_factory=build_workflow if arm == 'v2' else None)
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

def fingerprint():
    common.verify_baseline()
    paths=set()
    for folder in ('data/week4','reports/week4','docs','evaluation/week4/attributed_report_v1'):
        paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    return {str(p.relative_to(ROOT)):common.sha(p.read_bytes()) for p in sorted(paths)}


def run(input_path, output):
    common.clear_environment()
    with common.offline_guard() as parent_guard:
        from evaluation.week4.smoke import supervise
        from evaluation.week4.dependencies import verify_lock
        from evaluation.week4.contracts import InferenceCase
        dependencies=verify_lock()
        original=ROOT/'reports/week4/real-graph-mock-v1'
        assert common.CONFIG==json.loads((original/'experiment.json').read_text())['config']
        for path in (ROOT/'reports/week4').glob('*/artifact-hashes.json'):
            assert all(common.sha((path.parent/p).read_bytes())==h for p,h in json.loads(path.read_text()).items())
        expected=json.loads((original/'preflight.json').read_text())['asset_hashes']
        assert common.fingerprint()==expected
        before=fingerprint()
        input_path=Path(input_path).resolve();out=Path(output).resolve()
        if not input_path.is_relative_to(ROOT) or not out.is_relative_to(ROOT):
            raise ValueError('Input/output must stay in the new project')
        raw=json.loads(input_path.read_text())
        assert InferenceCase.model_validate(raw).model_dump(mode='json')==raw
        out.mkdir(parents=True,exist_ok=False,mode=0o700)
        sources=sorted((ROOT/'evaluation/week4').rglob('*.py'))+[
            Path(__file__).resolve(),ROOT/'scripts/week4_real_mock_run.py',ROOT/'scripts/week4_attributed_report_compare.py',
            ROOT/'tests/week4/test_attributed_report_v2.py']
        common.write(out/'experiment.json',{'version':'attributed-report-readiness-v2-paired-1',
            'config':common.CONFIG,'dependencies':dependencies,
            'input_path':str(input_path.relative_to(ROOT)),'input_sha256':common.sha(input_path.read_bytes()),
            'identical_revised_input_both_arms':True,
            'source_hashes':{str(p.relative_to(ROOT)):common.sha(p.read_bytes()) for p in sources},
            'latency_boundary':'Case elapsed: node-wrapper setup, graph construction/invoke and terminal serialization; excludes provider creation, initial state setup and local trace delivery. Supervisor includes process spawn/reaping. Model elapsed is sum of actual mock receipts.',
            'semantic_accuracy':None,'cost_usd':None})
        namespace=str(uuid4());results={};calls={};stop=False
        for arm in ('baseline','v2'):
            directory=out/arm;directory.mkdir(mode=0o700)
            if stop:
                row={'case_id':raw['case_id'],'terminal_status':'unattempted_security_stop','errors':['batch_stopped']}
            else:
                start=monotonic()
                control=supervise(worker,(raw,str(directory),namespace,arm),common.CONFIG['case_timeout_seconds'])
                file=directory/'result.json'
                row=json.loads(file.read_text()) if file.exists() else {
                    'case_id':raw['case_id'],'terminal_status':control['terminal'],'errors':[control['terminal']]}
                row.update(supervisor=control,supervised_elapsed_seconds=monotonic()-start)
                stop=row['terminal_status']=='security_stop' or any(parent_guard.values()) or not control['cleanup_verified']
            common.write(directory/'supervised-result.json',row)
            results[arm]=row
            cp=directory/'model-calls.json';calls[arm]=json.loads(cp.read_text()) if cp.exists() else []
        parity=compare_pair(results['baseline'],results['v2'],calls['baseline'],calls['v2']) if all(
            r.get('gate_observations') for r in results.values()) else {'not_checked':True}
        unchanged=all(common.sha((ROOT/p).read_bytes())==h for p,h in before.items())
        summary={'case_id':raw['case_id'],'assigned_real_inputs':1,'synthetic_cases':0,
            'parity':parity,'protected_files_unchanged':unchanged,'protected_files':len(before),
            'baseline':common.verify_baseline(),'parent_security':dict(parent_guard),
            'arms':{arm:{'route':r.get('actual_ordered_graph_path'),
                'readiness':(r.get('gate_observations') or [{}])[0].get('legacy' if arm=='baseline' else 'v2'),
                'analyst_entries':(r.get('actual_ordered_graph_path') or []).count('root_cause_analyst'),
                'calls':len(calls[arm]),'terminal_status':r['terminal_status'],'errors':r.get('errors',[])}
                for arm,r in results.items()},'semantic_accuracy':None,'cost_usd':None,
            'external_requests':0,'trace_exports':0}
        common.write(out/'summary.json',summary);common.write(out/'protected-hashes.json',before)
        common.finalize(out)
        assert unchanged and not any(parent_guard.values())
        assert 'not_checked' not in parity and all(parity.values())
        assert not stop
        return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();print(json.dumps(run(args.input,args.output),indent=2))
