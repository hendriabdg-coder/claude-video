# Reel · "Peris.ai juara 1 Korea-ASEAN AI Youth Festa: pelajaran keamanan buat UMKM" · 9:16 · VO manual Endrich (53,3 dtk).
# Timing dari align.py, sumber riset.md. Rekaman acara (aset/screen.mp4) ditempel di kartu #vcard lewat compose.py setelah render.
# Gaya dasar TERMINAL/EMBER (navy gelap, cyan, merah) + per beat:
#   hook PULSE (piala + perisai) · ancaman EMBER/TERMINAL (log serangan) · kemenangan SHOWCASE (rekaman acara + chip)
#   agentic AI SIGNAL (siklus deteksi-analisis-tindak, 24/7) · besar vs kecil PAPER/SIGNAL · 3 ancaman UMKM EMBER
#   langkah dasar GUIDE (checklist) · CTA AVATAR (chibi + opsi A/B + follow)
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
import reel_common  # noqa: E402

reel_common.TAIL = 1.2
from reel_common import chars, chibi_html, chibi_js, chibi_track, fitpx, page, setup, svg, words  # noqa: E402

SLUG = HERE.name
DUR = setup(HERE, SLUG)
T = words(SLUG)
VC = dict(left=200, top=400, w=680, h=921, b=8)   # kartu video (compose.py membaca nilai yang sama)

css = '''
:root { --k:#070B14; --cr:#EEF2F7; --c:#22D3EE; --r:#FF4F3A; --g:#22C55E; --y:#FBBF24; --gy:#8391A7; --o:#FF6A3D; }
html, body, #root { background: var(--k); color: var(--cr); font-family: "IDBlack"; }
#bg { position: absolute; inset: 0; background: radial-gradient(120% 70% at 50% 40%, #0F1830 0%, var(--k) 70%); }
#glow { position: absolute; inset: 0; background: radial-gradient(70% 45% at 50% 55%, rgba(255,79,58,.35), rgba(255,79,58,0) 70%); opacity: 0; }
#grid { position: absolute; inset: 0; opacity: .08; background-image: linear-gradient(var(--c) 1px, transparent 1px), linear-gradient(90deg, var(--c) 1px, transparent 1px); background-size: 90px 90px; }
#scan { position: absolute; left: 0; top: 0; width: 1080px; height: 6px; background: linear-gradient(90deg, transparent, rgba(34,211,238,.6), transparent); opacity: .5; }
#cam { position: absolute; inset: 0; }
#hud { position: absolute; left: 60px; top: 262px; display: flex; align-items: center; gap: 12px; font-family: "IDBold"; font-size: 24px; letter-spacing: .18em; opacity: 0; z-index: 5; }
#hud i { width: 12px; height: 12px; border-radius: 50%; background: var(--c); display: inline-block; }
.t { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; line-height: 1; letter-spacing: -.02em; }
.t .ch { opacity: 0; }
.sub { position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDBold"; font-size: 30px; letter-spacing: .16em; opacity: 0; color: var(--gy); }
.c { color: var(--c); } .r { color: var(--r); } .g { color: var(--g); } .gy { color: var(--gy); } .y { color: var(--y); }
.chip { position: absolute; font-family: "IDBold"; font-size: 32px; letter-spacing: .06em; padding: 12px 24px; border-radius: 40px; opacity: 0; white-space: nowrap; }
.ico2 { position: absolute; opacity: 0; }
/* A */
#trophy { left: 200px; top: 760px; width: 300px; height: 300px; color: var(--y); }
#shield { left: 580px; top: 740px; width: 320px; height: 340px; color: var(--c); }
#plus { position: absolute; left: 505px; top: 850px; font-size: 90px; color: var(--gy); opacity: 0; }
/* B log */
#log { position: absolute; left: 90px; top: 640px; width: 900px; height: 520px; border-radius: 22px; background: #0B0F18; border: 2px solid rgba(255,79,58,.5); opacity: 0; padding: 26px 32px;
  font-family: Consolas, "Courier New", monospace; font-size: 32px; line-height: 1.55; color: #FFC2B8; overflow: hidden; }
#log .tb { font-family: "IDBold"; font-size: 22px; letter-spacing: .16em; color: rgba(255,194,184,.6); margin-bottom: 8px; }
#log div.l { opacity: 0; white-space: pre; } #log b { color: var(--r); font-weight: normal; }
#skull { left: 780px; top: 1100px; width: 200px; height: 200px; color: var(--r); }
/* C video card */
#vcard { position: absolute; border-radius: 30px; background: #0B0F18; border: 8px solid var(--cr); opacity: 0; box-shadow: 0 40px 90px rgba(0,0,0,.6); }
#vlab { position: absolute; font-family: "IDBold"; font-size: 22px; letter-spacing: .16em; color: var(--gy); opacity: 0; }
/* D agentic */
#ring { position: absolute; left: 190px; top: 560px; width: 700px; height: 700px; opacity: 0; }
#ring svg { width: 100%; height: 100%; }
#bot { position: absolute; left: 430px; top: 800px; width: 220px; height: 220px; color: var(--c); opacity: 0; }
.st { position: absolute; width: 270px; margin-left: -135px; text-align: center; font-family: "IDBold"; font-size: 34px; padding: 14px 0; border-radius: 20px; background: #0F1830; border: 3px solid var(--c); opacity: 0; }
#clk { position: absolute; left: 0; width: 1080px; top: 1300px; text-align: center; opacity: 0; }
#clk span { display: inline-block; white-space: nowrap; font-size: 50px; color: var(--k); background: var(--c); padding: 8px 34px; border-radius: 22px; }
.atk { position: absolute; width: 60px; height: 14px; border-radius: 7px; background: var(--r); opacity: 0; }
#prod { position: absolute; left: 0; width: 1080px; top: 1430px; text-align: center; font-family: "IDBold"; font-size: 22px; letter-spacing: .14em; color: var(--gy); opacity: 0; }
/* E besar vs kecil */
.side { position: absolute; top: 640px; width: 430px; height: 600px; border-radius: 30px; padding: 34px; opacity: 0; text-align: center; }
.side .ic { width: 190px; height: 190px; margin: 30px auto 20px; }
.side h3 { font-size: 46px; line-height: 1.05; } .side p { font-family: "IDBold"; font-size: 30px; margin-top: 14px; }
#sB { left: 90px; background: #0F1830; border: 3px solid var(--c); } #sB .ic { color: var(--c); } #sB p { color: var(--c); }
#sK { left: 560px; background: #1A0F14; border: 3px dashed var(--r); } #sK .ic { color: var(--cr); } #sK p { color: var(--r); }
#qm { position: absolute; left: 830px; top: 690px; font-size: 120px; color: var(--r); opacity: 0; }
/* F threats */
.th { position: absolute; left: 90px; width: 900px; height: 200px; border-radius: 26px; background: #170C10; border: 3px solid rgba(255,79,58,.7); display: flex; align-items: center; gap: 30px; padding: 0 34px; opacity: 0; }
.th .ti { width: 120px; height: 120px; flex: none; border-radius: 28px; background: var(--r); color: var(--cr); padding: 24px; }
.th h4 { font-size: 50px; line-height: 1.05; } .th p { font-family: "IDBold"; font-size: 26px; letter-spacing: .1em; color: #FFB4A8; margin-top: 8px; }
#nyata { position: absolute; left: 0; width: 1080px; top: 1300px; text-align: center; opacity: 0; }
#nyata span { display: inline-block; font-size: 60px; color: var(--cr); background: var(--r); padding: 10px 34px; border-radius: 18px; transform: rotate(-3deg); }
/* G checklist */
.ck { position: absolute; left: 90px; width: 900px; height: 170px; border-radius: 26px; background: #0F1830; border: 3px solid rgba(34,211,238,.35); display: flex; align-items: center; gap: 28px; padding: 0 30px; opacity: 0; }
.ck .bx { width: 100px; height: 100px; flex: none; border-radius: 24px; border: 5px solid var(--c); color: var(--k); display: flex; align-items: center; justify-content: center; }
.ck .bx i { width: 100%; height: 100%; border-radius: 18px; background: var(--g); display: flex; align-items: center; justify-content: center; font-style: normal; font-size: 64px; transform: scale(0); }
.ck h4 { font-size: 46px; line-height: 1.05; } .ck p { font-family: "IDBold"; font-size: 26px; color: var(--gy); margin-top: 6px; letter-spacing: .06em; }
/* H CTA */
.opt { position: absolute; top: 470px; width: 420px; height: 130px; border-radius: 24px; display: flex; align-items: center; gap: 16px; padding: 0 24px; font-size: 40px; line-height: 1.05; opacity: 0; }
.opt .ol { width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 38px; flex: none; }
#oA { left: 100px; background: var(--g); color: var(--k); } #oA .ol { background: var(--k); color: var(--g); }
#oB { left: 560px; background: var(--r); color: var(--cr); } #oB .ol { background: var(--cr); color: var(--r); }
#follow { position: absolute; left: 300px; top: 470px; width: 480px; height: 110px; border-radius: 55px; background: var(--cr); color: var(--k); font-size: 46px; display: flex; align-items: center; justify-content: center; opacity: 0; }
#tapc { position: absolute; left: 690px; top: 520px; width: 70px; height: 70px; color: var(--k); opacity: 0; }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-size: 36px; color: var(--cr); z-index: 6; }
#brand b { color: var(--c); font-weight: normal; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; pointer-events: none; }
'''


def TX(tid, text, top, px, cls="", maxw=860):
    return f'<div class="t {cls}" id="{tid}" style="top:{top}px;font-size:{fitpx(text, px, maxw)}px">{chars(text)}</div>'


TROPHY = svg('<path d="M30 14h40v20a20 20 0 0 1-40 0z"/><path d="M30 20H16a12 12 0 0 0 14 16M70 20h14a12 12 0 0 1-14 16M50 54v16M34 86h32M40 70h20v16H40z"/>', 6)
SHIELD = svg('<path d="M50 8l34 12v26c0 22-14 38-34 46C30 84 16 68 16 46V20z"/><path d="M36 50l10 10 20-22"/>', 6)
SKULL = svg('<path d="M50 12c-20 0-34 13-34 31 0 11 5 19 13 24v13h42V67c8-5 13-13 13-24 0-18-14-31-34-31z"/><circle cx="37" cy="45" r="7"/><circle cx="63" cy="45" r="7"/><path d="M44 80v-8M56 80v-8"/>', 6)
BOT = svg('<rect x="18" y="30" width="64" height="48" rx="12"/><path d="M50 30V16"/><circle cx="50" cy="13" r="4"/><circle cx="38" cy="52" r="5"/><circle cx="62" cy="52" r="5"/><path d="M40 66h20"/>', 6)
BLDG = svg('<rect x="22" y="14" width="56" height="76" rx="4"/><path d="M34 28h8M58 28h8M34 42h8M58 42h8M34 56h8M58 56h8M44 90V74h12v16"/>', 5)
SHOP = svg('<path d="M14 36l8-20h56l8 20"/><path d="M14 36c0 6 6 10 12 10s12-4 12-10c0 6 6 10 12 10s12-4 12-10c0 6 6 10 12 10s12-4 12-10"/><path d="M20 46v40h60V46M42 86V64h16v22"/>', 5)
CHAT = svg('<path d="M50 12a36 36 0 0 0-31 54l-5 18 18-5a36 36 0 1 0 18-67z"/><path d="M38 38l24 24M62 38L38 62"/>', 6)
DB = svg('<ellipse cx="50" cy="22" rx="32" ry="11"/><path d="M18 22v56c0 6 14 11 32 11s32-5 32-11V22M18 50c0 6 14 11 32 11s32-5 32-11"/>', 6)
WEB = svg('<rect x="10" y="16" width="80" height="68" rx="8"/><path d="M10 32h80"/><circle cx="20" cy="24" r="2"/><path d="M34 52l10 10 18-20"/><path d="M60 48l14 14M74 48L60 62"/>', 5)
TAP = svg('<path d="M24 14l52 30-22 6 14 26-10 5-14-26-16 16z"/>', 5)

# siklus agentic: 3 stasiun di lingkaran r=290 (pusat 540,910)
STN = [("DETEKSI", 540, 610), ("ANALISIS", 800, 1060), ("TINDAK", 280, 1060)]
ring = ('<div id="ring"><svg viewBox="0 0 700 700" fill="none"><circle cx="350" cy="350" r="290" stroke="rgba(34,211,238,.25)" stroke-width="6"/>'
        '<circle id="rarc" cx="350" cy="350" r="290" stroke="#22D3EE" stroke-width="10" stroke-linecap="round" transform="rotate(-90 350 350)"/></svg></div>')
LOG = [("09:41:02", "login gagal ×58", "admin"), ("09:41:05", "brute-force", "IP 185.xx"), ("09:41:09", "phishing link", "wa.me/…"),
       ("09:41:12", "malware upload", "/wp-admin"), ("09:41:15", "inject: slot-gacor", "index.php"), ("09:41:18", "data dump", "customers.csv")]

body = f'''
  <div id="bg"></div><div id="glow"></div><div id="grid"></div><div id="scan"></div>
  <div id="cam">
    <div id="hud"><i></i>KEAMANAN SIBER &middot; AI</div>
    <!-- A hook -->
    {TX("a1", "JUARA 1 KOMPETISI AI", 360, 100)}
    {TX("a2", "SE-ASEAN", 480, 110, "y")}
    <div class="ico2" id="trophy">{TROPHY}</div><div id="plus">=</div><div class="ico2" id="shield">{SHIELD}</div>
    {TX("a3", "STARTUP KEAMANAN SIBER?", 1180, 84, "c")}
    <!-- B ancaman -->
    {TX("b1", "ANCAMAN HACKER", 340, 104)}
    {TX("b2", "MAKIN GILA", 460, 120, "r")}
    <div id="log"><div class="tb">LOG SERANGAN · ILUSTRASI</div>
      {"".join(f'<div class="l" id="lg{i}">{t}  <b>{a}</b>  {x}</div>' for i, (t, a, x) in enumerate(LOG))}</div>
    <div class="ico2" id="skull">{SKULL}</div>
    <!-- C kemenangan + rekaman acara -->
    <div id="vlab" style="left:{VC["left"]}px;top:{VC["top"] - 40}px">REKAMAN ACARA · 4–5 NOV 2026</div>
    <div id="vcard" style="left:{VC["left"]}px;top:{VC["top"]}px;width:{VC["w"]}px;height:{VC["h"]}px"></div>
    <div class="chip" id="cp1" style="left:90px;top:1345px;background:var(--cr);color:var(--k)">🇮🇩 PERIS.AI · JUARA 1</div>
    <div class="chip" id="cp2" style="left:610px;top:1345px;background:var(--y);color:var(--k)">$20.000</div>
    <div class="chip" id="cp3" style="left:90px;top:1425px;background:var(--c);color:var(--k)">vs 23 STARTUP</div>
    <div class="chip" id="cp4" style="left:430px;top:1425px;background:#1C2A4A;color:var(--cr)">12 NEGARA</div>
    <!-- D agentic AI -->
    {TX("d1", "AGENTIC AI", 340, 120, "c")}
    {TX("d2", "AI YANG KERJA SENDIRI", 470, 64)}
    {ring}<div id="bot">{BOT}</div>
    {"".join(f'<div class="st" id="st{i}" style="left:{x}px;top:{y - 36}px">{n}</div>' for i, (n, x, y) in enumerate(STN))}
    {"".join(f'<div class="atk" id="ak{i}" style="left:{-80}px;top:{760 + i * 140}px"></div>' for i in range(3))}
    <div id="clk"><span>24/7 · TANPA NUNGGU MANUSIA</span></div>
    <div id="prod">PRODUK: BRAHMAFUSION · MENURUT PERIS.AI</div>
    <!-- E besar vs kecil -->
    {TX("e1", "PELAJARANNYA BUAT KITA", 340, 86)}
    <div class="side" id="sB"><div class="ic">{BLDG}</div><h3>Perusahaan<br>besar</h3><p>pakai AI penjaga 🛡️</p></div>
    <div class="side" id="sK"><div class="ic">{SHOP}</div><h3>Bisnis<br>kecil</h3><p>pengamanan: nol?</p></div>
    <div id="qm">?</div>
    <!-- F ancaman UMKM -->
    {TX("f1", "NYATA DI UMKM", 340, 104, "r")}
    <div class="th" id="th0" style="top:520px"><div class="ti">{CHAT}</div><div><h4>WhatsApp bisnis dibajak</h4><p>KODE OTP DICURI</p></div></div>
    <div class="th" id="th1" style="top:750px"><div class="ti">{DB}</div><div><h4>Data pelanggan bocor</h4><p>NAMA · NO HP · ALAMAT</p></div></div>
    <div class="th" id="th2" style="top:980px"><div class="ti">{WEB}</div><div><h4>Website disusupi judol</h4><p>HALAMAN DISISIPI IKLAN JUDI</p></div></div>
    <div id="nyata"><span>SERING KEJADIAN!</span></div>
    <!-- G checklist -->
    {TX("g1", "MULAI DARI YANG DASAR", 340, 90, "c")}
    <div class="ck" id="ck0" style="top:560px"><div class="bx"><i id="cx0">✓</i></div><div><h4>Verifikasi 2 langkah</h4><p>WA · EMAIL · MARKETPLACE</p></div></div>
    <div class="ck" id="ck1" style="top:770px"><div class="bx"><i id="cx1">✓</i></div><div><h4>Password beda-beda</h4><p>PAKAI PASSWORD MANAGER</p></div></div>
    <div class="ck" id="ck2" style="top:980px"><div class="bx"><i id="cx2">✓</i></div><div><h4>Jangan asal klik link</h4><p>CEK PENGIRIM &amp; ALAMATNYA</p></div></div>
    <!-- H CTA -->
    {TX("h1", "BISNIS KAMU UDAH AMAN?", 330, 80)}
    <div class="opt" id="oA"><div class="ol">A</div>Udah aman</div>
    <div class="opt" id="oB"><div class="ol">B</div>Belum 😅</div>
    {TX("h2", "TIPS KEAMANAN BERIKUTNYA", 330, 72, "c")}
    <div id="follow">+ Follow</div><div id="tapc">{TAP}</div>
    {chibi_html(left=305, top=640, w=470)}
  </div>
  <div id="flash"></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

t_cta = T[119] - 0.1
track, emph_t = chibi_track(HERE, t_cta, DUR, [(T[119], "mikir"), (T[124], "netral"), (T[126], "tunjuk"),
                                               (T[127] + 0.4, "lambai"), (T[130], "netral"), (T[132] + 0.3, "keren")],
                            blinks=(T[122], T[129]))

W = {k: round(T[i] - 0.08, 3) for k, i in dict(B=11, C=17, D=35, E=57, F=80, G=100, H=119).items()}
js = f'''
    var T = {{}}; {"; ".join(f"T[{i}]={t}" for i, t in T.items())};
    var W = {W};
    function out(sel, t) {{ tl.to(sel, {{ opacity: 0, y: -40, duration: 0.2, ease: "power2.in" }}, q(t - 0.2)); }}
    tl.set("#hud", {{ opacity: 1 }}, 0);
    tl.fromTo("#scan", {{ y: 0 }}, {{ y: 1920, duration: 4, ease: "none", repeat: {int(DUR / 4)} }}, 0);

    // A · hook PULSE
    tl.fromTo("#a1", {{ opacity: 1, scale: 1.4 }}, {{ scale: 1, duration: 0.4, ease: "power4.out" }}, 0); sweep("#a1", 0.0, 0.3);
    sweep("#a2", T[5], 0.25);
    tl.fromTo("#trophy", {{ opacity: 0, scale: 0.4, rotation: -20 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }}, q(0.3));
    tl.fromTo("#plus", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, q(T[8]));
    tl.fromTo("#shield", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, q(T[8]));
    sweep("#a3", T[9], 0.35); kick(T[9] + 0.2, -12);
    out("#a1, #a2, #trophy, #plus, #shield, #a3", W.B);

    // B · EMBER/TERMINAL log serangan
    tl.fromTo("#glow", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, q(W.B));
    sweep("#b1", W.B, 0.3); sweep("#b2", T[15], 0.25); flash(T[15] + 0.1, "#flash", 0.2); kick(T[15] + 0.1, 14);
    fade("#log", W.B + 0.1, 0.3, {{ y: 80 }});
    [0, 1, 2, 3, 4, 5].forEach(function (i) {{ tl.fromTo("#lg" + i, {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.12 }}, q(W.B + 0.3 + i * 0.3)); }});
    tl.fromTo("#skull", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, q(T[16]));
    tl.to("#log", {{ x: 8, duration: 0.05, yoyo: true, repeat: 7 }}, q(T[16]));
    out("#b1, #b2, #log, #skull", W.C); tl.to("#glow", {{ opacity: 0, duration: 0.3 }}, q(W.C));

    // C · kartu rekaman acara (video ditempel compose.py) + chip
    tl.fromTo("#vcard", {{ opacity: 0, y: 120, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "power3.out" }}, q(W.C));
    tl.fromTo("#vlab", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(W.C + 0.2));
    pop("#cp1", T[19], 0.3); pop("#cp2", T[22], 0.3);
    pop("#cp3", T[30], 0.3); pop("#cp4", T[33], 0.3);
    out("#vcard, #vlab, .chip", W.D);

    // D · SIGNAL siklus agentic
    sweep("#d1", W.D, 0.3); sweep("#d2", T[40], 0.35);
    tl.fromTo("#ring", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }}, q(W.D + 0.1));
    pop("#bot", W.D + 0.3, 0.35);
    var C = 2 * Math.PI * 290;
    tl.set("#rarc", {{ strokeDasharray: C, strokeDashoffset: C }}, 0);
    tl.to("#rarc", {{ strokeDashoffset: 0, duration: 2.2, ease: "none", repeat: 2 }}, q(T[44]));
    [[0, T[49]], [1, T[50]], [2, T[53]]].forEach(function (e) {{ pop("#st" + e[0], e[1], 0.3); }});
    [0, 1, 2].forEach(function (i) {{
      tl.fromTo("#ak" + i, {{ opacity: 1, x: 0 }}, {{ x: 330, duration: 0.45, ease: "power2.in" }}, q(T[49] + i * 0.35));
      tl.to("#ak" + i, {{ opacity: 0, scale: 2.4, duration: 0.15 }}, q(T[49] + i * 0.35 + 0.45)); }});
    tl.fromTo("#clk", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, q(T[47]));
    tl.fromTo("#prod", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(T[36]));
    tl.to("#bot", {{ scale: 1.15, duration: 0.15, yoyo: true, repeat: 1 }}, q(T[53]));
    out("#d1, #d2, #ring, #bot, .st, #clk, #prod", W.E);

    // E · besar vs kecil
    sweep("#e1", W.E, 0.35);
    fade("#sB", T[62], 0.35, {{ x: -80 }}); fade("#sK", T[72], 0.35, {{ x: 80 }});
    pop("#qm", T[77], 0.3); tl.to("#sK", {{ x: 8, duration: 0.05, yoyo: true, repeat: 7 }}, q(T[79]));
    out("#e1, #sB, #sK, #qm", W.F);

    // F · EMBER 3 ancaman
    tl.fromTo("#glow", {{ opacity: 0 }}, {{ opacity: 0.9, duration: 0.4 }}, q(W.F));
    sweep("#f1", W.F, 0.3);
    [[0, T[80]], [1, T[84]], [2, T[87]]].forEach(function (e) {{
      tl.fromTo("#th" + e[0], {{ opacity: 0, x: 140 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "back.out(1.6)" }}, q(e[1])); kick(e[1] + 0.1, 10); }});
    tl.fromTo("#nyata", {{ opacity: 0, scale: 2 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }}, q(T[95]));
    flash(T[95] + 0.2, "#flash", 0.2);
    out("#f1, .th, #nyata", W.G); tl.to("#glow", {{ opacity: 0, duration: 0.3 }}, q(W.G));

    // G · GUIDE checklist
    sweep("#g1", W.G, 0.35);
    [[0, T[105]], [1, T[109]], [2, T[114]]].forEach(function (e) {{
      fade("#ck" + e[0], e[1] - 0.15, 0.3, {{ y: 60 }});
      tl.to("#cx" + e[0], {{ scale: 1, duration: 0.3, ease: "back.out(3)" }}, q(e[1] + 0.5)); }});
    out("#g1, .ck", W.H);

    // H · CTA A/B + follow (chibi)
    sweep("#h1", W.H, 0.35);
    pop("#oA", T[123], 0.3); pop("#oB", T[125], 0.3);
    out("#h1, #oA, #oB", T[126] - 0.05);
    pop("#follow", T[126], 0.3); sweep("#h2", T[129], 0.35);
    tl.fromTo("#tapc", {{ opacity: 0, x: 120, y: 120 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.35, ease: "power3.out" }}, q(T[126] + 0.1));
    tl.to("#follow", {{ backgroundColor: "#22D3EE", color: "#070B14", scale: 0.94, duration: 0.12 }}, q(T[127] + 0.1));
    tl.to("#follow", {{ scale: 1, duration: 0.2, ease: "back.out(3)" }}, q(T[127] + 0.22));
    tl.set("#follow", {{ textContent: "Following ✓" }}, q(T[127] + 0.1));
    tl.to("#tapc", {{ opacity: 0, duration: 0.2 }}, q(T[128] + 0.4));
'''
js += chibi_js(track, emph_t, t_cta)

(HERE / "public" / "index.html").write_text(page("peris-ai", DUR, css, body, js), encoding="utf-8")
(HERE / "vcard.txt").write_text(f'{VC["left"] + VC["b"]} {VC["top"] + VC["b"]} {VC["w"] - 2 * VC["b"]} {VC["h"] - 2 * VC["b"]} {W["C"] + 0.35:.3f} {W["D"] - 0.25:.3f}\n')
print("ok", DUR, open(HERE / "vcard.txt").read())
