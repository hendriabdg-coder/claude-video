# Reel lagu "Aku Bukan Programmer" (EndrichTech) · 9:16 · tanpa chibi (permintaan Endrich 2026-11-12).
# Gaya mengikuti teknik video referensi (terminal chat, counter karya, dialog izin, teks partikel, mosaik, kota malam 3D,
# TV CRT) dengan konsep, teks dan aset sendiri. UI generik (bukan tiruan Claude Code / X), tanpa logo pihak lain.
# Audio: audio/lagu_final.wav (vokal AI Eleven Music, baris AI berfilter telepon) -> public/vo.mp3.
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
from reel_common import chars, fitpx, page  # noqa: E402

ROOT = HERE.parents[2]
pub = HERE / "public"
for d in ("fonts", "vendor"):
    if not (pub / d).exists():
        shutil.copytree(ROOT / "motion" / "gaya" / "gaya-terminal" / "public" / d, pub / d)
shutil.copy(ROOT / "motion" / "gaya" / "gaya-terminal" / "public" / "hyperframes.json", pub / "hyperframes.json")
for f in ("three.module.min.js", "three.core.min.js"):
    shutil.copy(ROOT / "motion" / "gaya" / "gaya-showcase" / "public" / "vendor" / f, pub / "vendor" / f)
DUR = 43.5
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(HERE / "audio" / "lagu_final.wav"), "-af", f"apad,atrim=0:{DUR}",
                "-ar", "44100", "-b:a", "192k", str(pub / "vo.mp3")], check=True)
# per-frame loudness (0..1) for the waveform card and beat pulses
raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(pub / "vo.mp3"), "-ac", "1", "-ar", "30000", "-f", "s16le", "-"])
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
env = np.array([np.sqrt((x[i:i + 1000] ** 2).mean()) for i in range(0, len(x) - 1000, 1000)])
ENV = [round(float(v), 3) for v in np.clip(env / (np.percentile(env, 98) + 1e-9), 0, 1)]
THUMBS = sorted(p.name for p in (pub / "thumbs").glob("*.jpg"))

# lyric timeline (detik), dari silencedetect + Whisper pada vokal terisolasi (lirik.md)
L = {"l1": 0.74, "ai1": 3.24, "l3": 4.75, "ai2": 6.48, "web": 8.25, "wa": 9.92, "vid": 11.9, "sua": 12.76, "meja": 13.47,
     "kul": 15.23, "sal": 17.59, "ulang": 18.7, "enter": 19.9, "ch1": 20.68, "lihat": 22.45, "ide": 24.7, "prompt": 26.3,
     "nyata": 27.2, "malam": 28.0, "hold": 29.5, "ija": 32.88, "rajin": 34.95, "kamu": 36.71, "mulai": 38.73, "cta": 40.6}
W = {"term": (0, L["web"] - 0.05), "verse": (L["web"] - 0.05, L["kul"] - 0.05), "perm": (L["kul"] - 0.05, L["ch1"] - 0.05),
     "p0": (L["ch1"] - 0.05, L["lihat"] - 0.05), "mosaic": (L["lihat"] - 0.05, L["nyata"] - 0.05),
     "city": (L["nyata"] - 0.05, L["ija"] - 0.1), "tv": (L["ija"] - 0.1, L["kamu"] - 0.05),
     "p1": (L["kamu"] - 0.05, L["cta"] - 0.05), "cta": (L["cta"] - 0.05, DUR + 1)}

css = '''
:root { --k:#0B0B0C; --o:#F2994A; --cr:#EDE6DA; --g:#6B6F78; --gr:#7BD88F; --r:#FF5A4E; }
html, body, #root { background: var(--k); color: var(--cr); font-family: "IDBlack"; }
#bg { position: absolute; inset: 0; background: var(--k); }
#three { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; display: block; }
#grain { position: absolute; inset: 0; opacity: .06; pointer-events: none;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='160' height='160' filter='url(%23n)'/></svg>"); }
#cam { position: absolute; inset: 0; }
.mono { font-family: "DejaVu Sans Mono", Consolas, "Courier New", monospace; }
#hdr { position: absolute; left: 60px; top: 262px; font-size: 24px; letter-spacing: .14em; color: var(--o); z-index: 5; }
#vlab { position: absolute; left: 60px; top: 1462px; font-size: 20px; letter-spacing: .12em; color: var(--g); border: 2px solid #33363d; border-radius: 8px; padding: 5px 12px; z-index: 5; }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-size: 36px; color: var(--cr); z-index: 6; }
#brand b { color: var(--o); font-weight: normal; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; pointer-events: none; }
.t { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; line-height: 1; letter-spacing: -.02em;
  text-shadow: 0 4px 28px rgba(0,0,0,.95); }
.t .ch { opacity: 0; }
.o { color: var(--o); } .c { color: var(--cr); } .gr { color: var(--gr); } .r { color: var(--r); }
/* terminal */
#term { position: absolute; left: 60px; top: 340px; width: 900px; height: 800px; opacity: 0; font-size: 46px; line-height: 1.75; }
#term .wel { display: inline-block; border: 2px solid var(--o); border-radius: 10px; padding: 10px 22px; font-size: 26px; line-height: 1.4; color: var(--cr); margin-bottom: 40px; }
#term .wel i { color: var(--o); font-style: normal; } #term .wel s { display: block; text-decoration: none; color: var(--g); font-size: 20px; }
#term .ln { white-space: pre; opacity: 0; }
#term .u .p { color: var(--g); } #term .u .x { color: var(--cr); }
#term .a .p, #term .a .x { color: var(--o); }
.cur { display: inline-block; width: 22px; height: 44px; background: var(--cr); vertical-align: -8px; margin-left: 4px; }
/* verse */
#ls { position: absolute; left: 60px; top: 330px; width: 560px; opacity: 0; font-size: 36px; line-height: 1.6; color: var(--g); }
#ls .it { opacity: 0; color: var(--cr); } #ls .it b { color: var(--gr); font-weight: normal; }
#cnt { position: absolute; left: 560px; top: 300px; width: 400px; text-align: right; font-size: 250px; line-height: 1; color: var(--o); opacity: 0; font-variant-numeric: tabular-nums; }
#cntl { position: absolute; left: 560px; top: 560px; width: 400px; text-align: right; font-size: 30px; letter-spacing: .1em; color: var(--o); opacity: 0; }
.card { position: absolute; left: 140px; top: 760px; width: 800px; height: 560px; opacity: 0; }
#cWeb .bar { height: 50px; border-radius: 16px 16px 0 0; background: #1d1f24; border: 2px solid #33363d; border-bottom: 0; display: flex; align-items: center; gap: 10px; padding: 0 18px; font-size: 22px; color: var(--g); }
#cWeb .bar i { width: 13px; height: 13px; border-radius: 50%; background: #3b3e46; display: inline-block; }
#cWeb .bd { height: 510px; border: 2px solid #33363d; border-radius: 0 0 16px 16px; }
#cWeb .lbl { position: absolute; right: 24px; bottom: 20px; font-size: 26px; color: var(--o); }
#cWa { background: #121417; border: 2px solid #33363d; border-radius: 24px; padding: 34px; }
.bub { max-width: 560px; padding: 18px 26px; border-radius: 22px; font-family: "IDBold"; font-size: 34px; margin: 18px 0; opacity: 0; }
.bub.in { background: #24272e; color: var(--cr); border-bottom-left-radius: 6px; }
.bub.out { background: #1f6f4a; color: #EFFFF4; margin-left: auto; border-bottom-right-radius: 6px; }
#cVid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
#cVid div { border-radius: 16px; background-size: cover; background-position: center; position: relative; border: 2px solid #33363d; }
#cVid div:after { content: "▶"; position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%); font-size: 54px; color: rgba(255,255,255,.9); text-shadow: 0 2px 12px #000; }
#cSua { display: flex; align-items: center; gap: 8px; padding: 0 20px; }
#cSua i { flex: 1; height: 100%; background: var(--o); border-radius: 6px; transform-origin: 50% 50%; display: block; }
#lap { position: absolute; left: 190px; top: 780px; width: 700px; height: 520px; opacity: 0; }
#lap .scr { position: absolute; left: 40px; top: 0; width: 620px; height: 400px; border: 6px solid #3b3e46; border-radius: 18px; background: #121417; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 14px; }
#lap .scr div { border-radius: 8px; font-family: "IDBold"; font-size: 26px; display: flex; align-items: center; justify-content: center; color: var(--k); opacity: 0; }
#lap .base { position: absolute; left: 0; top: 404px; width: 700px; height: 30px; border-radius: 0 0 26px 26px; background: #3b3e46; }
/* permission + errors */
#perm { position: absolute; left: 90px; top: 520px; width: 900px; border: 3px solid var(--o); border-radius: 16px; padding: 30px 36px; opacity: 0; font-size: 36px; line-height: 1.7; background: rgba(11,11,12,.9); }
#perm .q { color: var(--cr); margin-bottom: 10px; }
#perm .op { color: var(--g); padding-left: 14px; border-radius: 8px; }
#perm .op.sel { color: var(--k); background: var(--o); }
#errs { position: absolute; left: 60px; top: 520px; width: 960px; font-size: 32px; line-height: 1.8; }
#errs div { opacity: 0; white-space: pre; }
#key { position: absolute; left: 340px; top: 1000px; width: 400px; height: 190px; border-radius: 26px; background: #EDE6DA; color: #0B0B0C; box-shadow: 0 16px 0 #8f887d; font-size: 70px; display: flex; align-items: center; justify-content: center; opacity: 0; }
/* mosaic / prompt */
#pbox { position: absolute; left: 90px; top: 1180px; width: 900px; border: 2px solid var(--o); border-radius: 16px; padding: 24px 28px; font-size: 32px; color: var(--cr); background: rgba(11,11,12,.92); opacity: 0; white-space: pre; }
#pbox .p { color: var(--o); }
/* tv */
#room { position: absolute; inset: 0; background: radial-gradient(ellipse 60% 40% at 50% 45%, #2a2b25 0%, #0B0B0C 70%); opacity: 0; }
#tv { position: absolute; left: 180px; top: 520px; width: 720px; height: 560px; border-radius: 30px; background: #1a1a18; border: 14px solid #2b2a27; box-shadow: 0 40px 80px rgba(0,0,0,.7); opacity: 0; overflow: hidden; }
#tv .scr { position: absolute; inset: 26px; border-radius: 40px / 30px; background: radial-gradient(ellipse at center, #2c3a2c 0%, #121812 80%); padding: 70px 50px; font-size: 52px; color: var(--o); }
#tv .scr:after { content: ""; position: absolute; inset: 0; border-radius: inherit; background: repeating-linear-gradient(0deg, rgba(0,0,0,.25) 0 2px, rgba(0,0,0,0) 2px 5px); }
#tvst { position: absolute; left: 420px; top: 1080px; width: 240px; height: 40px; background: #2b2a27; border-radius: 0 0 12px 12px; opacity: 0; }
/* cta */
.opt { position: absolute; top: 470px; width: 430px; height: 150px; border-radius: 22px; display: flex; align-items: center; gap: 18px; padding: 0 26px; font-size: 36px; line-height: 1.1; opacity: 0; }
.opt .ol { width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 40px; flex: none; }
#oA { left: 80px; background: #1d1f24; border: 3px solid var(--cr); color: var(--cr); } #oA .ol { background: var(--cr); color: var(--k); }
#oB { left: 570px; background: var(--o); color: var(--k); } #oB .ol { background: var(--k); color: var(--o); }
#follow { position: absolute; left: 330px; top: 700px; width: 420px; height: 100px; border-radius: 50px; background: var(--cr); color: var(--k); font-size: 46px; display: flex; align-items: center; justify-content: center; opacity: 0; }
'''


def TX(tid, text, top, px, cls="c", maxw=780, font="InterDisplay-Black.ttf"):
    return f'<div class="t {cls}" id="{tid}" style="top:{top}px;font-size:{fitpx(text, px, maxw, font)}px">{chars(text)}</div>'


TERM = [("u", "> ", "Aku nggak bisa ngoding."), ("a", "• ", "Terus?"), ("u", "> ", "Tapi aku punya ide."), ("a", "• ", "Ya udah, ketik aja."),
        ("u", "> ", "bikin semuanya")]
term_html = "".join(f'<div class="ln {k}" id="tl{i}"><span class="p">{p}</span><span class="x" id="tx{i}"></span>'
                    f'{"<span class=cur id=cur></span>" if i == 4 else ""}</div>' for i, (k, p, _) in enumerate(TERM))
LS = [("web-3d/", "✓"), ("chatbot-wa/", "✓"), ("video/", "✓"), ("suara/", "✓")]
ls_html = '<div>$ ls ~/karya</div>' + "".join(f'<div class="it" id="ls{i}">{n} <b>{c}</b></div>' for i, (n, c) in enumerate(LS))
vid_html = "".join(f'<div style="background-image:url(thumbs/{THUMBS[i]})"></div>' for i in (1, 15, 6, 20))
sua_html = "".join('<i class="sb"></i>' for _ in range(32))
ERRS = [('r', "✗ Error: build gagal"), ('r', "✗ TypeError: undefined"), ('r', "✗ 404: file tidak ada"),
        ('c', "↻ coba lagi…"), ('c', "↻ coba lagi…")]
errs_html = "".join(f'<div class="{c}" id="er{i}">{t}</div>' for i, (c, t) in enumerate(ERRS))

body = f'''
  <div id="bg"></div>
  <div id="room"></div>
  <canvas id="three" width="1080" height="1920"></canvas>
  <div id="grain"></div>
  <div id="cam">
    <div id="hdr" class="mono">♪ AKU BUKAN PROGRAMMER</div>
    <!-- terminal -->
    <div id="term" class="mono"><div class="wel"><i>✻</i> Selamat datang di studio<s>~/endrichtech · laptop yang sama</s></div>{term_html}</div>
    <!-- verse -->
    <div id="ls" class="mono">{ls_html}</div>
    <div id="cnt" class="mono">0</div><div id="cntl" class="mono">KARYA</div>
    <div class="card" id="cWeb"><div class="bar"><i></i><i></i><i></i>&nbsp; web-3d.html</div><div class="bd"></div><div class="lbl mono">website 3D</div></div>
    <div class="card" id="cWa"><div class="bub in" id="b1">Halo! Mau pesan apa? 🤖</div><div class="bub out" id="b2">Kopi susu 2</div><div class="bub in" id="b3">Siap, Rp36.000 ✓</div></div>
    <div class="card" id="cVid">{vid_html}</div>
    <div class="card" id="cSua">{sua_html}</div>
    <div id="lap"><div class="scr"><div style="background:#F2994A">WEB 3D</div><div style="background:#7BD88F">CHATBOT</div><div style="background:#EDE6DA">VIDEO</div><div style="background:#8FA2FF">SUARA</div></div><div class="base"></div></div>
    {TX("v1", "SEMUA DARI MEJA YANG SAMA", 1370, 70)}
    <!-- permission / errors / enter -->
    <div id="perm" class="mono"><div class="q">Lanjut tanpa ijazah IT?</div>
      <div class="op" id="op1">1. Ya</div><div class="op" id="op2">2. Ya, jangan tanya lagi</div><div class="op" id="op3">3. Nggak dulu</div></div>
    <div id="errs" class="mono">{errs_html}</div>
    <div id="key" class="mono">ENTER ⏎</div>
    {TX("ok", "✓ JALAN!", 1300, 150, "gr")}
    <!-- chorus -->
    {TX("m1", "LIHAT YANG AKU BIKIN", 330, 84, "o")}
    {TX("m2", "SATU IDE", 520, 150)}
    {TX("m3", "SATU PROMPT", 700, 150, "o")}
    <div id="pbox" class="mono"><span class="p">&gt; </span><span id="ptx"></span></div>
    {TX("n1", "JADI NYATA", 400, 170)}
    {TX("n2", "MALAM INI", 590, 170, "o")}
    {TX("n3", "4 KARYA · 0 IJAZAH IT", 1250, 70)}
    <!-- tv -->
    <div id="tv"><div class="scr mono"><span id="tvt"></span></div></div><div id="tvst"></div>
    {TX("rj", "Rajin nanya.", 1180, 150, "c", 860, "InterDisplay-SemiBoldItalic.ttf")}
    <!-- cta -->
    {TX("q0", "KAMU TIM MANA?", 330, 100)}
    <div class="opt" id="oA"><div class="ol">A</div>BELAJAR<br>NGODING DULU</div>
    <div class="opt" id="oB"><div class="ol">B</div>LANGSUNG<br>BIKIN PAKAI AI</div>
    <div id="follow">+ FOLLOW</div>
    <div class="t c" id="q1" style="top:850px;font-size:30px;font-family:IDBold;letter-spacing:.14em">JAWAB A / B DI KOMENTAR</div>
    <div id="vlab" class="mono">VOKAL: AI (ELEVEN MUSIC) · BUKAN SUARA ASLI</div>
  </div>
  <div id="flash"></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

js = f'''
    var L = {json.dumps(L)}, W = {json.dumps(W)}, ENV = {json.dumps(ENV)}, DUR = {DUR}, TERM = {json.dumps([t for _, _, t in TERM])};
    function slam(sel, t, s) {{ tl.set(sel + " .ch", {{ opacity: 1 }}, q(t)); tl.fromTo(sel, {{ opacity: 0, scale: s || 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(1.8)" }}, q(t)); }}
    function zip(sel, t) {{ var ch = document.querySelectorAll(sel + " .ch"); tl.set(sel, {{ opacity: 1 }}, q(t));
      tl.fromTo(ch, {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.16, ease: "back.out(2)", stagger: Math.min(0.03, 0.4 / ch.length) }}, q(t)); }}
    function rise(sel, t, d) {{ tl.fromTo(sel, {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: d || 0.24, ease: "back.out(1.6)" }}, q(t)); }}
    function off(sel, t) {{ tl.set(sel, {{ opacity: 0 }}, q(t)); }}
    tl.set("#bg", {{ backgroundColor: "#0B0B0C" }}, 0);
    tl.set("#bg", {{ backgroundColor: "#0a0f1f" }}, q(W.city[0])); tl.set("#bg", {{ backgroundColor: "#0B0B0C" }}, q(W.city[1]));

    // 1 TERMINAL CHAT
    rise("#term", 0.0, 0.3);
    [[0, L.l1, 0.75], [1, L.ai1, 0.3], [2, L.l3, 0.8], [3, L.ai2, 0.9], [4, L.ai2 + 1.4, 0.35]].forEach(function (e) {{
      tl.set("#tl" + e[0], {{ opacity: 1 }}, q(e[1] - 0.02)); type("#tx" + e[0], e[1], e[2], TERM[e[0]]); }});
    tl.to("#cur", {{ opacity: 0, duration: 0.25, yoyo: true, repeat: 3, ease: "steps(1)" }}, q(L.ai2 + 0.2));
    off("#term", W.term[1]);

    // 2 VERSE: ls + counter + cards
    tl.set("#ls, #cnt, #cntl", {{ opacity: 1 }}, q(W.verse[0]));
    var CARDS = ["#cWeb", "#cWa", "#cVid", "#cSua"], TT = [L.web, L.wa, L.vid, L.sua];
    TT.forEach(function (t, i) {{
      tl.fromTo("#ls" + i, {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.15 }}, q(t - 0.05));
      tl.set("#cnt", {{ textContent: String(i + 1) }}, q(t - 0.05));
      tl.fromTo("#cnt", {{ scale: 1.25 }}, Object.assign({{ scale: 1, duration: 0.25, ease: "back.out(2)" }}, NI), q(t - 0.05));
      tl.fromTo(CARDS[i], {{ opacity: 0, y: 80, rotation: i % 2 ? 2 : -2 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.22, ease: "back.out(1.5)" }}, q(t - 0.05));
      if (i > 0) off(CARDS[i - 1], t - 0.05);
      flash(t - 0.05, "#flash", 0.08);
    }});
    ["#b1", "#b2", "#b3"].forEach(function (b, k) {{ tl.fromTo(b, {{ opacity: 0, y: 30, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.18, ease: "back.out(2)" }}, q(L.wa + 0.1 + k * 0.5)); }});
    // waveform card follows the song loudness
    document.querySelectorAll("#cSua .sb").forEach(function (b, k) {{
      for (var f = Math.round(L.sua * 30); f < Math.round(L.meja * 30); f += 2) {{
        var v = ENV[Math.min(f + k % 6, ENV.length - 1)] * (0.55 + 0.45 * Math.abs(Math.sin(k * 1.7 + f * 0.21)));
        tl.set(b, {{ scaleY: Math.max(0.06, v) }}, f / 30); }} }});
    off("#cSua", L.meja - 0.05);
    tl.fromTo("#lap", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(1.4)" }}, q(L.meja - 0.05));
    tl.fromTo("#lap .scr div", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)", stagger: 0.08 }}, q(L.meja + 0.05));
    zip("#v1", L.meja + 0.4);
    off("#ls, #cnt, #cntl, #lap, #v1", W.verse[1]);

    // 3 PERMISSION -> ERRORS -> ENTER
    tl.fromTo("#perm", {{ opacity: 0, scale: 0.92 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(1.6)" }}, q(W.perm[0]));
    var SEL = {{ backgroundColor: "#F2994A", color: "#0B0B0C" }}, UNS = {{ backgroundColor: "rgba(0,0,0,0)", color: "#6B6F78" }};
    tl.set("#op1", SEL, q(L.kul + 0.5)); tl.set("#op1", UNS, q(L.kul + 1.1)); tl.set("#op2", SEL, q(L.kul + 1.1));
    tl.to("#op2", {{ opacity: 0.4, duration: 0.08, yoyo: true, repeat: 3 }}, q(L.kul + 1.6));
    off("#perm", L.sal - 0.05);
    [0, 1, 2].forEach(function (k) {{ tl.fromTo("#er" + k, {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.1 }}, q(L.sal + k * 0.28)); kick(L.sal + k * 0.28, 8); }});
    [3, 4].forEach(function (k, j) {{ tl.fromTo("#er" + k, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, q(L.ulang + j * 0.45)); }});
    tl.to("#errs div", {{ opacity: 0.25, duration: 0.15 }}, q(L.enter - 0.3));
    tl.fromTo("#key", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.2, ease: "back.out(1.6)" }}, q(L.enter - 0.4));
    tl.to("#key", {{ y: 14, boxShadow: "0 2px 0 #8f887d", duration: 0.06 }}, q(L.enter + 0.15));
    tl.to("#key", {{ y: 0, boxShadow: "0 16px 0 #8f887d", duration: 0.1 }}, q(L.enter + 0.25));
    slam("#ok", L.enter + 0.3, 1.6); flash(L.enter + 0.3, "#flash", 0.2);
    off("#errs div, #key, #ok", W.perm[1]);

    // 4 CHORUS: particles (3D) -> mosaic + prompt -> city
    zip("#m1", L.lihat + 0.05);
    slam("#m2", L.ide - 0.05); slam("#m3", L.prompt - 0.05);
    tl.set("#pbox", {{ opacity: 1 }}, q(L.ide + 0.2)); type("#ptx", L.ide + 0.25, 1.9, "bikin lagu: aku bukan programmer");
    off("#m1, #m2, #m3, #pbox", W.mosaic[1]);
    slam("#n1", L.nyata - 0.05, 1.5); slam("#n2", L.malam - 0.05, 1.5); kick(L.malam, 12);
    zip("#n3", L.hold + 0.3);
    off("#n1, #n2, #n3", W.city[1]);

    // 5 TV CRT
    tl.set("#room", {{ opacity: 1 }}, q(W.tv[0])); tl.set("#room", {{ opacity: 0 }}, q(W.tv[1]));
    tl.fromTo("#tv, #tvst", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08 }}, q(W.tv[0]));
    tl.fromTo("#tv .scr", {{ scaleY: 0.02 }}, Object.assign({{ scaleY: 1, duration: 0.18, ease: "power3.out" }}, NI), q(W.tv[0]));
    type("#tvt", L.ija, 0.75, "Ijazahmu apa?");
    tl.set("#rj .ch", {{ opacity: 1 }}, q(L.rajin - 0.05));
    tl.fromTo("#rj", {{ opacity: 0, scale: 1.6, rotation: -6 }}, {{ opacity: 1, scale: 1, rotation: -4, duration: 0.2, ease: "back.out(1.6)" }}, q(L.rajin - 0.05));
    kick(L.rajin + 0.1, 10);
    off("#tv, #tvst, #rj", W.tv[1]);

    // 6 CTA (particles handle "kamu juga bisa / mulai dari satu ide")
    zip("#q0", L.cta);
    tl.fromTo("#oA", {{ opacity: 0, x: -80 }}, {{ opacity: 1, x: 0, duration: 0.22, ease: "back.out(1.6)" }}, q(L.cta + 0.3));
    tl.fromTo("#oB", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 0.22, ease: "back.out(1.6)" }}, q(L.cta + 0.45));
    tl.fromTo("#follow", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.24, ease: "back.out(2.2)" }}, q(L.cta + 0.8));
    tl.to("#follow", {{ scale: 0.92, duration: 0.07, yoyo: true, repeat: 1 }}, q(L.cta + 1.5));
    tl.to("#follow", {{ backgroundColor: "#F2994A", duration: 0.08 }}, q(L.cta + 1.57));
    tl.set("#follow", {{ innerHTML: "&#10003; FOLLOWING" }}, q(L.cta + 1.57));
    zip("#q1", L.cta + 1.0);
'''

three = f'''
<script type="importmap">{{"imports": {{"three": "./vendor/three.module.min.js"}}}}</script>
<script type="module">
  import * as THREE from "three";
  var L = {json.dumps(L)}, W = {json.dumps(W)}, THUMBS = {json.dumps(THUMBS)};
  window.__hf = window.__hf || {{}}; window.__hf.buildReady = window.__hf.buildReady || {{}};
  var R = new THREE.WebGLRenderer({{ canvas: document.getElementById("three"), alpha: true, antialias: true, preserveDrawingBuffer: true }});
  R.setPixelRatio(1); R.setSize(1080, 1920, false); R.setClearColor(0x000000, 0);
  var scene = new THREE.Scene(), cam = new THREE.PerspectiveCamera(32, 1080 / 1920, 0.05, 200);
  scene.add(new THREE.HemisphereLight(0xffeedd, 0x10131c, 1.2));
  var key = new THREE.DirectionalLight(0xffffff, 2.0); key.position.set(-3, 5, 6); scene.add(key);
  var ORANGE = 0xF2994A, CREAM = 0xEDE6DA;
  function h(i) {{ var x = Math.sin(i * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); }}
  function ss(a, b, t) {{ var x = Math.min(1, Math.max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x); }}
  function inW(k, t) {{ return t >= W[k][0] && t < W[k][1]; }}

  // --- particle text
  var NP = 9000, pgeo = new THREE.BufferGeometry(), ppos = new Float32Array(NP * 3); pgeo.setAttribute("position", new THREE.BufferAttribute(ppos, 3));
  var dot = document.createElement("canvas"); dot.width = dot.height = 32; var dg = dot.getContext("2d"), gr = dg.createRadialGradient(16, 16, 0, 16, 16, 16);
  gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.6, "rgba(255,255,255,.85)"); gr.addColorStop(1, "rgba(255,255,255,0)"); dg.fillStyle = gr; dg.fillRect(0, 0, 32, 32);
  var pmat = new THREE.PointsMaterial({{ color: CREAM, size: 0.05, map: new THREE.CanvasTexture(dot), transparent: true, depthWrite: false }});
  var pts = new THREE.Points(pgeo, pmat); scene.add(pts);
  var SC = new Float32Array(NP * 3);
  for (var i = 0; i < NP; i++) {{ var u = h(i) * 2 - 1, th = h(i + 7e3) * 6.283, r = 3 + 4 * h(i + 9e3), s = Math.sqrt(1 - u * u);
    SC[i * 3] = r * s * Math.cos(th); SC[i * 3 + 1] = r * u * 1.6; SC[i * 3 + 2] = r * s * Math.sin(th) - 2; }}
  function textTargets(lines, px) {{
    var c = document.createElement("canvas"); c.width = 1000; c.height = 700; var g = c.getContext("2d");
    g.fillStyle = "#fff"; g.textAlign = "center"; g.textBaseline = "middle"; g.font = px + "px IDBlack";
    lines.forEach(function (l, k) {{ g.fillText(l, 500, 350 + (k - (lines.length - 1) / 2) * px * 1.05); }});
    var d = g.getImageData(0, 0, 1000, 700).data, cand = [];
    for (var y = 0; y < 700; y += 3) for (var x = 0; x < 1000; x += 3) if (d[(y * 1000 + x) * 4 + 3] > 128) cand.push(x, y);
    var out = new Float32Array(NP * 3), nc = cand.length / 2;
    for (var i = 0; i < NP; i++) {{ var j = Math.floor(h(i + 31) * nc) * 2; out[i * 3] = (cand[j] - 500) / 330 + (h(i + 5) - 0.5) * 0.01;
      out[i * 3 + 1] = -(cand[j + 1] - 350) / 330; out[i * 3 + 2] = (h(i + 3) - 0.5) * 0.08; }}
    return out;
  }}
  var T0, T1, T2, ready = document.fonts.load("150px IDBlack").then(function () {{
    T0 = textTargets(["AKU BUKAN", "PROGRAMMER"], 140); T1 = textTargets(["KAMU JUGA", "BISA"], 160); T2 = textTargets(["MULAI DARI", "SATU IDE."], 140); }});
  // keyframes: [time, target(null = scatter)]
  function particleState(t) {{
    var K = [[W.p0[0] - 0.4, null], [L.ch1 + 0.55, "T0"], [L.lihat - 0.25, "T0"], [L.lihat + 0.3, null],
             [W.p1[0] - 0.4, null], [L.kamu + 0.55, "T1"], [L.mulai - 0.1, "T1"], [L.mulai + 0.45, "T2"], [L.cta - 0.5, "T2"], [L.cta + 0.2, null]];
    for (var k = 0; k < K.length - 1; k++) if (t >= K[k][0] && t < K[k + 1][0]) return [K[k][1], K[k + 1][1], ss(K[k][0], K[k + 1][0], t)];
    return [null, null, 0];
  }}

  // --- 3D cube inside the browser card
  var cube = new THREE.Group(); scene.add(cube);
  cube.add(new THREE.Mesh(new THREE.BoxGeometry(1.15, 1.15, 1.15), new THREE.MeshStandardMaterial({{ color: ORANGE, roughness: 0.35, metalness: 0.2 }})));
  cube.add(new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(1.6, 1.6, 1.6)), new THREE.LineBasicMaterial({{ color: CREAM }})));

  // --- mosaic wall of Endrich's own reel frames
  var wall = new THREE.Group(); scene.add(wall); var tiles = [], loader = new THREE.TextureLoader();
  var texReady = Promise.all(THUMBS.map(function (n, i) {{ return new Promise(function (res) {{
    loader.load("thumbs/" + n, function (tx) {{ tx.colorSpace = THREE.SRGBColorSpace;
      var m = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.71), new THREE.MeshBasicMaterial({{ map: tx, transparent: true }})); m.userData.i = i; wall.add(m); tiles.push(m); res(); }}, undefined, res); }}); }}));

  // --- night city (instanced towers with lit windows)
  var wc = document.createElement("canvas"); wc.width = 64; wc.height = 128; var wg = wc.getContext("2d"); wg.fillStyle = "#000"; wg.fillRect(0, 0, 64, 128);
  for (var y = 4; y < 128; y += 10) for (var x = 4; x < 64; x += 10) if (h(x * 31 + y) > 0.55) {{ wg.fillStyle = h(x + y * 7) > 0.8 ? "#F2994A" : "#ffe7b0"; wg.fillRect(x, y, 5, 6); }}
  var wtex = new THREE.CanvasTexture(wc); wtex.wrapS = wtex.wrapT = THREE.RepeatWrapping;
  var NB = 260, city = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshStandardMaterial({{ color: 0x14161c, roughness: 0.8, emissive: 0xffffff, emissiveMap: wtex, emissiveIntensity: 0.9 }}), NB);
  scene.add(city); var M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), S = new THREE.Vector3();
  for (var b = 0; b < NB; b++) {{ var side = b % 2 ? 1 : -1, row = Math.floor(b / 2), hh = 2 + 9 * h(b + 3);
    V.set(side * (2.2 + 4 * h(b + 1)), hh / 2 - 1.5, 6 - row * 1.6 - h(b + 2)); S.set(1 + h(b + 4), hh, 1 + h(b + 5)); M4.compose(V, Q, S); city.setMatrixAt(b, M4); }}
  scene.fog = new THREE.Fog(0x0a0f1f, 12, 60);

  function renderAt(t) {{
    // particles
    var st = particleState(t), A = st[0] ? (st[0] == "T0" ? T0 : st[0] == "T1" ? T1 : T2) : SC, B = st[1] ? (st[1] == "T0" ? T0 : st[1] == "T1" ? T1 : T2) : SC;
    pts.visible = !!(A && B) && (inW("p0", t) || inW("p1", t) || (t > W.p0[0] - 0.4 && t < L.lihat + 0.3) || (t > W.p1[0] - 0.4 && t < L.cta + 0.2));
    if (pts.visible && A && B) {{ var k = st[2];
      for (var i = 0; i < NP * 3; i++) ppos[i] = A[i] + (B[i] - A[i]) * Math.min(1, Math.max(0, k * 1.15 - (i % 997) / 997 * 0.15));
      pgeo.attributes.position.needsUpdate = true; pmat.color.set(t > L.mulai + 0.2 ? ORANGE : CREAM);
      pts.rotation.y = 0.12 * Math.sin(t * 0.8); pts.position.set(0, 0.35, 0); }}
    // cube
    cube.visible = t >= L.web - 0.05 && t < L.wa - 0.05;
    cube.position.set(0, -0.33, 0); cube.rotation.set(0.5 + t * 0.9, t * 1.7, 0); cube.scale.setScalar(0.66 + 0.05 * Math.sin(t * 8));
    // mosaic
    wall.visible = inW("mosaic", t);
    tiles.forEach(function (m) {{ var i = m.userData.i, c = i % 7, r = Math.floor(i / 7), d = h(i + 11) * 0.7, k = ss(L.lihat + d * 0.6, L.lihat + 0.6 + d * 0.6, t);
      var gx = (c - 3) * 0.44, gy = (2 - r) * 0.77 + 0.15, sx = (h(i + 1) - 0.5) * 8, sy = (h(i + 2) - 0.5) * 12, sz = -6 - 8 * h(i + 3);
      m.position.set(sx + (gx - sx) * k, sy + (gy - sy) * k, sz * (1 - k)); m.rotation.set((1 - k) * h(i + 4) * 4, (1 - k) * h(i + 5) * 4, 0);
      m.material.opacity = 1 - 0.75 * ss(L.ide - 0.2, L.ide + 0.3, t); }});
    wall.position.z = -1.5 * ss(L.ide - 0.2, L.nyata, t); wall.scale.setScalar(0.9);
    // city
    city.visible = inW("city", t);
    var cz = 9 - 3.2 * (t - W.city[0]);
    // camera
    if (city.visible) {{ cam.position.set(0, 1.2 + 0.25 * (t - W.city[0]), cz); cam.lookAt(0, 3.0, cz - 10); }}
    else {{ cam.position.set(0, 0, 10); cam.lookAt(0, 0, 0); }}
    R.render(scene, cam);
  }}
  var allReady = Promise.all([ready, texReady]); window.__hf.buildReady["lagu"] = allReady;
  window.addEventListener("hf-seek", function (e) {{ var t = e.detail.time;
    if (!T0 || tiles.length < THUMBS.length) e.detail.waitUntil(allReady.then(function () {{ renderAt(t); }})); else renderAt(t); }});
  allReady.then(function () {{ renderAt(window.__hfThreeTime || 0); }});
</script>
'''

html = page("lagu-bukan-programmer", DUR, css, body, js).replace("</body>", three + "</body>")
(pub / "index.html").write_text(html, encoding="utf-8")
print("ok", DUR, len(THUMBS), "thumbs")
