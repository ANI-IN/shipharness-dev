"""The live variant's wrapper puts the learner's layer in place of the course state layer (no model
calls: only the registration is tested)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ASSIGNMENT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ASSIGNMENT))

from shipharness.harness.base import Harness, register_layer  # noqa: E402
from shipharness.harness.state.layer import StateLayer  # noqa: E402

spec = importlib.util.spec_from_file_location("a2_run_live", ASSIGNMENT / "live" / "run_live.py")
assert spec is not None and spec.loader is not None
run_live = importlib.util.module_from_spec(spec)
sys.modules["a2_run_live"] = run_live
spec.loader.exec_module(run_live)


@pytest.fixture
def restore_registry():
    yield
    register_layer(StateLayer)


def test_install_registers_the_learner_layer_as_state(restore_registry: None) -> None:
    layer = run_live.install(ASSIGNMENT / "starter")
    harness = Harness.from_names(frozenset({"state"}), feature_description="x", feature_steps=[])
    assert type(harness.layers[0]) is layer
    assert layer.__name__ == "ResumableStateLayer"


def test_a_command_is_required(restore_registry: None) -> None:
    with pytest.raises(SystemExit):
        run_live.main(["--impl", str(ASSIGNMENT / "starter")])
