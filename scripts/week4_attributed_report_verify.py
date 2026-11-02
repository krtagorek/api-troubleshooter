"""Read-only reconciliation of sealed paired mock results; stdlib only."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):return json.loads(path.read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(directory):
    directory=Path(directory).resolve()
    assert directory.is_relative_to(ROOT)
    hashes=load(directory/'artifact-hashes.json')
    assert all(sha(directory/p)==h for p,h in hashes.items())
    assert all((directory/p).stat().st_mode&0o222==0 for p in hashes)
    assert directory.stat().st_mode&0o222==0
    protected=load(directory/'protected-hashes.json')
    assert all(sha(ROOT/p)==h for p,h in protected.items())
    manifest=load(ROOT/'docs/source-baseline-manifest.json')
    assert len(manifest['files'])==328
    assert all(sha(ROOT/e['destination_relative_path'])==e['sha256'] for e in manifest['files'])
    meta=load(directory/'experiment.json')
    assert all(sha(ROOT/p)==h for p,h in meta['source_hashes'].items())
    historical=ROOT/'reports/week4/real-graph-mock-v1'
    old_hashes=load(historical/'artifact-hashes.json')
    assert all(sha(historical/p)==h for p,h in old_hashes.items())
    assert meta['config']==load(historical/'experiment.json')['config']
    assert all(sha(ROOT/load(directory/'preflight.json')['input_paths'][i])==h for i,h in meta['input_file_hashes'].items())
    summary=load(directory/'summary.json');assert len(summary['pairs'])==14
    total_calls=0;total_entries=0;complete=[]
    expected_route=['initialize','classifier','log_investigator','request_user_input']
    for pair in summary['pairs']:
        ident=pair['case_id'];assert all(pair['parity'].values())
        models={};results={}
        for arm in ('baseline','v1'):
            case=directory/arm/ident
            r=load(case/'result.json');s=load(case/'supervised-result.json')
            calls=load(case/'model-calls.json');spans=load(case/'spans.json')
            assert s['supervisor']['terminal']=='exited' and s['supervisor']['cleanup_verified']
            assert r['actual_ordered_graph_path']==expected_route
            assert r['terminal_status']=='held' and not r['errors'] and r['fatal_error'] is None
            assert r['input_preserved'] and all(r['span_structure'].values())
            assert not any(r['security'].values()) and r['grounding']['invalid']==[]
            assert r['advisory_changes']==[] and r['advisory_scope_checks']==[]
            # request_user_input deterministically supplies an inconclusive
            # diagnosis; this is not an executed analyst/model response.
            assert r['output']['diagnosis']['status']=='inconclusive'
            assert r['output']['diagnosis']['selected_hypothesis_id'] is None
            assert r['output']['final_report'] is None
            assert r['output']['validation_results']==[]
            assert r['usage']['model_calls']==len(calls)==2
            assert r['usage']['input_tokens']==sum(c['input_tokens'] for c in calls)==2
            assert r['usage']['output_tokens']==sum(c['output_tokens'] for c in calls)==2
            assert r['model_elapsed_seconds']==sum(c['elapsed_seconds'] for c in calls)
            assert 0<=r['model_elapsed_seconds']<=r['elapsed_seconds']<=s['supervised_elapsed_seconds']
            assert all(c['source']=='mock_test_data' for c in calls)
            assert [x['kind'] for x in spans].count('root')==1
            assert [x['kind'] for x in spans].count('node')==2
            assert [x['kind'] for x in spans].count('model')==2
            assert not any(x['kind']=='tool' for x in spans)
            assert [x['name'] for x in spans if x['kind']=='node']==['classifier','log_investigator']
            assert r['stage_coverage']=={'classifier':'completed','log_investigator':'completed',
                'root_cause_analyst':'not_reached','resolution_generator':'not_reached','validator':'not_reached'}
            assert r['semantic_accuracy'] is None and r['cost_usd'] is None
            total_calls+=len(calls);total_entries+=r['grounding']['checked']
            models[arm]=calls;results[arm]=r
        assert [c['messages'] for c in models['baseline']]==[c['messages'] for c in models['v1']]
        assert [c['response'] for c in models['baseline']]==[c['response'] for c in models['v1']]
        old_calls=load(historical/ident/'model-calls.json')['calls']
        assert [c['messages'] for c in old_calls]==[c['messages'] for c in models['baseline']]
        assert [c['response'] for c in old_calls]==[c['response'] for c in models['baseline']]
        assert results['baseline']['actual_ordered_graph_path']==load(historical/ident/'result.json')['actual_ordered_graph_path']
        bs=dict(results['baseline']['output']);ts=dict(results['v1']['output'])
        bs.pop('thread_id');ts.pop('thread_id');assert bs==ts
        complete.append(ident)
    assert total_calls==56 and total_entries==204
    return {'status':'PASS','paired_cases':complete,'arm_executions':28,
        'calls':total_calls,'selected_entries_checked':total_entries,'analyst_entries':0,
        'holds':28,'errors':0,'pre_analyst_parity':True,'historical_baseline_requests_outputs_routes_match':True,
        'protected_files_unchanged':len(protected),'baseline_files_unchanged':328,
        'historical_sealed_hashes_match':len(old_hashes),'paired_artifacts_match':len(hashes),
        'source_hashes_match':True,'timing_usage_span_reconciliation':True,
        'semantic_accuracy':None,'cost_usd':None,'external_requests':0,'trace_exports':0}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    output=args.output.resolve();assert output.is_relative_to(ROOT)
    result=verify(args.run)
    with output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))
