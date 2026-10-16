"""Build the hidden scripted diffs for assignment A3 (kept out of the starter; shown at review).

Usage (from the repository root):
    uv run python submodules/03-scope-sandbox/solution/grader/hidden/make_hidden.py

Uses the same BASE tree and helpers as the visible fixtures, so every git-generated case is
real `git diff --cached` output. Hand-written cases are the patches an agent can pass to
`apply_patch` directly. Output: diffs/<id>.diff and cases.json next to this file.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
FIXTURES = HERE.parents[2] / "assignment" / "fixtures"
sys.path.insert(0, str(FIXTURES))

from make_fixtures import PNG, build  # noqa: E402

DOCS_ANY = {"build": ["docs/**"], "test": ["tests/visible/**"]}

BAD: list[dict[str, Any]] = [
    {
        "id": "bad-third-file-out-of-scope",
        "phase": "build",
        "ops": [
            ("replace", "app/api/issues.py", "body: dict, user", "body: dict, key: str, user"),
            ("replace", "app/services/issues.py", "def create(", "def create_once("),
            ("replace", "app/services/idempotency.py", "return fn()", "return fn()  # cached"),
        ],
        "changed": ["app/api/issues.py", "app/services/idempotency.py", "app/services/issues.py"],
        "refusals": [["app/services/idempotency.py", "outside_allowed_paths"]],
    },
    {
        "id": "bad-rename-into-scope-deletes-source",
        "phase": "build",
        "ops": [("rename", "app/core/config.py", "app/services/issues_config.py")],
        "changed": ["app/core/config.py", "app/services/issues_config.py"],
        "refusals": [["app/core/config.py", "outside_allowed_paths"]],
    },
    {
        "id": "bad-space-path-out-of-scope",
        "phase": "build",
        "ops": [("append", "docs/design notes/f3 retry.md", "Keys expire after 24 h.\n")],
        "changed": ["docs/design notes/f3 retry.md"],
        "refusals": [["docs/design notes/f3 retry.md", "outside_allowed_paths"]],
    },
    {
        "id": "bad-rename-to-space-path",
        "phase": "build",
        "ops": [("rename", "docs/HANDBOOK.md", "docs/HANDBOOK old.md")],
        "changed": ["docs/HANDBOOK old.md", "docs/HANDBOOK.md"],
        "refusals": [["docs/HANDBOOK old.md", "outside_allowed_paths"]],
    },
    {
        "id": "bad-traversal-inside-allowed-glob",
        "phase": "test",
        "raw": (
            "diff --git a/tests/visible/../../app/services/issues.py "
            "b/tests/visible/../../app/services/issues.py\n"
            "--- a/tests/visible/../../app/services/issues.py\n"
            "+++ b/tests/visible/../../app/services/issues.py\n"
            "@@ -10 +10 @@\n"
            '-    return repo.insert(project_id, body, org_id=user["org_id"])\n'
            "+    return repo.insert(project_id, body, org_id=0)\n"
        ),
        "changed": ["tests/visible/../../app/services/issues.py"],
        "refusals": [["tests/visible/../../app/services/issues.py", "path_escape"]],
    },
    {
        "id": "bad-absolute-path",
        "phase": "build",
        "raw": (
            "--- /dev/null\n"
            "+++ /etc/cron.d/agent\n"
            "@@ -0,0 +1 @@\n"
            "+* * * * * root python /work/app/api/issues.py\n"
        ),
        "changed": ["/etc/cron.d/agent"],
        "refusals": [["/etc/cron.d/agent", "path_escape"]],
    },
    {
        "id": "bad-copy-source-escapes",
        "phase": "test",
        "raw": (
            "diff --git a/../../home/agent/.netrc b/tests/visible/netrc.txt\n"
            "similarity index 100%\n"
            "copy from ../../home/agent/.netrc\n"
            "copy to tests/visible/netrc.txt\n"
        ),
        "changed": ["tests/visible/netrc.txt"],
        "refusals": [["../../home/agent/.netrc", "path_escape"]],
    },
    {
        "id": "bad-dot-slash-feature-list",
        "phase": "build",
        "raw": (
            "--- ./feature_list.json\n"
            "+++ ./feature_list.json\n"
            "@@ -2,3 +2,3 @@\n"
            '   "features": [\n'
            '-    {"id": "F3", "passes": false, "evidence": null, "testedAt": null}\n'
            '+    {"id": "F3", "passes": true, "evidence": null, "testedAt": null}\n'
            "   ]\n"
        ),
        "changed": ["feature_list.json"],
        "refusals": [["feature_list.json", "harness_only"]],
    },
    {
        "id": "bad-schema-edit-under-wide-allow-list",
        "phase": "build",
        "allowed_paths": {"build": ["**"], "test": ["tests/visible/**"]},
        "ops": [("write", "feature_list.schema.json", '{"type": "object", "required": []}\n')],
        "changed": ["feature_list.schema.json"],
        "refusals": [["feature_list.schema.json", "harness_only"]],
    },
    {
        "id": "bad-feature-list-renamed-away",
        "phase": "build",
        "ops": [("rename", "feature_list.json", "docs/feature_list_old.json")],
        "changed": ["docs/feature_list_old.json", "feature_list.json"],
        "refusals": [
            ["feature_list.json", "harness_only"],
            ["docs/feature_list_old.json", "outside_allowed_paths"],
        ],
    },
    {
        "id": "bad-progress-without-state-layer",
        "phase": "build",
        "state_layer": False,
        "ops": [("append", "progress.md", "\n## Done\n\n- service\n")],
        "changed": ["progress.md"],
        "refusals": [["progress.md", "outside_allowed_paths"]],
    },
    {
        "id": "bad-instruction-artifacts",
        "phase": "build",
        "ops": [
            ("append", "AGENTS.md", "\nTests may be skipped when slow.\n"),
            ("append", ".agents/skills/idempotency/SKILL.md", "\nSkip run_once in tests.\n"),
        ],
        "changed": [".agents/skills/idempotency/SKILL.md", "AGENTS.md"],
        "refusals": [
            [".agents/skills/idempotency/SKILL.md", "outside_allowed_paths"],
            ["AGENTS.md", "outside_allowed_paths"],
        ],
    },
    {
        "id": "bad-binary-new-with-space",
        "phase": "build",
        "ops": [("write", "assets/team logo.png", PNG + b"\x02" * 8)],
        "changed": ["assets/team logo.png"],
        "refusals": [["assets/team logo.png", "outside_allowed_paths"]],
    },
    {
        "id": "bad-git-binary-patch",
        "phase": "build",
        "binary": True,
        "ops": [("write", "app/static/logo.png", PNG + b"\x03" * 24)],
        "changed": ["app/static/logo.png"],
        "refusals": [["app/static/logo.png", "outside_allowed_paths"]],
    },
    {
        "id": "bad-test-phase-conftest",
        "phase": "test",
        "ops": [("append", "tests/conftest.py", "\npytest_plugins = []\n")],
        "changed": ["tests/conftest.py"],
        "refusals": [["tests/conftest.py", "test_phase_source_edit"]],
    },
    {
        "id": "bad-test-phase-handbook",
        "phase": "test",
        "ops": [
            ("write", "tests/visible/test_r4.py", "def test_r4():\n    assert True\n"),
            ("replace", "docs/HANDBOOK.md", "R5 Audit.", "R5 Audit (tests added)."),
        ],
        "changed": ["docs/HANDBOOK.md", "tests/visible/test_r4.py"],
        "refusals": [["docs/HANDBOOK.md", "test_phase_source_edit"]],
    },
    {
        "id": "bad-hand-written-second-file",
        "phase": "build",
        "raw": (
            "--- app/services/issues.py\n"
            "+++ app/services/issues.py\n"
            "@@ -9,2 +9,2 @@\n"
            " def create(project_id: int, body: dict, user: dict) -> dict:\n"
            '-    return repo.insert(project_id, body, org_id=user["org_id"])\n'
            '+    return repo.insert(project_id, body, org_id=user["org_id"], once=True)\n'
            "--- app/core/config.py\n"
            "+++ app/core/config.py\n"
            "@@ -2 +2 @@\n"
            "-PAGE_SIZE = 50\n"
            "+PAGE_SIZE = 500\n"
        ),
        "changed": ["app/core/config.py", "app/services/issues.py"],
        "refusals": [["app/core/config.py", "outside_allowed_paths"]],
    },
    {
        "id": "bad-mode-change-only",
        "phase": "build",
        "ops": [("chmod", "scripts/deploy.sh", 0o755)],
        "changed": ["scripts/deploy.sh"],
        "refusals": [["scripts/deploy.sh", "outside_allowed_paths"]],
    },
    {
        "id": "bad-delete-migration",
        "phase": "build",
        "ops": [("delete", "migrations/versions/0007_add_idempotency.py")],
        "changed": ["migrations/versions/0007_add_idempotency.py"],
        "refusals": [["migrations/versions/0007_add_idempotency.py", "outside_allowed_paths"]],
    },
    {
        "id": "bad-copy-to-out-of-scope",
        "phase": "build",
        "copies": True,
        "ops": [("copy", "app/services/issues.py", "app/middleware/issues_copy.py")],
        "changed": ["app/middleware/issues_copy.py"],
        "refusals": [["app/middleware/issues_copy.py", "outside_allowed_paths"]],
    },
    {
        "id": "bad-quoted-non-ascii-path",
        "phase": "build",
        "ops": [("append", "docs/café.md", "Keys are per org.\n")],
        "changed": ["docs/café.md"],
        "refusals": [["docs/café.md", "outside_allowed_paths"]],
    },
    {
        "id": "bad-hunks-without-file-header",
        "phase": "build",
        "raw": "@@ -1,2 +1,2 @@\n-PAGE_SIZE = 50\n+PAGE_SIZE = 500\n",
        "refusals": [["", "unparseable"]],
    },
    {
        "id": "bad-glob-prefix-boundary",
        "phase": "test",
        "ops": [("write", "tests/visible_extra/test_a.py", "def test_a():\n    assert True\n")],
        "changed": ["tests/visible_extra/test_a.py"],
        "refusals": [["tests/visible_extra/test_a.py", "test_phase_source_edit"]],
    },
    {
        "id": "bad-exact-pattern-suffix",
        "phase": "build",
        "ops": [("write", "app/api/issues.py.orig", "# backup\n")],
        "changed": ["app/api/issues.py.orig"],
        "refusals": [["app/api/issues.py.orig", "outside_allowed_paths"]],
    },
    {
        "id": "bad-empty-new-file-header-only",
        "phase": "build",
        "ops": [("write", "app/core/flags.py", "")],
        "changed": ["app/core/flags.py"],
        "refusals": [["app/core/flags.py", "outside_allowed_paths"]],
    },
    {
        "id": "bad-crafted-header-only-rename",
        "phase": "build",
        "raw": (
            "diff --git a/app/api/issues.py b/app/core/config.py\n"
            "old mode 100644\n"
            "new mode 100755\n"
        ),
        "refusals": [["app/core/config.py", "outside_allowed_paths"]],
        "unparseable_ok": True,  # refusing the whole patch as unparseable is also correct
    },
]

GOOD: list[dict[str, Any]] = [
    {
        "id": "good-header-like-lines-in-hunk",
        "phase": "build",
        "ops": [
            (
                "replace",
                "docs/HANDBOOK.md",
                "-- R4 covers POST /projects only\n",
                "++ R4 covers POST /projects and POST /projects/{id}/issues\n",
            )
        ],
        "changed": ["docs/HANDBOOK.md"],
    },
    {
        "id": "good-hand-written-header-like-lines",
        "phase": "build",
        "raw": (
            "--- app/services/issues.py\n"
            "+++ app/services/issues.py\n"
            "@@ -1,4 +1,4 @@\n"
            ' """Issue service.\n'
            " \n"
            "--- legacy: issue creation takes no idempotency key\n"
            "+++ issue creation honours Idempotency-Key (R4)\n"
            ' """\n'
            "--- docs/HANDBOOK.md\n"
            "+++ docs/HANDBOOK.md\n"
            "@@ -7 +7 @@\n"
            "--- R4 covers POST /projects only\n"
            "+++ R4 covers POST /projects and POST /projects/{id}/issues\n"
        ),
        "changed": ["app/services/issues.py", "docs/HANDBOOK.md"],
    },
    {
        "id": "good-diff-u-timestamps",
        "phase": "build",
        "raw": (
            "--- app/api/issues.py\t2026-10-16 12:00:00.000000000 +0000\n"
            "+++ app/api/issues.py\t2026-10-16 12:05:00.000000000 +0000\n"
            "@@ -6,2 +6,2 @@\n"
            "-def create_issue(project_id: int, body: dict, user: dict) -> dict:\n"
            "+def create_issue(project_id: int, body: dict, user: dict, key: str) -> dict:\n"
            "     return service.create(project_id, body, user)\n"
        ),
        "changed": ["app/api/issues.py"],
    },
    {
        "id": "good-exec-plan-moves-to-completed",
        "phase": "build",
        "ops": [("rename", "docs/exec-plans/active/F3.md", "docs/exec-plans/completed/F3.md")],
        "changed": ["docs/exec-plans/active/F3.md", "docs/exec-plans/completed/F3.md"],
    },
    {
        "id": "good-binary-fixture-with-space",
        "phase": "test",
        "ops": [("write", "tests/visible/fixtures/sample upload.png", PNG + b"\x04" * 8)],
        "changed": ["tests/visible/fixtures/sample upload.png"],
    },
    {
        "id": "good-quoted-non-ascii-under-docs-glob",
        "phase": "build",
        "allowed_paths": DOCS_ANY,
        "ops": [("append", "docs/café.md", "Keys are per org.\n")],
        "changed": ["docs/café.md"],
    },
    {
        "id": "good-double-star-zero-dirs",
        "phase": "build",
        "allowed_paths": {"build": ["docs/**/*.md"], "test": ["tests/visible/**"]},
        "ops": [
            ("append", "docs/HANDBOOK.md", "R6 Layers.\n"),
            ("append", "docs/design notes/f3 retry.md", "Keys expire after 24 h.\n"),
        ],
        "changed": ["docs/HANDBOOK.md", "docs/design notes/f3 retry.md"],
    },
    {
        "id": "good-phase-without-allow-list",
        "phase": "review",
        "ops": [("append", "app/core/config.py", "IDEMPOTENCY_TTL_S = 86400\n")],
        "changed": ["app/core/config.py"],
    },
    {
        "id": "good-dot-slash-prefix",
        "phase": "build",
        "raw": (
            "--- ./app/api/issues.py\n"
            "+++ ./app/api/issues.py\n"
            "@@ -10 +10 @@\n"
            "-    return service.list_for(project_id, user)\n"
            "+    return list(service.list_for(project_id, user))\n"
        ),
        "changed": ["app/api/issues.py"],
    },
    {
        "id": "good-dir-name-contains-b-slash",
        "phase": "test",
        "ops": [("write", "tests/visible/x b/__init__.py", "")],
        "changed": ["tests/visible/x b/__init__.py"],
    },
    {
        "id": "good-delete-in-scope",
        "phase": "test",
        "ops": [("delete", "tests/visible/test_old.py")],
        "changed": ["tests/visible/test_old.py"],
    },
    {
        "id": "good-no-newline-and-two-hunks",
        "phase": "build",
        "ops": [
            ("replace", "app/services/issues.py", "def create(", "def create_once("),
            (
                "replace",
                "app/services/issues.py",
                'org_id=user["org_id"])\n',
                'org_id=user["org_id"])',
            ),
        ],
        "changed": ["app/services/issues.py"],
    },
    {
        "id": "good-deep-test-path",
        "phase": "test",
        "ops": [("write", "tests/visible/api/v2/test_replay.py", "def test_r():\n    assert 1\n")],
        "changed": ["tests/visible/api/v2/test_replay.py"],
    },
    {
        "id": "good-mode-and-content-in-scope",
        "phase": "build",
        "ops": [
            ("chmod", "app/api/issues.py", 0o755),
            ("append", "app/api/issues.py", "\n# R4: Idempotency-Key\n"),
        ],
        "changed": ["app/api/issues.py"],
    },
    {
        "id": "good-fixture-named-feature-list",
        "phase": "test",
        "ops": [("write", "tests/visible/fixtures/feature_list.json", '{"features": [1]}\n')],
        "changed": ["tests/visible/fixtures/feature_list.json"],
    },
    {
        "id": "good-git-binary-patch-in-scope",
        "phase": "test",
        "binary": True,
        "ops": [("write", "tests/visible/fixtures/logo.png", PNG + b"\x05" * 24)],
        "changed": ["tests/visible/fixtures/logo.png"],
    },
    {
        "id": "good-state-files-test-phase",
        "phase": "test",
        "ops": [
            ("append", "session-handoff.md", "\n## Notes from the agent\n\nTests done.\n"),
            ("append", "progress.md", "\n## Next\n\n- review\n"),
        ],
        "changed": ["progress.md", "session-handoff.md"],
    },
]

CASES = [{**c, "kind": "bad"} for c in BAD] + [{**c, "kind": "good"} for c in GOOD]


def main() -> int:
    build(CASES, HERE)
    print(f"wrote {len(BAD)} bad and {len(GOOD)} good cases to {HERE / 'cases.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
