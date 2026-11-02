"""Durable explicit span boundaries, with no ambient SDK tracing."""
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from time import monotonic
from uuid import uuid4
from tools.redaction import redact

class DurableTrace:
    def __init__(self, journal, case_id, root_id, enabled=True):
        self.journal, self.case_id, self.root_id = journal, case_id, root_id
        self.enabled = enabled
        self.parent = ContextVar('week4-live-parent', default=None)

    @contextmanager
    def span(self, kind, name, inputs=None):
        ident = self.root_id if kind == 'root' else str(uuid4())
        row = {'span_id': ident, 'parent_id': self.parent.get(), 'root_id': self.root_id,
               'case_id': self.case_id, 'kind': kind, 'name': name,
               'start_time': datetime.now(timezone.utc).isoformat(), 'inputs': redact(inputs or {}),
               'outputs': {}, 'metadata': {}, 'status': 'started', 'error': None}
        token = self.parent.set(ident)
        started = monotonic()
        if self.enabled: self.journal.append({'event': 'span_start', 'span': row})
        try:
            yield row
            if row['status']=='started': row['status'] = 'completed'
        except BaseException as exc:
            row['status'], row['error'] = 'failed', type(exc).__name__
            raise
        finally:
            self.parent.reset(token)
            row['end_time'] = datetime.now(timezone.utc).isoformat()
            row['elapsed_seconds'] = monotonic()-started
            row['outputs'] = redact(row['outputs'])
            if self.enabled: self.journal.append({'event': 'span_end', 'span': row})


def recover_spans(events, terminal):
    """Close only previously started spans after a child dies; never add calls."""
    spans = {}
    for event in events:
        if event['event'] in ('span_start', 'span_end'):
            spans[event['span']['span_id']] = event['span'].copy()
    attempts = {e['call_id']: e for e in events if e['event'] == 'attempt'}
    calls = {e['call_id']: e for e in events if e['event'] == 'reserve'}
    usage = {e['call_id']: e for e in events if e['event'] == 'usage'}
    for row in spans.values():
        if row['status'] == 'started':
            row.update(status='interrupted', error=terminal, end_time=datetime.now(timezone.utc).isoformat(),
                       elapsed_seconds=None)
        if row['kind'] == 'model':
            matches = [c for c in calls.values() if c['span_id'] == row['span_id']]
            if matches:
                call = matches[0]
                row['metadata'].update(call_id=call['call_id'], attempted=call['call_id'] in attempts,
                                       usage=usage.get(call['call_id'], {}).get('usage'))
    # A model span is a wire attempt, not schema construction or reserved work.
    return [s for s in spans.values() if s['kind'] != 'model' or s['metadata'].get('attempted')]
