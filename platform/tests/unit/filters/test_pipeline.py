from __future__ import annotations

from pathlib import Path

import pytest

from shipharness.events import EventBus, read_events
from shipharness.filters.models import CandidateTest, CoverageMap, FilterContext, FilterResult
from shipharness.filters.mutants import Mutant
from shipharness.filters.pipeline import (
    FilterSetupError,
    build_context,
    collect_candidates,
    discarded,
    kept_tests,
    run_pipeline,
)
from shipharness.sandbox import ExecResult, FakeSandbox

from .helpers import PY, local_sandbox, make_repo

NEW_TESTS = """\
from calc import add, clamp


def test_clamp_high():
    assert clamp(5, 0, 3) == 3


def test_vacuous():
    clamp(-1, 0, 3)
    assert True


def test_wrong():
    assert add(1, 1) == 3
"""


def test_collect_candidates_finds_functions_and_methods(tmp_path: Path) -> None:
    (tmp_path / "tests").mkdir()
    source = (
        "def helper():\n    return 1\n\n\ndef test_a():\n    assert helper() == 1\n\n\n"
        "class TestB:\n    def test_c(self):\n        assert 1 + helper() == 2\n\n"
        "    def other(self):\n        pass\n\n\nasync def test_d():\n    assert helper()\n"
    )
    (tmp_path / "tests" / "test_x.py").write_text(source, encoding="utf-8")
    (tmp_path / "tests" / "test_broken.py").write_text("def test_(:\n", encoding="utf-8")
    cands = collect_candidates(tmp_path, ["tests/test_x.py", "tests/test_broken.py"])
    assert [c.test_id for c in cands] == [
        "tests/test_x.py::test_a",
        "tests/test_x.py::TestB::test_c",
        "tests/test_x.py::test_d",
        "tests/test_broken.py",
    ]
    assert cands[0].source == source


def test_collect_candidates_ignores_paths_outside_the_workspace(tmp_path: Path) -> None:
    assert collect_candidates(tmp_path, ["../x/test_a.py", "tests/missing.py"]) == []


def test_pipeline_keeps_good_tests_and_gives_every_discard_a_reason(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    sandbox = local_sandbox(repo)
    ctx = build_context(
        repo, sandbox, existing_tests=["tests/test_calc.py"], target_module="calc", python=PY
    )
    (repo / "tests" / "test_new.py").write_text(NEW_TESTS, encoding="utf-8")
    cands = collect_candidates(repo, ["tests/test_new.py"])
    log = tmp_path / "events.jsonl"
    with EventBus(log, ab_id=None) as bus:
        results = run_pipeline(cands, ctx, bus, run_id="r-1", arm="harness")
    assert kept_tests(results) == ["tests/test_new.py::test_clamp_high"]
    rejected = discarded(results)
    assert set(rejected) == {"tests/test_new.py::test_vacuous", "tests/test_new.py::test_wrong"}
    assert rejected["tests/test_new.py::test_vacuous"].filter == 4
    assert rejected["tests/test_new.py::test_wrong"].filter == 2
    assert all(r.reason for r in results)

    events = list(read_events(log))
    proposed = [e for e in events if e.type == "test_proposed"]
    assert [e.data for e in proposed] == [{"test_id": c.test_id, "phase": "test"} for c in cands]
    filtered = [e for e in events if e.type == "test_filter_result"]
    # 5 filters for the kept test, 4 for the vacuous one, 2 for the failing one.
    assert len(filtered) == 11
    assert all(e.run_id == "r-1" and e.arm == "harness" for e in filtered)
    assert filtered[-1].data == rejected["tests/test_new.py::test_wrong"].model_dump()


class Boom:
    number = 1
    name = "boom"

    def evaluate(self, cand: CandidateTest, ctx: FilterContext) -> FilterResult:
        raise RuntimeError("disk full")


def test_pipeline_turns_filter_errors_into_discards(tmp_path: Path) -> None:
    ctx = FilterContext(
        workspace=tmp_path,
        sandbox=FakeSandbox(),
        baseline_coverage=CoverageMap(),
        filter_mutants=[],
        source_shas_at_phase_start={},
    )
    cand = CandidateTest(test_id="tests/test_a.py::test_a", file="tests/test_a.py", source="")
    results = run_pipeline([cand], ctx, None, filters=[Boom()])
    assert results == [
        FilterResult(
            test_id=cand.test_id,
            filter=1,
            passed=False,
            reason="filter error: RuntimeError: disk full",
        )
    ]
    assert kept_tests(results) == []


def test_build_context_records_baseline_and_surviving_mutants(tmp_path: Path) -> None:
    repo = make_repo(tmp_path / "repo")
    killed = Mutant(
        id="calc-m1",
        target="calc",
        set="filter",
        file="calc.py",
        line=2,
        original="    return a + b",
        replacement="    return a - b",
        rationale="wrong operator",
    )
    survivor = killed.model_copy(
        update={
            "id": "calc-m2",
            "line": 14,
            "original": "    if x < low:",
            "replacement": "    if x <= low:",
        }
    )
    referee = survivor.model_copy(update={"id": "calc-m3", "set": "referee"})
    ctx = build_context(
        repo,
        local_sandbox(repo),
        existing_tests=["tests/test_calc.py"],
        mutants=[killed, survivor, referee],
        target_module="calc",
        python=PY,
    )
    assert [m.id for m in ctx.filter_mutants] == ["calc-m1", "calc-m2"]  # referee set dropped
    assert ctx.surviving_mutant_ids == frozenset({"calc-m2"})
    assert 2 in ctx.baseline_coverage.lines("calc.py")
    assert set(ctx.source_shas_at_phase_start) == {"calc.py", "pytest.ini"}


def test_build_context_fails_when_the_existing_suite_cannot_run(tmp_path: Path) -> None:
    sandbox = FakeSandbox(default=ExecResult(exit_code=4, output="no such file", duration_ms=1))
    with pytest.raises(FilterSetupError, match="baseline coverage"):
        build_context(tmp_path, sandbox, existing_tests=["tests"])
