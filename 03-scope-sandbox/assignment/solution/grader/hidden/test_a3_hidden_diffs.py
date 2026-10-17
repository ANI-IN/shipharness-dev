"""Hidden scripted diffs (make_hidden.py): every bad diff rejected, every good diff accepted."""

from __future__ import annotations

from pathlib import Path

import pytest
from a3_checks import assert_accepted, assert_changed_paths, assert_rejected, load_cases

CASES = load_cases(Path(__file__).resolve().parent)
BAD = [c for c in CASES if c["kind"] == "bad"]
GOOD = [c for c in CASES if c["kind"] == "good"]
WITH_PATHS = [c for c in CASES if "changed" in c]


@pytest.mark.parametrize("case", WITH_PATHS, ids=[c["id"] for c in WITH_PATHS])
def test_parse_changed_paths(case) -> None:  # type: ignore[no-untyped-def]
    assert_changed_paths(case)


@pytest.mark.parametrize("case", BAD, ids=[c["id"] for c in BAD])
def test_bad_diff_rejected(case) -> None:  # type: ignore[no-untyped-def]
    assert_rejected(case)


@pytest.mark.parametrize("case", GOOD, ids=[c["id"] for c in GOOD])
def test_good_diff_accepted(case) -> None:  # type: ignore[no-untyped-def]
    assert_accepted(case)


def _case(case_id: str) -> bytes:
    return next(c["diff"] for c in CASES if c["id"] == case_id)


def test_parse_quoted_name_is_unquoted() -> None:
    from a3scope.diffparse import parse_diff

    (change,) = parse_diff(_case("bad-quoted-non-ascii-path"))
    assert change.new_path == "docs/café.md" and change.status == "modified"


def test_parse_git_binary_patch_is_binary_and_ends_the_section() -> None:
    from a3scope.diffparse import parse_diff

    changes = parse_diff(_case("bad-git-binary-patch"))
    assert [(c.new_path, c.binary) for c in changes] == [("app/static/logo.png", True)]


def test_parse_empty_new_file_from_header_only() -> None:
    from a3scope.diffparse import FileChange, parse_diff

    assert parse_diff(_case("good-dir-name-contains-b-slash")) == [
        FileChange(old_path=None, new_path="tests/visible/x b/__init__.py", status="added")
    ]


def test_parse_header_like_lines_inside_hunks_are_content() -> None:
    from a3scope.diffparse import parse_diff

    changes = parse_diff(_case("good-hand-written-header-like-lines"))
    assert [(c.old_path, c.new_path, c.status) for c in changes] == [
        ("app/services/issues.py", "app/services/issues.py", "modified"),
        ("docs/HANDBOOK.md", "docs/HANDBOOK.md", "modified"),
    ]


def test_parse_deleted_file_and_mode_change() -> None:
    from a3scope.diffparse import parse_diff

    (deleted,) = parse_diff(_case("bad-delete-migration"))
    assert (deleted.old_path, deleted.new_path, deleted.status) == (
        "migrations/versions/0007_add_idempotency.py",
        None,
        "deleted",
    )
    (mode,) = parse_diff(_case("bad-mode-change-only"))
    assert (mode.old_path, mode.new_path, mode.status) == (
        "scripts/deploy.sh",
        "scripts/deploy.sh",
        "modified",
    )


def test_parse_form_feed_in_content_does_not_split_lines() -> None:
    from a3scope.diffparse import changed_paths, parse_diff

    diff = (
        "--- a/app/api/issues.py\n+++ b/app/api/issues.py\n@@ -1,2 +1,2 @@\n"
        " # section\x0c break\n-x = 1\n+x = 2\n"
        "--- a/app/core/config.py\n+++ b/app/core/config.py\n@@ -1 +1 @@\n-A = 1\n+A = 2\n"
    )
    assert changed_paths(parse_diff(diff)) == ["app/api/issues.py", "app/core/config.py"]


def test_bad_crlf_patch_still_finds_the_out_of_scope_file() -> None:
    from a3scope.scope import PhasePolicy, check_diff

    diff = (
        "--- a/app/api/issues.py\r\n+++ b/app/api/issues.py\r\n@@ -1 +1 @@\r\n-a\r\n+b\r\n"
        "--- a/app/core/config.py\r\n+++ b/app/core/config.py\r\n@@ -1 +1 @@\r\n-A\r\n+B\r\n"
    )
    verdict = check_diff(PhasePolicy(allowed_paths={"build": ["app/api/issues.py"]}), "build", diff)
    assert [(r.path, r.code) for r in verdict.refusals] == [
        ("app/core/config.py", "outside_allowed_paths")
    ]


def test_good_commit_message_preamble_is_ignored() -> None:
    from a3scope.scope import PhasePolicy, check_diff

    diff = (
        "From 1a2b3c4 Mon Sep 17 00:00:00 2001\nSubject: [PATCH] F3 replay\n\n---\n"
        " app/api/issues.py | 2 +-\n 1 file changed\n\n"
        "diff --git a/app/api/issues.py b/app/api/issues.py\n"
        "--- a/app/api/issues.py\n+++ b/app/api/issues.py\n@@ -1 +1 @@\n-a\n+b\n"
    )
    verdict = check_diff(PhasePolicy(allowed_paths={"build": ["app/api/issues.py"]}), "build", diff)
    assert verdict.accepted is True
