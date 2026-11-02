"""Offline version verification against the inherited complete hash lock."""
import hashlib
import importlib.metadata
from pathlib import Path
import re
import sys


def verify_lock():
    root = Path(__file__).resolve().parents[2]
    lock = root/'requirements.lock'
    pins = dict(re.findall(r'^([\w-]+)==([^\s\\]+)', lock.read_text(), re.MULTILINE))
    mismatches = []
    for name, expected in pins.items():
        try: actual = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: actual = 'missing'
        if actual != expected: mismatches.append((name, expected, actual))
    expected_python = (Path(__file__).parent/'.python-version').read_text().strip()
    if '.'.join(map(str,sys.version_info[:3])) != expected_python:
        mismatches.append(('python',expected_python,sys.version.split()[0]))
    if mismatches: raise RuntimeError(f'Week 4 dependency mismatch: {mismatches}')
    return {'pins_checked':len(pins), 'python':expected_python,
            'lock_sha256':hashlib.sha256(lock.read_bytes()).hexdigest(), 'mismatches':[],
            'artifact_integrity':'installed versions checked; reinstall --require-hashes to verify distribution archives'}

if __name__=='__main__':
    import json
    print(json.dumps(verify_lock(),indent=2))
