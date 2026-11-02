"""Frozen inputs and existing supervised path, SDK MockTransport only."""
import copy
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import httpx2
from scripts import week4_real_mock_run as offline
from tests.week4.test_supervised_v2_provider import mock_only_sdk

ROOT=offline.ROOT
DATASET=ROOT/'data/week4/datasets/assignment-30-v1/manifest.json'


def make_plan(directory, *, arm='baseline', calls=150, budget='63.223200'):
    from evaluation.week4.live_cli import MANIFEST_PLAN
    from evaluation.week4.live_config import LiveConfig, MANIFEST_BUDGET_PROFILE, V2, SELECTION_V1
    from evaluation.week4.runner import metadata,digest
    settings=json.loads((ROOT/'data/week4/smoke-proposals/real-016-v2-3/config.json').read_text())
    settings.update(budget_profile=MANIFEST_BUDGET_PROFILE,max_usd='2.107440',
                    evidence_policy='inherited' if arm=='baseline' else V2,
                    selection_policy='off' if arm=='baseline' else SELECTION_V1)
    plan={'version':MANIFEST_PLAN,'arm':arm,'status':'OFFLINE_TEST_ONLY','execution_authorized':False,
        'approval_identity':None,'approval_time':None,'approval_binding_sha256':None,
        'trace_export_authorized':False,'external_tracing':False,'not_after_utc_date':'2027-01-13',
        'dataset_manifest_path':str(DATASET.relative_to(ROOT)),
        'dataset_manifest_sha256':hashlib.sha256(DATASET.read_bytes()).hexdigest(),
        'config':LiveConfig(**settings).public(),'configuration_sha256':digest(LiveConfig(**settings).public()),
        'source_hashes':metadata('test','test','test')['source_hashes'],
        'execution':{'case_count':30,'max_calls':calls,'max_usd':budget,'concurrency':1,'retries':0,'external_diagnostic_tools':False},
        'output_path':str((Path(directory)/'live-output').relative_to(ROOT))}
    p=Path(directory)/('plan-'+arm+'.json');p.write_text(json.dumps(plan));return p


def mock_worker(*args):
    os.environ.clear()
    with patch('openai.OpenAI.__init__',new=mock_only_sdk), \
         patch('langsmith.Client.__init__',side_effect=AssertionError('No exports')), \
         patch('langsmith.AsyncClient.__init__',side_effect=AssertionError('No exports')):
        from evaluation.week4.smoke import inference_worker
        inference_worker(*args)


class CaseManifestControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):offline.clear_environment()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT/'.venv-week4-locked');self.addCleanup(self.tmp.cleanup)
        self.directory=Path(self.tmp.name)
        for name in ('socket.socket.connect','socket.socket.connect_ex','socket.getaddrinfo','socket.create_connection',
                     'langsmith.Client.__init__','langsmith.AsyncClient.__init__'):
            p=patch(name,side_effect=AssertionError('External operation blocked'));p.start();self.addCleanup(p.stop)
    def test_thirty_inputs_references_and_nested_evaluator_isolation(self):
        from evaluation.week4.contracts import load_case_manifest,InferenceCase,BoundaryFailure
        from graph.state import initialize_state
        from tools.evidence_catalog import build_catalog,resolve_evidence
        manifest,cases=load_case_manifest(DATASET)
        self.assertEqual(len(cases),30);self.assertEqual(len({c['case_id'] for c in cases}),30)
        self.assertEqual(sum(r['artificial_allowance'] for r in manifest['cases']),5)
        self.assertNotIn('V2-01-03',[c['case_id'] for c in cases]);self.assertNotIn('W4-REAL-030',[c['case_id'] for c in cases])
        for raw in cases:
            typed=InferenceCase.model_validate(raw)
            state=initialize_state(typed.incident,'offline-contract',max_retries=0)
            self.assertEqual(state['sanitized_inputs'].model_dump(mode='json'),raw['incident'])
            for entry in build_catalog(typed.incident).values():
                self.assertEqual(resolve_evidence(typed.incident,entry.evidence_id),entry)
            for key in ('expected_answer','scenario_label','expected_supported_response','human_review'):
                bad=copy.deepcopy(raw);bad['incident']['request_metadata'][key]='EVALUATOR_ONLY'
                with self.assertRaises(BoundaryFailure):InferenceCase.model_validate(bad)
    def test_corrupt_input_reference_rubric_and_duplicate_manifest_rejected(self):
        from evaluation.week4.contracts import load_case_manifest,BoundaryFailure
        for relative in ('inputs/W4-REAL-005.json','references/W4-REAL-005.json','rubric.json','applicability.json','provenance.json','scenarios.json'):
            d=self.directory/relative.split('/')[0];d=self.directory/('copy-'+str(len(list(self.directory.iterdir()))))
            shutil.copytree(DATASET.parent,d);p=d/relative;p.write_text(p.read_text()+' ')
            with self.assertRaises(BoundaryFailure):load_case_manifest(d/'manifest.json')
        d=self.directory/'duplicate';shutil.copytree(DATASET.parent,d)
        m=json.loads((d/'manifest.json').read_text());m['cases'][1]=m['cases'][0];(d/'manifest.json').write_text(json.dumps(m))
        with self.assertRaises(BoundaryFailure):load_case_manifest(d/'manifest.json')
    def test_configuration_parity_old_defaults_and_unauthorized_live(self):
        from evaluation.week4.live_cli import load_plan
        from evaluation.week4 import smoke
        from evaluation.week4.live_config import LiveConfig
        bp=make_plan(self.directory);tp=make_plan(self.directory,arm='improved')
        b,bc=load_plan(bp);t,tc=load_plan(tp)
        self.assertEqual(b['dataset_manifest_sha256'],t['dataset_manifest_sha256'])
        bd=bc.public();td=tc.public()
        for k in ('evidence_policy','selection_policy'):bd.pop(k);td.pop(k)
        self.assertEqual(bd,td)
        with patch.object(smoke,'run_smoke',side_effect=AssertionError('No dispatch')):
            with self.assertRaises(ValueError):smoke.run_manifest(bp,self.directory/'denied',mode='live',execute_live=True)
        legacy=LiveConfig(model='test',input_per_million='1',output_per_million='1',pricing_source='https://example.invalid/test',pricing_verified_at='TEST')
        self.assertEqual(legacy.max_usd,'0.25')
        with self.assertRaises(ValueError):replace(legacy,max_usd='2.25')
        bad=copy.deepcopy(b);bad['config']['service_tier']='priority';bp.write_text(json.dumps(bad))
        with self.assertRaises((ValueError,RuntimeError)):load_plan(bp)
    def test_full_thirty_case_sdk_mock_batch_real_supervisor_and_parity(self):
        from evaluation.week4 import smoke
        from evaluation.week4.contracts import load_case_manifest
        cases=load_case_manifest(DATASET)[1]
        requests={}
        for arm in ('baseline','improved'):
            p=make_plan(self.directory,arm=arm);out=self.directory/arm
            with patch.object(smoke,'inference_worker',new=mock_worker):
                result=smoke.run_manifest(p,out)
            self.assertEqual(result['batch_status'],'finished');self.assertEqual(result['assigned_cases'],30)
            self.assertEqual(result['attempted_cases'],30)
            self.assertLessEqual(result['accounting']['attempted_model_calls'],150)
            self.assertEqual(len(result['case_statuses']),30)
            self.assertTrue(set(result['case_statuses'].values()) <= {'held','completed','failed'})
            requests[arm]=[]
            for i,c in enumerate(cases):
                record=json.loads((out/'case-records'/f'{i:03d}.json').read_text())
                self.assertEqual(record['terminal_status'],result['case_statuses'][c['case_id']])
                self.assertTrue(record['supervisor']['cleanup_verified'])
                child=out/'cases'/c['case_id']
                self.assertEqual(json.loads((child/'experiment.json').read_text())['input_sha256'],smoke.digest(c))
                sent=[json.loads(s) for s in (child/'mock-model-requests.jsonl').read_text().splitlines()]
                self.assertGreaterEqual(len(sent),1);self.assertLessEqual(len(sent),5)
                self.assertEqual(len(sent),record['accounting']['attempted_calls'])
                envelope=json.loads(sent[0]['messages'][1]['content'].split('\n',1)[1]);self.assertEqual(envelope['incident'],c['incident'])
                self.assertTrue((child/'spans.json').is_file())
                spans=json.loads((child/'spans.json').read_text())
                self.assertEqual(sum(s['kind']=='model' for s in spans),len(sent))
                self.assertEqual(json.loads((child/'trace-status.json').read_text()),{'status':'not_requested'})
                requests[arm].append(sent)
            self.assertEqual(sum(map(len,requests[arm])),result['accounting']['attempted_model_calls'])
        receipt={}
        for arm in requests:
            receipt[arm]=[]
            for i,(c,sent) in enumerate(zip(cases,requests[arm])):
                record=json.loads((self.directory/arm/'case-records'/f'{i:03d}.json').read_text())
                receipt[arm].append({'case_id':c['case_id'],'executed_calls':len(sent),
                    'schemas':[r['response_format']['json_schema']['name'] for r in sent],
                    'terminal_status':record['terminal_status'],'errors':record['errors'],
                    'stage_coverage':record['stage_coverage'],'supervisor':record['supervisor']})
        (self.directory/'paired-mock-summary.json').write_text(json.dumps(
            {'kind':'SCRIPTED_BRANCH_COVERAGE_NOT_SEMANTIC_QUALITY','arms':receipt,
             'input_parity':True,'semantic_accuracy':None,'actual_cost_usd':None},indent=2)+'\n')
        for case,baseline,improved in zip(cases,requests['baseline'],requests['improved']):
            self.assertEqual(baseline[0],improved[0])
            # Compare requests at shared actual boundaries, not invented child
            # calls. Different routes/errors remain recorded case outcomes.
            by_schema=lambda calls:{r['response_format']['json_schema']['name']:r for r in calls}
            bmap,tmap=by_schema(baseline),by_schema(improved)
            if not all('LiveLogInvestigatorOutput' in m for m in (bmap,tmap)):
                for arm,m in [('baseline',bmap),('improved',tmap)]:
                    if 'LiveLogInvestigatorOutput' not in m:
                        record=next(r for r in receipt[arm] if r['case_id']==case['case_id'])
                        self.assertIn(record['stage_coverage']['log_investigator'],('completed','failed','not_reached'))
                continue
            b=json.loads(bmap['LiveLogInvestigatorOutput']['messages'][1]['content'].split('\n',1)[1])
            t=json.loads(tmap['LiveLogInvestigatorOutput']['messages'][1]['content'].split('\n',1)[1]);t.pop('selection_dependency_advisory',None)
            self.assertEqual(b,t)
    def test_failed_parsing_case_retained_and_next_safe_case_continues(self):
        from evaluation.week4 import smoke
        p=make_plan(self.directory);real=smoke.run_smoke;count=[0]
        def first_parse(*args,**kwargs):
            count[0]+=1;kwargs['scenario']='parsing' if count[0]==1 else 'v2_mechanics'
            return real(*args,**kwargs)
        with patch.object(smoke,'inference_worker',new=mock_worker),patch.object(smoke,'run_smoke',side_effect=first_parse):
            result=smoke.run_manifest(p,self.directory/'failed-then-safe')
        self.assertEqual(result['batch_status'],'finished');self.assertEqual(result['assigned_cases'],30)
        records=sorted((self.directory/'failed-then-safe/case-records').glob('*.json'))
        first=json.loads(records[0].read_text());second=json.loads(records[1].read_text())
        self.assertEqual(first['terminal_status'],'failed');self.assertIn('schema_rejection',first['errors'])
        self.assertEqual(second['terminal_status'],'held');self.assertTrue(second['attempted'])
    def test_unknown_usage_retained_and_budget_stop_never_dispatches_further(self):
        from evaluation.week4 import smoke
        p=make_plan(self.directory)
        with patch.object(smoke,'inference_worker',new=mock_worker):
            result=smoke.run_manifest(p,self.directory/'missing',scenario='missing_usage')
        self.assertEqual(result['batch_status'],'stopped');self.assertEqual(result['accounting']['attempted_model_calls'],1)
        self.assertIsNone(result['accounting']['usage_priced_total_usd'])
        self.assertEqual(result['unattempted_cases'],29)
        tail=json.loads((self.directory/'missing/case-records/029.json').read_text())
        self.assertEqual(set(tail['stage_coverage'].values()),{'not_reached'})
        self.assertIsNone(tail['elapsed_seconds']);self.assertEqual(tail['receipts'],[])
        self.assertGreater(float(result['accounting']['retained_reservations_usd']),0)
        p=make_plan(self.directory,calls=4,budget='1.685952')
        with patch.object(smoke,'inference_worker',side_effect=AssertionError('No dispatch')):
            result=smoke.run_manifest(p,self.directory/'budget')
        self.assertEqual(result['accounting']['attempted_model_calls'],0);self.assertEqual(result['assigned_cases'],30)
    def test_changed_plan_binding_fails_before_dispatch(self):
        from evaluation.week4.live_cli import load_plan
        from evaluation.week4.contracts import BoundaryFailure
        p=make_plan(self.directory);v=json.loads(p.read_text());v['dataset_manifest_sha256']='0'*64;p.write_text(json.dumps(v))
        with self.assertRaises(BoundaryFailure):load_plan(p)
    def test_interrupted_and_timeout_children_retained_and_cleanup_verified(self):
        from evaluation.week4 import smoke
        from evaluation.week4.runner import digest
        for scenario in ('interrupt','timeout'):
            p=make_plan(self.directory);v=json.loads(p.read_text());v['config']['case_timeout_seconds']=2
            v['configuration_sha256']=digest(v['config']);p.write_text(json.dumps(v))
            out=self.directory/scenario
            with patch.object(smoke,'inference_worker',new=mock_worker):
                result=smoke.run_manifest(p,out,scenario=scenario)
            self.assertEqual(result['batch_status'],'stopped');self.assertEqual(result['unattempted_cases'],29)
            first=json.loads((out/'case-records/000.json').read_text())
            self.assertTrue(first['supervisor']['cleanup_verified'])
            self.assertEqual(first['accounting']['attempted_calls'],1)
            self.assertEqual(first['accounting']['uncertain_calls'],1)
            with self.assertRaises(ProcessLookupError):os.kill(first['supervisor']['child_pid'],0)
    def test_unreadable_journal_retains_liability_without_invented_attempts(self):
        from evaluation.week4 import smoke
        from evaluation.week4.contracts import AccountingFailure
        def broken(case,config,directory,**kwargs):
            directory.mkdir();(directory/'journal.jsonl').write_text('{"event":')
            raise AccountingFailure('SYNTHETIC interrupted append')
        p=make_plan(self.directory)
        with patch.object(smoke,'run_smoke',side_effect=broken):
            result=smoke.run_manifest(p,self.directory/'corrupt')
        self.assertEqual(result['batch_status'],'stopped')
        self.assertEqual(result['attempted_cases_unknown'],1)
        self.assertFalse(result['accounting']['attempted_model_calls_complete'])
        self.assertEqual(result['accounting']['unknown_call_slot_bound'],5)
        self.assertEqual(result['accounting']['unknown_case_liability_bound_usd'],'2.107440')
        first=json.loads((self.directory/'corrupt/case-records/000.json').read_text())
        self.assertIsNone(first['accounting']['attempted_calls'])
        self.assertFalse(first['stage_coverage_complete'])
        self.assertIsNone(result['accounting']['usage_priced_total_usd'])


if __name__=='__main__':unittest.main()
