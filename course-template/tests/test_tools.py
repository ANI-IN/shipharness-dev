"""course-template/slides/ and course-template/tools/: the slide template, the deck extractor,
and the generic course tooling (guide, capture, layout-check, release, scan, style)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from types import ModuleType

import pytest

KIT = Path(__file__).resolve().parents[1]
SLIDES = KIT / "slides"
TOOLS = KIT / "tools"
TEMPLATE = SLIDES / "template.pptx"
TOOL_DIRS = ("guide", "capture", "layout-check", "release", "scan", "style")
# Names of the course this kit was cut from, and of its author's machine: none may reach the kit.
DENY = (
    "ship" + "harness",
    "Team" + "Track",
    "Lang" + "Smith",
    "ab-" + "20",
    "ANI" + "-IN",
    "Len" + "ovo",
    "/home/" + "ani",
)
COURSE_WORDS = DENY + ("Harness Engineering", "Coding Agents", "Module 1")
EXAMPLE_KINDS = ("title", "section", "concept", "diagram", "demo", "table", "notes")


def load(path: Path, name: str | None = None) -> ModuleType:
    """Import a script by path; its folder goes on sys.path (scripts import their siblings)."""
    name = name or path.stem
    if str(path.parent) not in sys.path:
        sys.path.insert(0, str(path.parent))
    if name in sys.modules and getattr(sys.modules[name], "__file__", "") == str(path):
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# Slides ---------------------------------------------------------------------------------------


def test_template_loads_with_layouts_and_example_slides() -> None:
    pptx = pytest.importorskip("pptx")
    prs = pptx.Presentation(str(TEMPLATE))
    layouts = sum(len(m.slide_layouts) for m in prs.slide_masters)
    assert layouts >= 10
    assert len(prs.slides) == len(EXAMPLE_KINDS)
    titles = [s.shapes.title.text if s.shapes.title else "" for s in prs.slides]
    assert any("console screen" in sh.text_frame.text for s in prs.slides for sh in s.shapes
               if sh.has_text_frame)  # fmt: skip
    assert any(sh.has_table for s in prs.slides for sh in s.shapes)
    assert "<COURSE TITLE>" in titles[0]
    for slide in prs.slides:
        notes = slide.notes_slide.notes_text_frame.text
        assert notes.startswith("Time: "), notes[:40]


def test_template_size_is_small() -> None:
    assert TEMPLATE.stat().st_size < 6_000_000


def test_template_has_no_course_strings() -> None:
    with zipfile.ZipFile(TEMPLATE) as z:
        names = z.namelist()
        assert not any("thumbnail" in n or "commentAuthors" in n for n in names)
        for name in names:
            if not name.endswith((".xml", ".rels")):
                continue
            text = z.read(name).decode("utf-8", "replace").casefold()
            hits = [w for w in COURSE_WORDS if w.casefold() in text]
            assert not hits, f"{name}: {hits}"


def test_make_template_never_writes_the_deck(tmp_path: Path) -> None:
    pytest.importorskip("pptx")
    mk = load(SLIDES / "scripts" / "make_template.py")
    with pytest.raises(ValueError):
        mk.make_template(tmp_path / "deck.pptx", tmp_path / "deck.pptx")
    assert [e["kind"] for e in mk.EXAMPLES] == list(EXAMPLE_KINDS)


def test_extract_deck_on_the_template(tmp_path: Path) -> None:
    pytest.importorskip("pptx")
    ex = load(SLIDES / "scripts" / "extract_deck.py")
    md = ex.deck_markdown(TEMPLATE)
    assert md.count("\n## Slide ") == len(EXAMPLE_KINDS)
    assert "## Slide 1: <COURSE TITLE>" in md
    assert "> Time: " in md and "console screen <N>" in md
    assert "| Section | Without the layer |" in md
    out = tmp_path / "deck.md"
    assert ex.main([str(TEMPLATE), "--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8").startswith("# template.pptx")


@pytest.mark.parametrize("name", ["README.md", "outline-template.md", "slide-review.md"])
def test_slide_docs_exist(name: str) -> None:
    text = (SLIDES / name).read_text(encoding="utf-8")
    assert len(text.split()) > 150


def test_slide_review_never_edits_the_deck() -> None:
    text = (SLIDES / "slide-review.md").read_text(encoding="utf-8")
    assert "extract_deck.py" in text and "never" in text.lower()


# Kit hygiene ----------------------------------------------------------------------------------


def _text_files() -> list[Path]:
    exts = {".md", ".py", ".css", ".html", ".json", ".txt", ".toml", ".sh", ".yml", ".yaml"}
    return [
        p
        for root in (SLIDES, TOOLS)
        for p in root.rglob("*")
        if p.is_file() and p.suffix in exts and "__pycache__" not in p.parts
    ]


def test_denylist_absent_from_slides_and_tools() -> None:
    files = _text_files()
    assert len(files) > 15
    for path in files:
        text = path.read_text(encoding="utf-8").casefold()
        hits = [w for w in DENY if w.casefold() in text]
        assert not hits, f"{path.relative_to(KIT)}: {hits}"


@pytest.mark.parametrize("tool", TOOL_DIRS)
def test_each_tool_has_a_readme(tool: str) -> None:
    readme = TOOLS / tool / "README.md"
    assert readme.is_file()
    assert len(readme.read_text(encoding="utf-8").split()) > 60


@pytest.mark.parametrize(
    "script",
    sorted(str(p.relative_to(TOOLS)) for p in TOOLS.rglob("*.py")) if TOOLS.is_dir() else ["x"],
)
def test_each_tool_script_imports(script: str) -> None:
    path = TOOLS / script
    module = load(path, "kit_" + path.stem)
    assert module.__doc__ and len(module.__doc__.split()) > 10


def test_style_points_to_the_skeleton_scripts() -> None:
    text = (TOOLS / "style" / "README.md").read_text(encoding="utf-8")
    for name in ("check_style.py", "lint_prose.py"):
        assert f"skeleton/platform/scripts/{name}" in text
        assert (KIT / "skeleton" / "platform" / "scripts" / name).is_file()
    assert not list((TOOLS / "style").glob("*.py"))  # pointed to, not duplicated
    for rule in ("tonight", "bracket", "first use", "line number"):
        assert rule in text.lower()


# Guide builder --------------------------------------------------------------------------------


def _guide_tree(tmp_path: Path) -> Path:
    root = tmp_path / "guide"
    (root / "chapters").mkdir(parents=True)
    (root / "intro.md").write_text("# Introduction: why\n\nPlain text.\n", encoding="utf-8")
    (root / "chapters" / "1-first.md").write_text(
        "# Chapter 1: First demo\n\n## Run it\n\n### Step 1: Start\n\n**Where:** terminal 1\n\n"
        "```bash\nmake demo\n```\n\n> [!CHECKPOINT]\n> It printed ok.\n\n"
        "![Screen 1](../images/s1/screen-1.png)\n\n*Screen 1 after the run.*\n",
        encoding="utf-8",
    )
    cfg = {
        "title": "<COURSE>",
        "subtitle": "Live Demo Guide",
        "short": "<COURSE> · Live Demo Guide",
        "date": "<DATE>",
        "cover_tag": "<REPO> · <APP>",
        "output": "Demo Guide.pdf",
        "parts": [["intro.md", "intro"], ["chapters/1-*.md", "ch1"], ["appendix.md", "appendix"]],
    }
    (root / "guide.json").write_text(json.dumps(cfg), encoding="utf-8")
    return root


def test_guide_builds_html_from_a_config(tmp_path: Path) -> None:
    pytest.importorskip("markdown_it")
    root = _guide_tree(tmp_path)
    bp = load(TOOLS / "guide" / "build_pdf.py", "kit_build_pdf")
    out = tmp_path / "guide.html"
    assert bp.main(["--config", str(root / "guide.json"), "--no-pdf", "--html", str(out)]) == 0
    html = out.read_text(encoding="utf-8")
    assert "&lt;COURSE&gt;" in html and "Live Demo Guide" in html
    assert 'class="cmd"' in html and "box-checkpoint" in html
    assert "img-missing" in html  # the image is not there: a placeholder box
    assert "--accent" in html  # the palette is CSS variables


def test_guide_reports_missing_parts(tmp_path: Path) -> None:
    pytest.importorskip("markdown_it")
    root = _guide_tree(tmp_path)
    bp = load(TOOLS / "guide" / "build_pdf.py", "kit_build_pdf")
    cfg = bp.load_config(root / "guide.json")
    report = bp.Report()
    found = bp.sources(cfg, report)
    assert [name for _, name in found] == ["intro", "ch1"]
    assert report.missing_parts == ["appendix.md"]


# Layout check ---------------------------------------------------------------------------------


def test_layout_sweep_and_rules() -> None:
    lc = load(TOOLS / "layout-check" / "layout_check.py", "kit_layout_check")
    vps = lc.sweep(min_width=320, max_width=640, step=160, heights=(600,), dprs=(2.0,))
    assert [(v.width, v.dpr) for v in vps if v.dpr == 1] == [(320, 1), (480, 1), (640, 1)]
    assert any(v.dpr == 2.0 for v in vps)
    clean = {
        "panels": 1, "scrollWidth": 800, "width": 800, "wide": [], "ellipsis": [],
        "offscreen": [], "clipped": [], "wrappedPills": [], "brokenWords": [],
        "reachedBottom": True,
    }  # fmt: skip
    assert lc.problems(clean) == []
    bad = dict(clean, scrollWidth=900, wrappedPills=["span.pill"], brokenWords=["abcdefgh"],
               reachedBottom=False, offscreen=["div right 950"], clipped=["div"])  # fmt: skip
    found = " | ".join(lc.problems(bad))
    for words in ("sideways", "pill", "broken", "scroll", "right edge", "clipped"):
        assert words in found


def test_layout_config_loads(tmp_path: Path) -> None:
    lc = load(TOOLS / "layout-check" / "layout_check.py", "kit_layout_check")
    path = tmp_path / "layout.json"
    path.write_text(json.dumps({"pages": [{"name": "home", "url": "http://x/"}]}), "utf-8")
    cfg = lc.load_config(path)
    assert cfg.pages[0].root == "body"
    assert cfg.pill_selector and cfg.step == 40


# Release --------------------------------------------------------------------------------------


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout


def _private_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "private"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    files = {
        "README.md": "# Course\n",
        "src/app.py": "VALUE = 1\n",
        "tests/test_app.py": "def test_ok():\n    assert True\n",
        "tests/test_grader.py": 'GRADER = "grader/cases.py"\n\ndef test_g():\n    assert GRADER\n',
        "grader/cases.py": "CASES = []\n",
        "research/notes.md": "private notes\n",
    }
    for rel, text in files.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(text, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "-c", "user.name=a", "-c", "user.email=a@example.com", "commit", "-qm", "init")
    return repo


def _release_cfg(rel: ModuleType):
    return rel.Config(
        allow=["README.md", "src/**", "tests/**"],
        private_dirs=["research/", "grader/"],
        author_name="Course Author",
        author_email="author@example.com",
        commit_message="<COURSE> release",
        tags=["release-v1"],
        verify=[sys.executable, "-c", "print('ok')"],
    )


def test_release_select_leaks_and_excluded_tests(tmp_path: Path) -> None:
    rel = load(TOOLS / "release" / "make_release.py", "kit_make_release")
    cfg = _release_cfg(rel)
    paths = ["README.md", "src/app.py", "tests/test_app.py", "grader/cases.py", "other.txt"]
    included, excluded = rel.select(paths, cfg)
    assert included == ["README.md", "src/app.py", "tests/test_app.py"]
    assert excluded["grader/cases.py"] == "private" and excluded["other.txt"] == "not allowed"
    assert rel.leaks(["src/app.py", "research/x.md"], cfg) == ["research/x.md"]
    sources = {
        "tests/test_g.py": '"""grader/cases.py in a docstring."""\nX = "grader/cases.py"\n',
        "tests/test_doc.py": '"""Mentions grader/cases.py only here."""\n',
    }  # fmt: skip
    found = rel.find_excluded_tests(sources, ["grader/cases.py"])
    assert list(found) == ["tests/test_g.py"]


def test_release_dry_run_builds_one_commit_and_verifies(tmp_path: Path) -> None:
    rel = load(TOOLS / "release" / "make_release.py", "kit_make_release")
    repo = _private_repo(tmp_path)
    dest = tmp_path / "public"
    result = rel.release(repo, _release_cfg(rel), dest, ref="HEAD")
    assert result.ok, result.problems
    assert "tests/test_grader.py" in result.dropped_tests
    assert sorted(_git(dest, "ls-files").split()) == [
        "README.md",
        "src/app.py",
        "tests/test_app.py",
    ]
    assert _git(dest, "rev-list", "--count", "HEAD").strip() == "1"
    assert "release-v1" in _git(dest, "tag")
    assert _git(dest, "log", "-1", "--format=%an").strip() == "Course Author"


def test_release_refuses_a_key_in_a_public_file(tmp_path: Path) -> None:
    rel = load(TOOLS / "release" / "make_release.py", "kit_make_release")
    repo = _private_repo(tmp_path)
    (repo / "src" / "app.py").write_text('KEY = "sk-' + 'abcdefghijklmnopqrstuv"\n', "utf-8")
    _git(repo, "-c", "user.name=a", "-c", "user.email=a@example.com", "commit", "-qam", "key")
    result = rel.release(repo, _release_cfg(rel), tmp_path / "public", ref="HEAD")
    assert not result.ok
    assert any("key" in p for p in result.problems)
    assert not any("abcdefghijklmnop" in p for p in result.problems)


# Scan -----------------------------------------------------------------------------------------


def test_scan_patterns_use_word_boundaries_and_mask() -> None:
    sc = load(TOOLS / "scan" / "scan_secrets.py", "kit_scan_secrets")
    key = "sk-" + "proj-abcdefghijklmnop1234"
    hits = sc.find_keys(f"OPENAI_API_KEY={key}")
    assert hits and hits[0].masked.startswith("sk-p") and key not in hits[0].masked
    assert sc.find_keys("task-abcdefghijklmnopqrstuvwxyz") == []  # no word boundary
    assert sc.find_host_paths("see /home/someone/x and C:\\Users\\someone\\y")
    assert sc.find_host_paths("/workspace/app") == []


def test_scan_finds_a_key_in_history_only(tmp_path: Path, capsys) -> None:
    sc = load(TOOLS / "scan" / "scan_secrets.py", "kit_scan_secrets")
    repo = _private_repo(tmp_path)
    key = "sk-" + "abcdefghijklmnopqrstuv"
    (repo / "src" / "app.py").write_text(f'KEY = "{key}"\n', "utf-8")
    _git(repo, "-c", "user.name=a", "-c", "user.email=a@example.com", "commit", "-qam", "add")
    (repo / "src" / "app.py").write_text("KEY = None\n", "utf-8")
    _git(repo, "-c", "user.name=a", "-c", "user.email=a@example.com", "commit", "-qam", "drop")
    report = sc.scan_repo(repo)
    assert report["tree_keys"] is False and report["history_keys"] is True
    assert sc.main(["--repo", str(repo)]) == 1
    out = capsys.readouterr().out
    assert key not in out and "abcdefghijklmnop" not in out


def _minimal_pdf(text: str) -> bytes:
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    out += b"".join(f"{o:010d} 00000 n \n".encode() for o in offsets)
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(out)


def test_scan_pdf_flags_paths_and_placeholders(tmp_path: Path) -> None:
    pytest.importorskip("pypdf")
    sp = load(TOOLS / "scan" / "scan_pdf.py", "kit_scan_pdf")
    bad = tmp_path / "bad.pdf"
    bad.write_bytes(_minimal_pdf("open /home/someone/x then TODO fill"))
    good = tmp_path / "good.pdf"
    good.write_bytes(_minimal_pdf("open ~/x then run the demo"))
    found = sp.scan_pdf(bad)
    assert found["host_paths"] and found["placeholders"]
    assert not any(sp.scan_pdf(good).values())
