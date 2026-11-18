#!/bin/bash
# SessionStart hook: resume a benchmark round that a machine restart interrupted. Does nothing when no round is in progress.
# Logic and tests: benchmark/runner/round_resume.py. Remote (cloud) sessions only.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

# No round in progress: nothing to do, and nothing is started.
[ -f benchmark/results/.round.json ] || exit 0

# The script starts the resume detached and returns at once; a failure here must not block the session.
python3 benchmark/runner/round_resume.py || true
