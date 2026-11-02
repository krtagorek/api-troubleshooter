"""Offline 011–015 import. Never execute source prose, graphs, providers or URLs."""
import argparse
import copy
import csv
from datetime import datetime, timezone
import io
import json
from scripts.week4_reviewed_compatibility import ROOT,SOURCE,sha,json_bytes,write_identical_or_new,safe_errors,inventory_prefix
from scripts.week4_reviewed_batch2 import differences,deny_network

DEST=ROOT/'data/week4/reviewed-candidates/batch-011-015'
IDS=tuple(f'W4-REAL-{n:03d}' for n in range(11,16))
QUALIFICATIONS={
 IDS[0]:'Supported missing-authorization diagnosis, underlying cause unresolved. Preserve GET /api/list-files, reported 401 and adjacent missing-Authorization warning. Do not merge later invalid-token comments or confirm port, expiry or signing-secret causes.',
 IDS[1]:'Supported JSON-parsing diagnosis, exact payload defect unresolved. Preserve POST /euronews/mytable/1266?pretty=true, HTTP 400 and nested json_parse_exception location. Exact payload unavailable; no invented corrected JSON or confirmed later mapping fix.',
 IDS[2]:'Supported method-routing diagnosis and reported missing-Allow-header defect. Preserve GET-only configuration, successful GET and PUT / 405 without Allow shown. Informative rejection is intended, not PUT success. No full allowed-method list or guaranteed upgrade fix.',
 IDS[3]:'Reported write/response inconsistency and duplicate-retry risk, exact server defect unresolved. Preserve POST endpoint and HTTP 500. Persistence/duplicates are reporter claims. Check existing state before replay; no blind retries or confirmed serialization/transaction/code defect.',
 IDS[4]:'Supported route/handler rejection, underlying cause unresolved. Preserve POST /_plugins/_sm/policies/snapshot_policy, HTTP 400, Content-Type application/json, no-handler response and versions. Check deployed API support/plugins/method-path compatibility; no proven malformed JSON, missing plugin, licensing or POST-to-PUT fix.'}
GOALS={
 IDS[0]:'List the reporter\'s generated files through the reported GET /api/list-files operation.',
 IDS[1]:'Submit the intended document to the reported POST /euronews/mytable/1266?pretty=true operation.',
 IDS[2]:'Return an informative rejection for the reported unsupported PUT / request under the configured route contract.',
 IDS[3]:'Create the requested child issue and return a response consistent with the write outcome.',
 IDS[4]:'Submit the intended snapshot policy through the reported POST /_plugins/_sm/policies/snapshot_policy operation.'}
STATUS={IDS[0]:'reported_server_access_log',IDS[1]:'reported_client_exception_http_status_line',
        IDS[2]:'reported_httpie_status_line',IDS[3]:'reported_curl_status_line',IDS[4]:'reported_curl_status_line'}
MISSING={
 IDS[0]:['Original full request/header capture and exact missing-header cause not established; no proven port/session/expiry/signing-secret cause.'],
 IDS[1]:['Exact original payload bytes unavailable; no confirmed corrected JSON or exact serialization defect.'],
 IDS[2]:['Full allowed-method list and independently reproduced upgrade/remediation outcome unavailable.'],
 IDS[3]:['Independent verification of persistence/duplicates, request payload and exact server failure point unavailable.'],
 IDS[4]:['Deployed API/plugin support and exact root cause unresolved; alternative snapshot API advice not a verified repair.']}


def normalize(draft,reviewed):
    if tuple(c['id'] for c in draft['cases'])!=IDS or tuple(c['id'] for c in reviewed['cases'])!=IDS:
        raise ValueError('Unexpected batch IDs/order')
    result=copy.deepcopy(reviewed)
    result.update(version='week4-confirmed-011-015-1',review_status='ACCEPTED_CONTENT_RUNTIME_PENDING',
        reviewer='User in this conversation',reviewed_at=None,
        runtime_status='Human acceptance only; see separate runtime-assessment.json for input checks.')
    for original,case in zip(draft['cases'],result['cases']):
        if original['inference_evidence']!=case['inference_evidence']:
            raise ValueError('Draft/review evidence differs; manual source comparison required')
        ident=case['id'];prior=case.get('human_review')
        if ident!=IDS[-1] and (not prior or prior.get('status')!='ACCEPTED' or
                prior.get('reviewer')!='User in this conversation' or prior.get('reviewed_at') is not None):
            raise ValueError('Unexpected v5 acceptance')
        if ident==IDS[-1] and prior is not None:raise ValueError('Unexpected v5 review for 015')
        case['review_status']='ACCEPTED'
        case['human_review']={'decision':'ACCEPT','status':'ACCEPTED','reviewer':'User in this conversation',
            'reviewed_at':None,'confirmation_at':None,'recorded_at':None,'semantic_scores':None,
            'runtime_status':'RUNTIME_MAPPING_PENDING','notes':QUALIFICATIONS[ident],
            'confirmation_evidence':'Explicit user decisions in current 011–015 import request; 015 accepted after v5',
            'independently_reproduced':False,'execution_authorized':False,'trace_export_authorized':False}
        case['accepted_expected_behavior']=QUALIFICATIONS[ident]
        case['runtime_ready']=False
    return result


def proposal(case):
    e=case['inference_evidence'];ident=case['id']
    metadata=copy.deepcopy(e.get('request_metadata',{}))
    metadata.update(status_evidence={'kind':STATUS[ident]},
        observation_representation='Attributed public-report paraphrases, not independently reproduced measurements.',
        response_body_scope='reported_excerpt_completeness_unknown' if e['response_body'] is not None else 'not_supplied_not_a_captured_null')
    return {'case_id':ident,'incident':{'incident_id':ident,**{k:copy.deepcopy(e[k]) for k in
        ('service','http_method','endpoint','status_code','response_body','logs')},'request_metadata':metadata,
        'expected_behavior':GOALS[ident],
        'actual_behavior':'Reported historical observations; not independently reproduced:\n'+
                          '\n'.join('- '+o for o in e['observations'])+
                          '\nSource warnings/exceptions remain attributed prose; logs=[] does not establish that no source logs existed. Any supplied response body is an excerpt, with completeness unverified.'}}


def assess(records, *, goals=None, status=None, missing=None, proposal_factory=None):
    goals=GOALS if goals is None else goals
    status=STATUS if status is None else status
    missing=MISSING if missing is None else missing
    proposal_factory=proposal if proposal_factory is None else proposal_factory
    from pydantic import ValidationError
    from evaluation.week4.contracts import InferenceCase
    from graph.state import initialize_state
    from tools.evidence_catalog import build_catalog,handle_catalog
    from tools.redaction import redact
    results=[];projections={}
    for case in records['cases']:
        ident=case['id'];raw=proposal_factory(case)
        row={'case_id':ident,'human_decision':'ACCEPTED','status_provenance':status[ident],
             'editorial_goal':goals[ident],'editorial_goal_additionally_confirmed':False,
             'missing_evidence':missing[ident],'schema':'NOT_CHECKED','sanitization':'NOT_CHECKED',
             'initialization':'NOT_CHECKED','catalog':'NOT_CHECKED','graph_executed':False,
             'semantic_quality':'NOT_CHECKED','runtime_result':'NOT_CHECKED',
             'evaluation_eligibility':'NOT_GOLDEN_READY','safe_rejections':[],'blockers':[],
             'sanitization_changes':None}
        try:runtime=InferenceCase.model_validate(raw)
        except ValidationError as exc:
            row.update(schema='FAIL',runtime_result='BLOCKED_SCHEMA',safe_rejections=safe_errors(exc),
                       blockers=['See genuine input-validation errors; no filler values substituted.'])
        else:
            normalized=runtime.model_dump(mode='json')
            changes=differences(raw['incident'],{k:normalized['incident'][k] for k in raw['incident']})
            state=initialize_state(runtime.incident,'offline-input-check-'+ident,max_retries=0)
            catalog=build_catalog(state['sanitized_inputs']);handles=handle_catalog(state['sanitized_inputs'])
            if len(catalog)!=len(handles['evidence_catalog']):raise ValueError('Catalog/handle mismatch')
            if redact(normalized)!=normalized:raise ValueError('Unstable inherited redaction')
            row.update(schema='PASS',sanitization='CHANGED' if changes else 'PASS_UNCHANGED',
                initialization='PASS',catalog='PASS',catalog_entries=len(catalog),
                sanitization_changes=changes,runtime_result='INPUT_COMPATIBLE_NOT_EXECUTED',
                evaluation_eligibility='PENDING_MAPPING_AND_BENCHMARK_REVIEW',
                inference_sha256=sha(json_bytes(normalized)))
            if changes:
                row.update(runtime_result='SCHEMA_PASS_EVIDENCE_LOSS_BLOCKED',
                    evaluation_eligibility='BLOCKED_EVIDENCE_PRESERVATION_REVIEW',
                    blockers=['Diagnostic evidence changed by sanitizer; no equivalence or runnable export assumed.'],
                    sanitized_projection_preview=normalized)
            else:projections[ident]=normalized
        results.append(row)
    return results,projections


def overlap(records):
    with (ROOT/'data/week4/candidate-inventory.csv').open(newline='') as f:inventory=list(csv.DictReader(f))
    prior_paths=[ROOT/'data/week4/reviewed-candidates/real-incidents-v2.json',
                 ROOT/'data/week4/reviewed-candidates/batch-006-010/reviewed-candidates.json']
    prior=[c for p in prior_paths for c in json.loads(p.read_text())['cases']]
    historical=DEST/'family-overlap.json'
    if historical.exists():
        prior_ids=set(json.loads(historical.read_text())['prior_inventory_ids_checked'])
        inventory=[r for r in inventory if r['case_id'] in prior_ids]
    duplicates=[{'case_id':c['id'],'prior_case_id':p['id'],'source_url':c['source_url']}
        for c in records['cases'] for p in prior if c['source_url']==p['source_url']]
    return {'kind':'EVALUATOR_ONLY','independence_established':False,'final_split_assigned':False,
        'prior_inventory_ids_checked':[r['case_id'] for r in inventory if r['case_id'] not in IDS],
        'exact_source_url_matches_in_001_010':duplicates,
        'exact_family_matches_in_prior_inventory':[{'case_id':c['id'],'prior_case_ids':
            [r['case_id'] for r in inventory if r['case_id'] not in IDS and r['family']==c['family']]}
            for c in records['cases']],
        'broad_groups':[
            {'cases':['W4-REAL-011','W4-REAL-007'],
             'prior_generated_family':'v1:Proxy stripped the Authorization header',
             'qualification':'Header delivery/authentication exposure overlaps broadly; FastAPI query binding and missing header are not proven identical causes.'},
            {'cases':['W4-REAL-012','W4-REAL-001','W4-REAL-006','W4-REAL-010'],
             'qualification':'Broad request parsing/validation exposure; JSON syntax, expansion path and media-type negotiation are distinct. Shared 400/415/422 symptoms do not prove mechanism equality.'},
            {'cases':['W4-REAL-013','W4-REAL-015'],
             'qualification':'Method/route availability overlap. GET-only rejection with reported missing Allow differs from unresolved no-handler support.'},
            {'cases':['W4-REAL-014'],
             'prior_generated_families':['compression-double','recursive-template','v1:Server database migration was not applied'],
             'qualification':'Broad server-error exposure only, not confirmed causal overlap. Related source issues #6529/#3310 must not be counted as independent new incidents.'}],
        'limits':'Local source URL/family comparison plus explicit broad-family review, not independent causal or untouched-history verification. All development-exposed; previous model execution unknown.'}


def append_inventory(cases,results):
    path=ROOT/'data/week4/candidate-inventory.csv';before=path.read_bytes()
    reader=csv.DictReader(io.StringIO(before.decode(),newline=''));rows=list(reader);keys=reader.fieldnames
    if len(rows)!=len({r['case_id'] for r in rows}):raise ValueError('Duplicate inventory IDs')
    additions=[]
    for c,result in zip(cases,results):
        ident=c['id'];row={'case_id':ident,'family':c['family'],
            'source':'data/week4/reviewed-candidates/batch-011-015/reviewed-candidates.json#'+ident,
            'provenance_class':'real_public_incident_report',
            'generation_method':'AI-curated public-report evidence; explicit user content review; not independently reproduced',
            'prior_use_status':'development-exposed; earlier execution unknown; related-family review pending; not independent holdout',
            'scenario_type':'UNASSIGNED','review_status':'ACCEPT','inherited_split':'not_assigned',
            'limitations':result['runtime_result']+'; human status ACCEPTED; no final split/golden eligibility; see docs/week4-real-cases-011-015.md'}
        if set(row)!=set(keys):raise ValueError('Incompatible inventory schema')
        existing=[r for r in rows if r['case_id']==ident]
        if existing and existing!=[row]:raise ValueError('Existing decision differs; no overwrite')
        if not existing:additions.append(row)
    report_path=DEST/'inventory-update.json'
    if report_path.exists():
        old=json.loads(report_path.read_text())
        if additions or sha(inventory_prefix(before,old['before_rows']+len(old['appended_ids'])))!=old['after_sha256']:
            raise ValueError('Historical import inventory prefix changed')
        return old
    if additions:
        out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=keys,lineterminator='\r\n');writer.writerows(additions)
        with path.open('ab') as f:f.write(out.getvalue().encode())
    report={'before_rows':len(rows),'appended_ids':[r['case_id'] for r in additions],
        'before_sha256':sha(before),'after_sha256':sha(path.read_bytes()),
        'old_bytes_preserved':path.read_bytes().startswith(before)}
    write_identical_or_new(report_path,json_bytes(report));return report


def run_import():
    sources={name:(SOURCE/name).read_bytes() for name in ('api-incident-candidates-011-015-v1.json','api-incident-reviewed-011-015-v5.json')}
    draft=json.loads(sources['api-incident-candidates-011-015-v1.json']);v5=json.loads(sources['api-incident-reviewed-011-015-v5.json'])
    records=normalize(draft,v5)
    existing_provenance=DEST/'import-provenance.json'
    if existing_provenance.exists():
        prior_names=json.loads(existing_provenance.read_text())['prior_artifact_sha256']
        prior_artifacts={name:sha((ROOT/name).read_bytes()) for name in prior_names}
    else:
        prior_artifacts={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in (ROOT/'data/week4/reviewed-candidates').rglob('*.json') if not p.is_relative_to(DEST)}
    for name,data in sources.items():write_identical_or_new(DEST/'sources'/name,data)
    write_identical_or_new(DEST/'reviewed-candidates.json',json_bytes(records))
    results,projections=assess(records)
    for ident,p in projections.items():write_identical_or_new(DEST/'inference'/f'{ident}.json',json_bytes(p))
    counts={'human_accepted':5,'input_schema_compatible':sum(r['schema']=='PASS' for r in results),
        'evidence_preserving_input_compatible':len(projections),'graph_executed':0,'golden_set_ready':0}
    write_identical_or_new(DEST/'runtime-assessment.json',json_bytes({'kind':'EVALUATOR_ONLY','counts':counts,'cases':results}))
    refs={'kind':'EVALUATOR_ONLY','cases':[{k:copy.deepcopy(c[k]) for k in
        ('id','source_url','source_date','family','field_provenance','proposed_review','human_review','accepted_expected_behavior')}
        for c in records['cases']]}
    write_identical_or_new(DEST/'evaluator-references.json',json_bytes(refs))
    write_identical_or_new(DEST/'family-overlap.json',json_bytes(overlap(records)))
    provenance={'version':'week4-import-011-015-1','sources':{name:{'path':str(SOURCE/name),'sha256':sha(data),'bytes':len(data)} for name,data in sources.items()},
        'reviewer':'User in this conversation','reviewed_at':None,'confirmation_at':None,'recorded_at':None,
        'authority':'Explicit current user decisions for all five; 015 accepted after v5 was saved.',
        'v5_confirmed_ids':list(IDS[:4]),'newly_confirmed_id':IDS[-1],
        'source_evidence_identical_between_v1_v5':True,
        'normalization_note':'Derived collection and per-case review_status reflect authoritative acceptance; stale source NOT_REVIEWED flags remain in byte-identical archives.',
        'prior_artifact_sha256':prior_artifacts,'independent_reproduction':False,'execution_authorized':False,'golden_set_ready':False}
    pp=DEST/'import-provenance.json'
    if pp.exists():
        previous=json.loads(pp.read_text())
        if any(previous.get(k)!=v for k,v in provenance.items()):raise ValueError('Existing provenance differs')
        imported_at=previous['imported_at']
    else:
        imported_at=datetime.now(timezone.utc).isoformat()
        write_identical_or_new(pp,json_bytes({**provenance,'imported_at':imported_at,'time_note':'Import processing only, not human review/confirmation time.'}))
    append_inventory(records['cases'],results)
    for name,data in sources.items():
        if (SOURCE/name).read_bytes()!=data:raise ValueError('Source changed during import')
    return {'counts':counts,'inference_exports':list(projections),'imported_at':imported_at}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--import-reviewed',required=True,action='store_true')
    parser.parse_args();deny_network();print(json.dumps(run_import(),indent=2))
