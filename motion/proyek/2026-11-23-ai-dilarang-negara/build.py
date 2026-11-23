# Reel · "Kenapa negara melarang AI buatannya sendiri?" (kontrol ekspor Claude Fable 5 & Mythos 5, Juni 2026) · 9:16
# VO manual Endrich (58,5 dtk), timing dari align.py, sumber riset.md.
# Gaya dasar gelap + aksen kuning "dokumen rahasia" + per beat:
#   hook PULSE (larangan) · 2 model PAPER (kartu) · timeline + direktif PAPER/PULSE · offline global TERMINAL/EMBER (status + peta titik)
#   ketakutan TERMINAL (kode + celah) · AI = chip SIGNAL · dicabut PAPER (stempel hijau) · ajakan EMBER/PULSE (Indonesia)
#   melek AI SIGNAL (3 kartu orang) · CTA AVATAR (chibi + A/B)
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
import reel_common  # noqa: E402

reel_common.TAIL = 1.4
from reel_common import chars, chibi_html, chibi_js, chibi_track, fitpx, page, setup, svg, words  # noqa: E402

SLUG = HERE.name
DUR = setup(HERE, SLUG)
T = words(SLUG)

css = '''
:root { --k:#0C0C0E; --cr:#F4F1EA; --y:#F5B301; --r:#FF4F3A; --g:#22C55E; --c:#38BDF8; --gy:#8A8F9C; --id:#E5252A; }
html, body, #root { background: var(--k); color: var(--cr); font-family: "IDBlack"; }
#bg { position: absolute; inset: 0; background: radial-gradient(120% 70% at 50% 40%, #19181C 0%, var(--k) 70%); }
#glow { position: absolute; inset: 0; background: radial-gradient(70% 45% at 50% 55%, rgba(255,79,58,.32), rgba(255,79,58,0) 70%); opacity: 0; }
#grid { position: absolute; inset: 0; opacity: .06; background-image: linear-gradient(var(--cr) 1px, transparent 1px), linear-gradient(90deg, var(--cr) 1px, transparent 1px); background-size: 90px 90px; }
#cam { position: absolute; inset: 0; }
#hud { position: absolute; left: 60px; top: 262px; display: flex; align-items: center; gap: 12px; font-family: "IDBold"; font-size: 24px; letter-spacing: .18em; opacity: 0; z-index: 5; }
#hud i { width: 12px; height: 12px; border-radius: 2px; background: var(--y); display: inline-block; }
.t { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; line-height: 1; letter-spacing: -.02em; }
.t .ch { opacity: 0; }
.sub { position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDBold"; font-size: 28px; letter-spacing: .16em; opacity: 0; color: var(--gy); }
.y { color: var(--y); } .r { color: var(--r); } .g { color: var(--g); } .gy { color: var(--gy); } .id { color: var(--id); }
.chip { position: absolute; font-family: "IDBold"; font-size: 32px; letter-spacing: .06em; padding: 12px 26px; border-radius: 40px; opacity: 0; white-space: nowrap; }
.ico2 { position: absolute; opacity: 0; }
/* A */
#ban { left: 340px; top: 700px; width: 400px; height: 400px; }
#ban .chipi { position: absolute; inset: 70px; color: var(--cr); }
#ban .no { position: absolute; inset: 0; color: var(--r); }
/* B model cards */
.mc { position: absolute; top: 640px; width: 430px; height: 520px; border-radius: 30px; background: #F2EDE2; color: #141414; padding: 36px; opacity: 0; box-shadow: 0 40px 80px rgba(0,0,0,.5); }
.mc s { display: block; text-decoration: none; font-family: "IDBold"; font-size: 24px; letter-spacing: .16em; color: #8a5a00; }
.mc h3 { font-size: 76px; white-space: nowrap; line-height: .95; margin-top: 20px; letter-spacing: -.03em; }
.mc p { font-family: "IDSemi"; font-size: 30px; color: #555; margin-top: 22px; line-height: 1.25; }
#mcF { left: 90px; } #mcM { left: 560px; }
/* C timeline + direktif */
#tline { position: absolute; left: 120px; top: 500px; width: 840px; height: 120px; opacity: 0; }
#tline .ln { position: absolute; left: 0; top: 30px; width: 840px; height: 8px; border-radius: 4px; background: rgba(244,241,234,.18); }
#tline .fl { position: absolute; left: 0; top: 30px; width: 840px; height: 8px; border-radius: 4px; background: var(--y); transform-origin: 0 50%; transform: scaleX(0); }
.td { position: absolute; top: 14px; width: 40px; height: 40px; margin-left: -20px; border-radius: 50%; background: var(--k); border: 8px solid var(--y); opacity: 0; }
.tt { position: absolute; top: 70px; width: 240px; margin-left: -120px; font-family: "IDBold"; font-size: 26px; line-height: 1.2; opacity: 0; }
.tt b { display: block; font-family: "IDBlack"; font-size: 34px; font-weight: normal; color: var(--y); }
#doc { position: absolute; left: 110px; top: 680px; width: 860px; height: 560px; background: #F2EDE2; color: #141414; border-radius: 10px; padding: 40px 46px; opacity: 0; box-shadow: 0 40px 90px rgba(0,0,0,.55); }
#doc .dh { font-family: "IDBold"; font-size: 24px; letter-spacing: .16em; color: #666; border-bottom: 4px solid #141414; padding-bottom: 14px; }
#doc h3 { font-size: 66px; margin-top: 22px; letter-spacing: -.02em; }
#doc .ln2 { height: 16px; background: #d6cfbf; border-radius: 8px; margin: 18px 0; }
#doc .rw { font-family: "IDSemi"; font-size: 32px; margin-top: 16px; display: flex; gap: 16px; align-items: center; opacity: 0; }
#doc .rw i { font-style: normal; width: 46px; height: 46px; border-radius: 10px; background: var(--r); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 30px; }
#stp { position: absolute; left: 560px; top: 1080px; opacity: 0; }
#stp span { display: inline-block; font-size: 46px; color: var(--r); border: 7px solid var(--r); padding: 6px 22px; border-radius: 12px; transform: rotate(-10deg); background: rgba(242,237,226,.9); }
/* D status + peta */
#stat { position: absolute; left: 90px; top: 520px; width: 900px; height: 330px; border-radius: 22px; background: #101114; border: 2px solid rgba(244,241,234,.14); padding: 26px 32px; opacity: 0;
  font-family: Consolas, "Courier New", monospace; font-size: 38px; }
#stat .tb { font-family: "IDBold"; font-size: 22px; letter-spacing: .16em; color: var(--gy); margin-bottom: 18px; }
#stat .sr { display: flex; justify-content: space-between; margin: 22px 0; white-space: nowrap; }
#stat .sr b { font-weight: normal; }
#map { position: absolute; left: 90px; top: 900px; width: 900px; height: 420px; opacity: 0; }
.md { position: absolute; width: 14px; height: 14px; border-radius: 50%; background: var(--c); }
/* E kode */
#code { position: absolute; left: 90px; top: 520px; width: 900px; height: 640px; border-radius: 22px; background: #0F1114; border: 2px solid rgba(244,241,234,.14); padding: 28px 32px; opacity: 0;
  font-family: Consolas, "Courier New", monospace; font-size: 32px; line-height: 1.6; color: #C9D1D9; white-space: pre; overflow: hidden; }
#code .k { color: var(--c); } #code .s { color: #A5D6A7; }
#bugl { position: absolute; left: 100px; top: 0; width: 880px; height: 56px; border-radius: 10px; background: rgba(255,79,58,.22); border: 4px solid var(--r); opacity: 0; }
#lens { position: absolute; left: 160px; top: 640px; width: 200px; height: 200px; color: var(--y); opacity: 0; }
/* F chip = AI */
#eqA { left: 120px; top: 640px; width: 340px; height: 340px; color: var(--y); }
#eqB { left: 620px; top: 640px; width: 340px; height: 340px; color: var(--c); }
#eq { position: absolute; left: 0; width: 1080px; top: 740px; text-align: center; font-size: 140px; color: var(--cr); opacity: 0; }
.eql { position: absolute; top: 1000px; width: 340px; text-align: center; font-family: "IDBold"; font-size: 34px; letter-spacing: .1em; opacity: 0; }
/* G dicabut */
#stp2 { position: absolute; left: 0; width: 1080px; top: 760px; text-align: center; opacity: 0; }
#stp2 span { display: inline-block; font-size: 120px; color: var(--g); border: 10px solid var(--g); padding: 6px 40px 14px; border-radius: 20px; transform: rotate(-6deg); }
#shd { left: 410px; top: 1000px; width: 260px; height: 260px; color: var(--g); }
/* H */
#idbar { position: absolute; left: 0; top: 1040px; width: 1080px; height: 180px; opacity: 0; }
#idbar i { display: block; height: 90px; } #idbar i:first-child { background: var(--id); } #idbar i:last-child { background: #F4F1EA; }
#cart { left: 420px; top: 700px; width: 240px; height: 240px; color: var(--cr); }
#cartx { position: absolute; left: 400px; top: 810px; width: 280px; height: 14px; border-radius: 7px; background: var(--r); transform: rotate(-30deg) scaleX(0); opacity: 0; }
/* I */
.pp { position: absolute; top: 600px; width: 280px; height: 380px; border-radius: 30px; background: #16161A; border: 3px solid rgba(244,241,234,.16); text-align: center; padding-top: 40px; opacity: 0; }
.pp .pi { width: 150px; height: 150px; margin: 0 auto; color: var(--y); }
.pp h4 { font-size: 38px; margin-top: 30px; line-height: 1.05; }
#melek { position: absolute; left: 0; width: 1080px; top: 1060px; text-align: center; opacity: 0; }
#melek span { display: inline-block; font-size: 110px; color: var(--k); background: var(--y); padding: 6px 40px 14px; border-radius: 26px; }
#trend { position: absolute; left: 0; width: 1080px; top: 640px; text-align: center; opacity: 0; }
#trend span { position: relative; display: inline-block; font-size: 90px; color: var(--gy); }
#trend i { position: absolute; left: -4%; top: 46%; width: 108%; height: 14px; border-radius: 7px; background: var(--r); transform-origin: 0 50%; transform: scaleX(0); }
.spd { position: absolute; height: 6px; border-radius: 3px; background: linear-gradient(90deg, transparent, rgba(245,179,1,.8)); opacity: 0; }
/* J */
.opt { position: absolute; top: 470px; width: 420px; height: 130px; border-radius: 24px; display: flex; align-items: center; gap: 16px; padding: 0 24px; font-size: 36px; line-height: 1.05; opacity: 0; }
.opt .ol { width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 38px; flex: none; }
#oA { left: 100px; background: var(--g); color: var(--k); } #oA .ol { background: var(--k); color: var(--g); }
#oB { left: 560px; background: var(--y); color: var(--k); } #oB .ol { background: var(--k); color: var(--y); }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-size: 36px; color: var(--cr); z-index: 6; }
#brand b { color: var(--y); font-weight: normal; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; pointer-events: none; }
'''


def TX(tid, text, top, px, cls="", maxw=860):
    return f'<div class="t {cls}" id="{tid}" style="top:{top}px;font-size:{fitpx(text, px, maxw)}px">{chars(text)}</div>'


CHIP = svg('<rect x="22" y="22" width="56" height="56" rx="8"/><rect x="36" y="36" width="28" height="28" rx="4"/>'
           '<path d="M34 10v12M50 10v12M66 10v12M34 78v12M50 78v12M66 78v12M10 34h12M10 50h12M10 66h12M78 34h12M78 50h12M78 66h12"/>', 5)
NO = svg('<circle cx="50" cy="50" r="42"/><path d="M20 20l60 60"/>', 7)
BRAIN = svg('<path d="M40 16a12 12 0 0 0-12 12 12 12 0 0 0-8 20 12 12 0 0 0 6 20 12 12 0 0 0 14 14V16zM60 16a12 12 0 0 1 12 12 12 12 0 0 1 8 20 12 12 0 0 1-6 20 12 12 0 0 1-14 14V16z"/><path d="M40 40h-8M60 40h8M40 62h-8M60 62h8"/>', 5)
LENS = svg('<circle cx="42" cy="42" r="26"/><path d="M62 62l24 24"/>', 8)
SHIELD = svg('<path d="M50 8l34 12v26c0 22-14 38-34 46C30 84 16 68 16 46V20z"/><path d="M36 50l10 10 20-22"/>', 6)
CART = svg('<path d="M10 16h12l10 46h44l10-32H28"/><circle cx="38" cy="78" r="6"/><circle cx="70" cy="78" r="6"/>', 6)
CAP = svg('<path d="M8 40l42-18 42 18-42 18z"/><path d="M26 48v18c0 6 12 12 24 12s24-6 24-12V48M88 42v22"/>', 5)
BAG = svg('<rect x="12" y="30" width="76" height="52" rx="8"/><path d="M36 30v-8a6 6 0 0 1 6-6h16a6 6 0 0 1 6 6v8M12 52h76"/>', 5)
SHOP = svg('<path d="M14 36l8-20h56l8 20"/><path d="M14 36c0 6 6 10 12 10s12-4 12-10c0 6 6 10 12 10s12-4 12-10c0 6 6 10 12 10s12-4 12-10"/><path d="M20 46v40h60V46M42 86V64h16v22"/>', 5)

# timeline Juni: 9 rilis, 12 kontrol, 30 dicabut (x di 840 px untuk 1-30 Juni)
def tx(d):
    return round((d - 1) / 29 * 840)


TL = [(9, "9 JUN", "Fable 5 rilis"), (12, "12 JUN", "kontrol ekspor"), (30, "30 JUN", "dicabut")]
# peta titik (ilustrasi dunia, bukan geografi akurat)
import random  # noqa: E402
random.seed(7)
DOTS = [(random.randint(0, 880), random.randint(0, 400)) for _ in range(120)]
CODE = ('<span class="k">def</span> handle(req):\n    buf = alloc(<span class="s">256</span>)\n    copy(buf, req.body)   <span class="s"># ?</span>\n'
        '    <span class="k">if</span> auth(req.user):\n        <span class="k">return</span> render(buf)\n    log(req.headers)\n    <span class="k">return</span> deny()\n')

body = f'''
  <div id="bg"></div><div id="glow"></div><div id="grid"></div>
  <div id="cam">
    <div id="hud"><i></i>KEBIJAKAN AI &middot; AS</div>
    <!-- A hook -->
    {TX("a1", "NEGARA MELARANG", 360, 110)}
    {TX("a2", "AI BUATANNYA SENDIRI?", 490, 90, "y")}
    <div class="ico2" id="ban"><div class="chipi">{CHIP}</div><div class="no">{NO}</div></div>
    <!-- B dua model -->
    {TX("b1", "INI YANG TERJADI PADA", 400, 70, "gy")}
    <div class="mc" id="mcF"><s>CLAUDE</s><h3>Fable 5</h3><p>model publik<br>paling canggih</p></div>
    <div class="mc" id="mcM"><s>CLAUDE</s><h3>Mythos 5</h3><p>versi terbatas<br>untuk mitra</p></div>
    <!-- C timeline + direktif -->
    {TX("c1", "JUNI 2026", 330, 120, "y")}
    <div id="tline"><div class="ln"></div><div class="fl" id="tfl"></div>
      {"".join(f'<div class="td" id="td{i}" style="left:{tx(d)}px"></div><div class="tt" id="tt{i}" style="left:{tx(d) + (-110 if i == 0 else 110 if i == 1 else 0)}px;text-align:{"right" if i == 0 else "left" if i == 1 else "center"}"><b>{a}</b>{b}</div>' for i, (d, a, b) in enumerate(TL))}</div>
    <div id="doc"><div class="dh">DEPARTEMEN PERDAGANGAN AS · DIREKTIF</div><h3>Kontrol Ekspor</h3><div class="ln2"></div><div class="ln2" style="width:70%"></div>
      <div class="rw" id="rw1"><i>✕</i>Warga asing dilarang mengakses</div>
      <div class="rw" id="rw2"><i>✕</i>Berlaku di dalam &amp; luar AS</div></div>
    <div id="stp"><span>BERLAKU</span></div>
    <!-- D offline -->
    {TX("d1", "MATI TOTAL", 330, 130, "r")}
    <div id="stat"><div class="tb">STATUS MODEL · ILUSTRASI</div>
      <div class="sr">claude-fable-5 <b id="s1" class="g">● ONLINE</b></div>
      <div class="sr">claude-mythos-5 <b id="s2" class="g">● ONLINE</b></div></div>
    <div id="map">{"".join(f'<div class="md" style="left:{x}px;top:{y}px"></div>' for x, y in DOTS)}</div>
    {TX("d2", "SEMUA PENGGUNA DI DUNIA", 1360, 64)}
    <!-- E ketakutan -->
    {TX("e1", "KETAKUTANNYA:", 330, 100, "y")}
    <div id="code">{CODE}<div id="bugl" style="top:{28 + 2 * 51}px"></div></div>
    <div class="ico2" id="lens">{LENS}</div>
    {TX("e2", "CARI CELAH KEAMANAN", 1220, 80, "r")}
    {TX("e3", "PERANGKAT LUNAK", 1320, 64)}
    <!-- F AI = chip -->
    {TX("f1", "MODEL AI", 330, 120)}
    {TX("f2", "SESTRATEGIS CHIP", 460, 100, "y")}
    <div class="ico2" id="eqA">{CHIP}</div><div id="eq">=</div><div class="ico2" id="eqB">{BRAIN}</div>
    <div class="eql" id="eql1" style="left:120px;color:var(--y)">CHIP</div><div class="eql" id="eql2" style="left:620px;color:var(--c)">MODEL AI</div>
    {TX("f3", "ANALISIS", 1150, 26, "gy")}
    <!-- G dicabut -->
    {TX("g1", "AKHIR JUNI", 330, 120)}
    <div id="stp2"><span>DICABUT</span></div>
    <div class="ico2" id="shd">{SHIELD}</div>
    {TX("g2", "PENGAMANAN DIPERKETAT", 1300, 72, "g")}
    <div class="chip" id="g3" style="left:330px;top:1400px;background:#26262C;color:var(--cr)">±3 MINGGU OFFLINE</div>
    <!-- H -->
    {TX("h1", "TAPI COBA PIKIR…", 330, 110)}
    {TX("h2", "NEGARA MAJU SESERIUS ITU", 700, 80, "y")}
    {TX("h3", "KITA MASIH SANTAI?", 880, 110, "r")}
    <div class="ico2" id="cart">{CART}</div><div id="cartx"></div>
    <div id="idbar"><i></i><i></i></div>
    {TX("h4", "BUKAN CUMA JADI PASAR", 1290, 80)}
    <!-- I -->
    {"".join(f'<div class="pp" id="pp{i}" style="left:{70 + i * 335}px"><div class="pi">{ic}</div><h4>{n}</h4></div>' for i, (n, ic) in enumerate([("Pelajar", CAP), ("Pekerja", BAG), ("Pelaku<br>usaha", SHOP)]))}
    {TX("i1", "SEMUA PERLU", 360, 100)}
    <div id="melek"><span>MELEK AI</span></div>
    <div id="trend"><span>IKUT-IKUTAN TREN<i id="trx"></i></span></div>
    {TX("i2", "BIAR NGGAK TERTINGGAL", 860, 86, "y")}
    {"".join(f'<div class="spd" id="sp{i}" style="left:{60 + (i * 137) % 600}px;top:{1040 + i * 50}px;width:{300 + (i * 71) % 260}px"></div>' for i, _ in enumerate(range(7)))}
    <!-- J CTA -->
    {TX("j1", "KAMU YANG MANA?", 330, 100)}
    <div class="opt" id="oA"><div class="ol">A</div>Sudah mulai belajar</div>
    <div class="opt" id="oB"><div class="ol">B</div>Masih menunggu</div>
    {chibi_html(left=305, top=640, w=470)}
  </div>
  <div id="flash"></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

t_cta = T[128] - 0.1
track, emph_t = chibi_track(HERE, t_cta, DUR, [(T[128], "mikir"), (T[130], "tunjuk"), (T[133] + 0.2, "netral"),
                                               (T[134], "mikir"), (T[136] + 0.5, "kedip"), (T[136] + 1.0, "keren")],
                            blinks=(T[132],))

W = {k: round(T[i] - 0.08, 3) for k, i in dict(B=9, C=20, D=40, E=54, F=66, G=75, H=85, I=106, J=128).items()}
js = f'''
    var T = {{}}; {"; ".join(f"T[{i}]={t}" for i, t in T.items())};
    var W = {W};
    function out(sel, t) {{ tl.to(sel, {{ opacity: 0, y: -40, duration: 0.2, ease: "power2.in" }}, q(t - 0.2)); }}
    tl.set("#hud", {{ opacity: 1 }}, 0);

    // A · hook
    tl.fromTo("#a1", {{ opacity: 1, scale: 1.4 }}, {{ scale: 1, duration: 0.4, ease: "power4.out" }}, 0); sweep("#a1", 0.0, 0.3);
    sweep("#a2", T[5], 0.35);
    tl.fromTo("#ban", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, q(0.4));
    tl.fromTo("#ban .no", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }}, q(T[4]));
    flash(T[4] + 0.15, "#flash", 0.25); kick(T[4] + 0.15, -14);
    out("#a1, #a2, #ban", W.B);

    // B · dua model (PAPER)
    sweep("#b1", W.B, 0.35);
    tl.fromTo("#mcF", {{ opacity: 0, y: 160, rotation: -6 }}, {{ opacity: 1, y: 0, rotation: -3, duration: 0.4, ease: "back.out(1.6)" }}, q(T[14] - 0.1));
    tl.fromTo("#mcM", {{ opacity: 0, y: 160, rotation: 6 }}, {{ opacity: 1, y: 0, rotation: 3, duration: 0.4, ease: "back.out(1.6)" }}, q(T[18] - 0.1));
    out("#b1, .mc", W.C);

    // C · timeline + direktif
    sweep("#c1", W.C, 0.3);
    tl.fromTo("#tline", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, q(T[22]));
    tl.to("#tfl", {{ scaleX: {tx(12) / 840:.3f}, duration: 1.4, ease: "power2.inOut" }}, q(T[22]));
    pop("#td0", T[25], 0.25); fade("#tt0", T[25], 0.25);
    pop("#td1", T[28], 0.25); fade("#tt1", T[28], 0.25);
    tl.fromTo("#doc", {{ opacity: 0, y: 160, rotation: 3 }}, {{ opacity: 1, y: 0, rotation: -1, duration: 0.45, ease: "power3.out" }}, q(T[28]));
    tl.fromTo("#stp", {{ opacity: 0, scale: 2.2 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }}, q(T[32]));
    kick(T[32] + 0.2, 12);
    fade("#rw1", T[34], 0.25); fade("#rw2", T[38], 0.25);
    out("#c1, #tline, #doc, #stp", W.D);

    // D · offline global (TERMINAL/EMBER)
    tl.fromTo("#glow", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, q(T[47]));
    fade("#stat", W.D, 0.3, {{ y: 60 }});
    tl.fromTo("#map", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(W.D + 0.3));
    tl.set("#s1", {{ textContent: "● OFFLINE", color: "#FF4F3A" }}, q(T[47])); tl.set("#s2", {{ textContent: "● OFFLINE", color: "#FF4F3A" }}, q(T[47] + 0.25));
    sweep("#d1", T[47], 0.3); kick(T[47], -14);
    tl.to(".md", {{ backgroundColor: "#3A1A1A", scale: 0.6, duration: 0.15, stagger: {{ each: 0.012, from: "random" }} }}, q(T[49]));
    sweep("#d2", T[50], 0.4);
    out("#d1, #stat, #map, #d2", W.E); tl.to("#glow", {{ opacity: 0, duration: 0.3 }}, q(W.E));

    // E · ketakutan: celah keamanan
    sweep("#e1", W.E, 0.3);
    fade("#code", T[55], 0.35, {{ y: 60 }});
    tl.fromTo("#lens", {{ opacity: 0, x: 0, y: 0 }}, {{ opacity: 1, duration: 0.2 }}, q(T[60]));
    tl.to("#lens", {{ x: 420, y: 40, duration: 1.0, ease: "power1.inOut" }}, q(T[60]));
    tl.fromTo("#bugl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1, repeat: 3, yoyo: true }}, q(T[62]));
    tl.set("#bugl", {{ opacity: 1 }}, q(T[62] + 0.45));
    sweep("#e2", T[62], 0.35); sweep("#e3", T[64], 0.3);
    out("#e1, #code, #lens, #e2, #e3", W.F);

    // F · AI = chip (SIGNAL)
    sweep("#f1", W.F + 0.1, 0.3);
    tl.fromTo("#eqA", {{ opacity: 0, x: -100 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.6)" }}, q(T[69]));
    tl.fromTo("#eqB", {{ opacity: 0, x: 100 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.6)" }}, q(T[69] + 0.15));
    fade("#eql1", T[69] + 0.2, 0.25); fade("#eql2", T[69] + 0.3, 0.25);
    pop("#eq", T[71], 0.3); sweep("#f2", T[72], 0.35); kick(T[74], 12);
    tl.fromTo("#f3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(T[72]));
    out("#f1, #f2, #eqA, #eqB, #eq, .eql, #f3", W.G);

    // G · dicabut
    sweep("#g1", W.G, 0.3);
    tl.fromTo("#stp2", {{ opacity: 0, scale: 2.4 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }}, q(T[79]));
    flash(T[79] + 0.2, "#flash", 0.2); kick(T[79] + 0.2, -12);
    pop("#shd", T[83], 0.35); sweep("#g2", T[83], 0.35);
    pop("#g3", T[84] + 0.3, 0.3);
    out("#g1, #stp2, #shd, #g2, #g3", W.H);

    // H · ajakan
    sweep("#h1", W.H, 0.35); out("#h1", T[88]);
    sweep("#h2", T[88], 0.35); sweep("#h3", T[96], 0.3); kick(T[98], 12);
    out("#h2, #h3", T[100]);
    tl.fromTo("#cart", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, q(T[100]));
    tl.fromTo("#idbar", {{ opacity: 0, scaleX: 0 }}, {{ opacity: 1, scaleX: 1, duration: 0.5, ease: "power3.out" }}, q(T[100]));
    tl.set("#cartx", {{ opacity: 1 }}, q(T[103]));
    tl.to("#cartx", {{ scaleX: 1, duration: 0.25, ease: "power3.out" }}, q(T[103]));
    sweep("#h4", T[103], 0.35);
    out("#cart, #cartx, #idbar, #h4", W.I);

    // I · melek AI
    sweep("#i1", T[110], 0.3);
    [[0, T[106]], [1, T[107]], [2, T[108]]].forEach(function (e) {{
      tl.fromTo("#pp" + e[0], {{ opacity: 0, y: 120 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.8)" }}, q(e[1])); }});
    tl.fromTo("#melek", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)" }}, q(T[112]));
    flash(T[112] + 0.2, "#flash", 0.15);
    out("#i1, .pp, #melek", T[114]);
    fade("#trend", T[114], 0.25); tl.to("#trx", {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, q(T[117]));
    sweep("#i2", T[119], 0.35);
    [0, 1, 2, 3, 4, 5, 6].forEach(function (i) {{ tl.fromTo("#sp" + i, {{ opacity: 0, x: 300 }}, {{ opacity: 1, x: -300, duration: 0.5, ease: "none", repeat: 1 }}, q(T[122] + i * 0.06)); }});
    out("#trend, #i2, .spd", W.J);

    // J · CTA A/B (chibi)
    sweep("#j1", W.J, 0.35);
    pop("#oA", T[131], 0.3); pop("#oB", T[134], 0.3);
'''
js += chibi_js(track, emph_t, t_cta)

(HERE / "public" / "index.html").write_text(page("ai-dilarang-negara", DUR, css, body, js), encoding="utf-8")
print("ok", DUR)
