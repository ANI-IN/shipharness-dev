"""course-template/tools/capture/: redaction, key refusal, terminal renders, callout geometry,
and the capture config (adapted from the course's own guide-tooling tests)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

CAPTURE = Path(__file__).resolve().parents[1] / "tools" / "capture"
if str(CAPTURE) not in sys.path:
    sys.path.insert(0, str(CAPTURE))  # the scripts import capturelib by name

PIL = pytest.importorskip("PIL")
import callouts as co  # noqa: E402
import capturelib as gl  # noqa: E402
import term_render as tr  # noqa: E402
from PIL import Image  # noqa: E402

# Redaction -----------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "clean"),
    [
        ("cd /home/learner/guide-run && make demo", "cd ~/guide-run && make demo"),
        ("/home/someone", "~"),
        ("open /mnt/c/Users/someone/Desktop/x.png", "open ~/Desktop/x.png"),
        (r"C:\Users\someone\Desktop\x.png", r"~\Desktop\x.png"),
        ("/Users/someone/code/x", "~/code/x"),
        ("/workspace/app/main.py stays", "/workspace/app/main.py stays"),
        ("/homework/x is not a home", "/homework/x is not a home"),
    ],
)
def test_redact_paths(raw: str, clean: str) -> None:
    assert gl.redact_paths(raw) == clean


def test_redact_user_names() -> None:
    text = "built by jdoe on jdoe-laptop; jdoesmith stays"
    assert gl.redact_users(text, ["jdoe"]) == "built by <user> on <user>-laptop; jdoesmith stays"
    assert gl.redact_users(text, []) == text


def test_host_path_hits_finds_each_kind() -> None:
    text = "a /home/learner/x b /mnt/c/Users/someone/y c C:\\Users\\someone\\z"
    assert len(gl.host_path_hits(text)) == 3
    assert gl.host_path_hits("nothing personal at /workspace") == []
    assert gl.host_path_hits(gl.redact_paths("see /home/learner/guide-run/terminal.txt")) == []


def test_personal_hits_flags_real_mail_and_names_not_test_domains() -> None:
    assert gl.personal_hits("board as admin@acme.test") == []
    assert gl.personal_hits("me@example.com") == []
    assert gl.personal_hits("write to someone@gmail.com") == ["someone@gmail.com"]
    assert gl.personal_hits("owner jdoe", users=["jdoe"]) == ["jdoe"]


def test_account_hits_use_configured_url_patterns() -> None:
    url = "https://tracing.example.org/o/0a1b2c3d-1111-2222-3333-444455556666/projects/p"
    assert gl.account_hits(url)  # the UUID alone is enough
    assert gl.account_hits("see https://dash.vendor.io/org/x", [r"dash\.vendor\.io/org/"])
    assert gl.account_hits("see https://dash.vendor.io/org/x") == []
    assert gl.account_hits("container 39def2150923 · network none") == []


def test_mask_urls_replaces_matching_links() -> None:
    text = "trace at https://dash.vendor.io/org/123/run/9 and https://docs.python.org/3/"
    out = gl.mask_urls(text, [r"dash\.vendor\.io"])
    assert "dash.vendor.io/…" in out and "/org/123" not in out
    assert "https://docs.python.org/3/" in out


# Keys ----------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "OPENAI_API_KEY=sk-" + "proj-abcdefghijklmnop1234",
        "key sk-" + "abcdefghijklmnopqrstu",
        "TRACING_API_KEY=lsv2_" + "pt_0123456789abcdef_0123456789",
        "Authorization: Bearer abcdefghijklmnopqrstuvwxyz012345",
        "token ghp_" + "abcdefghijklmnopqrstuvwxyz0123456789",
        "aws AKIA" + "ABCDEFGHIJKLMNOP",
        "-----BEGIN " + "PRIVATE KEY-----",
    ],
)
def test_find_secrets_flags_keys(text: str) -> None:
    assert gl.find_secrets(text)
    with pytest.raises(gl.SecretFound):
        gl.check_no_secrets(text)


@pytest.mark.parametrize(
    "text",
    ["uv run app --section demo-1", "task-1 risk-free desk-top", "API_KEY is set (not shown)",
     "sk- alone", "task-abcdefghijklmnopqrstuvwxyz"],
)  # fmt: skip
def test_find_secrets_passes_plain_text(text: str) -> None:
    assert gl.find_secrets(text) == []
    gl.check_no_secrets(text)


def test_secret_message_never_contains_the_key() -> None:
    key = "sk-" + "proj-abcdefghijklmnop1234"
    with pytest.raises(gl.SecretFound) as err:
        gl.check_no_secrets(f"x={key}")
    assert key not in str(err.value) and "abcdefghijklmnop" not in str(err.value)


# Lines ---------------------------------------------------------------------------------------


def test_parse_and_select_ranges() -> None:
    assert gl.parse_ranges("1-3,7") == [(1, 3), (7, 7)]
    assert gl.parse_ranges("-5") == [(-5, -1)]
    with pytest.raises(ValueError):
        gl.parse_ranges("3-1")
    lines = [f"l{i}" for i in range(1, 11)]
    out = gl.select_lines(lines, gl.parse_ranges("2-3,9-10"))
    assert out == [gl.Gap(1), (2, "l2"), (3, "l3"), gl.Gap(5), (9, "l9"), (10, "l10")]


def test_wrap_and_clean() -> None:
    assert [len(p) for p in gl.wrap_line("x" * 250, 100)] == [100, 100, 50]
    assert gl.clean_line("\x1b[32mok\x1b[0m\tdone") == "ok      done"


# Callout geometry ----------------------------------------------------------------------------


def test_target_matches() -> None:
    assert gl.target_matches("← All runs", "← All  runs")
    assert not gl.target_matches("← All runs", "1 Live view")
    assert gl.target_matches(None, "anything")
    assert not gl.target_matches(None, "   ")


def test_place_callout_outside_target_and_inside_image() -> None:
    target = gl.Box(1000, 500, 400, 60)
    c = gl.place_callout(target, 3840, 2160, radius=60, taken=[])
    assert 60 <= c.cx <= 3840 - 60 and 60 <= c.cy <= 2160 - 60
    assert not target.inflate(60).contains(c.cx, c.cy)
    assert target.on_edge(c.tx, c.ty)


def test_place_callout_avoids_taken_and_other_targets() -> None:
    target = gl.Box(400, 300, 200, 40)
    first = gl.place_callout(target, 1600, 900, radius=30, taken=[])
    second = gl.place_callout(target, 1600, 900, radius=30, taken=[(first.cx, first.cy)])
    assert (second.cx - first.cx) ** 2 + (second.cy - first.cy) ** 2 >= (2 * 30) ** 2
    neighbour = gl.Box(200, 250, 190, 140)
    c = gl.place_callout(target, 1600, 900, radius=30, taken=[], avoid=[target, neighbour])
    assert not neighbour.inflate(18).contains(c.cx, c.cy)


def test_place_callout_arrow_does_not_cross_earlier_arrows() -> None:
    target = gl.Box(400, 300, 200, 40)
    earlier = [((360, 100), (360, 800))]
    c = gl.place_callout(target, 1600, 900, radius=30, taken=[], segments=earlier)
    assert not gl._crosses((c.cx, c.cy), (c.tx, c.ty), *earlier[0])


def test_conflicts_counts_crossing_arrows() -> None:
    a = gl.Placement(0, 0, 100, 100)
    b = gl.Placement(0, 100, 100, 0)
    assert gl.conflicts([a, b], 10) >= 1
    assert gl.conflicts([a, gl.Placement(300, 300, 400, 300)], 10) == 0


def test_callout_radius_and_scale() -> None:
    assert gl.callout_radius(3840) > gl.callout_radius(1200)
    assert gl.callout_radius(400) == gl.MIN_RADIUS
    assert gl.scale_box((10, 20, 30, 40), 2) == gl.Box(20, 40, 60, 80)


# Terminal renders and callouts ---------------------------------------------------------------

SAMPLE = "\n".join(
    [
        "START demo-1",
        "cd /home/learner/guide-run",
        "run 1 finished: passed=True " + "x" * 120,
        "END rc=0",
    ]
)


def test_prepare_rows_redacts_and_wraps() -> None:
    rows = tr.prepare_rows(SAMPLE, command="make demo", width=100)
    texts = [r.text for r in rows]
    assert texts[0] == "$ make demo" and "cd ~/guide-run" in texts
    assert not any("/home/learner" in t for t in texts)
    assert any(r.kind == "cont" for r in rows)


def test_prepare_rows_redacts_configured_users() -> None:
    rows = tr.prepare_rows("owner: jdoe\n", users=["jdoe"])
    assert rows[0].text == "owner: <user>"


def test_render_refuses_keys(tmp_path: Path) -> None:
    with pytest.raises(gl.SecretFound):
        tr.render(SAMPLE + "\nKEY=sk-" + "proj-abcdefghijklmnop1234", tmp_path / "t.png")
    assert not (tmp_path / "t.png").exists()


def test_render_writes_2x_png(tmp_path: Path) -> None:
    tr.render(SAMPLE, tmp_path / "two.png", command="make demo", scale=2)
    tr.render(SAMPLE, tmp_path / "one.png", command="make demo", scale=1)
    w2 = Image.open(tmp_path / "two.png").size[0]
    assert w2 == pytest.approx(2 * Image.open(tmp_path / "one.png").size[0], abs=2)


def _shot(tmp_path: Path, size=(1600, 1000)) -> Path:
    path = tmp_path / "shot.png"
    Image.new("RGB", size, "#101418").save(path)
    return path


def test_annotate_numbers_and_colour(tmp_path: Path) -> None:
    targets = [
        co.Target(gl.Box(100, 100, 300, 40), "Status pill"),
        co.Target(gl.Box(900, 600, 200, 80), "Result list"),
    ]
    colours = {"accent": "#4f8fd6", "bg": "#101418"}
    out = tmp_path / "a.png"
    callouts = co.annotate(_shot(tmp_path), out, targets, colours=colours)
    assert [c["n"] for c in callouts] == [1, 2]
    img = Image.open(out)
    for c in callouts:
        assert img.getpixel((c["x"] - 18, c["y"]))[:3] == (0x4F, 0x8F, 0xD6)


def test_annotate_arrows_do_not_cross(tmp_path: Path) -> None:
    targets = [
        co.Target(gl.Box(700, 700, 200, 40), "low"),
        co.Target(gl.Box(100, 100, 1400, 60), "wide top"),
        co.Target(gl.Box(700, 400, 200, 40), "middle"),
        co.Target(gl.Box(1200, 600, 200, 40), "right"),
    ]
    callouts = co.annotate(_shot(tmp_path), tmp_path / "a.png", targets)
    placements = []
    for c, t in zip(callouts, targets, strict=True):
        tx, ty = t.box.clamp(c["x"], c["y"])
        placements.append(gl.Placement(c["x"], c["y"], tx, ty))
    assert gl.conflicts(placements, gl.callout_radius(1600)) == 0


def test_palette_reads_css_tokens(tmp_path: Path) -> None:
    css = tmp_path / "app.css"
    css.write_text(":root {\n  --brand: #123456;\n  --page: #fafafa;\n}", encoding="utf-8")
    p = co.palette(css, accent_token="brand", bg_token="page")
    assert p == {"accent": "#123456", "bg": "#fafafa"}
    assert co.palette(None) == co.FALLBACK


# Capture config ------------------------------------------------------------------------------


def _config(tmp_path: Path, **over) -> Path:
    cfg = {
        "base": "http://127.0.0.1:8000",
        "users": ["jdoe"],
        "mask_urls": [r"dash\.vendor\.io"],
        "shots": [
            {
                "name": "home",
                "path": "/",
                "alt": "The home page with the list of runs and one status pill.",
                "callouts": [{"label": "Status pill", "sel": ".pill", "must": "passed"}],
            }
        ],
    }
    cfg.update(over)
    path = tmp_path / "capture.json"
    path.write_text(json.dumps(cfg), encoding="utf-8")
    return path


def test_capture_config_defaults(tmp_path: Path) -> None:
    import capture as cap

    cfg = cap.load_config(_config(tmp_path))
    assert (cfg.width, cfg.height, cfg.dpr) == (1024, 900, 2)
    assert cfg.shots[0].callouts[0].expected == "passed"


def test_capture_config_rejects_bad_names_and_too_many_callouts(tmp_path: Path) -> None:
    import capture as cap

    bad = [{"name": "../x", "path": "/", "alt": "A sentence of six words here."}]
    with pytest.raises(ValueError):
        cap.load_config(_config(tmp_path, shots=bad))
    many = [{"label": f"c{i}", "sel": "p"} for i in range(cap.MAX_CALLOUTS + 1)]
    shots = [{"name": "x", "path": "/", "alt": "A sentence of six words here.", "callouts": many}]
    with pytest.raises(ValueError):
        cap.load_config(_config(tmp_path, shots=shots))


def test_capture_privacy_check_on_page_text(tmp_path: Path) -> None:
    import capture as cap

    cfg = cap.load_config(_config(tmp_path, account_urls=[r"dash\.vendor\.io/org/"]))
    cap.check_private("A clean page: 3 runs, all passed.", cfg)
    for text in (
        "path /home/someone/x",
        "owner jdoe",
        "key sk-" + "abcdefghijklmnopqrstu",
        "link https://dash.vendor.io/org/77",
    ):
        with pytest.raises(cap.PrivacyError) as err:
            cap.check_private(text, cfg)
        assert "abcdefghijklmnop" not in str(err.value)
