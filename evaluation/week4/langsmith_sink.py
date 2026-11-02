"""Supported LangSmith Client only; explicit sanitized, post-inference delivery."""
from datetime import datetime
import requests
from urllib3.util.retry import Retry
from langsmith import Client, tracing_context
from tools.redaction import redact
from .contracts import BoundaryFailure

ENDPOINTS = {'https://api.smith.langchain.com', 'https://eu.api.smith.langchain.com',
             'https://apac.api.smith.langchain.com', 'https://aws.api.smith.langchain.com'}


def sdk_client(api_key, endpoint, *, session=None, workspace_id=None):
    if endpoint not in ENDPOINTS: raise BoundaryFailure('LangSmith endpoint not allowlisted')
    session = session or requests.Session()
    session.trust_env = False
    session.max_redirects = 0
    mock_adapters = session.adapters.copy() if getattr(session, 'week4_mock', False) else None
    client = Client(api_url=endpoint, api_key=api_key, session=session,
        auto_batch_tracing=False, retry_config=Retry(total=0), timeout_ms=5000,
        omit_traced_runtime_info=True, tracing_sampling_rate=1.0, tracing_mode="langsmith",
        workspace_id=workspace_id, hide_inputs=redact, hide_outputs=redact, hide_metadata=redact)
    # The SDK mounts its own HTTP adapter at construction. Restore only the
    # explicitly supplied OFFLINE test adapters, never a custom live transport.
    if mock_adapters:
        for prefix, adapter in mock_adapters.items(): session.mount(prefix, adapter)
    return client


def span_metadata(span, run_id):
    metadata = dict(span['metadata'])
    usage = metadata.pop('usage', None)
    if usage is not None:
        # Existing redaction treats any key containing "token" as sensitive.
        # Preserve numeric metering under explicit safe names, without weakening it.
        metadata['usage_counts'] = {k.replace('_tokens', '_units'): v for k,v in usage.items()}
    return redact({**metadata, 'week4_run_id':run_id, 'case_id':span['case_id'],
                   'local_span_id':span['span_id'], 'local_status':span['status']})


def numeric_usage(span):
    usage = span['metadata'].get('usage') or {}
    i, o = usage.get('input_tokens'), usage.get('output_tokens')
    return {'prompt_tokens':i, 'completion_tokens':o, 'total_tokens':i+o} if type(i) is int and type(o) is int else {}


def validate_tree(spans):
    ids = {s['span_id'] for s in spans}
    roots = [s for s in spans if s['kind']=='root']
    if len(roots)!=1 or len(ids)!=len(spans): raise BoundaryFailure('Exactly one root and unique spans required')
    for span in spans:
        if span['root_id'] != roots[0]['span_id'] or span['case_id'] != roots[0]['case_id']:
            raise BoundaryFailure('Mixed case/root linkage')
        if span['kind']!='root' and span['parent_id'] not in ids:
            raise BoundaryFailure('Missing parent span')
    return roots[0]


def match_runs(client, spans, *, run_id, project_id=None):
    root = validate_tree(spans)
    with tracing_context(enabled=False):
        for s in spans:
            run = client.read_run(s['span_id'], project_id=project_id,
                                  start_time=datetime.fromisoformat(s['start_time']))
            meta = span_metadata(s,run_id)
            remote = (run.extra or {}).get('metadata', {})
            if (str(run.id) != s['span_id'] or str(run.trace_id) != s['root_id'] or
                    (str(run.parent_run_id) if run.parent_run_id else None) != s['parent_id'] or
                    run.name != s['name'] or run.error != s['error'] or
                    run.inputs != redact(s['inputs']) or run.outputs != redact(s['outputs']) or
                    any(remote.get(k) != v for k,v in meta.items()) or
                    any(getattr(run,k) != v for k,v in numeric_usage(s).items()) or
                    run.start_time != datetime.fromisoformat(s['start_time']) or
                    run.end_time != datetime.fromisoformat(s['end_time'])):
                raise BoundaryFailure('Retrieved trace does not match local run/case/usage records')
    return {'status':'verified','root_id':root['span_id'],'matched_spans':len(spans),
            'case_id':root['case_id'],'run_id':run_id}


def export_and_match(client, spans, *, project, run_id, project_id=None):
    """Supported SDK create/read. No model invocation, automatic retry or fallback."""
    if not project: raise ValueError('Explicit project required')
    validate_tree(spans)
    with tracing_context(enabled=False):
        for s in spans:
            client.create_run(id=s['span_id'], trace_id=s['root_id'], parent_run_id=s['parent_id'],
                name=s['name'], inputs=redact(s['inputs']), outputs=redact(s['outputs']),
                run_type='llm' if s['kind']=='model' else 'tool' if s['kind']=='tool' else 'chain',
                project_name=project, start_time=datetime.fromisoformat(s['start_time']),
                end_time=datetime.fromisoformat(s['end_time']), error=s['error'],
                extra={'metadata':span_metadata(s,run_id)}, **numeric_usage(s))
    return match_runs(client, spans, run_id=run_id, project_id=project_id)
