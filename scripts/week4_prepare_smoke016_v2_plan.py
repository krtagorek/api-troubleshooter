"""Data-only blocked smoke proposal. NO workflow, model, SDK client or smoke run."""
import ast
from decimal import Decimal
import hashlib
import json
from pathlib import Path
from scripts import week4_real_mock_run as offline

ROOT=offline.ROOT
OUT=ROOT/'data/week4/smoke-proposals/real-016-v2-1'
INPUT=ROOT/'data/week4/report-evidence-v2-1/inference/W4-REAL-016.json'
DATE='2026-10-29'  # Actual UTC documentation retrieval date checked by clock tool.
MODEL='gpt-4.1-mini-2025-04-14'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def digest(v):return hashlib.sha256(canonical(v)).hexdigest()
def load(p):return json.loads(p.read_text())
def write(name,v):
    with (OUT/name).open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')


def main():
    # Inspect only named tracing flags in the supplied pre-snapshot, not secrets.
    before=load(OUT/'before-preservation.json')
    assert set(p.name for p in OUT.iterdir())=={'before-preservation.json'}
    offline.clear_environment()
    with offline.offline_guard() as guard:
        from evaluation.week4.dependencies import verify_lock
        from evaluation.week4.contracts import InferenceCase, check_inference
        from evaluation.week4.live_config import LiveConfig
        from evaluation.week4.live_provider import strict_wire
        from evaluation.week4.attributed_report_v2.readiness import assess
        from evaluation.week4.attributed_report_v2.archive import Archive
        from models.evidence import Evidence, EvidenceCollection
        from tools.evidence_catalog import build_catalog, handle_catalog
        from tools.redaction import redact
        from graph import state as schemas
        from agents import error_classifier, log_investigator, root_cause, resolution, validator
        from agents.common import SAFETY
        from langchain_core.messages import HumanMessage, SystemMessage

        dependencies=verify_lock()
        raw=load(INPUT);typed=InferenceCase.model_validate(raw)
        assert typed.model_dump(mode='json')==raw
        assert redact(raw)==raw
        check_inference(raw)
        with (OUT/'sanitized-input.json').open('xb') as f:f.write(INPUT.read_bytes())
        assert sha(OUT/'sanitized-input.json')==sha(INPUT)
        packet=raw['incident']['request_metadata']['report_attribution_v2']
        archive_path=ROOT/'data/week4/report-evidence-v2-1/archive'/(packet['source_sha256']+'.json')
        document=Archive().load(packet['source_sha256'])
        assert document.raw_capture_sha256 is None
        assert document.relationships[packet['relationship']].authenticated_request_correlation is False
        catalog=build_catalog(typed.incident)
        items=[Evidence(evidence_id=e.evidence_id,source=e.source,observation=e.observation,
                        reference=e.reference,reliability=0.5) for e in catalog.values()
               if e.reference!='/expected_behavior' and e.value_type!='null']
        assessment=assess(typed.incident,EvidenceCollection(items=items,completeness='partial'))
        assert assessment.qualified_analysis and not assessment.definitive_confirmation
        write('attribution-assessment.json',{
            'mode':'DETERMINISTIC_FULL_CATALOG_SCENARIO_NOT_LIVE_SELECTION',
            'selection_assumption':'All non-null catalog entries except expected_behavior; matches common mock policy, not an assertion about a future model.',
            'future_model_selection_known':False,'live_route_guaranteed':False,
            'assessment':assessment.model_dump(mode='json')})

        config={'model':MODEL,'input_per_million':'0.40','output_per_million':'1.60',
                'cached_input_per_million':'0.10','pricing_source':'https://developers.openai.com/api/docs/models/gpt-4.1-mini',
                'pricing_verified_at':DATE,'max_usd':'0.25','max_calls':5,'input_cap':65536,'output_cap':1536,
                'case_timeout_seconds':120,'call_timeout_seconds':20}
        write('proposed-config.json',config)
        try:LiveConfig(**config)
        except ValueError as exc:configuration_error=str(exc)
        else:raise AssertionError('Expected current LiveConfig to reject proposed 65536 input cap')
        assert configuration_error=='Invalid input cap'
        rate_in=Decimal(config['input_per_million']);rate_out=Decimal(config['output_per_million'])
        reserve=(rate_in*config['input_cap']+rate_out*config['output_cap'])/Decimal(1000000)
        maximum=reserve*config['max_calls']
        assert maximum==Decimal('0.14336') and maximum<Decimal(config['max_usd'])

        # Exact initial prompt is already recorded for these identical bytes.
        # No earlier model output exists at this stage. Cross-check it against
        # current protected prompts and deterministic catalog; no ask/agent call.
        historical=load(ROOT/'reports/week4/attributed-report-readiness-v2-paired-1/v2/model-calls.json')
        initial=historical[0]['messages']
        first_payload=json.loads(initial[-1]['content'].split('\n',1)[1])
        expected=redact(schemas.ClassifierInput(incident=typed.incident,**handle_catalog(typed.incident)))
        assert first_payload==expected
        assert initial[0]['content']==error_classifier.SYSTEM_PROMPT+SAFETY
        messages=[SystemMessage(content=initial[0]['content']),HumanMessage(content=initial[-1]['content'])]
        first_wire=strict_wire(schemas.ClassifierOutput,messages)
        def body(schema_name,messages,wire):
            return {'model':MODEL,'messages':[{'role':'system' if m['role']=='system' else 'user','content':m['content']} for m in messages],
                'temperature':0,'max_completion_tokens':config['output_cap'],'stream':False,'store':False,
                'response_format':{'type':'json_schema','json_schema':{'name':schema_name,'strict':True,'schema':wire}}}
        first_body=body('ClassifierOutput',initial,first_wire)
        write('first-request-preview.json',{'status':'EXACT_KNOWN_MESSAGES_AND_CURRENT_ADAPTER_API_PARAMETERS_NOT_SENT',
            'wire_body_preview':first_body,
            'service_tier_omitted_by_current_provider':True,
            'required_future_service_tier':'default',
            'json_serialization':'httpx2 compact UTF-8 JSON body convention; not an actual SDK dispatch',
            'body_bytes':len(json.dumps(first_body,ensure_ascii=False,separators=(',',':')).encode()),
            'source_record':'Existing V2 mock initial-request record, checked against current ClassifierInput/catalog/system prompt; no mock response imported.'})

        # Remaining requests are templates: no fabricated classifier, evidence,
        # hypotheses, diagnosis or proposed fix is supplied as a live result.
        alias_notice='\nUse the supplied short evidence handles in evidence ID reference fields. Copy evidence_contract and evidence_snapshot. Never invent mappings.'
        stages=[('log_investigator',log_investigator.LIVE_SYSTEM_PROMPT,schemas.LogInvestigatorInput,schemas.LiveLogInvestigatorOutput),
                ('root_cause_analyst',root_cause.SYSTEM_PROMPT,schemas.RootCauseAnalystInput,schemas.RootCauseAnalystOutput),
                ('resolution_generator',resolution.SYSTEM_PROMPT,schemas.ResolutionGeneratorInput,schemas.ResolutionGeneratorOutput),
                ('validator',validator.SYSTEM_PROMPT,schemas.ValidatorInput,schemas.ValidatorOutput)]
        templates=[]
        envelope=handle_catalog(typed.incident)
        for name,prompt,input_schema,output_schema in stages:
            dynamic={'classification':'Validated output from classifier; unknown before execution.'}
            if name!='log_investigator':
                dynamic.update(evidence='Validated selected evidence/completeness/gaps from investigator; unknown before execution.',
                    evidence_catalog='Actual selected-handle catalog, not predetermined full catalog.')
            if name=='root_cause_analyst':
                dynamic['analysis_readiness']='Recomputed V2 assessment of actual selected evidence, replacing only analyst advisory; legacy advisory retained. Live integration currently unsupported.'
            if name in ('resolution_generator','validator'):
                dynamic.update(hypotheses='Post-validation analyst hypotheses; unknown and may never exist.',
                               diagnosis='Post-validation diagnosis; unknown and may abstain.')
            if name=='validator':dynamic['proposed_fix']='Validated resolution output; unknown and may be absent.'
            known={'incident':raw['incident']}
            if name=='log_investigator':known.update(envelope)
            else:known['analysis_readiness']=({} if name!='root_cause_analyst' else 'DYNAMIC_V2_ADVISORY')
            templates.append({'stage':name,'status':'SYMBOLIC_TEMPLATE_NOT_RUNNABLE_NOT_PREDICTED_ROUTE',
                'system_prompt':prompt+(alias_notice if name!='log_investigator' else '')+SAFETY,
                'system_prompt_condition':'Short-handle notice is conditional on nonempty modern selected evidence.',
                'known_payload_fields':known,'dynamic_payload_fields':dynamic,
                'input_schema_template':input_schema.model_json_schema(),
                'output_schema_template':output_schema.model_json_schema(),
                'wire_schema_note':'Current strict_wire removes defaults, requires object properties, disallows extras and binds actual snapshot/handle enums at dispatch; later exact enums depend on earlier validated outputs.',
                'reachability':'Conditional on prior validated outputs and inherited routing; no skipped stage implies a call.'})
        write('later-request-templates.json',{'future_payloads_fully_known':False,'templates':templates})
        # A size-only historical scenario, never copied as a future live prompt.
        root_messages=historical[2]['messages']
        root_wire=strict_wire(schemas.RootCauseAnalystOutput,[
            SystemMessage(content=root_messages[0]['content']),HumanMessage(content=root_messages[-1]['content'])])
        replay_body=body('RootCauseAnalystOutput',root_messages,root_wire)
        replay_bytes=len(json.dumps(replay_body,ensure_ascii=False,separators=(',',':')).encode())
        limits={'calculation':'max_calls * (input_cap*input_rate + output_cap*output_rate) / 1000000',
            'currency':'USD','token_rate_unit':1000000,'cache_hit_assumption':False,
            'per_call_reservation_usd':str(reserve),'five_full_reservations_usd':str(maximum),
            'proposed_ceiling_usd':'0.25','headroom_usd':str(Decimal('0.25')-maximum),
            'scope':'Conditional capped-usage arithmetic at published model rates and default service tier; not an enforceable current-runner invoice guarantee.',
            'reasoning':'Selected documented model has no reasoning step. max_completion_tokens bounds total generated tokens including reasoning where applicable; completion_tokens is billed once at the output rate, never add reasoning twice.',
            'current_input_cap_max':32768,'proposed_input_cap':65536,
            'current_request_guard':'len(serialized HTTP request content)+4096 <= input_cap',
            'token_guard_status':'Byte/framing proxy, not verified pre-dispatch provider token metering; observed cap overruns are post-response failures.',
            'historical_all_selected_analyst_body_bytes':replay_bytes,
            'historical_all_selected_analyst_bytes_plus_allowance':replay_bytes+4096,
            'historical_size_scenario':'Recorded common-mock inputs only; size illustration, not a future analyst payload or semantic evidence.',
            'historical_scenario_fits_current_input_guard':replay_bytes+4096<=32768,
            'historical_scenario_fits_proposed_input_guard':replay_bytes+4096<=65536,
            'proposed_config_accepted_by_current_LiveConfig':False,
            'current_config_rejection':configuration_error}
        write('limits-and-cost.json',limits)

        # Static integration checks only; never call load_plan/run_smoke/run_case.
        smoke_source=(ROOT/'evaluation/week4/smoke.py').read_text()
        cli_source=(ROOT/'evaluation/week4/live_cli.py').read_text()
        provider_source=(ROOT/'evaluation/week4/live_provider.py').read_text()
        ast.parse(smoke_source);ast.parse(cli_source);ast.parse(provider_source)
        assert 'from graph.workflow import build_workflow' in smoke_source
        assert 'attributed_report_v2' not in smoke_source
        assert "plan.get('version')!='week4-smoke-plan-1'" in cli_source
        assert 'service_tier=' not in provider_source
        docs={'retrieved_date_utc':DATE,'raw_document_snapshots_saved':False,
            'account_discovery_performed':False,'official_sources':[
                {'url':'https://developers.openai.com/api/docs/models/gpt-4.1-mini','facts':{
                    'snapshot':MODEL,'chat_completions':True,'structured_outputs':True,'context_window':1047576,
                    'max_output_tokens':32768,'reasoning_step':False,'status':'deprecated',
                    'listed_usd_per_million':{'input':'0.40','cached_input':'0.10','output':'1.60'}}},
                {'url':'https://developers.openai.com/api/docs/deprecations','facts':{'model':MODEL,'scheduled_shutdown_date':'2027-01-14'}},
                {'url':'https://developers.openai.com/api/docs/guides/structured-outputs','facts':{'json_schema_strict_supported_for_compatible_models':True,'provider_schema_subset_still_requires_validation':True}},
                {'url':'https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create','facts':{
                    'temperature_zero_in_documented_range':True,'max_completion_tokens_includes_reasoning':True,
                    'omitted_service_tier_defaults_to_auto':True,'explicit_default_tier_uses_standard_pricing':True}},
                {'url':'https://developers.openai.com/api/docs/pricing','facts':{'pricing_mode_varies_by_service_tier':True,'no_tools_or_batch_discounts_assumed':True}}],
            'price_record_kind':'Local transcription of fetched official facts, not a raw-page hash or account quote.',
            'availability':'Documented deprecated model with future shutdown; actual project access/billing/tier unknown.'}
        write('official-docs.json',docs)
        worksheet={'version':'week4-real-016-v2-smoke-human-review-1','case_id':raw['case_id'],
            'reviewer':None,'reviewed_at':None,'independently_reproduced':None,'semantic_grades':None,
            'questions':{k:{'grade':None,'notes':None} for k in [
                'Evidence selection and resolvable grounding', 'Header-encoding diagnosis, if any',
                'Reporter attribution and causal uncertainty', 'Safe proposed diagnostic suggestions',
                'Unsupported claims or fabricated successful remediation']},
            'actual_run':{'run_id':None,'route':None,'terminal_status':None,'calls':None,'usage':None,
                'provider_usage_priced_cost_usd':None,'billing_uncertainty':None,'latency':None},
            'instruction':'A graceful hold or analyst entry is not diagnostic success. Do not fill grades until genuine post-run human review.'}
        write('review-worksheet.json',worksheet)
        source_paths=set()
        for folder in ('agents','models','tools','graph','diagnostic_contracts','evaluation/week4'):
            source_paths.update(p for p in (ROOT/folder).rglob('*.py') if '__pycache__' not in p.parts)
        source_paths.update(ROOT/p for p in ['requirements.lock','evaluation/week4/requirements.lock',
            'evaluation/week4/requirements.in','evaluation/week4/.python-version','docs/source-baseline-manifest.json',
            'scripts/week4_prepare_smoke016_v2_plan.py'])
        sources={str(p.relative_to(ROOT)):sha(p) for p in sorted(source_paths)}
        write('source-hashes.json',sources)
        policy_hashes={p:h for p,h in sources.items() if p.startswith('evaluation/week4/attributed_report_v2/')}
        blockers=[
            {'id':'V2_LIVE_PATH_UNSUPPORTED','evidence':'smoke.inference_worker uses graph.workflow.build_workflow directly and has no V2 workflow/advisory selector; V2 comparison supports deterministic model transport only.'},
            {'id':'NEW_PLAN_FORMAT_NOT_LOADABLE','evidence':'live_cli.load_plan accepts only week4-smoke-plan-1; the new version is intentionally incompatible. No V1/inherited fallback is permitted.'},
            {'id':'PROPOSED_INPUT_BOUND_UNSUPPORTED','evidence':'LiveConfig rejects 65536 (hard maximum 32768). Historical full-selection analyst request does not fit the current byte guard; do not trim required provenance or silently skip analysis.'},
            {'id':'SERVICE_TIER_AND_TOKEN_ENVELOPE_UNRESOLVED','evidence':'Provider omits service_tier (official API defaults to project auto) and journal does not validate returned tier. Input byte+4096 proxy is not provider-verified token metering.'},
            {'id':'ACCOUNT_ACCESS_AND_LIVE_SCHEMA_UNVERIFIED','evidence':'No authenticated model discovery or live schema submission authorized. Public support does not establish this account access or acceptance of every concrete dynamic wire schema.'},
        ]
        plan={'version':'week4-real-016-v2-live-smoke-proposal-1','status':'BLOCKED_NOT_READY_FOR_APPROVAL',
            'ready_for_approval':False,
            'execution_authorized':False,'trace_export_authorized':False,
            'approval_identity':None,'approval_time':None,
            'case_id':raw['case_id'],'case_count':1,'exposure':'Known development case; no holdout/golden claim',
            'policy':{'selected':'attributed-report-readiness-v2','fallback':False,'policy_files':policy_hashes,
                      'policy_files_digest':digest(policy_hashes)},
            'bindings':{'input_sha256':sha(INPUT),'sanitized_copy_sha256':sha(OUT/'sanitized-input.json'),
                'archive_sha256':sha(archive_path),'source_files_digest':digest(sources),
                'source_hashes_file_sha256':sha(OUT/'source-hashes.json'),
                'configuration_sha256':sha(OUT/'proposed-config.json'),
                'dependency_locks':{str(p):sources[str(p)] for p in map(Path,['requirements.lock','evaluation/week4/requirements.lock','evaluation/week4/requirements.in','evaluation/week4/.python-version'])},
                'assessment_sha256':sha(OUT/'attribution-assessment.json'),
                'first_request_preview_sha256':sha(OUT/'first-request-preview.json'),
                'later_templates_sha256':sha(OUT/'later-request-templates.json'),
                'pricing_record_sha256':sha(OUT/'official-docs.json')},
            'execution':{'command':None,'v2_live_command_supported':False,
                'existing_legacy_command_shape':'python -m evaluation.week4.live_cli run --plan OLD_FORMAT_PLAN --output NEW_DIR --execute-live (NOT COMPATIBLE WITH THIS PROPOSAL)',
                'existing_path':['live_cli.load_plan','smoke.run_smoke','supervise(smoke.inference_worker)','inherited graph.workflow.build_workflow','LiveModel','Journal'],
                'required_path':'Explicit V2 composition and scoped analyst advisory plus supported provider, durable reservations and process supervisor; currently not integrated.',
                'concurrency':1,'sdk_retries':0,'workflow_retries':0,'max_calls':5,
                'input_token_reservation_per_call':65536,'max_completion_tokens_per_call':1536,
                'combined_proposed_context_tokens':67072,'case_process_timeout_seconds':120,'network_phase_timeout_seconds':20,
                'external_diagnostic_tools':False,'external_tracing':False,'export_traces':False,'local_durable_spans':True},
            'model':{'selected_proposal':MODEL,'public_documentation_verified_on_utc':DATE,
                'documented_deprecated':True,'scheduled_shutdown_date':'2027-01-14',
                'account_access':'UNVERIFIED','revalidate_before_any_paid_run':True,'substitution_allowed':False},
            'budget':{'currency':'USD','proposed_max_usd':'0.25','maximum_full_reservations_usd':str(maximum),
                'enforceable_current_runner_guarantee':False,'no_cache_hits_assumed':True,
                'conditional_on':'Verified default service tier, accepted complete-request bound, exact snapshot/rates and future supported V2 live integration.',
                'actual_spend_usd':None},
            'credentials':{'required_dedicated_names':['WEEK4_OPENAI_API_KEY'],
                'langsmith_credentials_required':False,'do_not_load_original_credentials':True,
                'secret_values_read':False,'credential_files_opened':False,
                'future_worker_isolation':'Allowlist then clear environment; false ambient tracing flags; nonexistent local LangSmith SDK profile; fixed provider origin, trust_env=false, redirects disabled. Use a clean dedicated shell and omit all tracing credentials.'},
            'ambient_tracing_presence_check':before['ambient_tracing_flags'],
            'provenance':{'archive':'partial selected-excerpt transcription','association':'reporter-associated reproduction',
                'authenticated_request_correlation':False,'independent_reproduction':False,
                'model_selection_assumption':'Assessment uses deterministic full-catalog scenario only; actual live selection/readiness and later requests are unknown.'},
            'blockers':blockers,'human_review':'review-worksheet.json; all grades unset',
            'authorization_rule':'Any future paid run requires explicit user authorization tied to a supported, refreshed plan version and its exact hashes. This blocked proposal does not authorize execution or supersede the earlier smoke plan.',
            'no_runtime_changes_in_this_task':True}
        write('plan.json',plan)
        unchanged=all(sha(ROOT/p)==h for p,h in before['files'].items())
        assert unchanged and not any(guard.values())
        write('verification.json',{'status':'PASS_FOR_OFFLINE_PROPOSAL; LIVE_EXECUTION_BLOCKED',
            'baseline_files_checked':328,'protected_assets_checked':50,'preexisting_files_unchanged':len(before['files']),
            'prior_sealed_manifests':before['sealed'],'dependencies':dependencies,'sdk_or_network_or_command_attempts':dict(guard),
            'no_workflow_or_agent_or_smoke_invoked':True,'no_SDK_clients_initialized':True,
            'sanitization_unchanged':True,'inference_field_exclusion_check':True,'first_payload_and_system_match_current_code':True,
            'later_requests_symbolic_only':True,'deterministic_assessment_selection_conditional':True,
            'proposed_config_rejected_as_expected':configuration_error,
            'source_hashes_and_input_archive_bindings_checked':True,'budget_math_fits_proposed_ceiling':True,
            'current_execution_bound_support':False,'semantic_accuracy':None,'cost_usd':None})
        print(json.dumps({'status':plan['status'],'config_rejected':configuration_error,
              'conditional_max_usd':str(maximum),'historical_analyst_body_bytes':replay_bytes,
              'historical_plus_allowance':replay_bytes+4096,'guards':dict(guard),'preserved':len(before['files'])},indent=2))

if __name__=='__main__':main()
