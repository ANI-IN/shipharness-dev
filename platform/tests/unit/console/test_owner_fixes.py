"""Owner findings from live runs (2026-10-18): a single-arm run says "Not run (harness in
action)" wherever the bare arm would be, the test phase is labelled as such, a finished run says
"finished", screen 4 shows the runs before class next to this run, the run list says what each run
is, and more (one section per fix)."""

from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from shipharness.ab.score import REFEREE_VERSION
from shipharness.console.app import create_console_app, screen_updates
from shipharness.console.report import load_report
from shipharness.console.runs import run_summary
from shipharness.console.screens import ScreenContext, ScreenRenderer
from shipharness.console.state import ConsoleState
from shipharness.events import read_events
from shipharness.tracing import write_export
from tests.unit.ab.score_fixtures import record
from tests.unit.console.run_logs import ab_run, multi_session_run, single_arm_run, write_ab_json

NOT_RUN = "Not run (harness in action)"


def render(log: Path, exports: Path | None = None) -> dict[str, str]:
    exports = exports or log.parent.parent / "no-exports"
    state = ConsoleState.from_events(read_events(log))
    ctx = ScreenContext(log.parent.name, state, load_report(exports), str(exports))
    return ScreenRenderer().render_all(ctx)


def bare_blocks(html: str) -> list[str]:
    """The HTML of every bare-arm block (data-arm="bare") on one screen."""
    return re.findall(r'data-arm="bare">(.*?)</(?:section|article)>', html, flags=re.S)


# -- fix 1: single-arm runs ----------------------------------------------------------------------


@pytest.mark.parametrize("key", ["1", "2", "3", "4", "5"])
def test_every_screen_says_the_bare_arm_did_not_run(tmp_path: Path, key: str) -> None:
    screens = render(single_arm_run(tmp_path / "runs"))
    assert NOT_RUN in screens[key], key


def test_no_bare_block_shows_a_default_result_on_a_single_arm_run(tmp_path: Path) -> None:
    screens = render(single_arm_run(tmp_path / "runs"))
    defaults = [
        "none</span>",  # "Sandbox denials: ✓ none"
        "Nothing read yet",
        "No sessions yet",
        "No changes yet",
        "Referee not run yet",
        "no wrong turn found",
        "No trace link yet",
        "No board screenshot yet",
        "referee pending",
    ]
    for key in ("2", "3", "5"):
        blocks = bare_blocks(screens[key])
        assert blocks, key
        for block in blocks:
            assert NOT_RUN in block, key
            for text in defaults:
                assert text not in block, (key, text)
    # Screen 3 has three panels, each with a bare block: files read and sessions; diff map and
    # sandbox denials; referee.
    assert len(bare_blocks(screens["3"])) == 3
    report = screens["4"]
    assert "BARE</span> " in report and "referee pending" not in report
    assert screens["4"].count(NOT_RUN) == 1


def test_an_ab_run_shows_both_arms_normally(tmp_path: Path) -> None:
    screens = render(ab_run(tmp_path / "runs"))
    for key, html in screens.items():
        assert "Not run" not in html, key
    assert "Sandbox denials" in screens["3"] and "Session 1" in screens["3"]
    assert screens["4"].count("primary verdict ready") == 2


# -- fix 2: the test phase is not "Session 2" ----------------------------------------------------


def test_the_test_phase_is_labelled_test_phase_with_its_turns(tmp_path: Path) -> None:
    log = single_arm_run(tmp_path / "runs")
    state = ConsoleState.from_events(read_events(log))
    phases = [(s.index, s.phase, s.turns) for s in state.arm("harness").sessions()]
    assert phases == [(1, "build", 2), (2, "test", 3)]
    evidence = render(log)["3"]
    assert "Session 1 · 2 turns" in evidence
    assert "Test phase · 3 turns" in evidence
    assert "Session 2" not in evidence


def test_real_build_sessions_keep_their_numbers(tmp_path: Path) -> None:
    log = multi_session_run(tmp_path / "runs")
    sessions = ConsoleState.from_events(read_events(log)).arm("harness").sessions()
    assert [(s.index, s.phase) for s in sessions] == [(1, "build"), (2, "build"), (3, "test")]
    evidence = render(log)["3"]
    assert "Session 1 · 2 turns" in evidence
    assert "Session 2 · 10 turns" in evidence
    assert "Test phase · 2 turns" in evidence


# -- fix 9: session markers stay in the live "Last turns" view ------------------------------------


def test_session_markers_stay_in_the_last_turns_view_mid_run(tmp_path: Path) -> None:
    log = multi_session_run(tmp_path / "runs", finish=False, extra_turns=12)
    state = ConsoleState.from_events(read_events(log))
    harness = state.arm("harness")
    assert harness.run_end is None  # mid-run: the live view, not the full list
    rows = harness.recent(8)
    assert [r.kind for r in rows if r.kind != "turn"] == ["session_stop", "session_resume"]
    assert len([r for r in rows if r.kind == "turn"]) == 8
    assert [r.seq for r in rows] == sorted(r.seq for r in rows)  # in log order
    live = render(log)["1"]
    assert "Last turns" in live
    assert "Session 1 stopped" in live and "Session 2 resumed" in live


# -- fix 3: "finished" once the run is complete ---------------------------------------------------


def test_the_state_knows_when_the_run_is_finished(tmp_path: Path) -> None:
    done = ConsoleState.from_events(read_events(single_arm_run(tmp_path / "a")))
    running = ConsoleState.from_events(read_events(single_arm_run(tmp_path / "b", done=False)))
    assert (done.finished, running.finished) == (True, False)
    assert ConsoleState().finished is False


def test_screen_updates_carry_finished_and_the_page_shows_it(tmp_path: Path) -> None:
    runs = tmp_path / "runs"
    log = single_arm_run(runs)

    async def first() -> dict:
        gen = screen_updates(
            log, tmp_path / "exports", ScreenRenderer(), log.parent.name, follow=False
        )
        message = await gen.__anext__()
        await gen.aclose()
        return json.loads(message["data"])

    assert asyncio.run(first())["finished"] is True
    client = TestClient(create_console_app(runs, exports_dir=tmp_path / "exports"))
    page = client.get(f"/run/{log.parent.name}").text
    assert 'id="conn" class="conn">finished<' in page
    script = (Path(__file__).parents[3] / "src/shipharness/console/static/stream.js").read_text()
    assert '"finished"' in script and "update.finished" in script


# -- fix 5: screen 4 ------------------------------------------------------------------------------


def _exports(tmp_path: Path, captured: list[tuple[str, str, bool]]) -> Path:
    exports = tmp_path / "exports"
    for i, (arm, day, single) in enumerate(captured):
        rec = record(
            run_id=f"r-{i}",
            arm=arm,
            single_arm=single,
            referee_version=REFEREE_VERSION,
            captured_at=f"{day}T10:00:00+00:00",
        )
        write_export("scores", rec.run_id, rec, exports)
    return exports


def test_screen_4_labels_the_runs_before_class_next_to_this_run(tmp_path: Path) -> None:
    exports = _exports(tmp_path, [("bare", "2000-01-01", False), ("harness", "2000-01-01", False)])
    log = single_arm_run(tmp_path / "runs")
    state = ConsoleState.from_events(read_events(log))
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", state.started_on or "")
    report = load_report(exports, before=state.started_on)
    html = ScreenRenderer().render_all(ScreenContext("x", state, report, str(exports)))["4"]
    assert "This run" in html
    assert "Before class: 1 run per arm" in html
    assert html.index("This run") < html.index("Before class")


def test_before_class_counts_only_records_from_earlier_days() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        exports = _exports(
            Path(tmp),
            [
                ("bare", "2026-10-16", False),
                ("harness", "2026-10-16", False),
                ("bare", "2026-10-17", False),
                ("harness", "2026-10-17", False),
                ("bare", "2026-10-18", False),  # the class day: not before class
                ("harness", "2026-10-18", False),
            ],
        )
        report = load_report(exports, before="2026-10-18")
        assert sum(len(g.dots) for g in report.groups) == 4
        assert report.later == 2
        assert report.runs_per_arm == {"bare": 2, "harness": 2}
        assert report.before_label == "Before class: 2 runs per arm"
        everything = load_report(exports)
        assert sum(len(g.dots) for g in everything.groups) == 6


def test_screen_4_says_plainly_when_a_panel_has_no_data(tmp_path: Path) -> None:
    exports = _exports(tmp_path, [("bare", "2026-10-17", False), ("harness", "2026-10-17", False)])
    log = ab_run(tmp_path / "runs")
    state = ConsoleState.from_events(read_events(log))
    report = load_report(exports, before="2026-10-18")
    html = ScreenRenderer().render_all(ScreenContext("x", state, report, str(exports)))["4"]
    assert "No ablation runs yet." in html
    assert "No reviewer verdicts yet." in html
    assert "No LangSmith experiments yet." in html


def test_screen_4_without_any_results_says_how_to_get_some(tmp_path: Path) -> None:
    html = render(single_arm_run(tmp_path / "runs"))["4"]
    assert "make show-1" in html and "make demo-1" in html
    assert "ScoreRecords" not in html  # plain words, not the export format


def test_the_run_list_without_runs_says_to_start_one_with_make_show_1(tmp_path: Path) -> None:
    client = TestClient(create_console_app(tmp_path / "runs", exports_dir=tmp_path / "exports"))
    text = client.get("/").text
    assert "No runs yet" in text and "make show-1" in text


# -- fix 6: the run list says what each run is -----------------------------------------------------


def test_run_summary_reads_section_feature_type_status_and_start(tmp_path: Path) -> None:
    runs = tmp_path / "runs"
    log = single_arm_run(runs)
    write_ab_json(log.parent, section="demo-1", mode="harness in action", task={"feature_id": "F1"})
    row = run_summary(log.parent)
    assert row.section == "Section 1: Instructions"
    assert row.feature == "Feature 1: Org-wide issue search"
    assert row.kind == "harness in action"
    assert row.status == "finished"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC", row.started)


def test_run_summary_of_a_running_ab_and_of_the_final(tmp_path: Path) -> None:
    runs = tmp_path / "runs"
    log = ab_run(runs)
    row = run_summary(log.parent)  # no ab.json yet: the section is not in the events
    assert (row.kind, row.status, row.section) == ("A/B", "finished", "unknown")
    write_ab_json(log.parent, section="final", mode="A/B", task={"feature_id": "F5"})
    row = run_summary(log.parent)  # ab.json, written when the A/B ends, is the record
    assert (row.section, row.feature, row.kind) == ("Final project", "Feature 5: Bulk close", "A/B")
    running = single_arm_run(runs, "ab-20261018-050000-dddddd", done=False)
    assert run_summary(running.parent).status == "running"


def test_run_summary_says_unknown_for_missing_fields(tmp_path: Path) -> None:
    run_dir = tmp_path / "runs" / "ab-20261018-000000-eeeeee"
    run_dir.mkdir(parents=True)
    (run_dir / "events.jsonl").write_text("", encoding="utf-8")
    row = run_summary(run_dir)
    assert (row.section, row.feature, row.kind, row.started) == ("unknown",) * 4
    assert row.status == "running"


def test_the_run_list_shows_each_run_newest_first(tmp_path: Path) -> None:
    runs = tmp_path / "runs"
    old = single_arm_run(runs, "ab-20261017-100000-aaaaaa")
    write_ab_json(old.parent, section="demo-1", mode="harness in action", task={"feature_id": "F1"})
    ab_run(runs, "ab-20261018-120000-bbbbbb")
    client = TestClient(create_console_app(runs, exports_dir=tmp_path / "exports"))
    text = client.get("/").text
    assert text.index("ab-20261018-120000-bbbbbb") < text.index("ab-20261017-100000-aaaaaa")
    assert "Section 1: Instructions" in text and "Feature 1: Org-wide issue search" in text
    assert "harness in action" in text and "A/B" in text
    assert "finished" in text and "unknown" in text


# -- fix 7: back to the run list -----------------------------------------------------------------


def test_every_run_page_has_a_visible_all_runs_link(tmp_path: Path) -> None:
    runs = tmp_path / "runs"
    log = single_arm_run(runs)
    client = TestClient(create_console_app(runs, exports_dir=tmp_path / "exports"))
    page = client.get(f"/run/{log.parent.name}").text
    assert re.search(
        r'<a [^>]*class="all-runs"[^>]*href="/"[^>]*>← All runs</a>', page
    ) or re.search(r'<a [^>]*href="/"[^>]*class="all-runs"[^>]*>← All runs</a>', page)
    script = (Path(__file__).parents[3] / "src/shipharness/console/static/stream.js").read_text()
    assert '"Escape"' in script and '"h"' in script and '"H"' in script


# -- fix 12: the blinded reviewer's reason on screen 3 --------------------------------------------


def test_screen_3_shows_the_recorded_reviewer_reason(tmp_path: Path) -> None:
    from shipharness.events import EventBus

    log = single_arm_run(tmp_path / "runs")
    with EventBus(log, ab_id=log.parent.name) as bus:
        bus.publish(
            "reviewer_output",
            {
                "findings": [],
                "tenant_isolation_risk": "none",
                "verdict": "reject",
                "summary": "The search ignores archived projects only in one of two queries.",
            },
            run_id="r-harness",
            arm="harness",
        )
    evidence = render(log)["3"]
    assert "reviewer reject" in evidence
    assert "The search ignores archived projects only in one of two queries." in evidence


def test_screen_3_adds_no_reviewer_reason_when_none_is_recorded(tmp_path: Path) -> None:
    evidence = render(single_arm_run(tmp_path / "runs"))["3"]
    assert "reviewer" not in evidence.lower().replace("reviewer_", "")


# -- fix 11: redone work ignores the harness's own state files ------------------------------------


def test_redone_work_ignores_the_harness_state_files(tmp_path: Path) -> None:
    from shipharness.events import EventBus
    from tests.unit.console.run_logs import LogWriter

    log = tmp_path / "runs" / "ab-20261018-040749-ffffff" / "events.jsonl"
    state_files = [
        "progress.md",
        "session-handoff.md",
        "docs/exec-plans/active/f2-comments.md",
        "feature_list.json",
    ]
    with EventBus(log, ab_id=log.parent.name) as bus:
        w = LogWriter(bus)
        w.start("harness", single_arm=True, feature="F2")
        for path in [*state_files, "app/api/comments.py"]:
            w.turn("harness", 1, 1, edit=path)
        w.stop("harness", 1)
        w.resume("harness", 2)
        for path in [*state_files, "app/api/comments.py"]:
            w.turn("harness", 2, 1, edit=path)
    sessions = ConsoleState.from_events(read_events(log)).arm("harness").sessions()
    assert sessions[1].redone == ["app/api/comments.py"]  # product work redone; state files not
    evidence = render(log)["3"]
    assert "app/api/comments.py" in evidence
    assert "progress.md" not in evidence.split("Sessions", 1)[1].split("</ol>", 1)[0]


def test_the_console_and_the_referee_share_one_list_of_harness_files() -> None:
    from shipharness.ab.artifacts import is_harness_artifact
    from shipharness.console import state

    assert state.is_harness_artifact is is_harness_artifact
    for path in ("progress.md", "session-handoff.md", "docs/exec-plans/x.md", "feature_list.json"):
        assert is_harness_artifact(path), path


# -- fix 14: the test phase of an A/B arm (demo-3) is labelled too --------------------------------


def test_the_test_phase_of_each_ab_arm_is_labelled(tmp_path: Path) -> None:
    log = ab_run(tmp_path / "runs")
    state = ConsoleState.from_events(read_events(log))
    for arm in ("bare", "harness"):
        assert [(s.index, s.phase) for s in state.arm(arm).sessions()] == [
            (1, "build"),
            (2, "test"),
        ]
    evidence = render(log)["3"]
    assert len(re.findall(r"Test phase · 1 turn\b(?!s)", evidence)) == 2
    assert "Session 2" not in evidence
