# Scene 002 — Visual Asset Generation requests

Each request is one prompt run 5× (different seeds), giving five readings of the same locked text. **The producer picks one.** Nothing is auto-selected.

Log each pick in `02_bibles/refs/choice_log.json` as `{asset, candidate, picked_by, why}` and put the file at the path shown.

## Reference batches

### DANCES (locked_text)

```text
Character reference sheet on a neutral gray studio background, even lighting: full body front, 3/4 left, 3/4 right, full profile, close-up face. [DANCES] Same character as reference image: 22-year-old woman, mixed Cherokee and Black heritage, warm brown skin, high cheekbones, dark almond eyes, hard unimpressed expression, thick dark hair in two thick braids, tribal tattoos on both arms and neck only (no facial tattoos), worn brown leather jacket, gray tank top, dark jeans, boots. Maintain exact facial structure, tattoo placement, and wardrobe from reference. Neck tattoo limited to the left side of the neck only, small feather design, does not extend past the collarbone, no chest tattoo.
```

### CHURCH_STOOP (locked_text)

```text
Empty establishing reference plate, dawn, no people in foreground, 16:9. The Salinas Confucius Church: ornate red-tiled roof, decorative red trim, tan stucco walls, columned entrance with dark wooden double doors, church signage above the entrance door, a utility pole and street lamp nearby. On the church stoop, a small blue tent with a blue tarp draped over it sits on the left side (Dances' tent), and a light tan tent with no tarp sits on the right side (Brandon's tent).
```

## Expression manifest (Image Consistency → Wan first/last frames)

Generated once each character's reference is locked. File: `expr/<ID>.png`.

| Expression | Shots anchored |
|---|---|
| `DANCES_nodding_eyes_closed` | 2-02, 2-03 |
| `DANCES_pained_hum` | 2-03, 2-04 |
