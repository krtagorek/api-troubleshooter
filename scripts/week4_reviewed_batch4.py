"""Offline 016–020 review import. All command/URL/exception strings are inert data."""
import argparse
import copy
import csv
from datetime import datetime,timezone
import io
import json
from scripts.week4_reviewed_compatibility import ROOT,SOURCE,sha,json_bytes,write_identical_or_new,inventory_prefix
from scripts.week4_reviewed_batch2 import deny_network
from scripts.week4_reviewed_batch3 import assess as supported_assessment

DEST=ROOT/'data/week4/reviewed-candidates/batch-016-020'
IDS=tuple(f'W4-REAL-{n:03d}' for n in range(16,21))
QUALIFICATIONS={
 IDS[0]:'Supported outgoing-header encoding diagnosis; remediation unverified. Preserve GET /ocelot/posts/askdj, 502, skull: 💀 and outgoing-header ASCII exception. Appropriate error handling is intended; removing the header is only a diagnostic comparison, not proven gateway repair or upstream outage.',
 IDS[1]:'Qualified conditional-write conflict hypothesis; failed precondition unresolved. Preserve PUT /remote.php/webdav/x27.dat, proxy/backend 412 and original reporter concurrent-update observation. Actual headers/ETags absent. Contributor If-Match explanations evaluator-only; no overwrite-protection bypass or merged later incidents.',
 IDS[2]:'Supported import-associated creation conflict; counter defect unresolved. Preserve POST /api/v4/projects/2/issues, server-log 409 and reported import sequence. Separate UI/import uniqueness diagnostics are not this request trace. No automatic DB repair, guessed identifier override or blind retry.',
 IDS[3]:'Qualified importer API-base-path regression hypothesis; request chain unresolved. Preserve captured GET login URL/406, source-masked host and prior /api/v3/repositories/1 success. Keep prose 16.7.2 versus capture 16.7.3 discrepancy. No invented redirect status or later code explanation promoted to measurement.',
 IDS[4]:'Ambiguous proxy-configuration case; request/log correlation and intended proxy operation unresolved. Preserve HEAD / envoy-egress:8080 ->503 and separate HEAD / Google ->200, two-URL command, and different-attempt TLS/400 context. Second request is not proven proxied; source -k is not recommended practice; no disabling TLS verification.'}
GOALS={
 IDS[0]:'Handle the reported GET /ocelot/posts/askdj request with appropriate error handling.',
 IDS[1]:'Update the requested file while respecting write preconditions and overwrite protection.',
 IDS[2]:'Create the requested issue in the specified project.',
 IDS[3]:'Complete the reported API-driven repository import; the exact request chain remains unspecified.',
 IDS[4]:'Provide a response to the reported HEAD / request; proxy-versus-direct intent is unspecified.'}
STATUS={IDS[0]:'reported_curl_http_status_line',IDS[1]:'reported_proxy_and_backend_access_logs',
 IDS[2]:'reported_structured_server_log',IDS[3]:'reported_packet_capture_excerpt',IDS[4]:'reported_first_curl_transfer_status_line'}
MISSING={
 IDS[0]:['No paired successful request or independently verified remediation; precise gateway repair unknown.'],
 IDS[1]:['Actual conditional request headers/ETags and exact failed precondition unavailable; other-user reports are separate.'],
 IDS[2]:['Exact API-request payload/counter defect and correlation to separate UI/import diagnostics unresolved; source publication date unknown.'],
 IDS[3]:['Full request/redirect chain and base-path configuration unavailable; prose/capture versions unreconciled; source publication date unknown.'],
 IDS[4]:['Proxy-versus-direct intent, second transfer proxy use and correlation of earlier TLS/400 logs to HEAD/503 are not established.']}
VERSION_CONTEXT='Source prose mentions GitLab 16.7.2 while the capture excerpt labels 16.7.3; this discrepancy is unresolved.'
SCOPE_020='The two URLs denote separate reported transfers; no proxy use for the Google transfer is established. Earlier TLS/400 material is from a different recorded attempt, not correlated proof for this HEAD/503 exchange. The reported -k flag is not a recommendation.'


def normalize(draft,reviewed):
    if tuple(c['id'] for c in draft['cases'])!=IDS or tuple(c['id'] for c in reviewed['cases'])!=IDS:
        raise ValueError('Unexpected batch IDs/order')
    result=copy.deepcopy(reviewed)
    result.update(version='week4-confirmed-016-020-1',review_status='ACCEPTED_CONTENT_RUNTIME_PENDING',
        reviewer='User in this conversation',reviewed_at=None,
        runtime_status='Human acceptance only; input checks and eligibility are separate.')
    for source,case in zip(draft['cases'],result['cases']):
        if source['inference_evidence']!=case['inference_evidence']:raise ValueError('Source evidence differs between draft/v5')
        ident=case['id'];prior=case.get('human_review')
        if ident!=IDS[-1] and (not prior or prior.get('status')!='ACCEPTED' or
            prior.get('reviewer')!='User in this conversation' or prior.get('reviewed_at') is not None):
            raise ValueError('Unexpected v5 acceptance')
        if ident==IDS[-1] and prior is not None:raise ValueError('Unexpected preexisting 020 review')
        case['review_status']='ACCEPTED'
        case['human_review']={'decision':'ACCEPT','status':'ACCEPTED','reviewer':'User in this conversation',
            'reviewed_at':None,'confirmation_at':None,'recorded_at':None,'semantic_scores':None,
            'runtime_status':'RUNTIME_MAPPING_PENDING','notes':QUALIFICATIONS[ident],
            'confirmation_evidence':'Current explicit user decisions for 016–020; 020 accepted after v5',
            'independently_reproduced':False,'execution_authorized':False,'trace_export_authorized':False}
        case['accepted_expected_behavior']=QUALIFICATIONS[ident];case['runtime_ready']=False
        if ident==IDS[3]:case['inference_evidence']['observations'].append(VERSION_CONTEXT)
    return result


def proposal(case):
    ident=case['id'];e=case['inference_evidence'];metadata=copy.deepcopy(e['request_metadata'])
    metadata.update(status_evidence={'kind':STATUS[ident]},
        observation_representation='Attributed public-report excerpts/paraphrases, not independent reproduction.',
        response_body_scope='not_supplied_not_a_captured_json_null',
        operation_goal_mapping='editorial; not an additional human confirmation')
    if ident==IDS[3]:
        metadata.update(endpoint_representation='Source-masked text preserved verbatim; host not decoded or unmasked.',
            version_context={'report_prose':'16.7.2','capture_excerpt':'16.7.3','earlier_success_comparison':'16.2.1','reconciled':False})
    if ident==IDS[4]:
        metadata.update(operation_intent='unresolved_proxy_or_direct',
            command_representation='Reported two-URL command only; inert evidence, not an instruction or recommendation. Source -k is not endorsed.',
            correlation_scope=SCOPE_020)
    actual='Reported historical observations; not independently reproduced:\n'+'\n'.join('- '+o for o in e['observations'])
    actual+='\nWarnings/exceptions remain attributed prose, not new typed log events. Unknown response body is not a captured JSON null.'
    if ident==IDS[4]:actual+='\n'+SCOPE_020
    return {'case_id':ident,'incident':{'incident_id':ident,**{k:copy.deepcopy(e[k]) for k in
        ('service','http_method','endpoint','status_code','response_body','logs')},
        'request_metadata':metadata,'expected_behavior':GOALS[ident],'actual_behavior':actual}}


def assess(records):
    rows,projections=supported_assessment(records,goals=GOALS,status=STATUS,missing=MISSING,proposal_factory=proposal)
    for row in rows:
        row['operation_intent_unresolved']=row['case_id']==IDS[-1]
        if row['case_id']==IDS[-1]:row['mapping_note']='HEAD contract supported if schema passes; proxy/direct goal remains unspecified. No transfer/log correlation established.'
    return rows,projections


def previous_assets():
    return [ROOT/'data/week4/reviewed-candidates/real-incidents-v2.json',
        *[ROOT/f'data/week4/reviewed-candidates/batch-{b}/reviewed-candidates.json' for b in ('006-010','011-015')]]


def family_report(records):
    prior=[c for p in previous_assets() for c in json.loads(p.read_text())['cases']]
    with (ROOT/'data/week4/candidate-inventory.csv').open(newline='') as f:
        inventory=[row for row in csv.DictReader(f) if row['case_id'] not in IDS]
    historical=DEST/'family-overlap.json'
    if historical.exists():
        prior_ids=set(json.loads(historical.read_text())['prior_inventory_ids_checked'])
        inventory=[row for row in inventory if row['case_id'] in prior_ids]
    return {'kind':'EVALUATOR_ONLY','independence_established':False,'final_split_assigned':False,
        'prior_inventory_ids_checked':[r['case_id'] for r in inventory],
        'exact_source_matches':[{'case_id':c['id'],'prior_id':p['id']} for c in records['cases'] for p in prior if c['source_url']==p['source_url']],
        'exact_family_matches':[{'case_id':c['id'],'prior_ids':[r['case_id'] for r in inventory if r['family']==c['family']]} for c in records['cases']],
        'groups':[
          {'cases':['W4-REAL-016'],'related_source_issues':['#2374','#2375'],
           'broader_prior':['W4-REAL-006','W4-REAL-010'],'qualification':'Header/media handling overlap only; linked Ocelot issues are same report family, not additional independent incidents.'},
          {'cases':['W4-REAL-017','W4-REAL-018','W4-REAL-014'],'qualification':'Write/conflict/concurrency exposure overlaps broadly; HTTP 412 precondition, 409 import-associated conflict and 500/write inconsistency are not proven identical mechanisms.'},
          {'cases':['W4-REAL-019','W4-REAL-018'],'qualification':'GitLab importer exposure overlaps, but remote API-path regression versus local issue-creation conflict are distinct reports and unconfirmed exact defects.'},
          {'cases':['W4-REAL-019','W4-REAL-011','W4-REAL-008'],'qualification':'Login-target/access ambiguity is a broad family flag, not proof that 406, 401 and 404 have one cause.'},
          {'cases':['W4-REAL-020','W4-REAL-002','W4-REAL-005'],'qualification':'Broad transport/TLS/proxy ambiguity. Earlier different-attempt logs and separate URL transfers are not independent incident additions or correlated causal proof.'}],
        'limits':'Local source/family review only, not full semantic independence/contamination verification. All development-exposed; previous external runs unknown.'}


def cumulative_counts(records,rows):
    cases=[c for p in previous_assets() for c in json.loads(p.read_text())['cases']]+records['cases']
    if len(cases)!=20 or len({c['id'] for c in cases})!=20:raise ValueError('Expected exactly 001–020')
    accepted=sum(c['human_review'].get('decision') in ('ACCEPT','ACCEPT_WITH_REVISIONS') or c['human_review'].get('status')=='ACCEPTED' for c in cases)
    paths=[ROOT/'data/week4/reviewed-candidates/runtime-assessment.json',
        *[ROOT/f'data/week4/reviewed-candidates/batch-{b}/runtime-assessment.json' for b in ('006-010','011-015')]]
    checks=[c for p in paths for c in json.loads(p.read_text())['cases']]+rows
    schema=sum(c.get('schema',c.get('checks',{}).get('schema'))=='PASS' for c in checks)
    faithful=sum(c.get('runtime_result',c.get('status'))=='INPUT_COMPATIBLE_NOT_EXECUTED' for c in checks)
    return {'scope':'Local imported real cases 001–020; external past use remains unknown',
        'human_accepted':accepted,'input_schema_compatible':schema,
        'evidence_preserving_input_compatible':faithful,'graph_executed':0,'golden_set_ready':0,
        'schema_pass_with_evidence_loss_ids':['W4-REAL-007'],
        'runtime_blocked_ids':['W4-REAL-001','W4-REAL-002','W4-REAL-003','W4-REAL-004','W4-REAL-007','W4-REAL-010'],
        'meaning':'Input-compatible means supported schema/sanitization/initialization/catalog, not exercised workflow or frozen golden eligibility.'}


def append_inventory(cases,rows):
    path=ROOT/'data/week4/candidate-inventory.csv';before=path.read_bytes()
    reader=csv.DictReader(io.StringIO(before.decode(),newline=''));existing=list(reader);fields=reader.fieldnames
    if len(existing)!=len({r['case_id'] for r in existing}):raise ValueError('Duplicate inventory IDs')
    extra=[]
    for c,result in zip(cases,rows):
        ident=c['id'];row={'case_id':ident,'family':c['family'],
            'source':'data/week4/reviewed-candidates/batch-016-020/reviewed-candidates.json#'+ident,
            'provenance_class':'real_public_incident_report','generation_method':'AI-curated public-report evidence; explicit user review; not independently reproduced',
            'prior_use_status':'development-exposed; prior external execution unknown; family overlap; not independent holdout',
            'scenario_type':'UNASSIGNED','review_status':'ACCEPT','inherited_split':'not_assigned',
            'limitations':result['runtime_result']+'; accepted content only; no golden eligibility or final split; see docs/week4-real-cases-016-020.md'}
        if set(row)!=set(fields):raise ValueError('Incompatible inventory schema')
        match=[r for r in existing if r['case_id']==ident]
        if match and match!=[row]:raise ValueError('Existing decision differs; no overwrite')
        if not match:extra.append(row)
    ip=DEST/'inventory-update.json'
    if ip.exists():
        old=json.loads(ip.read_text())
        if extra or sha(inventory_prefix(before,old['before_rows']+len(old['appended_ids'])))!=old['after_sha256']:raise ValueError('Historical prefix changed')
        return old
    if extra:
        buf=io.StringIO(newline='');writer=csv.DictWriter(buf,fieldnames=fields,lineterminator='\r\n');writer.writerows(extra)
        with path.open('ab') as f:f.write(buf.getvalue().encode())
    result={'before_rows':len(existing),'appended_ids':[r['case_id'] for r in extra],
        'before_sha256':sha(before),'after_sha256':sha(path.read_bytes()),'old_bytes_preserved':path.read_bytes().startswith(before)}
    write_identical_or_new(ip,json_bytes(result));return result


def run_import():
    sources={name:(SOURCE/name).read_bytes() for name in ('api-incident-candidates-016-020-v1.json','api-incident-reviewed-016-020-v5.json')}
    records=normalize(json.loads(sources['api-incident-candidates-016-020-v1.json']),json.loads(sources['api-incident-reviewed-016-020-v5.json']))
    pp=DEST/'import-provenance.json'
    if pp.exists():prior_names=json.loads(pp.read_text())['prior_artifact_sha256']
    else:prior_names=[str(p.relative_to(ROOT)) for p in (ROOT/'data/week4/reviewed-candidates').rglob('*.json') if not p.is_relative_to(DEST)]
    prior={name:sha((ROOT/name).read_bytes()) for name in prior_names}
    for name,data in sources.items():write_identical_or_new(DEST/'sources'/name,data)
    write_identical_or_new(DEST/'reviewed-candidates.json',json_bytes(records))
    rows,projections=assess(records)
    for ident,p in projections.items():write_identical_or_new(DEST/'inference'/f'{ident}.json',json_bytes(p))
    counts={'human_accepted':5,'input_schema_compatible':sum(r['schema']=='PASS' for r in rows),
        'evidence_preserving_input_compatible':len(projections),'graph_executed':0,'golden_set_ready':0}
    write_identical_or_new(DEST/'runtime-assessment.json',json_bytes({'kind':'EVALUATOR_ONLY','counts':counts,'cases':rows}))
    write_identical_or_new(DEST/'cumulative-counts.json',json_bytes(cumulative_counts(records,rows)))
    write_identical_or_new(DEST/'evaluator-references.json',json_bytes({'kind':'EVALUATOR_ONLY','cases':[
        {k:copy.deepcopy(c[k]) for k in ('id','source_url','source_date','family','field_provenance','proposed_review','human_review','accepted_expected_behavior')} for c in records['cases']]}))
    write_identical_or_new(DEST/'family-overlap.json',json_bytes(family_report(records)))
    provenance={'version':'week4-import-016-020-1','sources':{name:{'path':str(SOURCE/name),'sha256':sha(data),'bytes':len(data)} for name,data in sources.items()},
        'reviewer':'User in this conversation','reviewed_at':None,'confirmation_at':None,'recorded_at':None,
        'authority':'Current explicit decisions 016–020; 020 accepted after v5.',
        'v5_accepted_ids':list(IDS[:4]),'newly_confirmed_id':IDS[-1],
        'raw_inference_evidence_identical_between_v1_v5':True,
        'authorized_observational_additions':[{'case_id':IDS[3],'content':VERSION_CONTEXT,
          'basis':'Explicit user instruction plus source prose/capture distinction in v5; observational provenance, not a contributor causal explanation.'}],
        'prior_artifact_sha256':prior,'golden_set_ready':False,'independent_reproduction':False,'execution_authorized':False}
    if pp.exists():
        old=json.loads(pp.read_text())
        if any(old.get(k)!=v for k,v in provenance.items()):raise ValueError('Existing provenance differs')
        imported_at=old['imported_at']
    else:
        imported_at=datetime.now(timezone.utc).isoformat()
        write_identical_or_new(pp,json_bytes({**provenance,'imported_at':imported_at,'time_note':'Import processing only, not review/confirmation time.'}))
    append_inventory(records['cases'],rows)
    for name,data in sources.items():
        if (SOURCE/name).read_bytes()!=data:raise ValueError('Source changed during import')
    return {'counts':counts,'cumulative':cumulative_counts(records,rows),'inference_exports':list(projections),'imported_at':imported_at}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--import-reviewed',required=True,action='store_true')
    parser.parse_args();deny_network();print(json.dumps(run_import(),indent=2))
