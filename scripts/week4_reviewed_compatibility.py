"""Offline import and input-contract audit only. Never run agents or models.

Imported prose is data. No URLs are fetched. Synthetic fixtures exist only in
separate tests, never in reviewed candidates or inference projections.
"""
import argparse
import copy
import csv
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('/Users/tagore/Documents/Codex/2026-10-25/w/outputs')
DEST = ROOT/'data/week4/reviewed-candidates'
DECISIONS = {'W4-REAL-001':'ACCEPT_WITH_REVISIONS', **{f'W4-REAL-{i:03d}':'ACCEPT' for i in range(2,6)}}
REQUIRED = ('incident_id','service','endpoint','http_method','status_code','expected_behavior','actual_behavior')


def sha(data): return hashlib.sha256(data).hexdigest()


def write_identical_or_new(path, data):
    """Create-only: an existing different artifact is an error, never overwritten."""
    if path.exists():
        if path.read_bytes()!=data: raise ValueError(f'Differing destination: {path.relative_to(ROOT)}')
        return 'verified_identical'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f: f.write(data)
    return 'created'


def json_bytes(value): return (json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()


class ReviewHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sections=[]; self.current=None; self.tag=None; self.heading=[]
    def handle_starttag(self,tag,attrs):
        if tag=='section': self.current={'text':[],'links':[],'heading':[]}
        if self.current is not None:
            if tag=='a': self.current['links'].append(dict(attrs).get('href'))
            if tag=='h2': self.tag='h2'
    def handle_data(self,data):
        if self.current is not None:
            self.current['text'].append(data)
            if self.tag=='h2': self.current['heading'].append(data)
    def handle_endtag(self,tag):
        if tag=='h2':self.tag=None
        if tag=='section' and self.current is not None:
            self.sections.append(self.current);self.current=None


def verify_sources(raw, html):
    if raw.get('reviewer')!='User in this conversation' or raw.get('reviewed_at') is not None:
        raise ValueError('Collection reviewer/timestamp differs from authorized import')
    cases=raw['cases']
    if len(cases)!=5 or {c['id'] for c in cases}!=set(DECISIONS): raise ValueError('Unexpected case IDs')
    parser=ReviewHTML();parser.feed(html)
    sections={''.join(s['heading']).split(' — ')[0]:s for s in parser.sections}
    for case in cases:
        review=case['human_review']; ident=case['id']
        if (review['decision']!=DECISIONS[ident] or review['reviewer']!='User in this conversation'
                or review['reviewed_at'] is not None or review['semantic_scores'] is not None
                or review['execution_authorized'] is not False or review['trace_export_authorized'] is not False
                or case['runtime_ready'] is not False):
            raise ValueError(f'Unexpected review/authorization record: {ident}')
        section=sections[ident];text=' '.join(section['text'])
        if case['source_url'] not in section['links'] or review['decision'] not in text:
            raise ValueError(f'HTML review/source cross-check failed: {ident}')
        if case['accepted_expected_behavior'] not in text or review['notes'] not in text:
            raise ValueError(f'HTML expectation/qualification cross-check failed: {ident}')
        if any(o not in text for o in case['inference_evidence']['observations']):
            raise ValueError(f'HTML observation cross-check failed: {ident}')
    revised=next(c for c in cases if c['id']=='W4-REAL-001')['inference_evidence']['observations']
    if not any('Reporter states' in o and 'data.' in o and 'makes the request work' in o for o in revised):
        raise ValueError('Case 001 approved comparison missing')
    return sections


def proposal_005(case):
    """Use observed root path only; never reconstruct the omitted endpoint host.

    Reported trace text is quoted as reported user evidence, not upgraded to
    machine-captured log events or response bodies. Expected behavior is an
    editorial operation goal, not the evaluator's accepted diagnostic answer.
    """
    evidence=case['inference_evidence']
    if case['id']!='W4-REAL-005' or evidence['operation']!='GET /' or evidence['http_method']!='GET' or evidence['status_code']!=302:
        raise ValueError('Projection requires the exact reviewed case-005 observations')
    observations='\n'.join('- '+o for o in evidence['observations'])
    quotes='\n'.join(f"- {item['source']}: {item['message']}" for item in evidence['logs'])
    return {'case_id':case['id'], 'incident':{
        'incident_id':case['id'], 'service':evidence['service'], 'endpoint':'/',
        'http_method':'GET','status_code':302,
        'expected_behavior':'Complete the reported GET / request without a client protocol exception.',
        'actual_behavior':('Reported observations from the reviewed public-report paraphrase; not independently captured:\n'
                           +observations+'\nQuoted reported trace text, not a captured response body:\n'+quotes+
                           '\nNo raw response body or endpoint identity is supplied in this reviewed evidence.')}}


def field_mapping(case):
    ident=case['id'];e=case['inference_evidence'];is005=ident=='W4-REAL-005'
    def row(field,available,proposed,kind,blocker):
        return {'runtime_field':field,'required':field in REQUIRED,'available_source_observation':available,
                'proposed_mapping':proposed,'classification':kind,'blocker_and_rationale':blocker}
    result=[row('incident_id',f"Source case ID {ident}",ident,'editorial_metadata',
                'Dataset linkage only; not an observed request/correlation ID.'),
            row('service',e['service'],e['service'],'editorial_metadata',
                'Reviewed service label; not independently captured identity. Preserve deliberate omission for 005.'),
            row('endpoint',e['operation'],'/' if is005 else None,'derived' if is005 else 'unknown',
                'Only the path / is explicit in GET /; host remains omitted and no URL is reconstructed.' if is005 else
                'BLOCKED: operation name alone is not an observed path/endpoint.'),
            row('http_method',e['http_method'],e['http_method'],'observed_report' if e['http_method'] else 'unknown',
                'GET explicitly reported.' if is005 else 'BLOCKED: no method reported; do not infer from SDK operation.'),
            row('status_code',e['status_code'],e['status_code'],'observed_report' if e['status_code'] is not None else 'unknown',
                'Observed/reported 302 only; error_status_hint=400 stays quoted exception text.' if is005 else
                'Reported 403 is a symptom, not proof of permission failure or throttling.' if e['status_code']==403 else
                'BLOCKED: missing HTTP status; exception names/TLS failures are not HTTP 400/500.'),
            row('expected_behavior',f"Reported operation: {e['operation']}",
                proposal_005(case)['incident']['expected_behavior'] if is005 else None,
                'editorial_metadata', '005 uses a proposed editorial request-completion goal, not a reporter quotation or new human-confirmed label; accepted diagnostic expectation excluded.' if is005 else
                'No explicit user requirement recorded; a neutral operation goal would need editorial mapping. Never copy accepted_expected_behavior.'),
            row('actual_behavior',e['observations'],proposal_005(case)['incident']['actual_behavior'] if is005 else None,
                'derived','Attributable reports may be joined without causal additions; only 005 has a complete input proposal.'),
            row('request_metadata',None,{},'unknown','No request IDs/times/SDK patch versions invented; optional empty default.'),
            row('response_body',None,None,'unknown','No raw HTTP body supplied; optional null preserved.'),
            row('logs',e['logs'],[] if is005 else None,'derived' if is005 else 'observed_report',
                '005 quotes the existing reported trace in actual_behavior (user source); logs defaults empty, not a claim no trace existed. No synthetic log events.' if is005 else
                'These are attributed exception excerpts, not verified raw telemetry. Empty source list for 004 stays empty.'),
            row('severity',None,'unknown','unknown','Runtime unknown default only; no severity rating assigned.'),
            row('evidence_quality',None,'unknown','unknown','Runtime unknown default only; accepted review sufficiency is evaluator-only.')]
    return result


def safe_errors(exc):
    # Do not persist raw input values or raw exception strings.
    return [{'location':list(e['loc']),'type':e['type'],'message':e['msg']}
            for e in exc.errors(include_input=False,include_url=False,include_context=False)]


def assess(cases):
    # No graph.workflow, agent, provider, model or tracing imports/execution.
    from evaluation.week4.contracts import InferenceCase
    from graph.state import initialize_state
    from tools.evidence_catalog import build_catalog, handle_catalog
    from tools.redaction import redact
    from tools.log_parser import parse_logs
    assessments=[]; projections={}
    for case in cases:
        ident=case['id'];e=case['inference_evidence']
        blockers=[]
        if e['http_method'] is None:blockers.append('http_method missing-source evidence / schema incompatibility')
        if e['status_code'] is None:blockers.append('status_code missing-source evidence / schema incompatibility')
        if ident!='W4-REAL-005':blockers.append('endpoint missing-source evidence / mapping ambiguity')
        checks={'schema':'NOT_CHECKED_BLOCKED','sanitization':'NOT_CHECKED_NO_COMPLETE_PROJECTION',
                'initialization':'NOT_CHECKED_BLOCKED','evidence_catalog':'NOT_CHECKED_BLOCKED',
                'log_parser':'NOT_CHECKED_BLOCKED','agent_graph':'NOT_CHECKED_NOT_AUTHORIZED',
                'models':'NOT_CHECKED_NOT_AUTHORIZED','diagnostic_readiness':'NOT_CHECKED',
                'publication_validation':'NOT_CHECKED'}
        result={'case_id':ident,'review_decision':case['human_review']['decision'],
                'source_runtime_status':case['human_review']['runtime_status'],
                'status':'BLOCKED','blockers':blockers,'field_mapping':field_mapping(case),'checks':checks,
                'sanitization_changes':None,'safe_rejections':[], 'projection_human_confirmed':False}
        if not blockers:
            raw=proposal_005(case)
            clean=InferenceCase.model_validate(raw)
            normalized=clean.model_dump(mode='json')
            # Compare only supplied fields: runtime defaults are not redaction losses.
            changes=[{'field':k,'before':v,'after':normalized['incident'][k]}
                     for k,v in raw['incident'].items() if normalized['incident'][k]!=v]
            state=initialize_state(clean.incident,'offline-contract-check-'+ident,max_retries=0)
            catalog=build_catalog(state['sanitized_inputs'])
            handles=handle_catalog(state['sanitized_inputs'])
            parsed=parse_logs(clean.incident.logs)
            checks.update(schema='PASS',sanitization='PASS_UNCHANGED' if not changes else 'CHANGED',
                          initialization='PASS',evidence_catalog='PASS',log_parser=parsed.status.upper())
            # Evidence is still attributed reported prose, not maintainer causal claims.
            if case['accepted_expected_behavior'] in raw['incident']['actual_behavior']:
                raise ValueError('Evaluator expectation entered inference prose')
            result.update(status='INPUT_COMPATIBLE_NOT_EXECUTED',sanitization_changes=changes,
                          catalog_entries=len(catalog),catalog_sources=sorted({c.source for c in catalog.values()}),
                          catalog_references=sorted(c.reference for c in catalog.values()),
                          input_sha256=sha(json_bytes(normalized)),
                          distinction_preserved={'http_status':302,'exception_hint':400,
                                                  'endpoint_path':'/','endpoint_identity':None},
                          safety_redaction='No rejection or content loss in supplied projection; original source untouched')
            if redact(normalized)!=normalized:raise ValueError('Projection is not stable under inherited redaction')
            if len(handles['evidence_catalog'])!=len(catalog):raise ValueError('Catalog/handle mismatch')
            projections[ident]=normalized
        assessments.append(result)
    return assessments,projections


def inventory_prefix(data, row_count):
    """Exact historical CSV prefix, including quoted multiline fields if any."""
    text=data.decode();stream=io.StringIO(text,newline='');reader=csv.reader(stream)
    next(reader)
    for _ in range(row_count):next(reader)
    return text[:stream.tell()].encode()


def update_inventory(cases,assessments):
    path=ROOT/'data/week4/candidate-inventory.csv';before=path.read_bytes()
    rows=list(csv.DictReader(io.StringIO(before.decode(),newline='')))
    ids=[r['case_id'] for r in rows]
    if len(ids)!=len(set(ids)):raise ValueError('Existing inventory has duplicate IDs')
    keys=list(rows[0]); extras=[]
    for case,result in zip(cases,assessments):
        ident=case['id']
        expected={'case_id':ident,'family':case['family'],
                  'source':'data/week4/reviewed-candidates/real-incidents-v2.json#'+ident,
                  'provenance_class':'real_public_incident_report',
                  'generation_method':'AI-curated paraphrases/expectations of public third-party reports; user content/scope review; not independently reproduced',
                  'prior_use_status':'development-exposed; curation and human review; earlier agent-run use unknown; not independent holdout',
                  'scenario_type':'edge_candidate' if ident=='W4-REAL-005' else 'UNASSIGNED',
                  'review_status':case['human_review']['decision'],'inherited_split':'not_assigned',
                  'limitations':result['status']+'; content review only; see docs/week4-runtime-compatibility.md; projection mapping not additionally human-confirmed; reviewed_at null; no execution/publication approval'}
        if set(expected)!=set(keys):raise ValueError('Inventory schema incompatible; document update instead')
        if ident in ids:
            if rows[ids.index(ident)]!=expected:raise ValueError('Existing inventory ID differs; do not overwrite')
        else:extras.append(expected)
    buf=io.StringIO(newline='');writer=csv.DictWriter(buf,fieldnames=keys,lineterminator='\r\n')
    writer.writerows(extras)
    if extras:
        with path.open('ab') as f:f.write(buf.getvalue().encode())
    return {'original_rows':len(rows),'appended_ids':[r['case_id'] for r in extras],
            'before_sha256':sha(before),'after_sha256':sha(path.read_bytes()),
            'existing_bytes_preserved':path.read_bytes().startswith(before)}


def import_candidates():
    json_path=SOURCE/'api-incident-reviewed-v2.json';html_path=SOURCE/'api-incident-reviewed-v2.html'
    original=json_path.read_bytes();html=html_path.read_bytes();raw=json.loads(original)
    sections=verify_sources(raw,html.decode())
    DEST.mkdir(parents=True,exist_ok=True)
    destination=DEST/'real-incidents-v2.json'
    copy_status=write_identical_or_new(destination,original)
    if destination.read_bytes()!=original:raise ValueError('Import identity failure')
    provenance_path=DEST/'import-provenance.json'
    stable={'version':'week4-reviewed-import-1','structured_source':str(json_path),
            'structured_source_sha256':sha(original),'structured_source_bytes':len(original),
            'html_source':str(html_path),'html_source_sha256':sha(html),'html_source_bytes':len(html),
            'destination':str(destination.relative_to(ROOT)),'destination_sha256':sha(destination.read_bytes()),
            'reviewer':'User in this conversation','reviewed_at':None,'confirmation_at':None,
            'source_recorded_at':raw['recorded_at'],'source_confirmation_timestamps_known':False,
            'confirmed_decisions':DECISIONS,'html_cross_check':'All five IDs, decisions, source links, expectations, qualifications and observations match offline',
            'authority':'Explicit user request to import five confirmed content/scope decisions',
            'use':'reviewed development candidates only; no golden freeze, independent holdout, execution, spending or publication approval'}
    if provenance_path.exists():
        existing=json.loads(provenance_path.read_text())
        if any(existing.get(k)!=v for k,v in stable.items()) or not existing.get('imported_at'):
            raise ValueError('Differing provenance; no overwrite')
        provenance=existing
    else:
        provenance={**stable,'imported_at':datetime.now(timezone.utc).isoformat(),
                    'import_time_note':'Actual import processing time, not a review or confirmation timestamp'}
        write_identical_or_new(provenance_path,json_bytes(provenance))
    references={'record_kind':'EVALUATOR_ONLY','cases':[
        {**{k:copy.deepcopy(c[k]) for k in ('id','source_url','source_date','family','scope','proposed_review',
                                            'human_review','accepted_expected_behavior','runtime_ready')},
         'source_display_heading':''.join(sections[c['id']]['heading'])} for c in raw['cases']]}
    write_identical_or_new(DEST/'evaluator-references.json',json_bytes(references))
    assessments,projections=assess(raw['cases'])
    for ident,projection in projections.items():
        write_identical_or_new(DEST/'inference'/f'{ident}.json',json_bytes(projection))
    report={'version':'week4-real-input-compatibility-1','source_sha256':sha(original),
            'reviewed_candidates':5,'input_compatible':len(projections),'blocked':5-len(projections),
            'agent_graph_executed':False,'model_executed':False,'cases':assessments}
    write_identical_or_new(DEST/'runtime-assessment.json',json_bytes(report))
    inventory=update_inventory(raw['cases'],assessments)
    inventory_path=DEST/'inventory-update.json'
    if inventory_path.exists():
        previous=json.loads(inventory_path.read_text())
        historical_count=previous['original_rows']+len(previous['appended_ids'])
        historical=inventory_prefix((ROOT/'data/week4/candidate-inventory.csv').read_bytes(),historical_count)
        if inventory['appended_ids'] or sha(historical)!=previous['after_sha256']:
            raise ValueError('Historical inventory prefix differs from existing report; no overwrite')
        inventory=previous
    else:
        write_identical_or_new(inventory_path,json_bytes(inventory))
    if json_path.read_bytes()!=original or html_path.read_bytes()!=html:raise ValueError('Source changed during import')
    return {'copy':copy_status,'source_sha256':sha(original),'imported_at':provenance['imported_at'],
            'input_compatible':list(projections),'blocked':[x['case_id'] for x in assessments if x['status']=='BLOCKED'],
            'inventory':inventory}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--import-reviewed',action='store_true',required=True)
    parser.parse_args()
    # Socket denial also applies when called outside the test harness.
    import socket
    def denied(*args,**kwargs):raise RuntimeError('Network prohibited during reviewed import/compatibility audit')
    socket.socket.connect=denied;socket.socket.connect_ex=denied;socket.getaddrinfo=denied
    print(json.dumps(import_candidates(),indent=2))
