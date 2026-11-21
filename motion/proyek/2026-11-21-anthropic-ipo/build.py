# Reel · "Rekor IPO Anthropic" · 9:16 · VO manual Endrich (60,8 dtk), timing kata dari align.py, sumber di riset.md.
# Gaya dasar gelap (EMBER/TERMINAL: hitam, krem, aksen oranye) + per beat:
#   hook PULSE · "bukan Elon Musk" PAPER · AI harian SIGNAL (chat, SIMULASI) · Nasdaq/ANT TERMINAL · harga & dana PULSE
#   grafik hari pertama PULSE (skematis) · rugi EMBER · taruhan investor SIGNAL (timbangan) · CTA AVATAR (chibi)
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
#glow { position: absolute; inset: 0; background: radial-gradient(70% 45% at 50% 55%, rgba(255,79,58,.35), rgba(255,79,58,0) 70%); opacity: 0; }
#grid { position: absolute; inset: 0; opacity: .07; background-image: linear-gradient(var(--cr) 1px, transparent 1px), linear-gradient(90deg, var(--cr) 1px, transparent 1px); background-size: 90px 90px; }
#cam { position: absolute; inset: 0; }
#hud { position: absolute; left: 60px; top: 262px; display: flex; align-items: center; gap: 12px; font-family: "IDBold"; font-size: 24px; letter-spacing: .18em; opacity: 0; z-index: 5; }
#hud i { width: 12px; height: 12px; border-radius: 50%; background: var(--r); display: inline-block; }
.t { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; line-height: 1; letter-spacing: -.02em; }
.t .ch { opacity: 0; }
.sub { position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDBold"; font-size: 32px; letter-spacing: .16em; opacity: 0; color: var(--gy); }
.o { color: var(--o); } .g { color: var(--g); } .r { color: var(--r); } .kk { color: var(--k); }
.rep { position: absolute; left: -60px; width: 1300px; font-size: 200px; line-height: 1; white-space: nowrap; color: transparent; -webkit-text-stroke: 3px rgba(244,241,234,.12); opacity: 0; }
.chip { position: absolute; font-family: "IDBold"; font-size: 30px; letter-spacing: .1em; padding: 10px 22px; border-radius: 40px; opacity: 0; white-space: nowrap; }
#stamp { position: absolute; left: 0; width: 1080px; top: 1060px; text-align: center; opacity: 0; }
#stamp span { display: inline-block; font-size: 150px; color: var(--cr); background: var(--r); padding: 6px 46px 18px; border-radius: 22px; transform: rotate(-6deg); }
#crack { position: absolute; left: 140px; top: 440px; width: 800px; height: 520px; color: var(--cr); opacity: 0; }
/* PAPER */
#paper { position: absolute; left: 90px; top: 430px; width: 900px; height: 820px; background: #F2EDE2; color: #141414; border-radius: 6px; opacity: 0;
  box-shadow: 0 40px 90px rgba(0,0,0,.55); padding: 44px 50px; }
#paper .mh { font-family: "IDBlack"; font-size: 60px; letter-spacing: -.02em; border-bottom: 6px double #141414; padding-bottom: 16px; display: flex; justify-content: space-between; align-items: flex-end; }
#paper .mh small { font-family: "IDBold"; font-size: 22px; letter-spacing: .12em; color: #555; }
#paper .kick { font-family: "IDBold"; font-size: 30px; letter-spacing: .14em; color: #8a2b16; margin-top: 46px; }
#paper .hd { font-family: "IDBlack"; font-size: 66px; line-height: 1.05; margin-top: 14px; }
#nm1 { position: absolute; left: 50px; top: 400px; font-size: 128px; letter-spacing: -.03em; color: #141414; white-space: nowrap; }
#strike { position: absolute; left: 40px; top: 470px; width: 760px; height: 16px; background: var(--r); border-radius: 8px; transform-origin: 0 50%; transform: scaleX(0) rotate(-3deg); }
#nm2 { position: absolute; left: 50px; top: 580px; font-size: 128px; letter-spacing: -.03em; color: #c4471d; white-space: nowrap; opacity: 0; }
#paper .ln { height: 14px; background: #d6cfbf; border-radius: 7px; margin: 14px 0; }
/* SIGNAL chat */
#chat { position: absolute; left: 110px; top: 560px; width: 860px; height: 640px; border-radius: 30px; background: #16161A; border: 2px solid rgba(244,241,234,.12); opacity: 0; padding: 30px; }
#chat .cb { font-family: "IDBold"; font-size: 24px; letter-spacing: .14em; color: var(--gy); display: flex; justify-content: space-between; }
.bub { position: absolute; max-width: 620px; padding: 24px 30px; font-family: "IDSemi"; font-size: 38px; line-height: 1.25; border-radius: 28px; opacity: 0; }
#bu { right: 30px; top: 110px; background: var(--b); color: var(--cr); border-bottom-right-radius: 8px; }
#ba { left: 30px; top: 290px; background: #F4F1EA; color: #141414; border-bottom-left-radius: 8px; }
#ba b { display: block; font-family: "IDBold"; font-size: 22px; letter-spacing: .14em; color: #c4471d; margin-bottom: 8px; }
.dots { position: absolute; left: 30px; top: 300px; display: flex; gap: 10px; opacity: 0; }
.dots i { width: 18px; height: 18px; border-radius: 50%; background: var(--gy); display: block; }
.sim { position: absolute; font-family: "IDBold"; font-size: 20px; letter-spacing: .16em; color: var(--gy); border: 2px solid rgba(138,143,156,.5); border-radius: 8px; padding: 4px 12px; opacity: 0; }
/* TERMINAL */
#date { position: absolute; left: 0; width: 1080px; top: 340px; text-align: center; opacity: 0; }
#date span { display: inline-block; font-size: 64px; padding: 14px 34px; border: 4px solid var(--cr); border-radius: 18px; letter-spacing: .02em; }
#term { position: absolute; left: 90px; top: 520px; width: 900px; height: 380px; border-radius: 22px; background: #0F1411; border: 2px solid rgba(34,197,94,.35); opacity: 0; padding: 30px 36px;
  font-family: Consolas, "Courier New", monospace; font-size: 38px; line-height: 1.45; color: #BFF5D0; }
#term .tb { font-family: "IDBold"; font-size: 22px; letter-spacing: .16em; color: rgba(191,245,208,.55); margin-bottom: 14px; }
#term div.l { opacity: 0; margin: 22px 0; white-space: pre; } #term b { color: var(--g); font-weight: normal; }
#tick { position: absolute; left: 0; width: 1080px; top: 1000px; text-align: center; font-size: 280px; line-height: 1; letter-spacing: .02em; color: var(--cr); opacity: 0; }
#tick i { display: inline-block; width: 26px; height: 230px; background: var(--g); margin-left: 18px; vertical-align: -10px; }
/* PULSE */
#lab { position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; font-family: "IDBold"; font-size: 36px; letter-spacing: .16em; color: var(--gy); opacity: 0; }
#big { position: absolute; left: 0; width: 1080px; top: 400px; text-align: center; font-size: 330px; line-height: 1; letter-spacing: -.04em; font-variant-numeric: tabular-nums; opacity: 0; }
#rng { position: absolute; left: 120px; top: 1010px; width: 840px; height: 300px; opacity: 0; }
#rng .ax { position: absolute; left: 0; top: 120px; width: 840px; height: 10px; border-radius: 5px; background: rgba(244,241,234,.2); }
#rng .bd { position: absolute; top: 96px; height: 58px; border-radius: 14px; background: rgba(244,241,234,.28); border: 3px solid rgba(244,241,234,.6); transform-origin: 50% 50%; }
#rng .tk { position: absolute; top: 190px; width: 120px; margin-left: -60px; text-align: center; font-family: "IDBold"; font-size: 32px; color: var(--gy); }
#rng .bl { position: absolute; top: 250px; font-family: "IDBold"; font-size: 28px; letter-spacing: .1em; color: var(--cr); white-space: nowrap; }
#mk { position: absolute; top: 60px; width: 10px; height: 130px; margin-left: -5px; border-radius: 5px; background: var(--o); }
#mk b { position: absolute; left: 50%; top: -58px; transform: translateX(-50%); font-family: "IDBlack"; font-size: 44px; color: var(--o); white-space: nowrap; font-weight: normal; }
#bigM { position: absolute; left: 0; width: 1080px; top: 420px; text-align: center; font-size: 150px; line-height: 1; letter-spacing: -.04em; font-variant-numeric: tabular-nums; opacity: 0; }
#rp { position: absolute; left: 0; width: 1080px; top: 640px; text-align: center; opacity: 0; }
#rp span { display: inline-block; font-size: 64px; color: var(--k); background: var(--cr); padding: 12px 34px; border-radius: 20px; }
#rpn { position: absolute; left: 0; width: 1080px; top: 760px; text-align: center; font-family: "IDBold"; font-size: 24px; letter-spacing: .1em; color: var(--gy); opacity: 0; }
.rb { position: absolute; left: 90px; width: 900px; opacity: 0; }
.rb s { display: flex; justify-content: space-between; text-decoration: none; font-family: "IDBold"; font-size: 36px; margin-bottom: 14px; color: var(--cr); }
.rb s b { font-family: "IDBlack"; font-weight: normal; }
.rb i { display: block; height: 74px; border-radius: 18px; transform-origin: 0 50%; }
/* chart */
#bell { position: absolute; left: 470px; top: 300px; width: 140px; height: 140px; color: var(--o); opacity: 0; transform-origin: 50% 10%; }
#chart { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
#chart .gl { stroke: rgba(244,241,234,.12); stroke-width: 2; }
#chart .ipo { stroke: var(--o); stroke-width: 4; stroke-dasharray: 14 12; }
#chart .ln { fill: none; stroke-width: 12; stroke-linecap: round; stroke-linejoin: round; }
#chart text { font-family: "IDBold"; font-size: 28px; fill: var(--gy); }
.dot { position: absolute; width: 38px; height: 38px; margin: -19px 0 0 -19px; border-radius: 50%; border: 8px solid var(--k); opacity: 0; }
#pz { position: absolute; left: 0; width: 1080px; top: 320px; text-align: center; font-size: 160px; line-height: 1; letter-spacing: -.03em; font-variant-numeric: tabular-nums; opacity: 0; }
#skm { position: absolute; left: 90px; top: 1290px; font-family: "IDBold"; font-size: 22px; letter-spacing: .14em; color: var(--gy); opacity: 0; }
/* EMBER */
#gpu { position: absolute; left: 340px; top: 700px; width: 400px; height: 400px; color: var(--r); opacity: 0; }
.cash { position: absolute; font-size: 70px; color: var(--o); opacity: 0; }
#loss { position: absolute; left: 90px; top: 1170px; width: 900px; padding: 26px 34px; border-radius: 22px; background: rgba(255,79,58,.12); border: 2px solid rgba(255,79,58,.6); opacity: 0;
  font-family: "IDBold"; font-size: 34px; line-height: 1.4; color: var(--cr); }
#loss b { font-family: "IDBlack"; font-weight: normal; color: var(--r); }
#loss small { display: block; font-size: 20px; letter-spacing: .1em; color: var(--gy); margin-top: 6px; }
/* SIGNAL scale */
#scale { position: absolute; left: 90px; top: 560px; width: 900px; height: 760px; opacity: 0; }
#beam { position: absolute; left: 90px; top: 150px; width: 720px; height: 16px; border-radius: 8px; background: var(--cr); transform-origin: 50% 50%; }
.pan { position: absolute; top: 158px; width: 300px; margin-left: -150px; transform-origin: 50% 0; }
.pan .rope { width: 4px; height: 160px; background: rgba(244,241,234,.6); margin: 0 auto; }
.pan .bowl { height: 30px; border-radius: 0 0 150px 150px; background: var(--cr); }
.pan .pl { margin-top: 20px; text-align: center; font-size: 40px; line-height: 1.05; }
#post { position: absolute; left: 442px; top: 158px; width: 16px; height: 520px; background: rgba(244,241,234,.45); border-radius: 8px; }
#base { position: absolute; left: 330px; top: 670px; width: 240px; height: 22px; background: rgba(244,241,234,.45); border-radius: 11px; }
.coin { position: absolute; width: 64px; height: 64px; border-radius: 50%; background: var(--o); color: var(--k); font-size: 38px; display: flex; align-items: center; justify-content: center; opacity: 0; }
/* CTA */
.opt { position: absolute; top: 470px; width: 420px; height: 130px; border-radius: 24px; display: flex; align-items: center; gap: 16px; padding: 0 24px; font-size: 38px; line-height: 1.05; opacity: 0; }
.opt .ol { width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 38px; flex: none; }
#oA { left: 100px; background: var(--b); color: var(--cr); } #oA .ol { background: var(--cr); color: var(--b); }
#oB { left: 560px; background: var(--r); color: var(--cr); } #oB .ol { background: var(--cr); color: var(--r); }
#follow { position: absolute; left: 300px; top: 470px; width: 480px; height: 110px; border-radius: 55px; background: var(--cr); color: var(--k); font-size: 46px; display: flex; align-items: center; justify-content: center; opacity: 0; }
#tapc { position: absolute; left: 690px; top: 520px; width: 70px; height: 70px; color: var(--k); opacity: 0; }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-size: 36px; color: var(--cr); z-index: 6; }
#brand b { color: var(--o); font-weight: normal; }
#flash { position: absolute; inset: 0; background: #fff; opacity: 0; pointer-events: none; }
'''


def TX(tid, text, top, px, cls="", maxw=860):
    return f'<div class="t {cls}" id="{tid}" style="top:{top}px;font-size:{fitpx(text, px, maxw)}px">{chars(text)}</div>'


def SUB(tid, text, top, color=None):
    return f'<div class="sub" id="{tid}" style="top:{top}px{";color:" + color if color else ""}">{text}</div>'


BELL = svg('<path d="M50 12a6 6 0 0 1 6 6v3a24 24 0 0 1 18 23v18l8 10H18l8-10V44a24 24 0 0 1 18-23v-3a6 6 0 0 1 6-6z"/><path d="M42 80a8 8 0 0 0 16 0"/>', 6)
GPU = svg('<rect x="22" y="22" width="56" height="56" rx="8"/><rect x="36" y="36" width="28" height="28" rx="4"/>'
          '<path d="M34 10v12M50 10v12M66 10v12M34 78v12M50 78v12M66 78v12M10 34h12M10 50h12M10 66h12M78 34h12M78 50h12M78 66h12"/>', 5)
CRACK = ('<svg class="ico" viewBox="0 0 800 520" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">'
         '<path class="ck" d="M400 0 L380 120 L430 200 L360 300 L410 400 L390 520"/>'
         '<path class="ck" d="M430 200 L560 170 L680 230 L800 210"/><path class="ck" d="M360 300 L240 330 L120 290 L0 320"/>'
         '<path class="ck" d="M410 400 L520 450 L640 430"/></svg>')
TAP = svg('<path d="M24 14l52 30-22 6 14 26-10 5-14-26-16 16z"/>', 5)

# chart geometry (skematis): harga 75..120 -> y 1240..600
X0, X1 = 150, 930


def py(p):
    return round(1240 - (p - 75) / 45 * 640, 1)


PTS = [(X0, py(83)), (250, py(111.5)), (430, py(115.1)), (560, py(106)), (700, py(101)), (X1, py(97.17))]
path1 = f"M{PTS[0][0]} {PTS[0][1]} L{PTS[1][0]} {PTS[1][1]}"
path2 = "M" + " L".join(f"{x} {y}" for x, y in PTS[1:])
chart = (f'<svg id="chart" viewBox="0 0 1080 1920">'
         + "".join(f'<line class="gl" x1="{X0}" x2="{X1}" y1="{py(p)}" y2="{py(p)}"/><text x="{X1 + 12}" y="{py(p) + 10}">${p}</text>' for p in (80, 90, 100, 110, 120))
         + f'<line class="ipo" x1="{X0}" x2="{X1}" y1="{py(83)}" y2="{py(83)}"/><text x="{X0}" y="{py(83) + 46}" style="fill:var(--o)">HARGA IPO $83</text>'
         + f'<path id="p1" class="ln" d="{path1}" stroke="var(--g)"/><path id="p2" class="ln" d="{path2}" stroke="var(--cr)"/></svg>')

body = f'''
  <div id="bg"></div><div id="glow"></div><div id="grid"></div>
  <div id="cam">
    <div id="hud"><i></i>BERITA AI &middot; IPO</div>
    <!-- A hook -->
    <div class="rep" id="rA1" style="top:300px">REKOR REKOR REKOR REKOR</div>
    <div class="rep" id="rA2" style="top:1290px">REKOR REKOR REKOR REKOR</div>
    {TX("a1", "REKOR IPO", 470, 190)}
    {TX("a2", "TERBESAR", 690, 170, "o")}
    {SUB("a3", "SEPANJANG SEJARAH", 900, "var(--cr)")}
    <div id="crack">{CRACK}</div>
    <div id="stamp"><span>PECAH!</span></div>
    <!-- B paper -->
    <div id="paper"><div class="mh">Kabar Pasar<small>19 NOV 2026</small></div>
      <div class="kick">REKOR IPO TERBESAR</div><div class="hd">Siapa pemecahnya?</div>
      <div id="nm1">ELON MUSK?</div><div id="strike"></div><div id="nm2">ANTHROPIC</div></div>
    <!-- C chat -->
    {TX("c1", "PERUSAHAAN DI BALIK…", 340, 84)}
    <div id="chat"><div class="cb"><span>CHAT AI</span><span>● ● ●</span></div>
      <div class="bub" id="bu">Bantu ringkas laporan ini, ya</div>
      <div class="dots" id="dots"><i></i><i></i><i></i></div>
      <div class="bub" id="ba"><b>CLAUDE</b>Siap! Ini 3 poin pentingnya…</div></div>
    <div class="sim" id="simC" style="left:110px;top:1215px">SIMULASI</div>
    {TX("c2", "AI YANG KAMU PAKAI", 1290, 84)}
    {TX("c3", "TIAP HARI", 1395, 84, "o")}
    <!-- D terminal -->
    <div id="date"><span>19 NOV 2026</span></div>
    <div id="term"><div class="tb">BURSA · LIVE</div>
      <div class="l" id="l1">&gt; status : <b>RESMI MELANTAI ✓</b></div>
      <div class="l" id="l2">&gt; bursa  : <b>NASDAQ</b></div>
      <div class="l" id="l3">&gt; kode   : <b>ANT</b></div></div>
    <div id="tick">ANT<i id="cur"></i></div>
    <!-- E harga -->
    <div id="lab">HARGA IPO · PER LEMBAR</div>
    <div id="big">$0</div>
    <div id="rng"><div class="ax"></div>
      <div class="bd" id="band" style="left:{(70 - 60) / 30 * 840:.0f}px;width:{8 / 30 * 840:.0f}px"></div>
      <div class="bl" id="bandl" style="left:{(70 - 60) / 30 * 840:.0f}px">TARGET AWAL</div>
      {"".join(f'<div class="tk" style="left:{(v - 60) / 30 * 840:.0f}px">${v}</div>' for v in (60, 70, 78, 90))}
      <div id="mk" style="left:{(78 - 60) / 30 * 840:.0f}px"><b>$83</b></div></div>
    <div class="chip" id="atas" style="left:620px;top:1330px;background:var(--o);color:var(--k)">DI ATAS TARGET ↑</div>
    <!-- F dana -->
    <div id="bigM">$0 MILIAR</div>
    <div id="rp"><span>&gt; Rp1.300 TRILIUN</span></div>
    <div id="rpn">KURS ±Rp16.000–18.000 / US$</div>
    <div class="rb" id="rb0" style="top:900px"><s>SpaceX · Jun 2026 <b>$75 M</b></s><i id="rbi0" style="width:{75 / 81.34 * 100:.1f}%;background:#3B3B42"></i></div>
    <div class="rb" id="rb1" style="top:1080px"><s>Anthropic · Nov 2026 <b class="o">$81,3 M</b></s><i id="rbi1" style="width:100%;background:var(--o)"></i></div>
    <div class="chip" id="rekor" style="left:700px;top:1250px;background:var(--cr);color:var(--k)">REKOR BARU 🏆</div>
    <!-- G/H grafik -->
    <div id="bell">{BELL}</div>
    {TX("g1", "BEL DIBUNYIKAN", 470, 70)}
    <div id="pz">$83</div>
    {chart}
    <div class="dot" id="d1" style="left:{PTS[1][0]}px;top:{PTS[1][1]}px;background:var(--g)"></div>
    <div class="dot" id="d2" style="left:{PTS[-1][0]}px;top:{PTS[-1][1]}px;background:var(--cr)"></div>
    <div class="chip" id="up34" style="left:{PTS[1][0] + 40}px;top:{PTS[1][1] - 40}px;background:var(--g);color:var(--k)">BUKA $111 · +34%</div>
    <div class="chip" id="up17" style="left:520px;top:{PTS[-1][1] + 40}px;background:var(--cr);color:var(--k)">TUTUP $97 · +17%</div>
    <div id="skm">GRAFIK SKEMATIS · TITIK BUKA / TERTINGGI / TUTUP</div>
    {TX("h1", "PASAR TETAP PASAR", 1350, 76, "o")}
    <!-- I ember -->
    {TX("i1", "TAPI…", 340, 90)}
    {TX("i2", "MASIH RUGI BESAR", 460, 110, "r")}
    <div id="gpu">{GPU}</div>
    {"".join(f'<div class="cash" id="cs{i}" style="left:{360 + i * 80}px;top:900px">$</div>' for i in range(5))}
    <div id="loss">Rugi operasional 2025: <b>$8,06 M</b><br>Biaya komputasi &amp; infrastruktur: <b>$7,33 M</b><small>SUMBER: PROSPEKTUS IPO, VIA REUTERS</small></div>
    {TX("i3", "KOMPUTASI AI SUPER MAHAL", 1420, 60, "o")}
    <!-- J scale -->
    {TX("j1", "INVESTOR LAGI BERTARUH", 340, 84)}
    <div id="scale"><div id="post"></div><div id="base"></div><div id="beam"></div>
      <div class="pan" id="pL" style="left:180px"><div class="rope"></div><div class="bowl" style="background:var(--o)"></div><div class="pl o">MASA DEPAN<br>AI</div></div>
      <div class="pan" id="pR" style="left:720px"><div class="rope"></div><div class="bowl"></div><div class="pl" id="plR">UNTUNG<br>HARI INI</div></div>
      {"".join(f'<div class="coin" id="kc{i}" style="left:{148 + (i % 2) * 70}px;top:{260 - i * 26}px">$</div>' for i in range(4))}</div>
    <!-- K CTA -->
    {TX("k1", "ERA BARU ATAU GELEMBUNG?", 330, 76)}
    <div class="opt" id="oA"><div class="ol">A</div>Awal era baru</div>
    <div class="opt" id="oB"><div class="ol">B</div>Gelembung AI</div>
    {TX("k2", "TULIS DI KOMENTAR", 330, 76, "o")}
    <div id="follow">+ Follow</div><div id="tapc">{TAP}</div>
    {chibi_html(left=305, top=640, w=470)}
  </div>
  <div id="flash"></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

# chibi: mikir saat pertanyaan, tunjuk di "tulis di komentar", lambai di "follow"
t_cta = T[123] - 0.1
track, emph_t = chibi_track(HERE, t_cta, DUR, [(T[123], "mikir"), (T[129], "netral"), (T[133] - 0.1, "tunjuk"),
                                               (T[135] + 0.4, "netral"), (T[137], "lambai"), (T[139] + 0.3, "netral"),
                                               (T[143] + 0.4, "keren")], blinks=(T[127], T[141]))

W = {k: round(T[i] - 0.08, 3) for k, i in dict(B=8, C=15, D=25, E=37, F=51, G=70, I=97, J=110, K=123).items()}
js = f'''
    var T = {{}}; {"; ".join(f"T[{i}]={t}" for i, t in T.items())};
    var W = {W};
    function out(sel, t) {{ tl.to(sel, {{ opacity: 0, y: -40, duration: 0.2, ease: "power2.in" }}, q(t - 0.2)); }}
    function money(sel, t, d, a, b, pre, post) {{ count(sel, t, d, a, b, function (v) {{ return pre + Math.round(v) + (post || ""); }}); }}
    tl.set("#hud", {{ opacity: 1 }}, 0);

    // A · hook PULSE: rekor pecah
    tl.set(".rep", {{ opacity: 1 }}, 0);
    tl.fromTo("#rA1", {{ x: 0 }}, {{ x: -500, duration: W.B, ease: "none" }}, 0);
    tl.fromTo("#rA2", {{ x: -500 }}, {{ x: 0, duration: W.B, ease: "none" }}, 0);
    tl.fromTo("#a1", {{ opacity: 1, scale: 1.6 }}, {{ scale: 1, duration: 0.45, ease: "power4.out" }}, 0);
    sweep("#a1", 0.0, 0.3);
    sweep("#a2", T[2] - 0.05, 0.3); kick(T[2], -14);
    tl.fromTo("#a3", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, q(T[3]));
    tl.set("#crack", {{ opacity: 1 }}, q(T[7] - 0.05));
    tl.fromTo("#crack .ck", {{ strokeDasharray: 900, strokeDashoffset: 900 }}, {{ strokeDashoffset: 0, duration: 0.25, ease: "power2.out", stagger: 0.03 }}, q(T[7] - 0.05));
    tl.to("#a1", {{ x: -30, rotation: -4, duration: 0.2 }}, q(T[7])); tl.to("#a2", {{ x: 30, rotation: 4, duration: 0.2 }}, q(T[7]));
    tl.fromTo("#stamp", {{ opacity: 0, scale: 2.4 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "power4.in" }}, q(T[7]));
    flash(T[7] + 0.2, "#flash", 0.5); kick(T[7] + 0.2, 18);
    out("#a1, #a2, #a3, #crack, #stamp, .rep", W.B);

    // B · PAPER: bukan Elon Musk -> Anthropic
    tl.fromTo("#paper", {{ opacity: 0, y: 200, rotation: 4 }}, {{ opacity: 1, y: 0, rotation: -1.5, duration: 0.45, ease: "power3.out" }}, q(W.B));
    tl.fromTo("#nm1", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.3 }}, q(T[11] - 0.1));
    tl.to("#strike", {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, q(T[12] + 0.25));
    tl.to("#nm1", {{ opacity: 0.35, duration: 0.2 }}, q(T[12] + 0.4));
    tl.fromTo("#nm2", {{ opacity: 0, scale: 1.8 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }}, q(T[14] - 0.1));
    flash(T[14] + 0.1, "#flash", 0.25); kick(T[14] + 0.1, 12);
    tl.to("#paper", {{ scale: 1.05, duration: 1.2, ease: "power1.out" }}, q(T[14]));
    out("#paper", W.C);

    // C · SIGNAL: AI yang kamu pakai tiap hari
    sweep("#c1", W.C, 0.4);
    fade("#chat", W.C + 0.3, 0.4, {{ y: 120 }}); tl.set("#simC", {{ opacity: 1 }}, q(W.C + 0.3));
    pop("#bu", T[16], 0.3);
    tl.fromTo("#dots", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, q(T[17]));
    tl.fromTo("#dots i", {{ y: 0 }}, {{ y: -12, duration: 0.18, yoyo: true, repeat: 3, stagger: 0.08 }}, q(T[17]));
    tl.set("#dots", {{ opacity: 0 }}, q(T[18] + 0.2));
    pop("#ba", T[18] + 0.2, 0.3);
    sweep("#c2", T[18], 0.4); sweep("#c3", T[23], 0.3);
    out("#c1, #chat, #simC, #c2, #c3", W.D);

    // D · TERMINAL: 19 Nov, Nasdaq, ANT
    pop("#date", W.D + 0.15, 0.35);
    fade("#term", T[29] - 0.2, 0.35, {{ y: 80 }});
    [["#l1", T[30]], ["#l2", T[32]], ["#l3", T[34]]].forEach(function (e) {{ tl.fromTo(e[0], {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.2 }}, q(e[1])); }});
    tl.fromTo("#tick", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, q(T[36] - 0.1));
    tl.fromTo("#cur", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.25, yoyo: true, repeat: 3, ease: "steps(1)" }}, q(T[36] + 0.2));
    out("#date, #term, #tick", W.E);

    // E · PULSE: harga $83 vs target 70-78
    tl.fromTo("#lab", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, q(W.E));
    tl.set("#big", {{ opacity: 1 }}, q(W.E)); money("#big", T[38], 0.8, 0, 83, "$");
    tl.fromTo("#big", {{ scale: 1.15 }}, Object.assign({{ scale: 1, duration: 0.4, ease: "back.out(2)" }}, NI), q(T[39] + 0.3));
    fade("#rng", T[43], 0.3);
    tl.fromTo("#band, #bandl", {{ scaleX: 0, opacity: 0 }}, {{ scaleX: 1, opacity: 1, duration: 0.4, ease: "power3.out" }}, q(T[47]));
    tl.fromTo("#mk", {{ opacity: 0, x: 0 }}, {{ opacity: 1, duration: 0.2 }}, q(T[49]));
    tl.to("#mk", {{ x: {(83 - 78) / 30 * 840:.0f}, duration: 0.5, ease: "back.out(2)" }}, q(T[50]));
    pop("#atas", T[50] + 0.1, 0.25);
    out("#lab, #big, #rng, #atas", W.F);

    // F · PULSE: dana $81 M, > Rp1.300 T, kalahkan SpaceX
    tl.set("#bigM", {{ opacity: 1 }}, q(W.F)); money("#bigM", T[53], 1.0, 0, 81, "$", " MILIAR");
    tl.fromTo("#bigM", {{ scale: 1.12 }}, Object.assign({{ scale: 1, duration: 0.4, ease: "back.out(2)" }}, NI), q(T[55]));
    pop("#rp", T[59], 0.35); tl.fromTo("#rpn", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(T[61]));
    fade("#rb0", T[64], 0.3); tl.fromTo("#rbi0", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power3.out" }}, q(T[66]));
    fade("#rb1", T[65], 0.3); tl.fromTo("#rbi1", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8, ease: "power3.out" }}, q(T[67]));
    pop("#rekor", T[68] + 0.2, 0.35);
    out("#bigM, #rp, #rpn, .rb, #rekor", W.G);

    // G/H · grafik hari pertama (skematis)
    tl.fromTo("#bell", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, q(W.G));
    tl.fromTo("#bell", {{ rotation: -22 }}, {{ rotation: 22, duration: 0.12, yoyo: true, repeat: 7, ease: "sine.inOut" }}, q(T[71]));
    sweep("#g1", T[71], 0.3);
    out("#bell, #g1", T[73]);
    tl.fromTo("#chart", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(T[73] - 0.1));
    tl.fromTo("#skm", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(T[73]));
    tl.set("#pz", {{ opacity: 1, color: "#F4F1EA" }}, q(T[73]));
    var L1 = document.getElementById("p1").getTotalLength(), L2 = document.getElementById("p2").getTotalLength();
    tl.set("#p1", {{ strokeDasharray: L1, strokeDashoffset: L1 }}, 0); tl.set("#p2", {{ opacity: 0 }}, 0); tl.set("#p2", {{ strokeDasharray: L2, strokeDashoffset: L2 }}, 0);
    tl.to("#p1", {{ strokeDashoffset: 0, duration: 0.6, ease: "power3.out" }}, q(T[75]));
    tl.set("#pz", {{ color: "#22C55E" }}, q(T[75])); money("#pz", T[75], 0.6, 83, 111, "$");
    pop("#d1", T[77], 0.25); pop("#up34", T[79], 0.3); kick(T[79], -10);
    sweep("#h1", T[82], 0.4);
    tl.set("#p2", {{ opacity: 1 }}, q(T[83])); tl.to("#p2", {{ strokeDashoffset: 0, duration: 1.8, ease: "power1.inOut" }}, q(T[83]));
    tl.set("#pz", {{ color: "#F4F1EA" }}, q(T[86])); money("#pz", T[86], 1.2, 111, 97, "$");
    pop("#d2", T[89], 0.25); pop("#up17", T[91], 0.3);
    out("#chart, #pz, .dot, #up34, #up17, #skm, #h1", W.I);

    // I · EMBER: masih rugi besar, komputasi mahal
    tl.fromTo("#glow", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, q(W.I));
    sweep("#i1", W.I, 0.25);
    sweep("#i2", T[101], 0.35); flash(T[102], "#flash", 0.2); kick(T[102], 14);
    tl.fromTo("#gpu", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, q(T[104]));
    tl.to("#gpu", {{ scale: 1.06, duration: 0.25, yoyo: true, repeat: 7, ease: "sine.inOut" }}, q(T[105]));
    [0, 1, 2, 3, 4].forEach(function (i) {{
      tl.fromTo("#cs" + i, {{ opacity: 0, y: 0 }}, {{ opacity: 1, y: -260, duration: 0.5, ease: "power2.out" }}, q(T[105] + i * 0.22));
      tl.to("#cs" + i, {{ opacity: 0, duration: 0.3 }}, q(T[105] + i * 0.22 + 0.5)); }});
    fade("#loss", T[106], 0.35, {{ y: 60 }});
    sweep("#i3", T[108] - 0.2, 0.35);
    out("#i1, #i2, #gpu, #loss, #i3", W.J); tl.to("#glow", {{ opacity: 0, duration: 0.4 }}, q(W.J));

    // J · SIGNAL: timbangan masa depan vs untung hari ini
    sweep("#j1", W.J, 0.35);
    fade("#scale", T[112], 0.35, {{ y: 60 }});
    [0, 1, 2, 3].forEach(function (i) {{ tl.fromTo("#kc" + i, {{ opacity: 0, y: -400 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "bounce.out" }}, q(T[113] + i * 0.18)); }});
    tl.to("#beam", {{ rotation: -12, duration: 0.8, ease: "back.out(1.6)" }}, q(T[115]));
    tl.to("#pL, .coin", {{ y: 76, duration: 0.8, ease: "back.out(1.6)" }}, q(T[115]));
    tl.to("#pR", {{ y: -76, duration: 0.8, ease: "back.out(1.6)" }}, q(T[115]));
    tl.to("#plR", {{ opacity: 0.35, duration: 0.3 }}, q(T[118]));
    out("#j1, #scale", W.K);

    // K · CTA A/B + komentar + follow (chibi)
    sweep("#k1", W.K, 0.4);
    pop("#oA", T[126], 0.3); pop("#oB", T[130], 0.3);
    out("#k1, #oA, #oB", T[133] - 0.05);
    sweep("#k2", T[133], 0.35);
    pop("#follow", T[137] - 0.1, 0.3);
    tl.fromTo("#tapc", {{ opacity: 0, x: 120, y: 120 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.35, ease: "power3.out" }}, q(T[137]));
    tl.to("#follow", {{ backgroundColor: "#FF6A3D", color: "#0B0B0D", scale: 0.94, duration: 0.12 }}, q(T[138]));
    tl.to("#follow", {{ scale: 1, duration: 0.2, ease: "back.out(3)" }}, q(T[138] + 0.12));
    tl.set("#follow", {{ textContent: "Following ✓" }}, q(T[138]));
    tl.to("#tapc", {{ opacity: 0, duration: 0.2 }}, q(T[139] + 0.4));
'''
js += chibi_js(track, emph_t, t_cta)

(HERE / "public" / "index.html").write_text(page("anthropic-ipo", DUR, css, body, js), encoding="utf-8")
print("ok", DUR)
