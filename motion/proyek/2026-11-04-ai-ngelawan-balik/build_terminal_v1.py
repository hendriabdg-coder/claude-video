# Reel hari 4 (2026-11-04) · "AI Ngelawan Balik" · Seri AI Pengawas #4 · gaya dasar TERMINAL (CRT hitam, hijau fosfor,
# amber/merah untuk peringatan) + per beat: PULSE (counter 129.000, bar 530 vs 75), SIGNAL (alur Big Sleep),
# EMBER (notif update retak), AVATAR (chibi CTA, lip-flap). VO: buatan Endrich di ElevenLabs (sesi cloud),
# timestamp kata dari tools/align_vo.py (perkiraan dari jeda). Sumber: riset.md.
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
from reel_common import (ICON, ROOT, VO_START, chars, chibi_html, chibi_js, chibi_track, fitpx, page,  # noqa: E402
                         setup, svg)

SLUG = "2026-11-04-ai-ngelawan-balik"
DUR = setup(HERE, SLUG)
WD = json.loads((ROOT / "output" / "motion" / SLUG / "vo" / "vo-full.json").read_text(encoding="utf-8"))["words"]


def at(word, n=1, end=False):
    """Start (or end) time on the composition clock of the n-th spoken word that starts with `word`."""
    k = 0
    for w in WD:
        if w["word"].lower().strip(",.?!").startswith(word.lower()):
            k += 1
            if k == n:
                return round((w["end"] if end else w["start"]) + VO_START, 3)
    raise KeyError(f"{word} #{n}")


A = {  # beat anchors
    "hook": 0.0, "dalam": at("dalam"), "ai1": at("AI"), "celah1": at("celah"),
    "masalah": at("masalahnya"), "setengah": at("setengah"), "tetap": at("tetap"), "nambal": at("nambal"),
    "tahun": at("tahun"), "google": at("google"), "hacker": at("hacker"), "untung": at("untungnya"), "ditambal1": at("ditambal"),
    "tapi": at("tapi"), "mei": at("mei"), "lima": at("lima"), "serius": at("serius"), "anthropic": at("anthropic"),
    "baru75": at("baru", 2), "tujuh": at("tujuh"), "ditambal2": at("ditambal", 2),
    "dan": at("dan"), "kalau1": at("kalau"), "pasang1": at("pasang"),
    "besok": at("besok"), "alat": at("alat"), "pencuri": at("pencuri"), "follow": at("follow"),
    "kalau2": at("kalau", 2), "langsung": at("langsung"), "nunggu": at("nunggu"), "maksa": at("maksa"),
}
CHIBI_IN = A["besok"] - 0.25

css = '''
:root { --bg:#050807; --g:#39FF88; --gd:rgba(57,255,136,.45); --amb:#FFB000; --red:#FF4A4A; --w:#D8FFE8; }
html, body, #root { background: var(--bg); color: var(--g); font-family: Consolas, "Courier New", monospace; }
#crt { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 45%, rgba(57,255,136,.08) 0%, rgba(0,0,0,0) 70%); }
#scan { position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,.28) 0px, rgba(0,0,0,.28) 2px, rgba(0,0,0,0) 2px, rgba(0,0,0,0) 5px); pointer-events: none; }
#vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 75% at 50% 50%, rgba(0,0,0,0) 60%, rgba(0,0,0,.85) 100%); pointer-events: none; }
#cam { position: absolute; inset: 0; }
#hud { position: absolute; left: 60px; top: 262px; display: flex; align-items: center; gap: 14px; font-size: 24px; letter-spacing: .2em; color: var(--gd); opacity: 0; }
#hud i { width: 14px; height: 14px; border-radius: 50%; background: var(--g); box-shadow: 0 0 10px var(--g); display: inline-block; }
#step { position: absolute; right: 150px; top: 258px; display: flex; gap: 8px; opacity: 0; }
#step b { width: 34px; height: 8px; border-radius: 4px; background: rgba(57,255,136,.2); display: block; }
.t { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; }
.t .ch { opacity: 0; }
.bigt { font-family: "IDBlack"; color: var(--g); text-shadow: 0 0 18px rgba(57,255,136,.7); }
.ambt { font-family: "IDBlack"; color: var(--amb); text-shadow: 0 0 18px rgba(255,176,0,.6); }
.redt { font-family: "IDBlack"; color: var(--red); text-shadow: 0 0 18px rgba(255,74,74,.6); }
.wt { font-family: "IDBlack"; color: var(--w); }
.lbl { position: absolute; left: 0; width: 1080px; text-align: center; font-size: 26px; letter-spacing: .2em; color: var(--gd); opacity: 0; }
.sim { position: absolute; font-size: 22px; letter-spacing: .2em; color: var(--gd); padding: 6px 12px; border: 2px solid rgba(57,255,136,.3); border-radius: 8px; opacity: 0; }
/* hook */
#prompt { position: absolute; left: 70px; top: 340px; font-size: 40px; color: var(--w); white-space: pre; opacity: 0; }
#cnt { position: absolute; left: 0; width: 1080px; top: 520px; text-align: center; font-family: "IDBlack"; font-size: 210px; color: var(--g);
       text-shadow: 0 0 30px rgba(57,255,136,.7); font-variant-numeric: tabular-nums; opacity: 0; }
#grid { position: absolute; left: 110px; top: 870px; width: 860px; height: 470px; display: grid; grid-template-columns: repeat(20, 1fr); gap: 10px; opacity: 0; }
#grid i { aspect-ratio: 1; border-radius: 4px; border: 2px solid rgba(57,255,136,.25); display: block; }
#grid i.h { background: var(--red); border-color: var(--red); box-shadow: 0 0 8px rgba(255,74,74,.6); opacity: 0; }
/* half way */
.stp { position: absolute; left: 110px; width: 860px; height: 150px; border: 3px solid var(--gd); border-radius: 22px; display: flex; align-items: center; gap: 30px; padding: 0 40px; opacity: 0; }
.stp .ic { width: 84px; height: 84px; flex: none; }
.stp .tx { font-family: "IDBlack"; font-size: 60px; color: var(--w); }
.stp .st { margin-left: auto; font-size: 30px; letter-spacing: .15em; }
#s1 { top: 640px; } #s1 .ic, #s1 .st { color: var(--g); }
#s2 { top: 840px; border-color: rgba(255,176,0,.7); } #s2 .ic, #s2 .st { color: var(--amb); }
#halfbar { position: absolute; left: 110px; top: 1060px; width: 860px; font-size: 40px; white-space: pre; color: var(--g); opacity: 0; }
/* google flow */
.nd { position: absolute; left: 190px; width: 700px; height: 150px; border: 3px solid var(--gd); border-radius: 22px; background: rgba(5,16,10,.9);
      display: flex; align-items: center; gap: 28px; padding: 0 36px; font-family: "IDBlack"; font-size: 46px; white-space: nowrap; color: var(--w); opacity: 0; }
.nd .ic { width: 76px; height: 76px; flex: none; }
#n1 { top: 560px; border-color: rgba(255,74,74,.7); } #n1 .ic { color: var(--red); }
#n2 { top: 820px; } #n2 .ic { color: var(--g); }
#n3 { top: 1080px; border-color: var(--g); box-shadow: 0 0 30px rgba(57,255,136,.3); } #n3 .ic { color: var(--g); }
.ln { position: absolute; left: 537px; width: 6px; height: 110px; background: var(--g); transform-origin: 50% 0; transform: scaleY(0); }
#l1 { top: 710px; } #l2 { top: 970px; }
#race { position: absolute; left: 190px; top: 1260px; width: 700px; font-size: 30px; letter-spacing: .12em; color: var(--gd); opacity: 0; }
/* bars */
.bar { position: absolute; left: 110px; width: 860px; opacity: 0; }
.bar .bl { display: flex; justify-content: space-between; font-family: "IDBold"; font-size: 40px; color: var(--w); margin-bottom: 14px; }
.bar .bl b { font-family: "IDBlack"; font-weight: normal; font-variant-numeric: tabular-nums; }
.bar .tr { height: 90px; border-radius: 16px; background: rgba(57,255,136,.08); border: 2px solid rgba(57,255,136,.25); overflow: hidden; }
.bar .fl { height: 100%; transform-origin: 0 50%; transform: scaleX(0); }
#b1 { top: 640px; } #b1 .fl { width: 100%; background: var(--red); box-shadow: 0 0 24px rgba(255,74,74,.6); } #b1 .bl b { color: var(--red); }
#b2 { top: 900px; } #b2 .fl { width: 14.15%; background: var(--g); box-shadow: 0 0 24px rgba(57,255,136,.6); } #b2 .bl b { color: var(--g); }
#gap { position: absolute; left: 0; width: 1080px; top: 1160px; text-align: center; font-family: "IDBlack"; font-size: 64px; color: var(--amb);
       text-shadow: 0 0 18px rgba(255,176,0,.6); opacity: 0; }
/* update notification (EMBER beat) */
#notif { position: absolute; left: 150px; top: 600px; width: 780px; border-radius: 34px; border: 2px solid var(--gd); background: rgba(8,20,13,.95);
         padding: 36px 40px; opacity: 0; }
#notif .nh { display: flex; align-items: center; gap: 22px; }
#notif .ni { width: 78px; height: 78px; border-radius: 20px; background: rgba(57,255,136,.12); color: var(--g); padding: 14px; flex: none; }
#notif .nt { font-family: "IDBlack"; font-size: 44px; color: var(--w); }
#notif .ns { font-family: "IDSemi"; font-size: 30px; color: rgba(216,255,232,.7); margin-top: 6px; }
#notif .bts { display: flex; gap: 24px; margin-top: 34px; }
#notif .bt { flex: 1; height: 100px; border-radius: 50px; display: flex; align-items: center; justify-content: center; font-family: "IDBlack"; font-size: 40px; position: relative; }
#bLater { border: 3px solid rgba(216,255,232,.4); color: rgba(216,255,232,.8); }
#bNow { background: var(--g); color: #04120a; }
#crack { position: absolute; inset: -6px; opacity: 0; color: var(--red); }
#tap { position: absolute; left: 700px; top: 860px; width: 70px; height: 70px; color: var(--w); opacity: 0; }
#ok { position: absolute; left: 150px; top: 1010px; width: 780px; font-size: 40px; color: var(--g); white-space: pre; opacity: 0; }
#ember { position: absolute; inset: 0; background: radial-gradient(ellipse 70% 40% at 50% 70%, rgba(255,120,0,.22), rgba(0,0,0,0) 70%); opacity: 0; }
/* CTA */
#follow { position: absolute; left: 340px; top: 590px; width: 400px; height: 96px; border-radius: 48px; background: var(--g); color: #04120a; font-family: "IDBlack";
          font-size: 46px; display: flex; align-items: center; justify-content: center; opacity: 0; box-shadow: 0 0 40px rgba(57,255,136,.5); }
#tapc { position: absolute; left: 660px; top: 630px; width: 70px; height: 70px; color: var(--w); opacity: 0; }
.opt { position: absolute; top: 470px; width: 400px; height: 130px; border-radius: 20px; display: flex; align-items: center; gap: 14px; padding: 0 22px;
       font-family: "IDBlack"; font-size: 34px; line-height: 1.1; opacity: 0; }
.opt .oi { width: 56px; height: 56px; flex: none; }
#oA { left: 110px; border: 4px solid var(--g); color: var(--g); background: rgba(57,255,136,.08); }
#oB { left: 570px; border: 4px solid var(--amb); color: var(--amb); background: rgba(255,176,0,.08); }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-family: "IDBlack"; font-size: 36px; color: var(--w); }
#brand b { color: var(--g); font-weight: normal; }
#flash { position: absolute; inset: 0; background: var(--amb); opacity: 0; pointer-events: none; mix-blend-mode: screen; }
#glitch { position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(255,74,74,.25) 0 6px, rgba(0,0,0,0) 6px 22px); opacity: 0; pointer-events: none; }
'''


def TX(tid, text, top, px, cls="bigt", maxw=820):
    return f'<div class="t {cls}" id="{tid}" style="top:{top}px;font-size:{fitpx(text, px, maxw)}px">{chars(text)}</div>'


HOLES = {3, 17, 26, 41, 58, 64, 77, 85, 99, 106, 118, 123, 137, 142, 159, 166, 171, 188, 193, 199}
GRID = "".join(f'<i class="{"h" if k in HOLES else ""}"></i>' for k in range(200))
BUG = svg('<circle cx="50" cy="56" r="22"/><path d="M50 34v44M30 46H14M70 46h16M30 66H14M70 66h16M38 30l-8-12M62 30l8-12"/>', 6)
SEARCH = svg('<circle cx="42" cy="42" r="26"/><path d="M62 62l24 24"/>', 8)
PATCH = svg('<rect x="14" y="34" width="72" height="32" rx="16" transform="rotate(-35 50 50)"/><path d="M44 44v0M56 56v0M44 56v0M56 44v0"/>', 7)
SKULL = svg('<path d="M50 12c-20 0-34 13-34 32 0 11 5 19 12 24v14h44V68c7-5 12-13 12-24 0-19-14-32-34-32z"/><circle cx="37" cy="46" r="7"/><circle cx="63" cy="46" r="7"/><path d="M42 82v-8M58 82v-8"/>', 6)
UPD = svg('<path d="M50 16v46M32 46l18 18 18-18"/><path d="M20 70v14h60V70"/>', 7)
CRACK = '<svg viewBox="0 0 330 112" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" style="width:100%;height:100%"><path d="M150 0l-14 30 22 14-28 26 18 16-10 26"/><path d="M136 30l-40 8M158 44l46-10M130 70l-36 18M148 86l40 12"/></svg>'

# chibi: point at the next-part promise, think at the comment question
track, emph_t = chibi_track(HERE, CHIBI_IN, DUR, [(A["besok"] + 0.1, "tunjuk"), (A["alat"] + 0.6, "netral"), (A["follow"], "lambai"),
                                                 (A["follow"] + 1.0, "netral"), (A["kalau2"], "mikir"), (A["langsung"] + 0.3, "netral"),
                                                 (A["maksa"] + 0.4, "kedip")], blinks=(A["alat"] + 2.0,))

body = f'''
  <div id="crt"></div>
  <div id="cam">
    <div id="hud"><i></i>AI PENGAWAS #4 &middot; MODE BERTAHAN</div>
    <div id="step">{"<b></b>" * 6}</div>
    <!-- HOOK: 129.000 -->
    <div id="prompt">&gt; <span id="pt"></span></div>
    <div id="cnt">0</div>
    {TX("h1a", "CELAH KEAMANAN DITEMUKAN AI", 760, 60, "wt")}
    <div class="lbl" id="h1b" style="top:836px">APR&ndash;JUL 2026 &middot; MITRA ANTHROPIC</div>
    <div id="grid">{GRID}</div>
    <!-- baru setengah jalan -->
    {TX("h2a", "BARU SETENGAH JALAN", 400, 84)}
    <div class="stp" id="s1"><span class="ic">{SEARCH}</span><span class="tx">TEMUKAN</span><span class="st">[OK]</span></div>
    <div class="stp" id="s2"><span class="ic">{PATCH}</span><span class="tx">TAMBAL</span><span class="st" id="s2s">MENUNGGU MANUSIA</span></div>
    <div id="halfbar"></div>
    <!-- google big sleep -->
    {TX("h3a", "AI GOOGLE NEMU DULUAN", 400, 80)}
    <div class="nd" id="n1"><span class="ic">{SKULL}</span><span>HACKER SIAP NYERANG</span></div>
    <div class="ln" id="l1"></div>
    <div class="nd" id="n2"><span class="ic">{SEARCH}</span><span>AI NEMU CELAHNYA</span></div>
    <div class="ln" id="l2"></div>
    <div class="nd" id="n3"><span class="ic">{ICON["check"]}</span><span>DITAMBAL DULUAN</span></div>
    <div class="lbl" id="h3b" style="top:480px">GOOGLE &middot; BIG SLEEP &middot; JUL 2025</div>
    <!-- loop -->
    {TX("h4a", "TAPI LIHAT INI...", 820, 96, "redt")}
    <!-- 530 vs 75 -->
    {TX("h5a", "CELAH SERIUS TEMUAN AI", 400, 70, "wt")}
    <div class="lbl" id="h5b" style="top:480px">PER MEI 2026 &middot; ANTHROPIC</div>
    <div class="bar" id="b1"><div class="bl"><span>DILAPORKAN</span><b id="v1">0</b></div><div class="tr"><div class="fl"></div></div></div>
    <div class="bar" id="b2"><div class="bl"><span>SUDAH DITAMBAL</span><b id="v2">0</b></div><div class="tr"><div class="fl"></div></div></div>
    <div id="gap">BARU 75 DARI 530</div>
    <!-- payoff: update -->
    <div id="ember"></div>
    {TX("h6a", "TAMBALAN = UPDATE", 400, 84, "ambt")}
    <div id="notif"><div class="nh"><span class="ni">{UPD}</span><div><div class="nt">Pembaruan keamanan</div><div class="ns">Tersedia untuk HP kamu</div></div></div>
      <div class="bts"><div class="bt" id="bLater">NANTI AJA<span id="crack">{CRACK}</span></div><div class="bt" id="bNow">PASANG</div></div></div>
    <div id="tap">{ICON["cursor"]}</div>
    <div id="ok"></div>
    <div class="sim" id="sim1" style="left:150px;top:1000px">SIMULASI</div>
    <!-- CTA seri -->
    <div class="lbl" id="h7a" style="top:300px">BESOK &middot; AI PENGAWAS #5</div>
    {TX("h7b", "ALAT AI POPULER", 350, 80)}
    {TX("h7c", "DISUSUPI PENCURI KUNCI AKSES", 450, 56, "ambt")}
    <div id="follow">+ FOLLOW</div><div id="tapc">{ICON["cursor"]}</div>
    <!-- CTA komentar -->
    {TX("h8a", "ADA NOTIF UPDATE?", 330, 80, "wt")}
    <div class="opt" id="oA"><span class="oi">{ICON["check"]}</span>A: LANGSUNG<br>PASANG</div>
    <div class="opt" id="oB"><span class="oi">{ICON["alert"]}</span>B: NUNGGU<br>DIPAKSA</div>
    <div class="lbl" id="h8b" style="top:625px">JAWAB DI KOMENTAR</div>
    {chibi_html(left=350, top=760, w=380)}
  </div>
  <div id="scan"></div><div id="vig"></div><div id="flash"></div><div id="glitch"></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

A_JS = json.dumps(A)
js = f'''
    var A = {A_JS}, DUR = {DUR};
    tl.to("#crt", {{ opacity: 0.6, duration: 0.07, yoyo: true, repeat: {int(DUR / 0.14) // 2 * 2 - 1}, ease: "steps(1)" }}, 0.3);
    fade("#hud", 0.05, 0.3, {{ x: -30, y: 0 }}); fade("#step", 0.05, 0.3, {{ x: 30, y: 0 }});
    tl.to("#hud i", {{ opacity: 0.2, duration: 0.5, yoyo: true, repeat: {int(DUR) // 2 * 2 - 1}, ease: "steps(1)" }}, 0.4);
    var STEPS = [0, A.masalah, A.tahun, A.mei, A.dan, A.besok];
    STEPS.forEach(function (t, k) {{ tl.to("#step b:nth-child(" + (k + 1) + ")", {{ backgroundColor: "#39FF88", duration: 0.15 }}, q(t + 0.05)); }});

    // HOOK: prompt typed from frame 0, counter to 129.000, grid with red holes
    cut("#prompt", 0, 1); type("#pt", 0, 0.7, "scan --celah --4bulan");
    tl.fromTo("#cnt", {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.4)" }}, 0.1);
    count("#cnt", A.dalam, A.celah1 - A.dalam + 0.3, 0, 129000, function (v) {{ return idn(v) + (v > 128999 ? "+" : ""); }});
    flash(A.celah1 + 0.35, "#flash", 0.22); kick(A.celah1 + 0.35, 12);
    sweep("#h1a", A.ai1, 0.4); fade("#h1b", A.celah1 + 0.2, 0.3, {{ y: 10 }});
    tl.fromTo("#grid", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, q(A.dalam));
    tl.fromTo("#grid i.h", {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "back.out(2)", stagger: (A.celah1 - A.dalam) / 22 }}, q(A.dalam + 0.2));
    hide("#prompt, #cnt, #h1a, #h1b, #grid", A.masalah - 0.12, 0.12);

    // HALF WAY: find OK, patch waits for humans
    sweep("#h2a", A.masalah, 0.4);
    tl.fromTo("#s1", {{ opacity: 0, x: -80 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "back.out(1.4)" }}, q(A.masalah + 0.4));
    tl.fromTo("#s2", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "back.out(1.4)" }}, q(A.tetap));
    tl.to("#s2s", {{ opacity: 0.25, duration: 0.25, yoyo: true, repeat: 5, ease: "steps(1)" }}, q(A.tetap + 0.3));
    cut("#halfbar", A.setengah, 1);
    var hb = {{ n: 0 }}, hel = document.querySelector("#halfbar");
    tl.to(hb, {{ n: 10, duration: 0.6, ease: "power2.out", onUpdate: function () {{ var k = Math.round(hb.n);
      hel.textContent = "[" + "#".repeat(k) + "-".repeat(20 - k) + "] " + (k * 5) + "%"; }} }}, q(A.setengah));
    hide("#h2a, #s1, #s2, #halfbar", A.tahun - 0.12, 0.12);

    // GOOGLE BIG SLEEP flow
    sweep("#h3a", A.tahun, 0.4); fade("#h3b", A.google, 0.3, {{ y: 10 }});
    tl.fromTo("#n1", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.4)" }}, q(A.hacker - 0.5));
    tl.to("#n1", {{ x: 8, duration: 0.06, yoyo: true, repeat: 5, ease: "none" }}, q(A.hacker - 0.1));
    tl.to("#l1", {{ scaleY: 1, duration: 0.3, ease: "power2.out" }}, q(A.untung - 0.4));
    tl.fromTo("#n2", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.4)" }}, q(A.untung - 0.15));
    tl.to("#l2", {{ scaleY: 1, duration: 0.3, ease: "power2.out" }}, q(A.ditambal1 - 0.3));
    tl.fromTo("#n3", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }}, q(A.ditambal1));
    tl.to("#n1", {{ opacity: 0.35, duration: 0.2 }}, q(A.ditambal1 + 0.2));
    hide("#h3a, #h3b, #n1, #n2, #n3, #l1, #l2", A.tapi - 0.12, 0.12);

    // LOOP: glitch
    tl.fromTo("#glitch", {{ opacity: 0.9 }}, Object.assign({{ opacity: 0, duration: 0.3, ease: "steps(3)" }}, NI), q(A.tapi));
    kick(A.tapi, 14); sweep("#h4a", A.tapi + 0.05, 0.35);
    tl.to("#h4a", {{ x: -10, duration: 0.05, yoyo: true, repeat: 3 }}, q(A.tapi + 0.6));
    hide("#h4a", A.mei - 0.12, 0.12);

    // 530 vs 75
    sweep("#h5a", A.mei, 0.4); fade("#h5b", A.mei + 0.3, 0.3, {{ y: 10 }});
    fade("#b1", A.lima - 0.1, 0.3, {{ y: 20 }});
    tl.to("#b1 .fl", {{ scaleX: 1, duration: 1.0, ease: "power2.out" }}, q(A.lima));
    count("#v1", A.lima, 1.0, 0, 530, function (v) {{ return Math.round(v); }});
    fade("#b2", A.baru75 - 0.1, 0.3, {{ y: 20 }});
    tl.to("#b2 .fl", {{ scaleX: 1, duration: 0.7, ease: "power2.out" }}, q(A.tujuh));
    count("#v2", A.tujuh, 0.7, 0, 75, function (v) {{ return Math.round(v); }});
    pop("#gap", A.ditambal2, 0.35); kick(A.ditambal2 + 0.1, 10);
    hide("#h5a, #h5b, #b1, #b2, #gap", A.dan - 0.12, 0.12);

    // PAYOFF: the patch only protects you once installed
    sweep("#h6a", A.dan, 0.4);
    tl.fromTo("#notif", {{ opacity: 0, y: -120 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.4)" }}, q(A.dan + 0.3)); cut("#sim1", A.dan + 0.3, 1);
    tl.set("#sim1", {{ top: 1180 }}, 0);
    tl.fromTo("#crack", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.15, ease: "power4.in" }}, q(A.kalau1));
    tl.to("#bLater", {{ opacity: 0.35, duration: 0.2 }}, q(A.kalau1 + 0.25));
    tl.fromTo("#ember", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, q(A.kalau1));
    tl.fromTo("#tap", {{ opacity: 0, x: 60, y: 60 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.3, ease: "power2.out" }}, q(A.pasang1 - 0.75));
    tl.to("#bNow", {{ scale: 0.92, duration: 0.08, yoyo: true, repeat: 1 }}, q(A.pasang1 - 0.4));
    tl.to("#bNow", {{ boxShadow: "0 0 50px rgba(57,255,136,.9)", duration: 0.2 }}, q(A.pasang1 - 0.3));
    cut("#ok", A.pasang1 - 0.3, 1); type("#ok", A.pasang1 - 0.3, 0.45, "> celah ditutup ........ [OK]");
    flash(A.pasang1 - 0.3, "#flash", 0.18);
    hide("#h6a, #notif, #tap, #ok, #sim1, #ember", A.besok - 0.12, 0.12);

    // CTA SERI
    fade("#h7a", A.besok, 0.3, {{ y: 10 }}); sweep("#h7b", A.besok + 0.3, 0.4); sweep("#h7c", A.pencuri - 0.1, 0.45);
    tl.set("#h7c", {{ top: 450 }}, 0);
    pop("#follow", A.follow - 0.05, 0.35);
    tl.fromTo("#tapc", {{ opacity: 0, x: 60, y: 60 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.3, ease: "power2.out" }}, q(A.follow + 0.2));
    tl.to("#follow", {{ scale: 0.92, duration: 0.08, yoyo: true, repeat: 1 }}, q(A.follow + 0.5));
    tl.to("#follow", {{ backgroundColor: "#D8FFE8", duration: 0.1 }}, q(A.follow + 0.58));
    hide("#h7a, #h7b, #h7c, #follow, #tapc", A.kalau2 - 0.12, 0.12);

    // CTA KOMENTAR
    sweep("#h8a", A.kalau2, 0.4);
    tl.fromTo("#oA", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }}, q(A.langsung - 0.05));
    tl.fromTo("#oB", {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }}, q(A.nunggu - 0.05));
    fade("#h8b", A.maksa, 0.3, {{ y: 10 }});
'''
js += chibi_js(track, emph_t, CHIBI_IN)

(HERE / "public" / "index.html").write_text(page("ai-ngelawan-balik", DUR, css, body, js), encoding="utf-8")
print("ok", DUR, json.dumps({k: round(v, 2) for k, v in A.items()}))
