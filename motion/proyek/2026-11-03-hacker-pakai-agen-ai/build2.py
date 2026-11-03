# Hari 3 v2 · gaya mengikuti video referensi Endrich (ref/referensi.mp4):
#  - latar berganti krem kertas (#EEECE6) / hitam (#161616) / merah (#E5401D, CTA), tekstur halftone
#  - baris header mono kecil "// 01 — ..." kiri + progres "KASUS 1/2" kanan
#  - teks besar kiri atas, muncul kata per kata, kata aksen serif italic merah  (di sini: frasa KATA KUNCI, bukan subtitle)
#  - tengah: kartu UI ilustratif garis hitam tebal + bayangan keras, aksen merah, masuk dengan spring/rotasi
#  - kiri bawah: badge brand tetap; kanan bawah: karakter besar (chibi Endrich) ganti pose per beat + lip-flap dari VO
# Timing dari vo/align.json (perkiraan dari vo/vo-full.mp3, lihat align.py).
import json
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
FPS, W, H = 30, 1080, 1920
A = json.loads((HERE / "vo" / "align.json").read_text(encoding="utf-8"))["words"]
WS = [a["start"] for a in A]
VO_DUR = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                        str(HERE / "vo" / "vo-full.mp3")]))
DUR = round(VO_DUR + 1.6, 2)


def clean(w):
    return w.lower().strip(".,?!\"'…").replace("...", "")


def idx(word, after=0):
    for i in range(after, len(A)):
        if clean(A[i]["word"]) == word:
            return i
    raise KeyError(word)


def t(word, after=0):
    return WS[idx(word, after)]


# ---- beat anchors (follow the actual VO order)
i_pad = idx("padahal"); i_tern = idx("ternyata"); i_di = idx("di", i_tern); i_biaya = idx("biaya")
i_gila = idx("gila"); i_cs = idx("crowdstrike"); i_org = idx("organisasi"); i_sebelas = idx("sebelas")
i_kec = idx("kecepatan"); i_empat = idx("empat"); i_jadi = idx("jadi", i_empat); i_tapi = idx("tapi")
i_ainya = idx("ai-nya"); i_manusia = idx("manusia"); i_makanya = idx("makanya"); i_update = idx("update")
i_batasi = idx("batasi"); i_backup = idx("backup"); i_besok = idx("besok"); i_melawan = idx("melawan")
i_follow = idx("follow"); i_kalau = idx("kalau"); i_data = idx("data", i_kalau); i_atau = idx("atau", i_kalau)
i_nggak1 = idx("nggak"); i_seratus2 = idx("seratus", i_di); i_dua2 = idx("dua", i_cs)

B = {  # beat start times
    "b0": 0.0, "b1": WS[i_pad] - 0.1, "b2": WS[i_tern - 1] - 0.1, "b3": WS[i_di] - 0.1, "b4": WS[i_gila - 3] - 0.1,
    "b5": WS[i_kec] - 0.1, "b6": WS[i_tapi] - 0.1, "b7": WS[i_ainya] - 0.1, "b8": WS[i_makanya] - 0.1,
    "b9": WS[i_besok] - 0.1, "b10": WS[i_follow] - 0.1, "b11": WS[i_kalau] - 0.1,
}
K = {  # word cue times used by the timeline
    "agen": t("agen"), "seribu": t("seribu"), "situs": t("situs"), "perintah": t("perintah"), "nggak1": WS[i_nggak1],
    "seratus1": t("seratus"), "pertama": t("pertama"), "seratus2": WS[i_seratus2], "ditembus": t("ditembus"),
    "biaya": WS[i_biaya], "lima": t("lima", i_biaya), "cs": WS[i_cs], "dua2": WS[i_dua2], "sebelas": WS[i_sebelas],
    "empat": WS[i_empat], "jadi": WS[i_jadi], "tahu": t("tahu"), "mempercepat": t("mempercepat"), "manusia": WS[i_manusia],
    "target": t("targetnya"), "penting": t("penting"), "update": WS[i_update], "batasi": WS[i_batasi],
    "backup": WS[i_backup], "melawan": WS[i_melawan], "ketinggalan": t("ketinggalan"), "data": WS[i_data],
    "atau": WS[i_atau], "khawatir": t("khawatir"),
}
print({k: round(v, 2) for k, v in B.items()})

# ---- chibi: pose per beat + lip-flap from VO loudness
raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(HERE / "vo" / "vo-full.mp3"), "-ac", "1", "-ar", "48000",
                               "-f", "s16le", "-"])
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
hop = 48000 // FPS
db = np.array([20 * np.log10(np.sqrt((x[i:i + hop] ** 2).mean()) + 1e-9) for i in range(0, len(x) - hop, hop)])
loud = db > db.max() - 24
sm = np.convolve(db, np.ones(7) / 7, mode="same")
open_ = loud & (db >= sm - 1.0)
EMPH = [  # (start, pose, hold seconds)
    (B["b0"] + 0.05, "tunjuk", 1.6), (K["seribu"], "kaget", 1.0), (B["b1"], "mikir", 1.4), (K["nggak1"], "kaget", 0.9),
    (B["b2"] + 0.2, "tunjuk", 1.0), (K["seratus2"], "kaget", 1.0), (K["biaya"] + 0.5, "keren", 0.9),
    (K["cs"], "tunjuk", 1.0), (K["sebelas"], "kaget", 0.9), (K["jadi"], "kaget", 1.1), (B["b6"], "mikir", 2.0),
    (K["manusia"], "tunjuk", 1.1), (K["backup"] + 0.3, "keren", 1.1), (B["b9"], "tunjuk", 1.2),
    (B["b10"], "lambai", 1.6), (K["khawatir"], "mikir", 99),
]
BLINK = [3.4, 9.2, 16.4, 25.0, 31.4, 38.8, 45.2, 51.0]
track, prev, hold = [], None, 0
for f in range(int(DUR * FPS) + 1):
    tt = f / FPS
    p = "netral"
    for s, name, hd in EMPH:
        if s <= tt < s + hd:
            p = name
    if p == "netral":
        want = "bicara" if f < len(open_) and open_[f] else "netral"
        if prev in ("netral", "bicara") and want != prev and hold < 2:
            want = prev
        if any(b <= tt < b + 0.13 for b in BLINK):
            want = "kedip"
        p = want
    hold = hold + 1 if p == prev else 1
    if p != prev:
        track.append([round(tt, 3), p])
    prev = p
EMPH_T = [round(s, 3) for s, _, _ in EMPH]

FONTS = '''@font-face { font-family: "IDMed"; src: url("fonts/InterDisplay-Medium.ttf"); font-display: block; }
@font-face { font-family: "IDSemi"; src: url("fonts/InterDisplay-SemiBold.ttf"); font-display: block; }
@font-face { font-family: "IDBold"; src: url("fonts/InterDisplay-Bold.ttf"); font-display: block; }
@font-face { font-family: "IDBlack"; src: url("fonts/InterDisplay-Black.ttf"); font-display: block; }
@font-face { font-family: "Serif"; src: url("fonts/SerifBI.ttf"); font-display: block; }
@font-face { font-family: "Mono"; src: url("fonts/JetBrainsMono-Regular.ttf"); font-display: block; }
@font-face { font-family: "MonoB"; src: url("fonts/JetBrainsMono-Bold.ttf"); font-display: block; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow: hidden; background: #EEECE6; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; }'''

CSS = '''
:root { --paper:#EEECE6; --ink:#121212; --red:#E5401D; --dark:#161616; --mut:#8A877F; --card:#FBFAF7; }
#root { font-family: "IDMed"; color: var(--ink); }
.bg { position: absolute; inset: 0; opacity: 0; }
#bgP { background: var(--paper); opacity: 1; }
#bgD { background: var(--dark); }
#bgR { background: var(--red); }
.dots { position: absolute; inset: 0; pointer-events: none;
  background-image: radial-gradient(circle, rgba(0,0,0,.16) 2.2px, transparent 2.6px); background-size: 14px 14px;
  -webkit-mask-image: radial-gradient(ellipse 60% 45% at 85% 88%, #000 0%, transparent 70%); }
#bgD .dots { background-image: radial-gradient(circle, rgba(255,255,255,.10) 2.2px, transparent 2.6px);
  -webkit-mask-image: radial-gradient(ellipse 55% 40% at 80% 80%, #000 0%, transparent 70%); }
#bgR .dots { background-image: radial-gradient(circle, rgba(0,0,0,.18) 2.2px, transparent 2.6px); }
#grain { position: absolute; inset: 0; opacity: .07; pointer-events: none; z-index: 60;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
/* header row */
#hdr { position: absolute; left: 70px; top: 262px; width: 860px; height: 30px; font-family: "Mono"; font-size: 24px; color: var(--mut); z-index: 40; }
#hdr .hl.r { left: auto; right: 0; letter-spacing: .06em; }
#hdr .r b { color: var(--red); font-family: "MonoB"; font-weight: normal; }
.hl { position: absolute; left: 0; top: 0; white-space: nowrap; opacity: 0; }
/* headline */
.head { position: absolute; left: 70px; top: 330px; width: 860px; font-family: "IDMed"; font-size: 74px; line-height: 1.08; letter-spacing: -.015em; color: var(--ink); opacity: 0; }
.head span { display: inline-block; opacity: 0; margin-right: .22em; }
.head i { font-family: "Serif"; font-style: normal; color: var(--red); letter-spacing: 0; }
.dk .head, .dk.head { color: #F3F1EC; }
.rd .head i { color: var(--ink); }
.rd .head { color: #fff; }
/* scenes */
.sc { position: absolute; inset: 0; opacity: 0; }
.card { position: absolute; background: var(--card); border: 4px solid var(--ink); border-radius: 22px; box-shadow: 12px 12px 0 var(--ink); }
.dk .card { box-shadow: 12px 12px 0 #000; border-color: #000; }
.tab { position: absolute; left: 26px; top: -46px; height: 46px; padding: 0 18px; border: 4px solid var(--ink); border-bottom: none; border-radius: 12px 12px 0 0; background: var(--red); color: #fff; font-family: "MonoB"; font-size: 22px; line-height: 42px; }
.pill { position: absolute; height: 72px; padding: 0 26px; border: 4px solid var(--ink); border-radius: 40px; background: #fff; font-family: "IDBold"; font-size: 38px; line-height: 64px; box-shadow: 6px 6px 0 var(--ink); white-space: nowrap; }
.pill b { color: var(--red); font-weight: normal; }
.num { font-variant-numeric: tabular-nums; }
.lbl { position: absolute; font-family: "MonoB"; font-size: 20px; letter-spacing: .14em; color: var(--mut); }
/* b0: shop windows fan */
.shop { width: 300px; height: 380px; }
.shop .bar { height: 46px; border-bottom: 4px solid var(--ink); display: flex; align-items: center; gap: 9px; padding: 0 16px; }
.shop .bar i { width: 13px; height: 13px; border-radius: 50%; border: 3px solid var(--ink); }
.shop .ban { margin: 16px; height: 120px; border-radius: 12px; background: repeating-linear-gradient(45deg, #E9E5DC 0 10px, #DED9CE 10px 20px); border: 3px solid var(--ink); }
.shop .row { margin: 0 16px 12px; height: 18px; border-radius: 9px; background: #D9D4C9; }
.shop .row.s { width: 55%; }
.shop .btn { margin: 14px 16px; width: 120px; height: 40px; border-radius: 20px; background: var(--red); border: 3px solid var(--ink); }
.shop .tg { position: absolute; right: 14px; top: 9px; font-family: "MonoB"; font-size: 17px; color: var(--mut); }
/* b1: prompt terminal */
#term { left: 70px; top: 640px; width: 860px; height: 300px; background: #1B1B1B; border-color: var(--ink); color: #EDEBE5; }
#term .tb { height: 56px; border-bottom: 3px solid #333; display: flex; align-items: center; gap: 10px; padding: 0 20px; font-family: "Mono"; font-size: 22px; color: #888; }
#term .tb i { width: 14px; height: 14px; border-radius: 50%; background: var(--red); }
#term .tb i + i { background: #555; } #term .tb i + i + i { background: #555; }
#term .bd { padding: 30px 30px; font-family: "MonoB"; font-size: 40px; line-height: 1.5; }
#term .bd .pr { color: var(--red); }
#red { color: #CFCBC2; letter-spacing: .02em; }
.cur { display: inline-block; width: 20px; height: 40px; background: #EDEBE5; vertical-align: -6px; margin-left: 4px; }
#cnt1 { left: 70px; top: 1000px; }
#sim { left: 760px; top: 960px; color: #999; }
/* b2 cards */
.kcard { width: 360px; height: 470px; display: flex; align-items: center; justify-content: center; flex-direction: column; }
.kcard .big { font-family: "IDBlack"; font-size: 120px; line-height: 1; }
.kcard .sm { font-family: "MonoB"; font-size: 26px; letter-spacing: .1em; margin-top: 18px; color: var(--mut); }
#kc1 { left: 110px; top: 610px; } #kc2 { left: 540px; top: 640px; background: #2A2A2A; color: #fff; }
#kc2 .big { font-family: "Serif"; color: var(--red); font-size: 220px; }
/* b3 grid of mini shops */
#mgrid { position: absolute; left: 90px; top: 600px; width: 840px; display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }
#mgrid .m { height: 120px; border: 3px solid #000; border-radius: 12px; background: #F4F2EC; position: relative; overflow: hidden; opacity: 0; }
#mgrid .m:before { content: ""; position: absolute; left: 0; right: 0; top: 0; height: 24px; border-bottom: 3px solid #000; background: #E2DED4; }
#mgrid .m b { position: absolute; inset: 0; background: var(--red); opacity: 0; font-family: "MonoB"; font-weight: normal; font-size: 18px; color: #fff; display: flex; align-items: center; justify-content: center; letter-spacing: .08em; }
#price { left: 120px; top: 1010px; width: 600px; height: 250px; padding: 30px 36px; }
#price .v { font-family: "IDBlack"; font-size: 110px; line-height: 1; }
#price .v small { font-family: "Serif"; font-size: 70px; color: var(--red); margin-right: 6px; }
#price .k { font-family: "MonoB"; font-size: 23px; letter-spacing: .08em; color: var(--mut); margin-top: 14px; }
#price .hole { position: absolute; right: 30px; top: 30px; width: 34px; height: 34px; border-radius: 50%; border: 4px solid var(--ink); background: var(--dark); }
/* b4 calendar */
#cal { left: 70px; top: 650px; width: 860px; height: 420px; padding: 80px 30px 30px; }
#cal .cg { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 14px; }
#cal .d { height: 120px; border: 3px solid var(--ink); border-radius: 12px; font-family: "MonoB"; font-size: 26px; padding: 10px 12px; position: relative; overflow: hidden; background: #fff; }
#cal .d s { position: absolute; inset: 0; background: var(--red); transform: scaleY(0); transform-origin: 50% 100%; }
#cal .d em { position: relative; font-style: normal; z-index: 2; }
#cal .cap { position: absolute; left: 30px; top: 22px; font-family: "MonoB"; font-size: 24px; letter-spacing: .1em; color: var(--mut); }
#orgp { left: 70px; top: 1130px; }
#src4 { left: 70px; top: 1230px; }
/* b5 gauge */
#gauge { left: 120px; top: 620px; width: 760px; height: 560px; }
#gauge svg { position: absolute; left: 40px; top: 40px; width: 680px; height: 380px; overflow: visible; }
#gauge .gv { position: absolute; left: 0; width: 760px; top: 330px; text-align: center; font-family: "IDBlack"; font-size: 110px; }
#gauge .gk { position: absolute; left: 0; width: 760px; top: 455px; text-align: center; font-family: "MonoB"; font-size: 24px; letter-spacing: .1em; color: var(--mut); }
#gauge .was { position: absolute; left: 40px; top: 508px; font-family: "MonoB"; font-size: 24px; color: var(--mut); }
#src5 { left: 70px; top: 1330px; }
/* b6 */
#bub { position: absolute; left: 560px; top: 1030px; width: 190px; height: 110px; border: 4px solid #000; border-radius: 55px; background: #fff; box-shadow: 8px 8px 0 #000; display: flex; align-items: center; justify-content: center; gap: 14px; }
#bub i { width: 18px; height: 18px; border-radius: 50%; background: #000; display: block; }
/* b7 flow */
.fc { left: 90px; width: 820px; height: 170px; padding: 0 34px; display: flex; align-items: center; gap: 28px; }
.fc .ic { width: 96px; height: 96px; border-radius: 20px; border: 4px solid var(--ink); display: flex; align-items: center; justify-content: center; font-family: "IDBlack"; font-size: 44px; flex: none; }
.fc .tx { font-family: "IDBold"; font-size: 46px; line-height: 1.1; }
.fc .tx small { display: block; font-family: "Mono"; font-size: 24px; color: var(--mut); margin-top: 8px; }
#fA { top: 620px; } #fA .ic { background: #E9E5DC; }
#fM { top: 900px; } #fM .ic { background: var(--red); color: #fff; }
#fM.on { background: #FFF1EC; }
#fl { position: absolute; left: 180px; top: 802px; width: 6px; height: 96px; background: var(--ink); transform-origin: 50% 0; }
#tgt { position: absolute; left: 720px; top: 1110px; }
/* b8 checklist (reference "is building" card) */
#chk { left: 70px; top: 610px; width: 860px; height: 640px; overflow: hidden; }
#chk .ttl { height: 90px; border-bottom: 4px solid var(--ink); display: flex; align-items: center; padding: 0 30px; font-family: "IDBold"; font-size: 40px; }
#chk .ttl b { color: var(--red); margin-right: 16px; font-weight: normal; }
#chk .ttl .n { margin-left: auto; font-family: "MonoB"; font-size: 30px; color: var(--mut); }
#chk .it { height: 182px; border-bottom: 3px solid #D8D4CA; display: flex; align-items: center; padding: 0 30px; gap: 28px; }
#chk .it:last-child { border-bottom: none; }
#chk .it.cur2 { background: #FBE3DA; }
#chk .ck { width: 64px; height: 64px; border-radius: 50%; border: 4px dashed #B9B4A9; flex: none; display: flex; align-items: center; justify-content: center; font-family: "IDBlack"; font-size: 38px; color: #fff; }
#chk .ck.ok { border: 4px solid var(--ink); background: var(--ink); }
#chk .tx { font-family: "IDBold"; font-size: 46px; }
#chk .tx small { display: block; font-family: "Mono"; font-size: 24px; color: var(--mut); margin-top: 6px; }
/* b9 / b10 */
#p4 { left: 110px; top: 660px; width: 560px; height: 440px; padding: 40px; }
#p4 .k { font-family: "MonoB"; font-size: 26px; letter-spacing: .12em; color: var(--mut); }
#p4 .v { font-family: "IDBlack"; font-size: 96px; line-height: 1; margin-top: 18px; }
#p4 .v i { font-family: "Serif"; font-style: normal; color: var(--red); }
#p4 svg { position: absolute; right: 36px; bottom: 34px; width: 130px; height: 150px; }
#prof { left: 90px; top: 640px; width: 640px; height: 400px; padding: 36px; }
#prof .av { width: 120px; height: 120px; border-radius: 50%; border: 4px solid var(--ink); background: var(--red); display: flex; align-items: center; justify-content: center; font-family: "IDBlack"; font-size: 54px; color: #fff; }
#prof .nm { position: absolute; left: 186px; top: 50px; font-family: "IDBold"; font-size: 46px; }
#prof .hd { position: absolute; left: 186px; top: 110px; font-family: "Mono"; font-size: 26px; color: var(--mut); }
#prof .sr { margin-top: 30px; font-family: "Mono"; font-size: 25px; color: var(--mut); line-height: 1.5; }
#fbtn { position: absolute; left: 36px; right: 36px; bottom: 34px; height: 84px; border-radius: 16px; background: var(--red); border: 4px solid var(--ink); color: #fff; font-family: "IDBold"; font-size: 40px; display: flex; align-items: center; justify-content: center; }
#fbtn.done { background: #fff; color: var(--ink); }
/* b11 comments */
#cm { left: 70px; top: 600px; width: 860px; height: 560px; }
#cm .ct { height: 80px; border-bottom: 3px solid #D8D4CA; text-align: center; font-family: "IDBold"; font-size: 34px; line-height: 76px; }
.cmt { position: absolute; left: 30px; right: 30px; height: 150px; display: flex; gap: 22px; align-items: center; }
.cmt .av { width: 76px; height: 76px; border-radius: 50%; border: 4px solid var(--ink); flex: none; display: flex; align-items: center; justify-content: center; font-family: "IDBlack"; font-size: 38px; }
.cmt .tx { font-family: "IDBold"; font-size: 42px; line-height: 1.12; }
.cmt .tx small { display: block; font-family: "Mono"; font-size: 22px; color: var(--mut); margin-bottom: 6px; }
#cA { top: 110px; } #cA .av { background: var(--ink); color: #fff; }
#cB { top: 290px; } #cB .av { background: var(--red); color: #fff; }
#cin { position: absolute; left: 30px; right: 30px; bottom: 26px; height: 70px; border: 3px solid #D8D4CA; border-radius: 35px; font-family: "Mono"; font-size: 24px; color: var(--mut); line-height: 64px; padding-left: 28px; }
/* persistent brand badge + chibi */
#badge { position: absolute; left: 70px; top: 1440px; width: 330px; height: 118px; z-index: 45; }
#badge .bx { position: absolute; left: 0; top: 0; width: 330px; height: 118px; border: 4px solid var(--ink); border-radius: 16px; background: #fff; box-shadow: 7px 7px 0 var(--ink); }
#badge .nm { position: absolute; left: 22px; top: 70px; font-family: "IDBlack"; font-size: 36px; color: var(--ink); white-space: nowrap; }
#badge .nm b { color: var(--red); font-weight: normal; }
#badge .h { position: absolute; left: 22px; top: 22px; height: 34px; padding: 0 12px; border-radius: 8px; background: var(--red); color: #fff; font-family: "MonoB"; font-size: 20px; line-height: 34px; }
#chibi { position: absolute; left: 430px; top: 1185px; width: 802px; height: 1428px; z-index: 50; transform-origin: 50% 40%; }
#chibiS img { position: absolute; left: 0; top: 0; width: 802px; height: 1428px; opacity: 0; }
#halo { position: absolute; left: 560px; top: 1240px; width: 560px; height: 720px; z-index: 49; opacity: .9;
  background-image: radial-gradient(circle, rgba(0,0,0,.18) 2.4px, transparent 2.8px); background-size: 13px 13px;
  -webkit-mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, #000 0%, transparent 72%); }
.dkC #halo { background-image: radial-gradient(circle, rgba(255,255,255,.14) 2.4px, transparent 2.8px); }
'''

POSES = ["netral", "lambai", "tunjuk", "mikir", "kaget", "keren", "bicara", "kedip"]
imgs = "".join(f'<img id="p_{p}" src="pose/pose_{i}_{p}.png">' for i, p in enumerate(POSES))
SHOP = '<div class="bar"><i></i><i></i><i></i></div><span class="tg">{}</span><div class="ban"></div><div class="row"></div><div class="row s"></div><div class="btn"></div>'
shops = "".join(f'<div class="card shop" id="sh{k}">{SHOP.format(n)}</div>' for k, n in enumerate(["toko-01", "shop.id", "store-77", "mall-x", "butik"]))
mgrid = "".join('<div class="m"><b>TEMBUS</b></div>' for _ in range(20))
HITS = [2, 7, 11, 13, 18]
cal = "".join(f'<div class="d"><s></s><em>{d + 1}</em></div>' for d in range(11)) + '<div class="d" style="border-style:dashed;background:transparent"><em style="color:#B9B4A9">12</em></div>'
BLK = "█"
RED = f"{BLK * 5} {BLK * 3} {BLK * 6} {BLK * 4} {BLK * 7} {BLK * 3}"
SHIELD = '<svg viewBox="0 0 130 150"><path d="M65 6 L120 26 L120 72 C120 108 96 132 65 144 C34 132 10 108 10 72 L10 26 Z" fill="#E5401D" stroke="#121212" stroke-width="7" stroke-linejoin="round"/><path d="M40 76 L58 94 L92 56" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# headlines: list of (scene id, html words, reveal start, reveal end); words split by "|"
HEADS = [
    ("h0", "Satu|orang|+|agen|AI:", B["b0"], K["agen"] + 0.3),
    ("h0b", "<i>1.200+</i>|situs|disasar", K["seribu"], K["situs"] + 0.3),
    ("h1", "Perintahnya|<i>nggak|sampai</i>|100|karakter", B["b1"] + 0.1, K["seratus1"] + 0.4),
    ("h2", "Itu|baru|kasus|<i>pertama.</i>", B["b2"] + 0.1, K["pertama"] + 0.2),
    ("h3", "<i>100+</i>|perusahaan|dilaporkan|tembus", K["seratus2"] - 0.1, K["ditembus"] + 0.2),
    ("h4", "<i>200+</i>|organisasi,|<i>11</i>|hari", K["dua2"], K["sebelas"] + 0.6),
    ("h5", "<i>40</i>|&rarr;|<i>1.500+</i>|perintah/jam", K["empat"], K["jadi"] + 0.8),
    ("h6", "Tapi|ada|satu|hal&hellip;", B["b6"] + 0.05, K["tahu"]),
    ("h7", "AI|mempercepat.|Target|dipilih|<i>manusia.</i>", K["mempercepat"] - 0.6, K["target"] + 0.3),
    ("h8", "Keamanan|dasar|<i>masih|penting</i>", B["b8"] + 0.1, K["penting"] + 0.3),
    ("h9", "Besok:|AI|yang|<i>ngelawan|balik</i>", B["b9"] + 0.1, K["melawan"] + 0.4),
    ("h10", "<i>Follow</i>|biar|nggak|ketinggalan", B["b10"] + 0.05, K["ketinggalan"] + 0.2),
    ("h11", "Punya|bisnis?|Lebih|khawatir|<i>mana?</i>", B["b11"] + 0.1, K["khawatir"] + 0.5),
]


def head_html(hid, words, top=330, extra=""):
    sp = "".join(f"<span>{w}</span>" for w in words.split("|"))
    return f'<div class="head" id="{hid}" style="top:{top}px;{extra}">{sp}</div>'


HDR = [  # (time, left label, right label html)
    (B["b0"], "// 01 &mdash; satu orang &middot; agen AI", "KASUS <b>1</b>/2"),
    (B["b1"], "// 02 &mdash; perintahnya pendek", "KASUS <b>1</b>/2"),
    (B["b3"], "// 03 &mdash; dilaporkan tembus", "KASUS <b>1</b>/2"),
    (B["b4"], "// 04 &mdash; menurut crowdstrike", "KASUS <b>2</b>/2"),
    (B["b6"], "// 05 &mdash; yang perlu kamu tahu", "INTI <b>!</b>"),
    (B["b8"], "// 06 &mdash; keamanan dasar", "CEK <b>3</b>/3"),
    (B["b9"], "// 07 &mdash; seri ai pengawas #3", "PART <b>4</b> BESOK"),
    (B["b11"], "// 08 &mdash; jawab di komentar", "A <b>/</b> B"),
]
hdr_html = "".join(f'<div class="hl" id="hd{k}">{a}</div><div class="hl r" id="hr{k}">{b}</div>' for k, (_, a, b) in enumerate(HDR))

BODY = f'''
  <div class="bg" id="bgP"><div class="dots"></div></div>
  <div class="bg" id="bgD"><div class="dots"></div></div>
  <div class="bg" id="bgR"><div class="dots"></div></div>
  <div id="hdr">{hdr_html}</div>
  <div class="sc" id="s0">{head_html("h0", HEADS[0][1])}{head_html("h0b", HEADS[1][1], 420)}
    {shops}
    <div class="pill" id="pill0" style="left:300px;top:1110px">&#9654; <span class="num" id="c0">0</span> <b>situs</b></div>
  </div>
  <div class="sc" id="s1">{head_html("h1", HEADS[2][1])}
    <div class="card" id="term"><div class="tb"><i></i><i></i><i></i>&nbsp; agen-ai &mdash; perintah</div>
      <div class="bd"><span class="pr">&gt;</span> <span id="red"></span><span class="cur" id="cu"></span></div></div>
    <div class="lbl" id="sim">SIMULASI</div>
    <div class="pill" id="cnt1"><b>&lt; 100</b> karakter</div>
  </div>
  <div class="sc dk" id="s2">{head_html("h2", HEADS[3][1])}
    <div class="card kcard" id="kc1"><div class="tab">KASUS</div><div class="big">#1</div><div class="sm">1.200+ SITUS</div></div>
    <div class="card kcard" id="kc2"><div class="tab">KASUS</div><div class="big">?</div><div class="sm" style="color:#aaa">BERIKUTNYA</div></div>
  </div>
  <div class="sc dk" id="s3">{head_html("h3", HEADS[4][1])}
    <div id="mgrid">{mgrid}</div>
    <div class="card" id="price"><div class="hole"></div><div class="v num"><small>&plusmn;</small>US$<span id="c3">0</span></div><div class="k">BIAYA AI &middot; PERKIRAAN PENELITI</div></div>
    <div class="lbl" style="left:70px;top:1330px;color:#777">sumber: NorForge via Reuters, Okt 2026</div>
  </div>
  <div class="sc" id="s4">{head_html("h4", HEADS[5][1])}
    <div class="card" id="cal"><div class="tab">KALENDER</div><div class="cap">SATU KELOMPOK &middot; 17 OKT &rarr;</div><div class="cg">{cal}</div></div>
    <div class="pill" id="orgp">&#9654; <span class="num" id="c4">0</span>+ <b>organisasi</b></div>
    <div class="lbl" id="src4" style="top:1330px">sumber: CrowdStrike, 29 Okt 2026</div>
  </div>
  <div class="sc" id="s5">{head_html("h5", HEADS[6][1])}
    <div class="card" id="gauge"><div class="tab">KECEPATAN</div>
      <svg viewBox="0 0 680 380"><path d="M40 340 A300 300 0 0 1 640 340" fill="none" stroke="#E2DED4" stroke-width="54"/>
        <path id="garc" d="M40 340 A300 300 0 0 1 640 340" fill="none" stroke="#E5401D" stroke-width="54" stroke-dasharray="943" stroke-dashoffset="943"/>
        <path d="M40 340 A300 300 0 0 1 640 340" fill="none" stroke="#121212" stroke-width="5"/>
        <g id="needle" transform="rotate(-90 340 340)"><path d="M334 340 L340 70 L346 340 Z" fill="#121212"/><circle cx="340" cy="340" r="22" fill="#121212"/></g></svg>
      <div class="gv num"><span id="c5">40</span></div><div class="gk">PERINTAH PER JAM</div><div class="was">dulu (manual): ~40</div></div>
    <div class="lbl" id="src5" style="top:1330px">sumber: CrowdStrike (Adam Meyers), 29 Okt 2026</div>
  </div>
  <div class="sc dk" id="s6">{head_html("h6", HEADS[7][1], 330, "font-size:96px")}<div id="bub"><i></i><i></i><i></i></div></div>
  <div class="sc" id="s7">{head_html("h7", HEADS[8][1])}
    <div class="card fc" id="fA"><div class="ic">AI</div><div class="tx">Agen AI<small>ngerjain cepat, ribuan perintah</small></div></div>
    <div id="fl"></div>
    <div class="card fc" id="fM"><div class="ic">&#9673;</div><div class="tx">Manusia<small>milih target &amp; keputusan penting</small></div></div>
    <div class="pill" id="tgt"><b>&#9673;</b> target</div>
  </div>
  <div class="sc" id="s8">{head_html("h8", HEADS[9][1])}
    <div class="card" id="chk"><div class="ttl"><b>&#10033;</b> Cek keamanan <span class="n" id="cn">0/3</span></div>
      <div class="it" id="i1"><div class="ck" id="k1"></div><div class="tx">Update sistem<small>rutin, terutama yang online</small></div></div>
      <div class="it" id="i2"><div class="ck" id="k2"></div><div class="tx">Batasi akses<small>cabut akun yang udah nggak dipakai</small></div></div>
      <div class="it" id="i3"><div class="ck" id="k3"></div><div class="tx">Backup data<small>otomatis, simpan terpisah</small></div></div></div>
  </div>
  <div class="sc dk" id="s9">{head_html("h9", HEADS[10][1])}
    <div class="card" id="p4"><div class="tab">SERI AI PENGAWAS</div><div class="k">PART 4 &middot; BESOK</div><div class="v">AI lawan<br><i>balik</i></div>{SHIELD}</div>
  </div>
  <div class="sc dk" id="s10">{head_html("h10", HEADS[11][1])}
    <div class="card" id="prof"><div class="av">E</div><div class="nm">EndrichTech</div><div class="hd">@end.rich9</div>
      <div class="sr" style="margin-top:110px">AI &amp; tech buat kerja + usaha.<br>Seri AI Pengawas tiap hari.</div><div id="fbtn">Follow</div></div>
  </div>
  <div class="sc rd" id="s11">{head_html("h11", HEADS[12][1])}
    <div class="card" id="cm"><div class="ct">Komentar</div>
      <div class="cmt" id="cA"><div class="av">A</div><div class="tx"><small>pilihan A</small>Data pelanggan dicuri</div></div>
      <div class="cmt" id="cB"><div class="av">B</div><div class="tx"><small>pilihan B</small>Bisnis nggak bisa jalan</div></div>
      <div id="cin">tulis A atau B&hellip;</div></div>
  </div>
  <div id="halo"></div>
  <div id="badge"><div class="bx"></div><div class="h">@end.rich9</div><div class="nm">Endrich<b>Tech</b></div></div>
  <div id="chibi"><div id="chibiS">{imgs}</div></div>
  <div id="grain"></div>
'''

JS = r'''
    var FPS = 30;
    function q(t) { return Math.round(t * FPS) / FPS; }
    var tl = gsap.timeline({ paused: true });
    var NI = { immediateRender: false };
    function cut(sel, t, v) { tl.set(sel, { opacity: v }, q(t)); }
    function spring(sel, t, from, d) { tl.fromTo(sel, Object.assign({ opacity: 0, y: 90, rotation: 0, scale: 1 }, from || {}), { opacity: 1, y: 0, x: 0, rotation: 0, scale: 1, duration: d || 0.45, ease: "back.out(1.5)" }, q(t)); }
    function count(sel, t, d, a, b, fmt) { var o = { v: a }, el = document.querySelector(sel); tl.fromTo(o, { v: a }, { v: b, duration: d, ease: "power2.out", onUpdate: function () { el.textContent = fmt(o.v); } }, q(t)); }
    function type(sel, t, d, msg) { var o = { n: 0 }, el = document.querySelector(sel); tl.fromTo(o, { n: 0 }, { n: msg.length, duration: d, ease: "none", onUpdate: function () { el.textContent = msg.slice(0, Math.round(o.n)); } }, q(t)); }
    function idn(n) { return Math.round(n).toLocaleString("id-ID"); }
    // background mode per beat (P=paper, D=dark, R=red); hard cuts like the reference
    MODES.forEach(function (m) {
      ["#bgP", "#bgD", "#bgR"].forEach(function (b) { tl.set(b, { opacity: b === "#bg" + m[1] ? 1 : 0 }, q(m[0])); });
      tl.set("#hdr", { color: m[1] === "P" ? "#8A877F" : (m[1] === "R" ? "#FFD9CF" : "#77746D") }, q(m[0]));
      tl.set("#root", { className: m[1] === "P" ? "" : "dkC" }, q(m[0]));
    });
    // scenes: visible from start to next start; each enters with a small push
    SCN.forEach(function (s, i) {
      cut(s[0], s[1], 1);
      tl.fromTo(s[0], { x: 70 }, Object.assign({ x: 0, duration: 0.3, ease: "power3.out" }, NI), q(s[1]));
      if (i + 1 < SCN.length) cut(s[0], SCN[i + 1][1], 0);
    });
    // header labels
    HDR.forEach(function (h, k) {
      tl.set("#hd" + k + ", #hr" + k, { opacity: 1 }, q(h));
      if (k + 1 < HDR.length) tl.set("#hd" + k + ", #hr" + k, { opacity: 0 }, q(HDR[k + 1]));
    });
    // headlines word by word
    HEADS.forEach(function (h) {
      var sp = document.querySelectorAll("#" + h[0] + " span"), n = sp.length, d = Math.max(0.2, h[3] - h[2]);
      tl.set("#" + h[0], { opacity: 1 }, q(h[2]));
      sp.forEach(function (s, k) { tl.fromTo(s, { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: 0.18, ease: "power2.out" }, q(h[2] + d * k / n)); });
    });
    // h0 -> h0b: line 2 sits under line 1
    // ---- S0 shops fan in + counter
    var fan = [[-26, -40, 640], [-12, 120, 610], [0, 300, 600], [12, 480, 610], [26, 640, 640]];
    fan.forEach(function (f, k) {
      tl.set("#sh" + k, { left: f[1] + 30, top: f[2] }, 0);
      tl.fromTo("#sh" + k, { opacity: 0, y: 600, rotation: 0 }, { opacity: 1, y: 0, rotation: f[0], duration: 0.5, ease: "back.out(1.4)" }, q(Math.max(0.0, K.agen - 0.6) + k * 0.12));
    });
    tl.set("#sh2", { opacity: 1, y: 0, rotation: 0 }, 0);
    spring("#pill0", K.seribu, { y: 40, scale: 0.7 }, 0.35);
    count("#c0", K.seribu, K.situs - K.seribu + 0.3, 0, 1200, function (v) { return idn(v) + (v > 1199 ? "+" : ""); });
    tl.fromTo(".shop", { y: 0 }, Object.assign({ y: -14, duration: 0.12, yoyo: true, repeat: 1, stagger: 0.04 }, NI), q(K.situs));
    // ---- S1 prompt
    spring("#term", B.b1 + 0.05, { y: 80, rotation: -2 });
    type("#red", K.perintah, K.nggak1 - K.perintah - 0.2, RED);
    tl.fromTo("#cu", { opacity: 1 }, { opacity: 0, duration: 0.35, yoyo: true, repeat: 9, ease: "steps(1)" }, q(B.b1));
    spring("#cnt1", K.seratus1 - 0.15, { scale: 0.5, y: 0 }, 0.35);
    cut("#sim", B.b1 + 0.3, 1);
    // ---- S2 cards
    spring("#kc1", B.b2 + 0.05, { y: 300, rotation: -14 });
    spring("#kc2", K.pertama - 0.2, { y: 300, rotation: 16 });
    tl.to("#kc1", { rotation: -5, duration: 0.3 }, q(K.pertama));
    tl.to("#kc2", { rotation: 6, duration: 0.3 }, q(K.pertama + 0.1));
    // ---- S3 grid + TEMBUS + price tag
    document.querySelectorAll("#mgrid .m").forEach(function (m, k) { tl.fromTo(m, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, q(B.b3 + 0.05 + k * 0.03)); });
    HITS.forEach(function (k, n) {
      var el = document.querySelectorAll("#mgrid .m b")[k];
      tl.fromTo(el, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }, q(K.seratus2 + 0.2 + n * 0.14));
    });
    spring("#price", K.biaya, { y: 260, rotation: 10 }, 0.5);
    tl.to("#price", { rotation: -4, duration: 0.4, ease: "sine.inOut" }, q(K.biaya + 0.5));
    count("#c3", K.biaya + 0.2, K.lima - K.biaya + 0.5, 0, 5000, function (v) { return idn(Math.round(v / 50) * 50); });
    // ---- S4 calendar 11 days + counter
    spring("#cal", B.b4 + 0.05, { y: 120 });
    spring("#orgp", K.dua2 - 0.1, { scale: 0.6, y: 0 }, 0.35);
    count("#c4", K.dua2 - 0.1, 1.0, 0, 200, function (v) { return Math.round(v); });
    document.querySelectorAll("#cal .d s").forEach(function (s, k) { tl.to(s, { scaleY: 1, duration: 0.12, ease: "power2.out" }, q(K.dua2 + 0.6 + k * ((K.sebelas + 0.6 - K.dua2 - 0.6) / 11))); });
    tl.set("#cal .d em", { color: "#fff" }, q(K.sebelas + 0.7));
    // ---- S5 gauge
    spring("#gauge", B.b5 + 0.05, { y: 120 });
    tl.fromTo("#garc", { attr: { "stroke-dashoffset": 943 } }, { attr: { "stroke-dashoffset": 920 }, duration: 0.4 }, q(K.empat));
    tl.fromTo("#needle", { attr: { transform: "rotate(-90 340 340)" } }, { attr: { transform: "rotate(-84 340 340)" }, duration: 0.4 }, q(K.empat));
    tl.to("#garc", { attr: { "stroke-dashoffset": 30 }, duration: 1.0, ease: "power3.out" }, q(K.jadi));
    tl.to("#needle", { attr: { transform: "rotate(84 340 340)" }, duration: 1.0, ease: "back.out(1.2)" }, q(K.jadi));
    count("#c5", K.jadi, 1.0, 40, 1500, function (v) { return idn(v) + (v > 1499 ? "+" : ""); });
    // ---- S6 thought bubble
    tl.fromTo("#bub", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, q(B.b6 + 0.3));
    tl.fromTo("#bub i", { y: 0 }, { y: -10, duration: 0.25, yoyo: true, repeat: 5, stagger: 0.1, ease: "sine.inOut" }, q(B.b6 + 0.6));
    // ---- S7 flow
    spring("#fA", B.b7 + 0.05, { x: -120, y: 0, rotation: -3 });
    tl.fromTo("#fl", { scaleY: 0 }, { scaleY: 1, duration: 0.25 }, q(K.manusia - 0.4));
    spring("#fM", K.manusia - 0.2, { x: 120, y: 0, rotation: 3 });
    tl.set("#fM", { className: "card fc on" }, q(K.target));
    spring("#tgt", K.target - 0.1, { scale: 0.5, y: 0 }, 0.35);
    // ---- S8 checklist
    spring("#chk", B.b8 + 0.05, { y: 140 });
    [["#i1", "#k1", K.update, "1/3"], ["#i2", "#k2", K.batasi, "2/3"], ["#i3", "#k3", K.backup, "3/3"]].forEach(function (r) {
      tl.set(r[0], { className: "it cur2" }, q(r[2] - 0.2));
      tl.set(r[1], { className: "ck ok", textContent: "✓" }, q(r[2] + 0.35));
      tl.fromTo(r[1], { scale: 1.4 }, Object.assign({ scale: 1, duration: 0.25, ease: "back.out(3)" }, NI), q(r[2] + 0.35));
      tl.set(r[0], { className: "it" }, q(r[2] + 0.5));
      tl.set("#cn", { textContent: r[3] }, q(r[2] + 0.35));
    });
    // ---- S9 part 4, S10 follow
    spring("#p4", B.b9 + 0.05, { y: 260, rotation: -10 });
    tl.fromTo("#p4 svg", { scale: 0, rotation: -30 }, { scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2.5)" }, q(K.melawan));
    spring("#prof", B.b10 + 0.05, { y: 200, rotation: 6 });
    tl.fromTo("#fbtn", { scale: 1 }, { scale: 0.9, duration: 0.1, yoyo: true, repeat: 1 }, q(B.b10 + 0.7));
    tl.set("#fbtn", { className: "done", textContent: "Following ✓" }, q(B.b10 + 0.9));
    // ---- S11 comments A/B
    spring("#cm", B.b11 + 0.05, { y: 220 });
    spring("#cA", K.data - 0.2, { x: -60, y: 0 }, 0.35);
    spring("#cB", K.atau + 0.2, { x: -60, y: 0 }, 0.35);
    // ---- chibi: always on screen, pose track + squash on emphasis + idle bob
    TRACK.forEach(function (e) { tl.set("#chibiS img:not(#p_" + e[1] + ")", { opacity: 0 }, q(e[0])); tl.set("#p_" + e[1], { opacity: 1 }, q(e[0])); });
    tl.fromTo("#chibi", { y: 500 }, { y: 0, duration: 0.5, ease: "back.out(1.3)" }, 0);
    tl.fromTo("#chibiS", { y: 0 }, { y: -8, duration: 0.7, yoyo: true, repeat: BOBS, ease: "sine.inOut" }, 0.6);
    EMPH.forEach(function (t) { tl.fromTo("#chibi", { scaleY: 0.96, scaleX: 1.03 }, Object.assign({ scaleY: 1, scaleX: 1, duration: 0.35, ease: "back.out(3)" }, NI), q(t)); });
    tl.set({}, {}, DUR);
'''

MODES = [[B["b0"], "P"], [B["b2"], "D"], [B["b4"], "P"], [B["b6"], "D"], [B["b7"], "P"], [B["b9"], "D"], [B["b11"], "R"]]
SCN = [["#s0", B["b0"]], ["#s1", B["b1"]], ["#s2", B["b2"]], ["#s3", B["b3"]], ["#s4", B["b4"]], ["#s5", B["b5"]],
       ["#s6", B["b6"]], ["#s7", B["b7"]], ["#s8", B["b8"]], ["#s9", B["b9"]], ["#s10", B["b10"]], ["#s11", B["b11"]]]
bobs = int(DUR / 0.7)
bobs += bobs % 2 == 0
head = (f"var B = {json.dumps(B)}; var K = {json.dumps(K)}; var DUR = {DUR}; var TRACK = {json.dumps(track)};"
        f" var EMPH = {json.dumps(EMPH_T)}; var BOBS = {bobs}; var MODES = {json.dumps(MODES)}; var SCN = {json.dumps(SCN)};"
        f" var HDR = {json.dumps([h[0] for h in HDR])}; var HEADS = {json.dumps([[h[0], h[1], h[2], h[3]] for h in HEADS])};"
        f" var HITS = {json.dumps(HITS)}; var RED = {json.dumps(RED)};")
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
{JS}
    window.__timelines = window.__timelines || {{}};
    window.__timelines["hari3"] = tl;
  }})();
  </script>
</div>
</body>
</html>
'''
(HERE / "public" / "index.html").write_text(html, encoding="utf-8")
print(f"ok dur={DUR}")
