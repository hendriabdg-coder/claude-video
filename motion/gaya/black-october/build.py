# "Black October" fact-check short — same approved visual language as gemini-cek-fakta v2 (warm black, wide glowing
# type swept in letter by letter, chapter numbers, tilted 3D panels, flash cards, dust, camera drift), re-themed for
# security: red = confirmed threat, amber = potential only, gold = brand/outro. VO = Endrich clone, eleven_v4.
import json
import random
import subprocess
from pathlib import Path
from PIL import ImageFont

HERE = Path(__file__).resolve().parent
VO = HERE / "vo-sumber" / "vo_A_s35"
W, H, GAP = 1080, 1920, 0.3
F_BLACK = str(HERE / "public" / "fonts" / "InterDisplay-Black.ttf")
WIDE = 1.16

WORDS, off = [], 0.0
for n in range(1, 7):
    d = json.loads((VO / f"scene_{n:02d}.json").read_text(encoding="utf-8"))
    WORDS += [{"x": w["word"], "t": round(off + w["start"], 3)} for w in d["words"]]
    off += float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                          "csv=p=0", str(VO / f"scene_{n:02d}.mp3")])) + GAP
DUR = round(off - GAP + 0.6, 2)
T = lambda i: WORDS[i]["t"]
assert WORDS[26]["x"] == "PHP2Shell." and WORDS[94]["x"] == "eMudhra." and WORDS[135]["x"] == "update.", WORDS[24:28]


def fit_heavy(text, px, maxw=930):
    while px > 30:
        if ImageFont.truetype(F_BLACK, px).getlength(text) * WIDE + len(text) * px * 0.02 <= maxw:
            return px
        px -= 2
    return px

def heavy(hid, text, top, px, color="c", center=False):
    lines = text.split("|")
    size = min(fit_heavy(l, px) for l in lines)
    rows = "".join('<div class="hr">' + "".join(f'<span class="ch">{c if c != " " else "&nbsp;"}</span>' for c in l)
                   + "</div>" for l in lines)
    pos = "left:0;width:1080px;text-align:center;transform-origin:center top" if center else "left:70px;transform-origin:left top"
    return f'<div class="heavy {color}" id="{hid}" style="top:{top}px;{pos};font-size:{size}px">{rows}</div>'

def lead(lid, text, top, left=72, px=46):
    return f'<div class="lead" id="{lid}" style="top:{top}px;left:{left}px;font-size:{px}px">{text}</div>'

def mono(mid, text, top, left=72, extra=""):
    return f'<div class="mono" id="{mid}" style="top:{top}px;left:{left}px;{extra}">{text}</div>'

def svg(body, sw=6):
    return (f'<svg class="ico" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>')

ICON = {
    "check": svg('<path d="M24 52l17 17 35-38"/>', 11),
    "cross": svg('<path d="M28 28l44 44M72 28L28 72"/>', 11),
    "alert": svg('<path d="M50 12l40 72H10z"/><path d="M50 40v20M50 70v2"/>', 7),
    "search": svg('<circle cx="43" cy="43" r="25"/><path d="M62 62l22 22"/>', 8),
    "lock": svg('<rect x="20" y="44" width="60" height="44" rx="10"/><path d="M32 44V32a18 18 0 0 1 36 0v12"/>'),
    "unlock": svg('<rect x="20" y="44" width="60" height="44" rx="10"/><path d="M32 44V32a18 18 0 0 1 34-8"/>'),
    "key": svg('<circle cx="32" cy="50" r="16"/><path d="M48 50h40M76 50v14M88 50v10"/>', 7),
    "shield": svg('<path d="M50 8l34 12v26c0 22-14 38-34 46C30 84 16 68 16 46V20z"/><path d="M34 34l32 32M66 34L34 66"/>', 6),
    "server": svg('<rect x="16" y="14" width="68" height="30" rx="6"/><rect x="16" y="56" width="68" height="30" rx="6"/>'
                  '<path d="M28 29h4M28 71h4M44 29h28M44 71h28"/>'),
    "coin": svg('<circle cx="50" cy="50" r="34"/><path d="M42 34h12a8 8 0 0 1 0 16H42zM42 50h14a8 8 0 0 1 0 16H42zM42 30v40M50 26v8M50 66v8"/>', 6),
    "bug": svg('<ellipse cx="50" cy="56" rx="20" ry="26"/><path d="M50 30v52M30 46H14M30 62H14M70 46h16M70 62h16M38 32l-8-10M62 32l8-10"/>', 6),
    "terminal": svg('<rect x="10" y="18" width="80" height="64" rx="8"/><path d="M24 40l12 10-12 10M44 62h22"/>', 6),
    "user": svg('<circle cx="50" cy="36" r="16"/><path d="M18 88c0-18 14-30 32-30s32 12 32 30"/>', 6),
}

def stamp(sid, text, color, icon, top, px=72):
    return (f'<div class="stamp {color}" id="{sid}" style="top:{top}px;font-size:{px}px"><span class="si" '
            f'style="width:{px}px;height:{px}px">{ICON[icon]}</span>{text}</div>')

def flashcard(fid, word, color, px=116):
    rows = "".join(f'<div class="fr{" solid" if k == 5 else ""}" style="font-size:{px}px">{word}</div>' for k in range(11))
    return f'<div class="flash {color}" id="{fid}"><div class="frs">{rows}</div></div>'

def cal(cid, top, days, marks):
    """horizontal October strip; marks = {day: (cls, label)}"""
    cells = "".join(f'<div class="day{" " + marks[d][0] if d in marks else ""}" id="{cid}-d{d}"><b>{d}</b>'
                    f'{"<i>" + marks[d][1] + "</i>" if d in marks else ""}</div>' for d in days)
    return f'<div class="cal" id="{cid}" style="top:{top}px"><div class="mon">OKTOBER 2026</div><div class="days">{cells}</div></div>'

def logo(lid, name, color, top, left=860, size=150):
    return (f'<div class="logo" id="{lid}" style="top:{top}px;left:{left}px;width:{size}px;height:{size}px;'
            f'background:{color};-webkit-mask:url(logos/{name}.svg) center/contain no-repeat;'
            f'mask:url(logos/{name}.svg) center/contain no-repeat;filter:drop-shadow(0 0 18px {color})"></div>')

IMG = HERE / "public" / "img"
def bgimg(iid, name):
    """AI illustration behind a chapter; skipped until the file exists in public/img/."""
    f = next((f for f in (IMG / f"{name}.jpg", IMG / f"{name}.png", IMG / f"{name}.webp") if f.exists()), None)
    if not f:
        return ""
    return (f'<div class="bgimg" id="{iid}"><img src="img/{f.name}" alt=""><div class="shade"></div>'
            f'<div class="ailbl">ILUSTRASI AI</div></div>')

random.seed(11)
DUST = "".join(f'<i class="dust" style="left:{random.randint(20, 1060)}px;top:{random.randint(150, 1700)}px;'
               f'width:{(s := random.choice((4, 5, 6, 8)))}px;height:{s}px;opacity:{random.uniform(.15, .5):.2f}"></i>'
               for _ in range(30))

S = {"hook": (0.0, T(25) - 0.05), "c1": (T(25) - 0.05, T(54) - 0.05), "c2": (T(54) - 0.05, T(75) - 0.05),
     "c3": (T(75) - 0.05, T(92) - 0.05), "c4": (T(92) - 0.05, T(117) - 0.05), "out": (T(117) - 0.05, DUR)}
DATA = {"S": S, "T": {i: w["t"] for i, w in enumerate(WORDS)}, "DUR": DUR}

HTML = f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8" />
<style>
@font-face {{ font-family: "IDBlack"; src: url("fonts/InterDisplay-Black.ttf") format("truetype"); font-display: block; }}
@font-face {{ font-family: "IDSemi"; src: url("fonts/InterDisplay-SemiBold.ttf") format("truetype"); font-display: block; }}
@font-face {{ font-family: "IDItal"; src: url("fonts/InterDisplay-SemiBoldItalic.ttf") format("truetype"); font-display: block; }}
:root {{ --bg:#0a0907; --gold:#F5C452; --cream:#FFF3D6; --red:#FF4A4A; --amber:#FFAA2C; --green:#59E38C; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 100%; height: 100%; overflow: hidden; background: var(--bg); color: var(--cream); font-family: "IDSemi", sans-serif; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: var(--bg); }}
.ico {{ width: 100%; height: 100%; display: block; }}
#bg {{ position: absolute; inset: 0; }}
.tint {{ position: absolute; inset: -200px; opacity: 0; }}
#t-gold {{ opacity: 1; background: radial-gradient(ellipse 60% 40% at 50% 42%, rgba(245,196,82,.15) 0%, rgba(245,196,82,0) 70%); }}
#t-red {{ background: radial-gradient(ellipse 60% 40% at 50% 42%, rgba(255,60,60,.17) 0%, rgba(255,60,60,0) 70%); }}
#t-amber {{ background: radial-gradient(ellipse 60% 40% at 50% 42%, rgba(255,170,44,.15) 0%, rgba(255,170,44,0) 70%); }}
#vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse 85% 70% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.78) 100%); pointer-events: none; }}
.dust {{ position: absolute; border-radius: 50%; background: var(--gold); box-shadow: 0 0 12px 3px rgba(245,196,82,.55); }}
#cam {{ position: absolute; inset: 0; transform-origin: 50% 45%; }}
.scene {{ position: absolute; inset: 0; opacity: 0; }}

.heavy {{ position: absolute; font-family: "IDBlack"; line-height: .98; letter-spacing: .02em; text-transform: uppercase; white-space: nowrap; transform: scaleX({WIDE}); }}
.heavy .hr {{ display: block; }}
.heavy .ch {{ display: inline-block; opacity: 0; }}
.heavy.c {{ color: var(--cream); text-shadow: 0 0 14px rgba(245,196,82,.85), 0 0 46px rgba(245,196,82,.45); }}
.heavy.g {{ color: var(--gold); text-shadow: 0 0 16px rgba(245,196,82,.9), 0 0 60px rgba(245,196,82,.5); }}
.heavy.r {{ color: #FFE2E2; text-shadow: 0 0 14px rgba(255,74,74,.95), 0 0 54px rgba(255,74,74,.6); }}
.heavy.a {{ color: #FFF0D6; text-shadow: 0 0 14px rgba(255,170,44,.95), 0 0 50px rgba(255,170,44,.5); }}
.heavy.gr {{ color: #E8FFF0; text-shadow: 0 0 14px rgba(89,227,140,.95), 0 0 50px rgba(89,227,140,.5); }}
.lead {{ position: absolute; font-family: "IDItal"; color: rgba(255,243,214,.88); text-shadow: 0 0 18px rgba(245,196,82,.35); opacity: 0; white-space: nowrap; }}
.mono {{ position: absolute; font-family: Consolas, "Courier New", monospace; font-size: 26px; letter-spacing: .16em; text-transform: uppercase; color: rgba(255,243,214,.6); opacity: 0; white-space: nowrap; }}

#hud {{ position: absolute; left: 72px; top: 236px; display: flex; align-items: center; gap: 18px; opacity: 0; }}
#hud .tag {{ font-family: Consolas, monospace; font-size: 26px; letter-spacing: .2em; color: var(--gold); padding: 8px 16px; border: 2px solid rgba(245,196,82,.6); border-radius: 8px; }}
#hud .dots {{ display: flex; gap: 10px; }}
#hud .dots i {{ width: 34px; height: 6px; border-radius: 3px; background: rgba(255,243,214,.18); }}
#hud .dots i.r {{ background: var(--red); box-shadow: 0 0 10px rgba(255,74,74,.8); }}
#hud .dots i.a {{ background: var(--amber); box-shadow: 0 0 10px rgba(255,170,44,.8); }}

.chap {{ position: absolute; left: 0; width: 1080px; top: 700px; text-align: center; opacity: 0; }}
.chap .n {{ font-family: "IDBlack"; font-size: 300px; line-height: 1; color: transparent; -webkit-text-stroke: 4px var(--gold); transform: scaleX({WIDE}); display: inline-block; }}
.chap.r .n {{ -webkit-text-stroke-color: var(--red); filter: drop-shadow(0 0 22px rgba(255,74,74,.6)); }}
.chap.a .n {{ -webkit-text-stroke-color: var(--amber); filter: drop-shadow(0 0 22px rgba(255,170,44,.6)); }}
.chap .l {{ font-family: Consolas, monospace; font-size: 30px; letter-spacing: .4em; color: rgba(255,243,214,.7); margin-top: 18px; }}

.stamp {{ position: absolute; left: 72px; display: flex; align-items: center; gap: 16px; padding: 12px 34px 14px 22px; border-radius: 18px; border: 5px solid; font-family: "IDBlack"; letter-spacing: .04em; line-height: 1; opacity: 0; white-space: nowrap; transform-origin: left center; }}
.stamp.r {{ color: var(--red); border-color: var(--red); background: rgba(255,74,74,.10); box-shadow: 0 0 44px rgba(255,74,74,.4), inset 0 0 24px rgba(255,74,74,.15); }}
.stamp.a {{ color: var(--amber); border-color: var(--amber); background: rgba(255,170,44,.10); box-shadow: 0 0 44px rgba(255,170,44,.35), inset 0 0 24px rgba(255,170,44,.15); }}
.stamp.gr {{ color: var(--green); border-color: var(--green); background: rgba(89,227,140,.10); box-shadow: 0 0 40px rgba(89,227,140,.35); }}

.panel {{ position: absolute; border-radius: 26px; background: linear-gradient(160deg, #1b1812, #100e0a); border: 2px solid rgba(245,196,82,.28); box-shadow: 0 40px 90px rgba(0,0,0,.6), 0 0 40px rgba(245,196,82,.12); opacity: 0; overflow: hidden; }}
.panel.r {{ border-color: rgba(255,74,74,.45); box-shadow: 0 40px 90px rgba(0,0,0,.6), 0 0 40px rgba(255,74,74,.18); }}
.panel.a {{ border-color: rgba(255,170,44,.45); box-shadow: 0 40px 90px rgba(0,0,0,.6), 0 0 40px rgba(255,170,44,.15); }}
.persp {{ position: absolute; inset: 0; perspective: 1600px; }}

/* calendar strip */
.cal {{ position: absolute; left: 72px; width: 936px; opacity: 0; }}
.cal .mon {{ font-family: Consolas, monospace; font-size: 26px; letter-spacing: .3em; color: rgba(255,243,214,.55); margin-bottom: 14px; }}
.cal .days {{ display: flex; gap: 10px; }}
.day {{ position: relative; flex: 1; height: 150px; border-radius: 16px; background: rgba(255,243,214,.05); border: 2px solid rgba(255,243,214,.12); display: flex; flex-direction: column; align-items: center; justify-content: center; }}
.day b {{ font-family: "IDBlack"; font-weight: normal; font-size: 52px; color: rgba(255,243,214,.5); }}
.day i {{ position: absolute; bottom: -46px; font-style: normal; font-family: Consolas, monospace; font-size: 22px; letter-spacing: .12em; white-space: nowrap; opacity: 0; }}
.day.hit b {{ color: #FFE2E2; }} .day.hit i {{ color: var(--red); }}
.day.fix b {{ color: #E8FFF0; }} .day.fix i {{ color: var(--green); }}
.span4 {{ position: absolute; height: 6px; border-radius: 3px; background: linear-gradient(90deg, var(--red), var(--green)); transform-origin: left; transform: scaleX(0); box-shadow: 0 0 14px rgba(255,74,74,.6); }}
.spanlbl {{ position: absolute; font-family: "IDBlack"; font-size: 64px; color: var(--cream); text-shadow: 0 0 20px rgba(255,74,74,.7); opacity: 0; transform: scaleX({WIDE}); transform-origin: center; white-space: nowrap; }}

/* stack diagram (PHP) */
.layer {{ position: absolute; left: 150px; width: 780px; height: 120px; border-radius: 20px; display: flex; align-items: center; gap: 24px; padding: 0 34px; font-family: "IDBlack"; font-size: 50px; background: rgba(255,243,214,.05); border: 2px solid rgba(255,243,214,.18); opacity: 0; }}
.layer .li {{ width: 64px; height: 64px; color: var(--gold); flex: none; }}
.layer.core {{ border-color: var(--red); background: rgba(255,74,74,.10); box-shadow: 0 0 40px rgba(255,74,74,.35); }}
.layer.core .li {{ color: var(--red); }}
.bugs {{ position: absolute; right: 30px; display: flex; gap: 14px; }}
.bugs i {{ width: 60px; height: 60px; color: var(--red); opacity: 0; }}
#nologin {{ position: absolute; left: 150px; top: 1250px; display: flex; align-items: center; gap: 22px; padding: 18px 36px; border-radius: 18px; border: 3px solid rgba(255,243,214,.3); font-family: "IDBlack"; font-size: 54px; color: rgba(255,243,214,.6); opacity: 0; }}
#nologin .ui {{ width: 56px; height: 56px; }}
#nologin .strike {{ position: absolute; left: -10px; right: -10px; top: 50%; height: 8px; border-radius: 4px; background: var(--red); box-shadow: 0 0 16px var(--red); transform-origin: left; transform: scaleX(0); }}

/* plex: miner server */
#rig {{ left: 110px; top: 830px; width: 860px; height: 420px; padding: 40px; }}
#rig .hd {{ display: flex; align-items: center; gap: 20px; font-family: Consolas, monospace; font-size: 26px; letter-spacing: .16em; color: rgba(255,243,214,.6); }}
#rig .hd .ico {{ width: 56px; height: 56px; color: var(--red); }}
#rig .cpu {{ margin-top: 40px; font-family: Consolas, monospace; font-size: 26px; letter-spacing: .16em; color: rgba(255,243,214,.6); }}
#rig .bar {{ margin-top: 14px; height: 34px; border-radius: 10px; background: rgba(255,255,255,.08); overflow: hidden; }}
#rig .bar i {{ display: block; height: 100%; width: 100%; background: linear-gradient(90deg, var(--amber), var(--red)); box-shadow: 0 0 20px var(--red); transform-origin: left; transform: scaleX(.12); }}
#rig .pct {{ position: absolute; right: 40px; top: 120px; font-family: "IDBlack"; font-size: 110px; color: #FFE2E2; text-shadow: 0 0 24px rgba(255,74,74,.8); }}
#rig .proc {{ margin-top: 30px; font-family: Consolas, monospace; font-size: 30px; color: var(--red); opacity: 0; }}
.coin {{ position: absolute; width: 90px; height: 90px; color: var(--gold); filter: drop-shadow(0 0 16px rgba(245,196,82,.7)); opacity: 0; }}
.mini {{ position: absolute; top: 1150px; width: 400px; height: 190px; padding: 26px 30px; }}
.mini .m1 {{ font-family: Consolas, monospace; font-size: 24px; letter-spacing: .2em; color: rgba(255,243,214,.55); }}
.mini .m2 {{ font-family: "IDBlack"; font-size: 58px; margin-top: 10px; }}
.mini .mi {{ position: absolute; right: 26px; top: 26px; width: 60px; height: 60px; }}
#gap2 {{ position: absolute; left: 0; width: 1080px; top: 1380px; text-align: center; font-family: "IDBlack"; font-size: 56px; color: var(--cream); text-shadow: 0 0 18px rgba(255,74,74,.6); opacity: 0; }}

/* gitlab: score gauge */
#gauge {{ position: absolute; left: 240px; top: 680px; width: 600px; height: 340px; opacity: 0; }}
#gauge svg {{ width: 600px; height: 340px; overflow: visible; }}
#gauge .num {{ position: absolute; left: 0; width: 600px; top: 150px; text-align: center; font-family: "IDBlack"; font-size: 150px; line-height: 1; color: #FFE2E2; text-shadow: 0 0 26px rgba(255,74,74,.8); }}
#gauge .sub {{ position: absolute; left: 0; width: 600px; top: 310px; text-align: center; font-family: Consolas, monospace; font-size: 26px; letter-spacing: .2em; color: rgba(255,243,214,.55); }}
#evid {{ left: 110px; top: 1080px; width: 860px; height: 230px; padding: 34px 40px; }}
#evid .e1 {{ font-family: Consolas, monospace; font-size: 26px; letter-spacing: .2em; color: rgba(255,243,214,.55); }}
#evid .e2 {{ display: flex; align-items: center; gap: 22px; margin-top: 22px; font-family: "IDBlack"; font-size: 60px; color: var(--amber); text-shadow: 0 0 18px rgba(255,170,44,.6); }}
#evid .e2 .ico {{ width: 70px; height: 70px; }}

/* emudhra: key + counter */
#keyw {{ position: absolute; left: 110px; top: 660px; width: 860px; height: 420px; opacity: 0; }}
#keyw .kk {{ position: absolute; left: 30px; top: 60px; width: 230px; height: 230px; color: var(--amber); filter: drop-shadow(0 0 22px rgba(255,170,44,.7)); }}
#keyw .cnt {{ position: absolute; left: 300px; top: 50px; font-family: "IDBlack"; font-size: 190px; line-height: 1; color: #FFF0D6; text-shadow: 0 0 30px rgba(255,170,44,.8); transform: scaleX({WIDE}); transform-origin: left; }}
#keyw .cl {{ position: absolute; left: 306px; top: 270px; font-family: Consolas, monospace; font-size: 28px; letter-spacing: .2em; color: rgba(255,243,214,.6); }}
#keyw .lk {{ position: absolute; right: 20px; top: 250px; width: 100px; height: 100px; color: var(--red); }}
#keyw .lk .ico {{ position: absolute; inset: 0; }}
#browser {{ left: 110px; top: 1080px; width: 860px; height: 300px; }}
#browser .bar {{ height: 64px; display: flex; align-items: center; gap: 12px; padding: 0 24px; border-bottom: 2px solid rgba(255,255,255,.08); }}
#browser .bar i {{ width: 16px; height: 16px; border-radius: 50%; background: rgba(255,243,214,.25); }}
#browser .bar span {{ margin-left: 20px; flex: 1; height: 30px; border-radius: 15px; background: rgba(255,255,255,.06); }}
#browser .bd {{ display: flex; align-items: center; gap: 26px; padding: 40px 44px; }}
#browser .bd .ico {{ width: 110px; height: 110px; color: var(--green); flex: none; filter: drop-shadow(0 0 18px rgba(89,227,140,.6)); }}
#browser .bd b {{ font-family: "IDBlack"; font-weight: normal; font-size: 62px; color: #E8FFF0; }}
#browser .bd em {{ display: block; font-style: normal; font-family: Consolas, monospace; font-size: 24px; letter-spacing: .16em; color: rgba(255,243,214,.55); margin-top: 8px; }}

/* flash cards */
.flash {{ position: absolute; inset: 0; opacity: 0; overflow: hidden; }}
.flash.red {{ background: #D7263D; }} .flash.amber {{ background: #F2A33A; }}
.flash .frs {{ position: absolute; left: 0; top: 230px; width: 1080px; }}
.flash .fr {{ font-family: "IDBlack"; font-size: 116px; line-height: 1.05; text-align: center; color: transparent; -webkit-text-stroke: 3px rgba(10,9,7,.35); transform: scaleX({WIDE}); white-space: nowrap; }}
.flash .fr.solid {{ color: #0a0907; -webkit-text-stroke: 0; }}

/* outro scoreboard */
.row {{ position: absolute; left: 90px; width: 900px; height: 100px; display: flex; align-items: center; gap: 22px; padding: 0 28px; border-radius: 20px; background: rgba(255,243,214,.05); border: 2px solid rgba(245,196,82,.22); opacity: 0; }}
.row .rt {{ font-family: "IDBlack"; font-size: 46px; flex: 1; }}
.row .rv {{ font-family: Consolas, monospace; font-size: 26px; letter-spacing: .16em; padding: 8px 16px; border-radius: 10px; border: 2px solid; }}
.row.r .rv {{ color: var(--red); border-color: var(--red); background: rgba(255,74,74,.1); }}
.row.a .rv {{ color: var(--amber); border-color: var(--amber); background: rgba(255,170,44,.1); }}
#massal {{ position: absolute; left: 0px; top: 1060px; opacity: 0; }}
#massal .strike {{ position: absolute; left: 60px; width: 900px; top: 52%; height: 12px; border-radius: 6px; background: var(--red); box-shadow: 0 0 20px var(--red); transform-origin: left; transform: scaleX(0); }}
.todo {{ position: absolute; left: 90px; display: flex; align-items: center; gap: 22px; font-family: "IDBlack"; font-size: 60px; opacity: 0; }}
.todo .tb {{ width: 76px; height: 76px; border-radius: 18px; border: 4px solid var(--gold); padding: 10px; color: var(--green); }}
.todo .tb .ico {{ opacity: 0; }}

.logo {{ position: absolute; opacity: 0; }}
.rlogo {{ display: inline-block; width: 46px; height: 46px; margin-right: 18px; flex: none; }}
.bgimg {{ position: absolute; inset: 0; opacity: 0; overflow: hidden; }}
.bgimg img {{ position: absolute; inset: -40px; width: calc(100% + 80px); height: calc(100% + 80px); object-fit: cover; filter: saturate(.9) contrast(1.05); }}
.bgimg .shade {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(10,9,7,.92) 0%, rgba(10,9,7,.55) 35%, rgba(10,9,7,.6) 65%, rgba(10,9,7,.95) 100%); }}
.bgimg .ailbl {{ position: absolute; right: 150px; bottom: 300px; font-family: Consolas, monospace; font-size: 20px; letter-spacing: .2em; color: rgba(255,243,214,.45); }}
#brand {{ position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-family: "IDBlack"; font-size: 38px; letter-spacing: .04em; color: var(--cream); opacity: .9; }}
#brand b {{ color: var(--gold); font-weight: normal; }}
#whiteflash {{ position: absolute; inset: 0; background: #FFF3D6; opacity: 0; pointer-events: none; }}
#redflash {{ position: absolute; inset: 0; background: #FF2A2A; opacity: 0; pointer-events: none; mix-blend-mode: screen; }}
</style>
</head>
<body>
<div id="root" data-composition-id="black-october" data-start="0" data-duration="{DUR}" data-fps="30" data-width="{W}" data-height="{H}">
  <audio id="vo" src="vo.mp3" data-start="0" data-duration="{DUR}" data-track-index="0"></audio>
  <div id="bg"><div class="tint" id="t-gold"></div><div class="tint" id="t-red"></div><div class="tint" id="t-amber"></div><div id="dust">{DUST}</div></div>

  <div id="cam">
  <div id="hud"><div class="tag">CEK FAKTA</div><div class="dots">{"".join(f'<i id="dot{k}"></i>' for k in range(1, 5))}</div></div>

  <!-- HOOK -->
  <div class="scene" id="s-hook">
    {bgimg("im-hook", "hook")}
    {lead("h-l1", "sebelum patch-nya keluar...", 380)}
    {heavy("h-h1", "4 HARI", 440, 230, "r")}
    {cal("cal1", 900, range(15, 23), {17: ("hit", "DIINCAR"), 21: ("fix", "PATCH")})}
    <div class="span4" id="h-span" style="left:{72 + 2 * 118 + 59}px;top:932px;width:{4 * 118}px"></div>
    {lead("h-l2", "makanya Oktober ini dijuluki", 380)}
    {lead("h-l3", "tapi, beneran internet lagi", 380)}
    {heavy("h-h3", "JEBOL|MASSAL?", 440, 190)}
    {lead("h-l4", "aku cek", 1040)}
    {heavy("h-h4", "SATU-SATU.", 1100, 150, "g")}
  </div>
  {flashcard("fl-black", "BLACK OCTOBER", "red", 82)}

  <!-- 01 PHP2SHELL -->
  <div class="scene" id="s-c1">
    {bgimg("im-c1", "php")}
    <div class="chap r" id="ch1"><div class="n">01</div><div class="l">PHP2SHELL</div></div>
    {lead("c1-l1", "pertama,", 360)}
    {heavy("c1-h1", "PHP2SHELL", 420, 170, "r")}
    {logo("lg1", "php", "#FF6B6B", 290, 840, 150)}
    <div class="layer" id="ly1" style="top:660px"><span class="li">{ICON["terminal"]}</span>WordPress &middot; Laravel</div>
    <div class="layer core" id="ly2" style="top:800px"><span class="li">{ICON["bug"]}</span>inti PHP<div class="bugs" style="top:30px"><i id="bg1">{ICON["bug"]}</i><i id="bg2">{ICON["bug"]}</i></div></div>
    <div class="layer" id="ly3" style="top:940px"><span class="li">{ICON["server"]}</span>server</div>
    {mono("c1-m1", "2 CELAH &middot; CVE-2026-109618 / 109619", 1090, 150)}
    <div id="nologin"><span class="ui">{ICON["user"]}</span>LOGIN<i class="strike"></i></div>
    {lead("c1-l2", "percobaan serangan terlihat...", 360)}
    {cal("cal2", 560, range(15, 23), {17: ("hit", "SERANGAN"), 21: ("fix", "PATCH")})}
    <div class="span4" id="c1-span" style="left:{72 + 2 * 118 + 59}px;top:592px;width:{4 * 118}px"></div>
    <div class="spanlbl" id="c1-gap" style="left:{72 + 2 * 118 + 59}px;width:{4 * 118}px;top:870px;text-align:center">4 HARI LEBIH DULU</div>
    {stamp("st1", "NYATA &middot; DIINCAR", "r", "alert", 1180)}
  </div>

  <!-- 02 PLEX -->
  <div class="scene" id="s-c2">
    {bgimg("im-c2", "plex")}
    <div class="chap r" id="ch2"><div class="n">02</div><div class="l">PLEX2SHELL</div></div>
    {lead("c2-l1", "kedua,", 360)}
    {heavy("c2-h1", "PLEX", 420, 200, "r")}
    {logo("lg2", "plex", "#FF6B6B", 290, 840, 150)}
    {stamp("st2", "BUKAN TEORI", "r", "alert", 640)}
    {mono("c2-m1", "CISA KEV &middot; 20 OKT 2026", 760)}
    <div class="persp"><div class="panel r" id="rig"><div class="hd"><span class="ico">{ICON["server"]}</span>SERVER BELUM UPDATE</div>
      <div class="cpu">CPU</div><div class="bar"><i></i></div><div class="pct" id="pct">12%</div>
      <div class="proc" id="proc">&gt; miner + proxy berjalan</div></div></div>
    {"".join(f'<div class="coin" id="cn{k}" style="left:{200 + k * 170}px;top:1290px">{ICON["coin"]}</div>' for k in range(4))}
    {lead("c2-l2", "padahal patch-nya udah ada dari", 640)}
    <div class="persp"><div class="panel mini" id="mn1" style="left:110px;top:720px"><div class="m1">PATCH TERSEDIA</div><div class="m2" style="color:var(--green)">3 AGU</div><div class="mi" style="color:var(--green)">{ICON["check"]}</div></div>
      <div class="panel mini r" id="mn2" style="left:570px;top:720px"><div class="m1">MASIH DISERANG</div><div class="m2" style="color:#FFE2E2">OKT</div><div class="mi" style="color:var(--red)">{ICON["alert"]}</div></div></div>
  </div>

  <!-- 03 GITLAB -->
  <div class="scene" id="s-c3">
    <div class="chap a" id="ch3"><div class="n">03</div><div class="l">GITLAB</div></div>
    {lead("c3-l1", "ketiga,", 360)}
    {heavy("c3-h1", "GITLAB", 420, 200, "a")}
    {logo("lg3", "gitlab", "#FFAA2C", 290, 860, 120)}
    <div id="gauge"><svg viewBox="0 0 600 340"><path d="M60 300 A240 240 0 0 1 540 300" stroke="rgba(255,255,255,.1)" stroke-width="34" fill="none" stroke-linecap="round"/>
      <path id="garc" d="M60 300 A240 240 0 0 1 540 300" stroke="url(#gg)" stroke-width="34" fill="none" stroke-linecap="round" stroke-dasharray="754" stroke-dashoffset="754"/>
      <defs><linearGradient id="gg" x1="0" x2="1"><stop offset="0" stop-color="#FFAA2C"/><stop offset="1" stop-color="#FF4A4A"/></linearGradient></defs></svg>
      <div class="num" id="gnum">0.0</div><div class="sub">SKOR CVSS v3.1 &middot; MAKS 10</div></div>
    <div class="persp"><div class="panel a" id="evid"><div class="e1">BUKTI DIPAKAI MENYERANG</div><div class="e2"><span class="ico">{ICON["search"]}</span>BELUM ADA</div></div></div>
    {stamp("st3", "MASIH POTENSI", "a", "alert", 1360)}
  </div>
  {flashcard("fl-tapi", "TAPI...", "amber")}

  <!-- 04 eMUDHRA -->
  <div class="scene" id="s-c4">
    {bgimg("im-c4", "emudhra")}
    <div class="chap a" id="ch4"><div class="n">04</div><div class="l">eMUDHRA</div></div>
    {lead("c4-l1", "keempat, sertifikat", 360)}
    {heavy("c4-h1", "EMUDHRA", 420, 190, "a")}
    <div id="keyw"><div class="kk">{ICON["key"]}</div><div class="cnt" id="kcnt">1</div><div class="cl">TEBAKAN UNTUK KUNCI RAHASIA</div>
      <div class="lk"><span class="ico" id="lk-c">{ICON["lock"]}</span><span class="ico" id="lk-o" style="opacity:0">{ICON["unlock"]}</span></div></div>
    <div class="persp"><div class="panel" id="browser"><div class="bar"><i></i><i></i><i></i><span></span></div>
      <div class="bd"><span class="ico">{ICON["shield"]}</span><div><b>DIBLOKIR</b><em>8 SERTIFIKAT &middot; CHROME, FIREFOX, APPLE</em></div></div></div></div>
    {stamp("st4", "MASIH POTENSI", "a", "alert", 1420)}
  </div>

  <!-- OUTRO -->
  <div class="scene" id="s-out">
    {lead("o-l1", "jadi,", 300)}
    {heavy("o-h1", "ANCAMANNYA NYATA", 360, 120, "r")}
    <div class="row r" id="rw1" style="top:520px"><span class="rlogo" style="background:#FF6B6B;-webkit-mask:url(logos/php.svg) center/contain no-repeat;mask:url(logos/php.svg) center/contain no-repeat"></span><span class="rt">PHP2Shell</span><span class="rv">NYATA</span></div>
    <div class="row r" id="rw2" style="top:636px"><span class="rlogo" style="background:#FF6B6B;-webkit-mask:url(logos/plex.svg) center/contain no-repeat;mask:url(logos/plex.svg) center/contain no-repeat"></span><span class="rt">Plex</span><span class="rv">NYATA</span></div>
    <div class="row a" id="rw3" style="top:752px"><span class="rlogo" style="background:#FFAA2C;-webkit-mask:url(logos/gitlab.svg) center/contain no-repeat;mask:url(logos/gitlab.svg) center/contain no-repeat"></span><span class="rt">GitLab</span><span class="rv">POTENSI</span></div>
    <div class="row a" id="rw4" style="top:868px"><span class="rt">eMudhra</span><span class="rv">POTENSI</span></div>
    <div id="massal">{heavy("o-h2", "JEBOL MASSAL?", 0, 120).replace('style="top:0px;', 'style="position:relative;top:0;', 1)}<i class="strike"></i></div>
    {heavy("o-h3", "BERLEBIHAN.", 1200, 140, "g")}
    {lead("o-l2", "yang penting:", 1060)}
    <div class="todo" id="td1" style="top:1150px"><span class="tb">{ICON["check"]}</span>cek teknologi kamu</div>
    <div class="todo" id="td2" style="top:1270px"><span class="tb">{ICON["check"]}</span>terus update</div>
  </div>
  </div>

  <div id="whiteflash"></div><div id="redflash"></div>
  <div id="brand">Endrich<b>Tech</b></div>
  <div id="vig"></div>

  <script src="vendor/gsap.min.js"></script>
  <script>
  (function () {{
    var D = {json.dumps(DATA)};
    var FPS = 30, T = D.T, S = D.S;
    function q(t) {{ return Math.round(t * FPS) / FPS; }}
    var tl = gsap.timeline({{ paused: true }});
    var NI = {{ immediateRender: false }};
    function cut(sel, t, v) {{ tl.set(sel, {{ opacity: v }}, q(t)); }}
    function hide(sel, t, d) {{ tl.to(sel, {{ opacity: 0, filter: "blur(8px)", duration: d || 0.16, ease: "power2.in" }}, q(t)); }}
    function fade(sel, t, d, from) {{
      tl.fromTo(sel, Object.assign({{ opacity: 0, y: 30, filter: "blur(12px)" }}, from || {{}}),
        {{ opacity: 1, y: 0, x: 0, scale: 1, filter: "blur(0px)", duration: d || 0.35, ease: "power3.out" }}, q(t));
    }}
    function pop(sel, t, d) {{ tl.fromTo(sel, {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: d || 0.34, ease: "back.out(2.2)" }}, q(t)); }}
    function sweep(sel, t, d) {{
      var chars = document.querySelectorAll(sel + " .ch");
      tl.set(sel, {{ opacity: 1 }}, q(t));
      tl.fromTo(chars, {{ opacity: 0, x: -14, filter: "blur(14px)" }},
        {{ opacity: 1, x: 0, filter: "blur(0px)", duration: 0.26, ease: "power3.out", stagger: Math.min(0.035, (d || 0.45) / chars.length) }}, q(t));
    }}
    function lead(sel, t) {{ fade(sel, t, 0.3, {{ y: 14 }}); }}
    function flash(t, sel, a) {{ tl.fromTo(sel || "#whiteflash", {{ opacity: a || 0.3 }}, Object.assign({{ opacity: 0, duration: 0.25, ease: "power2.out" }}, NI), q(t)); }}
    function kick(t, x) {{ tl.fromTo("#cam", {{ x: x || -8 }}, Object.assign({{ x: 0, duration: 0.28, ease: "elastic.out(1, .3)" }}, NI), q(t)); }}
    function stampIn(sel, t, red) {{
      tl.fromTo(sel, {{ opacity: 0, scale: 1.7, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.24, ease: "power4.in" }}, q(t));
      flash(t + 0.24, red ? "#redflash" : "#whiteflash", red ? 0.22 : 0.28); kick(t + 0.24);
    }}
    function tilt(sel, t, ry, rx) {{
      tl.fromTo(sel, {{ opacity: 0, rotationY: ry * 2.2, rotationX: rx * 2, z: -300, y: 80 }},
        {{ opacity: 1, rotationY: ry, rotationX: rx, z: 0, y: 0, duration: 0.6, ease: "power3.out" }}, q(t));
    }}
    function chapter(sel, t, d) {{
      tl.fromTo(sel, {{ opacity: 0, scale: 1.25, filter: "blur(16px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "power3.out" }}, q(t));
      tl.to(sel, {{ opacity: 0, scale: 0.92, filter: "blur(10px)", duration: 0.18, ease: "power2.in" }}, q(t + d));
    }}
    function scene(id, k) {{ cut(id, S[k][0], 1); cut(id, S[k][1], 0); }}
    function push(k, amt) {{ tl.fromTo("#cam", {{ scale: 1 }}, Object.assign({{ scale: 1 + (amt || 0.05), duration: S[k][1] - S[k][0], ease: "none" }}, NI), q(S[k][0])); }}
    function tint(name, t) {{
      ["#t-gold", "#t-red", "#t-amber"].forEach(function (id) {{ tl.to(id, {{ opacity: id === name ? 1 : 0, duration: 0.5 }}, q(t)); }});
    }}
    function counter(sel, t, d, a, b, dec, suffix) {{
      var o = {{ v: a }}, el = document.querySelector(sel);
      tl.to(o, {{ v: b, duration: d, ease: "power2.out", onUpdate: function () {{ el.textContent = (dec ? o.v.toFixed(1) : Math.round(o.v)) + (suffix || ""); }} }}, q(t));
    }}
    function calIn(id, t) {{
      fade(id, t, 0.35, {{ y: 30 }});
      tl.fromTo(id + " .day", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.25, stagger: 0.03, ease: "power2.out" }}, q(t));
    }}
    function mark(id, day, t, color) {{
      tl.to(id + "-d" + day, {{ borderColor: color, backgroundColor: color === "#FF4A4A" ? "rgba(255,74,74,.18)" : "rgba(89,227,140,.16)",
        boxShadow: "0 0 30px " + color, scale: 1.08, duration: 0.25, ease: "back.out(2)" }}, q(t));
      tl.fromTo(id + "-d" + day + " i", {{ opacity: 0, y: -8 }}, {{ opacity: 1, y: 0, duration: 0.2 }}, q(t + 0.1));
    }}

    document.querySelectorAll(".dust").forEach(function (p, k) {{
      tl.fromTo(p, {{ y: 0 }}, {{ y: -260 - (k % 7) * 40, duration: D.DUR, ease: "none" }}, 0);
      tl.to(p, {{ opacity: 0.08, duration: 1.6 + (k % 5) * 0.4, yoyo: true, repeat: Math.floor(D.DUR / (1.6 + (k % 5) * 0.4)) - 1, ease: "sine.inOut" }}, (k % 9) * 0.2);
    }});

    // ---------- HOOK ----------
    scene("#s-hook", "hook"); push("hook", 0.06); tint("#t-red", 0);
    lead("#h-l1", T[0]); sweep("#h-h1", T[0] + 0.1, 0.3);
    calIn("#cal1", T[2]);
    mark("#cal1", 21, T[3], "#59E38C");
    mark("#cal1", 17, T[5], "#FF4A4A"); flash(T[5] + 0.05, "#redflash", 0.18); kick(T[5] + 0.05, 10);
    tl.to("#h-span", {{ scaleX: 1, duration: 0.5, ease: "power2.out" }}, q(T[8]));
    hide("#h-l1, #h-h1, #cal1, #h-span", T[10] - 0.12, 0.12);
    lead("#h-l2", T[10]);
    // "BLACK OCTOBER" — red flash card, then the glowing headline
    cut("#fl-black", T[14] - 0.05, 1); cut("#fl-black", T[16] - 0.05, 0);
    tl.fromTo("#fl-black .frs", {{ y: 60 }}, {{ y: -60, duration: T[16] - T[14], ease: "none" }}, q(T[14] - 0.05));
    cut("#h-l2", T[14] - 0.05, 0);
    lead("#h-l3", T[16] + 0.1); sweep("#h-h3", T[20], 0.4);
    lead("#h-l4", T[22]); sweep("#h-h4", T[24], 0.35);

    // HUD
    fade("#hud", S.c1[0] + 0.9, 0.3, {{ x: -30, y: 0 }}); cut("#hud", S.out[0], 0);
    [["#dot1", "c1", "r"], ["#dot2", "c2", "r"], ["#dot3", "c3", "a"], ["#dot4", "c4", "a"]].forEach(function (d) {{
      tl.set(d[0], {{ className: d[2] }}, q(S[d[1]][0]));
    }});

    // ---------- 01 PHP2SHELL ----------
    scene("#s-c1", "c1"); push("c1", 0.05);
    chapter("#ch1", S.c1[0], 0.7);
    lead("#c1-l1", S.c1[0] + 0.75); sweep("#c1-h1", T[26], 0.4); pop("#lg1", T[26] + 0.35, 0.4);
    fade("#ly1", T[27], 0.3, {{ x: -40, y: 0 }}); fade("#ly2", T[27] + 0.12, 0.3, {{ x: -40, y: 0 }}); fade("#ly3", T[27] + 0.24, 0.3, {{ x: -40, y: 0 }});
    pop("#bg1", T[28], 0.3); pop("#bg2", T[28] + 0.2, 0.3); fade("#c1-m1", T[30], 0.3, {{ y: 10 }});
    tl.to("#ly3", {{ borderColor: "#FF4A4A", backgroundColor: "rgba(255,74,74,.12)", boxShadow: "0 0 40px rgba(255,74,74,.4)", duration: 0.3 }}, q(T[33]));
    flash(T[33], "#redflash", 0.15);
    fade("#nologin", T[36], 0.3);
    tl.to("#nologin .strike", {{ scaleX: 1, duration: 0.22, ease: "power2.out" }}, q(T[37]));
    hide("#c1-l1, #c1-h1, #ly1, #ly2, #ly3, #c1-m1, #nologin", T[38] - 0.12, 0.12);
    lead("#c1-l2", T[38]);
    calIn("#cal2", T[38] + 0.1);
    mark("#cal2", 17, T[44], "#FF4A4A"); kick(T[44] + 0.1, 8);
    mark("#cal2", 21, T[51], "#59E38C");
    tl.to("#c1-span", {{ scaleX: 1, duration: 0.5, ease: "power2.out" }}, q(T[51] + 0.1));
    fade("#c1-gap", T[51] + 0.3, 0.3, {{ y: 14 }});
    stampIn("#st1", T[53] + 0.15, true);

    // ---------- 02 PLEX ----------
    scene("#s-c2", "c2"); push("c2", 0.05);
    chapter("#ch2", S.c2[0], 0.6);
    lead("#c2-l1", S.c2[0] + 0.65); sweep("#c2-h1", T[55], 0.3); pop("#lg2", T[55] + 0.3, 0.4);
    stampIn("#st2", T[58], true); fade("#c2-m1", T[59] + 0.2, 0.3, {{ y: 10 }});
    tilt("#rig", T[61], -12, 6);
    tl.to("#rig .bar i", {{ scaleX: 1, duration: 1.4, ease: "power2.in" }}, q(T[65]));
    counter("#pct", T[65], 1.4, 12, 100, false, "%");
    fade("#proc", T[67], 0.25, {{ y: 10 }});
    [0, 1, 2, 3].forEach(function (k) {{
      tl.fromTo("#cn" + k, {{ opacity: 0, y: 40, scale: 0.5 }}, {{ opacity: 1, y: -30, scale: 1, duration: 0.4, ease: "back.out(2)" }}, q(T[67] + 0.12 * k));
    }});
    hide("#cn0, #cn1, #cn2, #cn3", T[69] - 0.1, 0.15);
    hide("#st2, #c2-m1, #rig", T[69] - 0.1, 0.12);
    lead("#c2-l2", T[69]);
    tilt("#mn1", T[70], 14, 6); tilt("#mn2", T[74] - 0.1, -14, 6);

    // ---------- 03 GITLAB (amber) ----------
    scene("#s-c3", "c3"); push("c3", 0.05); tint("#t-amber", S.c3[0]);
    chapter("#ch3", S.c3[0], 0.6);
    lead("#c3-l1", S.c3[0] + 0.65); sweep("#c3-h1", T[76], 0.35); pop("#lg3", T[76] + 0.3, 0.4);
    fade("#gauge", T[77], 0.3, {{ y: 30 }});
    tl.to("#garc", {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 1.0, ease: "power2.out" }}, q(T[77] + 0.1));
    counter("#gnum", T[77] + 0.1, 1.0, 0, 10, true);
    tl.to("#gauge .num", {{ scale: 1.12, duration: 0.15, yoyo: true, repeat: 1 }}, q(T[80]));
    flash(T[80], "#redflash", 0.14);
    // "Tapi..." amber flash card
    cut("#fl-tapi", T[81], 1); cut("#fl-tapi", T[82] - 0.1, 0);
    tl.fromTo("#fl-tapi .frs", {{ y: -60 }}, {{ y: 60, duration: T[82] - T[81], ease: "none" }}, q(T[81]));
    tilt("#evid", T[82], 12, 6);
    stampIn("#st3", T[91] - 0.1);

    // ---------- 04 eMUDHRA ----------
    scene("#s-c4", "c4"); push("c4", 0.05);
    chapter("#ch4", S.c4[0], 0.6);
    lead("#c4-l1", S.c4[0] + 0.65); sweep("#c4-h1", T[94], 0.35);
    fade("#keyw", T[95], 0.35, {{ y: 30 }});
    counter("#kcnt", T[97], T[107] - T[97], 1, 256, false);
    cut("#lk-c", T[107] + 0.1, 0); cut("#lk-o", T[107] + 0.1, 1);
    tl.fromTo("#keyw .lk", {{ scale: 1.3, rotation: -12 }}, {{ scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2)", immediateRender: false }}, q(T[107] + 0.1));
    flash(T[107] + 0.1, "#redflash", 0.18); kick(T[107] + 0.12, 10);
    tilt("#browser", T[108], -12, 6);
    stampIn("#st4", T[115]);

    // ---------- OUTRO ----------
    scene("#s-out", "out"); push("out", 0.04); tint("#t-gold", S.out[0]);
    lead("#o-l1", T[117]); sweep("#o-h1", T[118], 0.45);
    [1, 2, 3, 4].forEach(function (k) {{ fade("#rw" + k, T[118] + 0.12 * k, 0.3, {{ x: -40, y: 0 }}); }});
    cut("#massal", T[121], 1); sweep("#o-h2", T[121], 0.4);
    tl.to("#massal .strike", {{ scaleX: 1, duration: 0.25, ease: "power2.out" }}, q(T[124]));
    sweep("#o-h3", T[125], 0.35); kick(T[125] + 0.2, -8);
    hide("#massal, #o-h3", T[126] - 0.12, 0.12);
    lead("#o-l2", T[126]);
    fade("#td1", T[128], 0.3, {{ x: -40, y: 0 }}); tl.fromTo("#td1 .tb .ico", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, q(T[133]));
    fade("#td2", T[134], 0.3, {{ x: -40, y: 0 }}); tl.fromTo("#td2 .tb .ico", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, q(T[135] + 0.3));

    [["#im-hook", "hook"], ["#im-c1", "c1"], ["#im-c2", "c2"], ["#im-c4", "c4"]].forEach(function (b) {{
      if (!document.querySelector(b[0])) return;
      tl.fromTo(b[0], {{ opacity: 0 }}, {{ opacity: 0.55, duration: 0.8, ease: "power1.out" }}, q(S[b[1]][0] + 0.2));
      tl.fromTo(b[0] + " img", {{ scale: 1.0 }}, {{ scale: 1.08, duration: S[b[1]][1] - S[b[1]][0], ease: "none" }}, q(S[b[1]][0]));
    }});

    window.__timelines = window.__timelines || {{}};
    window.__timelines["black-october"] = tl;
  }})();
  </script>
</div>
</body>
</html>
'''
(HERE / "public" / "index.html").write_text(HTML, encoding="utf-8")
print("DUR", DUR, {k: (round(a, 2), round(b, 2)) for k, (a, b) in S.items()})
