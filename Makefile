# shipharness Makefile. Every target is a thin wrapper over `uv run ...`, so the same commands work
# without make (see README "Commands"). On Windows, run make inside WSL2.

SHELL := /bin/sh
UV ?= uv
RUNTIME ?= docker
PORT ?= 8000
CONSOLE_PORT ?= 8765

.PHONY: help setup images doctor up console datasets lint format lint-prose anchors test test-live \
	test-docker demo-1 demo-2 demo-3 demo-4 swap-1 swap-2 swap-3 swap-4 final replay experiments \
	report pilot check-assignment-1 check-assignment-2 check-assignment-3 check-assignment-4 \
	grade-assignment-1 grade-assignment-2 grade-assignment-3 grade-assignment-4 slides

help:
	@echo "setup doctor up console datasets lint format lint-prose test test-live test-docker"
	@echo "demo-N swap-N final replay experiments report pilot (later milestones)"

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

format:
	$(UV) run ruff check --fix .
	$(UV) run ruff format .

lint-prose:
	$(UV) run python scripts/lint_prose.py
	@if command -v vale >/dev/null 2>&1; then vale --minAlertLevel=error README.md DESIGN.md RESEARCH.md; fi

anchors:
	$(UV) run python scripts/anchors.py list

test:
	$(UV) run pytest

test-live:
	$(UV) run pytest -m live tests/live

test-docker:
	$(UV) run pytest -m docker tests/unit/test_sandbox_docker.py

# Targets delivered in later milestones (M4-M10) report when they become available.
demo-1 demo-2 demo-3 demo-4 swap-1 swap-2 swap-3 swap-4 final replay:
	@echo "! $@ is available after milestone M4 (A/B runner and console screens)"; exit 2

experiments report pilot:
	@echo "! $@ is available after milestones M6 and M8"; exit 2

check-assignment-1 check-assignment-2 check-assignment-3 check-assignment-4 \
grade-assignment-1 grade-assignment-2 grade-assignment-3 grade-assignment-4:
	@echo "! $@ is available after milestone M7"; exit 2

slides:
	@echo "! slides are built in milestone M10"; exit 2
