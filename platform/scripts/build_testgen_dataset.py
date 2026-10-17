"""Build platform/datasets/testgen-targets-v1.jsonl from its sources/testgen.toml (deterministic).

One line per target (CONTRACTS §16.2): 20 TeamTrack modules, 10 boltons and 10 WTForms modules.
Mutant references point at `<mutants_dir>/<module>.jsonl#filter` and `#referee`; the number of
mutants in each set is recorded in the metadata.

Usage:
  uv run python platform/scripts/build_testgen_dataset.py           # write the file
  uv run python platform/scripts/build_testgen_dataset.py --check   # exit 1 if the file is stale
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path, PurePosixPath
from typing import Any

from shipharness.layout import resolve

REPO = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file())
SOURCES = Path("datasets") / "sources" / "testgen.toml"
OUT = REPO / "platform" / "datasets" / "testgen-targets-v1.jsonl"
SPLIT = "testgen"


def dotted_module(module: str) -> str:
    parts = list(PurePosixPath(module).with_suffix("").parts)
    if parts and parts[0] == "src":
        parts = parts[1:]
    return ".".join(parts)


def _set_counts(path: Path) -> dict[str, int]:
    counts = {"filter": 0, "referee": 0}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            counts[json.loads(raw)["set"]] += 1
    return counts


def build_line(repo_root: Path, name: str, repo: dict[str, Any], target: dict[str, Any]) -> dict:
    module = target["module"]
    dotted = dotted_module(module)
    stem = dotted.removeprefix(repo["package_prefix"])
    mutants = f"{repo['mutants_dir']}/{stem}.jsonl"
    target_id = f"TG-{name}-{stem.replace('.', '-')}"
    metadata: dict[str, Any] = {
        "example_id": target_id,
        "source": repo["source"],
        "group": name,
        "target": dotted,
        "license": repo["license"],
        "commit": repo["commit"],
        "mutants": _set_counts(resolve(Path(repo_root), mutants)),
    }
    metadata.update(repo.get("metadata", {}))
    return {
        "inputs": {
            "target_id": target_id,
            "repo": name,
            "pin": repo["pin"],
            "module": module,
            "existing_tests": list(target["existing_tests"]),
        },
        "outputs": {
            "filter_mutants": f"{mutants}#filter",
            "referee_mutants": f"{mutants}#referee",
            "known_failures": list(repo["known_failures"]),
        },
        "metadata": metadata,
        "split": [SPLIT],
    }


def build_lines(repo_root: Path = REPO) -> list[dict[str, Any]]:
    sources = tomllib.loads(
        resolve(Path(repo_root), SOURCES.as_posix()).read_text(encoding="utf-8")
    )
    from shipharness.datasets.schema import TestgenTarget

    repos = sources["repos"]
    lines = [
        build_line(repo_root, target["repo"], repos[target["repo"]], target)
        for target in sources["targets"]
    ]
    for line in lines:
        TestgenTarget.model_validate(line)  # raises on a malformed line
    return lines


def render(lines: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(line, ensure_ascii=False) + "\n" for line in lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--check", action="store_true", help="fail if the file is out of date")
    args = parser.parse_args(argv)
    text = render(build_lines(REPO))
    if args.check:
        current = args.out.read_text(encoding="utf-8") if args.out.is_file() else None
        if current != text:
            print(
                f"x {args.out} is out of date: run platform/scripts/build_testgen_dataset.py",
                file=sys.stderr,
            )
            return 1
        print(f"ok {args.out} is up to date")
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(text.encode("utf-8"))
    print(f"wrote {len(text.splitlines())} lines to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
