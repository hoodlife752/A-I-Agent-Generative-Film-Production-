#!/bin/bash
# SessionStart hook for Claude Code on the web: tools this repo's pipeline needs.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi
cd "${CLAUDE_PROJECT_DIR:-.}"

# Pillow: tools/blocking_map.py (blocking-map PNGs) and tools/run_scene.py.
pip install -q -r requirements.txt 2>&1 | grep -v "Running pip as the 'root' user" || true

# runpodctl (Runpod's infra CLI, per docs.runpod.io agent setup) — only when a key is configured.
# Non-fatal: the environment's network policy may not allow cli.runpod.net yet.
if [ -n "${RUNPOD_API_KEY:-}" ] && ! command -v runpodctl >/dev/null 2>&1; then
  if curl -fsSL -m 60 https://cli.runpod.net | bash >/dev/null 2>&1; then
    echo "runpodctl installed: $(runpodctl version 2>/dev/null || echo ok)"
  else
    echo "runpodctl install skipped: cli.runpod.net not reachable (allow it in the environment's network settings)" >&2
  fi
fi
exit 0
