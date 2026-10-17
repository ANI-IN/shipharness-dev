"""Build the public course repository from an allow-list of this build repository (release).

    uv run python platform/scripts/make_release.py --dry-run    # default: build in a temp folder
    uv run python platform/scripts/make_release.py --build DIR  # build DIR for the owner's push

Both modes write the allow-listed files of --ref (default HEAD) plus a generated
docs/REFERENCES.md into a fresh git repository (one commit as ANI-IN), rebuild the checkpoint
tags there with the logic of platform/scripts/build_checkpoints.py, and write the annotated
`class-v1` release tag on its one commit (content hashes, checkpoint trees, run settings). The
public `harness-frozen` tag is written only when the build repository has a freeze record. The
report covers, in order:

1. the public files (counts per top-level folder; the full list goes to --list-file) and the
   owner-listed files that do not exist yet;
2. the leak check: no private file, grader (`grader/`), hidden grader case (`hidden/` under a
   section's solution or grader), or internal script; the reference solutions themselves
   (`section-N-*/assignment/solution/`) are public (owner message 14);
3. the broken-reference check: public files that link to or name a private or excluded file;
4. docs/REFERENCES.md (the sources and findings from RESEARCH.md and its notes that public files
   cite);
5. each checkpoint tag's tree against the build repository's tag tree;
6. the frozen-content check (shipharness.freeze) per frozen path, and the tags written;
7. the target repository and the push commands the owner's release step would run;
8. contributors: every commit of the built repository by ANI-IN (author and committer) with no
   co-author or generated-with trailer (platform/scripts/check_contributors.py), and no public
   file with a Co-authored-by line, a "Generated with Claude" attribution, an AUTHORS,
   CONTRIBUTORS, or CODEOWNERS file listing anyone else, or a Dependabot configuration.

The dry run exits 1 on a leak, a frozen path that differs, or a contributor problem; broken
references, unresolved finding ids, and checkpoint trees are reported. --build also refuses on
those. Nothing is ever
pushed: the script prints the push commands and never talks to GitHub. It creates tags only in
the new repository, never in the build repository.

Only files tracked at --ref are read, straight from git objects, so the working tree and
untracked files never leak into the public tree.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import os
import posixpath
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file())

# -- owner decisions (the allow-list) -----------------------------------------------------------

TARGET = "ANI-IN/harness-engineering-session"

# Root files, verbatim from the owner (the course-first layout, owner messages 12.2 and 13).
ROOT_FILES = (
    "README.md",
    "LICENSE",
    "Makefile",
    "pyproject.toml",
    "uv.lock",
    ".python-version",
    ".env.example",
    ".gitignore",
    ".gitattributes",
    ".dockerignore",
)
ALLOW_DIRS = (
    ".github/workflows/",
    "setup/",  # the setup index, pre-class steps, and the three platform guides
    "final-project/",  # every file: README, run.sh, tasks/, harness/, walkthrough, expected/, ...
    "use-in-your-repo/",  # the starter kit, the four skills, and the guide
    "platform/src/",
    "platform/teamtrack/",  # including reference/, the referee's hidden tests, and the mutants
    "platform/datasets/",
    "platform/sandbox/",
    "platform/config/",
    "platform/tests/",
    "slides/img/",  # screenshots the deck embeds (make slides)
    "docs/images/",  # screenshots the README and shared pages embed
    "docs/evidence/",  # run ids, finding ids, and provenance per section
)
DOCS_FILES = tuple(
    f"docs/{name}.md"
    for name in (
        "instructor-guide",
        "troubleshooting",
        "architecture",
        "after-class",
        "extras",
        "STYLE",  # the course style guide that make check-style implements
        "CHANGELOG",
        "reference",
        "evidence",
        "STYLE",
    )
)
SETUP_FILES = tuple(
    f"setup/{name}.md" for name in ("README", "pre-class", "windows", "macos", "linux")
)
REFERENCES_FILE = "docs/REFERENCES.md"  # generated from RESEARCH.md and research/notes/
SLIDE_SUFFIXES = (".md", ".pdf", ".pptx")
SECTIONS = ("section-1", "section-2", "section-3", "section-4")
# The course diagrams: each diagrams/ folder ships its README.md and, per diagram, the Excalidraw
# source and its two renders. Nothing else in a diagrams/ folder ships.
_DIAGRAM_FILE = r"diagrams/(?:README\.md|[a-z0-9][a-z0-9-]*\.(?:excalidraw|png|svg))"
_DOCS_DIAGRAM = re.compile(rf"^docs/{_DIAGRAM_FILE}$")
# Per section folder at the root: the owner's items, plus the folder README and the whole
# assignment/ folder (its README, check.py and what it imports, starter/, the reference solution
# in solution/, visible tests, fixtures, live-step helpers); the guard below still removes every
# grader/ folder and every hidden grader case.
_SECTION_ITEM = re.compile(
    r"^(?:" + "|".join(SECTIONS) + r")-[^/]+/(?:README\.md|concepts\.md"
    r"|session-notes\.md|demo/.+|post-class-reading/.+|assignment/.+"
    rf"|{_DIAGRAM_FILE})$"
)
_SECTION_DIR = re.compile(r"^(?:" + "|".join(SECTIONS) + r")-[^/]+/")
SECTION_EXPECTED = (
    "concepts.md",
    "session-notes.md",
    "demo/",
    "post-class-reading/",
    "assignment/README.md",
    "assignment/check.py",
    "assignment/starter/",
    "assignment/solution/",
)
EXPECTED_DIRS = (
    ".github/workflows/",
    "setup/",
    "final-project/",
    "slides/",
    "use-in-your-repo/kit/",
    "use-in-your-repo/skills/",
    "platform/src/",
    "platform/teamtrack/",
    "platform/teamtrack/reference/",
    "platform/datasets/",
    "platform/sandbox/",
    "platform/config/",
    "platform/tests/",
)
# The final project's own parts. The 2026-10-17 release candidate shipped final-project/ with only
# its README and screenshots: the allow-list took the whole folder, but the folder held nothing
# else, and the missing-files report only asked for "final-project/". Each part is listed now.
FINAL_EXPECTED = (
    "final-project/README.md",
    "final-project/run.sh",
    "final-project/tasks/",
    "final-project/harness/",
    "final-project/walkthrough.md",
    "final-project/expected/terminal.txt",
    "final-project/expected/README.md",
    "final-project/your-repo/README.md",
    "final-project/your-repo/example/",
    "final-project/CHECKLIST.md",
)
SCRIPTS_DIR = "platform/scripts/"
# Learner scripts: the ones a public Makefile target, CI job, or public document runs.
LEARNER_SCRIPTS = (
    "platform/scripts/anchors.py",  # make lint, make anchors, CI, the section docs
    "platform/scripts/lint_prose.py",  # make lint-prose, CI, README
    "platform/scripts/check_style.py",  # make check-style, CI, docs/STYLE.md
    "platform/scripts/fetch_testgen_libs.py",  # assignment 4 README
    "platform/scripts/grade_assignment.py",  # make grade-assignment-N: says graders are private
    "platform/scripts/build_slides.py",  # make slides
)
# Private only (owner), plus exports and local run state.
PRIVATE_FILES = (
    "RESEARCH.md",
    "DESIGN.md",
    "CONTRACTS.md",
    "VERIFICATION.md",
    "CODEOWNERS",
    "FREEZE-EXCEPTIONS.toml",
)
PRIVATE_DIRS = ("research/", "instructor/", "exports/", ".shipharness/")
# Internal scripts the reference check knows by name (any other platform/scripts/ file is
# internal too).
INTERNAL_SCRIPTS = (
    "platform/scripts/pilot.py",
    "platform/scripts/build_checkpoints.py",
    "platform/scripts/probe_langsmith.py",
    "platform/scripts/build_features_dataset.py",
    "platform/scripts/build_testgen_dataset.py",
    "platform/scripts/freeze_harness.py",
    "platform/scripts/make_release.py",
    "platform/scripts/publish_solutions.py",
    "platform/scripts/rewrite_paths.py",
    "platform/scripts/check_contributors.py",
)

TEACHING = tuple(f"A{n}" for n in range(1, 8)) + tuple(f"B{n}" for n in range(1, 14))
DO_NOT_CITE = ("B15",)

AUTHOR_NAME = "ANI-IN"
AUTHOR_EMAIL = "44803072+ANI-IN@users.noreply.github.com"
COMMIT_MESSAGE = "shipharness: Module 1 course release"
CHECKPOINT_PREFIX = "m1-"
APP_DIR = "platform/teamtrack"
LEGACY_APP_DIR = "teamtrack"  # checkpoint tags made before the course-first layout
DEFAULT_VERIFY = ("uv", "run", "--frozen", "pytest", "-q")
DEFAULT_LIST_FILE = "/tmp/shipharness-release-files.txt"
DEFAULT_REFERENCES_FILE = "/tmp/shipharness-release-REFERENCES.md"
DEFAULT_REPORT_FILE = "/tmp/shipharness-release-report.txt"

REASON_SOLUTION = "grader or hidden grader case content"
REASON_PRIVATE = "private (owner)"
REASON_INTERNAL = "internal script"
REASON_NOT_ALLOWED = "not in the allow-list"
# Kept for the excluded-test scan: reasons that make a path private.
_PRIVATE_REASONS = (REASON_SOLUTION, REASON_PRIVATE, REASON_INTERNAL)


class ReleaseError(RuntimeError):
    pass


# -- selection ----------------------------------------------------------------------------------


@dataclass
class Selection:
    included: list[str]
    excluded: dict[str, str] = field(default_factory=dict)


def _segments(path: str) -> list[str]:
    return path.split("/")[:-1]  # directories only


def is_guarded(path: str) -> bool:
    """Anything under a grader/ folder, or a hidden grader case: a hidden/ folder in a section
    folder or under a solution/ folder. The reference solutions themselves are public (owner
    message 14); the referee's hidden tests under platform/teamtrack/ are public too."""
    dirs = _segments(path)
    if "grader" in dirs:
        return True
    return "hidden" in dirs and (bool(_SECTION_DIR.match(path)) or "solution" in dirs)


def private_reason(path: str) -> str | None:
    """Why `path` must never be public (owner: private only), or None."""
    if is_guarded(path):
        return REASON_SOLUTION
    if path in PRIVATE_FILES or path.startswith(PRIVATE_DIRS):
        return REASON_PRIVATE
    if path.startswith(SCRIPTS_DIR) and path not in LEARNER_SCRIPTS:
        return REASON_INTERNAL
    return None


def leaks(paths: Iterable[str]) -> list[tuple[str, str]]:
    """Every private path among `paths` with its reason (the leak check; any hit fails)."""
    found = [(p, private_reason(p)) for p in sorted(paths)]
    return [(p, r) for p, r in found if r]


def _allowed(path: str) -> bool:
    if path in ROOT_FILES or path in LEARNER_SCRIPTS or path in DOCS_FILES:
        return True
    if path.startswith(ALLOW_DIRS) or _DOCS_DIAGRAM.match(path):
        return True
    if path.startswith("slides/"):
        return path.endswith(SLIDE_SUFFIXES)
    return bool(_SECTION_ITEM.match(path))


def classify(path: str) -> str | None:
    """None when `path` goes into the public tree, else the reason it does not."""
    reason = private_reason(path)
    if reason:
        return reason
    if not _allowed(path):
        return REASON_NOT_ALLOWED
    return None


def missing_expected(included: Iterable[str]) -> list[str]:
    """Owner-listed files and folders the public tree does not have (yet): reported, not failed.
    Section items are matched per number (`section-2-*/concepts.md`)."""
    present = set(included)

    def has(item: str) -> bool:
        if item.endswith("/"):
            return any(p.startswith(item) for p in present)
        return item in present

    missing = [p for p in (*ROOT_FILES, *DOCS_FILES, *SETUP_FILES) if not has(p)]
    missing += [d for d in EXPECTED_DIRS if not has(d)]
    missing += [p for p in FINAL_EXPECTED if not has(p)]
    for number in SECTIONS:
        folders = sorted({p.split("/")[0] for p in present if p.startswith(f"{number}-")})
        for item in SECTION_EXPECTED:
            if not any(has(f"{folder}/{item}") for folder in folders):
                missing.append(f"{number}-*/{item}")
    return missing


def select(paths: Iterable[str], extra_excluded: Mapping[str, str] | None = None) -> Selection:
    extra = dict(extra_excluded or {})
    sel = Selection(included=[])
    for path in sorted(paths):
        reason = classify(path) or extra.get(path)
        if reason:
            sel.excluded[path] = reason
        else:
            sel.included.append(path)
    return sel


# -- tests that exercise excluded files (decision b) --------------------------------------------

_TOKEN = re.compile(r"[\w.\-/]+")


def _docstring_ids(tree: ast.AST) -> set[int]:
    ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                ids.add(id(body[0].value))
    return ids


def _module_names(tree: ast.AST) -> list[str]:
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            names.append(base)
            names += [f"{base}.{a.name}" if base else a.name for a in node.names]
    return [n for n in names if n]


def _loading_call_args(tree: ast.AST) -> set[int]:
    """Ids of string constants passed directly to a call whose name suggests it loads a module or
    script (load_script, import_module, spec_from_file_location, ...)."""
    ids: set[int] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        if any(word in name.lower() for word in ("load", "import", "script", "spec")):
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    ids.add(id(arg))
    return ids


def _reason_key(reason: str) -> tuple[int, str]:
    m = re.match(r"line (\d+):", reason)
    return (int(m.group(1)) if m else 0), reason


def find_excluded_tests(
    sources: Mapping[str, str], excluded: Iterable[str], included: Iterable[str]
) -> dict[str, list[str]]:
    """Test files (and test helpers) whose code names an excluded file: a string constant that is
    or ends with an excluded path, has the basename of an excluded file that no included file
    shares, or is the module name of an excluded script; or an import of such a script. Docstrings
    and comments do not count. Tests that import a flagged helper are flagged too."""
    excluded = sorted(set(excluded))
    included_basenames = {posixpath.basename(p) for p in included}
    basenames = {
        posixpath.basename(p): p
        for p in excluded
        if posixpath.basename(p) not in included_basenames
    }
    stems = {
        posixpath.splitext(posixpath.basename(p))[0]: p
        for p in excluded
        if posixpath.dirname(p) + "/" == SCRIPTS_DIR and p.endswith(".py")
    }

    def token_hit(token: str, stem_ok: bool = False) -> str | None:
        token = token[2:] if token.startswith("./") else token
        folder = token.rstrip("/")
        is_excluded_folder = "/" in folder and classify(folder + "/x") in _PRIVATE_REASONS
        for path in excluded:
            if token == path or token.endswith("/" + path):
                return path
            if is_excluded_folder and path.startswith(folder + "/"):
                return path
        base = posixpath.basename(token)
        if base in basenames:
            return basenames[base]
        # A module path names a script ("scripts.pilot"); a bare stem does only where it is passed
        # to a loading call (load_script("build_testgen_dataset")): "pilot" is also a run purpose.
        if token.startswith("scripts.") and token.split(".")[-1] in stems:
            return stems[token.split(".")[-1]]
        if stem_ok and token in stems:
            return stems[token]
        return None

    found: dict[str, list[str]] = {}
    imports: dict[str, list[str]] = {}
    for path, text in sorted(sources.items()):
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        docs = _docstring_ids(tree)
        loaded = _loading_call_args(tree)
        reasons: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if id(node) in docs:
                    continue
                for token in _TOKEN.findall(node.value):
                    hit = token_hit(token, stem_ok=id(node) in loaded)
                    if hit:
                        reasons.append(f"line {node.lineno}: names {hit}")
        modules = _module_names(tree)
        imports[path] = modules
        for name in modules:
            last = name.rsplit(".", 1)[-1]
            if name.startswith("scripts") and last in stems:
                reasons.append(f"imports {stems[last]}")
        if reasons:
            found[path] = sorted(set(reasons), key=_reason_key)
    changed = True
    while changed:  # tests that import a flagged helper module
        changed = False
        helpers = {posixpath.splitext(posixpath.basename(p))[0]: p for p in found}
        for path, modules in imports.items():
            if path in found:
                continue
            for name in modules:
                last = name.rsplit(".", 1)[-1]
                if last in helpers:  # a helper, or a test module other tests import from
                    found[path] = [f"imports {helpers[last]}"]
                    changed = True
                    break
    return dict(sorted(found.items()))


# -- reference check (decision 5) ---------------------------------------------------------------


@dataclass(frozen=True)
class Hit:
    path: str
    line: int
    kind: str  # link, section-cite, mention, script, solution, run-id
    text: str
    pattern: str
    excerpt: str


_DOCS = "DESIGN|CONTRACTS|RESEARCH|VERIFICATION"
_LINK = re.compile(r"\[[^\]\n]*\]\(<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\)")
_SECTION = re.compile(
    rf"\b(?:{_DOCS})(?:\.md)?"
    r"(?:\s*§\s*\d+(?:\.\d+)*|\s+[A-Z]{1,2}-\d+(?:\s+to\s+[A-Z]{1,2}-\d+)?|\s+\d+\.\d+\b"
    r"|\s+correction\s+\d+)"
    r"|\bDesign\s*§\s*\d+(?:\.\d+)*"
)
_SCRIPT_STEMS = "|".join(posixpath.splitext(posixpath.basename(p))[0] for p in INTERNAL_SCRIPTS)
_SCRIPT = re.compile(
    rf"(?:\b(?:platform/)?scripts/)?\b(?:{_SCRIPT_STEMS})\.py\b"
    rf"|\b(?:platform/)?scripts/(?:{_SCRIPT_STEMS})\b"
)
_SOLUTION = re.compile(
    r"(?<![\w.-])grader/(?:[\w./-]*[\w/])?"
    r"|\bsection-[1-4]-[\w.-]+/(?:[\w.-]+/)*hidden/(?:[\w./-]*[\w/])?"
)
_MENTION = re.compile(
    rf"\b(?:{_DOCS})\.md\b"
    rf"|\b(?:{_DOCS})\b"
    r"|\bCODEOWNERS\b"
    r"|(?:(?<![\w./-])|(?<=\./))(?:research|instructor)/(?:[\w./-]*[\w/])?"  # no final "."
    r"|\bR-[a-e](?:\.md)?\b"
)
_RUN_ID = re.compile(r"\b(?:ab|r)-\d{8}-\d{6}-[0-9a-f]{6}\b")
_SOURCE_CITE = re.compile(r"\bF-[a-e]-\d+\b|\b[AB]\d{1,2}\b")
_NOT_INCLUDED = re.compile(r"\bnot\s+(?:included|shipped|part\s+of|in\s+this\s+repo)", re.I)


def _left_out(norm: str, existing: frozenset[str], public: frozenset[str]) -> bool:
    """`norm` (a file or folder) exists in the build repository but not in the public tree."""
    folder = norm.rstrip("/") + "/"
    if norm in public or any(p.startswith(folder) for p in public):
        return False
    return norm in existing or any(p.startswith(folder) for p in existing)


def _excluded_target(
    path: str,
    target: str,
    existing: frozenset[str] | None = None,
    public: frozenset[str] | None = None,
) -> str | None:
    """The private or excluded file or folder a link target points at, or None. With `existing`
    (the excluded tracked paths) and `public` (the public tree), a link to any file that exists
    in the build repository but is left out of the public tree counts too."""
    if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    norm = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
    norm = norm.lstrip("/")
    if norm in PRIVATE_FILES or norm in INTERNAL_SCRIPTS:
        return norm
    for folder in PRIVATE_DIRS:
        if norm == folder.rstrip("/") or norm.startswith(folder):
            return folder
    if is_guarded(norm + "/x"):
        return "grader/"
    # A wrong relative path still points the reader at a private file.
    if posixpath.basename(norm) in PRIVATE_FILES:
        return posixpath.basename(norm)
    for folder in PRIVATE_DIRS:
        if f"/{folder}" in f"/{target}":
            return folder
    if existing is not None and public is not None and _left_out(norm, existing, public):
        return norm
    return None


def _pattern(kind: str, text: str, target: str = "") -> str:
    if kind == "link":
        return f"link to {target}"
    if kind == "section-cite":
        label = re.sub(r"\s*§\s*[\d.]+", " §", text.replace("Design", "DESIGN"))
        label = re.sub(r"\b([A-Z]{1,2})-\d+(?:\s+to\s+[A-Z]{1,2}-\d+)?", r"\1-N", label)
        label = re.sub(r"correction\s+\d+", "correction N", label)
        return re.sub(r"\s+\d+\.\d+", " N.N", label).replace(".md", "")
    if kind == "script":
        return posixpath.basename(text)
    if kind == "solution":
        return "section-N-*/hidden/" if "hidden/" in text else text.split("/", 1)[0] + "/"
    if kind == "run-id":
        return "VERIFICATION run id"
    if text.startswith(("research/", "instructor/", "../", "./")):
        parts = [p for p in text.split("/") if p not in ("..", ".", "")]
        deep = len(parts) > 2 or (len(parts) == 2 and text.endswith("/"))
        return "/".join(parts[:2]) + "/" if deep else parts[0] + "/"
    if re.fullmatch(r"R-[a-e](?:\.md)?", text):
        return "R-x (research notes)"
    return text


def _take(taken: list[tuple[int, int]], m: re.Match[str]) -> bool:
    """Claim the span of `m` unless an earlier (higher-priority) match overlaps it."""
    if any(m.start() < e and s < m.end() for s, e in taken):
        return False
    taken.append((m.start(), m.end()))
    return True


def _names_existing(text: str, existing: frozenset[str] | None) -> bool:
    """A research/ or instructor/ path counts only when it names a tracked excluded file or one of
    its folders (a test fixture path such as instructor/notes.md does not)."""
    if existing is None or not text.startswith(("research/", "instructor/", "../", "./")):
        return True
    rel = "/".join(p for p in text.split("/") if p not in ("..", "."))
    folder = rel.rstrip("/") + "/"
    return any(p == rel or p.startswith(folder) for p in existing)


def _line_hits(
    path: str,
    line: str,
    run_ids: frozenset[str],
    existing: frozenset[str] | None = None,
    public: frozenset[str] | None = None,
) -> list[tuple[int, str, str, str]]:
    taken: list[tuple[int, int]] = []
    found: list[tuple[int, str, str, str]] = []
    for m in _LINK.finditer(line):
        target = _excluded_target(path, m.group(1), existing, public)
        if target and _take(taken, m):
            found.append((m.start(), "link", m.group(0), _pattern("link", "", target)))
    for m in _SECTION.finditer(line):
        if _take(taken, m):
            found.append((m.start(), "section-cite", m.group(0), _pattern("section-cite", m[0])))
    # Run ids are never hits: they label captured output and pilot numbers (owner rule,
    # 2026-10-17); `run_ids` stays in the signature for callers.
    # A statement that a file is not included is a hit only when it links to or cites it.
    quiet = bool(_NOT_INCLUDED.search(line))
    for kind, regex in (("script", _SCRIPT), ("solution", _SOLUTION), ("mention", _MENTION)):
        for m in regex.finditer(line):
            if not _names_existing(m.group(0), existing):
                continue
            if _take(taken, m) and not quiet:
                found.append((m.start(), kind, m.group(0), _pattern(kind, m.group(0))))
    return sorted(found)


def scan_references(
    path: str,
    text: str,
    run_ids: frozenset[str] = frozenset(),
    existing: frozenset[str] | None = None,
    public: frozenset[str] | None = None,
) -> list[Hit]:
    """Every place in `text` that links to, cites, or names a private or excluded file. Priority
    on overlapping matches: link, section citation, run id, script, solution path, plain mention.
    `existing`: the tracked excluded paths, when known (research/ and instructor/ mentions must
    name one of them); with `public` (the public tree) too, links to any excluded file count."""
    hits: list[Hit] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for _, kind, matched, label in _line_hits(path, line, run_ids, existing, public):
            hits.append(Hit(path, number, kind, matched, label, line.strip()[:160]))
    return hits


def run_ids_from(verification_md: str) -> frozenset[str]:
    return frozenset(_RUN_ID.findall(verification_md))


# -- REFERENCES.md (decision 4) -----------------------------------------------------------------


@dataclass(frozen=True)
class Source:
    id: str
    title: str
    url: str
    author: str = ""
    date: str = ""


@dataclass(frozen=True)
class Finding:
    id: str
    source: str
    quote: str


@dataclass
class References:
    text: str
    sources: list[Source]
    findings: list[Finding]
    unresolved: list[str]


def _section(md: str, heading: re.Pattern[str]) -> str:
    lines = md.splitlines()
    out: list[str] = []
    level = 0
    for line in lines:
        m = re.match(r"^(#+)\s", line)
        if level:
            if m and len(m.group(1)) <= level:
                break
            out.append(line)
        elif m and heading.search(line):
            level = len(m.group(1))
    return "\n".join(out)


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _table(section: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for line in section.splitlines():
        if not line.lstrip().startswith("|"):
            header = None  # a new table starts after any other line
            continue
        cells = _cells(line)
        if header is None:
            header = [c.lower() for c in cells]
        elif all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        else:
            rows.append(dict(zip(header, cells, strict=False)))
    return rows


def _column(row: Mapping[str, str], *starts: str, avoid: str = "") -> str:
    for key, value in row.items():
        if key.startswith(starts) and not (avoid and avoid in key):
            return value
    return ""


def _urls(cell: str) -> str:
    return " ; ".join(re.findall(r"https?://[^\s;)|]+", cell))


def _row_source(row: Mapping[str, str], sid: str) -> Source:
    return Source(
        id=sid,
        title=_column(row, "title"),
        url=_urls(_column(row, "url")),
        # No e-mail addresses in the learner repo (B6 lists the package author's address).
        author=re.sub(r"author_email\s+|\s*<[^>]*@[^>]*>", "", _column(row, "author")),
        date=_column(row, "date", "publication", avoid="access"),
    )


def parse_register(research_md: str) -> dict[str, Source]:
    """Single-id rows of the teaching-source table (RESEARCH §1.1)."""
    section = _section(research_md, re.compile(r"^###\s+1\.1\b"))
    found: dict[str, Source] = {}
    for row in _table(section):
        sid = row.get("id", "")
        if re.fullmatch(r"[A-E]\d{1,2}", sid):
            found[sid] = _row_source(row, sid)
    return found


def parse_note_sources(note_md: str) -> dict[str, Source]:
    found: dict[str, Source] = {}
    for row in _table(_section(note_md, re.compile(r"^##\s+Sources\b"))):
        m = re.match(r"([A-E]\d{1,2})\b", row.get("id", ""))
        if m:
            found[m.group(1)] = _row_source(row, m.group(1))
    return found


_FINDING_LINE = re.compile(r"^\s*(?:-\s*`|\|\s*`?)(F-[a-e]-\d+)`?\s*\|")


def parse_findings(note_md: str) -> dict[str, Finding]:
    found: dict[str, Finding] = {}
    for line in note_md.splitlines():
        m = _FINDING_LINE.match(line)
        if not m:
            continue
        body = re.sub(r"^\s*-\s*", "", line)
        cells = _cells(body)
        if len(cells) < 5:
            continue
        sid = re.search(r"\b([A-E]\d{1,2})\b", cells[-1])
        found[m.group(1)] = Finding(
            m.group(1), sid.group(1) if sid else "", "|".join(cells[3:-1]).strip()
        )
    return found


_FINDING = re.compile(r"\bF-([a-e])-(\d+)\b")
_FINDING_RANGE = re.compile(r"\bF-([a-e])-(\d+)\s+to\s+F-\1-(\d+)\b")
_SOURCE_ID = re.compile(r"\b([A-E])(\d{1,2})\b")
_SOURCE_RANGE = re.compile(r"\b([A-E])(\d{1,2})\s*(?:-|–|to)\s*\1(\d{1,2})\b")
_TECH_CONTEXT = re.compile(r"technical reference|OpenAI|§\s*4\.2", re.I)


def _finding_id(series: str, number: int) -> str:
    return f"F-{series}-{number:02d}"


def cited_ids(texts: Mapping[str, str]) -> tuple[set[str], set[str]]:
    """(finding ids, source ids) cited in `texts`. A and B ids count anywhere; D and E ids in
    Markdown; C ids (which collide with TeamTrack's control tasks and assessment checks) only on
    Markdown lines that name a technical reference or OpenAI."""
    findings: set[str] = set()
    sources: set[str] = set()
    for path, text in texts.items():
        markdown = path.endswith(".md")
        for line in text.splitlines():
            findings |= {_finding_id(s, int(n)) for s, n in _FINDING.findall(line)}
            for s, a, b in _FINDING_RANGE.findall(line):
                findings |= {_finding_id(s, n) for n in range(int(a), int(b) + 1)}
            sources |= {
                f"{s}{n}" for s, n in _SOURCE_ID.findall(line) if _counts(s, markdown, line)
            }
            for s, a, b in _SOURCE_RANGE.findall(line):
                if _counts(s, markdown, line):
                    sources |= {f"{s}{n}" for n in range(int(a), int(b) + 1)}
    return findings, sources


def _counts(letter: str, markdown: bool, line: str) -> bool:
    if letter in "AB":
        return True
    if letter in "DE":
        return markdown
    return markdown and bool(_TECH_CONTEXT.search(line))


def _prose_lint() -> tuple[Callable[[str], list[tuple[int, str]]], str]:
    """lint_prose.lint_text and its allow marker (verbatim quotes may contain a banned word)."""
    spec = importlib.util.spec_from_file_location(
        "lint_prose", Path(__file__).with_name("lint_prose.py")
    )
    if not spec or not spec.loader:  # pragma: no cover
        raise ReleaseError("platform/scripts/lint_prose.py not found")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.lint_text, module.ALLOW_MARKER


def _contributors() -> Any:
    """platform/scripts/check_contributors.py: the commit check (author, committer, trailers)."""
    spec = importlib.util.spec_from_file_location(
        "check_contributors", Path(__file__).with_name("check_contributors.py")
    )
    if not spec or not spec.loader:  # pragma: no cover
        raise ReleaseError("platform/scripts/check_contributors.py not found")
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_contributors"] = module
    spec.loader.exec_module(module)
    return module


def _cell(text: str) -> str:
    return text.replace("|", "\\|").strip()


def _sort_key(sid: str) -> tuple[str, int]:
    return sid[0], int(sid[1:])


def _finding_key(fid: str) -> tuple[str, int]:
    _, series, number = fid.split("-")
    return series, int(number)


def build_references(
    research_md: str,
    notes: Mapping[str, str],
    cited_texts: Mapping[str, str],
    teaching: Iterable[str] = TEACHING,
) -> References:
    note_sources: dict[str, Source] = {}
    all_findings: dict[str, Finding] = {}
    for _, text in sorted(notes.items()):
        note_sources.update(parse_note_sources(text))
        all_findings.update(parse_findings(text))
    register = parse_register(research_md)
    known = {**note_sources, **register}  # RESEARCH §1.1 wins for single-id rows
    access = re.search(r"Access date for every source:\s*(\d{4}-\d{2}-\d{2})", research_md)

    finding_ids, source_ids = cited_ids(cited_texts)
    unresolved = sorted(f for f in finding_ids if f not in all_findings)
    findings = [all_findings[f] for f in sorted(finding_ids - set(unresolved), key=_finding_key)]
    wanted = set(teaching) | source_ids | {f.source for f in findings if f.source}
    skipped = sorted(s for s in wanted if s in DO_NOT_CITE)
    sources = [known[s] for s in sorted(wanted, key=_sort_key) if s in known and s not in skipped]
    by_id = {s.id: s for s in sources}
    teach = [s for s in sources if s.id[0] in "AB"]
    tech = [s for s in sources if s.id[0] not in "AB"]

    lines = [
        "# References",
        "",
        "The public sources this course cites, with their URLs, and the findings that the course",
        "material cites by id. A finding id such as F-a-05 names one short verbatim quote from one",
        "source; source ids (A1, B11, D27, ...) are listed below.",
    ]
    if access:
        lines += ["", f"Every source was accessed on {access.group(1)}."]
    lines += [
        "",
        "## Teaching sources",
        "",
        "| ID | Title | Author or organization | Date | URL |",
        "|---|---|---|---|---|",
    ]
    lines += [
        f"| {s.id} | {_cell(s.title)} | {_cell(s.author)} | {_cell(s.date)} | {s.url} |"
        for s in teach
    ]
    if skipped:
        lines += [
            "",
            "B15 (Spec-Bench, arXiv 2401.07851) is a benchmark for speculative decoding with a",
            "name close to SpecBench. It is unrelated to this course and is not a course source.",
        ]
    if tech:
        lines += [
            "",
            "## Technical references",
            "",
            "Official documentation that the course material cites by id.",
            "",
            "| ID | Title | URL |",
            "|---|---|---|",
        ]
        lines += [f"| {s.id} | {_cell(s.title)} | {s.url} |" for s in tech]
    lines += ["", "## Findings", "", "| ID | Source | Quote | URL |", "|---|---|---|---|"]
    for f in findings:
        url = by_id[f.source].url.split(" ; ")[0] if f.source in by_id else ""
        lines.append(f"| {f.id} | {f.source} | {_cell(f.quote)} | {url} |")
    lint, marker = _prose_lint()
    text = "\n".join(
        f"{line} {marker}" if line.startswith("| F-") and lint(line) else line for line in lines
    )
    return References(text + "\n", sources, findings, unresolved)


# -- git access ---------------------------------------------------------------------------------


def _git_env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def _git(repo: Path, *args: str, data: bytes | None = None) -> bytes:
    done = subprocess.run(
        ["git", "-c", "core.autocrlf=false", *args],
        cwd=repo,
        input=data,
        capture_output=True,
        env=_git_env(),
        check=False,
    )
    if done.returncode != 0:
        detail = done.stderr.decode("utf-8", errors="replace").strip()[:800]
        raise ReleaseError(f"git {' '.join(args[:2])} failed: {detail}")
    return done.stdout


@dataclass(frozen=True)
class Entry:
    mode: str
    sha: str


def tracked(repo: Path, ref: str) -> dict[str, Entry]:
    """Blobs tracked at `ref` (path -> mode, object id). Gitlinks are an error."""
    out: dict[str, Entry] = {}
    for item in _git(repo, "ls-tree", "-r", "-z", "--full-tree", ref).split(b"\0"):
        if not item:
            continue
        meta, path = item.decode("utf-8").split("\t", 1)
        mode, kind, sha = meta.split()
        if kind != "blob":
            raise ReleaseError(f"{path}: {kind} entries (submodules) are not supported")
        out[path] = Entry(mode, sha)
    return out


def read_blobs(repo: Path, entries: Mapping[str, Entry]) -> dict[str, bytes]:
    paths = sorted(entries)
    if not paths:
        return {}
    data = "".join(f"{entries[p].sha}\n" for p in paths).encode()
    raw = _git(repo, "cat-file", "--batch", data=data)
    out: dict[str, bytes] = {}
    pos = 0
    for path in paths:
        end = raw.index(b"\n", pos)
        _, _, size = raw[pos:end].decode().split()
        start = end + 1
        out[path] = raw[start : start + int(size)]
        pos = start + int(size) + 1
    return out


def _texts(blobs: Mapping[str, bytes]) -> dict[str, str]:
    out: dict[str, str] = {}
    for path, data in blobs.items():
        if b"\0" in data[:8000]:
            continue
        try:
            out[path] = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
    return out


def _is_test_source(path: str) -> bool:
    return path.endswith(".py") and (path.startswith("tests/") or "/tests/" in path)


# -- analysis -----------------------------------------------------------------------------------


@dataclass
class Report:
    """What the allow-list selects at `ref`, before anything is written."""

    ref: str
    selection: Selection
    excluded_tests: dict[str, list[str]]
    leaks: list[tuple[str, str]]
    hits: list[Hit]
    references: References
    entries: dict[str, Entry] = field(default_factory=dict)
    commit: str = ""

    def dry_run_failures(self) -> list[str]:
        if not self.leaks:
            return []
        return [f"{len(self.leaks)} private path(s) would be public"]

    def build_failures(self) -> list[str]:
        out = self.dry_run_failures()
        if self.hits:
            files = len({h.path for h in self.hits})
            out.append(f"{len(self.hits)} broken reference(s) in {files} public file(s)")
        if self.references.unresolved:
            out.append(f"unresolved finding ids: {', '.join(self.references.unresolved)}")
        return out


def analyze(repo: Path, ref: str = "HEAD") -> Report:
    entries = tracked(repo, ref)
    first = select(entries)
    tests = {p: entries[p] for p in first.included if _is_test_source(p)}
    test_sources = _texts(read_blobs(repo, tests))
    excluded_tests = find_excluded_tests(test_sources, first.excluded, first.included)
    reasons = {p: "exercises excluded files: " + "; ".join(r) for p, r in excluded_tests.items()}
    sel = select(entries, reasons)
    texts = _texts(read_blobs(repo, {p: entries[p] for p in sel.included}))
    sources = _texts(
        read_blobs(
            repo,
            {
                p: e
                for p, e in entries.items()
                if p in ("RESEARCH.md", "VERIFICATION.md")
                or (p.startswith("research/notes/") and p.endswith(".md"))
            },
        )
    )
    notes = {p: t for p, t in sources.items() if p.startswith("research/")}
    references = build_references(sources.get("RESEARCH.md", ""), notes, texts)
    run_ids = run_ids_from(sources.get("VERIFICATION.md", ""))
    existing = frozenset(sel.excluded)
    public = frozenset(sel.included) | {REFERENCES_FILE}
    hits: list[Hit] = []
    for path in sorted(texts):
        hits += scan_references(path, texts[path], run_ids, existing, public)
    hits += scan_references(REFERENCES_FILE, references.text, run_ids, existing, public)
    return Report(
        ref=ref,
        selection=sel,
        excluded_tests=excluded_tests,
        leaks=leaks(sel.included),
        hits=hits,
        references=references,
        entries=entries,
        commit=_git(repo, "rev-parse", f"{ref}^{{commit}}").decode().strip(),
    )


# -- public repository: tree, checkpoint tags, frozen record ------------------------------------


@dataclass(frozen=True)
class TagCompare:
    """One checkpoint tag in the build repository against the rebuilt public tag."""

    name: str
    build_tree: str | None
    public_tree: str | None
    build_app: str | None  # tree id of TeamTrack (what an arm workspace is exported from)
    public_app: str | None
    differing: list[str]  # public paths whose content differs (docs/REFERENCES.md not counted)

    @property
    def rebuilt(self) -> bool:
        return self.public_tree is not None

    @property
    def full_match(self) -> bool:
        return self.build_tree is not None and self.build_tree == self.public_tree

    @property
    def app_match(self) -> bool:
        return self.build_app is not None and self.build_app == self.public_app


@dataclass
class FrozenResult:
    basis: str  # "tag": the build repo's harness-frozen record; "head": a record made from HEAD
    paths: dict[str, bool]  # frozen path -> content matches
    checkpoint_differs: list[str]  # record checkpoint trees (whole-tree ids) the public tags lack
    record_commit: str | None  # the public harness-frozen tag; None without a freeze record
    self_check: list[str]  # the public record against the public repository itself


@dataclass
class ClassTagResult:
    commit: str  # where the public class-v1 tag points
    paths: int
    checkpoint_trees: int
    self_check: list[str]  # the class-v1 record against the public repository itself


@dataclass
class Release:
    report: Report
    public: Path
    commit: str
    tags: list[str]
    public_files: list[str]
    tree_leaks: list[tuple[str, str]]
    checkpoints: list[TagCompare]
    frozen: FrozenResult
    class_tag: ClassTagResult
    missing: list[str]
    push: list[str]
    contributors: list[str] = field(default_factory=list)  # owner rule: ANI-IN only

    def failures(self) -> list[str]:
        """What fails the dry run: leaks, frozen content that differs, a tag record that does
        not match the public repository, and any contributor other than ANI-IN."""
        out = self.report.dry_run_failures()
        if self.contributors:
            out.append(
                f"contributors: {len(self.contributors)} problem(s), first: {self.contributors[0]}"
            )
        if self.tree_leaks:
            out.append(f"{len(self.tree_leaks)} private path(s) in the public repository")
        differs = [p for p, ok in self.frozen.paths.items() if not ok]
        if differs:
            out.append("frozen content differs: " + ", ".join(differs))
        if self.frozen.self_check:
            out.append("public record check: " + "; ".join(self.frozen.self_check))
        if self.class_tag.self_check:
            out.append("class-v1 record check: " + "; ".join(self.class_tag.self_check))
        return out

    def build_failures(self) -> list[str]:
        out = self.failures()
        out += [f for f in self.report.build_failures() if f not in out]
        bad = [c.name for c in self.checkpoints if c.rebuilt and not c.app_match]
        if bad:
            out.append(
                "checkpoint TeamTrack tree differs from the build repository: " + ", ".join(bad)
            )
        return out


def _rev(repo: Path, spec: str) -> str | None:
    done = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", spec],
        cwd=repo,
        capture_output=True,
        env=_git_env(),
        check=False,
    )
    return done.stdout.decode().strip() if done.returncode == 0 else None


def _tag_names(repo: Path, prefix: str = CHECKPOINT_PREFIX) -> list[str]:
    return _git(repo, "tag", "--list", f"{prefix}*").decode().split()


def _tree_blobs(repo: Path, spec: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in _git(repo, "ls-tree", "-r", "-z", "--full-tree", spec).split(b"\0"):
        if item:
            meta, path = item.decode("utf-8").split("\t", 1)
            out[path] = meta.split()[2]
    return out


def compare_checkpoints(repo: Path, public: Path, keep: Callable[[str], bool]) -> list[TagCompare]:
    """Each checkpoint tag of either repository: whole tree, TeamTrack tree (platform/teamtrack/,
    or teamtrack/ in a build tag made before the course-first layout), and the public paths
    (`keep` filters the build tag's files) whose content differs."""
    out: list[TagCompare] = []
    for name in sorted(set(_tag_names(repo)) | set(_tag_names(public))):
        ref = f"refs/tags/{name}"
        build_tree, public_tree = _rev(repo, f"{ref}^{{tree}}"), _rev(public, f"{ref}^{{tree}}")
        differing: list[str] = []
        if build_tree and public_tree:
            theirs = {p: s for p, s in _tree_blobs(repo, ref).items() if keep(p)}
            ours = _tree_blobs(public, ref)
            ours.pop(REFERENCES_FILE, None)
            differing = sorted(p for p in set(theirs) | set(ours) if theirs.get(p) != ours.get(p))
        out.append(
            TagCompare(
                name,
                build_tree,
                public_tree,
                _rev(repo, f"{ref}:{APP_DIR}") or _rev(repo, f"{ref}:{LEGACY_APP_DIR}"),
                _rev(public, f"{ref}:{APP_DIR}"),
                differing,
            )
        )
    return out


def _frozen_dirty(repo: Path, paths: Iterable[str]) -> list[str]:
    changed = _git(repo, "diff", "--name-only", "HEAD", "--", *paths).decode().split()
    untracked = _git(repo, "ls-files", "--others", "--exclude-standard", "--", *paths)
    return sorted(set(changed) | set(untracked.decode().split()))


def frozen_check(repo: Path, ref: str, public: Path) -> FrozenResult:
    """Owner rule 2: the public tree's frozen content against the build repo's harness-frozen
    record (exceptions applied) or, without that tag, a record made from the build repo's HEAD.
    Only with a real freeze record (the build repo's tag) is the record written as the public
    repository's own harness-frozen tag, with the public checkpoint trees (whole-tree ids differ
    between the two repositories by design); a HEAD record is compared, never tagged."""
    from shipharness import freeze
    from shipharness.config import Settings

    record = freeze.expected_record(repo)
    basis = "tag"
    if record is None:
        basis = "head"
        head = _git(repo, "rev-parse", "HEAD^{commit}").decode().strip()
        if _git(repo, "rev-parse", f"{ref}^{{commit}}").decode().strip() != head:
            raise ReleaseError(
                f"no {freeze.TAG} tag: the record comes from HEAD, so --ref must be HEAD"
            )
        dirty = _frozen_dirty(repo, freeze.FROZEN_PATHS)
        if dirty:
            raise ReleaseError("uncommitted changes under frozen paths: " + ", ".join(dirty[:10]))
        record = freeze.make_record(repo, Settings(_env_file=None))  # never reads .env
    found = freeze.compare_content(public, record)
    paths = {p: f"content differs: {p}" not in found for p in record["frozen_paths"]}
    prefix = "checkpoint content differs: "
    differs = sorted(f[len(prefix) :] for f in found if f.startswith(prefix))
    if basis != "tag":
        return FrozenResult(basis, paths, differs, None, [])
    own = {
        **record,
        "checkpoint_trees": freeze.checkpoint_trees(public),
        "checkpoint_tags": freeze.checkpoint_tags(public),
    }
    commit = freeze.write_record_tag(public, own, identity=(AUTHOR_NAME, AUTHOR_EMAIL))
    written = freeze.read_record(public) or {}
    return FrozenResult(basis, paths, differs, commit, freeze.compare_content(public, written))


def class_tag(public: Path, commit: str) -> ClassTagResult:
    """The annotated class-v1 release tag on the public commit: the owner's sentence and a record
    of the content hashes, checkpoint trees, and run settings computed in the public repository
    (code defaults; `.env` is never read). Its own check runs `shipharness verify` logic on it."""
    from shipharness import freeze
    from shipharness.config import Settings

    record = freeze.class_record(public, Settings(_env_file=None))
    at = freeze.write_class_tag(public, record, identity=(AUTHOR_NAME, AUTHOR_EMAIL), target=commit)
    _, found = freeze.verify_copy(public, freeze.CLASS_TAG)
    return ClassTagResult(at, len(record["paths"]), len(record["checkpoint_trees"]), found)


def push_commands(public: Path, tags: Iterable[str], *, harness_frozen: bool = False) -> list[str]:
    """What the owner's release step runs after a final yes (printed here, never executed)."""
    refs = [f"refs/tags/{t}" for t in sorted(tags)] + ["refs/tags/class-v1"]
    if harness_frozen:
        refs.append("refs/tags/harness-frozen")
    return [
        f"cd {public}",
        f"git remote add origin https://github.com/{TARGET}.git",
        "git push origin main",
        f"git push origin {' '.join(refs)}",
    ]


# -- contributors (owner rule: ANI-IN is the only contributor) ------------------------------------

_COAUTHOR_LINE = re.compile(r"co-authored-by\s*:", re.I)
_GENERATED_LINE = re.compile(r"generated with \[?claude", re.I)
_PEOPLE_FILES = ("AUTHORS", "CONTRIBUTORS", "CODEOWNERS")
_OWNERS = {f"@{AUTHOR_NAME}".lower(), AUTHOR_EMAIL.lower()}
DEPENDABOT = (".github/dependabot.yml", ".github/dependabot.yaml")


def _people_file_problems(path: str, text: str) -> list[str]:
    """An AUTHORS, CONTRIBUTORS, or CODEOWNERS file that lists anyone but ANI-IN."""
    codeowners = posixpath.basename(path).split(".")[0].upper() == "CODEOWNERS"
    out = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip().lstrip("-*").strip()
        if not line or line.startswith("#"):
            continue
        if codeowners:
            others = [o for o in line.split()[1:] if o.lower() not in _OWNERS]
            if others:
                out.append(f"{path}:{number}: lists {' '.join(others)}")
        elif AUTHOR_NAME not in line:
            out.append(f"{path}:{number}: lists {line[:60]}")
    return out


def contributor_file_problems(files: Mapping[str, str]) -> list[str]:
    """Public files that credit anyone but ANI-IN, or that would open pull requests as another
    author: Co-authored-by lines, "Generated with Claude" attributions, AUTHORS, CONTRIBUTORS, or
    CODEOWNERS files listing anyone else, and a Dependabot configuration."""
    out: list[str] = []
    for path in sorted(files):
        text = files[path]
        if path in DEPENDABOT:
            out.append(f"{path}: Dependabot would open pull requests as another author")
        if posixpath.basename(path).split(".")[0].upper() in _PEOPLE_FILES:
            out += _people_file_problems(path, text)
        for number, line in enumerate(text.splitlines(), 1):
            if _COAUTHOR_LINE.search(line):
                out.append(f"{path}:{number}: Co-authored-by line")
            if _GENERATED_LINE.search(line):
                out.append(f"{path}:{number}: Generated with Claude attribution")
    return out


def contributor_problems(public: Path, public_files: Iterable[str]) -> list[str]:
    """Every commit of the built repository (author, committer, trailers; the same check as
    platform/scripts/check_contributors.py) and every public file."""
    out = [f"commit {c.line()}" for c in _contributors().commit_problems(public)]
    texts: dict[str, str] = {}
    for path in public_files:
        target = public / path
        if target.is_symlink() or not target.is_file():
            continue
        try:
            texts[path] = target.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            continue
    return out + contributor_file_problems(texts)


def write_tree(repo: Path, entries: Mapping[str, Entry], dest: Path) -> None:
    blobs = read_blobs(repo, entries)
    for path, data in blobs.items():
        target = dest / path
        target.parent.mkdir(parents=True, exist_ok=True)
        mode = entries[path].mode
        if mode == "120000":
            os.symlink(data.decode("utf-8"), target)
            continue
        target.write_bytes(data)
        if mode == "100755":
            target.chmod(0o755)


def assemble(repo: Path, report: Report, dest: Path) -> Release:
    """Write the public repository into `dest` (empty or new): one commit, the rebuilt checkpoint
    tags, the class-v1 release tag, and the harness-frozen record tag only when the build
    repository has a freeze record. Nothing outside `dest` is changed."""
    dest = Path(dest)
    if dest.exists() and any(dest.iterdir()):
        raise ReleaseError(f"{dest} exists and is not empty")
    dest.mkdir(parents=True, exist_ok=True)
    write_tree(repo, {p: report.entries[p] for p in report.selection.included}, dest)
    (dest / REFERENCES_FILE).parent.mkdir(parents=True, exist_ok=True)
    (dest / REFERENCES_FILE).write_bytes(report.references.text.encode("utf-8"))
    _git(dest, "init", "-q", "-b", "main")
    _git(dest, "config", "user.name", AUTHOR_NAME)
    _git(dest, "config", "user.email", AUTHOR_EMAIL)
    _git(dest, "add", "-A", "-f")
    _git(dest, "commit", "-q", "-m", COMMIT_MESSAGE)
    commit = _git(dest, "rev-parse", "HEAD").decode().strip()

    from shipharness.ab.checkpoints import CheckpointError, build_commits, load_checkpoints

    try:
        built = build_commits(dest, dry_run=False)  # platform/scripts/build_checkpoints.py logic
    except CheckpointError as exc:
        raise ReleaseError(f"checkpoint tags: {exc}") from None
    tags = [b.name for b in built]
    if sorted(tags) != sorted(load_checkpoints(dest)):
        raise ReleaseError(f"checkpoint tags {tags} do not match checkpoints.toml")
    public_files = _git(dest, "ls-files", "-z").decode().split("\0")
    public_files = sorted(p for p in public_files if p)
    in_tags: set[str] = set(public_files)
    for tag in tags:
        in_tags |= set(_tree_blobs(dest, f"refs/tags/{tag}"))
    excluded_tests = set(report.excluded_tests)

    def keep(path: str) -> bool:
        return classify(path) is None and path not in excluded_tests

    checkpoints = compare_checkpoints(repo, dest, keep)
    frozen = frozen_check(repo, report.ref, dest)
    release_tag = class_tag(dest, commit)
    return Release(
        report=report,
        public=dest,
        commit=commit,
        tags=tags,
        public_files=public_files,
        tree_leaks=leaks(in_tags),
        checkpoints=checkpoints,
        frozen=frozen,
        class_tag=release_tag,
        missing=missing_expected(public_files),
        push=push_commands(dest, tags, harness_frozen=frozen.record_commit is not None),
        contributors=contributor_problems(dest, public_files),
    )


def dry_run(repo: Path, ref: str, workdir: Path) -> Release:
    return assemble(repo, analyze(repo, ref), workdir)


# -- report -------------------------------------------------------------------------------------


def _top(path: str) -> str:
    return path.split("/", 1)[0] + "/" if "/" in path else "(root files)"


def _file_kind(path: str) -> str:
    name = posixpath.basename(path)
    ext = posixpath.splitext(name)[1].lstrip(".")
    return ext or name


def render(rel: Release, list_file: str, references_file: str) -> str:
    report, sel = rel.report, rel.report.selection
    out: list[str] = []
    w = out.append
    sha = f" ({report.commit[:12]})" if report.commit else ""
    w(f"== 1. Public tree from {report.ref}{sha}: {len(rel.public_files)} files")
    w(f"   built in {rel.public} (one commit {rel.commit[:12]}; temporary, never pushed)")
    for top, n in sorted(Counter(_top(p) for p in rel.public_files).items()):
        w(f"   {top:<20} {n:>4}")
    w(f"   root files: {', '.join(p for p in rel.public_files if '/' not in p)}")
    w(f"   learner scripts: {', '.join(p for p in LEARNER_SCRIPTS if p in rel.public_files)}")
    w(f"   full list: {list_file}")
    w(f"   owner-listed files not present yet (listed, not failed): {len(rel.missing)}")
    for path in rel.missing:
        w(f"     - {path}")
    w("   left out of the build repository's tracked files:")
    by_reason = Counter(r.split(":")[0] for r in sel.excluded.values())
    for reason, n in sorted(by_reason.items()):
        w(f"   {n:>5}  {reason}")
    unlisted = Counter(_top(p) for p, r in sel.excluded.items() if r == REASON_NOT_ALLOWED)
    w(f"   not in the allow-list, by top-level path: {dict(sorted(unlisted.items()))}")
    w(f"   tests left out because they exercise excluded files: {len(report.excluded_tests)}")
    for path, reasons in report.excluded_tests.items():
        w(f"     {path}  ({len(reasons)}; first: {reasons[0]})")
    w("")
    leaked = sorted(set(report.leaks) | set(rel.tree_leaks))
    w("== 2. Leak check (commit and every checkpoint tag): " + ("FAIL" if leaked else "PASS"))
    w("   no private file, grader, hidden grader case, internal script, or export")
    for path, reason in leaked:
        w(f"   LEAK {path}: {reason}")
    w("")
    w(_render_hits(report.hits))
    refs = report.references
    w(
        f"== 4. {REFERENCES_FILE}: {len(refs.sources)} sources, {len(refs.findings)} findings "
        f"(generated from RESEARCH.md and research/notes/; copy in {references_file})"
    )
    w(f"   unresolved finding ids: {', '.join(refs.unresolved) or 'none'}")
    w("")
    w("== 5. Checkpoint tags: rebuilt tree against the build repository's tag tree")
    for c in rel.checkpoints:
        if not c.rebuilt:
            w(f"   {c.name}: build repository only (not in checkpoints.toml, not rebuilt)")
            continue
        if c.build_tree is None:
            w(f"   {c.name}: public only (no tag of that name in the build repository)")
            continue
        tops = Counter(_top(p) for p in c.differing)
        detail = f" ({dict(sorted(tops.items()))})" if tops else ""
        w(
            f"   {c.name}: whole tree {'match' if c.full_match else 'differs'}; "
            f"TeamTrack {'match' if c.app_match else 'DIFFERS'}; "
            f"{len(c.differing)} public file(s) differ{detail}"
        )
    w("   (whole trees differ by design: the build tree also holds the private files)")
    w("")
    f = rel.frozen
    basis = (
        "the build repository's harness-frozen record, exceptions applied"
        if f.basis == "tag"
        else "no freeze record: the content of the build repository's HEAD"
    )
    bad = [p for p, ok in f.paths.items() if not ok]
    w(f"== 6. Frozen content: {'PASS' if not bad else 'FAIL'} against {basis}")
    for path, ok in f.paths.items():
        w(f"   {'match  ' if ok else 'DIFFERS'} {path}")
    if f.checkpoint_differs:
        w(
            f"   record checkpoint trees (whole-tree ids) not equal in the public repo: "
            f"{len(f.checkpoint_differs)} ({', '.join(f.checkpoint_differs)}); see section 5"
        )
    if f.record_commit is None:
        w("   harness-frozen: not written (no freeze record in the build repository)")
    else:
        w(f"   public harness-frozen tag written at {f.record_commit[:12]} with the public")
        w(
            "   checkpoint trees; its own check: "
            + ("PASS" if not f.self_check else "; ".join(f.self_check))
        )
    c = rel.class_tag
    w(
        f"   class-v1 tag written at {c.commit[:12]}; its own check: "
        + ("PASS" if not c.self_check else "; ".join(c.self_check))
    )
    w(f"   (record: {c.paths} content hashes, {c.checkpoint_trees} checkpoint trees, run settings)")
    w("")
    w(f"== 7. Target: {TARGET} (recreated empty by the owner; nothing is pushed by this script)")
    w("   push commands for the owner's release step (printed, never executed):")
    for line in rel.push:
        w(f"   $ {line}")
    w("")
    w(
        "== 8. Contributors: "
        + ("PASS" if not rel.contributors else f"FAIL ({len(rel.contributors)} problem(s))")
        + f": every commit by {AUTHOR_NAME} <{AUTHOR_EMAIL}>, no co-author or generated-with"
        " line, no other AUTHORS/CONTRIBUTORS/CODEOWNERS entry, no Dependabot configuration"
    )
    for problem in rel.contributors:
        w(f"   {problem}")
    w("")
    failures, blockers = rel.failures(), rel.build_failures()
    w("== Dry run: " + ("PASS" if not failures else "FAIL: " + "; ".join(failures)))
    w("== --build would " + ("pass" if not blockers else "refuse: " + "; ".join(blockers)))
    return "\n".join(out) + "\n"


def _render_hits(hits: list[Hit]) -> str:
    out: list[str] = []
    w = out.append
    files = sorted({h.path for h in hits})
    w(f"== 3. Broken references (reported here; --build fails): {len(hits)} in {len(files)} files")
    w(
        "   by hit kind: "
        + ", ".join(f"{k} {n}" for k, n in Counter(h.kind for h in hits).most_common())
    )
    w(
        "   by file kind: "
        + ", ".join(f"{k} {n}" for k, n in Counter(_file_kind(h.path) for h in hits).most_common())
    )
    w("   top files:")
    for path, n in Counter(h.path for h in hits).most_common(15):
        w(f"   {n:>5}  {path}")
    w("   most frequent patterns:")
    first: dict[str, Hit] = {}
    for h in hits:
        first.setdefault(h.pattern, h)
    for pattern, n in Counter(h.pattern for h in hits).most_common(15):
        ex = first[pattern]
        w(f"   {n:>5}  {pattern}   e.g. {ex.path}:{ex.line}")
    grouped: dict[str, list[Hit]] = defaultdict(list)
    for h in hits:
        grouped[h.path].append(h)
    for path in files:
        w(f"-- {path} ({len(grouped[path])})")
        for h in grouped[path]:
            w(f"   {h.path}:{h.line}: [{h.kind}] {h.text}  |  {h.excerpt}")
    return "\n".join(out) + "\n"


# -- build --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class BuildResult:
    commit: str
    tags: list[str]


def build(
    repo: Path, ref: str, dest: Path, verify: Iterable[str] | None = DEFAULT_VERIFY
) -> BuildResult:
    """The release build: refuses before writing on a leak, a broken reference, or an unresolved
    finding id; after writing, on frozen content or a checkpoint TeamTrack tree that differs."""
    report = analyze(repo, ref)
    if report.build_failures():
        raise ReleaseError("release checks failed: " + "; ".join(report.build_failures()))
    rel = assemble(repo, report, Path(dest))
    if rel.build_failures():
        raise ReleaseError(
            f"release checks failed ({dest} kept for inspection): "
            + "; ".join(rel.build_failures())
        )
    if verify:
        done = subprocess.run(list(verify), cwd=dest, check=False)
        if done.returncode != 0:
            raise ReleaseError(f"verification failed ({' '.join(verify)}): exit {done.returncode}")
    return BuildResult(rel.commit, rel.tags)


# -- command line -------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="make_release",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="build in a temp folder (default)")
    mode.add_argument("--build", type=Path, metavar="DIR", help="build the public repo into DIR")
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument(
        "--workdir", type=Path, default=None, help="dry run: empty folder (default: a new temp one)"
    )
    parser.add_argument("--list-file", default=DEFAULT_LIST_FILE)
    parser.add_argument("--references-file", default=DEFAULT_REFERENCES_FILE)
    parser.add_argument("--report-file", default=DEFAULT_REPORT_FILE)
    parser.add_argument(
        "--skip-verify", action="store_true", help="--build: skip the fast-suite verification"
    )
    args = parser.parse_args(argv)
    try:
        if args.build:
            verify = None if args.skip_verify else DEFAULT_VERIFY
            result = build(args.repo, args.ref, args.build, verify)
            print(f"built {args.build}: commit {result.commit[:12]}, tags {', '.join(result.tags)}")
            print("nothing was pushed; the owner's release step pushes after a final yes")
            return 0
        workdir = args.workdir or Path(tempfile.mkdtemp(prefix="shipharness-public-"))
        rel = dry_run(args.repo, args.ref, workdir)
    except ReleaseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    Path(args.list_file).write_text("\n".join(rel.public_files) + "\n", encoding="utf-8")
    Path(args.references_file).write_text(rel.report.references.text, encoding="utf-8")
    text = render(rel, args.list_file, args.references_file)
    Path(args.report_file).write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    print(f"full report: {args.report_file}")
    return 0 if not rel.failures() else 1


if __name__ == "__main__":
    raise SystemExit(main())
