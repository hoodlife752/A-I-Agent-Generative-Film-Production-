# Scene 2 · Dances nodding on the church steps · MiniMax test run

> **TEST RUN**: protocol skipped at the producer's request. For seeing what MiniMax does, not for the cut.

## Where to run it

MiniMax is a hosted web service. You don't need a pod or ComfyUI. Open MiniMax's video site
(**Hailuo AI**, `hailuoai.video`) in a browser, sign in, and use the video mode that accepts
**reference images** (the multi-reference / "Omni" mode, up to 9 images). Screen names change;
look for "reference", "subject" or "multi-image".

## Files to upload (download them from this folder)

| Slot | File | What it is |
|---|---|---|
| 1 | `blocking_maps/2-02_blocking_map.png` (or 2-03 / 2-04) | Top-down staging for that shot |
| 2 | **Dances still** (make it in Step 1) | Her identity |
| 3 | optional: a photo of the real Confucius Church | The location |

## Step 1: make a Dances still (1 minute)

Dances has no reference image yet, and video models need a face to hold on to. In MiniMax's
**image** mode (or any image generator you like), paste:

```text
Photoreal portrait, soft dawn light, neutral background. 22-year-old woman, mixed Cherokee and Black heritage, warm brown skin, high cheekbones, dark almond eyes, hard unimpressed expression, thick dark hair in two thick braids, tribal tattoos on both arms (geometric Cherokee patterns, feathers, arrows), a small feather tattoo on the LEFT side of her neck only that does not extend past the collarbone, no facial tattoos, no chest tattoo. Worn brown leather jacket, gray tank top, dark jeans, scuffed boots, layered bracelets, small hoop earrings. Lean athletic build.
```

Make 4–5 and **pick the one that's Dances**. Save it; you'll reuse it for every shot.

## Step 2: run the shots

For each shot, upload the files in the slot order above, then paste the prompt.

### Shot 2-02 · the zoom in (10s)

```text
Image 1 is a top-down blocking map: follow its layout and the camera arrow, but do not show the map. Image 2 is the woman.
Dawn. Across a quiet street, the woman from Image 2 sits alone on the top step of an ornate Chinese-style church with a red-tiled roof, red trim, tan stucco walls and a columned entrance with dark wooden double doors. She is bent all the way forward at the waist, head drooping and slowly bobbing, drifting in and out, otherwise completely still. A small blue tent with a blue tarp sits on the left of the steps; a light tan tent with no tarp sits on the right. A worn blanket and backpack rest beside the doors. The camera slowly zooms in from across the street, steady, no shake. As it closes in, a long flat strip of foil and a small torch lighter become visible on the step by her boots. First sunlight warms the roof tiles; she and the steps stay in cool blue shade. Photoreal, cinematic, widescreen, gritty but tender, no text.
```

### Shot 2-03 · low close-up (6s)

```text
Image 1 is a top-down blocking map: follow it, but do not show the map. Image 2 is the woman.
Low angle close-up from the lower steps looking up at the woman from Image 2, framed from the neck up as she hangs forward on the top step of the church. Her eyes are half-closed and heavy, her lips twisted as if it hurts her to hum. A thin glistening string of saliva hangs from her chin. Behind and above her: the top of the columned entrance and the church's name lettering, warm in the first sun, while her face stays in cool blue shade. The camera holds still and lingers. Photoreal, cinematic, widescreen, intimate, no readable text.
```

### Shot 2-04 · tilt down to the foil (6s)

```text
Image 1 is a top-down blocking map: follow it, but do not show the map. Image 2 is the woman.
Close-up of the chin of the woman from Image 2 as she hangs forward on the church steps. The camera tilts slowly down, following a glistening string of saliva from her chin to the concrete step, where a drop lands on a small torch lighter lying on its side and rolls off onto a long, flat strip of foil. The foil catches the early light along its length, the only bright thing in the frame. At the edge of the step, a small curled photograph is half-tucked under the concrete. Photoreal, cinematic, widescreen, quiet and sad, no text.
```

## If something goes wrong

| What happens | Try |
|---|---|
| The map shows up in the video | Drop the map and keep only the Dances still. The map still guides your framing choices. |
| Refused for content | Remove "foil" and "torch lighter" from the prompt and run again. Note which words were refused. |
| Tattoo spreads to her chest / both sides | Add: "feather tattoo on the left side of the neck only, no chest tattoo" |
| Church lettering is garbled | Expected. The real lettering gets composited in post (F2-03). |
| She looks different in each shot | Always reuse the same Dances still; for 2-03/2-04 you can also add the last frame of the previous shot as an extra reference. |

Send me what comes back (screenshots or notes on what looked wrong) and I'll log it in the drift
log and tighten the prompts.

## Running it from here instead

If you'd rather I run MiniMax directly: create an API key on MiniMax's developer platform, add
it to this cloud environment as `MINIMAX_API_KEY`, and allow MiniMax's API domain under the
environment's network settings. Then I can submit the shots and pull the videos back
into the repo.
