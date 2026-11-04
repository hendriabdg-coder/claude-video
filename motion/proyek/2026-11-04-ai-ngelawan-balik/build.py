# Reel hari 4 (2026-11-04) · "AI Ngelawan Balik" · Seri AI Pengawas #4.
# Gaya: sama dengan hari 3 (permintaan Endrich 2026-11-04): editorial neo-brutal. Latar krem / arang / oranye-merah
# berganti per beat, label mono "// 0N — ..." di atas, judul Inter yang muncul per kata sinkron VO dengan kata aksen
# Fraunces miring merah, kartu krem ber-border hitam + shadow tegas, baris sumber mono, kartu watermark @end.rich9,
# chibi Endrich setengah badan di kanan bawah sepanjang video (pose + lip-flap).
# VO: buatan Endrich di ElevenLabs, timestamp kata dari tools/align_vo.py. Sumber: output/motion/<slug>/riset.md.
# Versi gaya TERMINAL sebelumnya: build_terminal_v1.py.
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
from reel_common import ROOT, VO_START, chibi_track, page, setup, svg  # noqa: E402

SLUG = "2026-11-04-ai-ngelawan-balik"
DUR = setup(HERE, SLUG)
WD = json.loads((ROOT / "output" / "motion" / SLUG / "vo" / "vo-full.json").read_text(encoding="utf-8"))["words"]


def at(word, n=1, end=False):
    k = 0
    for w in WD:
        if w["word"].lower().strip(",.?!").startswith(word.lower()):
            k += 1
            if k == n:
                return round((w["end"] if end else w["start"]) + VO_START, 3)
    raise KeyError(f"{word} #{n}")


A = {
    "udah": at("udah"), "tahu": at("tahu", 1), "belum": at("belum"),
    "dalam": at("dalam"), "empat": at("empat"), "ai1": at("AI"), "nemuin1": at("nemuin"), "seratus": at("seratus"), "celah1": at("celah"),
    "masalah": at("masalahnya"), "setengah": at("setengah"), "tetap": at("tetap"), "nambal": at("nambal"),
    "dan0": at("dan"), "tahun": at("tahun"), "google": at("google"), "nemuin3": at("nemuin", 3), "disiapin": at("disiapin"), "hacker": at("hacker"),
    "untung": at("untungnya"), "ditambal1": at("ditambal"), "duluan": at("duluan"),
    "tapi": at("tapi"), "lihat": at("lihat"),
    "mei": at("mei"), "lima": at("lima"), "serius": at("serius"), "anthropic": at("anthropic"),
    "baru75": at("baru", 2), "tujuh": at("tujuh"), "ditambal2": at("ditambal", 2),
    "dan": at("dan", 2), "tambalan": at("tambalan"), "ngelindungin": at("ngelindungin"), "kalau1": at("kalau"), "pasang1": at("pasang"),
    "besok": at("besok"), "alat": at("alat"), "populer": at("populer"), "disusupi": at("disusupi"), "pencuri": at("pencuri"),
    "follow": at("follow"), "ketinggalan": at("ketinggalan"),
    "kalau2": at("kalau", 2), "notifikasi": at("notifikasi"), "langsung": at("langsung"), "nunggu": at("nunggu"), "maksa": at("maksa"),
}
SC = [0.0, A["masalah"] - 0.1, A["dan0"] - 0.1, A["tapi"] - 0.08, A["mei"] - 0.1, A["dan"] - 0.1, A["besok"] - 0.1, A["kalau2"] - 0.1, DUR]

css = '''
@font-face { font-family: "Inter"; src: url("fonts/Inter-400.woff2") format("woff2"); font-weight: 400; font-display: block; }
@font-face { font-family: "Inter"; src: url("fonts/Inter-500.woff2") format("woff2"); font-weight: 500; font-display: block; }
@font-face { font-family: "Inter"; src: url("fonts/Inter-600.woff2") format("woff2"); font-weight: 600; font-display: block; }
@font-face { font-family: "Fra"; src: url("fonts/Fraunces-800-italic.woff2") format("woff2"); font-display: block; }
@font-face { font-family: "JB"; src: url("fonts/JBMono-400.woff2") format("woff2"); font-weight: 400; font-display: block; }
@font-face { font-family: "JB"; src: url("fonts/JBMono-500.woff2") format("woff2"); font-weight: 500; font-display: block; }
:root { --cream:#ECEAE4; --paper:#F6F4EF; --ink:#151515; --char:#242424; --red:#E0461F; --grey:#8A877F; --line:#D5D2CA; }
html, body, #root { background: var(--cream); font-family: "Inter"; color: var(--ink); }
.sc { position: absolute; inset: 0; opacity: 0; }
.cream { background: var(--cream); } .char { background: var(--char); color: #F3F1EC; } .redbg { background: var(--red); color: #FFF; }
.dots { position: absolute; right: 0; bottom: 0; width: 620px; height: 760px; opacity: .5;
        background-image: radial-gradient(rgba(0,0,0,.18) 1.6px, transparent 1.8px); background-size: 14px 14px;
        -webkit-mask-image: linear-gradient(200deg, rgba(0,0,0,0) 20%, #000 80%); }
.char .dots { background-image: radial-gradient(rgba(255,255,255,.12) 1.6px, transparent 1.8px); }
.redbg .dots { background-image: radial-gradient(rgba(0,0,0,.16) 1.6px, transparent 1.8px); }
.hd { position: absolute; left: 70px; right: 150px; top: 266px; display: flex; justify-content: space-between; font-family: "JB"; font-size: 26px; color: var(--grey); }
.char .hd { color: #8D8A84; } .redbg .hd { color: rgba(255,255,255,.85); }
.hd b { font-weight: 500; color: var(--red); } .redbg .hd b { color: #fff; }
.hl { position: absolute; left: 70px; width: 860px; top: 330px; font-size: 68px; line-height: 1.12; font-weight: 500; letter-spacing: -0.01em; }
.hl span { display: inline-block; opacity: 0; margin-right: 0.24em; }
.hl .ac { font-family: "Fra"; color: var(--red); font-size: 1.04em; }
.redbg .hl .ac { color: var(--ink); }
.hl.big { top: 330px; font-size: 92px; }
#h6s { font-size: 58px; }
.src { position: absolute; left: 70px; top: 1330px; font-family: "JB"; font-size: 24px; color: var(--grey); opacity: 0; }
.char .src { color: #8D8A84; }
.card { position: absolute; background: var(--paper); border: 3px solid var(--ink); border-radius: 22px; box-shadow: 12px 12px 0 var(--ink); color: var(--ink); opacity: 0; }
.tag { position: absolute; left: 26px; top: -46px; height: 46px; padding: 0 20px; border: 3px solid var(--ink); border-bottom: none; border-radius: 12px 12px 0 0;
       background: var(--red); color: #fff; font-family: "JB"; font-weight: 500; font-size: 24px; display: flex; align-items: center; }
.mono { font-family: "JB"; }
.chip { position: absolute; left: 70px; height: 76px; padding: 0 30px; border: 3px solid var(--ink); border-radius: 38px; background: var(--paper);
        box-shadow: 7px 7px 0 var(--ink); display: flex; align-items: center; gap: 14px; font-size: 40px; font-weight: 600; color: var(--ink); opacity: 0; }
.chip em { font-style: normal; color: var(--red); }
/* S1 report */
#rep { left: 70px; top: 560px; width: 860px; height: 640px; }
#rep .rh { position: absolute; left: 34px; top: 26px; font-size: 26px; color: var(--grey); letter-spacing: .04em; }
#cnt { position: absolute; left: 34px; top: 70px; font-family: "Inter"; font-weight: 600; font-size: 150px; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }
#cnt b { color: var(--red); font-weight: 600; }
#rep .rs { position: absolute; left: 38px; top: 250px; font-size: 26px; color: var(--grey); }
#grid { position: absolute; left: 34px; top: 310px; width: 786px; display: grid; grid-template-columns: repeat(16, 1fr); gap: 8px; }
#grid i { aspect-ratio: 1; border: 2.5px solid var(--ink); border-radius: 6px; background: #fff; display: block; }
#grid i.h { background: var(--red); }
/* S2 steps */
#steps { left: 70px; top: 560px; width: 860px; height: 470px; }
.row { position: absolute; left: 34px; right: 34px; height: 130px; border: 3px solid var(--ink); border-radius: 16px; display: flex; align-items: center; gap: 26px; padding: 0 28px; background: #fff; opacity: 0; }
.row .nm { width: 66px; height: 66px; border-radius: 50%; background: var(--ink); color: #fff; font-weight: 600; font-size: 34px; display: flex; align-items: center; justify-content: center; flex: none; }
.row .tx { font-size: 50px; font-weight: 600; }
.row .st { margin-left: auto; font-family: "JB"; font-size: 26px; }
#r1 { top: 40px; } #r1 .st { color: #1E8E4E; }
#r2 { top: 200px; border-style: dashed; } #r2 .nm { background: var(--red); } #r2 .st { color: var(--red); }
#pbar { position: absolute; left: 34px; right: 34px; top: 375px; height: 46px; border: 3px solid var(--ink); border-radius: 23px; overflow: hidden; background: #fff; }
#pbar i { position: absolute; left: 0; top: 0; bottom: 0; width: 50%; background: var(--red); transform-origin: 0 50%; transform: scaleX(0); }
#pbar span { position: absolute; right: 18px; top: 4px; font-family: "JB"; font-size: 26px; }
/* S3 flow */
.nd { width: 760px; height: 140px; left: 100px; display: flex; align-items: center; gap: 26px; padding: 0 30px; }
.nd .ic { width: 82px; height: 82px; border: 3px solid var(--ink); border-radius: 18px; padding: 14px; flex: none; background: #fff; }
.nd .tt { font-size: 46px; font-weight: 600; } .nd .ss { font-family: "JB"; font-size: 22px; color: var(--grey); margin-top: 4px; }
#n1 { top: 560px; } #n1 .ic { color: var(--red); }
#n2 { top: 790px; } #n3 { top: 1020px; } #n3 .ic { background: var(--red); color: #fff; }
.ln { position: absolute; left: 236px; width: 5px; background: var(--ink); height: 90px; transform-origin: 50% 0; transform: scaleY(0); }
#l1 { top: 703px; } #l2 { top: 933px; }
/* S5 bars */
#bars { left: 70px; top: 600px; width: 860px; height: 520px; }
.br { position: absolute; left: 34px; right: 34px; }
.br .bl { display: flex; justify-content: space-between; font-size: 36px; font-weight: 600; margin-bottom: 12px; }
.br .bl b { font-weight: 600; font-variant-numeric: tabular-nums; }
.br .tr { height: 96px; border: 3px solid var(--ink); border-radius: 14px; background: #fff; overflow: hidden; }
.br .fl { height: 100%; background: var(--ink); transform-origin: 0 50%; transform: scaleX(0); }
#br1 { top: 50px; } #br2 { top: 250px; } #br2 .fl { width: 14.15%; background: var(--red); } #br2 .bl b { color: var(--red); }
#bars .nt { position: absolute; left: 38px; top: 440px; font-family: "JB"; font-size: 24px; color: var(--grey); }
/* S6 notif */
#nt { left: 120px; top: 600px; width: 760px; padding: 34px 36px; }
#nt .nh { display: flex; align-items: center; gap: 22px; }
#nt .ni { width: 84px; height: 84px; border: 3px solid var(--ink); border-radius: 20px; background: var(--red); color: #fff; padding: 16px; flex: none; }
#nt .t1 { font-size: 42px; font-weight: 600; } #nt .t2 { font-family: "JB"; font-size: 24px; color: var(--grey); margin-top: 6px; }
#nt .bts { display: flex; gap: 22px; margin-top: 34px; }
#nt .bt { flex: 1; height: 96px; border: 3px solid var(--ink); border-radius: 48px; display: flex; align-items: center; justify-content: center; font-size: 38px; font-weight: 600; position: relative; }
#bL { background: #fff; color: var(--ink); } #bN { background: var(--ink); color: #fff; }
#bL s { position: absolute; left: 30px; right: 30px; top: 46px; height: 5px; background: var(--red); transform-origin: 0 50%; transform: scaleX(0); }
#tap { position: absolute; left: 700px; top: 870px; width: 74px; height: 74px; color: var(--ink); opacity: 0; }
#done { left: 70px; top: 1060px; }
.sim { position: absolute; left: 700px; top: 950px; font-family: "JB"; font-size: 20px; letter-spacing: .15em; color: var(--grey); opacity: 0; }
/* S7 teaser + follow */
#tz { left: 70px; top: 600px; width: 560px; height: 420px; padding: 36px; }
#tz .k { font-family: "JB"; font-size: 24px; color: var(--grey); }
#tz .tt { font-size: 78px; font-weight: 600; line-height: 1.04; margin-top: 18px; letter-spacing: -0.02em; }
#tz .tt i { font-family: "Fra"; font-style: normal; color: var(--red); }
#tz .key { position: absolute; right: 30px; bottom: 30px; width: 110px; height: 110px; color: var(--red); }
#fl { left: 70px; top: 600px; width: 760px; height: 300px; padding: 34px; opacity: 0; }
#fl .pr { display: flex; align-items: center; gap: 22px; }
#fl .av { width: 92px; height: 92px; border-radius: 50%; background: var(--red); border: 3px solid var(--ink); color: #fff; font-weight: 600; font-size: 44px; display: flex; align-items: center; justify-content: center; }
#fl .nm { font-size: 42px; font-weight: 600; } #fl .hn { font-family: "JB"; font-size: 24px; color: var(--grey); }
#fbtn { margin-top: 34px; height: 92px; border: 3px solid var(--ink); border-radius: 16px; background: var(--red); color: #fff; font-size: 40px; font-weight: 600;
        display: flex; align-items: center; justify-content: center; position: relative; }
#fbtn .ok { position: absolute; inset: -3px; border: 3px solid var(--ink); border-radius: 16px; background: #fff; color: var(--ink); display: flex; align-items: center; justify-content: center; opacity: 0; }
/* S8 comments */
#cm { left: 70px; top: 600px; width: 860px; height: 560px; }
#cm .ch { height: 86px; border-bottom: 3px solid var(--line); display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 600; }
.op { position: absolute; left: 34px; right: 34px; display: flex; align-items: center; gap: 22px; opacity: 0; }
.op .oa { width: 72px; height: 72px; border-radius: 50%; background: var(--ink); color: #fff; font-weight: 600; font-size: 36px; display: flex; align-items: center; justify-content: center; flex: none; }
.op .k { font-family: "JB"; font-size: 22px; color: var(--grey); } .op .v { font-size: 42px; font-weight: 600; }
#oA { top: 130px; } #oB { top: 270px; } #oB .oa { background: var(--red); }
#cm .in { position: absolute; left: 34px; right: 34px; bottom: 30px; height: 76px; border: 3px solid var(--line); border-radius: 38px; display: flex; align-items: center; padding: 0 30px; font-family: "JB"; font-size: 26px; color: var(--grey); }
/* overlay: watermark + chibi */
#wm { position: absolute; left: 70px; top: 1442px; width: 330px; height: 112px; background: var(--paper); border: 3px solid var(--ink); border-radius: 16px; box-shadow: 8px 8px 0 var(--ink); }
#wm .pl { position: absolute; left: 18px; top: 14px; height: 34px; padding: 0 12px; border-radius: 8px; background: var(--red); color: #fff; font-family: "JB"; font-size: 20px; display: flex; align-items: center; }
#wm .nm { position: absolute; left: 18px; top: 56px; font-family: "IDBlack"; font-size: 40px; color: var(--ink); letter-spacing: -0.01em; }
#wm .nm b { color: var(--red); font-weight: normal; }
#cb { position: absolute; left: 380px; top: 1180px; width: 944px; height: 1680px; transform-origin: 50% 30%; }
#cb img { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; }
'''


def HL(hid, toks, cls=""):
    """toks: [(text, t, accent)] -> headline whose words pop in at t."""
    spans = "".join(f'<span class="{"ac" if a else ""}" data-t="{t:.3f}">{w}</span>' for w, t, a in toks)
    return f'<div class="hl {cls}" id="{hid}">{spans}</div>'


def HD(left, right):
    return f'<div class="hd"><span>{left}</span><span>{right}</span></div>'


ICO = {
    "skull": svg('<path d="M50 12c-20 0-34 13-34 32 0 11 5 19 12 24v14h44V68c7-5 12-13 12-24 0-19-14-32-34-32z"/><circle cx="37" cy="46" r="7"/><circle cx="63" cy="46" r="7"/>', 7),
    "search": svg('<circle cx="42" cy="42" r="26"/><path d="M62 62l24 24"/>', 9),
    "check": svg('<path d="M22 52l18 18 38-40"/>', 11),
    "upd": svg('<path d="M50 14v48M30 44l20 20 20-20"/><path d="M18 70v14h64V70"/>', 8),
    "key": svg('<circle cx="32" cy="50" r="16"/><path d="M48 50h40M76 50v14M88 50v10"/>', 7),
    "cursor": svg('<path d="M24 14l52 30-22 6 14 26-10 5-14-26-16 16z"/>', 5),
}
HOLES = {5, 13, 20, 29, 38, 43, 52, 61, 66, 75, 84, 90}
GRID = "".join(f'<i class="{"h" if k in HOLES else ""}"></i>' for k in range(96))

b = A
body = f'''
  <!-- S1 hook: 129.000 -->
  <div class="sc cream" id="s1"><div class="dots"></div>{HD("// 01 &mdash; empat bulan", "AI PENGAWAS <b>#4</b>")}
    {HL("h1a", [("Udah", b["udah"], 0), ("tahu", b["tahu"], 0), ("belum?", b["belum"], 1)])}
    {HL("h1b", [("Dalam", b["dalam"], 0), ("4", b["empat"], 0), ("bulan,", b["empat"] + 0.25, 0), ("AI", b["ai1"], 0), ("nemu", b["nemuin1"], 0),
                ("129.000", b["seratus"] + 0.6, 1), ("celah", b["celah1"], 1)])}
    <div class="card" id="rep"><div class="tag">LAPORAN</div><div class="rh mono">celah terverifikasi &middot; apr&ndash;jul 2026</div>
      <div id="cnt">0</div><div class="rs mono">ditemukan mitra Project Glasswing</div><div id="grid">{GRID}</div></div>
    <div class="src" id="src1">sumber: Anthropic, 6 Okt 2026</div></div>
  <!-- S2 setengah jalan -->
  <div class="sc char" id="s2"><div class="dots"></div>{HD("// 02 &mdash; masalahnya", "AI PENGAWAS <b>#4</b>")}
    {HL("h2", [("Nemu", b["masalah"] + 0.5, 0), ("celah", b["masalah"] + 0.75, 0), ("baru", b["setengah"] - 0.4, 0), ("setengah", b["setengah"], 1), ("jalan.", b["setengah"] + 0.4, 1)])}
    <div class="card" id="steps"><div class="tag">STATUS</div>
      <div class="row" id="r1"><span class="nm">1</span><span class="tx">Temukan</span><span class="st">[selesai]</span></div>
      <div class="row" id="r2"><span class="nm">2</span><span class="tx">Tambal</span><span class="st">nunggu manusia</span></div>
      <div id="pbar"><i></i><span>50%</span></div></div></div>
  <!-- S3 google -->
  <div class="sc cream" id="s3"><div class="dots"></div>{HD("// 03 &mdash; kata google", "KASUS <b>1</b>/2")}
    {HL("h3", [("Google:", b["google"], 0), ("AI-nya", b["google"] + 0.5, 0), ("nemu", b["nemuin3"], 0), ("celah", b["nemuin3"] + 0.3, 0), ("duluan", b["untung"] + 0.3, 1)])}
    <div class="card nd" id="n1"><span class="ic">{ICO["skull"]}</span><div><div class="tt">Hacker siapin serangan</div><div class="ss">celahnya cuma diketahui penyerang</div></div></div>
    <div class="ln" id="l1"></div>
    <div class="card nd" id="n2"><span class="ic">{ICO["search"]}</span><div><div class="tt">AI nemu celahnya</div><div class="ss">agen Big Sleep</div></div></div>
    <div class="ln" id="l2"></div>
    <div class="card nd" id="n3"><span class="ic">{ICO["check"]}</span><div><div class="tt">Ditambal duluan</div><div class="ss">sebelum sempat dipakai</div></div></div>
    <div class="src" id="src3">sumber: Google Cloud blog, 17 Jul 2025</div></div>
  <!-- S4 tapi -->
  <div class="sc char" id="s4"><div class="dots"></div>{HD("// 04 &mdash; yang perlu kamu tahu", "")}
    {HL("h4", [("Tapi", b["tapi"], 0), ("lihat", b["lihat"], 0), ("ini.", b["lihat"] + 0.3, 1)], "big")}</div>
  <!-- S5 530 vs 75 -->
  <div class="sc cream" id="s5"><div class="dots"></div>{HD("// 05 &mdash; per mei 2026", "KASUS <b>2</b>/2")}
    {HL("h5", [("Dari", b["mei"] + 0.4, 0), ("530", b["lima"], 1), ("celah", b["serius"] - 0.3, 0), ("serius,", b["serius"], 0), ("baru", b["baru75"], 0),
               ("75", b["tujuh"], 1), ("ditambal", b["ditambal2"], 0)])}
    <div class="card" id="bars"><div class="tag">TEMUAN AI ANTHROPIC</div>
      <div class="br" id="br1"><div class="bl"><span>Dilaporkan</span><b id="v1">0</b></div><div class="tr"><div class="fl"></div></div></div>
      <div class="br" id="br2"><div class="bl"><span>Sudah ditambal</span><b id="v2">0</b></div><div class="tr"><div class="fl"></div></div></div>
      <div class="nt">celah high/critical &middot; rata-rata 2 minggu per tambalan</div></div>
    <div class="src" id="src5">sumber: Anthropic, 22 Mei 2026</div></div>
  <!-- S6 update -->
  <div class="sc cream" id="s6"><div class="dots"></div>{HD("// 06 &mdash; bagian kamu", "AI PENGAWAS <b>#4</b>")}
    {HL("h6s", [("Tambalan", b["tambalan"], 0), ("baru", b["ngelindungin"] - 0.3, 0), ("ngelindungin", b["ngelindungin"], 0), ("kalau", b["kalau1"], 1), ("dipasang.", b["pasang1"], 1)])}
    <div class="card" id="nt"><div class="nh"><span class="ni">{ICO["upd"]}</span><div><div class="t1">Pembaruan keamanan</div><div class="t2">tersedia untuk HP kamu</div></div></div>
      <div class="bts"><div class="bt" id="bL">Nanti aja<s></s></div><div class="bt" id="bN">Pasang</div></div></div>
    <div id="tap">{ICO["cursor"]}</div>
    <div class="chip" id="done" style="top:1080px"><span style="width:44px;height:44px;color:#1E8E4E">{ICO["check"]}</span>Celah <em>ditutup</em></div>
    <div class="sim" id="sim">SIMULASI</div></div>
  <!-- S7 besok + follow -->
  <div class="sc char" id="s7"><div class="dots"></div>{HD("// 07 &mdash; seri ai pengawas", "PART <b>5</b> BESOK")}
    {HL("h7a", [("Besok:", b["besok"], 0), ("alat", b["alat"], 0), ("AI", b["alat"] + 0.25, 0), ("populer", b["populer"], 0), ("disusupi", b["disusupi"], 1)])}
    <div class="card" id="tz"><div class="tag">PART 5 &middot; BESOK</div><div class="k">// alat AI populer</div>
      <div class="tt">Pencuri <i>kunci akses</i></div><span class="key">{ICO["key"]}</span></div>
    {HL("h7b", [("Follow", b["follow"], 1), ("biar", b["follow"] + 0.45, 0), ("nggak", b["ketinggalan"] - 0.3, 0), ("ketinggalan", b["ketinggalan"], 0)])}
    <div class="card" id="fl"><div class="pr"><span class="av">E</span><div><div class="nm">EndrichTech</div><div class="hn">@end.rich9</div></div></div>
      <div id="fbtn">Follow<div class="ok">Following &#10003;</div></div></div></div>
  <!-- S8 komentar -->
  <div class="sc redbg" id="s8"><div class="dots"></div>{HD("// 08 &mdash; jawab di komentar", "A &nbsp;&nbsp; B")}
    {HL("h8", [("Ada", b["notifikasi"] - 0.3, 0), ("notif", b["notifikasi"], 0), ("update?", b["notifikasi"] + 0.5, 0), ("Kamu", b["langsung"] - 0.4, 0), ("pilih", b["nunggu"] - 0.3, 0), ("mana?", b["maksa"], 1)])}
    <div class="card" id="cm"><div class="ch">Komentar</div>
      <div class="op" id="oA"><span class="oa">A</span><div><div class="k">pilihan A</div><div class="v">Langsung pasang</div></div></div>
      <div class="op" id="oB"><span class="oa">B</span><div><div class="k">pilihan B</div><div class="v">Nunggu HP-nya maksa</div></div></div>
      <div class="in">tulis A atau B&hellip;</div></div></div>
  <!-- overlay -->
  <div id="wm"><div class="pl">@end.rich9</div><div class="nm">Endrich<b>Tech</b></div></div>
  <div id="cb">{"".join(f'<img id="cp_{p}" src="pose/pose_{i}_{p}.png">' for i, p in enumerate(["netral", "lambai", "tunjuk", "mikir", "kaget", "keren", "bicara", "kedip"]))}</div>
'''

# chibi presenter all video long: pose per beat, lip-flap on the "netral" stretches
EMPH = [(0.0, "tunjuk"), (b["dalam"], "netral"), (b["celah1"], "kaget"), (b["celah1"] + 1.0, "netral"), (b["tetap"], "mikir"), (b["tahun"], "netral"),
        (b["duluan"], "keren"), (b["duluan"] + 0.9, "netral"), (b["tapi"], "mikir"), (b["mei"], "netral"), (b["ditambal2"], "kaget"),
        (b["ditambal2"] + 0.8, "netral"), (b["pasang1"] - 0.2, "tunjuk"), (b["besok"] + 0.3, "netral"), (b["follow"], "lambai"),
        (b["follow"] + 1.2, "netral"), (b["kalau2"] + 0.3, "mikir")]
track, emph_t = chibi_track(HERE, 0.0, DUR, EMPH[1:] if EMPH[0][0] == 0 else EMPH, blinks=(b["setengah"] + 0.6, b["anthropic"], b["populer"] + 0.4))
track = [[0.0, "tunjuk"]] + [e for e in track if e[0] > 0] if track and track[0][1] != "tunjuk" else track

js = f'''
    var A = {json.dumps(A)}, SC = {json.dumps(SC)}, DUR = {DUR};
    // hard-cut scene switches (as hari 3)
    ["#s1", "#s2", "#s3", "#s4", "#s5", "#s6", "#s7", "#s8"].forEach(function (s, k) {{ tl.set(s, {{ opacity: 1 }}, q(SC[k])); if (k < 7) tl.set(s, {{ opacity: 0 }}, q(SC[k + 1])); }});
    // headline words pop in on their VO word
    document.querySelectorAll(".hl span").forEach(function (w) {{
      tl.fromTo(w, {{ opacity: 0, y: 26 }}, {{ opacity: 1, y: 0, duration: 0.28, ease: "back.out(1.4)" }}, q(parseFloat(w.dataset.t)));
    }});
    function card(sel, t, rot) {{ tl.fromTo(sel, {{ opacity: 0, y: 70, rotation: rot || -2 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.42, ease: "back.out(1.4)" }}, q(t)); }}
    function src(sel, t) {{ tl.fromTo(sel, {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }}, q(t)); }}

    // S1
    tl.set("#h1a", {{ opacity: 1 }}, 0); tl.to("#h1a", {{ opacity: 0, duration: 0.1 }}, q(A.dalam - 0.1));
    card("#rep", A.dalam - 0.05);
    var cv = {{ v: 0 }}, cel = document.querySelector("#cnt");
    tl.to(cv, {{ v: 129000, duration: A.celah1 - A.dalam + 0.2, ease: "power2.out", onUpdate: function () {{
      cel.innerHTML = idn(cv.v) + (cv.v > 128999 ? "<b>+</b>" : ""); }} }}, q(A.dalam + 0.2));
    tl.fromTo("#grid i.h", {{ backgroundColor: "#FFFFFF" }}, {{ backgroundColor: "#E0461F", duration: 0.12, stagger: (A.celah1 - A.dalam) / 14 }}, q(A.dalam + 0.3));
    tl.fromTo("#rep", {{ scale: 1.03 }}, Object.assign({{ scale: 1, duration: 0.3, ease: "back.out(3)" }}, NI), q(A.celah1 + 0.2));
    src("#src1", A.celah1);

    // S2
    tl.set("#r1", {{ opacity: 1 }}, q(SC[1])); card("#steps", SC[1] + 0.05, 2);
    tl.fromTo("#r2", {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "back.out(1.6)" }}, q(A.tetap));
    tl.to("#pbar i", {{ scaleX: 1, duration: 0.6, ease: "power2.out" }}, q(A.setengah));
    tl.to("#r2 .st", {{ opacity: 0.3, duration: 0.25, yoyo: true, repeat: 3, ease: "steps(1)" }}, q(A.nambal - 0.3));

    // S3
    card("#n1", A.disiapin - 0.3, -2);
    tl.to("#l1", {{ scaleY: 1, duration: 0.3, ease: "power2.out" }}, q(A.untung - 0.45));
    card("#n2", A.untung - 0.2, 2);
    tl.to("#l2", {{ scaleY: 1, duration: 0.3, ease: "power2.out" }}, q(A.ditambal1 - 0.3));
    card("#n3", A.ditambal1, -1.5);
    src("#src3", A.google + 0.4);

    // S5
    card("#bars", SC[4] + 0.1, 2);
    tl.to("#br1 .fl", {{ scaleX: 1, duration: 0.9, ease: "power2.out" }}, q(A.lima));
    count("#v1", A.lima, 0.9, 0, 530, function (v) {{ return Math.round(v); }});
    tl.to("#br2 .fl", {{ scaleX: 1, duration: 0.6, ease: "power2.out" }}, q(A.tujuh));
    count("#v2", A.tujuh, 0.6, 0, 75, function (v) {{ return Math.round(v); }});
    tl.fromTo("#bars", {{ x: -8 }}, Object.assign({{ x: 0, duration: 0.3, ease: "elastic.out(1,.3)" }}, NI), q(A.ditambal2));
    src("#src5", A.anthropic);

    // S6
    card("#nt", SC[5] + 0.15, -2); cut("#sim", SC[5] + 0.3, 1);
    tl.to("#bL s", {{ scaleX: 1, duration: 0.25, ease: "power2.out" }}, q(A.kalau1));
    tl.to("#bL", {{ opacity: 0.4, duration: 0.2 }}, q(A.kalau1 + 0.2));
    tl.fromTo("#tap", {{ opacity: 0, x: 70, y: 70 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.3, ease: "power2.out" }}, q(A.kalau1 + 0.3));
    tl.to("#bN", {{ scale: 0.93, duration: 0.08, yoyo: true, repeat: 1 }}, q(A.pasang1 - 0.1));
    tl.to("#bN", {{ backgroundColor: "#E0461F", duration: 0.1 }}, q(A.pasang1));
    tl.fromTo("#done", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, q(A.pasang1 + 0.1));

    // S7
    card("#tz", A.alat - 0.1, -2);
    tl.to("#tz .key", {{ rotation: -18, duration: 0.15, yoyo: true, repeat: 3, ease: "power1.inOut" }}, q(A.pencuri));
    tl.to("#h7a, #tz", {{ opacity: 0, duration: 0.12 }}, q(A.follow - 0.12));
    card("#fl", A.follow - 0.05, 2);
    tl.to("#fbtn", {{ scale: 0.94, duration: 0.08, yoyo: true, repeat: 1 }}, q(A.follow + 0.6));
    tl.set("#fbtn .ok", {{ opacity: 1 }}, q(A.follow + 0.75));

    // S8
    card("#cm", SC[7] + 0.1, -2);
    tl.fromTo("#oA", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, q(A.langsung));
    tl.fromTo("#oB", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, q(A.nunggu));

    // chibi: pose track + small squash on pose changes + idle bob
    var CTRACK = {json.dumps(track)}, CEMPH = {json.dumps(emph_t)};
    CTRACK.forEach(function (e) {{ tl.set("#cb img:not(#cp_" + e[1] + ")", {{ opacity: 0 }}, q(e[0])); tl.set("#cp_" + e[1], {{ opacity: 1 }}, q(e[0])); }});
    tl.fromTo("#cb", {{ y: 420 }}, {{ y: 0, duration: 0.45, ease: "back.out(1.3)" }}, 0);
    tl.fromTo("#cb", {{ rotation: 0 }}, {{ rotation: 1.2, duration: 1.4, yoyo: true, repeat: {int(DUR / 1.4) // 2 * 2 - 1}, ease: "sine.inOut" }}, 0.5);
    CEMPH.forEach(function (t) {{ tl.fromTo("#cb", {{ scaleY: 0.95, scaleX: 1.03 }}, Object.assign({{ scaleY: 1, scaleX: 1, duration: 0.35, ease: "back.out(3)" }}, NI), q(t)); }});
'''

html = page("ai-ngelawan-balik", DUR, css, body, js).replace("#chibi {", "#chibi_unused {")
(HERE / "public" / "index.html").write_text(html, encoding="utf-8")
print("ok", DUR, [round(s, 2) for s in SC])
