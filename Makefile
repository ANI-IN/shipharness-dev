# shipharness Makefile. Every target is a thin wrapper over `uv run ...`, so the same commands work
# without make (see README "Commands"). On Windows, run make inside WSL2.

SHELL := /bin/sh
UV ?= uv
RUNTIME ?= docker
PORT ?= 8000
CONSOLE_PORT ?= 8765
# demo-N and final: LAYERS=-<layer> removes one layer from the section's stack.
LAYERS ?=
LAYERS_OPT = $(if $(LAYERS),--layers=$(LAYERS))
# demo-N: SESSION_BUDGET=12,38 overrides the task's session turn budget (pre-registered levers).
SESSION_BUDGET ?=
SESSION_BUDGET_OPT = $(if $(SESSION_BUDGET),--session-budget=$(SESSION_BUDGET))
# final: comma-separated feature ids picked by the class poll, e.g. FEATURES=F5,F6.
FEATURES ?= F5,F6
# swap-N: the A/B (or one of its run ids) to swap-test; default: the section's latest. replay: the A/B or run id to replay.
AB ?= latest
# demo-N, swap-N, final: PURPOSE picks the LangSmith project. class needs
# SHIPHARNESS_CLASS_DATE (the class day) in .env; PURPOSE=pilot traces to shipharness-pilot instead.
PURPOSE ?= class
RUN ?=

.PHONY: help setup images doctor up console datasets lint format lint-prose anchors test test-live \
	test-docker demo-1 demo-2 demo-3 demo-4 swap-1 swap-2 swap-3 swap-4 final replay experiments \
	report pilot check-assignment-1 check-assignment-2 check-assignment-3 check-assignment-4 \
	grade-assignment-1 grade-assignment-2 grade-assignment-3 grade-assignment-4 slides

help:
	@echo "setup doctor up console datasets lint format lint-prose test test-all test-live test-docker"
	@echo "demo-N [LAYERS=-<layer>]  swap-N [AB=<id>]  final [FEATURES=F5,F6]  replay RUN=<id>"
	@echo "experiments report pilot (later milestones)"

setup:
	$(UV) sync --frozen
	@if command -v $(RUNTIME) >/dev/null 2>&1; then $(MAKE) images; \
	else echo "! $(RUNTIME) not found: images not built; sandboxed runs need a container runtime"; fi
	@if [ ! -f .env ]; then cp .env.example .env && echo "+ created .env: fill in the two API keys"; fi

images:
	$(RUNTIME) build -f sandbox/Dockerfile --target agent -t shipharness-agent:1 .
	$(RUNTIME) build -f sandbox/Dockerfile --target referee -t shipharness-referee:1 .

doctor:
	$(UV) run shipharness doctor

up:
	$(UV) run shipharness up --port $(PORT)

console:
	$(UV) run shipharness console --port $(CONSOLE_PORT)

datasets:
	$(UV) run shipharness datasets upload

lint:
	$(UV) run ruff check .
	$(UV) run ruff format --check .
	cd teamtrack && $(UV) run lint-imports --config .importlinter
	$(UV) run python scripts/anchors.py check
	$(UV) run shipharness skills validate skills

format:
	$(UV) run ruff check --fix .
	$(UV) run ruff format .

lint-prose:
	$(UV) run python scripts/lint_prose.py
	@if command -v vale >/dev/null 2>&1; then vale --minAlertLevel=error README.md DESIGN.md RESEARCH.md; fi

anchors:
	$(UV) run python scripts/anchors.py list

# Fast suite: pyproject addopts deselects slow, live, and docker tests.
test:
	$(UV) run pytest

# Everything that needs no keys and no container runtime, including slow validations.
test-all:
	$(UV) run pytest -n auto -m "not live and not docker"

test-live:
	$(UV) run pytest -m live tests/live

test-docker:
	$(UV) run pytest -m docker tests/unit/test_sandbox_docker.py

# Section demos: section N's canonical task is feature FN, canonical variant.
demo-1:
	$(UV) run shipharness ab --section demo-1 --feature F1 $(LAYERS_OPT) $(SESSION_BUDGET_OPT) --purpose $(PURPOSE)

demo-2:
	$(UV) run shipharness ab --section demo-2 --feature F2 $(LAYERS_OPT) $(SESSION_BUDGET_OPT) --purpose $(PURPOSE)

demo-3:
	$(UV) run shipharness ab --section demo-3 --feature F3 $(LAYERS_OPT) $(SESSION_BUDGET_OPT) --purpose $(PURPOSE)

demo-4:
	$(UV) run shipharness ab --section demo-4 --feature F4 $(LAYERS_OPT) $(SESSION_BUDGET_OPT) --purpose $(PURPOSE)

# Swap test on the section's most recent A/B (ab.json records the section); AB=<ab or run id>
# picks another one.
swap-1:
	$(UV) run shipharness ab --swap $(AB) --section demo-1 --purpose $(PURPOSE)

swap-2:
	$(UV) run shipharness ab --swap $(AB) --section demo-2 --purpose $(PURPOSE)

swap-3:
	$(UV) run shipharness ab --swap $(AB) --section demo-3 --purpose $(PURPOSE)

swap-4:
	$(UV) run shipharness ab --swap $(AB) --section demo-4 --purpose $(PURPOSE)

# One A/B per feature; every feature runs, and the exit code is the last non-zero one.
final:
	rc=0; for f in $$(echo "$(FEATURES)" | tr ',' ' '); do \
	  $(UV) run shipharness ab --section final --feature $$f $(LAYERS_OPT) --purpose $(PURPOSE) || rc=$$?; \
	done; exit $$rc

replay:
	@if [ -z "$(RUN)" ]; then echo "! replay needs RUN=<ab or run id>"; exit 2; fi
	$(UV) run shipharness replay $(RUN) --purpose $(PURPOSE)

experiments report pilot:
	@echo "! $@ is available after milestones M6 and M8"; exit 2

# check-assignment-N: offline self-check of your work (A1_WORK, A2_IMPL, A3_IMPL, A4_IMPL pick a folder).
check-assignment-1:
	$(UV) run python submodules/01-instructions/assignment/check.py $(if $(A1_WORK),--work $(A1_WORK))

check-assignment-2:
	$(UV) run python submodules/02-state-lifecycle/assignment/check.py $(if $(A2_IMPL),--impl $(A2_IMPL))

check-assignment-3:
	$(UV) run python submodules/03-scope-sandbox/assignment/check.py $(if $(A3_IMPL),--impl $(A3_IMPL))

check-assignment-4:
	$(UV) run python submodules/04-verification/assignment/check.py $(if $(A4_IMPL),--impl $(A4_IMPL))

# grade-assignment-N SUBMISSION=<folder or git URL>: instructor only (graders are private).
grade-assignment-1 grade-assignment-2 grade-assignment-3 grade-assignment-4:
	@if [ -z "$(SUBMISSION)" ]; then echo "! $@ needs SUBMISSION=<folder or git URL>"; exit 2; fi
	$(UV) run python scripts/grade_assignment.py $(subst grade-assignment-,,$@) "$(SUBMISSION)"

slides:
	@echo "! slides are built in milestone M10"; exit 2
