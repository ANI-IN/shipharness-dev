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
