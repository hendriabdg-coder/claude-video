# Style template 02 · PAPER — light flat infographic (after ref-motion-3): cream canvas, soft circles, flat objects that
# morph, counters and calendars, one orange accent; calm. Best for money, data, simulations, "hitung-hitungan".
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from gaya_common import page, words  # noqa: E402

T = words("paper")

def svg(body, sw=6):
    return (f'<svg class="ico" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>')

CARD = svg('<rect x="14" y="20" width="72" height="60" rx="12"/><path d="M30 42h40M30 56h24"/><circle cx="72" cy="58" r="6"/>')

css = '''
:root { --bg:#F1ECE2; --ink:#1E1B18; --org:#D9622B; --mute:rgba(30,27,24,.5); --card:#FBF8F2; }
html, body, #root { background: var(--bg); color: var(--ink); font-family: "IDSemi", sans-serif; }
.blob { position: absolute; border-radius: 50%; background: rgba(30,27,24,.045); }
.head { position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDBlack"; text-transform: uppercase; line-height: 1.02; opacity: 0; }
.head em { font-style: normal; color: var(--org); }
.sub { position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDBlack"; font-size: 40px; letter-spacing: .02em; color: var(--mute); opacity: 0; }
.app { position: absolute; top: 760px; width: 260px; height: 300px; border-radius: 34px; background: var(--card); box-shadow: 0 18px 40px rgba(30,27,24,.12); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; opacity: 0; }
.app .ai { width: 110px; height: 110px; color: var(--ink); }
.app b { font-family: "IDBold"; font-weight: normal; font-size: 30px; color: var(--mute); }
.tag { position: absolute; top: 1080px; width: 260px; text-align: center; opacity: 0; }
.tag span { display: inline-block; font-family: "IDBlack"; font-size: 40px; color: #fff; background: var(--org); padding: 8px 22px; border-radius: 999px; }
#small { position: absolute; left: 0; width: 1080px; top: 1220px; text-align: center; font-family: "IDItal"; font-size: 64px; color: var(--org); opacity: 0; }
#cal { position: absolute; left: 190px; top: 640px; width: 700px; padding: 36px; border-radius: 30px; background: var(--card); box-shadow: 0 18px 40px rgba(30,27,24,.12); opacity: 0; }
#cal .ch { font-family: "IDBlack"; font-size: 28px; letter-spacing: .14em; color: var(--mute); }
#cal .g { display: grid; grid-template-columns: repeat(6, 1fr); gap: 18px; margin-top: 26px; }
#cal .m { height: 84px; border-radius: 16px; background: rgba(30,27,24,.06); display: flex; align-items: center; justify-content: center; font-family: "IDBold"; font-size: 24px; color: var(--mute); position: relative; }
#cal .m i { position: absolute; right: 10px; top: 10px; width: 18px; height: 18px; border-radius: 50%; background: var(--org); transform: scale(0); }
#usd { position: absolute; left: 0; width: 1080px; top: 1120px; text-align: center; font-family: "IDBlack"; font-size: 150px; color: var(--ink); opacity: 0; }
#idr { position: absolute; left: 0; width: 1080px; top: 1300px; text-align: center; opacity: 0; }
#idr span { display: inline-block; font-family: "IDBlack"; font-size: 96px; color: var(--org); }
#kurs { position: absolute; left: 0; width: 1080px; top: 1430px; text-align: center; opacity: 0; }
#kurs span { display: inline-block; font-family: "IDBlack"; font-size: 24px; letter-spacing: .1em; color: #fff; background: var(--ink); padding: 8px 18px; border-radius: 999px; }
#end { position: absolute; inset: 0; background: var(--bg); opacity: 0; }
#end .n { position: absolute; left: 0; width: 1080px; top: 760px; text-align: center; font-family: "IDBlack"; font-size: 46px; letter-spacing: .3em; color: var(--mute); }
#end .t { position: absolute; left: 0; width: 1080px; top: 830px; text-align: center; font-family: "IDBlack"; font-size: 200px; color: var(--ink); }
#end .t em { font-style: normal; color: var(--org); }
#end .d { position: absolute; left: 0; width: 1080px; top: 1080px; text-align: center; font-family: "IDBold"; font-size: 40px; color: var(--mute); }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-family: "IDBlack"; font-size: 36px; color: var(--ink); }
#brand b { color: var(--org); font-weight: normal; }
'''

apps = "".join(f'<div class="app" id="ap{k}" style="left:{90 + k * 310}px"><span class="ai">{CARD}</span><b>Tools AI #{k + 1}</b></div>'
               f'<div class="tag" id="tg{k}" style="left:{90 + k * 310}px"><span>$20/bln</span></div>' for k in range(3))
months = "".join(f'<div class="m">{m}<i id="mo{k}"></i></div>' for k, m in enumerate(
    ["JAN", "FEB", "MAR", "APR", "MEI", "JUN", "JUL", "AGU", "SEP", "OKT", "NOV", "DES"]))
body = f'''
  <div class="blob" style="left:-220px;top:1380px;width:620px;height:620px"></div>
  <div class="blob" style="left:760px;top:-120px;width:480px;height:480px"></div>
  <div class="head" id="h1" style="top:430px;font-size:96px">LANGGANAN<br><em>TOOLS AI</em></div>
  {apps}
  <div id="small">kecil, kan?</div>
  <div class="head" id="h2" style="top:400px;font-size:110px">TAPI <em>SETAHUN</em></div>
  <div id="cal"><div class="ch">12 BULAN &middot; 3 TOOLS</div><div class="g">{months}</div></div>
  <div id="usd">$0</div>
  <div id="idr"><span>&asymp; Rp11,7 JUTA</span></div>
  <div id="kurs"><span>ASUMSI KURS Rp16.300 / USD</span></div>
  <div id="end"><div class="n">GAYA 02</div><div class="t">PA<em>PER</em></div><div class="d">flat infografis &middot; data, uang, simulasi</div></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

js = f'''
    var T = {T};
    tl.fromTo(".blob", {{ scale: 0.9 }}, {{ scale: 1.08, duration: 15, ease: "none" }}, 0);
    rise("#h1", 0.25, 0.5, {{ y: 30 }});
    [0, 1, 2].forEach(function (k) {{ rise("#ap" + k, T[2] + 0.18 * k, 0.45, {{ y: 120, rotation: -6 }}); }});
    [0, 1, 2].forEach(function (k) {{ pop("#tg" + k, T[6] + 0.12 * k, 0.32); }});
    tl.to("#ap0, #ap1, #ap2, #tg0, #tg1, #tg2", {{ scale: 0.78, y: -40, duration: 0.5, ease: "power2.inOut" }}, q(T[10]));
    rise("#small", T[11], 0.35, {{ y: 20 }});
    hide("#h1, #ap0, #ap1, #ap2, #tg0, #tg1, #tg2, #small", T[12] - 0.15, 0.2);
    rise("#h2", T[12], 0.4, {{ y: 30 }});
    rise("#cal", T[13] - 0.05, 0.45, {{ y: 80 }});
    for (var k = 0; k < 12; k++) tl.to("#mo" + k, {{ scale: 1, duration: 0.18, ease: "back.out(3)" }}, q(T[13] + 0.08 * k));
    rise("#usd", T[14], 0.3, {{ y: 20 }});
    count("#usd", T[15], T[19] - T[15] + 0.3, 0, 720, function (v) {{ return "$" + Math.round(v); }});
    tl.to("#usd", {{ scale: 1.08, duration: 0.15, yoyo: true, repeat: 1 }}, q(T[19] + 0.35));
    rise("#idr", T[20], 0.4, {{ y: 30 }});
    tl.to("#idr span", {{ scale: 1.1, duration: 0.18, yoyo: true, repeat: 1 }}, q(T[23]));
    rise("#kurs", T[24], 0.3, {{ y: 10 }});
    tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, q(12.4));
    tl.fromTo("#end .t", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "back.out(1.6)" }}, q(12.6));
'''

(HERE / "public" / "index.html").write_text(page("gaya-paper", css, body, js), encoding="utf-8")
print("ok")
