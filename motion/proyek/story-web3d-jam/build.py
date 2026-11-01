# Reel "Kenapa pembeli batal checkout" — STORY MOTION (gaya 10, template motion/gaya/gaya-story): storytelling edu + ad for
# the creator's 3D-website service, aimed at UMKM owners. 5 acts (kenalan · masalah · kenapa? · berubah · kamu), the
# creator's real demo (Aset-iklan.mp4, prep.py) inside the browser card, animated chibi narrator via compose.py.
#   python prep.py && python build.py  ->  public/index.html + public/char_track.json
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
import gaya_common  # noqa: E402
from gaya_common import page  # noqa: E402

VS = 0.3
VO = json.loads((HERE / "vo" / "vo-full.json").read_text(encoding="utf-8"))
T = {i: round(w["start"] + VS, 3) for i, w in enumerate(VO["words"])}
END_VO = VO["words"][-1]["end"] + VS
DUR = round(END_VO + 1.2, 2)
gaya_common.DUR = DUR
# 0 Pernah 1 batal 2 checkout 3 karena 4 nggak 5 yakin 6 barangnya 7 sama 8 kayak 9 di 10 foto? 11 Kayak 12 pembeli 13 jam
# 14 di 15 toko 16 online 17 milik 18 Dimas. 19 Soalnya, 20 di 21 toko 22 online 23 kan, 24 barangnya 25 nggak 26 bisa
# 27 dipegang. 28 Dan 29 hasil 30 riset 31 Boston 32 College 33 menemukan: 34 bahwa 35 orang 36 yang 37 memilih 38 produk
# 39 pakai 40 layar 41 sentuh, 42 bukan 43 mouse, 44 itu 45 mematok 46 harga 47 jualnya 48 hampir 49 lima 50 puluh
# 51 persen 52 lebih 53 tinggi. 54 Kata 55 penelitinya, 56 nyentuh 57 layar 58 itu, 59 bikin 60 rasa 61 memilikinya
# 62 tinggi. 63 Makanya 64 Dimas 65 biarin 66 pembeli 67 pegang 68 lewat 69 layar, 70 melalui 71 website 72 3D. 73 Jamnya
# 74 berputar... 75 dibongkar 76 sampai 77 ke 78 mesin-mesinnya. 79 Dan 80 untuk 81 video 82 selanjutnya, 83 aku 84 akan
# 85 bahas 86 usaha 87 apa 88 aja 89 yang 90 cocok 91 pakai 92 website 93 3D. 94 Follow 95 biar 96 nggak 97 ketinggalan.
# 98 Mau 99 website 100 kayak 101 gini 102 aku 103 bikinin? 104 Komen 105 "3D" 106 buat 107 diskusi 108 lebih 109 lanjut.
# 110 Dan... 111 produk 112 kamu 113 lebih 114 butuh 115 foto 116 yang 117 bagus, 118 atau 119 3D?
A = [0, T[19] - 0.12, T[28] - 0.12, T[63] - 0.12, T[79] - 0.12]     # acts: kenalan, masalah, kenapa, berubah, kamu
A2b = T[54] - 0.12                                                  # inside act 3: "rasa memiliki"
B5, B6 = T[98] - 0.12, T[110] - 0.12                                # inside act 5: offer, A/B question
V0 = A[3] + 0.15                                                    # demo footage starts (prep.py cuts to this)

CHAR = {"dur": DUR, "wm_until": DUR,
        "places": [{"t0": 0.1, "t1": A[1], "scale": 1.0, "cx": 540, "top": 1000},
                   {"t0": A[1], "t1": A[4], "scale": 0.55, "cx": 880, "top": 1185},
                   {"t0": A[4], "t1": DUR, "scale": 0.86, "cx": 540, "top": 1035}],
        "segments": [[0.1, T[11] - 0.1, "tidak_tahu"], [T[11] - 0.1, A[1], "Menyambut_dengan_Dua_Tangan"],
                     [A[1], T[24] - 0.1, "menunjuk_ke_kiri"], [T[24] - 0.1, A[2], "menghela_nafas"],
                     [A[2], T[48] - 0.1, "Berfikir"], [T[48] - 0.1, A2b, "Terkejut"], [A2b, A[3], "menunjuk_keatas"],
                     [A[3], T[73] - 0.1, "jentikan_jari"], [T[73] - 0.1, A[4], "Memutar_Objek_Virtual_20261026051302"],
                     [A[4], T[94] - 0.2, "gerakan_menjelaskan"], [T[94] - 0.2, B5, "Mengepalkan_Tangan_Semangat_20261026045740"],
                     [B5, B6, "mengajak_mendekat"], [B6, DUR, "Presentasi_Kanan_dan_Kiri"]]}

css = '''
@font-face { font-family: "SerifBI"; src: url("fonts/SerifBI.ttf") format("truetype"); font-display: block; }
@font-face { font-family: "Mono"; src: url("fonts/Mono.ttf") format("truetype"); font-display: block; }
:root { --cream:#F2ECE3; --ink:#18161A; --lime:#C6F432; --org:#E2582B; --red:#E8392B; }
html, body, #root { background: var(--cream); color: var(--ink); font-family: "IDBold"; }
.bg { position: absolute; inset: 0; opacity: 0; }
.bg i { position: absolute; border-radius: 50%; filter: blur(95px); opacity: .7; }
#grain { position: absolute; inset: 0; opacity: .55; background-image: radial-gradient(rgba(0,0,0,.07) 1px, transparent 1.2px); background-size: 7px 7px; }
#cam { position: absolute; inset: 0; }
.hud { position: absolute; top: 262px; left: 70px; font-family: "Mono"; font-size: 27px; letter-spacing: .02em; color: rgba(24,22,26,.62); opacity: 0; }
#prog { position: absolute; right: 150px; top: 268px; display: flex; gap: 10px; align-items: center; }
#prog i { width: 46px; height: 12px; border-radius: 6px; background: rgba(24,22,26,.14); position: relative; overflow: hidden; }
#prog i b { position: absolute; inset: 0; background: var(--ink); transform-origin: 0 50%; transform: scaleX(0); }
#prog span { position: relative; width: 120px; height: 30px; font-family: "Mono"; font-size: 24px; color: rgba(24,22,26,.62); margin-left: 8px; }
.hl { position: absolute; left: 70px; top: 330px; width: 860px; font-size: 82px; line-height: 1.1; letter-spacing: -.02em; opacity: 0; font-family: "IDBlack"; }
.hl span { display: inline-block; opacity: 0; margin-right: 18px; }
.hl .ac { font-family: "SerifBI"; font-size: 94px; position: relative; z-index: 0; isolation: isolate; padding: 0 6px; }
.hl .ac:before { content: ""; position: absolute; left: -4px; right: -4px; bottom: 10px; height: 40%; background: var(--lime);
  z-index: -1; transform-origin: 0 50%; transform: scaleX(var(--hx, 0)); border-radius: 6px; }
.hl .num { font-family: "SerifBI"; font-size: 56px; width: 78px; height: 78px; border-radius: 50%; background: var(--org); color: #FFF4EA;
  text-align: center; line-height: 80px; vertical-align: 12px; margin-right: 22px; }
.prop { position: absolute; opacity: 0; }
.tag { position: absolute; opacity: 0; font-family: "Mono"; font-size: 20px; letter-spacing: .08em; color: rgba(24,22,26,.5); white-space: nowrap; }
.badge { position: absolute; width: 74px; height: 86px; border-radius: 14px; background: var(--ink); color: #fff; font-family: "IDBlack";
  font-size: 56px; text-align: center; line-height: 76px; box-shadow: 0 10px 22px rgba(0,0,0,.25); opacity: 0; }
.badge:after { content: ""; position: absolute; left: 18px; bottom: 9px; width: 38px; height: 6px; border-radius: 3px;
  background: linear-gradient(90deg, var(--org) 0 30%, rgba(255,255,255,.35) 30%); }
.win { position: absolute; border-radius: 28px; overflow: hidden; background: #FFFDFB; opacity: 0;
  box-shadow: 0 46px 80px rgba(60,40,30,.20), 0 6px 18px rgba(60,40,30,.10); }
.bar { height: 60px; background: #ECE6DE; display: flex; align-items: center; padding: 0 24px; gap: 12px; }
.bar b { width: 18px; height: 18px; border-radius: 50%; background: #D5CCC2; }
.bar .url { margin-left: 18px; flex: 1; height: 38px; border-radius: 19px; background: #FFFDFB; font-family: "IDSemi";
  font-size: 22px; line-height: 38px; padding-left: 22px; color: rgba(24,22,26,.6); }
/* act 1: product listing (photo) + checkout */
#shop { left: 70px; top: 500px; width: 620px; height: 440px; }
#shop .ph { position: relative; height: 230px; overflow: hidden; background: #1C2740; }
#shop .ph img { position: absolute; left: -170px; top: -70px; width: 960px; height: 540px; object-fit: cover; filter: saturate(.85); }
#shop .ph .p2 { position: absolute; left: 18px; top: 16px; background: rgba(255,255,255,.92); border-radius: 18px; padding: 6px 14px;
  font-family: "Mono"; font-size: 19px; letter-spacing: .08em; }
#shop .inf { padding: 18px 26px; }
#shop .nm { font-family: "IDBlack"; font-size: 34px; }
#shop .st { font-family: "IDSemi"; font-size: 22px; color: rgba(24,22,26,.55); margin-top: 4px; }
#shop .co { position: absolute; right: 26px; bottom: 24px; background: var(--org); color: #fff; font-family: "IDBlack"; font-size: 28px;
  padding: 14px 28px; border-radius: 16px; box-shadow: 0 6px 0 #A63A17; }
#xBat { left: 560px; top: 820px; width: 96px; height: 96px; border-radius: 50%; background: var(--red); color: #fff; font-family: "IDBlack";
  font-size: 62px; text-align: center; line-height: 92px; box-shadow: 0 12px 24px rgba(232,57,43,.35); }
#nameTag { left: 650px; top: 600px; width: 270px; background: #fff; border-radius: 22px; padding: 20px 24px 22px; box-shadow: 0 18px 36px rgba(0,0,0,.14); }
#nameTag .k { font-family: "Mono"; font-size: 18px; letter-spacing: .14em; color: rgba(24,22,26,.5); }
#nameTag .n { font-family: "SerifBI"; font-size: 60px; line-height: 1.05; margin-top: 4px; }
#nameTag .r { font-family: "IDSemi"; font-size: 22px; color: rgba(24,22,26,.65); margin-top: 6px; }
#nameTag:before { content: ""; position: absolute; left: 50%; top: -24px; width: 70px; height: 24px; margin-left: -35px; border-radius: 6px 6px 0 0; background: var(--lime); }
/* act 2: chat bubbles + crossed hand */
.bub { position: absolute; opacity: 0; background: #fff; border-radius: 26px 26px 26px 6px; padding: 18px 26px; font-family: "IDBold"; font-size: 34px;
  box-shadow: 0 14px 30px rgba(0,0,0,.12); white-space: nowrap; }
.bub small { display: block; font-family: "Mono"; font-size: 17px; color: rgba(24,22,26,.45); letter-spacing: .08em; margin-bottom: 4px; }
#hand { left: 120px; top: 900px; width: 230px; height: 230px; }
/* act 3: the fact */
.cmp { position: absolute; top: 590px; width: 330px; height: 360px; border-radius: 28px; padding: 24px; opacity: 0; box-shadow: 0 18px 36px rgba(0,0,0,.14); }
.cmp .l { font-family: "Mono"; font-size: 22px; letter-spacing: .1em; }
.cmp svg { display: block; width: 150px; height: 150px; margin: 22px auto 10px; }
.cmp .v { font-family: "IDBlack"; font-size: 70px; text-align: center; line-height: 1; }
.cmp .s { font-family: "IDSemi"; font-size: 22px; text-align: center; margin-top: 6px; opacity: .7; }
#cTouch { left: 70px; background: var(--ink); color: #F2ECE3; } #cTouch .l { color: var(--lime); }
#cMouse { left: 440px; background: #fff; }
#vs { left: 372px; top: 735px; width: 76px; height: 76px; border-radius: 50%; background: var(--org); color: #fff; font-family: "SerifBI";
  font-size: 40px; text-align: center; line-height: 74px; z-index: 2; }
#src { left: 70px; top: 985px; background: #fff; border: 2px solid rgba(24,22,26,.15); border-radius: 30px; padding: 10px 22px; font-family: "Mono";
  font-size: 20px; color: rgba(24,22,26,.7); white-space: nowrap; }
#own { left: 90px; top: 600px; width: 560px; height: 420px; }
#own .ring { position: absolute; left: 90px; top: 30px; width: 360px; height: 360px; border-radius: 50%; background: #fff; box-shadow: 0 24px 46px rgba(0,0,0,.14); }
#own svg { position: absolute; left: 150px; top: 80px; width: 240px; height: 260px; }
#own .ht { position: absolute; left: 340px; top: 20px; font-size: 110px; color: var(--org); font-family: "IDBlack"; }
#bc { left: 70px; top: 600px; width: 620px; background: #fff; border-radius: 26px; padding: 26px 32px; box-shadow: 0 18px 36px rgba(0,0,0,.12); }
#bc .k { font-family: "Mono"; font-size: 21px; letter-spacing: .12em; color: var(--org); }
#bc .n { font-family: "IDBlack"; font-size: 66px; line-height: 1.1; margin-top: 6px; }
#bc .n i { font-family: "SerifBI"; font-style: normal; }
#bc .r { font-family: "IDSemi"; font-size: 28px; color: rgba(24,22,26,.6); margin-top: 8px; }
/* halftone */
#dots { position: absolute; inset: 0; pointer-events: none; }
#dots i { position: absolute; width: 70px; height: 70px; margin: -35px 0 0 -35px; border-radius: 50%; background: var(--ink); transform: scale(0); }
/* act 4: browser with the real demo */
#stage { position: absolute; inset: 0; perspective: 1800px; }
#web { left: 60px; top: 580px; width: 960px; height: 600px; background: #0E1420; }
#web video { display: block; width: 960px; height: 540px; object-fit: cover; background: #0E1420; }
.lbl { position: absolute; left: 18px; top: 74px; z-index: 2; background: rgba(255,255,255,.9); border-radius: 16px; padding: 5px 14px;
  font-family: "Mono"; font-size: 17px; letter-spacing: .08em; color: rgba(24,22,26,.75); }
#cursor { position: absolute; left: 0; top: 0; width: 56px; height: 56px; opacity: 0; filter: drop-shadow(0 6px 8px rgba(0,0,0,.25)); }
/* act 5 */
#series { left: 70px; top: 580px; width: 860px; background: #fff; border-radius: 30px; padding: 30px 34px; box-shadow: 0 18px 36px rgba(0,0,0,.12); }
#series .k { font-family: "Mono"; font-size: 22px; letter-spacing: .12em; color: var(--org); }
#series .t { font-family: "IDBlack"; font-size: 52px; line-height: 1.08; margin-top: 10px; }
#series .t i { font-family: "SerifBI"; font-style: normal; position: relative; z-index: 0; isolation: isolate; padding: 0 6px; }
#series .t i:before { content: ""; position: absolute; left: -4px; right: -4px; bottom: 6px; height: 40%; background: var(--lime); z-index: -1; border-radius: 6px; }
#series .ch { display: flex; gap: 14px; margin-top: 22px; }
#series .ch span { width: 120px; height: 56px; border-radius: 16px; background: rgba(24,22,26,.08); font-family: "IDBlack"; font-size: 30px;
  color: rgba(24,22,26,.35); text-align: center; line-height: 56px; }
#series .fol { position: absolute; right: 34px; bottom: 30px; background: var(--org); color: #fff; font-family: "IDBlack"; font-size: 30px;
  padding: 14px 30px; border-radius: 18px; box-shadow: 0 7px 0 #A63A17; }
#offer { left: 70px; top: 560px; width: 860px; background: var(--ink); color: #F2ECE3; border-radius: 30px; padding: 26px; box-shadow: 0 30px 60px rgba(0,0,0,.25); }
#offer .k { font-family: "Mono"; font-size: 21px; letter-spacing: .12em; color: var(--lime); padding: 0 8px; }
#offer video { display: block; width: 808px; height: 360px; object-fit: cover; border-radius: 18px; margin-top: 14px; background: #0E1420; }
#offer .t { font-family: "IDBlack"; font-size: 46px; margin: 18px 8px 4px; }
#offer .t i { font-family: "SerifBI"; font-style: normal; color: var(--org); }
#kom { left: 560px; top: 610px; background: var(--lime); color: var(--ink); border-radius: 30px 30px 6px 30px; padding: 18px 30px; font-family: "IDBlack";
  font-size: 44px; box-shadow: 0 16px 30px rgba(0,0,0,.18); white-space: nowrap; }
#kom small { display: block; font-family: "IDSemi"; font-size: 22px; opacity: .75; }
#poll { left: 70px; top: 560px; width: 860px; }
#poll .q { font-family: "IDBlack"; font-size: 58px; line-height: 1.08; margin-bottom: 30px; }
.opt { position: absolute; top: 160px; width: 400px; height: 230px; border-radius: 28px; padding: 26px 30px; box-shadow: 0 18px 36px rgba(0,0,0,.14); opacity: 0; }
.opt .l { font-family: "Mono"; font-size: 26px; letter-spacing: .1em; }
.opt .w { font-family: "IDBlack"; font-size: 72px; line-height: 1.1; margin-top: 10px; }
.opt .w i { font-family: "SerifBI"; font-style: normal; }
#oA { left: 0; background: #fff; } #oB { left: 460px; background: var(--ink); color: #F2ECE3; }
#oB .l { color: var(--lime); }
#vs2 { position: absolute; left: 392px; top: 242px; width: 76px; height: 76px; border-radius: 50%; background: var(--org); color: #fff; font-family: "SerifBI";
  font-size: 40px; text-align: center; line-height: 74px; opacity: 0; z-index: 2; }
#cmt { left: 70px; top: 980px; font-family: "IDSemi"; font-size: 30px; color: rgba(24,22,26,.7); }
#cmt b { font-family: "IDBold"; color: var(--ink); }
'''

BLOBS = {"bg0": [("#FFC9A0", 120, 260, 620), ("#FFE1B0", 640, 900, 560), ("#FFD3B8", 200, 1350, 640)],
         "bg1": [("#C9C6C2", 80, 300, 620), ("#B8BCC4", 640, 960, 520), ("#D6D2CC", 260, 1380, 620)],
         "bg2": [("#A9CFFF", 80, 300, 620), ("#C6F4E0", 640, 960, 520), ("#BFE3FF", 260, 1380, 620)],
         "bg3": [("#FFB48A", 120, 260, 620), ("#FF8C6B", 620, 900, 560), ("#FFD9B0", 200, 1350, 640)],
         "bg4": [("#D5B8FF", 140, 240, 600), ("#FF9E80", 600, 880, 540), ("#E7C9FF", 220, 1360, 640)]}
bg = "".join(f'<div class="bg" id="{k}">' + "".join(
    f'<i style="background:{c};left:{x}px;top:{y}px;width:{s}px;height:{s}px"></i>' for c, x, y, s in v) + "</div>"
    for k, v in BLOBS.items())
HUD = ["// bab 01 &middot; kenalan", "// bab 02 &middot; masalah", "// bab 03 &middot; kenapa?", "// bab 04 &middot; berubah",
       "// bab 05 &middot; kamu"]
DOTS = "".join(f'<i style="left:{x * 90 + 45}px;top:{y * 90 + 45}px"></i>' for y in range(22) for x in range(12))
CUR = '<path d="M4 2 L4 19 L8.5 15 L11.5 22 L14.5 20.7 L11.6 14 L18 14 Z" fill="#18161A" stroke="#FFF" stroke-width="1.4"/>'
# simple line icons (own drawings)
FINGER = ('<svg viewBox="0 0 100 100"><rect x="22" y="8" width="56" height="84" rx="10" fill="none" stroke="currentColor" stroke-width="5"/>'
          '<path d="M52 98 L52 58 Q52 50 59 50 Q66 50 66 58 L66 70 Q72 64 78 70 L80 98" fill="#C6F432" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>'
          '<circle cx="59" cy="44" r="10" fill="none" stroke="#C6F432" stroke-width="4"/></svg>')
MOUSE = ('<svg viewBox="0 0 100 100"><rect x="28" y="14" width="44" height="72" rx="22" fill="none" stroke="currentColor" stroke-width="5"/>'
         '<line x1="50" y1="14" x2="50" y2="40" stroke="currentColor" stroke-width="5"/><path d="M50 14 Q50 2 62 2" fill="none" stroke="currentColor" stroke-width="5"/></svg>')
HAND = ('<svg viewBox="0 0 120 120"><path d="M40 100 L30 64 Q28 56 35 54 Q41 53 43 60 L46 70 L46 26 Q46 18 53 18 Q60 18 60 26 L60 56 L60 20 Q60 12 67 12 '
        'Q74 12 74 20 L74 56 L74 26 Q74 18 81 18 Q88 18 88 26 L88 74 Q88 100 66 104 Z" fill="#fff" stroke="#18161A" stroke-width="5" stroke-linejoin="round"/>'
        '<line x1="14" y1="14" x2="106" y2="106" stroke="#E8392B" stroke-width="10" stroke-linecap="round"/></svg>')
TOUCH = ('<svg viewBox="0 0 100 110"><path d="M34 106 L24 70 Q22 62 29 60 Q35 59 37 66 L40 76 L40 30 Q40 22 47 22 Q54 22 54 30 L54 60 L54 50 Q54 42 61 42 '
         'Q68 42 68 50 L68 62 Q74 56 80 62 L80 84 Q80 104 60 108 Z" fill="#C6F432" stroke="#18161A" stroke-width="5" stroke-linejoin="round"/>'
         '<path d="M30 20 Q47 0 64 20" fill="none" stroke="#18161A" stroke-width="4" stroke-linecap="round"/></svg>')

body = f'''
  {bg}
  <div id="grain"></div>
  <div id="cam">
    {"".join(f'<div class="hud" id="hud{k}">{h}</div>' for k, h in enumerate(HUD))}
    <div id="prog">{"".join(f'<i><b id="pg{k}"></b></i>' for k in range(5))}<span id="pgN">{"".join(f'<em id="pn{k}" style="font-style:normal;position:absolute;left:0;opacity:0">BAB {k + 1}/5</em>' for k in range(5))}</span></div>

    <!-- act 1 · kenalan (hook) -->
    <div class="hl" id="h0"><span>Batal</span><span class="ac">checkout?</span></div>
    <div class="win" id="shop"><div class="bar"><b></b><b></b><b></b><div class="url">toko-dimas.id</div></div>
      <div class="ph"><img src="assets/still_watch.jpg"><div class="p2">FOTO 2D</div><div class="p2" style="left:auto;right:18px;background:#18161A;color:#C6F432">vs WEB 3D?</div></div>
      <div class="inf"><div class="nm">Jam Titanium</div><div class="st">aslinya kayak gini nggak, ya?</div></div>
      <div class="co" id="co">Checkout</div></div>
    <div class="prop" id="xBat">&#10005;</div>
    <div class="prop" id="nameTag"><div class="k">TOKOH &middot; CERITA</div><div class="n">Dimas</div><div class="r">punya toko online jam</div></div>
    <div class="tag" id="tagIl" style="left:74px;top:468px">CERITA ILUSTRASI &middot; SIMULASI</div>

    <!-- act 2 · masalah -->
    <div class="hl" id="h1"><span>Nggak</span><span>bisa</span><span class="ac">dipegang.</span></div>
    <div class="bub" id="b1" style="left:400px;top:620px"><small>PEMBELI &middot; 09.12</small>Aslinya gimana, kak?</div>
    <div class="bub" id="b2" style="left:470px;top:760px"><small>PEMBELI &middot; 09.14</small>Beratnya berapa?</div>
    <div class="bub" id="b3" style="left:380px;top:900px"><small>PEMBELI &middot; 09.20</small>Takut beda sama foto&hellip;</div>
    <svg class="prop" id="hand" viewBox="0 0 120 120">{HAND[HAND.index(">") + 1:-6]}</svg>
    <div class="tag" id="sim1" style="left:404px;top:590px">SIMULASI</div>

    <!-- act 3 · kenapa (fakta) -->
    <div class="hl" id="h2"><span>Riset:</span><span class="ac">layar sentuh</span></div>
    <div class="cmp" id="cTouch"><div class="l">LAYAR SENTUH</div>{FINGER}<div class="v" id="pct">&asymp;+0%</div><div class="s">harga jual dipatok</div></div>
    <div class="cmp" id="cMouse"><div class="l">MOUSE</div>{MOUSE}<div class="v">&mdash;</div><div class="s">pembanding</div></div>
    <div class="prop" id="vs">vs</div>
    <div class="prop" id="bc"><div class="k">RISET KONSUMEN</div><div class="n">Boston <i>College</i></div><div class="r">orang yang memilih produk&hellip;</div></div>
    <div class="prop" id="src">Gips &amp; Brasel &middot; J. Consumer Psychology (2013/2014)</div>
    <div class="hl" id="h2b"><span>Nyentuh</span><span>layar</span><span>=</span><br><span class="ac">rasa memiliki</span></div>
    <div class="prop" id="own"><div class="ring"></div>{TOUCH}<div class="ht">&#9829;</div></div>
    <div class="tag" id="src2" style="left:74px;top:1060px">KESIMPULAN PENELITI &middot; STUDI LAB</div>

    <!-- act 4 · berubah (demo asli) -->
    <div class="hl" id="h3a"><span>&ldquo;Pegang&rdquo;</span><span>lewat</span><span class="ac">layar</span></div>
    <div class="hl" id="h3b"><span class="num">1</span><span class="ac">Berputar</span></div>
    <div class="hl" id="h3c"><span class="num">2</span><span class="ac">Dibongkar</span></div>
    <div id="stage">
      <div class="win" id="web"><div class="bar"><b></b><b></b><b></b><div class="url">entech-jam.id</div></div>
        <div class="lbl">DEMO KARYA &middot; MEREK FIKTIF</div>
        <video id="scr" src="assets/screen.mp4" data-start="{round(V0, 3)}" data-duration="{round(A[4] + 0.1 - V0, 3)}" data-track-index="1" muted playsinline></video>
      </div>
    </div>
    <div class="badge" id="bd3" style="left:840px;top:488px">3D</div>

    <!-- act 5 · kamu -->
    <div class="hl" id="h4"><span>Video</span><span class="ac">selanjutnya</span></div>
    <div class="prop" id="series"><div class="k">NEXT &middot; BESOK</div><div class="t">Usaha apa aja yang <i>cocok</i><br>pakai website 3D?</div>
      <div class="ch"><span>?</span><span>?</span><span>?</span><span>?</span></div>
      <div class="fol" id="fol"><span id="fol1">Follow</span><span id="fol2" style="display:none">Following &#10003;</span></div></div>
    <div class="hl" id="h5"><span>Mau</span><span>website</span><span class="ac">kayak gini?</span></div>
    <div class="prop" id="offer"><div class="k">JASA &middot; ENDRICHTECH</div><div class="lbl" style="top:72px;left:44px">DEMO KARYA &middot; MEREK FIKTIF</div>
      <video id="ofv" src="assets/offer.mp4" data-start="{round(B5, 3)}" data-duration="{round(B6 + 0.1 - B5, 3)}" data-track-index="2" muted playsinline></video>
      <div class="t">Website <i>3D</i> untuk usahamu</div></div>
    <div class="prop" id="kom"><small>buat diskusi lebih lanjut</small>Komen &ldquo;3D&rdquo;</div>
    <div class="prop" id="poll"><div class="q">Produk kamu lebih butuh&hellip;</div>
      <div class="opt" id="oA"><div class="l">A</div><div class="w">Foto bagus</div></div>
      <div class="opt" id="oB"><div class="l">B</div><div class="w"><i>3D</i></div></div><div id="vs2">vs</div></div>
    <div class="prop" id="cmt">Jawab <b>A</b> atau <b>B</b> di komentar</div>
    <svg id="cursor" viewBox="0 0 24 24">{CUR}</svg>
  </div>
  <div id="dots">{DOTS}</div>
'''

js = f'''
    var T = {json.dumps(T)};
    var A = {json.dumps(A)}, A2b = {A2b}, B5 = {B5}, B6 = {B6}, DUR = {DUR};
    function hudTo(k, t) {{ if (k > 0) cut("#hud" + (k - 1), t, 0);
      tl.fromTo("#hud" + k, {{ opacity: 0, y: -10 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power2.out" }}, q(t));
      tl.fromTo("#pg" + k, {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.45, ease: "power2.out" }}, q(t));
      if (k > 0) cut("#pn" + (k - 1), t, 0);
      cut("#pn" + k, t, 1); }}
    function mood(k, t) {{ tl.fromTo("#bg" + k, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.7, ease: "sine.inOut" }}, q(t - 0.2));
      if (k > 0) tl.to("#bg" + (k - 1), {{ opacity: 0, duration: 0.7, ease: "sine.inOut" }}, q(t - 0.2)); }}
    function head(id, t0, wt) {{
      tl.set(id, {{ opacity: 1 }}, q(t0));
      document.querySelectorAll(id + " > span").forEach(function (s, k) {{ var t = wt[k];
        tl.fromTo(s, {{ opacity: 0, y: 34 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, q(t));
        if (s.classList.contains("ac")) tl.fromTo(s, {{ "--hx": 0 }}, {{ "--hx": 1, duration: 0.35, ease: "power2.out" }}, q(t + 0.18)); }});
    }}
    function out(sel, t) {{ tl.to(sel, {{ opacity: 0, y: -24, duration: 0.16, ease: "power2.in" }}, q(t - 0.16)); }}
    function badge(id, t) {{ tl.fromTo(id, {{ opacity: 0, scale: 0.3, rotation: -25 }}, {{ opacity: 1, scale: 1, rotation: 8, duration: 0.4, ease: "back.out(2.6)" }}, q(t)); }}
    document.querySelectorAll(".bg i").forEach(function (b, k) {{
      tl.fromTo(b, {{ x: 0, y: 0 }}, {{ x: (k % 2 ? -80 : 70), y: (k % 3 ? 60 : -50), duration: 8, yoyo: true, repeat: 5, ease: "sine.inOut" }}, 0); }});
    tl.set("#bg0", {{ opacity: 1 }}, 0);

    // ---- BAB 1 · kenalan: hook on screen from frame 1
    hudTo(0, 0);
    head("#h0", 0, [0.0, 0.12]);
    tl.fromTo("#shop", {{ opacity: 0, y: 140, rotation: -5 }}, {{ opacity: 1, y: 0, rotation: -2, duration: 0.5, ease: "back.out(1.6)" }}, 0);
    cut("#tagIl", 0.3, 1);
    tl.fromTo("#cursor", {{ opacity: 0, x: 900, y: 1300 }}, {{ opacity: 1, duration: 0.15 }}, q(0.3));
    tl.to("#cursor", {{ x: 600, y: 1050, duration: 1.0, ease: "power2.inOut" }}, q(0.35));
    tl.to("#co", {{ scale: 1.06, duration: 0.3, yoyo: true, repeat: 1 }}, q(T[4]));
    tl.to("#cursor", {{ x: 960, y: 1360, duration: 0.7, ease: "power2.in" }}, q(T[5]));
    tl.set("#cursor", {{ opacity: 0 }}, q(T[5] + 0.7));
    tl.fromTo("#xBat", {{ opacity: 0, scale: 2.4, rotation: -30 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.28, ease: "power4.in" }}, q(T[6]));
    tl.to("#co", {{ backgroundColor: "#B9B2AA", boxShadow: "0 6px 0 #8E877F", duration: 0.2 }}, q(T[6] + 0.2));
    tl.fromTo("#nameTag", {{ opacity: 0, y: -120, rotation: 12 }}, {{ opacity: 1, y: 0, rotation: 4, duration: 0.6, ease: "back.out(1.8)" }}, q(T[12]));
    tl.to("#nameTag", {{ rotation: -2, duration: 0.6, yoyo: true, repeat: 1, ease: "sine.inOut" }}, q(T[12] + 0.6));
    tl.to("#shop .ph img", {{ scale: 1.06, duration: 5, ease: "none" }}, 0);
    out("#h0, #nameTag, #tagIl, #xBat", A[1]);
    tl.to("#shop", {{ x: -20, y: 60, scale: 0.55, rotation: -6, filter: "grayscale(1)", transformOrigin: "0% 0%", duration: 0.45, ease: "power3.inOut" }}, q(A[1] - 0.1));

    // ---- BAB 2 · masalah
    hudTo(1, A[1]); mood(1, A[1]);
    head("#h1", A[1], [T[25], T[26], T[27]]);
    cut("#sim1", A[1] + 0.2, 1);
    ["#b1", "#b2", "#b3"].forEach(function (s, k) {{
      tl.fromTo(s, {{ opacity: 0, x: 60, scale: 0.85 }}, {{ opacity: 1, x: 0, scale: 1, duration: 0.35, ease: "back.out(2)" }}, q(T[20] + 0.55 * k)); }});
    tl.fromTo("#hand", {{ opacity: 0, scale: 0.4, rotation: -20 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2.2)" }}, q(T[27] - 0.1));
    tl.to("#hand", {{ x: 8, duration: 0.06, yoyo: true, repeat: 5, ease: "none" }}, q(T[27] + 0.3));
    out("#h1, #b1, #b2, #b3, #hand, #sim1, #shop", A[2]);

    // ---- BAB 3 · kenapa: touch vs mouse, +50% harga jual, source chip
    hudTo(2, A[2]); mood(2, A[2]);
    head("#h2", A[2], [T[30], T[40]]);
    tl.fromTo("#cTouch", {{ opacity: 0, x: -160, rotation: -6 }}, {{ opacity: 1, x: 0, rotation: -2, duration: 0.45, ease: "back.out(1.6)" }}, q(T[40]));
    tl.fromTo("#cMouse", {{ opacity: 0, x: 160, rotation: 6 }}, {{ opacity: 1, x: 0, rotation: 2, duration: 0.45, ease: "back.out(1.6)" }}, q(T[43] - 0.1));
    pop("#vs", T[42], 0.3);
    rise("#src", T[31], 0.35, {{ y: 20 }});
    tl.fromTo("#bc", {{ opacity: 0, y: 80, rotation: -3 }}, {{ opacity: 1, y: 0, rotation: -1, duration: 0.45, ease: "back.out(1.6)" }}, q(T[31] - 0.05));
    tl.to("#bc", {{ opacity: 0, x: -80, duration: 0.2, ease: "power2.in" }}, q(T[40] - 0.25));
    count("#pct", T[48], T[53] - T[48] + 0.2, 0, 50, function (v) {{ return "≈+" + Math.round(v) + "%"; }});
    tl.fromTo("#cTouch", {{ scale: 1 }}, {{ scale: 1.07, duration: 0.18, yoyo: true, repeat: 1 }}, q(T[53]));
    tl.to("#cMouse", {{ opacity: 0.45, duration: 0.3 }}, q(T[53]));
    out("#h2, #cTouch, #cMouse, #vs", A2b);
    head("#h2b", A2b, [T[56], T[57], T[58], T[60]]);
    tl.fromTo("#own", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }}, q(T[56]));
    tl.fromTo("#own .ht", {{ scale: 0, rotation: -20 }}, {{ scale: 1, rotation: 8, duration: 0.4, ease: "back.out(3)" }}, q(T[61]));
    tl.to("#own .ht", {{ scale: 1.15, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, q(T[61] + 0.4));
    cut("#src2", T[55], 1);

    // ---- halftone wipe -> BAB 4
    var D = document.querySelectorAll("#dots i");
    D.forEach(function (d) {{ var x = parseFloat(d.style.left), y = parseFloat(d.style.top);
      var r = Math.hypot(x - 540, y - 800) / 1400;
      tl.to(d, {{ scale: 1.5, duration: 0.22, ease: "power2.in" }}, q(A[3] - 0.42 + r * 0.3));
      tl.to(d, {{ scale: 0, duration: 0.25, ease: "power2.out" }}, q(A[3] + 0.05 + r * 0.3)); }});
    tl.set("#h2b, #own, #src, #src2", {{ opacity: 0 }}, q(A[3]));

    // ---- BAB 4 · berubah: the creator's real 3D website demo
    hudTo(3, A[3]); mood(3, A[3]);
    head("#h3a", A[3] + 0.05, [T[67], T[68], T[69]]); out("#h3a", T[73] - 0.1);
    tl.set("#web", {{ transformOrigin: "50% 50%" }}, 0);
    tl.fromTo("#web", {{ opacity: 0, rotationY: -80, scale: 0.9 }}, {{ opacity: 1, rotationY: 0, scale: 1, duration: 0.55, ease: "back.out(1.3)" }}, q(A[3] + 0.15));
    tl.fromTo("#web", {{ y: 0 }}, {{ y: -12, duration: 1.4, yoyo: true, repeat: 3, ease: "sine.inOut" }}, q(A[3] + 0.8));
    badge("#bd3", T[72]);
    head("#h3b", T[73] - 0.1, [T[73] - 0.1, T[74]]); out("#h3b", T[75] - 0.1);
    head("#h3c", T[75] - 0.1, [T[75] - 0.1, T[75]]);
    tl.fromTo("#web", {{ scale: 1 }}, {{ scale: 1.04, duration: 1.6, ease: "power1.inOut" }}, q(T[75]));
    out("#h3c, #web, #bd3", A[4]);

    // ---- BAB 5 · kamu: next video + follow, offer + comment, A/B
    hudTo(4, A[4]); mood(4, A[4]);
    head("#h4", A[4], [T[81], T[82]]);
    tl.fromTo("#series", {{ opacity: 0, y: 120, rotation: 3 }}, {{ opacity: 1, y: 0, rotation: -1.5, duration: 0.5, ease: "back.out(1.5)" }}, q(T[83]));
    document.querySelectorAll("#series .ch span").forEach(function (s, k) {{ rise(s, T[86] + 0.15 * k, 0.3, {{ y: 20 }}); }});
    tl.fromTo("#fol", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.18, yoyo: true, repeat: 3, ease: "power2.out" }}, q(T[94]));
    tl.fromTo("#cursor", {{ opacity: 0, x: 700, y: 1100 }}, Object.assign({{ opacity: 1, duration: 0.2 }}, NI), q(T[94]));
    tl.to("#cursor", {{ x: 830, y: 880, duration: 0.5, ease: "power2.inOut" }}, q(T[94] + 0.05));
    tl.to("#fol", {{ y: 6, boxShadow: "0 1px 0 #A63A17", backgroundColor: "#18161A", duration: 0.08 }}, q(T[95] + 0.3));
    tl.set("#fol1", {{ display: "none" }}, q(T[95] + 0.32)); tl.set("#fol2", {{ display: "inline" }}, q(T[95] + 0.32));
    tl.to("#cursor", {{ opacity: 0, duration: 0.15 }}, q(T[97] + 0.3));
    out("#h4, #series", B5);
    head("#h5", B5, [T[98], T[99], T[100]]);
    tl.fromTo("#offer", {{ opacity: 0, y: 120, rotation: -3 }}, {{ opacity: 1, y: 0, rotation: 1, duration: 0.5, ease: "back.out(1.5)" }}, q(B5 + 0.05));
    tl.fromTo("#kom", {{ opacity: 0, scale: 0.4, rotation: -10 }}, {{ opacity: 1, scale: 1, rotation: -3, duration: 0.4, ease: "back.out(2.4)" }}, q(T[104]));
    tl.to("#kom", {{ y: -10, duration: 0.4, yoyo: true, repeat: 3, ease: "sine.inOut" }}, q(T[104] + 0.5));
    out("#h5, #offer, #kom", B6);
    tl.set("#poll", {{ opacity: 1 }}, q(B6));
    rise("#poll .q", T[111] - 0.1, 0.35);
    tl.fromTo("#oA", {{ opacity: 0, x: -200, rotation: -6 }}, {{ opacity: 1, x: 0, rotation: -2, duration: 0.45, ease: "back.out(1.6)" }}, q(T[115] - 0.1));
    tl.fromTo("#oB", {{ opacity: 0, x: 200, rotation: 6 }}, {{ opacity: 1, x: 0, rotation: 2, duration: 0.45, ease: "back.out(1.6)" }}, q(T[119] - 0.1));
    pop("#vs2", T[118], 0.3);
    rise("#cmt", T[119] + 0.3, 0.35, {{ y: 20 }});
    tl.fromTo("#oA, #oB", {{ y: 0 }}, Object.assign({{ y: -10, duration: 0.45, yoyo: true, repeat: 1, stagger: 0.2, ease: "sine.inOut" }}, NI), q(T[119] + 0.4));
'''

(HERE / "public" / "index.html").write_text(page("story-web3d-jam", css, body, js), encoding="utf-8")
(HERE / "public" / "char_track.json").write_text(json.dumps(CHAR, indent=1), encoding="utf-8")
print("ok DUR", DUR, " acts", [round(a, 2) for a in A], " A2b", round(A2b, 2), " B5", round(B5, 2), " B6", round(B6, 2))
