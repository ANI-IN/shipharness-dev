"""new_module.py generates a complete, empty module skeleton whose own checks run."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

TEMPLATE = Path(__file__).resolve().parents[1]
SCRIPT = TEMPLATE / "scripts" / "new_module.py"
SECTIONS = ["Triggers", "Loops", "Hill climbing", "Reliability"]
NAME = "Loop Engineering for Coding Agents"


def _load():
    spec = importlib.util.spec_from_file_location("new_module", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


new_module = _load()


@pytest.fixture(scope="module")
def module_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("gen") / "module2"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--name", NAME, "--module", "2", "--sections", *SECTIONS,
         "--out", str(out)],
        capture_output=True,
        text=True,
    )  # fmt: skip
    assert result.returncode == 0, result.stderr
    # The checker finds the repository root by its pyproject.toml.
    assert (out / "pyproject.toml").is_file()
    return out


def _run(module_dir: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=module_dir)


def test_tree_has_every_folder_and_page(module_dir: Path) -> None:
    expected = [
        "README.md",
        "Makefile",
        ".env.example",
        ".gitignore",
        ".github/workflows/ci.yml",
        "setup/README.md",
        "setup/windows.md",
        "setup/macos.md",
        "setup/linux.md",
        "setup/pre-class.md",
        "final-project/README.md",
        "final-project/run.sh",
        "final-project/walkthrough.md",
        "final-project/CHECKLIST.md",
        "final-project/expected/.gitkeep",
        "slides/README.md",
        "use-in-your-repo/README.md",
        "platform/config/course.toml",
        "platform/scripts/check_style.py",
        "platform/scripts/lint_prose.py",
        "platform/tests/test_style_tools.py",
    ] + [
        f"docs/{name}.md"
        for name in (
            "start-here", "glossary", "faq", "costs", "reference", "evidence",
            "instructor-guide", "troubleshooting", "architecture", "STYLE", "diagrams/README",
            "evidence/general", "evidence/s1", "evidence/s4",
        )
    ]  # fmt: skip
    for number, name in enumerate(SECTIONS, start=1):
        folder = f"section-{number}-{new_module.slugify(name)}"
        expected += [
            f"{folder}/{item}"
            for item in (
                "README.md", "concepts.md", "session-notes.md", "demo/README.md", "demo/run.sh",
                "demo/walkthrough.md", "demo/files/.gitkeep", "demo/expected/.gitkeep",
                "assignment/README.md", "assignment/SPEC.md", "assignment/starter/README.md",
                "assignment/solution/SOLUTION.md", "post-class-reading/README.md",
                "diagrams/README.md",
            )
        ]  # fmt: skip
    missing = [p for p in expected if not (module_dir / p).is_file()]
    assert missing == []
    assert (module_dir / "section-3-hill-climbing").is_dir()


def test_no_template_token_and_nothing_from_module_1(module_dir: Path) -> None:
    for path in module_dir.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        assert not re.search(r"\{\{[A-Z_]+\}\}", text), path
        assert not re.search(r"TeamTrack|shipharness|Harness Engineering", text), path


def test_titles_and_names_use_the_module(module_dir: Path) -> None:
    title = "# Module 2: Loop Engineering for Coding Agents"
    assert (module_dir / "README.md").read_text().splitlines()[0] == title
    first = (module_dir / "section-3-hill-climbing/README.md").read_text().splitlines()[0]
    assert first == f"{title} - Section 3: Hill climbing"
    toml = (module_dir / "platform/config/course.toml").read_text()
    assert 'name = "Hill climbing"' in toml and 'slug = "hill-climbing"' in toml
    makefile = (module_dir / "Makefile").read_text()
    for target in ("setup:", "check-style:", "test:", "demo-4:", "check-assignment-4:"):
        assert target in makefile


def test_generated_checker_passes_without_errors_and_fails_strict(module_dir: Path) -> None:
    result = _run(module_dir, "platform/scripts/check_style.py")
    assert result.returncode == 0, result.stdout
    assert ", 0 errors," in result.stdout
    strict = _run(module_dir, "platform/scripts/check_style.py", "--strict")
    assert strict.returncode == 1
    assert "SC27" in strict.stdout  # the guidance comments mark the pages as not written yet


def test_generated_checker_catches_a_bare_code_and_a_wrong_title(module_dir: Path) -> None:
    page = module_dir / "section-1-triggers" / "concepts.md"
    original = page.read_text()
    try:
        page.write_text(original + "\nIn S2 the loop stops.\n")
        result = _run(module_dir, "platform/scripts/check_style.py", str(page))
        assert "SC21" in result.stdout and "Section 2: Loops" in result.stdout
    finally:
        page.write_text(original)
    readme = module_dir / "setup" / "README.md"
    original = readme.read_text()
    try:
        readme.write_text("# Setup\n" + original.split("\n", 1)[1])
        result = _run(module_dir, "platform/scripts/check_style.py", str(readme))
        assert "SC15" in result.stdout and result.returncode == 1
    finally:
        readme.write_text(original)


def test_generated_tools_and_tests_run(module_dir: Path) -> None:
    assert _run(module_dir, "platform/scripts/lint_prose.py").returncode == 0
    listing = _run(module_dir, "platform/scripts/check_style.py", "--list-checks")
    assert "SC27" in listing.stdout
    tests = _run(module_dir, "-m", "pytest", "-q", "-p", "no:cacheprovider", "platform/tests")
    assert tests.returncode == 0, tests.stdout + tests.stderr


def test_demo_stub_fails_loudly(module_dir: Path) -> None:
    result = subprocess.run(
        ["bash", str(module_dir / "section-2-loops/demo/run.sh")], capture_output=True, text=True
    )
    assert result.returncode == 1
    assert "not built yet" in result.stderr


def test_refuses_to_overwrite(module_dir: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--name", NAME, "--module", "2", "--sections", "One",
         "--out", str(module_dir)],
        capture_output=True,
        text=True,
    )  # fmt: skip
    assert result.returncode == 1
    assert "already exists" in result.stderr


@pytest.mark.parametrize(
    ("sections", "message"),
    [(["Loops", "loops"], "same folder name"), (["!!"], "no letters"), ([], "between 1 and 12")],
)
def test_rejects_bad_sections(tmp_path: Path, sections: list[str], message: str) -> None:
    with pytest.raises(new_module.SkeletonError, match=message):
        new_module.generate(tmp_path / "m", NAME, 2, sections)
    assert not (tmp_path / "m").exists()  # checked before anything is written


def test_render_rejects_unknown_tokens() -> None:
    with pytest.raises(new_module.SkeletonError, match="unknown template value"):
        new_module.render("{{NOPE}}", {})


# -- the demo guide, release hygiene, and honest-results files ------------------------------------

STEP_FIELDS = (
    "**Where:**",
    "**Type:**",
    "**You should see:**",
    "**Look at:**",
    "**What it means:**",
    "> [!CHECKPOINT]",
    "> [!IFDIFFERENT]",
    "> [!INSTRUCTOR]",
)
GUIDE_README_H2 = [
    "Who it is for",
    "What you need first",
    "How to follow it",
    "Time and cost",
    "The slides",
    "Build the PDF",
]
APPENDIX_H2 = [
    "Command cheat sheet",
    "Troubleshooting",
    "Glossary",
    "Fallback: replay a recorded run",
]
CHAPTER_H2 = ["Result summary", "Time and cost", "What to say in class"]
# A run id from another machine, an ISO date, or a dashboard account link: never in a skeleton.
LEAKS = re.compile(r"\b(?:ab|r)-\d{8}-\d{6}-[0-9a-f]{6}\b|\b20\d\d-\d\d-\d\d\b|/o/[0-9a-f-]{8,}")


def _h2(path: Path) -> list[str]:
    return re.findall(r"^## (.+)$", path.read_text(encoding="utf-8"), re.M)


def _steps(path: Path) -> list[tuple[str, str]]:
    """(heading, body) for each '### Step N:' of a guide page."""
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^(### Step \d+: .+)$", text, flags=re.M)
    steps = []
    for i in range(1, len(parts), 2):
        body = re.split(r"^#{1,3} ", parts[i + 1], maxsplit=1, flags=re.M)[0]
        steps.append((parts[i], body))
    return steps


def _chapters(module_dir: Path) -> list[Path]:
    return sorted((module_dir / "guide" / "chapters").glob("*.md"))


def test_guide_folder_has_every_part(module_dir: Path) -> None:
    guide = module_dir / "guide"
    for rel in ("README.md", "part0.md", "appendix.md", "source/CONVENTIONS.md", "images/.gitkeep"):
        assert (guide / rel).is_file(), rel
    names = [p.name for p in _chapters(module_dir)]
    assert names == [f"{n}-{new_module.slugify(s)}.md" for n, s in enumerate(SECTIONS, start=1)]


def test_guide_readme_has_the_required_sections(module_dir: Path) -> None:
    readme = module_dir / "guide" / "README.md"
    first = readme.read_text(encoding="utf-8").splitlines()[0]
    assert first == "# Module 2: Loop Engineering for Coding Agents - Live Demo Guide"
    assert _h2(readme) == GUIDE_README_H2
    text = readme.read_text(encoding="utf-8")
    assert "../slides/README.md" in text  # the pointer to the slides
    assert "Section 4: Reliability" in text  # one row per section in the time and cost table


def test_every_guide_step_has_the_full_template_in_order(module_dir: Path) -> None:
    pages = [module_dir / "guide" / "part0.md", module_dir / "guide" / "appendix.md"]
    pages += _chapters(module_dir)
    for page in pages:
        steps = _steps(page)
        assert steps, page
        for heading, body in steps:
            positions = [body.find(field) for field in STEP_FIELDS]
            assert -1 not in positions, (page, heading, positions)
            assert positions == sorted(positions), (page, heading)


def test_chapters_end_with_results_time_and_what_to_say(module_dir: Path) -> None:
    for chapter in _chapters(module_dir):
        assert _h2(chapter) == CHAPTER_H2, chapter
        first = chapter.read_text(encoding="utf-8").splitlines()[0]
        assert re.fullmatch(r"# Chapter \d: Section \d: .+", first), first
        assert "If your run differs" in chapter.read_text(encoding="utf-8")


def test_appendix_has_cheat_sheet_troubleshooting_glossary_and_fallback(module_dir: Path) -> None:
    assert _h2(module_dir / "guide" / "appendix.md") == APPENDIX_H2
    conventions = (module_dir / "guide" / "source" / "CONVENTIONS.md").read_text(encoding="utf-8")
    for field in STEP_FIELDS:
        assert field.removeprefix("> ") in conventions, field


def test_no_placeholder_leaks_into_commands_or_ids(module_dir: Path) -> None:
    for path in (module_dir / "guide").rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert not LEAKS.search(text), path
        for block in re.findall(r"```bash\n(.*?)```", text, re.S):
            # copy-ready commands: no prompt sign, no guide comment, no angle placeholder
            assert "<!--" not in block and not re.search(r"<[a-z][^>]*>", block), path
            assert not re.search(r"^\s*\$ ", block, re.M), path
        assert not re.search(r"\b(?:tonight|tomorrow|yesterday)\b", text, re.I), path


def test_gitignore_lists_the_tool_output_folders_with_a_test(module_dir: Path) -> None:
    ignore = (module_dir / ".gitignore").read_text(encoding="utf-8")
    assert "# Every folder the tool writes in a learner's copy" in ignore
    assert (module_dir / "platform/tests/test_gitignore.py").is_file()


def test_release_list_includes_every_public_folder(module_dir: Path) -> None:
    release = (module_dir / "platform/config/release.toml").read_text(encoding="utf-8")
    for folder in ("setup/", "guide/", "docs/", "final-project/", "slides/", "section-*/"):
        assert f'"{folder}"' in release, folder
    assert (module_dir / "platform/tests/test_release_list.py").is_file()


def test_measures_and_before_class_records_have_a_place(module_dir: Path) -> None:
    measures = (module_dir / "platform/config/measures.toml").read_text(encoding="utf-8")
    assert measures.count("[[sections]]") == len(SECTIONS)
    assert 'headline = ""' in measures and "secondary = []" in measures
    assert (module_dir / "platform/before-class/README.md").is_file()


def test_checkers_scan_the_guide_and_ban_time_words(module_dir: Path) -> None:
    chapter = _chapters(module_dir)[0]
    original = chapter.read_text(encoding="utf-8")
    try:
        chapter.write_text(original + "\nIn S2 we run it tonight.\n", encoding="utf-8")
        style = _run(module_dir, "platform/scripts/check_style.py")
        assert "SC21" in style.stdout and chapter.name in style.stdout
        prose = _run(module_dir, "platform/scripts/lint_prose.py")
        assert prose.returncode == 1 and "tonight" in prose.stdout
    finally:
        chapter.write_text(original, encoding="utf-8")


def test_checker_reports_a_step_missing_a_field(module_dir: Path) -> None:
    chapter = _chapters(module_dir)[0]
    original = chapter.read_text(encoding="utf-8")
    try:
        chapter.write_text(original.replace("**Look at:**", "Look at", 1), encoding="utf-8")
        result = _run(module_dir, "platform/scripts/check_style.py", str(chapter))
        assert "SC28" in result.stdout and result.returncode == 1
    finally:
        chapter.write_text(original, encoding="utf-8")


def test_guide_and_checklist_stay_project_agnostic() -> None:
    banned = re.compile(
        r"shipharness|TeamTrack|LangSmith|ANI-IN|House rule|Feature \d|gpt-\d|engineering-notes"
        r"|\b20\d\d-\d\d-\d\d\b|\b(?:ab|r)-\d{8}-\d{6}",
        re.I,
    )
    for name in ("STRUCTURE-AND-TASTE.md", "STRUCTURE-AND-TASTE-CHECKLIST.md", "README.md"):
        text = (TEMPLATE / name).read_text(encoding="utf-8")
        found = sorted({m.group(0) for m in banned.finditer(text)})
        assert found == [], (name, found)


def _fake_kit(root: Path) -> Path:
    """A kit folder like course-template/, with one file per part (built here, not the real one)."""
    files = {
        "slides/template.pptx": b"PK\x03\x04 not a real deck",
        "slides/outline.md": b"# Outline\n",
        "tools/guide/build_pdf.py": b"print('build')\n",
        "tools/layout/sweep.py": b"print('sweep')\n",
        "tools/secret_scan.py": b"print('scan')\n",
        "tools/tests/test_tools.py": b"raise SystemExit(1)\n",
        "tools/__pycache__/x.pyc": b"\x00",
        "skills/build-a-section/SKILL.md": b"---\nname: build-a-section\n---\n",
    }
    for rel, data in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_bytes(data)
    return root


def test_installs_the_kit_parts_when_present(tmp_path: Path) -> None:
    kit = _fake_kit(tmp_path / "kit")
    out = tmp_path / "m"
    new_module.generate(out, NAME, 2, ["One"], kit=kit)
    assert (out / "slides/template.pptx").read_bytes() == (
        kit / "slides/template.pptx"
    ).read_bytes()
    assert (out / "slides/outline.md").is_file()
    assert (out / "slides/README.md").read_text().startswith("# Module 2")  # skeleton page kept
    assert (out / "guide/source/build_pdf.py").is_file()
    assert (out / "guide/source/CONVENTIONS.md").is_file()
    assert (out / "platform/scripts/kit/layout/sweep.py").is_file()
    assert (out / "platform/scripts/kit/secret_scan.py").is_file()
    assert not (out / "platform/scripts/kit/guide").exists()  # installed into guide/source/
    assert not (out / "platform/scripts/kit/tests").exists()  # the kit's own tests stay behind
    assert not list(out.rglob("__pycache__"))
    assert (out / ".claude/skills/build-a-section/SKILL.md").is_file()


def test_skips_kit_parts_that_do_not_exist(tmp_path: Path) -> None:
    kit = tmp_path / "kit"
    (kit / "skills/one").mkdir(parents=True)
    (kit / "skills/one/SKILL.md").write_text("---\nname: one\n---\n")
    out = tmp_path / "m"
    new_module.generate(out, NAME, 2, ["One"], kit=kit)
    assert (out / ".claude/skills/one/SKILL.md").is_file()
    assert not (out / "platform/scripts/kit").exists()
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--name", NAME, "--module", "2", "--sections", "One",
         "--out", str(tmp_path / "m2"), "--kit", str(kit)],
        capture_output=True,
        text=True,
    )  # fmt: skip
    assert result.returncode == 0, result.stderr
    assert "skills" in result.stdout and "slides: not in the kit" in result.stdout


def test_ruff_cache_is_not_in_the_skeleton() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "course-template/skeleton"],
        capture_output=True,
        text=True,
        cwd=TEMPLATE.parent,
    ).stdout
    assert ".ruff_cache" not in tracked


def test_readme_is_the_front_door() -> None:
    readme = (TEMPLATE / "README.md").read_text(encoding="utf-8")
    for folder in ("skeleton/", "skills/", "playbooks/", "slides/", "tools/", "scripts/"):
        assert f"]({folder}" in readme, folder
    assert re.search(r"^## Create a new course in \d+ steps$", readme, re.M)


def test_checklist_covers_every_guide_part() -> None:
    guide = (TEMPLATE / "STRUCTURE-AND-TASTE.md").read_text(encoding="utf-8")
    checklist = (TEMPLATE / "STRUCTURE-AND-TASTE-CHECKLIST.md").read_text(encoding="utf-8")
    for heading in ("Live console", "Terminal", "Honest results", "Demo guide", "Release",
                    "Building with agents"):  # fmt: skip
        assert re.search(rf"^##+ .*{heading}", guide, re.M | re.I), heading
        assert re.search(rf"^## .*{heading}", checklist, re.M | re.I), heading


def test_kit_pages_in_guide_source_carry_the_module_title(tmp_path: Path) -> None:
    kit = _fake_kit(tmp_path / "kit")
    (kit / "tools/guide/README.md").write_text("# guide: the PDF builder\n\nText.\n")
    out = tmp_path / "m"
    new_module.generate(out, NAME, 2, ["One"], kit=kit)
    first = (out / "guide/source/README.md").read_text().splitlines()[0]
    assert first == f"# Module 2: {NAME} - guide: the PDF builder"


def test_a_new_course_with_the_real_kit_has_no_style_errors(tmp_path: Path) -> None:
    out = tmp_path / "m"
    new_module.generate(out, NAME, 2, ["One", "Two"], kit=TEMPLATE)
    done = subprocess.run(
        [sys.executable, "platform/scripts/check_style.py"], cwd=out, capture_output=True, text=True
    )
    assert " 0 errors" in done.stdout, done.stdout[-2000:]
