#!/usr/bin/env python3
"""Render a shot with MiniMax H3 through MiniMax's hosted API (V2 video generation).

Default model: MiniMax-H3-Max (fast variant, 480P/768P, 5–15s). --model MiniMax-H3 for 2K.

Three modes, matching the API's input combinations (they can't be mixed in one request):

  t2v   text only: nothing else needed. Fastest way to see what H3 does with a shot.
  flf   first/last frame: pin the shot's opening and closing images, e.g. Wan-made
        frames or the Image Consistency expression anchors.
  ref   reference-to-video: up to 9 reference images (character stills, location,
        the shot's blocking map) plus optional reference audio (≤3 clips).

Prompts come from <scene dir>/h3_prompts.json ({"<shot>": {"t2v"|"flf"|"ref": text}}).
Local images/audio are sent inline as data URIs (request body ≤ 64 MB).

Usage:
    export MINIMAX_API_KEY=...
    python3 tools/minimax_h3.py projects/dances-with-feddie 002 2-02 --mode t2v
    python3 tools/minimax_h3.py projects/dances-with-feddie 002 2-03 --mode flf \\
        --first frames/2-03_first.png --last frames/2-03_last.png
    python3 tools/minimax_h3.py projects/dances-with-feddie 002 2-02 --mode ref \\
        --ref refs/dances.png --map
    ... add --dry-run to print the request without sending it.

Output: <scene dir>/renders/<shot>_<mode>_<task id>.mp4 plus a .json log of the
request (media elided) and the final task status. Refusals (HTTP 422, sensitive
content) are logged too, since those feed the drift log.
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.minimax.io"
IMAGE_MAX = 30 * 1024 * 1024
BODY_MAX = 64 * 1024 * 1024
MODELS = {"MiniMax-H3": {"res": ("768P", "2K"), "dur": (4, 15)},
          "MiniMax-H3-Max": {"res": ("480P", "768P"), "dur": (5, 15)}}


def data_uri(path, kind):
    p = Path(path)
    if not p.is_file():
        sys.exit(f"missing file: {p}")
    mime = mimetypes.guess_type(p.name)[0] or ("image/png" if kind == "image" else "audio/mpeg")
    if kind == "image" and p.stat().st_size > IMAGE_MAX:
        sys.exit(f"{p} is over the 30 MB image limit")
    return f"data:{mime.lower()};base64," + base64.b64encode(p.read_bytes()).decode()


def item(kind, path, role):
    key = {"image": "image_url", "audio": "audio_url", "video": "video_url"}[kind]
    return {"type": key, key: {"url": data_uri(path, kind)}, "role": role, "_file": str(path)}


def build(a, scene_dir, shot):
    prompts = json.loads((scene_dir / "h3_prompts.json").read_text())
    text = prompts.get(shot["id"], {}).get(a.mode)
    if not text:
        sys.exit(f"no '{a.mode}' prompt for shot {shot['id']} in {scene_dir / 'h3_prompts.json'}")
    content = [{"type": "text", "text": text}]
    if a.mode == "flf":
        if not a.first:
            sys.exit("flf mode needs --first (and optionally --last)")
        content.append(item("image", a.first, "first_frame"))
        if a.last:
            content.append(item("image", a.last, "last_frame"))
    elif a.mode == "ref":
        refs = list(a.ref)
        if a.map:
            refs.insert(0, str(scene_dir / "blocking_maps" / f"{shot['id']}_blocking_map.png"))
        if not refs and not a.audio:
            sys.exit("ref mode needs at least one --ref image, --map, or --audio")
        if len(refs) > 9:
            sys.exit("the API takes at most 9 reference images")
        n_named = sum(f"reference image {i}" in text.lower() for i in range(1, 10))
        if len(refs) < n_named:
            print(f"WARNING: the prompt names {n_named} reference image(s) but only {len(refs)} will be sent", file=sys.stderr)
        content += [item("image", r, "reference_image") for r in refs]
        content += [item("audio", r, "reference_audio") for r in a.audio]

    spec = MODELS[a.model]
    if a.resolution not in spec["res"]:
        sys.exit(f"{a.model} supports resolutions {spec['res']}")
    duration = a.duration or shot["duration_s"]
    duration = max(spec["dur"][0], min(spec["dur"][1], int(duration)))
    body = {"model": a.model, "content": content, "resolution": a.resolution, "duration": duration}
    if a.mode == "t2v":
        body["ratio"] = a.ratio if a.ratio != "adaptive" else "21:9"
    elif a.mode == "ref":
        body["ratio"] = a.ratio if a.ratio != "adaptive" else "21:9"
    if a.model == "MiniMax-H3-Max":
        body["extra"] = {"prompt_expansion_mode": a.expansion}
    return body


def redacted(body):
    out = json.loads(json.dumps(body))
    for c in out["content"]:
        f = c.pop("_file", None)
        for k in ("image_url", "audio_url", "video_url"):
            if k in c:
                c[k]["url"] = f"<{f}>"
    return out


def call(method, path, key, payload=None):
    req = urllib.request.Request(API + path, method=method,
                                 data=json.dumps(payload).encode() if payload is not None else None,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read() or b"{}")
        except json.JSONDecodeError:
            return e.code, {"error": {"message": e.reason}}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("scene")
    ap.add_argument("shot")
    ap.add_argument("--mode", choices=["t2v", "flf", "ref"], required=True)
    ap.add_argument("--model", choices=sorted(MODELS), default="MiniMax-H3-Max")
    ap.add_argument("--resolution", default="768P")
    ap.add_argument("--duration", type=int, help="seconds (default: the shot's own duration)")
    ap.add_argument("--ratio", default="adaptive", choices=["adaptive", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"])
    ap.add_argument("--first")
    ap.add_argument("--last")
    ap.add_argument("--ref", action="append", default=[], help="reference image (repeatable, ≤9 incl. --map)")
    ap.add_argument("--map", action="store_true", help="add the shot's blocking map as reference image 1")
    ap.add_argument("--audio", action="append", default=[], help="reference audio (repeatable, ≤3)")
    ap.add_argument("--expansion", default="balanced", choices=["disabled", "balanced", "quality"])
    ap.add_argument("--poll", type=int, default=15, help="seconds between status checks")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    scene_dir = Path(a.project) / "03_department_outputs" / f"scene_{a.scene}"
    shots = {s["id"]: s for s in json.loads((scene_dir / "shots.json").read_text())["shots"]}
    if a.shot not in shots:
        sys.exit(f"unknown shot {a.shot}; have {', '.join(shots)}")
    body = build(a, scene_dir, shots[a.shot])
    size = len(json.dumps(redacted(body))) + sum(len(json.dumps(c)) for c in body["content"] if "_file" in c)
    if size > BODY_MAX:
        sys.exit(f"request is {size / 1e6:.1f} MB, over the 64 MB limit; use smaller images")
    print(json.dumps(redacted(body), indent=2))
    print(f"request size ≈ {size / 1e6:.2f} MB")
    if a.dry_run:
        return 0

    key = os.environ.get("MINIMAX_API_KEY")
    if not key:
        sys.exit("MINIMAX_API_KEY is not set")
    send = {**body, "content": [{k: v for k, v in c.items() if k != "_file"} for c in body["content"]]}
    out_dir = scene_dir / "renders"
    out_dir.mkdir(exist_ok=True)
    log = {"shot": a.shot, "mode": a.mode, "request": redacted(body), "submitted_at": time.time()}

    status, resp = call("POST", "/v2/video_generation", key, send)
    task_id = resp.get("task_id")
    if status != 200 or not task_id:
        log["error"] = {"http": status, **resp}
        path = out_dir / f"{a.shot}_{a.mode}_failed_{int(time.time())}.json"
        path.write_text(json.dumps(log, indent=2, ensure_ascii=False))
        print(f"submit failed (HTTP {status}): {resp.get('error', resp)}\nlogged to {path}")
        return 1
    print(f"task {task_id} submitted; polling every {a.poll}s")

    while True:
        time.sleep(a.poll)
        status, resp = call("GET", f"/v2/query/video_generation/{task_id}", key)
        task = resp.get("task", {})
        state = task.get("status", f"http {status}")
        print(f"  {time.strftime('%H:%M:%S')} {state}")
        if state in ("succeeded", "failed", "cancelled") or status >= 400:
            break
    log["result"] = resp
    stem = out_dir / f"{a.shot}_{a.mode}_{task_id}"
    stem.with_suffix(".json").write_text(json.dumps(log, indent=2, ensure_ascii=False))
    url = task.get("content", {}).get("url")
    if state != "succeeded" or not url:
        print(f"task ended {state}; details in {stem.with_suffix('.json')}")
        return 1
    with urllib.request.urlopen(url, timeout=600) as r:
        stem.with_suffix(".mp4").write_bytes(r.read())
    print(f"saved {stem.with_suffix('.mp4')} ({task.get('resolution')}, {task.get('duration')}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
