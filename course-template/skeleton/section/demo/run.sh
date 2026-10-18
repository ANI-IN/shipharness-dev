#!/usr/bin/env bash
# Section {{N}} demo: {{SECTION_NAME}}. Not built yet.
#
# When it is built, this comment block says: what the script runs (the same make target the
# demo README shows), the most it can cost (the caps in .env.example), and how long it takes,
# measured three times on a dated run (with a link to the evidence page).
set -euo pipefail

# The repository root is two folders up from this script, so it works from any folder.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "x Section {{N}} demo is not built yet: build {{SECTION_DIR}}/demo/ first" >&2
exit 1
