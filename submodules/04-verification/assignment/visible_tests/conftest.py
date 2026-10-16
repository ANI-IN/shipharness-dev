"""Visible A4 tests: run against the implementation in `A4_IMPL` (default: the starter)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from a4_support import impl, impl_path, pytest_configure  # noqa: E402, F401
