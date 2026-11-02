"""Post-run read-only verification; never repeats real-case inference."""
import argparse
import json
from pathlib import Path
import socket
from scripts import week4_real_mock_run as run


def verify(directory):
    directory=Path(directory)
    summary=json.loads((directory/'summary.json').read_text())
    pre=json.loads((directory/'preflight.json').read_text())
    hashes=json.loads((directory/'artifact-hashes.json').read_text())
    assert directory.stat().st_mode&0o222==0
    for name,expected in hashes.items():
        path=directory/name
        assert run.sha(path.read_bytes())==expected,name
        assert path.stat().st_mode&0o222==0,name
    assert run.fingerprint()==pre['asset_hashes']==summary['input_hashes_after']
    assert run.verify_baseline()['mismatches']==[]
    assert [x['case_id'] for x in summary['results']]==list(run.EXPECTED)
    from graph.state import validate_state
    from tools.evidence_catalog import resolve_evidence,resolve_handles
    checks=[];all_ids=set();total_evidence=0;mock_calls=0
    for ident in run.EXPECTED:
        root=directory/ident
        result=json.loads((root/'supervised-result.json').read_text())
        events=json.loads((root/'graph-events.json').read_text())['events']
        calls=json.loads((root/'model-calls.json').read_text())['calls']
        spans=json.loads((root/'spans.json').read_text())['spans']
        raw=json.loads((run.ROOT/pre['input_paths'][ident]).read_text())
        state=result['output'];validate_state(state)
        assert result['input_preservation']['supplied_vs_initial_graph_input']
        assert result['input_preservation']['initial_vs_terminal_input']
        assert result['input_preservation']['evidence_loss']==[]
        assert result['input_preservation']['defaults_added']=={}
        assert state['sanitized_inputs']==raw['incident']
        actual_path=[e['name'] for e in events if e['kind']=='start' and e['name'] and e['name']==e['graph_node']]
        assert actual_path==result['actual_ordered_graph_path']
        assert result['supervisor']['cleanup_verified']
        assert result['supervisor']['terminal']=='exited'
        assert not any(result['security'].values())
        assert all(result['span_structure'].values())
        assert result['grounding']['invalid']==[]
        assert result['usage']['model_calls']==len(calls)==len([s for s in spans if s['kind']=='model'])
        assert result['model_elapsed_seconds']==sum(c['elapsed_seconds'] for c in calls)
        assert result['usage_priced_cost_usd'] is None and result['semantic_quality'] is None
        assert state['available_evidence_sources']==state['consumed_evidence_sources']==[]
        assert not any(state['retry_counts'].values())
        assert state['proposed_fix'] is None and state['final_report'] is None
        assert state['validation_results']==[]
        assert not any(s['kind']=='tool' for s in spans)
        requested=[]
        for call in calls:
            assert call['mocked'] and call['source']=='mock_test_data'
            response=call['response'];payload=json.loads(call['messages'][-1]['content'].split('\n',1)[1])
            assert payload['incident']==raw['incident']
            for key in ('human_review','accepted_expected_behavior','proposed_review','source_url','family'):
                assert key not in payload['incident']
            if call['schema']=='ClassifierOutput':
                assert response['classification']['category']=='unknown'
                assert response['classification']['confidence']==0
            if call['schema']=='LiveLogInvestigatorOutput':
                entries=resolve_handles(payload['incident'],response['selected_evidence_handles'],response['evidence_contract'],response['evidence_snapshot'])
                requested.extend(e.evidence_id for e in entries)
                assert response['completeness']=='partial'
        ids=[]
        for e in state['evidence']['items']:
            entry=resolve_evidence(raw['incident'],e['evidence_id'])
            assert (e['reference'],e['observation'],e['source'])==(entry.reference,entry.observation,entry.source)
            assert entry.evidence_id not in all_ids,'cross-case ID reuse'
            ids.append(entry.evidence_id)
        all_ids.update(ids)
        assert set(requested)==set(ids)
        total_evidence+=len(ids);mock_calls+=len(calls)
        checks.append({'case_id':ident,'input_preserved':True,'evidence_entries_valid':len(ids),
            'route':actual_path,'termination':result['terminal_status'],'state_valid':True,
            'no_new_evidence_or_tool_claims':True,'cleanup_verified':True,
            'gate_reason':result['gate_observations'][0]['readiness']['reason']})
    assert not any(summary['parent_security'].values())
    assert summary['trace_exports']==summary['external_requests']==0
    return {'mode':'POST_RUN_MECHANICAL_VERIFICATION','real_cases_checked':len(checks),
        'valid_selected_evidence_entries':total_evidence,'mocked_model_calls':mock_calls,
        'external_requests':0,'sdk_client_initializations':0,'trace_exports':0,
        'source_reference_assessment_input_hashes_unchanged':True,'baseline':run.verify_baseline(),
        'read_only_artifact_hashes_verified':len(hashes),'cases':checks,
        'semantic_quality':None,'cost_usd':None}

if __name__=='__main__':
    run.clear_environment()
    def denied(*a,**k):raise RuntimeError('Post-run verifier network prohibited')
    socket.socket.connect=denied;socket.socket.connect_ex=denied;socket.getaddrinfo=denied
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    result=verify(args.run)
    if not args.output.resolve().is_relative_to(run.ROOT):raise ValueError('Output outside project')
    run.write(args.output,result)
    print(json.dumps({k:result[k] for k in ('real_cases_checked','valid_selected_evidence_entries','mocked_model_calls','external_requests','sdk_client_initializations','trace_exports','baseline')},indent=2))
