"""Distinct quotation, editorial attribution, relationship and correlation types."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

VERSION = 'attributed-report-readiness-v2'

class Closed(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True, strict=True)

class Block(Closed):
    kind: Literal['verbatim_source_excerpt']
    location: str
    scope: str  # Editorial grouping in the archive, not a captured request ID.
    text: str = Field(min_length=1,max_length=8192)

class Relationship(Closed):
    kind: Literal['reporter_associated_reproduction']
    scope: str
    summary_kind: Literal['attributed_editorial_summary']
    summary: str
    roles: dict[str,str]
    authenticated_request_correlation: Literal[False]

class Document(Closed):
    version: Literal['reported-excerpt-archive-1']
    source_uri: str
    origin: Literal['prior_public_page_excerpt_transcription','synthetic_fixture']
    capture_basis: str
    raw_capture_sha256: None
    blocks: dict[str,Block]
    relationships: dict[str,Relationship]

class SourceAnchor(Closed):
    kind: Literal['verbatim_source_excerpt']
    block: str
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    literal: str = Field(min_length=1)

class Attribution(Closed):
    version: Literal['attributed-report-readiness-v2']
    source_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    relationship: str
    kind: Literal['reporter_associated_reproduction']
    summary_kind: Literal['attributed_editorial_summary']
    summary: str
    authenticated_request_correlation: Literal[False]
    method: str
    endpoint: str
    header_pointer: str
    exception_pointer: Literal['/request_metadata/reported_exception']
    anchors: dict[str,SourceAnchor]

class Assessment(Closed):
    version: Literal['attributed-report-readiness-v2'] = VERSION
    snapshot: str
    qualified_analysis: bool
    definitive_confirmation: Literal[False] = False
    reason: str
    legacy_reason: str
    legacy_qualified_analysis: bool
    rule: Literal['reported-ascii-header-rejection'] | None = None
    provenance: Literal['reported_unverified'] | None = None
    source_sha256: str | None = None
    relationship: str | None = None
    resolved_anchors: tuple[SourceAnchor,...] = ()
    evidence_ids: tuple[str,...] = ()
    limitations: tuple[str,...] = (
        'Literal excerpt binding does not authenticate source truth.',
        'Editorial summary is not a verbatim quotation.',
        'Reporter-associated reproduction is not authenticated request correlation.',
        'No independent reproduction, successful comparison or verified remediation.',
        'Qualified analysis does not authorize execution or publication.',
    )
