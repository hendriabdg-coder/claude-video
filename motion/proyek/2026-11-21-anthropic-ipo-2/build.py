# Reel · "Anthropic IPO: apa artinya buat kita?" (part 2) · 9:16 · VO manual Endrich (57,6 dtk), timing dari align.py, sumber riset.md.
# Gaya dasar sama dengan part 1 (gelap, krem, aksen oranye) + per beat:
#   hook SIGNAL (chat) · bursa AS TERMINAL (pita ticker) · Anthropic PAPER (kartu profil + stempel) · angka rekor PULSE
#   "3 hal" PULSE (kartu nomor) · 01 SIGNAL (jaringan global) · 02 PULSE (balapan fitur) · 03 PAPER/EMBER (dokumen IPO + meter limit)
#   jangan bergantung SIGNAL (tombol vs roda gigi) · penutup AVATAR (chibi + follow)
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

css = '''
:root { --k:#0B0B0D; --cr:#F4F1EA; --o:#FF6A3D; --g:#22C55E; --r:#FF4F3A; --b:#3A5BFF; --gy:#8A8F9C; }
html, body, #root { background: var(--k); color: var(--cr); font-family: "IDBlack"; }
#bg { position: absolute; inset: 0; background: radial-gradient(120% 70% at 50% 40%, #17171B 0%, var(--k) 70%); }
#glow { position: absolute; inset: 0; background: radial-gradient(70% 45% at 50% 55%, rgba(255,79,58,.3), rgba(255,79,58,0) 70%); opacity: 0; }
#grid { position: absolute; inset: 0; opacity: .07; background-image: linear-gradient(var(--cr) 1px, transparent 1px), linear-gradient(90deg, var(--cr) 1px, transparent 1px); background-size: 90px 90px; }
#cam { position: absolute; inset: 0; }
#hud { position: absolute; left: 60px; top: 262px; display: flex; align-items: center; gap: 12px; font-family: "IDBold"; font-size: 24px; letter-spacing: .18em; opacity: 0; z-index: 5; }
#hud i { width: 12px; height: 12px; border-radius: 50%; background: var(--r); display: inline-block; }
.t { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; line-height: 1; letter-spacing: -.02em; }
.t .ch { opacity: 0; }
.sub { position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDBold"; font-size: 32px; letter-spacing: .16em; opacity: 0; color: var(--gy); }
.o { color: var(--o); } .g { color: var(--g); } .r { color: var(--r); } .gy { color: var(--gy); }
.chip { position: absolute; font-family: "IDBold"; font-size: 30px; letter-spacing: .1em; padding: 10px 22px; border-radius: 40px; opacity: 0; white-space: nowrap; }
.sim { position: absolute; font-family: "IDBold"; font-size: 20px; letter-spacing: .16em; color: var(--gy); border: 2px solid rgba(138,143,156,.5); border-radius: 8px; padding: 4px 12px; opacity: 0; }
/* A chat */
#chat { position: absolute; left: 110px; top: 820px; width: 860px; height: 420px; border-radius: 30px; background: #16161A; border: 2px solid rgba(244,241,234,.12); opacity: 0; padding: 30px; }
#chat .cb { font-family: "IDBold"; font-size: 24px; letter-spacing: .14em; color: var(--gy); }
.bub { position: absolute; max-width: 640px; padding: 24px 30px; font-family: "IDSemi"; font-size: 38px; line-height: 1.25; border-radius: 28px; opacity: 0; }
#bu { right: 30px; top: 90px; background: var(--b); color: var(--cr); border-bottom-right-radius: 8px; }
#ba { left: 30px; top: 230px; background: var(--cr); color: #141414; border-bottom-left-radius: 8px; }
#ba b { display: block; font-family: "IDBold"; font-size: 22px; letter-spacing: .14em; color: #c4471d; margin-bottom: 6px; }
/* B ticker */
#tape { position: absolute; left: 0; top: 1060px; width: 1080px; height: 120px; background: #0F1411; border-top: 3px solid var(--g); border-bottom: 3px solid var(--g); overflow: hidden; opacity: 0; }
#tapeI { position: absolute; left: 0; top: 26px; white-space: nowrap; font-family: Consolas, "Courier New", monospace; font-size: 56px; color: var(--g); }
#bldg { position: absolute; left: 340px; top: 560px; width: 400px; height: 400px; color: var(--cr); opacity: 0; }
/* C profile card */
#card { position: absolute; left: 90px; top: 520px; width: 900px; height: 640px; background: #F2EDE2; color: #141414; border-radius: 18px; opacity: 0; padding: 46px 50px;
  box-shadow: 0 40px 90px rgba(0,0,0,.55); }
#card .k1 { font-family: "IDBold"; font-size: 26px; letter-spacing: .16em; color: #8a2b16; }
#card .nm { font-size: 118px; letter-spacing: -.03em; margin-top: 14px; }
#card .ds { font-family: "IDSemi"; font-size: 44px; color: #444; margin-top: 4px; }
#card .rw { display: flex; gap: 18px; margin-top: 50px; }
#card .rw div { flex: 1; border: 3px solid #141414; border-radius: 16px; padding: 18px 20px; opacity: 0; }
#card .rw s { display: block; text-decoration: none; font-family: "IDBold"; font-size: 22px; letter-spacing: .14em; color: #777; }
#card .rw u { display: block; text-decoration: none; font-size: 54px; margin-top: 8px; }
/* D numbers */
#lab { position: absolute; left: 0; width: 1080px; top: 560px; text-align: center; font-family: "IDBold"; font-size: 38px; letter-spacing: .16em; color: var(--gy); opacity: 0; }
#big { position: absolute; left: 0; width: 1080px; top: 630px; text-align: center; font-size: 170px; line-height: 1; letter-spacing: -.04em; font-variant-numeric: tabular-nums; opacity: 0; }
#trophy { position: absolute; left: 340px; top: 700px; width: 400px; height: 400px; color: var(--o); opacity: 0; }
.stat { position: absolute; left: 90px; width: 900px; height: 150px; border-radius: 24px; background: #16161A; border: 2px solid rgba(244,241,234,.12); display: flex; align-items: center; justify-content: space-between; padding: 0 36px; opacity: 0; }
.stat s { text-decoration: none; font-family: "IDBold"; font-size: 34px; color: var(--gy); }
.stat u { text-decoration: none; font-size: 72px; font-variant-numeric: tabular-nums; }
#arr { position: absolute; left: 690px; top: 1200px; width: 170px; height: 170px; color: var(--g); opacity: 0; }
/* E three */
.n3 { position: absolute; top: 780px; width: 260px; height: 320px; border-radius: 30px; background: #16161A; border: 3px solid rgba(244,241,234,.18); display: flex; align-items: center; justify-content: center; font-size: 200px; opacity: 0; }
/* F */
.num { position: absolute; left: 90px; top: 330px; font-size: 130px; line-height: 1; color: transparent; -webkit-text-stroke: 4px var(--o); opacity: 0; }
#globe { position: absolute; left: 290px; top: 640px; width: 500px; height: 500px; color: var(--o); opacity: 0; }
#tren { position: absolute; left: 0; width: 1080px; top: 1220px; text-align: center; opacity: 0; }
#tren span { display: inline-block; font-size: 64px; padding: 8px 26px; border-radius: 16px; }
#tren .a { color: var(--gy); position: relative; } #tren .a i { position: absolute; left: -6%; top: 48%; width: 112%; height: 10px; background: var(--r); border-radius: 5px; transform-origin: 0 50%; }
#tren .b { color: var(--k); background: var(--o); margin-left: 22px; opacity: 0; }
.lane { position: absolute; left: 90px; width: 900px; height: 130px; opacity: 0; }
.lane .tr { position: absolute; left: 0; top: 80px; width: 900px; height: 14px; border-radius: 7px; background: rgba(244,241,234,.12); }
.lane .cr { position: absolute; left: 0; top: 10px; width: 150px; height: 64px; border-radius: 18px; display: flex; align-items: center; justify-content: center; font-family: "IDBold"; font-size: 28px; color: var(--k); }
#flag { position: absolute; left: 960px; top: 620px; width: 12px; height: 480px; background: repeating-linear-gradient(var(--cr) 0 24px, var(--k) 24px 48px); opacity: 0; }
#doc { position: absolute; left: 110px; top: 540px; width: 860px; height: 620px; background: #F2EDE2; color: #141414; border-radius: 10px; opacity: 0; padding: 40px 46px; box-shadow: 0 40px 90px rgba(0,0,0,.55); }
#doc .dt { font-family: "IDBold"; font-size: 24px; letter-spacing: .16em; color: #777; border-bottom: 3px solid #141414; padding-bottom: 14px; }
#doc .ln { height: 16px; background: #d6cfbf; border-radius: 8px; margin: 20px 0; }
#doc .q { position: relative; font-family: "IDSemi"; font-size: 40px; line-height: 1.3; margin: 26px 0; padding: 6px 10px; }
#doc .q i { position: absolute; inset: 0; background: rgba(255,106,61,.35); border-radius: 8px; transform-origin: 0 50%; transform: scaleX(0); }
#doc .q span { position: relative; }
#meter { position: absolute; left: 140px; top: 1230px; width: 800px; height: 60px; border-radius: 30px; background: rgba(244,241,234,.12); overflow: hidden; opacity: 0; }
#mf { width: 100%; height: 100%; background: linear-gradient(90deg, var(--g), var(--o), var(--r)); transform-origin: 0 50%; }
#mlab { position: absolute; left: 140px; top: 1310px; width: 800px; display: flex; justify-content: space-between; font-family: "IDBold"; font-size: 26px; letter-spacing: .12em; color: var(--gy); opacity: 0; }
/* G */
#eggs { position: absolute; left: 0; width: 1080px; top: 560px; height: 420px; opacity: 0; }
.tool { position: absolute; top: 120px; width: 220px; height: 150px; border-radius: 26px; display: flex; align-items: center; justify-content: center; font-family: "IDBold"; font-size: 34px; color: var(--k); }
#btn { position: absolute; left: 140px; top: 1050px; width: 340px; height: 130px; border-radius: 65px; background: var(--cr); color: var(--k); display: flex; align-items: center; justify-content: center; font-size: 46px; opacity: 0; }
#gear { position: absolute; left: 620px; top: 990px; width: 260px; height: 260px; color: var(--o); opacity: 0; }
#vs { position: absolute; left: 500px; top: 1085px; font-size: 50px; color: var(--gy); opacity: 0; }
/* H/I */
#follow { position: absolute; left: 300px; top: 470px; width: 480px; height: 110px; border-radius: 55px; background: var(--cr); color: var(--k); font-size: 46px; display: flex; align-items: center; justify-content: center; opacity: 0; }
#tapc { position: absolute; left: 690px; top: 520px; width: 70px; height: 70px; color: var(--k); opacity: 0; }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-size: 36px; color: var(--cr); z-index: 6; }
#brand b { color: var(--o); font-weight: normal; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; pointer-events: none; }
'''


def TX(tid, text, top, px, cls="", maxw=860):
    return f'<div class="t {cls}" id="{tid}" style="top:{top}px;font-size:{fitpx(text, px, maxw)}px">{chars(text)}</div>'


BLDG = svg('<path d="M10 34L50 12l40 22z"/><path d="M14 38h72M20 44v34M35 44v34M50 44v34M65 44v34M80 44v34M12 84h76M8 90h84"/>', 5)
TROPHY = svg('<path d="M30 14h40v20a20 20 0 0 1-40 0z"/><path d="M30 20H16a12 12 0 0 0 14 16M70 20h14a12 12 0 0 1-14 16M50 54v16M34 86h32M40 70h20v16H40z"/>', 6)
ARROW = svg('<path d="M20 80L80 20M40 20h40v40"/>', 10)
GLOBE = ('<svg class="ico" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.5">'
         '<circle cx="50" cy="50" r="40"/><ellipse cx="50" cy="50" rx="18" ry="40"/><path d="M10 50h80M16 30h68M16 70h68"/>'
         + "".join(f'<circle class="nd" cx="{x}" cy="{y}" r="3.5" fill="currentColor"/>' for x, y in [(26, 34), (70, 28), (62, 62), (34, 70), (50, 46), (82, 52)])
         + '<path class="lk" d="M26 34L50 46L70 28M50 46L62 62L82 52M50 46L34 70" stroke-width="2"/></svg>')
GEAR = svg('<circle cx="50" cy="50" r="14"/><path d="M50 10v14M50 76v14M10 50h14M76 50h14M22 22l10 10M68 68l10 10M22 78l10-10M68 32l10-10"/>'
           '<circle cx="50" cy="50" r="28"/>', 6)
TAP = svg('<path d="M24 14l52 30-22 6 14 26-10 5-14-26-16 16z"/>', 5)

tape = "   ".join(["ANT ▲ NASDAQ", "IPO 19·11·2026", "ANT ▲ +34% HARI-1", "$81 M · REKOR"] * 3)
LANES = [("AI A", "var(--b)"), ("AI B", "var(--g)"), ("AI C", "var(--o)")]
TOOLS = [("Tool A", "#5B6CFF", 180), ("Tool B", "#22C55E", 430), ("Tool C", "#FF6A3D", 680)]

body = f'''
  <div id="bg"></div><div id="glow"></div><div id="grid"></div>
  <div id="cam">
    <div id="hud"><i></i>BERITA AI &middot; IPO #2</div>
    <!-- A hook -->
    {TX("a1", "KAMU PAKAI CLAUDE", 480, 120)}
    {TX("a2", "BUAT KERJA?", 620, 120, "o")}
    <div id="chat"><div class="cb">CHAT AI</div>
      <div class="bub" id="bu">Bikinin draf laporan mingguan</div>
      <div class="bub" id="ba"><b>CLAUDE</b>Siap, ini drafnya…</div></div>
    <div class="sim" id="simA" style="left:110px;top:1255px">SIMULASI</div>
    <!-- B bursa -->
    {TX("b1", "AI ANDALAN KAMU", 340, 96)}
    <div id="bldg">{BLDG}</div>
    {TX("b2", "RESMI MASUK BURSA", 1240, 86)}
    {TX("b3", "SAHAM AMERIKA", 1345, 86, "g")}
    <div id="tape"><div id="tapeI">{tape}</div></div>
    <!-- C profil -->
    <div id="card"><div class="k1">PROFIL PERUSAHAAN</div><div class="nm">Anthropic</div><div class="ds">pembuat Claude</div>
      <div class="rw"><div id="cr1"><s>BURSA</s><u>Nasdaq</u></div><div id="cr2"><s>TANGGAL</s><u>19 Nov</u></div><div id="cr3"><s>KODE</s><u style="color:#c4471d">ANT</u></div></div></div>
    <!-- D rekor -->
    {TX("d1", "BUKAN IPO BIASA", 340, 110)}
    {TX("d2", "IPO TERBESAR", 340, 120, "o")}
    {TX("d3", "SEPANJANG SEJARAH", 480, 72)}
    <div id="trophy">{TROPHY}</div>
    <div class="stat" id="s1" style="top:640px"><s>Dana masuk</s><u id="v1">$0 M</u></div>
    <div class="stat" id="s2" style="top:820px"><s>Valuasi ±</s><u id="v2" class="o">$0 T</u></div>
    <div class="stat" id="s3" style="top:1000px"><s>Hari pertama</s><u id="v3" class="g">+0%</u></div>
    <div class="sub" id="dil" style="top:1180px;font-size:22px">VALUASI FULLY DILUTED · HARGA IPO $83</div>
    <!-- E 3 hal -->
    {TX("e1", "APA ARTINYA BUAT KITA?", 340, 84)}
    {TX("e2", "YANG BUKAN INVESTOR", 450, 60, "gy")}
    {"".join(f'<div class="n3" id="n{i}" style="left:{90 + i * 320}px;{"color:var(--o)" if i == 1 else ""}">{i + 1}</div>' for i in range(3))}
    {TX("e3", "3 HAL", 1200, 110, "o")}
    <!-- F1 -->
    <div class="num" id="f1n">01</div>
    {TX("f1", "INDUSTRI RAKSASA", 480, 104)}
    <div id="globe">{GLOBE}</div>
    <div id="tren"><span class="a">TREN<i id="trx"></i></span><span class="b" id="trb">INDUSTRI</span></div>
    {TX("f1b", "DIPERCAYA PASAR GLOBAL", 1350, 56, "gy")}
    <!-- F2 -->
    <div class="num" id="f2n">02</div>
    {TX("f2", "PERSAINGAN MAKIN KETAT", 480, 90)}
    {"".join(f'<div class="lane" id="ln{i}" style="top:{640 + i * 160}px"><div class="tr"></div><div class="cr" id="lc{i}" style="background:{c}">{n}</div></div>' for i, (n, c) in enumerate(LANES))}
    <div id="flag"></div>
    {TX("f2b", "FITUR AI MAKIN CEPAT", 1200, 84, "o")}
    <div class="sub" id="f2c" style="top:1310px;font-size:22px">ILUSTRASI · BUKAN DATA</div>
    <!-- F3 -->
    <div class="num" id="f3n">03</div>
    <div id="doc"><div class="dt">DOKUMEN IPO (S-1) · ANTHROPIC</div><div class="ln"></div><div class="ln" style="width:80%"></div>
      <div class="q"><i id="qh"></i><span>“…batas pemakaian, rate limit, dan kemampuan model atau produk dapat berubah…”</span></div>
      <div class="ln" style="width:90%"></div><div class="ln" style="width:60%"></div>
      <div class="sub" style="position:static;opacity:1;text-align:left;font-size:18px;color:#777">PARAFRASE · SUMBER: S-1/A ANTHROPIC, SEC</div></div>
    <div id="meter"><div id="mf"></div></div>
    <div id="mlab"><span>LIMIT HARI INI</span><span>BISA BERUBAH</span></div>
    <!-- G -->
    {TX("g1", "JANGAN BERGANTUNG", 340, 100)}
    {TX("g2", "KE SATU TOOL", 460, 100, "o")}
    <div id="eggs">{"".join(f'<div class="tool" id="tl{i}" style="left:{x}px;background:{c}">{n}</div>' for i, (n, c, x) in enumerate(TOOLS))}</div>
    {TX("g3", "PELAJARI CARA KERJANYA", 900, 72)}
    <div id="btn">Tombol</div><div id="vs">vs</div><div id="gear">{GEAR}</div>
    <!-- H/I -->
    {TX("h1", "YANG PAHAM AI SEKARANG", 330, 78)}
    {TX("h2", "PALING SIAP", 430, 96, "o")}
    {TX("i1", "BIAR NGGAK KETINGGALAN", 330, 72, "o")}
    <div id="follow">+ Follow</div><div id="tapc">{TAP}</div>
    {chibi_html(left=305, top=640, w=470)}
  </div>
  <div id="flash"></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

t_cta = T[122] - 0.1
track, emph_t = chibi_track(HERE, t_cta, DUR, [(T[122], "netral"), (T[127], "keren"), (T[131], "netral"),
                                               (T[136] - 0.1, "tunjuk"), (T[138], "lambai"), (T[141], "netral")],
                            blinks=(T[125], T[134]))

W = {k: round(T[i] - 0.08, 3) for k, i in dict(B=5, C=20, D=32, E=60, F1=71, F2=84, F3=95, G=109, H=122, I=136).items()}
js = f'''
    var T = {{}}; {"; ".join(f"T[{i}]={t}" for i, t in T.items())};
    var W = {W};
    function out(sel, t) {{ tl.to(sel, {{ opacity: 0, y: -40, duration: 0.2, ease: "power2.in" }}, q(t - 0.2)); }}
    function money(sel, t, d, a, b, fmt) {{ count(sel, t, d, a, b, fmt); }}
    tl.set("#hud", {{ opacity: 1 }}, 0);

    // A · hook SIGNAL
    tl.fromTo("#a1", {{ opacity: 1, scale: 1.4 }}, {{ scale: 1, duration: 0.4, ease: "power4.out" }}, 0); sweep("#a1", 0.0, 0.3);
    sweep("#a2", T[3], 0.25); kick(T[3], -12);
    fade("#chat", 0.2, 0.35, {{ y: 140 }}); tl.set("#simA", {{ opacity: 1 }}, 0.3);
    pop("#bu", 0.45, 0.25); pop("#ba", T[3] + 0.1, 0.25);
    out("#a1, #a2, #chat, #simA", W.B);

    // B · TERMINAL bursa AS
    sweep("#b1", W.B, 0.35);
    tl.fromTo("#bldg", {{ opacity: 0, y: 80, scale: 0.8 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }}, q(T[13]));
    tl.fromTo("#tape", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, q(T[15]));
    tl.fromTo("#tapeI", {{ x: 0 }}, {{ x: -1800, duration: W.C - T[15], ease: "none" }}, q(T[15]));
    sweep("#b2", T[15], 0.35); sweep("#b3", T[17], 0.3);
    out("#b1, #bldg, #tape, #b2, #b3", W.C);

    // C · PAPER profil + stempel
    tl.fromTo("#card", {{ opacity: 0, y: 160, rotation: 3 }}, {{ opacity: 1, y: 0, rotation: -1, duration: 0.45, ease: "power3.out" }}, q(W.C));
    [["#cr1", T[25]], ["#cr2", T[27]], ["#cr3", T[31] - 0.1]].forEach(function (e) {{
      tl.fromTo(e[0], {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }}, q(e[1])); }});
    kick(T[31], 10);
    out("#card", W.D);

    // D · PULSE angka rekor
    sweep("#d1", W.D, 0.35);
    out("#d1", T[37]);
    sweep("#d2", T[37], 0.3); sweep("#d3", T[39], 0.35);
    tl.fromTo("#trophy", {{ opacity: 0, scale: 0.4, rotation: -20 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }}, q(T[39]));
    flash(T[39] + 0.1, "#flash", 0.25);
    out("#trophy, #d3", T[42]);
    fade("#s1", T[42], 0.3); money("#v1", T[45], 0.7, 0, 81, function (v) {{ return "$" + Math.round(v) + " M"; }});
    fade("#s2", T[48], 0.3); money("#v2", T[50], 0.7, 0, 1.5, function (v) {{ return "$" + v.toFixed(1).replace(".", ",") + " T"; }});
    tl.fromTo("#dil", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(T[51]));
    fade("#s3", T[53], 0.3); money("#v3", T[58], 0.6, 0, 34, function (v) {{ return "+" + Math.round(v) + "%"; }});
    tl.fromTo("#arr", {{ opacity: 0, x: -60, y: 60 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.35, ease: "back.out(2)" }}, q(T[58]));
    kick(T[59], -12);
    out("#d2, .stat, #dil, #arr", W.E);

    // E · 3 hal
    sweep("#e1", W.E, 0.35); sweep("#e2", T[65], 0.3);
    [0, 1, 2].forEach(function (i) {{ tl.fromTo("#n" + i, {{ opacity: 0, y: 120, rotation: (i - 1) * 8 }}, {{ opacity: 1, y: 0, rotation: (i - 1) * 4, duration: 0.35, ease: "back.out(1.8)" }}, q(T[68] + i * 0.12)); }});
    sweep("#e3", T[69], 0.25); kick(T[69], 12);
    out("#e1, #e2, .n3, #e3", W.F1);

    // F1 · industri raksasa (SIGNAL jaringan)
    tl.fromTo("#f1n", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.3 }}, q(W.F1));
    tl.fromTo("#globe", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, q(W.F1 + 0.1));
    tl.fromTo("#globe svg", {{ rotation: -10 }}, {{ rotation: 10, duration: 4.5, ease: "none" }}, q(W.F1));
    tl.fromTo("#globe .lk", {{ strokeDasharray: 300, strokeDashoffset: 300 }}, {{ strokeDashoffset: 0, duration: 1.5, ease: "power2.out" }}, q(T[82]));
    tl.fromTo("#globe .nd", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.25, stagger: 0.12, ease: "back.out(3)" }}, q(T[81]));
    tl.fromTo("#tren", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, q(T[75] - 0.1));
    tl.fromTo("#trx", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.25, ease: "power3.out" }}, q(T[76]));
    pop("#trb", T[78], 0.3);
    sweep("#f1", T[78], 0.3); sweep("#f1b", T[81], 0.35);
    out("#f1n, #globe, #tren, #f1, #f1b", W.F2);

    // F2 · balapan fitur (PULSE)
    tl.fromTo("#f2n", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.3 }}, q(W.F2));
    sweep("#f2", T[85], 0.35);
    tl.fromTo(".lane, #flag", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, stagger: 0.08 }}, q(T[85]));
    [[0, 560], [1, 610], [2, 590]].forEach(function (e) {{
      tl.fromTo("#lc" + e[0], {{ x: 0 }}, {{ x: e[1] + 120, duration: 2.6 + e[0] * 0.2, ease: "power2.inOut" }}, q(T[86])); }});
    sweep("#f2b", T[89], 0.35); tl.fromTo("#f2c", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(T[89]));
    out("#f2n, #f2, .lane, #flag, #f2b, #f2c", W.F3);

    // F3 · dokumen IPO + meter limit (PAPER/EMBER)
    tl.fromTo("#f3n", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.3 }}, q(W.F3));
    tl.fromTo("#doc", {{ opacity: 0, y: 160, rotation: -3 }}, {{ opacity: 1, y: 0, rotation: 1, duration: 0.45, ease: "power3.out" }}, q(T[97]));
    tl.to("#qh", {{ scaleX: 1, duration: 0.8, ease: "power2.inOut" }}, q(T[102]));
    tl.fromTo("#glow", {{ opacity: 0 }}, {{ opacity: 0.8, duration: 0.5 }}, q(T[106]));
    fade("#meter", T[102], 0.3); tl.fromTo("#mlab", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(T[102]));
    tl.fromTo("#mf", {{ scaleX: 1 }}, {{ scaleX: 0.35, duration: 0.5, ease: "power2.inOut", yoyo: true, repeat: 3 }}, q(T[107]));
    out("#f3n, #doc, #meter, #mlab", W.G); tl.to("#glow", {{ opacity: 0, duration: 0.3 }}, q(W.G));

    // G · jangan bergantung ke satu tool (SIGNAL)
    sweep("#g1", W.G, 0.35); sweep("#g2", T[113], 0.3);
    tl.fromTo("#eggs", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, q(T[110]));
    [0, 1, 2].forEach(function (i) {{ tl.fromTo("#tl" + i, {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, q(T[110] + i * 0.15)); }});
    tl.to("#tl0, #tl2", {{ opacity: 0.25, scale: 0.9, duration: 0.3 }}, q(T[114]));
    tl.to("#tl1", {{ scale: 1.15, duration: 0.3, ease: "back.out(2)" }}, q(T[114]));
    tl.to("#tl1", {{ rotation: 8, x: 20, duration: 0.08, yoyo: true, repeat: 5 }}, q(T[115] + 0.1));
    tl.to("#tl0, #tl2", {{ opacity: 1, scale: 1, duration: 0.3 }}, q(T[116]));
    tl.to("#tl1", {{ scale: 1, rotation: 0, x: 0, duration: 0.3 }}, q(T[116]));
    sweep("#g3", T[116], 0.35);
    pop("#btn", T[119], 0.3); tl.fromTo("#vs", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, q(T[119] + 0.2));
    pop("#gear", T[117], 0.3); tl.to("#gear svg", {{ rotation: 360, duration: 2.5, ease: "none" }}, q(T[117]));
    tl.to("#btn", {{ opacity: 0.3, scale: 0.9, duration: 0.3 }}, q(T[121]));
    out("#g1, #g2, #eggs, #g3, #btn, #vs, #gear", W.H);

    // H/I · penutup + follow (chibi)
    sweep("#h1", W.H, 0.35); sweep("#h2", T[128], 0.3);
    out("#h1, #h2", W.I);
    sweep("#i1", T[139], 0.35);
    pop("#follow", W.I + 0.05, 0.3);
    tl.fromTo("#tapc", {{ opacity: 0, x: 120, y: 120 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.35, ease: "power3.out" }}, q(T[136] + 0.1));
    tl.to("#follow", {{ backgroundColor: "#FF6A3D", color: "#0B0B0D", scale: 0.94, duration: 0.12 }}, q(T[137]));
    tl.to("#follow", {{ scale: 1, duration: 0.2, ease: "back.out(3)" }}, q(T[137] + 0.12));
    tl.set("#follow", {{ textContent: "Following ✓" }}, q(T[137]));
    tl.to("#tapc", {{ opacity: 0, duration: 0.2 }}, q(T[138] + 0.4));
'''
js += chibi_js(track, emph_t, t_cta)

(HERE / "public" / "index.html").write_text(page("anthropic-ipo-2", DUR, css, body, js), encoding="utf-8")
print("ok", DUR)
