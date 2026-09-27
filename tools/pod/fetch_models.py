#!/usr/bin/env python3
"""Download the model files ComfyUI needs, choosing them from each repo's own file list.

Presets:
  wan22  Wan 2.2 14B image/text-to-video (build pass)   Comfy-Org/Wan_2.2_ComfyUI_Repackaged
  ltx25  LTX-2.5 (edit pass: audio, extend, upscale)     Lightricks/LTX-2.5

Exact filenames aren't hard-coded (they couldn't be verified when this was written).
The script lists what the repo actually publishes, picks one file per role by
pattern, prints the plan, then downloads. --dry-run prints the plan only. If a
required role can't be matched, the repo's full weight list is printed so you can
pass --extra <filename> (or --repo <other repo>) by hand.
"""
import argparse
import re
import sys
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download

REPOS = {"wan22": "Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "ltx25": "Lightricks/LTX-2.5"}
WEIGHTS = re.compile(r"\.(safetensors|gguf)$", re.I)


def pick(files, include, exclude=(), prefer=()):
    cands = [f for f in files if WEIGHTS.search(f) and all(re.search(p, f, re.I) for p in include)
             and not any(re.search(p, f, re.I) for p in exclude)]
    for p in prefer:
        hit = [f for f in cands if re.search(p, f, re.I)]
        if hit:
            return sorted(hit, key=len)[0]
    return sorted(cands, key=len)[0] if cands else None


def wan_plan(files, precision):
    """Wan 2.2 A14B = a high-noise and a low-noise expert, for each of I2V and T2V."""
    q = r"fp8" if precision == "fp8" else r"fp16|bf16"
    return {
        "i2v high-noise": pick(files, [r"i2v", r"high", r"14b", q]),
        "i2v low-noise": pick(files, [r"i2v", r"low", r"14b", q]),
        "t2v high-noise": pick(files, [r"t2v", r"high", r"14b", q]),
        "t2v low-noise": pick(files, [r"t2v", r"low", r"14b", q]),
        "text encoder": pick(files, [r"umt5"], prefer=[r"fp8"]),
        "video VAE": pick(files, [r"wan_?2\.1_vae"]),
    }


def ltx_plan(files, precision):
    other = "bf16" if precision == "fp8" else "fp8"
    return {
        "diffusion model": pick(files, [r"ltx"], exclude=[r"vae", r"upscal", r"lora", r"gemma", r"text", other],
                                prefer=[rf"distill.*{precision}", precision, r"distill"]),
        "video VAE": pick(files, [r"vae"], exclude=[r"audio"], prefer=[r"video"]),
        "audio VAE": pick(files, [r"audio"], prefer=[r"vae"]),
        "spatial upscaler": pick(files, [r"upscal"], prefer=[r"spatial.*x2", r"spatial"]),
        "text encoder": pick(files, [r"gemma"], prefer=[precision, r"fp8", r"bf16"]),
        "text projection": pick(files, [r"proj"]),
    }


REQUIRED = {"wan22": ("i2v high-noise", "i2v low-noise", "text encoder", "video VAE"),
            "ltx25": ("diffusion model", "video VAE", "text encoder")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", choices=sorted(REPOS), required=True)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--precision", choices=["fp8", "bf16"], default="fp8")
    ap.add_argument("--repo", help="override the preset's repo")
    ap.add_argument("--extra", action="append", default=[], help="additional filename(s) from the repo to fetch")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    repo = a.repo or REPOS[a.preset]
    files = HfApi().list_repo_files(repo)
    plan = (wan_plan if a.preset == "wan22" else ltx_plan)(files, a.precision)
    for f in a.extra:
        plan[f"extra: {Path(f).name}"] = f

    print(f"{repo}: {len(files)} files. Plan ({a.preset}, {a.precision}):")
    for role, f in plan.items():
        print(f"  {role:18} {f or '— not found'}")
    missing = [r for r in REQUIRED[a.preset] if not plan.get(r)]
    if missing:
        print("\nCould not match: " + ", ".join(missing))
        print("The model card may point to a separate repo for these (e.g. the Gemma text encoder). Weights in this repo:")
        for f in files:
            if WEIGHTS.search(f):
                print("   ", f)
        print("Re-run with --extra <filename>, or --repo <other repo> --extra <filename>.")
    if a.dry_run:
        return 1 if missing else 0

    dest = Path(a.dest)
    dest.mkdir(parents=True, exist_ok=True)
    for role, f in plan.items():
        if not f:
            continue
        target = dest / Path(f).name
        if target.exists() and target.stat().st_size > 0:
            print(f"✓ {role}: {target.name} (already here)")
            continue
        print(f"↓ {role}: {f}")
        path = hf_hub_download(repo, f, local_dir=str(dest / ".hf"))
        Path(path).replace(target)
        print(f"  → {target} ({target.stat().st_size / 1e9:.1f} GB)")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
