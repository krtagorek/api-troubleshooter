"""Supervised SDK MockTransport checks; fixture receipts are not real spending."""
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import httpx2
from tests.week4.test_supervised_v2_provider import mock_only_sdk
from scripts import week4_real_mock_run as offline

ROOT = offline.ROOT


def paired_transport(directory, scenario):
    def handler(request):
        from graph import state
        from evaluation.week4.fixtures import mock_reply
        from evaluation.week4.attributed_selection_v1 import dependency_advisory
        body = json.loads(request.content)
        with (Path(directory)/'mock-model-requests.jsonl').open('a') as f:f.write(json.dumps(body)+'\n')
        envelope = json.loads(body['messages'][1]['content'].split('\n',1)[1])
        name = body['response_format']['json_schema']['name']
        raw = mock_reply(body)['output']
        if name == 'LiveLogInvestigatorOutput':
            handles = ['E41','E43','E47','E01']
            if scenario == 'dependencies':
                advice = dependency_advisory(envelope['incident'])
                handles = sorted(set(handles+[e['handle'] for g in advice['groups']
                    for e in g['operands']+g['required_all']]))
            raw.update(selected_evidence_handles=handles, completeness='complete', diagnostic_gaps=[])
        output = getattr(state,name).model_validate(raw).model_dump(mode='json')
        for key in ('evidence_contract','evidence_snapshot'):
            if key in output and key in envelope:output[key]=envelope[key]
        usage={'prompt_tokens':11,'completion_tokens':7,'total_tokens':18,
            'prompt_tokens_details':{'cached_tokens':0},'completion_tokens_details':{'reasoning_tokens':0}}
        return httpx2.Response(200,json={'id':'SCRIPTED-NOT-A-REAL-RECEIPT','object':'chat.completion',
            'created':0,'model':body['model'],'service_tier':'default','usage':usage,
            'choices':[{'index':0,'finish_reason':'stop','message':{'role':'assistant','content':json.dumps(output)}}]})
    return httpx2.MockTransport(handler)


def mock_worker(*args):
    os.environ.clear()
    with patch('openai.OpenAI.__init__',new=mock_only_sdk), \
         patch('langsmith.Client.__init__',side_effect=AssertionError('No exports')), \
         patch('langsmith.AsyncClient.__init__',side_effect=AssertionError('No exports')), \
         patch('evaluation.week4.sdk_fixtures.model_transport',new=paired_transport):
        from evaluation.week4.smoke import inference_worker
        inference_worker(*args)


def config(policy='off'):
    from evaluation.week4.live_config import LiveConfig
    values=json.loads((ROOT/'data/week4/smoke-proposals/real-016-v2-3/config.json').read_text())
    values['selection_policy']=policy
    return LiveConfig(**values)


def supervised_pair(directory,scenario):
    from evaluation.week4 import smoke
    from evaluation.week4.live_config import SELECTION_V1
    case=json.loads((ROOT/'data/week4/report-evidence-v2-1/inference/W4-REAL-016.json').read_text())
    results={};requests={}
    for arm,policy in [('baseline','off'),('treatment',SELECTION_V1)]:
        destination=Path(directory)/arm
        with patch.object(smoke,'inference_worker',new=mock_worker):
            result,tracing=smoke.run_smoke(case,config(policy),destination,mode='offline_test',scenario=scenario)
        results[arm]=result
        requests[arm]=[json.loads(x) for x in (destination/'mock-model-requests.jsonl').read_text().splitlines()]
        assert tracing=={'status':'not_requested'}
    return results,requests


class SupervisedSelectionControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):offline.clear_environment()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT/'.venv-week4-locked');self.addCleanup(self.tmp.cleanup)
        self.directory=Path(self.tmp.name)
        for name in ('socket.socket.connect','socket.socket.connect_ex','socket.getaddrinfo','socket.create_connection',
                     'langsmith.Client.__init__','langsmith.AsyncClient.__init__'):
            p=patch(name,side_effect=AssertionError('External operation blocked'));p.start();self.addCleanup(p.stop)
    def compare_requests(self,requests):
        b,t=requests['baseline'],requests['treatment']
        self.assertEqual(b[0],t[0])
        self.assertEqual({k:v for k,v in b[1].items() if k!='messages'},
                         {k:v for k,v in t[1].items() if k!='messages'})
        self.assertEqual(b[1]['messages'][0],t[1]['messages'][0])
        bp=json.loads(b[1]['messages'][1]['content'].split('\n',1)[1])
        tp=json.loads(t[1]['messages'][1]['content'].split('\n',1)[1])
        self.assertIn('selection_dependency_advisory',tp);tp.pop('selection_dependency_advisory')
        self.assertEqual(bp,tp)
        if len(b)>2:self.assertEqual(b[2:],t[2:])
    def test_recorded_selection_both_hold_and_only_advisory_request_differs(self):
        results,requests=supervised_pair(self.directory,'recorded');self.compare_requests(requests)
        for arm,row in results.items():
            self.assertEqual(row['terminal_status'],'held');self.assertEqual(row['errors'],[])
            self.assertEqual(row['accounting']['attempted_calls'],2)
            self.assertEqual(row['selection_measurements']['required_reference_count'],39)
            self.assertEqual(row['selection_measurements']['selected_required_reference_count'],2)
            self.assertEqual(len(row['selection_measurements']['missing_dependencies']),37)
            self.assertFalse(row['selection_measurements']['qualified_analysis'])
            self.assertEqual(row['stage_coverage']['root_cause_analyst'],'not_reached')
            self.assertEqual(len(row['output']['evidence']['items']),4)
            self.assertTrue(row['supervisor']['cleanup_verified'])
        self.assertTrue(any('V2 attribution selection' in e['description']
            for e in results['treatment']['output']['evidence']['missing']))
    def test_explicit_dependencies_both_reach_inconclusive_analyst_with_reconciled_mock_usage(self):
        results,requests=supervised_pair(self.directory,'dependencies');self.compare_requests(requests)
        for row in results.values():
            self.assertEqual(row['terminal_status'],'held');self.assertEqual(row['errors'],[])
            self.assertEqual(row['stage_coverage']['root_cause_analyst'],'completed')
            self.assertEqual(row['selection_measurements']['selected_required_reference_count'],39)
            self.assertTrue(row['selection_measurements']['qualified_analysis'])
            self.assertFalse(row['selection_measurements']['definitive_confirmation'])
            self.assertEqual(row['output']['diagnosis']['status'],'inconclusive')
            self.assertEqual(row['accounting']['attempted_calls'],3)
            self.assertEqual(row['accounting']['uncertain_calls'],0)
            self.assertEqual(row['accounting']['retained_reservations_usd'],'0')
            self.assertEqual(sum(c['input_tokens'] for c in row['receipts']),33)
            self.assertEqual(sum(c['output_tokens'] for c in row['receipts']),21)
    def test_unknown_selection_policy_and_inherited_treatment_rejected(self):
        from evaluation.week4.live_config import LiveConfig,SELECTION_V1
        for values in ({'selection_policy':'v99'}, {'selection_policy':SELECTION_V1,'evidence_policy':'inherited'}):
            with self.assertRaises(ValueError):replace(config(),**values)
    def test_direct_live_treatment_without_bound_authorization_cannot_dispatch(self):
        from evaluation.week4.smoke import run_smoke
        from evaluation.week4.live_config import SELECTION_V1
        from evaluation.week4.contracts import BoundaryFailure
        with self.assertRaises(BoundaryFailure):
            run_smoke({},config(SELECTION_V1),self.directory/'never',mode='live',execute_live=True)
        self.assertFalse((self.directory/'never').exists())


class PairPlanControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        offline.clear_environment();cls.guard=offline.offline_guard();cls.guard.__enter__()
    @classmethod
    def tearDownClass(cls):cls.guard.__exit__(None,None,None)
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT/'data/week4');self.addCleanup(self.tmp.cleanup)
        self.directory=Path(self.tmp.name)
        self.results=tempfile.TemporaryDirectory(dir=ROOT/'reports/week4');self.addCleanup(self.results.cleanup)
        self.outputs=Path(self.results.name)
    def plans(self):
        from evaluation.week4.live_config import SELECTION_V1,V2
        from evaluation.week4.paired_selection_plan_v1 import VERSION
        from evaluation.week4.live_cli import PAIR_ARM
        from evaluation.week4.runner import metadata,digest
        input_path='data/week4/report-evidence-v2-1/inference/W4-REAL-016.json'
        case=json.loads((ROOT/input_path).read_text());input_sha=hashlib.sha256((ROOT/input_path).read_bytes()).hexdigest()
        sources=metadata('proposed-smoke','development-smoke','development-fixtures-1')['source_hashes']
        manifest={'version':VERSION,'comparison_id':'SYNTHETIC-PLAN-CONTROL',
            'trace_export_authorized':False,'external_tracing':False,'incident_tools':False,
            'concurrency':1,'retries':0,'combined_ceiling_usd':'4.50','case_sha256':digest(case),
            'source_hashes':sources,'input_bytes_sha256':input_sha,
            'archive_sha256':case['incident']['request_metadata']['report_attribution_v2']['source_sha256'],
            'arms':{n:{'config':config(p).public(),'configuration_sha256':digest(config(p).public()),
                'output_path':str((self.outputs/n).relative_to(ROOT))}
                for n,p in [('baseline','off'),('treatment',SELECTION_V1)]}}
        master=self.directory/'comparison.json';master.write_text(json.dumps(manifest))
        plans={}
        for name in ('baseline','treatment'):
            settings=manifest['arms'][name]['config']
            plans[name]={'version':PAIR_ARM,'case':case,'case_sha256':digest(case),'source_hashes':sources,
                'config':settings,'configuration_sha256':digest(settings),'evidence_policy':V2,
                'external_tracing':False,'trace_export_authorized':False,'archive_sha256':manifest['archive_sha256'],
                'execution_authorized':False,'approval_identity':None,'approval_time':None,'approval_binding_sha256':None,
                'not_after_utc_date':'2027-01-13','input_path':input_path,'input_bytes_sha256':input_sha,
                'component_hashes':{input_path:input_sha,str(master.relative_to(ROOT)):hashlib.sha256(master.read_bytes()).hexdigest()},
                'comparison_manifest_path':str(master.relative_to(ROOT)),'comparison_id':manifest['comparison_id'],
                'arm':name,'output_path':manifest['arms'][name]['output_path']}
        return plans,manifest,master
    def test_funded_arms_and_unapproved_cli_cannot_dispatch(self):
        from evaluation.week4 import live_cli
        plans,_,_=self.plans()
        for name,plan in plans.items():
            path=self.directory/(name+'.json');path.write_text(json.dumps(plan))
            _,settings=live_cli.load_plan(path);self.assertEqual(settings.max_usd,'2.25')
            with self.assertRaises(ValueError):live_cli.require_execution_authorization(plan)
            with patch('sys.argv',['live_cli','run','--plan',str(path),'--output',str(self.outputs/name),'--execute-live']), \
                 patch.object(live_cli,'run_smoke',side_effect=AssertionError('Execution prohibited')) as run:
                with self.assertRaises(SystemExit):live_cli.main()
                run.assert_not_called()
    def test_manifest_budget_policy_case_and_component_tampering_rejected(self):
        from evaluation.week4.live_cli import load_plan
        plans,manifest,master=self.plans();plan=plans['treatment']
        for field in ('combined_ceiling_usd','case_sha256','concurrency','baseline_policy'):
            altered=json.loads(json.dumps(manifest))
            if field=='baseline_policy':altered['arms']['baseline']['config']['selection_policy']='attributed-selection-dependencies-v1'
            else:altered[field]={'combined_ceiling_usd':'2.25','case_sha256':'0'*64,'concurrency':2}[field]
            master.write_text(json.dumps(altered))
            # Even if a new file hash is supplied, semantic pairing must validate.
            plan['component_hashes'][str(master.relative_to(ROOT))]=hashlib.sha256(master.read_bytes()).hexdigest()
            path=self.directory/'arm.json';path.write_text(json.dumps(plan))
            with self.subTest(field=field),self.assertRaises(ValueError):load_plan(path)
    def test_output_single_use_and_treatment_cannot_precede_reconciliation(self):
        from evaluation.week4.paired_selection_plan_v1 import check_dispatch
        from evaluation.week4.contracts import BoundaryFailure
        plans,manifest,_=self.plans()
        check_dispatch(plans['baseline'],self.outputs/'baseline')
        with self.assertRaises(BoundaryFailure):check_dispatch(plans['treatment'],self.outputs/'treatment')
        (self.outputs/'baseline').mkdir()
        with self.assertRaises(BoundaryFailure):check_dispatch(plans['baseline'],self.outputs/'baseline')
        with self.assertRaises(BoundaryFailure):check_dispatch(plans['baseline'],self.outputs/'elsewhere')
        directory=self.outputs/'baseline'
        result={'fixture':'SYNTHETIC-GATE-CONTROL-NOT-A-LIVE-RUN','terminal_status':'held','errors':[],
            'mode':'live','supervisor':{'cleanup_verified':True},'accounting':{'uncertain_calls':1,'limit_violations':0}}
        meta={'config':manifest['arms']['baseline']['config'],'input_sha256':plans['baseline']['case_sha256'],
              'source_hashes':plans['baseline']['source_hashes']}
        def seal_fixture():
            (directory/'result.json').write_text(json.dumps(result));(directory/'experiment.json').write_text(json.dumps(meta))
            values={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in directory.iterdir() if p.name!='artifact-hashes.json'}
            (directory/'artifact-hashes.json').write_text(json.dumps(values))
        seal_fixture()
        with self.assertRaises(BoundaryFailure):check_dispatch(plans['treatment'],self.outputs/'treatment')
        result['accounting']['uncertain_calls']=0;seal_fixture()
        check_dispatch(plans['treatment'],self.outputs/'treatment')
    def test_old_proposal_cannot_enable_treatment_and_authorization_binding_is_arm_specific(self):
        from evaluation.week4.live_cli import load_plan,PROPOSAL3,authorization_identity,require_execution_authorization
        plans,_,_=self.plans();plan=plans['treatment'];plan['version']=PROPOSAL3
        path=self.directory/'old.json';path.write_text(json.dumps(plan))
        with self.assertRaisesRegex(ValueError,'paired-arm'):load_plan(path)
        plans,_,_=self.plans();baseline=plans['baseline'];treatment=plans['treatment']
        treatment.update(execution_authorized=True,approval_identity='SYNTHETIC-NOT-APPROVAL',
            approval_time='SYNTHETIC-NOT-A-TIMESTAMP',approval_binding_sha256=authorization_identity(baseline))
        with self.assertRaises(ValueError):require_execution_authorization(treatment)


if __name__=='__main__':unittest.main()
