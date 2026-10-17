"""Build datasets/teamtrack-features-v1.jsonl (DESIGN §10.1, M5 builder contract §5).

Usage:
  uv run python scripts/build_features_dataset.py [--repo DIR] [--out FILE] [--check]

Reads the task manifests (teamtrack/reference/<task>/task.toml for F1-F7 and C1-C8) and the ticket
variants (datasets/sources/tickets.toml), collects hidden test ids statically from the files each
manifest lists for the line's checkpoint, and writes 60 lines in a fixed order:
7 canonical + 21 reworded + 8 alternate-checkpoint + 9 session-stop + 7 trap + 8 control.

Splits: `smoke` (F1-F4 canonical, C5, C6) and `section-1` ... `section-4` (for feature Fn:
canonical, three rewordings, two alternate checkpoints, trap, and control Cn). Every other line is
in `extended`, because a line needs at least one split.

Every line is checked with shipharness.datasets.features_checks before anything is written.
`--check` compares the generated text with the file on disk instead of writing it.
Exit codes: 0 written (or identical), 1 checks failed or the file differs, 2 a source is missing.
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path
from typing import Any

from shipharness.datasets.features_checks import (
    check_features_file,
    check_features_line,
    hidden_test_ids,
)

REPO = Path(__file__).resolve().parents[1]
FEATURES = ("F1", "F2", "F3", "F4", "F5", "F6", "F7")
CONTROLS = ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8")
STYLES = ("terse", "pm", "bug")
TICKETS = Path("datasets") / "sources" / "tickets.toml"
OUT = Path("datasets") / "teamtrack-features-v1.jsonl"
SMOKE = {"F1-canonical", "F2-canonical", "F3-canonical", "F4-canonical"}
SMOKE |= {"C5-canonical", "C6-canonical"}
SECTION_GROUPS = ("canonical", "reworded", "alt_checkpoint", "trap")


class DatasetSourceError(LookupError):
    """A manifest, the ticket sources, or an entry they need is missing."""


def manifest_path(task_id: str) -> Path:
    return Path("teamtrack") / "reference" / task_id.lower() / "task.toml"


def load_manifest(repo: Path, task_id: str) -> dict[str, Any]:
    path = repo / manifest_path(task_id)
    if not path.is_file():
        raise DatasetSourceError(f"missing task manifest {manifest_path(task_id).as_posix()}")
    return tomllib.loads(path.read_text(encoding="utf-8"))


def load_tickets(repo: Path) -> dict[str, list[dict[str, Any]]]:
    path = repo / TICKETS
    if not path.is_file():
        raise DatasetSourceError(f"missing ticket sources {TICKETS.as_posix()}")
    return tomllib.loads(path.read_text(encoding="utf-8"))


def hidden_for(repo: Path, manifest: dict[str, Any], checkpoint: str) -> list[str]:
    files = manifest.get("hidden", {}).get(checkpoint)
    if not files:
        raise DatasetSourceError(
            f"{manifest['id']}: {manifest_path(manifest['id']).as_posix()} has no [hidden] entry "
            f"for checkpoint {checkpoint}"
        )
    try:
        return hidden_test_ids(repo, list(files))
    except FileNotFoundError as exc:
        raise DatasetSourceError(f"{manifest['id']}: {exc}") from None


def make_line(
    repo: Path,
    manifest: dict[str, Any],
    *,
    group: str,
    example_id: str,
    variant: str,
    ticket: str | None = None,
    checkpoint: str | None = None,
    session_budget: list[int] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    task_id = str(manifest["id"])
    checkpoint = checkpoint or str(manifest["start_checkpoint"])
    metadata: dict[str, Any] = {
        "group": group,
        "example_id": example_id,
        "control": task_id.startswith("C"),
        "section": manifest["section"],
        "title": manifest["title"],
        "description": manifest["title"],
    }
    metadata.update(extra or {})
    return {
        "inputs": {
            "feature_id": task_id,
            "checkpoint": checkpoint,
            "ticket_text": ticket if ticket is not None else manifest["canonical_ticket"],
            "variant": variant,
            "session_budget": list(session_budget or manifest["session_budget"]),
        },
        "outputs": {
            "hidden_test_ids": hidden_for(repo, manifest, checkpoint),
            "allowed_paths": {
                "build": list(manifest["allowed_paths"]["build"]),
                "test": list(manifest["allowed_paths"]["test"]),
            },
            "mutant_set": manifest["mutant_set"],
            "primary_measure": manifest["primary_measure"],
        },
        "metadata": metadata,
        "split": [],
    }


def split_budget(total: int, share: float) -> list[int]:
    """Two sessions: `share` of the total turns (half up, at least 1 each), then the rest."""
    first = max(1, min(total - 1, int(total * share + 0.5)))
    return [first, total - first]


def entries(tickets: dict[str, list[dict[str, Any]]], group: str) -> list[dict[str, Any]]:
    found = tickets.get(group)
    if not found:
        raise DatasetSourceError(f"{TICKETS.as_posix()} has no [[{group}]] entries")
    return found


def find(items: list[dict[str, Any]], **keys: Any) -> dict[str, Any]:
    for item in items:
        if all(item.get(k) == v for k, v in keys.items()):
            return item
    wanted = ", ".join(f"{k}={v}" for k, v in keys.items())
    raise DatasetSourceError(f"{TICKETS.as_posix()}: no entry with {wanted}")


def build_lines(repo: Path) -> list[dict[str, Any]]:
    repo = Path(repo)
    manifests = {task_id: load_manifest(repo, task_id) for task_id in FEATURES + CONTROLS}
    tickets = load_tickets(repo)
    lines: list[dict[str, Any]] = []
    for f in FEATURES:
        lines.append(
            make_line(
                repo,
                manifests[f],
                group="canonical",
                example_id=f"{f}-canonical",
                variant="canonical",
            )
        )
    reworded = entries(tickets, "reworded")
    for f in FEATURES:
        for style in STYLES:
            entry = find(reworded, feature=f, style=style)
            lines.append(
                make_line(
                    repo,
                    manifests[f],
                    group="reworded",
                    example_id=f"{f}-reworded-{style}",
                    variant=f"reworded-{style}",
                    ticket=entry["text"],
                    extra={"style": style},
                )
            )
    for entry in entries(tickets, "alt_checkpoint"):
        f, checkpoint = entry["feature"], entry["checkpoint"]
        manifest = manifests[f]
        lines.append(
            make_line(
                repo,
                manifest,
                group="alt_checkpoint",
                example_id=f"{f}-{checkpoint.removeprefix('m1-')}",
                variant=f"alt-{checkpoint}",
                ticket=entry.get("text"),
                checkpoint=checkpoint,
                extra={"base_checkpoint": manifest["start_checkpoint"]},
            )
        )
    for entry in entries(tickets, "session_stop"):
        f, stop, share = entry["feature"], int(entry["stop"]), float(entry["first_session_share"])
        total = sum(int(n) for n in manifests[f]["session_budget"])
        lines.append(
            make_line(
                repo,
                manifests[f],
                group="session_stop",
                example_id=f"{f}-stop-{stop}",
                variant=f"stop-{stop}",
                ticket=entry.get("text"),
                session_budget=split_budget(total, share),
                extra={"stop": stop, "first_session_share": share},
            )
        )
    traps = entries(tickets, "trap")
    for f in FEATURES:
        entry = find(traps, feature=f)
        lines.append(
            make_line(
                repo,
                manifests[f],
                group="trap",
                example_id=f"{f}-trap",
                variant=f"trap-{entry['trap']}",
                ticket=entry["text"],
                extra={"trap": entry["trap"], "trap_detail": entry["trap_detail"]},
            )
        )
    for c in CONTROLS:
        lines.append(
            make_line(
                repo,
                manifests[c],
                group="control",
                example_id=f"{c}-canonical",
                variant="canonical",
            )
        )
    assign_splits(lines)
    return lines


def assign_splits(lines: list[dict[str, Any]]) -> None:
    for line in lines:
        meta, feature = line["metadata"], line["inputs"]["feature_id"]
        splits = set()
        if meta["example_id"] in SMOKE:
            splits.add("smoke")
        number = feature[1:]
        if feature in FEATURES[:4] and meta["group"] in SECTION_GROUPS:
            splits.add(f"section-{number}")
        if feature in CONTROLS[:4]:
            splits.add(f"section-{number}")
        line["split"] = sorted(splits) or ["extended"]


def render(lines: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(line, ensure_ascii=False) + "\n" for line in lines)


def check(lines: list[dict[str, Any]], repo: Path) -> list[str]:
    problems = check_features_file(lines)
    for line in lines:
        problems += check_features_line(line, repo)
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", type=Path, default=REPO, help="course repository root")
    parser.add_argument("--out", type=Path, help=f"output file (default: <repo>/{OUT.as_posix()})")
    parser.add_argument("--check", action="store_true", help="compare with --out, do not write")
    args = parser.parse_args(argv)
    out = args.out or args.repo / OUT
    try:
        lines = build_lines(args.repo)
    except DatasetSourceError as exc:
        print(f"x {exc}", file=sys.stderr)
        return 2
    problems = check(lines, args.repo)
    if problems:
        for problem in problems:
            print(f"x {problem}")
        print(f"{len(problems)} problem(s); nothing written")
        return 1
    text = render(lines)
    if args.check:
        current = out.read_text(encoding="utf-8") if out.is_file() else ""
        if current != text:
            print(f"x {out} differs from the generated dataset")
            return 1
        print(f"{out} is up to date ({len(lines)} lines)")
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(text.encode("utf-8"))
    print(f"wrote {out} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
