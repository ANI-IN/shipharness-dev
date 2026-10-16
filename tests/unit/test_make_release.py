"""scripts/make_release.py: tree selection, guards, reference check, REFERENCES.md, build."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("make_release", REPO / "scripts" / "make_release.py")
assert _spec and _spec.loader
mr = importlib.util.module_from_spec(_spec)
sys.modules["make_release"] = mr
_spec.loader.exec_module(mr)


# -- selection ----------------------------------------------------------------------------------

TRACKED = [
    ".github/workflows/ci.yml",
    ".github/dependabot.yml",
    ".vale/styles/Shipharness/Banned.yml",
    ".vale.ini",
    ".env.example",
    "CODEOWNERS",
    "CONTRACTS.md",
    "DESIGN.md",
    "LICENSE",
    "Makefile",
    "README.md",
    "RESEARCH.md",
    "VERIFICATION.md",
    "instructor/run-sheet.md",
    "notes.txt",
    "pyproject.toml",
    "research/notes/R-a.md",
    "scripts/anchors.py",
    "scripts/fetch_testgen_libs.py",
    "scripts/lint_prose.py",
    "scripts/make_release.py",
    "scripts/pilot.py",
    "scripts/publish_solutions.py",
    "src/shipharness/cli.py",
    "submodules/01-instructions/README.md",
    "submodules/01-instructions/solution/README.md",
    "submodules/02-state-lifecycle/solution/grader/hidden/case_1.py",
    "submodules/03-scope-sandbox/assignment/hidden/cases.json",
    "teamtrack/reference/checkpoints.toml",
    "teamtrack/tests/hidden/f1/test_f1_search.py",
    "tests/unit/test_cli.py",
    "uv.lock",
]


def test_selection_includes_the_allow_list_and_three_scripts() -> None:
    sel = mr.select(TRACKED)
    for path in [
        ".github/workflows/ci.yml",
        ".vale/styles/Shipharness/Banned.yml",
        ".vale.ini",
        ".env.example",
        "LICENSE",
        "Makefile",
        "README.md",
        "pyproject.toml",
        "scripts/anchors.py",
        "scripts/fetch_testgen_libs.py",
        "scripts/lint_prose.py",
        "src/shipharness/cli.py",
        "submodules/01-instructions/README.md",
        "teamtrack/reference/checkpoints.toml",
        "teamtrack/tests/hidden/f1/test_f1_search.py",
        "tests/unit/test_cli.py",
        "uv.lock",
    ]:
        assert path in sel.included, path


def test_selection_excludes_internal_files_solutions_and_hidden_cases() -> None:
    sel = mr.select(TRACKED)
    for path in [
        ".github/dependabot.yml",
        "CODEOWNERS",
        "CONTRACTS.md",
        "DESIGN.md",
        "RESEARCH.md",
        "VERIFICATION.md",
        "instructor/run-sheet.md",
        "notes.txt",
        "research/notes/R-a.md",
        "scripts/make_release.py",
        "scripts/pilot.py",
        "scripts/publish_solutions.py",
        "submodules/01-instructions/solution/README.md",
        "submodules/02-state-lifecycle/solution/grader/hidden/case_1.py",
        "submodules/03-scope-sandbox/assignment/hidden/cases.json",
    ]:
        assert path not in sel.included, path
        assert path in sel.excluded, path
    assert sel.excluded["submodules/01-instructions/solution/README.md"] == mr.REASON_SOLUTION


def test_extra_exclusions_are_removed_with_their_reason() -> None:
    sel = mr.select(TRACKED, extra_excluded={"tests/unit/test_cli.py": "uses scripts/pilot.py"})
    assert "tests/unit/test_cli.py" not in sel.included
    assert "pilot" in sel.excluded["tests/unit/test_cli.py"]


@pytest.mark.parametrize(
    "path",
    [
        "submodules/01-instructions/solution/README.md",
        "submodules/02-state-lifecycle/solution/grader/hidden/case_1.py",
        "src/shipharness/grader/check.py",
        "submodules/03-scope-sandbox/assignment/hidden/cases.json",
        "skills/x/solution/answer.md",
    ],
)
def test_guard_fails_on_any_solution_grader_or_submodule_hidden_path(path: str) -> None:
    assert mr.guard_violations(["README.md", path]) == [path]


def test_guard_allows_the_referee_hidden_tests_under_teamtrack() -> None:
    assert mr.guard_violations(["teamtrack/tests/hidden/f1/test_f1_search.py", "README.md"]) == []


def test_a_guard_violation_makes_the_dry_run_fail() -> None:
    report = mr.Report(
        ref="HEAD",
        selection=mr.Selection(included=["README.md", "submodules/01-x/solution/a.md"]),
        excluded_tests={},
        guard=mr.guard_violations(["README.md", "submodules/01-x/solution/a.md"]),
        hits=[],
        references=mr.References(text="", sources=[], findings=[], unresolved=[]),
    )
    assert not report.ok
    assert any("solution" in p for p in report.problems())


# -- excluded tests -----------------------------------------------------------------------------

EXCLUDED = [
    "DESIGN.md",
    "scripts/pilot.py",
    "scripts/build_testgen_dataset.py",
    "instructor/README.md",
    "instructor/run-sheet.md",
]
INCLUDED = ["README.md", "scripts/lint_prose.py", "tests/unit/support.py"]

TEST_SOURCES = {
    "tests/unit/test_pilot.py": (
        "import importlib.util\nfrom pathlib import Path\nREPO = Path('.')\n"
        "_spec = importlib.util.spec_from_file_location('pilot', REPO / 'scripts' / 'pilot.py')\n"
    ),
    "tests/unit/test_reads_design.py": "TEXT = (ROOT / 'DESIGN.md').read_text()\n",
    "tests/unit/test_loads_by_stem.py": "mod = load_script('build_testgen_dataset')\n",
    "tests/unit/test_run_sheet.py": "p = ROOT / 'instructor' / 'run-sheet.md'\n",
    "tests/unit/test_docstring_only.py": (
        '"""Checks the layout in DESIGN.md §3 (scripts/pilot.py is not used)."""\n'
        "# DESIGN §4\nX = 'README.md'\n"
    ),
    "tests/unit/test_fixture_tree.py": "p = tmp / 'instructor' / 'notes.md'\nq = 'instructor'\n",
    "tests/unit/test_lint.py": "p = REPO / 'scripts' / 'lint_prose.py'\n",
}


def test_tests_that_exercise_excluded_files_are_found_mechanically() -> None:
    found = mr.find_excluded_tests(TEST_SOURCES, EXCLUDED, INCLUDED)
    assert sorted(found) == [
        "tests/unit/test_loads_by_stem.py",
        "tests/unit/test_pilot.py",
        "tests/unit/test_reads_design.py",
        "tests/unit/test_run_sheet.py",
    ]
    assert any("scripts/pilot.py" in r for r in found["tests/unit/test_pilot.py"])


def test_a_flagged_helper_excludes_the_tests_that_import_it() -> None:
    sources = {
        "tests/unit/datasets/build_support.py": "S = REPO / 'scripts' / 'pilot.py'\n",
        "tests/unit/datasets/test_uses_helper.py": "from .build_support import S\n",
        "tests/unit/datasets/test_other.py": "import json\n",
    }
    found = mr.find_excluded_tests(sources, EXCLUDED, INCLUDED)
    assert sorted(found) == [
        "tests/unit/datasets/build_support.py",
        "tests/unit/datasets/test_uses_helper.py",
    ]


# -- reference check ----------------------------------------------------------------------------


def _hits(text: str, path: str = "submodules/01-x/concepts.md", **kw: object) -> list:
    return mr.scan_references(path, text, **kw)


def test_a_design_section_reference_is_reported_with_line_and_text() -> None:
    hits = _hits("Intro line.\nSee DESIGN.md §3 for the layout.\n")
    assert [(h.line, h.kind, h.text) for h in hits] == [(2, "section-cite", "DESIGN.md §3")]
    assert hits[0].path == "submodules/01-x/concepts.md"


def test_links_mentions_and_citations_of_excluded_files() -> None:
    text = (
        "Interfaces: [CONTRACTS.md §1](../../CONTRACTS.md).\n"
        "Sources: RESEARCH G-7 and RESEARCH §4.8.\n"
        "Notes live in research/notes/R-a.md and R-b.\n"
        "Results come from VERIFICATION.md after M6.\n"
        "Run `uv run python scripts/build_features_dataset.py`.\n"
        "| `solution/` | Reference solution |\n"
        "Read [the run sheet](../instructor/run-sheet.md).\n"
        "# picked by the class poll (Design §14.1)\n"
    )
    kinds = [(h.line, h.kind) for h in _hits(text)]
    assert (1, "link") in kinds
    assert (2, "section-cite") in kinds and [k for k in kinds if k[0] == 2].count(
        (2, "section-cite")
    ) == 2
    assert (3, "mention") in kinds
    assert (4, "mention") in kinds
    assert (5, "script") in kinds
    assert (6, "solution") in kinds
    assert (7, "link") in kinds
    assert (8, "section-cite") in kinds
    assert len([k for k in kinds if k[0] == 1]) == 1  # the link text is not counted again


def test_near_misses_are_not_reported() -> None:
    text = (
        "opts = RunOptions(research=False)\n"
        "The solution: a harness.\n"
        "extend-exclude = ['.claude', 'research']\n"
        "Our research notes are summarised here.\n"
        "Instructors run the class; see the instructor notes.\n"
        "Design decisions: docs/design-docs/index.md\n"
        "Run `uv run python scripts/lint_prose.py` and scripts/anchors.py.\n"
        "Verification the agent does not control.\n"
        "make pilot is available later\n"
        "house rules R1 and R6\n"
    )
    assert _hits(text) == []


def test_a_sentence_end_does_not_hide_a_path_mention() -> None:
    existing = frozenset({"research/notes/R-a.md"})
    hits = _hits("Quotes come from research/notes/R-a.md.\n", existing=existing)
    assert [h.text for h in hits] == ["research/notes/R-a.md"]


def test_research_corrections_count_as_citations() -> None:
    hits = _hits("The separate evaluator comes from A3 (RESEARCH correction 3).\n")
    assert [(h.kind, h.pattern) for h in hits] == [("section-cite", "RESEARCH correction N")]


def test_folder_mentions_must_name_a_tracked_excluded_file_when_known() -> None:
    existing = frozenset({"instructor/run-sheet.md", "research/notes/R-a.md"})
    text = "fixture: 'instructor/notes.md'\nsee instructor/run-sheet.md and research/notes/\n"
    hits = _hits(text, path="tests/unit/test_x.py", existing=existing)
    assert [(h.line, h.text) for h in hits] == [
        (2, "instructor/run-sheet.md"),
        (2, "research/notes/"),
    ]


def test_a_not_included_statement_is_a_hit_only_when_it_links_or_cites() -> None:
    assert _hits("DESIGN.md is not included in this repository.\n") == []
    linked = _hits("[DESIGN.md](DESIGN.md) is not included in this repository.\n")
    assert [h.kind for h in linked] == ["link"]
    cited = _hits("The layout (DESIGN §3) is not included here.\n")
    assert [h.kind for h in cited] == ["section-cite"]


def test_a_verification_run_id_counts_only_as_the_sole_source() -> None:
    ids = frozenset({"ab-20261016-100000-abcdef"})
    alone = _hits("Measured in ab-20261016-100000-abcdef.\n", run_ids=ids)
    assert [h.kind for h in alone] == ["run-id"]
    assert _hits("A2 says so (F-a-13); see ab-20261016-100000-abcdef.\n", run_ids=ids) == []
    assert _hits("Fixture id ab-20261016-100000-ffffff.\n", run_ids=ids) == []


# -- REFERENCES.md ------------------------------------------------------------------------------

RESEARCH_MD = """# RESEARCH

- Research milestone: M1. Access date for every source: 2026-10-16.

## 1. Source register

### 1.1 Teaching sources (§1.9)

| ID | Title | URL | Author / org | Date | Summary |
|---|---|---|---|---|---|
| A1 | Harness engineering | https://ex.org/a1 | R. L., OpenAI | 2026-02-11 | s |
| A2 | Effective harnesses | https://ex.org/a2 | J. Y., Anthropic | 2025-11-26 | s |
| B13 / B14 | SpecBench; repo | https://ex.org/b13 ; https://ex.org/b14 | W | 2026 | s |

### 1.2 Technical references
"""

NOTES_A = """# R-a

## Sources

| id | title | URL | author(s)/org | publication date | access date | summary |
|---|---|---|---|---|---|---|
| A1 | Harness engineering | https://ex.org/a1 | R. L. | 2026-02-11 | x | s |
| A2 | Effective harnesses | https://ex.org/a2 | J. Y. | 2025-11-26 | x | s |
| A3 | Pkg | https://ex.org/a3 | author_email K. L. <kl@example.com> | 2026 | x | s |

## Findings

- `F-a-01` | storyline | Steering. | "Humans steer. Agents execute." | A1, introduction
- `F-a-02` | storyline | Design. | "design environments, specify intent" | A1, introduction
- `F-a-03` | cause2 | Memory. | "each new session begins with no memory." | A2, intro
"""

NOTES_B = """# R-b

## Sources

| id | title | URL | author(s)/org | date | access date | summary |
|---|---|---|---|---|---|---|
| B13 | SpecBench | https://arxiv.org/abs/2605.21384 | Weco AI | 2026 | x | s |
| B14 | WecoAI/SpecBench (GitHub) | https://github.com/WecoAI/SpecBench | Weco AI | repo | x | s |

## Findings

| ID | tags | claim | quote | source |
|---|---|---|---|---|
| F-b-01 | S4 | Gap. | "smaller models exhibiting larger gaps" | B13 §Abstract |
| F-b-02 | S4 | Hidden. | "never shown to the agent" | B14 README |
"""

NOTES_D = """# R-d

## Sources

| id | title | URL | access date | summary |
|---|---|---|---|---|
| D27 | None network driver | https://docs.docker.com/engine/network/drivers/none/ | x | s |
| D28 | Other | https://docs.docker.com/other/ | x | s |
"""


def _references(cited_texts: dict[str, str]) -> object:
    return mr.build_references(
        RESEARCH_MD,
        {"research/notes/R-a.md": NOTES_A, "research/notes/R-b.md": NOTES_B, "x/R-d.md": NOTES_D},
        cited_texts,
        teaching=("A1", "A2", "B13"),
    )


def test_references_list_only_the_cited_findings() -> None:
    refs = _references({"a.md": "As A1 puts it (F-a-02). The gap (B13, F-b-01) in D27.\n"})
    ids = [f.id for f in refs.findings]
    assert ids == ["F-a-02", "F-b-01"]
    assert "F-a-01" not in refs.text and "F-a-03" not in refs.text
    assert '"design environments, specify intent"' in refs.text
    assert (
        '| F-a-02 | A1 | "design environments, specify intent" | https://ex.org/a1 |' in refs.text
    )
    assert [s.id for s in refs.sources] == ["A1", "A2", "B13", "D27"]
    assert "D28" not in refs.text
    assert refs.unresolved == []


def test_references_expand_ranges_and_add_the_sources_of_cited_findings() -> None:
    refs = _references({"a.md": "See F-a-01 to F-a-03 and F-b-02.\n"})
    assert [f.id for f in refs.findings] == ["F-a-01", "F-a-02", "F-a-03", "F-b-02"]
    assert "B14" in [s.id for s in refs.sources]  # source of F-b-02


def test_references_carry_no_email_addresses() -> None:
    refs = _references({"a.md": "A3 says so.\n"})
    assert "| A3 | Pkg | K. L. |" in refs.text
    assert "@" not in refs.text


def test_unknown_finding_ids_are_reported_unresolved() -> None:
    refs = _references({"a.md": "Cited as F-a-99.\n"})
    assert refs.unresolved == ["F-a-99"]


def test_references_text_passes_the_prose_lint_and_the_reference_check() -> None:
    refs = _references({"a.md": "F-a-01 F-b-01\n"})
    lint = importlib.util.spec_from_file_location("lint_prose", REPO / "scripts" / "lint_prose.py")
    assert lint and lint.loader
    module = importlib.util.module_from_spec(lint)
    lint.loader.exec_module(module)
    assert module.lint_text(refs.text) == []
    assert mr.scan_references("REFERENCES.md", refs.text) == []


# -- build (miniature fixture repo) -------------------------------------------------------------


def _git(cwd: Path, *args: str) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_AUTHOR_NAME="t",
        GIT_AUTHOR_EMAIL="t@t.invalid",
        GIT_COMMITTER_NAME="t",
        GIT_COMMITTER_EMAIL="t@t.invalid",
    )
    done = subprocess.run(["git", *args], cwd=cwd, capture_output=True, env=env, check=True)
    return done.stdout.decode().strip()


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


@pytest.fixture
def mini_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "dev"
    files = {
        "README.md": "# mini\n\nAs A2 says (F-a-03).\n",
        "LICENSE": "MIT\n",
        "src/pkg/__init__.py": "X = 1\n",
        "teamtrack/app/x.py": "a = 1\n",
        "teamtrack/reference/f1/f1.patch": (
            "diff --git a/app/x.py b/app/x.py\n--- a/app/x.py\n+++ b/app/x.py\n"
            "@@ -1 +1,2 @@\n a = 1\n+b = 2\n"
        ),
        "teamtrack/reference/checkpoints.toml": (
            '[checkpoints."c-base"]\ntasks = []\n\n[checkpoints."c-one"]\ntasks = ["f1"]\n'
        ),
        "teamtrack/tests/hidden/test_h.py": "def test_h():\n    assert True\n",
        "submodules/01-x/README.md": "# one\n",
        "submodules/01-x/solution/README.md": "# answer\n",
        "DESIGN.md": "# design\n",
        "RESEARCH.md": RESEARCH_MD,
        "research/notes/R-a.md": NOTES_A,
        "research/notes/R-b.md": NOTES_B,
        "VERIFICATION.md": "# verification\n",
        "scripts/pilot.py": "print(1)\n",
        "tests/unit/test_pilot.py": "P = ROOT / 'scripts' / 'pilot.py'\n",
        "tests/unit/test_ok.py": "def test_ok():\n    assert True\n",
    }
    for rel, text in files.items():
        _write(repo, rel, text)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "first")
    _write(repo, "src/pkg/later.py", "Y = 2\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "second")
    return repo


def test_build_makes_one_commit_plus_the_checkpoint_tags(mini_repo: Path, tmp_path: Path) -> None:
    dest = tmp_path / "learner"
    result = mr.build(mini_repo, "HEAD", dest, verify=[sys.executable, "-c", "pass"])
    assert _git(dest, "rev-list", "--count", "HEAD") == "1"
    assert _git(dest, "log", "-1", "--format=%an|%s") == f"{mr.AUTHOR_NAME}|{mr.COMMIT_MESSAGE}"
    head = _git(dest, "rev-parse", "HEAD")
    assert sorted(_git(dest, "tag", "--list").split()) == ["c-base", "c-one"]
    assert _git(dest, "rev-parse", "c-one^") == head
    assert _git(dest, "show", "c-one:teamtrack/app/x.py") == "a = 1\nb = 2"
    assert sorted(result.tags) == ["c-base", "c-one"]
    tree = set(_git(dest, "ls-files").split())
    assert {"README.md", "REFERENCES.md", "src/pkg/later.py"} <= tree
    assert "teamtrack/tests/hidden/test_h.py" in tree
    for gone in [
        "DESIGN.md",
        "RESEARCH.md",
        "research/notes/R-a.md",
        "scripts/pilot.py",
        "submodules/01-x/solution/README.md",
        "tests/unit/test_pilot.py",
    ]:
        assert gone not in tree, gone
    assert "F-a-03" in (dest / "REFERENCES.md").read_text(encoding="utf-8")


def test_build_refuses_when_the_dry_run_checks_fail(mini_repo: Path, tmp_path: Path) -> None:
    _write(mini_repo, "README.md", "# mini\n\nSee DESIGN.md §3.\n")
    _git(mini_repo, "commit", "-q", "-am", "cite design")
    dest = tmp_path / "learner"
    with pytest.raises(mr.ReleaseError, match="dry-run checks failed"):
        mr.build(mini_repo, "HEAD", dest, verify=[sys.executable, "-c", "pass"])
    assert not dest.exists()


def test_dry_run_cli_exits_non_zero_on_hits_and_writes_the_list(
    mini_repo: Path, tmp_path: Path
) -> None:
    _write(mini_repo, "README.md", "# mini\n\nSee DESIGN.md §3.\n")
    _git(mini_repo, "commit", "-q", "-am", "cite design")
    listing = tmp_path / "files.txt"
    done = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "make_release.py"),
            "--repo",
            str(mini_repo),
            "--list-file",
            str(listing),
            "--references-file",
            str(tmp_path / "REFERENCES.md"),
            "--report-file",
            str(tmp_path / "report.txt"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert done.returncode == 1, done.stdout + done.stderr
    assert "README.md:3" in done.stdout and "DESIGN.md §3" in done.stdout
    assert "tests/unit/test_pilot.py" in done.stdout  # the excluded-tests list
    assert "README.md" in listing.read_text(encoding="utf-8").split()
