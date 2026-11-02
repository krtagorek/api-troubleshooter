"""Create-only offline request-diff and scripted comparison artifacts."""
import hashlib
import json
from pathlib import Path
from scripts import week4_real_mock_run as offline

ROOT = offline.ROOT
OUT = ROOT / 'reports/week4/attributed-selection-dependencies-v1-2'


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name, value):
    with (OUT / name).open('x') as f:
        json.dump(value, f, indent=2, ensure_ascii=False);f.write('\n')


def main():
    offline.clear_environment()
    with offline.offline_guard() as guard:
        from evaluation.week4.attributed_selection_v1 import SelectionAdvisory, missing_dependencies, VERSION
        from evaluation.week4.attributed_report_v2.readiness import assess
        from graph.state import LiveLogInvestigatorOutput
        from langchain_core.messages import SystemMessage, HumanMessage
        from evaluation.week4.live_provider import strict_wire
        from tests.week4.test_attributed_selection_v1 import run_graph
        from evaluation.week4.dependencies import verify_lock
        from tools.redaction import redact_message_content
        require_files = {'before-hashes.json', 'unittest.txt'}
        assert {p.name for p in OUT.iterdir()} == require_files
        live = ROOT / 'reports/week4/real-016-v2-3-approved-live-1/run'
        span = next(s for s in json.loads((live/'spans.json').read_text()) if s['name']=='LiveLogInvestigatorOutput')
        # Reestablish provider dict insertion order (sealed JSON is sorted).
        original = [dict(role=m['role'],content=m['content']) for m in span['inputs']['messages']]
        messages = [(SystemMessage if m['role']=='system' else HumanMessage)(content=m['content']) for m in original]
        class Capture:
            def with_structured_output(self, schema, **options):
                class Structured:
                    def invoke(self, messages):
                        Capture.messages=messages
                        return schema.model_validate(span['outputs'])
                return Structured()
        SelectionAdvisory(Capture()).with_structured_output(LiveLogInvestigatorOutput,
            method='json_schema',strict=True).invoke(messages)
        revised = [dict(role='system' if m.type=='system' else 'user',
            content=redact_message_content(m.content)) for m in Capture.messages]
        before=json.loads(original[-1]['content'].split('\n',1)[1])
        after=json.loads(revised[-1]['content'].split('\n',1)[1]);advice=after['selection_dependency_advisory']
        assert {k:v for k,v in after.items() if k!='selection_dependency_advisory'} == before
        assert original[:-1]==revised[:-1]
        assert strict_wire(LiveLogInvestigatorOutput,messages)==strict_wire(LiveLogInvestigatorOutput,Capture.messages)
        config=json.loads((ROOT/'data/week4/smoke-proposals/real-016-v2-3/config.json').read_text())
        def body(rows, objects):
            return dict(model=config['model'],messages=rows,temperature=0,max_completion_tokens=config['output_cap'],
                service_tier=config['service_tier'],stream=False,store=False,response_format={'type':'json_schema',
                'json_schema':{'name':'LiveLogInvestigatorOutput','strict':True,'schema':strict_wire(LiveLogInvestigatorOutput,objects)}})
        def encoded(body):return json.dumps(body,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
        bbody=body(original,messages);abody=body(revised,Capture.messages)
        assert hashlib.sha256(encoded(bbody)).hexdigest()==span['metadata']['request_bound']['prepared_request_sha256']
        assert len(encoded(abody)) < config['max_request_bytes']
        required=[e for g in advice['groups'] for e in g['operands']+g['required_all']]
        selected=span['outputs']['selected_evidence_handles'];omitted=[e for e in required if e['handle'] not in selected]
        write('required-and-omitted.json',{'selected_live_handles':selected,'required':required,'omitted':omitted,
            'all_packet_leaves_required':True,'original_exposure':'Incident metadata and flat catalog; no explicit dependency group.'})
        write('investigator-request-before.json',bbody);write('investigator-request-after.json',abody)
        write('request-diff.json',{'version':VERSION,'added_user_json_field':'selection_dependency_advisory','added':advice,
            'system_schema_parameters_unchanged':True,'other_user_fields_unchanged':True,
            'before_request_bytes':len(encoded(bbody)),'after_request_bytes':len(encoded(abody)),
            'before_prepared_request_sha256':hashlib.sha256(encoded(bbody)).hexdigest(),
            'after_prepared_request_sha256':hashlib.sha256(encoded(abody)).hexdigest(),
            'before_matches_sealed_live_prepared_hash':True,'request_limit_bytes':65536,'after_sent':False})
        results={}
        for selection in ('recorded','dependencies'):
            for arm in ('v2','selection_v1'):
                output,calls,path,states=run_graph(selection,treatment=arm=='selection_v1')
                state=states['log_investigator'];decision=assess(state['sanitized_inputs'],state['evidence'])
                results[selection+':'+arm]={'route':path,'model_calls':len(calls),'terminal_status':output['status'],
                    'analyst_entered':'root_cause_analyst' in path,'readiness':decision.model_dump(mode='json'),
                    'selection_dependency_report':missing_dependencies(state['sanitized_inputs'],state['evidence']),
                    'selected_evidence':state['evidence'].model_dump(mode='json'),'calls':calls,
                    'diagnosis':output['diagnosis'].model_dump(mode='json') if output['diagnosis'] else None,
                    'semantic_accuracy':None,'actual_cost_usd':None,'scripted_only':True}
        write('paired-scripted-controls.json',results)
        previous=json.loads((OUT/'before-hashes.json').read_text())
        changed=[p for p,h in previous.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
        assert not changed,changed
        baseline=json.loads((ROOT/'docs/source-baseline-manifest.json').read_text())['files']
        assert len(baseline)==328 and all(sha(ROOT/e['destination_relative_path'])==e['sha256'] for e in baseline)
        count=0;entries=0
        for directory in (ROOT/'reports/week4',ROOT/'data/week4/smoke-proposals'):
            for manifest in directory.rglob('artifact-hashes.json'):
                values=json.loads(manifest.read_text());assert all(sha(manifest.parent/p)==h for p,h in values.items())
                count+=1;entries+=len(values)
        dependencies=verify_lock()
        source_paths=sorted((ROOT/'evaluation/week4').rglob('*.py'))+[Path(__file__).resolve(),
            ROOT/'tests/week4/test_attributed_selection_v1.py']
        source_hashes={str(p.relative_to(ROOT)):sha(p) for p in source_paths if '__pycache__' not in p.parts}
        write('future-live-comparison-proposal.json',{'version':'v2-selection-dependencies-live-comparison-proposal-1',
            'status':'UNAUTHORIZED_NOT_EXECUTABLE','execution_authorized':False,'trace_export_authorized':False,
            'approval_identity':None,'approval_time':None,'case_id':'W4-REAL-016',
            'input_path':'data/week4/report-evidence-v2-1/inference/W4-REAL-016.json',
            'input_sha256':sha(ROOT/'data/week4/report-evidence-v2-1/inference/W4-REAL-016.json'),
            'archive_sha256':'dbc8ea81f66eba30c74cba89b08ab1c1ceee230886825f4f4f0acca429916d9f',
            'arms':['V2 without selection advisory','V2 plus attributed-selection-dependencies-v1'],
            'source_hashes':source_hashes,'dependencies':dependencies,
            'comparison':'Fresh arms, identical input/configuration/limits/schema/model; only advisory and missing-dependency reporting differ. Earlier sealed live result is historical, not a fresh paired control.',
            'max_calls_per_arm':5,'concurrency':1,'retries':0,'external_tracing':False,'incident_tools':False,
            'model_candidate_from_prior_proposal':'gpt-4.1-mini-2025-04-14','pricing_currently_verified':False,
            'comparison_budget_approved':False,'ceiling_usd':None,
            'blockers':['Explicit supervised-path integration/configuration for the new selection layer is not implemented.',
                'Refresh model lifecycle/pricing and calculate a funded two-arm budget; do not borrow the spent one-run approval.',
                'Prepare a newly bound executable proposal and obtain explicit approval.'],
            'semantic_accuracy':None})
        assert not any(guard.values())
        write('result.json',{'status':'PASS_OFFLINE_SCRIPTED_CONTROLS','version':VERSION,'tests_passed':32,
            'baseline_unchanged':328,'preexisting_protected_files_checked':len(previous),'changed_preexisting_files':changed,
            'sealed_manifests_verified':count,'sealed_artifact_entries_verified':entries,
            'required_evidence_count':len(required),'omitted_live_count':len(omitted),'real_input_versions_replayed':1,
            'synthetic_controls_counted_as_real_cases':False,'guard_attempts':guard,'dependencies':dependencies,
            'semantic_accuracy':None,'actual_cost_usd':None,'new_live_calls':0,'external_exports':0,
            'old_proposal_bytes_preserved':True,'old_proposal_current_source_inventory_matches':False,
            'source_inventory_note':'New Week 4 module changes current inventory. The old loader must reject replay; no rebinding performed.',
            'augmentation':'This layer adds no evidence. Within the attributed advisory scope it retains only explicitly selected IDs, reports omitted comparison candidates, and lets unchanged coverage checks hold. Outside scope the inherited path remains unchanged.',
            'reproduction':'The tests can be rerun; this artifact builder is create-once and intentionally refuses sealed output.'})
        offline.finalize(OUT)
        print(json.dumps({'required_count':len(required),'omitted_count':len(omitted),
            'request_bytes':[len(encoded(bbody)),len(encoded(abody))],'preserved_files':len(previous),'new_live_calls':0},indent=2))


if __name__=='__main__':main()
