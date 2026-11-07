# Reel Hari 10 · "Hampir 2.000 AI Agent Analisis Sel Otak Tikus" · Seri AI Agent #2.
# Gaya dasar PULSE (blok warna hitam/biru elektrik/coral/krem, kata raksasa, hard cut) + per beat:
#   hook/3D otak (PULSE + Three.js), "cepat banget" (PULSE), pil 3D (PULSE), DNA 3D + alur (SIGNAL),
#   peta laporan 3D (SIGNAL), log agent (TERMINAL, SIMULASI), otak kecil 3D, dua gen 3D, "satu hal penting" (PULSE),
#   preprint + labu lab 3D (PAPER), CTA chibi lip-flap (AVATAR).
# VO: Endrich generate manual (output/motion/<slug>/vo/vo-full.mp3), timing kata dari align.py. Sumber: riset.md.
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
import shutil  # noqa: E402

from reel_common import ICON, chars, chibi_html, chibi_js, chibi_track, fitpx, page, setup, words  # noqa: E402

SLUG = HERE.name
DUR = setup(HERE, SLUG)
T = words(SLUG)
pub = HERE / "public"
for f in ("three.module.min.js", "three.core.min.js"):
    shutil.copy(HERE.parents[1] / "gaya" / "gaya-showcase" / "public" / "vendor" / f, pub / "vendor" / f)

css = '''
:root { --k:#0E0E0E; --b:#3A5BFF; --c:#FF4F3A; --cr:#F4F1EA; --g:#8A8F9C; }
html, body, #root { background: var(--k); color: var(--cr); font-family: "IDBlack"; }
#bg { position: absolute; inset: 0; background: var(--k); }
#grain { position: absolute; inset: 0; opacity: .07; pointer-events: none;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='160' height='160' filter='url(%23n)'/></svg>"); }
#three { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; display: block; }
#cam { position: absolute; inset: 0; }
#hud { position: absolute; left: 60px; top: 262px; display: flex; align-items: center; gap: 12px; font-family: "IDBold"; font-size: 24px; letter-spacing: .18em; color: var(--cr); opacity: 0; z-index: 5; }
#hud i { width: 12px; height: 12px; background: var(--b); display: inline-block; }
.t { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; line-height: 1; letter-spacing: -.02em; }
.sh { text-shadow: 0 4px 28px rgba(0,0,0,.95), 0 0 6px rgba(0,0,0,.8); }
.t .ch { opacity: 0; }
.cr { color: var(--cr); } .bl { color: var(--b); } .co { color: var(--c); } .kk { color: var(--k); }
.sub { text-shadow: 0 2px 16px rgba(0,0,0,.9); position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDBold"; font-size: 30px; letter-spacing: .16em; opacity: 0; }
.chip { position: absolute; font-family: "IDBold"; font-size: 22px; letter-spacing: .16em; padding: 7px 14px; border: 2px solid currentColor; border-radius: 8px; opacity: 0; }
.rep { position: absolute; left: -40px; width: 1200px; font-size: 170px; line-height: 1.02; white-space: nowrap; color: transparent; -webkit-text-stroke: 3px rgba(244,241,234,.16); opacity: 0; }
#n1 { text-shadow: 0 4px 30px rgba(0,0,0,.95); position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; font-size: 210px; font-variant-numeric: tabular-nums; color: var(--cr); opacity: 0; line-height: 1; }
#n2 { text-shadow: 0 4px 30px rgba(0,0,0,.95); position: absolute; left: 0; width: 1080px; top: 1090px; text-align: center; font-size: 190px; font-variant-numeric: tabular-nums; color: var(--b); opacity: 0; line-height: 1; }
#strike { position: absolute; left: 150px; top: 1372px; width: 780px; height: 22px; background: var(--c); transform-origin: 0 50%; opacity: 0; }
.flow { position: absolute; top: 1250px; width: 270px; height: 150px; border-radius: 22px; background: var(--cr); color: var(--k); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; font-size: 34px; opacity: 0; }
.flow .fi { width: 56px; height: 56px; color: var(--b); }
.arr { position: absolute; top: 1305px; width: 50px; height: 40px; color: var(--cr); opacity: 0; }
#term { position: absolute; left: 60px; top: 420px; width: 960px; height: 520px; border-radius: 20px; border: 2px solid rgba(244,241,234,.25); background: #07080C; opacity: 0; overflow: hidden; }
#term .bar { height: 56px; display: flex; align-items: center; gap: 12px; padding: 0 22px; border-bottom: 2px solid rgba(244,241,234,.12); font-family: "IDBold"; font-size: 22px; letter-spacing: .14em; color: var(--g); }
#term .bar i { width: 14px; height: 14px; border-radius: 50%; border: 2px solid var(--g); display: inline-block; }
#term .ln { font-family: Consolas, "Courier New", monospace; font-size: 36px; line-height: 1.6; padding: 0 32px; white-space: pre; color: var(--cr); }
#term .ln b { color: var(--b); font-weight: normal; } #term .ln u { color: var(--c); text-decoration: none; }
#term .bd { padding-top: 22px; }
.barw { position: absolute; left: 150px; width: 760px; opacity: 0; }
.barw .bl0 { font-size: 46px; margin-bottom: 12px; display: flex; justify-content: space-between; }
.barw .bl0 span { font-family: "IDBold"; font-size: 26px; letter-spacing: .12em; color: var(--g); align-self: flex-end; }
.barw .tr { height: 64px; border-radius: 14px; background: rgba(244,241,234,.1); overflow: hidden; }
.barw .fl { height: 100%; border-radius: 14px; transform-origin: 0 50%; }
#doc { position: absolute; left: 90px; top: 450px; width: 900px; height: 420px; border-radius: 26px; background: #FFFDF8; color: var(--k); box-shadow: 0 30px 60px rgba(30,27,24,.18); opacity: 0; padding: 40px 48px; }
#doc .dh { display: flex; align-items: center; gap: 14px; font-family: "IDBold"; font-size: 24px; letter-spacing: .16em; color: var(--g); }
#doc .dh b { color: var(--c); font-weight: normal; border: 2px solid var(--c); border-radius: 6px; padding: 4px 10px; }
#doc .dt { font-size: 46px; margin: 22px 0 26px; line-height: 1.1; }
.row { display: flex; align-items: center; gap: 22px; font-size: 40px; margin: 18px 0; opacity: 0; white-space: nowrap; }
.row .mk { width: 58px; height: 58px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 36px; color: #fff; flex: none; }
.row .x { background: var(--c); } .row .ex { background: var(--b); }
#stamp { position: absolute; left: 190px; top: 1150px; padding: 18px 36px; border: 8px solid var(--c); border-radius: 18px; font-size: 84px; color: var(--c); transform: rotate(-6deg); opacity: 0; }
#xmark { position: absolute; left: 440px; top: 1130px; width: 200px; height: 200px; color: var(--c); opacity: 0; }
#follow { position: absolute; left: 330px; top: 430px; width: 420px; height: 100px; border-radius: 50px; background: var(--cr); color: var(--b); font-size: 48px; display: flex; align-items: center; justify-content: center; opacity: 0; }
#tapc { position: absolute; left: 670px; top: 475px; width: 70px; height: 70px; color: var(--k); opacity: 0; }
.opt { position: absolute; top: 440px; width: 420px; height: 130px; border-radius: 22px; display: flex; align-items: center; gap: 16px; padding: 0 24px; font-size: 36px; line-height: 1.05; opacity: 0; }
.opt .ol { width: 66px; height: 66px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 40px; flex: none; }
#oA { left: 100px; background: var(--b); color: var(--cr); } #oA .ol { background: var(--cr); color: var(--b); }
#oB { left: 560px; background: var(--c); color: var(--cr); } #oB .ol { background: var(--cr); color: var(--c); }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-size: 36px; color: var(--cr); z-index: 6; }
#brand b { color: var(--b); font-weight: normal; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; pointer-events: none; }
'''


def TX(tid, text, top, px, cls="cr", maxw=760):
    return f'<div class="t {cls}" id="{tid}" style="top:{top}px;font-size:{fitpx(text, px, maxw)}px">{chars(text)}</div>'


def SUB(tid, text, top, color="var(--cr)"):
    return f'<div class="sub" id="{tid}" style="top:{top}px;color:{color}">{text}</div>'


def REP(tid, word, top):
    return f'<div class="rep" id="{tid}" style="top:{top}px">{(" " + word) * 6}</div>'


X_SVG = '<svg class="ico" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="12" stroke-linecap="round"><path d="M22 22l56 56M78 22L22 78"/></svg>'
ARR = '<svg class="ico" viewBox="0 0 50 40" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h40M30 6l14 14-14 14"/></svg>'
DOC = '<svg class="ico" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="7" stroke-linejoin="round"><path d="M24 10h36l18 18v62H24z"/><path d="M36 46h30M36 60h30M36 74h20"/></svg>'
BOOK = '<svg class="ico" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="7" stroke-linejoin="round"><path d="M50 26c-10-8-24-10-38-8v60c14-2 28 0 38 8 10-8 24-10 38-8V18c-14-2-28 0-38 8z"/><path d="M50 26v60"/></svg>'
CELL = '<svg class="ico" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="7"><circle cx="50" cy="50" r="36"/><circle cx="56" cy="44" r="12"/><circle cx="34" cy="64" r="4"/><circle cx="68" cy="68" r="4"/></svg>'

# chibi (AVATAR) at the CTA: point at "bahaya", wave on "Follow", think on the A/B question
t_cta = T[143] - 0.1
track, emph_t = chibi_track(HERE, t_cta, DUR, [(T[148] - 0.1, "tunjuk"), (T[152], "netral"), (T[157] - 0.1, "lambai"),
                                               (T[159] + 0.2, "netral"), (T[162], "mikir"), (T[164] + 0.1, "netral"),
                                               (T[178] + 0.2, "mikir")], blinks=(T[150] + 0.3, T[168]))

TERM = [("$ ", "run atlas --agents ~2000"), ("agent_0412 › ", "gen <b>Tsc1</b> › laporan ✓"),
        ("agent_0413 › ", "gen <b>Tsc2</b> › laporan ✓"), ("atlas › ", "<u>efek beda</u> di otak kecil")]
term_html = "".join(f'<div class="ln" id="tl{k}" style="opacity:0">{a}{b}</div>' for k, (a, b) in enumerate(TERM))

body = f'''
  <div id="bg"></div>
  <canvas id="three" width="1080" height="1920"></canvas>
  <div id="grain"></div>
  <div id="cam">
    <div id="hud"><i></i>SERI AI AGENT &middot; #2</div>
    <!-- A hook: 3D brain + 1.946 agents -->
    <div id="n1">0</div>
    {SUB("a1", "HAMPIR 2.000 AGENT AI", 560)}
    {TX("a2", "DATA SEL OTAK TIKUS", 1230, 84, "cr sh")}
    <div id="n2">00:00</div>
    {SUB("a3", "MENIT", 1290, "var(--b)")}
    <div class="chip" id="srcA" style="left:60px;top:1450px;color:#8A8F9C">PREPRINT &middot; OPENAI, PERTURBAI, SCRIPPS &middot; OKT 2026</div>
    <!-- B cepat -->
    {REP("rB1", "CEPAT", 380)}{REP("rB2", "CEPAT", 1150)}
    {TX("b1", "CEPAT", 700, 230)}
    {TX("b2", "BANGET?", 930, 190, "kk")}
    <!-- C pil -->
    {TX("c1", "JANGAN SALAH PAHAM", 340, 84, "kk")}
    {TX("c2", "BUKAN", 1180, 120, "co")}
    {TX("c3", "OBAT BARU", 1320, 120, "kk")}
    <div id="strike"></div>
    <!-- D jadi gini -->
    {REP("rD1", "GINI", 380)}{REP("rD2", "GINI", 1150)}
    {TX("d1", "JADI GINI.", 820, 190)}
    <!-- E DNA + flow (SIGNAL) -->
    {TX("e1", "1 AGENT = 1 GEN", 340, 96, "cr sh")}
    <div class="flow" id="f1" style="left:60px"><div class="fi">{CELL}</div>DATA</div>
    <div class="arr" id="ar1" style="left:345px">{ARR}</div>
    <div class="flow" id="f2" style="left:405px"><div class="fi">{BOOK}</div>JURNAL</div>
    <div class="arr" id="ar2" style="left:690px">{ARR}</div>
    <div class="flow" id="f3" style="left:750px"><div class="fi">{DOC}</div>LAPORAN</div>
    <!-- F peta -->
    {TX("g1", "SEMUA DIGABUNG", 330, 96, "cr sh")}
    {TX("g2", "JADI SATU PETA", 1300, 96, "bl sh")}
    {TX("g3", "CARI POLA BARU", 1300, 90, "cr sh")}
    <!-- G terminal + bars -->
    {TX("h1", "TEMUAN MENARIK", 300, 96)}
    <div id="term"><div class="bar"><i></i><i></i><i></i>&nbsp;ATLAS AGENT &middot; LOG</div><div class="bd">{term_html}</div></div>
    <div class="barw" id="bw1" style="top:1010px"><div class="bl0">Tsc1<span>PERUBAHAN GEN SARAF</span></div><div class="tr"><div class="fl" id="fl1" style="width:10%;background:#F4F1EA"></div></div></div>
    <div class="barw" id="bw2" style="top:1190px"><div class="bl0">Tsc2</div><div class="tr"><div class="fl" id="fl2" style="width:88%;background:#FF4F3A"></div></div></div>
    <div class="chip" id="simG" style="left:60px;top:1450px;color:#8A8F9C">SIMULASI</div>
    <div class="chip" id="simF" style="left:60px;top:1450px;color:#8A8F9C">SIMULASI</div>
    {TX("h2", "EFEKNYA BEDA BANGET", 300, 90)}
    {TX("h3", "DI OTAK KECIL", 1300, 110, "co")}
    <!-- H dua gen -->
    {TX("i1", "PADAHAL...", 330, 96)}
    {TX("i2", "HUBUNGAN ERAT", 1300, 110, "bl")}
    <div class="chip" id="gL" style="left:215px;top:1130px;color:#3A5BFF;font-size:40px">Tsc1</div>
    <div class="chip" id="gR" style="left:730px;top:1130px;color:#FF4F3A;font-size:40px">Tsc2</div>
    <!-- I satu hal penting -->
    {REP("rI1", "PENTING", 380)}{REP("rI2", "PENTING", 1150)}
    {TX("j0", "!", 470, 300)}
    {TX("j1", "SATU HAL", 820, 170)}
    {TX("j2", "PENTING", 1010, 170, "kk")}
    <!-- J PAPER: preprint -->
    {TX("k1", "MASIH TEMUAN AWAL", 320, 92, "kk")}
    <div id="doc"><div class="dh"><b>PREPRINT</b>bioRxiv &middot; OKT 2026</div>
      <div class="dt">Ringkasan: atlas laporan agent</div>
      <div class="row" id="r1"><div class="mk x">&#10005;</div>Belum diuji di lab</div>
      <div class="row" id="r2"><div class="mk x">&#10005;</div>Belum review independen</div>
      <div class="row" id="r3"><div class="mk ex">!</div>Sebagian peneliti dari OpenAI</div>
    </div>
    <div id="xmark">{X_SVG}</div>
    {TX("k2", "BUKAN BERARTI SALAH", 1110, 84, "kk")}
    <div id="stamp">PERLU DIUJI</div>
    <div class="chip" id="ilJ" style="left:60px;top:1450px;color:#8A8F9C">ILUSTRASI 3D</div>
    <!-- K CTA seri -->
    {SUB("m0", "BESOK &middot; SERI AI AGENT #3", 335)}
    {TX("m1", "BAHAYA TERSEMBUNYI", 390, 92)}
    {TX("m2", "DI TOOL AI AGENT", 500, 80, "kk")}
    <div id="follow">+ FOLLOW</div><div id="tapc">{ICON["cursor"]}</div>
    <!-- L CTA komentar -->
    {TX("n0", "MENURUT KAMU?", 300, 96)}
    <div class="opt" id="oA"><div class="ol">A</div>LANGSUNG<br>PERCAYA</div>
    <div class="opt" id="oB"><div class="ol">B</div>BUKTIKAN<br>DI LAB</div>
    {SUB("n3", "TULIS A ATAU B DI KOMENTAR", 600)}
    <div class="chip" id="ilA" style="left:60px;top:1450px;color:#8A8F9C">ILUSTRASI 3D</div>
    {chibi_html()}
  </div>
  <div id="flash"></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

# scene windows (absolute seconds) shared by the GSAP timeline and the Three.js renderer
W = {
    "A": (0.0, T[16] - 0.12), "B": (T[16] - 0.12, T[19] - 0.1), "C": (T[19] - 0.1, T[33] - 0.1), "D": (T[33] - 0.1, T[35] - 0.1),
    "E": (T[35] - 0.1, T[55] - 0.12), "F": (T[55] - 0.12, T[70] - 0.12), "G": (T[70] - 0.12, T[86] - 0.1), "G2": (T[86] - 0.1, T[92] - 0.12),
    "H": (T[92] - 0.12, T[99] - 0.12), "I": (T[99] - 0.12, T[108] - 0.12), "J": (T[108] - 0.12, T[143] - 0.12),
    "K": (T[143] - 0.12, T[162] - 0.12), "L": (T[162] - 0.12, DUR + 1),
}
W = {k: (round(a, 3), round(b, 3)) for k, (a, b) in W.items()}
BG = {"A": "#0E0E0E", "B": "#3A5BFF", "C": "#F4F1EA", "D": "#FF4F3A", "E": "#0E0E0E", "F": "#0E0E0E", "G": "#0E0E0E",
      "G2": "#0E0E0E", "H": "#0E0E0E", "I": "#FF4F3A", "J": "#F4F1EA", "K": "#3A5BFF", "L": "#0E0E0E"}

js = f'''
    var T = {json.dumps(T)}, DUR = {DUR}, W = {json.dumps(W)}, BG = {json.dumps(BG)};
    function slam(sel, t, s) {{ tl.set(sel + " .ch", {{ opacity: 1 }}, q(t)); tl.fromTo(sel, {{ opacity: 0, scale: s || 1.35 }}, {{ opacity: 1, scale: 1, duration: 0.26, ease: "back.out(1.6)" }}, q(t)); }}
    function rise(sel, t, d) {{ tl.fromTo(sel, {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: d || 0.32, ease: "back.out(1.4)" }}, q(t)); }}
    function off(sel, t) {{ tl.set(sel, {{ opacity: 0 }}, q(t)); }}
    function repIn(a, b, t, t1) {{ tl.fromTo(a, {{ opacity: 1, x: 0 }}, Object.assign({{ x: -260, duration: t1 - t, ease: "none" }}, NI), q(t));
      tl.fromTo(b, {{ opacity: 1, x: -260 }}, Object.assign({{ x: 0, duration: t1 - t, ease: "none" }}, NI), q(t)); off(a + "," + b, t1); }}
    Object.keys(W).forEach(function (k) {{ tl.set("#bg", {{ backgroundColor: BG[k] }}, q(W[k][0])); }});
    tl.fromTo("#hud", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }}, 0.05);
    tl.set("#hud", {{ color: "#0E0E0E" }}, q(W.C[0])); tl.set("#hud", {{ color: "#F4F1EA" }}, q(W.D[0]));
    tl.set("#hud", {{ color: "#0E0E0E" }}, q(W.J[0])); tl.set("#hud", {{ color: "#F4F1EA" }}, q(W.K[0]));
    tl.set("#brand", {{ color: "#0E0E0E" }}, q(W.C[0])); tl.set("#brand", {{ color: "#F4F1EA" }}, q(W.D[0]));
    tl.set("#brand", {{ color: "#0E0E0E" }}, q(W.J[0])); tl.set("#brand", {{ color: "#F4F1EA" }}, q(W.K[0]));
    tl.set("#brand b", {{ color: "#F4F1EA" }}, q(W.D[0])); tl.set("#brand b", {{ color: "#3A5BFF" }}, q(W.E[0]));
    tl.set("#brand b", {{ color: "#F4F1EA" }}, q(W.I[0])); tl.set("#brand b", {{ color: "#3A5BFF" }}, q(W.J[0]));
    tl.set("#brand b", {{ color: "#F4F1EA" }}, q(W.K[0])); tl.set("#brand b", {{ color: "#3A5BFF" }}, q(W.L[0]));

    // A HOOK: counter lands on ±2.000 (VO "hampir 2000") as the swarm arrives, then the 32-minute clock
    tl.fromTo("#n1", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(1.6)" }}, 0);
    count("#n1", 0.05, T[6] - 0.1, 0, 2000, function (v) {{ return "±" + idn(v); }});
    rise("#a1", T[3], 0.3);
    sweep("#a2", T[7] - 0.05, 0.5);
    tl.fromTo("#srcA", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.3 }}, q(T[5]));
    off("#a2", T[14] - 0.15);
    slam("#n2", T[14] - 0.1, 1.5); rise("#a3", T[14] + 0.1, 0.3);
    count("#n2", T[14] - 0.1, 0.9, 0, 32, function (v) {{ return (v < 9.5 ? "0" : "") + Math.round(v) + ":00"; }});
    kick(T[14] + 0.8, 14);
    off("#n1, #a1, #n2, #a3, #srcA", W.A[1]);

    // B PULSE "cepat banget kan?"
    repIn("#rB1", "#rB2", W.B[0], W.B[1]);
    slam("#b1", W.B[0], 1.6); kick(W.B[0], -16); slam("#b2", T[17], 1.6); kick(T[17], 14);
    off("#b1, #b2", W.B[1]);

    // C pil 3D: "bukan obat baru", pill splits, coral strike
    sweep("#c1", W.C[0] + 0.05, 0.45);
    slam("#c2", T[25] - 0.05); slam("#c3", T[30] - 0.05);
    tl.fromTo("#strike", {{ opacity: 1, scaleX: 0 }}, {{ opacity: 1, scaleX: 1, duration: 0.3, ease: "power3.out" }}, q(T[31] + 0.05));
    kick(T[31] + 0.35, 12);
    off("#c1, #c2, #c3, #strike", W.C[1]);

    // D "jadi gini"
    repIn("#rD1", "#rD2", W.D[0], W.D[1]);
    slam("#d1", W.D[0], 1.6); kick(W.D[0], -14); off("#d1", W.D[1]);

    // E SIGNAL: DNA, one gene lights up, then DATA -> JURNAL -> LAPORAN
    sweep("#e1", T[36], 0.5);
    rise("#f1", T[45]); rise("#ar1", T[47] - 0.1, 0.25); rise("#f2", T[47]); rise("#ar2", T[50] + 0.1, 0.25); rise("#f3", T[52]);
    tl.to("#f1, #f2", {{ backgroundColor: "#8A8F9C", duration: 0.2 }}, q(T[53] + 0.1));
    tl.fromTo("#f3", {{ scale: 1 }}, Object.assign({{ scale: 1.08, duration: 0.18, yoyo: true, repeat: 1 }}, NI), q(T[54]));
    off("#e1, #f1, #f2, #f3, #ar1, #ar2", W.E[1]);

    // F 3D report cards fly into one map; a hidden pattern lights up
    sweep("#g1", W.F[0] + 0.05, 0.45); cut("#simF", W.F[0] + 0.3, 1); off("#simF", W.F[1]);
    rise("#g2", T[60] - 0.05); off("#g2", T[62] - 0.05); sweep("#g3", T[63] - 0.05, 0.45);
    off("#g1, #g3", W.F[1]);

    // G TERMINAL log (SIMULASI) + bars
    sweep("#h1", W.G[0] + 0.05, 0.4);
    tl.fromTo("#term", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.3)" }}, q(W.G[0] + 0.1));
    cut("#simG", W.G[0] + 0.1, 1);
    [[0, T[71]], [1, T[77] + 0.1], [2, T[80] + 0.6], [3, T[83]]].forEach(function (e) {{
      tl.fromTo("#tl" + e[0], {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power2.out" }}, q(e[1])); }});
    rise("#bw1", T[80] - 0.05);
    tl.fromTo("#fl1", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "power3.out" }}, q(T[80] + 0.15));
    rise("#bw2", T[82] - 0.05);
    tl.fromTo("#fl2", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.55, ease: "power3.out" }}, q(T[82] + 0.15));
    off("#h1", T[84] - 0.1); sweep("#h2", T[84] - 0.05, 0.45);
    off("#term, #bw1, #bw2, #simG, #h2", W.G[1]);
    // G2 3D brain again, cerebellum lit coral
    slam("#h3", T[89] - 0.05); off("#h3", W.G2[1]);

    // H two linked genes
    sweep("#i1", W.H[0] + 0.05, 0.4);
    rise("#gL", W.H[0] + 0.3, 0.3); rise("#gR", W.H[0] + 0.4, 0.3);
    slam("#i2", T[95] - 0.05); off("#i1, #i2, #gL, #gR", W.H[1]);

    // I PULSE "satu hal penting"
    repIn("#rI1", "#rI2", W.I[0], W.I[1]);
    slam("#j0", W.I[0], 1.8); kick(W.I[0], -16); slam("#j1", T[101] - 0.05, 1.5); slam("#j2", T[103] - 0.05, 1.5); kick(T[103], 12);
    off("#j0, #j1, #j2", W.I[1]);

    // J PAPER preprint + 3D flask
    sweep("#k1", W.J[0] + 0.05, 0.5);
    tl.fromTo("#doc", {{ opacity: 0, y: 80, rotation: -2 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.4, ease: "back.out(1.3)" }}, q(T[110]));
    rise("#r1", T[115]);
    tl.fromTo("#xmark", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }}, q(T[118] + 0.1));
    rise("#r2", T[121]);
    off("#xmark", T[125] - 0.1);
    rise("#r3", T[127]);
    cut("#ilJ", T[114], 1); off("#ilJ", T[125] - 0.1);
    tl.to("#r1, #r2, #r3", {{ opacity: 0.35, duration: 0.2 }}, q(T[133] - 0.1));
    sweep("#k2", T[134] - 0.05, 0.45);
    off("#k2", T[138] - 0.1);
    tl.fromTo("#stamp", {{ opacity: 0, scale: 1.8, rotation: -6 }}, {{ opacity: 1, scale: 1, rotation: -6, duration: 0.22, ease: "power4.in" }}, q(T[140] - 0.1));
    flash(T[140] + 0.12, "#flash", 0.25); kick(T[140] + 0.12, 12);
    off("#k1, #doc, #stamp", W.J[1]);

    // K CTA seri (AVATAR chibi)
    rise("#m0", T[144], 0.3); sweep("#m1", T[148] - 0.05, 0.45); sweep("#m2", T[152] - 0.05, 0.4);
    off("#m0, #m1, #m2", T[157] - 0.15);
    tl.fromTo("#follow", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.32, ease: "back.out(2.2)" }}, q(T[157] - 0.1));
    tl.fromTo("#tapc", {{ opacity: 0, x: 60, y: 60 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.3, ease: "power2.out" }}, q(T[158]));
    tl.to("#follow", {{ scale: 0.92, duration: 0.08, yoyo: true, repeat: 1 }}, q(T[159]));
    tl.to("#follow", {{ backgroundColor: "#0E0E0E", color: "#F4F1EA", duration: 0.1 }}, q(T[159] + 0.1));
    tl.set("#follow", {{ innerHTML: "&#10003; FOLLOWING" }}, q(T[159] + 0.1));
    off("#follow, #tapc", W.K[1]);

    // L CTA komentar A/B
    sweep("#n0", W.L[0] + 0.05, 0.45);
    tl.fromTo("#oA", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }}, q(T[170] - 0.05));
    tl.fromTo("#oB", {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }}, q(T[174] - 0.05));
    rise("#n3", T[178] + 0.2, 0.3);
'''
js += chibi_js(track, emph_t, t_cta)

# ---------------------------------------------------------------- Three.js: every frame is a pure function of t
three = f'''
<script type="importmap">{{"imports": {{"three": "./vendor/three.module.min.js"}}}}</script>
<script type="module">
  import * as THREE from "three";
  var T = {json.dumps(T)}, W = {json.dumps(W)};
  var canvas = document.getElementById("three");
  var R = new THREE.WebGLRenderer({{ canvas: canvas, alpha: true, antialias: true, preserveDrawingBuffer: true }});
  R.setPixelRatio(1); R.setSize(1080, 1920, false); R.setClearColor(0x000000, 0);
  R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.0;
  var scene = new THREE.Scene();
  var cam = new THREE.PerspectiveCamera(32, 1080 / 1920, 0.05, 100);
  scene.add(new THREE.HemisphereLight(0xf4f1ea, 0x1a1d2e, 1.1));
  var key = new THREE.DirectionalLight(0xfff1e0, 2.4); key.position.set(-3, 5, 5); scene.add(key);
  var rim = new THREE.DirectionalLight(0x8fa2ff, 1.6); rim.position.set(4, 1, -4); scene.add(rim);
  var BLUE = 0x3A5BFF, CORAL = 0xFF4F3A, CREAM = 0xF4F1EA, INK = 0x0E0E0E;
  function h(i) {{ var x = Math.sin(i * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); }}
  function ss(a, b, t) {{ var x = Math.min(1, Math.max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x); }}
  function inW(k, t) {{ return t >= W[k][0] && t < W[k][1]; }}
  function lerp3(a, b, k) {{ return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k]; }}
  function look(p, c) {{ cam.position.set(p[0], p[1], p[2]); cam.lookAt(c[0], c[1], c[2]); }}

  // --- mouse brain as a cloud of cells: two hemispheres, olfactory bulbs (front), cerebellum (back)
  var brain = new THREE.Group(); scene.add(brain);
  var PARTS = [[0.42, 0.05, 0.1, 0.5, 0.42, 0.85, 2200], [-0.42, 0.05, 0.1, 0.5, 0.42, 0.85, 2200], [0.16, -0.05, 1.05, 0.17, 0.17, 0.22, 260],
               [-0.16, -0.05, 1.05, 0.17, 0.17, 0.22, 260], [0, -0.12, -0.92, 0.55, 0.34, 0.3, 1100], [0, -0.38, -0.5, 0.18, 0.18, 0.4, 260]];
  function cloud(list, seed) {{
    var pos = [], n = 0;
    list.forEach(function (p) {{ for (var i = 0; i < p[6]; i++, n++) {{
      var u = h(seed + n * 3) * 2 - 1, th = h(seed + n * 3 + 1) * Math.PI * 2, r = 0.78 + 0.22 * Math.pow(h(seed + n * 3 + 2), 0.5), s = Math.sqrt(1 - u * u);
      pos.push(p[0] + p[3] * r * s * Math.cos(th), p[1] + p[4] * r * u, p[2] + p[5] * r * s * Math.sin(th)); }} }});
    var g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); return g;
  }}
  var dot = document.createElement("canvas"); dot.width = dot.height = 32; var dg = dot.getContext("2d");
  var gr = dg.createRadialGradient(16, 16, 0, 16, 16, 16); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.55, "rgba(255,255,255,.9)"); gr.addColorStop(1, "rgba(255,255,255,0)");
  dg.fillStyle = gr; dg.fillRect(0, 0, 32, 32); var dotTex = new THREE.CanvasTexture(dot);
  var cMat = new THREE.PointsMaterial({{ color: CREAM, size: 0.045, map: dotTex, transparent: true, depthWrite: false }});
  var cbMat = new THREE.PointsMaterial({{ color: CREAM, size: 0.045, map: dotTex, transparent: true, depthWrite: false }});
  brain.add(new THREE.Points(cloud(PARTS.slice(0, 4).concat([PARTS[5]]), 11), cMat));
  brain.add(new THREE.Points(cloud([PARTS[4]], 977), cbMat));

  // --- 1.946 agents: small blue cubes that fly in and settle into orbit shells around the brain
  var NA = 1946, agents = new THREE.InstancedMesh(new THREE.BoxGeometry(0.045, 0.045, 0.045), new THREE.MeshStandardMaterial({{ color: BLUE, roughness: 0.45 }}), NA);
  scene.add(agents); var M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), E = new THREE.Euler(), V = new THREE.Vector3(), S1 = new THREE.Vector3(1, 1, 1);
  var AG = []; for (var i = 0; i < NA; i++) {{
    var u = h(i * 7 + 1) * 2 - 1, th = h(i * 7 + 2) * Math.PI * 2, rr = 1.35 + 0.75 * h(i * 7 + 3), s = Math.sqrt(1 - u * u);
    AG.push({{ x: rr * s * Math.cos(th), y: rr * u * 0.8, z: rr * s * Math.sin(th) * 1.25, far: 9 + 6 * h(i * 7 + 4), arr: 0.1 + 3.3 * Math.pow(h(i * 7 + 5), 0.8), w: 0.12 + 0.25 * h(i * 7 + 6) }}); }}
  function placeAgents(t) {{
    for (var i = 0; i < NA; i++) {{ var a = AG[i], k = ss(a.arr, a.arr + 1.1, t), sc = 1 + (1 - k) * 0.6;
      var ang = a.w * t, c = Math.cos(ang), sn = Math.sin(ang), x = a.x * c - a.z * sn, z = a.x * sn + a.z * c;
      V.set(x * (1 + (a.far - 1) * (1 - k)), a.y * (1 + (a.far * 0.4) * (1 - k)), Math.min(z * (1 + (a.far - 1) * (1 - k)), 3.2));
      E.set(t * 1.3 + i, t * 0.9 + i * 2, 0); Q.setFromEuler(E); M4.compose(V, Q, S1.set(sc, sc, sc)); agents.setMatrixAt(i, M4); }}
    agents.instanceMatrix.needsUpdate = true;
  }}

  // --- capsule pill (coral / cream halves) that splits apart on "bukan obat baru"
  var pill = new THREE.Group(); scene.add(pill);
  var pTop = new THREE.Group(), pBot = new THREE.Group(); pill.add(pTop); pill.add(pBot);
  var coralM = new THREE.MeshStandardMaterial({{ color: CORAL, roughness: 0.35 }}), creamM = new THREE.MeshStandardMaterial({{ color: 0xFFFDF8, roughness: 0.4 }});
  pTop.add(new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.7, 48, 1, true), coralM)); pTop.children[0].position.y = 0.35;
  var capT = new THREE.Mesh(new THREE.SphereGeometry(0.5, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), coralM); capT.position.y = 0.7; pTop.add(capT);
  pBot.add(new THREE.Mesh(new THREE.CylinderGeometry(0.49, 0.49, 0.7, 48, 1, true), creamM)); pBot.children[0].position.y = -0.35;
  var capB = new THREE.Mesh(new THREE.SphereGeometry(0.49, 48, 24, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), creamM); capB.position.y = -0.7; pBot.add(capB);
  var pillSh = new THREE.Mesh(new THREE.CircleGeometry(0.9, 48), new THREE.MeshBasicMaterial({{ color: 0x1E1B18, transparent: true, opacity: 0.12 }}));
  pillSh.rotation.x = -Math.PI / 2; pillSh.position.y = -1.6; scene.add(pillSh);

  // --- DNA double helix; one gene segment turns blue, one agent docks on it
  var dna = new THREE.Group(); scene.add(dna); var NB = 44, sphG = new THREE.SphereGeometry(0.11, 20, 14);
  var strand = new THREE.InstancedMesh(sphG, new THREE.MeshStandardMaterial({{ color: 0xffffff, roughness: 0.4 }}), NB * 2);
  var rung = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.035, 0.035, 1, 10), new THREE.MeshStandardMaterial({{ color: 0xffffff, roughness: 0.5 }}), NB);
  dna.add(strand); dna.add(rung);
  var cA = new THREE.Color(CREAM), cB = new THREE.Color(0x8A8F9C), cG = new THREE.Color(BLUE), GENE = [20, 21, 22, 23, 24];
  for (var b = 0; b < NB; b++) {{ var y = (b - NB / 2) * 0.16, a1 = b * 0.42;
    var p1 = new THREE.Vector3(0.62 * Math.cos(a1), y, 0.62 * Math.sin(a1)), p2 = new THREE.Vector3(-0.62 * Math.cos(a1), y, -0.62 * Math.sin(a1));
    M4.makeTranslation(p1.x, p1.y, p1.z); strand.setMatrixAt(b * 2, M4); M4.makeTranslation(p2.x, p2.y, p2.z); strand.setMatrixAt(b * 2 + 1, M4);
    var mid = p1.clone().add(p2).multiplyScalar(0.5), dir = p2.clone().sub(p1), len = dir.length();
    Q.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.normalize()); M4.compose(mid, Q, new THREE.Vector3(1, len, 1)); rung.setMatrixAt(b, M4);
    strand.setColorAt(b * 2, cA); strand.setColorAt(b * 2 + 1, cB); rung.setColorAt(b, cB); }}
  var dock = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.22, 0.22), new THREE.MeshStandardMaterial({{ color: BLUE, roughness: 0.4 }})); dna.add(dock);
  function geneLit(k) {{ GENE.forEach(function (b) {{ var c = cB.clone().lerp(cG, k), c2 = cA.clone().lerp(cG, k);
    strand.setColorAt(b * 2, c2); strand.setColorAt(b * 2 + 1, c); rung.setColorAt(b, c); }}); strand.instanceColor.needsUpdate = true; rung.instanceColor.needsUpdate = true; }}

  // --- report cards: 144 pages fly from scattered spots into one 12x12 map; a hidden diagonal pattern lights blue
  var pg = document.createElement("canvas"); pg.width = 112; pg.height = 144; var g2 = pg.getContext("2d");
  g2.fillStyle = "#fff"; g2.fillRect(0, 0, 112, 144); g2.fillStyle = "#c9c6bf";
  for (var l = 0; l < 7; l++) g2.fillRect(14, 22 + l * 16, l % 3 == 2 ? 50 : 84, 6);
  var NC = 144, cards = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.28, 0.36), new THREE.MeshBasicMaterial({{ map: new THREE.CanvasTexture(pg), side: THREE.DoubleSide }}), NC);
  scene.add(cards); var CD = [];
  for (var c = 0; c < NC; c++) {{ var gx = c % 12, gy = Math.floor(c / 12), pat = Math.abs(gy - Math.round(5.5 + 3.5 * Math.sin(gx * 0.55))) <= 0;
    CD.push({{ gx: (gx - 5.5) * 0.34, gy: (gy - 5.5) * 0.42, sx: (h(c * 5 + 1) - 0.5) * 9, sy: (h(c * 5 + 2) - 0.5) * 12, sz: -2 - 6 * h(c * 5 + 3), r: h(c * 5 + 4) * 6, d: h(c * 5 + 5) * 1.6, pat: pat }});
    cards.setColorAt(c, new THREE.Color(0xffffff)); }}

  // --- two linked genes (Tsc1 blue, Tsc2 coral)
  var genes = new THREE.Group(); scene.add(genes);
  var g1m = new THREE.Mesh(new THREE.SphereGeometry(0.42, 48, 32), new THREE.MeshStandardMaterial({{ color: BLUE, roughness: 0.35 }}));
  var g2m = new THREE.Mesh(new THREE.SphereGeometry(0.42, 48, 32), new THREE.MeshStandardMaterial({{ color: CORAL, roughness: 0.35 }}));
  genes.add(g1m); genes.add(g2m); var links = [];
  for (var k = 0; k < 4; k++) {{ var lk = new THREE.Mesh(new THREE.TorusGeometry(0.13, 0.035, 12, 32), new THREE.MeshStandardMaterial({{ color: CREAM, roughness: 0.4 }})); genes.add(lk); links.push(lk); }}

  // --- lab flask (PAPER beat): glass, blue liquid, rising bubbles
  var flask = new THREE.Group(); scene.add(flask);
  var prof = [[0, -0.9], [0.62, -0.9], [0.68, -0.84], [0.66, -0.6], [0.3, 0.25], [0.2, 0.42], [0.2, 0.95], [0.25, 1.0]].map(function (p) {{ return new THREE.Vector2(p[0], p[1]); }});
  flask.add(new THREE.Mesh(new THREE.LatheGeometry(prof, 64), new THREE.MeshStandardMaterial({{ color: 0xdfe6ff, roughness: 0.1, transparent: true, opacity: 0.35, side: THREE.DoubleSide, depthWrite: false }})));
  var liq = [[0, -0.86], [0.6, -0.86], [0.62, -0.6], [0.44, -0.2], [0, -0.2]].map(function (p) {{ return new THREE.Vector2(p[0], p[1]); }});
  flask.add(new THREE.Mesh(new THREE.LatheGeometry(liq, 64), new THREE.MeshStandardMaterial({{ color: BLUE, roughness: 0.25 }})));
  var bub = []; for (var k = 0; k < 9; k++) {{ var bm = new THREE.Mesh(new THREE.SphereGeometry(0.05 + 0.03 * h(k + 40), 16, 12), new THREE.MeshStandardMaterial({{ color: 0xc8d2ff, roughness: 0.2 }})); flask.add(bm); bub.push(bm); }}
  var flSh = new THREE.Mesh(new THREE.CircleGeometry(0.9, 48), new THREE.MeshBasicMaterial({{ color: 0x1E1B18, transparent: true, opacity: 0.12 }}));
  flSh.rotation.x = -Math.PI / 2; flSh.position.y = -0.92; flask.add(flSh);

  function renderAt(t) {{
    var A = inW("A", t), G2 = inW("G2", t);
    brain.visible = A || G2; agents.visible = A; pill.visible = pillSh.visible = inW("C", t); dna.visible = inW("E", t);
    cards.visible = inW("F", t); genes.visible = inW("H", t); flask.visible = t >= T[113] && t < T[125] - 0.1;
    if (A) {{
      brain.rotation.set(0.25, -0.6 + 0.22 * t, 0); brain.position.set(0, 0.25, 0); cMat.color.set(CREAM); cbMat.color.set(CREAM);
      placeAgents(t); look(lerp3([0, 1.4, 8.2], [0, 0.7, 5.6], ss(0, W.A[1], t)), [0, 0.05, 0]);
    }}
    if (G2) {{
      var k = ss(W.G2[0], W.G2[0] + 1.4, t), lit = ss(T[89] - 0.3, T[89] + 0.3, t);
      brain.rotation.set(0.3, 2.6 + 0.25 * (t - W.G2[0]), 0); brain.position.set(0, 0.2, 0);
      cMat.color.set(0x5c6070); cbMat.color.set(new THREE.Color(CREAM).lerp(new THREE.Color(CORAL), lit));
      look(lerp3([0, 1.2, 7.2], [0, 0.6, 4.6], k), [0, 0.0, -0.4]);
    }}
    if (inW("C", t)) {{
      var sp = ss(T[31] + 0.05, T[31] + 0.6, t);
      pill.rotation.set(0.5, 0.9 * t, 0.65); pill.position.set(0, 0.55 + 0.08 * Math.sin(t * 1.8), 0);
      pTop.position.y = 0.55 * sp; pBot.position.y = -0.55 * sp; pTop.rotation.z = 0.5 * sp; pBot.rotation.z = -0.4 * sp;
      look([0, -0.1, 8.6], [0, -0.1, 0]);
    }}
    if (inW("E", t)) {{
      var lit2 = ss(T[42] - 0.2, T[42] + 0.4, t), dv = ss(T[41], T[44], t), back = ss(T[44] + 0.2, T[45] + 0.6, t);
      geneLit(lit2); dna.rotation.set(0, 0.55 * t, 0.18); dna.position.set(0, 0.6, 0);
      var gy = (22 - NB / 2) * 0.16;
      dock.position.set(1.6 - 0.95 * ss(T[38], T[42], t), gy + 0.9 * (1 - ss(T[38], T[42], t)), 0.4); dock.rotation.set(t, t * 1.4, 0);
      var far = [0, 0.8, 8.6], near = [0.4, gy + 0.75, 3.6], mid = [0, 1.6, 9.4];
      var p = lerp3(lerp3(far, near, dv), mid, back); look(p, lerp3([0, 0.5, 0], [0, gy + 0.6, 0], dv * (1 - back)));
    }}
    if (inW("F", t)) {{
      for (var c = 0; c < NC; c++) {{ var d = CD[c], k = ss(W.F[0] + 0.2 + d.d, W.F[0] + 1.6 + d.d, t);
        V.set(d.sx + (d.gx - d.sx) * k, d.sy + (d.gy - d.sy) * k, d.sz * (1 - k)); E.set(d.r * (1 - k), d.r * 0.7 * (1 - k), d.r * 0.4 * (1 - k)); Q.setFromEuler(E);
        M4.compose(V, Q, S1.set(1, 1, 1)); cards.setMatrixAt(c, M4);
        var pk = d.pat ? ss(T[63] - 0.1 + Math.abs(d.gx) * 0.12, T[63] + 0.3 + Math.abs(d.gx) * 0.12, t) : 0;
        cards.setColorAt(c, new THREE.Color(0xffffff).lerp(new THREE.Color(BLUE), pk)); }}
      cards.instanceMatrix.needsUpdate = true; cards.instanceColor.needsUpdate = true;
      cards.rotation.set(-0.25 + 0.15 * ss(W.F[0], W.F[1], t), 0.2 * Math.sin(t * 0.4), 0); cards.position.set(0, 0.15, 0);
      look([0, 0, 19.5 - 2.0 * ss(W.F[0], W.F[1], t)], [0, 0.1, 0]);
    }}
    if (inW("H", t)) {{
      var ang = 0.9 * (t - W.H[0]), pull = 1.1 - 0.35 * ss(T[95] - 0.2, T[96], t);
      genes.rotation.set(0.2, 0.25 * Math.sin(ang), 0); genes.position.set(0, 0.25, 0);
      g1m.position.set(-pull, 0.1 * Math.sin(ang * 2), 0); g2m.position.set(pull, -0.1 * Math.sin(ang * 2), 0);
      links.forEach(function (lk, i) {{ var f = (i + 0.5) / 4; lk.position.set(-pull + 2 * pull * f, 0, 0); lk.rotation.set(0, i % 2 ? Math.PI / 2 : 0, 0.0); }});
      look([0, 0.3, 8.4], [0, 0.35, 0]);
    }}
    if (flask.visible) {{
      var up = ss(T[113], T[114] + 0.4, t);
      flask.position.set(0, -1.62 + 0.3 * up, 0); flask.rotation.set(0, 0.5 * t, 0); flask.scale.setScalar(0.45 + 0.33 * up);
      bub.forEach(function (bm, i) {{ var ph = (t * 0.45 + h(i + 60)) % 1; bm.position.set(0.35 * (h(i + 70) - 0.5), -0.8 + 0.6 * ph, 0.35 * (h(i + 80) - 0.5)); bm.visible = ph < 0.98; }});
      look([0, -0.4, 7.4], [0, -1.15, 0]);
    }}
    R.render(scene, cam);
  }}
  window.addEventListener("hf-seek", function (e) {{ renderAt(e.detail.time); }});
  renderAt(window.__hfThreeTime || 0);
</script>
'''

html = page("ai-agent-sel-otak", DUR, css, body, js).replace("</body>", three + "</body>")
(pub / "index.html").write_text(html, encoding="utf-8")
print("ok", DUR, len(track), "pose events", W)
