# EndrichTech style tokens (concrete values)

The guidebook (`guidebook.md`) says *why*; this file says *exactly what*. Where they disagree, the
**Owner decisions** below win (set by the creator on 2026-10-06).

## Owner decisions (override the guidebook)

| Topic | Decision |
|---|---|
| Accent colors | Keep the approved set: yellow, red, green on a neutral base (not "1–2 accents"). Still: max 2 accents visible in one frame. |
| Text coverage | **No subtitles.** Kinetic text is the only text layer, so it carries comprehension: about **70–80% of spoken beats get on-screen text** (keyword/phrase lockups that summarise, never a full transcript). The other 20–30% stay text-free on purpose (human/emotional moments, payoff pauses, beats where a graphic already says it). |
| Word-by-word reveal | Allowed inside lockups (words appear at their spoken start), but the lockup holds 2–7 chosen words, not every word spoken. |
| Full-screen text cards | Rare: max 1 per 30 s, max 2 per video. Only for a shocking number, contradiction, chapter turn or payoff. |
| Dramatic device | **Hybrid — pick ONE per video by theme** (see table below), use it 1–2×. Never stack two devices in one video unless it is longer than 90 s. |
| Font | Inter Display (Apple-style SF Pro look-alike, OFL). One family per video. SF Pro itself is licensed for Apple platforms only — do not use it. Geist/Manrope are allowed alternates if their files are added to `assets/fonts/`. |
| Mode | `editkan` = fully automatic, no plan approval. Stop only for blockers (see SKILL.md). |
| Audio | **Claude adds no SFX and no music** — the creator does it in CapCut. Claude writes the SFX cue list + music mood in the CapCut notes. |
| Assets | Claude uses only the creator's **B-roll and logo** (`talking-head/aset/broll/`, `library/logos/` + `mentah/<slug>/_assets/`). |

### Dramatic device by theme
| Theme of the video | Device | What it looks like |
|---|---|---|
| Product / brand / a name is the hero ("ChatGPT", "KAMU") | **BEHIND** | Giant word (300–400 px) behind the head, subject matte on top |
| Warning, risk, serious turn ("tapi hati-hati…") | **B&W punch-in** | B&W + contrast 1.12 + zoom +0.15 for the line, back to color after |
| Shocking number / loss / contradiction | **CARD** | Hard-cut full-screen red `#E5243B` card with one number/phrase |
| Calm explainer / tutorial | **none** | Rely on SPLIT diagrams and punch-ins only |

## Canvas & safe zones (1080 × 1920, 30 fps)
- Essential content inside x 60–940 (right edge 140 px free for platform buttons), y 220–1540.
- Top 0–220: no text (platform header). Bottom 1540–1920: only the wordmark at 1640; nothing essential.
- Face anchor: measured per shot from `look.py` grids (eyes y ≈ 640–720 after plate zoom). All text positions are relative to it.

## Layout zones (relative to a face with eyes ≈ y 680, head-top ≈ y 430)
| Zone | y range | Use |
|---|---|---|
| Above head | 80–420 | accent: big number, icon, pill, "?" badge, BEHIND word (top ≈ 175–240) |
| Chest band | 1040–1440 (lockup box top 1060, h 400) | caption lockups |
| Seam (SPLIT only) | top ≈ 846 | single-word captions on the panel shade |
| Wordmark | 1640 | logo from `library/logos/` if present (PNG with alpha, height 56–64 px, centered, opacity .9; light variant on dark scenes), else text `Endrich**Tech**` (Tech in yellow), 40 px, opacity .92 — whole video, hidden on CARD scenes |

If the creator sits left/right of center, move lockups and graphics to the free side (guidebook §13) instead of centering.

## Typography (Inter Display, files in `assets/fonts/`)
| Level | Face | Size (px, fit to 960 px width) | Color | Use |
|---|---|---|---|---|
| Hero keyword (L1) | InterDisplay-Black | 120–140, letter-spacing −0.03em | yellow (or white/red by meaning) | 1–5 words |
| Supporting line (L2) | InterDisplay-SemiBold | 50–58 | white `#F6F5F1` | 5–12 words, above the hero |
| Tone word | InterDisplay-SemiBoldItalic | 96–104 | white or yellow | emotional/ironic word ("mungkin", "padahal") |
| Metadata (L3) | InterDisplay-Medium | 28–34, letter-spacing .12em, uppercase | white 60% | source, date, "CONTOH ILUSTRASI", "PARAFRASE" |
| Seam word | InterDisplay-Black | 76 | white / yellow for highlight | SPLIT only |
| BEHIND word | InterDisplay-Black | 300–400 | red or yellow + glow | dramatic device |

Lowercase captions except names and acronyms (EndrichTech, ChatGPT, OpenAI, AI). No paragraphs, ever. Text shadow
`0 4px 18px rgba(0,0,0,.75)`; hero gets a soft glow of its own color (`0 0 34px` at 45%).
Measure every line with PIL `ImageFont.truetype(...).getlength()` and shrink until it fits 960 px.

## Colors
| Token | Hex | Meaning |
|---|---|---|
| white | `#F6F5F1` | default text |
| yellow | `#FFD60A` | key word, highlight, positive emphasis |
| red | `#FF3B4E` (text) / `#E5243B` (card) | danger, loss, wrong |
| green | `#3BE07F` | safe, correct, solved |
| ink | `#0B0D10` | panels, dark cards; black card `#070708` |
| panel glass | `rgba(255,255,255,.07)` + 2 px border `rgba(255,255,255,.16)` | tiles, chips, cards |

## Scene types
- **FULL** — face full-bleed, lockup on the chest, optional accent above the head. Default scene.
- **SPLIT** — top panel ≈1010 px: solid `#0b0d10` to 780 px then gradient to transparent by 1010 px, 60 px grid masked out before the fade, video moved down with GSAP `y: 520` (transform, never `top`). **No seam line.** Panel holds one idea: diagram, list, chat mock, quote card, simplified chart. Seam words at top ≈ 846.
- **CARD** — full-screen color card (red for shock, black for teaser/CTA). Hard cut in/out. Rare (see decisions).
- **BEHIND** — see dramatic devices.
Rotate scene types so a meaningful visual change happens every ~1.5–3.5 s (hook 0.8–2 s).

## Motion (GSAP, one paused timeline, times snapped to 1/30 s)
| Event | Values |
|---|---|
| Text entrance | opacity 0→1, y 26→0, scale .92→1, blur 10→0 px, 0.22–0.30 s, `power3.out` |
| Editorial reveal | 0.30–0.45 s, `power3.out`; panels/split `power3.inOut` 0.42 s |
| Exit | 0.12–0.15 s, `power2.in` |
| Pop (icons, badges, chips) | scale .6→1, 0.28–0.35 s, `back.out(2)` — icons only, never body text |
| Emphasis scale | 85%→105%→100% only on the 1–2 biggest moments |
| Max per scene | 1 primary motion + 1 secondary |
Never rotate text randomly, no glitch transitions, no particles. Hard cuts carry 80–90% of changes.

## Camera / plate zoom (`plate.py`)
- Normal talk: 1.00–1.05 slow drift. Important line: punch-in +0.06–0.10. Strong conclusion: +0.12–0.15. Tension: slow push +0.08 over the beat. Max 1.18.
- Hook: pull-back 1.14→1.04 in the first second.
- Punch-ins are hard zoom jumps aligned to the word or to a camera cut; never zoom in/out every sentence.

## B-roll (scene type BROLL)
- Use only when it shows the thing being said, makes an abstract idea concrete, or hides a disruptive jump cut (guidebook §23, §48). A keyword match alone is not enough.
- 1.2–3.0 s per cutaway (hook 0.8–1.5 s); max ~25% of the video; always return to the creator afterwards; max 2 clips in a row.
- Cut in/out on a word boundary or a camera cut; hard cut by default; slow push 1.00→1.06 inside the clip.
- Kinetic text may sit on B-roll (chest band), L1/L2 only — no SPLIT panel or BEHIND over B-roll.
- Horizontal clips are cropped to 9:16 with `anchor` on the subject; below 4K use them briefly or skip.
- Prefer per-video clips (`mentah/<slug>/_assets/`) over library clips; never reuse a clip twice in one video.

## Logo
- Small and restrained (guidebook §41): no logo intro, no logo animation at the start. Optionally a slightly larger logo on the final CTA beat only.

## Audio (for the CapCut notes — Claude does not mix audio)
- Voice first. Final integrated loudness about −14 LUFS, true peak ≤ −1 dB (`alimiter=limit=0.95` in `sfx.py`).
- SFX level guide to suggest: impacts −17…−19 dB (≥3–5 dB under voice RMS where speech overlaps), whoosh −14…−15, pop −14…−16, click/typing −17…−21, chime/ping −13…−17.
- SFX map: whoosh → split in/out and big cuts; pop → each list item / icon; impact → BEHIND word, CARD in; glitch → B&W beat; chime/ping → positive reveal; error → "?" badge; typing/click → UI mock. Not every animation gets a sound (guidebook §35).
- Music suggestion: mood + tempo; duck about −20…−25 dB under the voice, dip further on payoff lines.

## Content honesty
Visualize claims exactly as spoken. Never fabricate screenshots of real publications or fake UIs of real brands. Paraphrased
quotes get a `PARAFRASE` label; illustrative numbers/UI get `CONTOH ILUSTRASI`. Real logos, B-roll, screen recordings and
source screenshots come from the creator's asset folders or go into the CapCut notes.
