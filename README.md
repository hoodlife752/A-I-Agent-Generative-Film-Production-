# A.I. Agent Generative Film Production

Scene runs for the ai-film-agency pre-production pipeline.

## Run a scene

```bash
pip install -r requirements.txt
python3 tools/run_scene.py projects/dances-with-feddie 001
```

A run gates every shot on the Creative Rationale Report rule, compiles Shot Reports, renders a
top-down **scene-blocking map** per shot, and writes three prompt targets per shot:

| Target | Output |
|---|---|
| LTX-2.3 | `prompts/ltx/<shot>.txt`: bible prefixes + scene + dialogue/audio |
| Wan 2.2 | `prompts/wan/<shot>.json`: positive/negative + first/last-frame expression anchors |
| MiniMax Omni | `prompts/omni/<shot>.json`: prompt + up to 9 reference slots; slot 1 is the blocking map |

A shot's prompts stay **BLOCKED** (drafts) until each character and location in it has a locked
reference image in `02_bibles/refs/` and any real-person likeness has documented consent.

## Dances With Feddie: Scene 1 outputs

- `projects/dances-with-feddie/04_qa/scene_001_qa_report.md`: status and producer decision queue (**start here**)
- `projects/dances-with-feddie/03_department_outputs/scene_001/shot_reports.md`: per-shot reports and prompts
- `projects/dances-with-feddie/03_department_outputs/scene_001/blocking_maps/`: 42 blocking-map PNGs
- `projects/dances-with-feddie/03_department_outputs/scene_001/visual_asset_batches.md`: reference-image batch requests
