"""Shared paths and helpers for the A1 grader tests."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

SOLUTION = Path(__file__).resolve().parents[2]
A1 = SOLUTION.parent
STARTER = A1 / "assignment" / "starter"
SOLUTION_WORK = SOLUTION / "work"
GRADER = SOLUTION / "grader"


def load(name: str, path: Path) -> ModuleType:
    """Import a module from a file path (the submodule folder name is not a package name)."""
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def write(root: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root
