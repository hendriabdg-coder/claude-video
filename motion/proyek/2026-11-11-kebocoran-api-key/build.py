# Reel · "3 Kesalahan yang Bikin API Key Kamu Bocor" · gaya sama dengan Hari 10 (dasar PULSE + SIGNAL/TERMINAL/PAPER/AVATAR
# + Three.js), tapi tempo motion dipercepat: masuk 0,18-0,22 dtk, ganti visual tiap ±1,5-2 dtk, rotasi 3D lebih cepat.
# 3D: kunci API (bocor jadi partikel), grafik commit git (commit lama tetap menyimpan key), hujan "secret", brankas.
# VO: Endrich generate manual (output/motion/<slug>/vo/vo-full.mp3), timing kata dari align.py. Sumber: riset.md.
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
import reel_common  # noqa: E402

reel_common.TAIL = 2.8   # VO tidak punya CTA follow/komentar: layar menahan CTA teks ±2,8 dtk setelah kata terakhir
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
#hud i { width: 12px; height: 12px; background: var(--c); display: inline-block; }
.t { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; line-height: 1; letter-spacing: -.02em; }
.sh { text-shadow: 0 4px 28px rgba(0,0,0,.95), 0 0 6px rgba(0,0,0,.8); }
.t .ch { opacity: 0; }
.cr { color: var(--cr); } .bl { color: var(--b); } .co { color: var(--c); } .kk { color: var(--k); }
.sub { text-shadow: 0 2px 16px rgba(0,0,0,.9); position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDBold"; font-size: 30px; letter-spacing: .16em; opacity: 0; }
.chip { position: absolute; font-family: "IDBold"; font-size: 22px; letter-spacing: .16em; padding: 7px 14px; border: 2px solid currentColor; border-radius: 8px; opacity: 0; }
.rep { position: absolute; left: -40px; width: 1200px; font-size: 170px; line-height: 1.02; white-space: nowrap; color: transparent; -webkit-text-stroke: 3px rgba(244,241,234,.16); opacity: 0; }
.num { position: absolute; left: 60px; top: 300px; font-size: 150px; line-height: 1; color: transparent; -webkit-text-stroke: 4px var(--c); opacity: 0; }
#big3 { position: absolute; left: 0; width: 1080px; top: 380px; text-align: center; font-size: 520px; line-height: 1; color: var(--c); opacity: 0; }
.win { position: absolute; left: 90px; width: 900px; border-radius: 22px; background: #FFFDF8; color: var(--k); opacity: 0; overflow: hidden; box-shadow: 0 30px 70px rgba(0,0,0,.45); }
.win .bar { height: 54px; background: #E9E5DC; display: flex; align-items: center; gap: 10px; padding: 0 20px; font-family: "IDBold"; font-size: 22px; color: #6b6f7a; }
.win .bar i { width: 14px; height: 14px; border-radius: 50%; background: #c9c5bc; display: inline-block; }
.win .bar span { margin-left: 16px; background: #fff; border-radius: 8px; padding: 4px 16px; letter-spacing: .04em; }
#page { top: 600px; height: 560px; }
#page .hero { margin: 40px; height: 200px; border-radius: 18px; background: var(--b); display: flex; align-items: center; justify-content: center; color: var(--cr); font-size: 54px; }
#page .ln { margin: 18px 40px; height: 22px; border-radius: 8px; background: #e4e0d6; }
#dev { position: absolute; left: 90px; top: 960px; width: 900px; height: 330px; border-radius: 0 0 22px 22px; background: #0B0D12; border-top: 3px solid var(--b); opacity: 0; padding: 20px 30px; font-family: Consolas, "Courier New", monospace; font-size: 32px; line-height: 1.55; color: var(--cr); white-space: pre; }
#dev .tb { font-family: "IDBold"; font-size: 22px; letter-spacing: .14em; color: var(--g); margin-bottom: 10px; }
#dev b { color: var(--b); font-weight: normal; } #dev u { color: var(--c); text-decoration: none; background: rgba(255,79,58,.15); }
#devhl { position: absolute; left: 110px; top: 1062px; width: 860px; height: 54px; border: 4px solid var(--c); border-radius: 10px; opacity: 0; }
.leak { position: absolute; left: 90px; width: 900px; height: 230px; border-radius: 22px; opacity: 0; padding: 26px 32px; display: flex; gap: 26px; align-items: center; }
.leak .li { width: 120px; height: 120px; flex: none; border-radius: 26px; padding: 26px; }
.leak .lt { font-size: 50px; line-height: 1.05; }
.leak .lc { font-family: Consolas, "Courier New", monospace; font-size: 30px; margin-top: 12px; }
.leak .lc u { color: var(--c); text-decoration: none; background: rgba(255,79,58,.16); padding: 0 6px; }
#lk1 { top: 520px; background: var(--cr); color: var(--k); } #lk1 .li { background: var(--k); color: var(--cr); }
#lk2 { top: 790px; background: #0B0D12; color: var(--cr); border: 2px solid rgba(244,241,234,.2); } #lk2 .li { background: var(--c); color: var(--cr); }
#lk3 { top: 1060px; background: var(--b); color: var(--cr); } #lk3 .li { background: var(--cr); color: var(--b); }
#n28 { position: absolute; left: 0; width: 1080px; top: 520px; text-align: center; font-size: 230px; line-height: 1; font-variant-numeric: tabular-nums; color: var(--cr); text-shadow: 0 6px 40px rgba(0,0,0,.95); opacity: 0; }
.imp { position: absolute; left: 90px; width: 900px; height: 170px; border-radius: 22px; background: var(--cr); color: var(--k); display: flex; align-items: center; gap: 26px; padding: 0 32px; font-size: 48px; opacity: 0; }
.imp .ii { width: 104px; height: 104px; flex: none; border-radius: 50%; background: var(--c); color: var(--cr); padding: 24px; }
#bal { position: absolute; left: 230px; top: 790px; width: 640px; height: 26px; border-radius: 13px; background: rgba(14,14,14,.15); overflow: hidden; opacity: 0; }
#balf { width: 100%; height: 100%; background: var(--c); transform-origin: 0 50%; }
.chk { position: absolute; left: 90px; width: 900px; height: 130px; border-radius: 22px; background: #FFFDF8; color: var(--k); display: flex; align-items: center; gap: 24px; padding: 0 30px; font-size: 46px; opacity: 0; box-shadow: 0 20px 40px rgba(30,27,24,.12); }
.chk .ck { width: 74px; height: 74px; flex: none; border-radius: 50%; background: var(--b); color: var(--cr); display: flex; align-items: center; justify-content: center; font-size: 42px; }
#follow { position: absolute; left: 330px; top: 470px; width: 420px; height: 100px; border-radius: 50px; background: var(--cr); color: var(--k); font-size: 46px; display: flex; align-items: center; justify-content: center; opacity: 0; }
#tapc { position: absolute; left: 670px; top: 515px; width: 70px; height: 70px; color: var(--k); opacity: 0; }
.opt { position: absolute; top: 470px; width: 420px; height: 120px; border-radius: 22px; display: flex; align-items: center; gap: 16px; padding: 0 24px; font-size: 36px; line-height: 1.05; opacity: 0; }
.opt .ol { width: 62px; height: 62px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 38px; flex: none; }
#oA { left: 100px; background: var(--b); color: var(--cr); } #oA .ol { background: var(--cr); color: var(--b); }
#oB { left: 560px; background: var(--c); color: var(--cr); } #oB .ol { background: var(--cr); color: var(--c); }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-size: 36px; color: var(--cr); z-index: 6; }
#brand b { color: var(--c); font-weight: normal; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; pointer-events: none; }
'''


def TX(tid, text, top, px, cls="cr sh", maxw=760):
    return f'<div class="t {cls}" id="{tid}" style="top:{top}px;font-size:{fitpx(text, px, maxw)}px">{chars(text)}</div>'


def SUB(tid, text, top, color="var(--cr)"):
    return f'<div class="sub" id="{tid}" style="top:{top}px;color:{color}">{text}</div>'


def REP(tid, word, top):
    return f'<div class="rep" id="{tid}" style="top:{top}px">{(" " + word) * 6}</div>'


def svg(body, sw=7):
    return (f'<svg class="ico" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>')


CAMI = svg('<rect x="10" y="26" width="80" height="56" rx="10"/><circle cx="50" cy="54" r="15"/><path d="M34 26l6-10h20l6 10"/>')
LOGI = svg('<path d="M14 18h72v64H14z"/><path d="M26 36l12 10-12 10M46 58h24"/>')
BOTI = svg('<rect x="18" y="30" width="64" height="48" rx="12"/><path d="M50 30V16"/><circle cx="50" cy="13" r="4"/><circle cx="38" cy="52" r="5"/><circle cx="62" cy="52" r="5"/><path d="M40 66h20"/>')
CARD = svg('<rect x="10" y="22" width="80" height="56" rx="10"/><path d="M10 40h80M24 62h20"/>')
DB = svg('<ellipse cx="50" cy="22" rx="32" ry="11"/><path d="M18 22v56c0 6 14 11 32 11s32-5 32-11V22M18 50c0 6 14 11 32 11s32-5 32-11"/>')
BUG = svg('<path d="M30 38h40v26a20 20 0 0 1-40 0z"/><path d="M38 38a12 12 0 0 1 24 0M50 44v38M30 50H14M70 50h16M30 66H16M70 66h14M34 30l-8-10M66 30l8-10"/>')

# chibi (AVATAR) di penutup: mikir di "pernah pakai AI buat coding", tunjuk di "cek lagi", kaget di "ikut terkirim"
t_cta = T[147] - 0.1
track, emph_t = chibi_track(HERE, t_cta, DUR, [(T[147] + 0.2, "mikir"), (T[150], "netral"), (T[154] - 0.1, "tunjuk"),
                                               (T[156] + 0.3, "netral"), (T[161], "kaget"), (T[163] + 0.5, "netral"),
                                               (T[163] + 1.6, "lambai")], blinks=(T[152], T[160]))

body = f'''
  <div id="bg"></div>
  <canvas id="three" width="1080" height="1920"></canvas>
  <div id="grain"></div>
  <div id="cam">
    <div id="hud"><i></i>KEAMANAN AI &middot; API KEY</div>
    <!-- A hook: 3D key -->
    {TX("a1", "WEBSITE / APLIKASI", 340, 92)}
    {TX("a2", "+ AI?", 1250, 150, "bl sh")}
    <!-- B hati-hati -->
    {REP("rB1", "AWAS", 380)}{REP("rB2", "AWAS", 1150)}
    {TX("b1", "HATI-HATI!", 820, 200, "cr", 900)}
    <!-- C 3 kesalahan, key leaks -->
    <div id="big3">3</div>
    {TX("c1", "KESALAHAN", 950, 130)}
    {TX("c2", "API KEY BOCOR", 330, 100, "co sh")}
    {TX("c3", "YANG KE-3?", 1250, 110)}
    {SUB("c4", "SERING NGGAK DISADARI", 1380)}
    <!-- D 01 GitHub -->
    <div class="num" id="d0">01</div>
    {TX("d1", "UPLOAD KE GITHUB", 470, 96)}
    {TX("d2", "ORANG LAIN BISA NEMU", 1250, 84)}
    {TX("d3", "MASIH ADA DI RIWAYAT", 1250, 84, "co sh")}
    {SUB("d4", "WALAU SUDAH DIHAPUS DARI KODE TERBARU", 1370)}
    <div class="chip" id="simD" style="left:60px;top:1450px;color:#8A8F9C">ILUSTRASI</div>
    <!-- E 02 front-end -->
    <div class="num" id="e0">02</div>
    {TX("e1", "KEY DI FRONT-END", 470, 96, "cr")}
    <div class="win" id="page"><div class="bar"><i></i><i></i><i></i><span>tokokamu.com</span></div>
      <div class="hero">Tanya AI</div><div class="ln"></div><div class="ln" style="width:60%"></div><div class="ln" style="width:75%"></div></div>
    {TX("e2", "NGGAK KELIHATAN...", 1200, 84, "cr")}
    <div id="dev"><div class="tb">DEVTOOLS &middot; SOURCES &middot; app.js</div><b>const</b> API_KEY =
  <u>"sk-proj-••••••••••••••••"</u>;
<b>fetch</b>("https://api…", {{ headers: … }})</div>
    <div id="devhl"></div>
    {TX("e3", "TERBACA DI BROWSER", 1330, 90, "co sh")}
    <div class="chip" id="simE" style="left:60px;top:1450px;color:#8A8F9C">SIMULASI</div>
    <!-- F 03 menarik -->
    {REP("rF1", "KETIGA", 380)}{REP("rF2", "KETIGA", 1150)}
    {TX("f1", "YANG KETIGA", 700, 150, "cr", 900)}
    {TX("f2", "INI MENARIK", 900, 150, "kk", 900)}
    <!-- G leaks -->
    <div class="num" id="g0">03</div>
    {TX("g1", "TANPA SADAR KAMU BAGIKAN", 330, 80)}
    <div class="leak" id="lk1"><div class="li">{CAMI}</div><div><div class="lt">SCREENSHOT</div><div class="lc">.env &nbsp;<u>OPENAI_KEY=sk-…</u></div></div></div>
    <div class="leak" id="lk2"><div class="li">{BUG}</div><div><div class="lt">LOG ERROR</div><div class="lc">401 key=<u>sk-…</u></div></div></div>
    <div class="leak" id="lk3"><div class="li">{BOTI}</div><div><div class="lt">CHAT AI CODING</div><div class="lc">"tolong cek: <u>sk-…</u>"</div></div></div>
    <div class="chip" id="simG" style="left:60px;top:1450px;color:#8A8F9C">SIMULASI</div>
    <!-- H GitGuardian -->
    {SUB("h0", "GITGUARDIAN &middot; STATE OF SECRETS SPRAWL 2026", 330, "var(--g)")}
    <div id="n28">0</div>
    {SUB("h1b", "JUTA", 770)}
    {TX("h1", "SECRET BARU", 840, 110, "co sh")}
    {TX("h2", "DI COMMIT GITHUB PUBLIK", 1250, 76)}
    {SUB("h3", "SEPANJANG 2025", 1350)}
    <!-- I dampak -->
    {TX("i0", "KALAU BOCOR:", 330, 110, "kk")}
    <div class="imp" id="im1" style="top:480px"><div class="ii">{CARD}</div>LAYANAN DISALAHGUNAKAN</div>
    <div class="imp" id="im2" style="top:690px"><div class="ii">{ICON["alert"]}</div>SALDO API HABIS</div>
    <div id="bal" style="top:832px"><div id="balf"></div></div>
    <div class="imp" id="im3" style="top:920px"><div class="ii">{DB}</div>DATA BISA DIAKSES</div>
    <div class="chip" id="i4" style="left:330px;top:1130px;color:#0E0E0E;font-size:30px">TERGANTUNG IZIN KEY</div>
    <!-- J solusi -->
    {TX("j0", "JADI:", 330, 110, "kk")}
    <div class="chk" id="k1" style="top:460px"><div class="ck">&#10003;</div>SIMPAN DI BACK-END</div>
    <div class="chk" id="k2" style="top:610px"><div class="ck">&#10003;</div>BATASI AKSESNYA</div>
    <div class="chk" id="k3" style="top:760px"><div class="ck">&#10003;</div>JANGAN DIBAGIKAN</div>
    <div class="chip" id="k4" style="left:250px;top:930px;color:#FF4F3A;font-size:28px">SUDAH BOCOR? GANTI (ROTASI) KEY</div>
    <!-- K penutup + CTA -->
    {TX("m1", "PERNAH PAKAI AI BUAT CODING?", 330, 74)}
    {TX("m2", "CEK LAGI.", 450, 120, "co sh")}
    {TX("m3", "KEY-MU IKUT TERKIRIM?", 330, 80)}
    <div id="follow">+ FOLLOW</div><div id="tapc">{ICON["cursor"]}</div>
    {SUB("m4", "SERI KEAMANAN AI &middot; TIPS TIAP MINGGU", 360)}
    <div class="opt" id="oA"><div class="ol">A</div>UDAH<br>AKU CEK</div>
    <div class="opt" id="oB"><div class="ol">B</div>BELUM<br>PERNAH</div>
    {SUB("m5", "JAWAB A ATAU B DI KOMENTAR", 610)}
    {chibi_html()}
  </div>
  <div id="flash"></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

W = {
    "A": (0.0, T[9] - 0.08), "B": (T[9] - 0.08, T[10] - 0.08), "C": (T[10] - 0.08, T[27] - 0.08), "D": (T[27] - 0.08, T[51] - 0.08),
    "E": (T[51] - 0.08, T[71] - 0.08), "F": (T[71] - 0.08, T[77] - 0.08), "G": (T[77] - 0.08, T[94] - 0.08),
    "H": (T[94] - 0.08, T[112] - 0.08), "I": (T[112] - 0.08, T[134] - 0.08), "J": (T[134] - 0.08, T[147] - 0.08),
    "K": (T[147] - 0.08, DUR + 1),
}
W = {k: (round(a, 3), round(b, 3)) for k, (a, b) in W.items()}
BG = {"A": "#0E0E0E", "B": "#FF4F3A", "C": "#0E0E0E", "D": "#0E0E0E", "E": "#0E0E0E", "F": "#3A5BFF", "G": "#0E0E0E",
      "H": "#0E0E0E", "I": "#F4F1EA", "J": "#F4F1EA", "K": "#0E0E0E"}
LIGHT = ["I", "J"]

js = f'''
    var T = {json.dumps(T)}, DUR = {DUR}, W = {json.dumps(W)}, BG = {json.dumps(BG)}, LIGHT = {json.dumps(LIGHT)};
    // tempo cepat: masuk 0,18-0,22 dtk
    function slam(sel, t, s) {{ tl.set(sel + " .ch", {{ opacity: 1 }}, q(t)); tl.fromTo(sel, {{ opacity: 0, scale: s || 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "back.out(1.8)" }}, q(t)); }}
    function zip(sel, t) {{ var ch = document.querySelectorAll(sel + " .ch"); tl.set(sel, {{ opacity: 1 }}, q(t));
      tl.fromTo(ch, {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.16, ease: "back.out(2)", stagger: Math.min(0.018, 0.3 / ch.length) }}, q(t)); }}
    function rise(sel, t, d) {{ tl.fromTo(sel, {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: d || 0.22, ease: "back.out(1.6)" }}, q(t)); }}
    function slide(sel, t, x) {{ tl.fromTo(sel, {{ opacity: 0, x: x || -140 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "back.out(1.5)" }}, q(t)); }}
    function off(sel, t) {{ tl.set(sel, {{ opacity: 0 }}, q(t)); }}
    function repIn(a, b, t, t1) {{ tl.fromTo(a, {{ opacity: 1, x: 0 }}, Object.assign({{ x: -360, duration: t1 - t, ease: "none" }}, NI), q(t));
      tl.fromTo(b, {{ opacity: 1, x: -360 }}, Object.assign({{ x: 0, duration: t1 - t, ease: "none" }}, NI), q(t)); off(a + "," + b, t1); }}
    Object.keys(W).forEach(function (k) {{
      var lt = LIGHT.indexOf(k) >= 0;
      tl.set("#bg", {{ backgroundColor: BG[k] }}, q(W[k][0]));
      tl.set("#hud, #brand", {{ color: lt ? "#0E0E0E" : "#F4F1EA" }}, q(W[k][0]));
      var ac = BG[k] == "#FF4F3A" ? "#0E0E0E" : "#FF4F3A";
      tl.set("#brand b", {{ color: ac }}, q(W[k][0])); tl.set("#hud i", {{ backgroundColor: ac }}, q(W[k][0]));
      if (k != "A") flash(W[k][0], "#flash", 0.12);
    }});
    tl.fromTo("#hud", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power3.out" }}, 0.05);

    // A HOOK
    zip("#a1", 0.05); slam("#a2", T[7] - 0.05, 1.6); kick(T[7] + 0.1, 12);
    off("#a1, #a2", W.A[1]);
    // B
    repIn("#rB1", "#rB2", W.B[0], W.B[1]); slam("#b1", W.B[0], 1.7); kick(W.B[0], -16); off("#b1", W.B[1]);
    // C 3 kesalahan, key bocor
    tl.fromTo("#big3", {{ opacity: 0, scale: 2.2, rotation: -8 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.2, ease: "back.out(1.6)" }}, q(T[11] - 0.05));
    kick(T[11] + 0.15, 16); zip("#c1", T[12]);
    off("#big3, #c1", T[16] - 0.1);
    slam("#c2", T[16] - 0.05); kick(T[19], 12);
    zip("#c3", T[22] - 0.05); rise("#c4", T[25] - 0.1, 0.2);
    off("#c2, #c3, #c4", W.C[1]);
    // D 01 GitHub, commit graph 3D
    slide("#d0", W.D[0], -80); zip("#d1", W.D[0] + 0.05);
    zip("#d2", T[40] - 0.05); off("#d2", T[44] - 0.1);
    zip("#d3", T[47] - 0.05); rise("#d4", T[48], 0.2); cut("#simD", W.D[0] + 0.2, 1);
    off("#d0, #d1, #d3, #d4, #simD", W.D[1]);
    // E 02 front-end
    slide("#e0", W.E[0], -80); zip("#e1", W.E[0] + 0.05);
    tl.fromTo("#page", {{ opacity: 0, y: 120, rotation: 2 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.24, ease: "back.out(1.4)" }}, q(T[56] - 0.1));
    zip("#e2", T[59]); off("#e2", T[64] - 0.1);
    tl.fromTo("#dev", {{ opacity: 0, y: 340 }}, {{ opacity: 1, y: 0, duration: 0.24, ease: "power3.out" }}, q(T[64] - 0.05));
    cut("#simE", T[56], 1);
    tl.fromTo("#devhl", {{ opacity: 0, scale: 1.2 }}, {{ opacity: 1, scale: 1, duration: 0.16, ease: "power3.out" }}, q(T[67]));
    tl.to("#devhl", {{ opacity: 0.3, duration: 0.12, yoyo: true, repeat: 3, ease: "steps(1)" }}, q(T[67] + 0.2));
    zip("#e3", T[68]); kick(T[68] + 0.1, 12);
    off("#e0, #e1, #page, #dev, #devhl, #e3, #simE", W.E[1]);
    // F 03 menarik (PULSE biru)
    repIn("#rF1", "#rF2", W.F[0], W.F[1]); slam("#f1", W.F[0], 1.6); kick(W.F[0], -16); slam("#f2", T[74] - 0.05, 1.6); kick(T[74], 14);
    off("#f1, #f2", W.F[1]);
    // G leaks: screenshot / log / AI chat
    slide("#g0", W.G[0], -80); zip("#g1", W.G[0] + 0.05); cut("#simG", W.G[0] + 0.1, 1);
    slide("#lk1", T[84] - 0.1, -200); flash(T[84] - 0.05, "#flash", 0.5);
    slide("#lk2", T[85] - 0.05, 200); kick(T[85] + 0.1, 10);
    slide("#lk3", T[90] - 0.05, -200); kick(T[91], 10);
    tl.to("#lk1 .lc u, #lk2 .lc u, #lk3 .lc u", {{ backgroundColor: "rgba(255,79,58,.45)", duration: 0.12, yoyo: true, repeat: 5 }}, q(T[92]));
    off("#g0, #g1, #lk1, #lk2, #lk3, #simG", W.H[0]);
    // H GitGuardian: 28,6 juta
    rise("#h0", W.H[0] + 0.05, 0.2);
    tl.fromTo("#n28", {{ opacity: 0, scale: 1.5 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(1.6)" }}, q(T[100] - 0.3));
    count("#n28", T[100] - 0.3, 1.0, 0, 28.65, function (v) {{ return v.toFixed(2).replace(".", ","); }});
    kick(T[100] + 0.75, 16); rise("#h1b", T[101] - 0.05, 0.18); slam("#h1", T[102] - 0.05); zip("#h2", T[106] - 0.05); rise("#h3", T[109], 0.2);
    off("#h0, #n28, #h1b, #h1, #h2, #h3", W.H[1]);
    // I dampak (krem)
    zip("#i0", W.I[0] + 0.05);
    slide("#im1", T[122] - 0.1, -200); slide("#im2", T[124] - 0.05, 200);
    tl.set("#bal", {{ opacity: 1 }}, q(T[124] + 0.1));
    tl.fromTo("#balf", {{ scaleX: 1 }}, {{ scaleX: 0.04, duration: 1.1, ease: "power2.in" }}, q(T[124] + 0.15));
    slide("#im3", T[128] - 0.05, -200); kick(T[129], 10);
    tl.fromTo("#i4", {{ opacity: 0, scale: 1.4, rotation: -4 }}, {{ opacity: 1, scale: 1, rotation: -4, duration: 0.18, ease: "power4.in" }}, q(T[130]));
    off("#i0, #im1, #im2, #bal, #im3, #i4", W.I[1]);
    // J solusi (PAPER checklist) + brankas 3D
    zip("#j0", W.J[0] + 0.05);
    slide("#k1", T[135] - 0.05, -200); slide("#k2", T[140] - 0.05, 200); slide("#k3", T[143] - 0.05, -200);
    rise("#k4", T[145], 0.2);
    off("#j0, #k1, #k2, #k3, #k4", W.J[1]);
    // K penutup (AVATAR) + CTA layar (VO tidak memuat CTA follow/komentar)
    zip("#m1", W.K[0] + 0.05); off("#m1", T[154] - 0.1);
    slam("#m2", T[154] - 0.05); kick(T[154] + 0.1, 12); off("#m2", T[157] - 0.1);
    zip("#m3", T[157]);
    off("#m3", T[163] + 0.75);
    tl.fromTo("#follow", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.24, ease: "back.out(2.2)" }}, q(T[163] + 0.8));
    rise("#m4", T[163] + 0.85, 0.2);
    tl.fromTo("#tapc", {{ opacity: 0, x: 60, y: 60 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.22, ease: "power2.out" }}, q(T[163] + 1.05));
    tl.to("#follow", {{ scale: 0.92, duration: 0.07, yoyo: true, repeat: 1 }}, q(T[163] + 1.3));
    tl.to("#follow", {{ backgroundColor: "#FF4F3A", color: "#F4F1EA", duration: 0.08 }}, q(T[163] + 1.37));
    tl.set("#follow", {{ innerHTML: "&#10003; FOLLOWING" }}, q(T[163] + 1.37));
    off("#follow, #tapc, #m4", T[163] + 1.75);
    slide("#oA", T[163] + 1.8, -120); slide("#oB", T[163] + 1.95, 120); rise("#m5", T[163] + 2.1, 0.2);
'''
js += chibi_js(track, emph_t, t_cta)

three = f'''
<script type="importmap">{{"imports": {{"three": "./vendor/three.module.min.js"}}}}</script>
<script type="module">
  import * as THREE from "three";
  var T = {json.dumps(T)}, W = {json.dumps(W)};
  var R = new THREE.WebGLRenderer({{ canvas: document.getElementById("three"), alpha: true, antialias: true, preserveDrawingBuffer: true }});
  R.setPixelRatio(1); R.setSize(1080, 1920, false); R.setClearColor(0x000000, 0);
  R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.0;
  var scene = new THREE.Scene(), cam = new THREE.PerspectiveCamera(32, 1080 / 1920, 0.05, 100);
  scene.add(new THREE.HemisphereLight(0xf4f1ea, 0x1a1d2e, 1.1));
  var key = new THREE.DirectionalLight(0xfff1e0, 2.4); key.position.set(-3, 5, 5); scene.add(key);
  var rim = new THREE.DirectionalLight(0xff9a8a, 1.5); rim.position.set(4, 1, -4); scene.add(rim);
  var BLUE = 0x3A5BFF, CORAL = 0xFF4F3A, CREAM = 0xF4F1EA;
  function h(i) {{ var x = Math.sin(i * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); }}
  function ss(a, b, t) {{ var x = Math.min(1, Math.max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x); }}
  function inW(k, t) {{ return t >= W[k][0] && t < W[k][1]; }}
  function look(p, c) {{ cam.position.set(p[0], p[1], p[2]); cam.lookAt(c[0], c[1], c[2]); }}
  var M4 = new THREE.Matrix4(), Q = new THREE.Quaternion(), E = new THREE.Euler(), V = new THREE.Vector3(), S1 = new THREE.Vector3(1, 1, 1);

  // --- API key (kunci): kepala ring + batang + gigi
  function makeKey(mat) {{
    var g = new THREE.Group();
    var head = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.14, 24, 64), mat); head.position.x = -0.95; g.add(head);
    var shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 1.5, 24), mat); shaft.rotation.z = Math.PI / 2; shaft.position.x = 0.15; g.add(shaft);
    [[0.55, 0.22], [0.78, 0.3], [0.98, 0.18]].forEach(function (d) {{ var b = new THREE.Mesh(new THREE.BoxGeometry(0.12, d[1], 0.12), mat); b.position.set(d[0], -0.1 - d[1] / 2, 0); g.add(b); }});
    return g;
  }}
  var keyMat = new THREE.MeshStandardMaterial({{ color: CREAM, roughness: 0.35, metalness: 0.35 }});
  var bigKey = makeKey(keyMat); scene.add(bigKey);
  // leak particles streaming out of the key
  var NL = 420, leak = new THREE.InstancedMesh(new THREE.BoxGeometry(0.05, 0.05, 0.05), new THREE.MeshStandardMaterial({{ color: CORAL, roughness: 0.4 }}), NL); scene.add(leak);

  // --- git commit graph: main line + branch; commit 3 menyimpan key (coral), commit baru masuk di kanan
  var git = new THREE.Group(); scene.add(git);
  var nodeG = new THREE.SphereGeometry(0.22, 32, 20), linkG = new THREE.CylinderGeometry(0.05, 0.05, 1, 12);
  var gm = new THREE.MeshStandardMaterial({{ color: CREAM, roughness: 0.4 }}), gb = new THREE.MeshStandardMaterial({{ color: BLUE, roughness: 0.4 }});
  var badM = new THREE.MeshStandardMaterial({{ color: CORAL, roughness: 0.35, emissive: CORAL, emissiveIntensity: 0.0 }});
  var NODES = [], NN = 9;
  for (var i = 0; i < NN; i++) {{ var m = new THREE.Mesh(nodeG, i == 3 ? badM : (i >= 6 ? gb : gm)); m.position.set(-3.2 + i * 0.8, 0, 0); git.add(m); NODES.push(m);
    if (i > 0) {{ var l = new THREE.Mesh(linkG, i >= 6 ? gb : gm); l.rotation.z = Math.PI / 2; l.scale.y = 0.8; l.position.set(-3.6 + i * 0.8, 0, 0); git.add(l); NODES.push(l); }} }}
  var miniKey = makeKey(new THREE.MeshStandardMaterial({{ color: CORAL, roughness: 0.35, metalness: 0.2 }})); miniKey.scale.setScalar(0.32); git.add(miniKey);
  var eye = new THREE.Mesh(new THREE.TorusGeometry(0.34, 0.05, 16, 48), new THREE.MeshStandardMaterial({{ color: CORAL, roughness: 0.4 }})); git.add(eye);

  // --- hujan secret: ribuan kunci mini (kotak pipih) jatuh
  var NR = 1400, rain = new THREE.InstancedMesh(new THREE.BoxGeometry(0.06, 0.2, 0.03), new THREE.MeshStandardMaterial({{ color: 0xffffff, roughness: 0.4 }}), NR); scene.add(rain);
  var cc = [new THREE.Color(CREAM), new THREE.Color(CORAL), new THREE.Color(BLUE)];
  for (var r = 0; r < NR; r++) rain.setColorAt(r, cc[r % 7 == 0 ? 1 : (r % 5 == 0 ? 2 : 0)]);

  // --- brankas (back-end): badan + pintu berengsel, kunci terbang masuk
  var vault = new THREE.Group(); scene.add(vault);
  var vm = new THREE.MeshStandardMaterial({{ color: 0x2a2d36, roughness: 0.45, metalness: 0.4 }}), vd = new THREE.MeshStandardMaterial({{ color: BLUE, roughness: 0.35, metalness: 0.3 }});
  [[0, 1.0, 0, 2.2, 0.15, 1.8], [0, -1.0, 0, 2.2, 0.15, 1.8], [-1.05, 0, 0, 0.15, 2.1, 1.8], [1.05, 0, 0, 0.15, 2.1, 1.8], [0, 0, -0.85, 2.2, 2.1, 0.15]].forEach(function (b) {{
    var m = new THREE.Mesh(new THREE.BoxGeometry(b[3], b[4], b[5]), vm); m.position.set(b[0], b[1], b[2]); vault.add(m); }});
  var hinge = new THREE.Group(); hinge.position.set(-1.05, 0, 0.9); vault.add(hinge);
  var door = new THREE.Mesh(new THREE.BoxGeometry(2.1, 2.0, 0.16), vd); door.position.set(1.05, 0, 0); hinge.add(door);
  var dial = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.07, 16, 48), new THREE.MeshStandardMaterial({{ color: CREAM, roughness: 0.3, metalness: 0.5 }})); dial.position.set(1.05, 0, 0.12); hinge.add(dial);
  var vKey = makeKey(keyMat.clone()); vKey.scale.setScalar(0.5); scene.add(vKey);
  var vSh = new THREE.Mesh(new THREE.CircleGeometry(1.6, 48), new THREE.MeshBasicMaterial({{ color: 0x1E1B18, transparent: true, opacity: 0.14 }})); vSh.rotation.x = -Math.PI / 2; vSh.position.y = -1.1; vault.add(vSh);

  function renderAt(t) {{
    var kv = t < W.D[0];
    bigKey.visible = kv; leak.visible = inW("C", t); git.visible = inW("D", t); rain.visible = inW("H", t);
    vault.visible = vKey.visible = inW("J", t);
    if (kv) {{
      var sp = 1.6 * t;
      bigKey.rotation.set(0.35 + 0.15 * Math.sin(t * 2), sp, 0.25 * Math.sin(t * 1.3));
      var y = inW("C", t) ? -0.75 : 0.05; bigKey.position.set(0.12, y, 0); bigKey.scale.setScalar(inW("B", t) ? 0.85 : 0.68);
      var crack = ss(T[19] - 0.2, T[19] + 0.3, t);
      keyMat.color.set(new THREE.Color(CREAM).lerp(new THREE.Color(CORAL), crack));
      look([0, 0.1, 8.4], [0, -0.05, 0]);
    }}
    if (leak.visible) {{
      for (var i = 0; i < NL; i++) {{ var t0 = T[19] - 0.2 + h(i + 3) * 0.6, age = t - t0, p = ((age * 0.9 + h(i + 9)) % 1.6);
        if (age < 0) {{ V.set(0, -100, 0); }} else {{ var a = h(i + 5) * 6.28;
          V.set(0.75 + p * (1.2 + h(i) * 1.5) * Math.cos(a) * 0.5, -0.95 - p * (1.2 + 2 * h(i + 1)), p * 1.5 * Math.sin(a) * 0.6); }}
        E.set(t * 3 + i, t * 2 + i, 0); Q.setFromEuler(E); M4.compose(V, Q, S1.set(1, 1, 1)); leak.setMatrixAt(i, M4); }}
      leak.instanceMatrix.needsUpdate = true;
    }}
    if (git.visible) {{
      var d0 = W.D[0], add = ss(T[44] - 0.1, T[46], t), glow = ss(T[33] - 0.2, T[34], t), stay = ss(T[47] - 0.2, T[48], t);
      for (var i = 0; i < NN; i++) {{ var n = NODES[i == 0 ? 0 : i * 2 - 1]; var k = i >= 6 ? add : ss(d0 + i * 0.07, d0 + i * 0.07 + 0.25, t);
        n.scale.setScalar(Math.max(k, 0.001)); if (i > 0) NODES[i * 2].scale.set(1, 0.8 * Math.max(k, 0.001), 1); }}
      badM.emissiveIntensity = 0.5 * glow + 0.35 * stay * (0.6 + 0.4 * Math.sin(t * 12));
      miniKey.position.set(-0.8, 0.62 + 0.06 * Math.sin(t * 4), 0); miniKey.rotation.set(0.3, t * 2.2, 0); miniKey.visible = t > T[33] - 0.2;
      eye.visible = t > T[40] - 0.1 && t < T[44]; eye.position.set(-0.8, 0, 0.5); eye.rotation.set(0, 0, 0); eye.scale.setScalar(1 + 0.15 * Math.sin(t * 9));
      git.rotation.set(0.25, -0.35 + 0.08 * Math.sin(t * 1.5), 0); git.position.set(0, -0.1, 0);
      var pan = ss(T[44] - 0.2, T[47], t);
      look([-0.6 + 1.2 * pan, 0.7, 11.5 - 1.0 * ss(T[47], T[49], t)], [-0.6 + 1.0 * pan - 0.4 * ss(T[47], T[49], t), -0.05, 0]);
    }}
    if (rain.visible) {{
      for (var r = 0; r < NR; r++) {{ var sp2 = 2.2 + 2.2 * h(r + 1), y = 6 - ((t * sp2 + h(r + 2) * 12) % 12);
        V.set((h(r + 3) - 0.5) * 7, y, -1 - 5 * h(r + 4)); E.set(t * 2 + r, t * 3 + r * 2, r); Q.setFromEuler(E);
        var dens = r < NR * (0.15 + 0.85 * ss(T[100] - 0.3, T[100] + 0.8, t)) ? 1 : 0.0001; M4.compose(V, Q, S1.set(dens, dens, dens)); rain.setMatrixAt(r, M4); }}
      rain.instanceMatrix.needsUpdate = true; look([0, 0, 7], [0, 0, -2]);
    }}
    if (vault.visible) {{
      var fly = ss(T[135], T[137], t), close = ss(T[138] - 0.1, T[139] + 0.2, t);
      vault.rotation.set(0.15, -0.5 + 0.12 * Math.sin(t * 1.4), 0); vault.position.set(0, -2.4, 0); vault.scale.setScalar(0.5);
      hinge.rotation.y = -1.9 * (1 - close); dial.rotation.z = t * 3 * close;
      vKey.position.set(2.2 - 2.2 * fly, -2.0 + 0.8 * (1 - fly) * Math.sin(fly * 3.14), 1.6 - 1.9 * fly); vKey.rotation.set(0, t * 3, 0.4 * (1 - fly));
      vKey.visible = fly < 0.98 || close < 0.6;
      look([0, -0.6, 8.6], [0, -1.7, 0]);
    }}
    R.render(scene, cam);
  }}
  window.addEventListener("hf-seek", function (e) {{ renderAt(e.detail.time); }});
  renderAt(window.__hfThreeTime || 0);
</script>
'''

html = page("kebocoran-api-key", DUR, css, body, js).replace("</body>", three + "</body>")
(pub / "index.html").write_text(html, encoding="utf-8")
print("ok", DUR, len(track), "pose events", W)
