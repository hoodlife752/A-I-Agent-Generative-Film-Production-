# Scene 001 — QA / Continuity report

**Shots:** 43 · **Ready to generate:** 0 · **Blocked (draft prompts written):** 42 · **CRR gate failures:** 0 · **Runtime:** ≈3m39s

## CRR gate

All shots passed: every department that touched a shot filed a report.


## Report confidence

| Report | Department | Confidence | Unresolved teamwork |
|---|---|---|---|
| CRR-001-CAS | casting | flagged_for_human_review | wardrobe (F-05); visual_asset_generation (F-04); script_supervisor (F-03, F-07, F-08, F-09) |
| CRR-001-WAR | wardrobe | provisional_pending_upstream | casting (F-05) |
| CRR-001-PRO | props | provisional_pending_upstream | location (F-02) |
| CRR-001-LOC | location | flagged_for_human_review | scene_blocking (F-10); set_designer (F-11) |
| CRR-001-BLK | scene_blocking | locked | — |
| CRR-001-SET | set_designer | locked | — |
| CRR-001-CIN | cinematography | provisional_pending_upstream | — |
| CRR-001-LGT | lighting | flagged_for_human_review | location (F-15) |
| CRR-001-IMG | image_consistency | provisional_pending_upstream | visual_asset_generation (F-18) |
| CRR-001-VAG | visual_asset_generation | provisional_pending_upstream | casting (F-04); producer (F-18) |
| CRR-001-EDT | editing | locked | — |

## Producer decision queue

Surfaced by the Managing Agent. No agent resolves these on its own.

- **F-04 [hard_block] (Visual Asset Generation)**: MOODY is based on a real person (Santa Cruz) and requires documented consent. consent_log.json is not visible to this run. A reference sheet was supplied on 2026-09-27; that is not proof of consent.
  - *Applied for now:* Every shot with MOODY (1-03) is blocked for generation.
  - *Needs:* Confirm the consent_log.json entry.
- **F-18 [hard_block] (Visual Asset Generation)**: No chosen reference image exists yet for PAUL, KILLA, RUBY, SEASON, SARAH, POOCHIE, GINA, BELLE, TINA or any location. Sheets were received for MOODY, IZZY and RICK, but the files are not in the repo.
  - *Applied for now:* 5-candidate batch prompts drafted (visual_asset_batches.md).
  - *Needs:* A producer pick per asset; commit the supplied sheet files to 02_bibles/refs/.
- **F-09 [block_until_bible] (Casting)**: No Character Bibles exist for POOCHIE, GINA, BELLE, IZZY, RICK, TINA. Gina is 25HF in the header vs 35 in the description. Poochie, Gina, Belle and Tina have no wardrobe. Izzy and Rick now have producer reference sheets (2026-09-27). The Location Bible note also mentions Elsa and Gina's daughter Samantha, who are not in the Sep 18 script.
  - *Applied for now:* Provisional script-only descriptions. Izzy and Rick descriptions come from their sheets. Elsa and Samantha are not included.
  - *Needs:* Approve or complete the bibles; reference sheets for Poochie, Gina, Belle and Tina.
- **F-12 [block_until_bible] (Location)**: No Location Bible for the Moongate Apartments entrance or the Victory Mission.
  - *Applied for now:* Minimal provisional descriptions.
  - *Needs:* Reference photos / bible entries.
- **F-03 [conflict] (Casting)**: PAUL is 23 / 'younger twenties' in the script; the Male Addict #1 bible says 'late 20s to early 30s'. The script also switches between the labels PAUL and MALE ADDICT #1.
  - *Applied for now:* Bible wording kept verbatim (locked).
  - *Needs:* Update the bible age or accept it.
- **F-05 [conflict] (Wardrobe)**: Ruby is 'in her robe', but the bible wardrobe is flannel / denim skirt / boots. Her age is 60 in the script vs 66 in the bible.
  - *Applied for now:* Scene variant uses Source 2 Panel 1: pink robe, barefoot. Age kept at 66 (bible).
  - *Needs:* Approve the robe variant; resolve the age.
- **F-06 [conflict] (Props / Script Supervisor)**: The coffee mug appears only in Ruby's threat line, and she is also smoking. Her curse line to Rick and Tina is garbled ('I'ma blow up the goddamn where son of a bitches at soons I find I out where the fuck its a-').
  - *Applied for now:* Mug established in 1-24 (mug in one hand, cigarette in the other). Placeholder reading used for the garbled line.
  - *Needs:* The clean line.
- **F-07 [conflict] (Casting)**: The Season bible says 'half Cherokee and half Black'; the Sep 18 script says 'full-blooded Cherokee like her mom'. The bible's present-day wardrobe is a waitress uniform, which is not mentioned in the script.
  - *Applied for now:* Bible wording kept verbatim.
  - *Needs:* Which heritage is correct? Is the uniform right for this scene?
- **F-10 [conflict] (Location)**: The Suey Sing geography contradicts itself inside the Location Bible: 'no fence anywhere' vs 'wooden fence + chainlink along its right side'; the field is 'behind' vs 'right of' Suey Sing; tent counts are 7 / 15 / 20.
  - *Applied for now:* The producer's CORRECTED LAYOUT: Moongate on the left, field on the right between Suey Sing and the Victory Mission, no fence in front, 20 tents (Sep 18 script).
  - *Needs:* Lock one layout. Is there a fence on the right side?
- **F-11 [conflict] (Location)**: Dorothy's Place colors: yellow stucco / dark-red trim / green windows (LOCATION 2) vs cream / dark wood / blue windows (corrected prompt). The producer promised the correct photo. The script also names a boarded 'La Puerta Negra' bar that has no bible.
  - *Applied for now:* LOCATION 2 description used.
  - *Needs:* Dorothy's photo; is La Puerta Negra in frame?
- **F-19 [conflict] (Casting)**: The Izzy sheet shows a petite tomboy in a green flannel with no cap. The script says 'wide-shouldered' and a 'boy cut under a 49ers baseball cap'.
  - *Applied for now:* Sheet used (a producer-supplied image outranks script-only text). No cap.
  - *Needs:* Is the 49ers cap in or out? Wide-shouldered or petite?
- **F-20 [conflict] (Casting / Props)**: The Rick sheet reads as late 30s–40s with a bicycle prop. The script says 30WM and has Rick and Tina walking hand in hand.
  - *Applied for now:* Sheet look used. The bike is left out of 1-26 so the hand-in-hand walk works.
  - *Needs:* Should Rick walk his bike (other hand on the handlebars)? Is the age OK?
- **F-01 [decision] (Script Supervisor)**: Two script versions exist. The Sep 18 fountain renames Male Addict #1→PAUL, Santa Cruz→MOODY, Diamond→BELLE, Male/Female Addict #2/#1→RICK/TINA, and adds Killa's pill sale.
  - *Applied for now:* Sep 18 fountain used as canonical.
  - *Needs:* Confirm.
- **F-02 [decision] (Location / Set Designer)**: Script: 'buildings tinted with shades of foil… street paved in a dull stealth-black, cracked foil.' Stylized, not social-realist. Under the CRR rules a departure like this has to be confirmed as intentional.
  - *Applied for now:* Rendered realistically: foil appears as litter (Props Bible). No stylized foil paving.
  - *Needs:* Is the foil-paved world literal (stylized look) or a writer's metaphor?
- **F-14 [decision] (Cinematography)**: The Dynamic Symmetry grid is 2.39:1 but earlier prompts said 16:9.
  - *Applied for now:* Generate at 16:9 and compose inside a centered 2.39:1 safe area (the grid coordinates are for that area). Crop to 2.39:1 in edit.
  - *Needs:* Confirm the delivery aspect.
- **F-15 [decision] (Tone & Lighting)**: No Tone & Lighting Bible exists.
  - *Applied for now:* Lighting drafted three scene-1 lighting states (L1 Blue hour, L2 Intrusion, L3 First light) from the Cinematography Bible. See the Lighting CRR.
  - *Needs:* Approve these as the start of the Tone & Lighting Bible.
- **F-16 [risk] (Prompt Engineer)**: Profanity and drug references in dialogue may trip hosted LTX filters. LTX-2.3 generates dialogue audio from the prompt.
  - *Applied for now:* LTX prompts include the dialogue; Wan prompts are picture-only. Fallback: generate picture without dialogue and add voice in post.
  - *Needs:* Choose native audio vs voice-in-post.
- **F-21 [question] (Location)**: A street photo was received on 2026-09-27 without a label: pink building on the left, parking lot and corrugated-metal warehouse on the right, green-roofed building at the far end.
  - *Applied for now:* Logged, not assigned.
  - *Needs:* Which location is this (Victory Mission end of Soledad? East Rossi?).
- **F-22 [question] (Location / Set Designer)**: The blocking-map site plan assumes Soledad St runs N–S with Moongate, Suey Sing, the field and the Victory Mission on the EAST side, north to south, and Dorothy's across on the WEST. That is inferred from 'Paul heads south past Suey Sing' and the Victory Mission sitting in the 'southern half' of the block.
  - *Applied for now:* 02_bibles/soledad_site_plan.json; all 42 maps drawn on it.
  - *Needs:* Check against the real block. If a side or a direction is wrong, fix the site plan and re-run. Every map regenerates.
- **F-08 [minor] (Casting)**: Sarah is 25 in the bible, 30WF in the script header, and 'late-twenties' in the description. 'Red hair' vs 'strawberry blonde'.
  - *Applied for now:* Bible kept.
  - *Needs:* Confirm the age.
- **F-13 [minor] (Props)**: The G-Wagon color is unspecified. Season's car make and color are unspecified.
  - *Applied for now:* G-Wagon color left open; Season's car is 'an ordinary, well-kept sedan'.
  - *Needs:* Specs.
- **F-17 [minor] (Script Supervisor)**: The OTS note in the script is garbled ('Here the OTS has to be over KILL happenings… La Puerta Negra barA"S right shoulder…').
  - *Applied for now:* Read as an OTS over Killa's right shoulder looking at the southern half of the block (1-18).
  - *Needs:* Confirm.

## Shot status

| Shot | Status | Blockers |
|---|---|---|
| 1-01 | EDITORIAL | audio only |
| 1-02 | BLOCKED | PAUL: no chosen reference image (F-18); SOLEDAD_SUEY_SING: no chosen location reference (F-18) |
| 1-03 | BLOCKED | SARAH: no chosen reference image (F-18); POOCHIE: no chosen reference image (F-18); POOCHIE: Character Bible is provisional (F-09); MOODY: real-person consent not confirmed (F-04); MOODY: sheet supplied but file not committed (F-18); GINA: no chosen reference image (F-18); GINA: Character Bible is provisional (F-09); BELLE: no chosen reference image (F-18); BELLE: Character Bible is provisional (F-09); IZZY: sheet supplied but file not committed (F-18); IZZY: Character Bible is provisional (F-09); SOLEDAD_SUEY_SING: no chosen location reference (F-18) |
| 1-04 | BLOCKED | GINA: no chosen reference image (F-18); GINA: Character Bible is provisional (F-09); SOLEDAD_SUEY_SING: no chosen location reference (F-18) |
| 1-05 | BLOCKED | SOLEDAD_SUEY_SING: no chosen location reference (F-18) |
| 1-06 | BLOCKED | SOLEDAD_SUEY_SING: no chosen location reference (F-18) |
| 1-07 | BLOCKED | PAUL: no chosen reference image (F-18); SOLEDAD_SUEY_SING: no chosen location reference (F-18) |
| 1-08 | BLOCKED | KILLA: no chosen reference image (F-18); DOROTHYS_PLACE: no chosen location reference (F-18) |
| 1-09 | BLOCKED | PAUL: no chosen reference image (F-18); SOLEDAD_SUEY_SING: no chosen location reference (F-18) |
| 1-10 | BLOCKED | KILLA: no chosen reference image (F-18); DOROTHYS_PLACE: no chosen location reference (F-18) |
| 1-11 | BLOCKED | KILLA: no chosen reference image (F-18); DOROTHYS_PLACE: no chosen location reference (F-18) |
| 1-12 | BLOCKED | PAUL: no chosen reference image (F-18); SOLEDAD_SUEY_SING: no chosen location reference (F-18) |
| 1-13 | BLOCKED | PAUL: no chosen reference image (F-18); SOLEDAD_SUEY_SING: no chosen location reference (F-18) |
| 1-14 | BLOCKED | KILLA: no chosen reference image (F-18); PAUL: no chosen reference image (F-18); DOROTHYS_PLACE: no chosen location reference (F-18) |
| 1-15 | BLOCKED | PAUL: no chosen reference image (F-18); DOROTHYS_PLACE: no chosen location reference (F-18) |
| 1-16 | BLOCKED | KILLA: no chosen reference image (F-18); DOROTHYS_PLACE: no chosen location reference (F-18) |
| 1-17 | BLOCKED | KILLA: no chosen reference image (F-18); DOROTHYS_PLACE: no chosen location reference (F-18) |
| 1-18 | BLOCKED | KILLA: no chosen reference image (F-18); VICTORY_MISSION: no chosen location reference (F-18) |
| 1-19 | BLOCKED | VICTORY_MISSION: no chosen location reference (F-18) |
| 1-20 | BLOCKED | VICTORY_MISSION: no chosen location reference (F-18) |
| 1-21 | BLOCKED | SOLEDAD_SUEY_SING: no chosen location reference (F-18) |
| 1-22 | BLOCKED | SOLEDAD_SUEY_SING: no chosen location reference (F-18) |
| 1-23 | BLOCKED | SOLEDAD_SUEY_SING: no chosen location reference (F-18) |
| 1-24 | BLOCKED | RUBY: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-25 | BLOCKED | RUBY: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-26 | BLOCKED | RUBY: no chosen reference image (F-18); RICK: sheet supplied but file not committed (F-18); RICK: Character Bible is provisional (F-09); TINA: no chosen reference image (F-18); TINA: Character Bible is provisional (F-09); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-27 | BLOCKED | RUBY: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-28 | BLOCKED | RICK: sheet supplied but file not committed (F-18); RICK: Character Bible is provisional (F-09); TINA: no chosen reference image (F-18); TINA: Character Bible is provisional (F-09); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-29 | BLOCKED | RUBY: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-30 | BLOCKED | RUBY: no chosen reference image (F-18); RICK: sheet supplied but file not committed (F-18); RICK: Character Bible is provisional (F-09); TINA: no chosen reference image (F-18); TINA: Character Bible is provisional (F-09); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-31 | BLOCKED | RUBY: no chosen reference image (F-18); RICK: sheet supplied but file not committed (F-18); RICK: Character Bible is provisional (F-09); TINA: no chosen reference image (F-18); TINA: Character Bible is provisional (F-09); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-32 | BLOCKED | RUBY: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-33 | BLOCKED | RUBY: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-34 | BLOCKED | SEASON: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-35 | BLOCKED | RUBY: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-36 | BLOCKED | SEASON: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-37 | BLOCKED | RUBY: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-38 | BLOCKED | RUBY: no chosen reference image (F-18); SEASON: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-39 | BLOCKED | SEASON: no chosen reference image (F-18); RUBY: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-40 | BLOCKED | RUBY: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-41 | BLOCKED | SEASON: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-42 | BLOCKED | RUBY: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
| 1-43 | BLOCKED | SEASON: no chosen reference image (F-18); RUBY: no chosen reference image (F-18); MOONGATE_FRONT: no chosen location reference (F-18) |
