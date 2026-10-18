"""platform/scripts/guide/guidelib.py: the pure parts of the demo guide's image tooling.

Redaction of host paths, refusing key-like text, line selection and wrapping for terminal
renders, callout geometry, and the images.json entry shape.
"""

from __future__ import annotations

import pytest

from .loader import load

gl = load("guidelib")


# Redaction -----------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "clean"),
    [
        ("cd /home/learner/guide-run && make show-1", "cd ~/guide-run && make show-1"),
        ("/home/someone", "~"),
        ("open /mnt/c/Users/someone/Desktop/x.png", "open ~/Desktop/x.png"),
        (r"C:\Users\someone\Desktop\x.png", r"~\Desktop\x.png"),
        ("/workspace/app/main.py stays", "/workspace/app/main.py stays"),
        ("/homework/x is not a home", "/homework/x is not a home"),
    ],
)
def test_redact_paths(raw: str, clean: str) -> None:
    assert gl.redact_paths(raw) == clean


def test_host_path_hits_finds_each_kind() -> None:
    text = "a /home/learner/x b /mnt/c/Users/someone/y c C:\\Users\\someone\\z"
    assert len(gl.host_path_hits(text)) == 3
    assert gl.host_path_hits("nothing personal at /workspace") == []


def test_personal_hits_flags_real_mail_not_test_domains() -> None:
    assert gl.personal_hits("board as admin@acme.test") == []
    assert gl.personal_hits("me@example.com") == []
    assert gl.personal_hits("write to someone@gmail.com") == ["someone@gmail.com"]


def test_host_path_hits_ignores_redacted_text() -> None:
    assert gl.host_path_hits(gl.redact_paths("see /home/learner/guide-run/terminal.txt")) == []


# Keys ----------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "OPENAI_API_KEY=sk-proj-abcdefghijklmnop1234",
        "key sk-abcdefghijklmnopqrstu",
        "LANGSMITH_API_KEY=lsv2_pt_0123456789abcdef_0123456789",
        "Authorization: Bearer abcdefghijklmnopqrstuvwxyz012345",
    ],
)
def test_find_secrets_flags_keys(text: str) -> None:
    assert gl.find_secrets(text)
    with pytest.raises(gl.SecretFound):
        gl.check_no_secrets(text)


@pytest.mark.parametrize(
    "text",
    [
        "uv run shipharness ab --section demo-1 --arms harness",
        "task-1 risk-free desk-top",
        "OPENAI_API_KEY is set (not shown)",
        "sk- alone",
    ],
)
def test_find_secrets_passes_plain_text(text: str) -> None:
    assert gl.find_secrets(text) == []
    gl.check_no_secrets(text)


def test_secret_message_never_contains_the_key() -> None:
    key = "sk-proj-abcdefghijklmnop1234"
    with pytest.raises(gl.SecretFound) as err:
        gl.check_no_secrets(f"x={key}")
    assert key not in str(err.value)
    assert "abcdefghijklmnop" not in str(err.value)


# Line selection and wrapping -----------------------------------------------------------------


def test_parse_ranges() -> None:
    assert gl.parse_ranges("1-3,7") == [(1, 3), (7, 7)]
    assert gl.parse_ranges("-5") == [(-5, -1)]
    assert gl.parse_ranges("") == []
    with pytest.raises(ValueError):
        gl.parse_ranges("3-1")


def test_select_lines_keeps_gaps_as_markers() -> None:
    lines = [f"l{i}" for i in range(1, 11)]
    out = gl.select_lines(lines, gl.parse_ranges("2-3,9-10"))
    assert out == [
        gl.Gap(1),
        (2, "l2"),
        (3, "l3"),
        gl.Gap(5),
        (9, "l9"),
        (10, "l10"),
    ]


def test_select_lines_last_n() -> None:
    lines = [f"l{i}" for i in range(1, 11)]
    out = gl.select_lines(lines, gl.parse_ranges("-3"))
    assert out == [gl.Gap(7), (8, "l8"), (9, "l9"), (10, "l10")]


def test_select_all_when_no_range() -> None:
    assert gl.select_lines(["a", "b"], []) == [(1, "a"), (2, "b")]


def test_wrap_line_short_and_long() -> None:
    assert gl.wrap_line("short", 100) == ["short"]
    assert gl.wrap_line("", 100) == [""]
    long = "word " * 30
    parts = gl.wrap_line(long.rstrip(), 40)
    assert all(len(p) <= 40 for p in parts)
    assert " ".join(p.strip() for p in parts).split() == long.split()


def test_wrap_line_breaks_unbroken_text() -> None:
    parts = gl.wrap_line("x" * 250, 100)
    assert [len(p) for p in parts] == [100, 100, 50]


def test_wrap_line_expands_tabs_and_strips_ansi() -> None:
    assert gl.clean_line("\x1b[32mok\x1b[0m\tdone") == "ok      done"


# Callout geometry ----------------------------------------------------------------------------


def test_scale_box() -> None:
    assert gl.scale_box((10, 20, 30, 40), 2) == gl.Box(20, 40, 60, 80)


def test_callout_radius_grows_with_width_and_has_a_floor() -> None:
    assert gl.callout_radius(3840) > gl.callout_radius(1200)
    assert gl.callout_radius(400) == gl.MIN_RADIUS


def test_place_callout_outside_target_and_inside_image() -> None:
    target = gl.Box(1000, 500, 400, 60)
    c = gl.place_callout(target, 3840, 2160, radius=60, taken=[])
    assert 60 <= c.cx <= 3840 - 60 and 60 <= c.cy <= 2160 - 60
    assert not target.inflate(60).contains(c.cx, c.cy)
    # The arrow tip lies on the target's edge.
    assert target.on_edge(c.tx, c.ty)


def test_place_callout_avoids_taken_circles() -> None:
    target = gl.Box(1000, 500, 400, 60)
    first = gl.place_callout(target, 3840, 2160, radius=60, taken=[])
    second = gl.place_callout(target, 3840, 2160, radius=60, taken=[(first.cx, first.cy)])
    assert (second.cx - first.cx) ** 2 + (second.cy - first.cy) ** 2 >= (2 * 60) ** 2


def test_place_callout_keeps_off_other_targets_and_busy_areas() -> None:
    target = gl.Box(400, 300, 200, 40)
    neighbour = gl.Box(200, 250, 190, 140)  # where the circle would go first (left)
    c = gl.place_callout(target, 1600, 900, radius=30, taken=[], avoid=[target, neighbour])
    assert not neighbour.inflate(18).contains(c.cx, c.cy)
    # A cost that marks everything above the target as busy pushes the circle elsewhere.
    c2 = gl.place_callout(
        target, 1600, 900, radius=30, taken=[], cost=lambda x, y: 500.0 if y < 300 else 0.0
    )
    assert c2.cy >= 300


def test_place_callout_arrow_does_not_cross_earlier_arrows() -> None:
    target = gl.Box(400, 300, 200, 40)
    # An earlier arrow runs vertically just left of the target.
    earlier = [((360, 100), (360, 800))]
    c = gl.place_callout(target, 1600, 900, radius=30, taken=[], segments=earlier)
    assert not gl._crosses((c.cx, c.cy), (c.tx, c.ty), *earlier[0])


def test_place_callout_inside_a_wide_row_when_outside_is_busy() -> None:
    target = gl.Box(100, 400, 1200, 50)
    inner_x = target.right - 30 - 8

    def cost(x: float, y: float) -> float:
        return 0.0 if abs(x - inner_x) < 1 else 500.0

    c = gl.place_callout(target, 1600, 900, radius=30, taken=[], cost=cost)
    assert target.contains(c.cx, c.cy)
    assert (c.tx, c.ty) == (c.cx, c.cy)  # no arrow


def test_place_callout_near_corner_stays_in_image() -> None:
    target = gl.Box(0, 0, 50, 20)
    c = gl.place_callout(target, 800, 600, radius=30, taken=[])
    assert 30 <= c.cx <= 770 and 30 <= c.cy <= 570


def test_place_callout_when_target_fills_image() -> None:
    target = gl.Box(0, 0, 800, 600)
    c = gl.place_callout(target, 800, 600, radius=30, taken=[])
    assert 30 <= c.cx <= 770 and 30 <= c.cy <= 570


def test_arrow_head_points_at_tip() -> None:
    pts = gl.arrow_head((100, 100), (0, 100), size=20)
    assert pts[0] == (100, 100)
    assert all(x < 100 for x, _ in pts[1:])


def test_crop_boxes_translate_and_drop_outside() -> None:
    crop = gl.Box(100, 100, 500, 500)
    inside = gl.Box(150, 160, 50, 20)
    outside = gl.Box(700, 700, 10, 10)
    assert gl.box_in_crop(inside, crop) == gl.Box(50, 60, 50, 20)
    assert gl.box_in_crop(outside, crop) is None


# images.json ---------------------------------------------------------------------------------


def _entry(**over):
    base = dict(
        file="s1-screen-1.png",
        screen=1,
        moment="after the run finished",
        alt="Screen 1 of the Section 1 run: the harness arm passed its gate.",
        callouts=[{"n": 1, "x": 10, "y": 20, "text": "Referee pill"}],
        source_run_id="ab-20261018-045459-2efbfc",
        recorded_or_live="recorded",
    )
    base.update(over)
    return gl.image_entry(**base)


def test_image_entry_shape() -> None:
    e = _entry()
    assert list(e) == [
        "file",
        "screen",
        "moment",
        "alt",
        "callouts",
        "source_run_id",
        "recorded_or_live",
    ]
    assert e["callouts"] == [{"n": 1, "x": 10, "y": 20, "text": "Referee pill"}]


@pytest.mark.parametrize(
    "over",
    [
        {"alt": ""},
        {"alt": "screenshot"},
        {"alt": "Screen 1 of the run without a full stop"},
        {"recorded_or_live": "maybe"},
        {"callouts": [{"n": 2, "x": 1, "y": 1, "text": "a"}]},
        {"callouts": [{"n": 1, "x": 1, "y": 1, "text": ""}]},
        {"file": "../escape.png"},
        {"file": "s1/screen.png"},
        {"alt": "Screen 1 shows /home/learner/guide-run on the page."},
    ],
)
def test_image_entry_rejects_bad_fields(over) -> None:
    with pytest.raises(ValueError):
        _entry(**over)


def test_merge_entries_replaces_by_file_and_keeps_order() -> None:
    a = _entry(file="a.png")
    b = _entry(file="b.png")
    b2 = _entry(file="b.png", moment="later")
    c = _entry(file="c.png")
    merged = gl.merge_entries([a, b], [b2, c])
    assert [e["file"] for e in merged] == ["a.png", "b.png", "c.png"]
    assert merged[1]["moment"] == "later"
