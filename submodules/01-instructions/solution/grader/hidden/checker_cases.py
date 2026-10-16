"""Hidden cases for the learner's check_docs.py (assignment A1, grading criterion D).

Each case is a small original file, a tree, and a product folder. The grader runs the learner's
checker as a command on the case and compares the set of (kind, key) pairs from its `ERROR` lines,
and its exit code, with the expected values. Every case follows the specification in the
assignment README ("Detailed requirements"); none tests behaviour the README does not state.
Kept out of the starter so that learners test their checker against the specification, not
against these fixtures.
"""

from __future__ import annotations

from dataclasses import dataclass, field

ORIGINAL = """# Rules

- [R1.1] Every query on customer data filters by the caller's `org_id`.
- [R2.1] Viewers can read but never write: every POST, PUT, PATCH, and DELETE
  returns 403 forbidden for a viewer.
- [R2.2] Creating and updating users is admin-only.
- [R2.5] (retired 2024-11, superseded by R2.2) Members may archive projects.
- [CV-02] Prefer small pull requests that touch only the files a feature needs.
"""

DOCS = """# Security

## Tenant isolation

- [R1.1] Every query on customer data filters by the caller's `org_id`.

## Roles

- [R2.1] Viewers can read but never write: every POST, PUT, PATCH, and DELETE returns 403
  forbidden for a viewer.
- [R2.2] Creating and updating users is admin-only.

## Scope

- [CV-02] Prefer small pull requests that touch only the files a feature needs.
"""

PRODUCT = {
    "app/api/deps.py": "",
    "alembic.ini": "",
    "migrations/versions/0001_initial.py": "",
    "docs/features/f1.md": "# F1\n\n## Scope\n",
}


@dataclass(frozen=True)
class Case:
    name: str
    tree: dict[str, str]
    expected: frozenset[tuple[str, str]]
    exit_code: int
    original: str = ORIGINAL
    product: dict[str, str] = field(default_factory=lambda: dict(PRODUCT))
    tree_missing: bool = False


def _case(name: str, tree: dict[str, str], expected: set[tuple[str, str]], **kw: object) -> Case:
    code = kw.pop("exit_code", 1 if expected else 0)
    return Case(name, tree, frozenset(expected), int(code), **kw)  # type: ignore[arg-type]


CASES: list[Case] = [
    _case(
        "clean tree with every link form",
        {
            "AGENTS.md": (
                "# Map\n"
                "\n"
                '- [Security](docs/SECURITY.md "Security rules"): R1 and R2.\n'
                "- [Roles](docs/SECURITY.md#roles), [top](#map).\n"
                "- [Two words](docs/Two%20Words.md), ![diagram](docs/img/map.png).\n"
                "- [F1 scope](docs/features/f1.md#scope); see CV-02.\n"
                "- Paths: `docs/SECURITY.md`, `app/api/deps.py`, `migrations/versions/`.\n"
                "- Commands: `python -m pytest tests/visible -q`, `GET /v1/issues`.\n"
            ),
            "docs/SECURITY.md": DOCS,
            "docs/Two Words.md": "# Two words\n",
            "docs/img/map.png": "",
        },
        set(),
    ),
    _case(
        "reference-style link definitions",
        {
            "AGENTS.md": (
                "# Map\n"
                "Read the [security doc][sec] and the [old doc][old].\n"
                "\n"
                "[sec]: docs/SECURITY.md\n"
                "[old]: docs/OLD.md\n"
            ),
            "docs/SECURITY.md": DOCS,
        },
        {("broken-link", "AGENTS.md:5")},
    ),
    _case(
        "anchors with repeated headings and product targets",
        {
            "AGENTS.md": (
                "# Map\n"
                "[sec](docs/SECURITY.md)\n"
                "[n1](docs/notes.md#notes-1)\n"
                "[n2](docs/notes.md#notes-2)\n"
                "[f1](docs/features/f1.md#scope)\n"
                "[f1x](docs/features/f1.md#rollout)\n"
            ),
            "docs/SECURITY.md": DOCS,
            "docs/notes.md": "# Notes\n\n## Notes\n\nText.\n",
        },
        {("broken-anchor", "AGENTS.md:4"), ("broken-anchor", "AGENTS.md:6")},
    ),
    _case(
        "links that leave the tree, absolute links, and missing images",
        {
            "AGENTS.md": "# Map\n[sec](docs/SECURITY.md)\n[abs](/docs/SECURITY.md)\n",
            "docs/SECURITY.md": DOCS + "\n[up](../../outside.md)\n![x](img/missing.png)\n",
        },
        {
            ("broken-link", "AGENTS.md:3"),
            ("broken-link", "docs/SECURITY.md:17"),
            ("broken-link", "docs/SECURITY.md:18"),
        },
    ),
    _case(
        "code-span paths inside a skill",
        {
            "AGENTS.md": "# Map\n[sec](docs/SECURITY.md) `.agents/skills/s/SKILL.md`\n",
            "docs/SECURITY.md": DOCS,
            ".agents/skills/s/SKILL.md": (
                "# Skill\n"
                "Read `references/tests.md`, then run `scripts/run.py`.\n"
                "Pattern: `app/api/deps.py`, config `alembic.ini`, "
                "`services.idempotency.run_once`.\n"
                "Legacy `/v1/issues` is not copied. First migration: `0001_initial.py`.\n"
            ),
            ".agents/skills/s/references/tests.md": "# Tests\n",
        },
        {
            ("broken-path", ".agents/skills/s/SKILL.md:2"),
            ("broken-path", ".agents/skills/s/SKILL.md:4"),
        },
    ),
    _case(
        "missing active rules; a retired rule may be left out",
        {
            "AGENTS.md": "# Map\n[sec](docs/SECURITY.md)\n",
            "docs/SECURITY.md": "# Security\n\n- [R1.1] Every query on customer data filters by "
            "the caller's `org_id`.\n",
        },
        {("missing-rule", "R2.1"), ("missing-rule", "R2.2"), ("missing-rule", "CV-02")},
    ),
    _case(
        "weak statements; the statement stops at the next list item",
        {
            "AGENTS.md": "# Map\n[sec](docs/SECURITY.md)\n",
            "docs/SECURITY.md": (
                "# Security\n"
                "\n"
                "- [R1.1] Queries on customer data always filter by the caller's `org_id`.\n"
                "- [R2.1] A viewer may read.\n"
                "  Every POST, PUT, PATCH, and DELETE returns 403 forbidden: viewers never write.\n"
                "- [R2.2] Admins only.\n"
                "- Creating and updating users is admin-only.\n"
                "- [CV-02] Keep changes focused.\n"
                "- Prefer small pull requests that touch only the files a feature needs.\n"
            ),
        },
        {("weak-rule", "R2.2"), ("weak-rule", "CV-02")},
    ),
    _case(
        "definitions in tables, two tags on one line, fenced examples ignored",
        {
            "AGENTS.md": "# Map\n[sec](docs/SECURITY.md)\n",
            "docs/SECURITY.md": (
                "# Security\n"
                "\n"
                "| Rule | Statement |\n"
                "|---|---|\n"
                "| [R1.1] | Every query on customer data filters by the caller's `org_id`. |\n"
                "\n"
                "[R2.1] Viewers never write: every POST, PUT, PATCH, and DELETE returns 403 "
                "forbidden for a viewer. [R2.2] Creating and updating users is admin-only.\n"
                "\n"
                "```markdown\n"
                "- [R9.1] An example tag in a code block is not a rule.\n"
                "```\n"
                "\n"
                "[CV-02] Prefer small pull requests that touch only the files a feature needs.\n"
            ),
        },
        set(),
    ),
    _case(
        "duplicate and retired definitions across files",
        {
            "AGENTS.md": "# Map\n[sec](docs/SECURITY.md) [more](docs/b/C.md)\n",
            "docs/SECURITY.md": DOCS,
            "docs/b/C.md": (
                "# More\n"
                "- [R1.1] Every query on customer data filters by the caller's `org_id`.\n"
                "- [R2.5] (retired 2024-11, superseded by R2.2) Members may archive projects.\n"
            ),
            ".agents/skills/s/SKILL.md": "# Skill\n- [R1.1] Every query filters by `org_id`.\n",
        },
        {("duplicate-rule", "R1.1"), ("retired-rule", "R2.5")},
    ),
    _case(
        "unknown references, linked ids, and a definition in the map",
        {
            "AGENTS.md": (
                "# Map\n"
                "Rules R1 and R2 are in [R2.1](docs/SECURITY.md#roles); R2.5 was retired.\n"
                "Not ours: R9, R1.7, and CV-99.\n"
                "- [R1.1] Every query on customer data filters by the caller's `org_id`.\n"
            ),
            "docs/SECURITY.md": DOCS.replace("- [R1.1] Every", "- Every"),
        },
        {
            ("unknown-rule", "R9"),
            ("unknown-rule", "R1.7"),
            ("unknown-rule", "CV-99"),
            ("rule-in-map", "R1.1"),
        },
    ),
    _case(
        "a missing tree is a usage error",
        {},
        {("usage", "--tree")},
        exit_code=2,
        tree_missing=True,
    ),
]
