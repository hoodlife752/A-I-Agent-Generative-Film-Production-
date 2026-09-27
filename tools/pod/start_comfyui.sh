#!/usr/bin/env bash
# Start ComfyUI on the pod after setup_pod.sh has run (run again after every pod restart).
set -euo pipefail
WORK=${WORK:-/workspace}
# shellcheck disable=SC1091
source "$WORK/venv/bin/activate"
cd "$WORK/ComfyUI"
mkdir -p "$WORK/renders"
exec python main.py --listen 0.0.0.0 --port 8188 --output-directory "$WORK/renders" "$@"
