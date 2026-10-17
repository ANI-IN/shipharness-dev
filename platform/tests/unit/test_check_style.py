"""platform/scripts/check_style.py: the mechanical rules of docs/STYLE.md.

Each check has at least one passing and one failing example. Fixtures build a small fake
repository under tmp_path and call `check_paths` directly; the CLI tests run the script.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

from shipharness.layout import find_repo_root

REPO = find_repo_root(Path(__file__))
SCRIPT = REPO / "platform" / "scripts" / "check_style.py"
_spec = importlib.util.spec_from_file_location("check_style", SCRIPT)
assert _spec and _spec.loader
cs = importlib.util.module_from_spec(_spec)
sys.modules["check_style"] = cs
_spec.loader.exec_module(cs)

TITLE = "# Module 1: Harness Engineering for Coding Agents"
DEMO = "section-1-instructions/demo/README.md"
PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 16
DEMO_H2 = [
    "The problem",
    "What you'll see",
    "Run it",
    "What to watch",
    "What the result means",
    "If it fails",
]
# Grader files and hidden test cases are not part of the course text (built by join, not literal).
GRADER_MD = "/".join(["section-1-instructions", "assignment", "solution", "grader", "x.md"])
HIDDEN_MD = "/".join(["section-3-scope-sandbox", "assignment", "hidden", "cases.md"])


def write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def write_bytes(root: Path, rel: str, data: bytes) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def problems(root: Path, rel: str, text: str, extra: dict[str, bytes] | None = None):
    write(root, rel, text)
    for name, data in (extra or {}).items():
        write_bytes(root, name, data)
    return cs.check_paths(root, [rel])


def demo_page(body: str) -> str:
    return f"{TITLE} - Demo 1: Search\n\n" + "".join(f"## {h}\n\n" for h in DEMO_H2) + body


IMG = "![Console screen 1 at minute 4](expected/screen-1-minute-4.png)"
IMG_FILE = {"section-1-instructions/demo/expected/screen-1-minute-4.png": PNG}
HD = "https://www.anthropic.com/engineering/harness-design-long-running-apps"
TG = "https://arxiv.org/abs/2402.09171"
CAPTION = "*At minute 4 the primary verdict is ready, while the secondary checks still run.*"

# (check, path, passing text, failing text, extra files for both, line of the failing problem)
CASES = [
    (
        "SC01",
        "docs/guide.md",
        "Run make doctor and check that both keys show ok.\n",
        "[[PENDING: screen 1 at minute 4 | source: live class | how: make show-1]]\n",
        {},
        1,
    ),
    (
        "SC01",
        "docs/guide.md",
        "```yaml\nkey: ${{ secrets.OPENAI_API_KEY }}\n```\n",
        "Intro.\n\nTODO: add the verdict screenshot\n",
        {},
        3,
    ),
    (
        "SC01",
        "docs/guide.md",
        "```bash\ndocker ps --format '{{.Names}}'\n```\n",
        "Open {{ class_url }} in your browser.\n",
        {},
        1,
    ),
    (
        "SC01",
        "docs/guide.md",
        "Capture the screen with the console open. The report has no `TODO` left.\n",
        "<!-- [[CAPTURE: screen 2 ]] -->\n",
        {},
        1,
    ),
    (
        "SC02",
        "docs/guide.md",
        "Captured from a real run of make show-1 on a quiet machine.\n",
        "Captured on , run ; your output will differ.\n",
        {},
        1,
    ),
    (
        "SC02",
        "docs/guide.md",
        "Run `make doctor`, then `make warm` (`make help` lists both). See `x`, `y`; then (`z`).\n",
        "The run took ( ) minutes.\n",
        {},
        1,
    ),
    (
        "SC02",
        "docs/guide.md",
        "After the run, the console shows the verdict.\n",
        "Read the line\n\nThe report was written by .\n",
        {},
        3,
    ),
    (
        "SC03",
        "docs/guide.md",
        "<details><summary>Answer</summary>\n\nSee <https://docs.docker.com/engine/install/>.\n"
        "Run `make replay RUN=<id>`.\n\n</details>\n\n"
        "Each line reads `ERROR <kind>\n<key>`, then the summary.\n",
        "The verdict appears after <time to verdict> minutes.\n",
        {},
        1,
    ),
    (
        "SC03",
        "docs/guide.md",
        "```bash\ngit clone https://github.com/ANI-IN/harness-engineering-session.git\n```\n",
        "```bash\ngit clone <course repository URL>\n```\n",
        {},
        2,
    ),
    (
        "SC04",
        "docs/guide.md",
        "```text\nConsole: http://127.0.0.1:8765/\n```\n",
        "Intro.\n\n```text\n\n```\n",
        {},
        3,
    ),
    (
        "SC04",
        "docs/guide.md",
        "````markdown\n```bash\nmake doctor\n```\n````\n",
        "Intro.\n\n```bash\nmake doctor\n",
        {},
        3,
    ),
    (
        "SC05",
        "docs/guide.md",
        "```python\n# platform/teamtrack/app/repositories/issues.py (lines 53-55)\n"
        "def list_all_legacy():\n    return []\n```\n",
        "```text\n# output captured in class\n```\n",
        {},
        1,
    ),
    (
        "SC05",
        "docs/guide.md",
        "```bash\n#!/usr/bin/env bash\n```\n\n```markdown\n# Title\n```\n",
        "```js\n// fill in later\n```\n",
        {},
        1,
    ),
    ("SC06", DEMO, f"{IMG}\n\n{CAPTION}\n", f"{IMG}\n\n{CAPTION}\n", {}, 1),  # missing file
    (
        "SC06",
        DEMO,
        f"{IMG}\n\n{CAPTION}\n",
        f"Text.\n\n![](expected/screen-1-minute-4.png)\n\n{CAPTION}\n",
        IMG_FILE,
        3,
    ),
    (
        "SC06",
        DEMO,
        f"{IMG}\n\n{CAPTION}\n",
        f"![Remote](https://example.com/screen.png)\n\n{CAPTION}\n",
        IMG_FILE,
        1,
    ),
    ("SC07", DEMO, f"{IMG}\n\n{CAPTION}\n", f"{IMG}\nThe next paragraph.\n", IMG_FILE, 1),
    ("SC07", DEMO, f"{IMG}\n\n{CAPTION}\n", f"{IMG}\n\n**Screen 1.**\n", IMG_FILE, 1),
    ("SC07", DEMO, f"{IMG}\n\n{CAPTION}\n", f"See this: {IMG}\n\n{CAPTION}\n", IMG_FILE, 1),
    (
        "SC08",
        "docs/guide.md",
        "No arm leaked data on this ticket ([evidence](evidence.md#section-1)).\n",
        "*Console screen 1, captured on 2026-10-17, run ab-20261017-112101-c5d839.*\n",
        {},
        1,
    ),
    (
        "SC08",
        "docs/guide.md",
        "| Run | Result |\n|---|---|\n| 2 | PASS |\n",
        "| Run | Result |\n|---|---|\n| r-20261016-181736-490aa2 | PASS |\n",
        {},
        3,
    ),
    (
        "SC09",
        "docs/guide.md",
        "Agents copy patterns ([OpenAI, Harness engineering](https://openai.com/a1)).\n",
        "Agents copy patterns that already exist (A1, F-a-20).\n",
        {},
        1,
    ),
    (
        "SC10",
        "docs/guide.md",
        "The checkpoint tag m1-s1-start marks where both arms begin.\n",
        "It runs (from `make -n show-1`, captured at commit `182d1a2`):\n",
        {},
        1,
    ),
    (
        "SC10",
        "docs/guide.md",
        "Tag the date 20261017 and the word defaced.\n",
        "```text\ncheckpoint_sha 0f3c9a1e\n```\n",
        {},
        2,
    ),
    (
        "SC11",
        "section-1-instructions/concepts.md",
        "word " * 1750 + "\n\n```mermaid\n" + "A --> B and more words here\n" * 30 + "```\n",
        "word " * 1801 + "\n",
        {},
        1,
    ),
    ("SC11", "README.md", TITLE + "\n" + "text\n" * 249, TITLE + "\n" + "text\n" * 250, {}, 1),
    (
        "SC11",
        "section-1-instructions/demo/walkthrough.md",
        "# Demo 1 walkthrough: x\n\n```python\n" + "x = 1\n" * 30 + "```\n",
        "# Demo 1 walkthrough: x\n\n```python\n" + "x = 1\n" * 41 + "```\n",
        {},
        3,
    ),
    (
        "SC12",
        "docs/guide.md",
        "| Minute | Screen | What appears |\n|---|---|---|\n| 1 | 1 | x |\n",
        "Intro.\n\n| Run | Ticket, effort | Bare arm | Harness arm | A/Bs |\n"
        "|---|---|---|---|---|\n",
        {},
        3,
    ),
    (
        "SC12",
        "docs/guide.md",
        "| A | B |\n|---|---|\n| short | `" + "c" * 90 + "` |\n",
        "| A | B |\n|---|---|\n| short | " + "word " * 20 + "|\n",
        {},
        3,
    ),
    (
        "SC13",
        DEMO,
        "> Your output will differ: run times change on every run.\n\n```text\nok\n```\n",
        "```text\nok\n```\n\nYour output will differ.\n\n```text\nok\n```\n\n"
        "*Caption.* Your results will differ.\n",
        {},
        11,
    ),
    (
        "SC13",
        DEMO,
        "> Your output will differ: run times change on every run.\n\n```text\nok\n```\n",
        "Intro.\n\n```text\nok\n```\n",
        {},
        3,
    ),
    (
        "SC14",
        "docs/guide.md",
        "On an Apple M2 Mac, install Docker Desktop first. A brief pause while the referee runs.\n",
        "This step is not a make target in this release.\n",
        {},
        1,
    ),
    (
        "SC14",
        "docs/guide.md",
        "Ask the instructor for the class date.\n",
        "Intro.\n\nThe numbers come from the M6 pilot and pilot run 3.\n",
        {},
        3,
    ),
    (
        "SC14",
        "docs/guide.md",
        "Run it on the instructor's machine.\n",
        "Run it on the class host, as the lead said.\n",
        {},
        1,
    ),
    (
        "SC15",
        DEMO,
        f"{TITLE} - Demo 1: Org-wide issue search\n",
        "# Demo 1: org-wide issue search (F1), instructions layer\n",
        {},
        1,
    ),
    ("SC15", "README.md", f"{TITLE}\n\nText.\n", f"{TITLE} - Home\n", {}, 1),
    (
        "SC15",
        "setup/pre-class.md",
        f"{TITLE} - Before class\n",
        "# Module 1 - Harness engineering\n",
        {},
        1,
    ),
    (
        "SC15",
        "docs/guide.md",
        "# Guide\n\n```markdown\n# Title in a block\n```\n",
        "# Guide\n\nText.\n\n# Second title\n",
        {},
        5,
    ),
    (
        "SC16",
        DEMO,
        demo_page(""),
        f"{TITLE} - Demo 1: x\n\n## The problem\n\n## 2. Prerequisites and dependencies\n",
        {},
        1,
    ),
    (
        "SC16",
        "section-1-instructions/assignment/README.md",
        f"{TITLE} - Assignment 1: Map\n\nTry it yourself first. The full solution is in "
        "[./solution/](solution/) with a step-by-step walkthrough.\n\n"
        "## The problem\n## What you'll build\n## Step by step\n## Grading criteria (100 points)\n"
        "## Solution walkthrough\n",
        f"{TITLE} - Assignment 1: Map\n\n## The problem\n## What you'll build\n## Step by step\n"
        "## Grading criteria (100 points)\n## Solution walkthrough\n",
        {},
        1,
    ),
    ("SC16", "docs/guide.md", "# Guide\n\n### Details\n", "# Guide\n\n#### Too deep\n", {}, 3),
    (
        "SC17",
        "section-1-instructions/README.md",
        f"{TITLE} - Section 1: Instructions\n\n## The problem\n\n> **Terms on this page**\n>\n"
        "> - **Harness**: the files.\n\n"
        "**Illustrative scenario.** You ask an agent to add search.\n",
        f"{TITLE} - Section 1: Instructions\n\n## The problem\n\n"
        "Our agent leaked data in 3 runs out of 10.\n",
        {},
        5,
    ),
    (
        "SC17",
        "section-1-instructions/README.md",
        f"{TITLE} - Section 1: Instructions\n\n## The problem\n\n"
        "**Illustrative scenario.** You ask an agent to add search.\n",
        f"{TITLE} - Section 1: Instructions\n\n## The problem\n\n"
        "**Illustrative scenario.** You ask an agent for 3 endpoints.\n",
        {},
        5,
    ),
    (
        "SC18",
        "docs/guide.md",
        "> **Terms on this page**\n>\n> - **Harness**: the files.\n> - **Bare arm**: no harness.\n"
        "> - **Harness arm**: the harness on.\n> - **Referee**: scores each run.\n",
        "> **Terms on this page**\n>\n> - **Harness**: the files.\n\nText.\n\n"
        "> **Terms on this page**\n>\n> - **Referee**: scores.\n",
        {},
        7,
    ),
    (
        "SC18",
        "docs/guide.md",
        "> **Terms on this page**\n>\n> - **Referee**: scores each run.\n",
        "> **Terms on this page**\n>\n> - **Referee**: scores.\n> - **referee**: again.\n",
        {},
        4,
    ),
    (
        "SC21",
        "docs/guide.md",
        "Hand in Assignment 2: State and sessions by Friday; the package is `a2_state`.\n",
        "Text.\n\nHand in A2 by Friday.\n",
        {},
        3,
    ),
    (
        "SC21",
        "docs/guide.md",
        "Run `make demo-3 FEATURE=version-checks`; the screen shows `F4` and `S4:gate`.\n",
        "Text.\n\nThe agent breaks R8 while it builds F4 in S3 (B11).\n",
        {},
        3,
    ),
    (
        "SC22",
        "docs/guide.md",
        "Feature 4: Version checks on issue edits adds a version. Feature 4 then ships.\n",
        "Text.\n\nFeature 4 adds a version column.\n",
        {},
        3,
    ),
    (
        "SC22",
        "docs/guide.md",
        "In [Section 3: Scope and sandbox](s3.md), House rule 1: Tenant\nisolation holds.\n",
        "Text.\n\nHouse rule 1: tenant isolation holds; Section 3 adds scope.\n",
        {},
        3,
    ),
    (
        "SC23",
        "docs/guide.md",
        f"Keep tests that pass five runs ([TestGen-LLM]({TG})).\n\n## Sources\n\n"
        "- Source 1: Automated Unit Test Improvement using Large Language Models at Meta, "
        f"<{TG}>, Nadia Alshahwan and others (Meta), 2024-02-14\n",
        "Text.\n\nKeep tests that pass five runs (TestGen-LLM).\n",
        {},
        3,
    ),
    (
        "SC23",
        "docs/guide.md",
        "Text.\n",
        "Text.\n\nSource 2 says so.\n",
        {},
        3,
    ),
    (
        "SC24",
        "docs/guide.md",
        "Read [the guide](guide.md) and [OpenAI](https://openai.com/).\n",
        "Text.\n\nRead [the guide]() and [link].\n",
        {},
        3,
    ),
    (
        "SC24",
        "docs/guide.md",
        f"See [the paper]({TG}).\n",
        "Text.\n\nSee [the paper](htps//arxiv.org/abs/2402.09171).\n",
        {},
        3,
    ),
    (
        "SC25",
        "docs/guide.md",
        "Text.\n",
        "Text.\n\nSee [SpecBench](https://arxiv.org/abs/2605.21384).\n",
        {},
        3,
    ),
    (
        "SC25",
        "docs/guide.md",
        "Text ([SpecBench](https://arxiv.org/abs/2605.21384)).\n\n## Sources\n\n"
        "- Source 1: SpecBench, <https://arxiv.org/abs/2605.21384>, WecoAI, 2026-05\n",
        "Text ([SpecBench](https://arxiv.org/abs/2605.21384)).\n\n## Sources\n\n"
        "- [SpecBench](https://arxiv.org/abs/2605.21384)\n",
        {},
        5,
    ),
]


@pytest.mark.parametrize(
    ("check", "rel", "passing", "failing", "extra", "line"),
    CASES,
    ids=[f"{c[0]}-{i}" for i, c in enumerate(CASES)],
)
def test_check_pass_and_fail(
    tmp_path: Path, check: str, rel: str, passing: str, failing: str, extra: dict, line: int
) -> None:
    good = tmp_path / "good"
    bad = tmp_path / "bad"
    passing_extra = IMG_FILE if check in ("SC06", "SC07") else extra
    found = [p for p in problems(good, rel, passing, passing_extra) if p.check == check]
    assert found == [], found
    found = [p for p in problems(bad, rel, failing, extra) if p.check == check]
    assert found, f"{check} did not fire"
    assert line in [p.line for p in found], found


def test_every_check_has_a_passing_and_a_failing_case() -> None:
    covered = {c[0] for c in CASES}
    assert covered == {f"SC{n:02d}" for n in [*range(1, 19), *range(21, 26)]}


def test_severities_follow_the_first_version() -> None:
    errors = {"SC00", "SC01", "SC02", "SC03", "SC04", "SC05", "SC06", "SC07", "SC08", "SC09"}
    errors |= {"SC10", "SC12", "SC13", "SC14", "SC15", "SC19", "SC20", "SC21", "SC22"}
    errors |= {"SC23", "SC24", "SC25"}
    warnings = {"SC11", "SC16", "SC17", "SC18"}
    for check, (_, severity) in cs.CHECKS.items():
        assert severity == ("error" if check in errors else "warning"), check
    assert set(cs.CHECKS) == errors | warnings


def test_long_table_cells_missing_output_note_and_scenario_digits_only_warn(tmp_path: Path) -> None:
    found = problems(tmp_path, "docs/guide.md", "| A | B |\n|---|---|\n| a | " + "w " * 50 + "|\n")
    assert [(p.check, p.severity) for p in found] == [("SC12", "warning")]
    found = problems(tmp_path, DEMO, demo_page("```text\nok\n```\n"))
    assert ("SC13", "warning") in {(p.check, p.severity) for p in found}
    assert not [p for p in found if p.severity == "error"], found
    scenario = "## The problem\n\n**Illustrative scenario.** You ask for 3 endpoints.\n"
    found = problems(
        tmp_path,
        "section-1-instructions/README.md",
        f"{TITLE} - Section 1: Instructions\n\n{scenario}",
    )
    assert ("SC17", "warning") in {(p.check, p.severity) for p in found}
    assert not [p for p in found if p.severity == "error"], found


def test_is_public() -> None:
    public = [
        "README.md",
        "setup/windows.md",
        "setup/pre-class.md",
        "section-1-instructions/concepts.md",
        "section-1-instructions/assignment/solution/SOLUTION.md",
        "section-4-verification/assignment/starter/README.md",
        "final-project/README.md",
        "use-in-your-repo/skills/house-rules/SKILL.md",
        "docs/instructor-guide.md",
        "docs/STYLE.md",
        "slides/README.md",
        "slides/deck.md",
        "section-4-verification/assignment/solution/portfolio/case-study.md",
    ]
    private = [
        GRADER_MD,
        HIDDEN_MD,
        "slides/img/notes.md",
        "slides/outline.md",
        "CHANGELOG.md",
        "docs/CHANGELOG.md",
        "platform/sandbox/README.md",
        "notes.md",
        "05x-extra/README.md",
    ]
    for rel in public:
        assert cs.is_public(rel), rel
    for rel in private:
        assert not cs.is_public(rel), rel


def test_section_folders_are_named_section_n() -> None:
    # The section folders are section-1-instructions to section-4-verification. Folders with the
    # old two-digit prefix are no longer section folders: their pages are not public course files.
    for name in (
        "section-1-instructions",
        "section-2-state-lifecycle",
        "section-3-scope-sandbox",
        "section-4-verification",
    ):
        assert re.fullmatch(cs._SECTION, name), name
        assert cs.is_public(f"{name}/README.md"), name
        assert cs.doc_type(f"{name}/concepts.md") == "concepts", name
    for name in ("01-intro", "04-checks", "section-x", "section-1"):
        assert not re.fullmatch(cs._SECTION, name), name
    assert not cs.is_public("01-intro/README.md")


def test_doc_type() -> None:
    table = {
        "README.md": "root-readme",
        "section-1-instructions/README.md": "section-readme",
        "section-1-instructions/concepts.md": "concepts",
        "section-1-instructions/demo/README.md": "demo-readme",
        "section-1-instructions/demo/walkthrough.md": "walkthrough",
        "section-1-instructions/assignment/README.md": "assignment-readme",
        "section-1-instructions/assignment/SPEC.md": "spec",
        "section-1-instructions/assignment/solution/SOLUTION.md": "solution",
        "section-1-instructions/post-class-reading/README.md": "reading-index",
        "section-1-instructions/post-class-reading/01-map-not-manual.md": "reading",
        "section-1-instructions/session-notes.md": "session-notes",
        "setup/README.md": "setup-index",
        "setup/windows.md": "setup-os",
        "setup/macos.md": "setup-os",
        "setup/linux.md": "setup-os",
        "docs/instructor-guide.md": "instructor-guide",
        "docs/reference.md": "reference",
        "docs/evidence.md": "other",  # the index of the evidence pages
        "docs/evidence/s1.md": "evidence",
        "docs/evidence/final.md": "evidence",
        "docs/evidence/general.md": "evidence",
        "final-project/README.md": "final-project",
        "use-in-your-repo/README.md": "section-readme",
        "docs/troubleshooting.md": "other",
        "setup/pre-class.md": "other",
    }
    for rel, kind in table.items():
        assert cs.doc_type(rel) == kind, rel


def test_agent_files() -> None:
    agent = [
        "section-1-instructions/demo/harness/AGENTS.md",
        "section-1-instructions/assignment/starter/instructions/AGENTS.md",
        "section-1-instructions/assignment/solution/work/instructions/AGENTS.md",
        "use-in-your-repo/kit/templates/AGENTS.md",
        "use-in-your-repo/kit/examples/boltons-queueutils/filled/progress.md",
        "use-in-your-repo/skills/house-rules/SKILL.md",
        "section-1-instructions/assignment/starter/original/AGENTS.md",
        "section-1-instructions/assignment/solution/work/instructions/.agents/skills/a/SKILL.md",
        "section-4-verification/assignment/solution/skill/testgen-evidence/SKILL.md",
        "final-project/harness/AGENTS.md",
        "final-project/harness/docs/exec-plans/active/F5.md",
    ]
    course = [
        "final-project/harness/README.md",
        "final-project/README.md",
        "final-project/your-repo/README.md",
        "section-1-instructions/assignment/starter/README.md",
        "section-1-instructions/assignment/solution/README.md",
        "section-1-instructions/assignment/solution/SOLUTION.md",
        "section-1-instructions/assignment/solution/work/ab-report.md",
        "section-1-instructions/assignment/solution/work/live/README.md",
        "section-2-state-lifecycle/assignment/solution/live/README.md",
        "section-4-verification/assignment/solution/live/README.md",
        "section-4-verification/assignment/solution/portfolio/case-study.md",
        "section-4-verification/assignment/starter/portfolio/langsmith.md",
        "use-in-your-repo/kit/README.md",
        "use-in-your-repo/README.md",
        "slides/deck.md",
    ]
    for rel in agent:
        assert cs.is_agent_file(rel), rel
    for rel in course:
        assert not cs.is_agent_file(rel), rel


def test_agent_files_get_only_the_image_checks(tmp_path: Path) -> None:
    rel = "section-1-instructions/demo/harness/AGENTS.md"
    text = "# Map\n\nTODO <placeholder> ab-20261017-112101-c5d839\n\n# Second\n"
    assert problems(tmp_path, rel, text) == []
    found = problems(tmp_path, rel, text + "\n![Board](missing.png)\n")
    assert [p.check for p in found] == ["SC06"]


EVIDENCE_TEXT = (
    "Run ab-20261017-112101-c5d839 passed.\n\nFinding F-a-20 says so.\n\n"
    "Captured at commit `182d1a2`.\n\nThe pilot run 3 numbers.\n"
)


@pytest.mark.parametrize(
    "rel",
    [
        "docs/evidence.md",
        "docs/evidence/s1.md",
        "docs/evidence/s4.md",
        "docs/evidence/final.md",
        "docs/evidence/general.md",
    ],
)
def test_evidence_pages_are_exempt(tmp_path: Path, rel: str) -> None:
    found = problems(tmp_path, rel, EVIDENCE_TEXT)
    assert not [p for p in found if p.check in ("SC08", "SC09", "SC10", "SC14")], found


@pytest.mark.parametrize("rel", ["docs/reference.md", "docs/evidence-notes.md", "docs/x/s1.md"])
def test_ids_outside_the_evidence_pages_fail(tmp_path: Path, rel: str) -> None:
    found = problems(tmp_path, rel, EVIDENCE_TEXT)
    assert sorted(p.check for p in found if p.check != "SC16") == ["SC08", "SC09", "SC10", "SC14"]


def test_style_guide_is_exempt_from_the_quoting_checks(tmp_path: Path) -> None:
    text = "# Course style guide\n\nDo not write TODO, a finding id, or the class host.\n"
    assert problems(tmp_path, "docs/STYLE.md", text) == []


def test_private_files_skipped(tmp_path: Path) -> None:
    write(tmp_path, "CHANGELOG.md", "Run ab-20261017-112101-c5d839, TODO.\n")
    write(tmp_path, GRADER_MD, "TODO\n")
    assert cs.check_paths(tmp_path, ["CHANGELOG.md", GRADER_MD]) == []
    done = run_cli(tmp_path, "CHANGELOG.md")
    assert done.returncode == 0
    assert "- CHANGELOG.md: skipped (not a public course file)" in done.stdout


def test_default_targets(tmp_path: Path) -> None:
    every = ["README.md", "setup/linux.md", "section-1-instructions/concepts.md", "docs/a.md"]
    every += ["slides/README.md", "slides/deck.md", "docs/CHANGELOG.md", GRADER_MD]
    every += ["platform/x.md", "final-project/README.md", "use-in-your-repo/README.md"]
    every += ["slides/module1-slides.md", "use-in-your-repo/skills/s/scripts/assess.py"]
    every += ["use-in-your-repo/kit/templates/init.sh", "section-1-instructions/demo/run.sh"]
    for rel in every:
        write(tmp_path, rel, "Text.\n")
    files = [p.relative_to(tmp_path).as_posix() for p in cs.default_files(tmp_path)]
    assert sorted(files) == sorted(
        [
            "README.md",
            "setup/linux.md",
            "section-1-instructions/concepts.md",
            "docs/a.md",
            "slides/README.md",
            "slides/deck.md",
            "slides/module1-slides.md",
            "final-project/README.md",
            "use-in-your-repo/README.md",
            "use-in-your-repo/skills/s/scripts/assess.py",
            "use-in-your-repo/kit/templates/init.sh",
        ]
    )


def test_fence_parser() -> None:
    page = cs.parse_page(
        "Intro.\n\n````markdown\n```bash\nmake doctor\n```\n````\n\n"
        "~~~text\nok\n~~~\n\n```bash\nopen\n"
    )
    fences = page.fences
    assert [(f.start, f.end, f.lang) for f in fences] == [(3, 7, "markdown"), (9, 11, "text"),
                                                          (13, None, "bash")]  # fmt: skip
    assert [ln.text for ln in fences[0].content] == ["```bash", "make doctor", "```"]
    kinds = [ln.kind for ln in page.lines]
    assert kinds[0] == "prose" and kinds[3] == "code" and kinds[13] == "code"
    found = cs.check_text("docs/a.md", "```bash\nopen\n", Path("/nonexistent"))
    assert [(p.check, p.line) for p in found] == [("SC04", 1)]


def test_comment_lines_are_not_prose() -> None:
    page = cs.parse_page("<!--\nhidden <x>\n-->\nText <!-- note --> after.\n")
    assert [ln.kind for ln in page.lines] == ["comment", "comment", "comment", "prose"]
    assert page.lines[3].prose == "Text  after."


def test_word_count() -> None:
    text = (
        "# Title words\n\nOne two [three](https://example.com/a/very/long/path) four.\n\n"
        "```python\nnot counted at all\n```\n\n```mermaid\nA --> B\n```\n\n"
        "<!-- hidden words here -->\n\n![Alt text words](img.png)\n\n| Five | six |\n"
    )
    assert cs.count_words(cs.parse_page(text)) == 8


def test_concepts_length_counts_table_cells(tmp_path: Path) -> None:
    rel = "section-1-instructions/concepts.md"
    prose = "word " * 1750 + "\n"
    table = "\n| Step | Result |\n|---|---|\n" + "| one two three | four five six |\n" * 20
    assert not [p for p in problems(tmp_path, rel, prose) if p.check == "SC11"]
    found = [p for p in problems(tmp_path, rel, prose + table) if p.check == "SC11"]
    assert [(p.line, p.message) for p in found] == [(1, "1872 prose words, limit about 1800")]


def test_allow_marker(tmp_path: Path) -> None:
    line = "Run ab-20261017-112101-c5d839 <!-- check-style: allow SC08 quoted output -->\n"
    assert problems(tmp_path, "docs/a.md", line) == []
    found = problems(tmp_path, "docs/a.md", line.replace(" quoted output", ""))
    assert {p.check for p in found} == {"SC00"}


def test_templates_match_style_guide() -> None:
    text = (REPO / "docs" / "STYLE.md").read_text(encoding="utf-8")
    skeletons: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        match = re.match(r"^```markdown skeleton:([a-z-]+)\s*$", line)
        if match:
            current = match.group(1)
            skeletons[current] = []
        elif current and line.startswith("```"):
            current = None
        elif current and line.startswith("## "):
            skeletons[current].append(line[3:].strip())
    assert skeletons == cs.TEMPLATES


def test_style_guide_passes_its_own_checks() -> None:
    found = cs.check_paths(REPO, ["docs/STYLE.md"])
    assert not [p for p in found if p.severity == "error"], found


def run_cli(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli(tmp_path: Path) -> None:
    write(
        tmp_path,
        "section-1-instructions/session-notes.md",
        "# Section 1: Instructions, session notes\n\nText.\n",
    )
    done = run_cli(tmp_path, "section-1-instructions/session-notes.md")
    assert done.returncode == 0, done.stdout
    assert re.search(r"^! section-1-instructions/session-notes\.md:1: SC16 ", done.stdout, re.M)
    assert done.stdout.splitlines()[-1] == "1 files checked, 0 errors, 1 warnings, 0 allowed lines"
    assert run_cli(tmp_path, "--strict", "section-1-instructions/session-notes.md").returncode == 1

    write(tmp_path, "docs/a.md", "TODO: finish\n")
    done = run_cli(tmp_path, "docs/a.md")
    assert done.returncode == 1
    assert "x docs/a.md:1: SC01 " in done.stdout
    assert run_cli(tmp_path, "--warn-only", "docs/a.md").returncode == 0

    listed = run_cli(tmp_path, "--list-checks")
    assert listed.returncode == 0
    rows = [ln for ln in listed.stdout.splitlines() if re.match(r"^SC\d\d ", ln)]
    assert len(rows) == len(cs.CHECKS) == 26

    assert run_cli(tmp_path, "docs/missing.md").returncode == 2


def test_ci_runs_the_style_check_strictly() -> None:
    ci = (REPO / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    lint_job = ci.split("\n  lint:\n", 1)[1].split("\n  fast:\n", 1)[0]
    assert "uv run python platform/scripts/check_style.py --strict" in lint_job


def test_every_public_page_passes_the_style_check_strictly() -> None:
    found = cs.check_paths(REPO, [])
    assert [f"{p.path}:{p.line}: {p.check} {p.message}" for p in found] == []


def test_numbered_starter_gaps_are_not_leftover_markers(tmp_path: Path) -> None:
    # A2's starter code marks the gaps learners fill as TODO 1 to TODO 7; pages name them.
    text = "# Module 1: Harness Engineering for Coding Agents - X\n\nFill TODO 1a, then TODO 6.\n"
    text += "The summary lists open TODO markers.\nA real TODO here.\n"
    found = [p for p in problems(tmp_path, "docs/a.md", text) if p.check == "SC01"]
    assert [p.line for p in found] == [5]


def test_a_marker_on_its_own_line_covers_the_code_block_after_it(tmp_path: Path) -> None:
    text = (
        "# Module 1: Harness Engineering for Coding Agents - X\n\n"
        "<!-- check-style: allow SC10 the ledger format names the commit -->\n"
        "```text\n- [x] S1 Comments table: done in commit 615f2d2\n```\n\n"
        "Then commit 615f2d2 again.\n"
    )
    found = [p for p in problems(tmp_path, "docs/a.md", text) if p.check == "SC10"]
    assert [p.line for p in found] == [8]


def test_screenshots_next_to_an_expected_page_count_as_captured_output(tmp_path: Path) -> None:
    extra = {"section-1-instructions/demo/expected/shot.png": PNG}
    text = (
        "# Module 1: Harness Engineering for Coding Agents - Demo 1: One run\n\n"
        "> Your output will differ: run times, ids, and the agent's wording change on every"
        " run.\n\n"
        "![Console screen 1 at minute 4](shot.png)\n\n*Console screen 1 at minute 4.*\n"
    )
    found = problems(tmp_path, "section-1-instructions/demo/expected/README.md", text, extra)
    assert [p for p in found if p.check == "SC13"] == []


def test_the_final_project_page_follows_the_demo_template_plus_the_take_home_step() -> None:
    assert cs.TEMPLATES["final-project"] == cs.TEMPLATES["demo-readme"] + [
        "Use it on your own repository"
    ]
    assert cs.doc_type("final-project/README.md") == "final-project"


def test_the_generated_references_page_is_not_checked() -> None:
    # The release build writes docs/REFERENCES.md into the public repo: every source and finding id.
    assert not cs.is_public("docs/REFERENCES.md")


def test_the_root_readme_tells_its_story_without_the_scenario_label(tmp_path: Path) -> None:
    # Owner edit on the RC, 2026-10-18: the root README's problem story has no label.
    text = (
        "# Module 1: Harness Engineering for Coding Agents\n\n## The problem\n\n"
        "Your team gives a week of tickets to a coding agent.\n"
    )
    assert [p for p in problems(tmp_path, "README.md", text) if p.check == "SC17"] == []
    found = problems(
        tmp_path, "section-1-instructions/README.md", text.replace("# Module", "# Module", 1)
    )
    assert [p.check for p in found if p.check == "SC17"] == ["SC17"]


# -- every Markdown page, internal phrases, folders, images, diagram sources -------------------


def test_solution_pages_get_every_check(tmp_path: Path) -> None:
    rel = "section-4-verification/assignment/solution/portfolio/case-study.md"
    found = problems(tmp_path, rel, "# Case study\n\nRun ab-20261017-112101-c5d839 passed.\n")
    assert "SC08" in {p.check for p in found}


def test_the_slide_deck_is_checked(tmp_path: Path) -> None:
    found = problems(tmp_path, "slides/deck.md", "## 1. Opening\n\nFinding F-a-20 says so.\n")
    assert "SC09" in {p.check for p in found}


@pytest.mark.parametrize(
    "text",
    [
        "Follow the owner's instructions.",
        "That is outside owner scope.",
        "Then switch back to the build branch.",
        "It lives in the build repository.",
        "Run it on the class host.",
        "The live run is not part of this release.",
    ],
)
def test_internal_phrases_are_banned(tmp_path: Path, text: str) -> None:
    found = problems(tmp_path, "docs/guide.md", text + "\n")
    assert [p.check for p in found if p.check == "SC14"] == ["SC14"], found


def test_the_teamtrack_owner_role_is_not_an_internal_phrase(tmp_path: Path) -> None:
    text = (
        "A project owner's token may archive it, and the owner's role is checked by R2.\n"
        "Each rule file has an owner. The handoff has two owners.\n"
    )
    assert [p for p in problems(tmp_path, "docs/guide.md", text) if p.check == "SC14"] == []


SVG = b'<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>'


def test_svg_images_on_relative_paths_must_exist(tmp_path: Path) -> None:
    rel = "section-1-instructions/demo/README.md"
    body = "![The flow of one run](../diagrams/flow.svg)\n\n*The flow of one run.*\n"
    found = [p for p in problems(tmp_path / "bad", rel, demo_page(body)) if p.check == "SC06"]
    assert found and "does not exist" in found[0].message
    svg = {"section-1-instructions/diagrams/flow.svg": SVG}
    found = problems(tmp_path / "good", rel, demo_page(body), svg)
    assert [p for p in found if p.check == "SC06"] == []
    empty = {"section-1-instructions/diagrams/flow.svg": b""}
    found = problems(tmp_path / "empty", rel, demo_page(body), empty)
    assert [p.message for p in found if p.check == "SC06"] == [
        "image file ../diagrams/flow.svg is empty"
    ]


SECTION = "section-1-instructions"
SECTION_FILES = [
    "README.md",
    "concepts.md",
    "session-notes.md",
    "demo/README.md",
    "demo/run.sh",
    "demo/walkthrough.md",
    "demo/harness/AGENTS.md",
    "demo/expected/terminal.txt",
    "assignment/README.md",
    "assignment/SPEC.md",
    "assignment/starter/README.md",
    "assignment/solution/SOLUTION.md",
    "post-class-reading/README.md",
]
SECTION_ITEMS = [
    "README.md",
    "concepts.md",
    "session-notes.md",
    "demo/README.md",
    "demo/run.sh",
    "demo/walkthrough.md",
    "demo/harness/",
    "demo/expected/",
    "assignment/README.md",
    "assignment/SPEC.md",
    "assignment/starter/",
    "assignment/solution/SOLUTION.md",
    "post-class-reading/",
]


def make_section(root: Path, skip: str = "") -> None:
    for rel in SECTION_FILES:
        if not skip or not (rel == skip or (skip.endswith("/") and rel.startswith(skip))):
            write(root, f"{SECTION}/{rel}", "x\n")


def folder_findings(found: list) -> list[tuple[str, str]]:
    return [(p.path, p.check) for p in found]


def test_a_complete_section_folder_passes(tmp_path: Path) -> None:
    make_section(tmp_path)
    assert cs.section_problems(tmp_path) == []


@pytest.mark.parametrize("missing", SECTION_ITEMS)
def test_a_section_folder_missing_an_item_fails(tmp_path: Path, missing: str) -> None:
    make_section(tmp_path, skip=missing)
    found = cs.section_problems(tmp_path)
    assert folder_findings(found) == [(f"{SECTION}/{missing}", "SC19")]
    assert found[0].severity == "error"


def test_a_diagrams_folder_needs_its_readme(tmp_path: Path) -> None:
    make_section(tmp_path)
    write_bytes(tmp_path, f"{SECTION}/diagrams/flow.svg", SVG)
    write(tmp_path, f"{SECTION}/diagrams/flow.excalidraw", "{}\n")
    found = cs.section_problems(tmp_path)
    assert folder_findings(found) == [(f"{SECTION}/diagrams/README.md", "SC19")]
    write(tmp_path, f"{SECTION}/diagrams/README.md", "x\n")
    assert cs.section_problems(tmp_path) == []


FINAL_FILES = [
    "README.md",
    "run.sh",
    "tasks/F5.md",
    "harness/AGENTS.md",
    "walkthrough.md",
    "expected/terminal.txt",
    "your-repo/README.md",
    "CHECKLIST.md",
]


@pytest.mark.parametrize(
    "missing", ["", "run.sh", "tasks/F5.md", "your-repo/README.md", "CHECKLIST.md"]
)
def test_the_final_project_folder_rule(tmp_path: Path, missing: str) -> None:
    for rel in FINAL_FILES:
        if rel != missing:
            write(tmp_path, f"final-project/{rel}", "x\n")
    found = cs.final_project_problems(tmp_path)
    if not missing:
        assert found == []
    else:
        item = missing.split("/")[0] + ("/" if "/" in missing else "")
        assert folder_findings(found) == [(f"final-project/{item}", "SC19")]


def test_every_diagram_needs_an_excalidraw_source(tmp_path: Path) -> None:
    write_bytes(tmp_path, "section-2-state-lifecycle/diagrams/handoff.png", PNG)
    write_bytes(tmp_path, "docs/diagrams/architecture.svg", SVG)
    write(tmp_path, "docs/diagrams/architecture.excalidraw", "{}\n")
    write_bytes(tmp_path, "docs/images/screen-1.png", PNG)  # a screenshot, not a diagram
    found = cs.diagram_problems(tmp_path)
    assert folder_findings(found) == [("section-2-state-lifecycle/diagrams/handoff.png", "SC20")]
    assert "handoff.excalidraw" in found[0].message


def test_the_default_run_adds_the_folder_checks_and_named_paths_do_not(tmp_path: Path) -> None:
    make_section(tmp_path, skip="concepts.md")
    write_bytes(tmp_path, f"{SECTION}/diagrams/flow.png", PNG)
    found = folder_findings(cs.run(tmp_path, []).problems)
    assert (f"{SECTION}/concepts.md", "SC19") in found
    assert (f"{SECTION}/diagrams/flow.png", "SC20") in found
    assert ("final-project/README.md", "SC19") in found
    named = folder_findings(cs.run(tmp_path, [f"{SECTION}/README.md"]).problems)
    assert not [f for f in named if f[1] in ("SC19", "SC20")]
    assert not [f for f in folder_findings(cs.check_paths(tmp_path, [])) if f[1] == "SC19"]


def test_every_section_folder_in_the_repo_is_complete() -> None:
    assert cs.section_problems(REPO) == []


def test_every_diagram_in_the_repo_has_its_source() -> None:
    assert cs.diagram_problems(REPO) == []


def test_the_final_project_folder_in_the_repo_is_complete() -> None:
    assert cs.final_project_problems(REPO) == []


def test_starter_fill_in_templates_keep_their_markers(tmp_path: Path) -> None:
    text = "# Case study: <title>\n\nTODO: one paragraph.\n\nRun ab-20261017-112101-c5d839.\n"
    rel = "section-4-verification/assignment/starter/portfolio/case-study.md"
    assert {p.check for p in problems(tmp_path, rel, text)} == {"SC08"}
    readme = "section-4-verification/assignment/starter/README.md"
    assert "SC01" in {p.check for p in problems(tmp_path, readme, text)}


# -- labels: source, assignment, finding, and section ids (SC09, SC21, SC22) ----------------------

LABELS = "Agents copy patterns (A1, F-a-20); in S1 they read the map.\n"


def label_checks(found) -> list[str]:
    return sorted(p.check for p in found if p.check in ("SC08", "SC09", "SC21"))


def test_finding_ids_with_any_number_of_digits_fail(tmp_path: Path) -> None:
    found = problems(tmp_path, "docs/guide.md", "Finding F-b-5 says so.\n")
    assert label_checks(found) == ["SC09"]


@pytest.mark.parametrize(
    "text",
    [
        "Run the A/B, then open `a2_state/layer.py`.\n",
        "Fill the stubs `TODO(A1-3)` and `TODO(A4-1)`.\n",
        "```bash\nuv run python -m a4_verification.run_r8 --feature A4\n```\n",
        "Part A1 parses the diff; Part A2 checks it.\n",
        "Task `F1-trap` and file f1.md; requirement R-S1; anchor S4:gate.\n",
        "Show anchor S4:gate, then `S1:prefix`.\n",
        "A B2B tool on a Mac M1, page A11y.\n",
        "Requirements R-S1 to R-S4 cover the skill.\n",
    ],
)
def test_identifiers_are_not_labels(tmp_path: Path, text: str) -> None:
    assert label_checks(problems(tmp_path, "docs/guide.md", text)) == []


def test_ids_in_html_comments_fail(tmp_path: Path) -> None:
    found = problems(tmp_path, "docs/guide.md", "Text.\n<!-- from A2 (F-a-08), see S2 -->\n")
    assert label_checks(found) == ["SC09", "SC21", "SC21"]


@pytest.mark.parametrize(
    "rel",
    [
        "use-in-your-repo/skills/house-rules/SKILL.md",
        "use-in-your-repo/skills/harness-setup/references/state.md",
        "use-in-your-repo/skills/harness-setup/assets/templates/progress.md",
        "use-in-your-repo/kit/templates/progress.md",
    ],
)
def test_skills_and_kit_templates_carry_no_ids(tmp_path: Path, rel: str) -> None:
    text = "# Progress\n\n<!-- golden principles (A1) -->\n" + LABELS
    text += "Run ab-20261017-112101-c5d839.\n"
    assert cs.is_agent_file(rel)
    found = problems(tmp_path, rel, text)
    assert label_checks(found) == ["SC08", "SC09", "SC21", "SC21", "SC21"]


def test_assignment_1_instruction_trees_get_only_the_finding_id_check(tmp_path: Path) -> None:
    # The AGENTS.md files a learner writes for Assignment 1: a grader reads their wording.
    rel = "section-1-instructions/assignment/solution/work/instructions/AGENTS.md"
    found = problems(tmp_path, rel, LABELS)
    assert label_checks(found) == ["SC09"]


@pytest.mark.parametrize(
    "rel",
    [
        "section-2-state-lifecycle/demo/harness/progress.md",
        "section-1-instructions/demo/harness/AGENTS.md",
        "final-project/harness/AGENTS.md",
    ],
)
def test_the_shipped_harness_docs_get_the_label_rules(tmp_path: Path, rel: str) -> None:
    # Option B (2026-10-18): the TeamTrack harness carries the course's names, so its copies do.
    found = problems(tmp_path, rel, LABELS)
    assert label_checks(found) == ["SC09", "SC21", "SC21"]


def test_scripts_and_shell_templates_in_skills_and_kit_carry_no_ids(tmp_path: Path) -> None:
    script = "use-in-your-repo/skills/harness-setup/scripts/assess.py"
    text = 'CHECK = Check("S1", "State", "t", "fail", "e", "f", "A2 (F-a-50)")\n'
    found = problems(tmp_path, script, text)
    assert label_checks(found) == ["SC09", "SC21"]  # "S1" is a check id in code
    ok = 'CHECK = Check("S1", "State", "t", "fail", "e", "f", "Anthropic, Effective harnesses")\n'
    assert problems(tmp_path / "ok", script, ok) == []
    shell = "use-in-your-repo/kit/templates/init.sh"
    assert label_checks(problems(tmp_path, shell, "#!/bin/sh\n# Source: A2\n")) == ["SC21"]
    write(tmp_path, "platform/x.py", "A1 = 1\n")
    assert cs.check_paths(tmp_path, ["platform/x.py"]) == []


@pytest.mark.parametrize("rel", ["docs/evidence.md", "docs/evidence/s1.md"])
def test_evidence_pages_keep_every_label(tmp_path: Path, rel: str) -> None:
    assert label_checks(problems(tmp_path, rel, LABELS)) == []


def test_the_working_slide_file_is_checked_for_labels_only(tmp_path: Path) -> None:
    rel = "slides/module1-slides.md"
    assert cs.is_public(rel)
    found = problems(tmp_path, rel, "## 1. Opening\n\nTODO " + LABELS)
    assert sorted(p.check for p in found) == ["SC09", "SC21", "SC21"]


# -- names, links, and sources (SC21 to SC25) ------------------------------------------------------


def plain_checks(found) -> list[str]:
    return sorted(p.check for p in found if p.check in ("SC21", "SC22", "SC23", "SC24", "SC25"))


def test_the_names_match_the_platform_names() -> None:
    from shipharness.datasets.names import (
        ASSIGNMENT_NAMES,
        FEATURE_NAMES,
        FILTER_NAMES,
        RULE_NAMES,
        SECTION_NAMES,
    )

    assert cs.NAMES["Feature"] == {int(k[1:]): v for k, v in FEATURE_NAMES.items()}
    assert cs.NAMES["House rule"] == {int(k[1:]): v for k, v in RULE_NAMES.items()}
    assert cs.NAMES["Section"] == SECTION_NAMES
    assert cs.NAMES["Assignment"] == ASSIGNMENT_NAMES
    assert cs.NAMES["Filter"] == FILTER_NAMES


@pytest.mark.parametrize(
    "text",
    [
        "Run `make final FEATURES=watchers,bulk-close`.\n",
        "```bash\nmake demo-3 FEATURE=F4\n```\n",
        "Open [f5-bulk-close.md](tasks/f5-bulk-close.md) for `F5`.\n",
        "Requirements R-S1 and R-L5, task `F1-trap`, file f1.md, Apple M1.\n",
        "The Section 4: Verification poll, Assignment 2: State and sessions, and the F-key.\n",
        "Sections 1 to 4 and Features 5 to 7 are plural; Section 12 is not one of ours.\n",
    ],
)
def test_identifiers_are_not_bare_codes(tmp_path: Path, text: str) -> None:
    assert plain_checks(problems(tmp_path, "docs/guide.md", text)) == []


@pytest.mark.parametrize(
    "text",
    [
        "Pick F5, F6, or F7.\n",
        "| R1 Tenant isolation | 404 |\n",
        "Clauses R1.1 to R1.6 hold.\n",
        "Features F1-F4 have a measure.\n",
        "<!-- F4 is the confirmation -->\nText.\n",
        "House rule R8 hides deleted issues.\n",
        "In S2 the agent resumes.\n",
        "The source B11 says so.\n",
    ],
)
def test_bare_codes_fail(tmp_path: Path, text: str) -> None:
    assert "SC21" in plain_checks(problems(tmp_path, "docs/guide.md", text))


def test_an_allow_marker_keeps_a_code_a_checker_reads(tmp_path: Path) -> None:
    text = (
        "| R1: runs | 0/3 | 1/3 | <!-- check-style: allow SC21 the Section 1 checker reads it -->\n"
    )
    found = problems(tmp_path, "docs/guide.md", text)
    assert [p for p in found if p.check == "SC21"] == []


@pytest.mark.parametrize(
    ("text", "ok"),
    [
        ("House rule 1: Tenant isolation, then House rule 1 again.\n", True),
        ("**Filter 2: Passes five runs** re-runs each test; Filter 2 drops flaky ones.\n", True),
        ("| Feature 7: Labels | final |\n|---|---|\n| Feature 7 | again |\n", True),
        ("Feature 3: Safe retries for issue creation.\n", True),
        ("Feature 3: Idempotent issue creation.\n", False),
        ("Feature 7: Labelsx.\n", False),
        ("See house rule 4 first.\n", False),
        ("Filter 6 drops duplicates.\n", False),
        ("Assignment 4 adds a rule.\n", False),
    ],
)
def test_the_first_mention_is_the_full_name(tmp_path: Path, text: str, ok: bool) -> None:
    found = [p for p in problems(tmp_path, "docs/guide.md", text) if p.check == "SC22"]
    assert (found == []) is ok, found


def test_each_slide_is_a_page_for_the_first_mention(tmp_path: Path) -> None:
    text = (
        "## Slide 1: Open\n\nSection 2: State and sessions starts.\n\n"
        "## Slide 2: Next\n\nSection 2 goes on.\n"
    )
    found = [p for p in problems(tmp_path, "slides/deck.md", text) if p.check == "SC22"]
    assert [p.line for p in found] == [7], found


@pytest.mark.parametrize(
    "rel",
    ["docs/evidence/s1.md", "docs/evidence.md"],
)
def test_evidence_pages_keep_their_codes(tmp_path: Path, rel: str) -> None:
    text = "F4 broke R1 in Feature 4 (Anthropic, Harness design).\n"
    assert plain_checks(problems(tmp_path, rel, text)) == []


@pytest.mark.parametrize(
    "rel",
    [
        "use-in-your-repo/skills/house-rules/SKILL.md",
        "use-in-your-repo/kit/templates/AGENTS.md",
        "section-4-verification/assignment/solution/skill/testgen-evidence/SKILL.md",
        "section-1-instructions/demo/harness/AGENTS.md",
        "slides/module1-slides.md",
        "slides/deck.md",
    ],
)
def test_skills_kit_templates_harness_and_slides_get_the_label_rules(
    tmp_path: Path, rel: str
) -> None:
    text = "# Skill\n\nKeep R1 (Meta, TestGen-LLM) in Feature 2; see [link].\n"
    found = plain_checks(problems(tmp_path, rel, text))
    assert found == ["SC21", "SC22", "SC23", "SC24", "SC25"], found


@pytest.mark.parametrize(
    ("text", "want"),
    [
        (
            f"Agents skew positive ([Harness design]({HD})).\n",
            ["SC25"],
        ),
        ("Held-out tests catch it (SpecBench).\n", ["SC23", "SC25"]),
        ("Anthropic's Effective harnesses article says so.\n", ["SC23", "SC25"]),
    ],
)
def test_a_source_needs_a_link_and_a_sources_list(
    tmp_path: Path, text: str, want: list[str]
) -> None:
    found = problems(tmp_path, "docs/guide.md", text)
    assert plain_checks(found) == want, found


SOURCES_LIST = (
    "## Sources\n\n"
    f"- Source 1: Harness design for long-running application development, <{HD}>,\n"
    "  Prithvi Rajasekaran (Anthropic), 2026-03-24\n"
    f"- Source 2: Automated Unit Test Improvement using Large Language Models at Meta, <{TG}>, "
    "Nadia Alshahwan and others (Meta), 2024-02-14\n"
)


def test_a_linked_source_with_a_numbered_sources_list_passes(tmp_path: Path) -> None:
    text = (
        f"Agents skew positive ([Harness design]({HD})). Tests pass five runs\n"
        f"([TestGen-LLM]({TG})); Source 2 measured it, and Source 1 too.\n\n" + SOURCES_LIST
    )
    assert plain_checks(problems(tmp_path, "docs/guide.md", text)) == []


def test_every_mention_of_a_source_title_is_a_link(tmp_path: Path) -> None:
    text = (
        f"First ([Harness design for long-running\napplication development]({HD})).\n\n"
        "Later, Harness design for long-running apps says more.\n\n"
        f"Tests ([TestGen-LLM]({TG})).\n\n" + SOURCES_LIST
    )
    found = [p for p in problems(tmp_path, "docs/guide.md", text) if p.check == "SC23"]
    assert [p.line for p in found] == [4], found


@pytest.mark.parametrize(
    ("items", "message"),
    [
        (
            f"- Source 1: Harness design, <{HD}>, Prithvi Rajasekaran, 2026-03-24\n"
            f"- Source 3: TestGen, <{TG}>, Meta, 2024-02-14\n",
            "is entry 2",
        ),
        (
            f"- Source 1: TestGen, <{TG}>, Meta, 2024-02-14\n"
            f"- Source 2: Harness design, <{HD}>, Prithvi Rajasekaran, 2026-03-24\n",
            "order",
        ),
        (
            f"- Source 1: Harness design, <{HD}>, Prithvi Rajasekaran, 2026-03-24\n",
            "TestGen",
        ),
        (
            f"- Source 1: Harness design, <{HD}>, 2026-03-24\n",
            "reads",
        ),
    ],
)
def test_the_sources_list_is_numbered_complete_and_in_order(
    tmp_path: Path, items: str, message: str
) -> None:
    text = f"A ([Harness design]({HD})).\n\nB ([TestGen-LLM]({TG})).\n\n## Sources\n\n" + items
    found = [p for p in problems(tmp_path, "docs/guide.md", text) if p.check == "SC25"]
    assert any(message in p.message for p in found), found


def test_a_sources_heading_may_close_any_template(tmp_path: Path) -> None:
    body = (
        f"Tests pass five times ([TestGen-LLM]({TG})).\n\n## Sources\n\n"
        f"- Source 1: Automated Unit Test Improvement using Large Language Models at Meta, <{TG}>, "
        "Nadia Alshahwan and others (Meta), 2024-02-14\n"
    )
    found = problems(tmp_path, DEMO, demo_page(body))
    assert [p for p in found if p.check in ("SC16", "SC25")] == [], found


def test_the_module_title_is_not_a_source_mention(tmp_path: Path) -> None:
    text = "Harness engineering is the work of this course; harness design matters.\n"
    assert plain_checks(problems(tmp_path, "docs/guide.md", text)) == []


def test_further_reading_is_not_the_sources_list(tmp_path: Path) -> None:
    url = "https://arxiv.org/abs/2605.21384"
    reading = (
        f"Held-out tests ([SpecBench]({url})).\n\n## Further reading\n\n- [SpecBench]({url})\n"
    )
    assert plain_checks(problems(tmp_path, "docs/guide.md", reading)) == ["SC25"]
    listed = reading + f"\n## Sources\n\n- Source 1: SpecBench, <{url}>, WecoAI, 2026-05\n"
    assert plain_checks(problems(tmp_path / "ok", "docs/guide.md", listed)) == []
