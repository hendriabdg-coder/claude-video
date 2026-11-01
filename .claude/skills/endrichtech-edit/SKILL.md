---
name: endrichtech-edit
description: Fully automatic edit of an EndrichTech talking-head take into a finished 9:16 short with kinetic text, plate zooms, split-screen diagrams, the creator's B-roll and logo, one dramatic device and CapCut notes (SFX/music suggestions), following the creator's guidebook. Use when the user drops/points to a video and types "editkan" (or "edit video ini", "edit sesuai guidebook", "/endrichtech-edit"). Not for PowerPoint decks or for plain subtitles.
---

# EndrichTech auto-edit

The creator's take is `D:/Claude Video/talking-head/mentah/<slug>/gabungan.mp4` — Flow clips merged with
`tools/gabung_klip.py` and **approved by the creator** (CLAUDE.md section 13; never start motion on an unapproved merge) —
or a single take they point to. They type **editkan**. Run the whole pipeline without
asking for plan approval and hand back a finished video. Talk to the creator in casual Bahasa Indonesia ("bro").

Read before starting (in this order):
1. `references/style-tokens.md` — concrete values + the **owner decisions that override the guidebook**.
2. `references/guidebook.md` — the creative constitution (philosophy, decision engine §44–46, QA §78).
3. `references/pipeline.md` — commands, job folder layout, machine gotchas.
Reference implementation of a finished job: `scripts/reference/video01_*` (approved by the creator).

## Inputs
- The take: path given by the user, else the newest approved `talking-head/mentah/<slug>/gabungan.mp4`.
  If `mentah/<slug>/klip/` exists but there is no approved `gabungan.mp4`, merge first, send it, and stop for approval.
- Creator assets (optional): reusable `D:/Claude Video/talking-head/aset/broll/` + `library/logos/`, and per-video
  `talking-head/mentah/<slug>/_assets/` (old takes: `<Name>_assets/` next to the take). Only B-roll and logos — **no music, no SFX** (the creator adds those in CapCut).
  Never invent stand-ins for real logos, real articles or real UIs.
- Slug = the `mentah/<slug>/` folder name (`YYYY-MM-DD-topik`). Work in `D:/Claude Video/talking-head/proyek/<slug>/`; deliverables go to `talking-head/hasil/<slug>/`.

## Stop only for blockers (otherwise never ask)
- A brand/product/person name in the transcript is uncertain and is going on screen → ask with the candidates.
- The creator refers to an asset that is not there ("pakai screenshot artikelnya") → ask once, or proceed without it and say so.
- The take is not a talking-head video (e.g. pure screen recording) → say the skill doesn't fit and propose an approach.
Everything else: decide using the guidebook decision rule (Clarity > Story > Human > Evidence > Visual interest > Decoration).

## Workflow (run end to end; long renders in the background)
0. **Style** — TH motion style is being re-tested (CLAUDE.md section 13): until a style is recorded there, make 2–3 ~10 s
   variants first, send them in chat and wait for the creator's pick.
1. **Transcribe** — `scripts/transcribe.py`. Fix confident spelling issues (EndrichTech, product names) in the JSON.
   **Assets** — `scripts/assets.py "<take>" talking-head/proyek/<slug>/assets` → look at `broll_sheet.jpg` to see what each clip shows.
2. **Look** — `scripts/look.py`. Measure per shot: eyes x/y (fraction of source), head-top y, free side. Detect jump cuts.
3. **Plan** — write `plan.md` in the job folder:
   - Content mode (A Story / B Evidence / C Product) and the **one dramatic device** chosen by theme (style-tokens table).
   - Beat table: `start–end | words | class (Human/Concept/Evidence/Demo/Transition) | intensity 1–4 | scene (FULL/SPLIT/CARD/BEHIND/BROLL) | on-screen text (L1/L2/tone) | graphic | zoom | sfx suggestion`.
   - B-roll only where it adds meaning (guidebook §23 + B-roll rules in style-tokens); no B-roll beats an unrelated one.
   - Check the plan: ~70–80% of spoken beats carry text; 20–30% text-free on purpose; a meaningful change every ~1.5–3.5 s
     (hook 0.8–2 s); max 2 full-screen cards; device used 1–2×; creator returns after every SPLIT/CARD; hook in the first 1 s,
     no logo intro; CTA = creator + one short line (+ optional FOLLOW pill).
4. **Plate** — `plate.json` → `scripts/plate.py` (zoom segments, punch-ins on key words, B-roll cutaways in `broll`, B&W only
   if that is the device).
5. **Graphics** — `build.py` (adapt `scripts/reference/video01_build.py`; Inter Display fonts from `assets/fonts/` copied to
   `public/fonts/`) → lint → snapshot every graphic beat and look at the images → fix → render `--low-memory-mode`.
6. **BEHIND matte** — only if that device was chosen (pipeline step 6). Check placement with the fast draft matte
   (`scripts/matte_fast.py`), then make the final matte with `remove-background`.
7. **No SFX / music** — the creator adds them in CapCut. Put the SFX cue list and a music mood in the CapCut notes instead
   (`scripts/sfx.py` stays available only if the creator explicitly asks for SFX again).
8. **QA** — `scripts/qa.py`; review sheets against guidebook §78 + safe zones + face never covered + no stuck text.
   Fix and re-render only what failed (max 2 fix rounds, then report what remains).
9. **Deliver** — see below.

## Deliverables
- `D:/Claude Video/talking-head/hasil/<slug>/<slug>_motion.mp4` (final, voice only — no SFX, no music).
- `D:/Claude Video/talking-head/hasil/<slug>/CATATAN_CAPCUT_<slug>.md` in Indonesian: (1) **SFX cue table** `detik | SFX | kenapa` using the SFX map in
  style-tokens, (2) **music**: mood/tempo + where to duck, (3) which B-roll clips were used where + where extra B-roll /
  screen recordings / source screenshots would help, (4) what was left as `CONTOH ILUSTRASI`, (5) safe-zone reminders. Never add subtitles — the creator chose kinetic text only.
- Send the final MP4 with SendUserFile and copy it to `%USERPROFILE%/OneDrive/Videos/EndrichTech/` (the creator checks on the phone).
- Final chat message (Indonesian, short): content mode, chosen dramatic device and why, B-roll/logo used, duration, what
  was skipped or flagged for CapCut, anything uncertain.
