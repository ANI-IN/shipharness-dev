"""The live path builds harness layers from the default registry in a fresh interpreter (the CLI
never imports the layer modules itself). Tests that pass their own registry cannot catch this."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def test_every_layer_resolves_in_a_fresh_interpreter() -> None:
    code = (
        "from shipharness.harness.base import Harness\n"
        "h = Harness.from_names(frozenset({'instructions', 'state', 'scope', 'verify'}))\n"
        "print(sorted(h.names))\n"
    )
    done = subprocess.run(
        [sys.executable, "-c", code], cwd=REPO, capture_output=True, text=True, check=False
    )
    assert done.returncode == 0, done.stderr[-800:]
    assert "instructions" in done.stdout and "verify" in done.stdout
