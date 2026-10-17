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
# SHIPHARNESS_CLASS_DATE (the class day, YYYY-MM-DD) in .env; PURPOSE=pilot traces to
# shipharness-pilot instead. doctor and warm check the class date when PURPOSE=class.
PURPOSE ?= class
# demo-N, final, show-N, warm: PROFILE=class (default) makes live class runs fast, identical for both
# arms: reasoning effort low, 2 CPUs per arm and referee container, OpenAI Fast tier for the agent
# arms (the reviewer keeps its own settings). PROFILE=standard runs the settings as loaded.
PROFILE ?= class
# demo-3's ticket: F3 by default; FEATURE=F4 runs the S3 confirmation task as a live A/B.
FEATURE ?= F3
# images, warm: the image names (the SANDBOX_IMAGE_AGENT and SANDBOX_IMAGE_REFEREE defaults).
AGENT_IMAGE ?= shipharness-agent:1
REFEREE_IMAGE ?= shipharness-referee:1
RUN ?=

.PHONY: help setup images doctor up console datasets lint format lint-prose check-style anchors test \
	test-live \
	test-docker demo-1 demo-2 demo-3 demo-4 show-1 show-2 show-3 show-4 swap-1 swap-2 swap-3 swap-4 \
	final replay warm experiments \
	report pilot check-assignment-1 check-assignment-2 check-assignment-3 check-assignment-4 \
	grade-assignment-1 grade-assignment-2 grade-assignment-3 grade-assignment-4 slides

help:
	@echo "setup doctor up console datasets lint format lint-prose check-style test test-all test-live test-docker"
	@echo "demo-N [LAYERS=-<layer>]  show-N  swap-N [AB=<id>]  final [FEATURES=F5,F6]  replay RUN=<id>"
	@echo "warm (before class: images, containers, referee and gate baselines; no model calls)"
	@echo "experiments and reports: uv run shipharness experiments --help; uv run shipharness report --help"

setup:
	$(UV) sync --frozen
	@if command -v $(RUNTIME) >/dev/null 2>&1; then $(MAKE) images; \
	else echo "! $(RUNTIME) not found: images not built; sandboxed runs need a container runtime"; fi
	@if [ ! -f .env ]; then cp .env.example .env && echo "+ created .env: fill in the two API keys"; fi

images:
	$(RUNTIME) build -f platform/sandbox/Dockerfile --target agent -t $(AGENT_IMAGE) .
	$(RUNTIME) build -f platform/sandbox/Dockerfile --target referee -t $(REFEREE_IMAGE) .

doctor:
	$(UV) run shipharness doctor --purpose $(PURPOSE)

up:
	$(UV) run shipharness up --port $(PORT)

console:
	$(UV) run shipharness console --port $(CONSOLE_PORT)

datasets:
	$(UV) run shipharness datasets upload

lint:
	$(UV) run ruff check .
	$(UV) run ruff format --check .
	cd platform/teamtrack && $(UV) run lint-imports --config .importlinter
	$(UV) run python platform/scripts/anchors.py check
	$(UV) run shipharness skills validate use-in-your-repo/skills

format:
	$(UV) run ruff check --fix .
	$(UV) run ruff format .

lint-prose:
	$(UV) run python platform/scripts/lint_prose.py
	@if command -v vale >/dev/null 2>&1; then vale --minAlertLevel=error README.md $(wildcard DESIGN.md RESEARCH.md); fi  # DESIGN.md, RESEARCH.md: build repository only, not included in the public release

# check-style: the mechanical rules of docs/STYLE.md on the public course pages. Errors fail;
# CHECK_STYLE_OPTS=--strict fails on warnings too, --warn-only reports and never fails.
CHECK_STYLE_OPTS ?=
check-style:
	$(UV) run python platform/scripts/check_style.py $(CHECK_STYLE_OPTS)

anchors:
	$(UV) run python platform/scripts/anchors.py list

# Fast suite: pyproject addopts deselects slow, live, and docker tests.
test:
	$(UV) run pytest

# Everything that needs no keys and no container runtime, including slow validations.
test-all:
	$(UV) run pytest -n auto -m "not live and not docker"

test-live:
	$(UV) run pytest -m live platform/tests/live

test-docker:
	$(UV) run pytest -m docker platform/tests/unit/test_sandbox_docker.py

# Section demos: section N's canonical task is feature FN, canonical variant.
demo-1:
	$(UV) run shipharness ab --section demo-1 --feature F1 $(LAYERS_OPT) $(SESSION_BUDGET_OPT) --purpose $(PURPOSE) \
	  --profile $(PROFILE)

demo-2:
	$(UV) run shipharness ab --section demo-2 --feature F2 $(LAYERS_OPT) $(SESSION_BUDGET_OPT) --purpose $(PURPOSE) \
	  --profile $(PROFILE)

demo-3:
	$(UV) run shipharness ab --section demo-3 --feature $(FEATURE) $(LAYERS_OPT) $(SESSION_BUDGET_OPT) --purpose $(PURPOSE) \
	  --profile $(PROFILE)

demo-4:
	$(UV) run shipharness ab --section demo-4 --feature F4 $(LAYERS_OPT) $(SESSION_BUDGET_OPT) --purpose $(PURPOSE) \
	  --profile $(PROFILE)

# Harness in action: the harness arm alone on section N's canonical task, judged by the referee
# (not an A/B; its records stay out of the bare-vs-harness comparison and of swap-N).
show-1:
	$(UV) run shipharness ab --section demo-1 --feature F1 --arms harness $(LAYERS_OPT) $(SESSION_BUDGET_OPT) --purpose $(PURPOSE) \
	  --profile $(PROFILE)

show-2:
	$(UV) run shipharness ab --section demo-2 --feature F2 --arms harness $(LAYERS_OPT) $(SESSION_BUDGET_OPT) --purpose $(PURPOSE) \
	  --profile $(PROFILE)

show-3:
	$(UV) run shipharness ab --section demo-3 --feature F3 --arms harness $(LAYERS_OPT) $(SESSION_BUDGET_OPT) --purpose $(PURPOSE) \
	  --profile $(PROFILE)

show-4:
	$(UV) run shipharness ab --section demo-4 --feature F4 --arms harness $(LAYERS_OPT) $(SESSION_BUDGET_OPT) --purpose $(PURPOSE) \
	  --profile $(PROFILE)

# Constructed example: section N's layer stack on its canonical task in the real sandbox, driven by
# scripted steps (no model, no API key, $0); labelled CONSTRUCTED EXAMPLE and never counted.
.PHONY: example-1 example-2 example-3 example-4
example-1:
	$(UV) run shipharness example --section demo-1 --profile $(PROFILE)

example-2:
	$(UV) run shipharness example --section demo-2 --profile $(PROFILE)

example-3:
	$(UV) run shipharness example --section demo-3 --profile $(PROFILE)

example-4:
	$(UV) run shipharness example --section demo-4 --profile $(PROFILE)

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
	  $(UV) run shipharness ab --section final --feature $$f $(LAYERS_OPT) --purpose $(PURPOSE) \
	    --profile $(PROFILE) || rc=$$?; \
	done; exit $$rc

replay:
	@if [ -z "$(RUN)" ]; then echo "! replay needs RUN=<ab or run id>"; exit 2; fi
	$(UV) run shipharness replay $(RUN) --purpose $(PURPOSE)

# Before class, on the class host: build the images only if their source changed, page each image
# in, and cache the referee and gate baselines of the class tasks. No model calls; safe to rerun.
warm:
	$(UV) run shipharness warm --purpose $(PURPOSE) --profile $(PROFILE) --images-command "make images RUNTIME=$(RUNTIME)"

experiments report pilot:
	@echo "! make $@ is not a make target in this release; use uv run shipharness experiments --help or uv run shipharness report --help"; exit 2

# check-assignment-N: offline self-check of your work (A1_WORK, A2_IMPL, A3_IMPL, A4_IMPL pick a folder).
check-assignment-1:
	$(UV) run python section-1-instructions/assignment/check.py $(if $(A1_WORK),--work $(A1_WORK))

check-assignment-2:
	$(UV) run python section-2-state-lifecycle/assignment/check.py $(if $(A2_IMPL),--impl $(A2_IMPL))

check-assignment-3:
	$(UV) run python section-3-scope-sandbox/assignment/check.py $(if $(A3_IMPL),--impl $(A3_IMPL))

check-assignment-4:
	$(UV) run python section-4-verification/assignment/check.py $(if $(A4_IMPL),--impl $(A4_IMPL))

# grade-assignment-N SUBMISSION=<folder or git URL>: instructor only (graders are private).
grade-assignment-1 grade-assignment-2 grade-assignment-3 grade-assignment-4:
	@if [ -z "$(SUBMISSION)" ]; then echo "! $@ needs SUBMISSION=<folder or git URL>"; exit 2; fi
	$(UV) run python platform/scripts/grade_assignment.py $(subst grade-assignment-,,$@) "$(SUBMISSION)"

# slides: slides/deck.md -> slides/dist/deck.{html,pdf,pptx} (platform/scripts/build_slides.py); lists open PENDING items and empty
# result slots. SLIDES_OPTS=--strict fails while any remain (release check); --check validates only.
SLIDES_OPTS ?=
slides:
	$(UV) run python platform/scripts/build_slides.py $(SLIDES_OPTS)
