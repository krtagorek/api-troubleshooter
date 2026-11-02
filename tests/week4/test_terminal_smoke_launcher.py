"""Launcher controls only; no live subprocess, model, key, or smoke execution."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from scripts import week4_run_approved_016_v2_3 as launcher
from scripts import week4_real_mock_run as offline


class TerminalLauncherControls(unittest.TestCase):
    def setUp(self):
        offline.clear_environment()
        self.guard = offline.offline_guard()
        self.counts = self.guard.__enter__()
        self.addCleanup(self.guard.__exit__, None, None, None)

    def test_missing_key_never_runs_subprocess_or_creates_claim(self):
        with patch.object(launcher.subprocess, 'run') as run:
            with self.assertRaisesRegex(RuntimeError, 'absent'):
                launcher.main(check_only=True)
            run.assert_not_called()
        self.assertFalse(launcher.DESTINATION.exists())

    def test_check_only_validates_real_bindings_but_cannot_launch(self):
        raw = json.loads((launcher.ROOT / 'reports/week4/smoke016-v2-3-environment-preparation-1/raw-existing-preflight.json').read_text())
        raw['credential_presence']['WEEK4_OPENAI_API_KEY'] = True
        raw['remaining_setup_blockers'] = [
            'Hash-locked archive installation not performed; version check is not archive-integrity proof.']
        result = subprocess.CompletedProcess([], 0, stdout=json.dumps(raw))
        with patch.dict(os.environ, {'WEEK4_OPENAI_API_KEY': 'SYNTHETIC-PRESENCE-FIXTURE-NOT-A-KEY'}), \
             patch.object(launcher.subprocess, 'run', return_value=result) as run:
            self.assertEqual(launcher.main(check_only=True), 0)
            self.assertEqual(run.call_count, 1)
            self.assertEqual(run.call_args.args[0][-1], 'scripts.week4_smoke016_v2_3_approval_preflight')
            self.assertIn('(version 1) (allow default) (deny network*)', run.call_args.args[0])
        self.assertFalse(launcher.DESTINATION.exists())
        self.assertFalse(any(self.counts.values()))

    def test_unexpected_blocker_stops_before_claim(self):
        raw = json.loads((launcher.ROOT / 'reports/week4/smoke016-v2-3-environment-preparation-1/raw-existing-preflight.json').read_text())
        raw['credential_presence']['WEEK4_OPENAI_API_KEY'] = True
        raw['remaining_setup_blockers'] = ['UNEXPECTED']
        result = subprocess.CompletedProcess([], 0, stdout=json.dumps(raw))
        with patch.dict(os.environ, {'WEEK4_OPENAI_API_KEY': 'SYNTHETIC-PRESENCE-ONLY'}), \
             patch.object(launcher.subprocess, 'run', return_value=result):
            with self.assertRaisesRegex(RuntimeError, 'Unexpected setup blocker'):
                launcher.main(check_only=True)
        self.assertFalse(launcher.DESTINATION.exists())

    def test_existing_claim_prevents_another_launch(self):
        with tempfile.TemporaryDirectory(dir=launcher.ROOT / '.venv-week4-locked') as directory:
            with patch.object(launcher, 'DESTINATION', Path(directory)), \
                 patch.dict(os.environ, {'WEEK4_OPENAI_API_KEY': 'SYNTHETIC-PRESENCE-ONLY'}), \
                 patch.object(launcher.subprocess, 'run') as run:
                with self.assertRaisesRegex(RuntimeError, 'already exists'):
                    launcher.main()
                run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
