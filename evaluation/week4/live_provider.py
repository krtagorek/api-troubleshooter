"""Supported OpenAI SDK, raw usage before semantic/schema parsing, no retries."""
import copy
import hashlib
import json
from time import monotonic
import httpx2
import jsonschema
from openai import OpenAI, APITimeoutError
from langsmith import tracing_context
from pydantic import ValidationError
from evaluation.provider import provider_schema, strict_root_schema
from tools.redaction import redact, redact_message_content, install_redaction_filters
from .contracts import AccountingFailure, BoundaryFailure, ResourceFailure
from .live_config import V2


def strict_wire(schema, messages):
    wire = provider_schema(schema, messages)
    wire = strict_root_schema(wire) if not isinstance(wire, dict) else copy.deepcopy(wire)
    def visit(item):
        if isinstance(item, dict):
            item.pop('default', None)
            if 'properties' in item:
                item['additionalProperties'] = False
                item['required'] = list(item['properties'])
            for value in item.values(): visit(value)
        elif isinstance(item, list):
            for value in item: visit(value)
    visit(wire)
    return wire


class LiveModel:
    def __init__(self, config, journal, trace, api_key, *, transport=None):
        self.config, self.journal, self.trace, self.api_key = config, journal, trace, api_key
        self.transport = transport
        self.fatal = None
        self.receipts = []
        install_redaction_filters()

    def with_structured_output(self, schema, **options):
        owner = self
        class Structured:
            def invoke(self, messages):
                config = owner.config
                if owner.fatal: raise owner.fatal
                clean = [m.model_copy(update={'content': redact_message_content(m.content)}) for m in messages]
                wire = strict_wire(schema, clean)
                wire_messages = [{'role': 'system' if m.type == 'system' else 'user', 'content': m.content} for m in clean]
                body = dict(model=config.model, messages=wire_messages, temperature=0,
                    max_completion_tokens=config.output_cap, service_tier=config.service_tier,
                    stream=False, store=False, response_format={'type':'json_schema',
                    'json_schema':{'name':schema.__name__,'strict':True,'schema':wire}})
                serialized = json.dumps(body, ensure_ascii=False, separators=(',',':'), allow_nan=False).encode()
                strict = config.input_bound_kind == 'model_context_max'
                # Complete messages/schema/advisory, recomputed for EVERY call.
                # Bytes are a transport resource limit, never a token estimate.
                if strict and len(serialized) > config.max_request_bytes:
                    owner.fatal = ResourceFailure('Complete provider request exceeds byte limit before reservation/dispatch')
                    owner.journal.append({'event':'request_rejected','schema':schema.__name__,
                                          'request_bytes':len(serialized),'reason':'complete_request_byte_limit'})
                    raise owner.fatal
                receipt = {'schema': schema.__name__, 'error': None, 'elapsed_seconds': 0,
                           'input_tokens': None, 'output_tokens': None,
                           'source': 'mock_test_data' if owner.transport is not None else 'provider_usage'}
                started = monotonic()
                with owner.trace.span('model', schema.__name__, {'messages': wire_messages}) as span:
                    span['metadata']['request_bound'] = {
                        'kind':config.input_bound_kind,'reserved_input_tokens':config.input_cap,
                        'request_bytes':len(serialized),'max_request_bytes':config.max_request_bytes,
                        'prepared_request_sha256':hashlib.sha256(serialized).hexdigest(),
                        'max_completion_tokens':config.output_cap,'service_tier':config.service_tier,
                        'exact_token_count':False}
                    try:
                        call_id = owner.journal.reserve(case_id=owner.trace.case_id, root_id=owner.trace.root_id,
                                                         span_id=span['span_id'], schema=schema.__name__)
                    except (AccountingFailure, ResourceFailure) as exc:
                        owner.fatal = exc
                        raise
                    receipt['call_id'] = call_id
                    span['metadata']['call_id'] = call_id
                    owner.receipts.append(receipt)
                    received = False
                    def request_guard(request):
                        if str(request.url) != 'https://api.openai.com/v1/chat/completions':
                            owner.fatal = BoundaryFailure('Provider origin/path mismatch')
                            raise owner.fatal
                        if strict and (len(request.content)>config.max_request_bytes or json.loads(request.content)!=body):
                            owner.fatal = BoundaryFailure('Serialized request differs from checked complete request')
                            raise owner.fatal
                        if not strict and len(request.content)+4096 > config.input_cap:
                            owner.fatal = ResourceFailure('Complete request byte envelope exceeds input reservation')
                            raise owner.fatal
                        owner.journal.attempt(call_id, len(request.content), hashlib.sha256(request.content).hexdigest())
                    def received_response(response):
                        nonlocal received
                        response.read()
                        try: payload = response.json()
                        except ValueError: payload = {}
                        payload = payload if isinstance(payload, dict) else {}
                        usage = payload.get('usage') or {}
                        usage = usage if isinstance(usage, dict) else {}
                        details = usage.get('prompt_tokens_details') or {}
                        details = details if isinstance(details, dict) else {}
                        known = {'input_tokens': usage.get('prompt_tokens'),
                                 'output_tokens': usage.get('completion_tokens'),
                                 'cached_input_tokens': details.get('cached_tokens', None if strict else 0),
                                 'total_tokens':usage.get('total_tokens'),
                                 'reasoning_tokens':(usage.get('completion_tokens_details') or {}).get('reasoning_tokens')
                                    if isinstance(usage.get('completion_tokens_details') or {},dict) else None}
                        received = True
                        receipt.update({k:v if type(v) is int else None for k,v in known.items()})
                        receipt['resolved_service_tier'] = payload.get('service_tier') if payload.get('service_tier') in ('default','priority','flex','scale') else None
                        # Store known provider counts durably before SDK or Pydantic parsing.
                        try:
                            owner.journal.usage(call_id, known, payload.get('model'), payload.get('service_tier'))
                        except AccountingFailure as exc:
                            owner.fatal = exc
                            raise
                        receipt.update(input_tokens=known['input_tokens'], output_tokens=known['output_tokens'])
                        span['metadata'].update(usage=known, resolved_model=payload.get('model'))
                        if response.status_code >= 400:
                            owner.fatal = AccountingFailure('Provider error; no further dispatch')
                            raise owner.fatal
                    try:
                        with tracing_context(enabled=False), httpx2.Client(transport=owner.transport,
                                trust_env=False, follow_redirects=False, timeout=config.call_timeout_seconds,
                                event_hooks={'request': [request_guard], 'response': [received_response]}) as http:
                            with OpenAI(api_key=owner.api_key, base_url='https://api.openai.com/v1',
                                        max_retries=0, timeout=config.call_timeout_seconds,
                                        http_client=http) as client:
                                completion = client.chat.completions.create(**body)
                        if not received:
                            raise AccountingFailure('No durable response metering')
                        choice = completion.choices[0]
                        if choice.message.refusal:
                            receipt['error'] = 'model_refusal'
                            raise ValueError('Model refusal')
                        if choice.finish_reason != 'stop':
                            receipt['error'] = 'incomplete_output'
                            raise ValueError('Incomplete structured output')
                        raw = json.loads(choice.message.content)
                        jsonschema.Draft202012Validator(wire).validate(raw)
                        parsed = schema.model_validate(raw)
                        span['outputs'] = redact(parsed)
                        return parsed
                    except Exception as exc:
                        if isinstance(exc, (AccountingFailure, BoundaryFailure, ResourceFailure)):
                            owner.fatal = exc
                        # Inherited ask() hides exceptions, so preserve safe classification here.
                        receipt['error'] = receipt['error'] or ('schema_rejection' if isinstance(exc,
                            (ValidationError, jsonschema.ValidationError, json.JSONDecodeError)) else
                            'timeout' if isinstance(exc, (httpx2.TimeoutException, APITimeoutError)) else type(exc).__name__)
                        if not received and not owner.fatal:
                            owner.fatal = AccountingFailure('Unknown usage; reservation retained')
                        owner.journal.append({'event': 'call_error', 'call_id': call_id, 'error': receipt['error']})
                        raise
                    finally:
                        receipt['elapsed_seconds'] = monotonic()-started
                        owner.journal.append({'event': 'call_end', 'call_id': call_id,
                                              'elapsed_seconds': receipt['elapsed_seconds'], 'error': receipt['error']})
        return Structured()
