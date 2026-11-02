"""Portable input-contract tests only. No graph, agents, SDKs or network execution."""
import copy
import csv
import hashlib
import json
from pathlib import Path
import socket
import sys
import tempfile
import unittest
from unittest.mock import patch
from pydantic import ValidationError
from models.incident import Incident
from evaluation.week4.contracts import InferenceCase, BoundaryFailure
from scripts import week4_reviewed_compatibility as audit


def synthetic_contract_input():
    """Wholly invented schema fixture, never copied into any reviewed incident."""
    return {'incident_id':'SYNTHETIC-CONTRACT-ONLY','service':'SYNTHETIC-CONTRACT-ONLY',
        'endpoint':'/synthetic-contract-only','http_method':'GET','status_code':200,
        'expected_behavior':'Synthetic input validation only; not an incident expectation.',
        'actual_behavior':'Wholly invented contract fixture; not a reported incident.'}


def constraint_report():
    results=[]
    for field in ('status_code','http_method','endpoint','expected_behavior'):
        for variant in ('missing','null'):
            raw=synthetic_contract_input()
            if variant=='missing':del raw[field]
            else:raw[field]=None
            try:Incident.model_validate(raw)
            except ValidationError as exc:
                results.append({'field':field,'test_input':variant,'result':'REJECTED',
                                'safe_errors':audit.safe_errors(exc)})
            else:raise AssertionError('Required null/missing field unexpectedly accepted')
    for field,value in [('endpoint',''),('expected_behavior',''),('http_method','UNKNOWN'),
                        ('status_code',99),('status_code',600),('status_code','302')]:
        raw=synthetic_contract_input();raw[field]=value
        try:Incident.model_validate(raw)
        except ValidationError as exc:
            results.append({'field':field,'test_input':value,'result':'REJECTED','safe_errors':audit.safe_errors(exc)})
        else:raise AssertionError('Invalid contract value unexpectedly accepted')
    return {'fixture_kind':'WHOLLY_SYNTHETIC_CONTRACT_TEST_NOT_A_REAL_INCIDENT',
            'tests':results,'real_candidates_constructed_with_fillers':False,
            'agent_graph_executed':False,'models_executed':False}


class ReviewedCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patches=[patch.object(socket.socket,'connect',side_effect=AssertionError('Network denied')),
                     patch.object(socket.socket,'connect_ex',side_effect=AssertionError('Network denied')),
                     patch.object(socket,'getaddrinfo',side_effect=AssertionError('Network denied')),
                     patch.object(socket,'create_connection',side_effect=AssertionError('Network denied'))]
        for p in cls.patches:p.start()
        cls.raw=json.loads((audit.DEST/'real-incidents-v2.json').read_text())
    @classmethod
    def tearDownClass(cls):
        for p in reversed(cls.patches):p.stop()

    def test_source_bytes_and_five_authorized_reviews(self):
        source=(audit.SOURCE/'api-incident-reviewed-v2.json').read_bytes()
        imported=(audit.DEST/'real-incidents-v2.json').read_bytes()
        self.assertEqual(source,imported)
        self.assertEqual(audit.sha(imported),'f3eb5764d834b6a65e4a54dfad61426fdeb08adc41bbe73e5ed703b8e826af28')
        audit.verify_sources(self.raw,(audit.SOURCE/'api-incident-reviewed-v2.html').read_text())
        for c in self.raw['cases']:
            self.assertEqual(c['human_review']['decision'],audit.DECISIONS[c['id']])
            self.assertIsNone(c['human_review']['reviewed_at'])
            self.assertIsNone(c['human_review']['semantic_scores'])
            self.assertFalse(c['runtime_ready'])
        provenance=json.loads((audit.DEST/'import-provenance.json').read_text())
        self.assertIsNone(provenance['confirmation_at'])
        self.assertEqual(provenance['source_recorded_at'],'2026-10-28T23:39:03Z')
        self.assertNotEqual(provenance['source_recorded_at'],provenance['imported_at'])

    def test_blocked_cases_are_not_constructed_or_projected(self):
        results,projections=audit.assess(self.raw['cases'])
        self.assertEqual([r['status'] for r in results],['BLOCKED']*4+['INPUT_COMPATIBLE_NOT_EXECUTED'])
        self.assertEqual(set(projections),{'W4-REAL-005'})
        self.assertEqual(sorted(p.stem for p in (audit.DEST/'inference').glob('*.json')),['W4-REAL-005'])
        for result in results[:4]:
            self.assertEqual(result['checks']['initialization'],'NOT_CHECKED_BLOCKED')
            self.assertIsNone(result['sanitization_changes'])

    def test_actual_required_constraints_with_synthetic_only_fixture(self):
        report=constraint_report()
        self.assertEqual(len(report['tests']),14)
        self.assertTrue(all(t['result']=='REJECTED' for t in report['tests']))
        self.assertTrue(all('input' not in e for t in report['tests'] for e in t['safe_errors']))
        self.assertFalse(report['real_candidates_constructed_with_fillers'])

    def test_005_observed_path_status_and_hint_separate_no_host(self):
        case=self.raw['cases'][4]
        projection=audit.proposal_005(case)
        runtime=InferenceCase.model_validate(projection)
        self.assertEqual(runtime.incident.http_method,'GET')
        self.assertEqual(runtime.incident.status_code,302)
        self.assertEqual(runtime.incident.endpoint,'/')
        self.assertEqual(runtime.incident.service,'HTTP endpoint (identity omitted)')
        self.assertIn('error_status_hint=400',runtime.incident.actual_behavior)
        self.assertIn('HTTPS port 4433',runtime.incident.actual_behavior)
        self.assertEqual(runtime.incident.logs,[])
        self.assertEqual(runtime.incident.request_metadata,{})
        self.assertIsNone(runtime.incident.response_body)
        self.assertEqual(runtime.incident.severity,'unknown')
        self.assertNotIn('https://',runtime.incident.endpoint)

    def test_sanitization_initialization_catalog_and_label_separation(self):
        from tools.redaction import redact
        from graph.state import initialize_state
        from tools.evidence_catalog import build_catalog,handle_catalog
        case=self.raw['cases'][4]
        proposed=audit.proposal_005(case)
        runtime=InferenceCase.model_validate(proposed)
        normalized=runtime.model_dump(mode='json')
        self.assertEqual(redact(normalized),normalized)
        for field,value in proposed['incident'].items():self.assertEqual(value,normalized['incident'][field])
        state=initialize_state(runtime.incident,'synthetic-contract-check-thread-only',max_retries=0)
        catalog=build_catalog(state['sanitized_inputs'])
        self.assertEqual(len(catalog),len(handle_catalog(state['sanitized_inputs'])['evidence_catalog']))
        actual=next(e for e in catalog.values() if e.reference=='/actual_behavior')
        self.assertEqual(actual.source,'user')
        self.assertIn('h11.RemoteProtocolError',actual.observation)
        self.assertIn('error_status_hint=400',actual.observation)
        self.assertFalse(any(e.reference.startswith('/logs/') for e in catalog.values()))
        text=json.dumps(normalized)
        for field in ('accepted_expected_behavior','proposed_review','human_review','source_url','source_date','family','scope'):
            self.assertNotIn('"'+field+'"',text)
        self.assertNotIn('missing/malformed chunked response framing',text)
        self.assertNotIn(case['accepted_expected_behavior'],text)
        self.assertIn('Reporter states curl works.',runtime.incident.actual_behavior)
        contaminated=copy.deepcopy(proposed)
        contaminated['incident'].setdefault('request_metadata',{})['expected_answer']='evaluator-only-sentinel'
        with self.assertRaises(BoundaryFailure):InferenceCase.model_validate(contaminated)

    def test_inventory_preserves_215_original_rows_and_exact_ids(self):
        path=audit.ROOT/'data/week4/candidate-inventory.csv';data=path.read_bytes()
        report=json.loads((audit.DEST/'inventory-update.json').read_text())
        # Old inventory has one physical line per record; verify its exact prefix hash.
        prefix=b''.join(data.splitlines(keepends=True)[:216])
        self.assertEqual(hashlib.sha256(prefix).hexdigest(),report['before_sha256'])
        with path.open(newline='') as f:rows=list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows),220)
        self.assertEqual(len({r['case_id'] for r in rows}),len(rows))
        for ident,decision in audit.DECISIONS.items():
            matched=[r for r in rows if r['case_id']==ident]
            self.assertEqual(len(matched),1)
            self.assertEqual(matched[0]['review_status'],decision)
        self.assertEqual(hashlib.sha256(audit.inventory_prefix(data,220)).hexdigest(),report['after_sha256'])

    def test_existing_different_destination_not_overwritten(self):
        base=audit.ROOT/'.venv-week4-py311'/'review-import-tests';base.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as temp:
            path=Path(temp)/'source.json';path.write_bytes(b'original')
            self.assertEqual(audit.write_identical_or_new(path,b'original'),'verified_identical')
            with self.assertRaises(ValueError):audit.write_identical_or_new(path,b'different')
            self.assertEqual(path.read_bytes(),b'original')

    def test_baseline_and_synthetic_smoke_proposal_unchanged(self):
        manifest=json.loads((audit.ROOT/'docs/source-baseline-manifest.json').read_text())
        self.assertEqual(len(manifest['files']),328)
        for entry in manifest['files']:
            data=(audit.ROOT/entry['destination_relative_path']).read_bytes()
            self.assertEqual(len(data),entry['bytes'])
            self.assertEqual(audit.sha(data),entry['sha256'])
        plan=json.loads((audit.ROOT/'data/week4/smoke-plan.json').read_text())
        self.assertEqual(plan['case']['case_id'],'W4-DEV-1')
        self.assertIsNone(plan['config']['model'])
        self.assertIsNone(plan['config']['input_per_million'])
        for name,expected in plan['source_hashes'].items():
            self.assertEqual(audit.sha((audit.ROOT/name).read_bytes()),expected)
        self.assertNotIn('graph.workflow',sys.modules)
        self.assertNotIn('agents.common',sys.modules)
        self.assertNotIn('evaluation.week4.live_provider',sys.modules)
        self.assertNotIn('openai',sys.modules)
        self.assertNotIn('langsmith',sys.modules)

if __name__=='__main__':unittest.main()
