"""Generate an empty course module skeleton: folders, page templates, style guide, checker, CI.

Usage:
    python course-template/scripts/new_module.py --name "Loop Engineering for Coding Agents" \
        --module 2 --sections "Triggers" "Loops" "Hill climbing" "Reliability" --out ../module2

Options:
    --name       the module name, without "Module N:"
    --module     the module number in the program
    --sections   the section names, in class order (one to twelve)
    --out        the folder to create; it must not exist yet (nothing is ever overwritten)
    --project    the name of the code project the module builds on, used in one concepts heading
                 ("How <project> does it"); default "the project", change it in course.toml later
    --demo-files the folder in each demo/ that holds the real files the demo uses (default "files")
    --kit        a kit folder (default: none); --with-kit uses this course-template/ folder. Each
                 part the kit has is installed: slides/ into slides/, tools/guide/ into
                 guide/source/, the other tools into platform/scripts/kit/, skills/ into
                 .claude/skills/. A missing part is skipped; a skeleton file is never replaced.

The pages hold their headings and `<!-- guide: ... -->` comments that say what goes in each part.
The generated checker passes on the empty skeleton (0 errors) and fails with --strict until every
guide comment is replaced by real content. No model calls, no network.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
SKELETON = KIT / "skeleton"
# Rendered once per section (into section-N-<slug>/), once per section into docs/evidence/, and
# once per operating system into setup/.
SECTION_DIR = "section"
EVIDENCE_TEMPLATE = Path("docs/evidence/section.md")
SETUP_TEMPLATE = Path("setup/os.md")
# Rendered once per section into guide/chapters/N-<slug>.md.
CHAPTER_TEMPLATE = Path("guide/chapter.md")
SYSTEMS = {"windows": "Windows", "macos": "macOS", "linux": "Linux"}
TEXT_SUFFIXES = {".md", ".sh", ".py", ".toml", ".yml", ".yaml", ".example", ".txt", ""}
# Tool caches that may appear inside the skeleton folder; never copied.
CACHE_DIRS = {"__pycache__", ".ruff_cache", ".pytest_cache"}
# The kit's parts: (source in the kit, destination in the new module). tools/guide/ goes first, so
# the other tools are installed without it. A kit's own tests are never copied.
KIT_PARTS = (
    ("slides", "slides"),
    ("tools/guide", "guide/source"),
    ("tools", "platform/scripts/kit"),
    ("skills", ".claude/skills"),
)
KIT_SKIP_DIRS = CACHE_DIRS | {"tests"}


class SkeletonError(Exception):
    """A problem with the arguments or the output folder."""


def slugify(name: str) -> str:
    """A folder slug: lower case, words joined by hyphens ("Hill climbing" -> "hill-climbing")."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not slug:
        raise SkeletonError(f"section name {name!r} has no letters or digits")
    return slug


def render(text: str, values: dict[str, str]) -> str:
    """`text` with every {{KEY}} replaced. An unknown key is an error, so no token ships."""

    def one(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            raise SkeletonError(f"unknown template value {{{{{key}}}}}")
        return values[key]

    return re.sub(r"\{\{([A-Z_]+)\}\}", one, text)


def _toml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def course_toml(name: str, module: int, sections: list[str], project: str, demo: str) -> str:
    lines = [
        "# The module's settings. platform/scripts/check_style.py and lint_prose.py read this",
        "# file; nothing specific to one module lives in the scripts.",
        "",
        "[module]",
        f"number = {module}",
        f"title = {_toml_string(name)}",
        "# Used in the concepts heading 'How <project> does it'.",
        f"project = {_toml_string(project)}",
        "# The folder in each demo/ that holds the real files the demo uses.",
        f"demo_files = {_toml_string(demo)}",
        "# More agent files (regex, relative to the repository root), and banned phrases.",
        "agent_paths = []",
        "banned_phrases = {}",
        "",
    ]
    for number, section in enumerate(sections, start=1):
        lines += [
            "[[sections]]",
            f"number = {number}",
            f"name = {_toml_string(section)}",
            f"slug = {_toml_string(slugify(section))}",
            "",
        ]
    lines += [
        "# Codes that must never appear bare in prose: letter -> kind.",
        "[codes]",
        'S = "Section"',
        'A = "Assignment"',
        "",
        "# Other named kinds, written '<Kind> N: <name>' on first mention, for example:",
        "# [names.Feature]",
        '# 1 = "Name of the first feature"',
        "",
        "# Ids that belong only in the evidence pages (regex).",
        "[ids]",
        "run = '\\b(?:ab|r)-\\d{8}-\\d{6}-[0-9a-f]{6}\\b'",
        "finding = '\\bF-[ab]-\\d+\\b'",
        "",
        "# Exact source titles that may contain a banned word.",
        "[prose]",
        "allowed_titles = []",
        "",
        "# The source register: each source a page may cite, with the URL a link to it must use.",
        "# [[sources]]",
        '# name = "Publisher, short title"',
        "# mention = '\\bShort title\\b'",
        "# url = 'https://example\\.org/the-article'",
        "",
    ]
    return "\n".join(lines)


def measures_toml(sections: list[str]) -> str:
    """The pre-registered measures: fill each section in before its first comparison run."""
    lines = [
        "# The measures of each section, written down before the first comparison run and never",
        "# changed after it. The demo's headline is the headline measure; every other result is",
        "# labelled secondary. A measure applied wrongly may be re-judged from stored data (no new",
        "# runs), and the re-judging is disclosed on the evidence page.",
        "",
    ]
    for number, section in enumerate(sections, start=1):
        lines += [
            "[[sections]]",
            f"number = {number}",
            f"name = {_toml_string(section)}",
            'headline = ""',
            "secondary = []",
            "# The time bar for the live demo, in minutes, from launch.",
            "time_bar_minutes = 0",
            "",
        ]
    return "\n".join(lines)


def install_kit(kit: Path, out: Path) -> tuple[list[Path], list[str]]:
    """Copy each part the kit has into `out`, byte for byte. Return the files written and one
    line per part for the summary. Files the skeleton already wrote are kept."""
    written: list[Path] = []
    summary: list[str] = []
    taken: set[Path] = set()
    for source, dest in KIT_PARTS:
        folder = kit / source
        if not folder.is_dir():
            summary.append(f"{source}: not in the kit, skipped")
            continue
        count = 0
        for file in sorted(p for p in folder.rglob("*") if p.is_file()):
            rel = file.relative_to(folder)
            if KIT_SKIP_DIRS.intersection(rel.parts[:-1]) or file.resolve() in taken:
                continue
            taken.add(file.resolve())
            target = out / dest / rel
            if target.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)
            written.append(target)
            count += 1
        summary.append(f"{source}: {count} files into {dest}/")
    return written, summary


def title_kit_pages(files: list[Path], out: Path, name: str, module: int) -> None:
    """Kit pages installed under guide/ become course pages: their first heading gets the module
    title the style check requires ("# Module N: <name> - <page name>")."""
    for file in files:
        rel = file.relative_to(out).as_posix()
        if not (rel.startswith("guide/") and file.suffix == ".md"):
            continue
        lines = file.read_text(encoding="utf-8").splitlines(keepends=True)
        if lines and lines[0].startswith("# ") and not lines[0].startswith("# Module "):
            lines[0] = f"# Module {module}: {name} - {lines[0][2:]}"
            file.write_text("".join(lines), encoding="utf-8")


def makefile(sections: list[str]) -> str:
    numbers = range(1, len(sections) + 1)
    demo_targets = " ".join(f"demo-{n}" for n in numbers)
    check_targets = " ".join(f"check-assignment-{n}" for n in numbers)
    out = [
        "# Every course command is a make target. `make help` lists them.",
        "SHELL := /bin/bash",
        "CHECK_STYLE_OPTS ?=",
        "",
        ".PHONY: help setup lint check-style check-style-strict lint-prose test "
        f"{demo_targets} {check_targets}",
        "",
        "help: ## List every target",
        "\t@grep -E '^[a-zA-Z0-9_-]+:.*## ' $(MAKEFILE_LIST) | "
        "awk -F':.*## ' '{printf \"  %-22s %s\\n\", $$1, $$2}'",
        "",
        "setup: ## Install the pinned tools and create .env from .env.example",
        "\tuv sync",
        "\t@test -f .env || (cp .env.example .env && echo '+ created .env: add your keys')",
        "",
        "lint: ## Ruff lint and format check",
        "\tuv run ruff check .",
        "\tuv run ruff format --check .",
        "",
        "check-style: ## Course style check (errors fail; CHECK_STYLE_OPTS=--strict for warnings)",
        "\tuv run python platform/scripts/check_style.py $(CHECK_STYLE_OPTS)",
        "",
        "check-style-strict: ## Style check where warnings fail too (run before every publish)",
        "\tuv run python platform/scripts/check_style.py --strict",
        "",
        "lint-prose: ## Banned words and emoji",
        "\tuv run python platform/scripts/lint_prose.py",
        "",
        "test: ## The test suite",
        "\tuv run pytest -q",
        "",
    ]
    for number, name in enumerate(sections, start=1):
        folder = f"section-{number}-{slugify(name)}"
        out += [
            f"demo-{number}: ## Section {number}: {name}, the live demo",
            f"\t./{folder}/demo/run.sh",
            "",
            f"check-assignment-{number}: ## Assignment {number}: {name}, the self-check",
            f"\t@echo 'x check-assignment-{number}: write the self-check for {folder}/assignment/'",
            "\t@exit 1",
            "",
        ]
    return "\n".join(out)


def _write(path: Path, text: str, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    if executable:
        path.chmod(0o755)


def _copy_tree(src: Path, dest: Path, values: dict[str, str]) -> list[Path]:
    """Render every file under `src` into `dest`; return the files written."""
    written = []
    for file in sorted(p for p in src.rglob("*") if p.is_file()):
        rel = file.relative_to(src)
        target = dest / rel
        if file.suffix in TEXT_SUFFIXES or file.name.startswith("."):
            _write(target, render(file.read_text(encoding="utf-8"), values), file.suffix == ".sh")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)
        written.append(target)
    return written


def generate(
    out: Path,
    name: str,
    module: int,
    sections: list[str],
    project: str = "the project",
    demo_files: str = "files",
    kit: Path | None = None,
    summary: list[str] | None = None,
) -> list[Path]:
    """Create the skeleton in `out`, which must not exist. Return the files written."""
    if out.exists():
        raise SkeletonError(f"{out} already exists: choose a new folder (nothing is overwritten)")
    if not name.strip():
        raise SkeletonError("--name is empty")
    if module < 1:
        raise SkeletonError("--module must be 1 or more")
    if not 1 <= len(sections) <= 12:
        raise SkeletonError("give between 1 and 12 section names")
    slugs = [slugify(s) for s in sections]
    if len(set(slugs)) != len(slugs):
        raise SkeletonError("two sections have the same folder name")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", demo_files):
        raise SkeletonError("--demo-files must be a lower-case folder name")
    if kit is not None and not kit.is_dir():
        raise SkeletonError(f"--kit {kit} is not a folder")

    title = f"Module {module}: {name.strip()}"
    section_rows = "\n".join(
        f"| Section {n}: {s} | [section-{n}-{slugify(s)}/](section-{n}-{slugify(s)}/README.md) |"
        for n, s in enumerate(sections, start=1)
    )
    base = {
        "MODULE_TITLE": title,
        "MODULE_NUMBER": str(module),
        "MODULE_NAME": name.strip(),
        "PROJECT": project,
        "DEMO_FILES": demo_files,
        "SECTION_COUNT": str(len(sections)),
        "SECTION_ROWS": section_rows,
        "GUIDE_CHAPTERS": "\n".join(
            f"   - [Section {n}: {s}](chapters/{n}-{slugify(s)}.md)"
            for n, s in enumerate(sections, start=1)
        ),
        "GUIDE_ROWS": "\n".join(
            f"| Section {n}: {s} | `make demo-{n}` | <!-- guide: range, two runs alone --> |"
            " <!-- guide: range --> |"
            for n, s in enumerate(sections, start=1)
        ),
    }
    written: list[Path] = []
    out.mkdir(parents=True)
    special = {SECTION_DIR}
    for file in sorted(p for p in SKELETON.rglob("*") if p.is_file()):
        rel = file.relative_to(SKELETON)
        if rel.parts[0] in special or rel in (EVIDENCE_TEMPLATE, SETUP_TEMPLATE, CHAPTER_TEMPLATE):
            continue
        if CACHE_DIRS.intersection(rel.parts):
            continue
        target = out / rel
        _write(target, render(file.read_text(encoding="utf-8"), base), file.suffix == ".sh")
        written.append(target)

    for key, label in SYSTEMS.items():
        text = render((SKELETON / SETUP_TEMPLATE).read_text(encoding="utf-8"), base | {"OS": label})
        target = out / "setup" / f"{key}.md"
        _write(target, text)
        written.append(target)

    for number, section in enumerate(sections, start=1):
        folder = f"section-{number}-{slugify(section)}"
        values = base | {
            "N": str(number),
            "SECTION_NAME": section,
            "SECTION_SLUG": slugify(section),
            "SECTION_DIR": folder,
        }
        written += _copy_tree(SKELETON / SECTION_DIR, out / folder, values)
        demo = out / folder / "demo" / demo_files / ".gitkeep"
        _write(demo, "")
        written.append(demo)
        text = render((SKELETON / EVIDENCE_TEMPLATE).read_text(encoding="utf-8"), values)
        target = out / "docs" / "evidence" / f"s{number}.md"
        _write(target, text)
        written.append(target)
        text = render((SKELETON / CHAPTER_TEMPLATE).read_text(encoding="utf-8"), values)
        target = out / "guide" / "chapters" / f"{number}-{slugify(section)}.md"
        _write(target, text)
        written.append(target)

    _write(out / "platform/config/course.toml", course_toml(name, module, sections, project,
                                                            demo_files))  # fmt: skip
    _write(out / "Makefile", makefile(sections))
    _write(out / "platform/config/measures.toml", measures_toml(sections))
    written += [out / name for name in ("platform/config/course.toml", "Makefile",
                                        "platform/config/measures.toml")]  # fmt: skip
    if kit is not None:
        files, lines = install_kit(kit, out)
        written += files
        title_kit_pages(files, out, name, module)
        if summary is not None:
            summary += lines
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--name", required=True, help="module name, without 'Module N:'")
    parser.add_argument("--module", required=True, type=int, help="module number")
    parser.add_argument("--sections", required=True, nargs="+", help="section names, in order")
    parser.add_argument("--out", required=True, type=Path, help="new folder to create")
    parser.add_argument("--project", default="the project", help="project name for one heading")
    parser.add_argument("--demo-files", default="files", help="folder of each demo's real files")
    kit = parser.add_mutually_exclusive_group()
    kit.add_argument("--kit", type=Path, help="install the parts of this kit folder")
    kit.add_argument("--with-kit", action="store_true", help="install this course-template kit")
    args = parser.parse_args(argv)
    summary: list[str] = []
    try:
        files = generate(
            args.out,
            args.name,
            args.module,
            args.sections,
            args.project,
            args.demo_files,
            kit=KIT if args.with_kit else args.kit,
            summary=summary,
        )
    except SkeletonError as error:
        print(f"x {error}", file=sys.stderr)
        return 1
    print(f"+ wrote {len(files)} files to {args.out}")
    for line in summary:
        print(f"  kit {line}")
    print("  next: cd into it, git init, make setup, make check-style (0 errors expected),")
    print("  then write each page until make check-style-strict passes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
