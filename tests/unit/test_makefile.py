"""The Makefile targets are thin wrappers over real `shipharness` commands, and the default pytest
run deselects slow validations while `make test-all` keeps them.

No make binary is needed: the Makefile is parsed as text, and each `shipharness` command line is
parsed by the real CLI (click make_context), so an option the CLI does not accept fails here.
"""

from __future__ import annotations

import re
import shlex
import tomllib
from pathlib import Path

import pytest
import typer
from _pytest.mark.expression import Expression

from shipharness.cli import app

REPO = Path(__file__).resolve().parents[2]
MAKEFILE = REPO / "Makefile"
PYPROJECT = REPO / "pyproject.toml"
CONFTEST = REPO / "tests" / "conftest.py"

# Sample values substituted for make variables before the CLI parses a recipe line.
SAMPLES = {
    "$(LAYERS_OPT)": "--layers=-scope",
    "$(SESSION_BUDGET_OPT)": "--session-budget=12,38",
    "$(PURPOSE)": "pilot",
    "$(AB)": "ab-20261016-000000-abcdef",
    "$(RUN)": "r-20261016-000000-abcdef",
    "$$f": "F5",
}


def _rules() -> dict[str, list[str]]:
    """target -> recipe lines (continuations joined), for every explicit rule in the Makefile."""
    text = MAKEFILE.read_text(encoding="utf-8").replace("\\\n", " ")
    rules: dict[str, list[str]] = {}
    current: list[str] = []
    for line in text.splitlines():
        if line.startswith("\t"):
            current.append(line.strip())
            continue
        match = re.match(r"^([A-Za-z0-9_. -]+?)\s*:(?!=)", line)
        if match and not line.startswith((".PHONY", "#")):
            current = []
            for target in match.group(1).split():
                rules[target] = current
        elif line.strip() and not line.startswith("#"):
            current = []
    return rules


def _variables() -> dict[str, str]:
    out = {}
    for line in MAKEFILE.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^([A-Z_]+)\s*(\?=|:=|=)\s*(.*)$", line)
        if match:
            out[match.group(1)] = match.group(3).strip()
    return out


def _shipharness_calls(target: str) -> list[list[str]]:
    """Every `$(UV) run shipharness ...` call in a target's recipe, as argv after `shipharness`."""
    calls = []
    for line in _rules()[target]:
        for chunk in line.split(";"):
            if "$(UV) run shipharness " not in chunk:
                continue
            rest = chunk.split("$(UV) run shipharness ", 1)[1]
            rest = rest.split("||", 1)[0]
            for name, value in SAMPLES.items():
                rest = rest.replace(name, value)
            calls.append(shlex.split(rest))
    return calls


def _parse(argv: list[str]) -> tuple[str, dict]:
    """Parse argv with the real CLI without running it; return (command, params)."""
    group = typer.main.get_command(app)
    command = group.commands[argv[0]]  # type: ignore[attr-defined]
    ctx = command.make_context(argv[0], list(argv[1:]), resilient_parsing=False)
    return argv[0], ctx.params


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_demo_target_runs_the_section_canonical_task(n: int) -> None:
    calls = _shipharness_calls(f"demo-{n}")
    assert len(calls) == 1
    command, params = _parse(calls[0])
    assert command == "ab"
    assert params["section"] == f"demo-{n}"
    assert params["feature"] == f"F{n}"  # section-N's canonical task is Fn canonical (DESIGN §10.1)
    assert params["variant"] == "canonical"
    assert params["layers"] == "-scope"  # LAYERS=-<layer> reaches the CLI (DESIGN §6.6)


def test_layers_option_is_empty_unless_layers_is_set() -> None:
    assert _variables()["LAYERS_OPT"] == "$(if $(LAYERS),--layers=$(LAYERS))"


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_swap_target_runs_the_swap_test_on_ab(n: int) -> None:
    calls = _shipharness_calls(f"swap-{n}")
    assert len(calls) == 1
    command, params = _parse(calls[0])
    assert command == "ab"
    assert params["swap"] == SAMPLES["$(AB)"]
    assert params["section"] == f"demo-{n}"
    assert _variables()["AB"] == "latest"  # make swap-N needs no id; AB=<id> still overrides


def test_final_runs_every_feature_in_features() -> None:
    # Two poll-chosen features by default (brief; owner 2026-10-17); the poll offers F5-F7.
    assert _variables()["FEATURES"] == "F5,F6"
    recipe = " ".join(_rules()["final"])
    assert "$(FEATURES)" in recipe
    assert "rc=$$?" in recipe and recipe.endswith("exit $$rc")  # one failure does not stop the rest
    raw = MAKEFILE.read_text(encoding="utf-8").splitlines()
    assert not [line for line in raw if "\t" in line.lstrip("\t")]  # continuations kept as lines
    calls = _shipharness_calls("final")
    assert len(calls) == 1
    command, params = _parse(calls[0])
    assert command == "ab"
    assert params["section"] == "final"
    assert params["feature"] == "F5"
    assert params["layers"] == "-scope"


def test_replay_target_replays_run() -> None:
    calls = _shipharness_calls("replay")
    assert len(calls) == 1
    command, params = _parse(calls[0])
    assert command == "replay"
    assert params["run"] == SAMPLES["$(RUN)"]
    assert any("RUN" in line and "exit 2" in line for line in _rules()["replay"])


def test_no_milestone_stub_remains_for_wired_targets() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")
    assert "available after milestone M4" not in text
    rules = _rules()
    for target in [*(f"demo-{n}" for n in range(1, 5)), *(f"swap-{n}" for n in range(1, 5))]:
        assert not any("is available after" in line for line in rules[target]), target
    for target in ("final", "replay"):
        assert not any("is available after" in line for line in rules[target]), target


# -- fast and full suites -----------------------------------------------------------------------


def _marker_expression(args: list[str]) -> str:
    return args[args.index("-m") + 1]


def _selects(expression: str, *markers: str) -> bool:
    return Expression.compile(expression).evaluate(lambda name, **_: name in markers)


def test_default_pytest_run_deselects_slow_live_and_docker() -> None:
    options = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["tool"]["pytest"]["ini_options"]
    expression = _marker_expression(shlex.split(options["addopts"]))
    assert _selects(expression)
    for marker in ("slow", "live", "docker"):
        assert not _selects(expression, marker), marker


def test_make_test_is_the_default_run_and_test_all_adds_slow() -> None:
    rules = _rules()
    assert rules["test"] == ["$(UV) run pytest"]
    (line,) = rules["test-all"]
    assert line.startswith("$(UV) run pytest ")
    args = shlex.split(line)
    assert args[args.index("-n") + 1] == "auto"  # the full suite runs in parallel
    expression = _marker_expression(args)
    assert _selects(expression)
    assert _selects(expression, "slow")
    assert not _selects(expression, "live")
    assert not _selects(expression, "docker")


def test_conftest_slow_list_names_existing_test_files() -> None:
    from tests.conftest import SLOW_TESTS, _is_slow

    assert SLOW_TESTS
    for pattern in SLOW_TESTS:
        path, _, name = pattern.partition("::")
        assert (REPO / path).is_file(), pattern
        assert f"def {name.split('::')[-1]}(" in (REPO / path).read_text(encoding="utf-8"), pattern
        assert _is_slow(pattern) and _is_slow(f"{pattern}[x]")
    assert not _is_slow(f"{SLOW_TESTS[0]}_other")


def test_demo_targets_pass_the_purpose_and_an_optional_session_budget() -> None:
    # Owner, 2026-10-17: PURPOSE picks the LangSmith project; SESSION_BUDGET=12,38 applies the
    # pre-registered F2 lever through make.
    assert _variables()["SESSION_BUDGET_OPT"] == (
        "$(if $(SESSION_BUDGET),--session-budget=$(SESSION_BUDGET))"
    )
    for n in (1, 2, 3, 4):
        _, params = _parse(_shipharness_calls(f"demo-{n}")[0])
        assert params["purpose"] == "pilot"
        assert params["session_budget"] == "12,38"


def test_replay_target_passes_the_purpose() -> None:
    _, params = _parse(_shipharness_calls("replay")[0])
    assert params["purpose"] == "pilot"
