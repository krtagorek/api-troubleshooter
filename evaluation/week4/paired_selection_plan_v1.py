"""Validate a prepared two-arm manifest; reuse single-case supervisor/journals."""
import hashlib
import json
from pathlib import Path
from .live_config import LiveConfig, V2, SELECTION_V1, CASE016_BUDGET_PROFILE
from .accounting import money
from .contracts import BoundaryFailure

VERSION = 'week4-real-016-v2-selection-pair-1'


def validate_arm(plan):
    from .runner import ROOT, digest
    path = plan.get('comparison_manifest_path')
    if path not in plan.get('component_hashes', {}):
        raise ValueError('Comparison manifest must be component-bound')
    manifest = json.loads((ROOT/path).read_text())
    if (manifest.get('version') != VERSION or manifest.get('comparison_id') != plan.get('comparison_id')
            or manifest.get('trace_export_authorized') is not False or manifest.get('external_tracing') is not False
            or manifest.get('incident_tools') is not False or manifest.get('concurrency') != 1
            or manifest.get('retries') != 0 or set(manifest.get('arms', {})) != {'baseline','treatment'}
            or manifest.get('case_sha256') != plan['case_sha256'] or manifest.get('source_hashes') != plan['source_hashes']
            or manifest.get('input_bytes_sha256') != plan['input_bytes_sha256']
            or manifest.get('archive_sha256') != plan['archive_sha256']):
        raise ValueError('Comparison manifest identity/limits mismatch')
    configs = {}
    for name, policy in (('baseline','off'),('treatment',SELECTION_V1)):
        arm = manifest['arms'][name]
        config = LiveConfig(**arm['config'])
        if (config.selection_policy != policy or config.evidence_policy != V2
                or config.budget_profile != CASE016_BUDGET_PROFILE or money(config.max_usd) != money('2.25')
                or config.max_calls != 5 or digest(arm['config']) != arm['configuration_sha256']):
            raise ValueError('Comparison arm configuration mismatch')
        output = (ROOT/arm['output_path']).resolve()
        if not output.is_relative_to(ROOT/'reports/week4') or output == ROOT/'reports/week4':
            raise ValueError('Comparison output must stay in reports/week4')
        configs[name] = config.public()
    b = dict(configs['baseline']); t = dict(configs['treatment'])
    b.pop('selection_policy');t.pop('selection_policy')
    if b != t or manifest['arms']['baseline']['output_path'] == manifest['arms']['treatment']['output_path']:
        raise ValueError('Arms differ beyond explicit selection policy or reuse output')
    if money(manifest.get('combined_ceiling_usd')) != sum(money(c['max_usd']) for c in configs.values()):
        raise ValueError('Combined ceiling does not equal bounded arm ceilings')
    name = plan.get('arm')
    if name not in configs or plan['config'] != manifest['arms'][name]['config'] or plan.get('output_path') != manifest['arms'][name]['output_path']:
        raise ValueError('Plan does not match bound comparison arm')
    return manifest


def check_dispatch(plan, output_dir):
    from .runner import ROOT, digest
    manifest = validate_arm(plan)
    output = Path(output_dir).resolve()
    if output != (ROOT/plan['output_path']).resolve() or output.exists():
        raise BoundaryFailure('Comparison arm output changed or already claimed; never retry')
    if plan['arm'] == 'baseline':
        return
    # With one baseline and one treatment directory, atomic mkdir prevents arm
    # reuse. Treatment cannot start before baseline is finished and reaped.
    baseline = ROOT/manifest['arms']['baseline']['output_path']
    try:
        hashes = json.loads((baseline/'artifact-hashes.json').read_text())
        if any(Path(name).name != name or hashlib.sha256((baseline/name).read_bytes()).hexdigest()!=h
               for name,h in hashes.items()):
            raise ValueError('Baseline output hash mismatch')
        result = json.loads((baseline/'result.json').read_text())
        meta = json.loads((baseline/'experiment.json').read_text())
        if (result['terminal_status'] not in ('held','completed') or result['errors']
                or result['mode'] != 'live' or not result['supervisor']['cleanup_verified']
                or result['accounting']['uncertain_calls'] or result['accounting']['limit_violations']
                or meta['config'] != manifest['arms']['baseline']['config']
                or meta['input_sha256'] != plan['case_sha256'] or meta['source_hashes'] != plan['source_hashes']):
            raise ValueError('Baseline outcome/accounting/identity is not safe for treatment')
    except (OSError,ValueError,KeyError,TypeError) as exc:
        raise BoundaryFailure('Treatment requires a finished, matching, reconciled baseline') from None
