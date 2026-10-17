#!/usr/bin/env bash
# init.sh for F5, written by the harness initializer step.
# A2: "an init.sh script that can run the development server", then
# "run through a basic end-to-end test before implementing a new feature".
#
#   bash init.sh          scratch database at head, then a basic end-to-end test
#   bash init.sh serve    the same, then the development server in the background
set -euo pipefail
cd "$(dirname "$0")"

# A scratch database outside the repository, so setup leaves no files to commit.
export TEAMTRACK_DATABASE_URL="sqlite:////tmp/teamtrack-dev.db"
export TEAMTRACK_SEED=true

echo "== migrations (house rule R7: exactly one head)"
python -m alembic heads
python -m alembic upgrade head

echo "== basic end-to-end test: issues, stop at the first failure (full suite: run_visible_tests)"
python -m pytest tests/visible/test_issues.py -x -q --no-header -p no:cacheprovider

if [ "${1:-}" = "serve" ]; then
  echo "== development server on http://127.0.0.1:8000 (log in /tmp/teamtrack-dev.log)"
  nohup python -m uvicorn app.main:create_app --factory --port 8000 \
    >/tmp/teamtrack-dev.log 2>&1 &
  echo "server pid $!"
fi
