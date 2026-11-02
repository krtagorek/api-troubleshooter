"""Single deterministic rule; legacy holds other than no-pattern are final."""
import json
import re
from pydantic import ValidationError
from models.incident import Incident
from tools.diagnostic_sufficiency import readiness as legacy_readiness
from tools.evidence_catalog import build_catalog, handle_catalog
from .contracts import Association, Assessment, Anchor, EXCEPTION

NO_PATTERN = 'No supported comparative or specific diagnostic observation; request discriminating evidence'
HEADER = re.compile(r'^/request_metadata/request_headers/[A-Za-z0-9!#$%&\'*+.^_`|~-]+$')
ATTRIBUTION = 'Attributed public-report excerpts/paraphrases, not independent reproduction.'


def statement(method, endpoint, header, value):
    """Bounded literal grammar; never inserted into real inputs by this module."""
    return (f'For the reported {method} {endpoint} operation, request header '
            f'{header} was {json.dumps(value, ensure_ascii=False)}; '
            f'the reported exception was "{EXCEPTION}".')


def assess(incident, evidence):
    incident = Incident.model_validate(incident)
    old = legacy_readiness(incident, evidence)
    base = dict(snapshot=handle_catalog(incident)['evidence_snapshot'],
                legacy_reason=old.reason, legacy_qualified_analysis=old.qualified_analysis)
    def hold(reason):
        return Assessment(**base, qualified_analysis=False, reason=reason)
    if old.qualified_analysis:
        return Assessment(**base, qualified_analysis=True, reason='Legacy readiness retained')
    if old.reason != NO_PATTERN:
        return hold('Legacy hold retained: ' + old.reason)
    catalog = build_catalog(incident)
    selected = {e.evidence_id: catalog[e.evidence_id] for e in evidence.items}
    by_path = {e.reference: e for e in selected.values()}
    md = incident.request_metadata
    # Exact pattern first: no diagnosis, class label or sufficiency flag is read.
    exception = by_path.get('/request_metadata/reported_exception')
    headers = [e for e in selected.values() if HEADER.fullmatch(e.reference)
               and e.value_type == 'str' and any(ord(c)>127 for c in e.observation)]
    if exception is None or exception.observation != EXCEPTION or not headers:
        return hold('No selected exact reported ASCII exception/non-ASCII header pair')
    # Header names are case-insensitive. Conflicting spellings must not select
    # whichever value happens to support the rule.
    names = {}
    for name,value in md.get('request_headers', {}).items():
        names.setdefault(name.casefold(), []).append(value)
    if any(len({json.dumps(v, sort_keys=True) for v in values})>1 for values in names.values()):
        return hold('Conflicting case-insensitive reported header values')
    if md.get('observation_representation') != ATTRIBUTION:
        return hold('Unknown or contradictory report attribution')
    attribution = by_path.get('/request_metadata/observation_representation')
    if attribution is None:
        return hold('Report attribution evidence not selected')
    try:
        association = Association.model_validate(md.get('reported_association'))
    except ValidationError:
        return hold('Missing or invalid explicit same-operation report association')
    if (association.method != incident.http_method or association.endpoint != incident.endpoint
            or not HEADER.fullmatch(association.header_pointer)):
        return hold('Report association operation/pointer mismatch')
    header = by_path.get(association.header_pointer)
    if header not in headers:
        return hold('Association header is not a selected non-ASCII header')
    # All association controls must themselves be selected, snapshot-bound data.
    controls = ['/request_metadata/reported_association/'+k
                for k in Association.model_fields]
    if any(p not in by_path for p in controls):
        return hold('Report association peers remain omitted')
    excerpt = by_path.get(association.statement_pointer)
    expected = statement(incident.http_method, incident.endpoint,
                         header.reference.rsplit('/',1)[1], header.observation)
    if excerpt is None or excerpt.value_type != 'str' or excerpt.observation != expected:
        return hold('Association statement does not resolve to the bounded literal relationship')
    # No inferred joins, fuzzy matching, appended instructions, or external lookup.
    entries = [header, exception, attribution, excerpt]+[by_path[p] for p in controls]
    anchors = tuple(Anchor(evidence_id=e.evidence_id, pointer=e.reference,
                          start=0, end=len(e.observation), literal=e.observation)
                    for e in entries)
    return Assessment(**base, qualified_analysis=True,
        reason='Selected attributed ASCII-header rejection permits qualified analysis only',
        rule='reported-ascii-header-rejection', provenance='reported_unverified', anchors=anchors)
