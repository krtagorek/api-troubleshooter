"""Actual live CLI/admission with synthetic authorization and MockTransport only.

The fixture never reads the private project .env. Network is also denied by
the test command's OS sandbox; these receipts are not provider spending.
"""
import copy
from contextlib import redirect_stdout
from dataclasses import replace
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import week4_real_mock_run as offline
from tests.week4.test_case_manifest import make_plan
from tests.week4.test_supervised_v2_provider import mock_only_sdk

ROOT = offline.ROOT
FIXTURE_KEY = 'offline-test-placeholder'


def live_mock_worker(*args):
    """Keep live mode and its guards; replace only the provider transport."""
    assert args[4] == 'live'
    os.environ.clear()
    os.environ['WEEK4_OPENAI_API_KEY'] = FIXTURE_KEY
    from evaluation.week4 import smoke
    from evaluation.week4.sdk_fixtures import block_network, model_transport
    block_network()
    original = smoke.LiveModel

    def model(config, journal, trace, key, *, transport=None):
        assert transport is None and key == FIXTURE_KEY
        assert os.environ['LANGSMITH_TRACING'] == 'false'
        assert os.environ['OTEL_TRACES_EXPORTER'] == 'none'
        return original(config, journal, trace, key,
                        transport=model_transport(args[2], args[5]))

    with patch.object(smoke, 'LiveModel', new=model), \
         patch('openai.OpenAI.__init__', new=mock_only_sdk), \
         patch('langsmith.Client.__init__', side_effect=AssertionError('No exports')), \
         patch('langsmith.AsyncClient.__init__', side_effect=AssertionError('No exports')):
        smoke.inference_worker(*args)


class ManifestLiveGuardControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        offline.clear_environment()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / '.venv-week4-locked')
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        env = patch.dict(os.environ, {'WEEK4_OPENAI_API_KEY': FIXTURE_KEY}, clear=True)
        env.start(); self.addCleanup(env.stop)
        for target in ('socket.socket.connect', 'socket.socket.connect_ex',
                       'socket.getaddrinfo', 'socket.create_connection',
                       'langsmith.Client.__init__', 'langsmith.AsyncClient.__init__'):
            guard = patch(target, side_effect=AssertionError('External operation blocked'))
            guard.start(); self.addCleanup(guard.stop)

    def fixture(self):
        from evaluation.week4.live_cli import authorization_identity
        from evaluation.week4.runner import digest
        # Five total fixture call slots admit only the first case, then prove
        # aggregate admission stops further dispatch. Per-case limit stays five.
        path = make_plan(self.directory, arm='improved', calls=5, budget='2.107440')
        plan = json.loads(path.read_text())
        plan['config']['reviewed_targets'] = True
        plan['configuration_sha256'] = digest(plan['config'])
        plan.update(execution_authorized=True,
                    approval_identity='SYNTHETIC-FIXTURE-NOT-USER-APPROVAL',
                    approval_time='SYNTHETIC-NOT-A-REVIEW-TIMESTAMP')
        plan['approval_binding_sha256'] = authorization_identity(plan)
        path.write_text(json.dumps(plan))
        return path, plan

    def test_live_cli_manifest_treatment_dispatches_only_mock_transport(self):
        from evaluation.week4 import smoke, live_cli
        path, plan = self.fixture()
        output = ROOT / plan['output_path']
        argv = ['week4', 'run-manifest', '--plan', str(path),
                '--output', str(output), '--execute-live']
        with patch.object(smoke, 'inference_worker', new=live_mock_worker), \
             patch.object(sys, 'argv', argv), redirect_stdout(io.StringIO()):
            status = live_cli.main()
        summary = json.loads((output / 'batch-summary.json').read_text())
        first = json.loads((output / 'case-records/000.json').read_text())
        self.assertEqual(status, 1)  # deliberate aggregate fixture budget stop
        self.assertEqual(summary['stop_reason'], 'ResourceFailure')
        self.assertEqual(summary['assigned_cases'], 30)
        self.assertEqual(summary['attempted_cases'], 1)
        self.assertTrue(first['attempted'])
        self.assertEqual(first['mode'], 'live')
        self.assertEqual(first['stage_coverage']['classifier'], 'completed')
        self.assertTrue(first['supervisor']['cleanup_verified'])
        child = output / 'cases' / first['case_id']
        requests = [json.loads(line) for line in
                    (child / 'mock-model-requests.jsonl').read_text().splitlines()]
        self.assertGreater(len(requests), 0)
        self.assertEqual(len(requests), summary['accounting']['attempted_model_calls'])
        self.assertLessEqual(len(requests), 5)
        self.assertTrue(all(r['service_tier'] == 'default' for r in requests))
        self.assertEqual(json.loads((child / 'experiment.json').read_text())['config']['reviewed_targets'], True)
        self.assertEqual(json.loads((child / 'trace-status.json').read_text()), {'status': 'not_requested'})
        self.assertFalse((output / 'cases' / 'W4-REAL-006').exists())
        # Live-mode accounting field names are exercised, but every receipt here
        # is a scripted fixture, never real cost or model-quality evidence.
        self.assertIsNone(summary['semantic_quality'])

    def test_invalid_or_mismatched_manifest_plans_never_dispatch(self):
        from evaluation.week4 import smoke
        from evaluation.week4.live_cli import authorization_identity
        from evaluation.week4.contracts import BoundaryFailure
        path, valid = self.fixture()
        mutations = {
            'unauthorized': lambda p: p.update(execution_authorized=False),
            'approval_mismatch': lambda p: p.update(approval_binding_sha256='0' * 64),
            'code_binding': lambda p: p['source_hashes'].update({'forged.py': '0' * 64}),
            'dataset_binding': lambda p: p.update(dataset_manifest_sha256='0' * 64),
            'configuration_binding': lambda p: p['config'].update(max_calls=4),
            'unsupported_tier': lambda p: p['config'].update(service_tier='priority'),
            'unfunded': lambda p: p['execution'].update(max_usd='0'),
            'exports': lambda p: p.update(trace_export_authorized=True),
            'baseline_mismatch': lambda p: p.update(arm='baseline'),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                plan = copy.deepcopy(valid); mutate(plan)
                if name not in ('unauthorized', 'approval_mismatch'):
                    plan['approval_binding_sha256'] = authorization_identity(plan)
                path.write_text(json.dumps(plan))
                with patch.object(smoke, 'inference_worker', side_effect=AssertionError('No dispatch')):
                    with self.assertRaises((ValueError, BoundaryFailure)):
                        smoke.run_manifest(path, ROOT / plan['output_path'], mode='live', execute_live=True)
                self.assertFalse((ROOT / plan['output_path']).exists())
        path.write_text(json.dumps(valid))
        with self.assertRaises(BoundaryFailure):
            smoke.run_manifest(path, self.directory / 'wrong-output', mode='live', execute_live=True)

    def test_case_configuration_and_frozen_bytes_still_checked(self):
        from evaluation.week4 import smoke
        from evaluation.week4.live_cli import load_plan, authorization_identity
        from evaluation.week4.contracts import load_case_manifest, BoundaryFailure
        path, plan = self.fixture(); _, config = load_plan(path)
        case = load_case_manifest(ROOT / plan['dataset_manifest_path'])[1][0]
        output = ROOT / plan['output_path']; output.mkdir(); (output / 'cases').mkdir()
        (output / 'batch-experiment.json').write_text(json.dumps({
            'plan_identity': authorization_identity(plan), 'mode': 'live'}))
        child = output / 'cases' / case['case_id']
        with patch.object(smoke, 'inference_worker', side_effect=AssertionError('No dispatch')):
            with self.assertRaisesRegex(BoundaryFailure, 'configuration mismatch'):
                smoke.run_smoke(case, replace(config, max_calls=4), child, mode='live',
                                execute_live=True, plan_path=path)
            bad = copy.deepcopy(case); bad['incident']['request_metadata']['forged'] = 'changed'
            with self.assertRaisesRegex(BoundaryFailure, 'frozen input'):
                smoke.run_smoke(bad, config, child, mode='live', execute_live=True, plan_path=path)
            # Matching case but no resource admission is also insufficient.
            with self.assertRaises((BoundaryFailure, FileNotFoundError)):
                smoke.run_smoke(case, config, child, mode='live', execute_live=True, plan_path=path)
        self.assertFalse(child.exists())

    def test_unsupported_legacy_plan_remains_rejected(self):
        from evaluation.week4 import smoke
        from evaluation.week4.live_cli import load_plan
        from evaluation.week4.live_config import CASE016_BUDGET_PROFILE, SELECTION_V1
        from evaluation.week4.contracts import load_case_manifest
        from evaluation.week4.runner import digest
        path, plan = self.fixture(); _, config = load_plan(path)
        case = load_case_manifest(ROOT / plan['dataset_manifest_path'])[1][0]
        legacy = dict(version='week4-smoke-plan-1', case=case, case_sha256=digest(case),
                      source_hashes=plan['source_hashes'], config=config.public())
        legacy['config'].update(budget_profile=CASE016_BUDGET_PROFILE, max_usd='2.25',
                                reviewed_targets=False, selection_policy=SELECTION_V1)
        path.write_text(json.dumps(legacy))
        legacy_config = replace(config, budget_profile=CASE016_BUDGET_PROFILE,
                                max_usd='2.25', reviewed_targets=False)
        with patch.object(smoke, 'inference_worker', side_effect=AssertionError('No dispatch')):
            with self.assertRaisesRegex(ValueError, 'Older plans cannot use'):
                smoke.run_smoke(case, legacy_config, self.directory / 'legacy',
                                mode='live', execute_live=True, plan_path=path)
        self.assertFalse((self.directory / 'legacy').exists())

    def test_actual_selective_env_loader_with_synthetic_file_only(self):
        import dotenv
        tasks = json.loads((ROOT / '.vscode/tasks.json').read_text())['tasks']
        check = next(t for t in tasks if t['label'] == 'Week 4: Check private key presence (NO API calls)')
        live = next(t for t in tasks if 'Run APPROVED final treatment' in t['label'])
        loader = check['args'][1].split("print('Dedicated credential", 1)[0]
        self.assertTrue(live['args'][1].startswith(loader))
        private = self.directory / '.env'
        private.write_text('WEEK4_OPENAI_API_KEY=offline-test-placeholder\n'
                           'OPENAI_API_KEY=unrelated-fixture\nLANGSMITH_API_KEY=unrelated-fixture\n'
                           'LANGSMITH_TRACING=true\nLANGCHAIN_TRACING_V2=true\n'
                           'OTEL_TRACES_EXPORTER=otlp\nUNRELATED_SETTING=${HOME}\n')
        values = dotenv.dotenv_values
        seen = []
        def fixture_values(path, **kwargs):
            self.assertEqual(path, private); self.assertEqual(kwargs, {'interpolate': False})
            seen.append(True)
            return values(path, **kwargs)
        captured = io.StringIO()
        with patch('pathlib.Path.cwd', return_value=self.directory), \
             patch('dotenv.dotenv_values', side_effect=fixture_values), redirect_stdout(captured):
            exec(compile(check['args'][1], '<synthetic-env-loader>', 'exec'), {})
        self.assertEqual(seen, [True])
        self.assertEqual(os.environ['WEEK4_OPENAI_API_KEY'], FIXTURE_KEY)
        for key in ('OPENAI_API_KEY', 'LANGSMITH_API_KEY', 'UNRELATED_SETTING'):
            self.assertNotIn(key, os.environ)
        for key in ('LANGSMITH_TRACING', 'LANGCHAIN_TRACING_V2', 'LANGCHAIN_TRACING', 'LANGSMITH_OTEL_ENABLED'):
            self.assertEqual(os.environ[key], 'false')
        self.assertEqual(os.environ['OTEL_TRACES_EXPORTER'], 'none')
        self.assertEqual(os.environ['OTEL_SDK_DISABLED'], 'true')
        self.assertNotIn(FIXTURE_KEY, captured.getvalue())
        self.assertNotIn('unrelated-fixture', captured.getvalue())


if __name__ == '__main__':
    unittest.main()
