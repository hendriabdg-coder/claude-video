# Style template 08 · SHOWCASE — ad/product-demo style (ref-moti0n-12/13/14 + the Hako ad, merged with 06 AVATAR):
# cream-peach canvas with soft colour blobs that change tint per chapter; the creator's chibi opens big, then shrinks
# to the corner as a reacting mascot while a floating browser card shows a REAL Three.js website (product spins, the
# camera dollies on "scroll"); sans titles + serif-italic accents with numbered step badges; keyword-only captions with
# an orange highlight box; twist "that was a website" + live cursor click.  Poses: public/pose/*.png.
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from gaya_common import VO_START, page, words  # noqa: E402

T = words("showcase")
FPS = 30
END = 12.3

# --- pose track: emphasis poses on beats, lip-flap + blinks while netral (same recipe as gaya-avatar) -------------
raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(HERE / "public" / "vo.mp3"), "-ac", "1", "-ar", "48000",
                               "-f", "s16le", "-"])
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
hop = 48000 // FPS
db = np.array([20 * np.log10(np.sqrt((x[i:i + hop] ** 2).mean()) + 1e-9) for i in range(0, len(x) - hop, hop)])
loud = db > db.max() - 22
sm = np.convolve(db, np.ones(7) / 7, mode="same")
open_ = loud & (db >= sm - 1.0)
EMPH = [(0.0, "netral"), (T[3] - 0.05, "kaget"), (T[4] - 0.05, "tunjuk"), (T[8] - 0.05, "netral"),
        (T[15] - 0.05, "mikir"), (T[20] - 0.05, "keren")]
BLINK = [1.6, 6.3]


def base(t):
    return [p for s, p in EMPH if s <= t + 1e-6][-1]


track, prev, hold = [], None, 0
for f in range(int(END * FPS)):
    t = f / FPS
    p = base(t)
    if p == "netral":
        want = "bicara" if open_[min(f, len(open_) - 1)] and t > VO_START else "netral"
        if prev in ("netral", "bicara") and want != prev and hold < 2:
            want = prev
        if any(b <= t < b + 0.13 for b in BLINK):
            want = "kedip"
        p = want
    hold = hold + 1 if p == prev else 1
    if p != prev:
        track.append([round(t, 3), p])
    prev = p
EMPH_T = [round(s, 3) for s, p in EMPH[1:] if p != "netral"]

css = '''
@font-face { font-family: "SerifBI"; src: url("fonts/SerifBI.ttf") format("truetype"); font-display: block; }
:root { --ink:#1E1B18; --org:#E2582B; --cream:#F4EBE1; }
html, body, #root { background: var(--cream); color: var(--ink); font-family: "IDBold"; }
.bg { position: absolute; inset: 0; opacity: 0; }
.bg i { position: absolute; border-radius: 50%; filter: blur(90px); }
#bgA { opacity: 1; }
#cam { position: absolute; inset: 0; }
#brand { position: absolute; right: 64px; top: 70px; font-family: "IDBlack"; font-size: 30px; color: var(--ink); }
#brand i { font-family: "SerifBI"; font-style: normal; color: var(--org); }
.h { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; line-height: 1.02;
  font-family: "IDBlack"; font-size: 84px; letter-spacing: -.025em; }
.h i { font-family: "SerifBI"; font-style: normal; color: var(--org); font-size: 1.12em; letter-spacing: -.01em; }
.h .n { display: inline-block; width: 74px; height: 74px; border-radius: 50%; background: var(--org); color: #FFF4EA;
  font-family: "SerifBI"; font-size: 50px; line-height: 76px; text-align: center; vertical-align: 10px; margin-right: 22px; }
.cap { position: absolute; left: 0; width: 1080px; top: 1380px; text-align: center; white-space: nowrap; font-family: "IDBlack";
  font-size: 64px; letter-spacing: -.02em; }
.cap span { display: inline-block; opacity: 0; margin: 0 8px; }
.cap span.k { background: var(--org); color: #FFF6EE; padding: 2px 18px 8px; border-radius: 12px; }
#stage { position: absolute; inset: 0; perspective: 1800px; }
.win { position: absolute; border-radius: 30px; overflow: hidden; background: #FFFDFB; opacity: 0;
  box-shadow: 0 50px 90px rgba(120,60,30,.22), 0 6px 18px rgba(120,60,30,.10); }
.bar { height: 62px; background: #F1E8DF; display: flex; align-items: center; padding: 0 24px; gap: 12px; }
.bar b { width: 18px; height: 18px; border-radius: 50%; background: #E9B8A6; }
.bar .url { margin-left: 18px; flex: 1; height: 38px; border-radius: 19px; background: #FFFDFB; font-family: "IDSemi";
  font-size: 22px; line-height: 38px; padding-left: 22px; color: rgba(30,27,24,.6); }
#flat { left: 130px; top: 390px; width: 820px; height: 520px; }
#flat .body { padding: 40px; }
#flat .g { background: #E3DDD6; border-radius: 10px; margin-bottom: 22px; }
#strike { position: absolute; left: 130px; top: 390px; width: 820px; height: 520px; overflow: visible; }
#strike path { fill: none; stroke: #E0402A; stroke-width: 16; stroke-linecap: round; stroke-linejoin: round; }
#web { left: 60px; top: 440px; width: 960px; height: 820px; }
#site { position: relative; width: 960px; height: 758px; overflow: hidden;
  background: radial-gradient(ellipse 70% 80% at 72% 55%, #FFE3CF 0%, #F7E6D6 55%, #EFDCCB 100%); }
#three { position: absolute; inset: 0; width: 960px; height: 758px; display: block; }
#nav { position: absolute; left: 44px; right: 44px; top: 30px; display: flex; justify-content: space-between; font-family: "IDSemi";
  font-size: 22px; color: rgba(30,27,24,.7); }
#nav .lg { font-family: "IDBlack"; font-size: 26px; color: var(--ink); letter-spacing: .06em; }
#nav .lg i { font-family: "SerifBI"; font-style: normal; color: var(--org); letter-spacing: 0; }
#scroller { position: absolute; left: 0; top: 0; width: 960px; }
.sec { position: relative; height: 758px; padding: 190px 0 0 48px; }
.sec .e { font-family: "IDSemi"; font-size: 20px; letter-spacing: .2em; color: var(--org); margin-bottom: 18px; }
.sec .t { font-family: "IDBlack"; font-size: 74px; line-height: .98; letter-spacing: -.03em; }
.sec .t i { font-family: "SerifBI"; font-style: normal; color: var(--org); font-size: 1.1em; }
.sec .p { margin-top: 22px; font-family: "IDSemi"; font-size: 26px; color: rgba(30,27,24,.65); width: 340px; line-height: 1.3; }
.btn { display: inline-block; margin-top: 30px; background: var(--ink); color: #FFF6EE; font-family: "IDBold"; font-size: 24px;
  padding: 18px 30px; border-radius: 40px; }
#sbar { position: absolute; right: 16px; top: 120px; width: 8px; height: 520px; border-radius: 4px; background: rgba(30,27,24,.08); }
#sbar i { position: absolute; left: 0; top: 0; width: 8px; height: 170px; border-radius: 4px; background: rgba(30,27,24,.35); }
.pill { position: absolute; opacity: 0; font-family: "IDBold"; font-size: 26px; padding: 12px 22px; border-radius: 30px; white-space: nowrap; }
#p360 { left: 760px; top: 600px; background: var(--ink); color: #FFF6EE; }
#pLive { left: 760px; top: 455px; background: #1F9D55; color: #F2FFF6; font-size: 22px; padding: 8px 18px; }
#pOk { left: 300px; top: 1290px; background: #FFFDFB; color: var(--ink); box-shadow: 0 14px 30px rgba(120,60,30,.16); }
#pOk b { color: #1F9D55; }
#toast { left: 400px; top: 1130px; background: var(--ink); color: #FFF6EE; font-size: 24px; }
#cursor { position: absolute; left: 0; top: 0; width: 56px; height: 56px; opacity: 0; filter: drop-shadow(0 6px 8px rgba(0,0,0,.25)); }
#chars { position: absolute; left: 248px; top: 868px; width: 585px; height: 1042px; }
#charS { position: absolute; inset: 0; }
#charS img { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; }
#shadow { position: absolute; left: 340px; top: 1840px; width: 400px; height: 46px; border-radius: 50%; background: rgba(120,60,30,.22);
  filter: blur(14px); opacity: 0; }
.spk { position: absolute; width: 16px; height: 16px; background: var(--org); border-radius: 3px; transform: rotate(45deg); opacity: 0; }
#end { position: absolute; inset: 0; background: radial-gradient(ellipse 90% 60% at 50% 35%, #FBEFE4 0%, #EED9C8 100%); opacity: 0; }
#end .n { position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; font-family: "IDSemi"; font-size: 40px; letter-spacing: .3em; color: rgba(30,27,24,.55); }
#end .t { position: absolute; left: 0; width: 1080px; top: 400px; text-align: center; font-family: "SerifBI"; font-size: 200px; color: var(--org); }
#end .d { position: absolute; left: 0; width: 1080px; top: 650px; text-align: center; font-family: "IDSemi"; font-size: 34px; color: rgba(30,27,24,.65); }
#endImg { position: absolute; left: 307px; top: 860px; width: 466px; height: 830px; }
'''

POSES = ["netral", "lambai", "tunjuk", "mikir", "kaget", "keren", "bicara", "kedip"]
imgs = "".join(f'<img id="p_{p}" src="pose/pose_{i}_{p}.png">' for i, p in enumerate(POSES))
# three blob sets: peach (hook/3D), sky (scroll), lilac (twist)
BLOBS = {"bgA": [("#FFB48A", 120, 260, 620), ("#FF8C6B", 620, 900, 560), ("#FFD9B0", 200, 1350, 640)],
         "bgB": [("#A9CFFF", 80, 300, 620), ("#FFB48A", 640, 960, 520), ("#BFE3FF", 260, 1380, 620)],
         "bgC": [("#D5B8FF", 140, 240, 600), ("#FF9E80", 600, 880, 540), ("#E7C9FF", 220, 1360, 640)]}
bg = "".join(f'<div class="bg" id="{k}">' + "".join(
    f'<i style="background:{c};left:{x}px;top:{y}px;width:{s}px;height:{s}px;opacity:.75"></i>' for c, x, y, s in v) + "</div>"
    for k, v in BLOBS.items())
SPK = [(150, 420), (930, 380), (110, 1180), (960, 1230), (520, 330)]
CAPS = [("capA", [(4, "Aku"), (5, "bikinin"), (6, "versi"), (7, "3D", True)]),
        ("capB", [(9, "bisa"), (10, "diputar", True)]),
        ("capC", [(12, "kayak"), (13, "nonton"), (14, "film", True)]),
        ("capD", [(17, "barusan"), (18, "kamu"), (19, "lihat?", True)])]
caps = "".join(f'<div class="cap" id="{cid}">' + "".join(
    f'<span id="{cid}w{w[0]}"{" class=k" if len(w) > 2 else ""}>{w[1]}</span>' for w in ws) + "</div>" for cid, ws in CAPS)
STRIKE = "M60 120 L760 400 M70 400 L770 110 M40 260 C200 200 300 330 420 250 C540 170 640 320 790 250"
body = f'''
  {bg}
  <div id="cam">
    <div class="h" id="h1a" style="top:150px">Website kamu</div>
    <div class="h" id="h1b" style="top:250px">masih <i>datar?</i></div>
    <div class="h" id="h2" style="top:200px"><span class="n">1</span>Versi <i>3D</i></div>
    <div class="h" id="h3" style="top:200px"><span class="n">2</span>Bisa <i>diputar</i></div>
    <div class="h" id="h4" style="top:200px"><span class="n">3</span>Scroll <i>sinematik</i></div>
    <div class="h" id="h5a" style="top:150px;font-size:70px">Yang barusan kamu lihat?</div>
    <div class="h" id="h5b" style="top:245px">Itu <i>website.</i></div>
    <div id="stage">
      <div class="win" id="flat"><div class="bar"><b></b><b></b><b></b><div class="url">toko-kamu.com</div></div>
        <div class="body"><div class="g" style="width:60%;height:46px"></div><div class="g" style="width:85%;height:22px"></div>
        <div class="g" style="width:70%;height:22px"></div><div class="g" style="width:100%;height:190px;margin-top:30px"></div></div></div>
      <svg id="strike" viewBox="0 0 820 520"><path d="{STRIKE}"/></svg>
      <div class="win" id="web"><div class="bar"><b></b><b></b><b></b><div class="url" id="url">kopinusa.id</div></div>
        <div id="site">
          <canvas id="three" width="960" height="758"></canvas>
          <div id="scroller">
            <div class="sec"><div class="e">KOPI NUSA &middot; SEJAK 2024</div><div class="t">Kopi<br><i>Nusantara</i></div>
              <div class="p">Sangrai segar tiap pagi, langsung ke mejamu.</div><div class="btn" id="btn">Pesan sekarang</div></div>
            <div class="sec"><div class="e">02 &middot; PROSES</div><div class="t">Sangrai<br><i>perlahan</i></div>
              <div class="p">Biji pilihan dari Gayo &amp; Toraja.</div><div class="btn" id="btn2">Pesan sekarang</div></div>
          </div>
          <div id="nav"><div class="lg">KOPI<i>nusa</i></div><div>Menu &nbsp;&middot;&nbsp; Cerita &nbsp;&middot;&nbsp; Kontak</div></div>
          <div id="sbar"><i id="thumb"></i></div>
        </div></div>
      <div class="pill" id="p360">&#8635; 360&deg;</div>
      <div class="pill" id="pLive">&#9679; LIVE</div>
      <div class="pill" id="toast">&#10003; Pesanan masuk</div>
    </div>
    {caps}
    <div class="pill" id="pOk"><b>&#10003;</b> bisa diklik &middot; bisa di-scroll</div>
    {"".join(f'<div class="spk" style="left:{a}px;top:{b}px"></div>' for a, b in SPK)}
    <div id="shadow"></div>
    <div id="chars"><div id="charS">{imgs}</div></div>
    <svg id="cursor" viewBox="0 0 24 24"><path d="M4 2 L4 19 L8.5 15 L11.5 22 L14.5 20.7 L11.6 14 L18 14 Z" fill="#1E1B18" stroke="#FFF" stroke-width="1.4"/></svg>
    <div id="brand">Endrich<i>Tech</i></div>
  </div>
  <div id="end"><div class="n">GAYA 08</div><div class="t">Showcase</div><div class="d">iklan &middot; chibi + website 3D &middot; langkah bernomor</div>
    <img id="endImg" src="pose/end_lambai.png"></div>
'''

js = f'''
    var T = {T};
    var TRACK = {track};
    var EMPH = {EMPH_T};
    TRACK.forEach(function (e) {{ tl.set("#charS img:not(#p_" + e[1] + ")", {{ opacity: 0 }}, q(e[0])); tl.set("#p_" + e[1], {{ opacity: 1 }}, q(e[0])); }});
    // chibi: big entrance, idle bob, shrink to the corner when the 3D card arrives, grow a little for the twist
    tl.set("#chars", {{ transformOrigin: "50% 100%" }}, 0);
    tl.fromTo("#chars", {{ y: 700 }}, {{ y: 0, duration: 0.55, ease: "back.out(1.4)" }}, 0.1);
    tl.fromTo("#shadow", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0.3);
    tl.fromTo("#charS", {{ y: 0 }}, {{ y: -10, duration: 0.6, yoyo: true, repeat: 15, ease: "sine.inOut" }}, 0.7);
    tl.to("#chars", {{ x: 360, y: -10, scale: 0.42, duration: 0.5, ease: "power3.inOut" }}, q(T[4] - 0.1));
    tl.to("#shadow", {{ x: 360, y: -20, scaleX: 0.42, duration: 0.5, ease: "power3.inOut" }}, q(T[4] - 0.1));
    tl.to("#chars", {{ scale: 0.5, duration: 0.4, ease: "back.out(2)" }}, q(T[20] - 0.05));
    EMPH.forEach(function (t) {{ tl.fromTo("#charS", {{ scaleY: 0.93, scaleX: 1.05 }}, Object.assign({{ scaleY: 1, scaleX: 1, duration: 0.35, ease: "back.out(3)", transformOrigin: "50% 100%" }}, NI), q(t)); }});
    // backgrounds: blobs drift; tint per chapter
    document.querySelectorAll(".bg i").forEach(function (b, k) {{
      tl.fromTo(b, {{ x: 0, y: 0 }}, {{ x: (k % 2 ? -80 : 70), y: (k % 3 ? 60 : -50), duration: 6, yoyo: true, repeat: 1, ease: "sine.inOut" }}, 0);
    }});
    tl.fromTo("#bgB", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, q(T[11] - 0.2));
    tl.fromTo("#bgC", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, q(T[15] - 0.1));
    // hook: headline + flat site, scribbled out
    rise("#h1a", T[0] - 0.05, 0.35); rise("#h1b", T[2] - 0.05, 0.4, {{ y: 50, rotation: -2 }});
    tl.set("#flat", {{ transformOrigin: "50% 50%" }}, 0);
    tl.fromTo("#flat", {{ opacity: 0, y: 80, rotationX: 18 }}, {{ opacity: 1, y: 0, rotationX: 0, duration: 0.55, ease: "power3.out" }}, 0.35);
    var sp = document.querySelector("#strike path"), L = Math.ceil(sp.getTotalLength()) + 2; sp.style.strokeDasharray = L;
    tl.fromTo(sp, {{ strokeDashoffset: L }}, {{ strokeDashoffset: 0, duration: 0.55, ease: "power1.inOut" }}, q(T[3]));
    tl.fromTo("#strike", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, q(T[3]));
    hide("#h1a, #h1b", T[4] - 0.2, 0.15);
    // flip: flat card out, 3D website card in
    tl.to("#flat, #strike", {{ rotationY: 90, opacity: 0, duration: 0.22, ease: "power2.in" }}, q(T[4] - 0.2));
    tl.set("#web", {{ transformOrigin: "50% 50%" }}, 0);
    tl.fromTo("#web", {{ opacity: 0, rotationY: -90, scale: 0.9 }}, {{ opacity: 1, rotationY: 0, scale: 1, duration: 0.5, ease: "back.out(1.3)" }}, q(T[4] + 0.02));
    tl.fromTo("#web", {{ y: 0 }}, {{ y: -12, duration: 1.2, yoyo: true, repeat: 1, ease: "sine.inOut" }}, q(T[4] + 0.6));
    // step titles
    rise("#h2", T[4], 0.4); hide("#h2", T[8] - 0.15, 0.12);
    rise("#h3", T[8], 0.4); hide("#h3", T[11] - 0.15, 0.12);
    rise("#h4", T[11], 0.4); hide("#h4", T[15] - 0.15, 0.12);
    // keyword captions, word by word; key word pops in its orange box
    [["capA", [4, 5, 6, 7], T[8] - 0.12], ["capB", [9, 10], T[11] - 0.12], ["capC", [12, 13, 14], T[15] - 0.12], ["capD", [17, 18, 19], T[20] - 0.12]].forEach(function (c) {{
      c[1].forEach(function (i) {{
        var s = "#" + c[0] + "w" + i;
        if (document.querySelector(s).className === "k") pop(s, T[i], 0.3); else rise(s, T[i], 0.2, {{ y: 16 }});
      }});
      hide("#" + c[0] + " span", c[2], 0.12);
    }});
    // spin: cursor drags across the cup, 360 pill
    tl.fromTo("#cursor", {{ opacity: 0, x: 640, y: 980 }}, {{ opacity: 1, duration: 0.2 }}, q(T[8]));
    tl.to("#cursor", {{ x: 900, y: 940, duration: 0.9, ease: "power2.inOut" }}, q(T[8] + 0.15));
    hide("#cursor", T[10] + 0.5, 0.15);
    tl.fromTo("#p360", {{ opacity: 0, scale: 0.5, rotation: 0 }}, {{ opacity: 1, scale: 1, rotation: -6, duration: 0.32, ease: "back.out(2.2)" }}, q(T[10]));
    hide("#p360", T[11] + 0.2, 0.15);
    // scroll: site content scrolls, thumb moves (camera dolly happens in Three)
    tl.fromTo("#scroller", {{ y: 0 }}, {{ y: -758, duration: T[14] + 0.3 - T[11], ease: "power2.inOut" }}, q(T[11]));
    tl.fromTo("#thumb", {{ y: 0 }}, {{ y: 350, duration: T[14] + 0.3 - T[11], ease: "power2.inOut" }}, q(T[11]));
    // twist: pull back, URL + LIVE, cursor clicks the button, toast
    tl.to("#web", {{ scale: 0.93, y: -30, duration: 0.6, ease: "power2.inOut" }}, q(T[15]));
    rise("#h5a", T[15], 0.35); rise("#h5b", T[20] - 0.05, 0.45, {{ y: 60, scale: 1.15 }});
    tl.to("#h5a", {{ opacity: 0.35, duration: 0.2 }}, q(T[20] - 0.1));
    pop("#pLive", T[19], 0.3);
    tl.fromTo("#cursor", {{ opacity: 0, x: 620, y: 1250 }}, Object.assign({{ opacity: 1, duration: 0.2 }}, NI), q(T[20] + 0.2));
    tl.to("#cursor", {{ x: 225, y: 1060, duration: 0.6, ease: "power2.inOut" }}, q(T[20] + 0.25));
    tl.to("#cursor", {{ scale: 0.8, duration: 0.08, yoyo: true, repeat: 1 }}, q(T[20] + 0.9));
    tl.to("#btn2", {{ scale: 0.92, backgroundColor: "#E2582B", duration: 0.08, yoyo: true, repeat: 1 }}, q(T[20] + 0.9));
    tl.fromTo("#toast", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, q(T[20] + 1.0));
    rise("#pOk", T[21] + 0.6, 0.4, {{ y: 30 }});
    document.querySelectorAll(".spk").forEach(function (s, k) {{
      tl.fromTo(s, {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1.5, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out" }}, q(T[21] + 0.08 * k));
    }});
    tl.fromTo("#cam", {{ scale: 1 }}, {{ scale: 1.04, duration: 2.4, ease: "power1.inOut" }}, q(T[20] - 0.05));
    // end card
    tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, q({END}));
    rise("#end .t", {END} + 0.05, 0.45, {{ y: 60 }});
    tl.set("#endImg", {{ transformOrigin: "50% 100%" }}, 0);
    tl.fromTo("#endImg", {{ y: 500 }}, {{ y: 0, duration: 0.5, ease: "back.out(1.4)" }}, q({END} + 0.1));
    tl.fromTo("#endImg", {{ rotation: -2 }}, {{ rotation: 2, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut" }}, q({END} + 0.6));
'''

# Three.js website hero: a ceramic cup on a saucer with floating beans. Every frame is a pure function of time.
three = f'''
<script type="importmap">{{"imports": {{"three": "./vendor/three.module.min.js"}}}}</script>
<script type="module">
  import * as THREE from "three";
  import {{ RoomEnvironment }} from "./vendor/RoomEnvironment.js";
  var T = {T};
  var canvas = document.getElementById("three");
  var renderer = new THREE.WebGLRenderer({{ canvas: canvas, alpha: true, antialias: true, preserveDrawingBuffer: true }});
  renderer.setPixelRatio(1); renderer.setSize(960, 758, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  var scene = new THREE.Scene();
  var pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  var key = new THREE.DirectionalLight(0xffe2c4, 2.2); key.position.set(-3, 5, 4); scene.add(key);
  var rim = new THREE.DirectionalLight(0xffb48a, 1.4); rim.position.set(4, 2, -3); scene.add(rim);
  var camera = new THREE.PerspectiveCamera(30, 960 / 758, 0.1, 100);

  function lathe(pts, mat) {{ return new THREE.Mesh(new THREE.LatheGeometry(pts.map(function (p) {{ return new THREE.Vector2(p[0], p[1]); }}), 96), mat); }}
  var ceramic = new THREE.MeshStandardMaterial({{ color: 0xE2582B, roughness: 0.32, metalness: 0.0, side: THREE.DoubleSide }});
  var cream = new THREE.MeshStandardMaterial({{ color: 0xF6ECE2, roughness: 0.4, side: THREE.DoubleSide }});
  var product = new THREE.Group(); scene.add(product);
  var cup = new THREE.Group(); product.add(cup);
  cup.add(lathe([[0, 0.1], [0.56, 0.1], [0.62, 0.15], [0.7, 0.5], [0.76, 1.0], [0.8, 1.06], [0.74, 1.06], [0.7, 1.0], [0.64, 0.5], [0.58, 0.2], [0, 0.2]], ceramic));
  var band = lathe([[0.72, 0.78], [0.745, 0.86]], cream); cup.add(band);
  var coffee = new THREE.Mesh(new THREE.CircleGeometry(0.71, 64), new THREE.MeshStandardMaterial({{ color: 0x3B2316, roughness: 0.15 }}));
  coffee.rotation.x = -Math.PI / 2; coffee.position.y = 0.93; cup.add(coffee);
  var foam = new THREE.Mesh(new THREE.RingGeometry(0.0, 0.32, 48), new THREE.MeshStandardMaterial({{ color: 0xC89A6A, roughness: 0.6 }}));
  foam.rotation.x = -Math.PI / 2; foam.position.set(0.08, 0.935, 0.05); foam.scale.set(1, 0.8, 1); cup.add(foam);
  var handle = new THREE.Mesh(new THREE.TorusGeometry(0.26, 0.065, 20, 48, Math.PI * 1.1), ceramic);
  handle.rotation.z = -Math.PI / 2 - 0.05; handle.position.set(0.73, 0.58, 0); cup.add(handle);
  product.add(lathe([[0, 0], [1.15, 0], [1.25, 0.07], [1.22, 0.1], [0.7, 0.06], [0, 0.06]], cream));
  // soft contact shadow
  var sc = document.createElement("canvas"); sc.width = sc.height = 128; var g = sc.getContext("2d");
  var gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, "rgba(90,40,20,.45)"); gr.addColorStop(1, "rgba(90,40,20,0)");
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  var shadow = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 3.6), new THREE.MeshBasicMaterial({{ map: new THREE.CanvasTexture(sc), transparent: true, depthWrite: false }}));
  shadow.rotation.x = -Math.PI / 2; shadow.position.y = -0.01; product.add(shadow);
  // beans (fixed layout, no randomness)
  var beanMat = new THREE.MeshStandardMaterial({{ color: 0x5A3420, roughness: 0.45 }});
  var BEANS = [[-1.3, 1.6, 0.4, 0.2], [1.5, 1.9, -0.3, 1.1], [-0.9, 2.4, -0.6, 2.0], [1.1, 0.9, 0.9, 2.9], [-1.6, 0.7, -0.2, 3.7],
               [0.4, 2.6, 0.5, 4.4], [1.7, 1.3, 0.3, 5.1], [-0.4, 1.1, 1.2, 5.9]];
  var beans = BEANS.map(function (b) {{
    var m = new THREE.Mesh(new THREE.SphereGeometry(0.14, 24, 16), beanMat); m.scale.set(1, 0.72, 0.58); product.add(m); return m;
  }});

  function ss(a, b, t) {{ var x = Math.min(1, Math.max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x); }}
  function mix(a, b, k) {{ return a.map(function (v, i) {{ return v + (b[i] - v) * k; }}); }}
  // camera keys: [position, target]
  var WIDE = [[-1.0, 2.1, 7.6], [-1.3, 0.75, 0]], CLOSE = [[0.2, 1.55, 3.9], [-0.55, 0.7, 0]], OUT = [[-1.2, 2.4, 8.6], [-1.4, 0.7, 0]];
  function renderAt(t) {{
    var spin = 0.35 * t - 0.9 + Math.PI * 2 * ss(T[8] + 0.15, T[10] + 0.45, t);
    product.rotation.y = spin;
    product.position.y = 0.06 * Math.sin(t * 1.6);
    BEANS.forEach(function (b, i) {{
      beans[i].position.set(b[0], b[1] + 0.12 * Math.sin(t * 1.3 + b[3]), b[2]);
      beans[i].rotation.set(t * 0.7 + b[3], t * 0.9 + b[3] * 2, b[3]);
    }});
    var k1 = ss(T[11], T[14] + 0.3, t), k2 = ss(T[15], T[15] + 1.0, t);
    var p = mix(mix(WIDE[0], CLOSE[0], k1), OUT[0], k2), c = mix(mix(WIDE[1], CLOSE[1], k1), OUT[1], k2);
    camera.position.set(p[0], p[1], p[2]); camera.lookAt(c[0], c[1], c[2]);
    renderer.render(scene, camera);
  }}
  window.addEventListener("hf-seek", function (e) {{ renderAt(e.detail.time); }});
  renderAt(window.__hfThreeTime || 0);
</script>
'''

html = page("gaya-showcase", css, body, js).replace("</body>", three + "</body>")
(HERE / "public" / "index.html").write_text(html, encoding="utf-8")
print("ok", len(track), "pose events")
