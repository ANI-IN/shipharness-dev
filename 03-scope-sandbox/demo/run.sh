#!/usr/bin/env bash
# Section 3 demo: a live A/B on F4 (stop lost updates on issues). The bare arm and the harness arm
# (instructions, state, and scope layers) get the same ticket; the referee counts the files each arm
# changed outside the ticket's allowed paths.
#
# Usage, from anywhere inside the repository:
#   ./03-scope-sandbox/demo/run.sh                  # class run (needs SHIPHARNESS_CLASS_DATE in .env)
#   PURPOSE=pilot ./03-scope-sandbox/demo/run.sh    # practice run outside class
#
# What it does: checks that both API keys are set, that Docker answers, and that a class run has its
# class date; then runs `make demo-3 FEATURE=F4`. Every run is live: two real agent runs and two real
# reviews. There is no recorded or scripted fallback in this script.
#
# Cost: at most $0.48, two arms at the per-arm cap ($0.20 each) plus two reviews at the per-review cap
# ($0.04 each); the caps are set in platform/src/shipharness/config/settings.py and .env.example. The
# measured run in docs/evidence.md cost $0.0487.
# Time: in the measured run the bare arm's primary verdict came 5 min 15 s after the run started and
# the harness arm's full verdict 11 min 18 s after; the command finished 11 min 41 s after launch
# (docs/evidence.md, "The captured demo-3 A/B").
#
# Start the console first, in another terminal: `make console`, then open http://127.0.0.1:8765/
set -euo pipefail

# The repository root is two folders up from this script.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PURPOSE="${PURPOSE:-class}"
fail() { echo "x $1" >&2; exit 2; }

# 1. Keys. Read .env only to see whether each key has a value; never print a value.
[ -f .env ] || fail "no .env in $ROOT: run 'make setup', then add your keys (setup/README.md)"
for key in OPENAI_API_KEY LANGSMITH_API_KEY; do
  if ! grep -Eq "^${key}=.+" .env && [ -z "${!key:-}" ]; then
    fail "$key is not set: add it to .env, then run 'make doctor'"
  fi
done
echo "+ keys present (make doctor checks that they are accepted)"

# 2. Docker. Each arm and the referee run in a container.
command -v docker >/dev/null 2>&1 || fail "docker not found: install Docker (setup/README.md)"
docker info >/dev/null 2>&1 || fail "Docker is not running: start it (Ubuntu: sudo systemctl start docker)"
echo "+ Docker is running"

# 3. Class date or purpose. A class run is traced to the LangSmith project of the class day.
if [ "$PURPOSE" = "class" ]; then
  # The environment wins over .env; quotes around the value in .env are removed.
  CLASS_DATE="${SHIPHARNESS_CLASS_DATE:-$(grep -E '^SHIPHARNESS_CLASS_DATE=' .env | tail -n 1 | cut -d= -f2- | tr -d "\"' " || true)}"
  if [ -z "$CLASS_DATE" ]; then
    fail "SHIPHARNESS_CLASS_DATE is not set: add the class day (YYYY-MM-DD) to .env, or run with PURPOSE=pilot"
  fi
  TODAY="$(date +%Y-%m-%d)"
  if [ "$CLASS_DATE" != "$TODAY" ]; then
    echo "! SHIPHARNESS_CLASS_DATE is $CLASS_DATE but today is $TODAY."
    echo "  The run will be traced to the project of $CLASS_DATE. Outside class, use PURPOSE=pilot."
  fi
  echo "+ class run for $CLASS_DATE"
else
  echo "+ purpose: $PURPOSE"
fi

# 4. The live A/B: both arms on F4, then the referee and the review for each arm.
echo "Launching make demo-3 FEATURE=F4 (at most \$0.48 at the caps). Watch the console: press 1, then 3, 5, 2, 4."
exec make demo-3 FEATURE=F4 PURPOSE="$PURPOSE"
