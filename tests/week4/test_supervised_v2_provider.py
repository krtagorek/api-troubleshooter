"""Mock SDK transports only. No plan execution, credentials or external exports."""
import dataclasses
from decimal import Decimal
import json
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch
import httpx2
from openai import OpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import ClassifierOutput
from evaluation.week4.live_config import LiveConfig, V2
from evaluation.week4.live_provider import LiveModel
from evaluation.week4.accounting import Journal
from evaluation.week4.durable_trace import DurableTrace
from evaluation.week4.contracts import ResourceFailure, AccountingFailure

ROOT=Path(__file__).resolve().parents[2]
ORIGINAL_INIT=OpenAI.__init__

def mock_only_sdk(self,*args,**kwargs):
    http=kwargs.get('http_client')
    if not isinstance(getattr(http,'_transport',None),httpx2.MockTransport):
        raise AssertionError('Live SDK construction forbidden in this test')
    if kwargs.get('api_key')!='offline-test-placeholder':
        raise AssertionError('Only fixture key is permitted')
    return ORIGINAL_INIT(self,*args,**kwargs)

def isolated_worker(*args):
    # The supervisor is tested, but no public run_smoke/live CLI is invoked.
    os.environ.clear()
    with patch('openai.OpenAI.__init__',new=mock_only_sdk), \
         patch('langsmith.Client.__init__',side_effect=AssertionError('Export forbidden')), \
         patch('langsmith.AsyncClient.__init__',side_effect=AssertionError('Export forbidden')):
        from evaluation.week4.smoke import inference_worker
        inference_worker(*args)


def config(**changes):
    values=dict(model='gpt-4.1-mini-2025-04-14',input_per_million='0.01',output_per_million='0.02',
        cached_input_per_million='0.001',pricing_source='https://example.invalid/TEST-ONLY',
        pricing_verified_at='TEST-ONLY',evidence_policy=V2,input_bound_kind='model_context_max',input_cap=1047576)
    values.update(changes);return LiveConfig(**values)

class ProviderControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):os.environ.clear()
    def setUp(self):
        base=ROOT/'.venv-week4-py311/supervised-v2-provider-tests';base.mkdir(exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=base);self.addCleanup(self.tmp.cleanup)
        self.directory=Path(self.tmp.name);self.sent=[]
        for target in ('socket.socket.connect','socket.socket.connect_ex','socket.getaddrinfo','socket.create_connection'):
            p=patch(target,side_effect=AssertionError('External network blocked'));p.start();self.addCleanup(p.stop)
        for target in ('langsmith.Client.__init__','langsmith.AsyncClient.__init__'):
            p=patch(target,side_effect=AssertionError('Exports prohibited'));p.start();self.addCleanup(p.stop)
        p=patch('openai.OpenAI.__init__',new=mock_only_sdk);p.start();self.addCleanup(p.stop)
    def model(self,scenario='normal',settings=None):
        settings=settings or config();directory=self.directory/('model-'+str(len(list(self.directory.iterdir()))));directory.mkdir()
        journal=Journal.create(directory,settings.public());trace=DurableTrace(journal,'SYNTHETIC-SDK','synthetic-root')
        def handler(request):
            body=json.loads(request.content);self.sent.append(body)
            self.assertEqual(body['service_tier'],'default');self.assertEqual(body['max_completion_tokens'],settings.output_cap)
            if scenario=='timeout':raise httpx2.ReadTimeout('synthetic timeout')
            output={'evidence_contract':None,'evidence_snapshot':None,
                    'classification':{'category':'unknown','confidence':0,'reasoning':'Synthetic test only.','evidence_references':[]}}
            usage={'prompt_tokens':11,'completion_tokens':7,'total_tokens':18,
                   'prompt_tokens_details':{'cached_tokens':2},'completion_tokens_details':{'reasoning_tokens':3}}
            payload={'id':'fixture','object':'chat.completion','created':0,'model':settings.model,
                'service_tier':'default','usage':usage,'choices':[{'index':0,'finish_reason':'stop',
                'message':{'role':'assistant','content':json.dumps(output)}}]}
            if scenario=='missing':payload.pop('usage')
            if scenario=='cache_missing':usage['prompt_tokens_details']={}
            if scenario=='ambiguous':usage['total_tokens']=19
            if scenario=='bad_tier':payload['service_tier']='priority'
            if scenario=='tier_missing':payload.pop('service_tier')
            if scenario=='parse':payload['choices'][0]['message']['content']='{}'
            return httpx2.Response(500 if scenario=='provider_error' else 200,json=payload)
        model=LiveModel(settings,journal,trace,'offline-test-placeholder',transport=httpx2.MockTransport(handler))
        return model,journal
    def invoke(self,model,text='Synthetic untrusted evidence only.'):
        return model.with_structured_output(ClassifierOutput).invoke([SystemMessage(content='Return schema.'),HumanMessage(content=text)])
    def test_usage_reconciles_cached_and_reasoning_counts_once_before_parse(self):
        m,j=self.model();self.invoke(m)
        self.assertEqual(Decimal(j.totals(j.events())['usage_priced_cost_usd']),Decimal('0.000000232'))
        self.assertEqual(m.receipts[0]['reasoning_tokens'],3)
        m,j=self.model('parse')
        with self.assertRaises(Exception):self.invoke(m)
        self.assertEqual(j.totals(j.events())['uncertain_calls'],0)
        events=[e['event'] for e in j.events()];self.assertLess(events.index('usage'),events.index('call_error'))
    def test_oversize_system_state_schema_and_advisory_rejected_before_dispatch(self):
        m,j=self.model(settings=config(max_request_bytes=1024))
        with self.assertRaises(ResourceFailure):self.invoke(m,'growing state/advisory '*2000)
        self.assertEqual(self.sent,[]);self.assertEqual(j.totals(j.events())['reserved_calls'],0)
        self.assertEqual(j.totals(j.events())['attempted_calls'],0)
        self.assertTrue(any(e['event']=='request_rejected' for e in j.events()))
        # Even short visible text cannot omit schema/system bytes from the cap.
        m,j=self.model(settings=config(max_request_bytes=1024))
        with self.assertRaises(ResourceFailure):self.invoke(m,'tiny')
        self.assertEqual(self.sent,[])
    def test_budget_and_call_limits_prevent_more_dispatch(self):
        m,j=self.model(settings=config(max_calls=1));self.invoke(m)
        with self.assertRaises(ResourceFailure):self.invoke(m)
        self.assertEqual(len(self.sent),1)
        m,j=self.model(settings=config(max_usd='0.000001'))
        with self.assertRaises(ResourceFailure):self.invoke(m)
        self.assertEqual(j.totals(j.events())['attempted_calls'],0)
        self.assertEqual(len(self.sent),1)
    def test_real_rate_full_context_reservation_is_infeasible_at_025(self):
        m,j=self.model(settings=config(input_per_million='0.40',output_per_million='1.60',cached_input_per_million='0.10'))
        with self.assertRaises(ResourceFailure):self.invoke(m)
        self.assertEqual(self.sent,[])
        self.assertEqual(j.totals(j.events())['reserved_calls'],0)
    def test_missing_ambiguous_cache_and_tier_usage_retain_and_block(self):
        for scenario in ('missing','cache_missing','ambiguous','bad_tier','tier_missing'):
            with self.subTest(scenario=scenario):
                m,j=self.model(scenario)
                with self.assertRaises(Exception):self.invoke(m)
                totals=j.totals(j.events());self.assertEqual(totals['uncertain_calls'],1)
                self.assertIsNone(totals['usage_priced_cost_usd'])
                self.assertGreater(Decimal(totals['retained_reservations_usd']),0)
                before=len(self.sent)
                with self.assertRaises(AccountingFailure):self.invoke(m)
                self.assertEqual(len(self.sent),before)
    def test_timeout_and_provider_error_fail_without_retry(self):
        for scenario in ('timeout','provider_error'):
            m,j=self.model(scenario);before=len(self.sent)
            with self.assertRaises(Exception):self.invoke(m)
            self.assertEqual(len(self.sent),before+1)
            self.assertIsInstance(m.fatal,AccountingFailure)
            if scenario=='timeout':self.assertEqual(j.totals(j.events())['uncertain_calls'],1)
    def test_unknown_policy_model_bound_and_tier_are_not_substituted(self):
        for change in ({'evidence_policy':'v1'},{'model':'some-alias'},
                       {'service_tier':'auto'},{'input_cap':65536},{'input_bound_kind':'character_estimate'}):
            with self.assertRaises(ValueError):config(**change)
    def test_environment_isolation_and_external_export_prohibition(self):
        from evaluation.week4.smoke import clean_environment,run_smoke
        from evaluation.week4.contracts import BoundaryFailure
        with patch.dict(os.environ,{'LANGSMITH_TRACING':'true','LANGCHAIN_TRACING':'true',
                'WEEK4_LANGSMITH_API_KEY':'fixture-only','OTEL_EXPORTER_OTLP_ENDPOINT':'synthetic://not-called'}):
            clean_environment(self.directory)
            self.assertEqual(os.environ['LANGSMITH_TRACING'],'false')
            self.assertEqual(os.environ['OTEL_TRACES_EXPORTER'],'none')
            self.assertNotIn('WEEK4_LANGSMITH_API_KEY',os.environ)
            self.assertNotIn('OTEL_EXPORTER_OTLP_ENDPOINT',os.environ)
        with self.assertRaises(BoundaryFailure):run_smoke({},config(),self.directory/'never',export_traces=True)
    def child(self,scenario,settings=None,seconds=15):
        from evaluation.week4.smoke import supervise
        settings=settings or config();d=self.directory/scenario;d.mkdir()
        Journal.create(d,settings.public())
        case=json.loads((ROOT/'data/week4/report-evidence-v2-1/inference/W4-REAL-016.json').read_text())
        control=supervise(isolated_worker,(case,settings.public(),str(d),'offline-root','offline_test',scenario,True),seconds)
        return d,control
    def test_supervised_mock_transport_actually_selects_v2_and_advisory(self):
        d,c=self.child('v2_mechanics');self.assertEqual(c['terminal'],'exited');self.assertTrue(c['cleanup_verified'])
        r=json.loads((d/'child-result.json').read_text());self.assertEqual(r['evidence_policy'],V2)
        self.assertEqual(r['stage_coverage']['root_cause_analyst'],'completed')
        self.assertEqual(r['terminal_status'],'held');self.assertEqual(r['errors'],[])
        requests=[json.loads(s) for s in (d/'mock-model-requests.jsonl').read_text().splitlines()]
        self.assertEqual(len(requests),3)
        payload=json.loads(requests[2]['messages'][1]['content'].split('\n',1)[1])
        self.assertEqual(payload['analysis_readiness']['version'],V2)
        self.assertTrue(payload['analysis_readiness']['qualified_analysis'])
        self.assertFalse(payload['analysis_readiness']['definitive_confirmation'])
        self.assertEqual(Journal(d).totals(Journal(d).events())['uncertain_calls'],0)
        self.assertFalse((d/'mock-langsmith-requests.jsonl').exists())
    def test_process_timeout_verified_cleanup_retains_real_attempt(self):
        d,c=self.child('timeout',seconds=2)
        self.assertEqual(c['terminal'],'timeout');self.assertTrue(c['cleanup_verified'])
        totals=Journal(d).totals(Journal(d).events());self.assertEqual(totals['attempted_calls'],1)
        self.assertEqual(totals['uncertain_calls'],1)
        with self.assertRaises(ProcessLookupError):os.kill(c['child_pid'],0)
    def test_new_plan_loader_selects_v2_and_rejects_configuration_tampering(self):
        from evaluation.week4.live_cli import load_plan
        from evaluation.week4.runner import metadata,digest
        case=json.loads((ROOT/'data/week4/report-evidence-v2-1/inference/W4-REAL-016.json').read_text())
        settings=config().public()
        plan={'version':'week4-real-016-v2-live-smoke-proposal-2','case':case,'case_sha256':digest(case),
            'config':settings,'configuration_sha256':digest(settings),'evidence_policy':V2,
            'external_tracing':False,'trace_export_authorized':False,'execution_authorized':False,
            'archive_sha256':case['incident']['request_metadata']['report_attribution_v2']['source_sha256'],
            'source_hashes':metadata('proposed-smoke','development-smoke','development-fixtures-1')['source_hashes']}
        path=self.directory/'plan.json';path.write_text(json.dumps(plan))
        _,loaded=load_plan(path);self.assertEqual(loaded.evidence_policy,V2)
        plan['config']['service_tier']='auto';path.write_text(json.dumps(plan))
        with self.assertRaises(ValueError):load_plan(path)

if __name__=='__main__':unittest.main()
