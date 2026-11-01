# Generates public/index.html for "video 01" (AI & harga jualan) — HyperFrames motion graphics over plate.mp4.
# House style from talking-head/proyek/take; split panels fade into the footage (no hard seam line).
import json
from PIL import ImageFont

DUR = 36.36
W, H = 1080, 1920
FONT = {"black": "public/fonts/seguibl.ttf", "bold": "public/fonts/segoeuib.ttf", "serif": "public/fonts/georgiai.ttf"}

raw = json.load(open("../../mentah/video01/video 01.words.json", encoding="utf-8"))["words"]
words = []
for w in raw:
    t = w["word"]
    if words and t.startswith("-"):
        words[-1]["text"] += t
        words[-1]["end"] = w["end"]
    else:
        words.append({"text": t, "start": w["start"], "end": w["end"]})
assert words[55]["text"] == "rata-rata" and words[94]["text"] == "berikutnya.", [x["text"] for x in words[50:60]]

KEEP_CASE = {"AI", "AI,", "AI.", "AI?"}
def disp(i, style):
    t = words[i]["text"]
    if t not in KEEP_CASE:
        t = t.lower()
    t = t.replace(",", "")
    if style not in ("ser", "sery"):
        t = t.rstrip(".")
    return t

STY = {"sm": ("bold", 52, "sm"), "big": ("black", 124, "big"), "bigw": ("black", 124, "bigw"),
       "red": ("black", 136, "red"), "ser": ("serif", 100, "ser"), "sery": ("serif", 104, "sery")}

def fit(text, key, px, maxw=960):
    while px > 30:
        if ImageFont.truetype(FONT[key], px).getlength(text) <= maxw:
            return px
        px -= 2
    return px

def lockup(start, end, spec):
    lines = []
    for part in spec.split("|"):
        rng, style = part.strip().split(":")
        a, b = (rng.split("-") + [rng])[:2]
        idx = range(int(a), int(b) + 1)
        text = " ".join(disp(i, style) for i in idx)
        key, px, cls = STY[style]
        lines.append({"cls": cls, "px": fit(text, key, px),
                      "words": [{"t": words[i]["start"], "x": disp(i, style)} for i in idx]})
    return {"start": start, "end": end, "lines": lines}

LOCKUPS = [
    lockup(0.00, 2.85, "1-3:sm|4-6:big"),
    lockup(2.90, 3.66, "7-8:sery"),
    lockup(7.78, 9.08, "20-21:sm|22-23:red"),
    lockup(18.38, 19.68, "50-53:sm|54:big"),
    lockup(19.70, 21.24, "55-57:ser"),
    lockup(23.40, 25.08, "63-64:sm|65-66:big"),
    lockup(30.94, 32.86, "82-83:sm|84-85:big"),
    lockup(32.88, 34.72, "86-87:sm|88-90:big"),
    lockup(34.74, DUR, "91:big|92-94:ser"),
]

# single-word captions on the split-screen seam: (first word, last word, window start, window stop)
SEAM_HL = {12, 13, 14, 16, 17, 19, 27, 28, 30, 33, 34, 35, 36, 38, 39, 44, 45, 46, 48, 69, 70, 72, 73, 74, 75, 77, 81}
SEAM = []
for a, b, start, stop in [(9, 19, 3.70, 7.60), (24, 49, 9.10, 18.20), (67, 82, 25.10, 30.93)]:
    for i in range(a, b + 1):
        nxt = words[i + 1]["start"] if i < b else stop
        t = max(words[i]["start"], start)
        end = min(nxt, words[i]["end"] + 0.35, stop)
        SEAM.append({"t": t, "e": round(end, 3), "x": disp(i, "sm"), "hl": i in SEAM_HL})

BEHIND = {"jangan": fit("JANGAN", "black", 300, 1000), "kamu": fit("KAMU", "black", 360, 980)}

def svg(body, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
dot = lambda x, y: f'<circle cx="{x}" cy="{y}" r="4.5" fill="currentColor" stroke="none"/>'
ICON = {
    "basket": svg('<path d="M12 40h76l-9 42H21z"/><path d="M33 40l11-24M67 40L56 16M38 54v16M62 54v16M50 54v16"/>'),
    "flame": svg('<path d="M50 10c6 16 24 24 24 46a24 24 0 0 1-48 0c0-12 7-19 10-28 4 9 8 11 12 11-1-11-3-19 2-29z"/>'),
    "store": svg('<path d="M14 40l7-22h58l7 22z"/><path d="M20 40v42h60V40"/><path d="M42 82V60h16v22"/>'),
    "people": svg('<circle cx="36" cy="34" r="12"/><path d="M12 82c0-15 11-25 24-25s24 10 24 25"/><circle cx="69" cy="38" r="10"/><path d="M64 58c13-2 25 8 25 23"/>'),
    "pin": svg('<path d="M50 90S22 60 22 38a28 28 0 0 1 56 0c0 22-28 52-28 52z"/><circle cx="50" cy="38" r="10"/>'),
    "dice": svg('<rect x="16" y="16" width="68" height="68" rx="15"/>' + dot(34, 34) + dot(66, 34) + dot(50, 50) + dot(34, 66) + dot(66, 66)),
    "globe": svg('<circle cx="50" cy="50" r="34"/><path d="M16 50h68M50 16c-12 12-12 56 0 68M50 16c12 12 12 56 0 68"/>'),
    "bulb": svg('<path d="M37 66c0-11-15-17-15-35a28 28 0 0 1 56 0c0 18-15 24-15 35z"/><path d="M38 76h24M43 87h14"/>'),
    "calc": svg('<rect x="22" y="10" width="56" height="80" rx="11"/><rect x="32" y="20" width="36" height="16" rx="3"/>' + ''.join(dot(x, y) for x in (37, 50, 63) for y in (52, 66, 79))),
    "bell": svg('<path d="M26 70V46a24 24 0 0 1 48 0v24l8 8H18z"/><path d="M42 85a8 8 0 0 0 16 0"/>'),
    "down": svg('<path d="M50 12v70M22 56l28 28 28-28"/>').replace('stroke-width="6"', 'stroke-width="11"'),
    "up": svg('<path d="M50 88V18M22 44l28-28 28 28"/>').replace('stroke-width="6"', 'stroke-width="11"'),
    "check": svg('<circle cx="50" cy="50" r="38"/><path d="M33 51l12 12 22-25"/>'),
}

def lrow(n, icon, text):
    return f'<div class="row" id="p2-r{n}"><div class="tile">{ICON[icon]}</div><div class="rtext">{text}</div><div class="qb">?</div></div>'

def cchip(n, icon, text):
    return f'<div class="cc" id="p4-c{n}"><span class="ci">{ICON[icon]}</span><span class="ct">{text}</span><span class="ck">{ICON["check"]}</span></div>'

USERQ = ["Harga", "nasi", "kotak", "yang", "pas", "berapa?"]
DATA = {"lockups": LOCKUPS, "seam": SEAM, "userq": [words[i]["start"] for i in range(12, 18)]}

HTML = f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8" />
<style>
@font-face {{ font-family: "SegoeBlack"; src: url("fonts/seguibl.ttf") format("truetype"); font-display: block; }}
@font-face {{ font-family: "SegoeBold"; src: url("fonts/segoeuib.ttf") format("truetype"); font-display: block; }}
@font-face {{ font-family: "GeorgiaIt"; src: url("fonts/georgiai.ttf") format("truetype"); font-display: block; }}
:root {{ --y:#FFD60A; --r:#FF3B4E; --g:#3BE07F; --ink:#0B0D10; --w:#F6F5F1; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 100%; height: 100%; overflow: hidden; background: #000; font-family: "SegoeBold", sans-serif; color: var(--w); }}
#root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #000; }}
#video-wrap {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }}
#video-wrap video {{ width: 100%; height: 100%; object-fit: cover; }}
.ico {{ width: 100%; height: 100%; }}

.behind {{ position: absolute; left: 0; width: 1080px; text-align: center; font-family: "SegoeBlack"; line-height: 1; opacity: 0; }}
#b-jangan {{ top: 236px; font-size: {BEHIND["jangan"]}px; letter-spacing: -6px; color: var(--r); text-shadow: 0 0 60px rgba(255,59,78,.55), 0 10px 40px rgba(0,0,0,.4); }}
#b-kamu {{ top: 175px; font-size: {BEHIND["kamu"]}px; letter-spacing: -8px; color: var(--y); text-shadow: 0 0 60px rgba(255,214,10,.55), 0 10px 40px rgba(0,0,0,.4); }}

.lock {{ position: absolute; left: 0; top: 1060px; width: 1080px; height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
.line {{ display: flex; justify-content: center; white-space: nowrap; line-height: 1.02; }}
.wd {{ display: inline-block; margin: 0 .13em; opacity: 0; }}
.sm {{ font-family: "SegoeBold"; color: var(--w); text-shadow: 0 3px 14px rgba(0,0,0,.8); }}
.big {{ font-family: "SegoeBlack"; color: var(--y); letter-spacing: -.02em; text-shadow: 0 0 34px rgba(255,214,10,.45), 0 5px 20px rgba(0,0,0,.6); }}
.bigw {{ font-family: "SegoeBlack"; color: var(--w); letter-spacing: -.02em; text-shadow: 0 0 30px rgba(255,255,255,.28), 0 5px 20px rgba(0,0,0,.6); }}
.red {{ font-family: "SegoeBlack"; color: var(--r); letter-spacing: -.02em; text-shadow: 0 0 36px rgba(255,59,78,.5), 0 5px 20px rgba(0,0,0,.6); }}
.ser {{ font-family: "GeorgiaIt"; color: var(--w); text-shadow: 0 4px 18px rgba(0,0,0,.75); }}
.sery {{ font-family: "GeorgiaIt"; color: var(--y); text-shadow: 0 0 26px rgba(255,214,10,.4), 0 4px 18px rgba(0,0,0,.75); }}

/* split panel: solid to 780px, then a soft shade into the footage (no seam line) */
#panel {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1010px; overflow: hidden; clip-path: inset(0 0 100% 0);
  background: linear-gradient(to bottom, #0b0d10 0px, #0b0d10 780px, rgba(11,13,16,.82) 860px, rgba(11,13,16,.4) 940px, rgba(11,13,16,0) 1010px); }}
#panel .glow {{ position: absolute; left: 0; top: 0; width: 1080px; height: 820px; background: radial-gradient(ellipse at 50% 28%, rgba(255,255,255,.07) 0%, rgba(255,255,255,0) 65%); }}
#panel .grid {{ position: absolute; inset: 0; opacity: .5;
  background-image: linear-gradient(rgba(255,255,255,.07) 2px, rgba(255,255,255,0) 2px), linear-gradient(90deg, rgba(255,255,255,.07) 2px, rgba(255,255,255,0) 2px);
  background-size: 60px 60px; -webkit-mask-image: linear-gradient(to bottom, #000 0px, #000 680px, rgba(0,0,0,0) 900px); mask-image: linear-gradient(to bottom, #000 0px, #000 680px, rgba(0,0,0,0) 900px); }}
.scene {{ position: absolute; left: 0; top: 0; width: 1080px; height: 820px; opacity: 0; }}
.chips {{ position: absolute; left: 60px; top: 60px; display: flex; gap: 16px; }}
.chip {{ font-family: "SegoeBlack"; font-size: 30px; letter-spacing: 3px; padding: 10px 22px; border-radius: 999px; border: 3px solid var(--y); color: var(--y); opacity: 0; }}
.tile {{ width: 96px; height: 96px; border-radius: 24px; padding: 18px; color: var(--y); background: rgba(255,255,255,.07); border: 2px solid rgba(255,255,255,.16); flex: none; }}

.chat {{ position: absolute; left: 60px; top: 136px; width: 960px; height: 640px; border-radius: 34px; background: #15181d; border: 2px solid rgba(255,255,255,.12); opacity: 0; overflow: hidden; }}
.chat .bar {{ height: 64px; display: flex; align-items: center; gap: 12px; padding: 0 26px; border-bottom: 2px solid rgba(255,255,255,.08); font-size: 28px; color: rgba(246,245,241,.6); }}
.chat .bar i {{ width: 16px; height: 16px; border-radius: 50%; background: rgba(255,255,255,.25); display: inline-block; }}
.ub {{ position: absolute; right: 30px; top: 96px; max-width: 700px; padding: 22px 30px; border-radius: 30px 30px 8px 30px; background: var(--y); color: var(--ink); font-size: 46px; line-height: 1.2; opacity: 0; }}
.ub span {{ opacity: 0; }}
.ab {{ position: absolute; left: 30px; top: 300px; width: 800px; padding: 24px 32px; border-radius: 30px 30px 30px 8px; background: #F3F1EA; color: var(--ink); opacity: 0; }}
.ab .s {{ font-size: 40px; color: #3b3d42; }}
.ab .n {{ font-family: "SegoeBlack"; font-size: 76px; line-height: 1.05; opacity: 0; }}
.typing {{ position: absolute; left: 32px; top: 30px; display: flex; gap: 12px; }}
.typing i {{ width: 18px; height: 18px; border-radius: 50%; background: #8a8d93; display: inline-block; }}
.conf {{ position: absolute; left: 30px; top: 540px; display: flex; align-items: center; gap: 12px; padding: 12px 24px; border-radius: 999px; background: rgba(59,224,127,.14); border: 3px solid var(--g); color: var(--g); font-family: "SegoeBlack"; font-size: 34px; opacity: 0; }}
.conf span {{ width: 40px; height: 40px; }}
.ilus {{ position: absolute; right: 26px; bottom: 18px; font-size: 24px; letter-spacing: 3px; color: rgba(246,245,241,.4); }}

.ttl {{ position: absolute; left: 60px; top: 70px; display: flex; align-items: baseline; gap: 22px; opacity: 0; }}
.ttl .a {{ font-family: "SegoeBlack"; font-size: 140px; letter-spacing: -4px; line-height: 1; }}
.ttl .b {{ font-family: "GeorgiaIt"; font-size: 88px; color: var(--y); }}
.row {{ position: absolute; left: 60px; width: 960px; height: 104px; display: flex; align-items: center; gap: 28px; opacity: 0; }}
.rtext {{ font-size: 48px; flex: 1; }}
.qb {{ width: 70px; height: 70px; border-radius: 50%; background: var(--r); color: #fff; font-family: "SegoeBlack"; font-size: 50px; line-height: 70px; text-align: center; box-shadow: 0 0 24px rgba(255,59,78,.6); opacity: 0; }}
.ctr {{ position: absolute; left: 0; width: 1080px; text-align: center; opacity: 0; }}
.pinw {{ position: absolute; left: 430px; top: 70px; width: 220px; height: 220px; opacity: 0; }}
.pinw .tile {{ width: 220px; height: 220px; border-radius: 52px; padding: 44px; }}
.pinw .qb {{ position: absolute; right: -30px; top: -24px; width: 92px; height: 92px; line-height: 92px; font-size: 64px; }}

.cc {{ position: absolute; width: 470px; height: 92px; display: flex; align-items: center; gap: 18px; padding: 0 22px; border-radius: 22px; background: rgba(255,255,255,.07); border: 2px solid rgba(255,255,255,.16); opacity: 0; }}
.cc .ci {{ width: 54px; height: 54px; color: var(--y); flex: none; }}
.cc .ct {{ font-size: 40px; flex: 1; }}
.cc .ck {{ width: 50px; height: 50px; color: var(--g); }}
#p4-f {{ position: absolute; left: 60px; top: 360px; width: 960px; text-align: center; font-family: "GeorgiaIt"; font-size: 58px; opacity: 0; }}
#p4-res {{ position: absolute; left: 60px; top: 452px; width: 960px; height: 136px; border-radius: 28px; border: 5px solid var(--y); background: rgba(255,214,10,.10); text-align: center; font-family: "SegoeBlack"; font-size: 74px; line-height: 126px; color: var(--y); text-shadow: 0 0 30px rgba(255,214,10,.45); opacity: 0; }}
#p4-x {{ position: absolute; left: 60px; top: 630px; width: 960px; height: 104px; display: flex; align-items: center; gap: 22px; padding: 0 28px; border-radius: 26px; border: 4px dashed var(--y); font-size: 46px; opacity: 0; }}
#p4-x .qb {{ background: var(--y); color: var(--ink); box-shadow: 0 0 24px rgba(255,214,10,.6); opacity: 1; }}

.seam {{ position: absolute; left: 0; top: 846px; width: 1080px; text-align: center; font-family: "SegoeBlack"; font-size: 76px; line-height: 1; color: var(--w); text-shadow: 0 0 26px rgba(255,255,255,.3), 0 4px 18px rgba(0,0,0,.85); opacity: 0; }}
.seam.hl {{ color: var(--y); text-shadow: 0 0 30px rgba(255,214,10,.6), 0 4px 18px rgba(0,0,0,.85); }}

.card {{ position: absolute; inset: 0; opacity: 0; }}
#card-red {{ background: #E5243B; }}
.arow {{ position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; align-items: center; gap: 26px; opacity: 0; }}
.arow .ar {{ width: 150px; height: 150px; }}

.top {{ position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; opacity: 0; }}
#tag {{ top: 120px; }}
#tag .p {{ position: relative; font-family: "SegoeBlack"; font-size: 96px; color: var(--ink); background: var(--w); padding: 10px 46px 18px; border-radius: 26px; box-shadow: 0 20px 50px rgba(0,0,0,.45); }}
#tag .qb {{ position: absolute; right: -36px; top: -36px; width: 96px; height: 96px; line-height: 96px; font-size: 68px; }}
#guess {{ top: 70px; gap: 330px; }}
.gt {{ width: 170px; text-align: center; opacity: 0; }}
.gt .tile {{ width: 170px; height: 170px; border-radius: 40px; padding: 36px; background: rgba(11,13,16,.72); border: 3px solid rgba(255,214,10,.6); }}
.gt .lbl {{ margin-top: 10px; font-size: 38px; text-shadow: 0 3px 12px rgba(0,0,0,.85); }}
#bulb {{ top: 70px; }}
#bulb .bi {{ width: 250px; height: 250px; color: var(--y); filter: drop-shadow(0 0 34px rgba(255,214,10,.7)); }}
#calc {{ top: 90px; }}
#calc .tile {{ position: relative; width: 210px; height: 210px; border-radius: 48px; padding: 38px; background: rgba(11,13,16,.72); border: 3px solid rgba(255,214,10,.6); overflow: visible; }}
#calc .ck {{ position: absolute; right: -34px; top: -30px; width: 90px; height: 90px; color: var(--g); background: var(--ink); border-radius: 50%; }}
#follow {{ top: 170px; }}
#follow .c {{ display: flex; align-items: center; gap: 18px; font-family: "SegoeBlack"; font-size: 58px; letter-spacing: 4px; padding: 18px 46px 18px 32px; border-radius: 999px; background: var(--y); color: var(--ink); box-shadow: 0 0 44px rgba(255,214,10,.55); }}
#follow .c span {{ width: 64px; height: 64px; }}

#brand {{ position: absolute; left: 0; top: 1640px; width: 1080px; text-align: center; font-family: "SegoeBlack"; font-size: 40px; letter-spacing: 2px; color: var(--w); text-shadow: 0 3px 14px rgba(0,0,0,.75); opacity: .92; }}
#brand b {{ color: var(--y); font-weight: normal; }}
</style>
</head>
<body>
<div id="root" data-composition-id="video01" data-start="0" data-duration="{DUR}" data-fps="30" data-width="{W}" data-height="{H}">

  <div id="video-wrap">
    <video id="plate" src="plate.mp4" playsinline data-has-audio="true" data-start="0" data-duration="{DUR}" data-track-index="0"></video>
  </div>

  <div id="b-jangan" class="behind">JANGAN</div>
  <div id="b-kamu" class="behind">KAMU</div>

  <div id="panel"><div class="glow"></div><div class="grid"></div>
    <div class="scene" id="p1">
      <div class="chips"><div class="chip" id="p1-c">COBA TANYA AI</div></div>
      <div class="chat" id="p1-chat">
        <div class="bar"><i></i><i></i><i></i>&nbsp;Chat AI</div>
        <div class="ub" id="p1-ub">{" ".join(f'<span id="p1-u{k}">{w}</span>' for k, w in enumerate(USERQ))}</div>
        <div class="ab" id="p1-ab"><div class="typing" id="p1-ty"><i></i><i></i><i></i></div>
          <div class="s" id="p1-s" style="opacity:0">Harga yang pas sekitar</div><div class="n" id="p1-n">Rp25.000/kotak</div></div>
        <div class="conf" id="p1-conf"><span>{ICON["check"]}</span>terdengar meyakinkan</div>
        <div class="ilus">CONTOH ILUSTRASI</div>
      </div>
    </div>
    <div class="scene" id="p2">
      <div class="ttl" id="p2-t"><span class="a">AI</span><span class="b">nggak tahu&#8230;</span></div>
      <div style="position:absolute;left:0;top:290px">{lrow(1, "basket", "Harga bahan di pasar")}</div>
      <div style="position:absolute;left:0;top:410px">{lrow(2, "flame", "Ongkos gas")}</div>
      <div style="position:absolute;left:0;top:530px">{lrow(3, "store", "Sewa tempat")}</div>
      <div style="position:absolute;left:0;top:650px">{lrow(4, "people", "Gaji karyawan")}</div>
    </div>
    <div class="scene" id="p3">
      <div class="pinw" id="p3-pin"><div class="tile">{ICON["pin"]}</div><div class="qb" id="p3-q">?</div></div>
      <div class="ctr" id="p3-t1" style="top:350px;font-family:'SegoeBlack';font-size:150px;line-height:1;color:var(--y);text-shadow:0 0 40px rgba(255,214,10,.5)">DAYA BELI</div>
      <div class="ctr" id="p3-t2" style="top:530px;font-size:58px">pelanggan di daerahmu</div>
    </div>
    <div class="scene" id="p4">
      <div class="chips"><div class="chip" id="p4-chip">SURUH AI HITUNG</div></div>
      <div style="position:absolute;left:60px;top:140px">{cchip(1, "basket", "Bahan")}</div>
      <div style="position:absolute;left:550px;top:140px">{cchip(2, "flame", "Gas")}</div>
      <div style="position:absolute;left:60px;top:246px">{cchip(3, "store", "Sewa")}</div>
      <div style="position:absolute;left:550px;top:246px">{cchip(4, "people", "Gaji")}</div>
      <div id="p4-f">total biaya &#247; jumlah porsi</div>
      <div id="p4-res">= MODAL PER PORSI</div>
      <div id="p4-x"><div class="qb">!</div>+ biaya yang mungkin kamu lupa</div>
    </div>
  </div>

  <div id="tag" class="top"><div class="p">Rp25.000<div class="qb" id="tag-q" style="opacity:0">?</div></div></div>
  <div id="guess" class="top">
    <div class="gt" id="g1"><div class="tile">{ICON["dice"]}</div><div class="lbl">tebakan</div></div>
    <div class="gt" id="g2"><div class="tile">{ICON["globe"]}</div><div class="lbl">internet</div></div>
  </div>
  <div id="bulb" class="top"><div class="bi">{ICON["bulb"]}</div></div>
  <div id="calc" class="top"><div class="tile" style="color:var(--y)">{ICON["calc"]}<span class="ck" id="calc-ck" style="opacity:0">{ICON["check"]}</span></div></div>
  <div id="follow" class="top"><div class="c"><span>{ICON["bell"]}</span>FOLLOW</div></div>

  <div id="captions"></div>

  <div class="card" id="card-red">
    <div class="ctr" id="r1" style="top:430px;font-size:66px">bisa bikin</div>
    <div class="arow" id="r2" style="top:520px"><span style="font-family:'SegoeBlack';font-size:290px;line-height:1">RUGI</span><span class="ar" style="color:var(--ink)">{ICON["down"]}</span></div>
    <div class="ctr" id="r3" style="top:930px;font-size:66px">bisa</div>
    <div class="arow" id="r4" style="top:1020px"><span style="font-family:'SegoeBlack';font-size:124px;line-height:1;color:var(--ink)">KEMAHALAN</span><span class="ar" style="width:120px;height:120px">{ICON["up"]}</span></div>
  </div>

  <div id="brand">Endrich<b>Tech</b></div>

  <script src="vendor/gsap.min.js"></script>
  <script>
  (function () {{
    var D = {json.dumps(DATA, ensure_ascii=False)};
    var FPS = 30;
    function q(t) {{ return Math.round(t * FPS) / FPS; }}
    var tl = gsap.timeline({{ paused: true }});
    function $(s) {{ return document.querySelector(s); }}
    function show(sel, t, d, from) {{
      tl.fromTo(sel, Object.assign({{ opacity: 0 }}, from || {{ y: 30 }}), {{ opacity: 1, y: 0, x: 0, scale: 1, filter: "blur(0px)", duration: d || 0.3, ease: "power3.out" }}, q(t));
    }}
    function pop(sel, t, d) {{ tl.fromTo(sel, {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: d || 0.32, ease: "back.out(2)" }}, q(t)); }}
    function hide(sel, t, d) {{ tl.to(sel, {{ opacity: 0, duration: d || 0.15, ease: "power2.in" }}, q(t)); }}
    function cut(sel, t, v) {{ tl.set(sel, {{ opacity: v }}, q(t)); }}

    // caption lockups (ids prefixed "cap" — never reuse generic ids)
    var host = $("#captions");
    D.lockups.forEach(function (L, li) {{
      var box = document.createElement("div"); box.className = "lock"; box.id = "cap" + li;
      L.lines.forEach(function (ln) {{
        var row = document.createElement("div"); row.className = "line " + ln.cls; row.style.fontSize = ln.px + "px";
        ln.words.forEach(function (w) {{
          var s = document.createElement("span"); s.className = "wd"; s.textContent = w.x; row.appendChild(s);
          tl.fromTo(s, {{ opacity: 0, y: 26, scale: 0.92, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.22, ease: "power3.out" }}, q(Math.max(w.t, L.start)));
        }});
        box.appendChild(row);
      }});
      host.appendChild(box);
      tl.to(box, {{ opacity: 0, duration: 0.12, ease: "power2.in" }}, q(L.end - 0.12));
    }});
    // seam captions — pop clamped so it always finishes before the hide
    D.seam.forEach(function (s) {{
      var e = document.createElement("div"); e.className = "seam" + (s.hl ? " hl" : ""); e.textContent = s.x; host.appendChild(e);
      var a = q(s.t), b = q(s.e), d = Math.min(0.14, b - a - 1 / FPS);
      if (d > 0.03) tl.fromTo(e, {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: d, ease: "back.out(2.5)" }}, a);
      else tl.set(e, {{ opacity: 1 }}, a);
      tl.set(e, {{ opacity: 0 }}, b);
    }});

    // behind-head giants (subject matte composited over them after render)
    tl.fromTo("#b-jangan", {{ opacity: 1, scale: 1.14 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }}, 0);
    tl.to("#b-jangan", {{ scale: 1.05, duration: 2.2, ease: "none" }}, q(0.45));
    hide("#b-jangan", 2.70, 0.13);
    tl.fromTo("#b-kamu", {{ opacity: 0, scale: 1.3, filter: "blur(24px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "power3.out" }}, q(33.77));
    tl.to("#b-kamu", {{ scale: 1.05, duration: 0.65, ease: "none" }}, q(34.07));
    cut("#b-kamu", 34.72, 0);

    // split choreography — the video slides down under the shaded panel (transform y, not top)
    var SHIFT = 520;
    function splitIn(t) {{
      tl.to("#video-wrap", {{ y: SHIFT, duration: 0.42, ease: "power3.inOut" }}, q(t));
      tl.fromTo("#panel", {{ clipPath: "inset(0 0 100% 0)" }}, {{ clipPath: "inset(0 0 0% 0)", duration: 0.42, ease: "power3.inOut" }}, q(t));
    }}
    function splitOut(t, d) {{
      tl.to("#video-wrap", {{ y: 0, duration: d, ease: "power3.inOut" }}, q(t));
      tl.to("#panel", {{ clipPath: "inset(0 0 100% 0)", duration: d, ease: "power3.inOut" }}, q(t));
    }}
    function splitCut(t) {{ tl.set("#video-wrap", {{ y: 0 }}, q(t)); tl.set("#panel", {{ clipPath: "inset(0 0 100% 0)" }}, q(t)); }}

    // A: chat mock (3.67–7.78)
    splitIn({110/30:.4f}); cut("#p1", {110/30:.4f}, 1);
    show("#p1-c", 3.75); show("#p1-chat", 3.95, 0.35, {{ y: 40 }});
    cut("#p1-ub", 4.72, 1);
    D.userq.forEach(function (t, k) {{ show("#p1-u" + k, t, 0.15, {{ y: 8 }}); }});
    show("#p1-ab", 6.10, 0.25, {{ y: 20 }});
    tl.to("#p1-ty i", {{ y: -10, duration: 0.14, yoyo: true, repeat: 1, stagger: 0.07, ease: "sine.inOut" }}, q(6.18));
    cut("#p1-ty", 6.52, 0); show("#p1-s", 6.52, 0.2, {{ y: 10 }});
    tl.fromTo("#p1-n", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, q(6.62));
    pop("#p1-conf", 7.04, 0.3);
    splitOut(7.50, 0.28); cut("#p1", 7.78, 0);

    // B&W beat: floating price tag questioned
    show("#tag", 7.82, 0.3, {{ y: -30, scale: 0.8 }});
    pop("#tag-q", 8.48, 0.3);
    hide("#tag", 8.95, 0.12);

    // B: what AI doesn't know (9.1–18.2)
    splitIn({273/30:.4f}); cut("#p2", {273/30:.4f}, 1);
    show("#p2-t", 9.25, 0.35, {{ x: -40 }});
    [[1, 10.16], [2, 11.90], [3, 12.92], [4, 13.92]].forEach(function (r) {{
      show("#p2-r" + r[0], r[1], 0.32, {{ x: -60 }});
      pop("#p2-r" + r[0] + " .qb", r[1] + 0.3, 0.28);
    }});
    tl.to("#p2", {{ opacity: 0, x: -80, duration: 0.22, ease: "power2.in" }}, q(14.95));
    tl.fromTo("#p3", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 0.28, ease: "power3.out" }}, q(15.12));
    pop("#p3-pin", 15.16, 0.35);
    show("#p3-t1", 16.06, 0.3, {{ scale: 1.25 }}); show("#p3-t2", 16.46, 0.25, {{ y: 16 }});
    pop("#p3-q", 16.92, 0.3);
    tl.to("#p3-q", {{ scale: 1.15, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, q(17.25));
    splitCut({546/30:.4f}); cut("#p3", {546/30:.4f}, 0);

    // guess + internet tiles above the head
    tl.set("#guess", {{ opacity: 1 }}, q(19.26));
    pop("#g1", 19.26); pop("#g2", 20.24);
    hide("#guess", 21.10, 0.12);

    // red card: rugi / kemahalan (hard cuts)
    cut("#card-red", 21.26, 1);
    show("#r1", 21.30, 0.2, {{ y: 16 }});
    tl.fromTo("#r2", {{ opacity: 0, scale: 1.35 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }}, q(21.92));
    show("#r3", 22.42, 0.15, {{ y: 12 }});
    tl.fromTo("#r4", {{ opacity: 0, scale: 1.35 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }}, q(22.58));
    cut("#card-red", 23.36, 0);

    // "gunanya apa?" bulb
    tl.fromTo("#bulb", {{ opacity: 0, scale: 0.4, rotation: -12 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2.2)" }}, q(24.16));
    hide("#bulb", 24.98, 0.1);

    // C: let AI do the math (25.1–30.93)
    splitIn(25.10); cut("#p4", 25.10, 1);
    show("#p4-chip", 25.20);
    [[1, 25.26], [2, 25.64], [3, 25.80], [4, 26.04]].forEach(function (c) {{
      pop("#p4-c" + c[0], c[1], 0.28); pop("#p4-c" + c[0] + " .ck", c[1] + 0.22, 0.25);
    }});
    show("#p4-f", 27.22, 0.3, {{ y: 16, filter: "blur(8px)" }});
    pop("#p4-res", 27.50, 0.35);
    tl.to("#p4-res", {{ scale: 1.04, duration: 0.2, yoyo: true, repeat: 1, ease: "sine.inOut" }}, q(28.10));
    show("#p4-x", 29.06, 0.3, {{ x: -60 }});
    splitCut({928/30:.4f}); cut("#p4", {928/30:.4f}, 0);

    // calculator approved, then follow CTA
    pop("#calc", 31.66, 0.32); pop("#calc-ck", 32.06, 0.28);
    hide("#calc", 32.74, 0.1);
    tl.fromTo("#follow", {{ opacity: 0, y: -30, scale: 0.8 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(2)" }}, q(34.76));
    tl.to("#follow .c", {{ scale: 1.06, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, q(35.2));

    window.__timelines["video01"] = tl;
  }})();
  </script>
</div>
</body>
</html>
'''
open("public/index.html", "w", encoding="utf-8").write(HTML)
print("lockups:", len(LOCKUPS), "seam words:", len(SEAM), "behind px:", BEHIND)
for L in LOCKUPS:
    print(f'{L["start"]:5.2f}', " / ".join(f'{" ".join(w["x"] for w in ln["words"])} [{ln["cls"]} {ln["px"]}]' for ln in L["lines"]))
