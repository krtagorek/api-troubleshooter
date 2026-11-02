"""Validated single-smoke settings; no default model or invented prices."""
from dataclasses import dataclass, asdict
from .accounting import money

V2 = 'attributed-report-readiness-v2'
# Documented model context ceiling, not a tokenizer/character estimate. Reserving
# the entire context also covers unknown provider-side Chat/schema framing.
MODEL_CONTEXT_LIMITS = {'gpt-4.1-mini-2025-04-14': 1047576}
DEFAULT_BUDGET_PROFILE = 'week4-025'
CASE016_BUDGET_PROFILE = 'real-016-v2-proposal-3'
SELECTION_V1 = 'attributed-selection-dependencies-v1'
MANIFEST_BUDGET_PROFILE = 'week4-case-manifest-1'

@dataclass(frozen=True)
class LiveConfig:
    model: str
    input_per_million: str
    output_per_million: str
    pricing_source: str
    pricing_verified_at: str
    cached_input_per_million: str | None = None
    max_usd: str = '0.25'
    max_calls: int = 5
    input_cap: int = 32768
    output_cap: int = 1536
    case_timeout_seconds: float = 120
    call_timeout_seconds: float = 30
    evidence_policy: str = 'inherited'
    service_tier: str = 'default'
    input_bound_kind: str = 'legacy_byte_proxy'
    max_request_bytes: int = 65536
    budget_profile: str = DEFAULT_BUDGET_PROFILE
    selection_policy: str = 'off'
    reviewed_targets: bool = False

    def __post_init__(self):
        if not self.model or not self.pricing_source.startswith('https://') or not self.pricing_verified_at:
            raise ValueError('Explicit snapshot and verified pricing provenance are required')
        for rate in (self.input_per_million, self.output_per_million):
            if money(rate) <= 0: raise ValueError('Verified positive rates are required')
        if self.cached_input_per_million is not None:
            if money(self.cached_input_per_million) > money(self.input_per_million):
                raise ValueError('Cached input rate exceeds conservative input rate')
        ceilings = {DEFAULT_BUDGET_PROFILE:'0.25', CASE016_BUDGET_PROFILE:'2.25', MANIFEST_BUDGET_PROFILE:'2.25'}
        if self.budget_profile not in ceilings:
            raise ValueError('Unknown budget profile')
        if self.budget_profile == CASE016_BUDGET_PROFILE and self.evidence_policy != V2:
            raise ValueError('Proposal-3 ceiling requires explicit V2')
        if not 0 < money(self.max_usd) <= money(ceilings[self.budget_profile]):
            raise ValueError('Money ceiling exceeds the selected budget profile')
        if type(self.max_calls) is not int or not 1 <= self.max_calls <= 5:
            raise ValueError('Smoke allows 1..5 calls')
        if self.evidence_policy not in ('inherited', V2):
            raise ValueError('Unknown evidence policy; no fallback')
        if self.selection_policy not in ('off', SELECTION_V1):
            raise ValueError('Unknown selection policy; no fallback')
        if self.selection_policy != 'off' and self.evidence_policy != V2:
            raise ValueError('Selection dependencies require explicit V2')
        if type(self.reviewed_targets) is not bool or (self.reviewed_targets and
                (self.evidence_policy != V2 or self.selection_policy != SELECTION_V1 or
                 self.budget_profile != MANIFEST_BUDGET_PROFILE)):
            raise ValueError('Reviewed targets require explicit V2/dependencies in the manifest path')
        if self.service_tier != 'default':
            raise ValueError('Only explicit default service tier is supported')
        if type(self.max_request_bytes) is not int or not 1 <= self.max_request_bytes <= 65536:
            raise ValueError('Invalid complete request byte bound')
        if self.evidence_policy == V2 or self.budget_profile == MANIFEST_BUDGET_PROFILE:
            if (self.input_bound_kind != 'model_context_max' or
                self.model not in MODEL_CONTEXT_LIMITS or
                type(self.input_cap) is not int or self.input_cap != MODEL_CONTEXT_LIMITS[self.model]):
                raise ValueError('V2 requires the pinned model full-context reservation')
        elif (self.input_bound_kind != 'legacy_byte_proxy' or type(self.input_cap) is not int
              or not 4096 < self.input_cap <= 32768):
            raise ValueError('Invalid input cap')
        if type(self.output_cap) is not int or not 1 <= self.output_cap <= 1536:
            raise ValueError('Invalid output cap')
        if not 0 < self.call_timeout_seconds <= 30 or not 0 < self.case_timeout_seconds <= 120:
            raise ValueError('Invalid finite timeouts')

    def public(self): return asdict(self)
