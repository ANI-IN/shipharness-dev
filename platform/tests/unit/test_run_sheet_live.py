"""instructor/run-sheet.md: every demo step is live, and the class follows the final deck's flow.

The run sheet's demo flow may only launch live model runs (`make show-N`, `make demo-N`,
`make final`). Section 3 runs a live A/B (`make demo-3 FEATURE=version-checks`), not the
harness-only `make show-3`. Replays, recorded showcases, and constructed examples are fallbacks or
optional extras: they may appear only under a `## Fallback: ...` heading, which this test skips.

The flow (owner, round 3): each section's run launches at the section start, so it has the whole
section to finish before its demo; exactly one poll, at the start of Section 4 (2:55-2:57), picks
the final feature right before `make show-4` and `make final` are launched; breaks of 10 minutes
after Section 1 and 5 minutes after Section 3.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from shipharness.layout import find_repo_root

REPO = find_repo_root(Path(__file__))
RUN_SHEET = REPO / "instructor" / "run-sheet.md"
POLL_FILE = REPO / "instructor" / "poll-questions.md"

# Anything that starts or names a recorded or scripted run instead of a live one.
NOT_LIVE = re.compile(r"make replay|make example|shipharness example|--replay|RUN=")
# In the minute-by-minute rows of a section, even the words are out of place.
NOT_LIVE_ROW = re.compile(r"replay|example|recording|recorded", re.IGNORECASE)
LIVE_LAUNCH = {
    "Section 1": "make show-1",
    "Section 2": "make show-2 SESSION_BUDGET=12,38",
    "Section 3": "make demo-3 FEATURE=version-checks",
    "Section 4": "make show-4",
}
# The minute each run is launched: one minute into its section (Section 4 also launches the
# final).
LAUNCH_AT = {"Section 1": "0:11", "Section 2": "1:11", "Section 3": "2:01", "Section 4": "2:57"}
# The commands in "How long the runs take", and the block whose start each must finish before.
RUN_ENDS_BEFORE = {
    "make show-1": "Section 1 demo",
    "make show-2 SESSION_BUDGET=12,38": "Section 2 demo",
    "make demo-3 FEATURE=version-checks": "Section 3 demo",
    "make show-4": "Section 4 demo",
}
# Minutes added to a measured time as a margin for a slower run on the class day.
LIMIT_MARGIN_MIN = 2


def sections(text: str) -> list[tuple[str, str]]:
    """(heading, body) for every `## ` section; text before the first heading is skipped."""
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def is_fallback(heading: str) -> bool:
    return heading.lower().startswith("fallback")


def demo_sections(text: str) -> list[tuple[str, str]]:
    return [(h, body) for h, body in sections(text) if not is_fallback(h)]


def minute_rows(text: str) -> list[list[str]]:
    """The cells of each row of the minute-by-minute table (time, block, what, where, slides)."""
    body = dict(sections(text)).get("Minute-by-minute", "")
    rows = []
    for line in body.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and re.fullmatch(r"\d:\d\d-\d:\d\d", cells[0]):
            rows.append(cells)
    return rows


def minutes(clock: str) -> int:
    hours, mins = clock.split(":")
    return int(hours) * 60 + int(mins)


def row_start(rows: list[list[str]], block: str) -> int:
    match = [r for r in rows if r[1].startswith(block)]
    assert match, f"no '{block}' row in the minute-by-minute table"
    return minutes(match[0][0].split("-")[0])


def run_times(text: str) -> dict[str, float]:
    """Command -> its longest measured whole-command time in minutes, from "How long the runs
    take"."""
    body = dict(sections(text)).get("Minute-by-minute", "")
    part = body.split("### How long the runs take", 1)[1].split("\n### ", 1)[0]
    out: dict[str, float] = {}
    for line in part.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not line.startswith("|") or len(cells) < 4 or not cells[0].startswith("`make"):
            continue
        found = re.findall(r"(\d+) min (\d+) s", cells[-3])
        if found:
            out[cells[0].strip("`")] = max(int(m) + int(s) / 60 for m, s in found)
    return out


def violations(text: str) -> list[str]:
    found = []
    for heading, body in demo_sections(text):
        for n, line in enumerate(body.splitlines(), 1):
            match = NOT_LIVE.search(line)
            if match:
                found.append(f"## {heading}, line {n}: {match.group(0)!r} in {line.strip()[:90]}")
    for cells in minute_rows(text):
        block = cells[1]
        if re.match(r"(Section [1-4]|Final)\b", block):
            match = NOT_LIVE_ROW.search(" ".join(cells))
            if match:
                found.append(f"minute-by-minute {cells[0]} {block}: {match.group(0)!r}")
    return found


@pytest.fixture(scope="module")
def run_sheet() -> str:
    return RUN_SHEET.read_text(encoding="utf-8")


def test_demo_steps_contain_only_live_commands(run_sheet: str) -> None:
    assert violations(run_sheet) == []


def test_each_section_launches_its_live_run(run_sheet: str) -> None:
    rows = minute_rows(run_sheet)
    for section, command in LIVE_LAUNCH.items():
        launch = [r for r in rows if r[1].startswith(f"{section} launch")]
        assert launch, f"no '{section} launch' row in the minute-by-minute table"
        assert command in " ".join(launch[0]), f"{section} launch does not run `{command}`"
        demo = [r for r in rows if r[1].startswith(f"{section} demo")]
        assert demo, f"no '{section} demo' row in the minute-by-minute table"
    s4 = [r for r in rows if r[1].startswith("Section 4 launch")][0]
    assert "make final FEATURES=" in " ".join(s4), "the final A/B is not launched in Section 4"


def test_each_run_launches_at_its_section_start(run_sheet: str) -> None:
    rows = minute_rows(run_sheet)
    for section, at in LAUNCH_AT.items():
        launch = [r for r in rows if r[1].startswith(f"{section} launch")][0]
        start, _ = launch[0].split("-")
        assert minutes(start) <= minutes(at) <= minutes(start) + 2, launch
        assert f"at {at}" in " ".join(launch), f"{section} launch row does not say 'at {at}'"


def test_exactly_one_poll_at_the_start_of_section_4(run_sheet: str) -> None:
    rows = minute_rows(run_sheet)
    polls = [r for r in rows if "poll" in r[1].lower()]
    assert [r[0] for r in polls] == ["2:55-2:57"], polls
    assert re.search(r"bulk.close", " ".join(polls[0]), re.I), "the poll picks the final feature"
    others = [r for r in rows if r not in polls and "poll" in " ".join(r).lower()]
    assert others == [], others


def test_no_section_opens_with_a_poll(run_sheet: str) -> None:
    for heading, body in demo_sections(run_sheet):
        found = re.findall(r"(?im)^\*\*(?:S[1-4] |Section [1-4] )?poll\b.*", body)
        assert found == [], f"## {heading}: {found}"
    assert not re.search(r"S[1-4] poll|opens with (?:its|two) polls?", run_sheet)


def test_every_run_finishes_before_its_demo(run_sheet: str) -> None:
    rows = minute_rows(run_sheet)
    times = run_times(run_sheet)
    for command, demo in RUN_ENDS_BEFORE.items():
        assert command in times, f"no measured time for `{command}`"
        section = demo.rsplit(" ", 1)[0]
        assert LIVE_LAUNCH[section] == command
        end = row_start(rows, f"{section} launch") + times[command] + LIMIT_MARGIN_MIN
        assert end <= row_start(rows, demo), f"`{command}` ends at minute {end:.0f}, after {demo}"
    final = [c for c in times if c.startswith("make final")]
    assert final, "no measured time for `make final`"
    # Two features run one after the other, next to show-4.
    end = row_start(rows, "Section 4 launch") + 2 * (times[final[0]] + LIMIT_MARGIN_MIN)
    assert end <= row_start(rows, "Final"), f"two final features end at minute {end:.0f}"


def test_the_poll_file_has_one_poll(run_sheet: str) -> None:
    text = POLL_FILE.read_text(encoding="utf-8")
    headings = [h for h, _ in sections(text)]
    assert len(headings) == 1 and "final feature" in headings[0].lower(), headings
    assert "2:55" in text and not re.search(r"\bS[1-4]\b.*poll|per section", text, re.I)


def test_breaks_follow_the_class_plan(run_sheet: str) -> None:
    # The breaks: 10 minutes after Section 1 and 5 minutes after Section 3 (Section 4 has 45
    # minutes).
    breaks = [r[0] for r in minute_rows(run_sheet) if r[1] == "Break"]
    assert breaks == ["1:00-1:10", "2:50-2:55"]


def test_minute_rows_cover_the_class_without_gaps(run_sheet: str) -> None:
    times = [r[0].split("-") for r in minute_rows(run_sheet)]
    assert times[0][0] == "0:00" and times[-1][1] == "4:00"
    for (_, end), (start, _) in zip(times, times[1:], strict=False):
        assert end == start, f"gap or overlap between {end} and {start}"


def test_fallbacks_have_their_own_marked_section(run_sheet: str) -> None:
    headings = [h for h, _ in sections(run_sheet)]
    fallback = [h for h in headings if is_fallback(h)]
    assert fallback, "no '## Fallback: ...' section for the replay procedure"
    assert any("make replay" in body for h, body in sections(run_sheet) if is_fallback(h))
    # Fallbacks come after the demo flow, never between its steps.
    assert headings.index(fallback[0]) > headings.index("Minute-by-minute")


@pytest.mark.parametrize(
    "line",
    [
        "| 0:40-0:50 | Section 1 demo: harness in action | then `make replay RUN=ab-1` | C | 19 |",
        "| 0:50-0:53 | Section 1 demo: extra | `make example-1` | Terminal B | 19 |",
        "| 0:50-0:53 | Section 1 demo: x | `uv run shipharness example --section demo-1` | B | 1 |",
        "| 0:50-0:53 | Section 1 demo: extra | `uv run shipharness ab --replay x` | B | 19 |",
        "| 0:46-0:50 | Section 1 demo: real run, replayed | The replay | C | 19 |",
    ],
)
def test_a_replay_or_example_in_a_demo_row_is_caught(line: str) -> None:
    text = (
        "## Minute-by-minute\n\n| Time | Block | What | Where | Slides |\n|---|---|---|---|---|\n"
        f"{line}\n\n## Fallback: replay procedure\n\n`make replay RUN=<id>`\n"
    )
    assert violations(text)


def test_the_fallback_section_is_skipped() -> None:
    text = (
        "## Minute-by-minute\n\n| Time | Block | What | Where | Slides |\n|---|---|---|---|---|\n"
        "| 0:10-0:12 | Section 1 launch | `make show-1` at 0:11 | B | Section 1 start |\n\n"
        "## Fallback: replay procedure\n\n`make replay RUN=<id>`; `make example-1`\n"
    )
    assert violations(text) == []
