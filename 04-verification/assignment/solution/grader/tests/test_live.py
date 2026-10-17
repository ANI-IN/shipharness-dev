"""Tests for the live-evidence checks (`assignment/visible_tests/a4_live.py`).

All evidence here is the SYNTHETIC fixture from `live_fixture.py`: made-up values, never a real
run. Each test breaks one thing and checks that the matching problem is reported.
"""

from __future__ import annotations

import inspect
import json
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

TESTS = Path(__file__).resolve().parent
GRADER = TESTS.parent
SOLUTION = GRADER.parent
ASSIGNMENT = SOLUTION.parent  # solution/ sits inside assignment/
VISIBLE = ASSIGNMENT / "visible_tests"
REPO = ASSIGNMENT.parents[1]
sys.path[:0] = [str(TESTS), str(VISIBLE)]

import a4_live  # noqa: E402
import a4_support  # noqa: E402
import live_fixture as fx  # noqa: E402
from a4_runner import run_tests  # noqa: E402

SHA = fx.checkpoint_sha(REPO)


@pytest.fixture
def root(tmp_path: Path) -> Path:
    return fx.write_live(tmp_path / "impl", SHA)


def _all_problems(root: Path, sha: str | None = SHA) -> list[str]:
    return [
        *a4_live.testgen_run_problems(root),
        *a4_live.filter6_problems(root),
        *a4_live.ab_run_problems(root),
        *a4_live.score_record_problems(root, sha),
    ]


def _edit_text(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, f"fixture changed: {old!r} not in {path.name}"
    path.write_text(text.replace(old, new), encoding="utf-8")


def _edit_json(path: Path, change: Callable[[dict[str, Any]], None]) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    change(data)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _record(root: Path, arm: str) -> Path:
    return root / "live" / "scores" / f"{fx.RUN_IDS[arm]}.json"


def _has(problems: list[str], *needles: str) -> bool:
    return any(all(n in p for n in needles) for p in problems)


# --- the synthetic fixture passes ----------------------------------------------------------------


def test_synthetic_fixture_passes_every_check(root: Path) -> None:
    assert _all_problems(root) == []


def test_missing_live_folder_fails_every_check(tmp_path: Path) -> None:
    assert _has(a4_live.testgen_run_problems(tmp_path), "live/testgen.txt", "missing")
    assert _has(a4_live.filter6_problems(tmp_path), "live/testgen-report.json", "missing")
    assert _has(a4_live.ab_run_problems(tmp_path), "live/ab.txt", "missing")
    assert _has(a4_live.score_record_problems(tmp_path, SHA), "live/scores", "2 score records")


# --- testgen run ---------------------------------------------------------------------------------


def test_testgen_command_must_be_shipharness_testgen_with_out(root: Path) -> None:
    _edit_text(root / "live" / "testgen.txt", " --out .shipharness/a4/testgen", "")
    assert _has(a4_live.testgen_run_problems(root), "--out")


def test_testgen_model_must_be_the_course_model(root: Path) -> None:
    _edit_text(root / "live" / "testgen.txt", "model gpt-6-luna", "model gpt-4o")
    assert _has(a4_live.testgen_run_problems(root), "gpt-6-luna", "gpt-4o")


def test_testgen_cost_must_be_within_the_run_cap(root: Path) -> None:
    _edit_text(root / "live" / "testgen.txt", "Cost: $0.012345", "Cost: $0.250000")
    assert _has(a4_live.testgen_run_problems(root), "0.25", "0.20")


def test_testgen_cost_of_zero_means_no_live_run(root: Path) -> None:
    _edit_text(root / "live" / "testgen.txt", "Cost: $0.012345", "Cost: $0.000000")
    assert _has(a4_live.testgen_run_problems(root), "no model call")


def test_testgen_run_id_must_match_the_report(root: Path) -> None:
    _edit_json(root / "live" / "testgen-report.json", lambda d: d.update(run_id="r-x"))
    assert _has(a4_live.testgen_run_problems(root), "run id")


def test_testgen_kept_count_must_match_the_report(root: Path) -> None:
    _edit_text(root / "live" / "testgen.txt", "kept 2 of 3", "kept 3 of 3")
    assert _has(a4_live.testgen_run_problems(root), "kept 3", "2")


def test_testgen_report_rows_must_be_filter_results(root: Path) -> None:
    def change(d: dict[str, Any]) -> None:
        d["results"][0]["extra"] = 1

    _edit_json(root / "live" / "testgen-report.json", change)
    assert _has(a4_live.testgen_run_problems(root), "results[0]")


def test_testgen_kept_must_follow_from_filters_1_to_5(root: Path) -> None:
    def change(d: dict[str, Any]) -> None:
        d["kept"].append(fx.DROPPED)

    _edit_json(root / "live" / "testgen-report.json", change)
    assert _has(a4_live.testgen_run_problems(root), "filters 1-5")


# --- filter 6 in the report ----------------------------------------------------------------------


def test_report_without_filter_6_rows_fails(root: Path) -> None:
    def change(d: dict[str, Any]) -> None:
        d["results"] = [r for r in d["results"] if r["filter"] != 6]
        del d["filter6"]

    _edit_json(root / "live" / "testgen-report.json", change)
    problems = a4_live.filter6_problems(root)
    assert _has(problems, "--update-report")


def test_every_kept_test_needs_one_filter_6_row(root: Path) -> None:
    def change(d: dict[str, Any]) -> None:
        d["results"] = [r for r in d["results"] if r["test_id"] != fx.KEPT[1] or r["filter"] != 6]

    _edit_json(root / "live" / "testgen-report.json", change)
    assert _has(a4_live.filter6_problems(root), fx.KEPT[1])


def test_filter_6_kept_list_must_match_its_rows(root: Path) -> None:
    _edit_json(
        root / "live" / "testgen-report.json", lambda d: d["filter6"].update(kept=list(fx.KEPT))
    )
    assert _has(a4_live.filter6_problems(root), "filter6.kept")


def test_filter_6_needs_at_least_one_kept_test(root: Path) -> None:
    def change(d: dict[str, Any]) -> None:
        d["kept"] = []
        d["results"] = [r for r in d["results"] if r["filter"] != 6]
        d["filter6"]["kept"] = []

    _edit_json(root / "live" / "testgen-report.json", change)
    assert _has(a4_live.filter6_problems(root), "kept no test")


def test_filter_6_rows_come_after_the_testgen_rows(root: Path) -> None:
    def change(d: dict[str, Any]) -> None:
        d["results"].insert(0, d["results"].pop())

    _edit_json(root / "live" / "testgen-report.json", change)
    assert _has(a4_live.filter6_problems(root), "after")


# --- A/B command and cost ------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("old", "new", "needle"),
    [
        ("--section demo-4", "--section demo-3", "--section demo-4"),
        ("--feature F4", "--feature F1", "--feature F4"),
        (" --no-preview", "", "--no-preview"),
        ("--no-preview", "--no-preview --from-working-tree", "--from-working-tree"),
        ("--no-preview", "--no-preview --k 2", "--k"),
        ("uv run shipharness ab", "uv run shipharness replay", "shipharness ab"),
        (" --purpose assignment", "", "--purpose assignment"),
        ("--purpose assignment", "--purpose class", "--purpose assignment"),
        ("--purpose assignment", "--purpose pilot", "--purpose assignment"),
    ],
)
def test_ab_command_must_be_the_one_in_the_readme(
    root: Path, old: str, new: str, needle: str
) -> None:
    _edit_text(
        root / "live" / "ab.txt", f"$ {fx.AB_COMMAND}", f"$ {fx.AB_COMMAND}".replace(old, new)
    )
    assert _has(a4_live.ab_run_problems(root), needle)


def test_ab_command_of_the_brief_is_accepted(root: Path) -> None:
    text = (root / "live" / "ab.txt").read_text(encoding="utf-8")
    assert "$ uv run shipharness ab --section demo-4 --feature F4 --purpose assignment " in text
    assert a4_live.ab_run_problems(root) == []


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("--no-preview", "--no-preview --k 1"),
        ("--purpose assignment", "--purpose=assignment"),
    ],
)
def test_ab_allowed_spellings(root: Path, old: str, new: str) -> None:
    _edit_text(root / "live" / "ab.txt", old, new)
    assert a4_live.ab_run_problems(root) == []


def test_ab_cost_line_as_shipharness_prints_it_lists_the_models(tmp_path: Path) -> None:
    from shipharness.ab.runtime import cost_line
    from shipharness.config import Prices, Settings
    from shipharness.cost.tracker import Caps, CostScope, CostTracker, Usage

    def default(name: str) -> Any:
        return Settings.model_fields[name].default

    caps = Caps(
        run=default("max_run_cost_usd"),
        review=default("max_review_cost_usd"),
        session=default("max_session_cost_usd"),
        batch=default("max_batch_cost_usd"),
        experiment=default("max_experiment_total_usd"),
    )
    tracker = CostTracker(
        Prices.load(default("prices_file")), caps, tmp_path / "ledger.jsonl", "assignment"
    )
    tracker.record(
        CostScope("run", "r-20000101-000000-00000c", caps.run),
        a4_live.MODEL,
        Usage(input_tokens=10_000, output_tokens=1_000),
    )
    match = a4_live.COST.match(cost_line(tracker))
    assert match, cost_line(tracker)
    assert list(a4_live.ab_cost_models(match.group(2))) == [a4_live.MODEL]


def test_ab_must_print_exactly_one_ab(root: Path) -> None:
    path = root / "live" / "ab.txt"
    line = f"A/B {fx.AB_ID} (F4, layers={fx.HARNESS_LAYERS})"
    _edit_text(path, line, f"{line}\n{line.replace('00000b', '00000e')}")
    assert _has(a4_live.ab_run_problems(root), "one A/B")


def test_ab_cost_must_be_within_the_command_cap(root: Path) -> None:
    _edit_text(root / "live" / "ab.txt", "Cost: $0.120000", "Cost: $2.600000")
    assert _has(a4_live.ab_run_problems(root), "2.60", "2.50")


def test_ab_cost_line_must_list_the_course_model(root: Path) -> None:
    _edit_text(root / "live" / "ab.txt", "gpt-6-luna $0.110000", "gpt-4o $0.110000")
    problems = a4_live.ab_run_problems(root)
    assert _has(problems, "gpt-6-luna")
    assert _has(problems, "gpt-4o")


def test_ab_cost_line_is_required(root: Path) -> None:
    _edit_text(root / "live" / "ab.txt", "Cost: $0.120000", "Spent: $0.120000")
    assert _has(a4_live.ab_run_problems(root), "Cost:")


# --- A/B score records ---------------------------------------------------------------------------


def test_score_records_must_validate_as_score_record(root: Path) -> None:
    _edit_json(_record(root, "bare"), lambda d: d.pop("hidden_total"))
    assert _has(a4_live.score_record_problems(root, SHA), "ScoreRecord", "hidden_total")


def test_score_records_must_not_be_replays(root: Path) -> None:
    _edit_json(_record(root, "harness"), lambda d: d.update(recorded=True))
    assert _has(a4_live.score_record_problems(root, SHA), "recorded")


def test_score_records_must_be_sandboxed(root: Path) -> None:
    _edit_json(_record(root, "harness"), lambda d: d.update(sandboxed=False))
    assert _has(a4_live.score_record_problems(root, SHA), "sandboxed")


def test_checkpoint_sha_must_be_the_checkpoint_commit(root: Path) -> None:
    assert _has(a4_live.score_record_problems(root, "0" * 40), "checkpoint_sha", SHA[:12])


def test_checkpoint_sha_must_be_present(root: Path) -> None:
    _edit_json(_record(root, "bare"), lambda d: d.update(checkpoint_sha=None))
    assert _has(a4_live.score_record_problems(root, SHA), "checkpoint_sha")


def test_arm_cost_must_be_within_the_run_cap(root: Path) -> None:
    _edit_json(_record(root, "bare"), lambda d: d.update(cost_usd=0.21))
    assert _has(a4_live.score_record_problems(root, SHA), "cost_usd", "0.20")


def test_review_cost_must_be_within_the_review_cap(root: Path) -> None:
    _edit_json(_record(root, "bare"), lambda d: d.update(review_cost_usd=0.05))
    assert _has(a4_live.score_record_problems(root, SHA), "review_cost_usd", "0.04")


def test_records_must_belong_to_the_printed_ab(root: Path) -> None:
    _edit_json(_record(root, "bare"), lambda d: d.update(ab_id="ab-20000101-000000-0000ff"))
    assert _has(a4_live.score_record_problems(root, SHA), "ab_id")


def test_record_file_name_must_be_its_run_id(root: Path) -> None:
    path = _record(root, "bare")
    path.rename(path.with_name("r-20000101-000000-0000ee.json"))
    assert _has(a4_live.score_record_problems(root, SHA), "file name")


def test_both_arms_are_required(root: Path) -> None:
    _record(root, "bare").unlink()
    assert _has(a4_live.score_record_problems(root, SHA), "2 score records")


def test_records_must_be_f4_canonical_at_m1_s4_start(root: Path) -> None:
    _edit_json(_record(root, "bare"), lambda d: d.update(feature_id="F1", checkpoint="m1-base"))
    problems = a4_live.score_record_problems(root, SHA)
    assert _has(problems, "feature_id")
    assert _has(problems, "checkpoint")


def test_harness_arm_must_run_the_demo_4_layers(root: Path) -> None:
    _edit_json(_record(root, "harness"), lambda d: d.update(layers=["instructions"]))
    assert _has(a4_live.score_record_problems(root, SHA), "layers")


def test_record_costs_must_fit_in_the_command_cost(root: Path) -> None:
    _edit_json(_record(root, "bare"), lambda d: d.update(cost_usd=0.19))
    assert _has(a4_live.score_record_problems(root, SHA), "more than the command")


def test_record_status_must_match_the_printed_line(root: Path) -> None:
    _edit_json(_record(root, "bare"), lambda d: d.update(status="ABORTED_COST"))
    assert _has(a4_live.score_record_problems(root, SHA), "status")


# --- no placeholder acceptance, and the LangSmith page -------------------------------------------

MARKER = "[[PENDING: captured live run | source: M6 pilot | how: x]]"


def test_a_pending_marker_alone_fails_live_evidence(tmp_path: Path) -> None:
    impl = tmp_path / "impl"
    (impl / "live").mkdir(parents=True)
    (impl / "live" / "README.md").write_text(MARKER + "\n", encoding="utf-8")
    outcomes, output = run_tests(impl, [VISIBLE / "test_live_visible.py"], timeout_s=300)
    live = [o for o in outcomes if o.criterion == "live-evidence"]
    assert len(live) == 4, output[-2000:]
    assert not any(o.passed for o in live), [(o.name, o.message) for o in live]


def test_no_visible_check_can_tell_the_reference_folder_apart() -> None:
    # The reference solution is graded like any submission: no visible test or self-check code
    # names the solution folder, so none can accept a marker there and nowhere else.
    assert not hasattr(a4_live, "pending_only")
    assert not hasattr(a4_support, "reference_mode")
    assert list(inspect.signature(a4_support.doc_problems).parameters) == ["root", "spec"]
    for path in [*VISIBLE.glob("*.py"), ASSIGNMENT / "check.py"]:
        text = path.read_text(encoding="utf-8").lower()
        assert "solution" not in text, f"{path.name} names the solution folder"


def test_reference_solution_passes_live_evidence_on_its_captured_run() -> None:
    assert a4_support.PENDING not in (SOLUTION / "live" / "README.md").read_text(encoding="utf-8")
    assert _all_problems(SOLUTION) == []
    outcomes, output = run_tests(SOLUTION, [VISIBLE / "test_live_visible.py"], timeout_s=300)
    live = [o for o in outcomes if o.criterion == "live-evidence"]
    assert len(live) == 4, output[-2000:]
    assert all(o.passed for o in live), [(o.name, o.message) for o in live]


def test_langsmith_page_must_link_a_trace_of_the_records(root: Path) -> None:
    good = f"## Trace links\n\n- {fx.RUN_IDS['harness']}: https://smith.langchain.com/synthetic-fixture/{fx.RUN_IDS['harness']}\n"
    assert a4_live.trace_link_problems(root, good) == []
    bad = "## Trace links\n\n- https://smith.langchain.com/o/other\n"
    assert _has(a4_live.trace_link_problems(root, bad), "trace_url")


# --- end to end through the visible tests --------------------------------------------------------


def test_visible_live_tests_pass_on_the_synthetic_fixture(tmp_path: Path) -> None:
    impl = fx.write_live(tmp_path / "impl", SHA)
    outcomes, output = run_tests(impl, [VISIBLE / "test_live_visible.py"], timeout_s=300)
    assert [o.name for o in outcomes if not o.criterion] == []  # every collected test is graded
    live = [o for o in outcomes if o.criterion == "live-evidence"]
    assert len(live) == 4, output[-2000:]
    assert all(o.passed for o in live), [(o.name, o.message) for o in live]


def test_visible_live_tests_fail_without_evidence(tmp_path: Path) -> None:
    impl = tmp_path / "impl"
    impl.mkdir()
    outcomes, output = run_tests(impl, [VISIBLE / "test_live_visible.py"], timeout_s=300)
    live = [o for o in outcomes if o.criterion == "live-evidence"]
    assert len(live) == 4, output[-2000:]
    assert not any(o.passed for o in live)
    shutil.rmtree(impl)


def test_the_ab_line_may_name_the_profile(root: Path) -> None:
    # `shipharness ab` prints ", profile=<name>" after the layers since the class profile
    # (2026-10-17); the real A4 capture has it.
    path = root / "live" / "ab.txt"
    line = f"A/B {fx.AB_ID} (F4, layers={fx.HARNESS_LAYERS})"
    _edit_text(path, line, line[:-1] + ", profile=standard)")
    assert not _has(a4_live.ab_run_problems(root), "one A/B")


def test_a_rebuilt_checkpoint_tag_with_the_same_teamtrack_tree_still_matches() -> None:
    # The checkpoint tags were rebuilt (2026-10-17 restructure); the reference run's records name the
    # previous m1-s4-start commit. Same TeamTrack tree -> the same checkpoint.
    repo = Path(__file__).resolve().parents[5]
    current = a4_live.course_checkpoint_sha(repo)
    assert current is not None
    old = "a9d6be25aca5"
    full = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", old], capture_output=True, text=True
    )
    if full.returncode != 0:
        pytest.skip("archived checkpoint commit not in this clone")
    assert a4_live.same_checkpoint(repo, full.stdout.strip(), current)
    other = a4_live.course_checkpoint_sha(repo, "m1-s1-start")
    assert other is not None and not a4_live.same_checkpoint(repo, other, current)
