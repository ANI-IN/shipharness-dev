from __future__ import annotations

import pytest

from shipharness.ab.artifacts import (
    HARNESS_ARTIFACT_PATTERNS,
    diff_paths,
    is_harness_artifact,
    strip_harness_artifacts,
)


def section(path: str, body: str = "+x\n", old: str | None = None) -> str:
    old = old or path
    return (
        f"diff --git a/{old} b/{path}\n"
        f"index 111..222 100644\n--- a/{old}\n+++ b/{path}\n@@ -1 +1 @@\n{body}"
    )


def new_file(path: str) -> str:
    return (
        f"diff --git a/{path} b/{path}\nnew file mode 100644\nindex 0000000..1111111\n"
        f"--- /dev/null\n+++ b/{path}\n@@ -0,0 +1 @@\n+hello\n"
    )


@pytest.mark.parametrize(
    "path",
    [
        "AGENTS.md",
        "ARCHITECTURE.md",
        "docs/SECURITY.md",
        "docs/RELIABILITY.md",
        "docs/QUALITY_SCORE.md",
        "docs/PLANS.md",
        "docs/design-docs/core-beliefs.md",
        "docs/product-specs/index.md",
        "docs/references/fastapi-llms.txt",
        ".agents/skills/add-endpoint/SKILL.md",
        "init.sh",
        "progress.md",
        "session-handoff.md",
        "docs/exec-plans/active/F1.md",
        "docs/exec-plans/completed/F1.md",
        "feature_list.json",
        "feature_list.schema.json",
    ],
)
def test_harness_artifacts_are_recognised(path: str) -> None:
    assert is_harness_artifact(path)


@pytest.mark.parametrize(
    "path",
    ["app/api/issues.py", "docs/HANDBOOK.md", "tests/visible/test_x.py", "app/AGENTS.md.py"],
)
def test_product_files_are_not_artifacts(path: str) -> None:
    assert not is_harness_artifact(path)


def test_patterns_constant_is_a_tuple_of_strings() -> None:
    assert isinstance(HARNESS_ARTIFACT_PATTERNS, tuple)
    assert all(isinstance(p, str) for p in HARNESS_ARTIFACT_PATTERNS)


def test_strip_keeps_only_product_changes() -> None:
    diff = (
        section("app/api/issues.py")
        + new_file("progress.md")
        + section("docs/exec-plans/active/F1.md")
        + new_file("tests/visible/test_new.py")
    )
    stripped = strip_harness_artifacts(diff)
    assert diff_paths(stripped) == ["app/api/issues.py", "tests/visible/test_new.py"]
    assert "progress.md" not in stripped


def test_strip_works_on_bytes_and_keeps_binary_sections() -> None:
    binary = (
        b"diff --git a/app/logo.png b/app/logo.png\nnew file mode 100644\n"
        b"index 0000000..1111111\nGIT binary patch\nliteral 3\nKcmZ?\xff\n\nliteral 0\n\n"
    )
    diff = section("AGENTS.md").encode() + binary
    stripped = strip_harness_artifacts(diff)
    assert isinstance(stripped, bytes)
    assert stripped == binary


def test_rename_from_product_file_to_artifact_is_kept() -> None:
    diff = section("AGENTS.md", old="app/api/issues.py")
    assert strip_harness_artifacts(diff) == diff


def test_quoted_paths_are_parsed() -> None:
    diff = (
        'diff --git "a/app/sp ace.py" "b/app/sp ace.py"\n'
        '--- "a/app/sp ace.py"\n+++ "b/app/sp ace.py"\n'
    )
    assert diff_paths(diff) == ["app/sp ace.py"]
