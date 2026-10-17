#!/usr/bin/env bash
# Final project: one live A/B. The bare arm and the harness arm with all four layers build the same
# feature, then the referee scores both.
#
# Usage, from anywhere inside the repository:
#   ./final-project/run.sh                               # class run, F5 (needs SHIPHARNESS_CLASS_DATE)
#   PURPOSE=pilot ./final-project/run.sh                 # practice run outside class
#   FEATURES=F6 PURPOSE=pilot ./final-project/run.sh     # another final feature: F5, F6, or F7
#
# What it does: checks that both API keys are set, that a class run has its class date, that Docker
# answers, and whether the console is up; then runs `make final FEATURES=<feature>`. Every run is
# live: two real agent runs and two real reviews. There is no recorded or scripted fallback here.
#
# Cost: at most $0.58 per feature, two arms at MAX_FINAL_RUN_COST_USD ($0.25) plus two reviews at
# MAX_REVIEW_COST_USD ($0.04); the caps are set in .env.example and
# platform/src/shipharness/config/settings.py. The measured run in docs/evidence/final.md cost less.
# Time: the measured run's timings are in docs/evidence/final.md ("The captured make final run").
#
# Start the console first, in another terminal: `make console`, then open http://127.0.0.1:8765/
set -euo pipefail

# The repository root is one folder up from this script.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PURPOSE="${PURPOSE:-class}"
FEATURES="${FEATURES:-F5}"
CONSOLE_PORT="${CONSOLE_PORT:-8765}"
fail() { echo "x $1" >&2; exit 2; }

# 1. The feature. Only the three final features run here; F1 to F4 belong to the section demos.
for feature in $(echo "$FEATURES" | tr ',' ' '); do
  case "$feature" in
    F5|F6|F7) ;;
    *) fail "FEATURES=$FEATURES: the final project runs F5, F6, or F7 (for example FEATURES=F6)" ;;
  esac
done
echo "+ features: $FEATURES"

# 2. Keys. Look in the environment, then in .env, only to see whether each key has a value; never
# print a value.
for key in OPENAI_API_KEY LANGSMITH_API_KEY; do
  if [ -z "${!key:-}" ] && ! { [ -f .env ] && grep -Eq "^${key}=.+" .env; }; then
    fail "$key is not set: add it to .env (make setup copies .env.example), then run 'make doctor'"
  fi
done
echo "+ keys present (make doctor checks that they are accepted)"

# 3. Class date or purpose. A class run is traced to the LangSmith project of the class day.
if [ "$PURPOSE" = "class" ]; then
  # The environment wins over .env; quotes around the value in .env are removed.
  CLASS_DATE="${SHIPHARNESS_CLASS_DATE:-$( { grep -E '^SHIPHARNESS_CLASS_DATE=' .env 2>/dev/null || true; } | tail -n 1 | cut -d= -f2- | tr -d "\"' ")}"
  if [ -z "$CLASS_DATE" ]; then
    fail "SHIPHARNESS_CLASS_DATE is not set: add the class day (YYYY-MM-DD) to .env, or run with PURPOSE=pilot"
  fi
  echo "+ class run for $CLASS_DATE"
else
  echo "+ purpose: $PURPOSE"
fi

# 4. Docker. Each arm and the referee run in their own container.
command -v docker >/dev/null 2>&1 || fail "docker not found: install Docker (setup/README.md)"
docker info >/dev/null 2>&1 || fail "Docker is not running: start it (Ubuntu: sudo systemctl start docker)"
echo "+ Docker is running"

# 5. The console. The run works without it, but the screens are where you watch it.
if curl -fs -o /dev/null "http://127.0.0.1:${CONSOLE_PORT}/" 2>/dev/null; then
  echo "+ console is up at http://127.0.0.1:${CONSOLE_PORT}/"
else
  echo "! console not reachable at http://127.0.0.1:${CONSOLE_PORT}/: start it in another terminal with 'make console'"
fi

# 6. The live run: both arms, then the referee and the review for each.
echo "Launching make final FEATURES=$FEATURES PURPOSE=$PURPOSE (at most \$0.58 per feature at the caps)."
exec make final FEATURES="$FEATURES" PURPOSE="$PURPOSE"
