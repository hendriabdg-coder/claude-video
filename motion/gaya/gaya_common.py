# Shared bits for the style-template previews (gaya-paper / gaya-pulse / gaya-terminal): 15 s, VO starts at 1.0 s,
# the last ~2.5 s is a style name card. Each build_*.py imports this and fills in its own CSS/HTML/timeline.
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DUR, VO_START, W, H = 15.0, 1.0, 1080, 1920


def words(style):
    d = json.loads((ROOT / "motion" / "panduan-gaya" / "_vo" / style / "scene_01.json").read_text(encoding="utf-8"))
    return {i: round(w["start"] + VO_START, 3) for i, w in enumerate(d["words"])}


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
    function rise(sel, t, d, from) { tl.fromTo(sel, Object.assign({ opacity: 0, y: 40 }, from || {}), { opacity: 1, y: 0, x: 0, scale: 1, rotation: 0, duration: d || 0.4, ease: "power3.out" }, q(t)); }
    function pop(sel, t, d) { tl.fromTo(sel, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: d || 0.32, ease: "back.out(2.2)" }, q(t)); }
    function hide(sel, t, d) { tl.to(sel, { opacity: 0, duration: d || 0.15, ease: "power2.in" }, q(t)); }
    function count(sel, t, d, a, b, fmt) { var o = { v: a }, el = document.querySelector(sel); tl.to(o, { v: b, duration: d, ease: "power2.out", onUpdate: function () { el.textContent = fmt(o.v); } }, q(t)); }
    function type(sel, t, d, msg) { var o = { n: 0 }, el = document.querySelector(sel); tl.to(o, { n: msg.length, duration: d, ease: "none", onUpdate: function () { el.textContent = msg.slice(0, Math.round(o.n)); } }, q(t)); }
'''


def page(comp_id, css, body, js):
    return f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8" />
<style>
{FONTS}
{css}
</style>
</head>
<body>
<div id="root" data-composition-id="{comp_id}" data-start="0" data-duration="{DUR}" data-fps="30" data-width="{W}" data-height="{H}">
  <audio id="vo" src="vo.mp3" data-start="0" data-duration="{DUR}" data-track-index="0"></audio>
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
