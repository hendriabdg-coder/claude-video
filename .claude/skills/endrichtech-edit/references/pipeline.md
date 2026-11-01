# Pipeline — commands, layout of a job, and machine gotchas

Machine: Windows 11, i3-1115G4, ~8 GB RAM (often <1 GB free), MX350 (no NVENC). Everything runs on CPU.
`SK` below = `D:/Claude Video/.claude/skills/endrichtech-edit`. Run Python/ffmpeg from Git Bash.

## Job folder
```
D:/Claude Video/
  talking-head/mentah/<slug>/klip/        ← Flow clips from the creator (klip_01.mp4 ...)
  talking-head/mentah/<slug>/gabungan.mp4 ← merged take (tools/gabung_klip.py), input once the creator approves it
  talking-head/mentah/<slug>/_assets/     ← optional per-video B-roll (and logo variants), creator-supplied
  talking-head/proyek/<slug>/     ← work folder created by the skill
    look/  assets/  qa/  matte/  renders/
    <slug>.words.json  plan.md  plate.json
    build.py  composite.sh  public/{index.html, plate.mp4, fonts/, vendor/gsap.min.js, hyperframes.json}
  talking-head/aset/broll/  library/logos/  ← reusable B-roll + EndrichTech logo, creator-supplied
  talking-head/hasil/<slug>/<slug>_motion.mp4  ← deliverable (voice only; creator adds SFX/music in CapCut)
  talking-head/hasil/<slug>/CATATAN_CAPCUT_<slug>.md ← notes: SFX cues, music mood, B-roll used/suggested
```
No music or SFX files are used by Claude. Copy the newest working job
(`talking-head/proyek/video01/public/` → `hyperframes.json`, `vendor/`) when creating `public/`; copy fonts from `SK/assets/fonts/`.

## Steps and commands
1. **Transcribe** — `python SK/scripts/transcribe.py "<take>" talking-head/proyek/<slug>/<slug>.words.json <ProductName> ...`
   (≈1–2 min per minute of audio). Look at the LOW-CONFIDENCE list; fix obvious brand/product spellings in the JSON
   (keep timings). Hyphenated words come split ("rata", "-rata") — join them when building lockups.
1b. **Assets** — `python SK/scripts/assets.py "<take>" talking-head/proyek/<slug>/assets` → `assets.json` + `broll_sheet.jpg`
   (3 frames per clip). Choose clips by what the frames show, not only by file name.
2. **Look** — `python SK/scripts/look.py "<take>" talking-head/proyek/<slug>/look` → read the sheets and the grids. Record per shot:
   eyes x/y as a fraction of the source frame, head-top y, chest band y, where the free space is.
3. **Plan** (`plan.md`) — see SKILL.md step 3. Write it to the file; in auto mode do not wait for approval.
4. **Plate** — write `plate.json` (cuts = shot boundaries in seconds = frame/30, eyes per shot, zoom segments, B&W windows,
   `broll` cutaways `{start,end,file,in,anchor,push}` snapped to word boundaries; no split/BEHIND during B-roll)
   → `python SK/scripts/plate.py plate.json` (≈1 min per 10 s on this CPU). Check 3–4 frames of plate.mp4.
5. **Graphics** — write `build.py` → `public/index.html` (start from `SK/scripts/reference/video01_build.py`; swap fonts to
   Inter Display; keep its helpers: `fit()`, `lockup()`, `show/pop/hide/cut`, split in/out, `q()` frame snapping).
   `python build.py` → `bash SK/scripts/hf.sh lint public` → `bash SK/scripts/hf.sh snapshot public --at <t1>,<t2>,...`
   on every beat with graphics → fix → render:
   `bash SK/scripts/hf.sh render public -o "<abs>/renders/overlay.mp4" --fps 30 --low-memory-mode --quiet`
   (≈6–7 min per 55 s — run it in the background with a long timeout).
6. **BEHIND matte** (only if the device is BEHIND) — cut the plate frame range of each beat, then
   `bash SK/scripts/hf.sh remove-background matte/segN.mp4 -o matte/mN.mov --device cpu` (~1 min per 60 frames),
   then overlay only the head region (crop 1080×760 from the top) at the exact frame offset. Template:
   `SK/scripts/reference/video01_composite.sh`. Without BEHIND, copy the overlay render to `<Video Name>_motion.mp4`.
   **Draft first:** `python SK/scripts/matte_fast.py matte/segN.mp4 matte/mN.mov` (MediaPipe, ~15 s per 60 frames
   instead of ~2 min, same ProRes-with-alpha output, so composite.sh is unchanged). Use it to check word placement and
   timing behind the head. Its hair/ear edges are softer (slight halo), so the **final** deliverable always uses
   `remove-background`. Needs `mediapipe` in the system Python (already installed); the model is in `SK/assets/models/`.
   Logo: copy the chosen `library/logos/*.png` into `public/` and place it as the wordmark (style-tokens).
7. **(No SFX/music)** — skip; put the SFX cue list + music mood into the CapCut notes. `sfx.py` is kept only for an explicit request.
8. **QA** — `python SK/scripts/qa.py "<Video Name>_motion.mp4" talking-head/proyek/<slug>/qa` → read the sheets; check the guidebook
   checklist (§78) + stuck text + safe zones + faces never covered. Fix and re-render only what failed.
9. **Deliver** — files listed above; send the final MP4 to the chat (SendUserFile) and copy it to
   `%USERPROFILE%/OneDrive/Videos/EndrichTech/` so the creator can check it on the phone.

## Gotchas (all hit before — do not rediscover)
- HF downloads stall on Xet → `HF_HUB_DISABLE_XET=1` (set inside transcribe.py). Use `large-v3-turbo`, not large-v3.
- faster-whisper `decode_audio` crashes (`metadata_errors`) → pass a numpy array (transcribe.py does).
- ffmpeg `drawtext` segfaults (no fontconfig) → never use drawtext; all text is rendered in HyperFrames.
- Git Bash mangles Windows paths inside ffmpeg filter arguments → use relative paths in filters.
- The safety check blocks `rm` of globs after `cd` → write temp/QA frames into fresh folders instead of clearing.
- HyperFrames lint rejects tweening `top`/`height` → move the video wrapper with transform `y`.
- Duplicate element ids silently break GSAP selectors → prefix generated ids per family (`cap…`, `seam…`, `p2-…`).
- A pop tween that outlasts a later `tl.set(opacity 0)` leaves the word stuck on screen when seeking → clamp duration to (hide − show − 1 frame).
- CSS `.q span` also hits nested spans → use child selectors (`> span`).
- Every BEHIND word needs an explicit hide, or it reappears after a covering card ends.
- No wrapper moves (split/zoom on `#video-wrap`) during BEHIND windows, or the matte will not line up.
- Plugin CLI is `node …/plugin-cli.mjs` (use `hf.sh`), not `npx hyperframes`.
- PowerPoint COM / LibreOffice are not part of this pipeline.
