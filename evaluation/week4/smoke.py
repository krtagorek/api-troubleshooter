"""Single-case process supervisor. Live calls/exports require explicit flags."""
import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import signal
from time import monotonic
from uuid import uuid4
from decimal import Decimal
from langsmith import tracing_context
from graph.state import AGENT_NAMES, initialize_state, serialize_state
from graph.workflow import build_workflow
from .runner import ROOT, FACTORIES, write_once, metadata, digest
from .contracts import InferenceCase, BoundaryFailure
from .accounting import Journal
from .durable_trace import DurableTrace, recover_spans
from .live_config import LiveConfig, V2, CASE016_BUDGET_PROFILE, SELECTION_V1, MANIFEST_BUDGET_PROFILE
from .live_provider import LiveModel
from .grading import worksheet
from .dependencies import verify_lock


def clean_environment(directory, *, external_tracing=False):
    # Dedicated Week 4 credentials only. Never load .env or Week 3 URLs/keys.
    allowed = {'PATH', 'HOME', 'TMPDIR', 'LANG', 'SYSTEMROOT', 'SSL_CERT_FILE', 'WEEK4_OPENAI_API_KEY'}
    if external_tracing:
        allowed |= {'WEEK4_LANGSMITH_API_KEY','WEEK4_LANGSMITH_PROJECT',
                    'WEEK4_LANGSMITH_PROJECT_ID','WEEK4_LANGSMITH_WORKSPACE_ID'}
    env = {k:v for k,v in os.environ.items() if k in allowed}
    os.environ.clear()
    os.environ.update(env)
    os.environ['LANGSMITH_CONFIG_FILE'] = str(Path(directory)/'no-sdk-profile.json')
    os.environ.update(LANGSMITH_TRACING='false', LANGCHAIN_TRACING_V2='false',
                      LANGCHAIN_TRACING='false', LANGSMITH_OTEL_ENABLED='false',
                      OTEL_SDK_DISABLED='true', OTEL_TRACES_EXPORTER='none',
                      DURABLE_WORKER_ENABLED='false', DIAGNOSTIC_CONTRACTS_ENABLED='false')


def inference_worker(raw_case, settings, directory, root_id, mode, scenario, trace_enabled):
    os.setsid()
    clean_environment(directory)
    if mode == 'offline_test':
        from .sdk_fixtures import block_network, model_transport
        block_network()
        transport = model_transport(directory, scenario)
        key = 'offline-test-placeholder'
    else:
        transport, key = None, os.environ['WEEK4_OPENAI_API_KEY']
    case = InferenceCase.model_validate(raw_case)
    config = LiveConfig(**settings)
    journal = Journal(directory)
    trace = DurableTrace(journal, case.case_id, root_id, enabled=trace_enabled)
    provider = LiveModel(config, journal, trace, key, transport=transport)
    workflow_factory = build_workflow
    agent_provider = provider
    if config.evidence_policy == V2:
        from .attributed_report_v2.workflow import build_workflow as v2_workflow, AnalystAdvisory
        workflow_factory = v2_workflow
        if config.reviewed_targets:
            from .attributed_report_v2.workflow import ReviewedAdvisories
            agent_provider = ReviewedAdvisories(agent_provider)
        agent_provider = AnalystAdvisory(agent_provider)
    state = initialize_state(case.incident, root_id, max_retries=0)
    coverage = {n:'not_reached' for n in AGENT_NAMES}
    selection_measurements = None
    error = None
    def wrap(name, factory):
        actual = factory(llm=agent_provider)
        def node(current):
            nonlocal state, selection_measurements
            state = current
            coverage[name] = 'started'
            journal.append({'event':'stage', 'name':name, 'status':'started'})
            try:
                with trace.span('node', name, {'incident_id': case.incident.incident_id}) as span:
                    result = actual(current)
                    span['outputs'] = result
                state = {**current, **result}
                if name == 'log_investigator' and config.evidence_policy == V2:
                    from .selection_metrics_v1 import measure
                    selection_measurements = measure(state['sanitized_inputs'], state['evidence'])
                    if config.reviewed_targets:
                        from .attributed_report_v2.workflow import clarification_context
                        selection_measurements['clarification_handoff'] = clarification_context(state)
                    journal.append({'event':'selection_measurements','measurement':selection_measurements})
                coverage[name] = 'completed'
                journal.append({'event':'stage', 'name':name, 'status':'completed'})
                return result
            except Exception:
                coverage[name] = 'failed'
                journal.append({'event':'stage', 'name':name, 'status':'failed'})
                raise
        return node
    try:
        with tracing_context(enabled=False), trace.span('root', 'week4.case', case.model_dump(mode='json')) as root:
            root['metadata'].update(config_sha256=digest(settings), input_sha256=digest(raw_case),
                                    mode=mode, model_requested=config.model)
            root['metadata']['evidence_policy'] = config.evidence_policy
            factories = FACTORIES
            if config.selection_policy == SELECTION_V1:
                from .attributed_selection_v1 import create_investigator
                if config.reviewed_targets:
                    from functools import partial
                    investigator = partial(create_investigator, explicit_selection_only=True)
                else:
                    investigator = create_investigator
                factories = {**FACTORIES, 'log_investigator': investigator}
            root['metadata']['selection_policy'] = config.selection_policy
            options = {'specific_clarification':True} if config.reviewed_targets else {}
            graph = workflow_factory(agents={n:wrap(n,f) for n,f in factories.items()}, trusted_semantics_enabled=False, **options)
            state = graph.invoke(state)
            if provider.fatal: raise provider.fatal
            root['outputs'] = json.loads(serialize_state(state))
            recorded_errors = [r['error'] for r in provider.receipts if r['error']]
            if recorded_errors:
                root.update(status='failed',error='RecordedModelFailure')
                root['metadata']['case_errors'] = recorded_errors
    except Exception as exc:
        error = type(provider.fatal or exc).__name__
    errors = list(dict.fromkeys([r['error'] for r in provider.receipts if r['error']] + ([error] if error else [])))
    write_once(Path(directory)/'child-result.json', {'case_id':case.case_id, 'root_id':root_id,
        'evidence_policy':config.evidence_policy,
        'selection_policy':config.selection_policy,'selection_measurements':selection_measurements,
        'terminal_status':'failed' if errors else 'held' if state['status']=='awaiting_evidence' else 'completed',
        'workflow_status':state['status'], 'errors':errors, 'stage_coverage':coverage,
        'output':json.loads(serialize_state(state)), 'receipts':provider.receipts})


def export_worker(directory, mode, scenario, project, run_id, endpoint, project_id, source_directory=None, retrieve_only=False):
    os.setsid()
    clean_environment(directory, external_tracing=True)
    from .langsmith_sink import sdk_client, export_and_match, match_runs
    from tools.redaction import install_redaction_filters
    install_redaction_filters()
    if mode == 'offline_test':
        from .sdk_fixtures import block_network, smith_session
        block_network()
        session, key = smith_session(directory, scenario), 'offline-test-placeholder'
    else:
        session, key = None, os.environ['WEEK4_LANGSMITH_API_KEY']
    client = None
    try:
        client = sdk_client(key, endpoint, session=session,
                           workspace_id=os.environ.get('WEEK4_LANGSMITH_WORKSPACE_ID'))
        spans = json.loads((Path(source_directory or directory)/'spans.json').read_text())
        result = (match_runs(client, spans, run_id=run_id, project_id=project_id) if retrieve_only else
                  export_and_match(client, spans, project=project, run_id=run_id, project_id=project_id))
    except Exception as exc:
        result = {'status':'TRACE_EXPORT_FAILED', 'error':type(exc).__name__}
    finally:
        if client: client.close(timeout=1)
    write_once(Path(directory)/'export-result.json', result)


def supervise(target, args, timeout):
    """Spawn a new session; terminate then kill its process group and verify gone."""
    process = multiprocessing.get_context('spawn').Process(target=target, args=args)
    process.start()
    terminal = None
    try:
        process.join(timeout)
        if process.is_alive(): terminal = 'timeout'
    except BaseException:
        terminal = 'interrupted'
    finally:
        # The child calls setsid before SDK work. Never signal the parent's group.
        try:
            own_group = os.getpgid(process.pid) == process.pid
        except ProcessLookupError:
            own_group = False
        if process.is_alive():
            if own_group: os.killpg(process.pid, signal.SIGTERM)
            else: process.terminate()
            process.join(1)
        if process.is_alive():
            if own_group: os.killpg(process.pid, signal.SIGKILL)
            else: process.kill()
            process.join(2)
        if process.is_alive(): raise BoundaryFailure('Child cleanup could not be verified')
        # Descendants must not survive even if the session leader has exited.
        try:
            os.killpg(process.pid, 0)
        except ProcessLookupError:
            pass
        else:
            os.killpg(process.pid, signal.SIGKILL)
            raise BoundaryFailure('Unexpected surviving process group was killed; inspect isolation')
    return {'terminal':terminal or ('exited' if process.exitcode==0 else 'interrupted'),
            'exit_code':process.exitcode, 'child_pid':process.pid, 'cleanup_verified':True}


def run_smoke(case, config, output_dir, *, mode='offline_test', scenario='hold',
              execute_live=False, export_traces=False, project=None,
              endpoint='https://api.smith.langchain.com', project_id=None, trace_enabled=True,
              plan_path=None):
    manifest_plan = None
    if config.budget_profile == MANIFEST_BUDGET_PROFILE:
        if plan_path is None:
            raise BoundaryFailure('Manifest case requires its bound batch plan')
        from .live_cli import load_plan, require_execution_authorization
        manifest_plan, checked = load_plan(plan_path)
        if checked != config:
            raise BoundaryFailure('Manifest case configuration mismatch')
        if mode == 'live': require_execution_authorization(manifest_plan)
        check_manifest_dispatch(manifest_plan, case, output_dir, mode)
        if export_traces: raise BoundaryFailure('Manifest tracing is local only')
    if config.evidence_policy == V2 and export_traces:
        raise BoundaryFailure('V2 external tracing/export is disabled')
    if mode not in ('offline_test', 'live'): raise ValueError('Invalid mode')
    # Manifest authorization/admission already ran above; the legacy gate owns
    # only the remaining single-case paths, not an authorized manifest case.
    if mode == 'live' and manifest_plan is None and (config.budget_profile == CASE016_BUDGET_PROFILE or config.selection_policy != 'off'):
        if plan_path is None:
            raise BoundaryFailure('Proposal-3 live ceiling requires its bound authorized plan')
        from .live_cli import load_plan, require_execution_authorization, PROPOSAL3, PAIR_ARM
        approved, checked = load_plan(plan_path)
        require_execution_authorization(approved)
        clean_case=InferenceCase.model_validate(case).model_dump(mode='json')
        if approved['version'] not in (PROPOSAL3,PAIR_ARM) or checked!=config or approved['case']!=clean_case:
            raise BoundaryFailure('Live case/configuration does not match authorized proposal')
        if approved['version'] == PAIR_ARM:
            from .paired_selection_plan_v1 import check_dispatch
            check_dispatch(approved, output_dir)
    if mode == 'live' and not execute_live:
        raise PermissionError('Explicit --execute-live required; paid execution is not currently authorized')
    if mode == 'live' and not os.environ.get('WEEK4_OPENAI_API_KEY'):
        raise ValueError('Dedicated WEEK4_OPENAI_API_KEY required')
    if export_traces:
        from .langsmith_sink import ENDPOINTS
        if endpoint not in ENDPOINTS: raise BoundaryFailure('LangSmith endpoint not allowlisted')
        if not project: raise ValueError('Explicit Week 4 LangSmith project required')
    if mode=='live' and export_traces and not os.environ.get('WEEK4_LANGSMITH_API_KEY'):
        raise ValueError('Dedicated WEEK4_LANGSMITH_API_KEY required')
    dependency_check = verify_lock()
    case = InferenceCase.model_validate(case)
    directory = Path(output_dir).resolve()
    if not directory.is_relative_to(ROOT): raise BoundaryFailure('Output must stay within new project')
    directory.mkdir(parents=True, exist_ok=False, mode=0o700)
    run_id, root_id = str(uuid4()), str(uuid4())
    meta = metadata(run_id, 'development-smoke', 'exposed-development-fixture-1')
    meta.update(dependency_check=dependency_check, mode=mode, config=config.public(), run_id=run_id, root_id=root_id,
                case_id=case.case_id, input_sha256=digest(case.model_dump(mode='json')),
                langsmith_project=project, langsmith_endpoint=endpoint)
    dataset_version = 'exposed-development-fixture-1'
    if manifest_plan:
        dataset_version = manifest_plan['dataset_manifest_sha256']
        meta.update(arm=manifest_plan['arm'], dataset_version=dataset_version,
                    dataset_manifest_sha256=dataset_version)
    write_once(directory/'experiment.json', meta)
    journal = Journal.create(directory, {**config.public(), 'mode':mode})
    started = monotonic()
    supervisor = supervise(inference_worker, (case.model_dump(mode='json'), config.public(),
                            str(directory), root_id, mode, scenario, trace_enabled), config.case_timeout_seconds)
    journal.append({'event':'case_terminal', **supervisor})
    child_path = directory/'child-result.json'
    if supervisor['terminal']=='exited' and child_path.exists():
        result = json.loads(child_path.read_text())
    else:
        result = {'case_id':case.case_id, 'root_id':root_id,
                  'terminal_status':supervisor['terminal'], 'errors':[supervisor['terminal']], 'output':None}
    events = journal.events()
    spans = recover_spans(events, result['terminal_status'])
    coverage = {n:'not_reached' for n in AGENT_NAMES}
    for event in events:
        if event['event']=='stage': coverage[event['name']] = event['status']
    attempted_ids = {e['call_id'] for e in events if e['event']=='attempt'}
    ended = {e['call_id']:e for e in events if e['event']=='call_end' and e['call_id'] in attempted_ids}
    leaf_seconds = sum(e['elapsed_seconds'] for e in ended.values())
    result.update(stage_coverage=coverage, accounting=journal.totals(events), mode=mode,
                  accounting_source='mock_test_data' if mode=='offline_test' else 'provider_usage_at_supplied_rates',
                  known_model_elapsed_seconds=leaf_seconds,
                  model_elapsed_seconds=leaf_seconds if len(ended)==len(attempted_ids) else None,
                  supervisor=supervisor, elapsed_seconds=monotonic()-started,
                  latency_boundary='before process start through reaping, fsynced terminal journal and reconciliation; excludes report/export',
                  semantic_quality=None)
    write_once(directory/'result.json', result)
    write_once(directory/'spans.json', spans)
    write_once(directory/'review.json', worksheet(case.case_id, dataset_version, root_id))
    trace_result = {'status':'not_requested'}
    if export_traces:
        export_started = monotonic()
        trace_supervisor = supervise(export_worker, (str(directory),mode,scenario,project,run_id,endpoint,project_id),30)
        path = directory/'export-result.json'
        trace_result = json.loads(path.read_text()) if path.exists() else {'status':'TRACE_EXPORT_FAILED'}
        trace_result.update(supervisor=trace_supervisor, elapsed_seconds=monotonic()-export_started)
    write_once(directory/'trace-status.json', trace_result)
    write_once(directory/'artifact-hashes.json', {p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                               for p in sorted(directory.iterdir()) if p.is_file()})
    for p in directory.iterdir(): p.chmod(0o400)
    directory.chmod(0o500)
    return result, trace_result


def _manifest_totals(rows):
    from .accounting import money
    known=sum((money(r.get('accounting',{}).get('known_cost_usd') or '0') for r in rows),Decimal(0))
    retained=sum((money(r.get('accounting',{}).get('retained_reservations_usd') or '0') for r in rows),Decimal(0))
    liability=sum((money(r.get('unknown_case_liability_bound_usd','0')) for r in rows),Decimal(0))
    reserved=sum(r.get('accounting',{}).get('reserved_calls') or 0 for r in rows)
    attempted=sum(r.get('accounting',{}).get('attempted_calls') or 0 for r in rows)
    unknown=any(r.get('accounting_uncertain') for r in rows)
    return {'reserved_call_slots':reserved,'attempted_model_calls':attempted,
            'known_cost_usd':str(known),'retained_reservations_usd':str(retained),
            'unknown_case_liability_bound_usd':str(liability),
            'unknown_call_slot_bound':sum(r.get('unknown_call_slot_bound',0) for r in rows),
            'accounted_ceiling_usd':str(known+retained+liability),
            'attempted_model_calls_complete':not unknown,
            'usage_priced_total_usd':str(known) if attempted and not retained and not unknown else None}


def _manifest_stop(result):
    accounting=result.get('accounting',{})
    errors=set(result.get('errors',[]))
    if errors.intersection({'BoundaryFailure','ResourceFailure','AccountingFailure'}):
        return 'security_resource_or_accounting_failure'
    if accounting.get('uncertain_calls') or accounting.get('limit_violations'):
        return 'uncertain_reservation_or_limit_violation'
    if not result.get('supervisor',{}).get('cleanup_verified'):
        return 'cleanup_not_verified'
    return None


def check_manifest_dispatch(plan, case, output_dir, mode):
    """Admission uses actual preceding case journals, never evaluator labels."""
    from .contracts import load_case_manifest, ResourceFailure, AccountingFailure
    from .accounting import money
    from .live_cli import authorization_identity
    config=LiveConfig(**plan['config'])
    _,cases=load_case_manifest(ROOT/plan['dataset_manifest_path'])
    directory=Path(output_dir).resolve(); batch=directory.parent.parent
    if not directory.is_relative_to(ROOT) or directory.parent.name!='cases':
        raise BoundaryFailure('Invalid manifest case output path')
    if mode=='live' and batch!=(ROOT/plan['output_path']).resolve():
        raise BoundaryFailure('Manifest output differs from approved location')
    meta=json.loads((batch/'batch-experiment.json').read_text())
    if meta['plan_identity']!=authorization_identity(plan) or meta['mode']!=mode:
        raise BoundaryFailure('Manifest run binding mismatch')
    ids=[c['case_id'] for c in cases]
    if case.get('case_id') not in ids: raise BoundaryFailure('Case not selected')
    index=ids.index(case['case_id'])
    if case!=cases[index] or directory.name!=case['case_id']:
        raise BoundaryFailure('Case bytes/identity differ from frozen input')
    prior=sorted((batch/'case-records').glob('*.json'))
    if len(prior)!=index: raise BoundaryFailure('Manifest cases must dispatch once in order')
    rows=[]
    for i,path in enumerate(prior):
        row=json.loads(path.read_text())
        if row['case_id']!=ids[i] or _manifest_stop(row):
            raise BoundaryFailure('Previous case cannot safely continue')
        child=batch/'cases'/row['case_id']
        hashes=json.loads((child/'artifact-hashes.json').read_text())
        if any(hashlib.sha256((child/name).read_bytes()).hexdigest()!=value for name,value in hashes.items()):
            raise BoundaryFailure('Previous supervised artifacts changed')
        actual=Journal(child).totals(Journal(child).events())
        if actual!=row['accounting']: raise AccountingFailure('Case accounting differs from durable journal')
        rows.append(row)
    totals=_manifest_totals(rows); bounds=plan['execution']
    reserve=(money(config.input_per_million)*config.input_cap+money(config.output_per_million)*config.output_cap)/money(1000000)
    if (totals['reserved_call_slots']+config.max_calls>bounds['max_calls'] or
        money(totals['accounted_ceiling_usd'])+reserve*config.max_calls>money(bounds['max_usd'])):
        raise ResourceFailure('Aggregate call/money budget exhausted before case dispatch')
    admission=json.loads((batch/'admissions'/f'{index:03d}.json').read_text())
    if admission!={'kind':'case_resource_admission_not_provider_call','case_id':case['case_id'],
                   'input_sha256':digest(case),'plan_identity':authorization_identity(plan)}:
        raise BoundaryFailure('Missing/mismatched case resource admission')


def run_manifest(plan_path, output_dir, *, mode='offline_test', execute_live=False, scenario='v2_mechanics'):
    """Sequential manifest extension of run_smoke; its supervisor owns each case.

    No second usage ledger: aggregate limits reconcile the same durable case
    journals. A fresh output directory prevents automatic retry/resume.
    """
    from .contracts import load_case_manifest, AccountingFailure, ResourceFailure
    from .live_cli import load_plan, require_execution_authorization, authorization_identity, MANIFEST_PLAN
    plan,config=load_plan(plan_path)
    if plan['version']!=MANIFEST_PLAN:raise BoundaryFailure('Not a case-manifest proposal')
    if mode not in ('offline_test','live'):raise ValueError('Invalid manifest mode')
    if mode=='live':
        if not execute_live:raise PermissionError('Explicit paid execution flag required')
        require_execution_authorization(plan)
    _,cases=load_case_manifest(ROOT/plan['dataset_manifest_path'])
    directory=Path(output_dir).resolve()
    if not directory.is_relative_to(ROOT) or (mode=='live' and directory!=(ROOT/plan['output_path']).resolve()):
        raise BoundaryFailure('Invalid manifest output')
    directory.mkdir(parents=True,exist_ok=False,mode=0o700)
    for name in ('cases','case-records','admissions'):(directory/name).mkdir()
    write_once(directory/'batch-experiment.json',{'version':MANIFEST_PLAN,'mode':mode,'arm':plan['arm'],
        'plan_identity':authorization_identity(plan),'dataset_manifest_sha256':plan['dataset_manifest_sha256'],
        'config':config.public(),'execution':plan['execution']})
    rows=[];stop=None
    for index,case in enumerate(cases):
        if stop:
            result={'case_id':case['case_id'],'terminal_status':'unattempted','errors':[stop],
                    'assigned':True,'attempted':False,'semantic_quality':None,'accounting':{},
                    'root_id':None,'output':None,'receipts':[],'mode':mode,
                    'stage_coverage':{n:'not_reached' for n in AGENT_NAMES},'stage_coverage_complete':True,
                    'elapsed_seconds':None,'model_elapsed_seconds':None}
        else:
            write_once(directory/'admissions'/f'{index:03d}.json',{'kind':'case_resource_admission_not_provider_call',
                'case_id':case['case_id'],'input_sha256':digest(case),'plan_identity':authorization_identity(plan)})
            try:
                result,_=run_smoke(case,config,directory/'cases'/case['case_id'],mode=mode,scenario=scenario,
                                   execute_live=execute_live,export_traces=False,trace_enabled=True,plan_path=plan_path)
                result.update(assigned=True,attempted=result['accounting']['attempted_calls']>0)
                stop=_manifest_stop(result)
            except Exception as exc:
                # No repeat of an interrupted case. Its fsynced journals remain
                # available; unknown accounting aborts all further dispatch.
                result={'case_id':case['case_id'],'terminal_status':'failed','errors':[type(exc).__name__],
                        'assigned':True,'attempted':False,'semantic_quality':None,'accounting':{},
                        'root_id':None,'output':None,'receipts':None,'mode':mode,
                        'stage_coverage':{n:'unknown' for n in AGENT_NAMES},'stage_coverage_complete':False,
                        'elapsed_seconds':None,'model_elapsed_seconds':None}
                child=directory/'cases'/case['case_id']
                if (child/'journal.jsonl').exists():
                    try:
                        result['accounting']=Journal(child).totals(Journal(child).events())
                        result['attempted']=result['accounting']['attempted_calls']>0
                    except Exception:
                        result.update(accounting_uncertain=True,attempted=None,
                            unknown_call_slot_bound=config.max_calls,unknown_case_liability_bound_usd=config.max_usd,
                            accounting={'reserved_calls':None,'attempted_calls':None,
                                'known_cost_usd':None,'retained_reservations_usd':None})
                stop=type(exc).__name__
        rows.append(result)
        write_once(directory/'case-records'/f'{index:03d}.json',result)
    totals=_manifest_totals(rows); attempted=sum(r['attempted'] is True for r in rows)
    summary={'batch_status':'stopped' if stop else 'finished','stop_reason':stop,'assigned_cases':len(rows),
             'attempted_cases':attempted,'unattempted_cases':sum(r['attempted'] is False for r in rows),
             'attempted_cases_unknown':sum(r['attempted'] is None for r in rows),
             'case_statuses':{r['case_id']:r['terminal_status'] for r in rows},'accounting':totals,
             'mean_usage_priced_cost_per_attempted_case_usd':str(Decimal(totals['usage_priced_total_usd'])/attempted)
                if attempted and totals['usage_priced_total_usd'] is not None else None,
             'accounting_source':'mock_test_data' if mode=='offline_test' else 'provider_receipts',
             'semantic_quality':None,'dataset_manifest_sha256':plan['dataset_manifest_sha256'],
             'latency_boundary':'Each case uses existing supervisor elapsed boundary; exclude manifest/preflight/report overhead. No unattempted zero-fill.'}
    write_once(directory/'batch-summary.json',summary)
    write_once(directory/'artifact-hashes.json',{str(p.relative_to(directory)):hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted(directory.rglob('*')) if p.is_file()})
    return summary


def trace_only(source_directory, output_dir, *, project, endpoint, project_id=None,
               export_traces=False, retrieve_traces=False):
    """Explicit future trace-only recovery: never imports/calls an inference worker."""
    verify_lock()
    if export_traces == retrieve_traces:
        raise PermissionError('Choose exactly one explicit export or retrieval action')
    source = Path(source_directory).resolve()
    directory = Path(output_dir).resolve()
    if not source.is_relative_to(ROOT) or not directory.is_relative_to(ROOT):
        raise BoundaryFailure('Trace artifacts must stay in new project')
    if not os.environ.get('WEEK4_LANGSMITH_API_KEY'):
        raise ValueError('Dedicated WEEK4_LANGSMITH_API_KEY required')
    meta = json.loads((source/'experiment.json').read_text())
    hashes = json.loads((source/'artifact-hashes.json').read_text())
    for name in ('experiment.json', 'spans.json'):
        if hashlib.sha256((source/name).read_bytes()).hexdigest()!=hashes[name]:
            raise BoundaryFailure('Source trace artifacts changed')
    directory.mkdir(parents=True, exist_ok=False, mode=0o700)
    supervisor = supervise(export_worker, (str(directory),'live','',project,meta['run_id'],endpoint,
                                           project_id,str(source),retrieve_traces),30)
    path = directory/'export-result.json'
    result = json.loads(path.read_text()) if path.exists() else {'status':'TRACE_EXPORT_FAILED'}
    result['supervisor'] = supervisor
    write_once(directory/'trace-status.json',result)
    return result
