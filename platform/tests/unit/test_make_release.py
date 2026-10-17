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

A1 = "submodules/01-instructions"
TRACKED = [
    ".github/workflows/ci.yml",
    "kit/README.md",
    "kit/templates/AGENTS.md",
    "kit/examples/boltons-queueutils/README.md",
    "docs/apply-to-your-repo.md",
    "docs/extras.md",
    "scripts/build_slides.py",
    "slides/deck.md",
    "slides/img/show-1-screen-1.png",
    ".github/dependabot.yml",
    ".vale/styles/Shipharness/Banned.yml",
    ".vale.ini",
    ".env.example",
    ".python-version",
    ".shipharness/runs/r-1/run.json",
    "CODEOWNERS",
    "CONTRACTS.md",
    "DESIGN.md",
    "FREEZE-EXCEPTIONS.toml",
    "LICENSE",
    "Makefile",
    "README.md",
    "RESEARCH.md",
    "VERIFICATION.md",
    "docs/setup-linux.md",
    "docs/scratch.md",
    "exports/scores.json",
    "instructor/run-sheet.md",
    "instructor/engineering-notes/release-plan.md",
    "notes.txt",
    "pyproject.toml",
    "research/notes/R-a.md",
    "scripts/anchors.py",
    "scripts/fetch_testgen_libs.py",
    "scripts/freeze_harness.py",
    "scripts/grade_assignment.py",
    "scripts/lint_prose.py",
    "scripts/make_release.py",
    "scripts/pilot.py",
    "scripts/publish_solutions.py",
    "setup/PRE-CLASS.md",
    "slides/outline.md",
    "slides/deck.pdf",
    "slides/deck.pptx",
    "slides/build.sh",
    "src/shipharness/cli.py",
    f"{A1}/README.md",
    f"{A1}/concepts.md",
    f"{A1}/session-notes.md",
    f"{A1}/demo/README.md",
    f"{A1}/post-class-reading/01-map.md",
    f"{A1}/assignment/README.md",
    f"{A1}/assignment/check.py",
    f"{A1}/assignment/live_evidence.py",
    f"{A1}/assignment/starter/AGENTS.md",
    f"{A1}/assignment/visible_tests/test_visible.py",
    f"{A1}/scratch/idea.md",
    f"{A1}/solution/README.md",
    f"{A1}/solution/grader/tests/test_grade.py",
    "submodules/02-state-lifecycle/solution/grader/hidden/case_1.py",
    "submodules/03-scope-sandbox/assignment/hidden/cases.json",
    "submodules/05-extra/concepts.md",
    "teamtrack/reference/checkpoints.toml",
    "teamtrack/mutants/m1.patch",
    "teamtrack/tests/hidden/f1/test_f1_search.py",
    "tests/unit/test_cli.py",
    "uv.lock",
]


def test_selection_follows_the_owner_structure() -> None:
    sel = mr.select(TRACKED)
    for path in [
        ".github/workflows/ci.yml",
        ".env.example",
        ".python-version",
        "LICENSE",
        "Makefile",
        "README.md",
        "docs/setup-linux.md",
        "pyproject.toml",
        "scripts/anchors.py",
        "scripts/fetch_testgen_libs.py",
        "scripts/grade_assignment.py",
        "scripts/lint_prose.py",
        "slides/outline.md",
        "slides/deck.pdf",
        "slides/deck.pptx",
        "src/shipharness/cli.py",
        f"{A1}/README.md",
        f"{A1}/concepts.md",
        f"{A1}/session-notes.md",
        f"{A1}/demo/README.md",
        f"{A1}/post-class-reading/01-map.md",
        f"{A1}/assignment/README.md",
        f"{A1}/assignment/check.py",
        f"{A1}/assignment/live_evidence.py",
        f"{A1}/assignment/starter/AGENTS.md",
        f"{A1}/assignment/visible_tests/test_visible.py",
        "teamtrack/reference/checkpoints.toml",
        "teamtrack/mutants/m1.patch",
        "teamtrack/tests/hidden/f1/test_f1_search.py",
        "tests/unit/test_cli.py",
        "uv.lock",
    ]:
        assert path in sel.included, path


def test_selection_leaves_out_private_internal_and_unlisted_files() -> None:
    sel = mr.select(TRACKED)
    for path in [
        ".github/dependabot.yml",
        ".vale/styles/Shipharness/Banned.yml",
        ".vale.ini",
        ".shipharness/runs/r-1/run.json",
        "CODEOWNERS",
        "CONTRACTS.md",
        "DESIGN.md",
        "FREEZE-EXCEPTIONS.toml",
        "RESEARCH.md",
        "VERIFICATION.md",
        "docs/scratch.md",
        "exports/scores.json",
        "instructor/run-sheet.md",
        "instructor/engineering-notes/release-plan.md",
        "notes.txt",
        "research/notes/R-a.md",
        "scripts/freeze_harness.py",
        "scripts/make_release.py",
        "scripts/pilot.py",
        "scripts/publish_solutions.py",
        "setup/PRE-CLASS.md",
        "slides/build.sh",
        f"{A1}/scratch/idea.md",
        f"{A1}/solution/README.md",
        f"{A1}/solution/grader/tests/test_grade.py",
        "submodules/02-state-lifecycle/solution/grader/hidden/case_1.py",
        "submodules/03-scope-sandbox/assignment/hidden/cases.json",
        "submodules/05-extra/concepts.md",
    ]:
        assert path not in sel.included, path
        assert path in sel.excluded, path
    assert sel.excluded[f"{A1}/solution/README.md"] == mr.REASON_SOLUTION
    assert sel.excluded["DESIGN.md"] == mr.REASON_PRIVATE
    assert sel.excluded["exports/scores.json"] == mr.REASON_PRIVATE
    assert sel.excluded["scripts/pilot.py"] == mr.REASON_INTERNAL
    assert sel.excluded["setup/PRE-CLASS.md"] == mr.REASON_NOT_ALLOWED


def test_leak_check_names_every_private_file_with_its_reason() -> None:
    public = [
        "README.md",
        "src/shipharness/cli.py",
        "scripts/anchors.py",
        "RESEARCH.md",
        "research/notes/R-a.md",
        "instructor/run-sheet.md",
        f"{A1}/solution/README.md",
        f"{A1}/solution/grader/tests/test_grade.py",
        "scripts/pilot.py",
        "exports/scores.json",
        ".shipharness/runs/r-1/run.json",
    ]
    found = dict(mr.leaks(public))
    assert sorted(found) == sorted(public[3:])
    assert found["scripts/pilot.py"] == mr.REASON_INTERNAL
    assert found[f"{A1}/solution/grader/tests/test_grade.py"] == mr.REASON_SOLUTION


def test_missing_owner_files_are_listed_not_failed() -> None:
    sel = mr.select(TRACKED)
    missing = mr.missing_expected(sel.included)
    assert "docs/setup-macos.md" in missing
    assert "docs/setup-linux.md" not in missing
    assert "CHANGELOG.md" in missing
    assert f"{A1}/concepts.md" not in missing
    assert "submodules/02-*/concepts.md" in missing
    assert "submodules/02-*/assignment/check.py" in missing


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
    assert [p for p, _ in mr.leaks(["README.md", path])] == [path]


def test_guard_allows_the_referee_hidden_tests_under_teamtrack() -> None:
    assert mr.leaks(["teamtrack/tests/hidden/f1/test_f1_search.py", "README.md"]) == []


def _report(included: list[str], hits: list | None = None) -> object:
    return mr.Report(
        ref="HEAD",
        selection=mr.Selection(included=included),
        excluded_tests={},
        leaks=mr.leaks(included),
        hits=hits or [],
        references=mr.References(text="", sources=[], findings=[], unresolved=[]),
    )


def test_a_leak_fails_the_dry_run_and_the_build() -> None:
    report = _report(["README.md", "submodules/01-x/solution/a.md"])
    assert any("private" in p for p in report.dry_run_failures())
    assert any("private" in p for p in report.build_failures())


def test_broken_references_are_reported_in_the_dry_run_and_fail_the_build() -> None:
    hit = mr.Hit("README.md", 3, "section-cite", "DESIGN §3", "DESIGN §", "See DESIGN §3.")
    report = _report(["README.md"], hits=[hit])
    assert report.dry_run_failures() == []
    assert any("reference" in p for p in report.build_failures())


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


def test_a_link_to_any_file_left_out_of_the_public_tree_is_reported() -> None:
    existing = frozenset({"setup/PRE-CLASS.md", f"{A1}/solution/README.md"})
    public = frozenset({"README.md", f"{A1}/concepts.md", f"{A1}/README.md"})
    text = (
        "Before class: [pre-class](../../setup/PRE-CLASS.md).\n"
        "The folder: [module](./).\n"
        "Read [concepts](concepts.md).\n"
    )
    hits = _hits(text, path=f"{A1}/README.md", existing=existing, public=public)
    assert [(h.line, h.kind, h.pattern) for h in hits] == [
        (1, "link", "link to setup/PRE-CLASS.md")
    ]


def test_internal_scripts_are_named_but_learner_scripts_are_not() -> None:
    hits = _hits("Run scripts/freeze_harness.py, then scripts/grade_assignment.py.\n")
    assert [(h.kind, h.text) for h in hits] == [("script", "scripts/freeze_harness.py")]


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


def test_run_ids_are_labels_never_broken_references() -> None:
    # Owner rule (2026-10-17): every number comes from a source or a real run id, and captured
    # output is labelled "captured on <date>, run <id>"; a run id is evidence, not a private link.
    ids = frozenset({"ab-20261016-100000-abcdef"})
    assert _hits("Measured in ab-20261016-100000-abcdef.\n", run_ids=ids) == []
    assert _hits("captured on 2026-10-16, run ab-20261016-100000-abcdef\n", run_ids=ids) == []


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
    """A miniature build repository with its own checkpoint tags (built here, in tmp_path)."""
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
            '[checkpoints."m1-s1-start"]\ntasks = []\n\n'
            '[checkpoints."m1-s2-start"]\ntasks = ["f1"]\n'
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
    _git(repo, "config", "user.name", "t")
    _git(repo, "config", "user.email", "t@t.invalid")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "first")
    _write(repo, "src/pkg/later.py", "Y = 2\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "second")
    from shipharness.ab.checkpoints import build_commits

    build_commits(repo, dry_run=False)
    return repo


def _refs(repo: Path) -> str:
    return _git(repo, "for-each-ref", "--format=%(refname) %(objectname)")


def test_dry_run_builds_one_commit_rebuilds_the_tags_and_writes_the_record(
    mini_repo: Path, tmp_path: Path
) -> None:
    from shipharness import freeze

    before = _refs(mini_repo)
    rel = mr.dry_run(mini_repo, "HEAD", tmp_path / "public")
    public = rel.public
    assert _refs(mini_repo) == before  # nothing tagged or moved in the build repository
    assert _git(public, "rev-list", "--count", "HEAD") == "1"
    assert _git(public, "remote") == ""
    assert sorted(_git(public, "tag", "--list").split()) == [
        "class-v1",
        "m1-s1-start",
        "m1-s2-start",
    ]  # no harness-frozen: the build repository has no freeze record
    assert "REFERENCES.md" in rel.public_files
    assert "DESIGN.md" not in rel.public_files
    assert rel.tree_leaks == []
    by_name = {c.name: c for c in rel.checkpoints}
    assert sorted(by_name) == ["m1-s1-start", "m1-s2-start"]
    for c in by_name.values():
        assert c.app_match and c.differing == [], c
        assert not c.full_match  # the build tree also holds the private files
    assert rel.frozen.basis == "head"
    assert rel.frozen.paths and all(rel.frozen.paths.values())
    assert rel.frozen.record_commit is None
    assert freeze.read_record(public) is None
    assert "refs/tags/harness-frozen" not in rel.push[-1]
    assert rel.failures() == []


def test_without_a_freeze_record_the_report_says_harness_frozen_was_not_written(
    mini_repo: Path, tmp_path: Path
) -> None:
    rel = mr.dry_run(mini_repo, "HEAD", tmp_path / "public")
    text = mr.render(rel, "files.txt", "REFERENCES.md")
    assert "harness-frozen: not written (no freeze record in the build repository)" in text
    assert f"class-v1 tag written at {rel.commit[:12]}; its own check: PASS" in text


def test_dry_run_writes_the_class_v1_tag_with_its_record(mini_repo: Path, tmp_path: Path) -> None:
    from shipharness import freeze
    from shipharness.config import Settings

    rel = mr.dry_run(mini_repo, "HEAD", tmp_path / "public")
    public = rel.public
    assert _git(public, "rev-parse", "class-v1^{commit}") == rel.commit
    assert _git(public, "cat-file", "-t", "class-v1") == "tag"  # annotated
    tagger = _git(public, "tag", "--list", "class-v1", "--format=%(taggername) %(taggeremail)")
    assert tagger == f"{mr.AUTHOR_NAME} <{mr.AUTHOR_EMAIL}>"
    message = _git(public, "tag", "--list", "class-v1", "--format=%(contents)")
    assert message.startswith(freeze.CLASS_MESSAGE + "\n\nclass-record:\n")
    record = freeze.read_tag_record(public, "class-v1")
    assert record is not None
    assert record["content_hashes"] == freeze.content_hashes(public, freeze.FROZEN_PATHS)
    assert record["checkpoint_trees"] == freeze.checkpoint_trees(public)
    assert sorted(record["checkpoint_trees"]) == ["m1-s1-start", "m1-s2-start"]
    assert record["run_settings"] == freeze.run_settings(Settings(_env_file=None))  # no .env
    assert rel.class_tag.commit == rel.commit
    assert rel.class_tag.self_check == []
    assert "refs/tags/class-v1" in rel.push[-1]


def test_dry_run_compares_against_the_build_repo_freeze_tag_when_it_exists(
    mini_repo: Path, tmp_path: Path
) -> None:
    from shipharness import freeze
    from shipharness.config import Settings

    freeze.create_tag(mini_repo, Settings(_env_file=None), identity=("t", "t@t.invalid"))
    rel = mr.dry_run(mini_repo, "HEAD", tmp_path / "public")
    assert rel.frozen.basis == "tag"
    assert all(rel.frozen.paths.values())
    public = rel.public
    assert {"harness-frozen", "class-v1"} <= set(_git(public, "tag", "--list").split())
    assert rel.frozen.record_commit == rel.commit
    assert rel.frozen.self_check == []
    record = freeze.read_record(public)
    assert record is not None
    assert record["checkpoint_trees"] == freeze.checkpoint_trees(public)
    assert rel.push[-1].endswith("refs/tags/class-v1 refs/tags/harness-frozen")


def test_a_frozen_path_that_differs_fails_the_dry_run(mini_repo: Path, tmp_path: Path) -> None:
    _write(mini_repo, "teamtrack/reference/solution/notes.md", "private\n")
    _git(mini_repo, "add", "-A")
    _git(mini_repo, "commit", "-q", "-m", "private note under a frozen path")
    rel = mr.dry_run(mini_repo, "HEAD", tmp_path / "public")
    assert rel.frozen.paths["teamtrack/reference"] is False
    assert rel.frozen.paths["teamtrack/tests/hidden"] is True
    assert any("teamtrack/reference" in f for f in rel.failures())


def test_a_checkpoint_whose_teamtrack_tree_differs_is_reported(
    mini_repo: Path, tmp_path: Path
) -> None:
    _write(mini_repo, "teamtrack/app/y.py", "c = 3\n")
    _git(mini_repo, "add", "-A")
    _git(mini_repo, "commit", "-q", "-m", "teamtrack changed after the tags")
    rel = mr.dry_run(mini_repo, "HEAD", tmp_path / "public")
    for c in rel.checkpoints:
        assert not c.app_match
        assert "teamtrack/app/y.py" in c.differing
    assert rel.failures() == []  # reported in the dry run
    assert any("checkpoint" in f for f in rel.build_failures())


def test_push_commands_are_printed_for_the_target_and_never_run() -> None:
    commands = mr.push_commands(Path("/tmp/pub"), ["m1-s2-start", "m1-s1-start"])
    assert commands[0] == "cd /tmp/pub"
    assert f"https://github.com/{mr.TARGET}.git" in commands[1]
    assert mr.TARGET == "ANI-IN/harness-engineering-session"
    assert "git push origin main" in commands
    assert commands[-1] == (
        "git push origin refs/tags/m1-s1-start refs/tags/m1-s2-start refs/tags/class-v1"
    )
    frozen = mr.push_commands(Path("/tmp/pub"), ["m1-s1-start"], harness_frozen=True)
    assert frozen[-1] == (
        "git push origin refs/tags/m1-s1-start refs/tags/class-v1 refs/tags/harness-frozen"
    )


def test_build_makes_one_commit_plus_the_checkpoint_tags(mini_repo: Path, tmp_path: Path) -> None:
    dest = tmp_path / "learner"
    result = mr.build(mini_repo, "HEAD", dest, verify=[sys.executable, "-c", "pass"])
    assert _git(dest, "rev-list", "--count", "HEAD") == "1"
    assert _git(dest, "log", "-1", "--format=%an|%s") == f"{mr.AUTHOR_NAME}|{mr.COMMIT_MESSAGE}"
    head = _git(dest, "rev-parse", "HEAD")
    assert sorted(result.tags) == ["m1-s1-start", "m1-s2-start"]
    assert _git(dest, "rev-parse", "m1-s2-start^") == head
    assert _git(dest, "show", "m1-s2-start:teamtrack/app/x.py") == "a = 1\nb = 2"
    assert sorted(_git(dest, "tag", "--list").split()) == ["class-v1", *sorted(result.tags)]
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


def test_build_refuses_on_a_broken_reference(mini_repo: Path, tmp_path: Path) -> None:
    _write(mini_repo, "README.md", "# mini\n\nSee DESIGN.md §3.\n")
    _git(mini_repo, "commit", "-q", "-am", "cite design")
    dest = tmp_path / "learner"
    with pytest.raises(mr.ReleaseError, match="release checks failed"):
        mr.build(mini_repo, "HEAD", dest, verify=[sys.executable, "-c", "pass"])
    assert not dest.exists()


def test_dry_run_cli_reports_broken_references_without_failing(
    mini_repo: Path, tmp_path: Path
) -> None:
    _write(mini_repo, "README.md", "# mini\n\nSee DESIGN.md §3.\n")
    _git(mini_repo, "commit", "-q", "-am", "cite design")
    listing = tmp_path / "files.txt"
    done = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "make_release.py"),
            "--dry-run",
            "--repo",
            str(mini_repo),
            "--workdir",
            str(tmp_path / "public"),
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
    assert done.returncode == 0, done.stdout + done.stderr
    out = done.stdout
    assert "README.md:3" in out and "DESIGN.md §3" in out
    assert "tests/unit/test_pilot.py" in out  # the excluded-tests list
    assert "ANI-IN/harness-engineering-session" in out
    assert "git push origin main" in out
    assert "harness-frozen: not written (no freeze record in the build repository)" in out
    assert "class-v1 tag written at" in out and "refs/tags/class-v1" in out
    assert "refs/tags/harness-frozen" not in out
    assert "REFERENCES.md" in listing.read_text(encoding="utf-8").split()


def test_the_starter_kit_its_guide_and_the_slide_builder_ship() -> None:
    # Learners apply the kit to their own repositories (docs/apply-to-your-repo.md), and the public
    # Makefile's `make slides` runs scripts/build_slides.py on slides/deck.md.
    sel = mr.select(TRACKED)
    for path in [
        "kit/README.md",
        "kit/templates/AGENTS.md",
        "kit/examples/boltons-queueutils/README.md",
        "docs/apply-to-your-repo.md",
        "docs/extras.md",
        "scripts/build_slides.py",
        "slides/deck.md",
    ]:
        assert path in sel.included, path


def test_a_word_that_equals_a_script_stem_is_not_a_reference_to_the_script() -> None:
    # "pilot" is also a run purpose; only a path or a module name names scripts/pilot.py
    # (release candidate, 2026-10-17: tests/unit/ab/test_commands.py was left out for this).
    sources = {
        "tests/unit/test_purpose.py": 'PURPOSES = ("class", "pilot")\n',
        "tests/unit/test_path.py": 'SCRIPT = "scripts/pilot.py"\n',
        "tests/unit/test_module.py": "import scripts.pilot\n",
    }
    found = mr.find_excluded_tests(sources, ["scripts/pilot.py"], [])
    assert "tests/unit/test_purpose.py" not in found
    assert "tests/unit/test_path.py" in found
    assert "tests/unit/test_module.py" in found


def test_a_test_importing_an_excluded_test_module_is_excluded_with_it() -> None:
    sources = {
        "tests/unit/ab/test_shared.py": (
            'SCRIPT = "scripts/pilot.py"\n\ndef make_app():\n    pass\n'
        ),
        "tests/unit/ab/test_user.py": "from .test_shared import make_app\n",
    }
    found = mr.find_excluded_tests(sources, ["scripts/pilot.py"], [])
    assert "tests/unit/ab/test_user.py" in found


def test_the_slide_screenshots_ship_with_the_deck() -> None:
    # slides/deck.md embeds slides/img/*.png; without them `make slides` fails in the public repo.
    assert "slides/img/show-1-screen-1.png" in mr.select(TRACKED).included
