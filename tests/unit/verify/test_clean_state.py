from __future__ import annotations

from collections.abc import Callable

from shipharness.harness.verify.clean_state import clean_state_check
from shipharness.sandbox import ExecResult, FakeSandbox

from .fakes import fail, ok

BASE = "a" * 40
DIFF_PRINT = """diff --git a/app/api/x.py b/app/api/x.py
--- a/app/api/x.py
+++ b/app/api/x.py
@@ -1,0 +2,2 @@
+    print("debug", items)
+    return items
"""


def scripted(**overrides: ExecResult) -> Callable[[str], ExecResult]:
    defaults = {
        "status": ok(""),
        "names": ok(""),
        "ruff": ok(""),
        "heads": ok("abc123 (head)\n"),
        "diff": ok(""),
    }
    defaults.update(overrides)

    def script(command: str) -> ExecResult:
        if command.startswith("git status"):
            return defaults["status"]
        if command.startswith("git diff --name-only"):
            return defaults["names"]
        if command.startswith("ruff"):
            return defaults["ruff"]
        if command.startswith("alembic"):
            return defaults["heads"]
        if command.startswith("git diff -U0"):
            return defaults["diff"]
        raise AssertionError(f"unexpected command {command}")

    return script


def test_clean_workspace_passes() -> None:
    item = clean_state_check(FakeSandbox(scripted()), BASE)
    assert item.name == "clean state"
    assert item.status == "pass"


def test_uncommitted_changes_fail_but_generated_files_are_ignored() -> None:
    status = ok("?? app/new.py\n M app/main.py\n?? .pytest_cache/v/x\n?? app/__pycache__/a.pyc\n")
    item = clean_state_check(FakeSandbox(scripted(status=status)), BASE)
    assert item.status == "fail"
    assert "uncommitted changes: app/new.py, app/main.py" in item.detail
    assert "pytest_cache" not in item.detail


def test_ruff_problems_in_changed_files_fail() -> None:
    sandbox = FakeSandbox(
        scripted(
            names=ok("app/api/x.py\n"),
            ruff=fail("app/api/x.py:3:1: F401 `os` imported but unused\nFound 1 error.\n"),
        )
    )
    item = clean_state_check(sandbox, BASE)
    assert item.status == "fail"
    assert "ruff" in item.detail and "F401" in item.detail
    assert any(c.startswith("ruff check") and "app/api/x.py" in c for c in sandbox.commands)


def test_ruff_is_not_run_when_no_python_file_changed() -> None:
    sandbox = FakeSandbox(scripted())
    clean_state_check(sandbox, BASE)
    assert not any(c.startswith("ruff") for c in sandbox.commands)


def test_two_migration_heads_fail() -> None:
    heads = ok("abc123 (head)\ndef456 (head)\n")
    item = clean_state_check(FakeSandbox(scripted(heads=heads)), BASE)
    assert item.status == "fail"
    assert "migration heads: 2" in item.detail


def test_added_print_in_source_fails_as_debug_output() -> None:
    item = clean_state_check(FakeSandbox(scripted(diff=ok(DIFF_PRINT))), BASE)
    assert item.status == "fail"
    assert "debug output: app/api/x.py" in item.detail


def test_changed_file_names_from_the_agent_are_quoted() -> None:
    sandbox = FakeSandbox(scripted(names=ok("app/x.py; touch /tmp/pwn.py\n")))
    clean_state_check(sandbox, BASE)
    [ruff] = [c for c in sandbox.commands if c.startswith("ruff")]
    assert "'app/x.py; touch /tmp/pwn.py'" in ruff


def test_without_a_base_commit_only_status_and_heads_are_checked() -> None:
    sandbox = FakeSandbox(scripted())
    item = clean_state_check(sandbox, "")
    assert item.status == "pass"
    assert not any(c.startswith("git diff") for c in sandbox.commands)
