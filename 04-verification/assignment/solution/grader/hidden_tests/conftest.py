"""Hidden A4 grader tests: run against the implementation in `A4_IMPL` (default: the starter).

Kept in solution/ and never shipped in the starter. They share the visible tests' support module.
"""

from __future__ import annotations

import sys
from pathlib import Path

VISIBLE = Path(__file__).resolve().parents[3] / "visible_tests"
sys.path.insert(0, str(VISIBLE))

from a4_support import (  # noqa: E402, F401
    impl,
    impl_path,
    pytest_collection_modifyitems,
    pytest_configure,
    pytest_runtest_logreport,
    pytest_sessionfinish,
)
