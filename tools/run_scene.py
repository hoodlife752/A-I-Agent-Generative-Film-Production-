#!/usr/bin/env python3
"""Run one scene through the Prompt Engineer + QA stages of the ai-film-agency pipeline.

Reads a project's bible extract, breakdown, department shot list and Creative
Rationale Reports, then:

  1. Gates every shot on the CRR rule: no prompt is produced for a shot unless
     every department that touched it has filed a report covering it.
  2. Compiles a Shot Report per shot (upstream reports -> synthesis -> prompts).
  3. Assembles the LTX-2.3 / Wan 2.2 prompt pair from locked bible wording,
     plus a MiniMax Omni prompt with a 9-slot reference manifest whose slot 1
     is the shot's top-down scene-blocking map (tools/blocking_map.py).
  4. Marks each pair READY or BLOCKED (missing image lock, missing consent,
     or a hard_block flag), per the Visual Asset Generation addendum.
  5. Writes Visual Asset batch requests and the QA / producer decision report.

Usage:
    python3 tools/run_scene.py projects/dances-with-feddie 001
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

from blocking_map import render_scene as render_blocking_maps

WAN_MAX_S = 5  # Wan 2.2: 81 frames @ 16 fps
OMNI_MAX_REFS = 9


def load(path):
    return json.loads(Path(path).read_text())


def strip_scene_label(prefix):
    prefix = prefix.strip()
    return prefix[: -len("Scene:")].strip() if prefix.endswith("Scene:") else prefix


def image_locked(entry):
    ref = entry.get("image_ref")
    return bool(ref) and ref.get("status") in ("producer_supplied", "chosen") and ref.get("file_in_repo", True)


def shot_blockers(shot, bibles, flags_by_id):
    blockers = []
    for c in shot.get("characters", []):
        ch = bibles["characters"][c["id"]]
        if ch.get("consent_required") and not str(ch.get("consent_status", "")).startswith("confirmed"):
            blockers.append(f"{c['id']}: real-person consent not confirmed (F-04)")
        if not image_locked(ch):
            ref = ch.get("image_ref")
            why = "sheet supplied but file not committed" if ref else "no chosen reference image"
            blockers.append(f"{c['id']}: {why} (F-18)")
        if ch["status"].startswith("provisional"):
            blockers.append(f"{c['id']}: Character Bible is provisional (F-09)")
    loc = shot.get("location")
    if loc and not image_locked(bibles["locations"][loc]):
        blockers.append(f"{loc}: no chosen location reference (F-18)")
    for f in shot.get("flags", []):
        if flags_by_id.get(f, {}).get("severity") == "hard_block" and not any(f in b for b in blockers):
            blockers.append(f"{f}: {flags_by_id[f]['issue']}")
    return list(dict.fromkeys(blockers))


def ltx_prompt(shot, bibles):
    std = bibles["standards"]
    parts = [strip_scene_label(bibles["characters"][c["id"]]["variants"][c["variant"]]) for c in shot.get("characters", [])]
    scene = []
    if shot.get("location"):
        scene.append(bibles["locations"][shot["location"]]["text"])
    scene.append(shot["action"])
    b = shot["blocking"]
    scene.append(f"{std['blocking_prefix']['text']} Focal point — {b['focal_point']}: {b['coords']}.")
    scene.append(f"Camera: {shot['framing']}, {shot['lens']} lens. {shot['camera']}")
    scene.append(f"Lighting: {shot['lighting']}")
    props = [bibles["props"][p]["text"] for p in shot.get("props", [])]
    if props:
        scene.append("Props in frame: " + "; ".join(props) + ".")
    scene.append(std["cinematography_prefix"]["text"])
    for d in shot.get("dialogue", []):
        tone = f" ({d['direction']})" if d.get("direction") else ""
        scene.append(f'{d["who"].title()} says{tone}: "{d["line"]}"')
    if shot.get("audio"):
        scene.append(f"Audio: {shot['audio']}")
    scene.append(f"Duration {shot['duration_s']} seconds. Compose inside a centered 2.39:1 safe area of a 16:9 frame.")
    return " ".join(parts + ["Scene: " + " ".join(scene)])


def wan_prompt(shot, bibles):
    std = bibles["standards"]
    parts = [strip_scene_label(bibles["characters"][c["id"]]["variants"][c["variant"]]) for c in shot.get("characters", [])]
    body = [shot["action"], f"{shot['framing']}, {shot['lens']}. {shot['camera']}", f"Placement: {shot['blocking']['coords']}.", shot["lighting"]]
    positive = " ".join(parts + ["Scene: " + " ".join(body)])
    neg = list(std["global_negatives"])
    for c in shot.get("characters", []):
        neg += bibles["characters"][c["id"]].get("negatives", [])
    if shot.get("location"):
        neg += bibles["locations"][shot["location"]].get("negatives", [])
    exp = shot.get("expressions") or {}
    out = {
        "shot": shot["id"],
        "positive": positive,
        "negative": ", ".join(dict.fromkeys(neg)),
        "first_frame": f"expr/{exp['start']}.png" if exp.get("start") else None,
        "last_frame": f"expr/{exp['end']}.png" if exp.get("end") else None,
        "frames": 81,
        "fps": 16,
    }
    if shot["duration_s"] > WAN_MAX_S:
        out["chaining"] = f"{shot['duration_s']}s > {WAN_MAX_S}s: generate {-(-shot['duration_s'] // WAN_MAX_S)} segments, each segment's last frame seeds the next."
    return out


def omni_refs(shot, bibles, map_path):
    """Reference slots for MiniMax Omni, in priority order, capped at 9."""
    refs = [{"slot_role": "blocking_map", "file": map_path, "status": "ready",
             "use": "Top-down scene-blocking map. Follow its positions and movement arrows; do not render the map itself."}]
    for c in shot.get("characters", []):
        ch = bibles["characters"][c["id"]]
        ref = ch.get("image_ref")
        refs.append({"slot_role": "character", "id": c["id"], "file": ref["file"] if ref else f"02_bibles/refs/{c['id'].lower()}_reference.png",
                     "status": "ready" if image_locked(ch) else "missing", "use": f"Identity + {c['variant']} wardrobe for {c['id']}."})
    if shot.get("location"):
        loc = bibles["locations"][shot["location"]]
        ref = loc.get("image_ref")
        refs.append({"slot_role": "location", "id": shot["location"], "file": ref["file"] if ref else f"02_bibles/refs/{shot['location'].lower()}_plate.png",
                     "status": "ready" if image_locked(loc) else "missing", "use": "Architecture and set dressing."})
    exp = shot.get("expressions") or {}
    for k in ("start", "end"):
        if exp.get(k) and not any(r.get("id") == exp[k] for r in refs):
            refs.append({"slot_role": f"expression_{k}", "id": exp[k], "file": f"expr/{exp[k]}.png", "status": "missing",
                         "use": f"{'Opening' if k == 'start' else 'Closing'} expression."})
    for pid in shot.get("props", []):
        if pid in ("G_WAGON", "SEASONS_CAR", "RICK_BICYCLE", "MILK_CRATE"):
            refs.append({"slot_role": "prop", "id": pid, "file": f"02_bibles/refs/{pid.lower()}.png", "status": "missing", "use": bibles["props"][pid]["text"]})
    dropped = refs[OMNI_MAX_REFS:]
    refs = refs[:OMNI_MAX_REFS]
    for i, r in enumerate(refs, 1):
        r["slot"] = i
    return refs, dropped


def omni_prompt(shot, bibles, refs):
    """MiniMax Omni prompt: prose, with every reference image named by slot."""
    lines = [f"Image {r['slot']}: {r['use']}" if r["slot_role"] == "blocking_map"
             else f"Image {r['slot']} is {r.get('id')} ({r['slot_role'].replace('_', ' ')})." for r in refs]
    b = shot["blocking"]
    body = (f"{shot['action']} Stage the action exactly as the blocking map in Image 1 shows: where each person stands, "
            f"the numbered movement arrows, and the camera position and viewing direction. In frame, the focal point ({b['focal_point']}) sits at {b['coords']}. "
            f"{shot['framing']}, {shot['lens']} lens. {shot['camera']} Lighting: {shot['lighting']} "
            f"{bibles['standards']['cinematography_prefix']['text']}")
    for d in shot.get("dialogue", []):
        body += f' {d["who"].title()} says: "{d["line"]}"'
    return "\n".join(lines) + "\n\n" + body + f"\n\nDuration {shot['duration_s']}s. Cinematic 2.39:1 composition, photoreal, no on-screen text, no map graphics in the output."


def main(project, scene):
    root = Path(project)
    bibles = load(root / "02_bibles" / f"scene_{scene}_bible_extract.json")
    breakdown = load(root / "01_breakdown" / f"scene_{scene}_breakdown.json")
    dept_dir = root / "03_department_outputs" / f"scene_{scene}"
    shotlist = load(dept_dir / "shots.json")
    crrs = load(dept_dir / "creative_rationale_reports.json")
    flags_by_id = {f["id"]: f for f in breakdown["open_flags"]}
    reports = {r["department"]: r for r in crrs["reports"]}

    (dept_dir / "prompts" / "ltx").mkdir(parents=True, exist_ok=True)
    (dept_dir / "prompts" / "wan").mkdir(parents=True, exist_ok=True)
    (dept_dir / "prompts" / "omni").mkdir(parents=True, exist_ok=True)
    maps = {sid: p.relative_to(root).as_posix() for sid, p in render_blocking_maps(project, scene).items()}

    md = [f"# Scene {scene} — Shot Reports\n", f"**{shotlist['slug']}** · {shotlist['timeline']} · source: {shotlist['source_script']}\n",
          "Review order per shot: department reports → Shot Report → prompt pair. Prompts marked **BLOCKED** are drafts and should not be generated until the listed blockers clear.\n"]
    status_rows, gate_failures, expr_use = [], [], defaultdict(list)

    for shot in shotlist["shots"]:
        depts = shot.get("departments", shotlist["default_departments"])
        missing = [d for d in depts if d not in reports]
        md.append(f"\n---\n\n## Shot {shot['id']} · {shot['duration_s']}s\n\n**Beat:** {shot['beat']}\n\n> {shot['script']}\n")
        if missing:
            gate_failures.append((shot["id"], missing))
            md.append(f"\n**GATE FAILED — no prompt produced.** Missing Creative Rationale Reports: {', '.join(missing)}\n")
            status_rows.append((shot["id"], "NO PROMPT", "missing CRR: " + ", ".join(missing)))
            continue
        md.append("\n**Upstream reports:** " + ", ".join(f"{reports[d]['report_id']} ({reports[d]['confidence']})" for d in depts) + "\n")
        if shot.get("type") == "audio_only":
            md.append(f"\n**Audio-only (editorial).** {shot['audio']}\n\n")
            for d in shot["dialogue"]:
                md.append(f"- {d['who']}: \"{d['line']}\"\n")
            md.append(f"\n**Editing:** {shot['editing']}\n")
            status_rows.append((shot["id"], "EDITORIAL", "audio only"))
            continue

        b = shot["blocking"]
        md.append("\n### Shot Report\n")
        md.append(f"- **Blocking / Set:** focal point is *{b['focal_point']}* at {b['hotspot']} — {b['coords']}. Spiral: {b['spiral']}. {b['notes']}\n")
        if shot.get("set_design"):
            md.append(f"- **Set design:** {shot['set_design']}\n")
        md.append(f"- **Camera:** {shot['framing']}, {shot['lens']}. {shot['camera']}\n")
        md.append(f"- **Lighting:** {shot['lighting']}\n")
        cast = ", ".join(f"{c['id']} ({c['variant']})" for c in shot.get("characters", [])) or "none"
        md.append(f"- **Cast / wardrobe:** {cast}\n")
        if shot.get("props"):
            md.append(f"- **Props:** {', '.join(shot['props'])}\n")
        exp = shot.get("expressions") or {}
        if exp:
            md.append(f"- **Expression anchors:** {exp.get('start')} → {exp.get('end')}\n")
            for k in ("start", "end"):
                if exp.get(k):
                    expr_use[exp[k]].append(shot["id"])
        md.append(f"- **Editing:** {shot.get('editing') or '—'}\n")
        md.append(f"- **How it works together:** the camera ({shot['lens']}) arrives at the blocking's focal point — {b['focal_point']} — under {shot['lighting'].split(':')[0]}, so the beat \"{shot['beat'].split('.')[0]}\" lands where the eye already is.\n")

        blockers = shot_blockers(shot, bibles, flags_by_id)
        status = "BLOCKED" if blockers else "READY"
        status_rows.append((shot["id"], status, "; ".join(blockers)))
        if shot.get("flags"):
            md.append(f"- **Open flags:** {', '.join(shot['flags'])}\n")
        md.append(f"\n### Prompt pair — **{status}**\n")
        if blockers:
            md.append("Blockers:\n" + "".join(f"- {x}\n" for x in blockers))

        ltx = ltx_prompt(shot, bibles)
        wan = wan_prompt(shot, bibles)
        (dept_dir / "prompts" / "ltx" / f"{shot['id']}.txt").write_text(ltx + "\n")
        (dept_dir / "prompts" / "wan" / f"{shot['id']}.json").write_text(json.dumps(wan, indent=2, ensure_ascii=False) + "\n")
        md.append(f"\n**LTX-2.3**\n\n```text\n{ltx}\n```\n")
        md.append(f"\n**Wan 2.2** (first frame `{wan['first_frame']}`, last frame `{wan['last_frame']}`)"
                  + (f" — {wan['chaining']}" if wan.get("chaining") else "") + "\n\n")
        md.append(f"```text\n{wan['positive']}\n```\n\nNegative:\n\n```text\n{wan['negative']}\n```\n")

        if shot["id"] in maps:
            refs, dropped = omni_refs(shot, bibles, maps[shot["id"]])
            omni = {"shot": shot["id"], "prompt": omni_prompt(shot, bibles, refs), "references": refs,
                    "dropped_over_limit": dropped, "duration_s": shot["duration_s"]}
            (dept_dir / "prompts" / "omni" / f"{shot['id']}.json").write_text(json.dumps(omni, indent=2, ensure_ascii=False) + "\n")
            md.append(f"\n**MiniMax Omni** ({len(refs)}/{OMNI_MAX_REFS} references"
                      + (f", {len(dropped)} dropped over the limit" if dropped else "") + ")\n\n"
                      + f"![blocking map {shot['id']}](blocking_maps/{shot['id']}_blocking_map.png)\n\n"
                      + "| Slot | Reference | File | Status |\n|---|---|---|---|\n"
                      + "".join(f"| {r['slot']} | {r['slot_role']}{' · ' + r['id'] if r.get('id') else ''} | `{r['file']}` | {r['status']} |\n" for r in refs)
                      + f"\n```text\n{omni['prompt']}\n```\n")

    (dept_dir / "shot_reports.md").write_text("".join(md))

    # Visual Asset Generation batch requests + expression manifest
    va = [f"# Scene {scene} — Visual Asset Generation requests\n\n",
          "Each request is one prompt run 5× (different seeds), giving five readings of the same locked text. **The producer picks one.** Nothing is auto-selected.\n\n",
          "Log each pick in `02_bibles/refs/choice_log.json` as `{asset, candidate, picked_by, why}` and put the file at the path shown.\n\n## Reference batches\n\n"]
    sheet = "Character reference sheet on a neutral gray studio background, even lighting: full body front, 3/4 left, 3/4 right, full profile, close-up face. "
    for cid, ch in bibles["characters"].items():
        if ch.get("consent_required") and not str(ch.get("consent_status", "")).startswith("confirmed"):
            va.append(f"### {cid} — HELD (consent)\n\n{ch['consent_status']}.\n\n")
            continue
        if ch.get("image_ref"):
            va.append(f"### {cid} — producer sheet received\n\nCommit to `{ch['image_ref']['file']}`. {ch['image_ref'].get('sheet_notes', '')}\n\n")
            continue
        variant = ch.get("scene_variant", "present_day")
        va.append(f"### {cid} ({ch['status']})\n\n```text\n{sheet}{strip_scene_label(ch['variants'][variant])}\n```\n\n")
    for lid, loc in bibles["locations"].items():
        if loc.get("status") == "producer_supplied_unassigned":
            va.append(f"### {lid} — producer photo received, location unassigned (F-21)\n\n{loc['description']}\n\n")
            continue
        va.append(f"### {lid} ({loc['status']})\n\n```text\nEmpty establishing reference plate, dawn, no people in foreground, 16:9. {loc['text']}\n```\n\n")
    va.append("## Expression manifest (Image Consistency → Wan first/last frames)\n\nGenerated once each character's reference is locked. File: `expr/<ID>.png`.\n\n| Expression | Shots anchored |\n|---|---|\n")
    for e, ids in sorted(expr_use.items()):
        va.append(f"| `{e}` | {', '.join(dict.fromkeys(ids))} |\n")
    (dept_dir / "visual_asset_batches.md").write_text("".join(va))

    # QA / Continuity report
    ready = [r for r in status_rows if r[1] == "READY"]
    blocked = [r for r in status_rows if r[1] == "BLOCKED"]
    qa = [f"# Scene {scene} — QA / Continuity report\n\n",
          f"**Shots:** {len(status_rows)} · **Ready to generate:** {len(ready)} · **Blocked (draft prompts written):** {len(blocked)} · "
          f"**CRR gate failures:** {len(gate_failures)} · **Runtime:** ≈{sum(s['duration_s'] for s in shotlist['shots']) // 60}m{sum(s['duration_s'] for s in shotlist['shots']) % 60:02d}s\n\n",
          "## CRR gate\n\n", "All shots passed: every department that touched a shot filed a report.\n\n" if not gate_failures
          else "".join(f"- {sid}: missing {', '.join(m)}\n" for sid, m in gate_failures),
          "\n## Report confidence\n\n| Report | Department | Confidence | Unresolved teamwork |\n|---|---|---|---|\n"]
    for r in crrs["reports"]:
        un = "; ".join(f"{t['with']} ({t.get('flag', '')})" for t in r["teamwork"] if t.get("unresolved")) or "—"
        qa.append(f"| {r['report_id']} | {r['department']} | {r['confidence']} | {un} |\n")
    qa.append("\n## Producer decision queue\n\nSurfaced by the Managing Agent. No agent resolves these on its own.\n\n")
    order = {"hard_block": 0, "block_until_bible": 1, "conflict": 2, "decision": 3, "risk": 4, "question": 5, "minor": 6}
    for f in sorted(breakdown["open_flags"], key=lambda f: order.get(f["severity"], 9)):
        qa.append(f"- **{f['id']} [{f['severity']}] ({f['owner']})**: {f['issue']}\n  - *Applied for now:* {f['applied']}\n  - *Needs:* {f['needs']}\n")
    qa.append("\n## Shot status\n\n| Shot | Status | Blockers |\n|---|---|---|\n")
    for sid, st, why in status_rows:
        qa.append(f"| {sid} | {st} | {why or '—'} |\n")
    qa_dir = root / "04_qa"
    qa_dir.mkdir(exist_ok=True)
    (qa_dir / f"scene_{scene}_qa_report.md").write_text("".join(qa))

    print(f"scene {scene}: {len(status_rows)} shots | ready {len(ready)} | blocked {len(blocked)} | gate failures {len(gate_failures)}")
    return 1 if gate_failures else 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
