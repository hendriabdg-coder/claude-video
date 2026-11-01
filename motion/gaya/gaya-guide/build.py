# Style template 09 · GUIDE — ATM of ref-moti0n-15 (+ bits of 16/17/18): warm cream canvas, mono HUD on top
# ("// 02 · tulis ide" + a counter that changes with the content), a keyword headline that grows word by word with
# ONE serif-italic accent word on a lime highlighter, numbered props with a black step badge, a halftone dot wipe
# into the proof/end card, and the creator's ANIMATED chibi (karakter/Animasi Karakter, green screen) presenting
# from the bottom.  The chibi is keyed and overlaid in ffmpeg (motion/gaya/chibi_track.py), so the HTML leaves the
# bottom free for it; public/char_track.json says which clip plays when (the watermark is drawn on top there too).
#   python build.py  ->  public/index.html + public/char_track.json
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from gaya_common import DUR, ROOT, VO_START, page, words  # noqa: E402

VO_JSON = ROOT / "motion" / "panduan-gaya" / "_vo" / "guide" / "scene_01.json"
if VO_JSON.exists():
    T = words("guide")
    END_VO = json.loads(VO_JSON.read_text(encoding="utf-8"))["words"][-1]["end"] + VO_START
else:  # no VO yet: estimated timing (~2.3 words/s, pauses on punctuation) so the visual can be previewed
    text = re.sub(r"\[[^\]]*\]\s*", "", (ROOT / "motion" / "panduan-gaya" / "_vo" / "guide.txt").read_text(encoding="utf-8")).split()
    T, t = {}, VO_START
    for i, w in enumerate(text):
        T[i] = round(t, 3)
        t += 0.40 + (0.30 if w[-1] in ".?" else 0.12 if w[-1] == "," else 0)
    END_VO = t - 0.3
# word index map for the demo line:
# 0 Cara 1 aku 2 bikin 3 reel 4 pakai 5 AI? 6 Cuma 7 tiga 8 langkah. 9 Satu, 10 tulis 11 ide 12 satu 13 kalimat.
# 14 Dua, 15 AI 16 nyusun 17 naskah 18 dan 19 suaranya. 20 Tiga, 21 cek, 22 lalu 23 posting.
B1, B2, B3, B4 = T[6] - 0.12, T[9] - 0.12, T[14] - 0.12, T[20] - 0.12
END = round(min(max(END_VO + 0.45, 12.3), 13.0), 3)

# chibi clip per beat (names = files in karakter/Animasi Karakter)
CHAR = {"dur": DUR, "place": {"scale": 1.3, "cx": 540, "top": 955, "enter": 0.1, "wm_until": END},
        "segments": [[0.1, B1, "Melambaikan_Tangan"], [B1, B2, "Menghitung_dengan_Jari"], [B2, B3, "mengetik"],
                     [B3, B4, "menunjuk_keatas"], [B4, END, "Acungkan-jempol"], [END, DUR, "Melambaikan_Tangan"]]}

css = '''
@font-face { font-family: "SerifBI"; src: url("fonts/SerifBI.ttf") format("truetype"); font-display: block; }
@font-face { font-family: "Mono"; src: url("fonts/Mono.ttf") format("truetype"); font-display: block; }
:root { --cream:#EEEBE4; --ink:#151515; --lime:#C6F432; --red:#E8392B; --card:#1C1C1E; }
html, body, #root { background: var(--cream); color: var(--ink); font-family: "IDBold"; }
#grain { position: absolute; inset: 0; opacity: .5; background-image: radial-gradient(rgba(0,0,0,.07) 1px, transparent 1.2px); background-size: 7px 7px; }
#cam { position: absolute; inset: 0; }
.hud { position: absolute; top: 262px; font-family: "Mono"; font-size: 27px; letter-spacing: .02em; color: rgba(21,21,21,.62); }
.hud { opacity: 0; } .hudL { left: 70px; } .hudR { right: 150px; text-align: right; }
.hudR b { font-family: "Mono"; font-weight: normal; color: var(--ink); margin-left: 10px; }
.hl { position: absolute; left: 70px; top: 330px; width: 860px; font-size: 80px; line-height: 1.12; letter-spacing: -.015em; opacity: 0; }
.hl span { display: inline-block; opacity: 0; margin-right: 18px; }
.hl .ac { font-family: "SerifBI"; font-size: 92px; position: relative; z-index: 0; isolation: isolate; padding: 0 6px; }
.hl .ac:before { content: ""; position: absolute; left: -4px; right: -4px; bottom: 10px; height: 40%; background: var(--lime);
  z-index: -1; transform-origin: 0 50%; transform: scaleX(var(--hx, 0)); border-radius: 6px; }
.hl .num { font-family: "Mono"; font-size: 54px; background: var(--ink); color: var(--cream); border-radius: 12px; padding: 4px 16px 6px; vertical-align: 12px; }
.prop { position: absolute; opacity: 0; }
.badge { position: absolute; width: 74px; height: 86px; border-radius: 14px; background: var(--ink); color: #fff; font-family: "IDBlack";
  font-size: 56px; text-align: center; line-height: 76px; box-shadow: 0 10px 22px rgba(0,0,0,.25); opacity: 0; }
.badge:after { content: ""; position: absolute; left: 18px; bottom: 9px; width: 38px; height: 6px; border-radius: 3px;
  background: linear-gradient(90deg, var(--red) 0 30%, rgba(255,255,255,.35) 30%); }
.sim { position: absolute; opacity: 0; font-family: "Mono"; font-size: 20px; letter-spacing: .08em; color: rgba(21,21,21,.5); }
/* B0 phone */
#phone { left: 285px; top: 600px; width: 330px; height: 390px; border-radius: 46px; background: #111; padding: 16px 16px 0;
  box-shadow: 0 30px 60px rgba(0,0,0,.25); overflow: hidden; }
#phone .scr { width: 100%; height: calc(100% - 16px); border-radius: 32px; background: linear-gradient(170deg, #FBF8F1 0%, #E8E3D8 100%); padding: 40px 26px; }
#phone .t1 { font-family: "IDBlack"; font-size: 40px; line-height: 1.05; }
#phone .t1 i { font-family: "SerifBI"; font-style: normal; background: var(--lime); padding: 0 6px; border-radius: 6px; }
#phone .row { margin-top: 26px; height: 16px; border-radius: 8px; background: rgba(0,0,0,.12); }
#phone .row.s { width: 60%; }
#views { left: 590px; top: 630px; background: #fff; border-radius: 22px; padding: 14px 22px; font-family: "IDBlack"; font-size: 40px;
  box-shadow: 0 16px 34px rgba(0,0,0,.16); white-space: nowrap; }
#views small { display: block; font-family: "Mono"; font-size: 18px; color: rgba(0,0,0,.5); letter-spacing: .06em; }
.heart { position: absolute; font-size: 34px; color: var(--red); opacity: 0; }
/* B1 tiles */
.tile { position: absolute; width: 150px; border-radius: 18px; background: var(--ink); color: #fff; font-family: "IDBlack"; font-size: 96px;
  text-align: center; padding-top: 14px; transform-origin: 50% 100%; opacity: 0; box-shadow: 0 18px 30px rgba(0,0,0,.2); }
#t1 { left: 230px; top: 790px; height: 170px; } #t2 { left: 400px; top: 700px; height: 260px; } #t3 { left: 570px; top: 600px; height: 360px; }
#t3 { background: var(--lime); color: var(--ink); }
#base { left: 200px; top: 958px; width: 560px; height: 10px; border-radius: 5px; background: var(--ink); }
/* B2 app window */
.win { left: 110px; top: 610px; width: 760px; border-radius: 26px; background: var(--card); color: #EDEDED; font-family: "IDSemi";
  box-shadow: 0 30px 60px rgba(0,0,0,.28); padding: 22px 30px 30px; }
.win .bar { font-family: "Mono"; font-size: 22px; color: rgba(255,255,255,.55); margin-bottom: 26px; }
.win .bar i { display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: rgba(255,255,255,.22); margin-right: 8px; }
.win .ask { font-size: 30px; color: rgba(255,255,255,.55); margin: 30px 0 34px; text-align: center; }
.win .ask b { color: var(--lime); font-weight: normal; }
.win .in { border: 2px solid rgba(255,255,255,.18); border-radius: 18px; padding: 20px 22px; font-family: "Mono"; font-size: 30px; min-height: 76px; }
.win .in .cur { display: inline-block; width: 3px; height: 32px; background: var(--lime); vertical-align: -5px; margin-left: 3px; }
#enter { left: 640px; top: 880px; padding: 14px 26px; border-radius: 16px; background: var(--red); color: #fff; font-family: "IDBlack";
  font-size: 34px; box-shadow: 0 8px 0 #9E2016; }
/* B3 checklist */
#list { left: 70px; top: 610px; width: 540px; }
.it { display: flex; align-items: center; height: 92px; margin-bottom: 14px; border-radius: 20px; background: #fff; padding: 0 26px;
  font-family: "IDBold"; font-size: 38px; box-shadow: 0 10px 24px rgba(0,0,0,.1); border: 3px solid transparent; opacity: 0; }
.it .ic { width: 50px; height: 50px; border-radius: 12px; background: var(--ink); color: #fff; font-size: 26px; text-align: center; line-height: 50px; margin-right: 20px; font-family: "IDBlack"; }
.it .st { margin-left: auto; width: 44px; height: 44px; border-radius: 50%; border: 4px solid rgba(0,0,0,.15); position: relative; }
.it .st .ok { position: absolute; inset: -4px; border-radius: 50%; background: var(--ink); color: var(--lime); font-size: 26px; text-align: center; line-height: 44px; opacity: 0; }
.it.on { border-color: var(--ink); }
#file { left: 640px; top: 760px; width: 290px; border-radius: 18px; background: #fff; padding: 18px 24px; font-family: "Mono"; font-size: 24px; box-shadow: 0 10px 24px rgba(0,0,0,.1); }
#file .pb { margin-top: 12px; height: 12px; border-radius: 6px; background: rgba(0,0,0,.1); overflow: hidden; }
#file .pb i { display: block; height: 100%; background: var(--ink); transform-origin: 0 50%; }
#file b { float: right; font-weight: normal; }
/* B4 post */
#post { left: 300px; top: 590px; width: 330px; height: 400px; border-radius: 46px; background: #111; padding: 16px 16px 0; box-shadow: 0 30px 60px rgba(0,0,0,.25); }
#post .scr { width: 100%; height: calc(100% - 16px); border-radius: 32px; background: #fff; padding: 30px 24px; font-family: "IDBold"; }
#post .hd { font-size: 26px; text-align: center; margin-bottom: 22px; }
#post .th { height: 130px; border-radius: 16px; background: linear-gradient(160deg, var(--lime), #8FD11B); position: relative; }
#post .th:after { content: "\\25B6"; position: absolute; left: 0; right: 0; top: 46px; text-align: center; font-size: 48px; color: rgba(0,0,0,.6); }
#post .ln { margin-top: 16px; height: 14px; border-radius: 7px; background: rgba(0,0,0,.1); }
#post .btn { margin-top: 26px; height: 64px; border-radius: 16px; background: #3B6CFF; color: #fff; font-size: 28px; text-align: center; line-height: 64px; }
#tap { left: 430px; top: 890px; width: 70px; height: 70px; border-radius: 50%; border: 6px solid var(--ink); opacity: 0; }
#stamp { left: 540px; top: 700px; padding: 12px 26px; border: 6px solid var(--red); border-radius: 14px; color: var(--red); font-family: "IDBlack";
  font-size: 46px; letter-spacing: .04em; transform: rotate(-10deg); background: rgba(238,235,228,.9); white-space: nowrap; }
/* halftone wipe + end card */
#dots { position: absolute; inset: 0; pointer-events: none; }
#dots i { position: absolute; width: 70px; height: 70px; margin: -35px 0 0 -35px; border-radius: 50%; background: var(--ink); transform: scale(0); }
#end { position: absolute; inset: 0; background: var(--cream); opacity: 0; }
#end .n { position: absolute; left: 0; width: 1080px; top: 300px; text-align: center; font-family: "Mono"; font-size: 34px; letter-spacing: .2em; color: rgba(21,21,21,.6); }
#end .t { position: absolute; left: 0; width: 1080px; top: 360px; text-align: center; font-family: "SerifBI"; font-size: 220px; line-height: 1.1; }
#end .t span { position: relative; z-index: 0; isolation: isolate; padding: 0 20px; }
#end .t span:before { content: ""; position: absolute; left: 0; right: 0; bottom: 34px; height: 36%; background: var(--lime); z-index: -1; border-radius: 10px; }
#end .d { position: absolute; left: 0; width: 1080px; top: 640px; text-align: center; font-family: "IDSemi"; font-size: 34px; color: rgba(21,21,21,.7); }
'''

HUD = [("// 01 &middot; hasilnya dulu", "VIEWS", "0"), ("// 02 &middot; cuma segini", "LANGKAH", "0/3"),
       ("// 03 &middot; tulis ide", "LANGKAH", "1/3"), ("// 04 &middot; AI kerja", "LANGKAH", "2/3"),
       ("// 05 &middot; cek &amp; posting", "LANGKAH", "3/3")]
DOTS = "".join(f'<i style="left:{x * 90 + 45}px;top:{y * 90 + 45}px"></i>' for y in range(22) for x in range(12))
body = f'''
  <div id="grain"></div>
  <div id="cam">
    {"".join(f'<div class="hud hudL" id="hl{k}">{l}</div><div class="hud hudR" id="hr{k}">{a}<b{" id=hudV" if k == 0 else ""}>{b}</b></div>'
             for k, (l, a, b) in enumerate(HUD))}

    <div class="hl" id="h0"><span>Bikin</span><span class="ac">reel</span><br><span>pakai AI</span></div>
    <div class="prop" id="phone"><div class="scr"><div class="t1">3 langkah bikin <i>reel</i></div><div class="row"></div><div class="row s"></div><div class="row"></div></div></div>
    <div class="prop" id="views"><small>DITONTON</small><span id="vv">0</span></div>
    <div class="heart" style="left:640px;top:780px">&#9829;</div><div class="heart" style="left:700px;top:740px">&#9829;</div><div class="heart" style="left:760px;top:790px">&#9829;</div>
    <div class="sim" id="sim0" style="left:290px;top:570px">SIMULASI</div>

    <div class="hl" id="h1"><span>Cuma</span><span class="ac">tiga</span><span>langkah.</span></div>
    <div class="tile" id="t1">1</div><div class="tile" id="t2">2</div><div class="tile" id="t3">3</div><div class="prop" id="base"></div>

    <div class="hl" id="h2"><span class="num">1</span><span>Tulis ide</span><br><span class="ac">satu kalimat</span></div>
    <div class="prop win" id="win"><div class="bar"><i></i><i></i><i></i>&nbsp;endrich-ai</div>
      <div class="ask">Mau bikin <b>reel</b> apa hari ini?</div><div class="in"><span id="typed"></span><span class="cur"></span></div></div>
    <div class="badge" id="bd1" style="left:820px;top:575px">1</div>
    <div class="prop" id="enter">ENTER &#8629;</div>

    <div class="hl" id="h3"><span class="num">2</span><span>AI susun</span><br><span class="ac">naskah + suara</span></div>
    <div class="prop" id="list">
      <div class="it" id="i1"><span class="ic">Aa</span>Naskah<span class="st"><span class="ok">&#10003;</span></span></div>
      <div class="it" id="i2"><span class="ic">&#9679;</span>Suara<span class="st"><span class="ok">&#10003;</span></span></div>
      <div class="it" id="i3"><span class="ic">&#9635;</span>Visual<span class="st"><span class="ok">&#10003;</span></span></div>
    </div>
    <div class="prop" id="file">reel_ai.mp4 <b id="pct">0%</b><div class="pb"><i id="pbI"></i></div></div>
    <div class="badge" id="bd2" style="left:850px;top:670px">2</div>

    <div class="hl" id="h4"><span class="num">3</span><span>Cek, lalu</span><br><span class="ac">posting</span></div>
    <div class="prop" id="post"><div class="scr"><div class="hd">Reel baru</div><div class="th"></div><div class="ln"></div><div class="ln" style="width:70%"></div>
      <div class="btn" id="share">Bagikan</div></div></div>
    <div class="prop" id="tap"></div>
    <div class="prop" id="stamp">SIAP TAYANG</div>
    <div class="badge" id="bd3" style="left:600px;top:565px">3</div>
    <div class="sim" id="sim4" style="left:305px;top:560px">SIMULASI</div>

  </div>
  <div id="end"><div class="n">GAYA 09</div><div class="t"><span>Guide</span></div>
    <div class="d">presenter chibi &middot; langkah bernomor &middot; props</div></div>
  <div id="dots">{DOTS}</div>
'''

js = f'''
    var T = {json.dumps(T)};
    var B = [0, {B1}, {B2}, {B3}, {B4}, {END}];
    // HUD: one pair of elements per beat, swapped (seek-safe)
    function hud(k, t) {{ if (k > 0) cut("#hl" + (k - 1) + ", #hr" + (k - 1), t, 0);
      tl.fromTo("#hl" + k + ", #hr" + k, {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power2.out" }}, q(t)); }}
    // headline: block on, words in on their VO word, highlighter swipes under the accent word
    function head(id, t0, wt) {{
      tl.set(id, {{ opacity: 1 }}, q(t0));
      var sp = document.querySelectorAll(id + " > span");
      sp.forEach(function (s, k) {{ var t = wt[k];
        tl.fromTo(s, {{ opacity: 0, y: 34 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, q(t));
        if (s.classList.contains("ac")) tl.fromTo(s, {{ "--hx": 0 }}, {{ "--hx": 1, duration: 0.35, ease: "power2.out" }}, q(t + 0.18)); }});
    }}
    function out(sel, t) {{ tl.to(sel, {{ opacity: 0, y: -24, duration: 0.16, ease: "power2.in" }}, q(t - 0.16)); }}
    function badge(id, t) {{ tl.fromTo(id, {{ opacity: 0, scale: 0.3, rotation: -25 }}, {{ opacity: 1, scale: 1, rotation: 8, duration: 0.4, ease: "back.out(2.6)" }}, q(t)); }}

    // ---- B0 hook: result first
    tl.set("#hl0, #hr0", {{ opacity: 1 }}, 0);
    head("#h0", 0, [0.12, 0.3, T[4]]);
    tl.fromTo("#phone", {{ opacity: 0, y: 220, rotation: -8 }}, {{ opacity: 1, y: 0, rotation: -4, duration: 0.55, ease: "back.out(1.5)" }}, 0.05);
    cut("#sim0", 0.4, 1);
    pop("#views", 0.5, 0.35);
    count("#vv", 0.6, 2.4, 0, 12400, function (v) {{ return v >= 1000 ? (v / 1000).toFixed(1) + "K" : Math.round(v) + ""; }});
    count("#hudV", 0.6, 2.4, 0, 12400, function (v) {{ return Math.round(v).toLocaleString("id-ID"); }});
    document.querySelectorAll(".heart").forEach(function (h, k) {{
      tl.fromTo(h, {{ opacity: 0, y: 0, scale: 0.4 }}, {{ opacity: 1, y: -90, scale: 1.1, duration: 0.7, ease: "power2.out" }}, q(T[3] + 0.15 * k));
      tl.to(h, {{ opacity: 0, duration: 0.25 }}, q(T[3] + 0.15 * k + 0.6)); }});
    tl.to("#phone", {{ y: -12, duration: 0.8, yoyo: true, repeat: 1, ease: "sine.inOut" }}, 0.7);
    out("#h0, #phone, #views, #sim0", B[1]);

    // ---- B1 three steps
    hud(1, B[1]);
    head("#h1", B[1], [T[6], T[7], T[8]]);
    cut("#base", B[1], 1);
    tl.fromTo("#base", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, q(B[1]));
    ["#t1", "#t2", "#t3"].forEach(function (s, k) {{
      tl.fromTo(s, {{ opacity: 0, scaleY: 0 }}, {{ opacity: 1, scaleY: 1, duration: 0.42, ease: "back.out(1.8)" }}, q(T[7] - 0.1 + 0.16 * k)); }});
    tl.fromTo("#t3", {{ rotation: 0 }}, {{ rotation: 4, duration: 0.15, yoyo: true, repeat: 3, ease: "sine.inOut" }}, q(T[8]));
    out("#h1, #t1, #t2, #t3, #base", B[2]);

    // ---- B2 step 1: one sentence
    hud(2, B[2]);
    head("#h2", B[2], [B[2] + 0.02, T[10], T[12]]);
    tl.fromTo("#win", {{ opacity: 0, y: 120, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "power3.out" }}, q(B[2]));
    badge("#bd1", B[2] + 0.25);
    type("#typed", T[10], Math.max(T[13] - T[10] + 0.2, 0.8), "reel: kenapa AI bisa salah?");
    tl.fromTo(".win .cur", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.25, yoyo: true, repeat: 9, ease: "steps(1)" }}, q(B[2] + 0.3));
    pop("#enter", T[13] + 0.15, 0.25);
    tl.to("#enter", {{ y: 8, boxShadow: "0 0 0 #9E2016", duration: 0.08, yoyo: true, repeat: 1 }}, q(T[13] + 0.5));
    out("#h2, #win, #bd1, #enter", B[3]);

    // ---- B3 step 2: AI builds it (checklist + progress, ref-15 "it builds the reel")
    hud(3, B[3]);
    head("#h3", B[3], [B[3] + 0.02, T[15], T[17]]);
    cut("#list", B[3], 1);
    ["#i1", "#i2", "#i3"].forEach(function (s, k) {{ rise(s, B[3] + 0.08 * k, 0.35, {{ x: -60, y: 0 }}); }});
    rise("#file", B[3] + 0.3, 0.35);
    badge("#bd2", B[3] + 0.3);
    var ck = [T[17], T[19], Math.min(T[19] + 0.6, B[4] - 0.3)];
    ["#i1", "#i2", "#i3"].forEach(function (s, k) {{
      tl.set(s, {{ borderColor: "#151515" }}, q(ck[k] - 0.35));
      tl.fromTo(s + " .ok", {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }}, q(ck[k]));
      tl.set(s, {{ borderColor: "rgba(0,0,0,0)" }}, q(ck[k] + 0.3)); }});
    tl.fromTo("#pbI", {{ scaleX: 0 }}, {{ scaleX: 1, duration: ck[2] - B[3] - 0.2, ease: "power1.inOut" }}, q(B[3] + 0.3));
    count("#pct", B[3] + 0.3, ck[2] - B[3] - 0.2, 0, 100, function (v) {{ return Math.round(v) + "%"; }});
    out("#h3, #list, #file, #bd2", B[4]);

    // ---- B4 step 3: check, post, stamp
    hud(4, B[4]);
    head("#h4", B[4], [B[4] + 0.02, T[21], T[23]]);
    tl.fromTo("#post", {{ opacity: 0, y: 200, rotation: 6 }}, {{ opacity: 1, y: 0, rotation: 3, duration: 0.5, ease: "back.out(1.5)" }}, q(B[4]));
    cut("#sim4", B[4] + 0.3, 1);
    badge("#bd3", B[4] + 0.3);
    tl.fromTo("#tap", {{ opacity: 0, scale: 1.8 }}, {{ opacity: 1, scale: 0.8, duration: 0.25, ease: "power2.out" }}, q(T[23] - 0.1));
    tl.to("#tap", {{ opacity: 0, scale: 1.5, duration: 0.3 }}, q(T[23] + 0.15));
    tl.to("#share", {{ backgroundColor: "#1B3FCF", duration: 0.1, yoyo: true, repeat: 1 }}, q(T[23]));
    tl.fromTo("#stamp", {{ opacity: 0, scale: 2.6, rotation: -22 }}, {{ opacity: 1, scale: 1, rotation: -10, duration: 0.28, ease: "power4.in" }}, q(T[23] + 0.3));
    tl.fromTo("#cam", {{ x: 0 }}, Object.assign({{ x: 10, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }}, NI), q(T[23] + 0.58));

    // ---- halftone dot wipe (ref-15) -> end card
    var D = document.querySelectorAll("#dots i");
    D.forEach(function (d) {{ var x = parseFloat(d.style.left), y = parseFloat(d.style.top);
      var r = Math.hypot(x - 540, y - 800) / 1400;
      tl.to(d, {{ scale: 1.5, duration: 0.22, ease: "power2.in" }}, q(B[5] - 0.42 + r * 0.3));
      tl.to(d, {{ scale: 0, duration: 0.25, ease: "power2.out" }}, q(B[5] + 0.05 + r * 0.3)); }});
    tl.set("#end", {{ opacity: 1 }}, q(B[5]));
    tl.set("#cam, #grain", {{ opacity: 0 }}, q(B[5]));
    rise("#end .n", B[5] + 0.25, 0.35, {{ y: -16 }});
    rise("#end .t", B[5] + 0.3, 0.45, {{ y: 60, rotation: -3 }});
    rise("#end .d", B[5] + 0.5, 0.35);
'''

(HERE / "public" / "index.html").write_text(page("gaya-guide", css, body, js), encoding="utf-8")
(HERE / "public" / "char_track.json").write_text(json.dumps(CHAR, indent=1), encoding="utf-8")
print("ok  END", END, " T", {k: T[k] for k in (0, 6, 9, 14, 20, 23)}, " VO", "asli" if VO_JSON.exists() else "estimasi")
