# Style template 07 · SETUP — motion graphics living inside a device on a desk (ref-moti0n-9/10/11): a CSS desk scene
# (wall, window light, monitor, lamp, plant), a top overlay title, the camera pushes into the monitor where a
# blueprint grid + UI animates, objects fly out of the screen toward the viewer, and a 3D keycap CTA closes it.
# No footage needed; swap #room for real room footage later if the creator records his own desk.
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from gaya_common import page, words  # noqa: E402

T = words("setup")

css = '''
:root { --cy:#6FD3FF; --am:#FFB054; --w:#F6F1EA; }
html, body, #root { background: #0C0B0D; color: var(--w); font-family: "IDBold"; }
#cam { position: absolute; inset: 0; transform-origin: 540px 830px; }
#wall { position: absolute; inset: 0; background: radial-gradient(ellipse 70% 45% at 75% 45%, #3A2A1C 0%, #1A1512 45%, #0C0B0D 100%); }
.ray { position: absolute; top: -200px; width: 120px; height: 1700px; background: linear-gradient(180deg, rgba(255,200,140,.10), rgba(255,200,140,0)); transform: rotate(28deg); transform-origin: 0 0; }
#glow { position: absolute; left: 640px; top: 640px; width: 520px; height: 520px; border-radius: 50%; background: radial-gradient(circle, rgba(255,176,84,.45) 0%, rgba(255,176,84,0) 70%); }
#lamp { position: absolute; left: 860px; top: 760px; width: 140px; height: 90px; background: linear-gradient(180deg, #2A2420, #141110); border-radius: 70px 70px 10px 10px; }
#lamp:after { content: ""; position: absolute; left: 30px; top: 86px; width: 80px; height: 14px; border-radius: 50%; background: #FFD9A0; box-shadow: 0 0 40px 18px rgba(255,190,110,.6); }
#lampArm { position: absolute; left: 925px; top: 845px; width: 12px; height: 380px; background: #1A1715; }
#pot { position: absolute; left: 70px; top: 1110px; width: 130px; height: 120px; background: linear-gradient(180deg, #C9B8A2, #8E7C68); border-radius: 8px 8px 30px 30px; }
.leaf { position: absolute; width: 70px; height: 190px; background: linear-gradient(180deg, #3F6B3A, #1E3A1E); border-radius: 50% 50% 50% 50% / 70% 70% 30% 30%; transform-origin: 50% 100%; }
#desk { position: absolute; left: -40px; top: 1220px; width: 1160px; height: 760px; background: linear-gradient(180deg, #6B4A33 0%, #3D2A1E 30%, #1E1510 100%); }
#desk:before { content: ""; position: absolute; left: 0; top: 0; width: 100%; height: 10px; background: #8A6446; }
#mon { position: absolute; left: 240px; top: 640px; width: 600px; height: 380px; background: #0A0A0B; border-radius: 16px; padding: 14px; box-shadow: 0 30px 80px rgba(0,0,0,.6), 0 0 120px rgba(111,211,255,.18); }
#neck { position: absolute; left: 515px; top: 1018px; width: 50px; height: 170px; background: linear-gradient(90deg, #2A2A2E, #121214); }
#base { position: absolute; left: 420px; top: 1176px; width: 240px; height: 44px; border-radius: 50%; background: #18181B; }
#kb { position: absolute; left: 290px; top: 1270px; width: 500px; height: 80px; border-radius: 12px; background: repeating-linear-gradient(90deg, #232326 0 34px, #18181A 34px 38px); box-shadow: 0 10px 20px rgba(0,0,0,.5); }
#mug { position: absolute; left: 820px; top: 1180px; width: 90px; height: 100px; background: linear-gradient(90deg, #E9E2D6, #B9AE9E); border-radius: 6px 6px 18px 18px; }
#scr { position: relative; width: 572px; height: 352px; border-radius: 6px; overflow: hidden; background: linear-gradient(135deg, #1B2B44 0%, #0E1626 100%); }
#wp { position: absolute; inset: 0; background: radial-gradient(ellipse 60% 70% at 70% 30%, rgba(255,176,84,.35), rgba(0,0,0,0) 70%); }
#clock { position: absolute; left: 30px; top: 24px; font-family: "IDSemi"; font-size: 22px; color: rgba(246,241,234,.8); }
#grid { position: absolute; inset: 0; opacity: 0; background-color: #0B2A55;
  background-image: linear-gradient(rgba(111,211,255,.22) 1px, transparent 1px), linear-gradient(90deg, rgba(111,211,255,.22) 1px, transparent 1px);
  background-size: 22px 22px; }
#dim { position: absolute; left: 20px; top: 16px; font-family: "IDSemi"; font-size: 13px; letter-spacing: .2em; color: var(--cy); opacity: 0; }
#frame { position: absolute; left: 16px; top: 40px; width: 540px; height: 296px; border: 2px dashed rgba(111,211,255,.7); opacity: 0; }
#idea { position: absolute; left: 186px; top: 116px; width: 200px; height: 120px; border: 2px solid var(--cy); border-radius: 14px; background: rgba(11,42,85,.9);
  text-align: center; opacity: 0; box-shadow: 0 0 30px rgba(111,211,255,.35); }
#idea b { display: block; font-family: "IDBlack"; font-size: 54px; color: var(--w); margin-top: 14px; line-height: 1; }
#idea span { font-family: "IDSemi"; font-size: 14px; letter-spacing: .25em; color: var(--cy); }
#line24 { position: absolute; left: 60px; top: 300px; width: 452px; height: 10px; border-radius: 5px; background: rgba(111,211,255,.18); opacity: 0; }
#line24 i { display: block; width: 100%; height: 100%; border-radius: 5px; background: var(--am); transform-origin: 0 50%; }
#line24 em { position: absolute; top: -26px; font-style: normal; font-family: "IDSemi"; font-size: 14px; color: var(--cy); }
.vid { position: absolute; top: 1240px; width: 250px; height: 400px; border-radius: 22px; opacity: 0; overflow: hidden; border: 3px solid rgba(255,255,255,.85);
  box-shadow: 0 30px 60px rgba(0,0,0,.6); }
.vid .pl { position: absolute; left: 85px; top: 140px; width: 80px; height: 80px; border-radius: 50%; background: rgba(255,255,255,.9); }
.vid .pl:after { content: ""; position: absolute; left: 32px; top: 22px; border-left: 26px solid #111; border-top: 18px solid transparent; border-bottom: 18px solid transparent; }
.vid .lb { position: absolute; left: 20px; bottom: 22px; font-family: "IDBlack"; font-size: 30px; color: #fff; }
.vid .bar { position: absolute; left: 20px; bottom: 70px; width: 140px; height: 10px; border-radius: 5px; background: rgba(255,255,255,.6); }
#v1 { left: 70px; background: linear-gradient(160deg, #FF8A3D, #8E1F6B); }
#v2 { left: 415px; background: linear-gradient(160deg, #6FD3FF, #2340A8); }
#v3 { left: 760px; background: linear-gradient(160deg, #C6F432, #2E7D4F); }
#ttl { position: absolute; left: 0; top: 270px; width: 1080px; text-align: center; }
#ttl div { position: absolute; left: 0; width: 1080px; opacity: 0; font-family: "IDBlack"; font-size: 92px; letter-spacing: -.02em; line-height: 1.05; text-shadow: 0 8px 40px rgba(0,0,0,.8); }
#ttl small { display: block; font-family: "IDSemi"; font-size: 28px; letter-spacing: .3em; color: var(--am); margin-bottom: 18px; }
#ttl .ac { color: var(--cy); }
#kp { position: absolute; inset: 0; opacity: 0; background: radial-gradient(ellipse 80% 55% at 50% 60%, #1E2A3A 0%, #08090C 100%); perspective: 1400px; }
#kpPlane { position: absolute; left: 40px; top: 760px; width: 1000px; height: 800px; transform: rotateX(46deg); transform-origin: 50% 50%; }
.row { display: flex; gap: 18px; justify-content: center; margin-bottom: 22px; }
.key { width: 140px; height: 140px; border-radius: 22px; background: linear-gradient(180deg, #3A3D44, #24262B); border-bottom: 22px solid #121317;
  box-shadow: 0 18px 30px rgba(0,0,0,.6); font-family: "IDBlack"; font-size: 70px; color: #D9DCE2; display: flex; align-items: center; justify-content: center; }
.key.blank { opacity: .55; }
#kpGlow { position: absolute; left: 90px; top: 1060px; width: 900px; height: 260px; border-radius: 50%; background: radial-gradient(ellipse, rgba(111,211,255,.45), rgba(111,211,255,0) 70%); opacity: 0; }
#cur { position: absolute; left: 0; top: 0; width: 60px; height: 60px; opacity: 0; }
#end { position: absolute; inset: 0; background: radial-gradient(ellipse 90% 60% at 50% 40%, #1A2330 0%, #0A0B0E 100%); opacity: 0; }
#end .n { position: absolute; left: 0; width: 1080px; top: 720px; text-align: center; font-family: "IDSemi"; font-size: 40px; letter-spacing: .3em; color: rgba(246,241,234,.6); }
#end .t { position: absolute; left: 0; width: 1080px; top: 790px; text-align: center; font-family: "IDBlack"; font-size: 190px; color: var(--cy); letter-spacing: -.02em; }
#end .d { position: absolute; left: 0; width: 1080px; top: 1030px; text-align: center; font-family: "IDSemi"; font-size: 36px; color: rgba(246,241,234,.7); }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-family: "IDBlack"; font-size: 34px; color: var(--w); }
#brand b { color: var(--cy); font-weight: normal; }
'''

LEAVES = [(95, 930, -25), (125, 910, -5), (150, 925, 18), (110, 950, -40), (165, 950, 38)]
ROWS = [["", "", "", "", "", ""], list("FOLLOW"), ["", "", "", "", "", ""]]
keys = "".join('<div class="row">' + "".join(f'<div class="key{"" if c else " blank"}"{" data-k" if c else ""}>{c}</div>' for c in r) + "</div>" for r in ROWS)
body = f'''
  <div id="cam">
    <div id="wall"></div>
    {"".join(f'<div class="ray" style="left:{x}px"></div>' for x in (520, 700, 880))}
    <div id="glow"></div><div id="lampArm"></div><div id="lamp"></div>
    {"".join(f'<div class="leaf" style="left:{x}px;top:{y}px;transform:rotate({r}deg)"></div>' for x, y, r in LEAVES)}
    <div id="pot"></div>
    <div id="desk"></div>
    <div id="neck"></div><div id="base"></div>
    <div id="mon"><div id="scr">
      <div id="wp"></div><div id="clock">09:41</div>
      <div id="grid"></div><div id="dim">LAYAR &middot; 24&quot; &middot; 1920&times;1080</div><div id="frame"></div>
      <div id="idea"><b>1</b><span>IDE</span></div>
      <div id="line24"><em style="left:0">00:00</em><em style="right:0">24:00</em><i id="l24"></i></div>
    </div></div>
    <div id="kb"></div><div id="mug"></div>
  </div>
  <div id="brand">Endrich<b>Tech</b></div>
  <div class="vid" id="v1"><div class="pl"></div><div class="bar"></div><div class="lb">VIDEO 1</div></div>
  <div class="vid" id="v2"><div class="pl"></div><div class="bar"></div><div class="lb">VIDEO 2</div></div>
  <div class="vid" id="v3"><div class="pl"></div><div class="bar"></div><div class="lb">VIDEO 3</div></div>
  <div id="kp"><div id="kpGlow"></div><div id="kpPlane">{keys}</div></div>
  <div id="ttl">
    <div id="t1"><small>N&ordm; 07 &middot; SETUP</small>Meja kerja<br>biasa aja.</div>
    <div id="t2"><small>DARI LAYAR KECIL INI</small><span class="ac">1 ide</span> &rarr; 3 video</div>
    <div id="t3"><small>DALAM SEHARI</small>Mau tahu<br><span class="ac">caranya?</span></div>
    <div id="t4"><small>SATU KLIK</small>Tekan <span class="ac">follow.</span></div>
  </div>
  <div id="end"><div class="n">GAYA 07</div><div class="t">SETUP</div><div class="d">motion graphic di dalam layar &middot; meja kerja &middot; CTA keypad 3D</div></div>
'''

js = f'''
    var T = {T};
    // A: establishing desk, slow drift; top overlay title
    tl.fromTo("#cam", {{ scale: 1.08, x: 30 }}, {{ scale: 1, x: 0, duration: 3.6, ease: "power1.out" }}, 0);
    tl.fromTo("#glow", {{ opacity: 0.7 }}, {{ opacity: 1, duration: 0.5, yoyo: true, repeat: 5, ease: "sine.inOut" }}, 0.2);
    rise("#t1", T[0], 0.45);
    hide("#t1", T[6] - 0.15, 0.15);
    // B: push into the monitor, blueprint takes over the screen
    tl.to("#cam", {{ scale: 1.7, y: -60, duration: 0.9, ease: "power3.inOut" }}, q(T[6] - 0.05));
    tl.fromTo("#grid", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(T[7]));
    cut("#dim", T[8], 1);
    tl.fromTo("#frame", {{ opacity: 0, scale: 1.08 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power2.out" }}, q(T[9]));
    rise("#t2", T[7], 0.4);
    // C: 1 idea -> 3 videos fly out of the screen toward the viewer
    pop("#idea", T[11] - 0.05, 0.35);
    tl.to("#frame", {{ opacity: 0, duration: 0.2 }}, q(T[13]));
    tl.to("#idea", {{ scale: 1.15, duration: 0.15, yoyo: true, repeat: 1 }}, q(T[14]));
    [["#v1", -8, 0], ["#v2", 0, 0.1], ["#v3", 8, 0.2]].forEach(function (v) {{
      tl.fromTo(v[0], {{ opacity: 0, scale: 0.25, y: -420, x: function (i, el) {{ return 540 - (el.offsetLeft + 125); }}, rotation: 0 }},
        {{ opacity: 1, scale: 1, y: 0, x: 0, rotation: v[1], duration: 0.55, ease: "back.out(1.5)" }}, q(T[15] + v[2]));
      tl.to(v[0], {{ y: -14, duration: 0.6, yoyo: true, repeat: 1, ease: "sine.inOut" }}, q(T[15] + 0.6 + v[2]));
    }});
    cut("#line24", T[17], 1);
    tl.fromTo("#l24", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power2.inOut" }}, q(T[17]));
    hide("#t2", T[19] - 0.15, 0.12);
    // D: pull back, title, then cut to the 3D keypad CTA
    tl.to("#cam", {{ scale: 1.25, y: 0, duration: 0.6, ease: "power2.inOut" }}, q(T[19] - 0.1));
    hide(".vid", T[19] - 0.1, 0.2);
    rise("#t3", T[19], 0.4);
    hide("#t3", T[22] - 0.25, 0.12);
    tl.fromTo("#kp", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, q(T[22] - 0.25));
    tl.fromTo("#kpPlane", {{ y: 160, rotationX: 60 }}, {{ y: 0, rotationX: 46, duration: 0.6, ease: "power3.out" }}, q(T[22] - 0.25));
    rise("#t4", T[22] - 0.1, 0.35);
    document.querySelectorAll("[data-k]").forEach(function (k, i) {{
      var t = q(T[23] + 0.12 * i);
      tl.to(k, {{ y: 16, borderBottomWidth: 6, duration: 0.07, ease: "power2.in" }}, t);
      tl.set(k, {{ backgroundImage: "linear-gradient(180deg, #8FE1FF, #3AA8E0)", color: "#06121C" }}, t);
      tl.to(k, {{ y: 0, borderBottomWidth: 22, duration: 0.18, ease: "back.out(2)" }}, t + 0.08);
    }});
    tl.fromTo("#kpGlow", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(T[23] + 0.7));
    tl.fromTo("#kpPlane", {{ scale: 1 }}, Object.assign({{ scale: 1.04, duration: 0.15, yoyo: true, repeat: 1 }}, NI), q(T[23] + 0.7));
    // end card
    tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, q(12.3));
    rise("#end .t", 12.35, 0.45, {{ y: 60 }});
    hide("#t4", 12.3, 0.1);
'''

(HERE / "public" / "index.html").write_text(page("gaya-setup", css, body, js), encoding="utf-8")
print("ok")
