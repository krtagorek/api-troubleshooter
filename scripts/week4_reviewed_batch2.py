"""Offline 006–010 import. Source prose is data, never executable instructions."""
import argparse
import copy
import csv
from datetime import datetime, timezone
import io
import json
from pathlib import Path
from scripts.week4_reviewed_compatibility import ROOT, SOURCE, sha, json_bytes, write_identical_or_new, safe_errors, inventory_prefix

DEST=ROOT/'data/week4/reviewed-candidates/batch-006-010'
IDS=tuple(f'W4-REAL-{n:03d}' for n in range(6,11))
QUALIFICATIONS={
 IDS[0]:'Supported media-type diagnosis. Preserve empty-body/no-Content-Type failure and successful JSON-header comparison; historical Spring behavior only.',
 IDS[1]:'Supported parameter-binding diagnosis. Preserve query-token validation and dependency signature; no credential values; later resolution evaluator-only; do not prefer URL credentials.',
 IDS[2]:'Ambiguous evidence. Separate example repository from reporter-owned repositories; clarify resource absence versus access, not one cause for every 404.',
 IDS[3]:'Supported rate-limit response, scope/cause unresolved. Reporter-stated 429 echoed in body, not a captured status line. No invented Retry-After, quotas, excessive traffic or outage.',
 IDS[4]:'Ambiguous media-type rejection. Body status is "415"; transport status unknown. Request actual Content-Type, boundary, sanitized payload structure and response status. Missing boundary, invalid UUID and Postman bugs unproven.'}
STATUS={IDS[0]:'published_http_transcript',IDS[1]:'published_http_transcript',IDS[2]:'reporter_stated',
        IDS[3]:'reporter_stated_and_body_echo',IDS[4]:'error_body_only_transport_unknown'}
GOALS={IDS[0]:'Process the reported POST /records request.',IDS[1]:'Complete the reported GET /users/me request.',
       IDS[2]:'Retrieve Pages information for the repository in the shown GET request.',
       IDS[3]:'Retrieve the requested album information.',IDS[4]:'Process the reported POST /api/v1/test form-data request.'}


def deny_network():
    import socket
    def denied(*a,**k):raise RuntimeError('Network prohibited in reviewed import checks')
    socket.socket.connect=denied;socket.socket.connect_ex=denied
    socket.create_connection=denied;socket.getaddrinfo=denied


def corrected_records(draft,reviewed):
    if tuple(c['id'] for c in draft['cases'])!=IDS or tuple(c['id'] for c in reviewed['cases'])!=IDS:
        raise ValueError('Unexpected batch IDs/order')
    result=copy.deepcopy(reviewed)
    result.update(version='week4-confirmed-006-010-1',review_status='ACCEPTED_CONTENT_RUNTIME_PENDING',
                  reviewer='User in this conversation',reviewed_at=None)
    for before,case in zip(draft['cases'],result['cases']):
        if before['inference_evidence']!=case['inference_evidence']:
            raise ValueError('Source draft/review evidence differs; requires explicit inspection')
        ident=case['id']
        old_review=case.get('human_review')
        if ident!=IDS[-1] and (not old_review or old_review['status']!='ACCEPTED' or
            old_review['reviewer']!='User in this conversation' or old_review['reviewed_at'] is not None):
            raise ValueError('Unexpected v5 acceptance record')
        case['human_review']={'decision':'ACCEPT','status':'ACCEPTED','reviewer':'User in this conversation',
            'reviewed_at':None,'confirmation_at':None,'recorded_at':None,'semantic_scores':None,
            'runtime_status':'RUNTIME_VALIDATION_PENDING' if ident==IDS[-1] else 'RUNTIME_MAPPING_PENDING',
            'notes':QUALIFICATIONS[ident],'confirmation_evidence':'Explicit user decisions in this conversation (006–010 import request)',
            'independently_reproduced':False,'execution_authorized':False,'trace_export_authorized':False}
        case['runtime_ready']=False
        # These are authoritative evaluator expectations, NEVER runtime user requirements.
        case['accepted_expected_behavior']=case['proposed_review']['expected_behavior']
        if ident==IDS[-1]:
            case['accepted_expected_behavior']='Request actual Content-Type, boundary, sanitized payload structure and actual HTTP response status; distinguish error-body "415" from unverified transport status. Missing boundary, invalid UUID and Postman bugs remain unproven hypotheses.'
            case['inference_evidence']['status_code']=None
        evidence=case['inference_evidence']
        evidence.setdefault('request_metadata',{})['status_evidence']={'kind':STATUS[ident]}
        if ident in (IDS[2],IDS[3],IDS[4]):
            evidence['request_metadata']['status_evidence']['captured_status_line_available']=False
        if ident==IDS[-1]:
            evidence['request_metadata']['status_evidence'].update(body_status='415',transport_status=None)
        if ident==IDS[2]:
            evidence['request_metadata']['repository_scope']={
                'shown_endpoint_role':'example repository',
                'other_reported_requests':'Reporter-owned repositories; identities and exact requests not supplied; separate from the shown example.'}
    return result


def proposal(case):
    evidence=case['inference_evidence'];ident=case['id']
    actual='Reported evidence from the reviewed historical public-report paraphrase; not independently reproduced:\n'
    actual+='\n'.join('- '+s for s in evidence['observations'])
    if ident==IDS[2]:
        actual+='\nThe shown example request and the separately reported reporter-owned repository requests are distinct; no shared outcome is established.'
    # No source resolution, family, URL, proposed stratum or expected diagnosis copied.
    return {'case_id':ident,'incident':{'incident_id':ident,**{k:copy.deepcopy(evidence[k]) for k in
        ('service','http_method','endpoint','status_code','request_metadata','response_body','logs')},
        'expected_behavior':GOALS[ident],'actual_behavior':actual}}


def differences(before,after,path=''):
    if type(before)!=type(after):return [{'path':path,'before':before,'after':after}]
    if isinstance(before,dict):
        return [change for k in before for change in differences(before[k],after.get(k),path+'/'+k)]
    if isinstance(before,list):
        return [change for i,v in enumerate(before) for change in differences(v,after[i],path+'/'+str(i))]
    return [] if before==after else [{'path':path,'before':before,'after':after}]


def assess(records):
    from pydantic import ValidationError
    from evaluation.week4.contracts import InferenceCase
    from graph.state import initialize_state
    from tools.evidence_catalog import build_catalog,handle_catalog
    from tools.redaction import redact
    results=[];projections={}
    for case in records['cases']:
        ident=case['id'];raw=proposal(case)
        row={'case_id':ident,'human_decision':'ACCEPTED','status_provenance':STATUS[ident],
            'runtime_result':'NOT_CHECKED','evaluation_eligibility':'NOT_GOLDEN_READY',
            'schema':'NOT_CHECKED','sanitization':'NOT_CHECKED','initialization':'NOT_CHECKED',
            'catalog':'NOT_CHECKED','agent_graph':'NOT_CHECKED','models':'NOT_CHECKED',
            'safe_rejections':[],'sanitization_changes':None,'blockers':[],
            'mapping_note':'Neutral expected_behavior is editorial, not an additional human confirmation.'}
        try:runtime=InferenceCase.model_validate(raw)
        except ValidationError as exc:
            row.update(schema='FAIL',runtime_result='BLOCKED_UNKNOWN_TRANSPORT_STATUS',
                       evaluation_eligibility='BLOCKED_RUNTIME_CONTRACT',safe_rejections=safe_errors(exc),
                       blockers=['Transport HTTP status unknown; Incident requires integer 100..599. Body "415" is not a substitute.'])
        else:
            normalized=runtime.model_dump(mode='json')
            changes=differences(raw['incident'],{k:normalized['incident'][k] for k in raw['incident']})
            state=initialize_state(runtime.incident,'offline-input-check-'+ident,max_retries=0)
            catalog=build_catalog(state['sanitized_inputs'])
            if len(catalog)!=len(handle_catalog(state['sanitized_inputs'])['evidence_catalog']):
                raise ValueError('Catalog/handle mismatch')
            if redact(normalized)!=normalized:raise ValueError('Sanitization is not stable')
            row.update(schema='PASS',initialization='PASS',catalog='PASS',catalog_entries=len(catalog),
                       sanitization='CHANGED' if changes else 'PASS_UNCHANGED',sanitization_changes=changes,
                       runtime_result='INPUT_COMPATIBLE_NOT_EXECUTED',
                       evaluation_eligibility='PENDING_MAPPING_AND_BENCHMARK_REVIEW')
            if changes:
                # Do not publish a weakened payload in the runnable inference directory.
                row.update(runtime_result='SCHEMA_PASS_EVIDENCE_LOSS_BLOCKED',
                    evaluation_eligibility='BLOCKED_EVIDENCE_PRESERVATION_REVIEW',
                    blockers=['Inherited sanitizer redacts reported authorization scheme and truncates the dependency signature; no equivalent runtime mapping approved.'],
                    sanitized_projection_preview=normalized)
            else:projections[ident]=normalized
        results.append(row)
    return results,projections


def append_inventory(cases,results):
    path=ROOT/'data/week4/candidate-inventory.csv';before=path.read_bytes()
    stream=io.StringIO(before.decode(),newline='');reader=csv.DictReader(stream)
    rows=list(reader);keys=reader.fieldnames
    if len({r['case_id'] for r in rows})!=len(rows):raise ValueError('Duplicate preexisting inventory IDs')
    additions=[]
    for case,result in zip(cases,results):
        ident=case['id']
        row={'case_id':ident,'family':case['family'],
            'source':'data/week4/reviewed-candidates/batch-006-010/reviewed-candidates.json#'+ident,
            'provenance_class':'real_public_incident_report',
            'generation_method':'AI-curated public-report evidence; explicit user content review; not independently reproduced',
            'prior_use_status':'development-exposed; prior model-run history unknown; related-family overlap; not independent holdout',
            'scenario_type':'UNASSIGNED','review_status':'ACCEPT','inherited_split':'not_assigned',
            'limitations':result['runtime_result']+'; human status ACCEPTED; no final split or golden eligibility; see docs/week4-real-cases-006-010.md'}
        if set(row)!=set(keys):raise ValueError('Inventory schema incompatible')
        existing=[r for r in rows if r['case_id']==ident]
        if existing and existing!=[row]:raise ValueError('Existing decision differs; no overwrite')
        if not existing:additions.append(row)
    if additions:
        buffer=io.StringIO(newline='');writer=csv.DictWriter(buffer,fieldnames=keys,lineterminator='\r\n')
        writer.writerows(additions)
        with path.open('ab') as f:f.write(buffer.getvalue().encode())
    return {'before_rows':len(rows),'appended_ids':[r['case_id'] for r in additions],
        'before_sha256':sha(before),'after_sha256':sha(path.read_bytes()),
        'old_bytes_preserved':path.read_bytes().startswith(before)}


def run_import():
    sources={name:(SOURCE/name).read_bytes() for name in ('api-incident-candidates-006-010-v1.json','api-incident-reviewed-006-010-v5.json')}
    draft=json.loads(next(iter(sources.values())));v5=json.loads(sources['api-incident-reviewed-006-010-v5.json'])
    for name,content in sources.items():write_identical_or_new(DEST/'sources'/name,content)
    records=corrected_records(draft,v5)
    write_identical_or_new(DEST/'reviewed-candidates.json',json_bytes(records))
    results,projections=assess(records)
    for ident,payload in projections.items():write_identical_or_new(DEST/'inference'/f'{ident}.json',json_bytes(payload))
    write_identical_or_new(DEST/'runtime-assessment.json',json_bytes({'kind':'EVALUATOR_ONLY',
        'agent_graph_executed':False,'cases':results}))
    refs={'kind':'EVALUATOR_ONLY','cases':[{k:copy.deepcopy(c[k]) for k in
        ('id','source_url','source_date','family','proposed_stratum','proposed_review','human_review','accepted_expected_behavior')}
        for c in records['cases']]}
    write_identical_or_new(DEST/'evaluator-references.json',json_bytes(refs))
    overlap={'kind':'EVALUATOR_ONLY','final_split_assigned':False,'independence_established':False,'groups':[
        {'cases':['W4-REAL-006','W4-REAL-010'],'level':'media-type rejection family',
         'difference':'006 historical empty-body/header comparison; 010 ambiguous multipart rejection with transport status unknown'},
        {'cases':['W4-REAL-004','W4-REAL-009'],'level':'broad rate-limiting/ambiguity family',
         'difference':'004 GitHub 403 secondary-limit hypothesis; 009 Spotify reporter/body 429 supported response category, cause/scope unknown'},
        {'cases':['W4-REAL-008','W4-REAL-004'],'level':'broad GitHub access/response-ambiguity exposure',
         'difference':'Different resources and symptoms; exact causes not shared or proven'}],
        'limits':'Not a full semantic independence audit of inherited synthetic families. Do not count Spring linked duplicate #21955 as another independent incident.'}
    write_identical_or_new(DEST/'family-overlap.json',json_bytes(overlap))
    stable={'version':'week4-import-006-010-1','sources':{name:{'path':str(SOURCE/name),'sha256':sha(data),'bytes':len(data)} for name,data in sources.items()},
        'reviewer':'User in this conversation','reviewed_at':None,'confirmation_at':None,'recorded_at':None,
        'authority':'Current explicit user decisions 006–010; 010 acceptance and body/transport correction supersede unreviewed v5 entry and draft placement.',
        'prior_v5_accepted_ids':list(IDS[:4]),'newly_confirmed_id':IDS[-1],
        'corrections':[{'case_id':IDS[-1],'path':'inference_evidence/status_code','source_value':415,'imported_value':None,
                        'retained_body_path':'response_body/errors/0/status','retained_body_value':'415'}],
        'prior_batch_sha256':sha((ROOT/'data/week4/reviewed-candidates/real-incidents-v2.json').read_bytes()),
        'source_bytes_preserved':True,'no_independent_reproduction':True,'golden_ready':False}
    provenance_path=DEST/'import-provenance.json'
    if provenance_path.exists():
        previous=json.loads(provenance_path.read_text())
        if any(previous.get(k)!=v for k,v in stable.items()):raise ValueError('Existing provenance differs')
    else:write_identical_or_new(provenance_path,json_bytes({**stable,'imported_at':datetime.now(timezone.utc).isoformat(),
        'time_note':'Import processing time only; no review/confirmation time inferred.'}))
    inventory=append_inventory(records['cases'],results)
    ip=DEST/'inventory-update.json'
    if ip.exists():
        previous=json.loads(ip.read_text())
        count=previous['before_rows']+len(previous['appended_ids'])
        prefix=inventory_prefix((ROOT/'data/week4/candidate-inventory.csv').read_bytes(),count)
        if inventory['appended_ids'] or sha(prefix)!=previous['after_sha256']:raise ValueError('Historical inventory prefix differs from logged import')
    else:write_identical_or_new(ip,json_bytes(inventory))
    for name,data in sources.items():
        if (SOURCE/name).read_bytes()!=data:raise ValueError('Source changed during import')
    return {'accepted':list(IDS),'inference_exports':list(projections),'results':[{k:r[k] for k in
            ('case_id','runtime_result','evaluation_eligibility')} for r in results]}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--import-reviewed',required=True,action='store_true')
    parser.parse_args();deny_network();print(json.dumps(run_import(),indent=2))
