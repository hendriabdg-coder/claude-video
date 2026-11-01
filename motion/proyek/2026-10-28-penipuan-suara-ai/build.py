# Reel Rabu 28 Okt · "Suara Temanmu Bisa Palsu" · seri Internet Jebol · gaya TERMINAL (CRT black, phosphor green,
# amber warnings, typed lines). Call screen + waveforms are SIMULASI. VO: output/motion/2026-10-28-penipuan-suara-ai/vo
# (naskah final Endrich, CTA "part tiga" by his choice). Sources: riset.md.
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
from reel_common import ICON, chars, chibi_anim_html, chibi_anim_js, fitpx, page, setup, words  # noqa: E402

SLUG = "2026-10-28-penipuan-suara-ai"
DUR = setup(HERE, SLUG)
T = words(SLUG)
random.seed(3)

css = '''
:root { --bg:#050807; --g:#39FF88; --gd:rgba(57,255,136,.45); --amb:#FFB000; --red:#FF4A4A; --w:#D8FFE8; }
html, body, #root { background: var(--bg); color: var(--g); font-family: Consolas, "Courier New", monospace; }
#crt { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 45%, rgba(57,255,136,.08) 0%, rgba(0,0,0,0) 70%); }
#scan { position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,.28) 0px, rgba(0,0,0,.28) 2px, rgba(0,0,0,0) 2px, rgba(0,0,0,0) 5px); pointer-events: none; }
#vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 75% at 50% 50%, rgba(0,0,0,0) 60%, rgba(0,0,0,.85) 100%); pointer-events: none; }
#cam { position: absolute; inset: 0; }
#hud { position: absolute; left: 60px; top: 262px; display: flex; align-items: center; gap: 14px; font-size: 24px; letter-spacing: .2em; color: var(--gd); opacity: 0; }
#hud i { width: 14px; height: 14px; border-radius: 50%; background: var(--red); box-shadow: 0 0 10px var(--red); display: inline-block; }
.t { position: absolute; left: 0; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; }
.t .ch { opacity: 0; }
.bigt { font-family: "IDBlack"; color: var(--g); text-shadow: 0 0 18px rgba(57,255,136,.7); }
.ambt { font-family: "IDBlack"; color: var(--amb); text-shadow: 0 0 18px rgba(255,176,0,.6); }
.lbl { position: absolute; left: 0; width: 1080px; text-align: center; font-size: 26px; letter-spacing: .2em; color: var(--gd); opacity: 0; }
#money { position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; font-family: "IDBlack"; font-size: 94px; color: var(--amb); text-shadow: 0 0 24px rgba(255,176,0,.7); opacity: 0; }
#call { position: absolute; left: 290px; top: 640px; width: 500px; height: 640px; border-radius: 48px; border: 2px solid var(--gd); background: rgba(5,16,10,.9); opacity: 0; text-align: center; }
#call .av { margin: 70px auto 0; width: 170px; height: 170px; border-radius: 50%; border: 3px solid var(--g); padding: 36px; color: var(--g); box-shadow: 0 0 30px rgba(57,255,136,.4); }
#call .nm { margin-top: 30px; font-family: "IDBlack"; font-size: 60px; color: var(--w); }
#call .st { margin-top: 8px; font-size: 26px; letter-spacing: .2em; color: var(--gd); }
#call .bt { position: absolute; bottom: 60px; width: 110px; height: 110px; border-radius: 50%; padding: 26px; }
#call .acc { left: 300px; background: var(--g); color: #04120a; }
#call .rej { left: 90px; background: var(--red); color: #fff; transform: rotate(135deg); }
.ringp { position: absolute; left: 455px; top: 725px; width: 170px; height: 170px; border-radius: 50%; border: 3px solid var(--g); opacity: 0; }
#win { position: absolute; left: 60px; top: 560px; width: 960px; height: 300px; border: 2px solid var(--gd); border-radius: 18px; background: rgba(5,12,9,.85); box-shadow: 0 0 40px rgba(57,255,136,.18); opacity: 0; overflow: hidden; }
#win .bar { height: 54px; border-bottom: 2px solid rgba(57,255,136,.25); display: flex; align-items: center; gap: 12px; padding: 0 22px; font-size: 22px; color: var(--gd); }
#win .bar i { width: 14px; height: 14px; border-radius: 50%; border: 2px solid var(--gd); display: inline-block; }
#win .bd { padding: 24px 30px; font-size: 40px; line-height: 1.5; color: var(--w); white-space: pre; }
.wave { position: absolute; left: 110px; width: 860px; height: 150px; border: 2px solid var(--gd); border-radius: 18px; padding: 14px 24px; opacity: 0; }
.wave .wl { font-size: 22px; letter-spacing: .2em; color: var(--gd); }
.wave .wb { display: flex; align-items: center; gap: 6px; height: 90px; }
.wave .wb i { flex: 1; background: var(--g); border-radius: 3px; transform-origin: 50% 50%; }
#w2 { border-color: rgba(255,176,0,.6); }
#w2 .wl { color: var(--amb); }
#w2 .wb i { background: var(--amb); }
.stampx { position: absolute; left: 360px; top: 1070px; padding: 12px 28px; border: 5px solid var(--amb); border-radius: 14px; font-family: "IDBlack"; font-size: 64px; color: var(--amb); background: rgba(255,176,0,.08); opacity: 0; }
#cnt { position: absolute; left: 0; width: 1080px; top: 560px; text-align: center; font-family: "IDBlack"; font-size: 220px; color: var(--g); text-shadow: 0 0 30px rgba(57,255,136,.7); opacity: 0; }
#rec { position: absolute; left: 240px; top: 600px; width: 600px; height: 260px; border: 2px solid var(--gd); border-radius: 20px; opacity: 0; padding: 30px 40px; }
#rec .rh { display: flex; align-items: center; gap: 16px; font-size: 28px; letter-spacing: .2em; color: var(--red); }
#rec .rh i { width: 22px; height: 22px; border-radius: 50%; background: var(--red); box-shadow: 0 0 14px var(--red); display: inline-block; }
#rec .rt { font-family: "IDBlack"; font-size: 130px; color: var(--w); margin-top: 6px; }
.chk { position: absolute; left: 80px; width: 860px; font-family: "IDBlack"; font-size: 42px; color: var(--w); opacity: 0; white-space: nowrap; }
.chk b { color: var(--g); font-weight: normal; margin-right: 18px; }
#warn { position: absolute; left: 90px; top: 560px; width: 900px; padding: 34px 40px; border: 4px solid var(--amb); border-radius: 18px; color: var(--amb); background: rgba(255,176,0,.06); box-shadow: 0 0 40px rgba(255,176,0,.25); opacity: 0; }
#warn .wh { font-family: "IDBlack"; font-size: 64px; }
#warn .ws { font-family: "IDBold"; font-size: 44px; color: var(--w); margin-top: 14px; line-height: 1.35; }
#follow { position: absolute; left: 340px; top: 540px; width: 400px; height: 96px; border-radius: 48px; background: var(--g); color: #04120a; font-family: "IDBlack"; font-size: 46px; display: flex; align-items: center; justify-content: center; opacity: 0; box-shadow: 0 0 40px rgba(57,255,136,.5); }
#tapc { position: absolute; left: 660px; top: 580px; width: 70px; height: 70px; color: var(--w); opacity: 0; }
.opt { position: absolute; top: 430px; width: 390px; height: 120px; border-radius: 20px; display: flex; align-items: center; gap: 14px; padding: 0 22px; font-family: "IDBlack"; font-size: 34px; opacity: 0; }
.opt .oi { width: 56px; height: 56px; flex: none; }
#oA { left: 120px; border: 4px solid var(--g); color: var(--g); background: rgba(57,255,136,.08); }
#oB { left: 540px; border: 4px solid var(--amb); color: var(--amb); background: rgba(255,176,0,.08); }
.sim { position: absolute; font-size: 22px; letter-spacing: .2em; color: var(--gd); padding: 6px 12px; border: 2px solid rgba(57,255,136,.3); border-radius: 8px; opacity: 0; }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-family: "IDBlack"; font-size: 36px; color: var(--w); }
#brand b { color: var(--g); font-weight: normal; }
#flash { position: absolute; inset: 0; background: var(--amb); opacity: 0; pointer-events: none; mix-blend-mode: screen; }
'''


def TX(tid, text, top, px, cls="bigt"):
    return f'<div class="t {cls}" id="{tid}" style="top:{top}px;font-size:{fitpx(text, px)}px">{chars(text)}</div>'


BARS = [random.randint(18, 100) for _ in range(40)]
WB = "".join(f'<i style="height:{h}%"></i>' for h in BARS)
# animated chibi (keyed loop clips): point up at the next-part promise, press the virtual button on "Follow",
# shocked on "suara palsu", shrug on "atau video call palsu?"
CLIPS = [("menunjuk_keatas", T[58] - 0.2, T[58] + 3.8), ("Menekan_Tombol_Virtual", T[58] + 3.8, T[74] - 0.1),
         ("Terkejut", T[74] - 0.1, T[80] - 0.1), ("tidak_tahu", T[80] - 0.1, DUR)]

body = f'''
  <div id="crt"></div>
  <div id="cam">
    <div id="hud"><i></i>INTERNET JEBOL &middot; PENIPUAN SUARA</div>
    <!-- hook -->
    <div id="money">Rp0</div>
    {TX("h1b", "TELEPON DARI 'TEMAN'", 480, 72, "ambt")}
    {TX("h1c", "SUARA AI?", 1360, 80)}
    <div class="ringp" id="rp1"></div><div class="ringp" id="rp2"></div>
    <div id="call"><div class="av">{ICON["phone"]}</div><div class="nm">Teman</div><div class="st">PANGGILAN MASUK</div>
      <div class="bt rej">{ICON["phone"]}</div><div class="bt acc">{ICON["phone"]}</div></div>
    <div class="sim" id="sim1" style="left:290px;top:1300px">SIMULASI</div>
    <!-- malang + waveforms -->
    {TX("h2a", "DILAPORKAN DI MALANG", 360, 84)}
    <div class="lbl" id="h2b" style="top:470px">SUMBER: OJK MALANG &middot; MALANG POST, 2 OKT 2026</div>
    <div class="wave" id="w1" style="top:640px"><div class="wl">SUARA ASLI &middot; TEMAN</div><div class="wb">{WB}</div></div>
    <div class="wave" id="w2" style="top:840px"><div class="wl">TIRUAN AI</div><div class="wb">{WB}</div></div>
    <div class="stampx" id="st1">DITIRU AI</div>
    <div class="sim" id="sim2" style="left:110px;top:1000px">SIMULASI</div>
    <!-- OJK + McAfee -->
    {TX("h3a", "LAPORAN TERINDIKASI AI", 360, 76)}
    <div id="cnt">0</div>
    <div class="lbl" id="h3b" style="top:820px">OJK &middot; NOV 2024 &ndash; JUN 2026</div>
    {TX("h3c", "BEBERAPA DETIK BISA CUKUP", 360, 76, "ambt")}
    <div id="rec"><div class="rh"><i></i>REC</div><div class="rt" id="rect">00:00</div></div>
    <div class="lbl" id="h3d" style="top:900px">RISET MCAFEE, 2023</div>
    <!-- checklist -->
    {TX("h4a", "LINDUNGI KELUARGA", 360, 84)}
    <div class="chk" id="c1" style="top:560px"><b>[1]</b><span id="c1t"></span></div>
    <div class="chk" id="c2" style="top:680px"><b>[2]</b><span id="c2t"></span></div>
    <div class="chk" id="c3" style="top:800px"><b>[3]</b><span id="c3t"></span></div>
    <div id="warn"><div class="wh">KENA?</div><div class="ws">1. Hubungi bank<br>2. Lapor IASC / OJK 157</div></div>
    <!-- CTA -->
    <div class="lbl" id="h6a" style="top:340px">MINGGU DEPAN &middot; INTERNET JEBOL PART 3</div>
    {TX("h6b", "CEK VIDEO CALL PALSU", 400, 84)}
    <div id="follow">+ FOLLOW</div><div id="tapc">{ICON["cursor"]}</div>
    {TX("h7a", "LEBIH TAKUT MANA?", 330, 84, "ambt")}
    <div class="opt" id="oA"><span class="oi">{ICON["phone"]}</span>SUARA PALSU</div>
    <div class="opt" id="oB"><span class="oi">{ICON["video"]}</span>VIDEO CALL PALSU</div>
    <div class="lbl" id="h7b" style="top:580px">TULIS DI KOMENTAR</div>
    {chibi_anim_html(HERE, CLIPS)}
  </div>
  <div id="scan"></div><div id="vig"></div><div id="flash"></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

js = f'''
    var T = {T}, DUR = {DUR};
    tl.to("#crt", {{ opacity: 0.6, duration: 0.07, yoyo: true, repeat: {int(DUR / 0.14) // 2 * 2 - 1}, ease: "steps(1)" }}, 0.3);
    fade("#hud", 0.1, 0.3, {{ x: -30, y: 0 }});
    tl.to("#hud i", {{ opacity: 0.2, duration: 0.5, yoyo: true, repeat: {int(DUR) // 2 * 2 - 1}, ease: "steps(1)" }}, 0.4);

    // HOOK: 80 juta drains to 0, incoming call from "Teman"
    tl.fromTo("#money", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }}, 0);
    // loss counter (not a balance): 0 -> minus 80 juta, as reported
    count("#money", T[1], 0.9, 0, 80000000, function (v) {{ return "−Rp" + idn(v); }});
    tl.to("#money", {{ color: "#FF4A4A", textShadow: "0 0 24px rgba(255,74,74,.8)", duration: 0.2 }}, q(T[3]));
    flash(T[3] + 0.9, "#flash", 0.25); kick(T[3] + 0.9, 12);
    tl.fromTo("#call", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, 0.15);
    cut("#sim1", 0.3, 1);
    ["#rp1", "#rp2"].forEach(function (r, k) {{
      tl.fromTo(r, {{ opacity: 0.8, scale: 1 }}, {{ opacity: 0, scale: 1.9, duration: 1.0, repeat: 3, ease: "power1.out" }}, 0.4 + 0.5 * k);
    }});
    tl.fromTo("#call", {{ rotation: -1.5 }}, Object.assign({{ rotation: 1.5, duration: 0.08, yoyo: true, repeat: 17, ease: "none" }}, NI), 0.5);
    tl.set("#call", {{ rotation: 0 }}, q(2.0));
    sweep("#h1b", T[6], 0.35);
    sweep("#h1c", T[9] - 0.2, 0.3);
    hide("#money, #h1b, #h1c, #call, #sim1", T[10] - 0.15, 0.15);

    // MALANG + VOICE CLONE
    sweep("#h2a", T[11] - 0.1, 0.4); fade("#h2b", T[13], 0.3, {{ y: 10 }});
    fade("#w1", T[14], 0.35, {{ y: 30 }}); cut("#sim2", T[14], 1);
    tl.fromTo("#w1 .wb i", {{ scaleY: 0.1 }}, {{ scaleY: 1, duration: 0.3, stagger: 0.012, ease: "power2.out" }}, q(T[14]));
    fade("#w2", T[16], 0.35, {{ y: 30 }});
    tl.fromTo("#w2 .wb i", {{ scaleY: 0.1 }}, {{ scaleY: 1, duration: 0.3, stagger: 0.012, ease: "power2.out" }}, q(T[16]));
    tl.fromTo("#st1", {{ opacity: 0, scale: 1.7, rotation: -6 }}, {{ opacity: 1, scale: 1, rotation: -6, duration: 0.22, ease: "power4.in" }}, q(T[17]));
    flash(T[17] + 0.22, "#flash", 0.2); kick(T[17] + 0.22, 10);
    hide("#h2a, #h2b, #w1, #w2, #st1, #sim2", T[19] - 0.15, 0.15);

    // OJK COUNT + MCAFEE
    sweep("#h3a", T[19], 0.4);
    cut("#cnt", T[20], 1);
    count("#cnt", T[20], 1.6, 0, 1379, function (v) {{ return idn(v); }});
    fade("#h3b", T[24], 0.3, {{ y: 10 }});
    hide("#h3a, #cnt, #h3b", T[28] - 0.12, 0.12);
    fade("#h3d", T[29], 0.3, {{ y: 10 }}); sweep("#h3c", T[31], 0.4);
    tl.fromTo("#rec", {{ opacity: 0, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.8)" }}, q(T[28]));
    tl.to("#rec .rh i", {{ opacity: 0.2, duration: 0.3, yoyo: true, repeat: 9, ease: "steps(1)" }}, q(T[28]));
    count("#rect", T[31], 1.2, 0, 3, function (v) {{ return "00:0" + Math.floor(v); }});
    tl.to("#rect", {{ color: "#FFB000", duration: 0.15 }}, q(T[35]));
    hide("#h3c, #h3d, #rec", T[38] - 0.12, 0.12);

    // CHECKLIST (one point per beat)
    sweep("#h4a", T[38] - 0.05, 0.35);
    [["#c1", "#c1t", T[38], "TELEPON BALIK KE NOMOR LAMA"], ["#c2", "#c2t", T[44], "KATA RAHASIA KELUARGA"], ["#c3", "#c3t", T[49], "JANGAN KASIH OTP"]].forEach(function (c, k, a) {{
      cut(c[0], c[2], 1); type(c[1], c[2], 0.5, c[3]);
      if (k > 0) tl.to(a[k - 1][0], {{ opacity: 0.35, duration: 0.2 }}, q(c[2]));
    }});
    tl.to("#c3", {{ color: "#FFB000", duration: 0.15 }}, q(T[52]));
    hide("#h4a, #c1, #c2, #c3", T[52] + 0.45, 0.12);
    tl.fromTo("#warn", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.25, ease: "power3.out" }}, q(T[52] + 0.55));
    tl.to("#warn", {{ opacity: 0.5, duration: 0.1, yoyo: true, repeat: 3, ease: "steps(1)" }}, q(T[52] + 0.9));
    hide("#warn", T[58] - 0.15, 0.15);

    // CTA SERI
    fade("#h6a", T[53], 0.3, {{ y: 10 }}); sweep("#h6b", T[53] + 0.3, 0.4);
    pop("#follow", T[69] - 0.05, 0.35);
    tl.fromTo("#tapc", {{ opacity: 0, x: 60, y: 60 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.3, ease: "power2.out" }}, q(T[69] + 0.2));
    tl.to("#follow", {{ scale: 0.92, duration: 0.08, yoyo: true, repeat: 1 }}, q(T[69] + 0.5));
    tl.to("#follow", {{ backgroundColor: "#D8FFE8", duration: 0.1 }}, q(T[69] + 0.58));
    hide("#h6a, #h6b, #follow, #tapc", T[74] - 0.12, 0.12);

    // COMMENT CTA
    sweep("#h7a", T[74], 0.4);
    tl.fromTo("#oA", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }}, q(T[78] - 0.05));
    tl.fromTo("#oB", {{ opacity: 0, x: 60 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }}, q(T[81] - 0.05));
    fade("#h7b", T[83] + 0.4, 0.3, {{ y: 10 }});
'''
js += chibi_anim_js(T[58] - 0.2)

(HERE / "public" / "index.html").write_text(page("penipuan-suara-ai", DUR, css, body, js), encoding="utf-8")
print("ok", DUR, len(CLIPS), "chibi clips")
