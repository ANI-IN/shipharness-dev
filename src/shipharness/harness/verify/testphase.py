"""Test-phase hook of the verify layer: every test the agent proposed in the test phase goes through
the five filters (CONTRACTS §14, owned by the filters package); discarded tests are removed from
the workspace with their reason, kept tests are committed.

Workspace files are read and written on the host without following links (untrusted workspace).
"""

from __future__ import annotations

import ast
import hashlib
from collections.abc import Callable
from pathlib import Path
from typing import Any

from shipharness.runner.paths import resolve_in_workspace
from shipharness.runner.tools import iter_workspace_files

TEST_ROOT = "tests/visible/"
Pipeline = Callable[[list[dict[str, str]], Any, dict[str, str]], list[Any]]


class PipelineUnavailable(RuntimeError):
    """The filter pipeline cannot run (package or helper missing)."""


def snapshot(workspace: Path) -> tuple[dict[str, str], dict[str, str]]:
    """(sha256 of every workspace file, text of every visible test file)."""
    shas: dict[str, str] = {}
    texts: dict[str, str] = {}
    root = Path(workspace)
    for path in iter_workspace_files(root):
        rel = path.relative_to(root).as_posix()
        data = path.read_bytes()
        shas[rel] = hashlib.sha256(data).hexdigest()
        if rel.startswith(TEST_ROOT) and rel.endswith(".py"):
            texts[rel] = data.decode("utf-8", errors="replace")
    return shas, texts


def _test_nodes(tree: ast.Module) -> list[tuple[str, ast.AST]]:
    nodes: list[tuple[str, ast.AST]] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith(
            "test"
        ):
            nodes.append((node.name, node))
        elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            for item in node.body:
                if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef) and (
                    item.name.startswith("test")
                ):
                    nodes.append((f"{node.name}::{item.name}", item))
    return nodes


def _span(node: ast.AST) -> tuple[int, int]:
    decorators = getattr(node, "decorator_list", [])
    start = min([node.lineno, *(d.lineno for d in decorators)])  # type: ignore[attr-defined]
    return start, node.end_lineno or node.lineno  # type: ignore[attr-defined]


def _sources(text: str) -> dict[str, str]:
    lines = text.splitlines()
    out = {}
    for name, node in _test_nodes(ast.parse(text)):
        start, end = _span(node)
        out[name] = "\n".join(lines[start - 1 : end])
    return out


def find_candidates(
    workspace: Path, start_texts: dict[str, str]
) -> tuple[list[dict[str, str]], dict[str, str]]:
    """(candidates {test_id, file, source}, unparseable test files -> reason). A candidate is a
    test function that is new or changed since the start of the test phase."""
    _shas, now_texts = snapshot(workspace)
    candidates: list[dict[str, str]] = []
    broken: dict[str, str] = {}
    for rel, text in sorted(now_texts.items()):
        if not Path(rel).name.startswith("test") or start_texts.get(rel) == text:
            continue
        try:
            current = _sources(text)
        except SyntaxError as exc:
            broken[rel] = f"does not parse: {exc.msg} (line {exc.lineno})"
            continue
        try:
            before = _sources(start_texts.get(rel, ""))
        except SyntaxError:
            before = {}
        for name, source in current.items():
            if before.get(name) != source:
                candidates.append({"test_id": f"{rel}::{name}", "file": rel, "source": source})
    return candidates, broken


def remove_tests(workspace: Path, by_file: dict[str, list[str]]) -> list[str]:
    """Remove the named tests (`name` or `Class::name`) from each file; delete a file left with no
    tests. Returns the files changed."""
    changed = []
    for rel, names in by_file.items():
        path = resolve_in_workspace(workspace, rel)
        if not rel.startswith(TEST_ROOT) or path.is_symlink() or not path.is_file():
            raise ValueError(f"not a visible test file in the workspace: {rel!r}")
        text = path.read_bytes().decode("utf-8", errors="replace")
        nodes = dict(_test_nodes(ast.parse(text)))
        lines = text.splitlines(keepends=True)
        spans = sorted((_span(nodes[n]) for n in names if n in nodes), reverse=True)
        for start, end in spans:
            del lines[start - 1 : end]
        remaining = "".join(lines)
        if not _test_nodes(ast.parse(remaining)):
            path.unlink()
        else:
            path.write_text(remaining, encoding="utf-8", newline="")
        changed.append(rel)
    return changed


def delete_files(workspace: Path, rels: list[str]) -> None:
    for rel in rels:
        path = resolve_in_workspace(workspace, rel)
        if rel.startswith(TEST_ROOT) and path.is_file() and not path.is_symlink():
            path.unlink()


def filters_pipeline(
    candidates: list[dict[str, str]], ctx: Any, source_shas: dict[str, str]
) -> list[Any]:
    """Default pipeline: the filters package (CONTRACTS §14). It must expose CandidateTest,
    run_pipeline, and build_filter_context(workspace, sandbox, source_shas_at_phase_start)."""
    try:
        from shipharness import filters  # type: ignore[attr-defined]
    except ImportError as exc:
        raise PipelineUnavailable(f"shipharness.filters is not installed ({exc})") from None
    missing = [
        n
        for n in ("CandidateTest", "run_pipeline", "build_filter_context")
        if not hasattr(filters, n)
    ]
    if missing:
        raise PipelineUnavailable(f"shipharness.filters lacks {', '.join(missing)}")
    fctx = filters.build_filter_context(
        workspace=ctx.workspace, sandbox=ctx.sandbox, source_shas_at_phase_start=source_shas
    )
    cands = [filters.CandidateTest(**c) for c in candidates]
    return list(filters.run_pipeline(cands, fctx, ctx.bus))


def _field(result: Any, name: str) -> Any:
    return result.get(name) if isinstance(result, dict) else getattr(result, name)


def discarded_reasons(results: list[Any]) -> dict[str, str]:
    """test_id -> reason of the first failing filter."""
    out: dict[str, str] = {}
    for r in sorted(results, key=lambda r: int(_field(r, "filter"))):
        if not _field(r, "passed"):
            out.setdefault(str(_field(r, "test_id")), str(_field(r, "reason")))
    return out
