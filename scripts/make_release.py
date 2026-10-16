"""Build the learner repository from an allow-list of this build repository (release, M11).

    uv run python scripts/make_release.py                  # dry run (the default): report only
    uv run python scripts/make_release.py --dry-run        # the same
    uv run python scripts/make_release.py --build DIR      # write the learner tree into DIR

The dry run prints the included files (counts per top-level path; the full list goes to
--list-file), the tests left out because they exercise excluded files, REFERENCES.md, and the
reference check. It exits 1 when solution or hidden grader content would be included, when an
included file references an excluded file, or when a cited finding id does not resolve.

--build refuses unless the dry-run checks pass. It writes the selected files of --ref (default
HEAD) into DIR, adds REFERENCES.md, runs `git init`, makes one commit as ANI-IN with a fixed
message, rebuilds the checkpoint tags on top of it (shipharness.ab.checkpoints.build_commits,
teamtrack/reference/checkpoints.toml), and runs the learner tree's fast suite. Nothing is pushed;
the script never talks to GitHub.

Only files tracked at --ref are read, straight from git objects, so the working tree and
untracked files never leak into the learner tree.
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
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# -- owner decisions ----------------------------------------------------------------------------

ALLOW_DIRS = (
    "src/",
    "teamtrack/",
    "sandbox/",
    "config/",
    "datasets/",
    "skills/",
    "tests/",
    "submodules/",
    "final-project/",
    "setup/",
    "slides/",
    ".vale/",
    ".github/workflows/",
)
ALLOW_FILES = (
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "Makefile",
    "pyproject.toml",
    "uv.lock",
    ".env.example",
    ".gitignore",
    ".gitattributes",
    ".dockerignore",
    ".python-version",
    ".vale.ini",
)
# Integrator decision (a): scripts/ is not allow-listed, but these three are used by `make lint`,
# CI, tests, and the testgen library targets.
EXTRA_SCRIPTS = ("scripts/anchors.py", "scripts/lint_prose.py", "scripts/fetch_testgen_libs.py")
EXCLUDED_FILES = ("RESEARCH.md", "DESIGN.md", "CONTRACTS.md", "VERIFICATION.md", "CODEOWNERS")
EXCLUDED_DIRS = ("research/", "instructor/")
EXCLUDED_SCRIPTS = (
    "scripts/pilot.py",
    "scripts/build_checkpoints.py",
    "scripts/probe_langsmith.py",
    "scripts/build_features_dataset.py",
    "scripts/build_testgen_dataset.py",
    "scripts/make_release.py",
    "scripts/publish_solutions.py",
)
# Flagged inclusions (decision c): the referee's held-out tests and the reference patches.
FLAGGED_DIRS = ("teamtrack/tests/hidden/", "teamtrack/reference/")

TEACHING = tuple(f"A{n}" for n in range(1, 8)) + tuple(f"B{n}" for n in range(1, 14))
DO_NOT_CITE = ("B15",)

AUTHOR_NAME = "ANI-IN"
AUTHOR_EMAIL = "44803072+ANI-IN@users.noreply.github.com"
COMMIT_MESSAGE = "shipharness: Module 1 learner release"
DEFAULT_VERIFY = ("uv", "run", "--frozen", "pytest", "-q")
DEFAULT_LIST_FILE = "/tmp/shipharness-release-files.txt"
DEFAULT_REFERENCES_FILE = "/tmp/shipharness-release-REFERENCES.md"
DEFAULT_REPORT_FILE = "/tmp/shipharness-release-report.txt"

REASON_SOLUTION = "solution, grader, or hidden case content (owner decision 2)"
REASON_OWNER = "excluded by the owner (decision 2)"
REASON_NOT_ALLOWED = "not in the allow-list"


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
    """Anything under a solution/ or grader/ folder, or under a hidden/ folder in submodules/."""
    dirs = _segments(path)
    if "solution" in dirs or "grader" in dirs:
        return True
    return path.startswith("submodules/") and "hidden" in dirs


def guard_violations(paths: Iterable[str]) -> list[str]:
    return [p for p in paths if is_guarded(p)]


def _owner_excluded(path: str) -> bool:
    return (
        path in EXCLUDED_FILES
        or path in EXCLUDED_SCRIPTS
        or any(path.startswith(d) for d in EXCLUDED_DIRS)
    )


def _allowed(path: str) -> bool:
    return path in ALLOW_FILES or path in EXTRA_SCRIPTS or path.startswith(ALLOW_DIRS)


def classify(path: str) -> str | None:
    """None when `path` goes into the learner tree, else the reason it does not."""
    if is_guarded(path):
        return REASON_SOLUTION
    if _owner_excluded(path):
        return REASON_OWNER
    if not _allowed(path):
        return REASON_NOT_ALLOWED
    return None


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
        if p.startswith("scripts/") and p.endswith(".py") and p.count("/") == 1
    }

    def token_hit(token: str) -> str | None:
        token = token[2:] if token.startswith("./") else token
        folder = token.rstrip("/")
        is_excluded_folder = "/" in folder and classify(folder + "/x") in (
            REASON_OWNER,
            REASON_SOLUTION,
        )
        for path in excluded:
            if token == path or token.endswith("/" + path):
                return path
            if is_excluded_folder and path.startswith(folder + "/"):
                return path
        base = posixpath.basename(token)
        if base in basenames:
            return basenames[base]
        if token in stems:
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
        reasons: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if id(node) in docs:
                    continue
                for token in _TOKEN.findall(node.value):
                    hit = token_hit(token)
                    if hit:
                        reasons.append(f"line {node.lineno}: names {hit}")
        modules = _module_names(tree)
        imports[path] = modules
        for name in modules:
            last = name.rsplit(".", 1)[-1]
            if name.startswith("scripts") and last in stems:
                reasons.append(f"imports {stems[last]}")
        if reasons:
            found[path] = sorted(set(reasons))
    changed = True
    while changed:  # tests that import a flagged helper module
        changed = False
        helpers = {posixpath.splitext(posixpath.basename(p))[0]: p for p in found}
        for path, modules in imports.items():
            if path in found:
                continue
            for name in modules:
                last = name.rsplit(".", 1)[-1]
                if last in helpers and not last.startswith("test_"):
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
_SCRIPT_STEMS = "|".join(posixpath.splitext(posixpath.basename(p))[0] for p in EXCLUDED_SCRIPTS)
_SCRIPT = re.compile(rf"(?:\bscripts/)?\b(?:{_SCRIPT_STEMS})\.py\b|\bscripts/(?:{_SCRIPT_STEMS})\b")
_SOLUTION = re.compile(
    r"(?<![\w.-])(?:solution|grader)/[\w./-]*|\bsubmodules/[\w.-]+/(?:[\w.-]+/)*hidden/[\w./-]*"
)
_MENTION = re.compile(
    rf"\b(?:{_DOCS})\.md\b"
    rf"|\b(?:{_DOCS})\b"
    r"|\bCODEOWNERS\b"
    r"|(?:(?<![\w./-])|(?<=\./))(?:research|instructor)/[\w./-]*"
    r"|\bR-[a-e](?:\.md)?\b"
)
_RUN_ID = re.compile(r"\b(?:ab|r)-\d{8}-\d{6}-[0-9a-f]{6}\b")
_SOURCE_CITE = re.compile(r"\bF-[a-e]-\d+\b|\b[AB]\d{1,2}\b")
_NOT_INCLUDED = re.compile(r"\bnot\s+(?:included|shipped|part\s+of|in\s+this\s+repo)", re.I)


def _excluded_target(path: str, target: str) -> str | None:
    """The excluded file or folder a link target points at, or None."""
    if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    norm = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
    norm = norm.lstrip("/")
    if norm in EXCLUDED_FILES or norm in EXCLUDED_SCRIPTS:
        return norm
    for folder in EXCLUDED_DIRS:
        if norm == folder.rstrip("/") or norm.startswith(folder):
            return folder
    if is_guarded(norm + "/x"):
        return "solution/"
    # A wrong relative path still points the reader at an excluded file.
    if posixpath.basename(norm) in EXCLUDED_FILES:
        return posixpath.basename(norm)
    for folder in EXCLUDED_DIRS:
        if f"/{folder}" in f"/{target}":
            return folder
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
        return "submodules/*/hidden/" if "hidden/" in text else text.split("/", 1)[0] + "/"
    if kind == "run-id":
        return "VERIFICATION run id"
    if text.startswith(("research/", "instructor/", "../", "./")):
        parts = [p for p in text.split("/") if p not in ("..", ".", "")]
        return "/".join(parts[:2]) + "/" if len(parts) > 2 else parts[0] + "/"
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
    path: str, line: str, run_ids: frozenset[str], existing: frozenset[str] | None = None
) -> list[tuple[int, str, str, str]]:
    taken: list[tuple[int, int]] = []
    found: list[tuple[int, str, str, str]] = []
    for m in _LINK.finditer(line):
        target = _excluded_target(path, m.group(1))
        if target and _take(taken, m):
            found.append((m.start(), "link", m.group(0), _pattern("link", "", target)))
    for m in _SECTION.finditer(line):
        if _take(taken, m):
            found.append((m.start(), "section-cite", m.group(0), _pattern("section-cite", m[0])))
    if run_ids and not _SOURCE_CITE.search(line):
        for m in _RUN_ID.finditer(line):
            if m.group(0) in run_ids and _take(taken, m):
                found.append((m.start(), "run-id", m.group(0), _pattern("run-id", "")))
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
) -> list[Hit]:
    """Every place in `text` that links to, cites, or names an excluded file. Priority on
    overlapping matches: link, section citation, run id, script, solution path, plain mention.
    `existing`: the tracked excluded paths, when known (research/ and instructor/ mentions must
    name one of them)."""
    hits: list[Hit] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for _, kind, matched, label in _line_hits(path, line, run_ids, existing):
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
        raise ReleaseError("scripts/lint_prose.py not found")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.lint_text, module.ALLOW_MARKER


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
    ref: str
    selection: Selection
    excluded_tests: dict[str, list[str]]
    guard: list[str]
    hits: list[Hit]
    references: References
    entries: dict[str, Entry] = field(default_factory=dict)
    commit: str = ""

    def problems(self) -> list[str]:
        out: list[str] = []
        if self.guard:
            out.append(f"{len(self.guard)} solution/grader/hidden path(s) would be included")
        if self.hits:
            files = len({h.path for h in self.hits})
            out.append(f"{len(self.hits)} reference(s) to excluded files in {files} file(s)")
        if self.references.unresolved:
            out.append(f"unresolved finding ids: {', '.join(self.references.unresolved)}")
        return out

    @property
    def ok(self) -> bool:
        return not self.problems()


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
    hits: list[Hit] = []
    for path in sorted(texts):
        hits += scan_references(path, texts[path], run_ids, existing)
    hits += scan_references("REFERENCES.md", references.text, run_ids, existing)
    return Report(
        ref=ref,
        selection=sel,
        excluded_tests=excluded_tests,
        guard=guard_violations(sel.included),
        hits=hits,
        references=references,
        entries=entries,
        commit=_git(repo, "rev-parse", f"{ref}^{{commit}}").decode().strip(),
    )


# -- report -------------------------------------------------------------------------------------


def _top(path: str) -> str:
    return path.split("/", 1)[0] + "/" if "/" in path else "(root files)"


def _file_kind(path: str) -> str:
    name = posixpath.basename(path)
    ext = posixpath.splitext(name)[1].lstrip(".")
    return ext or name


def render(report: Report, list_file: str, references_file: str) -> str:
    sel = report.selection
    out: list[str] = []
    w = out.append
    sha = f" ({report.commit[:12]})" if report.commit else ""
    w(f"== Learner tree from {report.ref}{sha}: {len(sel.included) + 1} files")
    w("   (the tracked files below plus the generated REFERENCES.md)")
    counts = Counter(_top(p) for p in sel.included)
    for top, n in sorted(counts.items()):
        w(f"   {top:<20} {n:>4}")
    roots = [p for p in sel.included if "/" not in p]
    w(f"   root files: {', '.join(roots)}")
    w(f"   full list: {list_file}")
    w("")
    w("== Flagged inclusions (integrator decisions a and c)")
    for path in EXTRA_SCRIPTS:
        w(f"   {path}: {'included' if path in sel.included else 'MISSING at this ref'}")
    for folder in FLAGGED_DIRS:
        n = sum(p.startswith(folder) for p in sel.included)
        w(f"   {folder}: {n} files included")
    w("")
    w("== Left out")
    by_reason = Counter(r.split(":")[0] for r in sel.excluded.values())
    for reason, n in sorted(by_reason.items()):
        w(f"   {n:>4}  {reason}")
    excl_tops = Counter(_top(p) for p, r in sel.excluded.items() if r == REASON_SOLUTION)
    if excl_tops:
        w(f"   solution/grader/hidden by top-level path: {dict(sorted(excl_tops.items()))}")
    w("")
    w(f"== Excluded tests (integrator decision b): {len(report.excluded_tests)}")
    for path, reasons in report.excluded_tests.items():
        w(f"   {path}")
        for reason in reasons:
            w(f"      {reason}")
    w("")
    w("== Solution/hidden guard: " + ("PASS" if not report.guard else "FAIL"))
    for path in report.guard:
        w(f"   would include {path}")
    w("")
    refs = report.references
    w(
        f"== REFERENCES.md: {len(refs.sources)} sources, {len(refs.findings)} findings "
        f"(also written to {references_file})"
    )
    if refs.unresolved:
        w(f"   UNRESOLVED finding ids: {', '.join(refs.unresolved)}")
    w(refs.text)
    w(_render_hits(report.hits))
    w("== Result: " + ("PASS" if report.ok else "FAIL: " + "; ".join(report.problems())))
    return "\n".join(out) + "\n"


def _render_hits(hits: list[Hit]) -> str:
    out: list[str] = []
    w = out.append
    files = sorted({h.path for h in hits})
    w(f"== Reference check: {len(hits)} hits in {len(files)} files")
    w(
        "   by hit kind: "
        + ", ".join(f"{k} {n}" for k, n in Counter(h.kind for h in hits).most_common())
    )
    w(
        "   by file kind: "
        + ", ".join(f"{k} {n}" for k, n in Counter(_file_kind(h.path) for h in hits).most_common())
    )
    w("   most frequent patterns:")
    first: dict[str, Hit] = {}
    for h in hits:
        first.setdefault(h.pattern, h)
    for pattern, n in Counter(h.pattern for h in hits).most_common(15):
        ex = first[pattern]
        w(f"   {n:>5}  {pattern}   e.g. {ex.path}:{ex.line}")
    grouped: dict[str, dict[str, list[Hit]]] = defaultdict(lambda: defaultdict(list))
    for h in hits:
        grouped[h.path][h.kind].append(h)
    for path in files:
        total = sum(len(v) for v in grouped[path].values())
        w(f"-- {path} ({total})")
        for kind in sorted(grouped[path]):
            w(f"   [{kind}]")
            for h in grouped[path][kind]:
                w(f"     {h.path}:{h.line}: {h.text}  |  {h.excerpt}")
    return "\n".join(out) + "\n"


# -- build --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class BuildResult:
    commit: str
    tags: list[str]


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


def build(
    repo: Path, ref: str, dest: Path, verify: Iterable[str] | None = DEFAULT_VERIFY
) -> BuildResult:
    report = analyze(repo, ref)
    if not report.ok:
        raise ReleaseError("dry-run checks failed: " + "; ".join(report.problems()))
    dest = Path(dest)
    if dest.exists() and any(dest.iterdir()):
        raise ReleaseError(f"{dest} exists and is not empty")
    dest.mkdir(parents=True, exist_ok=True)
    write_tree(repo, {p: report.entries[p] for p in report.selection.included}, dest)
    (dest / "REFERENCES.md").write_bytes(report.references.text.encode("utf-8"))
    _git(dest, "init", "-q", "-b", "main")
    _git(dest, "config", "user.name", AUTHOR_NAME)
    _git(dest, "config", "user.email", AUTHOR_EMAIL)
    _git(dest, "add", "-A", "-f")
    _git(dest, "commit", "-q", "-m", COMMIT_MESSAGE)
    commit = _git(dest, "rev-parse", "HEAD").decode().strip()

    from shipharness.ab.checkpoints import build_commits, load_checkpoints

    built = build_commits(dest, dry_run=False)
    tags = [b.name for b in built]
    if sorted(tags) != sorted(load_checkpoints(dest)):
        raise ReleaseError(f"checkpoint tags {tags} do not match checkpoints.toml")
    if verify:
        done = subprocess.run(list(verify), cwd=dest, check=False)
        if done.returncode != 0:
            raise ReleaseError(f"verification failed ({' '.join(verify)}): exit {done.returncode}")
    return BuildResult(commit, tags)


# -- command line -------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="make_release",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="report only (the default)")
    mode.add_argument("--build", type=Path, metavar="DIR", help="write the learner repo into DIR")
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--ref", default="HEAD")
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
            return 0
        report = analyze(args.repo, args.ref)
    except ReleaseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    Path(args.list_file).write_text("\n".join(report.selection.included) + "\n", encoding="utf-8")
    Path(args.references_file).write_text(report.references.text, encoding="utf-8")
    text = render(report, args.list_file, args.references_file)
    Path(args.report_file).write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
