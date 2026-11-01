# Ad · "Website kamu cuma jadi brosur online?" (jasa website 3D) in style 08 SHOWCASE (from motion/gaya/gaya-showcase):
# hook with a flat "brochure" site that gets scribbled out, then a floating browser card playing the creator's own
# web-3D demos (watch -> logistics -> housing, public/assets/screen.mp4 from prep_clips.py), numbered steps with
# keyword captions, three stills for "aku yang bikin", and a DM CTA bubble held by the chibi.  25 s, VO at 0.3 s.
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
import gaya_common  # noqa: E402

DUR, VO_START, FPS = 25.0, 0.3, 30
gaya_common.DUR = DUR
d = json.loads((HERE / "vo" / "scene_01.json").read_text(encoding="utf-8"))
T = {i: round(w["start"] + VO_START, 3) for i, w in enumerate(d["words"])}

# --- pose track (recipe from gaya-avatar): emphasis poses on beats, lip-flap + blinks while netral -----------------
raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(HERE / "public" / "vo.mp3"), "-ac", "1", "-ar", "48000",
                               "-f", "s16le", "-"])
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
hop = 48000 // FPS
db = np.array([20 * np.log10(np.sqrt((x[i:i + hop] ** 2).mean()) + 1e-9) for i in range(0, len(x) - hop, hop)])
loud = db > db.max() - 22
sm = np.convolve(db, np.ones(7) / 7, mode="same")
open_ = loud & (db >= sm - 1.0)
END_WAVE = T[53] + 0.6
EMPH = [(0.0, "netral"), (T[5] - 0.05, "kaget"), (T[10] - 0.05, "tunjuk"), (T[12] - 0.05, "netral"),
        (T[35] - 0.05, "keren"), (T[38] - 0.05, "netral"), (T[44] - 0.05, "tunjuk"), (T[46] - 0.05, "netral"),
        (END_WAVE, "lambai")]
BLINK = [9.0, 16.1, 19.9]


def base(t):
    return [p for s, p in EMPH if s <= t + 1e-6][-1]


track, prev, hold = [], None, 0
for f in range(int(DUR * FPS)):
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
#wm { position: absolute; left: 0; width: 1080px; top: 1508px; text-align: center; font-family: "IDBlack"; font-size: 30px; color: rgba(30,27,24,.8); }
#wm i { font-family: "SerifBI"; font-style: normal; color: var(--org); }
.h { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; line-height: 1.02;
  font-family: "IDBlack"; font-size: 84px; letter-spacing: -.025em; }
.h i { font-family: "SerifBI"; font-style: normal; color: var(--org); font-size: 1.12em; letter-spacing: -.01em; }
.h .n { display: inline-block; width: 74px; height: 74px; border-radius: 50%; background: var(--org); color: #FFF4EA;
  font-family: "SerifBI"; font-size: 50px; line-height: 76px; text-align: center; vertical-align: 10px; margin-right: 22px; }
.cap { position: absolute; left: 0; width: 820px; text-align: center; white-space: nowrap; font-family: "IDBlack";
  font-size: 64px; letter-spacing: -.02em; }
.cap span { display: inline-block; opacity: 0; margin: 0 8px; }
.cap span.k { background: var(--org); color: #FFF6EE; padding: 2px 18px 8px; border-radius: 12px; }
#stage { position: absolute; inset: 0; perspective: 1800px; }
.win { position: absolute; border-radius: 28px; overflow: hidden; background: #FFFDFB; opacity: 0;
  box-shadow: 0 50px 90px rgba(120,60,30,.24), 0 6px 18px rgba(120,60,30,.10); }
.bar { position: relative; height: 56px; background: #F1E8DF; display: flex; align-items: center; padding: 0 22px; gap: 11px; }
.bar b { width: 16px; height: 16px; border-radius: 50%; background: #E9B8A6; }
.bar .url { position: relative; margin-left: 16px; flex: 1; height: 34px; border-radius: 17px; background: #FFFDFB; font-family: "IDSemi";
  font-size: 21px; line-height: 34px; padding-left: 20px; color: rgba(30,27,24,.6); }
.url span { position: absolute; left: 20px; top: 0; opacity: 0; }
.lbl { position: absolute; font-family: "IDBold"; font-size: 18px; letter-spacing: .16em; padding: 6px 14px; border-radius: 8px; }
#flat { left: 130px; top: 505px; width: 820px; height: 430px; }
#flat .body { padding: 36px; }
#flat .g { background: #E3DDD6; border-radius: 10px; margin-bottom: 20px; }
#flat .lbl { right: 22px; top: 13px; background: rgba(30,27,24,.08); color: rgba(30,27,24,.6); }
#strike { position: absolute; left: 130px; top: 505px; width: 820px; height: 430px; overflow: visible; opacity: 0; }
#strike path { fill: none; stroke: #E0402A; stroke-width: 16; stroke-linecap: round; stroke-linejoin: round; }
#stick { position: absolute; left: 300px; top: 690px; opacity: 0; background: #FFFDFB; border-radius: 16px; padding: 14px 24px;
  font-family: "IDBlack"; font-size: 40px; box-shadow: 0 16px 34px rgba(120,60,30,.2); white-space: nowrap; }
#stick i { font-family: "SerifBI"; font-style: normal; color: #E0402A; }
#web { left: 60px; top: 450px; width: 960px; height: 596px; }
#web video { display: block; width: 960px; height: 540px; object-fit: cover; background: #0E1420; }
#web .lbl { right: 22px; top: 13px; background: var(--org); color: #FFF6EE; }
.still { position: absolute; width: 440px; height: 278px; border-radius: 20px; overflow: hidden; background: #FFFDFB; opacity: 0;
  box-shadow: 0 30px 60px rgba(120,60,30,.25); }
.still .bar { height: 30px; padding: 0 14px; gap: 7px; }
.still .bar b { width: 10px; height: 10px; }
.still img { display: block; width: 440px; height: 248px; object-fit: cover; }
#s1 { left: 70px; top: 560px; } #s2 { left: 320px; top: 500px; } #s3 { left: 570px; top: 560px; }
#demo { position: absolute; left: 0; width: 1080px; top: 445px; text-align: center; opacity: 0; }
#demo span { font-family: "IDBold"; font-size: 22px; letter-spacing: .2em; color: var(--org); background: rgba(226,88,43,.1); padding: 8px 18px; border-radius: 10px; }
#bub { position: absolute; left: 170px; top: 485px; width: 740px; height: 365px; opacity: 0; background: #FFFDFB; border-radius: 36px;
  box-shadow: 0 30px 70px rgba(120,60,30,.22); text-align: center; }
#bub:after { content: ""; position: absolute; left: 345px; bottom: -26px; width: 52px; height: 52px; background: #FFFDFB; transform: rotate(45deg); border-radius: 6px; }
#bub .a { padding-top: 40px; font-family: "IDBlack"; font-size: 58px; letter-spacing: -.02em; }
#bub .p { display: inline-block; margin-top: 18px; background: var(--org); color: #FFF6EE; font-family: "IDBlack"; font-size: 96px;
  padding: 4px 56px 14px; border-radius: 60px; transform: rotate(-3deg); opacity: 0; }
#bub .c { position: absolute; left: 0; width: 740px; top: 290px; font-family: "SerifBI"; font-size: 40px; color: rgba(30,27,24,.75); opacity: 0; }
#bub .c i { font-style: normal; color: var(--org); }
#cursor { position: absolute; left: 0; top: 0; width: 56px; height: 56px; opacity: 0; filter: drop-shadow(0 6px 8px rgba(0,0,0,.25)); }
#chars { position: absolute; left: 248px; top: 868px; width: 585px; height: 1042px; }
#charS { position: absolute; inset: 0; }
#charS img { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; }
#shadow { position: absolute; left: 380px; top: 1458px; width: 320px; height: 40px; border-radius: 50%; background: rgba(120,60,30,.22);
  filter: blur(12px); opacity: 0; }
.spk { position: absolute; width: 16px; height: 16px; background: var(--org); border-radius: 3px; transform: rotate(45deg); opacity: 0; }
'''

POSES = ["netral", "lambai", "tunjuk", "mikir", "kaget", "keren", "bicara", "kedip"]
imgs = "".join(f'<img id="p_{p}" src="pose/pose_{i}_{p}.png">' for i, p in enumerate(POSES))
BLOBS = {"bgA": [("#FFB48A", 120, 260, 620), ("#FF8C6B", 620, 900, 560), ("#FFD9B0", 200, 1350, 640)],
         "bgB": [("#A9CFFF", 80, 300, 620), ("#FFB48A", 640, 960, 520), ("#BFE3FF", 260, 1380, 620)],
         "bgC": [("#D5B8FF", 140, 240, 600), ("#FF9E80", 600, 880, 540), ("#E7C9FF", 220, 1360, 640)],
         "bgD": [("#FFB48A", 120, 260, 620), ("#FF8C6B", 620, 900, 560), ("#FFD9B0", 200, 1350, 640)]}
bg = "".join(f'<div class="bg" id="{k}">' + "".join(
    f'<i style="background:{c};left:{x}px;top:{y}px;width:{s}px;height:{s}px;opacity:.75"></i>' for c, x, y, s in v) + "</div>"
    for k, v in BLOBS.items())
SPK = [(170, 470), (900, 460), (130, 820), (930, 800), (540, 440), (300, 900), (780, 900)]
CAPS = [("capA", 1130, [(16, "dibongkar", True), (17, "pakai"), (18, "scroll")]),
        ("capB", 1130, [(22, "jalan"), (23, "kayak"), (24, "film", True)]),
        ("capC", 1130, [(28, "dimasuki", True), (29, "calon"), (30, "pembeli")]),
        ("capD", 1000, [(35, "aku", True), (36, "yang"), (37, "bikin")])]
caps = "".join(f'<div class="cap" id="{cid}" style="top:{y}px">' + "".join(
    f'<span id="{cid}w{w[0]}"{" class=k" if len(w) > 2 else ""}>{w[1]}</span>' for w in ws) + "</div>" for cid, y, ws in CAPS)
STRIKE = "M60 110 L760 330 M70 330 L770 100 M40 220 C200 170 300 280 420 210 C540 140 640 270 790 210"
URLS = ["aurum.id", "kaldera-logistics.id", "rimbunsentul.id"]
body = f'''
  {bg}
  <div id="cam">
    <div class="h" id="h1a" style="top:290px">Website kamu cuma jadi</div>
    <div class="h" id="h1b" style="top:380px"><i>brosur online?</i></div>
    <div class="h" id="h2" style="top:300px"><span class="n">1</span>Produk <i>3D</i></div>
    <div class="h" id="h3" style="top:300px"><span class="n">2</span>Scroll <i>sinematik</i></div>
    <div class="h" id="h4" style="top:300px"><span class="n">3</span>Bisa <i>dimasuki</i></div>
    <div class="h" id="h5" style="top:300px">Ini <i>website 3D.</i></div>
    <div class="h" id="h6a" style="top:280px;font-size:76px">Produk kamu layak</div>
    <div class="h" id="h6b" style="top:368px;font-size:76px"><i>dilihat kayak gini.</i></div>
    <div id="stage">
      <div class="win" id="flat"><div class="bar"><b></b><b></b><b></b><div class="url"><span style="opacity:1">brosur-kamu.com</span></div></div>
        <div class="lbl">SIMULASI</div>
        <div class="body"><div class="g" style="width:60%;height:44px"></div><div class="g" style="width:85%;height:20px"></div>
        <div class="g" style="width:70%;height:20px"></div><div class="g" style="width:100%;height:150px;margin-top:26px"></div></div></div>
      <svg id="strike" viewBox="0 0 820 430"><path d="{STRIKE}"/></svg>
      <div id="stick">pengunjung <i>cepat pergi</i></div>
      <div class="win" id="web"><div class="bar"><b></b><b></b><b></b>
          <div class="url">{"".join(f'<span id="u{k}">{u}</span>' for k, u in enumerate(URLS))}</div></div>
        <div class="lbl">DEMO KARYA</div>
        <video id="scr" class="clip" src="assets/screen.mp4" data-start="{T[10]}" data-duration="{round(T[31] - T[10] + 0.1, 3)}" data-track-index="1" muted playsinline></video>
      </div>
      <div id="demo"><span>DEMO KARYA ENDRICHTECH</span></div>
      {"".join(f'<div class="still" id="s{k + 1}"><div class="bar"><b></b><b></b><b></b></div><img src="assets/still_{n}.jpg"></div>' for k, n in enumerate(["watch", "log", "int"]))}
      <div id="bub"><div class="a">DM aku, ketik</div><div class="p" id="dm3d">&ldquo;3D&rdquo;</div>
        <div class="c" id="bubc">kita bahas website kamu <i>hari ini</i></div></div>
    </div>
    {caps}
    {"".join(f'<div class="spk" style="left:{a}px;top:{b}px"></div>' for a, b in SPK)}
    <div id="shadow"></div>
    <div id="chars"><div id="charS">{imgs}</div></div>
    <svg id="cursor" viewBox="0 0 24 24"><path d="M4 2 L4 19 L8.5 15 L11.5 22 L14.5 20.7 L11.6 14 L18 14 Z" fill="#1E1B18" stroke="#FFF" stroke-width="1.4"/></svg>
    <div id="wm">Endrich<i>Tech</i></div>
  </div>
'''

js = f'''
    var T = {T};
    var TRACK = {track};
    var EMPH = {EMPH_T};
    TRACK.forEach(function (e) {{ tl.set("#charS img:not(#p_" + e[1] + ")", {{ opacity: 0 }}, q(e[0])); tl.set("#p_" + e[1], {{ opacity: 1 }}, q(e[0])); }});
    // chibi: big under the brochure, corner mascot while the demos play, big again for the CTA
    tl.set("#chars", {{ transformOrigin: "50% 100%", scale: 0.58, y: -430 }}, 0);
    tl.set("#shadow", {{ opacity: 1 }}, 0);
    tl.fromTo("#charS", {{ y: 600 }}, {{ y: 0, duration: 0.5, ease: "back.out(1.4)" }}, 0);
    tl.to("#chars", {{ x: 320, y: -430, scale: 0.34, duration: 0.5, ease: "power3.inOut" }}, q(T[10] - 0.1));
    tl.to("#shadow", {{ x: 320, scaleX: 0.55, duration: 0.5, ease: "power3.inOut" }}, q(T[10] - 0.1));
    tl.to("#chars", {{ x: 0, y: -430, scale: 0.58, duration: 0.55, ease: "back.out(1.3)" }}, q(T[38] - 0.1));
    tl.to("#shadow", {{ x: 0, scaleX: 1, duration: 0.55, ease: "power3.out" }}, q(T[38] - 0.1));
    EMPH.forEach(function (t) {{ tl.fromTo("#charS", {{ scaleY: 0.93, scaleX: 1.05 }}, Object.assign({{ scaleY: 1, scaleX: 1, duration: 0.35, ease: "back.out(3)", transformOrigin: "50% 100%" }}, NI), q(t)); }});
    // background blobs drift; tint per chapter
    document.querySelectorAll(".bg i").forEach(function (b, k) {{
      tl.fromTo(b, {{ x: 0, y: 0 }}, {{ x: (k % 2 ? -80 : 70), y: (k % 3 ? 60 : -50), duration: 6.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, 0);
    }});
    [["#bgB", T[19] - 0.2], ["#bgC", T[25] - 0.2], ["#bgD", T[38] - 0.2]].forEach(function (b) {{ tl.fromTo(b[0], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, q(b[1])); }});
    // HOOK: headline + brochure site, scribbled out, sticker
    rise("#h1a", 0.05, 0.35); rise("#h1b", T[4] - 0.05, 0.4, {{ y: 50, rotation: -2 }});
    tl.set("#flat", {{ transformOrigin: "50% 50%" }}, 0);
    tl.fromTo("#flat", {{ opacity: 0, y: 80, rotationX: 18 }}, {{ opacity: 1, y: 0, rotationX: 0, duration: 0.5, ease: "power3.out" }}, 0.0);
    var sp = document.querySelector("#strike path"), L = Math.ceil(sp.getTotalLength()) + 2; sp.style.strokeDasharray = L;
    tl.set("#strike", {{ opacity: 1 }}, q(T[6]));
    tl.fromTo(sp, {{ strokeDashoffset: L }}, {{ strokeDashoffset: 0, duration: 0.6, ease: "power1.inOut" }}, q(T[6]));
    tl.fromTo("#stick", {{ opacity: 0, scale: 0.5, rotation: 0 }}, {{ opacity: 1, scale: 1, rotation: -5, duration: 0.32, ease: "back.out(2.2)" }}, q(T[8]));
    hide("#h1a, #h1b, #stick", T[10] - 0.2, 0.15);
    tl.to("#flat, #strike", {{ rotationY: 90, opacity: 0, duration: 0.22, ease: "power2.in" }}, q(T[10] - 0.22));
    // DEMOS: browser card flips in, urls follow the clip cuts (watch 3.24 s, logistics 2.4 s, housing)
    tl.set("#web", {{ transformOrigin: "50% 50%" }}, 0);
    tl.fromTo("#web", {{ opacity: 0, rotationY: -90, scale: 0.9 }}, {{ opacity: 1, rotationY: 0, scale: 1, duration: 0.45, ease: "back.out(1.3)" }}, q(T[10]));
    tl.fromTo("#web", {{ y: 0 }}, {{ y: -10, duration: 2.0, yoyo: true, repeat: 3, ease: "sine.inOut" }}, q(T[10] + 0.5));
    var C1 = T[10] + 3.267, C2 = T[10] + 5.667;
    [["#u0", T[10], C1], ["#u1", C1, C2], ["#u2", C2, 99]].forEach(function (u) {{ tl.set(u[0], {{ opacity: 1 }}, q(u[1])); if (u[2] < 99) tl.set(u[0], {{ opacity: 0 }}, q(u[2])); }});
    [C1, C2].forEach(function (c) {{ tl.fromTo("#web", {{ scale: 0.97 }}, Object.assign({{ scale: 1, duration: 0.35, ease: "back.out(2.5)" }}, NI), q(c)); }});
    rise("#h2", T[10], 0.4); hide("#h2", T[19] - 0.15, 0.12);
    rise("#h3", T[19], 0.4); hide("#h3", T[25] - 0.15, 0.12);
    rise("#h4", T[25], 0.4); hide("#h4", T[31] - 0.15, 0.12);
    // scroll cursor on the watch, click on the housing
    tl.fromTo("#cursor", {{ opacity: 0, x: 700, y: 760 }}, {{ opacity: 1, duration: 0.2 }}, q(T[16]));
    tl.to("#cursor", {{ y: 900, duration: 0.8, ease: "power2.inOut" }}, q(T[16] + 0.1));
    hide("#cursor", T[18] + 0.3, 0.15);
    tl.fromTo("#cursor", {{ opacity: 0, x: 500, y: 980 }}, Object.assign({{ opacity: 1, duration: 0.2 }}, NI), q(T[28] - 0.3));
    tl.to("#cursor", {{ x: 760, y: 700, duration: 0.5, ease: "power2.inOut" }}, q(T[28] - 0.2));
    tl.to("#cursor", {{ scale: 0.8, duration: 0.08, yoyo: true, repeat: 1 }}, q(T[28] + 0.35));
    hide("#cursor", T[30], 0.15);
    // keyword captions, word by word; key word pops in its orange box
    [["capA", [16, 17, 18], T[19] - 0.12], ["capB", [22, 23, 24], T[25] - 0.12], ["capC", [28, 29, 30], T[31] - 0.12], ["capD", [35, 36, 37], T[38] - 0.15]].forEach(function (c) {{
      c[1].forEach(function (i) {{
        var s = "#" + c[0] + "w" + i;
        if (document.querySelector(s).className === "k") pop(s, T[i], 0.3); else rise(s, T[i], 0.2, {{ y: 16 }});
      }});
      hide("#" + c[0] + " span", c[2], 0.12);
    }});
    // PROOF: card shrinks away, three stills fan out
    tl.to("#web", {{ scale: 0.6, opacity: 0, duration: 0.3, ease: "power2.in" }}, q(T[31] - 0.1));
    rise("#h5", T[31], 0.4, {{ y: 50, scale: 1.1 }});
    [["#s1", -7, -200], ["#s2", 0, 0], ["#s3", 7, 200]].forEach(function (s, k) {{
      tl.fromTo(s[0], {{ opacity: 0, x: -s[2], y: 120, rotation: 0, scale: 0.8 }}, {{ opacity: 1, x: 0, y: 0, rotation: s[1], scale: 1, duration: 0.45, ease: "back.out(1.6)" }}, q(T[32] + 0.1 * k));
    }});
    rise("#demo", T[33], 0.3, {{ y: 10 }});
    hide("#h5, #s1, #s2, #s3, #demo", T[38] - 0.2, 0.15);
    // CTA: headline, DM bubble, "3D" pill, handwriting line, sparkles
    rise("#h6a", T[38], 0.35); rise("#h6b", T[40] - 0.05, 0.4, {{ y: 40, rotation: -2 }});
    tl.set("#bub", {{ transformOrigin: "50% 100%" }}, 0);
    tl.fromTo("#bub", {{ opacity: 0, scale: 0.6, y: 40 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(1.8)" }}, q(T[44] - 0.1));
    tl.fromTo("#dm3d", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.6)" }}, q(T[47]));
    tl.fromTo("#bubc", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power2.out" }}, q(T[48]));
    tl.fromTo("#dm3d", {{ scale: 1 }}, Object.assign({{ scale: 1.07, duration: 0.45, yoyo: true, repeat: 5, ease: "sine.inOut" }}, NI), q(T[53] + 0.4));
    document.querySelectorAll(".spk").forEach(function (s, k) {{
      tl.fromTo(s, {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1.5, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out" }}, q(T[47] + 0.07 * k));
    }});
    tl.fromTo("#cam", {{ scale: 1 }}, Object.assign({{ scale: 1.03, duration: 4.0, ease: "power1.inOut" }}, NI), q(T[53]));
'''

html = gaya_common.page("iklan-web3d", css, body, js)
(HERE / "public" / "index.html").write_text(html, encoding="utf-8")
print("ok", len(track), "pose events")
