"""Only mocked provider and LangSmith transports; external sockets prohibited."""
import json
import copy
import os
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch
from evaluation.week4.runner import ROOT
from evaluation.week4.fixtures import development_cases
from evaluation.week4.live_config import LiveConfig
from evaluation.week4.smoke import run_smoke, supervise, export_worker
from evaluation.week4.accounting import Journal
from evaluation.week4.contracts import AccountingFailure


def fixture_config(**kwargs):
    # Arbitrary test rates, never proposed/current model pricing.
    return LiveConfig(model='offline-sdk-fixture', input_per_million='1', output_per_million='2',
                      pricing_source='https://example.invalid/TEST-ONLY', pricing_verified_at='TEST-ONLY',
                      **kwargs)


class LiveSDKTests(unittest.TestCase):
    def setUp(self):
        self.patches = [patch.object(socket.socket,'connect', side_effect=AssertionError('Network blocked')),
                        patch.object(socket,'getaddrinfo', side_effect=AssertionError('Network blocked'))]
        for p in self.patches: p.start(); self.addCleanup(p.stop)
        base = ROOT/'.venv-week4-py311'/'sdk-test-artifacts'
        base.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.tmp.cleanup)
        self.case = development_cases()[0]

    def run_case(self, scenario='hold', config=None, **kwargs):
        path = Path(self.tmp.name)/scenario
        result, trace = run_smoke(self.case, config or fixture_config(), path, scenario=scenario, **kwargs)
        return result, trace, path

    def test_success_all_five_sdk_calls_and_trace_retrieval(self):
        result, trace, path = self.run_case('full', export_traces=True, project='week4-offline-test')
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['accounting']['attempted_calls'],5)
        self.assertEqual(result['accounting']['usage_received_calls'],5)
        self.assertEqual(result['accounting']['uncertain_calls'],0)
        self.assertTrue(result['supervisor']['cleanup_verified'])
        self.assertGreaterEqual(result['elapsed_seconds'],result['model_elapsed_seconds'])
        self.assertEqual(trace['status'],'verified')
        spans = json.loads((path/'spans.json').read_text())
        self.assertEqual(len([s for s in spans if s['kind']=='root']),1)
        self.assertEqual(len([s for s in spans if s['kind']=='model']),5)
        self.assertFalse(any(s['kind']=='tool' for s in spans))
        self.assertEqual(trace['matched_spans'],11)
        smith_requests=[json.loads(line) for line in (path/'mock-langsmith-requests.jsonl').read_text().splitlines()]
        model_posts=[r['body'] for r in smith_requests if r['method']=='POST' and r['body'].get('run_type')=='llm']
        self.assertEqual(len(model_posts),5)
        self.assertTrue(all(b['prompt_tokens']==11 and b['completion_tokens']==7 for b in model_posts))
        self.assertTrue(all(b['extra']['metadata']['usage_counts']['input_units']==11 for b in model_posts))
        self.assertEqual(result['output']['validation_results'][-1]['status'],'NOT_TESTED')
        requests = [json.loads(x) for x in (path/'mock-model-requests.jsonl').read_text().splitlines()]
        self.assertTrue(all(r['response_format']['json_schema']['strict'] for r in requests))
        self.assertNotIn('expected_resolution',json.dumps(requests))
        self.assertIsNone(json.loads((path/'review.json').read_text())['reviewer'])

    def test_parsing_rejection_keeps_received_usage(self):
        result, _, path = self.run_case('parsing')
        self.assertEqual(result['terminal_status'],'failed')
        self.assertEqual(result['accounting']['attempted_calls'],1)
        self.assertEqual(result['accounting']['usage_received_calls'],1)
        self.assertEqual(result['accounting']['uncertain_calls'],0)
        self.assertEqual(result['accounting']['known_cost_usd'],'0.000025')
        self.assertIn('schema_rejection',result['errors'])
        self.assertLess([e['event'] for e in Journal(path).events()].index('usage'),
                        [e['event'] for e in Journal(path).events()].index('call_error'))

    def test_missing_usage_is_unknown_and_retains_reservation(self):
        result, _, path = self.run_case('missing_usage')
        self.assertEqual(result['accounting']['attempted_calls'],1)
        self.assertEqual(result['accounting']['uncertain_calls'],1)
        self.assertIsNone(result['accounting']['usage_priced_cost_usd'])
        self.assertEqual(result['accounting']['retained_reservations_usd'],'0.03584')
        self.assertEqual(len((path/'mock-model-requests.jsonl').read_text().splitlines()),1)

    def test_interrupted_child_has_one_real_attempt_and_verified_cleanup(self):
        result, _, path = self.run_case('interrupt')
        self.assertEqual(result['terminal_status'],'interrupted')
        self.assertTrue(result['supervisor']['cleanup_verified'])
        self.assertEqual(result['accounting']['attempted_calls'],1)
        self.assertEqual(result['accounting']['uncertain_calls'],1)
        self.assertIsNone(result['model_elapsed_seconds'])
        spans = json.loads((path/'spans.json').read_text())
        self.assertEqual(len([s for s in spans if s['kind']=='model']),1)
        self.assertTrue(all(s['status']=='interrupted' for s in spans))

    def test_process_timeout_terminates_blocked_transport(self):
        result, _, path = self.run_case('timeout',fixture_config(case_timeout_seconds=2))
        self.assertEqual(result['terminal_status'],'timeout')
        self.assertTrue(result['supervisor']['cleanup_verified'])
        self.assertEqual(result['accounting']['attempted_calls'],1)
        self.assertEqual(result['accounting']['uncertain_calls'],1)
        with self.assertRaises(ProcessLookupError): os.kill(result['supervisor']['child_pid'],0)

    def test_trace_failure_never_repeats_inference(self):
        result, trace, path = self.run_case('trace_failure',export_traces=True,project='week4-offline-test')
        self.assertEqual(result['accounting']['attempted_calls'],2)
        self.assertEqual(trace['status'],'TRACE_EXPORT_FAILED')
        self.assertEqual(len((path/'mock-model-requests.jsonl').read_text().splitlines()),2)

    def test_trace_retrieval_mismatch_is_failure(self):
        _, trace, _ = self.run_case('trace_mismatch',export_traces=True,project='week4-offline-test')
        self.assertEqual(trace['status'],'TRACE_EXPORT_FAILED')

    def test_tracing_parity_with_ambient_tracing_enabled(self):
        results=[]; requests=[]
        with patch.dict(os.environ,{'LANGSMITH_TRACING':'true','OPENAI_API_KEY':'must-not-be-used'}):
            for enabled in (False,True):
                path = Path(self.tmp.name)/str(enabled)
                result,_ = run_smoke(self.case,fixture_config(),path,trace_enabled=enabled)
                output=result['output']; output.pop('thread_id')
                results.append(output)
                requests.append((path/'mock-model-requests.jsonl').read_text())
        self.assertEqual(requests[0],requests[1])
        self.assertEqual(results[0],results[1])
        self.assertFalse((Path(self.tmp.name)/'False'/'mock-langsmith-requests.jsonl').exists())

    def test_caps_before_dispatch_and_live_mode_guard(self):
        result, _, path = self.run_case('money-cap',fixture_config(max_usd='0.01'))
        self.assertEqual(result['accounting']['attempted_calls'],0)
        self.assertFalse((path/'mock-model-requests.jsonl').exists())
        self.assertFalse(any(s['kind']=='model' for s in json.loads((path/'spans.json').read_text())))
        result,_,path = self.run_case('call-cap',fixture_config(max_calls=1))
        self.assertEqual(result['accounting']['attempted_calls'],1)
        with self.assertRaises(PermissionError):
            run_smoke(self.case,fixture_config(),Path(self.tmp.name)/'live',mode='live')

    def test_transport_failure_is_one_attempt_not_zero_usage(self):
        result,_,path=self.run_case('transport_error')
        self.assertEqual(result['accounting']['attempted_calls'],1)
        self.assertEqual(result['accounting']['uncertain_calls'],1)
        self.assertIsNone(result['accounting']['usage_priced_cost_usd'])
        self.assertEqual(len((path/'mock-model-requests.jsonl').read_text().splitlines()),1)

    def test_overrun_is_recorded_without_hiding_observed_cost(self):
        result,_,path=self.run_case('overrun')
        self.assertEqual(result['accounting']['attempted_calls'],1)
        self.assertEqual(result['accounting']['limit_violations'],1)
        self.assertEqual(result['accounting']['known_cost_usd'],'1.000014')
        self.assertEqual(result['terminal_status'],'failed')

    def test_sdk_trace_and_provider_inputs_are_sanitized(self):
        self.case=copy.deepcopy(self.case)
        self.case['incident']['request_metadata']['Authorization']='Bearer fixture-secret-value'
        result,trace,path=self.run_case('redaction',export_traces=True,project='week4-offline-test')
        self.assertEqual(trace['status'],'verified')
        for name in ('mock-model-requests.jsonl','mock-langsmith-requests.jsonl','spans.json'):
            text=(path/name).read_text()
            self.assertNotIn('fixture-secret-value',text)
            self.assertNotIn('expected_resolution',text)
        self.assertEqual(result['accounting']['attempted_calls'],2)

    def test_swallowed_validator_rejection_marks_root_failed(self):
        result,_,path=self.run_case('validator_parsing')
        self.assertIn('schema_rejection',result['errors'])
        self.assertEqual(result['accounting']['attempted_calls'],5)
        root=next(s for s in json.loads((path/'spans.json').read_text()) if s['kind']=='root')
        self.assertEqual(root['status'],'failed')

    def test_trace_only_recovery_has_no_inference_path(self):
        result,_,source=self.run_case('hold')
        destination=Path(self.tmp.name)/'trace-only';destination.mkdir()
        run_id=json.loads((source/'experiment.json').read_text())['run_id']
        supervisor=supervise(export_worker,(str(destination),'offline_test','hold','week4-offline-test',
            run_id,'https://api.smith.langchain.com',None,str(source),False),30)
        self.assertTrue(supervisor['cleanup_verified'])
        report=json.loads((destination/'export-result.json').read_text())
        self.assertEqual(report['status'],'verified')
        self.assertFalse((destination/'mock-model-requests.jsonl').exists())
        self.assertEqual(len((source/'mock-model-requests.jsonl').read_text().splitlines()),2)

    def test_proposal_keeps_selection_and_human_review_unresolved(self):
        from evaluation.week4.live_cli import prepare_plan,load_plan
        plan=prepare_plan()
        for name in ('model','input_per_million','output_per_million','pricing_source','pricing_verified_at'):
            self.assertIsNone(plan['config'][name])
        self.assertIsNone(plan['human_review']['confirmed'])
        self.assertEqual(plan['config']['max_usd'],'0.25')
        self.assertEqual(plan['execution']['retries'],0)
        path=Path(self.tmp.name)/'proposal.json';path.write_text(json.dumps(plan))
        with self.assertRaises(ValueError):load_plan(path)

    def test_torn_journal_fails_closed(self):
        path = Path(self.tmp.name)/'torn';path.mkdir()
        journal = Journal.create(path,fixture_config().public())
        with journal.path.open('a') as f:f.write('{')
        with self.assertRaises(AccountingFailure): journal.events()

if __name__=='__main__': unittest.main()
