"""Portable integration controls; real cases are run only by paired runner."""
import json
from pathlib import Path
import tempfile
import unittest
from scripts import week4_real_mock_run as common
from tests.week4.test_attributed_report_v1 import fixture

class CompositionControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        common.clear_environment();cls.guard_context=common.offline_guard();cls.guard_context.__enter__()
    @classmethod
    def tearDownClass(cls):cls.guard_context.__exit__(None,None,None)
    def setUp(self):
        folder=common.ROOT/'.venv-week4-py311/attributed-report-test-artifacts';folder.mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=folder);self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)
    def execute(self,raw,arm,label):
        from scripts.week4_attributed_report_compare import worker
        from evaluation.week4.smoke import supervise
        directory=self.path/label;directory.mkdir()
        control=supervise(worker,(raw,str(directory),'SYNTHETIC-CONTROLS',arm),30)
        self.assertEqual(control['terminal'],'exited');self.assertTrue(control['cleanup_verified'])
        row=json.loads((directory/'result.json').read_text());calls=json.loads((directory/'model-calls.json').read_text())
        self.assertTrue(all(v==0 for v in row['security'].values()))
        self.assertTrue(all(row['span_structure'].values()),row['span_structure'])
        self.assertEqual(row['grounding']['invalid'],[])
        self.assertIsNone(row['cost_usd']);self.assertIsNone(row['semantic_accuracy'])
        return row,calls
    def test_topology_and_original_builder_are_unchanged(self):
        from evaluation.week4.attributed_report_v1.workflow import build_workflow
        from graph.workflow import build_workflow as baseline
        b=baseline(trusted_semantics_enabled=False);t=build_workflow(agents={},trusted_semantics_enabled=False)
        def topology(g):
            graph=g.get_graph();return sorted(graph.nodes),sorted((e.source,e.target,e.conditional) for e in graph.edges)
        self.assertEqual(topology(b),topology(t))
        self.assertEqual(set(b.compiled.builder.branches['log_investigator']),{'route_evidence'})
        self.assertEqual(set(t.compiled.builder.branches['log_investigator']),{'route_evidence_v1'})
        # No other branch or node logic has been replaced.
        for node in b.compiled.builder.branches:
            if node!='log_investigator':
                self.assertEqual(set(b.compiled.builder.branches[node]),set(t.compiled.builder.branches[node]))
        with self.assertRaises(ValueError):build_workflow(agents={},trusted_semantics_enabled=True)
    def test_positive_reaches_real_analyst_with_scoped_advisory_only(self):
        from scripts.week4_attributed_report_compare import compare_pair
        b,bc=self.execute(fixture(),'baseline','positive-baseline');t,tc=self.execute(fixture(),'v1','positive-v1')
        parity=compare_pair(b,t,bc,tc)
        self.assertTrue(all(parity.values()),parity)
        self.assertEqual(len(bc),2);self.assertEqual(len(tc),3)
        self.assertEqual(t['actual_ordered_graph_path'],['initialize','classifier','log_investigator','root_cause_analyst','request_user_input'])
        self.assertEqual(t['terminal_status'],'held');self.assertEqual(t['output']['diagnosis']['status'],'inconclusive')
        self.assertEqual(t['output']['validation_results'],[]);self.assertIsNone(t['output']['final_report'])
        self.assertEqual(len(t['advisory_changes']),1)
        self.assertTrue(all(t['advisory_scope_checks'][0].values()))
        payload=json.loads(tc[2]['messages'][-1]['content'].split('\n',1)[1]);advisory=payload['analysis_readiness']
        self.assertTrue(advisory['qualified_analysis']);self.assertFalse(advisory['definitive_confirmation'])
        self.assertFalse(advisory['legacy']['qualified_analysis'])
        from agents.root_cause import SYSTEM_PROMPT
        self.assertTrue(tc[2]['messages'][0]['content'].startswith(SYSTEM_PROMPT))
        self.assertEqual(payload['incident'],t['output']['sanitized_inputs'])
        self.assertEqual(t['usage']['input_tokens'],3);self.assertEqual(t['usage']['output_tokens'],3)
        self.assertEqual(t['model_elapsed_seconds'],sum(c['elapsed_seconds'] for c in tc))
    def test_insufficient_still_holds_and_legacy_telemetry_parity(self):
        raw=fixture();raw['incident']['request_metadata'].pop('reported_association')
        b,bc=self.execute(raw,'baseline','missing-b');t,tc=self.execute(raw,'v1','missing-t')
        self.assertEqual([c['messages'] for c in bc],[c['messages'] for c in tc])
        self.assertEqual(b['actual_ordered_graph_path'],t['actual_ordered_graph_path']);self.assertEqual(len(tc),2)
        from evaluation.week4.fixtures import development_cases
        raw=development_cases()[0];raw['case_id']='SYNTHETIC-LEGACY-CONTROL'
        b,bc=self.execute(raw,'baseline','legacy-b');t,tc=self.execute(raw,'v1','legacy-t')
        self.assertEqual([c['messages'] for c in bc],[c['messages'] for c in tc])
        self.assertEqual([c['response'] for c in bc],[c['response'] for c in tc])
        self.assertEqual(b['actual_ordered_graph_path'],t['actual_ordered_graph_path'])
        self.assertEqual(t['advisory_changes'],[])

if __name__=='__main__':unittest.main()
