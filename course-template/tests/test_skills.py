"""The kit's skills and playbooks: complete, well-formed, project-agnostic, with working links."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

TEMPLATE = Path(__file__).resolve().parents[1]
SKILLS = TEMPLATE / "skills"
PLAYBOOKS = TEMPLATE / "playbooks"

EXPECTED_SKILLS = [
    "new-course",
    "section-author",
    "live-demo-runner",
    "demo-guide-writer",
    "screenshot-capture",
    "fresh-reviewer",
    "evidence-and-results",
    "release-and-publish",
    "ui-layout-check",
    "slide-review",
    "style-and-naming",
]
# Every skill body has these H2 headings, in this order.
SKILL_HEADINGS = ["When to use", "Inputs", "Steps", "Outputs", "Checks"]

PLAYBOOK_HEADINGS: dict[str, list[str]] = {
    "brief-template.md": [
        "Goals",
        "Hard rules",
        "Deliverables",
        "Stop points",
        "Report format",
    ],
    "shared-agent-brief-template.md": [
        "Environment",
        "Running commands",
        "Hard rules",
        "Folder contract",
        "Write scopes",
        "Conventions fixed up front",
        "Step template",
    ],
    "agent-prompt-templates.md": [
        "How to use these prompts",
        "Implementer in a worktree",
        "Live runner",
        "Screenshot tooling",
        "Writer",
        "Repo updater",
        "Fresh reviewer",
        "Editor fix pass",
        "Slide reviewer",
    ],
    "status-and-report-formats.md": [
        "Five-line status",
        "Phase line",
        "Final report",
        "Budget line",
        "Decisions for you",
        "For afterwards",
    ],
    "merge-and-verify.md": [
        "Merge the branches",
        "Re-run the full suite on the combined tree",
        "Verify the agents' claims",
        "Scans before every push",
        "CI on both repositories",
        "Refresh the test copy",
    ],
    "honesty-and-measures.md": [
        "Pre-register before any run",
        "Never re-run for a nicer result",
        "Disclosure wording",
        "Timing rules",
    ],
    "lessons-learned.md": [
        "Real-screen overflow at display scaling",
        "Stale stylesheet",
        "Tests that fail only on the combined branch",
        "A moved folder falls out of the checks",
        "A redaction breaks the graders",
        "Fake keys trip the secret scanner",
        "A wording change breaks a parser",
        "Captions that describe a cut-off part",
        "Demo results that differ from expectations",
        "Agents hand back stale reports",
    ],
}

# Names that tie a document to one project, person, or machine.
DENYLIST = ["shipharness", "teamtrack", "langsmith", "ab-20", "ani-in", "lenovo", "/home/"]
DATE = re.compile(r"\b20\d\d-\d\d-\d\d\b")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADING = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
FENCE = re.compile(r"^(```|~~~).*?^\1\s*$", re.MULTILINE | re.DOTALL)


def _headings(text: str) -> list[str]:
    """The H2 headings outside fenced blocks (templates quote headings inside fences)."""
    return HEADING.findall(FENCE.sub("", text))


def _docs() -> list[Path]:
    return sorted(
        p for root in (SKILLS, PLAYBOOKS) if root.is_dir() for p in root.rglob("*") if p.is_file()
    )


def _frontmatter(text: str) -> dict[str, str]:
    assert text.startswith("---\n"), "SKILL.md must start with a YAML frontmatter block"
    end = text.index("\n---\n", 4)
    fields: dict[str, str] = {}
    key = ""
    for line in text[4:end].splitlines():
        m = re.match(r"^([a-z][a-z0-9_-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            fields[key] = "" if m.group(2) in (">", "|", ">-", "|-") else m.group(2).strip()
        elif key and line.startswith(" "):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def _load_lint():
    path = TEMPLATE / "skeleton" / "platform" / "scripts" / "lint_prose.py"
    spec = importlib.util.spec_from_file_location("kit_lint_prose", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_every_expected_skill_exists() -> None:
    missing = [name for name in EXPECTED_SKILLS if not (SKILLS / name / "SKILL.md").is_file()]
    assert not missing, f"skills without SKILL.md: {missing}"


def test_every_skill_folder_has_a_skill_md() -> None:
    assert SKILLS.is_dir()
    bare = [p.name for p in SKILLS.iterdir() if p.is_dir() and not (p / "SKILL.md").is_file()]
    assert not bare, f"skill folders without SKILL.md: {bare}"


@pytest.mark.parametrize("name", EXPECTED_SKILLS)
def test_skill_frontmatter(name: str) -> None:
    path = SKILLS / name / "SKILL.md"
    assert path.is_file()
    fields = _frontmatter(path.read_text(encoding="utf-8"))
    assert fields.get("name") == name, "frontmatter name must match the folder name"
    description = fields.get("description", "")
    assert description, "description missing"
    assert ": " not in description, "a colon-space breaks the YAML plain scalar; reword"
    assert len(description) <= 300, f"description is {len(description)} chars, keep it <= 300"
    assert re.search(r"\buse (when|before|at|after)\b", description, re.IGNORECASE), (
        "description must say when to use the skill"
    )


@pytest.mark.parametrize("name", EXPECTED_SKILLS)
def test_skill_body_headings_and_pointers(name: str) -> None:
    path = SKILLS / name / "SKILL.md"
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    headings = _headings(text)
    missing = [h for h in SKILL_HEADINGS if h not in headings]
    assert not missing, f"missing headings: {missing}"
    positions = [headings.index(h) for h in SKILL_HEADINGS]
    assert positions == sorted(positions), f"headings out of order: {headings}"
    links = LINK.findall(text)
    assert any("playbooks/" in link for link in links), "link at least one playbook"
    assert any("STRUCTURE-AND-TASTE" in link for link in links), "link the structure guide"


@pytest.mark.parametrize("playbook", sorted(PLAYBOOK_HEADINGS))
def test_playbook_headings(playbook: str) -> None:
    path = PLAYBOOKS / playbook
    assert path.is_file(), f"missing playbook {playbook}"
    headings = _headings(path.read_text(encoding="utf-8"))
    wanted = PLAYBOOK_HEADINGS[playbook]
    missing = [h for h in wanted if h not in headings]
    assert not missing, f"{playbook} lacks headings: {missing}"
    order = [headings.index(h) for h in wanted]
    assert order == sorted(order), f"{playbook} headings out of order"


def test_playbooks_index_lists_every_playbook() -> None:
    index = PLAYBOOKS / "README.md"
    assert index.is_file()
    text = index.read_text(encoding="utf-8")
    for playbook in PLAYBOOK_HEADINGS:
        assert f"]({playbook})" in text, f"playbooks/README.md does not link {playbook}"


def test_no_project_specific_names_or_dates() -> None:
    docs = _docs()
    assert docs, "no skill or playbook files yet"
    hits = []
    for path in docs:
        text = path.read_text(encoding="utf-8", errors="replace")
        low = text.lower()
        hits += [f"{path.relative_to(TEMPLATE)}: {word}" for word in DENYLIST if word in low]
        hits += [f"{path.relative_to(TEMPLATE)}: {m}" for m in DATE.findall(text)]
    assert not hits, "project-specific text:\n" + "\n".join(hits)


def test_every_relative_link_resolves() -> None:
    docs = [p for p in _docs() if p.suffix == ".md"]
    assert docs
    broken = []
    for path in docs:
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            if re.match(r"^[a-z]+:", target) or target.startswith("#") or target.startswith("<"):
                continue
            rel = target.split("#", 1)[0]
            if rel and not (path.parent / rel).resolve().exists():
                broken.append(f"{path.relative_to(TEMPLATE)} -> {target}")
    assert not broken, "broken links:\n" + "\n".join(broken)


def test_prose_lint_passes() -> None:
    lint = _load_lint()
    docs = [p for p in _docs() if p.suffix == ".md"]
    assert docs
    problems = []
    for path in docs:
        for line, message in lint.lint_text(path.read_text(encoding="utf-8")):
            problems.append(f"{path.relative_to(TEMPLATE)}:{line}: {message}")
    assert not problems, "\n".join(problems)
