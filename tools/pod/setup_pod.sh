#!/usr/bin/env bash
# One-time (and re-runnable) ComfyUI setup on a RunPod GPU pod.
#
# PRESETS picks what gets installed (default "h3 wan22"):
#   h3     MiniMax H3 (Ref2VA reference-to-video + FL2VA first/last frame, native audio)
#          + Muse Minimax Director. MiniMax H3 Community License: local use is NOT permitted
#          in the US, EU, UK or South Korea. The pod's datacenter must be outside them too.
#   wan22  Wan 2.2 14B image-to-video + first/last frame (start/stop frames)
#   ltx25  LTX-2.5 + LTX 2.5 Director (32 GB+ VRAM recommended)
#
# Everything lives on the network volume at /workspace, so a pod stop/start keeps it all:
#   /workspace/venv       Python environment
#   /workspace/ComfyUI    ComfyUI + custom nodes
#   /workspace/models     model weights, one folder per preset (every loader sees them all)
#
# Usage (in the pod's web terminal, from a checkout of this repo):
#   export HF_TOKEN=hf_...          # needed for gated model repos
#   export PRESETS="h3 wan22"       # optional; this is the default
#   bash tools/pod/setup_pod.sh
#
# Re-running is safe: existing installs and downloads are skipped.
set -euo pipefail

WARN=0
PRESETS=${PRESETS:-"h3 wan22"}
has() { [[ " $PRESETS " == *" $1 "* ]]; }
WORK=${WORK:-/workspace}
HERE="$(cd "$(dirname "$0")" && pwd)"
COMFY="$WORK/ComfyUI"
VENV="$WORK/venv"

say() { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }

say "GPU and disk"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
VRAM_MB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
CC=$(nvidia-smi --query-gpu=compute_cap --format=csv,noheader | head -1 | tr -d .)
RAM_GB=$(awk '/MemTotal/ {printf "%d", $2/1024/1024}' /proc/meminfo)
echo "Presets: $PRESETS · compute capability ${CC} · system RAM ${RAM_GB} GB"
if has ltx25 && [ "$VRAM_MB" -lt 30000 ]; then
  echo "WARNING: ${VRAM_MB} MB VRAM. LTX-2.5's requirements ask for 32 GB+." >&2
fi
if has h3 && [ "$RAM_GB" -lt 48 ]; then
  echo "WARNING: ${RAM_GB} GB system RAM. H3 reference mode measured 43 GB+ of RAM; pick a pod with 64 GB." >&2
fi
if has h3; then
  echo "REMINDER: MiniMax H3's license excludes local use in the US, EU, UK and South Korea (this pod's datacenter included)."
fi
df -h "$WORK" | tail -1

say "System packages"
if ! command -v ffmpeg >/dev/null || ! command -v git >/dev/null; then
  apt-get update -qq && apt-get install -y -qq git ffmpeg >/dev/null
fi

say "Python environment ($VENV)"
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"
pip install -q --upgrade pip wheel

say "ComfyUI"
if [ ! -d "$COMFY/.git" ]; then
  git clone -q https://github.com/comfyanonymous/ComfyUI "$COMFY"
else
  git -C "$COMFY" pull -q --ff-only || echo "(ComfyUI has local changes; not updated)"
fi
if ! python -c "import torch, sys; sys.exit(0 if torch.cuda.is_available() else 1)" 2>/dev/null; then
  pip install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
fi
pip install -q -r "$COMFY/requirements.txt"
pip install -q "huggingface_hub[cli]" hf_transfer

say "Custom nodes"
add_node() {  # add_node <git url> <folder>
  local dir="$COMFY/custom_nodes/$2"
  if [ ! -d "$dir/.git" ]; then git clone -q "$1" "$dir"; else git -C "$dir" pull -q --ff-only || true; fi
  if [ -f "$dir/requirements.txt" ]; then pip install -q -r "$dir/requirements.txt"; fi
}
add_node https://github.com/kijai/ComfyUI-KJNodes ComfyUI-KJNodes
add_node https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite ComfyUI-VideoHelperSuite
add_node https://github.com/ltdrdata/ComfyUI-Manager comfyui-manager
if has h3; then
  # H3 itself is in ComfyUI core; these add the Director timeline, chunk continuity and the unified loader.
  add_node https://github.com/muse-collective-26/MiniMaxH3-Director-V1.2 MiniMaxH3-Director
  add_node https://github.com/seitanism/ComfyUI-H3-Motion-Context-MultiRef ComfyUI-H3-Motion-Context-MultiRef
  add_node https://github.com/muse-collective-26/Muse-MiniMax-H3-Unified-Loader Muse-MiniMax-H3-Unified-Loader
  pip install -q av
fi
if has ltx25; then
  add_node https://github.com/Lightricks/ComfyUI-LTXVideo ComfyUI-LTXVideo
  add_node https://github.com/CGlide/LTX-2.5-Director LTX-2.5-Director
  # The 2.5 Director must not run alongside the 2.3 pack (its README says so).
  if [ -d "$COMFY/custom_nodes/WhatDreamsCost-ComfyUI" ]; then
    mv "$COMFY/custom_nodes/WhatDreamsCost-ComfyUI" "$COMFY/custom_nodes/WhatDreamsCost-ComfyUI.disabled"
    echo "Disabled the LTX 2.3 Director pack (conflicts with 2.5)."
  fi
fi

say "Model folders → every ComfyUI loader"
: > "$COMFY/extra_model_paths.yaml"
for name in $PRESETS; do
  mkdir -p "$WORK/models/$name"
  cat >> "$COMFY/extra_model_paths.yaml" <<YAML
$name:
  base_path: $WORK/models/$name
  checkpoints: .
  diffusion_models: .
  unet: .
  text_encoders: .
  clip: .
  vae: .
  loras: .
  latent_upscale_models: .
  upscale_models: .
YAML
done

export HF_HUB_ENABLE_HF_TRANSFER=1
if has h3; then
  # int8 fits a 24 GB card fully; the nvfp4 text encoder needs a Blackwell GPU (compute capability 10+).
  ENC=int4; [ "${CC:-0}" -ge 100 ] && ENC=nvfp4
  say "MiniMax H3 weights (${H3_PRECISION:-int8}, encoder $ENC)"
  python "$HERE/fetch_models.py" --preset h3 --dest "$WORK/models/h3" --precision "${H3_PRECISION:-int8}" --encoder "$ENC" || WARN=1
fi
if has wan22; then
  say "Wan 2.2 weights (fp8)"
  python "$HERE/fetch_models.py" --preset wan22 --dest "$WORK/models/wan22" --precision fp8 || WARN=1
fi
if has ltx25; then
  say "LTX-2.5 weights (${LTX_PRECISION:-fp8})"
  python "$HERE/fetch_models.py" --preset ltx25 --dest "$WORK/models/ltx25" --precision "${LTX_PRECISION:-fp8}" || WARN=1
fi

say "Done"
if [ "$WARN" = 1 ]; then
  echo "Some model files weren't matched automatically. Check the file lists printed above and re-run fetch_models.py with --extra <filename>." >&2
fi
df -h "$WORK" | tail -1
echo "Start ComfyUI:  bash $HERE/start_comfyui.sh"
echo "Then open it:   RunPod → your pod → Connect → HTTP port 8188"
