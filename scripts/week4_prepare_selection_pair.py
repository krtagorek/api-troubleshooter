"""Prepare two bound single-arm plans; never execute or orchestrate a live run."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
from scripts import week4_real_mock_run as offline

ROOT = offline.ROOT
OUT = ROOT/'data/week4/smoke-proposals/real-016-v2-selection-pair-1'
DATE = '2026-10-29'  # Public documentation retrieval date, not a human review time.


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name, value):
    with (OUT/name).open('x') as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')


def main():
    offline.clear_environment()
    with offline.offline_guard() as guard:
        from evaluation.week4.live_config import LiveConfig, V2, SELECTION_V1
        from evaluation.week4.live_cli import load_plan, PAIR_ARM, require_execution_authorization, authorization_identity
        from evaluation.week4.paired_selection_plan_v1 import VERSION
        from evaluation.week4.runner import metadata, digest
        from evaluation.week4.dependencies import verify_lock
        from tools.evidence_catalog import handle_catalog
        prior=ROOT/'data/week4/smoke-proposals/real-016-v2-3'
        raw=(prior/'sanitized-input.json').read_bytes();case=json.loads(raw)
        base=json.loads((prior/'config.json').read_text())
        base.update(selection_policy='off',pricing_verified_at=DATE)
        treatment={**base,'selection_policy':SELECTION_V1}
        configs={'baseline':LiveConfig(**base),'treatment':LiveConfig(**treatment)}
        sources=metadata('proposed-smoke','development-smoke','development-fixtures-1')['source_hashes']
        dependencies=verify_lock()
        receipt_dir=ROOT/'reports/week4/smoke016-v2-3-environment-preparation-1'
        receipt=json.loads((receipt_dir/'result.json').read_text())
        hashes=json.loads((receipt_dir/'artifact-hashes.json').read_text())
        assert all(sha(receipt_dir/p)==h for p,h in hashes.items())
        assert receipt['archive_integrity']['status']=='PASS_HASH_LOCKED_INSTALL'
        assert receipt['dependency_versions']['lock_sha256']==dependencies['lock_sha256']
        each=(Decimal(base['input_cap'])*Decimal(base['input_per_million'])+
              Decimal(base['output_cap'])*Decimal(base['output_per_million']))/1000000
        assert each==Decimal('0.421488') and each*10==Decimal('4.214880')
        OUT.mkdir(parents=True,exist_ok=False,mode=0o700)
        with (OUT/'sanitized-input.json').open('xb') as f:f.write(raw)
        for name,config in configs.items():
            write(name+'-config.json',config.public())
        worksheet=json.loads((prior/'review-worksheet.json').read_text())
        write('review-worksheet.json',worksheet)
        docs={'verified_date_utc':DATE,'model':base['model'],'service_tier':'default',
            'listed_usd_per_million_tokens':{'input':'0.40','cached_input':'0.10','output':'1.60'},
            'cache_savings_assumed':False,'documented_context':1047576,'documented_max_output':32768,
            'chat_completions':True,'structured_outputs':True,'lifecycle':'deprecated_not_retired',
            'scheduled_shutdown_date':'2027-01-14','not_after_utc_date':'2027-01-13',
            'sources':['https://developers.openai.com/api/docs/models/gpt-4.1-mini',
                       'https://developers.openai.com/api/docs/deprecations'],
            'raw_page_hashes':None,'authenticated_discovery':False,
            'account_access':'Not rechecked; earlier one-case run does not guarantee a future run.',
            'provider_invoice_tariff':'NOT_INDEPENDENTLY_ATTESTED'}
        write('official-pricing.json',docs)
        measurements={
            'assigned_arms':2,'case_version':'report-evidence-v2-1','measurement_values_before_execution':None,
            'required_reference_coverage':'selected_required_reference_count / required_reference_count from snapshot-bound V2 operands and attribution leaves; not semantic accuracy',
            'valid_selection':'valid_selected_references means catalog ID/reference/scalar binding; not sufficient evidence or confirmed cause',
            'analyst_entry':'actual root_cause_analyst stage start/completion only; not diagnostic success',
            'terminal_outcome':'held/completed/failed/timeout/interrupted with errors; unattempted arm retained if baseline blocks treatment',
            'tokens':'sum durable provider receipts across actual attempted calls; input/output/cache/reasoning; unknown stays null',
            'cost':'usage at bound rates, or retained uncertain reservations; never assume absent usage is zero; not invoice verification',
            'latency':'case elapsed from before process start through reaping and fsynced terminal journal/reconciliation, excluding report/export; model elapsed sum of ended attempted calls, never root+node+model totals',
            'semantic_quality':'Genuine human review required; review worksheet remains blank',
            'pairing_limitations':'Independent live outputs may differ; identical upstream requests do not guarantee identical classifier responses. Later payload differences may be downstream consequences. One case cannot establish isolated causality.'}
        write('planned-measurements.json',measurements)
        # Exact investigator example conditions on the sealed prior classifier;
        # it is not a prediction of the next independently sampled classifier.
        examples=ROOT/'reports/week4/attributed-selection-dependencies-v1-2'
        for src,dst in [('investigator-request-before.json','baseline-investigator-example.json'),
                        ('investigator-request-after.json','treatment-investigator-example.json'),
                        ('request-diff.json','investigator-example-diff.json')]:
            with (OUT/dst).open('xb') as f:f.write((examples/src).read_bytes())
        manifest={'version':VERSION,'comparison_id':'real-016-v2-selection-pair-1',
            'status':'PREPARED_NOT_AUTHORIZED','execution_authorized':False,'trace_export_authorized':False,
            'approval_identity':None,'approval_time':None,'external_tracing':False,'incident_tools':False,
            'concurrency':1,'retries':0,'model_fallback':False,'combined_ceiling_usd':'4.50',
            'full_ten_call_reservations_usd':str(each*10),'combined_headroom_usd':str(Decimal('4.50')-each*10),
            'per_call_reservation_usd':str(each),'input_bound_kind':'whole documented context, not exact token count',
            'not_after_utc_date':'2027-01-13','case_sha256':digest(case),'input_bytes_sha256':sha(OUT/'sanitized-input.json'),
            'archive_sha256':case['incident']['request_metadata']['report_attribution_v2']['source_sha256'],
            'evidence_snapshot':handle_catalog(case['incident'])['evidence_snapshot'],
            'source_hashes':sources,'dependencies':dependencies,
            'verified_installation_receipt_sha256':sha(receipt_dir/'result.json'),
            'verified_installation_manifest_sha256':sha(receipt_dir/'artifact-hashes.json'),
            'preparation_source_sha256':sha(Path(__file__)),
            'request_difference':'Investigator selection_dependency_advisory only, conditional on identical preceding outputs; system/schema/catalog/provider parameters unchanged.',
            'measurement_specification':'planned-measurements.json','semantic_accuracy':None,'actual_cost_usd':None,
            'execution_mechanism':'Existing live_cli run -> run_smoke -> supervise -> inference_worker -> LiveModel + Journal; no new runner.',
            'sequencing':'Baseline first; treatment dispatch requires sealed, reconciled, matching, reaped baseline. Fixed create-only output paths prevent repeats/concurrent arms.',
            'remaining_prerequisites':['Explicit new paired-run approval bound to both arm identities; no previous authorization carries over.',
                'Private dedicated WEEK4_OPENAI_API_KEY in actual execution environment; no value was read or presence checked here.',
                'Recheck lifecycle/pricing, current hashes and account permissions before authorized execution; no authenticated discovery now.'],
            'arms':{name:{'config':config.public(),'configuration_sha256':digest(config.public()),
                'output_path':'reports/week4/real-016-v2-selection-paired-live-1/'+name}
                for name,config in configs.items()}}
        write('plan.json',manifest)
        components={str(p.relative_to(ROOT)):sha(p) for p in OUT.iterdir() if p.is_file()}
        arm_identities={}
        for name,config in configs.items():
            plan={'version':PAIR_ARM,'status':'PREPARED_NOT_AUTHORIZED','execution_authorized':False,
                'trace_export_authorized':False,'external_tracing':False,'approval_identity':None,
                'approval_time':None,'approval_binding_sha256':None,'not_after_utc_date':'2027-01-13',
                'comparison_id':manifest['comparison_id'],'arm':name,
                'comparison_manifest_path':str((OUT/'plan.json').relative_to(ROOT)),
                'output_path':manifest['arms'][name]['output_path'],'evidence_policy':V2,
                'case':case,'case_sha256':digest(case),'input_path':str((OUT/'sanitized-input.json').relative_to(ROOT)),
                'input_bytes_sha256':manifest['input_bytes_sha256'],'archive_sha256':manifest['archive_sha256'],
                'config':config.public(),'configuration_sha256':digest(config.public()),
                'source_hashes':sources,'component_hashes':components}
            path=OUT/(name+'-plan.json');write(path.name,plan)
            _,checked=load_plan(path);assert checked==config
            try:require_execution_authorization(plan)
            except ValueError:pass
            else:raise AssertionError('Unapproved arm authorized')
            arm_identities[name]={'plan_sha256':sha(path),'immutable_authorization_identity_sha256':authorization_identity(plan)}
        assert not any(guard.values())
        write('verification.json',{'status':'PASS_OFFLINE_CONFIGURATION; NOT_AUTHORIZED',
            'master_plan_sha256':sha(OUT/'plan.json'),'arm_bindings':arm_identities,'guard_attempts':guard,
            'combined_budget_funded':True,'arm_count':2,'max_calls_per_arm':5,'max_total_calls':10,
            'live_calls':0,'semantic_accuracy':None,'actual_cost_usd':None})
        offline.finalize(OUT)
        print(json.dumps({'status':'PREPARED_NOT_AUTHORIZED','combined_worst_reservations_usd':str(each*10),
            'proposed_combined_ceiling_usd':'4.50','master_plan_sha256':sha(OUT/'plan.json'),
            'arm_bindings':arm_identities,'guard_attempts':guard},indent=2))


if __name__=='__main__':main()
