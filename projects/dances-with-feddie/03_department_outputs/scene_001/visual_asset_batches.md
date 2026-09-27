# Scene 001 — Visual Asset Generation requests

Each request is one prompt run 5× (different seeds), giving five readings of the same locked text. **The producer picks one.** Nothing is auto-selected.

Log each pick in `02_bibles/refs/choice_log.json` as `{asset, candidate, picked_by, why}` and put the file at the path shown.

## Reference batches

### PAUL (locked_text)

```text
Character reference sheet on a neutral gray studio background, even lighting: full body front, 3/4 left, 3/4 right, full profile, close-up face. [PAUL] Same character as reference image: white man in his late 20s to early 30s, gaunt thin build, dirty blonde wavy shoulder-length hair, disheveled, light patchy stubble, blue eyes, pained distressed expression, wearing a gray hooded sweatshirt. Maintain exact facial structure and build from reference.
```

### KILLA (locked_text)

```text
Character reference sheet on a neutral gray studio background, even lighting: full body front, 3/4 left, 3/4 right, full profile, close-up face. [KILLA] Same character as reference image: 40-year-old African American man, tall, slim build, long shoulder-length dreadlocks, missing front left tooth, clean-shaven, black eyes, sagging jawline, longish hands, smooth confident charming demeanor, several gold rings, gold nugget bracelet. Wearing a bomber jacket with a fake fur-lined hood, jeans, boots, and a dark brown beanie. Maintain exact facial structure and build from reference.
```

### RUBY (locked_text)

```text
Character reference sheet on a neutral gray studio background, even lighting: full body front, 3/4 left, 3/4 right, full profile, close-up face. [RUBY] Same character as reference image: 66-year-old Cherokee woman, smooth skin with only faint fine lines at the eyes, high cheekbones, sharp restless dark eyes, thick dark hair with silver strands in a loose braid, wearing a pink robe, barefoot, turquoise ring, turquoise pendant necklace. No facial tattoos, no gray-all-over hair, no gaunt features, no wrinkling. Maintain exact facial structure from reference.
```

### SEASON (locked_text)

```text
Character reference sheet on a neutral gray studio background, even lighting: full body front, 3/4 left, 3/4 right, full profile, close-up face. [SEASON] Same character as reference image: 44-year-old woman, half Cherokee and half Black, tall, overweight build, thick hair in a braid, black eyes, wears glasses, dimples visible when smiling, cross necklace, pigeon-toed stance, serious devout demeanor. Wearing a waitress work uniform. Maintain exact facial structure and build from reference.
```

### SARAH (locked_text)

```text
Character reference sheet on a neutral gray studio background, even lighting: full body front, 3/4 left, 3/4 right, full profile, close-up face. [SARAH] Same character as reference image: 25-year-old pretty woman with strawberry blonde hair styled in a 1940s-style updo, emerald green eyes, strong jawline, dimpled chin, curvaceous figure. Wearing a blouse, cream sweater, and black stylish boots. Maintain exact facial structure and build from reference.
```

### MOODY — HELD (consent)

unverified — a reference sheet exists but consent_log.json is not visible to this run; the sheet does not prove consent.

### POOCHIE (provisional_script_only)

```text
Character reference sheet on a neutral gray studio background, even lighting: full body front, 3/4 left, 3/4 right, full profile, close-up face. [POOCHIE] 35-year-old mixed-race Black man with a half-straight afro, dark striking good looks, relaxed ladies'-man confidence.
```

### GINA (provisional_script_only)

```text
Character reference sheet on a neutral gray studio background, even lighting: full body front, 3/4 left, 3/4 right, full profile, close-up face. [GINA] 35-year-old Hispanic woman, a fighter's posture and a loud, instigating energy.
```

### BELLE (provisional_script_only)

```text
Character reference sheet on a neutral gray studio background, even lighting: full body front, 3/4 left, 3/4 right, full profile, close-up face. [BELLE] 30-year-old Black woman, small of stature and ladylike, wearing a dress and heels, hair, make-up and nails done to perfection.
```

### IZZY — producer sheet received

Commit to `02_bibles/refs/izzy_reference_sheet.png`. Full body front / 3-4 L / 3-4 R / profile / glasses close-up / stance, plus expressions: embarrassed half-smile, forced laugh, wincing/flinching, rare unguarded moment.

### RICK — producer sheet received

Commit to `02_bibles/refs/rick_reference_sheet.png`. 3-4 L / 3-4 R / close-up face (beard) / back view / hands on handlebars / feet & footwear / bicycle as prop (dark green bike with front wire basket holding a cardboard box).

### TINA (provisional_script_only)

```text
Character reference sheet on a neutral gray studio background, even lighting: full body front, 3/4 left, 3/4 right, full profile, close-up face. [TINA] 30-year-old white woman, worn street clothes.
```

### SOLEDAD_SUEY_SING (locked_text_with_open_conflicts)

```text
Empty establishing reference plate, dawn, no people in foreground, 16:9. The Suey Sing Building on Soledad Street, Chinatown, Salinas: tan/cream single-story stucco building, weathered signage, boarded and graffiti-covered sections along the lower wall, no fence in front. The seven-story Moongate Apartments rise on its left. On its right, a dirt, weed and rock-filled field holds twenty weathered tents. Against the building's wall: a tent in each corner and a huge tarp-built two-unit structure between them, with shopping carts, bikes and belongings.
```

### DOROTHYS_PLACE (locked_text_with_open_conflicts)

```text
Empty establishing reference plate, dawn, no people in foreground, 16:9. Dorothy's Place, directly across Soledad Street from the Suey Sing Building: two-story Spanish/mission-style building, yellow stucco walls, dark-red trim and support beams, upper wooden balcony with railing, green-trimmed windows, three recessed cubbyhole entrances at ground level, yellow brick wall topped with black steel spikes running left and right, a large shade tree, a utility pole standing directly in front near the entrance.
```

### MOONGATE_FRONT (provisional_script_only)

```text
Empty establishing reference plate, dawn, no people in foreground, 16:9. The sidewalk in front of the entrance of the seven-story Moongate Apartments on Soledad Street, the Suey Sing Building to its right.
```

### VICTORY_MISSION (provisional_script_only)

```text
Empty establishing reference plate, dawn, no people in foreground, 16:9. The Victory Mission at the southern end of the block, a brick building past the tent field, people hanging out in front.
```

### UNLABELED_STREET_PHOTO — producer photo received, location unassigned (F-21)

Wide, overcast street: pink two-story building and a tree on the left, cars parked nose-in at a lot on the right in front of a corrugated-metal warehouse with a roll-up door, a long green-roofed building at the far end, utility poles and overhead lines, a tan pickup in the right foreground.

## Expression manifest (Image Consistency → Wan first/last frames)

Generated once each character's reference is locked. File: `expr/<ID>.png`.

| Expression | Shots anchored |
|---|---|
| `GINA_neutral_busy` | 1-04 |
| `KILLA_cool_unbothered` | 1-08, 1-11 |
| `KILLA_smile_dealing` | 1-16, 1-17 |
| `KILLA_smirk_unsympathetic` | 1-14 |
| `KILLA_wide_eyed_impressed` | 1-17 |
| `PAUL_deflated_crushed` | 1-12, 1-13 |
| `PAUL_hope_desperation` | 1-09, 1-12 |
| `PAUL_pleading_outward` | 1-07 |
| `PAUL_scanning_restless` | 1-02, 1-09 |
| `PAUL_sick_pained` | 1-13, 1-15 |
| `PAUL_thoughtful_weighing` | 1-15 |
| `RICK_concerned` | 1-28 |
| `RICK_guilty` | 1-28, 1-30 |
| `RUBY_annoyed` | 1-33, 1-35, 1-37 |
| `RUBY_cold_satisfaction` | 1-42 |
| `RUBY_disgust` | 1-37, 1-40 |
| `RUBY_gunfighter_squint` | 1-40, 1-42 |
| `RUBY_haunted_fear` | 1-27, 1-29 |
| `RUBY_mocking_laugh` | 1-43 |
| `RUBY_nervous_worried` | 1-24, 1-25, 1-26, 1-27 |
| `RUBY_sour_face` | 1-31, 1-33 |
| `RUBY_suspicious` | 1-29 |
| `SARAH_tipsy_storytelling` | 1-03 |
| `SEASON_caught_off_guard` | 1-41 |
| `SEASON_giddy_goofy_smile` | 1-34, 1-36, 1-38 |
| `SEASON_huffy_offended` | 1-43 |
| `SEASON_playful_teasing` | 1-39, 1-41 |
