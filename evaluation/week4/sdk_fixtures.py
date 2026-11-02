"""Offline SDK transport fixtures. Never expected semantic answers or live usage."""
import json
import os
import socket
import time
from pathlib import Path
import httpx2
import requests
from requests.adapters import BaseAdapter
from graph import state
from .fixtures import full_path_reply, mock_reply


def block_network():
    def denied(*args, **kwargs): raise RuntimeError('External network prohibited in offline SDK checks')
    socket.socket.connect = denied
    socket.socket.connect_ex = denied
    socket.getaddrinfo = denied
    socket.create_connection = denied


def model_transport(directory, scenario='hold'):
    directory = Path(directory)
    def handler(request):
        body = json.loads(request.content)
        with (directory/'mock-model-requests.jsonl').open('a') as f:
            f.write(json.dumps(body)+'\n')
        if scenario == 'interrupt': os._exit(23)
        if scenario == 'timeout':
            while True: time.sleep(.05)
        if scenario == 'transport_error': raise httpx2.ReadTimeout('offline test timeout')
        schema_name = body['response_format']['json_schema']['name']
        schema = getattr(state, schema_name)
        answer = (full_path_reply if scenario in ('full','validator_parsing') else mock_reply)(body)
        if scenario=='v2_mechanics' and schema_name=='LiveLogInvestigatorOutput':
            envelope=json.loads(body['messages'][1]['content'].split('\n',1)[1])
            answer['output'].update(selected_evidence_handles=[e['handle'] for e in envelope['evidence_catalog']
                if e['reference']!='/expected_behavior' and e['value_type']!='null'],completeness='partial')
        parsed = schema.model_validate(answer['output']).model_dump(mode='json')
        envelope = json.loads(body['messages'][1]['content'].split('\n', 1)[1])
        if 'evidence_contract' in parsed and 'evidence_contract' in envelope:
            parsed.update({k: envelope[k] for k in ('evidence_contract', 'evidence_snapshot')})
        if scenario == 'parsing' or (scenario=='validator_parsing' and schema_name=='ValidatorOutput'): parsed = {}
        usage = None if scenario == 'missing_usage' else {
            'prompt_tokens': 11, 'completion_tokens': 7, 'total_tokens': 18,
            'prompt_tokens_details': {'cached_tokens': 0}}
        if scenario=='overrun': usage['prompt_tokens']=1000000
        return httpx2.Response(200, json={'id': 'offline-provider-response',
            'object': 'chat.completion', 'created': 0, 'model': body['model'], 'usage': usage,
            'service_tier':body.get('service_tier','default'),
            'choices': [{'index': 0, 'finish_reason': 'stop', 'message':
                         {'role': 'assistant', 'content': json.dumps(parsed)}}]})
    return httpx2.MockTransport(handler)


class SmithAdapter(BaseAdapter):
    def __init__(self, directory, fail=False, mismatch=False):
        self.directory = Path(directory)
        self.fail, self.mismatch = fail, mismatch
        self.runs = {}

    def send(self, request, **kwargs):
        body = request.body
        if isinstance(body, bytes): body = body.decode()
        if body: body = json.loads(body)
        with (self.directory/'mock-langsmith-requests.jsonl').open('a') as f:
            f.write(json.dumps({'method': request.method, 'url': request.url, 'body': body})+'\n')
        response = requests.Response()
        response.status_code = 200
        response.request = request
        response.url = request.url
        if self.fail and request.method == 'POST':
            response.status_code, payload = 500, {'detail': 'Offline simulated trace failure'}
        elif request.method == 'POST' and request.url.endswith('/runs'):
            self.runs[body['id']] = body
            payload = {}
        elif request.method == 'GET' and '/runs/' in request.url:
            ident = request.url.split('/runs/')[1].split('?')[0]
            payload = self.runs[ident].copy()
            if self.mismatch: payload['extra'] = {'metadata': {'case_id': 'wrong-case'}}
        elif request.method == 'GET' and request.url.endswith('/info'):
            payload = {'version': 'offline-sdk-fixture'}
        else: raise RuntimeError('Unexpected LangSmith SDK request')
        response._content = json.dumps(payload).encode()
        return response

    def close(self): pass


def smith_session(directory, scenario):
    session = requests.Session()
    session.week4_mock = True
    session.mount('https://', SmithAdapter(directory, fail=scenario=='trace_failure', mismatch=scenario=='trace_mismatch'))
    return session
