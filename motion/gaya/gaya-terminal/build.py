# Style template 04 · TERMINAL — developer / security look: near-black CRT screen, phosphor-green monospace, a terminal
# window where commands are typed in sync with the VO, amber warnings, scanlines + flicker, ASCII progress bars.
# Best for security news, tutorials with commands, "cara cek", dev tips.
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from gaya_common import page, words  # noqa: E402

T = words("terminal")

css = '''
:root { --bg:#050807; --g:#39FF88; --gd:rgba(57,255,136,.45); --amb:#FFB000; --w:#D8FFE8; }
html, body, #root { background: var(--bg); color: var(--g); font-family: Consolas, "Courier New", monospace; }
#crt { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 45%, rgba(57,255,136,.08) 0%, rgba(0,0,0,0) 70%); }
#scan { position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,.28) 0px, rgba(0,0,0,.28) 2px, rgba(0,0,0,0) 2px, rgba(0,0,0,0) 5px); pointer-events: none; }
#vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 75% at 50% 50%, rgba(0,0,0,0) 60%, rgba(0,0,0,.85) 100%); pointer-events: none; }
#cam { position: absolute; inset: 0; }
#boot { position: absolute; left: 70px; top: 250px; font-size: 26px; line-height: 1.6; color: var(--gd); }
#boot div { opacity: 0; }
.big { position: absolute; left: 70px; font-size: 104px; line-height: 1.05; color: var(--g); text-shadow: 0 0 18px rgba(57,255,136,.7); white-space: pre; }
.big .cur { display: inline-block; width: 52px; height: 92px; background: var(--g); vertical-align: -10px; margin-left: 8px; }
#win { position: absolute; left: 60px; top: 700px; width: 960px; height: 640px; border: 2px solid var(--gd); border-radius: 18px; background: rgba(5,12,9,.85); box-shadow: 0 0 40px rgba(57,255,136,.18); opacity: 0; overflow: hidden; }
#win .bar { height: 60px; border-bottom: 2px solid rgba(57,255,136,.25); display: flex; align-items: center; gap: 12px; padding: 0 22px; font-size: 24px; color: var(--gd); }
#win .bar i { width: 16px; height: 16px; border-radius: 50%; border: 2px solid var(--gd); display: inline-block; }
#win .body { padding: 30px 34px; font-size: 44px; line-height: 1.5; }
#cmd { color: var(--w); }
#ps { color: var(--g); }
.out { opacity: 0; }
.amb { color: var(--amb); text-shadow: 0 0 14px rgba(255,176,0,.6); }
#warn { position: absolute; left: 60px; top: 1380px; width: 960px; padding: 22px 30px; border: 3px solid var(--amb); border-radius: 14px; color: var(--amb); font-size: 40px; text-shadow: 0 0 14px rgba(255,176,0,.5); opacity: 0; }
#upd { position: absolute; left: 70px; top: 1380px; width: 940px; font-size: 44px; color: var(--g); opacity: 0; }
#upd .pb { margin-top: 10px; white-space: pre; }
.lbl { position: absolute; right: 140px; top: 1350px; font-size: 20px; letter-spacing: .2em; color: rgba(57,255,136,.4); opacity: 0; }
#end { position: absolute; inset: 0; background: var(--bg); opacity: 0; }
#end .n { position: absolute; left: 0; width: 1080px; top: 740px; text-align: center; font-size: 44px; letter-spacing: .3em; color: var(--gd); }
#end .t { position: absolute; left: 0; width: 1080px; top: 820px; text-align: center; font-size: 170px; color: var(--g); text-shadow: 0 0 30px rgba(57,255,136,.8); }
#end .d { position: absolute; left: 0; width: 1080px; top: 1060px; text-align: center; font-size: 36px; color: var(--gd); }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-family: "IDBlack"; font-size: 36px; color: var(--w); }
#brand b { color: var(--g); font-weight: normal; }
'''

BOOT = ["> menghubungkan ke server...", "> auth ............ [OK]", "> shell siap"]
PB = "[##########----------]"
body = f'''
  <div id="crt"></div>
  <div id="cam">
    <div id="boot">{"".join(f"<div>{l}</div>" for l in BOOT)}</div>
    <div class="big" id="b1" style="top:380px"><span id="b1t"></span><span class="cur" id="c1"></span></div>
    <div id="win"><div class="bar"><i></i><i></i><i></i>&nbsp;~/server &mdash; bash</div>
      <div class="body"><span id="ps">$ </span><span id="cmd"></span><span class="cur" id="c2" style="display:inline-block;width:26px;height:46px;background:#39FF88;vertical-align:-8px"></span>
        <div class="out" id="o1">PHP <span class="amb">7.4.33</span> (cli)</div>
        <div class="out" id="o2">Copyright (c) The PHP Group</div>
        <div class="out amb" id="o3">! versi ini sudah EOL</div></div></div>
    <div class="lbl" id="lbl">CONTOH OUTPUT</div>
    <div id="warn">&#9888; VERSI TIDAK DIDUKUNG = TANPA PATCH KEAMANAN</div>
    <div id="upd"><div>&gt; <span id="updt"></span></div><div class="pb" id="pb">{PB}</div></div>
  </div>
  <div id="scan"></div><div id="vig"></div>
  <div id="end"><div class="n">GAYA 04</div><div class="t">TERMINAL_</div><div class="d">dev &middot; keamanan &middot; tutorial perintah</div></div>
  <div id="brand">Endrich<b>Tech</b></div>
'''

js = f'''
    var T = {T};
    // CRT flicker and blinking cursors across the whole clip (finite repeats: seek-safe)
    tl.to("#crt", {{ opacity: 0.6, duration: 0.07, yoyo: true, repeat: 41, ease: "steps(1)" }}, 0.3);
    tl.to("#c1, #c2", {{ opacity: 0, duration: 0.4, yoyo: true, repeat: 29, ease: "steps(1)" }}, 0);
    document.querySelectorAll("#boot div").forEach(function (d, k) {{ cut(d, 0.1 + 0.25 * k, 1); }});
    type("#b1t", T[0], T[9] - T[0] - 0.4, "1 PERINTAH\\nCEK SERVER");
    tl.to("#boot", {{ opacity: 0.25, duration: 0.3 }}, q(T[1]));
    rise("#win", T[9] - 0.2, 0.4, {{ y: 60 }});
    tl.to("#b1", {{ scale: 0.6, y: -120, x: -170, duration: 0.4, ease: "power2.inOut" }}, q(T[9] - 0.2));
    type("#cmd", T[10], 0.25, "php");
    type("#cmd", T[11], 0.25, "php ");
    type("#cmd", T[12], T[13] - T[12] + 0.2, "php -v");
    tl.set("#c2", {{ display: "none" }}, q(T[14] - 0.1));
    [["#o1", 0], ["#o2", 0.15], ["#o3", 0.6]].forEach(function (o) {{ cut(o[0], T[14] + o[1], 1); }});
    cut("#lbl", T[14], 1);
    tl.fromTo("#warn", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.25, ease: "power3.out" }}, q(T[18]));
    tl.to("#warn", {{ opacity: 0.4, duration: 0.12, yoyo: true, repeat: 5, ease: "steps(1)" }}, q(T[18] + 0.3));
    tl.to("#warn", {{ opacity: 0, duration: 0.15 }}, q(T[20] - 0.1));
    cut("#upd", T[20], 1);
    type("#updt", T[20], 0.6, "sudo apt upgrade php");
    var pb = {{ n: 0 }}, pel = document.querySelector("#pb");
    tl.to(pb, {{ n: 20, duration: T[25] - T[21] + 0.5, ease: "power1.inOut", onUpdate: function () {{
      var k = Math.round(pb.n); pel.textContent = "[" + "#".repeat(k) + "-".repeat(20 - k) + "] " + (k * 5) + "%"; }} }}, q(T[21]));
    tl.fromTo("#cam", {{ x: 6 }}, Object.assign({{ x: 0, duration: 0.2, ease: "elastic.out(1,.3)" }}, NI), q(T[18]));
    tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, q(12.4));
    tl.fromTo("#end .t", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, yoyo: true, repeat: 4, ease: "steps(1)" }}, q(12.45));
'''

(HERE / "public" / "index.html").write_text(page("gaya-terminal", css, body, js), encoding="utf-8")
print("ok")
