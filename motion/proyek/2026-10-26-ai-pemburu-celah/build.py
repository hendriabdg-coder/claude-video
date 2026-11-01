# Reel Senin 26 Okt · "AI Pemburu Celah" · Seri Internet Jebol #2 · gaya EMBER (warm black + gold glow, red = threat).
# VO: output/motion/2026-10-26-ai-pemburu-celah/vo (naskah final Endrich). Facts + sources: riset.md in the same folder.
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
from reel_common import ICON, chars, chibi_anim_html, chibi_anim_js, fitpx, page, setup, words  # noqa: E402

SLUG = "2026-10-26-ai-pemburu-celah"
DUR = setup(HERE, SLUG)
T = words(SLUG)
random.seed(7)

css = '''
:root { --bg:#0a0907; --gold:#F5C452; --cream:#FFF3D6; --red:#FF4A4A; --green:#59E38C; }
html, body, #root { background: var(--bg); color: var(--cream); font-family: "IDSemi"; }
.tint { position: absolute; inset: -200px; opacity: 0; }
#t-gold { opacity: 1; background: radial-gradient(ellipse 60% 40% at 50% 42%, rgba(245,196,82,.17) 0%, rgba(245,196,82,0) 70%); }
#t-red { background: radial-gradient(ellipse 60% 40% at 50% 42%, rgba(255,60,60,.2) 0%, rgba(255,60,60,0) 70%); }
#vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 70% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.8) 100%); pointer-events: none; }
.dust { position: absolute; border-radius: 50%; background: var(--gold); box-shadow: 0 0 12px 3px rgba(245,196,82,.55); }
#cam { position: absolute; inset: 0; transform-origin: 50% 45%; }
.heavy { position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDBlack"; line-height: 1; letter-spacing: .02em; white-space: nowrap; opacity: 0; }
.heavy .ch { opacity: 0; }
.c { color: var(--cream); text-shadow: 0 0 14px rgba(245,196,82,.85), 0 0 46px rgba(245,196,82,.45); }
.g { color: var(--gold); text-shadow: 0 0 16px rgba(245,196,82,.9), 0 0 60px rgba(245,196,82,.5); }
.r { color: #FFE2E2; text-shadow: 0 0 14px rgba(255,74,74,.95), 0 0 54px rgba(255,74,74,.6); }
.lead { position: absolute; left: 0; width: 1080px; text-align: center; font-family: "IDItal"; font-size: 50px; color: rgba(255,243,214,.88); opacity: 0; }
.mono { position: absolute; left: 0; width: 1080px; text-align: center; font-family: Consolas, monospace; font-size: 28px; letter-spacing: .2em; color: rgba(255,243,214,.6); opacity: 0; }
#hud { position: absolute; left: 72px; top: 262px; display: flex; align-items: center; gap: 18px; opacity: 0; }
#hud .tag { font-family: Consolas, monospace; font-size: 24px; letter-spacing: .2em; color: var(--gold); padding: 8px 16px; border: 2px solid rgba(245,196,82,.6); border-radius: 8px; }
#hud .dots { display: flex; gap: 10px; }
#hud .dots i { width: 34px; height: 6px; border-radius: 3px; background: rgba(255,243,214,.18); }
#shield { position: absolute; left: 340px; top: 760px; width: 400px; height: 400px; color: var(--gold); filter: drop-shadow(0 0 30px rgba(245,196,82,.8)); opacity: 0; }
#shield .ico { position: absolute; inset: 0; }
#shieldR { color: var(--red); filter: drop-shadow(0 0 30px rgba(255,74,74,.9)); opacity: 0; position: absolute; inset: 0; }
#crack { position: absolute; left: 0; top: 0; width: 400px; height: 400px; opacity: 0; }
.stamp { position: absolute; left: 50%; display: flex; align-items: center; gap: 18px; padding: 14px 40px 16px 26px; border-radius: 18px; border: 5px solid; font-family: "IDBlack"; font-size: 76px; letter-spacing: .04em; line-height: 1; opacity: 0; white-space: nowrap; }
.stamp .si { width: 64px; height: 64px; }
.stamp.gr { color: var(--green); border-color: var(--green); background: rgba(89,227,140,.10); box-shadow: 0 0 40px rgba(89,227,140,.35); }
.stamp.gd { color: var(--gold); border-color: var(--gold); background: rgba(245,196,82,.08); box-shadow: 0 0 40px rgba(245,196,82,.3); }
.stamp.rd { color: var(--red); border-color: var(--red); background: rgba(255,74,74,.10); box-shadow: 0 0 44px rgba(255,74,74,.4); }
.persp { position: absolute; inset: 0; perspective: 1600px; }
.panel { position: absolute; border-radius: 26px; background: linear-gradient(160deg, #1b1812, #100e0a); border: 2px solid rgba(245,196,82,.3); box-shadow: 0 40px 90px rgba(0,0,0,.6), 0 0 40px rgba(245,196,82,.12); opacity: 0; padding: 38px 44px; }
.panel.rp { border-color: rgba(255,74,74,.5); box-shadow: 0 40px 90px rgba(0,0,0,.6), 0 0 40px rgba(255,74,74,.2); }
.panel .k { font-family: Consolas, monospace; font-size: 24px; letter-spacing: .2em; color: rgba(255,243,214,.55); }
.panel .v { font-family: "IDBlack"; font-size: 64px; margin-top: 14px; }
.panel .s { font-family: "IDSemi"; font-size: 28px; color: rgba(255,243,214,.6); margin-top: 18px; }
.big { font-family: "IDBlack"; font-size: 190px; line-height: 1; color: #FFE2E2; text-shadow: 0 0 30px rgba(255,74,74,.8); }
.big small { font-size: 80px; color: rgba(255,226,226,.6); }
.sim { position: absolute; font-family: Consolas, monospace; font-size: 22px; letter-spacing: .2em; color: rgba(255,226,226,.7); padding: 6px 12px; border: 2px solid rgba(255,74,74,.5); border-radius: 8px; }
.flashc { position: absolute; inset: 0; background: #D7263D; opacity: 0; overflow: hidden; }
.flashc .frs { position: absolute; left: 0; top: 300px; width: 1080px; }
.flashc .fr { font-family: "IDBlack"; font-size: 150px; line-height: 1.05; text-align: center; color: transparent; -webkit-text-stroke: 3px rgba(10,9,7,.35); white-space: nowrap; }
.flashc .fr.solid { color: #0a0907; -webkit-text-stroke: 0; }
#follow { position: absolute; left: 340px; top: 530px; width: 400px; height: 96px; border-radius: 48px; background: var(--gold); color: #0a0907; font-family: "IDBlack"; font-size: 46px; display: flex; align-items: center; justify-content: center; gap: 14px; opacity: 0; box-shadow: 0 0 40px rgba(245,196,82,.6); }
#tapc { position: absolute; left: 660px; top: 570px; width: 70px; height: 70px; color: var(--cream); opacity: 0; }
.opt { position: absolute; top: 420px; width: 380px; height: 120px; border-radius: 22px; display: flex; align-items: center; gap: 14px; padding: 0 20px; font-family: "IDBlack"; font-size: 34px; opacity: 0; }
.opt .oi { width: 64px; height: 64px; flex: none; }
#optA { left: 110px; color: var(--green); border: 4px solid var(--green); background: rgba(89,227,140,.1); box-shadow: 0 0 34px rgba(89,227,140,.3); }
#optB { left: 530px; color: var(--red); border: 4px solid var(--red); background: rgba(255,74,74,.1); box-shadow: 0 0 34px rgba(255,74,74,.3); }
#brand { position: absolute; left: 0; top: 1525px; width: 1080px; text-align: center; font-family: "IDBlack"; font-size: 38px; color: var(--cream); opacity: .9; }
#brand b { color: var(--gold); font-weight: normal; }
#flash { position: absolute; inset: 0; background: #FFF3D6; opacity: 0; pointer-events: none; }
#rflash { position: absolute; inset: 0; background: #FF2A2A; opacity: 0; pointer-events: none; mix-blend-mode: screen; }
'''

DUST = "".join(f'<i class="dust" style="left:{random.randint(20, 1060)}px;top:{random.randint(260, 1700)}px;'
               f'width:{random.choice([4, 5, 6, 8])}px;height:{random.choice([4, 5, 6, 8])}px;opacity:.5"></i>' for _ in range(40))
CRACK = ('<svg id="crack" viewBox="0 0 100 100" fill="none" stroke="#FF4A4A" stroke-width="2.6" stroke-linecap="round">'
         '<path d="M52 14 L46 34 L56 46 L44 62 L54 76 L48 90"/><path d="M46 34 L32 40 M56 46 L70 50 M44 62 L30 70"/></svg>')
FLASH_ROWS = "".join(f'<div class="fr{" solid" if k == 2 else ""}">TAPI...</div>' for k in range(6))
# animated chibi (keyed loop clips) — replaces the static poses: point up at the Rabu promise, press the virtual
# button on "Follow", think on the question, shrug on "penjagaan, atau pembobolan?"
CLIPS = [("menunjuk_keatas", T[54] - 0.3, T[54] + 3.7), ("Menekan_Tombol_Virtual", T[54] + 3.7, T[71] - 0.1),
         ("Berfikir", T[71] - 0.1, T[80] - 0.1), ("tidak_tahu", T[80] - 0.1, DUR)]

body = f'''
  <div class="tint" id="t-gold"></div><div class="tint" id="t-red"></div>
  {DUST}
  <div id="cam">
    <div id="hud"><div class="tag">INTERNET JEBOL #2</div><div class="dots"><i id="d1"></i><i id="d2"></i><i id="d3"></i><i id="d4"></i></div></div>
    <!-- hook -->
    <div class="lead" id="h0" style="top:330px">AI ini dibikin buat</div>
    <div class="heavy c" id="h1" style="top:400px;font-size:{fitpx("JAGA INTERNET", 112)}px">{chars("JAGA INTERNET")}</div>
    <div id="shield">{ICON["shield"]}<div id="shieldR">{ICON["key"]}</div>{CRACK}</div>
    <div class="mono" id="h0b" style="top:545px">GEMINI 4 ARGON &middot; GOOGLE</div>
    <div class="lead" id="h2" style="top:560px">masalahnya...</div>
    <div class="heavy r" id="h3" style="top:1230px;font-size:{fitpx("JAGO NYERANG", 120)}px">{chars("JAGO NYERANG")}</div>
    <!-- Argon -->
    <div class="lead" id="a0" style="top:340px">namanya</div>
    <div class="heavy g" id="a1" style="top:410px;font-size:{fitpx("GEMINI 4 ARGON", 118)}px">{chars("GEMINI 4 ARGON")}</div>
    <div class="mono" id="a2" style="top:560px">KLAIM GOOGLE &middot; 30 SEP 2026</div>
    <div class="stamp gd" id="st1" style="top:700px"><span class="si">{ICON["shield"]}</span>TEMUKAN</div>
    <div class="stamp gd" id="st2" style="top:860px"><span class="si">{ICON["check"]}</span>CEK</div>
    <div class="stamp gr" id="st3" style="top:1020px"><span class="si">{ICON["check"]}</span>TAMBAL</div>
    <div class="persp"><div class="panel" id="pro" style="left:110px;top:720px;width:860px">
      <div class="k">DIBUKA &middot; 13 OKT 2026</div><div class="v">Google AI Pro &amp; Ultra</div>
      <div class="s">versi tanpa pengaman: hanya tim keamanan terpilih</div></div></div>
    <!-- twist -->
    <div class="flashc" id="fl"><div class="frs">{FLASH_ROWS}</div></div>
    <div class="lead" id="b0" style="top:340px">di tes Google sendiri</div>
    <div class="heavy r" id="b1" style="top:410px;font-size:{fitpx("SKOR SERANG NAIK", 104)}px">{chars("SKOR SERANG NAIK")}</div>
    <div class="persp"><div class="panel rp" id="sc1" style="left:190px;top:700px;width:700px;text-align:center">
      <div class="k">SKENARIO SERANGAN BERHASIL</div><div class="big"><span id="sc1n">5</span><small> / 12</small></div></div></div>
    <div class="sim" id="sim1" style="left:420px;top:1100px">UJI SIMULASI</div>
    <div class="lead" id="c0" style="top:340px">di uji Anthropic</div>
    <div class="heavy c" id="c1" style="top:410px;font-size:{fitpx("MODEL AI TERBUKA", 100)}px">{chars("MODEL AI TERBUKA")}</div>
    <div class="persp"><div class="panel rp" id="sc2" style="left:190px;top:680px;width:700px;text-align:center">
      <div class="k">EKSPLOIT BERHASIL DIBUAT</div><div class="big"><span id="sc2n">0</span><small> / 410</small></div>
      <div class="s">percobaan</div></div></div>
    <div class="sim" id="sim2" style="left:420px;top:1150px">UJI SIMULASI</div>
    <div class="stamp rd" id="st4" style="top:1250px"><span class="si">{ICON["key"]}</span>ALAT PEMBOBOL</div>
    <!-- CTA -->
    <div class="mono" id="e0" style="top:330px">RABU &middot; INTERNET JEBOL PART 3</div>
    <div class="heavy g" id="e1" style="top:390px;font-size:{fitpx("PENIPUAN SUARA AI", 96)}px">{chars("PENIPUAN SUARA AI")}</div>
    <div id="follow">+ FOLLOW</div><div id="tapc">{ICON["cursor"]}</div>
    <div class="lead" id="f0" style="top:340px;font-size:42px">menurut kamu, AI ini lebih condong ke...</div>
    <div class="opt" id="optA"><span class="oi">{ICON["shield"]}</span>PENJAGAAN</div>
    <div class="opt" id="optB"><span class="oi">{ICON["key"]}</span>PEMBOBOLAN</div>
    <div class="mono" id="f1" style="top:575px">TULIS DI KOMENTAR</div>
    {chibi_anim_html(HERE, CLIPS)}
  </div>
  <div id="flash"></div><div id="rflash"></div>
  <div id="brand">Endrich<b>Tech</b></div>
  <div id="vig"></div>
'''

js = f'''
    var T = {T}, DUR = {DUR};
    document.querySelectorAll(".dust").forEach(function (p, k) {{
      tl.fromTo(p, {{ y: 0 }}, {{ y: -240 - (k % 7) * 40, duration: DUR, ease: "none" }}, 0);
    }});
    tl.set(".stamp", {{ xPercent: -50 }}, 0);
    tl.fromTo("#cam", {{ scale: 1.06 }}, {{ scale: 1, duration: 5, ease: "power2.out" }}, 0);
    function tint(name, t) {{ ["#t-gold", "#t-red"].forEach(function (id) {{ tl.to(id, {{ opacity: id === name ? 1 : 0, duration: 0.4 }}, q(t)); }}); }}
    function hud(k, t, red) {{ tl.to("#d" + k, {{ backgroundColor: red ? "#FF4A4A" : "#F5C452", boxShadow: "0 0 10px " + (red ? "#FF4A4A" : "#F5C452"), duration: 0.2 }}, q(t)); }}

    // HOOK: guardian shield -> cracks -> turns into a key (attacker)
    fade("#h0", 0.05, 0.3, {{ y: 16 }});
    sweep("#h1", 0.25, 0.4); fade("#h0b", 0.6, 0.3, {{ y: 10 }}); hide("#h0b", T[6] - 0.1, 0.12);
    tl.fromTo("#shield", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.8)" }}, 0.1);
    tl.fromTo("#shield", {{ y: 0 }}, Object.assign({{ y: -16, duration: 0.8, yoyo: true, repeat: 1, ease: "sine.inOut" }}, NI), 0.6);
    hide("#h0, #h1", T[6] - 0.1, 0.12);
    fade("#h2", T[6], 0.3, {{ y: 16 }});
    tl.fromTo("#crack path", {{ strokeDasharray: 120, strokeDashoffset: 120 }}, {{ strokeDashoffset: 0, duration: 0.5, ease: "power2.in" }}, q(T[6] + 0.3));
    cut("#crack", T[6] + 0.3, 1);
    tint("#t-red", T[9] - 0.1);
    tl.to("#shield > .ico", {{ opacity: 0, scale: 0.7, duration: 0.2 }}, q(T[9] - 0.05));
    cut("#crack", T[9] - 0.05, 0);
    tl.fromTo("#shieldR", {{ opacity: 0, rotation: -40, scale: 0.6 }}, {{ opacity: 1, rotation: 0, scale: 1, duration: 0.35, ease: "back.out(2)" }}, q(T[9] - 0.05));
    sweep("#h3", T[9], 0.35); flash(T[9], "#rflash", 0.25); kick(T[9], 14);
    hide("#h2, #h3, #shield", T[11] - 0.15, 0.15);

    // ARGON
    fade("#hud", T[11], 0.3, {{ x: -30, y: 0 }}); hud(1, T[11]); tint("#t-gold", T[11] - 0.1);
    fade("#a0", T[11], 0.3, {{ y: 14 }}); sweep("#a1", T[12] - 0.05, 0.4); fade("#a2", T[15], 0.3, {{ y: 10 }});
    [["#st1", T[19]], ["#st2", T[21]], ["#st3", T[23]]].forEach(function (s) {{
      tl.fromTo(s[0], {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }}, q(s[1])); flash(s[1] + 0.22, "#flash", 0.15); kick(s[1] + 0.22, 6);
    }});
    hide("#st1, #st2, #st3", T[25] - 0.15, 0.15);
    tl.fromTo("#pro", {{ opacity: 0, rotationY: -40, rotationX: 14, z: -300, y: 80 }}, {{ opacity: 1, rotationY: -12, rotationX: 6, z: 0, y: 0, duration: 0.6, ease: "power3.out" }}, q(T[25]));
    tl.to("#pro", {{ rotationY: 8, duration: 2.4, ease: "sine.inOut" }}, q(T[25] + 0.6));
    hide("#a0, #a1, #a2, #pro", T[32] - 0.15, 0.15);

    // TWIST
    hud(2, T[32], true); tint("#t-red", T[32]);
    cut("#fl", T[32] - 0.05, 1); cut("#fl", T[33] - 0.05, 0);
    tl.fromTo("#fl .frs", {{ y: 80 }}, {{ y: -80, duration: T[33] - T[32], ease: "none" }}, q(T[32] - 0.05));
    fade("#b0", T[33], 0.3, {{ y: 14 }}); sweep("#b1", T[37], 0.4);
    tl.fromTo("#sc1", {{ opacity: 0, rotationX: 30, z: -200, y: 60 }}, {{ opacity: 1, rotationX: 6, z: 0, y: 0, duration: 0.5, ease: "power3.out" }}, q(T[37]));
    count("#sc1n", T[39], 0.8, 5, 12, function (v) {{ return Math.round(v); }});
    flash(T[40] + 0.3, "#rflash", 0.2); kick(T[40] + 0.3, 10);
    pop("#sim1", T[40], 0.3);
    hide("#b0, #b1, #sc1, #sim1", T[41] - 0.1, 0.12);
    hud(3, T[41], true);
    fade("#c0", T[41], 0.3, {{ y: 14 }}); sweep("#c1", T[45], 0.4);
    tl.fromTo("#sc2", {{ opacity: 0, rotationX: 30, z: -200, y: 60 }}, {{ opacity: 1, rotationX: 6, z: 0, y: 0, duration: 0.5, ease: "power3.out" }}, q(T[46]));
    count("#sc2n", T[50] - 0.6, 1.2, 0, 50, function (v) {{ return Math.round(v); }});
    pop("#sim2", T[50], 0.3);
    tl.fromTo("#st4", {{ opacity: 0, scale: 1.7 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }}, q(T[52]));
    flash(T[52] + 0.22, "#rflash", 0.25); kick(T[52] + 0.22, 12);
    hide("#c0, #c1, #sc2, #sim2, #st4", T[54] - 0.15, 0.15);

    // CTA SERI + chibi
    hud(4, T[54]); tint("#t-gold", T[54]);
    fade("#e0", T[55], 0.3, {{ y: 12 }}); sweep("#e1", T[61], 0.4);
    pop("#follow", T[65] - 0.05, 0.35);
    tl.fromTo("#tapc", {{ opacity: 0, x: 60, y: 60 }}, {{ opacity: 1, x: 0, y: 0, duration: 0.3, ease: "power2.out" }}, q(T[65] + 0.2));
    tl.to("#follow", {{ scale: 0.92, duration: 0.08, yoyo: true, repeat: 1 }}, q(T[65] + 0.5));
    tl.to("#follow", {{ backgroundColor: "#59E38C", duration: 0.1 }}, q(T[65] + 0.58));
    hide("#e0, #e1, #follow, #tapc", T[71] - 0.15, 0.15);

    // CTA KOMENTAR
    fade("#f0", T[71], 0.3, {{ y: 14 }});
    tl.fromTo("#optA", {{ opacity: 0, x: -80 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.8)" }}, q(T[80] - 0.05));
    tl.fromTo("#optB", {{ opacity: 0, x: 80 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.8)" }}, q(T[82] - 0.05));
    fade("#f1", T[82] + 0.5, 0.3, {{ y: 10 }});
    tl.to("#f1", {{ opacity: 0.4, duration: 0.4, yoyo: true, repeat: 2, ease: "sine.inOut" }}, q(T[82] + 0.9));
'''
js += chibi_anim_js(T[54] - 0.3)

(HERE / "public" / "index.html").write_text(page("ai-pemburu-celah", DUR, css, body, js), encoding="utf-8")
print("ok", DUR, len(CLIPS), "chibi clips")
