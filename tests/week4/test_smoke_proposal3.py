"""Configuration/journal/authorization only: no SDK transport or smoke invocation."""
import copy
from decimal import Decimal
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts import week4_real_mock_run as offline

ROOT=offline.ROOT

class Proposal3Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        offline.clear_environment();cls.guard_context=offline.offline_guard();cls.guard=cls.guard_context.__enter__()
    @classmethod
    def tearDownClass(cls):cls.guard_context.__exit__(None,None,None)
    def setUp(self):
        base=ROOT/'.venv-week4-py311/proposal3-config-tests';base.mkdir(exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=base);self.addCleanup(self.tmp.cleanup)
        self.directory=Path(self.tmp.name)
    def config(self,**changes):
        from evaluation.week4.live_config import LiveConfig,CASE016_BUDGET_PROFILE
        values=json.loads((ROOT/'data/week4/smoke-proposals/real-016-v2-2/config.json').read_text())
        values.update(max_usd='2.25',budget_profile=CASE016_BUDGET_PROFILE);values.update(changes)
        return LiveConfig(**values)
    def plan(self):
        from evaluation.week4.runner import metadata,digest
        from evaluation.week4.live_cli import PROPOSAL3
        case_path='data/week4/report-evidence-v2-1/inference/W4-REAL-016.json'
        raw=(ROOT/case_path).read_bytes();case=json.loads(raw)
        settings=self.config().public()
        return {'version':PROPOSAL3,'case':case,'case_sha256':digest(case),
            'config':settings,'configuration_sha256':digest(settings),
            'source_hashes':metadata('proposed-smoke','development-smoke','development-fixtures-1')['source_hashes'],
            'archive_sha256':case['incident']['request_metadata']['report_attribution_v2']['source_sha256'],
            'evidence_policy':'attributed-report-readiness-v2','external_tracing':False,'trace_export_authorized':False,
            'input_path':case_path,'input_bytes_sha256':offline.sha(raw),
            'component_hashes':{case_path:offline.sha(raw)},'execution_authorized':False,
            'approval_identity':None,'approval_time':None,'approval_binding_sha256':None,
            'not_after_utc_date':'2027-01-13'}
    def write(self,plan):
        path=self.directory/'plan.json';path.write_text(json.dumps(plan));return path
    def test_five_full_reservations_are_funded_without_cache_savings(self):
        from evaluation.week4.live_cli import load_plan
        plan,config=load_plan(self.write(self.plan()))
        each=(Decimal(config.input_cap)*Decimal(config.input_per_million)+Decimal(config.output_cap)*Decimal(config.output_per_million))/1000000
        self.assertEqual(each,Decimal('0.421488'))
        self.assertEqual(each*5,Decimal('2.107440'));self.assertLess(each*5,Decimal('2.25'))
        self.assertFalse(plan['execution_authorized']);self.assertEqual(config.max_usd,'2.25')
    def test_default_and_older_configs_keep_025(self):
        from evaluation.week4.live_config import LiveConfig,DEFAULT_BUDGET_PROFILE
        old=json.loads((ROOT/'data/week4/smoke-proposals/real-016-v2-2/config.json').read_text())
        settings=LiveConfig(**old);self.assertEqual(settings.max_usd,'0.25')
        self.assertEqual(settings.budget_profile,DEFAULT_BUDGET_PROFILE)
        old['max_usd']='2.25'
        with self.assertRaises(ValueError):LiveConfig(**old)
    def test_older_plan_version_cannot_borrow_the_new_ceiling(self):
        from evaluation.week4.live_cli import load_plan
        for version in ('week4-smoke-plan-1','week4-real-016-v2-live-smoke-proposal-2'):
            p=self.plan();p['version']=version
            with self.assertRaisesRegex(ValueError,'Older plans'):load_plan(self.write(p))
    def test_missing_authorization_prevents_entry_without_reading_credentials(self):
        from evaluation.week4 import live_cli
        path=self.write(self.plan())
        with patch('sys.argv',['live_cli','run','--plan',str(path),'--output',str(self.directory/'never'),'--execute-live']), \
             patch.object(live_cli,'run_smoke',side_effect=AssertionError('Smoke execution prohibited')) as entry:
            with self.assertRaises(SystemExit) as result:live_cli.main()
            self.assertEqual(result.exception.code,2);entry.assert_not_called()
        self.assertFalse((self.directory/'never').exists())
    def test_direct_high_ceiling_live_entry_requires_a_bound_authorized_plan(self):
        from evaluation.week4.smoke import run_smoke
        from evaluation.week4.contracts import BoundaryFailure
        with self.assertRaises(BoundaryFailure):
            run_smoke({},self.config(),self.directory/'never',mode='live',execute_live=True)
        self.assertFalse((self.directory/'never').exists())
    def test_changed_case_config_source_and_component_bindings_reject(self):
        from evaluation.week4.live_cli import load_plan
        for field in ('case','config','source','component','archive'):
            p=self.plan()
            if field=='case':p['case']['incident']['status_code']=400
            if field=='config':p['config']['max_calls']=4
            if field=='source':p['source_hashes']['evaluation/week4/live_config.py']='0'*64
            if field=='component':p['component_hashes'][p['input_path']]='0'*64
            if field=='archive':p['archive_sha256']='0'*64
            with self.subTest(field=field),self.assertRaises(ValueError):load_plan(self.write(p))
    def test_wrong_case_profile_policy_tier_or_model_cannot_dispatch(self):
        from evaluation.week4.live_cli import load_plan
        from evaluation.week4.runner import digest
        p=self.plan();p['case']['case_id']='DIFFERENT';p['case_sha256']=digest(p['case'])
        with self.assertRaises(ValueError):load_plan(self.write(p))
        for changes in ({'evidence_policy':'inherited'},{'service_tier':'auto'},
                        {'model':'gpt-4.1-mini'},{'max_usd':'2.250001'},{'budget_profile':'unlisted'}):
            with self.subTest(changes=changes),self.assertRaises(ValueError):self.config(**changes)
    def test_call_exhaustion_blocks_journal_dispatch(self):
        from evaluation.week4.accounting import Journal
        from evaluation.week4.contracts import ResourceFailure
        j=Journal.create(self.directory,self.config().public())
        for i in range(5):
            call=j.reserve(case_id='SYNTHETIC-ACCOUNTING-ONLY',root_id='fixture',span_id=str(i),schema='fixture')
            j.attempt(call,20)
            j.usage(call,{'input_tokens':1047576,'output_tokens':1536,'cached_input_tokens':0,
                         'total_tokens':1049112},self.config().model,'default')
        self.assertEqual(Decimal(j.totals(j.events())['known_cost_usd']),Decimal('2.107440'))
        with self.assertRaises(ResourceFailure):j.reserve(case_id='fixture',root_id='fixture',span_id='6',schema='fixture')
        self.assertEqual(j.totals(j.events())['attempted_calls'],5)
    def test_money_exhaustion_and_uncertain_reservations_block(self):
        from evaluation.week4.accounting import Journal
        from evaluation.week4.contracts import AccountingFailure,ResourceFailure
        settings=self.config(max_usd='1.70');j=Journal.create(self.directory,settings.public())
        for i in range(4):
            call=j.reserve(case_id='SYNTHETIC',root_id='fixture',span_id=str(i),schema='fixture');j.attempt(call,20)
            j.usage(call,{'input_tokens':1047576,'output_tokens':1536,'cached_input_tokens':0,
                         'total_tokens':1049112},settings.model,'default')
        with self.assertRaises(ResourceFailure):j.reserve(case_id='fixture',root_id='fixture',span_id='5',schema='fixture')
        other=self.directory/'uncertain';other.mkdir();j=Journal.create(other,self.config().public())
        j.reserve(case_id='SYNTHETIC',root_id='fixture',span_id='1',schema='fixture')
        with self.assertRaises(AccountingFailure):j.reserve(case_id='fixture',root_id='fixture',span_id='2',schema='fixture')
    def test_authorization_identity_changes_with_immutable_bindings(self):
        from evaluation.week4.live_cli import authorization_identity,require_execution_authorization
        p=self.plan();old=authorization_identity(p);p['config']['max_calls']=4
        self.assertNotEqual(old,authorization_identity(p))
        with self.assertRaises(ValueError):require_execution_authorization(p)
        # Counterfactual markers are NOT a human approval or review record.
        p.update(execution_authorized=True,approval_identity='SYNTHETIC-NOT-A-HUMAN-APPROVAL',
                 approval_time='SYNTHETIC-NOT-A-REVIEW-TIME',approval_binding_sha256=old)
        with self.assertRaisesRegex(ValueError,'does not match'):require_execution_authorization(p)
    def test_lifecycle_window_cannot_be_extended_by_plan_data(self):
        from evaluation.week4.live_cli import load_plan
        p=self.plan();p['not_after_utc_date']='2030-01-01'
        with self.assertRaisesRegex(ValueError,'lifecycle'):load_plan(self.write(p))
    def test_no_network_sdk_or_command_attempts(self):
        self.assertFalse(any(self.guard.values()),self.guard)

if __name__=='__main__':unittest.main()
