"""Prepare funded proposal 3, without running any smoke, model or SDK client."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
from scripts import week4_real_mock_run as offline
ROOT=offline.ROOT
OUT=ROOT/'data/week4/smoke-proposals/real-016-v2-3'
DATE='2026-10-29' # Actual public documentation retrieval date in UTC.

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):
    with (OUT/name).open('x') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')

def main():
    offline.clear_environment()
    with offline.offline_guard() as guard:
        from evaluation.week4.live_config import LiveConfig,CASE016_BUDGET_PROFILE,V2
        from evaluation.week4.live_cli import load_plan,require_execution_authorization,authorization_identity,PROPOSAL3
        from evaluation.week4.runner import metadata,digest
        from evaluation.week4.dependencies import verify_lock
        from evaluation.week4.contracts import InferenceCase
        olddir=ROOT/'data/week4/smoke-proposals/real-016-v2-2'
        previous=json.loads((olddir/'plan.json').read_text())
        case=json.loads((olddir/'sanitized-input.json').read_text())
        assert InferenceCase.model_validate(case).model_dump(mode='json')==case
        values=json.loads((olddir/'config.json').read_text())
        values.update(max_usd='2.25',budget_profile=CASE016_BUDGET_PROFILE,pricing_verified_at=DATE)
        config=LiveConfig(**values);each=(Decimal(config.input_cap)*Decimal(config.input_per_million)+
            Decimal(config.output_cap)*Decimal(config.output_per_million))/Decimal(1000000)
        total=each*config.max_calls;headroom=Decimal(config.max_usd)-total
        assert each==Decimal('0.421488') and total==Decimal('2.107440') and headroom==Decimal('0.142560')
        OUT.mkdir(parents=True,exist_ok=False,mode=0o700)
        for name in ('sanitized-input.json','review-worksheet.json','attribution-assessment.json','later-request-templates.json'):
            with (OUT/name).open('xb') as f:f.write((olddir/name).read_bytes())
        write('config.json',values)
        first=json.loads((olddir/'first-request-preview.json').read_text())
        first['status']='KNOWN_INITIAL_API_PARAMETER_PREVIEW_NOT_SENT'
        write('first-request-preview.json',first)
        official={'retrieved_date_utc':DATE,'retrieval':'Official public HTML pages via documentation tools; no authenticated discovery',
            'raw_page_hashes':None,'account_access':'UNVERIFIED',
            'model':'gpt-4.1-mini-2025-04-14','lifecycle':'deprecated_not_retired_on_retrieval_date',
            'scheduled_shutdown_date':'2027-01-14','snapshot_retained':True,
            'selection_reason':'Existing supported Chat Completions snapshot is suitable for a near-term bounded smoke; no model fallback or baseline model change.',
            'documented_features':{'chat_completions':True,'structured_outputs':True,'context_window':1047576,
                'maximum_output_tokens':32768,'reasoning_step':False},
            'listed_text_rates':{'currency':'USD','per_tokens':1000000,'input':'0.40','cached_input':'0.10','output':'1.60'},
            'reservation_cache_assumption':'No cache savings',
            'sources':[
                'https://developers.openai.com/api/docs/models/gpt-4.1-mini',
                'https://developers.openai.com/api/docs/deprecations',
                'https://developers.openai.com/api/docs/guides/structured-outputs',
                'https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create'],
            'limits':'Public support is not account access, invoice attestation or acceptance of every concrete dynamic schema. Recheck before paid execution.'}
        write('official-docs.json',official)
        write('cost-reservation.json',{'currency':'USD','per_call_input_reservation_tokens':1047576,
            'input_bound_kind':'Entire documented model context; conservative bound, not exact input token count',
            'max_complete_request_bytes':65536,'output_cap_total_tokens':1536,'calls':5,
            'per_call_usd':str(each),'five_call_usd':str(total),'proposed_ceiling_usd':'2.25','headroom_usd':str(headroom),
            'cached_savings_assumed':False,'reasoning_billed':'Included in completion_tokens once; no double counting',
            'actual_usage':None,'actual_cost_usd':None})
        sources=metadata('proposed-smoke','development-smoke','development-fixtures-1')['source_hashes']
        write('source-hashes.json',sources)
        files={str(p.relative_to(ROOT)):sha(p) for p in sorted(OUT.iterdir()) if p.is_file()}
        plan={'version':PROPOSAL3,'status':'PREPARED_FUNDED_NOT_AUTHORIZED','configuration_budget_ready':True,
            'execution_ready':False,'execution_authorized':False,'trace_export_authorized':False,
            'approval_identity':None,'approval_time':None,'approval_binding_sha256':None,
            'not_after_utc_date':'2027-01-13','external_tracing':False,'evidence_policy':V2,
            'case':case,'case_sha256':digest(case),'input_path':str((OUT/'sanitized-input.json').relative_to(ROOT)),
            'input_bytes_sha256':sha(OUT/'sanitized-input.json'),'archive_sha256':previous['archive_sha256'],
            'config':values,'configuration_sha256':digest(values),'source_hashes':sources,
            'component_hashes':files,'dependency_check':verify_lock(),
            'preparation_source_sha256':sha(Path(__file__)),
            'execution':{'path':'live_cli -> load_plan -> supervised smoke worker -> explicit V2 + scoped advisory -> provider + durable Journal',
                'command_shape':'python -m evaluation.week4.live_cli run --plan APPROVED_BOUND_COPY --output NEW_DIRECTORY --execute-live',
                'command_authorized':False,'case_count':1,'case_id':'W4-REAL-016','concurrency':1,
                'max_model_calls':5,'sdk_retries':0,'workflow_retries':0,'model_policy_tier_fallback':False,
                'incident_tools':False,'external_exports':False,'local_sanitized_spans':True,
                'worker_timeout_seconds':120,'http_phase_timeout_seconds':20},
            'budget':{'proposed_ceiling_usd':'2.25','per_call_full_reservation_usd':str(each),
                'five_call_full_reservations_usd':str(total),'headroom_usd':str(headroom),
                'execution_authorized':False,'older_plan_default_unchanged':'0.25'},
            'provenance':'Partial original-excerpt transcription; reporter-associated reproduction, not authenticated request correlation or independent reproduction.',
            'request_preview_limits':'Initial content known; later classification, selections, hypotheses, diagnosis, plan and advisory depend on earlier validated model outputs. No future route or diagnostic success is guaranteed.',
            'credentials':{'required_names':['WEEK4_OPENAI_API_KEY'],'values_read':False,'langsmith_required':False},
            'remaining_prerequisites':[
                'Explicit future paid-run authorization bound to this exact immutable identity; no authorization is granted here.',
                'Dedicated account access remains unverified until authorized execution; no authenticated discovery.',
                'Installed versions/Python match locks, but distribution archive integrity has not been reverified; resolve or explicitly accept environment provenance before execution without modifying old environments.',
                'Recheck public pricing/lifecycle and confirm applicable default-tier account tariff before execution; no model substitution.',
                'Any changed bindings require a new proposal; preserve the sealed original and use an explicitly authorized bound copy only.'],
            'human_review':'review-worksheet.json; all grades/identity/time blank','semantic_accuracy':None,'actual_cost_usd':None}
        write('plan.json',plan)
        loaded,checked=load_plan(OUT/'plan.json')
        assert checked==config and loaded['execution_authorized'] is False
        try:require_execution_authorization(loaded)
        except ValueError:authorization_rejected=True
        else:raise AssertionError('Unapproved plan must not authorize execution')
        assert not any(guard.values())
        write('verification.json',{'status':'PASS_CONFIGURATION_BUDGET; EXECUTION_NOT_AUTHORIZED',
            'five_calls_funded':True,'authorization_rejected_as_expected':authorization_rejected,
            'immutable_authorization_identity_sha256':authorization_identity(plan),
            'dependencies':plan['dependency_check'],'guard_attempts':dict(guard),
            'no_model_or_workflow_or_smoke_execution':True,'account_access':'UNVERIFIED',
            'semantic_accuracy':None,'actual_cost_usd':None})
        print(json.dumps({'status':plan['status'],'five_call_usd':str(total),'headroom_usd':str(headroom),
                          'authorization':False,'guard_attempts':guard},indent=2))

if __name__=='__main__':main()
