#!/usr/bin/env bash
# Final project: not built yet.
#
# When it is built, this comment block says: what the script runs, the most it can cost (the caps
# in .env.example), and how long it takes, measured three times on a dated run.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "x the final project is not built yet: build final-project/ first" >&2
exit 1
