"""Closed, versioned report-only attribution and assessment contracts."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

VERSION = 'attributed-report-readiness-v1'
EXCEPTION = ('System.Net.Http.HttpRequestException: '
             'Request headers must contain only ASCII characters.')

class Closed(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True, strict=True)

class Association(Closed):
    """A literal reported-operation statement, not authenticated correlation.

    Accepted only from request_metadata.reported_association. Its statement must
    exist verbatim in a selected catalog scalar, not be authored by the adapter.
    V1 intentionally recognizes one bounded statement grammar, not arbitrary prose.
    """
    version: Literal['attributed-report-readiness-v1']
    kind: Literal['reporter_statement']
    scope: Literal['single_reported_operation']
    method: str
    endpoint: str
    header_pointer: str
    exception_pointer: Literal['/request_metadata/reported_exception']
    statement_pointer: Literal['/request_metadata/reported_operation_excerpt']

class Anchor(Closed):
    evidence_id: str
    pointer: str
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    literal: str

class Assessment(Closed):
    version: Literal['attributed-report-readiness-v1'] = VERSION
    snapshot: str
    qualified_analysis: bool
    definitive_confirmation: Literal[False] = False
    reason: str
    legacy_reason: str
    legacy_qualified_analysis: bool
    rule: Literal['reported-ascii-header-rejection'] | None = None
    provenance: Literal['reported_unverified'] | None = None
    anchors: tuple[Anchor, ...] = ()
    limitations: tuple[str, ...] = (
        'Reported association is not authenticated trace correlation.',
        'No independent reproduction, successful comparison or origin confirmation.',
        'Qualified analysis does not authorize publication or execution.',
    )
