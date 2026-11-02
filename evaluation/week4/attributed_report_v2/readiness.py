"""Same narrow mechanism, original anchors and explicit reported relationship."""
import json
from pydantic import ValidationError
from models.incident import Incident
from tools.diagnostic_sufficiency import readiness as legacy_readiness
from tools.evidence_catalog import build_catalog, handle_catalog
from evaluation.week4.attributed_report_v1.readiness import NO_PATTERN, HEADER, ATTRIBUTION
from evaluation.week4.attributed_report_v1.contracts import EXCEPTION
from .archive import Archive
from .contracts import Attribution, Assessment

ROLES = {'request','header','status','exception','bridge'}
PACKET = '/request_metadata/report_attribution_v2'


def assess(incident, evidence, *, archive=None):
    incident=Incident.model_validate(incident)
    old=legacy_readiness(incident,evidence)
    base=dict(snapshot=handle_catalog(incident)['evidence_snapshot'],legacy_reason=old.reason,
              legacy_qualified_analysis=old.qualified_analysis)
    def hold(reason):return Assessment(**base,qualified_analysis=False,reason=reason)
    if old.qualified_analysis:
        return Assessment(**base,qualified_analysis=True,reason='Legacy readiness retained')
    if old.reason!=NO_PATTERN:
        return hold('Legacy hold retained: '+old.reason)
    catalog=build_catalog(incident)
    selected={e.evidence_id:catalog[e.evidence_id] for e in evidence.items}
    paths={e.reference:e for e in selected.values()}
    exception=paths.get('/request_metadata/reported_exception')
    headers=[e for e in selected.values() if HEADER.fullmatch(e.reference) and e.value_type=='str'
             and any(ord(c)>127 for c in e.observation)]
    if exception is None or exception.observation!=EXCEPTION or not headers:
        return hold('No selected exact reported ASCII exception/non-ASCII header pair')
    md=incident.request_metadata
    names={}
    for name,value in md.get('request_headers',{}).items():
        names.setdefault(name.casefold(),[]).append(value)
    if any(len({json.dumps(v,sort_keys=True) for v in values})>1 for values in names.values()):
        return hold('Conflicting case-insensitive reported header values')
    attr=paths.get('/request_metadata/observation_representation')
    if attr is None or attr.observation!=ATTRIBUTION:
        return hold('Missing selected reported/unverified attribution')
    try:
        packet=Attribution.model_validate(md.get('report_attribution_v2'))
    except ValidationError:
        return hold('Missing or invalid V2 report-attribution record')
    # Every packet leaf, including interpretation and quotation kinds, is a peer.
    peers=[e for e in catalog.values() if e.reference.startswith(PACKET+'/')]
    if not peers or any(e.evidence_id not in selected for e in peers):
        return hold('Report-attribution peers remain omitted')
    if packet.method!=incident.http_method or packet.endpoint!=incident.endpoint:
        return hold('Reported operation mismatch')
    header=paths.get(packet.header_pointer)
    if header not in headers or not HEADER.fullmatch(packet.header_pointer):
        return hold('Association header is not selected non-ASCII request evidence')
    try:
        document=(archive or Archive()).load(packet.source_sha256)
        relation=document.relationships[packet.relationship]
        if (relation.kind!=packet.kind or relation.summary_kind!=packet.summary_kind
            or relation.summary!=packet.summary or set(relation.roles)!=ROLES
            or set(packet.anchors)!=ROLES):
            return hold('Unsupported or altered archived reporter relationship')
        for role,anchor in packet.anchors.items():
            block=document.blocks[anchor.block]
            if (relation.roles[role]!=anchor.block or block.scope!=relation.scope
                or not 0<=anchor.start<anchor.end<=len(block.text)
                or block.text[anchor.start:anchor.end]!=anchor.literal):
                return hold('Original excerpt anchor/scope mismatch')
        # Structured operand comparisons only. No model assertion or prose can
        # create roles/relationships in the separately bound archive.
        expected={'request':f'{incident.http_method} {incident.endpoint}',
                  'header':header.reference.rsplit('/',1)[1]+': '+header.observation,
                  'status':f'HTTP/1.1 {incident.status_code}', 'exception':EXCEPTION}
        if any(packet.anchors[k].literal!=v for k,v in expected.items()):
            return hold('Source operands do not match the reported operation')
    except (ValueError, KeyError, OSError, TypeError):
        return hold('Original archive/anchors could not be resolved')
    return Assessment(**base,qualified_analysis=True,
        reason='Original excerpt-bound reporter association permits qualified analysis only',
        rule='reported-ascii-header-rejection',provenance='reported_unverified',
        source_sha256=packet.source_sha256,relationship=packet.relationship,
        resolved_anchors=tuple(packet.anchors[k] for k in sorted(ROLES)),
        evidence_ids=tuple(e.evidence_id for e in [header,exception,attr,*peers]))
