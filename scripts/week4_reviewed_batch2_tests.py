"""No graph/model execution; pure supported input checks and import consistency."""
import copy
import csv
import json
import socket
import sys
import tempfile
import unittest
from unittest.mock import patch
from scripts import week4_reviewed_batch2 as batch
from scripts.week4_reviewed_compatibility import inventory_prefix,sha,json_bytes,write_identical_or_new

class Batch2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patches=[patch.object(socket.socket,'connect',side_effect=AssertionError('Network blocked')),
            patch.object(socket.socket,'connect_ex',side_effect=AssertionError('Network blocked')),
            patch.object(socket,'getaddrinfo',side_effect=AssertionError('Network blocked')),
            patch.object(socket,'create_connection',side_effect=AssertionError('Network blocked'))]
        for p in cls.patches:p.start()
        cls.records=json.loads((batch.DEST/'reviewed-candidates.json').read_text())
        cls.results,cls.projections=batch.assess(cls.records)
    @classmethod
    def tearDownClass(cls):
        for p in reversed(cls.patches):p.stop()

    def test_source_archives_and_confirmations(self):
        provenance=json.loads((batch.DEST/'import-provenance.json').read_text())
        for name,entry in provenance['sources'].items():
            b=(batch.SOURCE/name).read_bytes()
            self.assertEqual(sha(b),entry['sha256'])
            self.assertEqual(b,(batch.DEST/'sources'/name).read_bytes())
        self.assertEqual(len(self.records['cases']),5)
        for case in self.records['cases']:
            review=case['human_review']
            self.assertEqual(review['status'],'ACCEPTED');self.assertEqual(review['decision'],'ACCEPT')
            self.assertEqual(review['reviewer'],'User in this conversation')
            for field in ('reviewed_at','recorded_at','confirmation_at','semantic_scores'):self.assertIsNone(review[field])
            self.assertFalse(case['runtime_ready']);self.assertFalse(review['independently_reproduced'])
        self.assertEqual(provenance['newly_confirmed_id'],'W4-REAL-010')
        self.assertIsNone(provenance['reviewed_at'])

    def test_010_body_only_correction_not_coerced_into_runtime(self):
        case=self.records['cases'][4];e=case['inference_evidence']
        self.assertIsNone(e['status_code'])
        self.assertEqual(e['response_body']['errors'][0]['status'],'415')
        self.assertEqual(e['request_metadata']['status_evidence']['body_status'],'415')
        self.assertIsNone(e['request_metadata']['status_evidence']['transport_status'])
        row=self.results[4]
        self.assertEqual(row['runtime_result'],'BLOCKED_UNKNOWN_TRANSPORT_STATUS')
        self.assertEqual(row['schema'],'FAIL')
        self.assertTrue(any(e['location']==['incident','status_code'] and e['type']=='int_type' for e in row['safe_rejections']))
        self.assertEqual(row['initialization'],'NOT_CHECKED')
        self.assertNotIn(case['id'],self.projections)
        self.assertFalse((batch.DEST/'inference'/f"{case['id']}.json").exists())
        expected=case['accepted_expected_behavior']
        for term in ('Content-Type','boundary','sanitized payload','response status','unproven'):self.assertIn(term,expected)

    def test_006_failure_and_comparison_preserved(self):
        p=self.projections['W4-REAL-006']['incident']
        self.assertEqual(p['status_code'],415)
        self.assertIs(p['request_metadata']['request_body_present'],False)
        self.assertIs(p['request_metadata']['content_type_present'],False)
        self.assertEqual(p['request_metadata']['framework_version'],'5.1.2')
        self.assertIn('consumes = "application/json"',p['request_metadata']['handler_code'])
        self.assertIn('same empty-body request reportedly returns HTTP 200 and []',p['actual_behavior'])
        self.assertEqual(self.results[0]['sanitization_changes'],[])
        self.assertNotIn('every Spring',p['actual_behavior'])

    def test_007_loss_is_explicit_and_no_weakened_inference_export(self):
        case=self.records['cases'][1]
        self.assertEqual(case['inference_evidence']['request_metadata']['dependency_code'],'decode_access_token(token: str)')
        self.assertEqual(case['inference_evidence']['response_body']['detail'][0]['loc'],['query','token'])
        row=self.results[1]
        self.assertEqual(row['schema'],'PASS')
        self.assertEqual(row['runtime_result'],'SCHEMA_PASS_EVIDENCE_LOSS_BLOCKED')
        self.assertEqual(row['evaluation_eligibility'],'BLOCKED_EVIDENCE_PRESERVATION_REVIEW')
        paths={d['path'] for d in row['sanitization_changes']}
        self.assertIn('/request_metadata/dependency_code',paths)
        self.assertIn('/request_metadata/authorization_scheme_reported',paths)
        self.assertNotIn('W4-REAL-007',self.projections)
        preview=row['sanitized_projection_preview']['incident']
        self.assertEqual(preview['response_body']['detail'][0]['loc'],['query','token'])
        self.assertNotEqual(preview['request_metadata']['dependency_code'],'decode_access_token(token: str)')
        self.assertNotIn('Reporter later confirms',json.dumps(preview))
        self.assertFalse((batch.DEST/'inference/W4-REAL-007.json').exists())

    def test_008_repository_scope_and_reporter_status(self):
        p=self.projections['W4-REAL-008']['incident']
        self.assertEqual(p['status_code'],404)
        self.assertEqual(p['request_metadata']['status_evidence']['kind'],'reporter_stated')
        self.assertEqual(p['endpoint'],'/repos/octocat/hello-world/pages')
        self.assertEqual(p['request_metadata']['repository_scope']['shown_endpoint_role'],'example repository')
        self.assertIn('separately reported reporter-owned',p['actual_behavior'])
        self.assertIsNone(p['response_body'])
        self.assertNotIn('lacks Pages',json.dumps(p));self.assertNotIn('later confirms',json.dumps(p))

    def test_009_status_provenance_and_no_fabricated_headers(self):
        p=self.projections['W4-REAL-009']['incident']
        self.assertEqual(p['status_code'],429);self.assertEqual(p['response_body']['error']['status'],429)
        self.assertEqual(p['request_metadata']['status_evidence']['kind'],'reporter_stated_and_body_echo')
        self.assertFalse(p['request_metadata']['status_evidence']['captured_status_line_available'])
        text=json.dumps(p)
        for term in ('Retry-After','quota_limit','outage','excessive','timestamp'):self.assertNotIn(term,text)

    def test_separation_supported_projections_and_unknown_fields(self):
        from evaluation.week4.contracts import InferenceCase,BoundaryFailure
        from tools.redaction import redact
        for ident,p in self.projections.items():
            self.assertEqual(InferenceCase.model_validate(p).model_dump(mode='json'),p)
            self.assertEqual(redact(p),p)
            text=json.dumps(p)
            for field in ('source_url','source_date','proposed_review','accepted_expected_behavior','human_review','family','proposed_stratum'):
                self.assertNotIn('"'+field+'"',text)
            self.assertEqual(p['incident']['logs'],[])
            poisoned=copy.deepcopy(p);poisoned['incident']['request_metadata']['expected_answer']='TEST-ONLY'
            with self.assertRaises(BoundaryFailure):InferenceCase.model_validate(poisoned)
        self.assertEqual(set(self.projections),{'W4-REAL-006','W4-REAL-008','W4-REAL-009'})

    def test_family_overlap_not_splits_or_independence(self):
        report=json.loads((batch.DEST/'family-overlap.json').read_text())
        self.assertFalse(report['final_split_assigned']);self.assertFalse(report['independence_established'])
        pairs=[g['cases'] for g in report['groups']]
        self.assertIn(['W4-REAL-006','W4-REAL-010'],pairs)
        self.assertIn(['W4-REAL-004','W4-REAL-009'],pairs)

    def test_inventory_append_preserves_old_batch_and_all_220_rows(self):
        p=batch.ROOT/'data/week4/candidate-inventory.csv';data=p.read_bytes()
        self.assertEqual(sha(inventory_prefix(data,220)),'e636f576e250162a477b937e5eb139430e2106cd4e921f1542f9be596cc19b42')
        with p.open(newline='') as f:rows=list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows),225);self.assertEqual(len({r['case_id'] for r in rows}),len(rows))
        for ident in batch.IDS:
            row=next(r for r in rows if r['case_id']==ident)
            self.assertEqual(row['review_status'],'ACCEPT');self.assertEqual(row['scenario_type'],'UNASSIGNED')
        prior=batch.ROOT/'data/week4/reviewed-candidates/real-incidents-v2.json'
        self.assertEqual(sha(prior.read_bytes()),'f3eb5764d834b6a65e4a54dfad61426fdeb08adc41bbe73e5ed703b8e826af28')

    def test_baseline_328_and_no_execution_modules(self):
        manifest=json.loads((batch.ROOT/'docs/source-baseline-manifest.json').read_text())
        self.assertEqual(len(manifest['files']),328)
        for entry in manifest['files']:
            data=(batch.ROOT/entry['destination_relative_path']).read_bytes()
            self.assertEqual(sha(data),entry['sha256']);self.assertEqual(len(data),entry['bytes'])
        for name in ('graph.workflow','agents.common','openai','langsmith','evaluation.week4.live_provider'):
            self.assertNotIn(name,sys.modules)

if __name__=='__main__':unittest.main()
