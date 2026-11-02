"""Final-approval preflight only. No smoke, provider, SDK client or network dispatch."""
from pathlib import Path
import hashlib,json,os
from decimal import Decimal
from scripts import week4_real_mock_run as offline
ROOT=offline.ROOT
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    key_present='WEEK4_OPENAI_API_KEY' in os.environ
    offline.clear_environment()
    with offline.offline_guard() as guard:
        from evaluation.week4.live_cli import load_plan,require_execution_authorization,authorization_identity
        from evaluation.week4.dependencies import verify_lock
        folder=ROOT/'data/week4/smoke-proposals/real-016-v2-3'
        plan,config=load_plan(folder/'plan.json')
        try:require_execution_authorization(plan)
        except ValueError:blocked=True
        else:raise AssertionError('Unapproved proposal authorized')
        checked={}
        for directory in (folder,ROOT/'reports/week4/smoke-proposal3-verification-1'):
            values=json.loads((directory/'artifact-hashes.json').read_text())
            assert all(sha(directory/p)==h for p,h in values.items())
            checked[str(directory.relative_to(ROOT))]=len(values)
        before=json.loads((ROOT/'reports/week4/smoke-proposal3-verification-1/before-hashes.json').read_text())['files']
        changed=[p for p,h in before.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
        metadata_changed=[p for p in changed if p=='data/week4/smoke-proposals/.DS_Store']
        protected_changed=[p for p in changed if p not in metadata_changed]
        assert not protected_changed,protected_changed
        baseline=ROOT/'docs/source-baseline-manifest.json'
        assert sha(baseline)=='0ad4421d9342b780996b70de8b72d9d0cab1b771e6f37fd82dd4c5ccbf42b62f'
        entries=json.loads(baseline.read_text())['files']
        assert len(entries)==328
        assert all(sha(ROOT/e['destination_relative_path'])==e['sha256'] for e in entries)
        count=0;artifacts=0
        for relative in before:
            if relative.startswith('reports/week4/') and relative.endswith('/artifact-hashes.json'):
                path=ROOT/relative;values=json.loads(path.read_text())
                assert all(sha(path.parent/p)==h for p,h in values.items())
                count+=1;artifacts+=len(values)
        for name in ('real-016-v2-1','real-016-v2-2'):
            path=ROOT/'data/week4/smoke-proposals'/name/'artifact-hashes.json'
            assert all(sha(path.parent/p)==h for p,h in json.loads(path.read_text()).items())
        assets=offline.asset_paths()
        assert len(assets)==50 and all(sha(p)==before[str(p.relative_to(ROOT))] for p in assets)
        preservation={'baseline_unchanged':328,'reviewed_assets_unchanged':50,
            'snapshot_files_checked':len(before),'protected_content_changes':protected_changed,
            'prior_sealed_manifests_verified':count,'prior_sealed_artifacts_verified':artifacts,
            'finder_metadata_mismatch':{p:{'before':before[p],'current':sha(ROOT/p)} for p in metadata_changed},
            'original_full_snapshot_audit':'FAIL: Finder metadata differs; not regenerated or restored',
            'bound_proposal_and_protected_content':'PASS'}
        each=(Decimal(config.input_cap)*Decimal(config.input_per_million)+Decimal(config.output_cap)*Decimal(config.output_per_million))/1000000
        assert each*5==Decimal('2.107440') and Decimal(config.max_usd)==Decimal('2.25')
        assert all(plan[k] is None for k in ('approval_identity','approval_time','approval_binding_sha256'))
        assert not any(guard.values())
        return {'status':'PASS_OFFLINE_PREFLIGHT; FINAL_READINESS_BLOCKED',
            'proposal':'real-016-v2-3','plan_sha256':sha(folder/'plan.json'),
            'immutable_authorization_identity_sha256':authorization_identity(plan),
            'case_id':plan['case']['case_id'],'policy':config.evidence_policy,'model':config.model,
            'service_tier':config.service_tier,'max_usd':config.max_usd,'max_calls':config.max_calls,
            'worst_five_call_reservation_usd':str(each*5),'retries':0,
            'authorization_rejected':blocked,'execution_authorized':False,'trace_export_authorized':False,
            'approval_fields_unset':True,'guard_attempts':guard,'smoke_executed':False,
            'dependencies':verify_lock(),'sealed_artifact_manifests_verified':checked,
            'credential_presence':{'WEEK4_OPENAI_API_KEY':key_present,'mechanism':'Environment-name membership only; no value fetched','nonempty_validity':'NOT_CHECKED'},
            'preservation':preservation,'remaining_setup_blockers':['Hash-locked archive installation not performed; version check is not archive-integrity proof.',
                'Dedicated WEEK4_OPENAI_API_KEY absent from inspected execution environment; no value read.'] if not key_present else ['Hash-locked archive installation not performed; version check is not archive-integrity proof.'],
            'account_access':'UNVERIFIED','real_provider_behavior':'UNVERIFIED',
            'semantic_accuracy':None,'actual_cost_usd':None}
if __name__=='__main__':print(json.dumps(main(),indent=2))
