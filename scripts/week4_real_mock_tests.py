"""Synthetic calibration and guard checks only; real14 execution is separate."""
import copy
import json
from pathlib import Path
import socket
import tempfile
import unittest
from scripts import week4_real_mock_run as runner

class MechanicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        runner.clear_environment();cls.guard_context=runner.offline_guard();cls.guard=cls.guard_context.__enter__()
    @classmethod
    def tearDownClass(cls):cls.guard_context.__exit__(None,None,None)
    def setUp(self):
        root=runner.ROOT/'.venv-week4-py311'/'real-mock-test-artifacts';root.mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=root);self.addCleanup(self.temp.cleanup)
        self.directory=Path(self.temp.name)
        from evaluation.week4.fixtures import development_cases
        self.synthetic=development_cases()[0]
        self.synthetic['case_id']='SYNTHETIC-MECHANICS-ONLY'
    def child(self,name,scenario='normal',timeout=10):
        from evaluation.week4.smoke import supervise
        path=self.directory/name;path.mkdir()
        control=supervise(runner.worker,(copy.deepcopy(self.synthetic),str(path),'SYNTHETIC-UNIT-PROBE',scenario),timeout)
        result=json.loads((path/'result.json').read_text()) if (path/'result.json').exists() else None
        return path,control,result

    def test_preflight_exact_eligible_assets_and_goals(self):
        pre,inputs=runner.preflight()
        self.assertEqual(tuple(sorted(inputs)),runner.EXPECTED)
        self.assertEqual(pre['baseline']['checked'],328)
        self.assertEqual(len(pre['excluded_ids']),6)
        self.assertIn('W4-REAL-007',pre['excluded_ids'])
        self.assertIn('intent is unspecified',inputs['W4-REAL-020']['incident']['expected_behavior'])
        self.assertIn('informative rejection',inputs['W4-REAL-013']['incident']['expected_behavior'])
        self.assertEqual(pre['asset_hashes'],runner.fingerprint())
        self.assertTrue(all(not goal['newly_approved'] for goal in pre['goals'].values()))

    def test_real_adapter_factories_and_actual_callback_path_synthetic(self):
        path,control,result=self.child('synthetic-graph')
        self.assertTrue(control['cleanup_verified']);self.assertEqual(control['terminal'],'exited')
        self.assertEqual(result['terminal_status'],'held')
        self.assertEqual(result['actual_ordered_graph_path'],['initialize','classifier','log_investigator','root_cause_analyst','request_user_input'])
        self.assertEqual(result['usage']['model_calls'],3)
        self.assertTrue(all(result['span_structure'].values()))
        self.assertTrue(result['input_preservation']['supplied_vs_initial_graph_input'])
        self.assertEqual(result['grounding']['invalid'],[])
        self.assertTrue(all(result['security'][k]==0 for k in result['security']))
        self.assertTrue(all(h['correct_case'] for h in result['selected_handle_checks']))
        self.assertTrue(result['final_contract']['state_valid'])
        self.assertEqual(result['output']['validation_results'],[])
        self.assertIsNone(result['semantic_quality']);self.assertIsNone(result['usage_priced_cost_usd'])
        self.assertTrue(result['actual_router_returns'])
        self.assertFalse(any(s['kind']=='tool' for s in json.loads((path/'spans.json').read_text())['spans']))

    def test_deterministic_model_outputs_and_trace_parentage(self):
        a,_,ra=self.child('deterministic-a');b,_,rb=self.child('deterministic-b')
        ca=json.loads((a/'model-calls.json').read_text())['calls'];cb=json.loads((b/'model-calls.json').read_text())['calls']
        self.assertEqual([c['response'] for c in ca],[c['response'] for c in cb])
        self.assertEqual([c['messages'] for c in ca],[c['messages'] for c in cb])
        self.assertTrue(all(c['source']=='mock_test_data' for c in ca))
        self.assertEqual(ra['output'],rb['output'])

    def test_failed_case_then_subsequent_safe_synthetic_case(self):
        _,first,failed=self.child('failure','failure')
        _,second,success=self.child('subsequent')
        self.assertTrue(first['cleanup_verified']);self.assertTrue(second['cleanup_verified'])
        self.assertEqual(failed['terminal_status'],'failed');self.assertEqual(failed['usage']['model_calls'],1)
        self.assertEqual(success['terminal_status'],'held')

    def test_process_timeout_and_verified_cleanup(self):
        _,control,result=self.child('timeout','timeout',timeout=1)
        self.assertEqual(control['terminal'],'timeout');self.assertTrue(control['cleanup_verified'])
        self.assertIsNone(result)
        import os
        with self.assertRaises(ProcessLookupError):os.kill(control['child_pid'],0)

    def test_guard_denies_network_clients_and_commands_without_execution(self):
        import os,openai
        with runner.offline_guard(worker=True) as counts:
            with socket.socket() as sock:
                with self.assertRaises(RuntimeError):sock.connect(('127.0.0.1',1))
            with self.assertRaises(RuntimeError):openai.OpenAI(api_key='SYNTHETIC-NOT-A-CREDENTIAL')
            with self.assertRaises(RuntimeError):os.system('SYNTHETIC COMMAND MUST NOT EXECUTE')
        self.assertEqual(counts,{'network_attempts_blocked':1,'sdk_initializations_blocked':1,'command_attempts_blocked':1})

    def test_read_only_finalization_and_immutable_artifacts(self):
        path=self.directory/'final';path.mkdir();runner.write(path/'result.json',{'mocked':True})
        runner.finalize(path)
        self.assertEqual(path.stat().st_mode&0o222,0)
        self.assertEqual((path/'result.json').stat().st_mode&0o222,0)
        self.assertIn('result.json',json.loads((path/'artifact-hashes.json').read_text()))

if __name__=='__main__':unittest.main()
