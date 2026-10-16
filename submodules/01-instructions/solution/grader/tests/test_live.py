"""Tests for the A1 live-run evidence (assignment/live_evidence.py) on SYNTHETIC fixtures.

The evidence used here is invented by synthetic_live.py (batch `a1-synthetic`); it is never a real
run. No keys, no Docker, no model calls.

Run: uv run python -m pytest -q -p no:cacheprovider submodules/01-instructions/solution/grader/tests
"""

from __future__ import annotations

import json
import shutil
from collections.abc import Callable
from pathlib import Path

import pytest
import synthetic_live as syn
from helpers import A1, SOLUTION_WORK, load

live = load("a1_live", A1 / "assignment" / "live_evidence.py")
summary_tool = load("a1_ab_summary", A1 / "assignment" / "ab_summary.py")

TASKS = sorted(live.section_tasks())
NAMES = ["live-files", "live-command", "live-caps", "live-tree", "live-report"]


def scores(work: Path, **kwargs: object) -> dict[str, tuple[float, str]]:
    return {name: (score, detail) for name, score, detail in live.check_live(work, **kwargs)}


def fresh_work(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    shutil.copytree(SOLUTION_WORK, work, ignore=shutil.ignore_patterns("__pycache__", "live"))
    return work


@pytest.fixture
def work(tmp_path: Path) -> Path:
    """The reference work folder with SYNTHETIC live evidence and a report that matches it."""
    work = fresh_work(tmp_path)
    placed = live.tree_files(work / "instructions")
    summary = syn.write_live(work, TASKS, placed, r1_fail={"bare": 5}, r3_fail={"harness": 2})
    text = syn.report(summary, r1=("5/24", "0/24"), r3=("0/24", "2/24"), runs=24)
    (work / "ab-report.md").write_text(text, encoding="utf-8")
    return work


def edit_json(path: Path, change: Callable[[dict], None]) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    change(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def first(work: Path, folder: str, arm: str) -> Path:
    prefix = "r-20261016-120000-b0" if arm == "bare" else "r-20261016-120000-c0"
    if folder == "runs":
        return next((work / "live" / "runs").glob(f"{prefix}*")) / "events.jsonl"
    return next((work / "live" / folder).glob(f"{prefix}*.json"))


def export(work: Path, arm: str) -> Path:
    return next((work / "live" / "experiments").glob(f"*-{arm}-*.json"))


def replace_in(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, old
    path.write_text(text.replace(old, new), encoding="utf-8")


# -- the whole check ------------------------------------------------------------------------------


def test_the_section_1_subset_has_eight_tasks() -> None:
    assert len(TASKS) == 8
    assert ("F1", "trap-legacy-pattern", "m1-s1-start") in TASKS


def test_synthetic_evidence_that_matches_the_tree_and_report_passes(work: Path) -> None:
    result = scores(work)
    assert list(result) == NAMES
    assert {n: d for n, (s, d) in result.items() if s < 1} == {}


def test_without_a_live_folder_every_live_item_fails_and_says_what_to_add(tmp_path: Path) -> None:
    result = scores(fresh_work(tmp_path))
    assert all(score == 0 for score, _ in result.values())
    assert "live/" in result["live-files"][1]
    assert "live_evidence.py" in result["live-files"][1]


# -- live-files: missing or malformed evidence fails the whole criterion ---------------------------


def _extra_field(work: Path) -> None:
    edit_json(first(work, "scores", "bare"), lambda d: d.update(model="gpt-6-luna"))


def _missing_field(work: Path) -> None:
    edit_json(first(work, "scores", "harness"), lambda d: d.pop("checkpoint_sha"))


def _not_json(work: Path) -> None:
    first(work, "scores", "bare").write_text("{not json", encoding="utf-8")


def _missing_score(work: Path) -> None:
    first(work, "scores", "harness").unlink()


def _one_arm_only(work: Path) -> None:
    export(work, "bare").unlink()


def _no_cost_line(work: Path) -> None:
    out = work / "live" / "output.txt"
    kept = [ln for ln in out.read_text(encoding="utf-8").splitlines() if not ln.startswith("Cost:")]
    out.write_text("\n".join(kept) + "\n", encoding="utf-8")


def _no_command_line(work: Path) -> None:
    out = work / "live" / "output.txt"
    out.write_text(out.read_text(encoding="utf-8").split("\n", 1)[1], encoding="utf-8")


def _missing_run_log(work: Path) -> None:
    first(work, "runs", "harness").unlink()


def _bad_event(work: Path) -> None:
    log = first(work, "runs", "harness")
    log.write_text(log.read_text(encoding="utf-8") + '{"type": "made_up"}\n', encoding="utf-8")


@pytest.mark.parametrize(
    "breaks",
    [
        _extra_field,
        _missing_field,
        _not_json,
        _missing_score,
        _one_arm_only,
        _no_cost_line,
        _no_command_line,
        _missing_run_log,
        _bad_event,
    ],
    ids=lambda f: f.__name__.strip("_"),
)
def test_missing_or_malformed_evidence_fails_every_live_item(
    work: Path, breaks: Callable[[Path], None]
) -> None:
    breaks(work)
    result = scores(work)
    assert result["live-files"][0] == 0
    assert all(score == 0 for score, _ in result.values())
    assert result["live-files"][1]


# -- live-command: run ids, batch, split, k, layers consistent with the command --------------------


@pytest.mark.parametrize(
    ("change", "needle"),
    [
        (lambda w: replace_in(w / "live" / "output.txt", "--k 3", "--k 2"), "--k 3"),
        (
            lambda w: replace_in(
                w / "live" / "output.txt", "--layers instructions", "--layers all"
            ),
            "--layers instructions",
        ),
        (
            lambda w: replace_in(
                w / "live" / "output.txt", "--batch a1-synthetic", "--batch a1-other"
            ),
            "batch",
        ),
        (
            lambda w: replace_in(
                w / "live" / "output.txt",
                "instructions --batch",
                "instructions --from-working-tree --batch",
            ),
            "--from-working-tree",
        ),
        (lambda w: edit_json(export(w, "harness"), lambda d: d.update(split="smoke")), "split"),
        (
            lambda w: edit_json(
                first(w, "scores", "bare"), lambda d: d.update(checkpoint_sha=None)
            ),
            "checkpoint_sha",
        ),
        (
            lambda w: edit_json(first(w, "scores", "bare"), lambda d: d.update(feature_id="F5")),
            "section-1",
        ),
        (
            lambda w: edit_json(first(w, "scores", "harness"), lambda d: d.update(layers=[])),
            "layers",
        ),
        (
            lambda w: edit_json(first(w, "scores", "bare"), lambda d: d.update(arm="harness")),
            "arm",
        ),
        (
            lambda w: replace_in(
                w / "live" / "output.txt", "-bare-2026-10-16-synthetic", "-bare-x"
            ),
            "output",
        ),
    ],
    ids=[
        "k",
        "layers",
        "batch",
        "working-tree",
        "split",
        "checkpoint-sha",
        "task",
        "record-layers",
        "record-arm",
        "export-name",
    ],
)
def test_evidence_inconsistent_with_the_command_loses_command_points(
    work: Path, change: Callable[[Path], None], needle: str
) -> None:
    change(work)
    result = scores(work)
    assert result["live-files"][0] == 1, result["live-files"][1]
    assert result["live-command"][0] < 1
    assert needle in result["live-command"][1]


def test_each_part_of_a_check_costs_one_share_at_most(work: Path) -> None:
    """Command flags are one of four live-command parts; command cap and cost line one of five
    live-caps parts, as the grading criteria say."""
    out = work / "live" / "output.txt"
    replace_in(
        out, "--k 3 --layers instructions", "--k 2 --layers instructions --from-working-tree"
    )
    replace_in(out, "this command: gpt-6-luna $1.440000", "this command: other $3.100000")
    replace_in(out, "Cost: $1.440000", "Cost: $3.100000")
    result = scores(work)
    assert result["live-command"][0] == pytest.approx(3 / 4)
    assert result["live-caps"][0] == pytest.approx(4 / 5)


def test_a_run_missing_from_both_arms_is_named(work: Path) -> None:
    for arm in ("bare", "harness"):
        rid = first(work, "scores", arm).stem
        first(work, "scores", arm).unlink()
        if arm == "harness":
            shutil.rmtree(work / "live" / "runs" / rid)
        edit_json(export(work, arm), lambda d, rid=rid: d["rows"].remove(rid))
    result = scores(work)
    assert result["live-files"][0] == 1, result["live-files"][1]
    assert result["live-command"][0] < 1
    assert "23 runs" in result["live-command"][1]


# -- live-caps: model, recorded, sandbox, cost caps ------------------------------------------------


@pytest.mark.parametrize(
    ("change", "needle"),
    [
        (
            lambda w: edit_json(
                export(w, "bare"), lambda d: d["metadata"].update(model="gpt-5.6-luna")
            ),
            "gpt-6-luna",
        ),
        (lambda w: replace_in(first(w, "runs", "harness"), '"gpt-6-luna"', '"gpt-4o"'), "model"),
        (
            lambda w: edit_json(first(w, "scores", "bare"), lambda d: d.update(recorded=True)),
            "recorded",
        ),
        (
            lambda w: edit_json(first(w, "scores", "bare"), lambda d: d.update(sandboxed=False)),
            "sandbox",
        ),
        (
            lambda w: edit_json(first(w, "scores", "harness"), lambda d: d.update(cost_usd=0.25)),
            "0.20",
        ),
        (
            lambda w: replace_in(w / "live" / "output.txt", "Cost: $1.440000", "Cost: $3.100000"),
            "2.50",
        ),
        (
            lambda w: replace_in(
                w / "live" / "output.txt", "this command: gpt-6-luna", "this command: no calls"
            ),
            "cost line",
        ),
    ],
    ids=[
        "export-model",
        "run-model",
        "recorded",
        "sandboxed",
        "run-cap",
        "command-cap",
        "cost-line-model",
    ],
)
def test_runs_outside_the_class_model_or_caps_lose_cap_points(
    work: Path, change: Callable[[Path], None], needle: str
) -> None:
    change(work)
    result = scores(work)
    assert result["live-files"][0] == 1, result["live-files"][1]
    assert result["live-caps"][0] < 1
    assert needle in result["live-caps"][1]


# -- live-tree: the harness arm placed the learner's tree -----------------------------------------


def test_a_run_that_placed_another_tree_fails_the_tree_check(work: Path) -> None:
    course_tree = live.tree_files(live.REPO / "teamtrack" / "harness" / "instructions")
    for log in (work / "live" / "runs").glob("*/events.jsonl"):
        lines = [json.loads(ln) for ln in log.read_text(encoding="utf-8").splitlines()]
        for event in lines:
            if event["type"] == "harness_decision":
                event["data"]["paths"] = course_tree
        log.write_text("\n".join(json.dumps(e) for e in lines) + "\n", encoding="utf-8")
    result = scores(work)
    assert result["live-tree"][0] == 0
    assert "add-list-endpoint" in result["live-tree"][1]


def test_a_file_added_to_the_tree_after_the_run_is_named(work: Path) -> None:
    (work / "instructions" / "docs" / "LATER.md").write_text("# later\n", encoding="utf-8")
    result = scores(work)
    assert result["live-tree"][0] == 0
    assert "docs/LATER.md" in result["live-tree"][1]


def test_a_harness_run_without_the_placement_note_fails_the_tree_check(work: Path) -> None:
    log = first(work, "runs", "harness")
    kept = [
        ln for ln in log.read_text(encoding="utf-8").splitlines() if "harness_decision" not in ln
    ]
    log.write_text("\n".join(kept) + "\n", encoding="utf-8")
    result = scores(work)
    assert result["live-tree"][0] == 0
    assert log.parent.name in result["live-tree"][1]


# -- live-report: the report's values come from the evidence --------------------------------------


@pytest.mark.parametrize(
    ("old", "new", "needle"),
    [
        ("| 5/24 | 0/24 |", "| 4/24 | 0/24 |", "R1"),
        ("| 0/24 | 2/24 |", "| 0/24 | 1/24 |", "R3"),
        ("Runs per arm: 24", "Runs per arm: 12", "Runs per arm"),
        ("selectedSessions=bare", "selectedSessions=other", "link"),
        ("--batch a1-synthetic`", "--batch a1-synth`", "command"),
    ],
    ids=["r1", "r3", "runs", "links", "command"],
)
def test_report_values_that_differ_from_the_evidence_lose_report_points(
    work: Path, old: str, new: str, needle: str
) -> None:
    replace_in(work / "ab-report.md", old, new)
    result = scores(work)
    assert result["live-report"][0] < 1
    assert needle in result["live-report"][1]


# -- the reference solution: pending until the integrator captures the real run -------------------


def test_a_pending_marker_stands_in_for_the_evidence_only_when_allowed(tmp_path: Path) -> None:
    work = fresh_work(tmp_path)
    shutil.copytree(SOLUTION_WORK / "live", work / "live")
    assert all(score == 1 for score, _ in scores(work, allow_pending=True).values())
    result = scores(work)
    assert all(score == 0 for score, _ in result.values())
    assert "pending" in result["live-files"][1]


def test_the_reference_live_folder_holds_the_pending_marker_and_the_command() -> None:
    text = (SOLUTION_WORK / "live" / "README.md").read_text(encoding="utf-8")
    assert live.PENDING.search(text)
    assert "source: M8 batch 1" in text
    assert syn.COMMAND.replace(syn.BATCH, "a1-reference") in text


# -- collecting the evidence ----------------------------------------------------------------------


def test_collect_copies_the_batch_into_live_and_checks_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    work = fresh_work(tmp_path)
    (work / "ab-report.md").unlink()  # the report is written after collecting
    exports = tmp_path / "exports"
    placed = live.tree_files(work / "instructions")
    summary = syn.exports_layout(exports, TASKS, placed)
    other = exports / "experiments" / "shipharness-batch-1-bare-2026-10-01-x.json"
    other.write_text(json.dumps({"name": "x", "arm": "bare", "metadata": {"batch": "b"}}))
    out = tmp_path / "a1-live-output.txt"
    out.write_text(syn.output_text(summary), encoding="utf-8")
    argv = ["--batch", syn.BATCH, "--output", str(out), "--work", str(work)]
    argv += ["--exports", str(exports), "--runs", str(exports / "runs")]
    assert live.main(argv) == 0
    stdout = capsys.readouterr().out
    assert "PASS live-files" in stdout
    assert "FAIL live-report" in stdout  # no report yet: the only open item
    copied = work / "live"
    assert len(list((copied / "experiments").glob("*.json"))) == 2
    assert len(list((copied / "scores").glob("*.json"))) == 48
    assert len(list((copied / "runs").glob("*/events.jsonl"))) == 24
    assert (copied / "output.txt").read_text(encoding="utf-8") == out.read_text(encoding="utf-8")
    assert summary_tool.main(["--batch", syn.BATCH, "--exports", str(copied)]) == 0


def test_collect_with_an_unknown_batch_exits_2(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out = tmp_path / "out.txt"
    out.write_text("$ x\n", encoding="utf-8")
    argv = ["--batch", "a1-nobody", "--output", str(out), "--work", str(fresh_work(tmp_path))]
    argv += ["--exports", str(tmp_path / "exports"), "--runs", str(tmp_path / "runs")]
    assert live.main(argv) == 2
    assert "a1-nobody" in capsys.readouterr().out
