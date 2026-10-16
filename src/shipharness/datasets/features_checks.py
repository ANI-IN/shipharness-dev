"""Checks for `teamtrack-features-v1` beyond the line schema (M5 builder contract §5).

`check_features_line(line, repo)` checks one line against the course repository: the checkpoint is
defined in `teamtrack/reference/checkpoints.toml`, every hidden test id exists in its file, the
mutant set resolves to a non-empty referee set, the primary measure parses against `ScoreRecord`
(and is the measure registered for the feature, ruling R-5), and the allowed paths are non-empty
relative globs. `check_features_file(lines)` checks the whole file: group counts, split sizes,
unique example ids. Both return a list of messages; an empty list means the check passed.
"""

from __future__ import annotations

import ast
import tomllib
import types
import typing
from collections import Counter
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from pydantic import BaseModel, ValidationError

from shipharness.ab.score import ScoreRecord, evaluate_primary
from shipharness.datasets.schema import FeatureTask

APP_DIR = "teamtrack"
CHECKPOINTS_FILE = Path(APP_DIR) / "reference" / "checkpoints.toml"
HIDDEN_PREFIX = "tests/hidden/"

# Design §10.1 and the contract: 7 + 21 + 8 + 9 + 7 + 8 = 60 lines.
GROUP_COUNTS: dict[str, int] = {
    "canonical": 7,
    "reworded": 21,
    "alt_checkpoint": 8,
    "session_stop": 9,
    "trap": 7,
    "control": 8,
}
TOTAL_LINES = 60
SPLIT_SIZES: dict[str, int] = {
    "smoke": 6,
    "section-1": 8,
    "section-2": 8,
    "section-3": 8,
    "section-4": 8,
}
# Ruling R-5: the pre-registered primary measure per feature; F5-F7 and controls have none.
REGISTERED_PRIMARY: dict[str, str] = {
    "F1": "r1_new_violations>=1",
    "F2": "continuity_failure",
    "F3": "out_of_scope_files>=1 or test_phase_source_edits>=1",
    "F4": "hidden_passed,mutants_killed",
    "F5": "",
    "F6": "",
    "F7": "",
}


# -- hidden tests -------------------------------------------------------------------------------


def _is_parametrized(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any("parametrize" in ast.unparse(d) for d in node.decorator_list)


def collect_tests(path: Path) -> dict[str, bool]:
    """Test names pytest would collect from one file, read statically (the file is never
    imported): `test_x` or `TestGroup::test_x` -> True when the test is parametrized. A
    parametrized test gets ids like `test_x[1]`, which a dataset id `file::test_x` never matches."""
    tree = ast.parse(Path(path).read_text(encoding="utf-8"), filename=str(path))
    found: dict[str, bool] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith(
            "test"
        ):
            found[node.name] = _is_parametrized(node)
        elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            for item in node.body:
                if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef) and (
                    item.name.startswith("test")
                ):
                    found[f"{node.name}::{item.name}"] = _is_parametrized(item)
    return found


def hidden_test_ids(repo: Path, files: list[str]) -> list[str]:
    """Node ids (relative to the TeamTrack root, ruling R-1) for every test in `files`."""
    ids: list[str] = []
    for rel in files:
        path = Path(repo) / APP_DIR / rel
        if not path.is_file():
            raise FileNotFoundError(f"hidden test file {APP_DIR}/{rel} does not exist")
        ids += [f"{rel}::{name}" for name in collect_tests(path)]
    return ids


def _check_hidden(ids: list[str], repo: Path) -> list[str]:
    if not ids:
        return ["outputs.hidden_test_ids: no hidden test ids"]
    errors: list[str] = []
    cache: dict[str, dict[str, bool] | None] = {}
    for node_id in ids:
        rel, sep, name = node_id.partition("::")
        if not sep or not name or not rel.startswith(HIDDEN_PREFIX):
            errors.append(
                f"hidden id {node_id!r}: expected '{HIDDEN_PREFIX}<task>/<file>.py::<test>' "
                "(relative to the TeamTrack root, ruling R-1)"
            )
            continue
        if rel not in cache:
            path = Path(repo) / APP_DIR / rel
            cache[rel] = collect_tests(path) if path.is_file() else None
        tests = cache[rel]
        if tests is None:
            errors.append(f"hidden id {node_id!r}: file {APP_DIR}/{rel} does not exist")
        elif name not in tests:
            errors.append(f"hidden id {node_id!r}: no test {name!r} in {APP_DIR}/{rel}")
        elif tests[name]:
            errors.append(
                f"hidden id {node_id!r}: parametrized tests get ids the referee cannot match"
            )
    return errors


# -- checkpoints --------------------------------------------------------------------------------


def checkpoint_names(repo: Path) -> set[str]:
    """Checkpoint names defined in `teamtrack/reference/checkpoints.toml`. Accepts a
    `[checkpoints.<name>]` table, top-level `[<name>]` tables, or `[[checkpoint]]` entries with a
    `name`. INTEGRATION: switch to `shipharness.ab.checkpoints.load_checkpoints()` once merged."""
    path = Path(repo) / CHECKPOINTS_FILE
    if not path.is_file():
        raise FileNotFoundError(f"{CHECKPOINTS_FILE.as_posix()} not found")
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    if isinstance(data.get("checkpoints"), dict):
        return set(data["checkpoints"])
    if isinstance(data.get("checkpoint"), list):
        return {str(entry["name"]) for entry in data["checkpoint"] if "name" in entry}
    return {name for name, value in data.items() if isinstance(value, dict)}


# -- primary measure ----------------------------------------------------------------------------


def _is_bool_field(name: str) -> bool:
    annotation = ScoreRecord.model_fields[name].annotation
    if annotation is bool:
        return True
    if isinstance(annotation, types.UnionType) or typing.get_origin(annotation) is typing.Union:
        args = {a for a in typing.get_args(annotation) if a is not type(None)}
        return args == {bool}
    return False


def _check_primary(measure: str, feature_id: str) -> list[str]:
    text = measure.strip()
    errors: list[str] = []
    dummy: dict[str, Any] = dict.fromkeys(ScoreRecord.model_fields, 0)
    try:
        evaluate_primary(text, dummy)
    except KeyError as exc:
        return [f"outputs.primary_measure {measure!r}: unknown ScoreRecord field {exc.args[0]!r}"]
    except (TypeError, ValueError) as exc:
        return [f"outputs.primary_measure {measure!r}: does not parse ({exc})"]
    if text and "," not in text:
        for term in (t.strip() for t in text.split(" or ")):
            if term in ScoreRecord.model_fields and not _is_bool_field(term):
                errors.append(
                    f"outputs.primary_measure {measure!r}: bare field {term!r} is not boolean"
                )
    expected = REGISTERED_PRIMARY.get(feature_id, "" if feature_id.startswith("C") else None)
    if expected is not None and text != expected:
        errors.append(
            f"outputs.primary_measure {measure!r}: {feature_id} registers {expected!r} (ruling R-5)"
        )
    return errors


# -- mutants and paths --------------------------------------------------------------------------


def _check_mutants(mutant_set: str, repo: Path) -> list[str]:
    from shipharness.ab.mutants import load_referee_mutants
    from shipharness.filters.mutants import MutantError

    try:
        mutants = load_referee_mutants(mutant_set, Path(repo))
    except (ValueError, MutantError) as exc:
        return [f"outputs.mutant_set {mutant_set!r}: {exc}"]
    if not mutants:
        return [f"outputs.mutant_set {mutant_set!r}: no referee mutants"]
    return []


def _bad_glob(pattern: str) -> bool:
    return (
        not pattern.strip()
        or "\\" in pattern
        or pattern.startswith("/")
        or bool(PureWindowsPath(pattern).drive)
        or ".." in PurePosixPath(pattern).parts
    )


def _check_paths(allowed: dict[str, list[str]]) -> list[str]:
    errors: list[str] = []
    for phase in ("build", "test"):
        patterns = allowed.get(phase)  # type: ignore[call-overload]
        if not patterns:
            errors.append(f"outputs.allowed_paths.{phase}: missing or empty")
            continue
        errors += [
            f"outputs.allowed_paths.{phase}: {p!r} is not a relative POSIX glob"
            for p in patterns
            if _bad_glob(p)
        ]
    return errors


# -- entry points -------------------------------------------------------------------------------


def _as_task(line: FeatureTask | BaseModel | dict[str, Any]) -> FeatureTask:
    if isinstance(line, FeatureTask):
        return line
    data = line.model_dump(mode="json") if isinstance(line, BaseModel) else line
    return FeatureTask.model_validate(data)


def check_features_line(line: FeatureTask | dict[str, Any], repo: Path) -> list[str]:
    """Problems with one dataset line, checked against the course repository at `repo`."""
    try:
        task = _as_task(line)
    except ValidationError as exc:
        return [f"{'.'.join(str(p) for p in err['loc'])}: {err['msg']}" for err in exc.errors()]
    errors: list[str] = []
    try:
        if task.inputs.checkpoint not in checkpoint_names(repo):
            errors.append(
                f"inputs.checkpoint {task.inputs.checkpoint!r} is not defined in "
                f"{CHECKPOINTS_FILE.as_posix()}"
            )
    except (FileNotFoundError, tomllib.TOMLDecodeError) as exc:
        errors.append(f"inputs.checkpoint: cannot read {CHECKPOINTS_FILE.as_posix()} ({exc})")
    errors += _check_hidden(task.outputs.hidden_test_ids, repo)
    errors += _check_mutants(task.outputs.mutant_set, repo)
    errors += _check_primary(task.outputs.primary_measure, task.inputs.feature_id)
    errors += _check_paths(task.outputs.allowed_paths)
    example = task.metadata.get("example_id", task.inputs.feature_id)
    return [f"{example}: {e}" for e in errors]


def check_features_file(lines: list[FeatureTask] | list[dict[str, Any]]) -> list[str]:
    """Problems with the file as a whole: line total, group counts, split sizes, unique ids."""
    tasks: list[FeatureTask] = []
    errors: list[str] = []
    for number, line in enumerate(lines, start=1):
        try:
            tasks.append(_as_task(line))
        except ValidationError as exc:
            errors.append(f"line {number}: does not match the line schema ({exc.error_count()})")
    if len(lines) != TOTAL_LINES:
        errors.append(f"expected {TOTAL_LINES} lines, found {len(lines)}")
    groups = Counter(str(t.metadata.get("group")) for t in tasks)
    for group in sorted(set(groups) | set(GROUP_COUNTS)):
        want, got = GROUP_COUNTS.get(group, 0), groups.get(group, 0)
        if want != got:
            errors.append(f"group {group!r}: expected {want} lines, found {got}")
    splits = Counter(name for t in tasks for name in t.split)
    for name, size in SPLIT_SIZES.items():
        if splits.get(name, 0) != size:
            errors.append(f"split {name!r}: expected {size} lines, found {splits.get(name, 0)}")
    ids = Counter(str(t.metadata.get("example_id")) for t in tasks)
    errors += [f"duplicate example_id {i!r} ({n} lines)" for i, n in sorted(ids.items()) if n > 1]
    return errors
