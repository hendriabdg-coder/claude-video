# Reel Selasa 27 Okt · "Jawaban ChatGPT Bisa Diklik" · Update AI Minggu Ini #1 · gaya SIGNAL (charcoal + lime, HUD,
# UI objects). Phone mockups are labelled SIMULASI. VO: output/motion/2026-10-27-chatgpt-intelligent-ui/vo. Sources: riset.md.
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
from reel_common import ICON, chars, chibi_anim_html, chibi_anim_js, fitpx, page, setup, words  # noqa: E402

SLUG = "2026-10-27-chatgpt-intelligent-ui"
DUR = setup(HERE, SLUG)
T = words(SLUG)

css = '''
:root { --bg:#121314; --lime:#C6F432; --cream:#F2EEE3; --ink:#121314; --mute:rgba(242,238,227,.5); --line:rgba(242,238,227,.16); }
html, body, #root { background: var(--bg); color: var(--cream); font-family: "IDSemi"; }
#grid { position: absolute; inset: 0; background-image: linear-gradient(var(--line) 1px, transparent 1px), linear-gradient(90deg, var(--line) 1px, transparent 1px); background-size: 90px 90px; opacity: .25; }
#glow { position: absolute; left: 140px; top: 560px; width: 800px; height: 800px; border-radius: 50%; background: radial-gradient(circle, rgba(198,244,50,.16), rgba(198,244,50,0) 65%); }
#cam { position: absolute; inset: 0; transform-origin: 50% 50%; }
#prog { position: absolute; left: 0; top: 0; height: 6px; width: 1080px; background: var(--lime); transform-origin: 0 50%; }
#hud { position: absolute; left: 60px; top: 262px; display: flex; align-items: center; gap: 12px; font-family: Consolas, monospace; font-size: 24px; letter-spacing: .18em; opacity: 0; }
#hud i { width: 12px; height: 12px; border-radius: 50%; background: var(--lime); box-shadow: 0 0 10px var(--lime); display: inline-block; }
#hudR { position: absolute; right: 160px; top: 262px; font-family: Consolas, monospace; font-size: 24px; letter-spacing: .18em; color: var(--mute); opacity: 0; }
.h { position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDBlack"; line-height: 1; white-space: nowrap; opacity: 0; letter-spacing: -.01em; }
.h .ch { opacity: 0; }
.lime { color: var(--lime); }
.sub { position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDBold"; font-size: 48px; color: var(--cream); opacity: 0; }
.mono { position: absolute; left: 0; width: 1080px; text-align: center; font-family: Consolas, monospace; font-size: 26px; letter-spacing: .2em; color: var(--mute); opacity: 0; }
.pill { position: absolute; padding: 14px 30px; border-radius: 40px; font-family: "IDBlack"; font-size: 44px; opacity: 0; white-space: nowrap; }
.pill.l { background: var(--lime); color: var(--ink); }
.pill.o { border: 3px solid var(--lime); color: var(--lime); }
/* phone */
#phone { position: absolute; left: 300px; top: 560px; width: 480px; height: 860px; border-radius: 64px; background: #0b0c0d; border: 3px solid rgba(242,238,227,.22); box-shadow: 0 40px 100px rgba(0,0,0,.6), 0 0 60px rgba(198,244,50,.12); opacity: 0; overflow: hidden; }
#phone .notch { position: absolute; left: 180px; top: 18px; width: 120px; height: 30px; border-radius: 15px; background: #000; }
#phone .top { position: absolute; left: 0; top: 64px; width: 100%; text-align: center; font-family: "IDBold"; font-size: 26px; color: var(--mute); }
.bub { position: absolute; border-radius: 26px; font-family: "IDSemi"; font-size: 26px; line-height: 1.35; padding: 18px 22px; }
#ub { right: 24px; top: 130px; width: 340px; background: #2a2c2e; color: var(--cream); }
#ab { left: 24px; top: 300px; width: 400px; background: transparent; padding: 0; }
#ab i { display: block; height: 18px; border-radius: 9px; background: rgba(242,238,227,.25); margin-bottom: 16px; transform-origin: 0 50%; }
#strike { position: absolute; left: 14px; top: 330px; width: 420px; height: 8px; border-radius: 4px; background: #FF5A4A; transform-origin: 0 50%; opacity: 0; }
.card { position: absolute; left: 24px; top: 290px; width: 432px; height: 360px; border-radius: 28px; background: var(--cream); color: var(--ink); opacity: 0; padding: 26px; overflow: hidden; }
.card .ct { font-family: "IDBlack"; font-size: 30px; }
.card .cs { font-family: "IDSemi"; font-size: 22px; color: rgba(18,19,20,.55); margin-top: 4px; }
.bars { position: absolute; left: 30px; right: 30px; bottom: 30px; height: 210px; display: flex; align-items: flex-end; gap: 22px; }
.bars i { flex: 1; border-radius: 10px 10px 4px 4px; background: var(--ink); transform-origin: 50% 100%; }
.bars i.on { background: #7DAA00; }
.btns { margin-top: 40px; display: flex; flex-direction: column; gap: 18px; }
.btns b { display: block; padding: 20px; border-radius: 18px; border: 3px solid var(--ink); font-family: "IDBlack"; font-size: 30px; text-align: center; font-weight: normal; }
.btns b.on { background: var(--ink); color: var(--lime); }
.disp { margin-top: 16px; padding: 14px 20px; border-radius: 16px; background: var(--ink); color: var(--lime); font-family: "IDBlack"; font-size: 44px; text-align: right; }
.keys { margin-top: 14px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
.keys i { height: 30px; border-radius: 12px; background: rgba(18,19,20,.12); }
.keys i.on { background: var(--lime); }
#ring { position: absolute; width: 150px; height: 150px; border-radius: 34px; border: 6px solid var(--lime); box-shadow: 0 0 30px rgba(198,244,50,.7); opacity: 0; }
.mini { position: absolute; top: 720px; width: 150px; height: 150px; border-radius: 34px; background: var(--cream); color: var(--ink); padding: 34px; opacity: 0; }
.sim { position: absolute; left: 300px; top: 1440px; font-family: Consolas, monospace; font-size: 22px; letter-spacing: .2em; color: var(--mute); padding: 6px 12px; border: 2px solid var(--line); border-radius: 8px; opacity: 0; }
/* plans */
.plan { position: absolute; top: 560px; width: 420px; height: 520px; border-radius: 34px; padding: 34px; opacity: 0; }
#pf { left: 90px; background: var(--cream); color: var(--ink); }
#pp { left: 570px; border: 3px solid var(--line); }
.plan .pn { font-family: "IDBlack"; font-size: 60px; }
.plan .pr { margin-top: 26px; font-family: "IDBold"; font-size: 32px; display: flex; align-items: center; gap: 14px; }
.plan .pr .ic { width: 38px; height: 38px; flex: none; }
.plan .rb { margin-top: 34px; height: 26px; border-radius: 13px; background: rgba(18,19,20,.12); overflow: hidden; }
.plan .rb i { display: block; height: 100%; width: 100%; background: repeating-linear-gradient(45deg, var(--ink) 0 14px, #3a3d40 14px 28px); transform-origin: 0 50%; }
/* note */
#note { position: absolute; left: 230px; top: 470px; width: 620px; height: 150px; border-radius: 26px; background: #1d1f21; border: 2px solid var(--line); padding: 22px 28px; display: flex; align-items: center; gap: 22px; opacity: 0; }
#note .nb { flex: 1; height: 100px; display: flex; align-items: flex-end; gap: 12px; }
#note .nb i { flex: 1; background: var(--lime); border-radius: 6px 6px 2px 2px; }
#note .ng { width: 90px; height: 90px; color: var(--lime); }
/* series */
.week { position: absolute; left: 150px; top: 490px; width: 760px; display: flex; gap: 12px; opacity: 0; }
.week b { flex: 1; height: 100px; border-radius: 20px; border: 2px solid var(--line); display: flex; align-items: center; justify-content: center; font-family: "IDBlack"; font-size: 30px; font-weight: normal; color: var(--mute); }
.week b.on { background: var(--lime); color: var(--ink); border-color: var(--lime); box-shadow: 0 0 30px rgba(198,244,50,.5); }
#follow { position: absolute; left: 340px; top: 600px; width: 400px; height: 80px; border-radius: 40px; background: var(--lime); color: var(--ink); font-family: "IDBlack"; font-size: 46px; display: flex; align-items: center; justify-content: center; opacity: 0; }
#tapc { position: absolute; left: 660px; top: 630px; width: 70px; height: 70px; color: var(--cream); opacity: 0; }
.opt { position: absolute; top: 450px; width: 300px; height: 120px; border-radius: 60px; display: flex; align-items: center; justify-content: center; font-family: "IDBlack"; font-size: 50px; opacity: 0; }
#oA { left: 200px; background: var(--lime); color: var(--ink); }
#oB { left: 580px; border: 4px solid var(--cream); color: var(--cream); }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-family: "IDBlack"; font-size: 36px; color: var(--cream); }
#brand b { color: var(--lime); font-weight: normal; }
#flash { position: absolute; inset: 0; background: var(--lime); opacity: 0; pointer-events: none; }
'''


def H(hid, text, top, px, cls=""):
    return f'<div class="h {cls}" id="{hid}" style="top:{top}px;font-size:{fitpx(text, px)}px">{chars(text)}</div>'


CHART = '<div class="bars">' + "".join(f'<i style="height:{h}%"{" class=on" if k == 3 else ""}></i>' for k, h in enumerate([40, 62, 50, 92, 70])) + '</div>'
# animated chibi (keyed loop clips): attention gesture on "satu catatan", nod on "tetap kamu cek", explaining the
# weekly recap, pressing the virtual button on "Follow", confused on the closing question
CLIPS = [("Gestur_Berhenti___Perhatikan", T[40] - 0.3, T[47]), ("Setuju", T[47], T[52] - 0.05),
         ("gerakan_menjelaskan", T[52] - 0.05, T[61] - 0.05), ("Menekan_Tombol_Virtual", T[61] - 0.05, T[70] - 0.05),
         ("Bingung", T[70] - 0.05, DUR)]

body = f'''
  <div id="grid"></div><div id="glow"></div><div id="prog"></div>
  <div id="cam">
    {H("h1a", "ChatGPT sekarang", 340, 72)}
    {H("h1b", "NGGAK CUMA TEKS", 430, 120, "lime")}
    {H("h2a", "INTELLIGENT UI", 300, 130, "lime")}
    <div class="pill l" id="p1" style="left:270px;top:450px">GPT-6</div>
    <div class="pill o" id="p2" style="left:520px;top:450px">7 OKT 2026</div>
    <div class="sub" id="h3a" style="top:330px">jawabannya bisa jadi</div>
    {H("h3b", "GRAFIK", 400, 120, "lime")}{H("h3c", "TOMBOL", 400, 120, "lime")}{H("h3d", "KALKULATOR", 400, 120, "lime")}
    {H("h3e", "AI YANG MILIH FORMAT", 400, 96, "lime")}
    <div id="phone"><div class="notch"></div><div class="top">ChatGPT</div>
      <div class="bub" id="ub">Patungan ber-4, total 480 ribu. Bagi dong?</div>
      <div class="bub" id="ab"><i style="width:92%"></i><i style="width:80%"></i><i style="width:88%"></i><i style="width:60%"></i></div>
      <div id="strike"></div>
      <div class="card" id="cg"><div class="ct">Pengeluaran</div><div class="cs">per orang</div>{CHART}</div>
      <div class="card" id="cb"><div class="ct">Cara bagi?</div><div class="btns"><b class="on">Bagi rata</b><b>Per item</b><b>+ Tip</b></div></div>
      <div class="card" id="ck"><div class="ct">Pembagi tagihan</div><div class="disp">Rp120.000</div>
        <div class="keys">{"".join(f'<i{" class=on" if k in (3, 7, 15) else ""}></i>' for k in range(16))}</div></div>
    </div>
    <div class="mini" id="m1" style="left:150px">{ICON["chat"]}</div><div class="mini" id="m2" style="left:465px">{ICON["check"]}</div><div class="mini" id="m3" style="left:780px">{ICON["cursor"]}</div>
    <div id="ring" style="left:150px;top:720px"></div>
    <div class="sim" id="sim">SIMULASI</div>
    {H("h4a", "GRATIS JUGA KEBAGIAN", 360, 100)}
    <div class="plan" id="pf"><div class="pn">Gratis</div>
      <div class="pr"><span class="ic">{ICON["check"]}</span>mulai 8 Okt</div><div class="pr"><span class="ic">{ICON["check"]}</span>versi dasar</div>
      <div class="pr" style="margin-top:40px">bertahap</div><div class="rb"><i id="rbi"></i></div></div>
    <div class="plan" id="pp"><div class="pn">Plus/Pro</div>
      <div class="pr"><span class="ic" style="color:#C6F432">{ICON["check"]}</span>mulai 7 Okt</div></div>
    <div class="mono" id="h4b" style="top:1130px">ANGKA KUOTA BELUM DIUMUMKAN</div>
    <div class="sub" id="h5a" style="top:330px">satu catatan dari aku</div>
    <div id="note"><div class="nb"><i style="height:50%"></i><i style="height:75%"></i><i style="height:35%"></i><i style="height:95%"></i></div><div class="ng">{ICON["alert"]}</div></div>
    {H("h5b", "RAPI ≠ PASTI BENAR", 360, 96)}
    {H("h6a", "UPDATE AI MINGGU INI", 340, 96, "lime")}
    <div class="week" id="wk"><b>SEN</b><b class="on">SEL</b><b>RAB</b><b>KAM</b><b>JUM</b><b>SAB</b><b>MIN</b></div>
    <div id="follow">+ FOLLOW</div><div id="tapc">{ICON["cursor"]}</div>
    <div class="mono" id="h6b" style="top:440px">EDISI #2 &middot; SELASA DEPAN</div>
    {H("h7a", "UDAH DAPET FITUR INI?", 340, 92)}
    <div class="opt" id="oA">UDAH</div><div class="opt" id="oB">BELUM</div>
    <div class="mono" id="h7b" style="top:600px">TULIS DI KOMENTAR</div>
    {chibi_anim_html(HERE, CLIPS)}
  </div>
  <div id="flash"></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

js = f'''
    var T = {T}, DUR = {DUR};
    tl.fromTo("#prog", {{ scaleX: 0 }}, {{ scaleX: 1, duration: DUR, ease: "none" }}, 0);
    tl.fromTo("#grid", {{ y: 0 }}, {{ y: -90, duration: DUR, ease: "none" }}, 0);

    // HOOK: plain-text answer gets struck out
    sweep("#h1a", 0.05, 0.3); sweep("#h1b", T[2], 0.4);
    tl.fromTo("#phone", {{ opacity: 0, y: 120, rotation: -4 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "power3.out" }}, 0);
    cut("#sim", 0.3, 1);
    tl.fromTo("#ub", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }}, 0.35);
    tl.fromTo("#ab i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, stagger: 0.18, ease: "power2.out" }}, 0.8);
    tl.fromTo("#strike", {{ opacity: 1, scaleX: 0 }}, {{ opacity: 1, scaleX: 1, duration: 0.25, ease: "power3.in" }}, q(T[6]));
    flash(T[6] + 0.2, "#flash", 0.25); kick(T[6] + 0.2, 10);
    hide("#h1a, #h1b", T[7] - 0.12, 0.12);
    tl.to("#ab, #strike", {{ opacity: 0, duration: 0.2 }}, q(T[7]));

    // INTELLIGENT UI
    sweep("#h2a", T[8] - 0.1, 0.45); pop("#p1", T[12]); pop("#p2", T[15]);
    hide("#h2a, #p1, #p2", T[17] - 0.12, 0.12);

    // GRAFIK / TOMBOL / KALKULATOR
    fade("#h3a", T[17], 0.3, {{ y: 14 }});
    [["#h3b", "#cg", T[20]], ["#h3c", "#cb", T[21]], ["#h3d", "#ck", T[23]]].forEach(function (s, k, a) {{
      sweep(s[0], s[2] - 0.05, 0.3);
      tl.fromTo(s[1], {{ opacity: 0, scale: 0.85, y: 40 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }}, q(s[2] - 0.05));
      var end = k < 2 ? a[k + 1][2] - 0.1 : T[24] - 0.1;
      hide(s[0], end, 0.1); if (k < 2) hide(s[1], end, 0.1);
    }});
    tl.fromTo("#cg .bars i", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.4, stagger: 0.06, ease: "back.out(1.6)" }}, q(T[20]));
    tl.to("#cb .btns b:nth-child(2)", {{ backgroundColor: "#121314", color: "#C6F432", duration: 0.1 }}, q(T[22]));
    count("#ck .disp", T[23] + 0.1, 0.7, 0, 120000, function (v) {{ return "Rp" + idn(v); }});
    hide("#h3a", T[24] - 0.1, 0.1);
    // AI picks the format: phone steps back, three format tiles, selection ring hops
    tl.to("#phone", {{ y: 240, scale: 0.8, opacity: 0.25, duration: 0.4, ease: "power2.inOut" }}, q(T[24] - 0.1));
    sweep("#h3e", T[24], 0.4);
    ["#m1", "#m2", "#m3"].forEach(function (m, k) {{ pop(m, T[24] + 0.1 * k, 0.3); }});
    cut("#ring", T[25], 1);
    tl.to("#ring", {{ x: 315, duration: 0.18, ease: "power2.inOut" }}, q(T[26]));
    tl.to("#ring", {{ x: 630, duration: 0.18, ease: "power2.inOut" }}, q(T[27]));
    tl.to("#ring", {{ x: 315, duration: 0.25, ease: "back.out(2)" }}, q(T[28]));
    tl.to("#m2", {{ backgroundColor: "#C6F432", scale: 1.1, duration: 0.2 }}, q(T[28] + 0.2));
    hide("#h3e, #m1, #m2, #m3, #ring, #phone, #ck, #sim", T[29] - 0.12, 0.12);

    // FREE vs PLUS
    sweep("#h4a", T[29], 0.4);
    tl.fromTo("#pp", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, q(T[29] + 0.1));
    tl.fromTo("#pf", {{ opacity: 0, x: -80, rotation: -3 }}, {{ opacity: 1, x: 0, rotation: -2, duration: 0.45, ease: "back.out(1.6)" }}, q(T[30]));
    tl.fromTo("#pf .pr", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.25, stagger: 0.5, ease: "power2.out" }}, q(T[34]));
    tl.fromTo("#rbi", {{ scaleX: 0 }}, {{ scaleX: 0.45, duration: 1.2, ease: "power1.inOut" }}, q(T[39] - 0.2));
    fade("#h4b", T[39], 0.3, {{ y: 10 }});
    hide("#h4a, #pf, #pp, #h4b", T[40] - 0.12, 0.12);

    // NOTE (opini) — chibi arrives
    fade("#h5a", T[40], 0.3, {{ y: 14 }});
    tl.fromTo("#note", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, q(T[44]));
    tl.fromTo("#note .nb i", {{ scaleY: 0 }}, {{ scaleY: 1, transformOrigin: "50% 100%", duration: 0.3, stagger: 0.06 }}, q(T[44]));
    hide("#h5a", T[46] - 0.1, 0.1); sweep("#h5b", T[46], 0.35);
    tl.to("#note .ng", {{ scale: 1.25, duration: 0.15, yoyo: true, repeat: 3 }}, q(T[47]));
    hide("#h5b, #note", T[52] - 0.12, 0.12);

    // SERIES CTA
    sweep("#h6a", T[52], 0.4);
    tl.fromTo("#wk", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, q(T[53]));
    tl.fromTo("#wk b.on", {{ scale: 0.6 }}, {{ scale: 1, duration: 0.35, ease: "back.out(2.5)" }}, q(T[53] + 0.2));
    pop("#follow", T[59], 0.35);
    tl.fromTo("#tapc", {{ opacity: 0, x: 60, y: 60 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.3, ease: "power2.out" }}, q(T[61] + 0.2));
    tl.to("#follow", {{ scale: 0.92, duration: 0.08, yoyo: true, repeat: 1 }}, q(T[61] + 0.5));
    tl.to("#follow", {{ backgroundColor: "#F2EEE3", duration: 0.1 }}, q(T[61] + 0.58));
    fade("#h6b", T[64], 0.3, {{ y: 10 }});
    hide("#h6a, #wk, #follow, #tapc, #h6b", T[70] - 0.12, 0.12);

    // COMMENT CTA
    sweep("#h7a", T[70], 0.4);
    tl.fromTo("#oA", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, q(T[72]));
    tl.fromTo("#oB", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, q(T[76]));
    fade("#h7b", T[76] + 0.5, 0.3, {{ y: 10 }});
'''
js += chibi_anim_js(T[40] - 0.3)

(HERE / "public" / "index.html").write_text(page("chatgpt-intelligent-ui", DUR, css, body, js), encoding="utf-8")
print("ok", DUR, len(CLIPS), "chibi clips")
