"""Optional live variant: run a shipharness command with your state layer in place of the course's.

    uv run python submodules/02-state-lifecycle/assignment/live/run_live.py --impl <folder> -- \
        ab --example F2-canonical --layers instructions,state --no-reviewer

Everything after `--` is passed to the `shipharness` CLI unchanged. Your `ResumableStateLayer` is
registered under the name "state", so every harness arm that uses the state layer uses yours.
This calls OpenAI and LangSmith and costs money (README, "Optional live variant").
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSIGNMENT = HERE.parent
if str(ASSIGNMENT) not in sys.path:
    sys.path.insert(0, str(ASSIGNMENT))

from a2_scenario.report import load_layer  # noqa: E402

from shipharness.harness.base import BaseLayer, register_layer  # noqa: E402


def install(impl: Path) -> type[BaseLayer]:
    """Register the layer from `<impl>/a2_state` as "state", after the course layers."""
    importlib.import_module("shipharness.harness.layers")  # the course layers register first
    layer = load_layer(impl)
    register_layer(layer)
    return layer


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    split = args.index("--") if "--" in args else len(args)
    parser = argparse.ArgumentParser(description="Run shipharness with your A2 state layer.")
    parser.add_argument("--impl", type=Path, default=ASSIGNMENT / "starter")
    options = parser.parse_args(args[:split])
    command = args[split + 1 :]
    if not command:
        parser.error("give the shipharness command after --")
    layer = install(options.impl)
    print(f"state layer: {layer.__module__}.{layer.__qualname__} from {options.impl}")
    from shipharness.cli import app

    try:
        app(args=command, prog_name="shipharness")
    except SystemExit as exc:
        return int(exc.code or 0) if not isinstance(exc.code, str) else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
