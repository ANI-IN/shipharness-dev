"""Load a module of platform/scripts/guide/ by name (the folder is scripts, not a package)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

from shipharness.layout import find_repo_root

GUIDE = find_repo_root(Path(__file__)) / "platform" / "scripts" / "guide"


def load(name: str) -> ModuleType:
    if str(GUIDE) not in sys.path:
        sys.path.insert(0, str(GUIDE))  # the scripts import guidelib by name
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, GUIDE / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
