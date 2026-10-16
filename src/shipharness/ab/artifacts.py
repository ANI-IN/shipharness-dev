"""Harness-owned workspace files (contract I-6) and diff filtering.

The layers place these files in `prepare_workspace`, and the agent may update the state files
(progress.md, session-handoff.md, exec plans) while it works. They are never product changes: the
referee strips them before applying an arm's diff, the blinded reviewer never sees them, and the
diff-scope check does not count them as out-of-scope files. The same list applies to both arms.
"""

from __future__ import annotations

import fnmatch
import re
from typing import overload

HARNESS_ARTIFACT_PATTERNS: tuple[str, ...] = (
    # instructions layer
    "AGENTS.md",
    "ARCHITECTURE.md",
    "docs/SECURITY.md",
    "docs/RELIABILITY.md",
    "docs/QUALITY_SCORE.md",
    "docs/PLANS.md",
    "docs/design-docs/**",
    "docs/product-specs/**",
    "docs/references/*-llms.txt",
    ".agents/**",
    # state layer
    "init.sh",
    "progress.md",
    "session-handoff.md",
    "docs/exec-plans/**",
    # scope layer
    "feature_list.json",
    "feature_list.schema.json",
)

_HEADER = re.compile(rb"^diff --git (\"(?:[^\"\\]|\\.)*\"|\S+) (\"(?:[^\"\\]|\\.)*\"|\S+)\s*$")


def _match(path: str, pattern: str) -> bool:
    """Segment-wise glob: `*` stays within one path segment; a trailing `**` matches the rest."""
    parts, pats = path.split("/"), pattern.split("/")
    if pats[-1] == "**":
        head = pats[:-1]
        return len(parts) > len(head) and all(
            fnmatch.fnmatchcase(p, q) for p, q in zip(parts, head, strict=False)
        )
    return len(parts) == len(pats) and all(
        fnmatch.fnmatchcase(p, q) for p, q in zip(parts, pats, strict=True)
    )


def is_harness_artifact(path: str) -> bool:
    clean = path.replace("\\", "/")
    while clean.startswith("./"):
        clean = clean[2:]
    return any(_match(clean, pattern) for pattern in HARNESS_ARTIFACT_PATTERNS)


def _unquote(token: bytes) -> str:
    text = token.decode("utf-8", errors="replace")
    if text.startswith('"') and text.endswith('"'):
        text = (
            text[1:-1]
            .encode("utf-8")
            .decode("unicode_escape")
            .encode("latin-1")
            .decode("utf-8", errors="replace")
        )
    return text[2:] if text[:2] in ("a/", "b/") else text


def _sections(diff: bytes) -> list[tuple[list[str], bytes]]:
    """Split a git diff into (paths, section bytes). Text before the first header has no paths."""
    out: list[tuple[list[str], bytes]] = []
    current: list[bytes] = []
    paths: list[str] = []
    for line in diff.splitlines(keepends=True):
        match = _HEADER.match(line.rstrip(b"\r\n"))
        if match:
            if current:
                out.append((paths, b"".join(current)))
            current, paths = [line], [_unquote(match.group(1)), _unquote(match.group(2))]
        else:
            current.append(line)
    if current:
        out.append((paths, b"".join(current)))
    return out


@overload
def strip_harness_artifacts(diff: str) -> str: ...
@overload
def strip_harness_artifacts(diff: bytes) -> bytes: ...
def strip_harness_artifacts(diff: str | bytes) -> str | bytes:
    """Drop every file section whose old and new paths are both harness artifacts."""
    raw = diff.encode("utf-8") if isinstance(diff, str) else diff
    kept = [
        body
        for paths, body in _sections(raw)
        if not (paths and all(is_harness_artifact(p) for p in paths if p != "/dev/null"))
    ]
    joined = b"".join(kept)
    return joined.decode("utf-8") if isinstance(diff, str) else joined


def diff_paths(diff: str | bytes) -> list[str]:
    """The new-side path of every file section, in order."""
    raw = diff.encode("utf-8") if isinstance(diff, str) else diff
    return [paths[-1] for paths, _body in _sections(raw) if paths]
