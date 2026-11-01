# Style template 06 · AVATAR — the creator's chibi character presents (ref-moti0n-6/7/8): character at the bottom
# with pose swaps on VO beats, lip-flap (netral/bicara) driven by VO loudness, blinks, idle bob; editorial sans +
# serif-italic accent words; one mood colour per chapter (orange -> red -> blueprint blue -> warm neon); floating
# dark UI cards; a sketch that turns into neon.  Poses: public/pose/*.png (from karakter/pose_fix).
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from gaya_common import VO_START, page, words  # noqa: E402

T = words("avatar")
FPS = 30

# --- pose track: emphasis poses on beats, lip-flap + blinks while netral -----------------------------------------
raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(HERE / "public" / "vo.mp3"), "-ac", "1", "-ar", "48000",
                               "-f", "s16le", "-"])
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
hop = 48000 // FPS
db = np.array([20 * np.log10(np.sqrt((x[i:i + hop] ** 2).mean()) + 1e-9) for i in range(0, len(x) - hop, hop)])
loud = db > db.max() - 22
# syllable-ish flap: open while the envelope sits above its own short moving average
sm = np.convolve(db, np.ones(7) / 7, mode="same")
open_ = loud & (db >= sm - 1.0)
EMPH = [(0.0, "netral"), (T[0] - 0.05, "lambai"), (T[2] - 0.1, "netral"), (T[4] + 0.45, "kedip"), (T[4] + 0.8, "netral"),
        (T[5] - 0.05, "tunjuk"), (T[8], "netral"), (T[13] - 0.05, "mikir"), (T[18] - 0.05, "kaget"), (T[21] - 0.05, "keren")]
BLINK = [2.55, 6.95]


def base(t):
    return [p for s, p in EMPH if s <= t + 1e-6][-1]


track, prev, hold = [], None, 0
for f in range(int(12.3 * FPS)):
    t = f / FPS
    p = base(t)
    if p == "netral":
        want = "bicara" if open_[min(f, len(open_) - 1)] and t > VO_START else "netral"
        # keep each mouth state >= 2 frames so the flap reads as talking, not flicker
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
:root { --cream:#FFF4E6; }
html, body, #root { background: #1A0A06; color: var(--cream); font-family: "IDBold"; }
.bg { position: absolute; inset: 0; opacity: 0; }
#bg1 { background: radial-gradient(ellipse 90% 60% at 50% 38%, #FF8A3D 0%, #E0531F 45%, #5A1A08 100%); opacity: 1; }
#bg2 { background: radial-gradient(ellipse 90% 60% at 50% 38%, #FF4B3E 0%, #B81E24 50%, #3A060A 100%); }
#bg3 { background: #123A7A; }
#bg3:before { content: ""; position: absolute; inset: 0;
  background-image: linear-gradient(rgba(255,255,255,.10) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,.10) 2px, transparent 2px);
  background-size: 60px 60px; }
#bg3:after { content: ""; position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 40%, rgba(80,150,255,.35) 0%, rgba(5,15,40,.85) 100%); }
#bg4 { background: radial-gradient(ellipse 80% 55% at 50% 33%, #FF6A3D 0%, #8E1F6B 45%, #1B0A2A 100%); }
#cam { position: absolute; inset: 0; transform-origin: 540px 262px; }
.tag { position: absolute; left: 70px; top: 262px; font-family: "IDSemi"; font-size: 30px; letter-spacing: .22em; color: rgba(255,244,230,.75); opacity: 0; }
.tag b { font-family: "SerifBI"; font-weight: normal; letter-spacing: 0; font-size: 36px; color: var(--cream); margin-right: 14px; }
#brand { position: absolute; right: 150px; top: 260px; font-family: "IDBlack"; font-size: 32px; color: var(--cream); }
#brand i { font-family: "SerifBI"; font-style: normal; color: #FFD6A8; }
.l { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; line-height: 1; }
.s { font-family: "IDBlack"; font-size: 96px; letter-spacing: -.02em; }
.it { font-family: "SerifBI"; font-size: 168px; letter-spacing: -.01em; }
#c1b { color: #FFE2B8; }
#c2c i { font-family: "SerifBI"; font-style: normal; color: #FFD0C4; font-size: 132px; }
#c3b { color: #BFE0FF; }
#c4b { color: #FFE66B; text-shadow: 0 0 24px rgba(255,90,200,.9), 0 0 60px rgba(255,90,40,.6); }
.card { position: absolute; background: rgba(18,12,14,.92); border: 1.5px solid rgba(255,255,255,.12); border-radius: 26px; padding: 26px 30px;
  box-shadow: 0 30px 60px rgba(0,0,0,.45); font-family: "IDSemi"; color: #F4EDE6; opacity: 0; }
.card .k { font-size: 22px; letter-spacing: .18em; color: rgba(244,237,230,.55); margin-bottom: 12px; }
.card .v { font-family: "IDBold"; font-size: 36px; }
.bar { margin-top: 16px; height: 12px; border-radius: 6px; background: rgba(255,255,255,.12); overflow: hidden; }
.bar i { display: block; height: 100%; width: 100%; background: #FF5A4A; transform-origin: 0 50%; }
#cardV { left: 680px; top: 640px; }
#cardV .v { font-family: "SerifBI"; font-size: 46px; color: #FFD6A8; }
#cardA { left: 40px; top: 1040px; width: 330px; }
#cardB { left: 720px; top: 1180px; width: 320px; }
#cardB .v { font-size: 30px; line-height: 1.3; }
#cardB .ok { color: #7CF29A; }
#sk { position: absolute; left: 330px; top: 545px; width: 420px; height: 353px; opacity: 0; overflow: visible; }
#sk path { fill: none; stroke: #EAF4FF; stroke-width: 7; stroke-linecap: round; stroke-linejoin: round; }
#sk path.neon { stroke: #FFE66B; filter: drop-shadow(0 0 10px #FF4FD8) drop-shadow(0 0 26px #FF6A3D); }
#skFill { opacity: 0; }
#chars { position: absolute; left: 248px; top: 868px; width: 585px; height: 1042px; }
#charS { position: absolute; inset: 0; }
#charS img { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; }
#shadow { position: absolute; left: 340px; top: 1830px; width: 400px; height: 50px; border-radius: 50%; background: rgba(0,0,0,.35); filter: blur(14px); opacity: 0; }
.spk { position: absolute; width: 18px; height: 18px; background: #FFE66B; border-radius: 50%; box-shadow: 0 0 18px #FF4FD8; opacity: 0; }
#flash { position: absolute; inset: 0; background: #FFF6E8; opacity: 0; }
#end { position: absolute; inset: 0; background: radial-gradient(ellipse 90% 60% at 50% 35%, #2A1530 0%, #120A10 100%); opacity: 0; }
#end .n { position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; font-family: "IDSemi"; font-size: 40px; letter-spacing: .3em; color: rgba(255,244,230,.6); }
#end .t { position: absolute; left: 0; width: 1080px; top: 400px; text-align: center; font-family: "SerifBI"; font-size: 210px; color: #FFD6A8; }
#end .d { position: absolute; left: 0; width: 1080px; top: 660px; text-align: center; font-family: "IDSemi"; font-size: 36px; color: rgba(255,244,230,.7); }
#endImg { position: absolute; left: 307px; top: 860px; width: 466px; height: 830px; }
'''

POSES = ["netral", "lambai", "tunjuk", "mikir", "kaget", "keren", "bicara", "kedip"]
imgs = "".join(f'<img id="p_{p}" src="pose/pose_{i}_{p}.png">' for i, p in enumerate(POSES))
SPK = [(330, 520), (760, 560), (280, 820), (820, 800), (540, 430), (420, 700), (700, 690)]
LAMP = "M250 40 C330 40 380 100 380 165 C380 215 350 245 325 275 L315 315 L185 315 L175 275 C150 245 120 215 120 165 C120 100 170 40 250 40 Z"
body = f'''
  <div class="bg" id="bg1"></div><div class="bg" id="bg2"></div><div class="bg" id="bg3"></div><div class="bg" id="bg4"></div>
  <div id="cam">
    <div class="tag" id="tg1"><b>01</b>SAPA</div><div class="tag" id="tg2"><b>02</b>JANJI</div>
    <div class="tag" id="tg3"><b>03</b>CORETAN</div><div class="tag" id="tg4"><b>04</b>JADI KEREN</div>
    <div class="l s" id="c1a" style="top:340px">Halo, aku</div>
    <div class="l it" id="c1b" style="top:450px">Endrich</div>
    <div class="card" id="cardV"><div class="k">VERSI BARU</div><div class="v">kartun!</div></div>
    <div class="l s" id="c2a" style="top:330px">Mulai sekarang,</div>
    <div class="l s" id="c2b" style="top:440px;font-size:76px">aku yang nemenin kamu</div>
    <div class="l s" id="c2c" style="top:540px">belajar <i>AI.</i></div>
    <div class="card" id="cardA"><div class="k">KELAS AI &middot; HARI 1</div><div class="v">Prompt dasar</div><div class="bar"><i id="barI"></i></div></div>
    <div class="card" id="cardB"><div class="k">TUGAS</div><div class="v"><span class="ok">&#10003;</span> Bikin ringkasan<br><span class="ok">&#10003;</span> Cek fakta</div></div>
    <div class="l s" id="c3a" style="top:330px;font-size:80px">Dari yang tadinya</div>
    <div class="l it" id="c3b" style="top:420px;font-size:112px">cuma coretan&hellip;</div>
    <div class="l s" id="c4a" style="top:330px;font-size:80px">jadi sesuatu yang</div>
    <div class="l it" id="c4b" style="top:420px;font-size:112px">beneran keren.</div>
    <svg id="sk" viewBox="0 0 500 420">
      <path id="skFill" d="{LAMP}" style="fill:rgba(255,230,107,.18);stroke:none"/>
      <path class="d" d="{LAMP}"/>
      <path class="d" d="M195 345 L305 345 M205 375 L295 375 M230 405 L270 405"/>
      <path class="d" d="M215 245 L235 160 L250 215 L265 160 L285 245"/>
      <path class="d" d="M60 150 L20 140 M440 150 L480 140 M95 50 L65 20 M405 50 L435 20"/>
    </svg>
    {"".join(f'<div class="spk" style="left:{a}px;top:{b}px"></div>' for a, b in SPK)}
    <div id="shadow"></div>
    <div id="chars"><div id="charS">{imgs}</div></div>
    <div id="brand">Endrich<i>Tech</i></div>
  </div>
  <div id="flash"></div>
  <div id="end"><div class="n">GAYA 06</div><div class="t">Avatar</div><div class="d">karakter presenter &middot; editorial &middot; warna per bab</div>
    <img id="endImg" src="pose/end_lambai.png"></div>
'''

js = f'''
    var T = {T};
    var TRACK = {track};
    var EMPH = {EMPH_T};
    // pose track (seek-safe sets)
    TRACK.forEach(function (e) {{ tl.set("#charS img:not(#p_" + e[1] + ")", {{ opacity: 0 }}, q(e[0])); tl.set("#p_" + e[1], {{ opacity: 1 }}, q(e[0])); }});
    // entrance, idle bob, squash on each emphasis pose
    tl.set("#chars", {{ transformOrigin: "50% 100%" }}, 0);
    tl.fromTo("#chars", {{ y: 700 }}, {{ y: 0, duration: 0.55, ease: "back.out(1.4)" }}, 0.15);
    tl.fromTo("#shadow", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0.3);
    tl.fromTo("#charS", {{ y: 0 }}, {{ y: -10, duration: 0.6, yoyo: true, repeat: 17, ease: "sine.inOut" }}, 0.7);
    EMPH.forEach(function (t) {{ tl.fromTo("#chars", {{ scaleY: 0.94, scaleX: 1.04 }}, Object.assign({{ scaleY: 1, scaleX: 1, duration: 0.35, ease: "back.out(3)" }}, NI), q(t)); }});
    // chapter backgrounds + tags
    [["#bg2", T[5] - 0.1], ["#bg3", T[13] - 0.1], ["#bg4", T[18] - 0.05]].forEach(function (b) {{ tl.fromTo(b[0], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, q(b[1])); }});
    [["#tg1", 0.4, T[5] - 0.1], ["#tg2", T[5] - 0.1, T[13] - 0.1], ["#tg3", T[13] - 0.1, T[18] - 0.05], ["#tg4", T[18] - 0.05, 99]].forEach(function (g) {{
      rise(g[0], g[1], 0.3, {{ y: -16 }}); if (g[2] < 12.3) hide(g[0], g[2] - 0.12, 0.1); }});
    // ch1
    rise("#c1a", T[0], 0.35); rise("#c1b", T[2] - 0.05, 0.45, {{ y: 60, rotation: -3 }});
    tl.fromTo("#cardV", {{ opacity: 0, scale: 0.5, rotation: 0 }}, {{ opacity: 1, scale: 1, rotation: 5, duration: 0.35, ease: "back.out(2.2)" }}, q(T[4]));
    tl.fromTo("#cardV", {{ y: 0 }}, {{ y: -14, duration: 0.7, yoyo: true, repeat: 1, ease: "sine.inOut" }}, q(T[4] + 0.35));
    hide("#c1a, #c1b, #cardV", T[5] - 0.2, 0.15);
    // ch2
    rise("#c2a", T[5], 0.35); rise("#c2b", T[7], 0.35); rise("#c2c", T[11], 0.4);
    rise("#cardA", T[9], 0.45, {{ x: -120, y: 0, rotation: -6 }});
    tl.fromTo("#barI", {{ scaleX: 0 }}, {{ scaleX: 0.72, duration: 1.2, ease: "power2.out" }}, q(T[9] + 0.3));
    rise("#cardB", T[11] + 0.15, 0.45, {{ x: 120, y: 0, rotation: 6 }});
    tl.to("#cardA", {{ y: -12, duration: 0.6, yoyo: true, repeat: 1, ease: "sine.inOut" }}, q(T[10] + 0.2));
    tl.to("#cardB", {{ y: 12, duration: 0.5, yoyo: true, repeat: 1, ease: "sine.inOut" }}, q(T[12] + 0.1));
    hide("#c2a, #c2b, #c2c, #cardA, #cardB", T[13] - 0.2, 0.15);
    // ch3: sketch drawn on
    rise("#c3a", T[13], 0.35); rise("#c3b", T[16], 0.45, {{ y: 50, rotation: -2 }});
    cut("#sk", T[14], 1);
    document.querySelectorAll("#sk .d").forEach(function (p, k) {{
      var L = Math.ceil(p.getTotalLength()) + 2; p.style.strokeDasharray = L;
      tl.fromTo(p, {{ strokeDashoffset: L }}, {{ strokeDashoffset: 0, duration: 0.55, ease: "power1.inOut" }}, q(T[14] + 0.3 * k));
    }});
    tl.fromTo("#sk", {{ rotation: -2 }}, {{ rotation: 2, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut" }}, q(T[14]));
    hide("#c3a, #c3b", T[18] - 0.15, 0.12);
    // ch4: flash -> neon
    tl.fromTo("#flash", {{ opacity: 0.85 }}, Object.assign({{ opacity: 0, duration: 0.35, ease: "power2.out" }}, NI), q(T[18] - 0.05));
    tl.set("#sk .d", {{ attr: {{ class: "d neon" }} }}, q(T[18] - 0.05));
    tl.fromTo("#skFill", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(T[18]));
    tl.fromTo("#sk", {{ scale: 0.9 }}, Object.assign({{ scale: 1.08, duration: 0.5, ease: "back.out(2)" }}, NI), q(T[18] - 0.05));
    tl.to("#sk", {{ opacity: 0.55, duration: 0.06, yoyo: true, repeat: 5, ease: "steps(1)" }}, q(T[18] + 0.4));
    rise("#c4a", T[18], 0.35); rise("#c4b", T[21] - 0.05, 0.4, {{ y: 60, scale: 1.2 }});
    document.querySelectorAll(".spk").forEach(function (s, k) {{
      tl.fromTo(s, {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1.4, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out" }}, q(T[21] + 0.07 * k));
    }});
    tl.fromTo("#cam", {{ scale: 1 }}, {{ scale: 1.05, duration: 2.6, ease: "power1.inOut" }}, q(T[18] - 0.05));
    // end card
    tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, q(12.3));
    rise("#end .t", 12.35, 0.45, {{ y: 60 }});
    tl.set("#endImg", {{ transformOrigin: "50% 100%" }}, 0);
    tl.fromTo("#endImg", {{ y: 500 }}, {{ y: 0, duration: 0.5, ease: "back.out(1.4)" }}, q(12.4));
    tl.fromTo("#endImg", {{ rotation: -2 }}, {{ rotation: 2, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut" }}, q(12.9));
'''

(HERE / "public" / "index.html").write_text(page("gaya-avatar", css, body, js), encoding="utf-8")
print("ok", len(track), "pose events")
