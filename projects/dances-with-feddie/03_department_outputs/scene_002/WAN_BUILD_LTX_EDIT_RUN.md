# Scene 2 · Build with Wan 2.2, edit with LTX-2.5

> **TEST RUN**: protocol skipped. For trying the two-model workflow, not for the cut.

| Pass | Model | Does |
|---|---|---|
| **Build** | Wan 2.2 14B (image-to-video, first/last frame) | Picture: Dances, the steps, the camera move |
| **Edit** | LTX-2.5 + LTX 2.5 Director | The hum (Wan makes no audio), extending 2-02 to its full 10s, stitching 2-02→2-04, 2× upscale |

## 1. Create the pod (RunPod website)

| Setting | Value | Why |
|---|---|---|
| GPU | **48 GB**: L40S, RTX 6000 Ada, or RTX A6000 | LTX-2.5 needs 32 GB+; 48 GB runs the fp8 model fully on the card. Both models fit, one at a time. |
| Template | RunPod PyTorch (CUDA 12.x) | |
| Network volume | **New, 200 GB** | Wan 2.2 + LTX-2.5 weights ≈ 100–120 GB. Your old 50 GB volume is too small. |
| Container disk | 30 GB | |
| Exposed HTTP port | **8188** | ComfyUI |

Stop the pod when you're not using it. The volume keeps everything; you pay for GPU time only while it runs.

## 2. One-time setup (pod → Connect → Web Terminal)

```bash
cd /workspace
git clone https://github.com/hoodlife752/A-I-Agent-Generative-Film-Production- film
cd film && git checkout claude/dances-with-feddie-scene-eeqbfl
export HF_TOKEN=hf_...        # huggingface.co → Settings → Access Tokens (read)
bash tools/pod/setup_pod.sh   # 30–60 min, mostly downloads
```

- If the repo is private, `git clone` asks for a username and password. Use your GitHub username and a GitHub access token as the password.
- If the Gemma text encoder is gated, open its Hugging Face page once and click "accept" with the same account as the token.
- The script prints which model file it picked for each role. If anything says "not found", send me that output.

## 3. Start ComfyUI (after every pod restart)

```bash
bash /workspace/film/tools/pod/start_comfyui.sh
```

Open it: RunPod → your pod → Connect → **HTTP 8188**.

## 4. Build pass: Wan 2.2

Use ComfyUI's built-in templates (**Workflow → Browse Templates → Video → Wan 2.2**). The model
loaders will list the files the setup script downloaded.

**a. Make the Dances still (T2V template, length = 1 frame, 1280×720).** Paste as the prompt:

```text
Photoreal, soft dawn light. Across a quiet street, a 22-year-old woman of mixed Cherokee and Black heritage, warm brown skin, high cheekbones, thick dark hair in two thick braids, worn brown leather jacket, gray tank top, dark jeans, scuffed boots, tribal tattoos on both arms, small feather tattoo on the left side of her neck only, sits alone on the top step of an ornate church with a red-tiled roof, red trim, tan stucco walls and a columned entrance with dark wooden double doors. She is bent all the way forward at the waist, head drooping. A small blue tent with a blue tarp on the left of the steps, a light tan tent on the right. Wide shot, first sun on the roof tiles, the steps in cool blue shade.
```

Run 4–5 seeds and pick the one that's her. That frame is the first frame of 2-02.

**b. Shots (I2V template, 1280×720, 81 frames @ 16 fps = 5s).** Prompt and negative prompt for
each shot are in `prompts/wan/2-02.json`, `2-03.json` and `2-04.json` (`positive` / `negative`).

| Shot | Start image | Note |
|---|---|---|
| 2-02 zoom in | the Dances still from (a) | 10s in the script. Wan makes 5s; LTX extends it in the edit pass |
| 2-03 low close-up | last frame of 2-02 | Use the First/Last-Frame template if you want to pin the end frame too |
| 2-04 tilt down | last frame of 2-03 | |

Save each clip; they land in `/workspace/renders`.

## 5. Edit pass: LTX 2.5 Director

1. Load the three Wan clips onto the Director's timeline video track in order.
2. **Audio**: Dances' broken, off-key mumble-hum, pained, close and dry, fading out on 2-04.
   The hum should be the melody of "The Feddie Blues". Until that exists, describe it (F2-06).
3. **Extend 2-02** from 5s to 10s: pin its last frame, prompt the continued zoom.
4. Render with the 2× spatial upscaler.

The 2.5 Director hides its reference-image features (2.5 wasn't trained for them). Identity
carries through the Wan frames and keyframes instead. Its exact controls weren't verifiable
before install. If a step above doesn't match what you see, screenshot it to me.

## 6. Bring the results back

Download from ComfyUI's output (or `/workspace/renders`) and send them here. I'll log what
worked and what drifted and tighten the prompts.
