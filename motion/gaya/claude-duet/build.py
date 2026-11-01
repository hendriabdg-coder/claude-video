# "Claude Duet" explainer — first video in the SIGNAL style (merged from ref-motion-2..5): charcoal base + one lime
# accent, cream "paper" cards, series HUD (tag, frame counter, progress bar, chapter stepper), data shown as objects
# (phone notifications, connector chips, approval card, status receipt), typed comment + Follow click ending.
# No kinetic subtitles (creator's rule). VO = Endrich clone, eleven_v4, scene 1 from vo_open2.
import json
import subprocess
from pathlib import Path
from PIL import ImageFont

HERE = Path(__file__).resolve().parent
VO = HERE / "vo-sumber" / "vo_final"
W, H, GAP = 1080, 1920, 0.3
F_BLACK = str(HERE / "public" / "fonts" / "InterDisplay-Black.ttf")

WORDS, off = [], 0.0
for n in range(1, 6):
    d = json.loads((VO / f"scene_{n:02d}.json").read_text(encoding="utf-8"))
    WORDS += [{"x": w["word"], "t": round(off + w["start"], 3)} for w in d["words"]]
    off += float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                          "csv=p=0", str(VO / f"scene_{n:02d}.mp3")])) + GAP
DUR = round(off - GAP + 0.6, 2)
T = lambda i: WORDS[i]["t"]
assert WORDS[22]["x"] == "Claude" and WORDS[85]["x"] == "trading" and WORDS[133]["x"] == "komentar.", WORDS[20:24]


def fit(text, px, maxw=930):
    while px > 30 and ImageFont.truetype(F_BLACK, px).getlength(text) + len(text) * px * 0.01 > maxw:
        px -= 2
    return px

def head(hid, text, top, px, accent=(), left=72):
    """Heavy uppercase lines; words listed in `accent` turn lime. Letters stagger in (SIGNAL keeps the sweep)."""
    lines = text.split("|")
    size = min(fit(l, px) for l in lines)
    rows = []
    for l in lines:
        spans = []
        for wi, w in enumerate(l.split(" ")):
            cls = "ch acc" if w.strip(".,!?:") in accent else "ch"
            spans.append("".join(f'<span class="{cls}">{c}</span>' for c in w))
        rows.append('<div class="hr">' + '<span class="sp"> </span>'.join(spans) + "</div>")
    return f'<div class="head" id="{hid}" style="top:{top}px;left:{left}px;font-size:{size}px">{"".join(rows)}</div>'

def lead(lid, text, top, left=72, px=44):
    return f'<div class="lead" id="{lid}" style="top:{top}px;left:{left}px;font-size:{px}px">{text}</div>'

def mono(mid, text, top, left=72, extra=""):
    return f'<div class="mono" id="{mid}" style="top:{top}px;left:{left}px;{extra}">{text}</div>'

def svg(body, sw=6):
    return (f'<svg class="ico" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>')

ICON = {
    "mail": svg('<rect x="12" y="22" width="76" height="56" rx="8"/><path d="M14 26l36 28 36-28"/>'),
    "cal": svg('<rect x="14" y="20" width="72" height="66" rx="10"/><path d="M14 40h72M34 10v20M66 10v20"/>'),
    "pen": svg('<path d="M20 80l8-26 40-40 18 18-40 40z"/><path d="M60 22l18 18"/>'),
    "bell": svg('<path d="M26 70V46a24 24 0 0 1 48 0v24l8 8H18z"/><path d="M42 85a8 8 0 0 0 16 0"/>'),
    "cloud": svg('<path d="M30 74h44a18 18 0 0 0 0-36 26 26 0 0 0-50 6 15 15 0 0 0 6 30z"/>'),
    "chat": svg('<path d="M14 20h72v48H44L26 84V68H14z"/>'),
    "bolt": svg('<path d="M56 8L22 56h26l-6 36 36-50H52z"/>'),
    "lock": svg('<rect x="20" y="44" width="60" height="44" rx="10"/><path d="M32 44V32a18 18 0 0 1 36 0v12"/>'),
    "check": svg('<path d="M24 52l17 17 35-38"/>', 11),
    "cross": svg('<path d="M28 28l44 44M72 28L28 72"/>', 11),
    "send": svg('<path d="M12 50l76-36-20 72-16-28z"/><path d="M52 58L88 14"/>'),
    "card": svg('<rect x="10" y="24" width="80" height="54" rx="8"/><path d="M10 40h80M22 62h18"/>'),
    "sign": svg('<path d="M14 72c14-30 22-30 26-10s10 10 16-8 12-8 16 4M14 84h72"/>'),
    "trash": svg('<path d="M20 28h60M40 28V18h20v10M26 28l4 58h40l4-58"/>'),
    "chart": svg('<path d="M14 82h72M24 70V48M44 70V30M64 70V54M84 70V20"/>', 7),
    "bank": svg('<path d="M12 40L50 16l38 24zM20 44v30M40 44v30M60 44v30M80 44v30M12 82h76"/>'),
    "pin": svg('<path d="M50 90S22 60 22 38a28 28 0 0 1 56 0c0 22-28 52-28 52z"/><circle cx="50" cy="38" r="10"/>'),
    "radar": svg('<circle cx="50" cy="50" r="38"/><circle cx="50" cy="50" r="22"/><path d="M50 50L82 30"/>', 5),
}
CURSOR = ('<svg viewBox="0 0 40 40" class="ico"><path d="M6 4l26 14-12 3-5 12z" fill="#F2EEE3" stroke="#121314" '
          'stroke-width="2.5" stroke-linejoin="round"/></svg>')

def notif(nid, icon, title, sub, top):
    return (f'<div class="notif" id="{nid}" style="top:{top}px"><span class="ni">{ICON[icon]}</span>'
            f'<div><b>{title}</b><em>{sub}</em></div><span class="nt">sekarang</span></div>')

def chip(cid, icon, text, extra=""):
    return f'<div class="chip" id="{cid}" style="{extra}"><span class="ci">{ICON[icon]}</span>{text}</div>'

S = {"s1": (0.0, T(30) - 0.05), "s2": (T(30) - 0.05, T(56) - 0.05), "s3": (T(56) - 0.05, T(91) - 0.6),
     "s4": (T(91) - 0.6, T(114) - 0.05), "s5": (T(114) - 0.05, DUR)}
DATA = {"S": S, "T": {i: w["t"] for i, w in enumerate(WORDS)}, "DUR": DUR}

HTML = f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8" />
<style>
@font-face {{ font-family: "IDBlack"; src: url("fonts/InterDisplay-Black.ttf") format("truetype"); font-display: block; }}
@font-face {{ font-family: "IDBold"; src: url("fonts/InterDisplay-Bold.ttf") format("truetype"); font-display: block; }}
@font-face {{ font-family: "IDSemi"; src: url("fonts/InterDisplay-SemiBold.ttf") format("truetype"); font-display: block; }}
@font-face {{ font-family: "IDItal"; src: url("fonts/InterDisplay-SemiBoldItalic.ttf") format("truetype"); font-display: block; }}
:root {{ --bg:#121314; --panel:#1B1D1F; --line:rgba(255,255,255,.10); --lime:#C6F432; --cream:#F2EEE3; --ink:#121314; --mute:rgba(242,238,227,.55); }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 100%; height: 100%; overflow: hidden; background: var(--bg); color: var(--cream); font-family: "IDSemi", sans-serif; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: var(--bg); }}
.ico {{ width: 100%; height: 100%; display: block; }}
#bg {{ position: absolute; inset: 0; background: radial-gradient(ellipse 70% 45% at 50% 38%, rgba(198,244,50,.07) 0%, rgba(198,244,50,0) 70%), radial-gradient(ellipse 90% 60% at 50% 110%, rgba(80,90,110,.25) 0%, rgba(0,0,0,0) 70%); }}
#grain {{ position: absolute; inset: 0; opacity: .5; background-image: radial-gradient(rgba(255,255,255,.035) 1px, transparent 1px); background-size: 6px 6px; }}
#cam {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
.scene {{ position: absolute; inset: 0; opacity: 0; }}

/* HUD */
#hud {{ position: absolute; left: 0; top: 0; width: 1080px; height: 340px; }}
#prog {{ position: absolute; left: 0; top: 0; height: 6px; width: 1080px; background: var(--lime); transform-origin: left; transform: scaleX(0); }}
#tag {{ position: absolute; left: 60px; top: 210px; display: flex; align-items: center; gap: 12px; font-family: Consolas, monospace; font-size: 24px; letter-spacing: .18em; color: var(--cream); }}
#tag i {{ width: 12px; height: 12px; border-radius: 50%; background: var(--lime); box-shadow: 0 0 10px var(--lime); display: inline-block; }}
#frame {{ position: absolute; right: 150px; top: 210px; font-family: Consolas, monospace; font-size: 24px; letter-spacing: .18em; color: var(--mute); }}
#steps {{ position: absolute; left: 60px; top: 262px; display: flex; gap: 10px; }}
.st {{ font-family: Consolas, monospace; font-size: 20px; letter-spacing: .12em; padding: 6px 12px; border-radius: 8px; border: 1px solid var(--line); color: var(--mute); }}
.st.on {{ color: var(--ink); background: var(--lime); border-color: var(--lime); }}

.head {{ position: absolute; font-family: "IDBlack"; line-height: 1.0; letter-spacing: -.01em; text-transform: uppercase; color: var(--cream); white-space: nowrap; }}
.head .hr {{ display: block; }}
.head .ch {{ display: inline-block; opacity: 0; }}
.head .acc {{ color: var(--lime); }}
.lead {{ position: absolute; font-family: "IDItal"; color: var(--mute); opacity: 0; white-space: nowrap; }}
.mono {{ position: absolute; font-family: Consolas, monospace; font-size: 24px; letter-spacing: .16em; text-transform: uppercase; color: var(--mute); opacity: 0; white-space: nowrap; }}
.sim {{ position: absolute; right: 150px; bottom: 300px; font-family: Consolas, monospace; font-size: 20px; letter-spacing: .2em; color: rgba(242,238,227,.35); opacity: 0; }}

/* phone + notifications */
#phone {{ position: absolute; left: 270px; top: 600px; width: 540px; height: 860px; border-radius: 64px; background: #0B0C0D; border: 3px solid rgba(255,255,255,.14); box-shadow: 0 50px 120px rgba(0,0,0,.6); opacity: 0; overflow: hidden; }}
#phone .clk {{ position: absolute; left: 0; width: 100%; top: 80px; text-align: center; font-family: "IDBlack"; font-size: 120px; color: var(--cream); }}
#phone .dt {{ position: absolute; left: 0; width: 100%; top: 220px; text-align: center; font-size: 30px; color: var(--mute); }}
#phone .bell {{ position: absolute; left: 230px; top: 290px; width: 80px; height: 80px; color: var(--lime); }}
.notif {{ position: absolute; left: 24px; width: 492px; height: 120px; border-radius: 26px; background: rgba(242,238,227,.08); border: 1px solid var(--line); display: flex; align-items: center; gap: 18px; padding: 0 22px; opacity: 0; }}
.notif .ni {{ width: 56px; height: 56px; padding: 12px; border-radius: 16px; background: var(--lime); color: var(--ink); flex: none; }}
.notif b {{ display: block; font-family: "IDBold"; font-weight: normal; font-size: 30px; color: var(--cream); }}
.notif em {{ display: block; font-style: normal; font-size: 22px; color: var(--mute); margin-top: 4px; }}
.notif .nt {{ position: absolute; right: 20px; top: 16px; font-size: 18px; color: var(--mute); }}

/* cream paper card */
.paper {{ position: absolute; background: var(--cream); color: var(--ink); border-radius: 22px; box-shadow: 0 40px 90px rgba(0,0,0,.55); opacity: 0; }}
#title {{ left: 90px; top: 660px; width: 900px; height: 470px; padding: 50px; }}
#title .k {{ font-family: Consolas, monospace; font-size: 24px; letter-spacing: .2em; color: rgba(18,19,20,.55); }}
#title .n {{ font-family: "IDBlack"; font-size: 140px; line-height: .95; margin-top: 26px; }}
#title .n span {{ background: var(--lime); padding: 0 14px; border-radius: 12px; }}
#title .d {{ position: absolute; left: 50px; bottom: 46px; display: flex; gap: 12px; }}
#title .d i {{ font-style: normal; font-family: Consolas, monospace; font-size: 22px; letter-spacing: .14em; padding: 8px 14px; border-radius: 8px; border: 2px solid var(--ink); opacity: 0; }}

/* chatbot vs duet */
.vs {{ position: absolute; top: 640px; width: 440px; height: 520px; border-radius: 28px; padding: 40px 36px; opacity: 0; }}
#vs1 {{ left: 70px; background: var(--panel); border: 1px solid var(--line); }}
#vs2 {{ left: 570px; background: var(--lime); color: var(--ink); }}
.vs .vk {{ font-family: Consolas, monospace; font-size: 22px; letter-spacing: .2em; opacity: .7; }}
.vs .vt {{ font-family: "IDBlack"; font-size: 64px; line-height: 1.0; margin-top: 18px; }}
.vs .vi {{ width: 110px; height: 110px; margin-top: 50px; }}
.vs .vd {{ font-size: 32px; margin-top: 30px; line-height: 1.25; }}
#typing {{ display: flex; gap: 10px; margin-top: 16px; }}
#typing i {{ width: 16px; height: 16px; border-radius: 50%; background: var(--mute); display: inline-block; opacity: .3; }}

/* cloud hub + connectors */
#hub {{ position: absolute; left: 400px; top: 700px; width: 280px; height: 280px; border-radius: 50%; background: var(--panel); border: 2px solid var(--lime); box-shadow: 0 0 60px rgba(198,244,50,.25); padding: 70px; color: var(--lime); opacity: 0; }}
#hub .lbl {{ position: absolute; left: 0; width: 280px; bottom: -60px; text-align: center; font-family: Consolas, monospace; font-size: 24px; letter-spacing: .2em; color: var(--cream); }}
#ring {{ position: absolute; left: 340px; top: 640px; width: 400px; height: 400px; border-radius: 50%; border: 2px dashed rgba(198,244,50,.4); opacity: 0; }}
.chip {{ position: absolute; display: flex; align-items: center; gap: 14px; padding: 16px 26px 16px 18px; border-radius: 999px; background: var(--panel); border: 1px solid var(--line); font-family: "IDBold"; font-size: 36px; opacity: 0; white-space: nowrap; }}
.chip .ci {{ width: 44px; height: 44px; color: var(--lime); }}
#alert {{ position: absolute; left: 140px; top: 1260px; width: 800px; opacity: 0; }}
#alert .notif {{ position: relative; left: 0; width: 800px; height: 130px; opacity: 1; background: rgba(198,244,50,.12); border-color: rgba(198,244,50,.5); }}

/* rules */
.act {{ position: absolute; width: 440px; height: 120px; border-radius: 22px; background: var(--panel); border: 1px solid var(--line); display: flex; align-items: center; gap: 20px; padding: 0 26px; font-family: "IDBlack"; font-size: 40px; opacity: 0; }}
.act .ai {{ width: 56px; height: 56px; color: var(--cream); flex: none; }}
.act .lk {{ position: absolute; right: 22px; width: 44px; height: 44px; color: var(--lime); opacity: 0; }}
#ask {{ left: 110px; top: 1060px; width: 860px; height: 330px; padding: 40px 44px; }}
#ask .q {{ font-family: "IDBlack"; font-size: 52px; line-height: 1.1; }}
#ask .q em {{ font-style: normal; display: block; font-family: "IDSemi"; font-size: 28px; color: rgba(18,19,20,.6); margin-top: 10px; }}
#ask .btns {{ position: absolute; left: 44px; bottom: 40px; display: flex; gap: 18px; }}
#ask .btns b {{ font-family: "IDBlack"; font-weight: normal; font-size: 36px; padding: 16px 38px; border-radius: 16px; }}
#ask .yes {{ background: var(--ink); color: var(--lime); }}
#ask .no {{ border: 3px solid var(--ink); }}
.cur {{ position: absolute; width: 64px; height: 64px; opacity: 0; filter: drop-shadow(0 6px 10px rgba(0,0,0,.6)); }}
.deny {{ position: absolute; left: 110px; width: 860px; height: 130px; border-radius: 22px; background: var(--panel); border: 1px solid var(--line); display: flex; align-items: center; gap: 24px; padding: 0 30px; font-family: "IDBlack"; font-size: 46px; opacity: 0; }}
.deny .di {{ width: 64px; height: 64px; color: var(--cream); flex: none; }}
.deny .strike {{ position: absolute; left: 120px; right: 200px; top: 50%; height: 6px; background: var(--cream); transform-origin: left; transform: scaleX(0); }}
.deny .x {{ position: absolute; right: 30px; width: 60px; height: 60px; color: var(--lime); opacity: 0; }}
.stampc {{ position: absolute; left: 110px; font-family: "IDBlack"; font-size: 54px; letter-spacing: .04em; padding: 10px 26px; border: 5px solid var(--lime); color: var(--lime); border-radius: 14px; opacity: 0; white-space: nowrap; transform-origin: left center; }}

/* receipt */
#rcpt {{ left: 150px; top: 520px; width: 780px; padding: 46px 50px 60px; border-radius: 6px; }}
#rcpt:after {{ content: ""; position: absolute; left: 0; right: 0; bottom: -18px; height: 20px; background: linear-gradient(-45deg, transparent 12px, var(--cream) 0) 0 0/24px 20px, linear-gradient(45deg, transparent 12px, var(--cream) 0) 0 0/24px 20px; }}
#rcpt .rh {{ text-align: center; font-family: Consolas, monospace; font-size: 26px; letter-spacing: .22em; color: rgba(18,19,20,.6); padding-bottom: 22px; border-bottom: 2px dashed rgba(18,19,20,.3); }}
.rl {{ display: flex; justify-content: space-between; align-items: baseline; font-size: 36px; padding: 18px 0; border-bottom: 1px dashed rgba(18,19,20,.2); opacity: .12; }}
.rl b {{ font-family: "IDBlack"; font-weight: normal; }}
.rl b.hl {{ background: var(--lime); padding: 2px 12px; border-radius: 8px; }}
.rl.no b {{ color: #C23B2E; }}
#lim {{ margin-top: 26px; opacity: 0; }}
#lim .lb {{ display: flex; justify-content: space-between; font-family: Consolas, monospace; font-size: 22px; letter-spacing: .16em; color: rgba(18,19,20,.6); }}
#lim .bar {{ height: 26px; border-radius: 8px; background: rgba(18,19,20,.12); margin-top: 10px; overflow: hidden; }}
#lim .bar i {{ display: block; height: 100%; width: 100%; background: var(--ink); transform-origin: left; transform: scaleX(.18); }}

/* ending */
#idq {{ position: absolute; left: 0; width: 1080px; top: 640px; text-align: center; opacity: 0; }}
#idq .pi {{ display: inline-block; width: 120px; height: 120px; color: var(--lime); }}
#cmt {{ left: 110px; top: 1000px; width: 860px; height: 260px; padding: 34px 40px; }}
#cmt .u {{ display: flex; align-items: center; gap: 14px; font-family: Consolas, monospace; font-size: 22px; letter-spacing: .14em; color: rgba(18,19,20,.6); }}
#cmt .u i {{ width: 44px; height: 44px; border-radius: 50%; background: var(--ink); display: inline-block; }}
#cmt .tx {{ margin-top: 22px; font-family: "IDBold"; font-size: 40px; line-height: 1.25; min-height: 100px; }}
#cmt .caret {{ display: inline-block; width: 4px; height: 44px; background: var(--ink); vertical-align: middle; margin-left: 4px; }}
#follow {{ position: absolute; left: 330px; top: 1340px; width: 420px; height: 110px; border-radius: 999px; background: var(--lime); color: var(--ink); font-family: "IDBlack"; font-size: 46px; letter-spacing: .06em; display: flex; align-items: center; justify-content: center; gap: 14px; opacity: 0; box-shadow: 0 0 50px rgba(198,244,50,.4); }}
#follow .fi {{ width: 40px; height: 40px; }}

#brand {{ position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-family: "IDBlack"; font-size: 36px; color: var(--cream); opacity: .9; }}
#brand b {{ color: var(--lime); font-weight: normal; }}
#flash {{ position: absolute; inset: 0; background: var(--lime); opacity: 0; pointer-events: none; mix-blend-mode: soft-light; }}
</style>
</head>
<body>
<div id="root" data-composition-id="claude-duet" data-start="0" data-duration="{DUR}" data-fps="30" data-width="{W}" data-height="{H}">
  <audio id="vo" src="vo.mp3" data-start="0" data-duration="{DUR}" data-track-index="0"></audio>
  <div id="bg"></div><div id="grain"></div>

  <div id="cam">
  <!-- 1. APA -->
  <div class="scene" id="s1">
    {head("s1-h1", "BAYANGIN DEH!", 380, 130, ("DEH!",))}
    <div id="phone"><div class="clk">07:00</div><div class="dt">Senin &middot; alarm</div><div class="bell" id="bell">{ICON["bell"]}</div>
      {notif("n1", "mail", "32 email sudah dibaca", "3 yang penting ditandai", 400)}
      {notif("n2", "cal", "Jadwal hari ini siap", "4 agenda &middot; 1 bentrok", 540)}
      {notif("n3", "pen", "3 draft balasan", "tinggal kamu cek", 680)}</div>
    <div class="sim" id="sim1">SIMULASI</div>
    {lead("s1-l2", "itu", 380)}
    <div class="paper" id="title"><div class="k">AGEN AI PROAKTIF &middot; ANTHROPIC</div><div class="n">CLAUDE<br><span>DUET</span></div>
      <div class="d"><i id="t1">21 OKT 2026</i><i id="t2">RESEARCH PREVIEW</i><i id="t3">OPUS 5.5</i></div></div>
  </div>

  <!-- 2. CARA KERJA -->
  <div class="scene" id="s2">
    {lead("s2-l1", "bedanya sama chatbot biasa:", 380)}
    {head("s2-h1", "NGGAK NUNGGU|DISURUH", 440, 110, ("NUNGGU", "DISURUH"))}
    <div class="vs" id="vs1"><div class="vk">CHATBOT BIASA</div><div class="vt">nunggu<br>disuruh</div><div class="vi">{ICON["chat"]}</div>
      <div class="vd">diam sampai kamu nanya</div><div id="typing"><i></i><i></i><i></i></div></div>
    <div class="vs" id="vs2"><div class="vk">CLAUDE DUET</div><div class="vt">jalan<br>duluan</div><div class="vi">{ICON["bolt"]}</div>
      <div class="vd">kerja di cloud, meski aplikasi ditutup</div></div>
    <div id="ring"></div>
    <div id="hub">{ICON["cloud"]}<div class="lbl">DI CLOUD</div></div>
    {chip("c1", "mail", "Gmail", "left:120px;top:640px")}
    {chip("c2", "cal", "Kalender", "left:700px;top:640px")}
    {chip("c3", "chat", "Slack", "left:110px;top:1080px")}
    {chip("c4", "chart", "QuickBooks", "left:640px;top:1080px")}
    {mono("s2-m1", "DICEK SECARA BERKALA", 1190, 0, "width:1080px;text-align:center")}
    <div id="alert">{notif("n4", "bell", "Invoice klien telat bayar", "Duet: mau aku siapkan email pengingat?", 0)}</div>
    <div class="sim" id="sim2">SIMULASI</div>
  </div>

  <!-- 3. ATURAN -->
  <div class="scene" id="s3">
    {lead("s3-l1", "tapi ada satu", 380)}
    {head("s3-h1", "ATURAN MENARIK", 440, 120, ("ATURAN",))}
    {"".join(f'<div class="act" id="a{k}" style="left:{70 + (k % 2) * 500}px;top:{620 + (k // 2) * 150}px"><span class="ai">{ICON[ic]}</span>{tx}<span class="lk">{ICON["lock"]}</span></div>' for k, (ic, tx) in enumerate([("send", "kirim pesan"), ("card", "bayar"), ("sign", "tanda tangan"), ("trash", "hapus")]))}
    <div class="paper" id="ask"><div class="q">&ldquo;Boleh aku kirim email ini?&rdquo;<em>Duet selalu minta izin dulu</em></div>
      <div class="btns"><b class="yes" id="yes">IZINKAN</b><b class="no">TOLAK</b></div></div>
    <div class="cur" id="cursor" style="left:800px;top:1560px">{CURSOR}</div>
    {lead("s3-l2", "dan ini yang dia tolak, meski kamu izinkan:", 380, 72, 40)}
    <div class="deny" id="d1" style="top:620px"><span class="di">{ICON["chart"]}</span>trading saham<i class="strike"></i><span class="x">{ICON["cross"]}</span></div>
    <div class="deny" id="d2" style="top:780px"><span class="di">{ICON["bank"]}</span>transfer antar rekening<i class="strike"></i><span class="x">{ICON["cross"]}</span></div>
    <div class="stampc" id="st-tolak" style="top:960px">DITOLAK MESKI DIIZINKAN</div>
  </div>

  <!-- 4. BATASAN -->
  <div class="scene" id="s4">
    {head("s4-h1", "SAYANGNYA...", 380, 120, ("SAYANGNYA...",))}
    <div class="paper" id="rcpt"><div class="rh">STATUS CLAUDE DUET</div>
      <div class="rl" id="r1"><span>Tahap</span><b>Research preview</b></div>
      <div class="rl" id="r2"><span>Paket</span><b>Pro &amp; Max</b></div>
      <div class="rl" id="r3"><span>Wilayah</span><b>Akun Amerika</b></div>
      <div class="rl no" id="r4"><span>Indonesia</span><b>Belum</b></div>
      <div class="rl" id="r5"><span>Akses</span><b>Waitlist</b></div>
      <div class="rl" id="r6"><span>Biaya tambahan</span><b class="hl">Rp0</b></div>
      <div id="lim"><div class="lb"><span>LIMIT PRO/MAX TERPAKAI</span><span id="limv">18%</span></div><div class="bar"><i></i></div></div></div>
    <div class="stampc" id="st-limit" style="top:1500px;left:150px">TETAP MAKAN LIMIT</div>
  </div>

  <!-- 5. PENUTUP -->
  <div class="scene" id="s5">
    {lead("s5-l1", "jadi, kalau suatu hari Duet masuk", 380)}
    {head("s5-h1", "INDONESIA...", 440, 140, ("INDONESIA...",))}
    <div id="idq"><span class="pi">{ICON["pin"]}</span></div>
    <div class="paper" id="cmt"><div class="u"><i></i>KAMU &middot; BARU SAJA</div><div class="tx"><span id="cmtx"></span><span class="caret" id="caret"></span></div></div>
    <div id="follow"><span class="fi">{ICON["check"]}</span><span id="f1">FOLLOW</span><span id="f2" style="display:none">FOLLOWING</span></div>
    <div class="cur" id="cursor2" style="left:900px;top:1700px">{CURSOR}</div>
  </div>
  </div>

  <div id="hud"><div id="prog"></div><div id="tag"><i></i>CEK AI &middot; N&ordm; 01</div><div id="frame">FRAME 0000</div>
    <div id="steps"><span class="st" id="st1">01 APA</span><span class="st" id="st2">02 CARA KERJA</span><span class="st" id="st3">03 ATURAN</span><span class="st" id="st4">04 BATASAN</span></div></div>
  <div id="flash"></div>
  <div id="brand">Endrich<b>Tech</b></div>

  <script src="vendor/gsap.min.js"></script>
  <script>
  (function () {{
    var D = {json.dumps(DATA)};
    var FPS = 30, T = D.T, S = D.S;
    function q(t) {{ return Math.round(t * FPS) / FPS; }}
    var tl = gsap.timeline({{ paused: true }});
    var NI = {{ immediateRender: false }};
    function cut(sel, t, v) {{ tl.set(sel, {{ opacity: v }}, q(t)); }}
    function hide(sel, t, d) {{ tl.to(sel, {{ opacity: 0, y: -10, duration: d || 0.15, ease: "power2.in" }}, q(t)); }}
    function rise(sel, t, d, from) {{
      tl.fromTo(sel, Object.assign({{ opacity: 0, y: 40 }}, from || {{}}), {{ opacity: 1, y: 0, x: 0, scale: 1, duration: d || 0.4, ease: "power3.out" }}, q(t));
    }}
    function pop(sel, t, d) {{ tl.fromTo(sel, {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: d || 0.32, ease: "back.out(2)" }}, q(t)); }}
    function lead(sel, t) {{ rise(sel, t, 0.3, {{ y: 14 }}); }}
    function headIn(sel, t, d) {{
      var ch = document.querySelectorAll(sel + " .ch");
      tl.set(sel, {{ opacity: 1 }}, q(t));
      tl.fromTo(ch, {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out", stagger: Math.min(0.03, (d || 0.4) / ch.length) }}, q(t));
    }}
    function stampIn(sel, t) {{
      tl.fromTo(sel, {{ opacity: 0, scale: 1.6, rotation: -4 }}, {{ opacity: 1, scale: 1, rotation: -2, duration: 0.22, ease: "power4.in" }}, q(t));
      tl.fromTo("#flash", {{ opacity: 0.5 }}, Object.assign({{ opacity: 0, duration: 0.3 }}, NI), q(t + 0.22));
      tl.fromTo("#cam", {{ x: -8 }}, Object.assign({{ x: 0, duration: 0.25, ease: "elastic.out(1,.3)" }}, NI), q(t + 0.22));
    }}
    function scene(id, k) {{ cut(id, S[k][0], 1); cut(id, S[k][1], 0); }}
    function push(k) {{ tl.fromTo("#cam", {{ scale: 1 }}, Object.assign({{ scale: 1.04, duration: S[k][1] - S[k][0], ease: "none" }}, NI), q(S[k][0])); }}
    function step(n, t) {{ for (var k = 1; k <= 4; k++) tl.set("#st" + k, {{ className: k === n ? "st on" : "st" }}, q(t)); }}

    // HUD: progress bar, frame counter, chapter stepper
    tl.fromTo("#prog", {{ scaleX: 0 }}, {{ scaleX: 1, duration: D.DUR, ease: "none" }}, 0);
    var fr = {{ f: 0 }}, fel = document.querySelector("#frame");
    tl.to(fr, {{ f: Math.round(D.DUR * FPS), duration: D.DUR, ease: "none", onUpdate: function () {{ fel.textContent = "FRAME " + String(Math.round(fr.f)).padStart(4, "0"); }} }}, 0);
    step(1, 0); step(2, S.s2[0]); step(3, S.s3[0]); step(4, S.s4[0]);

    // 1. APA
    scene("#s1", "s1"); push("s1");
    headIn("#s1-h1", T[0], 0.35);
    rise("#phone", T[2] - 0.1, 0.5, {{ y: 120 }});
    tl.fromTo("#bell", {{ rotation: -18 }}, {{ rotation: 18, duration: 0.12, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }}, q(T[3]));
    tl.to("#phone .clk, #phone .dt, #bell", {{ opacity: 0.25, duration: 0.3 }}, q(T[6]));
    rise("#n1", T[9], 0.35, {{ y: -30 }}); rise("#n2", T[12], 0.35, {{ y: -30 }}); rise("#n3", T[18], 0.35, {{ y: -30 }});
    cut("#sim1", T[9], 1);
    hide("#s1-h1, #phone, #sim1", T[21] - 0.15, 0.15);
    lead("#s1-l2", T[21]);
    rise("#title", T[22] - 0.05, 0.45, {{ y: 80, rotation: -3 }});
    [["#t1", 24], ["#t2", 26], ["#t3", 28]].forEach(function (d) {{ pop(d[0], T[d[1]], 0.3); }});

    // 2. CARA KERJA
    scene("#s2", "s2"); push("s2");
    lead("#s2-l1", T[30]);
    rise("#vs1", T[32], 0.4, {{ x: -60, y: 0 }});
    tl.to("#typing i", {{ opacity: 1, duration: 0.25, stagger: 0.15, yoyo: true, repeat: 3 }}, q(T[32] + 0.4));
    headIn("#s2-h1", T[35], 0.35);
    rise("#vs2", T[34], 0.4, {{ x: 60, y: 0 }});
    hide("#s2-l1, #s2-h1, #vs1, #vs2", T[38] - 0.1, 0.15);
    pop("#hub", T[39], 0.4); tl.fromTo("#ring", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.5 }}, q(T[40]));
    tl.to("#ring", {{ rotation: 360, duration: 8, ease: "none" }}, q(T[40]));
    [["#c1", 43], ["#c2", 44], ["#c3", 45], ["#c4", 47]].forEach(function (c) {{ pop(c[0], T[c[1]], 0.32); }});
    rise("#s2-m1", T[48], 0.3, {{ y: 10 }});
    tl.to("#hub", {{ boxShadow: "0 0 90px rgba(198,244,50,.6)", duration: 0.25, yoyo: true, repeat: 3 }}, q(T[48]));
    rise("#alert", T[51], 0.4, {{ y: 60 }}); cut("#sim2", T[51], 1);

    // 3. ATURAN
    scene("#s3", "s3"); push("s3");
    lead("#s3-l1", T[56]); headIn("#s3-h1", T[59], 0.35);
    [["#a0", 63], ["#a1", 65], ["#a2", 66], ["#a3", 69]].forEach(function (a) {{
      rise(a[0], T[a[1]], 0.3, {{ y: 30 }}); pop(a[0] + " .lk", T[a[1]] + 0.25, 0.3);
    }});
    rise("#ask", T[71], 0.45, {{ y: 80 }});
    tl.fromTo("#cursor", {{ opacity: 0, x: 0, y: 0 }}, {{ opacity: 1, x: -550, y: -220, duration: 0.6, ease: "power2.out" }}, q(T[73]));
    tl.to("#yes", {{ scale: 0.92, duration: 0.08, yoyo: true, repeat: 1 }}, q(T[75]));
    tl.fromTo("#flash", {{ opacity: 0.35 }}, Object.assign({{ opacity: 0, duration: 0.25 }}, NI), q(T[75] + 0.1));
    hide("#s3-l1, #s3-h1, #a0, #a1, #a2, #a3, #ask, #cursor", T[76] - 0.1, 0.15);
    lead("#s3-l2", T[76]);
    // both rows wait faintly under the lead line, then light up on their word
    tl.fromTo("#d1, #d2", {{ opacity: 0, x: -50 }}, {{ opacity: 0.22, x: 0, duration: 0.4, stagger: 0.12, ease: "power3.out" }}, q(T[77]));
    tl.to("#d1", {{ opacity: 1, duration: 0.25 }}, q(T[85])); tl.to("#d2", {{ opacity: 1, duration: 0.25 }}, q(T[88]));
    tl.to("#d1 .strike", {{ scaleX: 1, duration: 0.25 }}, q(T[86] + 0.2)); pop("#d1 .x", T[86] + 0.4, 0.3);
    tl.to("#d2 .strike", {{ scaleX: 1, duration: 0.25 }}, q(T[90] + 0.1)); pop("#d2 .x", T[90] + 0.3, 0.3);
    stampIn("#st-tolak", T[90] + 0.45);

    // 4. BATASAN
    scene("#s4", "s4"); push("s4");
    headIn("#s4-h1", T[91], 0.35);
    rise("#rcpt", T[92], 0.45, {{ y: 100 }});
    [["#r1", 94], ["#r2", 99], ["#r3", 103], ["#r4", 103], ["#r5", 105], ["#r6", 107]].forEach(function (r, k) {{
      rise(r[0], T[r[1]] + (k === 3 ? 0.4 : 0), 0.25, {{ y: -12, opacity: 0.12 }});
    }});
    tl.to("#r4 b", {{ scale: 1.15, duration: 0.15, yoyo: true, repeat: 1 }}, q(T[103] + 0.6));
    rise("#lim", T[110], 0.3, {{ y: 10 }});
    tl.to("#lim .bar i", {{ scaleX: 0.72, duration: 1.0, ease: "power2.inOut" }}, q(T[111]));
    var lv = {{ v: 18 }}, lel = document.querySelector("#limv");
    tl.to(lv, {{ v: 72, duration: 1.0, ease: "power2.inOut", onUpdate: function () {{ lel.textContent = Math.round(lv.v) + "%"; }} }}, q(T[111]));
    stampIn("#st-limit", T[113]);

    // 5. PENUTUP
    scene("#s5", "s5"); push("s5");
    lead("#s5-l1", T[115]); headIn("#s5-h1", T[120], 0.35);
    tl.fromTo("#idq", {{ opacity: 0, y: -60 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "bounce.out" }}, q(T[120] + 0.2));
    rise("#cmt", T[121] - 0.1, 0.4, {{ y: 80 }});
    var msg = "Tugas pertama buat Duet: beresin inbox kerjaanku tiap pagi", cel = document.querySelector("#cmtx"), cs = {{ n: 0 }};
    tl.to(cs, {{ n: msg.length, duration: T[131] - T[121], ease: "none", onUpdate: function () {{ cel.textContent = msg.slice(0, Math.round(cs.n)); }} }}, q(T[121] + 0.2));
    tl.to("#caret", {{ opacity: 0, duration: 0.3, yoyo: true, repeat: 12, ease: "steps(1)" }}, q(T[121]));
    pop("#follow", T[131], 0.35);
    tl.fromTo("#cursor2", {{ opacity: 0, x: 0, y: 0 }}, {{ opacity: 1, x: -340, y: -300, duration: 0.5, ease: "power2.out" }}, q(T[132]));
    tl.to("#follow", {{ scale: 0.93, duration: 0.08, yoyo: true, repeat: 1 }}, q(T[133] + 0.3));
    tl.set("#f1", {{ display: "none" }}, q(T[133] + 0.38)); tl.set("#f2", {{ display: "inline" }}, q(T[133] + 0.38));

    window.__timelines = window.__timelines || {{}};
    window.__timelines["claude-duet"] = tl;
  }})();
  </script>
</div>
</body>
</html>
'''
(HERE / "public" / "index.html").write_text(HTML, encoding="utf-8")
print("DUR", DUR, {k: (round(a, 2), round(b, 2)) for k, (a, b) in S.items()})
