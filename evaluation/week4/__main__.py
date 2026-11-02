"""Only built-in development fixtures and mock transport are executable."""
import argparse
from pathlib import Path
from .runner import run_batch
from .fixtures import development_cases, mock_reply
from .tracing import FakeTracingSink


def main():
    parser = argparse.ArgumentParser(description='Offline mock evaluation only; no live/export mode')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--experiment', required=True)
    args = parser.parse_args()
    _, summary = run_batch(development_cases(), args.output, experiment=args.experiment,
                           reply_factory=lambda case: mock_reply, sink=FakeTracingSink())
    import json
    print(json.dumps(summary, indent=2))
    return 1 if summary['failed'] or summary['stop_reason'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
