"""Bounded real-input workflow mechanics only; SDK-free deterministic model stub.

Run inside the documented OS network-deny sandbox. No credential reads, endpoint
commands, evaluator answers or source resolutions are supplied to the graph.
"""
import argparse
from contextlib import ExitStack,contextmanager
import hashlib
import json
import os
from pathlib import Path
import sys
from time import monotonic
from uuid import uuid4

ROOT=Path(__file__).resolve().parents[1]
EXPECTED=tuple(f'W4-REAL-{i:03d}' for i in (5,6,8,9,*range(11,21)))
CONFIG={'version':'real-mechanics-mock-1','mode':'MOCKED_GRAPH_MECHANICS',
    'classifier':'unknown, confidence zero; no diagnostic classification',
    'investigator':'Select all supplied non-null catalog leaves except expected_behavior; partial completeness.',
    'analyst':'If inherited gates reach it, return inconclusive with no hypotheses or causal claims.',
    'resolution':'If reached, abstain without proposing a fix.',
    'validator':'If reached, return NOT_TESTED with no checks.',
    'max_calls_per_case':5,'workflow_retries':0,'case_timeout_seconds':30,
    'concurrency':1,'external_tools':False,'external_tracing':False,
    'mock_input_tokens_per_call':1,'mock_output_tokens_per_call':1,
    'cost_usd':None,'semantic_quality':None,'branch_targeting':False}


def sha(data):return hashlib.sha256(data).hexdigest()

def write(path,value):
    with Path(path).open('x') as f:
        os.chmod(path,0o600);json.dump(value,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())


def clear_environment():
    # Clear without fetching any credential values; child executable uses sys.executable.
    os.environ.clear()
    os.environ.update(LANGSMITH_TRACING='false',LANGCHAIN_TRACING_V2='false',
        DIAGNOSTIC_CONTRACTS_ENABLED='false',DURABLE_WORKER_ENABLED='false')


@contextmanager
def offline_guard(*,worker=False):
    """Defense in depth under sandbox-exec deny network*, including spawned workers."""
    from unittest.mock import patch
    counts={'network_attempts_blocked':0,'sdk_initializations_blocked':0,'command_attempts_blocked':0}
    def deny_network(*a,**k):
        counts['network_attempts_blocked']+=1;raise RuntimeError('OFFLINE_NETWORK_BOUNDARY')
    def deny_client(*a,**k):
        counts['sdk_initializations_blocked']+=1;raise RuntimeError('OFFLINE_SDK_CONSTRUCTION_BOUNDARY')
    def deny_command(*a,**k):
        counts['command_attempts_blocked']+=1;raise RuntimeError('OFFLINE_COMMAND_BOUNDARY')
    with ExitStack() as stack:
        for name in ('socket.socket.connect','socket.socket.connect_ex','socket.socket.sendto',
                     'socket.socket.sendmsg','socket.getaddrinfo','socket.create_connection'):
            stack.enter_context(patch(name,deny_network))
        # Imports construct no clients. Block every constructor the supported path can use.
        import openai,langsmith
        from langchain_openai import ChatOpenAI
        for cls in (openai.OpenAI,openai.AsyncOpenAI,openai.AzureOpenAI,openai.AsyncAzureOpenAI,
                    langsmith.Client,langsmith.AsyncClient,ChatOpenAI):
            stack.enter_context(patch.object(cls,'__init__',deny_client))
        if worker:
            for name in ('subprocess.Popen','os.system','os.popen','os.execv','os.execve','os.execl',
                         'os.execlp','os.execvp','os.execvpe','os.posix_spawn','os.posix_spawnp'):
                stack.enter_context(patch(name,deny_command))
        yield counts


def asset_paths():
    paths=sorted((ROOT/'data/week4/reviewed-candidates').rglob('*.json'))
    return paths+[ROOT/'data/week4/candidate-inventory.csv',ROOT/'data/week4/smoke-plan.json']


def fingerprint():return {str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in asset_paths()}


def verify_baseline():
    path=ROOT/'docs/source-baseline-manifest.json';m=json.loads(path.read_text())
    errors=[e['destination_relative_path'] for e in m['files'] if
        sha((ROOT/e['destination_relative_path']).read_bytes())!=e['sha256'] or
        (ROOT/e['destination_relative_path']).stat().st_size!=e['bytes']]
    if len(m['files'])!=328 or errors:raise RuntimeError('Inherited baseline verification failed: '+str(errors))
    return {'checked':328,'mismatches':errors,'manifest_sha256':sha(path.read_bytes())}


def preflight():
    baseline=verify_baseline()  # Must precede model/graph execution.
    assets=fingerprint()
    root=ROOT/'data/week4/reviewed-candidates'
    assessments=[json.loads((root/'runtime-assessment.json').read_text())]+[
        json.loads((root/f'batch-{b}/runtime-assessment.json').read_text()) for b in ('006-010','011-015','016-020')]
    eligible=[];excluded=[]
    for report in assessments:
        for row in report['cases']:
            ident=row['case_id'];status=row.get('runtime_result',row.get('status'))
            (eligible if status=='INPUT_COMPATIBLE_NOT_EXECUTED' else excluded).append(ident)
    if tuple(sorted(eligible))!=EXPECTED:raise RuntimeError('Recorded eligibility disagrees with expected list')
    from evaluation.week4.contracts import InferenceCase
    inputs={};goals={};paths={}
    for ident in eligible:
        matches=list(root.rglob('inference/'+ident+'.json'))
        if len(matches)!=1:raise RuntimeError('Missing/duplicate inference file: '+ident)
        raw=json.loads(matches[0].read_text())
        typed=InferenceCase.model_validate(raw).model_dump(mode='json')
        if typed!=raw:raise RuntimeError('Input projection changed at preflight: '+ident)
        text=json.dumps(raw)
        for key in ('human_review','accepted_expected_behavior','proposed_review','source_url','source_date','family','proposed_stratum'):
            if '"'+key+'"' in text:raise RuntimeError('Evaluator field in inference input')
        inputs[ident]=raw;goals[ident]={'expected_behavior':raw['incident']['expected_behavior'],
            'newly_approved':False,'status':'Existing editorial mapping; unresolved intent retained where stated.'}
        paths[ident]=str(matches[0].relative_to(ROOT))
    return {'baseline':baseline,'asset_hashes':assets,'eligible_ids':list(EXPECTED),
            'excluded_ids':sorted(excluded),'goals':goals,'input_paths':paths,
            'leakage_inspection':'Fields and actual prose inspected; no evaluator answers, resolutions, families or rubric supplied.',
            'intent_notes':{'W4-REAL-005':'Path-only, omitted host; neutral completion goal editorial.',
                'W4-REAL-013':'Informative rejection, not PUT success.',
                'W4-REAL-016':'Appropriate error handling, not claimed repair or a forced status.',
                'W4-REAL-020':'Proxy/direct intent unspecified; transfers and earlier-attempt logs kept distinct.'}},inputs


class DeterministicModel:
    """Only the existing StructuredLLM injection boundary is mocked; no SDK client."""
    def __init__(self,trace,*,fail_first=False):
        self.trace=trace;self.receipts=[];self.fatal=None;self.fail_first=fail_first
    def with_structured_output(self,schema,**options):
        owner=self
        class Structured:
            def invoke(self,messages):
                from evaluation.week4.contracts import ResourceFailure
                if len(owner.receipts)>=CONFIG['max_calls_per_case']:
                    owner.fatal=ResourceFailure('Mock call ceiling exhausted');raise owner.fatal
                started=monotonic()
                receipt={'schema':schema.__name__,'source':'mock_test_data','mocked':True,
                    'input_tokens':1,'output_tokens':1,'elapsed_seconds':0,'error':None,
                    'messages':[{'role':m.type,'content':m.content} for m in messages]}
                owner.receipts.append(receipt)
                try:
                    with owner.trace.span('model',schema.__name__):
                        payload=json.loads(messages[-1].content.split('\n',1)[1])
                        name=schema.__name__
                        if owner.fail_first and len(owner.receipts)==1:raise ValueError('SYNTHETIC MOCK FAILURE')
                        if name=='ClassifierOutput':
                            output={'classification':{'category':'unknown','confidence':0,
                                'reasoning':'MOCKED mechanics run; no diagnostic classification or causal claim.'}}
                        elif name=='LiveLogInvestigatorOutput':
                            selected=[];omitted=[]
                            for e in payload['evidence_catalog']:
                                if e['reference']=='/expected_behavior':reason='Editorial user goal, not an observed diagnostic measurement.'
                                elif e['value_type']=='null':reason='Unknown/default null is not a captured observation.'
                                else:selected.append(e['handle']);continue
                                omitted.append({'handle':e['handle'],'reference':e['reference'],'reason':reason})
                            output={'evidence_contract':payload['evidence_contract'],'evidence_snapshot':payload['evidence_snapshot'],
                                'selected_evidence_handles':selected,'completeness':'partial',
                                'diagnostic_gaps':[{'description':'MOCKED completeness assessment; no independent observations were collected.',
                                    'required_to_resolve':'Provide additional sanitized incident evidence for human review.'}]}
                            receipt['omitted_catalog_entries']=omitted
                        elif name=='RootCauseAnalystOutput':
                            output={'hypotheses':[],'diagnosis':{'status':'inconclusive','confidence':0,
                                'summary':'MOCKED mechanics run; no causal diagnosis assigned.',
                                'uncertainty':['MOCKED response; causal quality is not evaluated.']}}
                        elif name=='ResolutionGeneratorOutput':
                            output={'proposed_fix':None,'abstention_reason':'MOCKED: no supported remediation established.'}
                        elif name=='ValidatorOutput':
                            output={'validation':{'status':'NOT_TESTED','checks':[],
                                'issues':['MOCKED; no tool or fix was executed.'],'retry_recommended':False}}
                        else:raise ValueError('Unexpected model schema')
                        parsed=schema.model_validate(output)
                        receipt['response']=parsed.model_dump(mode='json')
                        return parsed
                except Exception as exc:
                    receipt['error']=type(exc).__name__;raise
                finally:receipt['elapsed_seconds']=monotonic()-started
        return Structured()


def recorder():
    from langchain_core.callbacks import BaseCallbackHandler
    class Recorder(BaseCallbackHandler):
        def __init__(self):self.events=[];self.runs={};self.path=[];self.decisions=[];self.graph_input=None
        def on_chain_start(self,serialized,inputs,*,run_id,parent_run_id=None,metadata=None,**kw):
            name=kw.get('name') or (serialized or {}).get('name');node=(metadata or {}).get('langgraph_node')
            self.runs[run_id]=(name,node)
            self.events.append({'kind':'start','run_id':str(run_id),'parent_id':str(parent_run_id) if parent_run_id else None,'name':name,'graph_node':node})
            if name==node and node:
                self.path.append(node)
                if node=='initialize' and self.graph_input is None:
                    value=inputs['sanitized_inputs'];self.graph_input=value.model_dump(mode='json') if hasattr(value,'model_dump') else value
        def on_chain_end(self,outputs,*,run_id,**kw):
            name,node=self.runs.get(run_id,(None,None))
            if isinstance(outputs,str) and name and ('route' in name or name=='validation_route'):
                self.decisions.append({'router':name,'from_node':node,'returned':outputs,'source':'actual callback return'})
            self.events.append({'kind':'end','run_id':str(run_id),'name':name,'graph_node':node})
        def on_chain_error(self,error,*,run_id,**kw):
            name,node=self.runs.get(run_id,(None,None))
            self.events.append({'kind':'error','run_id':str(run_id),'name':name,'graph_node':node,'error':type(error).__name__})
    return Recorder()


def worker(raw,directory,namespace,scenario='normal'):
    os.setsid();clear_environment()
    with offline_guard(worker=True) as guard:
        from dataclasses import asdict
        from evaluation.week4.runner import run_case
        from evaluation.week4.contracts import InferenceCase
        from evaluation.week4.tracing import FakeTracingSink
        from evaluation.week4.grading import grounding_checks,structural_checks
        from tools.diagnostic_sufficiency import readiness
        from graph.state import serialize_state,validate_state
        from tools.evidence_catalog import build_catalog,resolve_handles
        from tools.redaction import redact
        capture={};gates=[];events=recorder()
        def provider_factory(trace):
            if scenario=='timeout':
                import time
                time.sleep(60)
            capture['model']=DeterministicModel(trace,fail_first=scenario=='failure')
            return capture['model']
        def observer(name,state):
            if name=='log_investigator':
                ready=readiness(state['sanitized_inputs'],state['evidence'])
                gates.append({'after_agent':name,'readiness':asdict(ready),
                    'selected_evidence':state['evidence'].model_dump(mode='json'),
                    'influence':'Selection/completeness are mocked; readiness is inherited deterministic code.'})
        result,spans,receipts,fatal=run_case(InferenceCase.model_validate(raw),namespace,None,FakeTracingSink(),
            provider_factory=provider_factory,callbacks=[events],node_observer=observer)
        row=result.model_dump(mode='json');state=result.output
        input_observed=events.graph_input or (state or {}).get('sanitized_inputs')
        preservation={'supplied_vs_initial_graph_input':raw['incident']==input_observed,
            'initial_vs_terminal_input':input_observed==(state or {}).get('sanitized_inputs'),
            'defaults_added':{k:v for k,v in (input_observed or {}).items() if k not in raw['incident']},
            'unknown_defaults_already_in_projection':{k:raw['incident'].get(k) for k in
                ('severity','evidence_quality','response_body','logs')},'evidence_loss':[] if raw['incident']==input_observed else ['Input differs; inspect artifact.']}
        selection_checks=[]
        for receipt in receipts:
            if receipt['schema']=='LiveLogInvestigatorOutput' and 'response' in receipt:
                payload=json.loads(receipt['messages'][-1]['content'].split('\n',1)[1]);o=receipt['response']
                entries=resolve_handles(payload['incident'],o['selected_evidence_handles'],o['evidence_contract'],o['evidence_snapshot'])
                selection_checks=[{'handle':h,'reference':e.reference,'evidence_id':e.evidence_id,
                    'observation':e.observation,'source':e.source,'correct_case':payload['incident']['incident_id']==raw['incident']['incident_id']}
                    for h,e in zip(o['selected_evidence_handles'],entries)]
        contract={'state_valid':False,'validation_not_claimed':False}
        if state is not None:
            validate_state(state);contract['state_valid']=True
            contract['validation_not_claimed']=all(v['status']=='NOT_TESTED' and not v['checks'] for v in state['validation_results'])
        row.update(mode='MOCKED_GRAPH_MECHANICS',all_model_responses_mocked=True,
            semantic_quality=None,usage_priced_cost_usd=None,
            actual_ordered_graph_path=events.path,actual_router_returns=events.decisions,
            input_preservation=preservation,selected_handle_checks=selection_checks,
            grounding=grounding_checks(result),span_structure=structural_checks(result,spans,receipts),
            gate_observations=gates,final_contract=contract,
            retries=(state or {}).get('retry_counts'),fatal_error=type(fatal).__name__ if fatal else None,
            unsupported_mock_claims='No new causal, API-observation, remediation or validation claims by construction; semantic quality ungraded.',
            security=dict(guard))
        if any(guard.values()):row['terminal_status']='security_stop'
        write(Path(directory)/'result.json',row)
        write(Path(directory)/'spans.json',{'mode':'MOCKED_GRAPH_MECHANICS','spans':spans})
        write(Path(directory)/'model-calls.json',{'mode':'MOCKED_GRAPH_MECHANICS','calls':receipts})
        write(Path(directory)/'graph-events.json',{'mode':'MOCKED_GRAPH_MECHANICS','events':events.events})


def finalize(directory):
    files=sorted(p for p in directory.rglob('*') if p.is_file())
    write(directory/'artifact-hashes.json',{str(p.relative_to(directory)):sha(p.read_bytes()) for p in files})
    for p in directory.rglob('*'):
        if p.is_file():p.chmod(0o400)
    for p in sorted([p for p in directory.rglob('*') if p.is_dir()],key=lambda p:len(p.parts),reverse=True):p.chmod(0o500)
    directory.chmod(0o500)


def run(output,*,test_scenarios=None,timeout=None):
    clear_environment()
    with offline_guard() as parent_guard:
        from evaluation.week4.smoke import supervise  # Process control only; NO run_smoke/client construction.
        from evaluation.week4.dependencies import verify_lock
        pre,inputs=preflight();dependencies=verify_lock()
        directory=Path(output).resolve()
        if not directory.is_relative_to(ROOT):raise ValueError('Output must stay in new project')
        directory.mkdir(parents=True,exist_ok=False,mode=0o700)
        write(directory/'preflight.json',pre)
        namespace=str(uuid4())
        source_paths=sorted((ROOT/'evaluation/week4').rglob('*.py'))+[Path(__file__).resolve()]
        write(directory/'experiment.json',{'version':'week4-real-mock-1','run_id':namespace,'config':CONFIG,
            'dependencies':dependencies,'runner_source_hashes':{str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in source_paths},
            'os_network_boundary':'sandbox-exec deny network* required by documented invocation; Python guards also active.'})
        results=[];stopped=False
        for ident in EXPECTED:
            case_dir=directory/ident;case_dir.mkdir(mode=0o700)
            if stopped:
                row={'case_id':ident,'terminal_status':'unattempted_security_stop'};write(case_dir/'result.json',row)
            else:
                started=monotonic()
                control=supervise(worker,(inputs[ident],str(case_dir),namespace,(test_scenarios or {}).get(ident,'normal')),
                                  timeout or CONFIG['case_timeout_seconds'])
                rp=case_dir/'result.json'
                row=json.loads(rp.read_text()) if rp.exists() else {'case_id':ident,'terminal_status':control['terminal'],
                    'errors':[control['terminal']],'semantic_quality':None,'usage_priced_cost_usd':None}
                row={**row,'supervisor':control,'supervised_elapsed_seconds':monotonic()-started}
                write(case_dir/'supervised-result.json',row)
                stopped=row['terminal_status']=='security_stop' or any(parent_guard.values())
            results.append(row)
        after=fingerprint();baseline_after=verify_baseline()
        same=pre['asset_hashes']==after
        totals={'scope':'Local imported real cases 001–020; mechanical mocks only',
            'human_accepted':20,'evidence_preserving_input_compatible':14,'schema_pass_including_damaged_007':15,
            'mocked_graph_attempted_this_run':sum(bool(r.get('root_id')) for r in results),
            'mocked_graph_safely_terminated':sum(r['terminal_status'] in ('held','completed') for r in results),
            'mocked_graceful_holds':sum(r['terminal_status']=='held' for r in results),
            'mocked_full_workflow_completions':sum(r.get('workflow_status')=='completed' for r in results),
            'live_graph_execution':0,'golden_set_ready':0,'semantic_quality':None,'cost_usd':None,
            'earlier_external_usage':'unknown; no independent holdout claim'}
        summary={'mode':'MOCKED_GRAPH_MECHANICS','assigned':len(EXPECTED),'results':[
                {'case_id':r['case_id'],'termination':r['terminal_status'],'route':r.get('actual_ordered_graph_path'),
                 'model_calls':(r.get('usage') or {}).get('model_calls')} for r in results],
            'cumulative_counts':totals,'asset_hashes_unchanged':same,'baseline_after':baseline_after,
            'parent_security':dict(parent_guard),'child_security':{r['case_id']:r.get('security') for r in results},
            'input_hashes_after':after,'model_calls':sum((r.get('usage') or {}).get('model_calls',0) for r in results),
            'cost_usd':None,'semantic_quality':None,'trace_exports':0,'external_requests':0,
            'limitations':'No semantic grading, live provider/SDK behavior, remediation or golden qualification. Holds are not full diagnostic completions.'}
        write(directory/'summary.json',summary);write(directory/'cumulative-counts.json',totals)
        finalize(directory)
        if not same:raise RuntimeError('Reviewed/reference/input artifact hashes changed')
        return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();summary=run(args.output)
    print(json.dumps({k:summary[k] for k in ('assigned','model_calls','cumulative_counts','asset_hashes_unchanged','baseline_after')},indent=2))
