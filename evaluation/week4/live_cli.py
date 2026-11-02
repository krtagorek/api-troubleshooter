"""Offline plan by default. Future live/export operations require explicit flags."""
import argparse
import json
import os
import hashlib
from datetime import date, datetime, timezone
from pathlib import Path
from .runner import ROOT, metadata, digest, write_once
from .fixtures import development_cases
from .accounting import money
from .dependencies import verify_lock
from .live_config import LiveConfig, V2, DEFAULT_BUDGET_PROFILE, CASE016_BUDGET_PROFILE, MANIFEST_BUDGET_PROFILE
from .smoke import run_smoke, trace_only, run_manifest

PROPOSAL3 = 'week4-real-016-v2-live-smoke-proposal-3'
PAIR_ARM = 'week4-real-016-v2-selection-pair-arm-1'
MANIFEST_PLAN = 'week4-case-manifest-evaluation-1'


def authorization_identity(plan):
    """Bind any future authorization to immutable proposal contents, not flags."""
    mutable = {'execution_authorized','approval_identity','approval_time',
               'approval_binding_sha256','status','ready_for_approval'}
    return digest({k:v for k,v in plan.items() if k not in mutable})


def require_execution_authorization(plan):
    if (plan.get('execution_authorized') is not True or
        not isinstance(plan.get('approval_identity'),str) or not plan['approval_identity'].strip() or
        not isinstance(plan.get('approval_time'),str) or not plan['approval_time'].strip()):
        raise ValueError('This plan has no explicit execution authorization')
    if plan.get('version') in (PROPOSAL3,PAIR_ARM,MANIFEST_PLAN) and plan.get('approval_binding_sha256') != authorization_identity(plan):
        raise ValueError('Authorization does not match proposal bindings')


def load_manifest_plan(plan):
    from .contracts import load_case_manifest, BoundaryFailure
    if plan.get('version') != MANIFEST_PLAN:
        raise BoundaryFailure('Unknown manifest plan')
    expected = metadata('manifest-preflight','manifest','frozen')['source_hashes']
    if plan.get('source_hashes') != expected:
        raise BoundaryFailure('Manifest proposal code/dependency bindings changed')
    config = LiveConfig(**plan['config'])
    if config.budget_profile != MANIFEST_BUDGET_PROFILE or digest(plan['config']) != plan['configuration_sha256']:
        raise BoundaryFailure('Manifest configuration binding changed')
    if plan.get('trace_export_authorized') is not False or plan.get('external_tracing') is not False:
        raise BoundaryFailure('Manifest evaluation cannot export traces')
    if plan.get('arm') not in ('baseline','improved'):
        raise BoundaryFailure('Explicit evaluation arm required')
    if plan['arm']=='baseline' and (config.evidence_policy!='inherited' or config.selection_policy!='off' or config.reviewed_targets):
        raise BoundaryFailure('Original baseline requires inherited graph/factories')
    if plan['arm']=='improved' and config.evidence_policy!=V2:
        raise BoundaryFailure('Improved arm requires explicit existing V2 composition')
    path=(ROOT/plan['dataset_manifest_path']).resolve()
    if not path.is_relative_to(ROOT) or hashlib.sha256(path.read_bytes()).hexdigest()!=plan['dataset_manifest_sha256']:
        raise BoundaryFailure('Frozen dataset manifest changed')
    manifest,cases=load_case_manifest(path)
    bounds=plan['execution']
    if (bounds.get('case_count')!=30 or bounds.get('concurrency')!=1 or bounds.get('retries')!=0 or
        bounds.get('external_diagnostic_tools') is not False or type(bounds.get('max_calls')) is not int or
        not 1<=bounds['max_calls']<=30*config.max_calls):
        raise BoundaryFailure('Invalid bounded manifest execution')
    reserve=(money(config.input_per_million)*config.input_cap+money(config.output_per_million)*config.output_cap)/money(1000000)
    if (reserve*config.max_calls>money(config.max_usd) or
        money(bounds['max_usd'])<reserve*bounds['max_calls'] or
        money(bounds['max_usd'])>30*money(config.max_usd)):
        raise BoundaryFailure('Manifest proposal does not fund bounded reservations')
    if (plan.get('not_after_utc_date')!='2027-01-13' or datetime.now(timezone.utc).date()>date(2027,1,13)):
        raise BoundaryFailure('Manifest proposal lifecycle window expired')
    verify_lock()
    return plan,config


def prepare_plan():
    case = development_cases()[0]
    return {'version':'week4-smoke-plan-1', 'status':'PROPOSED_NOT_AUTHORIZED',
        'case':case, 'case_sha256':digest(case), 'provenance':'Exposed V2 development issuer-canonicalization variant; not holdout or real incident',
        'source_hashes':metadata('proposed-smoke','development-smoke','development-fixtures-1')['source_hashes'],
        'dependency_check':verify_lock(),
        'config':{'model':None, 'input_per_million':None, 'output_per_million':None,
            'cached_input_per_million':None, 'pricing_source':None, 'pricing_verified_at':None,
            'max_usd':'0.25','max_calls':5,'input_cap':32768,'output_cap':1536,
            'case_timeout_seconds':120,'call_timeout_seconds':30},
        'execution':{'concurrency':1,'retries':0,'fallback':False,'external_diagnostic_tools':False,
                     'case_count':1,'external_trace_export':'NOT_AUTHORIZED'},
        'human_review':{'reviewer':None,'reviewed_at':None,'confirmed':None,'notes':None}}


def load_plan(path):
    plan = json.loads(Path(path).read_text())
    if plan.get('version') == MANIFEST_PLAN:
        return load_manifest_plan(plan)
    if plan.get('version') not in ('week4-smoke-plan-1','week4-real-016-v2-live-smoke-proposal-2',PROPOSAL3,PAIR_ARM) or digest(plan['case'])!=plan['case_sha256']:
        raise ValueError('Plan case/version changed; prepare a new plan')
    expected = metadata('proposed-smoke','development-smoke','development-fixtures-1')['source_hashes']
    if expected!=plan['source_hashes']:
        raise ValueError('Source/dependency hashes changed; prepare a new plan')
    config = LiveConfig(**plan['config'])
    if plan['version'] not in (PROPOSAL3,PAIR_ARM) and config.budget_profile != DEFAULT_BUDGET_PROFILE:
        raise ValueError('Older plans cannot use the proposal-3 ceiling')
    if plan['version'] != PAIR_ARM and config.selection_policy != 'off':
        raise ValueError('Selection treatment requires the new paired-arm plan')
    if plan['version'] in ('week4-real-016-v2-live-smoke-proposal-2',PROPOSAL3,PAIR_ARM):
        if (config.evidence_policy!=V2 or plan.get('evidence_policy')!=V2 or
            plan.get('trace_export_authorized') is not False or plan.get('external_tracing') is not False):
            raise ValueError('Explicit V2 policy and tracing-off identity required')
        if digest(plan['config']) != plan.get('configuration_sha256'):
            raise ValueError('Configuration binding changed')
        from .attributed_report_v2.archive import Archive
        packet=plan['case']['incident']['request_metadata']['report_attribution_v2']
        if packet['source_sha256'] != plan.get('archive_sha256'):
            raise ValueError('Archive binding changed')
        Archive().load(packet['source_sha256'])
    if plan['version'] in (PROPOSAL3,PAIR_ARM):
        from .contracts import InferenceCase
        case=InferenceCase.model_validate(plan['case'])
        if (config.budget_profile != CASE016_BUDGET_PROFILE or money(config.max_usd)!=money('2.25') or
            case.case_id!='W4-REAL-016' or case.incident.incident_id!='W4-REAL-016'):
            raise ValueError('Proposal-3 case/ceiling identity mismatch')
        if (plan.get('not_after_utc_date') != '2027-01-13' or
            datetime.now(timezone.utc).date() > date(2027,1,13)):
            raise ValueError('Proposal lifecycle window expired or mismatched')
        components=plan.get('component_hashes',{})
        if not components or plan.get('input_path') not in components:
            raise ValueError('Proposal component bindings required')
        for relative, expected_hash in components.items():
            component=(ROOT/relative).resolve()
            if (not component.is_relative_to(ROOT/'data/week4') or component.suffix!='.json' or not component.is_file() or
                hashlib.sha256(component.read_bytes()).hexdigest()!=expected_hash):
                raise ValueError('Proposal component binding changed')
        input_path=(ROOT/plan['input_path']).resolve()
        if (hashlib.sha256(input_path.read_bytes()).hexdigest()!=plan['input_bytes_sha256'] or
            json.loads(input_path.read_text())!=plan['case']):
            raise ValueError('Sanitized input binding changed')
        if plan['version'] == PAIR_ARM:
            from .paired_selection_plan_v1 import validate_arm
            validate_arm(plan)
    reservation = (money(config.input_per_million)*config.input_cap +
                   money(config.output_per_million)*config.output_cap)/money(1000000)
    if reservation*config.max_calls > money(config.max_usd):
        raise ValueError('Plan cannot fund its maximum calls at full reservations; revise before dispatch')
    return plan, config


def main():
    parser = argparse.ArgumentParser(description='Week 4 single smoke: plan offline; live/export require future authorization')
    subs = parser.add_subparsers(dest='command',required=True)
    prepare = subs.add_parser('plan');prepare.add_argument('--output',type=Path,required=True)
    run = subs.add_parser('run');run.add_argument('--plan',type=Path,required=True)
    run.add_argument('--output',type=Path,required=True)
    run.add_argument('--execute-live',action='store_true');run.add_argument('--export-traces',action='store_true')
    batch = subs.add_parser('run-manifest',help='Existing case supervisor over a frozen manifest; no implicit authorization')
    batch.add_argument('--plan',type=Path,required=True);batch.add_argument('--output',type=Path,required=True)
    batch.add_argument('--execute-live',action='store_true')
    trace = subs.add_parser('trace-only');trace.add_argument('--source',type=Path,required=True)
    trace.add_argument('--output',type=Path,required=True)
    trace.add_argument('--export-traces',action='store_true');trace.add_argument('--retrieve-traces',action='store_true')
    for p in (run,trace):
        p.add_argument('--langsmith-endpoint',default='https://api.smith.langchain.com')
    args = parser.parse_args()
    if args.command=='plan':
        path = args.output.resolve()
        if not path.is_relative_to(ROOT): raise ValueError('Plan must stay in new project')
        write_once(path,prepare_plan())
        print('Prepared unresolved plan; no paid call or external trace operation authorized/executed.')
        return 0
    if args.command=='run-manifest':
        if not args.execute_live:parser.error('--execute-live and separately authorized bound baseline proposal required')
        result=run_manifest(args.plan,args.output,mode='live',execute_live=True)
        print(json.dumps(result,indent=2))
        return 0 if result['batch_status']=='finished' else 1
    project = os.environ.get('WEEK4_LANGSMITH_PROJECT')
    project_id = os.environ.get('WEEK4_LANGSMITH_PROJECT_ID')
    if args.command=='run':
        if not args.execute_live: parser.error('--execute-live requires future explicit paid authorization')
        plan,config = load_plan(args.plan)
        if config.evidence_policy == V2:
            if args.export_traces:
                parser.error('V2 external tracing/export disabled')
            try:require_execution_authorization(plan)
            except ValueError as exc:parser.error(str(exc))
        result,tracing = run_smoke(plan['case'],config,args.output,mode='live',
            execute_live=args.execute_live,export_traces=args.export_traces,project=project,
            endpoint=args.langsmith_endpoint,project_id=project_id,plan_path=args.plan)
        print(json.dumps({'terminal_status':result['terminal_status'],'accounting':result['accounting'],'trace':tracing},indent=2))
        return 1 if result['terminal_status'] not in ('held','completed') or tracing['status']=='TRACE_EXPORT_FAILED' else 0
    result = trace_only(args.source,args.output,project=project,endpoint=args.langsmith_endpoint,
                        project_id=project_id,export_traces=args.export_traces,retrieve_traces=args.retrieve_traces)
    print(json.dumps(result,indent=2))
    return 0 if result['status']=='verified' else 1

if __name__=='__main__': raise SystemExit(main())
