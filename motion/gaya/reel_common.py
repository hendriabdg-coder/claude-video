# Shared bits for full reels built under CLAUDE.md (25-35 s, VO from output/motion/<slug>/vo/vo-full.*, chibi CTA, IG safe
# area). Each motion/proyek/<slug>/build.py imports this: setup() copies fonts/vendor/poses + pads the VO, words() gives the
# word timeline, chibi_*() give the presenter with VO-driven lip-flap, page() wraps CSS/HTML/JS into the composition.
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
W, H, FPS = 1080, 1920, 30
VO_START = 0.2          # VO starts almost immediately: the hook moves from frame 0
TAIL = 0.9              # hold after the last word (comment question stays readable; QC: keep tails short)
SAFE_TOP, SAFE_BOTTOM, BRAND_Y = 250, 1570, 1525


def setup(here, slug):
    """Copy shared assets into here/public and write a VO padded to the composition length. Returns DUR."""
    pub = here / "public"
    pub.mkdir(parents=True, exist_ok=True)
    (here / "renders").mkdir(exist_ok=True)
    src = ROOT / "motion" / "gaya" / "gaya-terminal" / "public"
    for d in ("fonts", "vendor"):
        if not (pub / d).exists():
            shutil.copytree(src / d, pub / d)
    if not (pub / "hyperframes.json").exists():
        shutil.copy(src / "hyperframes.json", pub / "hyperframes.json")
    if not (pub / "pose").exists():
        shutil.copytree(ROOT / "karakter" / "pose_fix", pub / "pose")
    vo = ROOT / "output" / "motion" / slug / "vo"
    dur = round(json.loads((vo / "vo-full.json").read_text(encoding="utf-8"))["duration"] + VO_START + TAIL, 2)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vo / "vo-full.mp3"), "-af",
                    f"adelay={int(VO_START * 1000)}:all=1,apad,atrim=0:{dur}", "-ar", "44100", str(pub / "vo.mp3")], check=True)
    return dur


def words(slug):
    d = json.loads((ROOT / "output" / "motion" / slug / "vo" / "vo-full.json").read_text(encoding="utf-8"))
    return {i: round(w["start"] + VO_START, 3) for i, w in enumerate(d["words"])}


# ---------------------------------------------------------------- chibi presenter (lip-flap from VO loudness)
POSES = ["netral", "lambai", "tunjuk", "mikir", "kaget", "keren", "bicara", "kedip"]


def chibi_track(here, t0, t1, emph, blinks=()):
    """Pose events between t0 and t1. emph = [(t, pose)], 'netral' segments talk (netral/bicara) when the VO is loud."""
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(here / "public" / "vo.mp3"), "-ac", "1", "-ar", "48000",
                                   "-f", "s16le", "-"])
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = 48000 // FPS
    db = np.array([20 * np.log10(np.sqrt((x[i:i + hop] ** 2).mean()) + 1e-9) for i in range(0, len(x) - hop, hop)])
    sm = np.convolve(db, np.ones(7) / 7, mode="same")
    open_ = (db > db.max() - 22) & (db >= sm - 1.0)
    emph = sorted([(t0, "netral")] + list(emph))
    track, prev, hold = [], None, 0
    for f in range(int(t0 * FPS), int(t1 * FPS)):
        t = f / FPS
        cand = [q for s, q in emph if s <= t + 1e-6]
        p = cand[-1] if cand else "netral"   # first frame can sit a hair before t0
        if p == "netral":
            want = "bicara" if open_[min(f, len(open_) - 1)] else "netral"
            if prev in ("netral", "bicara") and want != prev and hold < 2:
                want = prev
            if any(b <= t < b + 0.13 for b in blinks):
                want = "kedip"
            p = want
        hold = hold + 1 if p == prev else 1
        if p != prev:
            track.append([round(t, 3), p])
        prev = p
    return track, [round(t, 3) for t, p in emph[1:] if p != "netral"]


CHIBI_CSS = '''
#chibi { position: absolute; width: 520px; height: 925px; opacity: 0; transform-origin: 50% 100%; }
#chibiS { position: absolute; inset: 0; }
#chibiS img { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; }
#chibiSh { position: absolute; width: 360px; height: 46px; border-radius: 50%; background: rgba(0,0,0,.45); filter: blur(14px); opacity: 0; }
'''


def chibi_html(left=305, top=650, w=470):
    """Default: 470 px wide, feet at ~y 1440 so the watermark (y 1525) stays clear."""
    h = round(w * 1680 / 944)
    imgs = "".join(f'<img id="cp_{p}" src="pose/pose_{i}_{p}.png">' for i, p in enumerate(POSES))
    return (f'<div id="chibiSh" style="left:{left + w * 0.16:.0f}px;top:{top + h * 0.83:.0f}px;width:{w * 0.7:.0f}px"></div>'
            f'<div id="chibi" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px"><div id="chibiS">{imgs}</div></div>')


# ---------------------------------------------------------------- animated chibi (looping 4 s clips, keyed WebM alpha)
ANIM_DIR = ROOT / "karakter" / "anim_alpha"   # made by tools/key_anim.py from karakter/Animasi Karakter


def chibi_anim_html(here, clips, left=305, top=650, w=470):
    """clips = [(name, t_start, t_end)], back to back. Each clip is a 4 s WebM; segments longer than 4 s get
    another copy of the clip. Copies the WebMs into public/anim. Returns HTML."""
    h = round(w * 1280 / 720)
    (here / "public" / "anim").mkdir(parents=True, exist_ok=True)
    vids, k = [], 0
    for name, t0, t1 in clips:
        shutil.copy(ANIM_DIR / f"{name}.webm", here / "public" / "anim" / f"{name}.webm")
        t = t0
        while t < t1 - 0.05:
            d = round(min(4.0, t1 - t), 3)
            vids.append(f'<video id="cv{k}" class="cva" src="anim/{name}.webm" data-start="{round(t, 3)}" data-duration="{d}" '
                        f'data-track-index="{1 + k % 2}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;opacity:0"></video>')
            k += 1
            t += d
    return (f'<div id="chibiSh" style="left:{left + w * 0.16:.0f}px;top:{top + h * 0.86:.0f}px;width:{w * 0.7:.0f}px"></div>'
            f'<div id="chibi" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px">{"".join(vids)}</div>')


def chibi_anim_js(t_in):
    """Show each clip only inside its window (seek-safe sets) + slide-in entrance."""
    return f'''
    document.querySelectorAll(".cva").forEach(function (v) {{
      var s = parseFloat(v.dataset.start), d = parseFloat(v.dataset.duration);
      tl.set(v, {{ opacity: 1 }}, q(s)); tl.set(v, {{ opacity: 0 }}, q(s + d));
    }});
    tl.fromTo("#chibi", {{ y: 700, opacity: 1 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, q({t_in}));
    tl.fromTo("#chibiSh", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, q({t_in} + 0.2));
'''


def fitpx(text, px, maxw=760, font="InterDisplay-Black.ttf", spacing=0.02):
    """Largest font size <= px at which one line of text fits maxw (keeps headlines inside the IG safe area)."""
    from PIL import ImageFont
    path = str(ROOT / "motion" / "gaya" / "gaya-terminal" / "public" / "fonts" / font)
    while px > 30 and ImageFont.truetype(path, px).getlength(text) + len(text) * px * spacing > maxw:
        px -= 2
    return px


def chibi_js(track, emph_t, t_in, t_out=None):
    out = "" if t_out is None else f'''
    tl.to("#chibi", {{ y: 700, opacity: 0, duration: 0.35, ease: "power2.in" }}, q({t_out}));
    cut("#chibiSh", {t_out}, 0);'''
    span = (t_out if t_out is not None else t_in + 14) - t_in
    bob = max(int(span / 1.2), 1)   # one bob cycle = 1.2 s (0.6 s up + 0.6 s down)
    return f'''
    var CTRACK = {json.dumps(track)}, CEMPH = {json.dumps(emph_t)};
    CTRACK.forEach(function (e) {{ tl.set("#chibiS img:not(#cp_" + e[1] + ")", {{ opacity: 0 }}, q(e[0])); tl.set("#cp_" + e[1], {{ opacity: 1 }}, q(e[0])); }});
    tl.fromTo("#chibi", {{ y: 700, opacity: 1 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }}, q({t_in}));
    tl.fromTo("#chibiSh", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, q({t_in} + 0.2));
    tl.fromTo("#chibiS", {{ y: 0 }}, {{ y: -10, duration: 0.6, yoyo: true, repeat: {bob * 2 - 1}, ease: "sine.inOut" }}, q({t_in} + 0.5));
    CEMPH.forEach(function (t) {{ tl.fromTo("#chibi", {{ scaleY: 0.94, scaleX: 1.04 }}, Object.assign({{ scaleY: 1, scaleX: 1, duration: 0.35, ease: "back.out(3)" }}, NI), q(t)); }});{out}
'''


# ---------------------------------------------------------------- page
FONTS = '''@font-face { font-family: "IDBlack"; src: url("fonts/InterDisplay-Black.ttf") format("truetype"); font-display: block; }
@font-face { font-family: "IDBold"; src: url("fonts/InterDisplay-Bold.ttf") format("truetype"); font-display: block; }
@font-face { font-family: "IDSemi"; src: url("fonts/InterDisplay-SemiBold.ttf") format("truetype"); font-display: block; }
@font-face { font-family: "IDItal"; src: url("fonts/InterDisplay-SemiBoldItalic.ttf") format("truetype"); font-display: block; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow: hidden; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; }
.ico { width: 100%; height: 100%; display: block; }'''

JS_HELPERS = '''
    var FPS = 30;
    function q(t) { return Math.round(t * FPS) / FPS; }
    var tl = gsap.timeline({ paused: true });
    var NI = { immediateRender: false };
    function cut(sel, t, v) { tl.set(sel, { opacity: v }, q(t)); }
    function hide(sel, t, d) { tl.to(sel, { opacity: 0, duration: d || 0.15, ease: "power2.in" }, q(t)); }
    function fade(sel, t, d, from) { tl.fromTo(sel, Object.assign({ opacity: 0, y: 30 }, from || {}), { opacity: 1, y: 0, x: 0, scale: 1, rotation: 0, duration: d || 0.35, ease: "power3.out" }, q(t)); }
    function pop(sel, t, d) { tl.fromTo(sel, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: d || 0.32, ease: "back.out(2.2)" }, q(t)); }
    function sweep(sel, t, d) {
      var chars = document.querySelectorAll(sel + " .ch");
      tl.set(sel, { opacity: 1 }, q(t));
      tl.fromTo(chars, { opacity: 0, x: -14 }, { opacity: 1, x: 0, duration: 0.24, ease: "power3.out", stagger: Math.min(0.035, (d || 0.45) / chars.length) }, q(t));
    }
    function count(sel, t, d, a, b, fmt) { var o = { v: a }, el = document.querySelector(sel); tl.to(o, { v: b, duration: d, ease: "power2.out", onUpdate: function () { el.textContent = fmt(o.v); } }, q(t)); }
    function type(sel, t, d, msg) { var o = { n: 0 }, el = document.querySelector(sel); tl.to(o, { n: msg.length, duration: d, ease: "none", onUpdate: function () { el.textContent = msg.slice(0, Math.round(o.n)); } }, q(t)); }
    function flash(t, sel, a) { tl.fromTo(sel || "#flash", { opacity: a || 0.3 }, Object.assign({ opacity: 0, duration: 0.25, ease: "power2.out" }, NI), q(t)); }
    function kick(t, x) { tl.fromTo("#cam", { x: x || -10 }, Object.assign({ x: 0, duration: 0.3, ease: "elastic.out(1, .3)" }, NI), q(t)); }
    function idn(v) { return Math.round(v).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, "."); }
'''


def chars(text):
    """Wrap each character for sweep()."""
    return "".join(f'<span class="ch" style="display:inline-block">{c if c != " " else "&nbsp;"}</span>' for c in text)


def svg(body, sw=6):
    return (f'<svg class="ico" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>')


ICON = {
    "shield": svg('<path d="M50 8l34 12v26c0 22-14 38-34 46C30 84 16 68 16 46V20z"/><path d="M36 50l10 10 20-22"/>', 6),
    "key": svg('<circle cx="32" cy="50" r="16"/><path d="M48 50h40M76 50v14M88 50v10"/>', 7),
    "phone": svg('<path d="M30 14h16l6 18-10 7a44 44 0 0 0 19 19l7-10 18 6v16c0 4-3 7-7 7C46 77 23 54 23 21c0-4 3-7 7-7z"/>', 6),
    "video": svg('<rect x="10" y="28" width="56" height="44" rx="8"/><path d="M66 44l24-14v40L66 56"/>', 6),
    "check": svg('<path d="M24 52l17 17 35-38"/>', 11),
    "alert": svg('<path d="M50 12l40 72H10z"/><path d="M50 40v20M50 70v2"/>', 7),
    "mic": svg('<rect x="36" y="12" width="28" height="46" rx="14"/><path d="M24 46a26 26 0 0 0 52 0M50 72v16M36 88h28"/>', 6),
    "chat": svg('<path d="M14 20h72v46H44L26 82V66H14z"/>', 6),
    "cursor": svg('<path d="M24 14l52 30-22 6 14 26-10 5-14-26-16 16z"/>', 5),
}


def page(comp_id, dur, css, body, js):
    return f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8" />
<style>
{FONTS}
{CHIBI_CSS}
{css}
</style>
</head>
<body>
<div id="root" data-composition-id="{comp_id}" data-start="0" data-duration="{dur}" data-fps="{FPS}" data-width="{W}" data-height="{H}">
  <audio id="vo" src="vo.mp3" data-start="0" data-duration="{dur}" data-track-index="0"></audio>
{body}
  <script src="vendor/gsap.min.js"></script>
  <script>
  (function () {{
{JS_HELPERS}
{js}
    window.__timelines = window.__timelines || {{}};
    window.__timelines["{comp_id}"] = tl;
  }})();
  </script>
</div>
</body>
</html>
'''
