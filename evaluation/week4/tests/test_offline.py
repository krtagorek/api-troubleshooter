import copy
import json
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import httpx
from pydantic import ValidationError
from evaluation.week4.contracts import InferenceCase, EvaluatorReference, BoundaryFailure
from evaluation.week4.fixtures import development_cases, mock_reply, full_path_reply
from evaluation.week4.runner import run_batch, run_case, ROOT
from evaluation.week4.tracing import FakeTracingSink
from evaluation.week4.grading import structural_checks, worksheet, quality_denominators, grounding_checks

class OfflineTests(unittest.TestCase):
    def setUp(self):
        # No test is allowed to open sockets, including accidental service/SDK access.
        self.network = patch.object(socket.socket, 'connect', side_effect=AssertionError('Network prohibited'))
        self.network.start()
        self.addCleanup(self.network.stop)
        local_tmp = ROOT/'.venv-week4-py311'/'test-artifacts'
        local_tmp.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=local_tmp)
        self.addCleanup(self.tmp.cleanup)
        self.cases = development_cases()

    def batch(self, cases=None, reply=mock_reply, sink=None, **kwargs):
        return run_batch(cases or self.cases, Path(self.tmp.name)/'run', experiment='test-1',
                         reply_factory=lambda case: reply, sink=sink, **kwargs)

    def test_real_graph_factories_and_span_receipts(self):
        result, spans, receipts, fatal = run_case(InferenceCase.model_validate(self.cases[0]), 'trace', mock_reply, FakeTracingSink())
        self.assertIsNone(fatal)
        self.assertEqual(result.terminal_status, 'held')
        self.assertEqual(result.workflow_status, 'awaiting_evidence')
        self.assertEqual(result.stage_coverage['classifier'], 'completed')
        self.assertEqual(result.stage_coverage['log_investigator'], 'completed')
        self.assertEqual(result.stage_coverage['root_cause_analyst'], 'not_reached')
        self.assertEqual(result.usage.model_calls, 2)
        self.assertEqual(result.usage.input_tokens, 22)
        self.assertIsNone(result.usage.usage_priced_cost_usd)
        self.assertTrue(all(structural_checks(result, spans, receipts).values()))
        self.assertEqual([s['kind'] for s in spans], ['root', 'node', 'model', 'node', 'model'])
        self.assertFalse(any(s['kind'] == 'tool' for s in spans))
        self.assertGreaterEqual(result.elapsed_seconds, result.model_elapsed_seconds)
        nodes = {s['span_id']: s for s in spans if s['kind'] == 'node'}
        for span in spans:
            if span['kind'] == 'model':
                self.assertIn(span['parent_id'], nodes)

    def test_all_five_real_factories_and_no_validation_tool(self):
        result, spans, receipts, fatal = run_case(InferenceCase.model_validate(self.cases[0]), 'full', full_path_reply)
        self.assertIsNone(fatal)
        self.assertEqual(set(result.stage_coverage.values()), {'completed'})
        self.assertEqual(result.usage.model_calls, 5)
        self.assertTrue(all(structural_checks(result, spans, receipts).values()))
        self.assertEqual(result.output['validation_results'][-1]['status'], 'NOT_TESTED')
        self.assertFalse(any(s['kind'] == 'tool' for s in spans))
        checks = grounding_checks(result)
        self.assertGreater(checks['checked'], 0)
        self.assertEqual(checks['invalid'], [])
        tampered = result.model_copy(deep=True)
        tampered.output['evidence']['items'][0]['observation'] = 'invented evidence'
        self.assertTrue(grounding_checks(tampered)['invalid'])

    def test_traced_untraced_request_output_parity_and_no_labels(self):
        captures = [[], []]
        outputs = []
        for i, sink in enumerate((None, FakeTracingSink())):
            def reply(req):
                captures[i].append(req)
                return mock_reply(req)
            result, spans, receipts, fatal = run_case(InferenceCase.model_validate(self.cases[0]), 'same', reply, sink, trace_enabled=bool(i))
            self.assertEqual(bool(spans), bool(i))
            outputs.append(result)
        self.assertEqual(captures[0], captures[1])
        self.assertEqual(outputs[0].output, outputs[1].output)
        text = json.dumps(captures)
        for forbidden in ('expected_resolution', 'expected_answer', 'reviewer', 'rubric', 'semantic_labels'):
            self.assertNotIn('"'+forbidden+'"', text)

    def test_case_schema_errors_continue_and_denominators_keep_failures(self):
        bad = copy.deepcopy(self.cases[0]); bad['incident']['status_code'] = 'wrong'
        bad['case_id'] = 'bad-schema'
        results, summary = self.batch([bad, self.cases[1]])
        self.assertEqual([r['terminal_status'] for r in results], ['failed', 'held'])
        self.assertEqual(summary['assigned'], 2)
        self.assertEqual(summary['failed'], 1)
        refs = [EvaluatorReference(case_id=r['case_id'], dataset_version='dev') for r in results]
        self.assertEqual(quality_denominators(results, refs)['assigned'], 2)
        self.assertEqual(quality_denominators(results, refs)['unreviewed_sufficiency'], 2)

    def test_model_failure_kinds_continue(self):
        for kind in ('schema', 'refusal', 'grounding', 'timeout', 'application'):
            with self.subTest(kind=kind):
                path = Path(self.tmp.name)/kind
                first = True
                def reply(req):
                    nonlocal first
                    if not first: return mock_reply(req)
                    first = False
                    if kind == 'schema': return {'output': {}}
                    if kind == 'refusal': return {'refusal': 'Offline simulated refusal'}
                    if kind == 'timeout': return httpx.ReadTimeout('mock')
                    if kind == 'application': return ValueError('offline fixture error')
                    return {'output': {'classification': {'category': 'authentication', 'confidence': 0.5,
                        'reasoning': 'Scripted invalid reference', 'evidence_references': ['/not-present']}}}
                rows, summary = run_batch(self.cases, path, experiment=kind, reply_factory=lambda c: reply)
                self.assertEqual([r['terminal_status'] for r in rows], ['failed', 'held'])
                self.assertEqual(summary['assigned'], 2)
                self.assertIsNone(summary['stop_reason'])
                self.assertTrue(rows[0]['errors'])

    def test_label_leak_stops_before_model_and_marks_rest(self):
        bad = copy.deepcopy(self.cases[0]); bad['incident']['logs'][0]['expected_answer'] = 'do-not-send'
        rows, summary = self.batch([bad, self.cases[1]])
        self.assertEqual([r['terminal_status'] for r in rows], ['batch_stopped', 'unattempted'])
        self.assertEqual(summary['mock_model_calls'], 0)
        self.assertNotIn('do-not-send', ''.join(p.read_text() for p in (Path(self.tmp.name)/'run').glob('*.json')))
        with self.assertRaises(BoundaryFailure): InferenceCase.model_validate(bad)

    def test_reference_fields_rejected_in_nested_inference(self):
        for key in EvaluatorReference.model_fields:
            if key == 'case_id': continue
            raw = copy.deepcopy(self.cases[0])
            raw['incident']['request_metadata'][key] = 'evaluator-only-sentinel'
            with self.subTest(key=key), self.assertRaises(BoundaryFailure):
                InferenceCase.model_validate(raw)

    def test_missing_usage_stops_bounded_accounting(self):
        def reply(req): return {**mock_reply(req), 'usage': None}
        rows, summary = self.batch(reply=reply)
        self.assertEqual(rows[0]['terminal_status'], 'batch_stopped')
        self.assertEqual(rows[1]['terminal_status'], 'unattempted')
        self.assertFalse(rows[0]['usage']['complete'])

    def test_trace_delivery_failure_does_not_repeat_or_stop_safe_cases(self):
        rows, summary = self.batch(sink=FakeTracingSink(fail=True))
        self.assertEqual(summary['mock_model_calls'], 4)
        self.assertEqual([r['trace_status'] for r in rows], ['TRACE_DELIVERY_FAILED']*2)
        self.assertIsNone(summary['stop_reason'])

    def test_swallowed_validator_failure_is_still_failed(self):
        def reply(req):
            if req['response_format']['json_schema']['name'] == 'ValidatorOutput':
                return {'output': {}}
            return full_path_reply(req)
        result, spans, receipts, fatal = run_case(InferenceCase.model_validate(self.cases[0]), 'validator-error', reply)
        self.assertIsNone(fatal)
        self.assertEqual(result.stage_coverage['validator'], 'completed')
        self.assertIn('schema_rejection', result.errors)
        self.assertEqual(result.terminal_status, 'failed')
        self.assertEqual(result.usage.model_calls, 5)
        self.assertEqual(result.usage.input_tokens, 55)

    def test_security_failure_in_transport_stops(self):
        def reply(req): raise BoundaryFailure('Mock isolation failure')
        rows, summary = self.batch(reply=reply)
        self.assertEqual(rows[0]['terminal_status'], 'batch_stopped')
        self.assertEqual(rows[1]['terminal_status'], 'unattempted')
        self.assertEqual(summary['stop_reason'], 'BoundaryFailure')

    def test_oversized_usage_stops(self):
        def reply(req): return {**mock_reply(req), 'usage': {'prompt_tokens': 999999, 'completion_tokens': 7, 'total_tokens': 1000006}}
        rows, summary = self.batch(reply=reply)
        self.assertEqual(rows[0]['terminal_status'], 'batch_stopped')
        self.assertEqual(rows[1]['terminal_status'], 'unattempted')

    def test_output_isolation(self):
        with self.assertRaises(BoundaryFailure):
            run_batch([], Path('/outside-week4'), experiment='blocked', reply_factory=lambda c: mock_reply)

    def test_create_only_versions_and_review_stays_empty(self):
        rows, summary = self.batch()
        with self.assertRaises(FileExistsError): self.batch()
        path = Path(self.tmp.name)/'run'
        self.assertTrue((path/'artifact-hashes.json').exists())
        self.assertEqual(path.stat().st_mode & 0o222, 0)
        self.assertEqual((path/'summary.json').stat().st_mode & 0o222, 0)
        meta = json.loads((path/'experiment.json').read_text())
        self.assertEqual(meta['mode'], 'offline_mock')
        self.assertTrue(meta['source_hashes'])
        sheet = worksheet(rows[0]['case_id'], 'dev', rows[0]['root_id'])
        for key in ('reviewer', 'reviewed_at', 'confirmed', 'diagnostic_correctness'):
            self.assertIsNone(sheet[key])

    def test_resource_ceiling_stops_and_no_fake_children(self):
        rows, summary = self.batch(max_cases=1)
        self.assertEqual(rows[1]['terminal_status'], 'batch_stopped')
        self.assertEqual(summary['mock_model_calls'], 2)

if __name__ == '__main__': unittest.main()
