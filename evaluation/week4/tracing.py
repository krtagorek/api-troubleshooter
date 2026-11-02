"""Explicit local spans. No SDK client, network, or remote transport."""
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, asdict
from time import monotonic
from uuid import uuid5, NAMESPACE_URL

@dataclass
class Span:
    span_id: str
    parent_id: str | None
    root_id: str
    case_id: str
    kind: str
    name: str
    started: float
    elapsed_seconds: float = 0.0
    status: str = 'started'
    error: str | None = None

class FakeTracingSink:
    """In-memory sink for local checks; delivery failure cannot rerun inference."""
    def __init__(self, fail=False):
        self.records = []
        self.fail = fail

    def write(self, records):
        if self.fail:
            raise OSError('Simulated local sink failure')
        self.records.extend(records)

class LocalTrace:
    def __init__(self, experiment, case_id, sink=None, enabled=True):
        self.enabled = enabled
        self.case_id = case_id
        self.root_id = str(uuid5(NAMESPACE_URL, f'week4:{experiment}:{case_id}'))
        self.spans = []
        self.parent = ContextVar(f'parent-{self.root_id}', default=None)
        self.sink = sink

    @contextmanager
    def span(self, kind, name):
        if not self.enabled:
            yield None
            return
        parent = self.parent.get()
        ident = self.root_id if kind == 'root' else str(uuid5(NAMESPACE_URL, f'{self.root_id}:{len(self.spans)}:{name}'))
        span = Span(ident, parent, self.root_id, self.case_id, kind, name, monotonic())
        self.spans.append(span)
        token = self.parent.set(ident)
        try:
            yield span
            span.status = 'completed'
        except BaseException as exc:
            span.status = 'failed'
            # Exception text can include model content; keep only type here.
            span.error = type(exc).__name__
            raise
        finally:
            span.elapsed_seconds = monotonic() - span.started
            self.parent.reset(token)

    def deliver(self):
        if self.sink is None or not self.enabled:
            return 'disabled'
        try:
            self.sink.write([asdict(s) for s in self.spans])
            return 'local'
        except Exception:
            return 'TRACE_DELIVERY_FAILED'
