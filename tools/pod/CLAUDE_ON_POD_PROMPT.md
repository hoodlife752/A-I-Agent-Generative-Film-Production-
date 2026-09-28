# Prompt for Claude Code running on the RunPod pod

Paste everything between the lines into `claude` after starting it in `/workspace/film`.

---

You're running on a RunPod GPU pod. This repo (`/workspace/film`, branch
`claude/dances-with-feddie-scene-eeqbfl`) is the AI pre-production pipeline for the feature
film *Dances With Feddie*. Your job: set up ComfyUI with MiniMax H3 and Wan 2.2 on this pod,
then render scene 2 (Dances nodding on the Salinas Confucius Church steps) as a test.

Read first: `README.md`, `tools/pod/setup_pod.sh`, `tools/pod/fetch_models.py`,
`projects/dances-with-feddie/03_department_outputs/scene_002/` (`shots.json`, `h3_prompts.json`,
`prompts/wan/*.json`, `blocking_maps/*.png`), and the Muse Minimax Director README once it's
installed (`/workspace/ComfyUI/custom_nodes/MiniMaxH3-Director/README.md`).

1. **Check the machine**: `nvidia-smi`, system RAM, free space on `/workspace`. Tell me what you
   find before downloading anything big. MiniMax H3's license excludes local use in the US, EU, UK
   and South Korea. If this pod's datacenter is in one of those, stop and tell me.
2. **Set up**: run `bash tools/pod/setup_pod.sh` (defaults to `PRESETS="h3 wan22"`). `HF_TOKEN` is
   already exported in this shell. The model picker chooses files by pattern; if it reports
   anything "not found", read the file list it prints, pick the right files and re-run with
   `--extra` / `--repo`. Fix script bugs in the repo and commit them.
3. **Start ComfyUI** in the background (`bash tools/pod/start_comfyui.sh`), confirm it answers
   on `http://127.0.0.1:8188`, and confirm the MiniMax H3 nodes (`MiniMaxH3ReferenceToVideo`,
   `MiniMaxH3ImageToVideo`) and the Wan nodes show up in `/object_info`.
4. **Dances still**: generate 4 candidate stills of Dances for shot 2-02 (a one-frame Wan 2.2
   text-to-video run is fine; the prompt is in
   `projects/dances-with-feddie/03_department_outputs/scene_002/WAN_BUILD_LTX_EDIT_RUN.md`, step 4a).
   Save them to `.../scene_002/renders/stills/`, commit, push, and **stop and ask me to pick one**.
   Never pick for me.
5. **Render** once I've picked:
   - Wan 2.2 first/last frame makes the start/stop frames for each shot (2-02 starts on my pick;
     each later shot starts on the previous shot's last frame).
   - MiniMax H3 renders each shot from those frames (FL2VA, first/last frame) with native audio:
     Dances' broken, pained mumble-hum, fading out on 2-04. Use the `flf` prompts in
     `h3_prompts.json`.
   - Drive ComfyUI through its HTTP API (`/prompt`, `/history`, `/view`); save API-format
     workflows you build into `tools/pod/workflows/` so they're reusable.
   - Start at 768p-ish and short durations; report the time per clip.
6. **Deliver**: save clips to `.../scene_002/renders/`, commit and push them (Git LFS if they're
   over ~50 MB), and log anything that rendered wrong (tattoo drift, garbled lettering, content
   refusals, identity drift) with the exact prompt wording in `.../scene_002/renders/drift_log.md`.

Keep me posted in short lines as you go. Ask before anything that costs real money beyond this
pod or deletes data.

---
