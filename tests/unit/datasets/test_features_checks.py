"""features_checks: per-line checks against the course repository, and whole-file checks."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest

from shipharness.datasets.features_checks import (
    GROUP_COUNTS,
    SPLIT_SIZES,
    check_features_file,
    check_features_line,
    checkpoint_names,
    collect_tests,
)

from .features_fixtures import make_repo


@pytest.fixture(scope="module")
def repo(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return make_repo(tmp_path_factory.mktemp("course"), real_sources=False)


def f1_line() -> dict[str, Any]:
    return {
        "inputs": {
            "feature_id": "F1",
            "checkpoint": "m1-s1-start",
            "ticket_text": "Fixture canonical ticket for F1.",
            "variant": "canonical",
            "session_budget": [30],
        },
        "outputs": {
            "hidden_test_ids": [
                "tests/hidden/f1/test_f1_fixture.py::test_f1_one",
                "tests/hidden/f1/test_f1_fixture.py::test_f1_two",
            ],
            "allowed_paths": {"build": ["app/api/issues.py"], "test": ["tests/visible/**"]},
            "mutant_set": "features/f1",
            "primary_measure": "r1_new_violations>=1",
        },
        "metadata": {"group": "canonical", "example_id": "F1-canonical", "control": False},
        "split": ["section-1", "smoke"],
    }


def with_change(path: str, value: Any) -> dict[str, Any]:
    line = copy.deepcopy(f1_line())
    target = line
    keys = path.split(".")
    for key in keys[:-1]:
        target = target[key]
    target[keys[-1]] = value
    return line


def test_a_valid_line_passes(repo: Path) -> None:
    assert check_features_line(f1_line(), repo) == []


def test_schema_errors_are_reported_not_raised(repo: Path) -> None:
    line = f1_line()
    del line["outputs"]["primary_measure"]
    errors = check_features_line(line, repo)
    assert errors and "primary_measure" in errors[0]


def test_checkpoint_must_be_defined_in_checkpoints_toml(repo: Path) -> None:
    errors = check_features_line(with_change("inputs.checkpoint", "m1-s9-start"), repo)
    assert any("m1-s9-start" in e and "checkpoints.toml" in e for e in errors)


def test_checkpoint_names_reads_the_checkpoints_table(repo: Path) -> None:
    assert {"m1-s1-start", "m1-alt-a", "m1-alt-b", "m1-complete"} <= checkpoint_names(repo)


def test_checkpoint_names_uses_the_checkpoints_module(tmp_path: Path) -> None:
    path = tmp_path / "teamtrack" / "reference" / "checkpoints.toml"
    path.parent.mkdir(parents=True)
    path.write_text('[checkpoints."m1-s1-start"]\ntasks = []\n', encoding="utf-8")
    assert checkpoint_names(tmp_path) == {"m1-s1-start"}


def test_missing_checkpoints_toml_is_an_error(tmp_path: Path) -> None:
    errors = check_features_line(f1_line(), tmp_path)
    assert any("checkpoints.toml" in e for e in errors)


def test_hidden_ids_must_exist_in_their_files(repo: Path) -> None:
    ids = ["tests/hidden/f1/test_f1_fixture.py::test_missing"]
    errors = check_features_line(with_change("outputs.hidden_test_ids", ids), repo)
    assert any("test_missing" in e for e in errors)


def test_hidden_file_must_exist(repo: Path) -> None:
    ids = ["tests/hidden/f1/test_nowhere.py::test_f1_one"]
    errors = check_features_line(with_change("outputs.hidden_test_ids", ids), repo)
    assert any("test_nowhere.py" in e for e in errors)


def test_hidden_ids_are_relative_to_the_teamtrack_root(repo: Path) -> None:
    ids = ["teamtrack/tests/hidden/f1/test_f1_fixture.py::test_f1_one"]
    errors = check_features_line(with_change("outputs.hidden_test_ids", ids), repo)
    assert any("tests/hidden/" in e for e in errors)


def test_feature_lines_need_hidden_ids(repo: Path) -> None:
    errors = check_features_line(with_change("outputs.hidden_test_ids", []), repo)
    assert any("hidden" in e for e in errors)


def test_parametrized_hidden_tests_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "test_p.py"
    path.write_text(
        "import pytest\n\n\n@pytest.mark.parametrize('x', [1, 2])\ndef test_p(x):\n    pass\n\n\n"
        "def test_plain():\n    pass\n\n\nclass TestGroup:\n    def test_inner(self):\n"
        "        pass\n",
        encoding="utf-8",
    )
    expected = {"test_p": True, "test_plain": False, "TestGroup::test_inner": False}
    assert collect_tests(path) == expected


def test_mutant_set_must_resolve_to_referee_mutants(repo: Path) -> None:
    errors = check_features_line(with_change("outputs.mutant_set", "features/nope"), repo)
    assert any("features/nope" in e for e in errors)


def test_mutant_set_without_referee_mutants_is_an_error(repo: Path) -> None:
    filter_only = repo / "teamtrack" / "mutants" / "features" / "filteronly.jsonl"
    filter_only.write_text(
        '{"id": "features.filteronly-m1", "target": "features.filteronly", "set": "filter", '
        '"file": "app/x.py", "line": 1, "original": "a", "replacement": "b", "rationale": "r"}\n',
        encoding="utf-8",
    )
    errors = check_features_line(with_change("outputs.mutant_set", "features/filteronly"), repo)
    assert any("no referee mutants" in e for e in errors)


@pytest.mark.parametrize(
    "measure",
    ["r1_new_violation>=1", "r1_new_violations=>1", "nonsense", "hidden_passed,unknown_field"],
)
def test_primary_measure_must_parse_against_score_record(repo: Path, measure: str) -> None:
    errors = check_features_line(with_change("outputs.primary_measure", measure), repo)
    assert any("primary_measure" in e for e in errors)


def test_primary_measure_follows_the_registered_measure_for_the_feature(repo: Path) -> None:
    errors = check_features_line(with_change("outputs.primary_measure", "continuity_failure"), repo)
    assert any("R-5" in e for e in errors)


def test_bare_primary_field_must_be_boolean(repo: Path) -> None:
    line = with_change("outputs.primary_measure", "hidden_passed")
    assert any("boolean" in e for e in check_features_line(line, repo))


@pytest.mark.parametrize(
    "paths",
    [
        {"build": [], "test": ["tests/visible/**"]},
        {"build": ["app/api/issues.py"]},
        {"build": ["/app/api/issues.py"], "test": ["tests/visible/**"]},
        {"build": ["../app.py"], "test": ["tests/visible/**"]},
        {"build": ["app\\api.py"], "test": ["tests/visible/**"]},
        {"build": [""], "test": ["tests/visible/**"]},
    ],
)
def test_allowed_paths_are_non_empty_relative_globs(repo: Path, paths: dict[str, Any]) -> None:
    errors = check_features_line(with_change("outputs.allowed_paths", paths), repo)
    assert any("allowed_paths" in e for e in errors)


def line_for(group: str, n: int, splits: list[str]) -> dict[str, Any]:
    line = f1_line()
    line["metadata"] = {"group": group, "example_id": f"{group}-{n}", "control": False}
    line["split"] = splits
    return line


def full_file() -> list[dict[str, Any]]:
    lines: list[dict[str, Any]] = []
    for group, count in GROUP_COUNTS.items():
        lines += [line_for(group, n, ["extended"]) for n in range(count)]
    slots = [name for name, size in SPLIT_SIZES.items() for _ in range(size)]
    for line, name in zip(lines, slots, strict=False):
        line["split"] = [name]
    return lines


def test_file_check_accepts_the_registered_shape() -> None:
    assert sum(GROUP_COUNTS.values()) == 60
    assert check_features_file(full_file()) == []


def test_file_check_reports_group_counts() -> None:
    lines = full_file()
    lines[0]["metadata"]["group"] = "reworded"
    errors = check_features_file(lines)
    assert any("canonical" in e for e in errors) and any("reworded" in e for e in errors)


def test_file_check_reports_split_sizes() -> None:
    lines = full_file()
    lines[0]["split"] = ["section-1"]
    assert any("smoke" in e for e in check_features_file(lines))


def test_file_check_reports_duplicate_example_ids() -> None:
    lines = full_file()
    lines[1]["metadata"]["example_id"] = lines[0]["metadata"]["example_id"]
    assert any("duplicate" in e for e in check_features_file(lines))


def test_file_check_reports_the_total() -> None:
    assert any("60" in e for e in check_features_file(full_file()[:-1]))
