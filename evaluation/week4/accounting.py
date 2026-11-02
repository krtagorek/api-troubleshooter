"""Fresh Week 4 append-only journal. No historical ledger dependencies."""
import fcntl
import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from uuid import uuid4
from .contracts import AccountingFailure, ResourceFailure


def money(value):
    result = Decimal(str(value))
    if not result.is_finite() or result < 0:
        raise ValueError('Money/rates must be finite and nonnegative')
    return result


class Journal:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.path = self.directory/'journal.jsonl'

    @classmethod
    def create(cls, directory, config):
        result = cls(directory)
        with result.path.open('x', encoding='utf-8') as f:
            os.chmod(result.path, 0o600)
            result._write(f, {'event': 'run', 'config': config})
        result._sync_directory()
        return result

    def _sync_directory(self):
        for directory in (self.directory, self.directory.parent):
            fd = os.open(directory, os.O_RDONLY)
            try: os.fsync(fd)
            finally: os.close(fd)

    @staticmethod
    def _write(f, event):
        f.write(json.dumps({**event, 'recorded_at': datetime.now(timezone.utc).isoformat()},
                           sort_keys=True, allow_nan=False)+'\n')
        f.flush()
        os.fsync(f.fileno())

    @contextmanager
    def locked(self, readonly=False):
        with self.path.open('r' if readonly else 'r+', encoding='utf-8') as f:
            fcntl.flock(f, fcntl.LOCK_SH if readonly else fcntl.LOCK_EX)
            try:
                raw = f.read()
                if not raw.endswith('\n'):
                    raise AccountingFailure('Interrupted journal append; reconciliation required')
                try: events = [json.loads(line) for line in raw.splitlines()]
                except (ValueError, TypeError):
                    raise AccountingFailure('Unreadable journal; reconciliation required') from None
                f.seek(0, os.SEEK_END)
                yield f, events
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def events(self):
        with self.locked(readonly=True) as (_, events): return events

    def append(self, event):
        with self.locked() as (f, _): self._write(f, event)

    @staticmethod
    def calls(events):
        calls = {}
        for event in events:
            ident = event.get('call_id')
            if event['event'] == 'reserve':
                if ident in calls: raise AccountingFailure('Duplicate reservation')
                calls[ident] = {**event, 'attempted': False, 'usage': None, 'cost_usd': None}
            elif event['event'] in ('attempt', 'usage'):
                if ident not in calls: raise AccountingFailure('Unreserved call record')
                if event['event'] == 'attempt':
                    if calls[ident]['attempted']: raise AccountingFailure('Repeated call attempt')
                    calls[ident]['attempted'] = True
                else:
                    if not calls[ident]['attempted'] or calls[ident]['usage'] is not None:
                        raise AccountingFailure('Invalid usage sequence')
                    calls[ident]['usage'] = event['usage']
                    calls[ident]['cost_usd'] = event['cost_usd']
                    calls[ident]['limit_violation'] = event.get('limit_violation',False)
        return calls

    @staticmethod
    def totals(events):
        calls = Journal.calls(events)
        settled = sum((money(c['cost_usd']) for c in calls.values() if c['cost_usd'] is not None), Decimal(0))
        retained = sum((money(c['reserved_usd']) for c in calls.values() if c['cost_usd'] is None), Decimal(0))
        return {'reserved_calls': len(calls), 'attempted_calls': sum(c['attempted'] for c in calls.values()),
                'usage_received_calls': sum(c['usage'] is not None and
                    all(type(c['usage'].get(k)) is int for k in ('input_tokens','output_tokens'))
                    for c in calls.values()),
                'uncertain_calls': sum(c['cost_usd'] is None for c in calls.values()),
                'limit_violations':sum(c.get('limit_violation',False) for c in calls.values()),
                'known_cost_usd': str(settled), 'retained_reservations_usd': str(retained),
                'accounted_ceiling_usd': str(settled+retained),
                'usage_priced_cost_usd': str(settled) if all(c['cost_usd'] is not None for c in calls.values()) else None}

    def reserve(self, *, case_id, root_id, span_id, schema):
        with self.locked() as (f, events):
            config = events[0]['config']
            totals = self.totals(events)
            if totals['uncertain_calls'] or totals['limit_violations']:
                raise AccountingFailure('Unsettled call; no further dispatch')
            if totals['reserved_calls'] >= config['max_calls']:
                raise ResourceFailure('Call limit exhausted')
            reserve = (money(config['input_per_million'])*config['input_cap'] +
                       money(config['output_per_million'])*config['output_cap'])/Decimal(1000000)
            if reserve + money(totals['accounted_ceiling_usd']) > money(config['max_usd']):
                raise ResourceFailure('Money limit exhausted before dispatch')
            ident = str(uuid4())
            self._write(f, {'event': 'reserve', 'call_id': ident, 'case_id': case_id,
                           'root_id': root_id, 'span_id': span_id, 'schema': schema,
                           'reserved_usd': str(reserve)})
            return ident

    def attempt(self, call_id, request_bytes, request_sha256=None):
        with self.locked() as (f, events):
            call = self.calls(events)[call_id]
            if call['attempted']: raise AccountingFailure('Duplicate request dispatch')
            self._write(f, {'event': 'attempt', 'call_id': call_id, 'request_bytes': request_bytes,
                           'request_sha256':request_sha256})

    def usage(self, call_id, usage, resolved_model, resolved_tier=None):
        """Persist even partial/invalid received metering before parsing output."""
        with self.locked() as (f, events):
            config = events[0]['config']
            call = self.calls(events)[call_id]
            if call['usage'] is not None: raise AccountingFailure('Duplicate received usage')
            safe = {k: usage.get(k) if type(usage.get(k)) is int else None
                    for k in ('input_tokens', 'output_tokens', 'cached_input_tokens',
                              'total_tokens', 'reasoning_tokens')}
            count_ok = all(type(safe[k]) is int and safe[k] >= 0 for k in ('input_tokens','output_tokens'))
            cap_ok = count_ok and safe['input_tokens'] <= config['input_cap'] and safe['output_tokens'] <= config['output_cap']
            cached = safe['cached_input_tokens']
            cache_ok = type(cached) is int and count_ok and 0 <= cached <= safe['input_tokens']
            rates_ok = not cached or config.get('cached_input_per_million') is not None
            strict = config.get('input_bound_kind') == 'model_context_max'
            tier_ok = not strict or resolved_tier == config['service_tier'] == 'default'
            total_ok = (not strict or (count_ok and type(safe['total_tokens']) is int
                        and safe['total_tokens'] == safe['input_tokens']+safe['output_tokens']))
            reasoning = safe['reasoning_tokens']
            reasoning_ok = reasoning is None or (count_ok and 0 <= reasoning <= safe['output_tokens'])
            cost = None
            if (count_ok and cache_ok and rates_ok and tier_ok and total_ok and reasoning_ok
                    and resolved_model == config['model']):
                cost = ((safe['input_tokens']-cached)*money(config['input_per_million'])+
                        cached*money(config.get('cached_input_per_million') or 0)+
                        safe['output_tokens']*money(config['output_per_million']))/Decimal(1000000)
            self._write(f, {'event': 'usage', 'call_id': call_id, 'usage': safe,
                           'resolved_model': resolved_model if isinstance(resolved_model,str) and len(resolved_model)<128 else None,
                           'resolved_service_tier': resolved_tier if resolved_tier in ('default','priority','flex','scale') else None,
                           'cost_usd': str(cost) if cost is not None else None,
                           'limit_violation':not cap_ok or (cost is not None and cost>money(call['reserved_usd']))})
            if cost is None or not cap_ok or cost>money(call['reserved_usd']): raise AccountingFailure('Received usage/model/tier cannot be settled within approved rates/caps')
