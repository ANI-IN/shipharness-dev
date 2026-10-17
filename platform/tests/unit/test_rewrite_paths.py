"""platform/scripts/rewrite_paths.py: links and path mentions follow the course-first layout."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from shipharness.layout import find_repo_root

REPO = find_repo_root(Path(__file__))
_spec = importlib.util.spec_from_file_location(
    "rewrite_paths", REPO / "platform" / "scripts" / "rewrite_paths.py"
)
assert _spec and _spec.loader
rp = importlib.util.module_from_spec(_spec)
sys.modules["rewrite_paths"] = rp
_spec.loader.exec_module(rp)

OLD = rp.OldTree(
    [
        "README.md",
        "CHANGELOG.md",
        "docs/setup-linux.md",
        "docs/troubleshooting.md",
        "docs/apply-to-your-repo.md",
        "setup/PRE-CLASS.md",
        "scripts/lint_prose.py",
        "src/shipharness/ab/referee.py",
        "kit/README.md",
        "skills/assured-tests/SKILL.md",
        "skills/assured-tests/scripts/run_testgen.py",
        "submodules/section-1-instructions/README.md",
        "submodules/section-1-instructions/assignment/README.md",
        "submodules/section-1-instructions/solution/README.md",
        "teamtrack/app/main.py",
    ]
)


def test_the_mapping_moves_folders_and_named_files() -> None:
    assert rp.map_path("submodules/section-1-instructions/solution/README.md") == (
        "section-1-instructions/assignment/solution/README.md"
    )
    assert (
        rp.map_path("submodules/section-1-instructions/concepts.md")
        == "section-1-instructions/concepts.md"
    )
    assert rp.map_path("src/shipharness/cli.py") == "platform/src/shipharness/cli.py"
    assert rp.map_path("teamtrack") == "platform/teamtrack"
    assert rp.map_path("skills/x/SKILL.md") == "use-in-your-repo/skills/x/SKILL.md"
    assert rp.map_path("docs/setup-macos.md") == "setup/macos.md"
    assert rp.map_path("setup/PRE-CLASS.md") == "setup/pre-class.md"
    assert rp.map_path("CHANGELOG.md") == "docs/CHANGELOG.md"
    assert rp.map_path("REFERENCES.md") == "docs/REFERENCES.md"
    assert rp.map_path("docs/troubleshooting.md") is None  # stays
    assert rp.old_location("section-1-instructions/assignment/solution/README.md") == (
        "submodules/section-1-instructions/solution/README.md"
    )
    assert rp.old_location("setup/linux.md") == "docs/setup-linux.md"


def test_links_are_recomputed_from_the_old_to_the_new_location() -> None:
    def link(target: str, old: str, new: str) -> str:
        return rp.rewrite_link(target, old, new, OLD)

    # a file that did not move, a target that moved
    assert link("docs/setup-linux.md#wsl", "README.md", "README.md") == "setup/linux.md#wsl"
    assert link("CHANGELOG.md", "README.md", "README.md") == "docs/CHANGELOG.md"
    # a file that moved, a target that did not
    assert (
        link(
            "../../README.md",
            "submodules/section-1-instructions/README.md",
            "section-1-instructions/README.md",
        )
        == "../README.md"
    )
    # both moved together: unchanged
    assert (
        link(
            "assignment/README.md",
            "submodules/section-1-instructions/README.md",
            "section-1-instructions/README.md",
        )
        == "assignment/README.md"
    )
    # solution/ moved one level deeper, next to starter/
    assert (
        link(
            "../assignment/README.md",
            "submodules/section-1-instructions/solution/README.md",
            "section-1-instructions/assignment/solution/README.md",
        )
        == "../README.md"
    )
    assert link("./", "README.md", "README.md") == "./"
    assert link("https://example.com/x.md", "README.md", "README.md") == "https://example.com/x.md"
    assert link("no-such-file.md", "README.md", "README.md") == "no-such-file.md"


def test_backtick_mentions_from_the_root_move_and_local_ones_stay() -> None:
    span = rp.rewrite_span("uv run python scripts/lint_prose.py", "README.md", OLD)
    assert span == "uv run python platform/scripts/lint_prose.py"
    assert rp.rewrite_span("src/shipharness/ab/referee.py:40-60", "README.md", OLD) == (
        "platform/src/shipharness/ab/referee.py:40-60"
    )
    assert (
        rp.rewrite_span("submodules/section-1-instructions/", "README.md", OLD)
        == "section-1-instructions/"
    )
    # a skill's own scripts/ folder is next to the document: unchanged
    skill = "skills/assured-tests/SKILL.md"
    assert rp.rewrite_span("scripts/run_testgen.py", skill, OLD) == "scripts/run_testgen.py"
    # not a tracked path: unchanged
    assert rp.rewrite_span("tests/visible/test_x.py", "README.md", OLD) == "tests/visible/test_x.py"


def test_rewrite_text_handles_links_spans_and_fenced_commands() -> None:
    text = (
        "See [setup](docs/setup-linux.md) and `scripts/lint_prose.py`.\n"
        "```\nuv run python scripts/lint_prose.py\nmake check-assignment-2 A2_IMPL=submodules/"
        "section-1-instructions/solution\n```\n"
    )
    out = rp.rewrite_text(text, "README.md", "README.md", OLD)
    assert "[setup](setup/linux.md)" in out
    assert "`platform/scripts/lint_prose.py`" in out
    assert "uv run python platform/scripts/lint_prose.py" in out
    assert "A2_IMPL=section-1-instructions/assignment/solution" in out


def test_the_link_check_reports_targets_that_do_not_exist(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(rp, "REPO", tmp_path)
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "ok.md").write_text("# ok\n", encoding="utf-8")
    (tmp_path / "a" / "doc.md").write_text(
        "[ok](ok.md) [gone](gone.md#x) ![img](img/none.png) `[code](x.md)`\n"
        "[refs](../docs/REFERENCES.md) [web](https://example.com) [top](#top)\n",
        encoding="utf-8",
    )
    assert rp.broken_links(["a/doc.md"]) == ["a/doc.md:1: gone.md#x", "a/doc.md:1: img/none.png"]


def test_a_code_span_of_backticks_is_not_a_fence_and_path_link_texts_move() -> None:
    text = (
        "Fences (```` ``` ```` or `~~~`) are ignored.\n"
        "See [docs/setup-linux.md](docs/setup-linux.md) and [skills/](skills/).\n"
    )
    out = rp.rewrite_text(text, "README.md", "README.md", OLD)
    assert "[setup/linux.md](setup/linux.md)" in out
    assert "[use-in-your-repo/skills/](use-in-your-repo/skills/)" in out


def test_bare_words_stay_and_command_path_arguments_move() -> None:
    def span(text: str) -> str:
        return rp.rewrite_span(text, "README.md", OLD)

    assert span("uv run shipharness skills validate skills") == (
        "uv run shipharness skills validate use-in-your-repo/skills"
    )
    assert span("make datasets") == "make datasets"
    assert span("visible tests") == "visible tests"
    assert span("update_status(document, end, sandbox, now)") == (
        "update_status(document, end, sandbox, now)"
    )
    assert span("assess.py teamtrack --out x.html") == "assess.py platform/teamtrack --out x.html"
    assert span("shipharness check --app teamtrack --rules R6") == (
        "shipharness check --app platform/teamtrack --rules R6"
    )
    assert span("CHANGELOG.md") == "docs/CHANGELOG.md"
