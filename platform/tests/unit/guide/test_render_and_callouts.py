"""platform/scripts/guide/term_render.py and callouts.py: terminal PNGs and numbered callouts."""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from .loader import load

tr = load("term_render")
co = load("callouts")
gl = load("guidelib")

SAMPLE = "\n".join(
    [
        "START 2026-10-18T04:54:55Z show-1",
        "cd /home/learner/guide-run",
        "A/B ab-20261018-045459-2efbfc (Feature 1: Org-wide issue search)",
        "  harness  completed  claim=done  passed=True " + "x" * 120,
        "END rc=0 wall=343s",
    ]
)


def test_prepare_lines_redacts_and_wraps() -> None:
    rows = tr.prepare_rows(SAMPLE, command="make show-1", width=100)
    texts = [r.text for r in rows]
    assert texts[0] == "$ make show-1"
    assert rows[0].kind == "prompt"
    assert "cd ~/guide-run" in texts
    assert not any("/home/learner" in t for t in texts)
    assert all(len(t) <= 100 for t in texts)
    # The long line wraps onto a continuation row.
    assert any(r.kind == "cont" for r in rows)


def test_prepare_lines_shows_the_command_once() -> None:
    text = "$ make show-1 PURPOSE=pilot\nA/B ab-1 (Feature 1)\nCost: $0.02\n"
    rows = tr.prepare_rows(text, command="make show-1 PURPOSE=pilot")
    assert [r.text for r in rows].count("$ make show-1 PURPOSE=pilot") == 1
    assert [r.text for r in rows][1] == "A/B ab-1 (Feature 1)"


def test_cli_takes_the_command_from_the_prompt_line(tmp_path: Path) -> None:
    src = tmp_path / "terminal.txt"
    src.write_text("$ make show-1\nA/B ab-1\n", encoding="utf-8")
    assert tr.main([str(src), str(tmp_path / "t.png")]) == 0
    rows = tr.prepare_rows("A/B ab-1\n", command="make show-1")
    assert [r.text for r in rows] == ["$ make show-1", "A/B ab-1"]


def test_prepare_lines_ranges_and_highlight() -> None:
    rows = tr.prepare_rows(SAMPLE, command="make show-1", ranges="-2", highlight={5})
    kinds = [r.kind for r in rows]
    assert kinds[0] == "prompt" and kinds[1] == "gap"
    assert "3 lines above" in rows[1].text
    last = [r for r in rows if r.text == "END rc=0 wall=343s"][0]
    assert last.highlight


def test_render_refuses_keys(tmp_path: Path) -> None:
    with pytest.raises(gl.SecretFound):
        tr.render(SAMPLE + "\nOPENAI_API_KEY=sk-" + "proj-abcdefghijklmnop1234", tmp_path / "t.png")
    assert not (tmp_path / "t.png").exists()


def test_render_refuses_key_in_command(tmp_path: Path) -> None:
    with pytest.raises(gl.SecretFound):
        tr.render("ok", tmp_path / "t.png", command="export K=lsv2_" + "pt_0123456789abcdef_01")


def test_render_writes_2x_png(tmp_path: Path) -> None:
    out = tmp_path / "t.png"
    tr.render(SAMPLE, out, command="make show-1", width=100, scale=2)
    img = Image.open(out)
    one = tmp_path / "one.png"
    tr.render(SAMPLE, one, command="make show-1", width=100, scale=1)
    assert img.size[0] == pytest.approx(2 * Image.open(one).size[0], abs=2)


def _shot(tmp_path: Path, size=(1600, 900)) -> Path:
    path = tmp_path / "shot.png"
    Image.new("RGB", size, "#0b0f14").save(path)
    return path


def test_annotate_returns_numbered_callouts(tmp_path: Path) -> None:
    src = _shot(tmp_path)
    out = tmp_path / "annotated.png"
    targets = [
        co.Target(gl.Box(100, 100, 300, 40), "Referee pill"),
        co.Target(gl.Box(900, 600, 200, 80), "Gate list"),
    ]
    callouts = co.annotate(src, out, targets)
    assert [c["n"] for c in callouts] == [1, 2]
    assert [c["text"] for c in callouts] == ["Referee pill", "Gate list"]
    img = Image.open(out)
    assert img.size == (1600, 900)
    for c in callouts:
        # The circle is drawn in the callout colour (left of the digit at its centre).
        assert img.getpixel((c["x"] - 18, c["y"]))[:3] == (127, 215, 255)


def test_annotate_arrows_do_not_cross(tmp_path: Path) -> None:
    src = _shot(tmp_path, size=(1600, 1000))
    # A layout that invites crossings: a wide target at the top, small ones stacked below it.
    targets = [
        co.Target(gl.Box(700, 700, 200, 40), "low"),
        co.Target(gl.Box(100, 100, 1400, 60), "wide top"),
        co.Target(gl.Box(700, 400, 200, 40), "middle"),
        co.Target(gl.Box(1200, 600, 200, 40), "right"),
    ]
    callouts = co.annotate(src, tmp_path / "a.png", targets)
    r = gl.callout_radius(1600)
    placements = []
    for c, t in zip(callouts, targets, strict=True):
        tx, ty = t.box.clamp(c["x"], c["y"])
        placements.append(gl.Placement(c["x"], c["y"], tx, ty))
    assert gl.conflicts(placements, r) == 0


def test_conflicts_counts_crossing_arrows() -> None:
    a = gl.Placement(0, 0, 100, 100)
    b = gl.Placement(0, 100, 100, 0)
    assert gl.conflicts([a, b], 10) >= 1
    c = gl.Placement(300, 300, 400, 300)
    assert gl.conflicts([a, c], 10) == 0


def test_annotate_without_targets_copies_image(tmp_path: Path) -> None:
    src = _shot(tmp_path)
    out = tmp_path / "plain.png"
    assert co.annotate(src, out, []) == []
    assert Image.open(out).size == (1600, 900)


def test_callout_colour_comes_from_console_css() -> None:
    css = ":root {\n  --harness: #7fd7ff;\n  --bg: #0b0f14;\n}"
    assert co.css_tokens(css)["harness"] == "#7fd7ff"
