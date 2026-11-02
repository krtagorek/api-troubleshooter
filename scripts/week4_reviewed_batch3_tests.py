"""Focused, network-denied real-input checks. No graph/provider execution."""
import copy
import csv
import json
import socket
import sys
import unittest
from unittest.mock import patch
from scripts import week4_reviewed_batch3 as batch
from scripts.week4_reviewed_compatibility import sha,inventory_prefix

class Batch3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patches=[patch.object(socket.socket,'connect',side_effect=AssertionError('No network')),
            patch.object(socket.socket,'connect_ex',side_effect=AssertionError('No network')),
            patch.object(socket,'getaddrinfo',side_effect=AssertionError('No network')),
            patch.object(socket,'create_connection',side_effect=AssertionError('No network'))]
        for p in cls.patches:p.start()
        cls.records=json.loads((batch.DEST/'reviewed-candidates.json').read_text())
        cls.results,cls.projections=batch.assess(cls.records)
    @classmethod
    def tearDownClass(cls):
        for p in reversed(cls.patches):p.stop()

    def test_sources_confirmations_and_prior_decisions_unchanged(self):
        provenance=json.loads((batch.DEST/'import-provenance.json').read_text())
        for name,entry in provenance['sources'].items():
            source=(batch.SOURCE/name).read_bytes()
            self.assertEqual(sha(source),entry['sha256'])
            self.assertEqual(source,(batch.DEST/'sources'/name).read_bytes())
        for name,expected in provenance['prior_artifact_sha256'].items():
            self.assertEqual(sha((batch.ROOT/name).read_bytes()),expected)
        for case in self.records['cases']:
            self.assertEqual(case['review_status'],'ACCEPTED')
            self.assertEqual(case['human_review']['status'],'ACCEPTED')
            self.assertEqual(case['human_review']['reviewer'],'User in this conversation')
            self.assertFalse(case['runtime_ready'])
            self.assertFalse(case['human_review']['independently_reproduced'])
            for k in ('reviewed_at','confirmation_at','recorded_at','semantic_scores'):self.assertIsNone(case['human_review'][k])
        self.assertEqual(provenance['newly_confirmed_id'],'W4-REAL-015')

    def test_011_missing_header_warning_and_original_report_only(self):
        p=self.projections['W4-REAL-011']['incident']
        self.assertEqual((p['http_method'],p['endpoint'],p['status_code']),('GET','/api/list-files',401))
        self.assertIn('Adjacent middleware warning reports Missing Authorization header.',p['actual_behavior'])
        self.assertIn('image 0.15, Linux, changed port 3001',p['actual_behavior'])
        self.assertEqual(p['logs'],[])
        for term in ('invalid-token','token-expiry','signing-secret','port causes'):
            self.assertNotIn(term,p['actual_behavior'])

    def test_012_nested_exception_and_location_no_payload_repair(self):
        p=self.projections['W4-REAL-012']['incident']
        self.assertEqual((p['http_method'],p['endpoint'],p['status_code']),('POST','/euronews/mytable/1266?pretty=true',400))
        error=p['response_body']['error']
        self.assertEqual(error['type'],'mapper_parsing_exception')
        self.assertEqual(error['caused_by']['type'],'json_parse_exception')
        self.assertIn('line: 2, column: 45',error['caused_by']['reason'])
        self.assertIn("'f' (code 102)",error['caused_by']['reason'])
        self.assertNotIn('request_body',p['request_metadata'])
        self.assertNotIn('corrected',json.dumps(p))

    def test_013_expected_rejection_not_put_success(self):
        p=self.projections['W4-REAL-013']['incident']
        self.assertEqual((p['http_method'],p['endpoint'],p['status_code']),('PUT','/',405))
        self.assertIn('informative rejection',p['expected_behavior'])
        self.assertNotIn('succeed',p['expected_behavior'])
        for term in ('only GET /','GET / comparison receives HTTP 200','no Allow header shown','content-length 0'):
            self.assertIn(term,p['actual_behavior'])
        self.assertNotIn('allowed_methods',json.dumps(p));self.assertNotIn('upgrade',json.dumps(p))

    def test_014_exact_write_endpoint_and_reporter_attribution(self):
        p=self.projections['W4-REAL-014']['incident']
        self.assertEqual(p['endpoint'],'/api/issues/5a773a8c-85e8-4668-a72e-b7feff2ce14a/children')
        self.assertEqual((p['http_method'],p['status_code']),('POST',500))
        self.assertIn('Reporter says a subsequent listing shows the row created by this request.',p['actual_behavior'])
        self.assertIn('Reporter describes duplicate rows after repeated creates.',p['actual_behavior'])
        self.assertNotIn('serialization',json.dumps(p));self.assertNotIn('transaction',json.dumps(p))
        expectation=self.records['cases'][3]['accepted_expected_behavior']
        self.assertIn('Check existing state before replay',expectation)
        self.assertIn('no blind retries',expectation)

    def test_015_route_body_content_type_versions_not_speculation(self):
        p=self.projections['W4-REAL-015']['incident']
        self.assertEqual((p['http_method'],p['endpoint'],p['status_code']),('POST','/_plugins/_sm/policies/snapshot_policy',400))
        self.assertEqual(p['response_body']['error'],'no handler found for uri [/_plugins/_sm/policies/snapshot_policy] and method [POST]')
        for term in ('Content-Type application/json','OpenSearch 2.0.1 with Graylog 5.0.3'):self.assertIn(term,p['actual_behavior'])
        for term in ('licensing','malformed','switching','missing plugin','snapshot API'):self.assertNotIn(term,json.dumps(p))

    def test_supported_input_path_separation_and_excerpt_qualification(self):
        from evaluation.week4.contracts import InferenceCase,BoundaryFailure
        from tools.redaction import redact
        for ident,p in self.projections.items():
            self.assertEqual(InferenceCase.model_validate(p).model_dump(mode='json'),p)
            self.assertEqual(redact(p),p)
            text=json.dumps(p)
            for field in ('source_url','source_date','family','proposed_review','human_review','accepted_expected_behavior'):
                self.assertNotIn('"'+field+'"',text)
            self.assertEqual(p['incident']['logs'],[])
            self.assertIn('excerpt',p['incident']['actual_behavior'])
            metadata=p['incident']['request_metadata']
            self.assertNotIn('timestamp',metadata);self.assertNotIn('request_id',metadata)
            if p['incident']['response_body'] is not None:
                self.assertEqual(metadata['response_body_scope'],'reported_excerpt_completeness_unknown')
            poisoned=copy.deepcopy(p);poisoned['incident']['request_metadata']['expected_answer']='TEST-ONLY'
            with self.assertRaises(BoundaryFailure):InferenceCase.model_validate(poisoned)
        self.assertEqual(len(self.projections),5)
        for result in self.results:
            self.assertEqual(result['sanitization_changes'],[])
            self.assertEqual((result['schema'],result['initialization'],result['catalog']),('PASS','PASS','PASS'))
            self.assertFalse(result['graph_executed'])
            self.assertFalse(result['editorial_goal_additionally_confirmed'])

    def test_counts_overlap_and_no_golden_or_splits(self):
        report=json.loads((batch.DEST/'runtime-assessment.json').read_text())
        self.assertEqual(report['counts'],{'human_accepted':5,'input_schema_compatible':5,
            'evidence_preserving_input_compatible':5,'graph_executed':0,'golden_set_ready':0})
        overlap=json.loads((batch.DEST/'family-overlap.json').read_text())
        self.assertFalse(overlap['independence_established']);self.assertFalse(overlap['final_split_assigned'])
        self.assertEqual(overlap['exact_source_url_matches_in_001_010'],[])
        self.assertEqual(len(overlap['prior_inventory_ids_checked']),225)
        self.assertTrue(any(g['cases']==['W4-REAL-013','W4-REAL-015'] for g in overlap['broad_groups']))
        self.assertTrue(any('#6529/#3310' in g['qualification'] for g in overlap['broad_groups']))

    def test_inventory_and_repeat_import_idempotence(self):
        path=batch.ROOT/'data/week4/candidate-inventory.csv'
        before=path.read_bytes()
        self.assertEqual(sha(inventory_prefix(before,225)),'d55dde9f418447033216dcc06867d73ac7f5af002f2d8a332e1dfc33fe5cedb6')
        with path.open(newline='') as f:rows=list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows),230);self.assertEqual(len({r['case_id'] for r in rows}),len(rows))
        snapshot={p:p.read_bytes() for p in batch.DEST.rglob('*.json')}
        result=batch.run_import()
        self.assertEqual(result['counts']['human_accepted'],5)
        self.assertEqual(path.read_bytes(),before)
        for p,data in snapshot.items():self.assertEqual(p.read_bytes(),data)
        self.assertEqual(set(snapshot),set(batch.DEST.rglob('*.json')))

    def test_328_hashes_and_no_execution_sdk_imports(self):
        manifest=json.loads((batch.ROOT/'docs/source-baseline-manifest.json').read_text())
        self.assertEqual(len(manifest['files']),328)
        for entry in manifest['files']:
            data=(batch.ROOT/entry['destination_relative_path']).read_bytes()
            self.assertEqual(sha(data),entry['sha256']);self.assertEqual(len(data),entry['bytes'])
        for module in ('graph.workflow','agents.common','openai','langsmith','evaluation.week4.live_provider'):
            self.assertNotIn(module,sys.modules)

if __name__=='__main__':unittest.main()
