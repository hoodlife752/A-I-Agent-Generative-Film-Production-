#!/usr/bin/env python3
"""Render top-down scene-blocking maps: one labeled PNG per shot.

Each map is a blueprint of the location (site plan) with the shot's actors,
vehicles, props, camera position + field-of-view cone, and numbered arrows for
every movement, plus a side panel that spells the movements out in text. The
maps are made to be uploaded as a reference image (slot 1) for multi-reference
video models such as MiniMax Omni.

Usage (normally called by run_scene.py):
    python3 tools/blocking_map.py projects/dances-with-feddie 001
"""
import json
import math
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
MAP_AT = (40, 40)                   # where the map is pasted on the canvas
MAP = (0, 0, 1000, 1000)            # map drawing area, on its own (clipped) image
PANEL_X = 1090
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
LENS_FOV = {14: 104, 24: 84, 28: 75, 35: 63, 50: 47, 85: 28, 100: 24}

INK, PAPER, GRID = (28, 38, 56), (236, 240, 245), (214, 221, 230)
STREET, WALK, FIELD = (120, 126, 136), (196, 200, 206), (206, 192, 150)
BLDG, BLDG_MUTED = (160, 176, 196), (205, 211, 219)
CAM_C = (200, 30, 40)
PALETTE = [(24, 110, 190), (214, 110, 20), (40, 150, 80), (150, 60, 170), (190, 150, 0),
           (0, 150, 160), (200, 60, 120), (110, 90, 60), (60, 60, 60), (90, 130, 30)]


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(str(FONT_DIR / name), size)
    except OSError:
        return ImageFont.load_default()


def lens_mm(lens):
    m = re.search(r"(\d+)\s*mm", lens or "")
    return int(m.group(1)) if m else 50


def fov_for(lens):
    mm = lens_mm(lens)
    return LENS_FOV[min(LENS_FOV, key=lambda k: abs(k - mm))]


class View:
    """World (meters, y up) → canvas (px, y down) for a square viewport."""

    def __init__(self, cx, cy, span):
        self.x0, self.y0, self.span = cx - span / 2, cy - span / 2, span
        self.s = (MAP[2] - MAP[0]) / span

    def p(self, x, y):
        return (MAP[0] + (x - self.x0) * self.s, MAP[3] - (y - self.y0) * self.s)

    def r(self, x0, y0, x1, y1):
        a, b = self.p(x0, y1), self.p(x1, y0)
        return [a[0], a[1], b[0], b[1]]


def viewport(spec, extent):
    pts = [spec["cam"][:2]]
    pts += list(spec.get("actors", {}).values()) + list(spec.get("vehicles", {}).values())
    pts += [p for _, p in spec.get("props", [])]
    for m in spec.get("moves", []):
        pts += m[1]
    pts += spec.get("cam_path", [])
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    span = max(max(xs) - min(xs), max(ys) - min(ys)) + 24
    span = max(span, 44)
    span = min(span, max(extent[2] - extent[0], extent[3] - extent[1]))
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return View(cx, cy, span)


def arrow(d, pts, color, width=5, dash=False):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if dash:
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / 14))
            for i in range(0, n, 2):
                a, b = i / n, min(1, (i + 1) / n)
                d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)], fill=color, width=width)
        else:
            d.line([(x0, y0), (x1, y1)], fill=color, width=width)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ang = math.atan2(y1 - y0, x1 - x0)
    head = [(x1, y1), (x1 - 22 * math.cos(ang - 0.4), y1 - 22 * math.sin(ang - 0.4)),
            (x1 - 22 * math.cos(ang + 0.4), y1 - 22 * math.sin(ang + 0.4))]
    d.polygon(head, fill=color)


def badge(d, xy, text, color):
    x, y = xy
    d.ellipse([x - 15, y - 15, x + 15, y + 15], fill=color, outline=PAPER, width=3)
    f = font(17, True)
    tw = d.textlength(text, font=f)
    d.text((x - tw / 2, y - 11), text, font=f, fill=PAPER)


def draw_site(d, v, site):
    ex = site["extent"]
    d.rectangle(v.r(*ex), fill=PAPER)
    step = 10
    for gx in range(int(ex[0]), int(ex[2]) + 1, step):
        d.line([v.p(gx, ex[1]), v.p(gx, ex[3])], fill=GRID, width=1)
    for gy in range(int(ex[1]), int(ex[3]) + 1, step):
        d.line([v.p(ex[0], gy), v.p(ex[2], gy)], fill=GRID, width=1)
    for sw in site["sidewalks"]:
        d.rectangle(v.r(sw["x"][0], ex[1], sw["x"][1], ex[3]), fill=WALK)
    sx = site["street"]["x"]
    d.rectangle(v.r(sx[0], ex[1], sx[1], ex[3]), fill=STREET)
    mid = (sx[0] + sx[1]) / 2
    for y in range(int(ex[1]), int(ex[3]), 6):
        d.line([v.p(mid, y), v.p(mid, y + 3)], fill=(235, 200, 60), width=3)
    for a in site.get("areas", []):
        d.rectangle(v.r(*a["rect"]), fill=tuple(a.get("fill", FIELD)), outline=INK, width=2)
        x0, y0, x1, y1 = a["rect"]
        for k in range(1, a.get("steps", 0)):
            sx_ = x0 + (x1 - x0) * k / a["steps"]
            d.line([v.p(sx_, y0), v.p(sx_, y1)], fill=INK, width=2)
    fr = site.get("field", {}).get("rect")
    if fr:
        d.rectangle(v.r(*fr), fill=FIELD, outline=INK, width=2)
    cols = 5
    for i in range(site.get("field", {}).get("tents", 0)):
        tx = fr[0] + 3 + (i % cols) * (fr[2] - fr[0] - 6) / (cols - 1)
        ty = fr[1] + 4 + (i // cols) * (fr[3] - fr[1] - 8) / 3 + (2 if i % 2 else 0)
        px, py = v.p(tx, ty)
        s = max(4, v.s * 1.2)
        d.polygon([(px, py - s), (px - s, py + s * 0.7), (px + s, py + s * 0.7)], fill=(120, 110, 90), outline=INK)
    if site.get("alley"):
        d.rectangle(v.r(*site["alley"]["rect"]), fill=WALK)
    for b in site["buildings"]:
        d.rectangle(v.r(*b["rect"]), fill=BLDG_MUTED if b.get("muted") else BLDG, outline=INK, width=3)
    pc = site.get("parked_cars")
    for curb_x, key in ((sx[0] + 1.2, "west_curb_y"), (sx[1] - 3.2, "east_curb_y")) if pc else ():
        y = pc[key][0]
        while y < pc[key][1]:
            d.rectangle(v.r(curb_x, y, curb_x + 2, y + 4.5), fill=(90, 96, 108), outline=INK)
            y += pc["spacing"]
    for fx in site["fixtures"]:
        px, py = v.p(*fx["at"])
        k = fx["kind"]
        if k == "pole":
            d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=INK)
        elif k == "tree":
            rr = v.s * 3
            d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=(120, 170, 110), outline=INK)
        elif k in ("tent", "shelter"):
            s = v.s * (1.5 if k == "tent" else 2.5)
            fill = tuple(fx["color"]) if fx.get("color") else (80, 120, 150) if k == "shelter" else (120, 110, 90)
            d.rectangle([px - s, py - s, px + s, py + s], fill=fill, outline=INK, width=2)
        else:
            d.rectangle([px - 6, py - 10, px + 6, py + 10], fill=(90, 60, 40))


def draw_labels(d, v, site):
    """Text on top of everything, clipped to what's visible."""
    def visible(x, y):
        return v.x0 <= x <= v.x0 + v.span and v.y0 <= y <= v.y0 + v.span

    f_b, f_s = font(20, True), font(15)
    for b in site["buildings"]:
        x0, y0, x1, y1 = b["rect"]
        cx, cy = (max(x0, v.x0) + min(x1, v.x0 + v.span)) / 2, (max(y0, v.y0) + min(y1, v.y0 + v.span)) / 2
        if visible(cx, cy):
            px, py = v.p(cx, cy)
            d.multiline_text((px, py), b["label"], font=f_b, fill=INK, anchor="mm", align="center")
    for a in ([site["field"]] if site.get("field") else []) + site.get("areas", []):
        fr = a["rect"]
        cx, cy = (max(fr[0], v.x0) + min(fr[2], v.x0 + v.span)) / 2, min(fr[3] - 2, v.y0 + v.span - 2)
        if visible(cx, cy) and cy > fr[1]:
            d.multiline_text(v.p(cx, cy), a["label"], font=f_b, fill=INK, anchor="ma", align="center")
    sx = site["street"]["x"]
    ly = v.y0 + v.span * 0.12
    img_txt = Image.new("RGBA", (600, 40), (0, 0, 0, 0))
    ImageDraw.Draw(img_txt).text((300, 20), site["street"]["label"], font=font(24, True), fill=(255, 255, 255), anchor="mm")
    d._image.paste(img_txt.rotate(90, expand=True), tuple(int(c) for c in (v.p((sx[0] + sx[1]) / 2, ly)[0] - 20, v.p(0, ly)[1] - 300)),
                   img_txt.rotate(90, expand=True))
    for fx in site["fixtures"]:
        if visible(*fx["at"]) and (fx["kind"] in ("door", "pole", "shelter") or fx.get("color")):
            px, py = v.p(*fx["at"])
            d.text((px + 10, py + 8), fx["label"], font=f_s, fill=INK)


def draw_camera(d, v, cam, lens, cam_path):
    x, y, hdg = cam
    fov = fov_for(lens)
    L = 28 if lens_mm(lens) >= 70 else 20
    px, py = v.p(x, y)
    pts = [(px, py)]
    for a in (hdg - fov / 2, hdg + fov / 2):
        wx, wy = x + L * math.sin(math.radians(a)), y + L * math.cos(math.radians(a))
        pts.append(v.p(wx, wy))
    overlay = Image.new("RGBA", d._image.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).polygon(pts, fill=CAM_C + (48,), outline=CAM_C + (200,))
    d._image.paste(Image.alpha_composite(d._image.convert("RGBA"), overlay).convert("RGB"))
    if cam_path:
        arrow(d, [v.p(*p) for p in cam_path], CAM_C, width=4, dash=True)
    s = 16
    d.polygon([(px, py - s), (px + s, py), (px, py + s), (px - s, py)], fill=CAM_C, outline=PAPER)
    d.text((px + 18, py - 30), f"CAM {lens_mm(lens)}mm", font=font(18, True), fill=CAM_C)


def render_shot(shot, spec, site, colors, out_path, scene_label):
    img = Image.new("RGB", (W, H), (250, 251, 253))
    m = Image.new("RGB", (MAP[2], MAP[3]), PAPER)
    d = ImageDraw.Draw(m)
    v = viewport(spec, site["extent"])
    draw_site(d, v, site)
    draw_camera(d, v, spec["cam"], shot.get("lens"), spec.get("cam_path"))
    d = ImageDraw.Draw(m)
    draw_labels(d, v, site)

    notes, n = [], 0
    for who, path, label in spec.get("moves", []):
        color = CAM_C if who == "CAM" else (255, 200, 0) if who == "LIGHT" else colors.get(who, INK)
        pts = [v.p(*p) for p in path]
        if len(pts) >= 2 and math.dist(pts[0], pts[-1]) > 4:
            arrow(d, pts, color, width=6, dash=who in ("CAM", "LIGHT"))
        if label:
            n += 1
            mx, my = pts[len(pts) // 2] if len(pts) > 2 else ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2)
            badge(d, (mx + 22, my), str(n), color)
            notes.append((str(n), who, label, color))
    if spec.get("whip_to") is not None:
        x, y, _ = spec["cam"]
        tip = (x + 16 * math.sin(math.radians(spec["whip_to"])), y + 16 * math.cos(math.radians(spec["whip_to"])))
        arrow(d, [v.p(x, y), v.p(*tip)], CAM_C, width=6, dash=True)

    f_name = font(19, True)
    for who, (x, y) in {**spec.get("actors", {}), **spec.get("vehicles", {})}.items():
        px, py = v.p(x, y)
        c = colors.get(who, INK)
        if who in spec.get("vehicles", {}):
            d.rounded_rectangle([px - 14, py - 26, px + 14, py + 26], radius=6, fill=c, outline=INK, width=2)
        else:
            d.ellipse([px - 13, py - 13, px + 13, py + 13], fill=c, outline=PAPER, width=3)
        tw = d.textlength(who, font=f_name)
        d.rectangle([px + 16, py - 13, px + 22 + tw, py + 13], fill=(255, 255, 255))
        d.text((px + 19, py - 11), who, font=f_name, fill=c)
    for label, (x, y) in spec.get("props", []):
        px, py = v.p(x, y)
        d.rectangle([px - 7, py - 7, px + 7, py + 7], fill=(250, 250, 250), outline=INK, width=3)
        d.text((px + 10, py + 6), label, font=font(16, True), fill=INK)

    # north arrow + scale
    nx, ny = MAP[2] - 50, MAP[1] + 60
    d.polygon([(nx, ny - 34), (nx - 14, ny + 6), (nx + 14, ny + 6)], fill=INK)
    d.text((nx, ny + 10), "N", font=font(22, True), fill=INK, anchor="mt")
    sb = v.s * 10
    d.line([(MAP[0] + 20, MAP[3] - 24), (MAP[0] + 20 + sb, MAP[3] - 24)], fill=INK, width=5)
    d.text((MAP[0] + 20, MAP[3] - 52), "10 m", font=font(16, True), fill=INK)
    d.rectangle([0, 0, MAP[2] - 1, MAP[3] - 1], outline=INK, width=4)
    img.paste(m, MAP_AT)
    d = ImageDraw.Draw(img)

    # side panel
    y = 48
    d.text((PANEL_X, y), f"{scene_label} · SHOT {shot['id']}", font=font(40, True), fill=INK)
    y += 56
    d.text((PANEL_X, y), "SCENE-BLOCKING MAP · top-down plan", font=font(22, True), fill=(90, 100, 120))
    y += 44
    y = wrap(d, shot["beat"], PANEL_X, y, font(22), 780) + 16
    cast = ", ".join(c["id"] for c in shot.get("characters", [])) or "—"
    for k, val in (("Camera", f"{shot.get('framing')} · {shot.get('lens')} · {shot.get('camera')}"),
                   ("Cast", cast), ("Light", shot.get("lighting", ""))):
        d.text((PANEL_X, y), k.upper(), font=font(18, True), fill=CAM_C if k == "Camera" else INK)
        y = wrap(d, val, PANEL_X + 110, y, font(19), 670) + 10
    y += 8
    d.line([(PANEL_X, y), (W - 40, y)], fill=GRID, width=3)
    y += 16
    d.text((PANEL_X, y), "MOVEMENT", font=font(24, True), fill=INK)
    y += 38
    if not notes:
        y = wrap(d, "No movement: held positions.", PANEL_X, y, font(20), 780) + 6
    for num, who, label, color in notes:
        badge(d, (PANEL_X + 16, y + 14), num, color)
        y = wrap(d, f"{who}: {label}", PANEL_X + 44, y, font(20), 736) + 10
    for note in spec.get("notes", []):
        y = wrap(d, f"• {note}", PANEL_X, y, font(20), 780) + 6
    y += 10
    d.text((PANEL_X, H - 70), "Red diamond = camera, cone = field of view. Solid arrows = actor/vehicle moves.\n"
           "Dashed red = camera move / whip. Dashed yellow = light. Plan view only; in-frame\n"
           "placement follows the Dynamic Symmetry coordinates in the shot report.",
           font=font(15), fill=(90, 100, 120))
    img.save(out_path, optimize=True)


def wrap(d, text, x, y, f, width):
    line = ""
    for word in str(text).split():
        trial = f"{line} {word}".strip()
        if d.textlength(trial, font=f) > width and line:
            d.text((x, y), line, font=f, fill=INK)
            y += f.size + 6
            line = word
        else:
            line = trial
    if line:
        d.text((x, y), line, font=f, fill=INK)
        y += f.size + 6
    return y


def render_scene(project, scene):
    root = Path(project)
    dept_dir = root / "03_department_outputs" / f"scene_{scene}"
    shotlist = json.loads((dept_dir / "shots.json").read_text())
    site = json.loads((root / "02_bibles" / shotlist.get("site_plan", "soledad_site_plan.json")).read_text())
    shots = {s["id"]: s for s in shotlist["shots"]}
    maps = json.loads((dept_dir / "blocking_maps.json").read_text())["maps"]
    out_dir = dept_dir / "blocking_maps"
    out_dir.mkdir(exist_ok=True)
    names = sorted({w for m in maps.values() for w in list(m.get("actors", {})) + list(m.get("vehicles", {})) + [mv[0] for mv in m.get("moves", [])]} - {"CAM", "LIGHT"})
    colors = {n: PALETTE[i % len(PALETTE)] for i, n in enumerate(names)}
    written = {}
    for sid, spec in maps.items():
        path = out_dir / f"{sid}_blocking_map.png"
        render_shot(shots[sid], spec, site, colors, path, f"SCENE {int(scene)}")
        written[sid] = path
    return written


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    print(f"{len(render_scene(sys.argv[1], sys.argv[2]))} blocking maps written")
