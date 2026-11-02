"""Terminal-only launcher for the already approved, single bounded smoke.

No secrets are loaded from files. Default invocation can incur the approved cost.
--check-only cannot launch inference or create an authorization copy.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / 'data/week4/smoke-proposals/real-016-v2-3'
EXPECTED = '69e756641250cd698921804cb4dbde0757c6c9e84fa75c04821c29e8b7446acb'
IDENTITY = 'a996d40dd93440d58ed722e2eb9999d98d40a9165d676300db6ac5b1aa8322b4'
DESTINATION = ROOT / 'reports/week4/real-016-v2-3-approved-live-1'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verify_seal(directory):
    manifest = json.loads((directory / 'artifact-hashes.json').read_text())
    require(all(sha(directory / name) == value for name, value in manifest.items()),
            'Sealed artifact mismatch: ' + str(directory.relative_to(ROOT)))


def verify_bindings(plan):
    require(sha(PROPOSAL / 'plan.json') == EXPECTED, 'Approved proposal hash mismatch')
    for group in ('source_hashes', 'component_hashes'):
        require(all(sha(ROOT / name) == value for name, value in plan[group].items()),
                'Proposal binding mismatch: ' + group)
    baseline = ROOT / 'docs/source-baseline-manifest.json'
    require(sha(baseline) == '0ad4421d9342b780996b70de8b72d9d0cab1b771e6f37fd82dd4c5ccbf42b62f',
            'Baseline manifest mismatch')
    entries = json.loads(baseline.read_text())['files']
    require(len(entries) == 328 and all(sha(ROOT / e['destination_relative_path']) == e['sha256'] for e in entries),
            'Inherited baseline mismatch')
    verify_seal(PROPOSAL)


def write_new(path, value):
    with path.open('x', encoding='utf-8') as handle:
        os.chmod(path, 0o600)
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
        handle.flush()
        os.fsync(handle.fileno())


def main(check_only=False):
    os.chdir(ROOT)
    require(Path(sys.prefix).resolve() == (ROOT / '.venv-week4-locked').resolve(),
            'Use .venv-week4-locked/bin/python')
    require('WEEK4_OPENAI_API_KEY' in os.environ,
            'WEEK4_OPENAI_API_KEY is absent in this terminal. Export it privately here; no key file is read.')
    require(not DESTINATION.exists(), 'Single-run destination already exists. Do not retry; inspect its journal/results.')
    plan = json.loads((PROPOSAL / 'plan.json').read_text())
    verify_bindings(plan)
    receipt_dir = ROOT / 'reports/week4/smoke016-v2-3-environment-preparation-1'
    verify_seal(receipt_dir)
    receipt = json.loads((receipt_dir / 'result.json').read_text())
    require(receipt['archive_integrity']['status'] == 'PASS_HASH_LOCKED_INSTALL' and
            receipt['archive_integrity']['install_exit_code'] == 0 and
            receipt['dependency_versions']['lock_sha256'] == sha(ROOT / 'requirements.lock'),
            'Hash-locked installation receipt missing or mismatched')
    checked = subprocess.run([
        '/usr/bin/sandbox-exec', '-p', '(version 1) (allow default) (deny network*)',
        sys.executable, '-m', 'scripts.week4_smoke016_v2_3_approval_preflight'],
        cwd=ROOT, capture_output=True, text=True, check=True)
    preflight = json.loads(checked.stdout)
    require(preflight['plan_sha256'] == EXPECTED and
            preflight['immutable_authorization_identity_sha256'] == IDENTITY and
            preflight['credential_presence']['WEEK4_OPENAI_API_KEY'] is True and
            not any(preflight['guard_attempts'].values()) and
            preflight['dependencies']['mismatches'] == [] and
            preflight['authorization_rejected'] is True,
            'Offline preflight mismatch')
    # The existing preflight has this fixed historical message. The sealed,
    # successful fresh-install receipt above resolves it; no other blocker is waived.
    require(preflight['remaining_setup_blockers'] == [
        'Hash-locked archive installation not performed; version check is not archive-integrity proof.'],
        'Unexpected setup blocker')
    if check_only:
        print('PASS: terminal preflight only; no authorization copy or model call created.')
        return 0
    # Disable ambient exports before importing provider/graph modules. The existing
    # supervised worker independently applies its own stricter allowlist as well.
    for name in tuple(os.environ):
        if name.startswith(('LANGSMITH_', 'LANGCHAIN_', 'OTEL_','WEEK4_LANGSMITH_')):
            os.environ.pop(name, None)
    os.environ.update(LANGSMITH_TRACING='false', LANGCHAIN_TRACING_V2='false',
                      LANGCHAIN_TRACING='false', LANGSMITH_OTEL_ENABLED='false',
                      OTEL_SDK_DISABLED='true', OTEL_TRACES_EXPORTER='none')
    from evaluation.week4.live_cli import load_plan, authorization_identity, require_execution_authorization
    loaded, config = load_plan(PROPOSAL / 'plan.json')
    require(authorization_identity(loaded) == IDENTITY, 'Immutable authorization identity mismatch')
    require(config.model == 'gpt-4.1-mini-2025-04-14' and config.service_tier == 'default' and
            config.max_usd == '2.25' and config.max_calls == 5 and
            config.evidence_policy == 'attributed-report-readiness-v2', 'Approved run limits mismatch')
    DESTINATION.mkdir(mode=0o700, exist_ok=False)  # Durable single-use claim; never delete to retry.
    recorded = datetime.now(timezone.utc).isoformat()
    write_new(DESTINATION / 'authorization.json', {
        'approval_identity': 'User in this conversation', 'approval_time': None,
        'approval_time_note': 'Exact message timestamp unavailable; not invented.',
        'record_created_at_utc': recorded, 'approved_plan_sha256': EXPECTED,
        'immutable_authorization_identity_sha256': IDENTITY,
        'source': 'Explicit user approval of the exact real-016-v2-3 SHA-256 and subsequent instructions to execute.',
        'max_usd': '2.25', 'max_calls': 5, 'concurrency': 1, 'retries': 0,
        'trace_export_authorized': False, 'incident_tools': False})
    # The supported loader requires a nonempty approval_time string, not ISO time.
    # Preserve the honest provenance text rather than invent a historical timestamp.
    loaded.update(execution_authorized=True, approval_identity='User in this conversation',
                  approval_time='Previously explicitly approved in this conversation; exact message timestamp unavailable',
                  approval_binding_sha256=IDENTITY)
    require_execution_authorization(loaded)
    launch = DESTINATION / 'authorized-plan.json'
    write_new(launch, loaded)
    launch.chmod(0o400)
    load_plan(launch)
    print('Launching the already approved smoke once. Maximum $2.25; five calls; zero retries; no exports.', flush=True)
    completed = subprocess.run([sys.executable, '-m', 'evaluation.week4.live_cli', 'run',
        '--plan', str(launch), '--output', str(DESTINATION / 'run'), '--execute-live'], cwd=ROOT)
    verify_bindings(plan)
    write_new(DESTINATION / 'launcher-outcome.json', {
        'supervised_cli_exit_code': completed.returncode, 'sealed_proposal_and_baseline': 'UNCHANGED',
        'retry_performed': False, 'result_directory': str((DESTINATION / 'run').relative_to(ROOT)),
        'note': 'Inspect actual result/journal; a nonzero exit never authorizes a retry.'})
    print('Results: ' + str(DESTINATION.relative_to(ROOT)), flush=True)
    return completed.returncode


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    try:
        raise SystemExit(main(args.check_only))
    except (RuntimeError, subprocess.CalledProcessError, ValueError, KeyError, OSError) as exc:
        # Do not print arbitrary provider errors or environment contents.
        print('STOP: ' + (str(exc) if isinstance(exc, RuntimeError) else type(exc).__name__), file=sys.stderr)
        raise SystemExit(1)
