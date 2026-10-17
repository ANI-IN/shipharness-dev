"""Hidden grader tests: A3_IMPL names the folder that holds `a3scope` (default: the starter)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUBMODULE = HERE.parents[3]  # hidden/ -> grader/ -> solution/ -> assignment/ -> the section
VISIBLE = SUBMODULE / "assignment" / "visible_tests"  # a3_checks.py: the shared case checks
IMPL = Path(os.environ.get("A3_IMPL") or SUBMODULE / "assignment" / "starter").resolve()
for folder in (VISIBLE, IMPL):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))
