"""Hidden tests: the history rule against agent-style and harness commands.

test_rule_denies_*: refused before running, reason write_outside_workspace.
test_rule_allows_*: no false positives, including every git command the harness itself runs in
the sandbox, and the default network rules still decide network commands first.
"""

from __future__ import annotations

import pytest

from shipharness.harness.state.commit import commit_command
from shipharness.runner.loop import SETUP_COMMIT
from shipharness.runner.tools import PATCH_FILE
from shipharness.sandbox import FakeSandbox, check_command

DENIED = [
    "git reset --hard",
    "git reset --soft HEAD^",
    "git reset HEAD~2",
    "git reset --mixed 3f2a9c1",
    "git reset ORIG_HEAD",
    "git -C /work reset --hard HEAD~1",
    "git -c user.name=agent -c user.email=a@example.invalid commit --amend -m 'F3 done'",
    "git commit -a --amend --no-edit",
    "git rebase --onto main HEAD~2",
    "git rebase -i --root",
    "cd /work && git rebase main",
    "git update-ref refs/heads/main HEAD~1",
    "git filter-branch --tree-filter 'rm -f feature_list.json' HEAD",
    "git reflog expire --expire=now --all && git gc --prune=now",
    "git branch -D main",
    "git branch -f main HEAD~1",
    "git checkout --orphan clean-history",
    "git switch --orphan fresh",
    "rm -rf ./.git",
    "rm -rf /work/.git",
    "mv .git /tmp/old-git",
    "echo 0000000000000000000000000000000000000000 > .git/refs/heads/main",
    "GIT_DIR=.git git reset --hard HEAD~1",
    "/usr/bin/git reset --hard",
    "git status; git reset --hard HEAD~1",
    "git replace HEAD HEAD~1",
    "python -m pytest -q || git reset --hard",
    "git --no-pager commit --amend --no-edit",
]

NETWORK = [
    "pip install requests",
    "curl -s https://pypi.org/simple/",
    "git push --force origin main",
    "uv add httpx",
]

ALLOWED = [
    SETUP_COMMIT,
    commit_command(["feature_list.json", "feature_list.schema.json"], "harness: F3 passes"),
    commit_command(["progress.md", "session-handoff.md"], "harness: session 2 handoff"),
    f"git apply --check -p1 --whitespace=nowarn {PATCH_FILE}",
    f"git apply -p0 --whitespace=nowarn {PATCH_FILE}",
    "git status --porcelain --untracked-files=all",
    "git diff --name-only --diff-filter=AM 1a2b3c4d5e6f -- '*.py'",
    "git diff -U0 1a2b3c4 -- '*.py' ':(exclude)tests/**'",
    "git add -A tests/visible && git commit -q -m 'test: keep 3 tests that passed' || true",
    "git log --oneline --no-decorate --no-color -5",
    "git show HEAD~1:app/services/issues.py",
    "git revert --no-edit HEAD",
    "git restore --staged app/api/issues.py",
    "git restore app/api/issues.py",
    "git stash && python -m pytest tests/visible -q && git stash pop",
    "git reset",
    "git reset HEAD app/api/issues.py",
    "git reset -q -- tests/visible/test_f3.py",
    "git branch",
    "git branch f3-retry",
    "git switch -c f3-retry",
    "git checkout -b f3-retry",
    "git checkout HEAD~2 -- app/services/issues.py",
    "git log --grep=rebase --oneline",
    "git log --grep=amend",
    'git commit -m "docs: explain the reset to defaults"',
    "git cherry-pick 1a2b3c4",
    "git tag f3-done",
    "git rm --cached app/tmp.py",
    "git mv app/api/issues.py app/api/issue_routes.py",
    "git diff --stat HEAD~3..HEAD",
    "rm -rf .github/workflows",
    "rm .gitignore",
    "cat .git/HEAD",
    "ls -la .git",
    "rm -rf build .pytest_cache __pycache__",
    'grep -rn "git rebase" docs/',
    'echo "never run git reset --hard" >> progress.md',
    "python -c \"print('git reset --hard')\"",
    "alembic upgrade head",
    "python -m pytest tests/visible -q -k reset",
    "sed -n '1,40p' app/services/issues.py",
]


@pytest.mark.parametrize("command", DENIED)
def test_rule_denies_history_rewrite(command: str) -> None:
    from a3scope.policy import policy
    from a3scope.sandbox import PolicySandbox

    inner = FakeSandbox()
    result = PolicySandbox(policy(), inner).exec(command, timeout_s=30)
    assert result.denied is not None, f"not denied: {command}"
    assert result.denied.reason_code == "write_outside_workspace"
    assert inner.commands == []


@pytest.mark.parametrize("command", NETWORK)
def test_rule_allows_default_rules_to_decide_first(command: str) -> None:
    from a3scope.policy import policy

    denial = check_command(policy(), command)
    assert denial is not None and denial.reason_code == "network"


@pytest.mark.parametrize("command", ALLOWED)
def test_rule_allows_command(command: str) -> None:
    from a3scope.policy import policy

    assert check_command(policy(), command) is None, f"false positive: {command}"


def test_rule_denies_every_pattern_compiles_and_shares_the_message() -> None:
    import re

    from a3scope.policy import HISTORY_RULES

    assert HISTORY_RULES
    for rule in HISTORY_RULES:
        re.compile(rule.pattern)
    assert len({r.message for r in HISTORY_RULES}) == 1
    assert {r.reason_code for r in HISTORY_RULES} == {"write_outside_workspace"}
