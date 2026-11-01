# Revisi v2 "AI Mengawasi AI Lain" (59 dtk) setelah review 2026-11-01.
# Kerangka HYBRID 50/50, tapi gaya dicampur per beat:
#   CUT (latar dihapus) -> "split-pop": video asli digeser turun + blur + gelap, orang tajam di posisi aslinya (matte, composite_v2.sh),
#                          panel gelap di atas berisi grafis. Meja/kursi/cahaya tetap ada, jadi tidak melayang.
#   1.4 TERMINAL monitor · 3.6 PAPER/Headline (kartu OpenAI distabilo) · 8.9 TERMINAL sandbox · 18.9 Isometric stack ·
#   20.3/27.6 SIGNAL stepper (4 langkah, yang belum aktif redup) · 34.1 Stat chart tanpa glow · 51.4/53.9 Versus · 56.7 kartu A/B.
#   python build_v2.py && bash composite_v2.sh
import json, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "uji-gaya"))
import build_uji as U
from build_uji import lockup, svg, ROBOT, LOCK, FONTS, MONO, SK, ROOT

DUR = 59.1
TAKE = ROOT / "talking-head/mentah/2026-11-01-ai-mengawasi-ai-lain/gabungan.mp4"
LOGO = ROOT / "talking-head/aset/Image & Logo/OpenAI_logo.png"
SRC = json.load(open(HERE / "sumber.json", encoding="utf-8")) if (HERE / "sumber.json").exists() else {}

EYES = [(600, 395, 265), (560, 356, 216), (572, 464, 335), (648, 432, 216), (605, 464, 313), (583, 535, 324), (606, 486, 308),
        (577, 518, 324), (551, 340, 243), (509, 340, 253), (544, 324, 220), (486, 399, 301), (573, 463, 220), (577, 463, 227),
        (583, 480, 246), (557, 318, 237), (544, 544, 130), (567, 454, 211), (600, 610, 405), (600, 615, 400), (632, 567, 405),
        (573, 616, 470), (577, 583, 324), (583, 625, 463), (541, 560, 350), (544, 544, 350), (551, 593, 350), (541, 544, 366)]
look = json.load(open(HERE / "look/look.json"))["shots"]
SHOTS = [(round(s["start_s"], 3), round(s["end_s"], 3)) + EYES[i] for i, s in enumerate(look)]
U.DUR, U.SHOTS = DUR, SHOTS
PIP = []
for s0, s1, ex, ey, ht in SHOTS:
    head = ey - ht
    r = max(150, min(320, head * 1.9))
    PIP.append({"r": round(r), "fx": ex, "fy": round(ey + head * 0.25), "s": round(175 / r, 4)})

# split-pop: (mulai, selesai, geser turun px) — composite_v2.sh memakai angka yang sama
CUTS = [(1.4, 3.6, 300), (529 / 30, 568 / 30, 280), (1541 / 30, 1616 / 30, 180)]

EYE = svg('<path d="M8 50s16-28 42-28 42 28 42 28-16 28-42 28S8 50 8 50z"/><circle cx="50" cy="50" r="12"/>')
WARN = svg('<path d="M50 12L92 86H8z"/><path d="M50 40v20"/><circle cx="50" cy="72" r="3" fill="currentColor"/>')
SEARCH = svg('<circle cx="42" cy="42" r="26"/><path d="M62 62l26 26"/>')
BELL = svg('<path d="M26 70V46a24 24 0 0 1 48 0v24l8 8H18z"/><path d="M42 85a8 8 0 0 0 16 0"/>')
SHIELD = svg('<path d="M50 10l34 12v26c0 22-15 36-34 44C31 84 16 70 16 48V22z"/>')
FILM = svg('<rect x="14" y="22" width="72" height="56" rx="8"/><path d="M14 36h72M14 64h72M30 22v14M50 22v14M70 22v14M30 64v14M50 64v14M70 64v14"/>')
REPLAY = svg('<path d="M24 50a26 26 0 1 0 8-19"/><path d="M28 16v16h16"/><path d="M45 40l16 10-16 10z" fill="currentColor"/>')

L = lockup
CH, CHH = 1060, 400  # pita dada
LOCKS = [
    L("t01", 0.0, 1.4, [("l2", [("pakai", 0.0), ("AI", 0.3), ("untuk", 0.54)]), ("l1", [("mengawasi", 0.84)])]),
    L("m01", 1.4, 2.2, [("l1w", [("AI", 1.4), ("lain?", 1.54)])]),
    L("m02", 2.2, 3.6, [("l2", [("kedengarannya", 2.24)]), ("tone", [("aneh,", 2.84), ("kan?", 3.14)])]),
    L("t02", 5.933, 7.46, [("l2", [("beberapa", 5.92)]), ("l1", [("AI", 6.38), ("agent", 6.62)])]),
    L("t03", 7.48, 8.9, [("l2", [("berhasil", 7.52)]), ("l1r", [("keluar", 7.96), ("dari", 8.22)]), ("l1r", [("sandbox", 8.44)])]),
    L("t04", 11.8, 13.1, [("l2", [("setelah", 11.84), ("kejadian", 12.14), ("itu", 12.48)])]),
    L("t05", 13.12, 14.78, [("l2", [("OpenAI", 13.14), ("memperluas", 13.46)]), ("l1", [("sistem", 13.98), ("pengawasan", 14.26)])]),
    L("t06", 14.8, 16.12, [("l2", [("tindakan", 15.14)]), ("l1r", [("di", 15.54), ("luar", 15.66), ("izin", 15.86)])]),
    L("t07", 16.14, 17.633, [("l2", [("bisa", 16.16), ("terdeteksi", 16.42)]), ("l1", [("lebih", 17.0), ("cepat", 17.18)])]),
    L("m03", 17.633, 18.933, [("tone", [("nah,", 17.68), ("yang", 17.98), ("menarik,", 18.12)])], top=260, h=200),
    L("m04", 18.933, 20.333, [("l2", [("pengawasnya", 18.933)]), ("l1", [("nggak", 19.42), ("cuma", 19.54), ("satu", 19.74), ("lapis", 19.96)])], top=250, h=230),
    L("t08", 25.2, 27.6, [("l2", [("AI", 25.32), ("investigasi", 25.54)]), ("l1", [("menelusuri", 26.46)])]),
    L("t09", 31.033, 33.767, [("l2", [("tapi,", 31.02), ("seberapa", 31.64)]), ("l1", [("cepat?", 32.7)])]),
    L("m06", 41.6, 43.7, [("tone", [("tapi", 41.62), ("ingat,", 41.82)]), ("l1", [("hasil", 42.72), ("simulasi", 43.08)])], top=470, h=330),
    L("t10", 43.7, 47.1, [("l2", [("bukan", 43.84), ("berarti", 44.18), ("insiden", 44.7), ("aslinya", 45.28)]),
                          ("l1r", [("berhasil", 45.78), ("dihentikan", 46.3)])]),
    L("t11", 47.1, 49.26, [("l2", [("intinya,", 47.08)]), ("l1w", [("AI", 48.08), ("semakin", 48.52), ("mandiri", 48.88)])]),
    L("t12", 49.28, 51.367, [("l2", [("tetap", 49.3), ("butuh", 49.74)]), ("l1", [("batas", 50.04), ("&", 50.44), ("pengawasan", 50.66)])]),
    L("m07", 51.367, 53.867, [("l2", [("besok", 51.52), ("kita", 52.04), ("bahas", 52.32)]), ("l1", [("kasus", 52.64), ("lebih", 53.08), ("mengejutkan", 53.3)])], top=250, h=230),
    L("m08", 53.867, 56.7, [("l2", [("ketika", 54.06), ("AI", 54.56), ("justru", 54.88)]), ("l1r", [("melemahkan", 55.32)]),
                            ("l1r", [("pengawasnya", 55.86), ("sendiri", 56.4)])], top=250, h=360),
    L("t13", 56.7, DUR + 0.2, [("l1", [("save", 57.04), ("+", 57.3), ("follow", 57.48)]), ("l2", [("biar", 57.8), ("nggak", 58.1), ("ketinggalan", 58.2)])], top=1250, h=200),
]

GRAIN = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'>"
         "<feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .5 0'/></filter>"
         "<rect width='100%' height='100%' filter='url(%23n)' opacity='.10'/></svg>\")")

CSS = """
.line { opacity: 0; } .wd { opacity: 1; }
.l1 { text-shadow: 0 5px 20px rgba(0,0,0,.6); } .l1r { text-shadow: 0 5px 20px rgba(0,0,0,.6); }
#wm { top: 1525px; }
#mbg { position: absolute; inset: 0; background: GRAIN, radial-gradient(ellipse at 50% 30%, #181b21 0%, #0b0d10 65%); opacity: 0; }
#vw { clip-path: circle(1400px at 540px 960px); }
#shade { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
#ring { position: absolute; left: 122px; top: 1152px; width: 356px; height: 356px; border-radius: 50%; border: 4px solid var(--y); opacity: 0; }
.sc { position: absolute; inset: 0; opacity: 0; }
.chip { position: absolute; left: 0; width: 1080px; text-align: center; opacity: 0; }
.chip span { font-family: "IMed"; font-size: 30px; letter-spacing: .16em; color: var(--w); padding: 11px 22px; border-radius: 999px;
  background: rgba(255,255,255,.08); border: 2px solid rgba(255,255,255,.2); }
.chip.y span { color: var(--y); background: none; border-color: rgba(255,214,10,.5); }
.tile { position: absolute; border-radius: 30px; padding: 24px; }
.tl-y { background: var(--y); color: #111; } .tl-d { background: #1b1e24; color: var(--w); border: 3px solid rgba(255,255,255,.3); }
.tl-r { background: var(--r); color: #fff; }
.blab { position: absolute; font-family: "IMed"; font-size: 28px; letter-spacing: .14em; color: rgba(246,245,241,.85); white-space: nowrap; opacity: 0; }
/* TERMINAL */
.term { position: absolute; border-radius: 20px; background: rgba(10,12,14,.92); border: 2px solid rgba(255,255,255,.14); overflow: hidden; opacity: 0;
  box-shadow: 0 20px 60px rgba(0,0,0,.5); }
.term .bar { height: 54px; background: rgba(255,255,255,.06); border-bottom: 2px solid rgba(255,255,255,.08); font-family: "Mono"; font-size: 24px;
  color: rgba(246,245,241,.5); line-height: 54px; padding-left: 120px; position: relative; }
.term .bar i { position: absolute; top: 19px; width: 16px; height: 16px; border-radius: 50%; }
.term .ln { font-family: "Mono"; font-size: 38px; line-height: 1.55; color: var(--w); white-space: nowrap; padding: 0 30px; opacity: 0; }
.term .ln .g { color: var(--g); } .term .ln .a { color: #FFB020; } .term .ln .r { color: var(--r); }
.cur { display: inline-block; width: 20px; height: 36px; background: #FFB020; vertical-align: -6px; margin-left: 6px; }
/* PAPER kartu OpenAI */
#paper { position: absolute; left: 230px; top: 380px; width: 620px; height: 640px; background: #F4F2EC; border-radius: 10px; opacity: 0;
  box-shadow: 0 30px 70px rgba(0,0,0,.55); transform: rotate(-3deg); }
#paper img { position: absolute; left: 210px; top: 70px; width: 200px; height: 200px; }
#paper .nm { position: absolute; left: 0; top: 300px; width: 620px; text-align: center; font-family: "IBlack"; font-size: 96px; letter-spacing: -.03em; color: #111; }
#paper .hl { position: absolute; left: 70px; top: 440px; width: 480px; height: 62px; background: #FFE024; transform-origin: 0 50%; }
#paper .kw { position: absolute; left: 0; top: 444px; width: 620px; text-align: center; font-family: "ISemi"; font-size: 44px; color: #111; }
#paper .src { position: absolute; left: 40px; bottom: 30px; width: 540px; font-family: "IMed"; font-size: 24px; line-height: 1.3; letter-spacing: .08em; color: rgba(17,17,17,.55); }
#seri { position: absolute; left: 90px; top: 262px; font-family: "IMed"; font-size: 26px; letter-spacing: .16em; color: #111; background: var(--y);
  padding: 9px 18px; border-radius: 10px; opacity: 0; }
/* ISOMETRIC */
.iso { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
.isoP { opacity: 0; }
/* SIGNAL stepper */
.node { position: absolute; left: 110px; width: 830px; height: 170px; border-radius: 30px; background: rgba(255,255,255,.05);
  border: 2px solid rgba(255,255,255,.14); opacity: 0; }
.node .ic { position: absolute; left: 24px; top: 24px; width: 122px; height: 122px; padding: 24px; border-radius: 28px; }
.node .no { position: absolute; right: 30px; top: 30px; font-family: "Mono"; font-size: 30px; color: rgba(246,245,241,.4); }
.node .tt { position: absolute; left: 176px; top: 30px; font-family: "ISemi"; font-size: 58px; color: var(--w); white-space: nowrap; }
.node .sb { position: absolute; left: 178px; top: 106px; font-family: "IMed"; font-size: 34px; color: rgba(246,245,241,.6); white-space: nowrap; }
.node .sb b { font-weight: normal; color: var(--y); opacity: 0; }
.conn { position: absolute; left: 200px; width: 6px; height: 46px; background: rgba(246,245,241,.3); transform-origin: 50% 0; }
/* STAT */
.st { position: absolute; top: 560px; width: 300px; text-align: center; opacity: 0; }
.st .tile { position: relative; display: inline-block; width: 170px; height: 170px; padding: 36px; }
.st div.t { font-family: "ISemi"; font-size: 40px; color: var(--w); margin-top: 18px; }
#stArr { position: absolute; left: 470px; top: 610px; width: 140px; height: 80px; color: rgba(246,245,241,.6); opacity: 0; }
#big { position: absolute; left: 0; top: 450px; width: 1080px; text-align: center; font-family: "IBlack"; font-size: 230px; letter-spacing: -.05em;
  color: var(--y); opacity: 0; white-space: nowrap; font-variant-numeric: tabular-nums; }
#big small { font-size: 96px; color: var(--w); letter-spacing: -.02em; }
#bar { position: absolute; left: 170px; top: 880px; width: 740px; height: 14px; border-radius: 7px; background: rgba(255,255,255,.14); opacity: 0; }
#bar i { position: absolute; left: 0; top: 0; height: 14px; width: 740px; border-radius: 7px; background: linear-gradient(90deg, var(--r), var(--y)); transform-origin: 0 50%; }
.tick { position: absolute; top: 916px; width: 4px; height: 22px; background: rgba(246,245,241,.35); opacity: 0; }
.tdot { position: absolute; width: 100px; height: 100px; padding: 20px; border-radius: 50%; top: 837px; opacity: 0; }
#tdA { left: 120px; } #tdB { left: 860px; }
.tlab { position: absolute; top: 960px; font-family: "ISemi"; font-size: 38px; line-height: 1.25; color: var(--w); opacity: 0; }
#tlA { left: 90px; } #tlB { right: 140px; text-align: right; }
#warn { position: absolute; left: 470px; top: 300px; width: 140px; height: 140px; color: #FFB020; opacity: 0; }
#strike { position: absolute; left: 140px; top: 0; width: 800px; height: 10px; background: var(--w); border-radius: 5px; transform-origin: 0 50%;
  box-shadow: 0 2px 12px rgba(0,0,0,.6); opacity: 0; }
/* VERSUS */
#vsL, #vsR { position: absolute; inset: 0; opacity: 0; }
#vsL { background: linear-gradient(160deg, rgba(255,59,78,.30), rgba(255,59,78,.06)); clip-path: polygon(0 0, 560px 0, 470px 1920px, 0 1920px); }
#vsR { background: linear-gradient(200deg, rgba(255,214,10,.22), rgba(255,214,10,.04)); clip-path: polygon(560px 0, 1080px 0, 1080px 1920px, 470px 1920px); }
#vsTxt { position: absolute; left: 0; top: 790px; width: 1080px; text-align: center; font-family: "IBlack"; font-size: 90px; color: var(--w); opacity: 0; letter-spacing: -.02em; }
#p2 { position: absolute; left: 0; top: 1060px; width: 1080px; text-align: center; opacity: 0; }
#p2 span { font-family: "IMed"; font-size: 30px; letter-spacing: .14em; color: #111; background: var(--y); padding: 11px 22px; border-radius: 10px; }
/* A/B */
#ab { position: absolute; left: 110px; top: 960px; width: 860px; padding: 26px 30px 30px; border-radius: 28px; background: rgba(10,12,14,.82);
  border: 2px solid rgba(255,255,255,.16); opacity: 0; text-align: center; }
#ab .q { font-family: "ISemi"; font-size: 46px; color: var(--w); }
#ab .opts { display: flex; gap: 22px; justify-content: center; margin-top: 22px; }
#ab .o { font-family: "IBlack"; font-size: 46px; padding: 14px 30px; border-radius: 18px; }
#ab .o1 { background: var(--y); color: #111; } #ab .o2 { background: #F6F5F1; color: #111; }
#ab .k { font-family: "IMed"; font-size: 26px; letter-spacing: .14em; color: rgba(246,245,241,.6); margin-top: 18px; }
""".replace("GRAIN", GRAIN)

def term(tid, style, title, lines, color="#FF5F57"):
    dots = '<i style="left:30px;background:#FF5F57"></i><i style="left:58px;background:#FEBC2E"></i><i style="left:86px;background:#28C840"></i>'
    body = "".join(f'<div class="ln" id="{lid}">{txt}</div>' for lid, txt in lines)
    return f'<div class="term" id="{tid}" style="{style}"><div class="bar">{dots}{title}</div><div style="padding-top:18px">{body}</div></div>'

def iso_plate(i, cy, color, label):
    # belah ketupat isometrik + tebal 26 px
    w, h, t = 260, 130, 26
    top = f"540,{cy - h} {540 + w},{cy} 540,{cy + h} {540 - w},{cy}"
    left = f"{540 - w},{cy} 540,{cy + h} 540,{cy + h + t} {540 - w},{cy + t}"
    right = f"540,{cy + h} {540 + w},{cy} {540 + w},{cy + t} 540,{cy + h + t}"
    return (f'<g class="isoP" id="ip{i}"><polygon points="{left}" fill="{color}" opacity=".55"/><polygon points="{right}" fill="{color}" opacity=".35"/>'
            f'<polygon points="{top}" fill="{color}" opacity=".9"/><text x="{540 + w + 30}" y="{cy + 14}" font-family="Mono" font-size="40" fill="#F6F5F1">{label}</text></g>')

src = SRC.get("openai", {})
SRC_TXT = f'SUMBER: {src["title"]} · {src["date"]}' if src else "UJI INTERNAL OPENAI · PARAFRASE DARI NASKAH"

BODY = f'''  <div id="mbg"></div>
  <div id="vw"><video id="vid" src="plate.mp4" playsinline data-has-audio="true" data-start="0" data-duration="{DUR}" data-track-index="0"></video></div>
  <div id="shade"></div>
  <div class="sc" id="sc1">{term("t1", "left:110px;top:250px;width:830px;height:250px", "monitor — ai_pengawas", [
      ("a1", '<span class="g">$</span> pengawas = AI'), ("a2", '<span class="g">&gt;</span> target: AI lain'),
      ("a3", '<span class="a">&gt;</span> status: aneh?<span class="cur" id="cur1"></span>')])}</div>
  <div class="sc" id="sc2"><div id="seri">SERI AI PENGAWAS #1</div><div class="chip" id="ochip" style="top:262px;left:150px"><span>PENGUJIAN INTERNAL</span></div>
    <div id="paper"><img src="openai.png" /><div class="nm">OpenAI</div><div class="hl"></div><div class="kw">pengujian internal</div><div class="src">{SRC_TXT}</div></div></div>
  <div class="sc" id="sc3">{term("t2", "left:110px;top:330px;width:830px;height:420px", "agent_02 — sandbox", [
      ("s1", '<span class="g">$</span> run agent_02 --sandbox'), ("s2", '<span class="g">[ok]</span> lingkungan terisolasi'),
      ("s3", '<span class="a">[..]</span> seharusnya:'), ("s4", '&nbsp;&nbsp;&nbsp;&nbsp; akses <span class="a">DIBATASI</span>'),
      ("s5", '<span class="r">[!!] ESCAPED</span>')])}<div id="lock" class="tile tl-d" style="left:800px;top:290px;width:110px;height:110px;padding:20px;opacity:0">{LOCK}</div></div>
  <div class="sc" id="sc4"><svg class="iso" viewBox="0 0 1080 1920">{iso_plate(3, 860, "#3a3f48", "03")}{iso_plate(2, 740, "#8a8f98", "02")}{iso_plate(1, 620, "#FFD60A", "01")}</svg></div>
  <div class="sc" id="sc5">
    <div class="node" id="n1" style="top:300px"><div class="ic tl-y">{EYE}</div><div class="no">01</div><div class="tt">AI pemeriksa</div>
      <div class="sb"><b id="n1a">aktivitas</b> · <b id="n1b">penggunaan tools</b></div></div>
    <div class="conn" style="top:470px"></div>
    <div class="node" id="n2" style="top:516px"><div class="ic tl-r">{WARN}</div><div class="no">02</div><div class="tt">tanda mencurigakan</div><div class="sb">kalau ditemukan</div></div>
    <div class="conn" style="top:686px"></div>
    <div class="node" id="n3" style="top:732px"><div class="ic tl-d">{SEARCH}</div><div class="no">03</div><div class="tt">AI investigasi</div><div class="sb">menelusuri kejadian</div></div>
    <div class="conn" style="top:902px"></div>
    <div class="node" id="n4" style="top:948px"><div class="ic tl-y">{BELL}</div><div class="no">04</div><div class="tt">peringatan</div><div class="sb">ke tim keamanan</div></div>
  </div>
  <div class="sc" id="sc6"><div class="chip y" id="simc" style="top:262px"><span>REKAMAN INSIDEN · SIMULASI ULANG</span></div>
    <div class="st" id="stA" style="left:150px"><div class="tile tl-d">{FILM}</div><div class="t">rekaman insiden</div></div>
    <div id="stArr">{svg('<path d="M10 50h70M60 28l22 22-22 22"/>')}</div>
    <div class="st" id="stB" style="left:630px"><div class="tile tl-y">{REPLAY}</div><div class="t">disimulasikan ulang</div></div>
    <div id="big"><span id="num">0</span><small> menit</small></div>
    <div id="bar"><i></i></div>{"".join(f'<div class="tick" style="left:{170 + k * 148}px"></div>' for k in range(6))}
    <div class="tdot tl-r" id="tdA">{ROBOT}</div><div class="tdot tl-y" id="tdB">{BELL}</div>
    <div class="tlab" id="tlA">agent keluar<br>sandbox</div><div class="tlab" id="tlB">peringatan<br>muncul</div>
    <div id="warn">{WARN}</div>
  </div>
  <div class="sc" id="sc7"><div id="vsL"></div><div id="vsR"></div>
    <div class="tile tl-r" id="ev" style="left:60px;top:640px;width:170px;height:170px;padding:24px;opacity:0">{ROBOT}</div><div class="blab" id="evl" style="left:128px;top:826px">AI</div>
    <div class="tile tl-y" id="gd" style="left:800px;top:650px;width:150px;height:150px;padding:26px;opacity:0">{SHIELD}</div><div class="blab" id="gdl" style="left:788px;top:816px">PENGAWAS</div>
    <div id="vsTxt">VS</div><div id="p2"><span>PART 2 · BESOK</span></div>
  </div>
  <div class="sc" id="sc_none"></div>
  <div id="ring"></div>
  {"".join(h for h, _ in LOCKS)}
  <div id="strike"></div>
  <div id="ab"><div class="q">siapa yang harus mengawasi AI?</div><div class="opts"><span class="o o1">A · AI lain</span><span class="o o2">B · manusia</span></div>
    <div class="k">JAWAB DI KOMENTAR</div></div>
  <div id="wm">Endrich<b>Tech</b></div>'''

JS = """
    // reveal per baris, tetap rata tengah sejak muncul
    D.locks.forEach(function (k) {
      var el = document.getElementById(k.id);
      cut(el, k.start, 1);
      el.querySelectorAll(".line").forEach(function (ln) {
        var ts = [].map.call(ln.querySelectorAll("[data-t]"), function (w) { return parseFloat(w.dataset.t); });
        var t = Math.max(Math.min.apply(null, ts), k.start);
        tl.fromTo(ln, { opacity: 0, y: 26, scale: 0.92, filter: "blur(10px)" }, { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.26, ease: "power3.out" }, q(t));
      });
      hide(el, k.end - 0.12, 0.12);
    });
    var P = D.pip, BIG = "circle(1400px at 540px 960px)";
    function circ(p) { return "circle(" + p.r + "px at " + p.fx + "px " + p.fy + "px)"; }
    function pipSet(t, k) {
      var p = P[k];
      tl.set("#vw", { clipPath: circ(p), transformOrigin: p.fx + "px " + p.fy + "px", scale: p.s, x: 300 - p.fx, y: 1330 - p.fy, opacity: 1 }, q(t));
    }
    // dari layar penuh ATAU dari split-pop (posisi sekarang) menyusut ke bulatan
    function pipIn(t, k, fromFull, s0) {
      var p = P[k];
      if (fromFull) tl.set("#vw", { clipPath: BIG, x: 0, y: 0, scale: s0 || 1.1, transformOrigin: p.fx + "px " + p.fy + "px" }, q(t));
      else { tl.set("#vw", { transformOrigin: p.fx + "px " + (p.fy) + "px" }, q(t)); }
      tl.set("#vid", { filter: "none" }, q(t));
      tl.to("#shade", { opacity: 0, duration: 0.3 }, q(t));
      tl.to("#vw", { clipPath: circ(p), scale: p.s, x: 300 - p.fx, y: 1330 - p.fy, duration: 0.45, ease: "power3.inOut" }, q(t));
      tl.fromTo("#ring", { opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }, q(t + 0.27));
      tl.set("#mbg", { opacity: 1 }, q(t));
    }
    function full(t, k, s0, s1, t1) {
      var sh = SH[k];
      tl.set("#vw", { clipPath: BIG, x: 0, y: 0, opacity: 1, transformOrigin: sh[2] + "px " + sh[3] + "px" }, q(t));
      tl.set("#vid", { filter: "none" }, q(t));
      tl.set(["#ring", "#mbg", "#shade"], { opacity: 0 }, q(t));
      tl.fromTo("#vw", { scale: s0 }, { scale: s1, duration: q(t1 || sh[1]) - q(t), ease: t1 && t1 - t < 0.6 ? "power3.out" : "none" }, q(t));
    }
    // split-pop: video turun + blur, panel gelap di atas; orang tajam ditempel di composite_v2.sh dengan kurva yang sama (power3.out 0.4 dtk)
    function splitPop(t, shift, sc) {
      tl.set("#vw", { clipPath: BIG, x: 0, y: 0, scale: 1, opacity: 1, transformOrigin: "540px 960px" }, q(t));
      tl.set("#mbg", { opacity: 1 }, q(t)); cut(sc, t, 1); cut("#wm", t, 0);
      tl.set("#shade", { background: "linear-gradient(to bottom, #0b0d10 0px, #0b0d10 " + (shift + 40) + "px, rgba(11,13,16,.6) " + (shift + 170) + "px, rgba(11,13,16,0) " + (shift + 320) + "px)" }, q(t));
      tl.to("#vw", { y: shift, duration: 0.4, ease: "power3.out" }, q(t));
      tl.fromTo("#vid", { filter: "blur(0px) brightness(1) saturate(1)" }, { filter: "blur(16px) brightness(.5) saturate(.75)", duration: 0.4, ease: "power2.out" }, q(t));
      tl.fromTo("#shade", { opacity: 0 }, { opacity: 1, duration: 0.4 }, q(t));
    }
    function punch(t, s) { tl.to("#vw", { scale: s, duration: 0.25, ease: "power3.out" }, q(t)); }
    function bw(t0, t1) { tl.to("#vid", { filter: "grayscale(1) contrast(1.12)", duration: 0.1 }, q(t0)); tl.set("#vid", { filter: "none" }, q(t1)); }

    // 0-1.4 hook
    full(0, 0, 1.34, 1.16, 0.5); tl.to("#vw", { scale: 1.2, duration: 0.9, ease: "none" }, q(0.5));
    // 1.4-3.6 split-pop + TERMINAL monitor
    splitPop(1.4, D.cuts[0][2], "#sc1");
    show("#t1", 1.45, 0.3, { y: -20 });
    type("#a1", 1.5, 0.3); type("#a2", 1.6, 0.35); type("#a3", 2.84, 0.3);
    tl.to("#cur1", { opacity: 0, duration: 0.2, repeat: 3, yoyo: true, ease: "steps(1)" }, q(3.0));
    cut("#sc1", 3.6, 0);
    // 3.6-5.93 PIP + PAPER (kartu OpenAI distabilo)
    cut("#sc2", 3.6, 1); pipIn(3.6, 1, false); cut("#wm", 3.6, 0.92);
    show("#seri", 3.7, 0.3, { x: -30 });
    tl.fromTo("#paper", { opacity: 0, y: 120, rotation: 6 }, { opacity: 1, y: 0, rotation: -3, duration: 0.5, ease: "power3.out" }, q(3.8));
    tl.fromTo("#paper .hl", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.inOut" }, q(4.38));
    tl.to("#paper", { scale: 1.06, duration: 0.25, ease: "power3.out" }, q(5.24));
    cut("#sc2", 5.933, 0);
    // 5.93-8.9 TH
    full(5.933, 2, 1.0, 1.06);
    full(7.333, 3, 1.04, 1.06, 7.5); punch(7.52, 1.22); bw(7.52, 8.9);
    // 8.9-11.8 PIP + TERMINAL sandbox
    cut("#sc3", 8.9, 1); pipIn(8.9, 4, true, 1.1);
    show("#t2", 8.95, 0.3, { y: 30 });
    type("#s1", 9.0, 0.35); type("#s2", 9.38, 0.4); type("#s3", 10.18, 0.25); type("#s4", 10.62, 0.3); pop("#lock", 10.62);
    type("#s5", 11.1, 0.2);
    tl.to("#t2", { borderColor: "rgba(255,59,78,.9)", duration: 0.08, yoyo: true, repeat: 5 }, q(11.1));
    tl.fromTo("#t2", { x: 0 }, { x: 10, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, q(11.12));
    tl.to("#lock", { color: "#FF3B4E", rotation: 15, duration: 0.2 }, q(11.2));
    cut("#sc3", 11.8, 0);
    // 11.8-17.63 TH
    full(11.8, 5, 1.04, 1.1);
    full(13.067, 6, 1.02, 1.06, 13.1); punch(13.14, 1.16); tl.to("#vw", { scale: 1.2, duration: 2.5, ease: "none" }, q(13.4));
    full(15.933, 7, 1.04, 1.1);
    // 17.63-18.93 split-pop (satu shot saja)
    splitPop(17.633, D.cuts[1][2], "#sc_none");
    // 18.93-25.2 PIP: isometric -> stepper
    pipIn(18.933, 9, false); cut("#wm", 18.933, 0.92);
    cut("#sc4", 18.933, 1);
    [[1, 19.42], [2, 19.74], [3, 19.96]].forEach(function (p) {
      tl.fromTo("#ip" + p[0], { opacity: 0, y: -70 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, q(p[1]));
    });
    tl.to("#sc4", { opacity: 0, scale: 0.85, duration: 0.3, ease: "power2.in" }, q(20.2));
    cut("#sc5", 20.333, 1); pipSet(20.333, 10); pipSet(23.267, 11);
    tl.fromTo([".node", ".conn"], { opacity: 0 }, { opacity: 0.28, duration: 0.3, stagger: 0.04 }, q(20.35));
    function act(sel, t) { tl.to(sel, { opacity: 1, borderColor: "rgba(255,214,10,.6)", duration: 0.25 }, q(t)); tl.fromTo(sel + " .ic", { scale: 0.7 }, { scale: 1, duration: 0.3, ease: "back.out(2)" }, q(t)); }
    act("#n1", 20.72);
    tl.fromTo("#n1a", { opacity: 0 }, { opacity: 1, duration: 0.2 }, q(21.64)); tl.fromTo("#n1b", { opacity: 0 }, { opacity: 1, duration: 0.2 }, q(22.36));
    tl.to("#n1", { borderColor: "rgba(255,255,255,.14)", duration: 0.2 }, q(23.3));
    act("#n2", 23.44); tl.to("#n2", { borderColor: "rgba(255,59,78,.85)", duration: 0.12, yoyo: true, repeat: 3 }, q(24.22));
    cut("#sc5", 25.2, 0);
    // 25.2-27.6 TH
    full(25.2, 12, 1.04, 1.12);
    // 27.6-31.03 PIP stepper lanjut
    cut("#sc5", 27.6, 1); pipIn(27.6, 13, true, 1.05); pipSet(29.167, 14);
    tl.to("#n2", { borderColor: "rgba(255,255,255,.14)", duration: 0.2 }, q(27.6));
    act("#n3", 27.66); tl.to("#n3", { borderColor: "rgba(255,255,255,.14)", duration: 0.2 }, q(29.3));
    act("#n4", 29.44);
    tl.to("#n4 .ic", { rotation: 10, duration: 0.1, yoyo: true, repeat: 5, ease: "sine.inOut" }, q(30.16));
    cut("#sc5", 31.033, 0);
    // 31.03-34.13 TH
    full(31.033, 15, 1.06, 1.1);
    full(31.867, 16, 1.0, 1.04, 32.6); punch(32.7, 1.14);
    full(33.767, 17, 1.0, 1.02);
    // 34.13-41.6 PIP STAT
    cut("#sc6", 34.133, 1); pipIn(34.133, 18, true, 1.05); pipSet(36.033, 19); pipSet(39.667, 20);
    show("#simc", 34.2, 0.3, { y: -16 });
    show("#stA", 34.44, 0.3, { y: 30 }); show("#stArr", 35.3, 0.25, { x: -20 }); show("#stB", 35.5, 0.3, { y: 30 });
    tl.to(["#stA", "#stB", "#stArr"], { opacity: 0, y: -40, duration: 0.25, ease: "power2.in" }, q(36.6));
    show("#bar", 36.9, 0.3, { y: 20 }); tl.fromTo(".tick", { opacity: 0 }, { opacity: 1, duration: 0.2, stagger: 0.03 }, q(36.95));
    pop("#tdA", 37.0); pop("#tdB", 37.22); show("#tlB", 37.4, 0.28, { y: 16 });
    tl.fromTo("#bar i", { scaleX: 0 }, { scaleX: 1, duration: 2.2, ease: "power1.inOut" }, q(37.4));
    show("#big", 38.16, 0.3, { scale: 0.85 });
    var cnt = { v: 0 }, numEl = document.getElementById("num");
    tl.fromTo(cnt, { v: 0 }, { v: 30, duration: 1.0, ease: "power2.out", onUpdate: function () { numEl.textContent = "±" + Math.round(cnt.v); } }, q(38.3));
    show("#tlA", 40.06, 0.28, { y: 16 });
    tl.to("#tdA", { scale: 1.15, duration: 0.15, yoyo: true, repeat: 3 }, q(40.36));
    // 41.6-43.7 PIP peringatan (menutup subtitle bawaan Flow)
    tl.set(["#simc", "#big", "#bar", "#tdA", "#tdB", "#tlA", "#tlB", ".tick"], { opacity: 0 }, q(41.6));
    pipSet(41.6, 21); pipSet(42.267, 22);
    pop("#warn", 41.62, 0.35);
    cut("#sc6", 43.7, 0);
    // 43.7-51.37 TH
    full(43.7, 23, 1.38, 1.44); bw(45.78, 47.1);
    tl.set("#strike", { top: 1300 }, 0);
    tl.fromTo("#strike", { opacity: 1, scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out" }, q(46.6));
    hide("#strike", 46.98, 0.12);
    full(47.1, 24, 1.04, 1.08, 49.7); punch(49.74, 1.16);
    // 51.37-53.87 split-pop + VERSUS
    splitPop(51.367, D.cuts[2][2], "#sc7");
    [["#ev", "#evl", 52.64], ["#gd", "#gdl", 52.9]].forEach(function (a) { pop(a[0], a[2], 0.32); show(a[1], a[2] + 0.1, 0.2, { y: 10 }); });
    // 53.87-56.7 PIP VERSUS
    pipIn(53.867, 26, false); pipSet(55.167, 27); cut("#wm", 53.867, 0.92);
    tl.to(["#ev", "#evl", "#gd", "#gdl"], { y: "+=40", duration: 0.45, ease: "power3.inOut" }, q(53.867));
    tl.fromTo(["#vsL", "#vsR"], { opacity: 0 }, { opacity: 1, duration: 0.3 }, q(53.9));
    pop("#vsTxt", 54.06, 0.3); show("#p2", 54.3, 0.3, { y: 16 });
    tl.to("#vsL", { clipPath: "polygon(0px 0px, 900px 0px, 810px 1920px, 0px 1920px)", duration: 0.45, ease: "power3.in" }, q(55.32));
    tl.to("#vsR", { clipPath: "polygon(900px 0px, 1080px 0px, 1080px 1920px, 810px 1920px)", duration: 0.45, ease: "power3.in" }, q(55.32));
    tl.to("#ev", { x: 520, duration: 0.45, ease: "power3.in" }, q(55.32));
    tl.to("#gd", { background: "#3a3d44", color: "#FF3B4E", rotation: -14, y: "+=30", duration: 0.25, ease: "power2.out" }, q(55.77));
    tl.to("#gdl", { color: "#FF3B4E", duration: 0.2 }, q(55.86));
    tl.to("#vsTxt", { opacity: 0, duration: 0.15 }, q(55.4));
    cut("#sc7", 56.7, 0);
    // 56.7-59.1 TH + kartu A/B (CTA komentar visual) + save/follow
    full(56.7, 27, 1.08, 1.04, 57.2); tl.to("#vw", { scale: 1.08, duration: 1.9, ease: "none" }, q(57.2));
    show("#ab", 56.75, 0.35, { y: 30, scale: 0.95 });
"""

def main():
    pub = HERE / "public"
    for f in FONTS.values():
        shutil.copy(SK / "assets/fonts" / f, pub / "fonts" / f)
    shutil.copy(MONO, pub / "fonts/Mono.ttf")
    shutil.copy(LOGO, pub / "openai.png")
    html = U.page("V2", CSS, BODY, JS, {"locks": [d for _, d in LOCKS], "pip": PIP, "cuts": CUTS})
    (pub / "index.html").write_text(html, encoding="utf-8")
    print("ok", len(LOCKS), "lockups; sumber:", SRC_TXT)

main()
