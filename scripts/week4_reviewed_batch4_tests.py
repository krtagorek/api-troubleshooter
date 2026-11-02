"""Network-denied input checks only; no endpoint, graph, model or SDK execution."""
import copy
import csv
import json
import socket
import sys
from typing import get_args
import unittest
from unittest.mock import patch
from scripts import week4_reviewed_batch4 as batch
from scripts.week4_reviewed_compatibility import sha,inventory_prefix

class Batch4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patches=[patch.object(socket.socket,'connect',side_effect=AssertionError('No network')),
            patch.object(socket.socket,'connect_ex',side_effect=AssertionError('No network')),
            patch.object(socket,'getaddrinfo',side_effect=AssertionError('No network')),
            patch.object(socket,'create_connection',side_effect=AssertionError('No network'))]
        for p in cls.patches:p.start()
        cls.records=json.loads((batch.DEST/'reviewed-candidates.json').read_text())
        cls.rows,cls.projections=batch.assess(cls.records)
    @classmethod
    def tearDownClass(cls):
        for p in reversed(cls.patches):p.stop()

    def test_sources_review_times_and_prior_artifacts(self):
        provenance=json.loads((batch.DEST/'import-provenance.json').read_text())
        for name,entry in provenance['sources'].items():
            b=(batch.SOURCE/name).read_bytes()
            self.assertEqual(sha(b),entry['sha256'])
            self.assertEqual((batch.DEST/'sources'/name).read_bytes(),b)
        for name,expected in provenance['prior_artifact_sha256'].items():
            self.assertEqual(sha((batch.ROOT/name).read_bytes()),expected)
        self.assertEqual(provenance['newly_confirmed_id'],'W4-REAL-020')
        for c in self.records['cases']:
            h=c['human_review'];self.assertEqual(h['status'],'ACCEPTED')
            self.assertEqual(h['reviewer'],'User in this conversation')
            for k in ('reviewed_at','recorded_at','confirmation_at','semantic_scores'):self.assertIsNone(h[k])
            self.assertFalse(c['runtime_ready']);self.assertFalse(h['independently_reproduced'])
        self.assertIsNone(self.records['cases'][2]['source_date'])
        self.assertIsNone(self.records['cases'][3]['source_date'])

    def test_016_unicode_header_exception_and_error_handling(self):
        from tools.evidence_catalog import build_catalog
        from evaluation.week4.contracts import InferenceCase
        p=self.projections['W4-REAL-016']['incident']
        self.assertEqual((p['http_method'],p['endpoint'],p['status_code']),('GET','/ocelot/posts/askdj',502))
        self.assertEqual(p['request_metadata']['request_headers']['skull'],'💀')
        self.assertEqual(p['request_metadata']['reported_exception'],'System.Net.Http.HttpRequestException: Request headers must contain only ASCII characters.')
        self.assertIn('appropriate error handling',p['expected_behavior'])
        self.assertIn('Content-Length is 0',p['actual_behavior'])
        self.assertIn('24.1.0',p['actual_behavior'])
        self.assertNotIn('upstream outage',json.dumps(p));self.assertNotIn('successful repair',json.dumps(p))
        model=InferenceCase.model_validate(self.projections['W4-REAL-016'])
        leaf=next(e for e in build_catalog(model.incident).values() if e.reference=='/request_metadata/request_headers/skull')
        self.assertEqual(leaf.observation,'💀')

    def test_017_two_log_views_and_concurrency_without_conditional_header(self):
        p=self.projections['W4-REAL-017']['incident']
        self.assertEqual((p['http_method'],p['endpoint'],p['status_code']),('PUT','/remote.php/webdav/x27.dat',412))
        self.assertIn('Proxy and backend access logs both',p['actual_behavior'])
        self.assertIn('Original reporter later observes',p['actual_behavior'])
        self.assertIn('two clients update',p['actual_behavior'])
        self.assertEqual(p['logs'],[])
        text=json.dumps(p)
        for term in ('If-Match','ETag','overwrite_protection_disabled','disable'):self.assertNotIn(term,text)

    def test_018_import_sequence_no_ui_trace_or_repairs(self):
        p=self.projections['W4-REAL-018']['incident']
        self.assertEqual((p['http_method'],p['endpoint'],p['status_code']),('POST','/api/v4/projects/2/issues',409))
        self.assertIn('import is ongoing',p['actual_behavior']);self.assertIn('after import',p['actual_behavior'])
        self.assertIn('Reporter describes',p['actual_behavior']);self.assertIn('suspects',p['actual_behavior'])
        for term in ('UniquenessValidator','database repair','iid override','retry loop'):self.assertNotIn(term,json.dumps(p))
        self.assertEqual(p['logs'],[])
        self.assertIsNone(p['response_body'])

    def test_019_masked_login_endpoint_and_version_conflict(self):
        p=self.projections['W4-REAL-019']['incident']
        self.assertEqual(p['endpoint'],'/login?return_to=http%3A%2F%2Fx.x.x.239%2Frepositories%2F1')
        self.assertEqual(p['status_code'],406);self.assertEqual(p['http_method'],'GET')
        self.assertIn('GET /api/v3/repositories/1 returning HTTP 200',p['actual_behavior'])
        v=p['request_metadata']['version_context']
        self.assertEqual(v['report_prose'],'16.7.2');self.assertEqual(v['capture_excerpt'],'16.7.3')
        self.assertEqual(v['earlier_success_comparison'],'16.2.1');self.assertFalse(v['reconciled'])
        self.assertIn(batch.VERSION_CONTEXT,p['actual_behavior'])
        self.assertNotIn('redirect_status',json.dumps(p));self.assertNotIn('base-path regression',json.dumps(p))
        self.assertNotEqual(p['endpoint'],'/api/v3/repositories/1')

    def test_020_head_allowed_two_urls_and_separate_attempt(self):
        from models.incident import Incident
        self.assertIn('HEAD',get_args(Incident.model_fields['http_method'].annotation))
        p=self.projections['W4-REAL-020']['incident']
        self.assertEqual((p['http_method'],p['endpoint'],p['status_code']),('HEAD','/',503))
        metadata=p['request_metadata']
        self.assertEqual(metadata['request_host_reported'],'envoy-egress:8080')
        self.assertEqual(metadata['command_structure'],'curl -v -k http://envoy-egress:8080 -I http://www.google.com')
        self.assertIn('200 as a separate request',p['actual_behavior'])
        self.assertIn('WRONG_VERSION_NUMBER',p['actual_behavior'])
        self.assertIn('different recorded attempt',p['actual_behavior'])
        self.assertIn('not correlated proof',metadata['correlation_scope'])
        self.assertIn('no proxy use for the Google transfer is established',metadata['correlation_scope'])
        self.assertIn('not a recommendation',metadata['correlation_scope'])
        self.assertEqual(metadata['operation_intent'],'unresolved_proxy_or_direct')
        self.assertIn('intent is unspecified',p['expected_behavior'])
        self.assertTrue(self.rows[-1]['operation_intent_unresolved'])
        self.assertEqual(p['logs'],[])

    def test_supported_checks_no_loss_and_no_label_leakage(self):
        from evaluation.week4.contracts import InferenceCase,BoundaryFailure
        from tools.redaction import redact
        self.assertEqual(len(self.projections),5)
        for ident,p in self.projections.items():
            self.assertEqual(InferenceCase.model_validate(p).model_dump(mode='json'),p)
            self.assertEqual(redact(p),p)
            self.assertEqual(p['incident']['logs'],[]);self.assertIsNone(p['incident']['response_body'])
            self.assertEqual(p['incident']['severity'],'unknown')
            text=json.dumps(p)
            for key in ('source_url','source_date','family','proposed_review','human_review','accepted_expected_behavior'):
                self.assertNotIn('"'+key+'"',text)
            self.assertNotIn('request_id',p['incident']['request_metadata'])
            self.assertNotIn('timestamp',p['incident']['request_metadata'])
            contaminated=copy.deepcopy(p);contaminated['incident']['request_metadata']['expected_answer']='TEST-ONLY'
            with self.assertRaises(BoundaryFailure):InferenceCase.model_validate(contaminated)
        for row in self.rows:
            self.assertEqual((row['schema'],row['initialization'],row['catalog']),('PASS','PASS','PASS'))
            self.assertEqual(row['sanitization_changes'],[])
            self.assertFalse(row['graph_executed']);self.assertFalse(row['editorial_goal_additionally_confirmed'])

    def test_cumulative_counts_not_inflated_by_schema_only_007(self):
        counts=batch.cumulative_counts(self.records,self.rows)
        self.assertEqual(counts['human_accepted'],20)
        self.assertEqual(counts['input_schema_compatible'],15)
        self.assertEqual(counts['evidence_preserving_input_compatible'],14)
        self.assertEqual(counts['graph_executed'],0);self.assertEqual(counts['golden_set_ready'],0)
        self.assertEqual(counts['schema_pass_with_evidence_loss_ids'],['W4-REAL-007'])
        self.assertEqual(len(counts['runtime_blocked_ids']),6)
        self.assertEqual(counts,json.loads((batch.DEST/'cumulative-counts.json').read_text()))

    def test_family_flags_not_independence_or_splits(self):
        report=json.loads((batch.DEST/'family-overlap.json').read_text())
        self.assertFalse(report['independence_established']);self.assertFalse(report['final_split_assigned'])
        self.assertEqual(len(report['prior_inventory_ids_checked']),230)
        self.assertEqual(report['exact_source_matches'],[])
        self.assertTrue(any('#2374' in g.get('related_source_issues',[]) for g in report['groups']))
        self.assertTrue(any(g['cases']==['W4-REAL-017','W4-REAL-018','W4-REAL-014'] for g in report['groups']))

    def test_append_only_and_idempotent_import(self):
        path=batch.ROOT/'data/week4/candidate-inventory.csv';before=path.read_bytes()
        self.assertEqual(sha(inventory_prefix(before,230)),'ba82e186f1fb9ced192f2c7727260864414c6e96d9c121e99eb7e405aa8df537')
        with path.open(newline='') as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),235);self.assertEqual(len({r['case_id'] for r in rows}),235)
        snapshot={p:p.read_bytes() for p in batch.DEST.rglob('*.json')}
        result=batch.run_import();self.assertEqual(result['counts']['human_accepted'],5)
        self.assertEqual(path.read_bytes(),before)
        self.assertEqual(set(snapshot),set(batch.DEST.rglob('*.json')))
        for p,data in snapshot.items():self.assertEqual(p.read_bytes(),data)

    def test_328_inherited_files_and_no_execution_modules(self):
        manifest=json.loads((batch.ROOT/'docs/source-baseline-manifest.json').read_text())
        self.assertEqual(len(manifest['files']),328)
        for entry in manifest['files']:
            data=(batch.ROOT/entry['destination_relative_path']).read_bytes()
            self.assertEqual(sha(data),entry['sha256']);self.assertEqual(len(data),entry['bytes'])
        for module in ('graph.workflow','agents.common','openai','langsmith','evaluation.week4.live_provider'):
            self.assertNotIn(module,sys.modules)

if __name__=='__main__':unittest.main()
