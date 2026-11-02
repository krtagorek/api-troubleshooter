"""Stdlib-only read-only reconciliation of V2 paired and projection artifacts."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def verify(directory):
    directory=Path(directory).resolve();assert directory.is_relative_to(ROOT)
    for path in [directory,ROOT/'data/week4/report-evidence-v2-1',ROOT/'reports/week4/attributed-report-readiness-v2-controls-1']:
        hashes=load(path/'artifact-hashes.json')
        assert all(sha(path/p)==h for p,h in hashes.items())
        assert path.stat().st_mode&0o222==0
        assert all((path/p).stat().st_mode&0o222==0 for p in hashes)
    meta=load(directory/'experiment.json')
    assert all(sha(ROOT/p)==h for p,h in meta['source_hashes'].items())
    assert sha(ROOT/meta['input_path'])==meta['input_sha256']
    assert meta['config']==load(ROOT/'reports/week4/real-graph-mock-v1/experiment.json')['config']
    protected=load(directory/'protected-hashes.json');assert all(sha(ROOT/p)==h for p,h in protected.items())
    m=load(ROOT/'docs/source-baseline-manifest.json');assert len(m['files'])==328
    assert all(sha(ROOT/e['destination_relative_path'])==e['sha256'] for e in m['files'])
    assets=load(ROOT/'reports/week4/real-graph-mock-v1/preflight.json')['asset_hashes']
    assert len(assets)==50 and all(sha(ROOT/p)==h for p,h in assets.items())
    revised=load(ROOT/meta['input_path']);without=load(ROOT/meta['input_path'])
    without['incident']['request_metadata'].pop('report_attribution_v2')
    assert without==load(ROOT/'data/week4/reviewed-candidates/batch-016-020/inference/W4-REAL-016.json')
    packet=revised['incident']['request_metadata']['report_attribution_v2']
    archive=ROOT/'data/week4/report-evidence-v2-1/archive'/(packet['source_sha256']+'.json')
    assert sha(archive)==packet['source_sha256'];document=load(archive)
    rel=document['relationships'][packet['relationship']]
    assert rel['kind']=='reporter_associated_reproduction' and rel['summary_kind']=='attributed_editorial_summary'
    assert rel['authenticated_request_correlation'] is False
    for role,a in packet['anchors'].items():
        block=document['blocks'][a['block']]
        assert block['text'][a['start']:a['end']]==a['literal']
        assert rel['roles'][role]==a['block'] and rel['scope']==block['scope']
    summary=load(directory/'summary.json');assert all(summary['parity'].values())
    rows={};calls={};spans={}
    prefix=['initialize','classifier','log_investigator']
    for arm,count in [('baseline',2),('v2',3)]:
        case=directory/arm;r=load(case/'result.json');rows[arm]=r
        c=load(case/'model-calls.json');calls[arm]=c;s=load(case/'spans.json');spans[arm]=s
        superv=load(case/'supervised-result.json')
        assert superv['supervisor']['terminal']=='exited' and superv['supervisor']['cleanup_verified']
        expected=prefix+(['root_cause_analyst'] if arm=='v2' else [])+['request_user_input']
        assert r['actual_ordered_graph_path']==expected and r['terminal_status']=='held'
        assert not r['errors'] and r['fatal_error'] is None and not any(r['security'].values())
        assert r['input_preserved'] and r['grounding']['invalid']==[] and all(r['span_structure'].values())
        assert r['output']['diagnosis']['status']=='inconclusive' and r['output']['diagnosis']['selected_hypothesis_id'] is None
        assert not r['output']['validation_results'] and r['output']['final_report'] is None
        assert len(c)==r['usage']['model_calls']==count
        assert sum(x['input_tokens'] for x in c)==r['usage']['input_tokens']==count
        assert sum(x['output_tokens'] for x in c)==r['usage']['output_tokens']==count
        assert sum(x['elapsed_seconds'] for x in c)==r['model_elapsed_seconds']
        assert 0<=r['model_elapsed_seconds']<=r['elapsed_seconds']<=superv['supervised_elapsed_seconds']
        assert all(x['source']=='mock_test_data' for x in c)
        assert sum(x['kind']=='model' for x in s)==count
        assert sum(x['kind']=='node' for x in s)==count
        assert sum(x['kind']=='root' for x in s)==1 and not any(x['kind']=='tool' for x in s)
        assert r['semantic_accuracy'] is None and r['cost_usd'] is None
    assert [c['messages'] for c in calls['baseline']]==[c['messages'] for c in calls['v2'][:2]]
    assert [c['response'] for c in calls['baseline']]==[c['response'] for c in calls['v2'][:2]]
    assert rows['baseline']['gate_observations'][0]['selected']==rows['v2']['gate_observations'][0]['selected']
    assert rows['baseline']['advisory_changes']==[] and len(rows['v2']['advisory_changes'])==1
    assert all(rows['v2']['advisory_scope_checks'][0].values())
    advisory=rows['v2']['advisory_changes'][0]
    assert advisory['qualified_analysis'] is True and advisory['definitive_confirmation'] is False
    assert advisory['provenance']=='reported_unverified' and advisory['legacy']['qualified_analysis'] is False
    payload=load(directory/'v2/model-calls.json')[2]['messages'][-1]['content']
    assert json.loads(payload.split('\n',1)[1])['incident']==revised['incident']
    assert not any(summary['parent_security'].values())
    return {'status':'PASS','assigned_real_inputs':1,'arms':{a:{'route':r['actual_ordered_graph_path'],
        'calls':len(calls[a]),'analyst_entries':r['actual_ordered_graph_path'].count('root_cause_analyst'),
        'terminal_status':r['terminal_status'],'errors':r['errors']} for a,r in rows.items()},
        'pre_analyst_parity':True,'scoped_advisory_only':True,'timing_usage_spans_reconcile':True,
        'baseline_files_unchanged':328,'protected_assets_unchanged':50,'protected_files_unchanged':len(protected),
        'archive_source_binding':True,'source_truth_authenticated':False,'authenticated_request_correlation':False,
        'original_fields_preserved':True,'semantic_accuracy':None,'cost_usd':None,
        'external_requests':0,'trace_exports':0}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    result=verify(args.run);output=args.output.resolve();assert output.is_relative_to(ROOT)
    with output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))
