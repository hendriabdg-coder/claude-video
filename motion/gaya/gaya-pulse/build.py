# Style template 03 · PULSE — loud kinetic typography (after ref-motion-4's "TEXT KINETIK / TRANSISI CEPAT" and ref-2's
# bold cards): full-screen colour blocks that hard-cut on the beat, giant stacked words that slam in, numbered beats,
# camera shake. Best for opinions, hot takes, tips, "3 hal" lists, motivational hooks.
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from gaya_common import page, words  # noqa: E402
from PIL import ImageFont

F = str(HERE / "public" / "fonts" / "InterDisplay-Black.ttf")
def fit(lines, px, maxw=880):
    """largest size <= px where every line (with -.03em tracking, +6% end-of-beat zoom) fits the frame"""
    while px > 60 and max(ImageFont.truetype(F, px).getlength(l) - len(l) * px * 0.03 for l in lines) * 1.06 > maxw:
        px -= 4
    return px

T = words("pulse")

# (id, start word, end word or None, bg, fg, lines, size)
CARDS = [
    ("k0", None, 0, "#0E0E0E", "#F4F1EA", ["SIAP?"], 260),
    ("k1", 0, 3, "#3A5BFF", "#F4F1EA", ["PROMPT", "PANJANG"], 230),
    ("k2", 3, 7, "#0E0E0E", "#F4F1EA", ["BUKAN", "JAMINAN"], 220),
    ("k3", 7, 12, "#FF4F3A", "#0E0E0E", ["YANG BIKIN", "AI PINTAR"], 160),
    ("k4", 12, 13, "#F4F1EA", "#0E0E0E", ["KONTEKS."], 230),
    ("k5", 13, 14, "#3A5BFF", "#F4F1EA", ["JELAS."], 280),
    ("k6", 14, 15, "#FF4F3A", "#0E0E0E", ["SPESIFIK."], 220),
    ("k7", 15, 17, "#0E0E0E", "#F4F1EA", ["KASIH", "CONTOH."], 230),
    ("k8", 17, 21, "#F4F1EA", "#0E0E0E", ["3 HAL", "ITU AJA"], 230),
    ("k9", 21, None, "#3A5BFF", "#F4F1EA", ["HASILNYA", "LANGSUNG", "BEDA!"], 190),
]
NUMS = {"k5": "1", "k6": "2", "k7": "3"}

css = '''
html, body, #root { background: #0E0E0E; font-family: "IDBlack", sans-serif; }
#cam { position: absolute; inset: 0; }
.card { position: absolute; inset: 0; opacity: 0; overflow: hidden; }
.card .stack { position: absolute; left: 60px; top: 50%; transform: translateY(-50%); width: 960px; }
.card .ln { display: block; line-height: .9; letter-spacing: -.03em; text-transform: uppercase; white-space: nowrap; }
.card .ln span { display: inline-block; }
.card .num { position: absolute; right: 40px; top: 260px; font-size: 420px; line-height: 1; color: transparent; -webkit-text-stroke: 6px currentColor; opacity: .35; }
.card .rib { position: absolute; left: -200px; width: 1600px; font-size: 64px; letter-spacing: .1em; opacity: .14; white-space: nowrap; }
#prompt { position: absolute; left: 90px; top: 1260px; width: 900px; padding: 26px; border-radius: 18px; border: 3px solid rgba(244,241,234,.35); opacity: 0; }
#prompt i { display: block; height: 14px; border-radius: 7px; background: rgba(244,241,234,.45); margin: 10px 0; }
#prompt .x { position: absolute; left: -20px; right: -20px; top: 50%; height: 14px; background: #FF4F3A; transform: scaleX(0); transform-origin: left; }
#end { position: absolute; inset: 0; background: #0E0E0E; opacity: 0; }
#end .n { position: absolute; left: 0; width: 1080px; top: 740px; text-align: center; font-size: 46px; letter-spacing: .3em; color: rgba(244,241,234,.5); }
#end .t { position: absolute; left: 0; width: 1080px; top: 810px; text-align: center; font-size: 230px; letter-spacing: -.03em; color: #F4F1EA; }
#end .t span { color: #3A5BFF; }
#end .d { position: absolute; left: 0; width: 1080px; top: 1080px; text-align: center; font-family: "IDBold"; font-size: 40px; color: rgba(244,241,234,.55); }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-size: 36px; color: #F4F1EA; text-shadow: 0 2px 12px rgba(0,0,0,.6); }
#brand b { font-weight: normal; }
'''

cards = []
for cid, a, b, bg, fg, lines, px in CARDS:
    px = fit(lines, px)
    rows = "".join(f'<span class="ln" style="font-size:{px}px">' + "".join(f"<span>{c}</span>" for c in l.replace(" ", " ")) + "</span>"
                   for l in lines)
    rib = ""
    if cid == "k1":
        rib = "".join(f'<div class="rib" style="top:{120 + r * 260}px">' + "PROMPT " * 30 + "</div>" for r in range(7))
    num = f'<div class="num">{NUMS[cid]}</div>' if cid in NUMS else ""
    extra = '<div id="prompt">' + '<i style="width:96%"></i>' * 3 + '<i style="width:70%"></i><b class="x"></b></div>' if cid == "k2" else ""
    cards.append(f'<div class="card" id="{cid}" style="background:{bg};color:{fg}">{rib}{num}<div class="stack">{rows}</div>{extra}</div>')
body = f'''
  <div id="cam">{"".join(cards)}</div>
  <div id="end"><div class="n">GAYA 03</div><div class="t">PUL<span>SE</span></div><div class="d">tipografi kinetik &middot; opini, tips, hot take</div></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

windows = []
for cid, a, b, bg, fg, *_ in CARDS:
    t0 = 0.0 if a is None else T[a] - 0.04
    t1 = T[0] - 0.04 if b is None and a is None else (12.3 if b is None else T[b] - 0.04)
    windows.append([cid, round(t0, 3), round(t1, 3), fg])

js = f'''
    var T = {T};
    var W = {windows};
    W.forEach(function (w) {{
      cut("#" + w[0], w[1], 1); cut("#" + w[0], w[2], 0);
      tl.set("#brand", {{ color: w[3] }}, q(w[1]));  // wordmark follows each card's ink colour
      var ch = document.querySelectorAll("#" + w[0] + " .ln > span");
      // letters slam in from oversized, staggered, then the whole stack keeps drifting
      tl.fromTo(ch, {{ opacity: 0, scale: 1.8, y: -30 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.18, ease: "power4.out", stagger: Math.min(0.025, 0.22 / ch.length) }}, q(w[1]));
      tl.fromTo("#" + w[0] + " .stack", {{ scale: 1.0 }}, {{ scale: 1.06, duration: Math.max(w[2] - w[1], 0.2), ease: "none" }}, q(w[1]));
      tl.fromTo("#cam", {{ x: 14, y: -10 }}, Object.assign({{ x: 0, y: 0, duration: 0.22, ease: "elastic.out(1, .3)" }}, NI), q(w[1]));
    }});
    tl.fromTo(".rib", {{ x: 0 }}, {{ x: -300, duration: 3, ease: "none" }}, 0);
    tl.fromTo(".num", {{ x: 80 }}, {{ x: 0, duration: 0.4, ease: "power3.out", immediateRender: false }}, q(T[13]));
    rise("#prompt", T[3] + 0.1, 0.25, {{ y: 30 }});
    tl.to("#prompt .x", {{ scaleX: 1, duration: 0.25, ease: "power2.out" }}, q(T[5]));
    tl.to("#k9 .stack", {{ rotation: -3, duration: 0.08, yoyo: true, repeat: 5 }}, q(T[23]));
    tl.set("#brand", {{ color: "#F4F1EA" }}, q(12.3));
    tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, q(12.3));
    tl.fromTo("#end .t", {{ scale: 1.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "power4.out" }}, q(12.35));
'''

(HERE / "public" / "index.html").write_text(page("gaya-pulse", css, body, js), encoding="utf-8")
print("ok", windows)
