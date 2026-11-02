"""Real SDK serialization over httpx.MockTransport, never a live provider."""
import json
from time import monotonic
import httpx
from pydantic import ValidationError
from langchain_openai import ChatOpenAI
from langsmith import tracing_context
from tools.redaction import redact_message_content
from .contracts import AccountingFailure, ResourceFailure, BoundaryFailure

class MockModel:
    """Injected StructuredLLM; reply(request_json) supplies test-only model output.

    Tokens in mock replies are test data. We retain receipts even when the
    inherited ask() wrapper intentionally collapses parser/provider exceptions.
    """
    def __init__(self, reply, trace, max_calls=5):
        self.reply = reply
        self.trace = trace
        self.max_calls = max_calls
        self.requests = []
        self.receipts = []
        self.fatal = None

    def with_structured_output(self, schema, **options):
        owner = self
        class Structured:
            def invoke(self, messages):
                if len(owner.receipts) >= owner.max_calls:
                    owner.fatal = ResourceFailure('Model-call ceiling exhausted')
                    raise owner.fatal
                clean = [m.model_copy(update={'content': redact_message_content(m.content)}) for m in messages]
                receipt = {'schema': schema.__name__, 'input_tokens': None, 'output_tokens': None,
                           'elapsed_seconds': 0.0, 'error': None, 'source': 'mock_test_data'}
                owner.receipts.append(receipt)
                started = monotonic()
                def handler(request):
                    body = json.loads(request.content)
                    if len(request.content) > 32768:
                        owner.fatal = ResourceFailure('Mock request byte ceiling exhausted')
                        raise owner.fatal
                    owner.requests.append(body)
                    answer = owner.reply(body)
                    if isinstance(answer, Exception):
                        raise answer
                    usage = answer.get('usage', {'prompt_tokens': 11, 'completion_tokens': 7, 'total_tokens': 18})
                    # Capture mock provider metering before SDK parsing: parser errors
                    # must not discard known usage from the received response.
                    for wire_key, key, cap in (('prompt_tokens', 'input_tokens', 32768),
                                                ('completion_tokens', 'output_tokens', 1536)):
                        val = usage.get(wire_key) if isinstance(usage, dict) else None
                        if type(val) is not int or val < 0 or val > cap:
                            owner.fatal = AccountingFailure('Missing/invalid mock usage')
                            raise owner.fatal
                        receipt[key] = val
                    if 'refusal' in answer:
                        receipt['error'] = 'model_refusal'
                    return httpx.Response(200, json={
                        'id': 'offline-mock-response', 'object': 'chat.completion', 'created': 0,
                        'model': 'week4-offline-mock', 'usage': usage,
                        'choices': [{'index': 0, 'finish_reason': 'stop', 'message':
                            {'role': 'assistant', 'content': json.dumps(answer.get('output', {})),
                             **({'refusal': answer['refusal']} if 'refusal' in answer else {})}}]})
                try:
                    with owner.trace.span('model', schema.__name__):
                        # Disable ambient LangSmith tracing, including inherited callbacks.
                        # Explicit dummy key and MockTransport prohibit credential/network use.
                        with tracing_context(enabled=False), httpx.Client(transport=httpx.MockTransport(handler), trust_env=False) as client:
                            llm = ChatOpenAI(model='week4-offline-mock', api_key='offline-placeholder',
                                base_url='https://offline.invalid/v1', http_client=client,
                                max_retries=0, timeout=1, temperature=0, cache=False,
                                max_completion_tokens=1536)
                            result = llm.with_structured_output(schema, **{**options, 'include_raw': True}).invoke(clean)
                        usage = result['raw'].usage_metadata or {}
                        for key in ('input_tokens', 'output_tokens'):
                            val = usage.get(key)
                            if type(val) is not int or val < 0 or val > (32768 if key == 'input_tokens' else 1536):
                                owner.fatal = AccountingFailure('Missing/invalid mock usage')
                                raise owner.fatal
                            receipt[key] = val
                        if result['raw'].additional_kwargs.get('refusal'):
                            receipt['error'] = 'model_refusal'
                            raise ValueError('Model refusal')
                        if result.get('parsing_error') or result.get('parsed') is None:
                            receipt['error'] = 'schema_rejection'
                            raise ValueError('Schema rejected')
                        return result['parsed']
                except Exception as exc:
                    if isinstance(exc, (BoundaryFailure, ResourceFailure, AccountingFailure)):
                        owner.fatal = exc
                    receipt['exception_class'] = type(exc).__name__
                    receipt['error'] = receipt['error'] or ('timeout' if isinstance(exc, httpx.TimeoutException) else 'schema_rejection' if isinstance(exc, ValidationError) else 'transport_or_application_error')
                    # Mock failures are known to incur zero real usage and are bounded.
                    # Unknown usage on a received reply is handled by fatal above.
                    if not owner.fatal and receipt['input_tokens'] is None:
                        receipt.update(input_tokens=0, output_tokens=0)
                    raise
                finally:
                    receipt['elapsed_seconds'] = monotonic() - started
        return Structured()
