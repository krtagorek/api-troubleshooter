"""Create-only offline batches invoking inherited factories and guarded graph."""
import hashlib
import importlib.metadata
import json
import os
import math
from pathlib import Path
from time import monotonic
from dataclasses import asdict
from typing import Callable
from uuid import uuid4
from langsmith import tracing_context
from pydantic import ValidationError
from agents import error_classifier, log_investigator, root_cause, resolution, validator
from agents.common import AgentOutputError
from graph.state import AGENT_NAMES, initialize_state, serialize_state
from graph.workflow import build_workflow
from .contracts import (InferenceCase, CaseResult, Usage, BoundaryFailure,
                        ResourceFailure, AccountingFailure, check_inference)
from .tracing import LocalTrace
from .transport import MockModel
from .grading import worksheet, structural_checks, grounding_checks

ROOT = Path(__file__).resolve().parents[2]
FACTORIES = dict(zip(AGENT_NAMES, (error_classifier.create_agent, log_investigator.create_agent,
                 root_cause.create_agent, resolution.create_agent, validator.create_agent)))
FATAL = (BoundaryFailure, ResourceFailure, AccountingFailure)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def write_once(path, value):
    with path.open('x', encoding='utf-8') as f:
        os.chmod(path, 0o600)
        json.dump(value, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


def metadata(experiment, arm, dataset_version):
    paths = []
    for folder in ('agents', 'graph', 'models', 'tools', 'evaluation/week4', 'diagnostic_contracts'):
        paths.extend(p for p in (ROOT/folder).rglob('*.py') if '__pycache__' not in p.parts)
    paths.extend(ROOT/p for p in ('requirements.lock', 'docs/source-baseline-manifest.json',
        'evaluation/week4/requirements.lock', 'evaluation/week4/requirements.in', 'evaluation/week4/.python-version'))
    return {'version': 'week4-experiment-1', 'experiment_id': experiment, 'arm': arm,
            'dataset_version': dataset_version, 'mode': 'offline_mock',
            'source_hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)},
            'packages': {p: importlib.metadata.version(p) for p in ('pydantic', 'langgraph', 'langchain-openai', 'httpx', 'langsmith')},
            'config': {'model': 'week4-offline-mock', 'temperature': 0, 'max_calls_per_case': 5,
                       'sdk_retries': 0, 'workflow_retries': 0, 'external_tools': False,
                       'remote_tracing': False, 'semantic_quality': None, 'real_cost': None}}


def run_case(case, experiment, reply, sink=None, *, trace_enabled=True,
             provider_factory=None, callbacks=None, node_observer=None,
             workflow_factory=None):
    # Revalidation also catches mutation of the nested Incident after construction.
    case = InferenceCase.model_validate(case.model_dump(mode='json'))
    trace = LocalTrace(experiment, case.case_id, sink, enabled=trace_enabled)
    provider = provider_factory(trace) if provider_factory is not None else MockModel(reply, trace)
    coverage = {name: 'not_reached' for name in AGENT_NAMES}
    state = initialize_state(case.incident, trace.root_id, max_retries=0)
    errors = []
    fatal = None
    output = None
    workflow_status = None
    started = monotonic()

    def wrap(name, factory):
        actual = factory(llm=provider)
        def node(current):
            nonlocal state
            coverage[name] = 'started'
            state = current
            try:
                with trace.span('node', name):
                    update = actual(current)
                coverage[name] = 'completed'
                state = {**current, **update}
                if node_observer is not None:
                    node_observer(name, state)
                return update
            except Exception:
                coverage[name] = 'failed'
                raise
        return node

    try:
        with tracing_context(enabled=False), trace.span('root', 'week4.case'):
            graph = (workflow_factory or build_workflow)(agents={n: wrap(n, f) for n, f in FACTORIES.items()},
                                   trusted_semantics_enabled=False)
            state = graph.invoke(state, config={'callbacks': callbacks or []})
            workflow_status = state['status']
            if provider.fatal:
                raise provider.fatal
    except Exception as exc:
        if isinstance(exc, FATAL) or provider.fatal:
            fatal = provider.fatal or exc
            errors.append(type(fatal).__name__)
        elif isinstance(exc, AgentOutputError):
            # Preserve inherited rejection; never repair model output or references.
            errors.append('grounding_or_agent_rejection' if not any(r['error'] for r in provider.receipts) else 'agent_rejection')
        else:
            errors.append('application_error')
    errors.extend(r['error'] for r in provider.receipts if r['error'])
    errors = list(dict.fromkeys(errors))
    output = json.loads(serialize_state(state))
    elapsed = monotonic() - started
    usage_known = all(r['input_tokens'] is not None and r['output_tokens'] is not None for r in provider.receipts)
    usage = Usage(input_tokens=sum(r['input_tokens'] for r in provider.receipts) if usage_known else None,
                  output_tokens=sum(r['output_tokens'] for r in provider.receipts) if usage_known else None,
                  model_calls=len(provider.receipts), complete=usage_known)
    terminal = 'batch_stopped' if fatal else 'failed' if errors else 'held' if workflow_status == 'awaiting_evidence' else 'completed'
    if trace.spans:
        trace.spans[0].status = 'failed' if errors else 'completed'
    result = CaseResult(case_id=case.case_id, root_id=trace.root_id, terminal_status=terminal,
        workflow_status=workflow_status, error=errors[0] if errors else None, errors=tuple(errors),
        stage_coverage=coverage, elapsed_seconds=elapsed,
        model_elapsed_seconds=sum(r['elapsed_seconds'] for r in provider.receipts),
        usage=usage, output=output, trace_status=trace.deliver())
    return result, [asdict(s) for s in trace.spans], provider.receipts, fatal


def empty_result(case_id, status, error):
    return CaseResult(case_id=case_id, root_id=None, terminal_status=status, error=error,
        errors=(error,), stage_coverage={n: 'not_reached' for n in AGENT_NAMES},
        elapsed_seconds=None, model_elapsed_seconds=0, usage=None,
        trace_status='not_started').model_dump(mode='json')


def run_batch(cases: list[dict], output_dir: Path, *, experiment: str,
              reply_factory: Callable, sink=None, arm='baseline', dataset_version='development-fixtures-1',
              max_cases=40):
    """No references argument by design. Outputs are create-only, never resumed.

    Ordinary case errors continue. Boundary/resource/accounting failures persist
    the failing row and mark remaining cases unattempted, then stop dispatch.
    """
    if max_cases < 1 or max_cases > 40:
        raise ValueError('Offline batch ceiling must be 1..40')
    if not experiment or not arm:
        raise ValueError('Experiment and arm are required')
    output_dir = Path(output_dir).resolve()
    if not output_dir.is_relative_to(ROOT):
        raise BoundaryFailure('Output must stay within the new project')
    output_dir.mkdir(parents=True, exist_ok=False, mode=0o700)
    meta = metadata(experiment, arm, dataset_version)
    # Hash references neither reads nor persists any evaluator-only material.
    meta['assigned_cases'] = len(cases)
    meta['run_id'] = str(uuid4())
    write_once(output_dir/'experiment.json', meta)
    results = []
    stopped = None
    seen = set()
    for i, raw in enumerate(cases):
        ident = raw.get('case_id', f'invalid-{i}') if isinstance(raw, dict) else f'invalid-{i}'
        # Unsafe/invalid IDs never become paths or leak into reports.
        import re
        if not isinstance(ident, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', ident):
            ident = f'invalid-{i}'
        if stopped:
            row = empty_result(ident, 'unattempted', stopped)
        else:
            try:
                if i >= max_cases:
                    raise ResourceFailure('Case ceiling exhausted')
                check_inference(raw)
                if ident in seen:
                    raise BoundaryFailure('Duplicate case ID')
                seen.add(ident)
                case = InferenceCase.model_validate(raw)
                result, spans, receipts, fatal = run_case(case, f'{experiment}:{arm}:{meta["run_id"]}', reply_factory(case), sink)
                row = result.model_dump(mode='json')
                row['input_sha256'] = digest(case.model_dump(mode='json'))
                write_once(output_dir/f'{i:03d}-spans.json', spans)
                write_once(output_dir/f'{i:03d}-receipts.json', receipts)
                write_once(output_dir/f'{i:03d}-checks.json',
                    {'structure': structural_checks(result, spans, receipts),
                     'grounding': grounding_checks(result)})
                if fatal:
                    stopped = type(fatal).__name__
            except FATAL as exc:
                stopped = type(exc).__name__
                row = empty_result(ident, 'batch_stopped', stopped)
            except ValidationError:
                row = empty_result(ident, 'failed', 'input_schema_rejection')
            except Exception:
                row = empty_result(ident, 'failed', 'application_error')
        results.append(row)
        write_once(output_dir/f'{i:03d}-result.json', row)
        write_once(output_dir/f'{i:03d}-review.json', worksheet(ident, dataset_version, row.get('root_id')))
    known = [r['usage'] for r in results if r.get('usage')]
    times = sorted(r['elapsed_seconds'] for r in results if r.get('elapsed_seconds') is not None)
    def quantile(q):
        return times[max(0, math.ceil(q*len(times))-1)] if times else None
    summary = {'assigned': len(cases), 'attempted': sum(bool(r.get('root_id')) for r in results),
               'failed': sum(r['terminal_status'] in ('failed', 'batch_stopped') for r in results),
               'completed': sum(r['terminal_status'] == 'completed' for r in results),
               'held': sum(r['terminal_status'] == 'held' for r in results),
               'unattempted': sum(r['terminal_status'] == 'unattempted' for r in results),
               'stop_reason': stopped, 'mock_model_calls': sum(u['model_calls'] for u in known),
               'mock_input_tokens': sum(u['input_tokens'] or 0 for u in known),
               'mock_output_tokens': sum(u['output_tokens'] or 0 for u in known),
               'usage_complete': all(u['complete'] for u in known),
               'latency_attempted_denominator': len(times), 'p50_seconds': quantile(.50),
               'p95_seconds': quantile(.95),
               'model_elapsed_seconds': sum(r.get('model_elapsed_seconds', 0) for r in results),
               'usage_priced_cost_usd': None, 'semantic_quality': None,
               'mode': 'offline_mock'}
    write_once(output_dir/'summary.json', summary)
    write_once(output_dir/'artifact-hashes.json', {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted(output_dir.glob('*.json'))})
    for artifact in output_dir.iterdir():
        artifact.chmod(0o400)
    output_dir.chmod(0o500)
    return results, summary
