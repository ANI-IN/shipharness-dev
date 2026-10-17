"""instructor/run-sheet.md: every demo step is live (owner message 7: demo sections are live).

The run sheet's demo flow may only launch live model runs (`make show-N`, `make demo-N`,
`make final`). Replays, recorded showcases, and constructed examples are fallbacks or optional
extras: they may appear only under a `## Fallback: ...` heading, which this test skips.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from shipharness.layout import find_repo_root

REPO = find_repo_root(Path(__file__))
RUN_SHEET = REPO / "instructor" / "run-sheet.md"

# Anything that starts or names a recorded or scripted run instead of a live one.
NOT_LIVE = re.compile(r"make replay|make example|shipharness example|--replay|RUN=")
# In the minute-by-minute rows of a section, even the words are out of place.
NOT_LIVE_ROW = re.compile(r"replay|example|recording|recorded", re.IGNORECASE)
LIVE_LAUNCH = {
    "S1": "make show-1",
    "S2": "make show-2 SESSION_BUDGET=12,38",
    "S3": "make show-3",
    "S4": "make show-4",
}


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


def violations(text: str) -> list[str]:
    found = []
    for heading, body in demo_sections(text):
        for n, line in enumerate(body.splitlines(), 1):
            match = NOT_LIVE.search(line)
            if match:
                found.append(f"## {heading}, line {n}: {match.group(0)!r} in {line.strip()[:90]}")
    for cells in minute_rows(text):
        block = cells[1]
        if re.match(r"(S[1-4]|Final)\b", block):
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
    s4 = [r for r in rows if r[1].startswith("S4 launch")][0]
    assert "make final FEATURES=" in " ".join(s4), "the final A/B is not launched live in S4"


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
        "| 0:40-0:50 | S1 demo: harness in action | then `make replay RUN=ab-1` | Console | 19 |",
        "| 0:50-0:53 | S1 demo: extra | `make example-1` | Terminal B | 19 |",
        "| 0:50-0:53 | S1 demo: extra | `uv run shipharness example --section demo-1` | B | 19 |",
        "| 0:50-0:53 | S1 demo: extra | `uv run shipharness ab --replay x` | B | 19 |",
        "| 0:46-0:50 | S1 demo: real run, replayed | The replay | Console | 19 |",
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
        "| 0:13-0:15 | S1 launch | `make show-1` | Terminal B | 9 |\n\n"
        "## Fallback: replay procedure\n\n`make replay RUN=<id>`; `make example-1`\n"
    )
    assert violations(text) == []
