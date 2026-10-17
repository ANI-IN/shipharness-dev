"""Point every evidence link at the file that holds its anchor.

Course pages link to `docs/evidence.md#<anchor>` (the index) and to
`docs/evidence/<part>.md#<anchor>` (s1, s2, s3, s4, final, general). This script maps every anchor
(`<a id="...">`, `<a name="...">`, and GitHub heading anchors) to the evidence file that defines it,
and rewrites each link whose target file lacks the anchor to the one file that has it. Links inside
the evidence files themselves, `(#anchor)` and `(s1.md#anchor)`, are handled the same way.

When an anchor is defined in more than one part file, a section page (0N-*/) takes its own part
(sN.md), a final-project page takes final.md, and any other page takes general.md.

Re-runnable: a second run changes nothing. It reports anchors defined in more than one evidence file
(page-structure headings that every file or the index shares are left out), links it could not
place because of such a duplicate, and links to anchors defined nowhere.

Usage (repository root):
  uv run python platform/scripts/fix_evidence_links.py           # rewrite links, report the rest
  uv run python platform/scripts/fix_evidence_links.py --check   # change nothing; exit 1 if any
"""

from __future__ import annotations

import argparse
import os
import posixpath
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

INDEX = "docs/evidence.md"
PARTS_DIR = "docs/evidence/"
SKIP_DIRS = {".git", ".venv", "node_modules", ".shipharness", "exports", ".hypothesis", ".claude"}
# Pages filled from live runs or kept as a log; never rewritten here.
DO_NOT_EDIT = re.compile(
    r"(^|/)assignment/solution/live/|(^|/)solution/work/live/|(^|/)solution/captured/"
    r"|^VERIFICATION\.md$"
)

_FENCE = re.compile(r"^\s*(```|~~~)")
_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_HTML_ANCHOR = re.compile(r"<a\s+(?:[^>]*?\s)?(?:id|name)=[\"']([^\"']+)[\"']", re.IGNORECASE)
_LINK = re.compile(r"\]\(([^()\s#]*)#([^()\s]+)\)")


def slug(heading: str) -> str:
    """The anchor GitHub gives a heading (before the -1, -2 suffixes for repeats)."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors_in(text: str) -> set[str]:
    """Every anchor a markdown page defines: HTML anchors and heading anchors."""
    found: set[str] = set()
    counts: dict[str, int] = {}
    fenced = False
    for line in text.splitlines():
        if _FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        found.update(_HTML_ANCHOR.findall(line))
        heading = _HEADING.match(line)
        if heading:
            base = slug(heading.group(2))
            n = counts.get(base, 0)
            counts[base] = n + 1
            found.add(base if n == 0 else f"{base}-{n}")
    return found


def evidence_files(root: Path) -> list[str]:
    files = [INDEX] if (root / INDEX).is_file() else []
    parts = root / PARTS_DIR
    if parts.is_dir():
        files += sorted(f"{PARTS_DIR}{p.name}" for p in parts.glob("*.md"))
    return files


def anchor_index(root: Path) -> dict[str, list[str]]:
    """Anchor -> the evidence files (repository-relative) that define it."""
    index: dict[str, list[str]] = {}
    for rel in evidence_files(root):
        for anchor in anchors_in((root / rel).read_text(encoding="utf-8")):
            index.setdefault(anchor, []).append(rel)
    return index


def preferred(page: str) -> str:
    """The part file a page's evidence belongs in."""
    section = re.match(r"0(\d)-", page)
    if section:
        return f"{PARTS_DIR}s{section.group(1)}.md"
    if page.startswith("final-project/"):
        return f"{PARTS_DIR}final.md"
    return f"{PARTS_DIR}general.md"


def duplicates(index: dict[str, list[str]], files: list[str]) -> dict[str, list[str]]:
    """Anchors in two or more evidence files, without the page-structure headings."""
    return {
        anchor: sorted(holders)
        for anchor, holders in sorted(index.items())
        if len(holders) > 1 and INDEX not in holders and len(holders) < len(files)
    }


def markdown_files(root: Path) -> list[str]:
    found: list[str] = []
    for folder, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            if name.endswith(".md"):
                rel = (Path(folder) / name).relative_to(root).as_posix()
                if not DO_NOT_EDIT.search(rel):
                    found.append(rel)
    return found


@dataclass
class Report:
    changed: list[str] = field(default_factory=list)
    missing: list[tuple[str, str]] = field(default_factory=list)  # (page, link target)
    ambiguous: list[tuple[str, str]] = field(default_factory=list)
    duplicates: dict[str, list[str]] = field(default_factory=dict)


def fix(root: Path, *, write: bool = True) -> Report:
    root = Path(root)
    index = anchor_index(root)
    evidence = set(evidence_files(root))
    report = Report(duplicates=duplicates(index, sorted(evidence)))
    for page in markdown_files(root):
        page_dir = posixpath.dirname(page)
        text = (root / page).read_text(encoding="utf-8")

        def place(match: re.Match[str], page: str = page, page_dir: str = page_dir) -> str:
            path, anchor = match.group(1), match.group(2)
            target = posixpath.normpath(posixpath.join(page_dir, path)) if path else page
            if target not in evidence:
                return match.group(0)
            holders = index.get(anchor, [])
            if target in holders:
                return match.group(0)
            shown = f"{path}#{anchor}" if path else f"#{anchor}"
            if not holders:
                report.missing.append((page, shown))
                return match.group(0)
            holder = holders[0]
            if len(holders) > 1:
                if preferred(page) not in holders:
                    report.ambiguous.append((page, shown))
                    return match.group(0)
                holder = preferred(page)
            new = posixpath.relpath(holder, page_dir or ".") if holder != page else ""
            return f"]({new}#{anchor})"

        new_text = _LINK.sub(place, text)
        if new_text != text:
            report.changed.append(page)
            if write:
                (root / page).write_text(new_text, encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="change nothing; exit 1 if any")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args(argv)
    report = fix(args.root, write=not args.check)
    verb = "would rewrite" if args.check else "rewrote"
    for page in report.changed:
        print(f"{verb} {page}")
    for anchor, files in report.duplicates.items():
        print(f"x anchor {anchor} is defined in {', '.join(files)}")
    for page, link in report.ambiguous:
        print(f"x {page}: {link} (anchor in more than one evidence file)")
    for page, link in report.missing:
        print(f"x {page}: {link} (anchor defined nowhere)")
    problems = len(report.duplicates) + len(report.ambiguous) + len(report.missing)
    print(f"{len(report.changed)} pages {verb}, {problems} problems")
    return 1 if problems or (args.check and report.changed) else 0


if __name__ == "__main__":
    sys.exit(main())
