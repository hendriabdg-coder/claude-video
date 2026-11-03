# Hari 3 · Hacker pakai agen AI (Seri AI Pengawas #3)
# Gaya dasar TERMINAL (hitam + hijau fosfor, JetBrains Mono) + PULSE (angka/bar), SIGNAL (alur), EMBER (amber checklist),
# AVATAR (chibi Endrich di CTA) — semua dalam palet TERMINAL.
# Timing: kalau vo/scene_NN.json (VO clone asli) ada, dipakai; kalau belum, diperkirakan dari vo/naskah.txt
# dengan tempo VO lama yang terukur (2,37 kata/dtk) -> preview tanpa suara.
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
VO = HERE / "vo"
FPS, W, H = 30, 1080, 1920
LEAD_IN = 0.25          # VO mulai sedikit setelah frame 0 (hook visual sudah tampil di frame 0)
TAIL = 1.8              # tahan layar A/B setelah VO selesai

segs = [p.strip() for p in (VO / "naskah.txt").read_text(encoding="utf-8").split("\n\n") if p.strip()]
words = [s.split() for s in segs]


def probe(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))


real = all((VO / f"scene_{i + 1:02d}.json").exists() for i in range(len(segs)))
WT, SEG = [], []
t = LEAD_IN
if real:
    for i in range(len(segs)):
        d = json.loads((VO / f"scene_{i + 1:02d}.json").read_text(encoding="utf-8"))
        ws = d["words"] if isinstance(d, dict) else d
        WT.append([round(t + w["start"], 3) for w in ws])
        SEG.append(round(t, 3))
        t += probe(VO / f"scene_{i + 1:02d}.mp3")
else:
    RATE = 2.37
    for ws in words:
        SEG.append(round(t, 3))
        row = []
        for w in ws:
            row.append(round(t, 3))
            t += 1 / RATE
            if w.endswith("..."):
                t += 0.55
            elif w[-1] in ".?!":
                t += 0.25
            elif w[-1] == ",":
                t += 0.12
        WT.append(row)
        t += 0.35
VO_END = t
DUR = round(VO_END + TAIL, 2)
assert [len(r) for r in WT] == [len(w) for w in words], "jumlah kata JSON != naskah"

FONTS = '''@font-face { font-family: "IDBlack"; src: url("fonts/InterDisplay-Black.ttf"); font-display: block; }
@font-face { font-family: "IDBold"; src: url("fonts/InterDisplay-Bold.ttf"); font-display: block; }
@font-face { font-family: "IDSemi"; src: url("fonts/InterDisplay-SemiBold.ttf"); font-display: block; }
@font-face { font-family: "JB"; src: url("fonts/JetBrainsMono-Regular.ttf"); font-display: block; }
@font-face { font-family: "JBB"; src: url("fonts/JetBrainsMono-Bold.ttf"); font-display: block; }
@font-face { font-family: "JBX"; src: url("fonts/JetBrainsMono-ExtraBold.ttf"); font-display: block; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow: hidden; background: #050807; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; }'''

CSS = '''
:root { --bg:#050807; --g:#39FF88; --gd:rgba(57,255,136,.5); --gf:rgba(57,255,136,.14); --amb:#FFB000; --w:#D8FFE8; --red:#FF4D3D; }
#root { background: var(--bg); color: var(--g); font-family: "JB"; }
#crt { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 45%, rgba(57,255,136,.09) 0%, rgba(0,0,0,0) 70%); }
#scan { position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,.26) 0px, rgba(0,0,0,.26) 2px, rgba(0,0,0,0) 2px, rgba(0,0,0,0) 5px); pointer-events: none; z-index: 50; }
#vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 75% at 50% 50%, rgba(0,0,0,0) 60%, rgba(0,0,0,.85) 100%); pointer-events: none; z-index: 51; }
#grain { position: absolute; inset: -50%; width: 200%; height: 200%; opacity: .06; z-index: 52; pointer-events: none;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
#cam { position: absolute; inset: 0; }
.sc { position: absolute; inset: 0; opacity: 0; }
#hud { position: absolute; left: 70px; top: 262px; font-family: "JBB"; font-size: 26px; letter-spacing: .14em; color: var(--gd); z-index: 40; }
#hud b { color: var(--g); font-weight: normal; }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-family: "IDBlack"; font-size: 36px; color: var(--w); z-index: 40; }
#brand b { color: var(--g); font-weight: normal; }
.big { position: absolute; left: 70px; width: 860px; font-family: "JBX"; font-size: 104px; line-height: 1.05; color: var(--g); text-shadow: 0 0 18px rgba(57,255,136,.6); white-space: pre; }
.mid { position: absolute; left: 70px; width: 860px; font-family: "JBB"; font-size: 54px; line-height: 1.15; color: var(--w); white-space: pre; }
.amb { color: var(--amb) !important; text-shadow: 0 0 16px rgba(255,176,0,.55) !important; }
.cur { display: inline-block; width: .5em; height: .85em; background: var(--g); vertical-align: -.08em; margin-left: 6px; }
.tag { position: absolute; font-family: "JBB"; font-size: 22px; letter-spacing: .18em; color: var(--gd); border: 2px solid var(--gd); padding: 6px 12px; border-radius: 6px; }
.src { position: absolute; left: 70px; top: 1440px; font-family: "JB"; font-size: 22px; letter-spacing: .06em; color: rgba(216,255,232,.55); }
.num { font-variant-numeric: tabular-nums; }
/* scene 0/2: grid of sites */
#grid { position: absolute; left: 90px; top: 640px; width: 820px; display: grid; grid-template-columns: repeat(12, 1fr); gap: 10px; }
#grid i { display: block; height: 44px; border: 2px solid rgba(57,255,136,.35); border-radius: 6px; background: rgba(57,255,136,.05); opacity: 0; }
#grid i.on { border-color: var(--g); background: rgba(57,255,136,.22); }
#grid i.hit { border-color: var(--amb); background: rgba(255,176,0,.55); box-shadow: 0 0 12px rgba(255,176,0,.6); }
#cnt { position: absolute; left: 70px; top: 1330px; width: 860px; font-family: "JBX"; font-size: 120px; color: var(--g); text-shadow: 0 0 20px rgba(57,255,136,.6); }
#cnt small { font-family: "JBB"; font-size: 34px; color: var(--w); letter-spacing: .08em; margin-left: 18px; text-shadow: none; }
/* scene 1: prompt window */
#win { position: absolute; left: 70px; top: 700px; width: 860px; height: 420px; border: 2px solid var(--gd); border-radius: 18px; background: rgba(5,12,9,.9); box-shadow: 0 0 40px rgba(57,255,136,.15); overflow: hidden; }
#win .bar { height: 60px; border-bottom: 2px solid rgba(57,255,136,.25); display: flex; align-items: center; gap: 12px; padding: 0 22px; font-size: 24px; color: var(--gd); }
#win .bar i { width: 16px; height: 16px; border-radius: 50%; border: 2px solid var(--gd); display: inline-block; }
#win .body { padding: 34px 34px; font-family: "JBB"; font-size: 46px; line-height: 1.5; color: var(--w); }
#red { letter-spacing: .02em; }
#chars { position: absolute; left: 70px; top: 1170px; width: 860px; }
#chars .k { font-family: "JBB"; font-size: 30px; letter-spacing: .14em; color: var(--gd); }
#chars .v { font-family: "JBX"; font-size: 110px; color: var(--amb); text-shadow: 0 0 20px rgba(255,176,0,.55); }
/* scene 2 */
#cost { position: absolute; left: 70px; top: 1130px; width: 860px; padding: 26px 34px; border: 3px solid var(--amb); border-radius: 16px; background: rgba(30,20,0,.7); }
#cost .v { font-family: "JBX"; font-size: 120px; color: var(--amb); line-height: 1; text-shadow: 0 0 20px rgba(255,176,0,.5); }
#cost .k { font-family: "JBB"; font-size: 30px; color: var(--w); margin-top: 12px; letter-spacing: .06em; }
/* scene 3 */
#k1 { position: absolute; left: 70px; top: 640px; width: 860px; text-align: center; font-family: "JBX"; font-size: 150px; color: var(--g); text-shadow: 0 0 24px rgba(57,255,136,.6); }
#stamp { position: absolute; left: 130px; top: 900px; width: 740px; text-align: center; font-family: "JBX"; font-size: 64px; color: var(--amb); border: 6px solid var(--amb); border-radius: 14px; padding: 18px 10px; transform: rotate(-6deg); text-shadow: 0 0 14px rgba(255,176,0,.5); }
#k2 { position: absolute; left: 70px; top: 1150px; width: 860px; text-align: center; font-family: "JBX"; font-size: 96px; color: var(--amb); }
.gl { position: absolute; left: 0; width: 1080px; height: 30px; background: rgba(57,255,136,.35); mix-blend-mode: screen; opacity: 0; }
/* scene 4 */
#org { position: absolute; left: 70px; top: 640px; width: 860px; font-family: "JBX"; font-size: 200px; line-height: 1; color: var(--g); text-shadow: 0 0 24px rgba(57,255,136,.6); }
#orgk { position: absolute; left: 76px; top: 860px; font-family: "JBB"; font-size: 44px; color: var(--w); letter-spacing: .08em; }
#cal { position: absolute; left: 70px; top: 1020px; width: 860px; display: grid; grid-template-columns: repeat(11, minmax(0, 1fr)); gap: 8px; }
#cal i { display: block; height: 96px; border: 2px solid var(--gd); border-radius: 8px; font-style: normal; font-family: "JBB"; font-size: 22px; color: var(--gd); text-align: center; padding-top: 32px; position: relative; overflow: hidden; }
#cal i b { position: absolute; inset: 0; background: var(--amb); transform: scaleY(0); transform-origin: 50% 100%; opacity: .85; }
#calk { position: absolute; left: 70px; top: 1150px; width: 860px; font-family: "JBX"; font-size: 84px; color: var(--amb); text-shadow: 0 0 16px rgba(255,176,0,.5); }
/* scene 5: bars */
.bcol { position: absolute; bottom: 470px; width: 300px; }
.bcol .bar2 { width: 300px; border-radius: 12px 12px 0 0; transform-origin: 50% 100%; }
.bcol .lab { font-family: "JBB"; font-size: 30px; color: var(--w); text-align: center; margin-top: 16px; letter-spacing: .06em; }
.bcol .val { font-family: "JBX"; font-size: 78px; text-align: center; margin-bottom: 12px; }
#bA { left: 120px; } #bA .bar2 { height: 16px; background: var(--gd); } #bA .val { color: var(--gd); }
#bB { left: 560px; } #bB .bar2 { height: 560px; background: linear-gradient(180deg, var(--amb), rgba(255,176,0,.35)); box-shadow: 0 0 30px rgba(255,176,0,.35); } #bB .val { color: var(--amb); text-shadow: 0 0 16px rgba(255,176,0,.5); }
#axis { position: absolute; left: 90px; top: 1450px; width: 840px; height: 3px; background: var(--gd); }
/* scene 6 */
#tapi { position: absolute; left: 70px; top: 760px; width: 860px; text-align: center; font-family: "JBX"; font-size: 190px; color: var(--amb); text-shadow: 0 0 26px rgba(255,176,0,.6); }
#tapi2 { position: absolute; left: 70px; top: 1000px; width: 860px; text-align: center; font-family: "JBB"; font-size: 50px; color: var(--w); }
/* scene 7: flow */
.node { position: absolute; left: 240px; width: 600px; height: 150px; border: 3px solid var(--gd); border-radius: 18px; background: rgba(5,14,10,.95); display: flex; align-items: center; justify-content: center; font-family: "JBX"; font-size: 60px; color: var(--w); }
#nM { top: 560px; } #nA { top: 860px; } #nT { top: 1160px; }
#nM.hl { border-color: var(--amb); color: var(--amb); box-shadow: 0 0 30px rgba(255,176,0,.45); }
.arrow { position: absolute; left: 536px; width: 8px; background: var(--g); transform-origin: 50% 0; }
#a1 { top: 710px; height: 150px; } #a2 { top: 1010px; height: 150px; }
#side { position: absolute; left: 150px; top: 635px; width: 60px; height: 600px; border: 6px solid var(--amb); border-right: none; border-radius: 30px 0 0 30px; opacity: 0; }
.nlab { position: absolute; font-family: "JBB"; font-size: 30px; letter-spacing: .1em; padding: 6px 14px; border-radius: 8px; }
#lA { left: 560px; top: 1028px; color: var(--bg); background: var(--g); }
#lM { left: 70px; top: 470px; color: var(--bg); background: var(--amb); }
/* scene 8: checklist */
#kd { position: absolute; left: 70px; top: 560px; width: 860px; font-family: "JBX"; font-size: 92px; color: var(--amb); text-shadow: 0 0 24px rgba(255,176,0,.55); line-height: 1.05; }
.row { position: absolute; left: 70px; width: 860px; height: 150px; border: 3px solid var(--gd); border-radius: 18px; display: flex; align-items: center; padding: 0 34px; font-family: "JBX"; font-size: 60px; color: var(--w); background: rgba(5,14,10,.9); }
.row .bx { font-family: "JBX"; color: var(--g); margin-right: 30px; }
.row.ok { border-color: var(--g); box-shadow: 0 0 24px rgba(57,255,136,.25); }
#r1 { top: 820px; } #r2 { top: 1000px; } #r3 { top: 1180px; }
/* CTA + chibi */
#chibi { position: absolute; left: 10px; top: 880px; width: 472px; height: 840px; z-index: 30; transform-origin: 50% 100%; }
#chibiS { position: absolute; inset: 0; }
#chibiS img { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; }
#shadow { position: absolute; left: 110px; top: 1675px; width: 260px; height: 40px; border-radius: 50%; background: rgba(57,255,136,.18); filter: blur(12px); z-index: 29; opacity: 0; }
.ctx { position: absolute; left: 430px; width: 500px; }
#p4a { top: 560px; font-family: "JBB"; font-size: 34px; letter-spacing: .16em; color: var(--gd); }
#p4b { top: 620px; font-family: "JBX"; font-size: 96px; line-height: 1; color: var(--g); text-shadow: 0 0 20px rgba(57,255,136,.6); }
#p4c { top: 850px; font-family: "JBX"; font-size: 62px; line-height: 1.1; color: var(--amb); text-shadow: 0 0 16px rgba(255,176,0,.5); }
#fol { top: 1070px; height: 120px; border-radius: 60px; background: var(--g); color: var(--bg); font-family: "JBX"; font-size: 60px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 30px rgba(57,255,136,.45); }
#fol2 { top: 1210px; font-family: "JBB"; font-size: 32px; color: var(--w); text-align: center; }
#q { position: absolute; left: 70px; top: 330px; width: 860px; font-family: "JBX"; font-size: 64px; line-height: 1.1; color: var(--w); }
.ab { position: absolute; left: 430px; width: 500px; border: 3px solid var(--g); border-radius: 18px; padding: 22px 26px; background: rgba(5,14,10,.92); font-family: "JBX"; font-size: 46px; line-height: 1.12; color: var(--w); }
.ab b { display: block; font-size: 30px; letter-spacing: .14em; color: var(--g); margin-bottom: 8px; font-weight: normal; }
#abA { top: 640px; } #abB { top: 940px; border-color: var(--amb); } #abB b { color: var(--amb); }
#vs { position: absolute; left: 640px; top: 878px; font-family: "JBX"; font-size: 40px; color: var(--gd); }
'''

POSES = ["netral", "lambai", "tunjuk", "mikir", "kaget", "keren", "bicara", "kedip"]
imgs = "".join(f'<img id="p_{p}" src="pose/pose_{i}_{p}.png">' for i, p in enumerate(POSES))
TILES = 12 * 12
HITS = [3, 17, 22, 30, 41, 47, 58, 63, 70, 79, 88, 95, 101, 110, 117, 126, 133, 140]   # ~10% = "100+ dari 1.200+"
grid = "".join("<i></i>" for _ in range(TILES))
cal = "".join(f"<i>{d + 1}<b></b></i>" for d in range(11))
BLOCK = "█"
RED = f"{BLOCK * 4} {BLOCK * 6} {BLOCK * 3} {BLOCK * 7} {BLOCK * 5} {BLOCK * 4} {BLOCK * 6}"

BODY = f'''
  <div id="crt"></div>
  <div id="cam">
    <div class="sc" id="s0">
      <div class="big" id="h1" style="top:330px"><span id="h1t">1 ORANG</span></div>
      <div class="big amb" id="h2" style="top:450px;font-size:84px">+ AGEN AI</div>
      <div id="grid">{grid}</div>
      <div id="cnt"><span class="num" id="cntv">0</span><small>SITUS DISASAR</small></div>
    </div>
    <div class="sc" id="s1">
      <div class="big" style="top:400px;font-size:90px"><span id="s1t"></span><span class="cur" id="c1"></span></div>
      <div id="win"><div class="bar"><i></i><i></i><i></i>&nbsp;agen-ai &mdash; perintah</div>
        <div class="body">&gt; <span id="red"></span><span class="cur" id="c2"></span></div></div>
      <div class="tag" style="left:740px;top:1130px">SIMULASI</div>
      <div id="chars"><div class="k">PANJANG PERINTAH</div><div class="v num" id="chv">&lt; 100 KARAKTER</div></div>
    </div>
    <div class="sc" id="s2">
      <div class="big" id="s2a" style="top:330px;font-size:120px">100+</div>
      <div class="mid" id="s2b" style="top:470px">PERUSAHAAN<br><span class="amb">DILAPORKAN TEMBUS</span></div>
      <div id="cost"><div class="v num" id="costv">US$0</div><div class="k">BIAYA AI &middot; PERKIRAAN PENELITI</div></div>
      <div class="src">sumber: NorForge via Reuters, Okt 2026</div>
    </div>
    <div class="sc" id="s3">
      <div id="k1">KASUS #1</div>
      <div id="stamp">BARU YANG PERTAMA</div>
      <div id="k2">KASUS #2 &rarr;</div>
      <div class="gl" id="gl1" style="top:700px"></div><div class="gl" id="gl2" style="top:980px"></div><div class="gl" id="gl3" style="top:1240px"></div>
    </div>
    <div class="sc" id="s4">
      <div class="tag" id="cs" style="left:70px;top:340px">MENURUT CROWDSTRIKE</div>
      <div class="mid" id="s4h" style="top:420px;font-size:60px">1 KELOMPOK</div>
      <div id="org"><span class="num" id="orgv">0</span>+</div>
      <div id="orgk">ORGANISASI</div>
      <div id="cal">{cal}</div>
      <div id="calk">11 HARI</div>
      <div class="src">sumber: CrowdStrike, 29 Okt 2026</div>
    </div>
    <div class="sc" id="s5">
      <div class="big" style="top:330px;font-size:84px">KECEPATAN</div>
      <div class="mid" style="top:440px;font-size:44px;color:var(--gd)">PERINTAH PER JAM</div>
      <div class="bcol" id="bA"><div class="val num" id="vA">~40</div><div class="bar2"></div><div class="lab">DULU</div></div>
      <div class="bcol" id="bB"><div class="val num" id="vB">0</div><div class="bar2"></div><div class="lab">SEKARANG</div></div>
      <div id="axis"></div>
      <div class="src" style="top:510px">sumber: CrowdStrike (Adam Meyers), 29 Okt 2026</div>
    </div>
    <div class="sc" id="s6">
      <div id="tapi"><span id="tapit"></span><span class="cur" id="c3" style="background:var(--amb)"></span></div>
      <div id="tapi2">SATU HAL YANG PERLU KAMU TAHU</div>
    </div>
    <div class="sc" id="s7">
      <div class="nlab" id="lM">PILIH TARGET</div>
      <div class="node" id="nM">MANUSIA</div>
      <div class="arrow" id="a1"></div>
      <div class="node" id="nA">AGEN AI</div>
      <div class="nlab" id="lA">MEMPERCEPAT</div>
      <div class="arrow" id="a2"></div>
      <div class="node" id="nT">TARGET</div>
      <div id="side"></div>
    </div>
    <div class="sc" id="s8">
      <div id="kd">KEAMANAN<br>DASAR</div>
      <div class="row" id="r1"><span class="bx" id="x1">[ ]</span>UPDATE SISTEM</div>
      <div class="row" id="r2"><span class="bx" id="x2">[ ]</span>BATASI AKSES</div>
      <div class="row" id="r3"><span class="bx" id="x3">[ ]</span>BACKUP DATA</div>
    </div>
    <div class="sc" id="s9">
      <div class="ctx" id="p4a">SERI AI PENGAWAS</div>
      <div class="ctx" id="p4b">PART 4<br>BESOK</div>
      <div class="ctx" id="p4c">AI LAWAN<br>BALIK</div>
      <div class="ctx" id="fol">FOLLOW</div>
      <div class="ctx" id="fol2">biar nggak ketinggalan</div>
    </div>
    <div class="sc" id="s11">
      <div id="q">PUNYA BISNIS? LEBIH KHAWATIR MANA?</div>
      <div class="ab" id="abA"><b>A</b>DATA PELANGGAN DICURI</div>
      <div id="vs">atau</div>
      <div class="ab" id="abB"><b>B</b>BISNIS NGGAK BISA JALAN</div>
    </div>
    <div id="shadow"></div>
    <div id="chibi"><div id="chibiS">{imgs}</div></div>
  </div>
  <div id="hud"><b>SERI AI PENGAWAS</b> #3</div>
  <div id="brand">Endrich<b>Tech</b></div>
  <div id="scan"></div><div id="vig"></div><div id="grain"></div>
'''

JS = r'''
    var FPS = 30;
    function q(t) { return Math.round(t * FPS) / FPS; }
    var tl = gsap.timeline({ paused: true });
    var NI = { immediateRender: false };
    function w(k, j) { return WT[k][j]; }
    function cut(sel, t, v) { tl.set(sel, { opacity: v }, q(t)); }
    function rise(sel, t, d, from) { tl.fromTo(sel, Object.assign({ opacity: 0, y: 50 }, from || {}), { opacity: 1, y: 0, x: 0, scale: 1, rotation: 0, duration: d || 0.35, ease: "back.out(1.4)" }, q(t)); }
    function slam(sel, t) { tl.fromTo(sel, { opacity: 0, scale: 1.35 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, q(t)); }
    function count(sel, t, d, a, b, fmt) { var o = { v: a }, el = document.querySelector(sel); tl.to(o, { v: b, duration: d, ease: "power2.out", onUpdate: function () { el.textContent = fmt(o.v); } }, q(t)); }
    function type(sel, t, d, msg) { var o = { n: 0 }, el = document.querySelector(sel); tl.fromTo(o, { n: 0 }, { n: msg.length, duration: d, ease: "none", onUpdate: function () { el.textContent = msg.slice(0, Math.round(o.n)); } }, q(t)); }
    function id(n) { return n.toLocaleString("id-ID"); }
    function blink(sel, t, d) { var n = Math.max(2, Math.floor(d / 0.4)); if (n % 2) n++; tl.fromTo(sel, { opacity: 1 }, { opacity: 0, duration: 0.4, yoyo: true, repeat: n - 1, ease: "steps(1)" }, q(t)); }
    // scene switching: hard cuts (TERMINAL/PULSE), each scene owns [start, next start)
    var SC = [["#s0", 0], ["#s1", SEG[1]], ["#s2", SEG[2]], ["#s3", SEG[3]], ["#s4", SEG[4]], ["#s5", SEG[5]], ["#s6", SEG[6]],
              ["#s7", SEG[7]], ["#s8", SEG[8]], ["#s9", SEG[9]], ["#s11", SEG[11]]];
    SC.forEach(function (s, i) { cut(s[0], s[1], 1); if (i + 1 < SC.length) cut(s[0], SC[i + 1][1], 0); });
    tl.set("#s0", { opacity: 1 }, 0);
    // CRT flicker on scene cuts
    SC.slice(1).forEach(function (s) { tl.fromTo("#crt", { opacity: 0.3 }, Object.assign({ opacity: 1, duration: 0.18, ease: "steps(3)" }, NI), q(s[1])); });

    // ---- S0 HOOK: readable at frame 0, then grid of sites + counter
    tl.fromTo("#h1", { scale: 1.12, transformOrigin: "0% 50%" }, { scale: 1, duration: 0.35, ease: "back.out(1.4)" }, 0);
    tl.fromTo("#h2", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.3, ease: "back.out(1.4)" }, q(w(0, 4)));
    var tiles = document.querySelectorAll("#grid i");
    tiles.forEach(function (el, k) { var r = Math.floor(k / 12), c = k % 12; cut(el, w(0, 8) + (r + c) * 0.035, 1); });
    tiles.forEach(function (el, k) { var r = Math.floor(k / 12), c = k % 12; tl.set(el, { className: "on" }, q(w(0, 11) + (r * 12 + c) * 0.006)); });
    tl.set("#cnt", { opacity: 0 }, 0); cut("#cnt", w(0, 11), 1);
    count("#cntv", w(0, 11), w(0, 16) - w(0, 11) + 0.2, 0, 1200, function (v) { return id(Math.round(v)) + (v > 1199 ? "+" : ""); });
    tl.fromTo("#cnt", { scale: 1.1 }, Object.assign({ scale: 1, duration: 0.3, ease: "back.out(2)" }, NI), q(w(0, 16)));

    // ---- S1 prompt < 100 chars
    type("#s1t", SEG[1], 0.5, "PERINTAHNYA?");
    blink("#c1", SEG[1], w(1, 8) - SEG[1]);
    type("#red", w(1, 1), w(1, 7) - w(1, 1), "%RED%");
    blink("#c2", w(1, 7), w(1, 10) - w(1, 7));
    tl.fromTo("#chars", { opacity: 0 }, { opacity: 1, duration: 0.01 }, q(w(1, 8)));
    slam("#chv", w(1, 10));

    // ---- S2 100+ breached, ~US$5.000
    var hits = %HITS%;
    hits.forEach(function (k, n) { tl.set(tiles[k], { className: "hit" }, q(w(2, 2) + n * 0.04)); });
    slam("#s2a", w(2, 2));
    rise("#s2b", w(2, 6), 0.3);
    rise("#cost", w(2, 9), 0.35, { y: 80 });
    count("#costv", w(2, 9) + 0.1, w(2, 17) - w(2, 9), 0, 5000, function (v) { return "±US$" + id(Math.round(v / 50) * 50); });
    // grid lives in S0; S2 brings it back (smaller) with the ~10% "hit" tiles
    tl.set("#s0 > :not(#grid)", { opacity: 0 }, q(SEG[1]));
    tl.set("#grid", { scale: 0.7, transformOrigin: "50% 0%", y: 20 }, q(SEG[2]));
    tl.set("#s0", { opacity: 1 }, q(SEG[2])); tl.set("#s0", { opacity: 0 }, q(SEG[3]));

    // ---- S3 glitch: kasus #1 -> baru yang pertama -> kasus #2
    slam("#k1", SEG[3]);
    ["#gl1", "#gl2", "#gl3"].forEach(function (g, i) { tl.fromTo(g, { opacity: 0, x: -200 }, { opacity: 1, x: 200, duration: 0.12, yoyo: true, repeat: 1, ease: "steps(2)" }, q(SEG[3] + 0.05 * i)); });
    tl.fromTo("#stamp", { opacity: 0, scale: 2.2, rotation: -14 }, { opacity: 1, scale: 1, rotation: -6, duration: 0.25, ease: "power4.in" }, q(w(3, 3)));
    tl.fromTo("#cam", { x: 10 }, Object.assign({ x: 0, duration: 0.25, ease: "elastic.out(1,.3)" }, NI), q(w(3, 3) + 0.25));
    rise("#k2", w(3, 5) + 0.3, 0.3, { x: -80, y: 0 });

    // ---- S4 CrowdStrike: 200+ organisations in 11 days
    tl.fromTo("#cs", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25 }, q(w(4, 5)));
    rise("#s4h", w(4, 8), 0.3);
    tl.set("#org, #orgk", { opacity: 0 }, q(SEG[4]));
    cut("#org", w(4, 12), 1); cut("#orgk", w(4, 14), 1);
    count("#orgv", w(4, 12), w(4, 14) - w(4, 12), 0, 200, function (v) { return Math.round(v); });
    tl.set("#cal, #calk", { opacity: 0 }, q(SEG[4]));
    cut("#cal", w(4, 15), 1);
    document.querySelectorAll("#cal i b").forEach(function (b, k) { tl.to(b, { scaleY: 1, duration: 0.1, ease: "power2.out" }, q(w(4, 16) + k * 0.06)); });
    slam("#calk", w(4, 18));
    tl.set("#calk", { y: 150 }, q(SEG[4]));

    // ---- S5 speed bars 40 -> 1.500
    tl.set("#bA, #bB", { opacity: 0 }, q(SEG[5]));
    rise("#bA", w(5, 4), 0.3);
    tl.fromTo("#bA .bar2", { scaleY: 0 }, { scaleY: 1, duration: 0.3 }, q(w(5, 4)));
    cut("#bB", w(5, 10), 1);
    tl.fromTo("#bB .bar2", { scaleY: 0 }, { scaleY: 1, duration: w(5, 13) - w(5, 10) + 0.3, ease: "power3.out" }, q(w(5, 10)));
    count("#vB", w(5, 10), w(5, 13) - w(5, 10) + 0.3, 0, 1500, function (v) { return id(Math.round(v)) + (v > 1499 ? "+" : ""); });
    tl.fromTo("#cam", { y: 8 }, Object.assign({ y: 0, duration: 0.25, ease: "elastic.out(1,.3)" }, NI), q(w(5, 13) + 0.2));

    // ---- S6 "Tapi..."
    type("#tapit", SEG[6], 0.35, "TAPI");
    blink("#c3", SEG[6], SEG[7] - SEG[6]);
    tl.set("#tapi2", { opacity: 0 }, q(SEG[6]));
    rise("#tapi2", w(6, 3), 0.3);

    // ---- S7 flow: human -> AI -> target
    tl.set("#nM, #nA, #nT, #a1, #a2, #lA, #lM", { opacity: 0 }, q(SEG[7]));
    rise("#nA", SEG[7], 0.3);
    rise("#lA", w(7, 3), 0.25, { x: 40, y: 0 });
    rise("#nT", w(7, 4), 0.3);
    tl.fromTo("#a2", { opacity: 1, scaleY: 0 }, { scaleY: 1, duration: 0.25, ease: "power3.out" }, q(w(7, 4)));
    rise("#nM", w(7, 6), 0.3, { y: -50 });
    tl.fromTo("#a1", { opacity: 1, scaleY: 0 }, { scaleY: 1, duration: 0.25, ease: "power3.out" }, q(w(7, 6) + 0.2));
    tl.set("#nM", { className: "node hl" }, q(w(7, 9)));
    tl.fromTo("#side", { opacity: 0, scaleY: 0, transformOrigin: "50% 0%" }, { opacity: 1, scaleY: 1, duration: 0.35, ease: "power3.out" }, q(w(7, 9)));
    rise("#lM", w(7, 9) + 0.1, 0.25, { x: -40, y: 0 });

    // ---- S8 checklist
    tl.set("#r1, #r2, #r3", { opacity: 0 }, q(SEG[8]));
    rise("#kd", SEG[8], 0.3);
    tl.fromTo("#kd", { scale: 1 }, Object.assign({ scale: 1.06, duration: 0.15, yoyo: true, repeat: 1 }, NI), q(w(8, 5)));
    [["#r1", "#x1", 8], ["#r2", "#x2", 10], ["#r3", "#x3", 15]].forEach(function (r, i) {
      rise(r[0], w(8, r[2]) - 0.15, 0.3, { x: -60, y: 0 });
      tl.set(r[1], { textContent: "[✓]" }, q(w(8, r[2]) + 0.35));
      tl.set(r[0], { className: "row ok" }, q(w(8, r[2]) + 0.35));
    });

    // ---- S9/S10 CTA series + follow
    tl.set("#p4a, #p4b, #p4c, #fol, #fol2", { opacity: 0 }, q(SEG[9]));
    rise("#p4a", SEG[9], 0.25);
    slam("#p4b", SEG[9] + 0.1);
    rise("#p4c", w(9, 9), 0.3);
    tl.fromTo("#fol", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)" }, q(SEG[10]));
    rise("#fol2", w(10, 2), 0.25);
    tl.fromTo("#fol", { scale: 1 }, Object.assign({ scale: 0.92, duration: 0.1, yoyo: true, repeat: 1 }, NI), q(w(10, 0) + 0.5));

    // ---- S11 A/B question
    tl.set("#q, #abA, #abB, #vs", { opacity: 0 }, q(SEG[11]));
    rise("#q", SEG[11], 0.3);
    rise("#abA", w(11, 7), 0.3, { x: 80, y: 0 });
    cut("#vs", w(11, 10), 1);
    rise("#abB", w(11, 11), 0.3, { x: 80, y: 0 });

    // ---- chibi Endrich (CTA): pose track with word-based lip-flap
    TRACK.forEach(function (e) { tl.set("#chibiS img:not(#p_" + e[1] + ")", { opacity: 0 }, q(e[0])); tl.set("#p_" + e[1], { opacity: 1 }, q(e[0])); });
    tl.set("#chibi, #shadow", { opacity: 0 }, 0);
    tl.set("#chibi, #shadow", { opacity: 1 }, q(SEG[9] - 0.05));
    tl.fromTo("#chibi", { y: 700 }, { y: 0, duration: 0.5, ease: "back.out(1.4)" }, q(SEG[9] - 0.05));
    tl.fromTo("#chibiS", { y: 0 }, { y: -10, duration: 0.6, yoyo: true, repeat: BOBS, ease: "sine.inOut" }, q(SEG[9] + 0.5));
    EMPH.forEach(function (t) { tl.fromTo("#chibi", { scaleY: 0.94, scaleX: 1.04 }, Object.assign({ scaleY: 1, scaleX: 1, duration: 0.35, ease: "back.out(3)" }, NI), q(t)); });

    tl.set({}, {}, DUR);
'''


# ---- chibi pose track (CTA): emphasis poses, otherwise netral/bicara flap on estimated or real word times
def pose_track():
    s9, s10, s11 = SEG[9], SEG[10], SEG[11]
    emph = [(s9 - 0.05, "tunjuk", 0.9), (s10 - 0.05, "lambai", 1.1), (WT[11][6] - 0.05, "mikir", 99)]
    flap = []   # (start, end) mouth-open windows from words
    ends = [WT[k][j + 1] if j + 1 < len(WT[k]) else WT[k][j] + 0.4 for k in range(len(WT)) for j in range(len(WT[k]))]
    starts = [WT[k][j] for k in range(len(WT)) for j in range(len(WT[k]))]
    for a, b in zip(starts, ends):
        d = b - a
        flap += [(a, a + d * 0.35), (a + d * 0.55, a + d * 0.8)]
    track, prev = [], None
    for f in range(int(s9 * FPS) - 2, int(DUR * FPS) + 1):
        t = f / FPS
        p = "netral"
        for s, name, hold in emph:
            if s <= t < s + hold:
                p = name
        if p == "netral":
            if t < VO_END and any(a <= t < b for a, b in flap):
                p = "bicara"
            if any(b0 <= t < b0 + 0.13 for b0 in (s9 + 2.2, s11 + 1.0)):
                p = "kedip"
        if p != prev:
            track.append([round(t, 3), p])
        prev = p
    return track, [round(s, 3) for s, _, _ in emph]


TRACK, EMPH = pose_track()
bobs = int((DUR - SEG[9]) / 0.6)
bobs += bobs % 2 == 0   # odd repeat => ends on yoyo start state

js = (JS.replace("%RED%", RED).replace("%HITS%", json.dumps(HITS)))
head = (f"var WT = {json.dumps(WT)}; var SEG = {json.dumps(SEG)}; var DUR = {DUR}; var TRACK = {json.dumps(TRACK)};"
        f" var EMPH = {json.dumps(EMPH)}; var BOBS = {bobs};")
html = f'''<!doctype html>
<html lang="id">
<head><meta charset="utf-8" />
<style>
{FONTS}
{CSS}
</style></head>
<body>
<div id="root" data-composition-id="hari3" data-start="0" data-duration="{DUR}" data-fps="30" data-width="{W}" data-height="{H}">
  <audio id="vo" src="vo.mp3" data-start="0" data-duration="{DUR}" data-track-index="0"></audio>
{BODY}
  <script src="vendor/gsap.min.js"></script>
  <script>
  (function () {{
    {head}
{js}
    window.__timelines = window.__timelines || {{}};
    window.__timelines["hari3"] = tl;
  }})();
  </script>
</div>
</body>
</html>
'''
(HERE / "public" / "index.html").write_text(html, encoding="utf-8")
(HERE / "public" / "timing.json").write_text(json.dumps({"real_vo": real, "dur": DUR, "vo_end": round(VO_END, 3), "seg": SEG}, indent=1))
print(f"ok  real_vo={real}  dur={DUR}s  segs={SEG}")
