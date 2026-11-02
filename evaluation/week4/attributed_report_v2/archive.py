"""Bounded local archive resolution by content hash. No URL fetching or tools."""
import hashlib
import json
import re
from pathlib import Path
from .contracts import Document

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ARCHIVE = ROOT/'data/week4/report-evidence-v2-1/archive'


def encode(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()

class Archive:
    def __init__(self, directory=DEFAULT_ARCHIVE):
        self.directory = Path(directory).resolve()
        if not self.directory.is_relative_to(ROOT):
            raise ValueError('Archive must stay in the new project')

    def load(self, digest):
        if not isinstance(digest,str) or not re.fullmatch('[0-9a-f]{64}',digest):
            raise ValueError('Invalid archive digest')
        path = self.directory/(digest+'.json')
        if path.is_symlink() or not path.resolve().is_relative_to(self.directory):
            raise ValueError('Archive path escape')
        if path.stat().st_size>65536:
            raise ValueError('Archive document exceeds bound')
        data=path.read_bytes()
        if hashlib.sha256(data).hexdigest()!=digest:
            raise ValueError('Archive content hash mismatch')
        return Document.model_validate(json.loads(data))
