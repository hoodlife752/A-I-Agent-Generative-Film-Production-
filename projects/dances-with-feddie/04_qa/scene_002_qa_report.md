# Scene 002 — QA / Continuity report

**Shots:** 4 · **Ready to generate:** 3 · **Blocked (draft prompts written):** 0 · **CRR gate failures:** 0 · **Runtime:** ≈0m26s

## CRR gate

All shots passed: every department that touched a shot filed a report.


## Report confidence

| Report | Department | Confidence | Unresolved teamwork |
|---|---|---|---|

## Producer decision queue

Surfaced by the Managing Agent. No agent resolves these on its own.

- **F2-01 [hard_block] (Visual Asset Generation)**: No chosen reference image exists for DANCES or the CHURCH_STOOP. The Scene Blocking Bible's 'First Five' roster lists both as '❌ Missing Source 2'.
  - *Applied for now:* Reference batch prompts drafted (visual_asset_batches.md). A MiniMax TEST pass is possible with just the map and text, but it is not for the cut.
  - *Needs:* Pick a Dances reference and a church plate.
- **F2-02 [decision] (Casting)**: The Dances bible says 'Neck tattoo side placement: CONFIRM before first generation batch'. The Drift Log correction and the Scene Blocking roster both say left side only.
  - *Applied for now:* Left side only, small feather, does not extend past the collarbone, no chest tattoo (the Drift Log's wording).
  - *Needs:* Confirm LEFT and update the bible line.
- **F2-04 [decision] (Props)**: The script adds a torch lighter, which has no Props Bible entry. It also says 'the piece of foil'; the Props Bible's hero foil for this scene is the elongated 4"×16" strip.
  - *Applied for now:* Elongated strip (Props Bible) + a provisional small handheld butane torch lighter.
  - *Needs:* Approve the torch as a Props Bible entry (color/model?).
- **F2-06 [decision] (Editing / Sound)**: Dances' hum has to be the same melody as 'The Feddie Blues' (scene 3 dream). No melody exists yet.
  - *Applied for now:* Hum treated as a separately recorded audio track.
  - *Needs:* The melody (a voice memo is enough).
- **F2-03 [risk] (Location / Props)**: Rendered text is unreliable (Dances Drift Log). The 'Salinas Confucius Church' lettering will probably garble in video.
  - *Applied for now:* The prompt asks for lettering above the door without exact text. The Drift Log's composite workaround is recommended: add the real lettering in post.
  - *Needs:* OK to composite the lettering in post?
- **F2-07 [risk] (Prompt Engineer)**: Drug-use imagery (nodding, foil, torch) may trip MiniMax's hosted content filters.
  - *Applied for now:* Filter-safe wording: no substance names and no 'smoking'. Nodding is described as a drooping, bobbing head.
  - *Needs:* If MiniMax refuses, log it in shared/drift_logs and try the fallback wording in the run sheet.
- **F2-05 [question] (Location)**: The church's street and compass orientation aren't in any bible. The blocking map assumes the church faces west across a street toward the field where Chris stands in scene 7 (corner of East Rossi / Sherwood).
  - *Applied for now:* 02_bibles/church_stoop_site_plan.json
  - *Needs:* Confirm the street name and which way the church faces, or send a reference photo.

## Shot status

| Shot | Status | Blockers |
|---|---|---|
| 2-01 | EDITORIAL | audio only |
| 2-02 | TEST | DANCES: no chosen reference image (F-18); CHURCH_STOOP: no chosen location reference (F-18); F2-01: No chosen reference image exists for DANCES or the CHURCH_STOOP. The Scene Blocking Bible's 'First Five' roster lists both as '❌ Missing Source 2'. |
| 2-03 | TEST | DANCES: no chosen reference image (F-18); CHURCH_STOOP: no chosen location reference (F-18) |
| 2-04 | TEST | DANCES: no chosen reference image (F-18); CHURCH_STOOP: no chosen location reference (F-18) |
