"""Prepare proposal 2 only. Never execute an agent, provider, supervisor or smoke."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
from scripts import week4_real_mock_run as offline
ROOT=offline.ROOT
OUT=ROOT/'data/week4/smoke-proposals/real-016-v2-2'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):
    with (OUT/name).open('x') as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')

def main():
    offline.clear_environment()
    with offline.offline_guard() as guard:
        from evaluation.week4.live_config import LiveConfig,V2
        from evaluation.week4.live_cli import load_plan
        from evaluation.week4.runner import metadata,digest
        from evaluation.week4.dependencies import verify_lock
        from evaluation.week4.contracts import InferenceCase
        previous=ROOT/'data/week4/smoke-proposals/real-016-v2-1'
        old=json.loads((previous/'plan.json').read_text())
        case=json.loads((previous/'sanitized-input.json').read_text())
        assert InferenceCase.model_validate(case).model_dump(mode='json')==case
        config=json.loads((previous/'proposed-config.json').read_text())
        config.update(evidence_policy=V2,service_tier='default',input_bound_kind='model_context_max',
                      input_cap=1047576,max_request_bytes=65536)
        LiveConfig(**config) # Valid settings; deliberately unfundable at current real rates/cap.
        reservation=(Decimal(config['input_cap'])*Decimal(config['input_per_million'])+
            Decimal(config['output_cap'])*Decimal(config['output_per_million']))/Decimal(1000000)
        assert reservation==Decimal('0.421488')
        maximum=reservation*config['max_calls'];assert maximum==Decimal('2.107440')
        OUT.mkdir(parents=True,exist_ok=False,mode=0o700)
        for name in ('sanitized-input.json','review-worksheet.json','attribution-assessment.json'):
            with (OUT/name).open('xb') as f:f.write((previous/name).read_bytes())
        write('config.json',config)
        source=metadata('proposed-smoke','development-smoke','development-fixtures-1')['source_hashes']
        pricing=json.loads((previous/'official-docs.json').read_text())
        pricing['implementation_check_date_utc']='2026-10-29'
        pricing['additional_official_verification']=[
            {'url':'https://developers.openai.com/api/docs/guides/token-counting',
             'finding':'Documented input counter is Responses-specific. No equivalent Chat structured-schema pre-dispatch exact count established. No counting API request performed.'},
            {'url':'https://developers.openai.com/api/docs/models/gpt-4.1-mini',
             'finding':'Full documented model context 1047576, used as a conservative reservation, not an estimate or exact input count.'}]
        write('official-docs.json',pricing)
        first=json.loads((previous/'first-request-preview.json').read_text())
        first['wire_body_preview']['service_tier']='default'
        first['service_tier_omitted_by_current_provider']=False
        first['required_future_service_tier']='default'
        first['body_bytes']=len(json.dumps(first['wire_body_preview'],ensure_ascii=False,separators=(',',':')).encode())
        first['maximum_request_bytes']=65536
        write('first-request-preview.json',first)
        later=json.loads((previous/'later-request-templates.json').read_text())
        for item in later['templates']:
            if 'analysis_readiness' in item['dynamic_payload_fields']:
                item['dynamic_payload_fields']['analysis_readiness']='V2 assessment of actual selected evidence, scoped to analyst; supported in supervised worker. Prior outputs remain unknown.'
        write('later-request-templates.json',later)
        plan={'version':'week4-real-016-v2-live-smoke-proposal-2','status':'BLOCKED_BUDGET_INFEASIBLE_AND_ACCOUNT_UNVERIFIED',
            'ready_for_approval':False,'execution_authorized':False,'trace_export_authorized':False,
            'approval_identity':None,'approval_time':None,'external_tracing':False,'evidence_policy':V2,
            'case':case,'case_sha256':digest(case),'input_bytes_sha256':sha(OUT/'sanitized-input.json'),
            'archive_sha256':old['bindings']['archive_sha256'],'config':config,'configuration_sha256':digest(config),
            'source_hashes':source,'dependency_check':verify_lock(),
            'preparation_source_sha256':sha(Path(__file__)),
            'pricing_record_sha256':sha(OUT/'official-docs.json'),
            'execution':{'supported_path':'live_cli.load_plan -> run_smoke -> supervised inference_worker -> explicit V2 workflow + AnalystAdvisory -> LiveModel/Journal',
                'command_shape':'python -m evaluation.week4.live_cli run --plan THIS_PLAN --output NEW_DIR --execute-live',
                'command_is_not_authorized_or_fundable':True,'concurrency':1,'sdk_retries':0,'workflow_retries':0,
                'max_model_calls':5,'max_complete_request_bytes':65536,'output_token_cap':1536,
                'input_reservation_kind':'Full documented model context, 1047576 tokens, regardless of local wire size; no byte/character token estimate.',
                'worker_timeout_seconds':120,'http_phase_timeout_seconds':20,'external_tools':False,
                'local_spans':True,'remote_exports':False},
            'budget':{'currency':'USD','current_enforced_stop_limit_usd':'0.25',
                'viable_smoke_ceiling_at_025':False,'worst_case_per_call_usd':str(reservation),
                'worst_case_five_calls_usd':str(maximum),'minimum_rounded_candidate_ceiling_usd':'2.11',
                'higher_ceiling_implemented':False,'higher_ceiling_authorized':False,
                'cache_hits_assumed':False,'actual_cost_usd':None,
                'reasoning':'All billed completion tokens counted once, including non-visible/reasoning tokens. No additional reasoning multiplier.'},
            'remaining_blockers':[
                'Current $0.25 hard stop cannot fund even one full-context reservation; first dispatch is rejected.',
                'Reducing this conservative reserve requires a justified Chat/schema bound or separately scoped counting/API work. Raising the ceiling requires explicit approval and implementation outside this change.',
                'Dedicated account/model access, current tariff/lifecycle and real provider schema/tier/usage behavior remain operationally unverified.'],
            'credentials':{'required':['WEEK4_OPENAI_API_KEY'],'langsmith_required':False,'private_values_read':False},
            'provenance':'Partial excerpt transcription and reporter-associated reproduction; not authenticated correlation or independent reproduction.',
            'human_review':'review-worksheet.json; all semantic grades blank',
            'authorization_rule':'No current or prior proposal authorizes a run. Any blocker resolution changes bindings and requires a new version plus explicit user authorization tied to exact hashes.'}
        write('plan.json',plan)
        try:load_plan(OUT/'plan.json')
        except ValueError as exc:
            assert 'cannot fund' in str(exc),str(exc)
            rejection=str(exc)
        else:raise AssertionError('Unfunded real-price plan must not load for dispatch')
        assert not any(guard.values())
        write('verification.json',{'status':'PASS_LOCAL_IMPLEMENTATION_CHECKS; PAID_RUN_BLOCKED',
            'settings_supported':True,'explicit_V2_selected':True,'plan_loader_rejection':rejection,
            'budget_025_infeasible':True,'network_or_sdk_or_command_attempts':dict(guard),
            'no_workflow_or_smoke_executed':True,'semantic_accuracy':None,'cost_usd':None})
        print(json.dumps({'status':plan['status'],'per_call_usd':str(reservation),'five_calls_usd':str(maximum),
                          'loader_rejection':rejection,'guards':guard},indent=2))

if __name__=='__main__':main()
