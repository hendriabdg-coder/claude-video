# Iklan "Dashboard Kuliner UMKM" (templat Google Sheets Endrich) · 9:16 · 2 varian dari satu struktur adegan:
#   python build.py keynote   -> gaya Apple (VO take 1): malam gelap -> terang, MacBook mockup, angka raksasa, tipografi lega
#   python build.py material  -> gaya Google (VO take 2): kartu Material, chip warna, kursor + ripple, kolom komentar
# Angka = DATA DEMO "Kopi Senja" dari screenshot Endrich (dicek silang di analisis.md). Okt dari tab Laba Rugi.
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
from reel_common import chars, fitpx, page  # noqa: E402

V = sys.argv[1] if len(sys.argv) > 1 else "keynote"
assert V in ("keynote", "material")
OUT = HERE / f"build_{V}"
pub = OUT / "public"
pub.mkdir(parents=True, exist_ok=True)
for d in ("fonts", "vendor"):
    if not (pub / d).exists():
        shutil.copytree(ROOT / "motion" / "gaya" / "gaya-terminal" / "public" / d, pub / d)
shutil.copy(ROOT / "motion" / "gaya" / "gaya-terminal" / "public" / "hyperframes.json", pub / "hyperframes.json")
if (pub / "shots").exists():
    shutil.rmtree(pub / "shots")
shutil.copytree(HERE / "shots", pub / "shots")

LEAD, TAIL = 0.15, 1.1
VO = HERE / "vo" / ("vo1.mp3" if V == "keynote" else "vo2.mp3")
vod = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(VO)]))
DUR = round(vod + LEAD + TAIL, 2)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VO), "-af", f"adelay={int(LEAD * 1000)}:all=1,apad,atrim=0:{DUR}",
                "-ar", "44100", str(pub / "vo.mp3")], check=True)

# cue (detik VO) dari silencedetect + Whisper per frasa (lihat analisis.md)
CUE = {
    "keynote": dict(jam=0.0, nota=1.63, catat=3.57, menit=6.05, harga=7.48, dash=10.14, kotor=11.45, bersih=12.3, banding=13.35,
                    bulan=15.87, pilih=17.0, grafik=17.85, bahan=19.92, daftar=21.4, mau=22.9, comment=23.88, link=24.81),
    "material": dict(jam=0.0, nota=1.58, catat=3.56, menit=6.31, harga=7.58, dash=10.39, kotor=11.7, bersih=12.55, banding=13.74,
                     bulan=16.27, pilih=17.41, grafik=18.24, bahan=20.51, daftar=22.0, mau=23.49, comment=24.52, link=25.48),
}[V]
K = {k: round(v + LEAD, 3) for k, v in CUE.items()}
K["end"] = DUR

KEY = V == "keynote"
P = dict(  # palet
    bg="#F5F5F7" if KEY else "#FFFFFF", ink="#1D1D1F" if KEY else "#202124", sub="#6E6E73" if KEY else "#5F6368",
    acc="#0071E3" if KEY else "#1A73E8", brand="#B8611D", night="#050506" if KEY else "#E8EAED",
    g_blue="#4285F4", g_red="#EA4335", g_yel="#FBBC04", g_grn="#34A853", card="#FFFFFF")

css = f'''
:root {{ --bg:{P["bg"]}; --ink:{P["ink"]}; --sub:{P["sub"]}; --acc:{P["acc"]}; --brand:{P["brand"]};
  --gb:{P["g_blue"]}; --gr:{P["g_red"]}; --gy:{P["g_yel"]}; --gg:{P["g_grn"]}; }}
html, body, #root {{ background: var(--bg); color: var(--ink); font-family: "IDBlack"; }}
#bg {{ position: absolute; inset: 0; background: var(--bg); }}
#night {{ position: absolute; inset: 0; background: {P["night"]}; }}
#cam {{ position: absolute; inset: 0; }}
.t {{ position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; line-height: 1.02; letter-spacing: -.03em; }}
.t .ch {{ opacity: 0; }}
.s {{ font-family: "IDSemi"; letter-spacing: -.01em; color: var(--sub); }}
.lab {{ position: absolute; font-family: "IDBold"; font-size: 22px; letter-spacing: .14em; color: var(--sub); opacity: 0; }}
.card {{ position: absolute; background: #fff; border-radius: {28 if not KEY else 22}px; overflow: hidden; opacity: 0;
  box-shadow: 0 {30 if KEY else 8}px {80 if KEY else 24}px rgba(0,0,0,{.18 if KEY else .14}){'' if KEY else ', 0 2px 6px rgba(60,64,67,.15)'}; }}
.card img {{ display: block; width: 100%; }}
.demo {{ position: absolute; left: 60px; top: 1462px; font-family: "IDBold"; font-size: 20px; letter-spacing: .14em; color: var(--sub);
  border: 2px solid rgba(110,110,115,.35); border-radius: 8px; padding: 5px 12px; z-index: 6; }}
#brand {{ position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-size: 34px; color: var(--ink); z-index: 6; }}
#brand b {{ color: var(--brand); font-weight: normal; }}
#flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; pointer-events: none; }}
/* S1 malam */
#clock {{ position: absolute; left: 0; width: 1080px; top: 420px; text-align: center; font-family: "IDSemi"; font-size: 250px; letter-spacing: -.04em;
  color: {"#F5F5F7" if KEY else "#5F6368"}; opacity: 0; font-variant-numeric: tabular-nums; }}
.rc {{ position: absolute; width: 230px; height: 300px; background: #FBFAF6; border-radius: 6px; padding: 22px 20px; opacity: 0;
  box-shadow: 0 10px 30px rgba(0,0,0,.35); }}
.rc i {{ display: block; height: 10px; border-radius: 5px; background: #cfcac0; margin: 14px 0; }}
.rc b {{ display: block; height: 14px; width: 60%; border-radius: 5px; background: #8b8478; }}
.kw {{ position: absolute; top: 760px; font-family: "IDBold"; font-size: 40px; padding: 12px 26px; border-radius: 40px; opacity: 0;
  color: {"#F5F5F7" if KEY else "#fff"}; border: {"2px solid rgba(245,245,247,.5)" if KEY else "0"}; }}
/* MacBook (keynote) */
#mac {{ position: absolute; left: 70px; top: 700px; width: 940px; opacity: 0; transform-origin: 50% 100%; }}
#mac .lid {{ background: #1d1d1f; border-radius: 30px 30px 0 0; padding: 22px 22px 26px; }}
#mac .scr {{ position: relative; height: 560px; border-radius: 8px; overflow: hidden; background: #fff; }}
#mac .scr img {{ position: absolute; left: 0; top: 0; width: 100%; }}
#mac .base {{ height: 28px; margin: 0 -40px; background: linear-gradient(#d8d8dc, #a1a1a6); border-radius: 0 0 26px 26px; }}
.hl {{ position: absolute; border: 4px solid var(--acc); border-radius: 10px; background: rgba(0,113,227,.08); opacity: 0; }}
/* input row (material) */
#row {{ position: absolute; left: 70px; top: 560px; width: 940px; padding: 26px 30px; display: grid; grid-template-columns: 1.1fr 1.7fr .6fr .8fr; gap: 14px; opacity: 0; }}
#row .f {{ border-radius: 14px; background: #F1F3F4; padding: 14px 16px; }}
#row .f s {{ display: block; text-decoration: none; font-family: "IDBold"; font-size: 18px; letter-spacing: .08em; color: var(--sub); }}
#row .f u {{ display: block; text-decoration: none; font-family: "IDBold"; font-size: 30px; color: var(--ink); min-height: 36px; white-space: nowrap; overflow: hidden; }}
#cur {{ position: absolute; width: 56px; height: 56px; color: var(--ink); opacity: 0; z-index: 7; }}
.rip {{ position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%; background: rgba(26,115,232,.25); opacity: 0; z-index: 6; }}
.chip {{ position: absolute; border-radius: 40px; font-family: "IDBold"; color: #fff; padding: 16px 30px; font-size: 40px; opacity: 0; white-space: nowrap; }}
.vchip {{ position: absolute; width: 300px; height: 210px; border-radius: 26px; padding: 26px; color: #fff; opacity: 0; }}
.vchip s {{ display: block; text-decoration: none; font-family: "IDBold"; font-size: 26px; opacity: .9; }}
.vchip u {{ display: block; text-decoration: none; font-family: "IDBlack"; font-size: 46px; margin-top: 26px; font-variant-numeric: tabular-nums; }}
/* KPI */
.kpi {{ position: absolute; left: 90px; width: 900px; opacity: 0; }}
.kpi s {{ display: block; text-decoration: none; font-family: "IDBold"; font-size: 34px; color: var(--sub); }}
.kpi u {{ display: block; text-decoration: none; font-family: "IDBlack"; font-size: 112px; letter-spacing: -.035em; font-variant-numeric: tabular-nums; color: var(--ink); }}
.kpi.m {{ padding: 26px 34px; border-radius: 26px; background: #fff; box-shadow: 0 6px 20px rgba(60,64,67,.15); border-top: 10px solid var(--gb); }}
.kpi.m u {{ font-size: 92px; }}
/* compare bars */
.cmp {{ position: absolute; left: 90px; width: 900px; opacity: 0; }}
.cmp s {{ display: flex; justify-content: space-between; text-decoration: none; font-family: "IDBold"; font-size: 34px; color: var(--sub); margin-bottom: 12px; }}
.cmp s b {{ font-weight: normal; color: var(--ink); font-family: "IDBlack"; font-variant-numeric: tabular-nums; }}
.cmp i {{ display: block; height: 56px; border-radius: 28px; transform-origin: 0 50%; }}
/* dropdown */
#dd {{ position: absolute; left: 240px; top: 560px; width: 600px; padding: 14px; opacity: 0; }}
#dd .it {{ font-family: "IDBold"; font-size: 40px; padding: 20px 26px; border-radius: 14px; color: var(--ink); display: flex; justify-content: space-between; }}
#dd .it.on {{ background: var(--acc); color: #fff; }}
.mbar {{ position: absolute; bottom: 0; width: 140px; border-radius: 18px 18px 6px 6px; transform-origin: 50% 100%; }}
#mchart {{ position: absolute; left: 140px; top: 960px; width: 800px; height: 380px; opacity: 0; }}
#mchart .ml {{ position: absolute; bottom: -54px; width: 140px; text-align: center; font-family: "IDBold"; font-size: 30px; color: var(--sub); }}
#mval {{ position: absolute; left: 0; width: 1080px; top: 860px; text-align: center; font-family: "IDBlack"; font-size: 64px; opacity: 0; font-variant-numeric: tabular-nums; }}
/* belanja list */
#buy {{ position: absolute; left: 90px; top: 1010px; width: 900px; padding: 30px 36px; opacity: 0; }}
#buy h4 {{ font-family: "IDBlack"; font-size: 44px; margin-bottom: 10px; }}
#buy .bi {{ display: flex; align-items: center; gap: 22px; font-family: "IDBold"; font-size: 38px; padding: 14px 0; opacity: 0; }}
#buy .bi i {{ width: 22px; height: 22px; border-radius: 50%; background: var(--gr); flex: none; }}
#buy .bi b {{ margin-left: auto; font-weight: normal; color: var(--gr); font-variant-numeric: tabular-nums; }}
/* CTA */
#sheet {{ position: absolute; left: 0; width: 1080px; top: 610px; text-align: center; opacity: 0; }}
#sheet span {{ display: inline-block; font-family: "IDBlack"; font-size: 190px; letter-spacing: -.03em; color: #fff; background: var(--brand); padding: 6px 54px 20px; border-radius: 40px; }}
#strip {{ position: absolute; top: 1080px; left: 0; height: 330px; display: flex; gap: 26px; opacity: 0; }}
#strip div {{ width: 420px; height: 330px; border-radius: 22px; background-size: cover; background-position: top left; box-shadow: 0 16px 40px rgba(0,0,0,.18); flex: none; }}
#cbox {{ position: absolute; left: 90px; top: 1080px; width: 900px; padding: 26px 30px; display: flex; align-items: center; gap: 22px; opacity: 0; }}
#cbox .av {{ width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg, var(--gb), var(--gg)); flex: none; }}
#cbox .in {{ flex: 1; font-family: "IDBlack"; font-size: 54px; color: var(--ink); }}
#cbox .snd {{ width: 72px; height: 72px; border-radius: 50%; background: var(--acc); color: #fff; font-size: 38px; display: flex; align-items: center; justify-content: center; }}
#reply {{ position: absolute; right: 90px; top: 1260px; max-width: 760px; padding: 24px 32px; border-radius: 30px 30px 8px 30px; background: var(--gg); color: #fff;
  font-family: "IDBold"; font-size: 40px; opacity: 0; }}
'''

CUR = ('<svg class="ico" viewBox="0 0 100 100"><path d="M24 12l52 32-22 6 14 28-11 5-14-28-17 15z" fill="#202124" stroke="#fff" stroke-width="5" '
       'stroke-linejoin="round"/></svg>')


def TX(tid, text, top, px, cls="", maxw=900, font="InterDisplay-Black.ttf", color=None):
    st = f"top:{top}px;font-size:{fitpx(text, px, maxw, font)}px" + (f";color:{color}" if color else "")
    fam = "" if font == "InterDisplay-Black.ttf" else ';font-family:"IDSemi"'
    return f'<div class="t {cls}" id="{tid}" style="{st}{fam}">{chars(text)}</div>'


RCPOS = [(110, 980, -14), (330, 920, 8), (560, 1000, -6), (760, 940, 12), (190, 1150, 5), (430, 1130, -10), (680, 1160, 7), (520, 900, -3)]
rc_html = "".join(f'<div class="rc" id="rc{i}" style="left:{x}px;top:{y}px"><b></b><i></i><i></i><i style="width:70%"></i><i></i><i style="width:50%"></i></div>'
                  for i, (x, y, _) in enumerate(RCPOS))
KWC = [P["g_red"], P["g_yel"], P["g_blue"]]
kw_html = "".join(f'<div class="kw" id="kw{i}" style="left:{x}px;{"" if KEY else f"background:{KWC[i]}"}">{t}</div>'
                  for i, (t, x) in enumerate([("NOTA", 150), ("BUKU KAS", 380), ("KALKULATOR", 680)]))
THUMBS = ["dash", "jual", "stok", "labarugi", "menu", "resep", "kas", "belanja", "rincian", "atur"]
strip_html = "".join(f'<div style="background-image:url(shots/{n}.png)"></div>' for n in THUMBS * 2)

# --- body
s2 = (f'<div id="mac"><div class="lid"><div class="scr"><img id="macimg" src="shots/jual.png">'
      f'<div class="hl" id="hl1" style="left:330px;top:40px;width:96px;height:520px"></div>'
      f'<div class="hl" id="hl2" style="left:700px;top:40px;width:98px;height:520px"></div>'
      f'<div class="hl" id="hl3" style="left:792px;top:40px;width:102px;height:520px"></div></div></div><div class="base"></div></div>') if KEY else (
      '<div class="card" id="row"><div class="f"><s>TANGGAL</s><u id="r1"></u></div><div class="f"><s>MENU</s><u id="r2"></u></div>'
      '<div class="f"><s>JUMLAH</s><u id="r3"></u></div><div class="f"><s>BAYAR</s><u id="r4"></u></div></div>'
      '<div class="card" id="jcard" style="left:70px;top:820px;width:940px;height:600px"><img src="shots/jual.png"></div>')
s3 = "" if KEY else "".join(
    f'<div class="vchip" id="vc{i}" style="left:{70 + i * 320}px;top:1000px;background:{c}"><s>{l}</s><u id="vu{i}">Rp0</u></div>'
    for i, (l, c) in enumerate([("Harga satuan", P["g_blue"]), ("Modal (HPP)", P["g_red"]), ("Laba kotor", P["g_grn"])]))
KPIV = [("Omzet bulan ini", 62250000), ("Laba kotor", 40283050), ("Laba bersih", 21817050)]
KPIC = [P["g_blue"], P["g_yel"], P["g_grn"]]
kpi_html = "".join(f'<div class="kpi{"" if KEY else " m"}" id="kp{i}" style="top:{330 + i * (230 if KEY else 215)}px;{"" if KEY else f"border-top-color:{KPIC[i]}"}">'
                   f'<s>{l}</s><u id="kv{i}">Rp0</u></div>' for i, (l, _) in enumerate(KPIV))
dd_html = "".join(f'<div class="it" id="dd{i}">{m}<span id="ddk{i}"></span></div>' for i, m in enumerate(["September", "Oktober", "November"]))
MB = [("Sep", 62.25), ("Okt", 64.011), ("Nov*", 30.194)]
mb_html = "".join(f'<div class="mbar" id="mb{i}" style="left:{40 + i * 260}px;height:{v / 64.011 * 360:.0f}px;background:#D2D2D7"></div>'
                  f'<div class="ml" style="left:{40 + i * 260}px">{l}</div>' for i, (l, v) in enumerate(MB))

body = f'''
  <div id="bg"></div>
  <div id="night"></div>
  <div id="cam">
    <div id="clock">23:00</div>
    {rc_html}{kw_html}
    {TX("t1", "Masih ngitung nota?", 330, 96, color="#F5F5F7" if KEY else None)}
    <!-- S2 / S3 -->
    {TX("t2a", "Cukup catat penjualan.", 330, 92)}
    {TX("t2b", "per hari, per menu.", 440, 64, "s", font="InterDisplay-SemiBold.ttf")}
    {TX("t2c", "5 menit beres.", 440, 72, color=P["acc"])}
    {s2}
    {TX("t3a", "Harga. Modal. Laba.", 330, 100)}
    {TX("t3b", "terisi sendiri.", 450, 64, "s", font="InterDisplay-SemiBold.ttf")}
    {s3}
    <!-- S4 KPI -->
    {kpi_html}
    <div class="card" id="dcard" style="left:90px;top:1040px;width:900px;height:{380 if KEY else 360}px"><img src="shots/dash.png"></div>
    <!-- S5 banding -->
    {TX("t5a", "Dibandingin bulan lalu.", 330, 86)}
    <div class="cmp" id="cm0" style="top:520px"><s>September <b>Rp62.250.000</b></s><i id="cb0" style="width:{62.25 / 64.011 * 100:.1f}%;background:#D2D2D7"></i></div>
    <div class="cmp" id="cm1" style="top:690px"><s>Oktober <b>Rp64.011.000</b></s><i id="cb1" style="width:100%;background:{P["acc"]}"></i></div>
    <div class="chip" id="up" style="left:760px;top:840px;background:{P["g_grn"]};font-size:36px">+2,8%</div>
    <div class="card" id="lrcard" style="left:90px;top:960px;width:900px;height:480px"><img src="shots/labarugi2.png">
      <div class="hl" id="lh1" style="left:428px;top:66px;width:316px;height:40px"></div>
      <div class="hl" id="lh2" style="left:428px;top:132px;width:316px;height:40px"></div></div>
    <!-- S6 pilih bulan -->
    {TX("t6a", "Mau lihat bulan lain?", 330, 90)}
    <div class="card" id="dd">{dd_html}</div>
    <div id="mval">Rp62.250.000</div>
    <div id="mchart">{mb_html}</div>
    <!-- S7 bahan -->
    {TX("t7a", "Bahan hampir habis?", 330, 90)}
    {TX("t7b", "langsung masuk daftar belanja.", 440, 54, "s", font="InterDisplay-SemiBold.ttf")}
    <div class="card" id="skcard" style="left:140px;top:540px;width:800px;height:470px"><img src="shots/stok2.png" style="margin-top:-40px">
      <div class="hl" id="sh0" style="left:0;top:132px;width:800px;height:40px;border-color:{P["g_red"]};background:rgba(234,67,53,.08)"></div>
      <div class="hl" id="sh1" style="left:0;top:288px;width:800px;height:40px;border-color:{P["g_red"]};background:rgba(234,67,53,.08)"></div>
      <div class="hl" id="sh2" style="left:0;top:444px;width:800px;height:40px;border-color:{P["g_red"]};background:rgba(234,67,53,.08)"></div></div>
    <div class="card" id="buy" style="top:1040px"><h4>Perlu dibeli (3 bahan)</h4>
      <div class="bi" id="bi0"><i></i>Susu UHT<b>sisa 3.534 ml</b></div>
      <div class="bi" id="bi1"><i></i>Cup Plastik + Tutup<b>sisa 92</b></div>
      <div class="bi" id="bi2"><i></i>Telur Ayam<b>sisa 10</b></div></div>
    <!-- S8 CTA -->
    {TX("t8a", "Mau templatenya?", 330, 92)}
    {TX("t8b", "Comment", 470, 130)}
    <div id="sheet"><span>SHEET</span></div>
    {TX("t8c", "nanti aku kirim linknya.", 900, 58, "s", font="InterDisplay-SemiBold.ttf")}
    <div id="strip">{strip_html}</div>
    <div class="card" id="cbox"><div class="av"></div><div class="in" id="cin"></div><div class="snd">➤</div></div>
    <div id="reply">Link templat terkirim ✓ cek DM</div>
    {TX("t8d", "Dashboard Kuliner UMKM · Google Sheets", 1395, 34, "s", font="InterDisplay-SemiBold.ttf")}
    <div class="rip" id="rip"></div>
    <div id="cur">{CUR}</div>
  </div>
  <div class="demo" id="demo">DATA DEMO · KOPI SENJA</div>
  <div id="flash"></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

js = f'''
    var K = {json.dumps(K)}, KEY = {str(KEY).lower()}, RC = {json.dumps(RCPOS)};
    var EZ = KEY ? "power3.out" : "back.out(1.7)";            // Apple: halus · Google: memantul
    function rise(sel, t, d, y) {{ tl.fromTo(sel, {{ opacity: 0, y: y || 50 }}, {{ opacity: 1, y: 0, duration: d || (KEY ? 0.6 : 0.4), ease: EZ }}, q(t)); }}
    function words(sel, t) {{ var ch = document.querySelectorAll(sel + " .ch"); tl.set(sel, {{ opacity: 1 }}, q(t));
      tl.fromTo(ch, {{ opacity: 0, y: KEY ? 30 : 46 }}, {{ opacity: 1, y: 0, duration: KEY ? 0.5 : 0.32, ease: EZ, stagger: Math.min(0.025, 0.45 / ch.length) }}, q(t)); }}
    function out(sel, t) {{ tl.to(sel, {{ opacity: 0, y: -30, duration: 0.25, ease: "power2.in" }}, q(t - 0.25)); }}
    function money(sel, t, d, a, b) {{ count(sel, t, d, a, b, function (v) {{ return "Rp" + idn(v); }}); }}
    function click(x, y, t, hold) {{
      tl.to("#cur", {{ opacity: 1, x: x, y: y, duration: 0.45, ease: "power3.inOut" }}, q(t - 0.5));
      tl.to("#cur", {{ scale: 0.85, duration: 0.07, yoyo: true, repeat: 1 }}, q(t));
      tl.set(".rip", {{ x: x + 10, y: y + 8 }}, q(t));
      tl.fromTo(".rip", {{ opacity: 0.9, scale: 0.2 }}, {{ opacity: 0, scale: 1.6, duration: 0.5, ease: "power2.out" }}, q(t));
      tl.to("#cur", {{ opacity: 0, duration: 0.2 }}, q(t + (hold || 0.6)));
    }}
    tl.set("#cur", {{ x: 900, y: 1500 }}, 0); tl.set("#demo", {{ opacity: 0 }}, 0);

    // S1 · jam 23:00, nota berserakan
    tl.fromTo("#clock", {{ opacity: 0, scale: 1.15 }}, {{ opacity: 1, scale: 1, duration: 0.8, ease: "power3.out" }}, 0.0);
    RC.forEach(function (r, i) {{ tl.fromTo("#rc" + i, {{ opacity: 0, y: -900, rotation: r[2] * 3 }}, {{ opacity: 1, y: 0, rotation: r[2], duration: 0.7, ease: "power3.out" }}, q(0.2 + i * 0.12)); }});
    out("#clock", K.nota);
    words("#t1", K.nota);
    [0, 1, 2].forEach(function (i) {{ tl.fromTo("#kw" + i, {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, q(K.nota + 0.35 + i * 0.3)); }});

    // S2 · terang, catat penjualan
    tl.to("#night", {{ opacity: 0, duration: KEY ? 0.6 : 0.35, ease: "power2.inOut" }}, q(K.catat - 0.15));
    tl.to(".rc", {{ opacity: 0, y: 400, duration: 0.4, ease: "power2.in", stagger: 0.03 }}, q(K.catat - 0.2));
    out("#t1, .kw", K.catat);
    words("#t2a", K.catat); words("#t2b", K.catat + 0.6);
    tl.set("#demo", {{ opacity: 1 }}, q(K.catat));
    if (KEY) {{
      tl.fromTo("#mac", {{ opacity: 0, y: 260, rotationX: 38, scale: 0.86 }}, {{ opacity: 1, y: 0, rotationX: 0, scale: 1, duration: 1.1, ease: "power3.out" }}, q(K.catat + 0.1));
      tl.to("#macimg", {{ y: -150, duration: 2.2, ease: "power1.inOut" }}, q(K.catat + 1.2));
    }} else {{
      rise("#row", K.catat + 0.1); rise("#jcard", K.catat + 0.5, 0.45, 120);
      click(330, 640, K.catat + 0.6, 2.0);
      type("#r1", K.catat + 0.7, 0.5, "01/09/2026"); type("#r2", K.catat + 1.25, 0.7, "Es Kopi Susu Aren");
      type("#r3", K.catat + 2.0, 0.2, "23"); type("#r4", K.catat + 2.25, 0.3, "Tunai");
    }}
    out("#t2b", K.menit); words("#t2c", K.menit);
    tl.fromTo("#t2c", {{ scale: 1.3 }}, Object.assign({{ scale: 1, duration: 0.4, ease: "back.out(2)" }}, NI), q(K.menit));

    // S3 · harga/modal/laba otomatis
    out("#t2a, #t2c", K.harga);
    words("#t3a", K.harga); words("#t3b", K.harga + 0.8);
    if (KEY) {{
      tl.to("#macimg", {{ y: 0, duration: 0.5, ease: "power2.out" }}, q(K.harga - 0.3));
      ["#hl1", "#hl2", "#hl3"].forEach(function (h, i) {{ tl.fromTo(h, {{ opacity: 0, scaleY: 0.2 }}, {{ opacity: 1, scaleY: 1, duration: 0.35, ease: "power3.out" }}, q(K.harga + i * 0.45)); }});
      out("#mac", K.dash); out(".hl", K.dash);
    }} else {{
      out("#jcard", K.harga);
      [[0, 22000], [1, 196995], [2, 309005]].forEach(function (v, i) {{
        tl.fromTo("#vc" + i, {{ opacity: 0, y: 80, scale: 0.8 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2)" }}, q(K.harga + i * 0.45));
        money("#vu" + i, K.harga + 0.15 + i * 0.45, 0.6, 0, v[1]); }});
      out("#row, .vchip", K.dash);
    }}
    out("#t3a, #t3b", K.dash);

    // S4 · KPI
    [[0, K.dash], [1, K.kotor], [2, K.bersih]].forEach(function (e) {{
      rise("#kp" + e[0], e[1] - 0.1, KEY ? 0.6 : 0.4, 60); money("#kv" + e[0], e[1] - 0.05, 0.9, 0, {json.dumps([v for _, v in KPIV])}[e[0]]); }});
    rise("#dcard", K.dash + 0.3, 0.6, 140);
    tl.to("#dcard img", {{ y: -70, duration: 2.5, ease: "power1.inOut" }}, q(K.dash + 0.9));
    out(".kpi, #dcard", K.banding);

    // S5 · banding bulan lalu (Laba Rugi Sep vs Okt)
    words("#t5a", K.banding);
    rise("#cm0", K.banding + 0.2); rise("#cm1", K.banding + 0.45);
    tl.fromTo("#cb0", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power3.out" }}, q(K.banding + 0.3));
    tl.fromTo("#cb1", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power3.out" }}, q(K.banding + 0.55));
    tl.fromTo("#up", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.4)" }}, q(K.banding + 1.1));
    rise("#lrcard", K.banding + 0.5, 0.6, 120);
    tl.fromTo("#lh1, #lh2", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, stagger: 0.25 }}, q(K.banding + 1.2));
    out("#t5a, .cmp, #up, #lrcard", K.bulan);

    // S6 · pilih bulan
    words("#t6a", K.bulan);
    tl.fromTo("#dd", {{ opacity: 0, scale: 0.9, y: -20 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.35, ease: EZ }}, q(K.bulan + 0.3));
    var ON = {{ backgroundColor: "{P["acc"]}", color: "#fff" }}, OFF = {{ backgroundColor: "rgba(0,0,0,0)", color: "{P["ink"]}" }};
    tl.set("#dd0", ON, q(K.bulan + 0.3)); tl.set("#ddk0", {{ textContent: "✓" }}, q(K.bulan + 0.3));
    tl.fromTo("#mchart", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, q(K.bulan + 0.4));
    tl.fromTo(".mbar", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.6, ease: "power3.out", stagger: 0.08 }}, q(K.bulan + 0.4));
    tl.set("#mb0", {{ backgroundColor: "{P["acc"]}" }}, q(K.bulan + 0.4));
    tl.fromTo("#mval", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, q(K.bulan + 0.5));
    click(540, 700, K.pilih);
    tl.set("#dd0", OFF, q(K.pilih)); tl.set("#ddk0", {{ textContent: "" }}, q(K.pilih));
    tl.set("#dd1", ON, q(K.pilih)); tl.set("#ddk1", {{ textContent: "✓" }}, q(K.pilih));
    tl.set("#mb0", {{ backgroundColor: "#D2D2D7" }}, q(K.grafik)); tl.set("#mb1", {{ backgroundColor: "{P["acc"]}" }}, q(K.grafik));
    tl.fromTo("#mb1", {{ scaleY: 0.85 }}, Object.assign({{ scaleY: 1, duration: 0.4, ease: "back.out(2)" }}, NI), q(K.grafik));
    money("#mval", K.grafik, 0.7, 62250000, 64011000);
    tl.to("#cur", {{ opacity: 0, duration: 0.2 }}, q(K.grafik + 0.6));
    out("#t6a, #dd, #mval, #mchart", K.bahan);

    // S7 · bahan habis -> daftar belanja
    words("#t7a", K.bahan); words("#t7b", K.bahan + 0.7);
    rise("#skcard", K.bahan + 0.2, 0.5, 100);
    [0, 1, 2].forEach(function (i) {{
      tl.fromTo("#sh" + i, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, q(K.bahan + 0.8 + i * 0.25));
      tl.to("#sh" + i, {{ opacity: 0.35, duration: 0.18, yoyo: true, repeat: 3 }}, q(K.bahan + 1.0 + i * 0.25)); }});
    rise("#buy", K.daftar - 0.1, 0.45, 80);
    [0, 1, 2].forEach(function (i) {{ tl.fromTo("#bi" + i, {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: EZ }}, q(K.daftar + 0.1 + i * 0.2)); }});
    out("#t7a, #t7b, #skcard, #buy", K.mau);

    // S8 · CTA
    words("#t8a", K.mau);
    words("#t8b", K.comment - 0.05);
    tl.fromTo("#sheet", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, q(K.comment + 0.2));
    if (KEY) {{
      words("#t8c", K.link);
      tl.fromTo("#strip", {{ opacity: 0, x: 200 }}, {{ opacity: 1, x: -1600, duration: K.end - K.mau, ease: "none" }}, q(K.mau));
    }} else {{
      rise("#cbox", K.comment - 0.1, 0.4, 60);
      type("#cin", K.comment + 0.1, 0.4, "SHEET");
      click(950, 1100, K.comment + 0.7);
      tl.fromTo("#reply", {{ opacity: 0, y: 40, scale: 0.8 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2)" }}, q(K.link));
      tl.to("#cur", {{ opacity: 0, duration: 0.2 }}, q(K.link + 0.3));
    }}
    words("#t8d", K.link + 0.4);
'''

html = page(f"iklan-dashboard-{V}", DUR, css, body, js)
(pub / "index.html").write_text(html, encoding="utf-8")
print("ok", V, DUR, K)
