"""V2-specific synthetic workflow parity for existing legacy/insufficient paths."""
import json
from pathlib import Path
import tempfile
import unittest
from scripts import week4_real_mock_run as common
from tests.week4.test_attributed_report_v1 import fixture

class ExistingPathControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        common.clear_environment();cls.guard=common.offline_guard();cls.guard.__enter__()
    @classmethod
    def tearDownClass(cls):cls.guard.__exit__(None,None,None)
    def compare(self,raw,count):
        from scripts.week4_attributed_report_v2_compare import worker
        from evaluation.week4.smoke import supervise
        parent=common.ROOT/'.venv-week4-py311/v2-regression-controls';parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as tmp:
            rows={};calls={}
            for arm in ('baseline','v2'):
                d=Path(tmp)/arm;d.mkdir()
                c=supervise(worker,(raw,str(d),'SYNTHETIC-V2-REGRESSION',arm),30)
                self.assertEqual(c['terminal'],'exited');self.assertTrue(c['cleanup_verified'])
                rows[arm]=json.loads((d/'result.json').read_text());calls[arm]=json.loads((d/'model-calls.json').read_text())
                self.assertEqual(rows[arm]['terminal_status'],'held');self.assertEqual(len(calls[arm]),count)
                self.assertEqual(rows[arm]['advisory_changes'],[])
                self.assertTrue(all(rows[arm]['span_structure'].values()))
                self.assertFalse(any(rows[arm]['security'].values()))
            self.assertEqual(rows['baseline']['actual_ordered_graph_path'],rows['v2']['actual_ordered_graph_path'])
            self.assertEqual([c['messages'] for c in calls['baseline']],[c['messages'] for c in calls['v2']])
            self.assertEqual([c['response'] for c in calls['baseline']],[c['response'] for c in calls['v2']])
    def test_v2_missing_original_anchor_contract_still_holds(self):
        self.compare(fixture(),2)
    def test_v2_legacy_qualified_telemetry_requests_outputs_and_route_match(self):
        from evaluation.week4.fixtures import development_cases
        raw=development_cases()[0];raw['case_id']='SYNTHETIC-V2-LEGACY-PARITY'
        self.compare(raw,3)

if __name__=='__main__':unittest.main()
