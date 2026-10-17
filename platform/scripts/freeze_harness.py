"""Create the `harness-frozen` tag when the M6 pilot gate passes (DESIGN §10.4).

    uv run python platform/scripts/freeze_harness.py --dry-run   # print the record, change nothing
    uv run python platform/scripts/freeze_harness.py             # tag HEAD

Refuses when the tag exists or frozen paths have uncommitted changes. Prints the tag and its commit
for VERIFICATION.md. Secrets are never read into the record.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from shipharness import freeze
from shipharness.config import Settings

REPO = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file())
IDENTITY = ("ANI-IN", "44803072+ANI-IN@users.noreply.github.com")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    effective = Settings(_env_file=REPO / ".env")
    if args.dry_run:
        print(json.dumps(freeze.make_record(REPO, effective), indent=2, sort_keys=True))
        return 0
    try:
        commit = freeze.create_tag(REPO, effective, identity=IDENTITY)
    except freeze.FreezeError as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1
    print(f"tagged {freeze.TAG} at {commit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
