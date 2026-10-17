"""testgen-targets-v1: the generator is deterministic and its committed output passes the checks."""

from __future__ import annotations

import copy
import tomllib
from collections import Counter
from typing import Any

import pytest

from shipharness.datasets import validate_file
from shipharness.datasets.testgen_checks import check_testgen_file, check_testgen_line

from .testgen_support import DATASET, REPO, SOURCES, committed_lines, load_script


@pytest.fixture(scope="module")
def build() -> Any:
    return load_script("build_testgen_dataset")


def test_generator_is_deterministic_and_matches_the_committed_file(build: Any) -> None:
    first = build.render(build.build_lines(REPO))
    second = build.render(build.build_lines(REPO))
    assert first == second
    assert DATASET.read_text(encoding="utf-8") == first, (
        "datasets/testgen-targets-v1.jsonl is stale: run "
        "uv run python scripts/build_testgen_dataset.py"
    )


def test_generator_check_mode_reports_a_stale_file(build: Any, tmp_path) -> None:  # type: ignore[no-untyped-def]
    out = tmp_path / "targets.jsonl"
    assert build.main(["--out", str(out), "--check"]) == 1
    assert build.main(["--out", str(out)]) == 0
    assert build.main(["--out", str(out), "--check"]) == 0


def test_committed_file_validates_against_the_line_model() -> None:
    assert validate_file(DATASET, "testgen") == []


def test_committed_file_passes_the_file_and_line_checks() -> None:
    lines = committed_lines()
    assert check_testgen_file(lines) == []
    problems = [p for line in lines for p in check_testgen_line(line, REPO)]
    assert problems == []


def test_forty_targets_twenty_teamtrack_ten_per_library() -> None:
    lines = committed_lines()
    assert Counter(line["inputs"]["repo"] for line in lines) == {
        "teamtrack": 20,
        "boltons": 10,
        "wtforms": 10,
    }
    assert all(line["split"] == ["testgen"] for line in lines)


def test_metadata_records_license_commit_and_owner_decisions() -> None:
    sources = tomllib.loads(SOURCES.read_text(encoding="utf-8"))
    for line in committed_lines():
        repo = line["inputs"]["repo"]
        meta = line["metadata"]
        assert meta["license"] == sources["repos"][repo]["license"]
        assert meta["commit"] == sources["repos"][repo]["commit"]
        assert meta["example_id"] == line["inputs"]["target_id"]
        if repo == "boltons":
            assert meta["baseline_includes_doctests"] is True  # G-19
            assert line["outputs"]["known_failures"] == [
                "tests/test_jsonutils.py::test_reverse_iter_lines"
            ]
        if repo == "wtforms":
            assert meta["pytest_config"] == "upstream"  # G-20
            assert meta["warnings_are_errors"] is True
            assert line["outputs"]["known_failures"] == ["tests/fields/test_date.py::test_basic"]
        if repo == "teamtrack":
            assert line["inputs"]["pin"] == "m1-base"
            assert line["outputs"]["filter_mutants"].startswith("teamtrack/mutants/")
            assert line["outputs"]["known_failures"] == []


def test_pins_match_the_research_record() -> None:
    by_repo = {line["inputs"]["repo"]: line for line in committed_lines()}
    assert by_repo["boltons"]["inputs"]["pin"] == "26.2.0"
    assert by_repo["boltons"]["metadata"]["commit"] == "4332b35a278d694f30c99881faa61cde695c7a96"
    assert by_repo["wtforms"]["inputs"]["pin"] == "3.2.2"
    assert by_repo["wtforms"]["metadata"]["commit"] == "ea57c11591556333b4f0ac494d1e5d3f250ab305"


def _line(repo: str = "boltons") -> dict[str, Any]:
    return copy.deepcopy(next(x for x in committed_lines() if x["inputs"]["repo"] == repo))


def test_line_check_rejects_a_mutant_ref_that_does_not_resolve() -> None:
    line = _line()
    line["outputs"]["filter_mutants"] = "datasets/mutants/boltons/nope.jsonl#filter"
    assert any("filter_mutants" in p for p in check_testgen_line(line, REPO))


def test_line_check_rejects_refs_without_their_set() -> None:
    line = _line()
    line["outputs"]["referee_mutants"] = line["outputs"]["filter_mutants"]
    assert any("#referee" in p for p in check_testgen_line(line, REPO))


def test_line_check_rejects_mutants_for_another_module() -> None:
    line = _line()
    line["inputs"]["module"] = "boltons/listutils.py"
    assert any("module" in p for p in check_testgen_line(line, REPO))


def test_line_check_rejects_missing_existing_tests_and_metadata() -> None:
    line = _line("teamtrack")
    line["inputs"]["existing_tests"] = ["tests/visible/test_missing.py"]
    del line["metadata"]["commit"]
    problems = check_testgen_line(line, REPO)
    assert any("test_missing.py" in p for p in problems)
    assert any("commit" in p for p in problems)
    line["inputs"]["existing_tests"] = []
    assert any("existing_tests" in p for p in check_testgen_line(line, REPO))


def test_line_check_rejects_a_library_line_without_its_owner_decision() -> None:
    boltons, wtforms = _line("boltons"), _line("wtforms")
    boltons["metadata"]["baseline_includes_doctests"] = False
    wtforms["metadata"].pop("warnings_are_errors")
    assert any("baseline_includes_doctests" in p for p in check_testgen_line(boltons, REPO))
    assert any("warnings_are_errors" in p for p in check_testgen_line(wtforms, REPO))


def test_line_check_rejects_an_invalid_line_shape() -> None:
    line = _line()
    del line["outputs"]
    assert check_testgen_line(line, REPO)
    line = _line()
    line["split"] = ["smoke"]
    assert any("split" in p for p in check_testgen_line(line, REPO))


def test_file_check_counts_groups_and_unique_ids() -> None:
    lines = committed_lines()
    assert any("40" in p for p in check_testgen_file(lines[:-1]))
    duplicated = lines[:-1] + [copy.deepcopy(lines[0])]
    problems = check_testgen_file(duplicated)
    assert any("duplicate" in p for p in problems)
    assert any("wtforms" in p for p in problems)
