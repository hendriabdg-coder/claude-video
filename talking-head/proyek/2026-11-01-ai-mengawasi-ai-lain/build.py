# Edit penuh "AI Mengawasi AI Lain" (59 dtk) dengan gaya TH HYBRID 50/50 (varian D, dipilih Endrich 2026-11-01).
# Scene: TH full (lockup dada, punch-in, B&W) | CUT = latar dihapus (matte di-overlay di composite.sh) |
#        PIP = motion di kanvas gelap + wajah di frame bulat kiri bawah.
#   python build.py && bash composite.sh
import json, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "uji-gaya"))
import build_uji as U
from build_uji import lockup, svg, ROBOT, LOCK, WM, FONTS, MONO, SK, ROOT

DUR = 59.1
TAKE = ROOT / "talking-head/mentah/2026-11-01-ai-mengawasi-ai-lain/gabungan.mp4"
LOGO = ROOT / "talking-head/aset/Image & Logo/OpenAI_logo.png"

# mata x/y + puncak kepala per shot (px frame sumber, diukur dari look/grid_shot*.jpg); batas shot dari look.json
EYES = [(600, 395, 265), (560, 356, 216), (572, 464, 335), (648, 432, 216), (605, 464, 313), (583, 535, 324), (606, 486, 308),
        (577, 518, 324), (551, 340, 243), (509, 340, 253), (544, 324, 220), (486, 399, 301), (573, 463, 220), (577, 463, 227),
        (583, 480, 246), (557, 318, 237), (544, 544, 130), (567, 454, 211), (600, 610, 405), (600, 615, 400), (632, 567, 405),
        (573, 616, 470), (577, 583, 324), (583, 625, 463), (541, 560, 350), (544, 544, 350), (551, 593, 350), (541, 544, 366)]
look = json.load(open(HERE / "look/look.json"))["shots"]
SHOTS = [(round(s["start_s"], 3), round(s["end_s"], 3)) + EYES[i] for i, s in enumerate(look)]
U.DUR, U.SHOTS = DUR, SHOTS

# bulatan wajah: radius ikut ukuran kepala, tampil r=175 di (300, 1330)
PIP = []
for s0, s1, ex, ey, ht in SHOTS:
    head = ey - ht
    r = max(150, min(320, head * 1.9))
    PIP.append({"r": round(r), "fx": ex, "fy": round(ey + head * 0.25), "s": round(175 / r, 4)})

EYE = svg('<path d="M8 50s16-28 42-28 42 28 42 28-16 28-42 28S8 50 8 50z"/><circle cx="50" cy="50" r="12"/>')
WARN = svg('<path d="M50 12L92 86H8z"/><path d="M50 40v20"/><circle cx="50" cy="72" r="3" fill="currentColor"/>')
SEARCH = svg('<circle cx="42" cy="42" r="26"/><path d="M62 62l26 26"/>')
BELL = svg('<path d="M26 70V46a24 24 0 0 1 48 0v24l8 8H18z"/><path d="M42 85a8 8 0 0 0 16 0"/>')
SHIELD = svg('<path d="M50 10l34 12v26c0 22-15 36-34 44C31 84 16 70 16 48V22z"/>')

L = lambda *a, **k: lockup(*a, **k)
LOCKS = [
    # TH full
    L("t01", 0.0, 1.4, [("l2", [("pakai", 0.0), ("AI", 0.3), ("untuk", 0.54)]), ("l1", [("mengawasi", 0.84)])]),
    L("t02", 5.933, 7.46, [("l2", [("beberapa", 5.92)]), ("l1", [("AI", 6.38), ("agent", 6.62)])]),
    L("t03", 7.48, 8.9, [("l2", [("berhasil", 7.52)]), ("l1r", [("keluar", 7.96), ("dari", 8.22)]), ("l1r", [("sandbox", 8.44)])]),
    L("t04", 11.8, 13.1, [("l2", [("setelah", 11.84), ("kejadian", 12.14), ("itu", 12.48)])]),
    L("t05", 13.12, 14.78, [("l2", [("OpenAI", 13.14), ("memperluas", 13.46)]), ("l1", [("sistem", 13.98), ("pengawasan", 14.26)])]),
    L("t06", 14.8, 16.12, [("l2", [("tindakan", 15.14)]), ("l1r", [("di", 15.54), ("luar", 15.66), ("izin", 15.86)])]),
    L("t07", 16.14, 17.633, [("l2", [("bisa", 16.16), ("terdeteksi", 16.42)]), ("l1", [("lebih", 17.0), ("cepat", 17.18)])]),
    L("t08", 25.2, 27.6, [("l2", [("AI", 25.32), ("investigasi", 25.54)]), ("l1", [("menelusuri", 26.46)])]),
    L("t09", 31.033, 33.767, [("l2", [("tapi,", 31.02), ("seberapa", 31.64)]), ("l1", [("cepat?", 32.7)])]),
    L("t10", 43.7, 47.1, [("l2", [("bukan", 43.84), ("berarti", 44.18), ("insiden", 44.7), ("aslinya", 45.28)]),
                          ("l1r", [("berhasil", 45.78), ("dihentikan", 46.3)])]),
    L("t11", 47.1, 49.26, [("l2", [("intinya,", 47.08)]), ("l1w", [("AI", 48.08), ("semakin", 48.52), ("mandiri", 48.88)])]),
    L("t12", 49.28, 51.367, [("l2", [("tetap", 49.3), ("butuh", 49.74)]), ("l1", [("batas", 50.04), ("&", 50.44), ("pengawasan", 50.66)])]),
    L("t13", 56.7, DUR + 0.2, [("l1", [("save", 57.04), ("+", 57.3), ("follow", 57.48)]), ("l2", [("biar", 57.8), ("nggak", 58.1), ("ketinggalan", 58.2)])]),
    # scene motion (teks di atas)
    L("m01", 1.4, 2.2, [("l1w", [("AI", 1.4), ("lain?", 1.54)])], top=250, h=250),
    L("m02", 2.2, 3.6, [("l2", [("kedengarannya", 2.24)]), ("tone", [("aneh,", 2.84), ("kan?", 3.14)])], top=250, h=250),
    L("m03", 17.633, 18.62, [("tone", [("nah,", 17.68), ("yang", 17.98), ("menarik,", 18.12)])], top=250, h=230),
    L("m04", 18.64, 20.333, [("l2", [("pengawasnya", 18.68)]), ("l1", [("nggak", 19.42), ("cuma", 19.54), ("satu", 19.74), ("lapis", 19.96)])], top=250, h=230),
    L("m05", 34.133, 41.6, [("l2", [("rekaman", 34.44), ("insiden", 34.84)])], top=250, h=120),
    L("m06", 41.6, 43.7, [("tone", [("tapi", 41.62), ("ingat,", 41.82)]), ("l1", [("hasil", 42.72), ("simulasi", 43.08)])], top=470, h=330),
    L("m07", 51.367, 53.85, [("l2", [("besok", 51.52), ("kita", 52.04), ("bahas", 52.32)]), ("l1", [("kasus", 52.64), ("lebih", 53.08), ("mengejutkan", 53.3)])], top=250, h=240),
    L("m08", 53.867, 56.7, [("l2", [("ketika", 54.06), ("AI", 54.56), ("justru", 54.88)]), ("l1r", [("melemahkan", 55.32)]),
                            ("l1r", [("pengawasnya", 55.86), ("sendiri", 56.4)])], top=250, h=360),
]

CSS = """
#mbg { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 32%, #1a1d24 0%, #0b0d10 62%); opacity: 0; }
#mbg .grid { position: absolute; inset: 0; opacity: .55;
  background-image: linear-gradient(rgba(255,255,255,.05) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,.05) 2px, transparent 2px);
  background-size: 60px 60px; }
#vw { clip-path: circle(1400px at 540px 960px); }
#ring { position: absolute; left: 122px; top: 1152px; width: 356px; height: 356px; border-radius: 50%; border: 5px solid var(--y);
  box-shadow: 0 0 30px rgba(255,214,10,.35); opacity: 0; }
.sc { position: absolute; inset: 0; opacity: 0; }
.chip { position: absolute; left: 0; width: 1080px; text-align: center; opacity: 0; }
.chip span { font-family: "IMed"; font-size: 32px; letter-spacing: .16em; color: var(--w); padding: 12px 24px; border-radius: 999px;
  background: rgba(255,255,255,.08); border: 2px solid rgba(255,255,255,.2); }
.chip.y span { color: var(--y); background: none; border-color: rgba(255,214,10,.5); }
.tile { position: absolute; border-radius: 34px; padding: 26px; }
.tl-y { background: var(--y); color: #111; box-shadow: 0 0 50px rgba(255,214,10,.45); }
.tl-d { background: #1b1e24; color: var(--w); border: 3px solid rgba(255,255,255,.3); }
.tl-r { background: var(--r); color: #fff; box-shadow: 0 0 50px rgba(255,59,78,.5); }
.blab { position: absolute; font-family: "IMed"; font-size: 28px; letter-spacing: .14em; color: rgba(246,245,241,.8); white-space: nowrap; }
/* OpenAI */
#orbit { position: absolute; left: 290px; top: 400px; width: 500px; height: 500px; border-radius: 50%; border: 3px dashed rgba(246,245,241,.28); }
#logo { position: absolute; left: 390px; top: 500px; width: 300px; height: 300px; filter: invert(1) drop-shadow(0 0 30px rgba(255,255,255,.35)); opacity: 0; }
#oname { position: absolute; left: 0; top: 930px; width: 1080px; text-align: center; font-family: "IBlack"; font-size: 128px; letter-spacing: -.03em;
  color: var(--w); text-shadow: 0 0 30px rgba(255,255,255,.25); opacity: 0; }
/* sandbox */
#sbx { position: absolute; left: 150px; top: 390px; width: 780px; height: 440px; border: 6px dashed rgba(246,245,241,.6); border-radius: 36px;
  background: rgba(255,255,255,.04); opacity: 0; }
#sbx .wall { position: absolute; right: -6px; top: 110px; width: 6px; height: 220px; background: var(--r); box-shadow: 0 0 30px var(--r); opacity: 0; }
#agent { left: 470px; top: 540px; width: 140px; height: 140px; padding: 22px; opacity: 0; }
#lock { position: absolute; left: 850px; top: 340px; width: 110px; height: 110px; padding: 18px; border-radius: 30px; background: #1b1e24; color: var(--w);
  border: 2px solid rgba(255,255,255,.25); opacity: 0; }
.pt { position: absolute; left: 0; top: 900px; width: 1080px; text-align: center; white-space: nowrap; opacity: 0; }
.pt .a { font-family: "ISemi"; font-size: 60px; color: var(--w); }
.pt .b { font-family: "IItal"; font-size: 66px; color: var(--y); margin-right: 18px; }
.pt .c { font-family: "IBlack"; font-size: 100px; color: var(--y); letter-spacing: -.03em; display: block; line-height: 1.1; }
/* lapis */
.lap { position: absolute; border-radius: 50%; border: 4px solid rgba(255,214,10,.75); box-shadow: 0 0 30px rgba(255,214,10,.25); opacity: 0; }
/* pipeline */
.node { position: absolute; left: 120px; width: 820px; height: 150px; border-radius: 30px; background: rgba(255,255,255,.06);
  border: 2px solid rgba(255,255,255,.16); opacity: 0; }
.node .ic { position: absolute; left: 22px; top: 22px; width: 106px; height: 106px; padding: 20px; border-radius: 26px; }
.node .tt { position: absolute; left: 156px; top: 26px; font-family: "ISemi"; font-size: 52px; color: var(--w); white-space: nowrap; }
.node .sb { position: absolute; left: 158px; top: 92px; font-family: "IMed"; font-size: 32px; color: rgba(246,245,241,.62); white-space: nowrap; }
.node .sb b { font-weight: normal; color: var(--y); opacity: 0; }
.conn { position: absolute; left: 192px; width: 6px; height: 50px; background: rgba(246,245,241,.35); transform-origin: 50% 0; opacity: 0; }
/* timeline */
#big { position: absolute; left: 0; top: 520px; width: 1080px; text-align: center; font-family: "IBlack"; font-size: 190px; letter-spacing: -.04em;
  color: var(--y); text-shadow: 0 0 44px rgba(255,214,10,.4); opacity: 0; white-space: nowrap; }
#big small { font-size: 90px; color: var(--w); letter-spacing: -.02em; }
#bar { position: absolute; left: 170px; top: 880px; width: 740px; height: 10px; border-radius: 5px; background: rgba(255,255,255,.15); opacity: 0; }
#bar i { position: absolute; left: 0; top: 0; height: 10px; width: 740px; border-radius: 5px; background: linear-gradient(90deg, var(--r), var(--y)); transform-origin: 0 50%; }
.tdot { position: absolute; width: 96px; height: 96px; padding: 18px; border-radius: 50%; top: 837px; opacity: 0; }
#tdA { left: 122px; } #tdB { left: 862px; }
.tlab { position: absolute; top: 950px; font-family: "ISemi"; font-size: 36px; line-height: 1.25; color: var(--w); opacity: 0; }
#tlA { left: 90px; } #tlB { right: 140px; text-align: right; }
#warn { position: absolute; left: 470px; top: 300px; width: 140px; height: 140px; color: var(--y); opacity: 0; }
#strike { position: absolute; left: 140px; top: 0; width: 800px; height: 10px; background: var(--w); border-radius: 5px; transform-origin: 0 50%;
  box-shadow: 0 2px 12px rgba(0,0,0,.6); opacity: 0; }
"""

BODY = f'''  <div id="mbg"><div class="grid"></div></div>
  <div class="sc" id="sc1">
    <svg viewBox="0 0 1080 1920" style="position:absolute;inset:0"><defs><linearGradient id="bm" x1="0" x2="1"><stop offset="0" stop-color="#FFD60A" stop-opacity=".55"/>
      <stop offset="1" stop-color="#FFD60A" stop-opacity=".05"/></linearGradient></defs>
      <polygon id="cone" points="280,920 871,960 871,1090" fill="url(#bm)"/>
      <line id="bline" x1="280" y1="920" x2="871" y2="1025" stroke="#FFD60A" stroke-width="4" stroke-dasharray="14 12"/></svg>
    <div class="tile tl-y" id="bot1" style="left:80px;top:820px;width:200px;height:200px">{ROBOT}</div><div class="blab" style="left:80px;top:1040px">AI PENGAWAS</div>
    <div class="tile tl-d" id="bot2" style="left:806px;top:960px;width:130px;height:130px;padding:18px">{ROBOT}</div><div class="blab" style="left:806px;top:1110px">AI LAIN</div>
  </div>
  <div class="sc" id="sc2"><div class="chip" id="ochip" style="top:280px"><span>PENGUJIAN INTERNAL</span></div><div id="orbit"></div>
    <img id="logo" src="openai.png" /><div id="oname">OpenAI</div></div>
  <div class="sc" id="sc3"><div class="chip y" id="stag" style="top:290px"><span>SANDBOX</span></div>
    <div id="sbx"><div class="wall"></div></div><div class="tile tl-y" id="agent">{ROBOT}</div><div id="lock">{LOCK}</div>
    <div class="pt" id="pt1"><span class="a">lingkungan</span><span class="c">terisolasi</span></div>
    <div class="pt" id="pt2"><span class="b">seharusnya</span><span class="a">membatasi akses</span></div></div>
  <div class="sc" id="sc4">
    <div class="lap" id="lp1" style="left:290px;top:640px;width:500px;height:500px"></div>
    <div class="lap" id="lp2" style="left:190px;top:540px;width:700px;height:700px;border-color:rgba(246,245,241,.55)"></div>
    <div class="lap" id="lp3" style="left:90px;top:440px;width:900px;height:900px;border-color:rgba(255,214,10,.45)"></div>
  </div>
  <div class="sc" id="sc5">
    <div class="node" id="n1" style="top:300px"><div class="ic tl-y">{EYE}</div><div class="tt">AI pemeriksa</div>
      <div class="sb"><b id="n1a">aktivitas</b> · <b id="n1b">penggunaan tools</b></div></div>
    <div class="conn" id="c1" style="top:450px"></div>
    <div class="node" id="n2" style="top:500px"><div class="ic tl-r">{WARN}</div><div class="tt">tanda mencurigakan</div><div class="sb">kalau ditemukan</div></div>
    <div class="conn" id="c2" style="top:650px"></div>
    <div class="node" id="n3" style="top:700px"><div class="ic tl-d">{SEARCH}</div><div class="tt">AI investigasi</div><div class="sb">menelusuri kejadian</div></div>
    <div class="conn" id="c3" style="top:850px"></div>
    <div class="node" id="n4" style="top:900px"><div class="ic tl-y">{BELL}</div><div class="tt">peringatan</div><div class="sb">ke tim keamanan</div></div>
  </div>
  <div class="sc" id="sc6"><div class="chip y" id="simc" style="top:400px"><span>SIMULASI ULANG</span></div>
    <div id="big"><span id="num">0</span><small> menit</small></div>
    <div id="bar"><i></i></div>
    <div class="tdot tl-r" id="tdA">{ROBOT}</div><div class="tdot tl-y" id="tdB">{BELL}</div>
    <div class="tlab" id="tlA">agent keluar<br>sandbox</div><div class="tlab" id="tlB">peringatan<br>muncul</div>
    <div id="warn">{WARN}</div>
  </div>
  <div class="sc" id="sc7">
    <div class="tile tl-r" id="ev" style="left:60px;top:540px;width:170px;height:170px;padding:22px">{ROBOT}</div><div class="blab" id="evl" style="left:130px;top:725px">AI</div>
    <div class="tile tl-y" id="gd" style="left:800px;top:560px;width:140px;height:140px;padding:22px">{SHIELD}</div><div class="blab" id="gdl" style="left:790px;top:715px">PENGAWAS</div>
  </div>
  <div id="vw"><video id="vid" src="plate.mp4" playsinline data-has-audio="true" data-start="0" data-duration="{DUR}" data-track-index="0"></video></div>
  <div id="ring"></div>
  {"".join(h for h, _ in LOCKS)}
  <div id="strike"></div>
  {WM}'''

JS = """
    lockups(D.locks);
    var P = D.pip, BIG = "circle(1400px at 540px 960px)";
    function pipSet(t, k) {
      var p = P[k];
      tl.set("#vw", { clipPath: "circle(" + p.r + "px at " + p.fx + "px " + p.fy + "px)", transformOrigin: p.fx + "px " + p.fy + "px",
                      scale: p.s, x: 300 - p.fx, y: 1330 - p.fy, opacity: 1 }, q(t));
    }
    function pipIn(t, k, s0) {
      var p = P[k], sh = SH[k];
      tl.set("#vw", { clipPath: BIG, x: 0, y: 0, scale: s0 || 1.1, transformOrigin: p.fx + "px " + p.fy + "px", opacity: 1 }, q(t));
      tl.to("#vw", { clipPath: "circle(" + p.r + "px at " + p.fx + "px " + p.fy + "px)", scale: p.s, x: 300 - p.fx, y: 1330 - p.fy,
                     duration: 0.45, ease: "power3.inOut" }, q(t));
      tl.fromTo("#ring", { opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }, q(t + 0.27));
      tl.fromTo("#mbg", { opacity: 0 }, { opacity: 1, duration: 0.3 }, q(t));
    }
    function full(t, k, s0, s1, t1) {
      var sh = SH[k];
      tl.set("#vw", { clipPath: BIG, x: 0, y: 0, opacity: 1, transformOrigin: sh[2] + "px " + sh[3] + "px" }, q(t));
      tl.set("#ring", { opacity: 0 }, q(t)); tl.set("#mbg", { opacity: 0 }, q(t));
      tl.fromTo("#vw", { scale: s0 }, { scale: s1, duration: q(t1 || sh[1]) - q(t), ease: t1 && t1 - t < 0.6 ? "power3.out" : "none" }, q(t));
    }
    function cutout(t, sc) { tl.set("#vw", { opacity: 0 }, q(t)); tl.set("#ring", { opacity: 0 }, q(t)); tl.set("#mbg", { opacity: 1 }, q(t)); cut(sc, t, 1); }
    function punch(t, s) { tl.to("#vw", { scale: s, duration: 0.25, ease: "power3.out" }, q(t)); }
    function bw(t0, t1) { tl.to("#vid", { filter: "grayscale(1) contrast(1.12)", duration: 0.1 }, q(t0)); tl.set("#vid", { filter: "grayscale(0) contrast(1)" }, q(t1)); }
    function draw(sel, t) { tl.fromTo(sel, { opacity: 1, scaleY: 0 }, { scaleY: 1, duration: 0.3, ease: "power2.out" }, q(t)); }

    // 0-1.4 TH hook
    full(0, 0, 1.34, 1.16, 0.5); tl.to("#vw", { scale: 1.2, duration: 0.9, ease: "none" }, q(0.5));
    // 1.4-3.6 CUT 1: AI pengawas -> AI lain
    cutout(1.4, "#sc1");
    pop("#bot1", 1.4, 0.3); pop("#bot2", 1.56, 0.3);
    tl.fromTo("#cone", { opacity: 0 }, { opacity: 1, duration: 0.3 }, q(1.7));
    tl.fromTo("#bline", { strokeDashoffset: 0 }, { strokeDashoffset: -260, duration: 1.9, ease: "none" }, q(1.7));
    tl.to("#bot2", { borderColor: "rgba(255,214,10,.9)", duration: 0.2, yoyo: true, repeat: 3 }, q(2.84));
    cut("#sc1", 3.6, 0);
    // 3.6-5.93 PIP: OpenAI
    cut("#sc2", 3.6, 1); pipIn(3.6, 1, 1.18);
    tl.fromTo("#orbit", { opacity: 0, scale: 0.7, rotation: -40 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "power3.out" }, q(3.7));
    tl.to("#orbit", { rotation: 60, duration: 2.0, ease: "none" }, q(4.2));
    show("#ochip", 4.38, 0.3, { y: -20 });
    tl.fromTo("#logo", { opacity: 0, scale: 0.5, rotation: -90 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }, q(5.1));
    show("#oname", 5.24, 0.28, { y: 26, scale: 0.92, filter: "blur(10px)" });
    cut("#sc2", 5.933, 0);
    // 5.93-8.9 TH: AI agent, B&W "keluar dari sandbox"
    full(5.933, 2, 1.0, 1.06);
    full(7.333, 3, 1.04, 1.06, 7.5); punch(7.52, 1.22); bw(7.52, 8.9);
    // 8.9-11.8 PIP: sandbox
    cut("#sc3", 8.9, 1); pipIn(8.9, 4, 1.1);
    show("#stag", 9.0, 0.3, { y: -16 }); show("#sbx", 9.05, 0.35, { scale: 0.9 }); pop("#agent", 9.25);
    cut("#pt1", 8.96, 1); tl.fromTo("#pt1 .a", { opacity: 0 }, { opacity: 1, duration: 0.2 }, q(8.96));
    tl.fromTo("#pt1 .c", { opacity: 0, y: 26, scale: 0.92, filter: "blur(10px)" }, { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.26, ease: "power3.out" }, q(9.38));
    hide("#pt1", 10.06, 0.12); show("#pt2", 10.18, 0.28, { y: 20 }); pop("#lock", 10.62);
    tl.to("#agent", { x: 400, rotation: 12, duration: 0.45, ease: "power3.in" }, q(11.1));
    tl.to("#agent", { background: "#FF3B4E", boxShadow: "0 0 54px rgba(255,59,78,.7)", duration: 0.2 }, q(11.3));
    tl.fromTo("#sbx .wall", { opacity: 0 }, { opacity: 1, duration: 0.08, yoyo: true, repeat: 3 }, q(11.4));
    tl.to("#sbx", { borderColor: "rgba(255,59,78,.85)", duration: 0.2 }, q(11.4));
    cut("#sc3", 11.8, 0);
    // 11.8-17.63 TH: sistem pengawasan diperluas
    full(11.8, 5, 1.04, 1.1);
    full(13.067, 6, 1.02, 1.06, 13.1); punch(13.14, 1.16); tl.to("#vw", { scale: 1.2, duration: 2.5, ease: "none" }, q(13.4));
    full(15.933, 7, 1.04, 1.1);
    // 17.63-20.33 CUT 2: pengawasnya berlapis
    cutout(17.633, "#sc4");
    show("#lp1", 19.42, 0.3, { scale: 0.7 }); show("#lp2", 19.74, 0.3, { scale: 0.7 }); show("#lp3", 19.96, 0.3, { scale: 0.7 });
    tl.to(["#lp1", "#lp2", "#lp3"], { scale: 1.04, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 1, stagger: 0.06 }, q(20.0));
    cut("#sc4", 20.333, 0);
    // 20.33-25.2 PIP: pemeriksa -> tanda mencurigakan
    cut("#sc5", 20.333, 1); pipIn(20.333, 10, 1.05); pipSet(23.267, 11);
    show("#n1", 20.72, 0.3, { x: -50 });
    tl.fromTo("#n1a", { opacity: 0 }, { opacity: 1, duration: 0.2 }, q(21.64)); tl.fromTo("#n1b", { opacity: 0 }, { opacity: 1, duration: 0.2 }, q(22.36));
    draw("#c1", 23.08); show("#n2", 23.44, 0.3, { x: -50 });
    tl.to("#n2", { borderColor: "rgba(255,59,78,.8)", duration: 0.12, yoyo: true, repeat: 3 }, q(24.22));
    cut("#sc5", 25.2, 0);
    // 25.2-27.6 TH: AI investigasi menelusuri
    full(25.2, 12, 1.04, 1.12);
    // 27.6-31.03 PIP: investigasi -> peringatan
    cut("#sc5", 27.6, 1); pipIn(27.6, 13, 1.05); pipSet(29.167, 14);
    draw("#c2", 27.6); show("#n3", 27.66, 0.3, { x: -50 });
    draw("#c3", 28.9); show("#n4", 29.44, 0.3, { x: -50 });
    tl.to("#n4 .ic", { scale: 1.12, rotation: 8, duration: 0.12, yoyo: true, repeat: 5, ease: "sine.inOut" }, q(30.16));
    tl.to("#n4", { borderColor: "rgba(255,214,10,.85)", duration: 0.2 }, q(30.16));
    cut("#sc5", 31.033, 0);
    // 31.03-33.77 TH: seberapa cepat? (open loop)
    full(31.033, 15, 1.06, 1.1);
    full(31.867, 16, 1.0, 1.04, 32.6); punch(32.7, 1.14);
    // 33.77-41.6 PIP: ~30 menit
    full(33.767, 17, 1.0, 1.02);
    cut("#sc6", 34.133, 1); pipIn(34.133, 18, 1.05); pipSet(36.033, 19); pipSet(39.667, 20);
    show("#simc", 35.5, 0.3, { y: -16 });
    show("#bar", 36.2, 0.3, { y: 20 }); pop("#tdA", 36.3); pop("#tdB", 37.22);
    show("#tlB", 37.4, 0.28, { y: 16 });
    tl.fromTo("#bar i", { scaleX: 0 }, { scaleX: 1, duration: 2.4, ease: "power1.inOut" }, q(37.22));
    show("#big", 38.16, 0.3, { scale: 0.8 });
    var cnt = { v: 0 }, numEl = document.getElementById("num");
    tl.fromTo(cnt, { v: 0 }, { v: 30, duration: 1.0, ease: "power2.out", onUpdate: function () { numEl.textContent = "±" + Math.round(cnt.v); } }, q(38.3));
    show("#tlA", 40.06, 0.28, { y: 16 });
    tl.to("#tdA", { scale: 1.15, duration: 0.15, yoyo: true, repeat: 3 }, q(40.36));
    // 41.6-43.7 PIP: tapi ingat, hasil simulasi (shot ini ada subtitle bawaan Flow: wajib tertutup)
    tl.set(["#simc", "#big", "#bar", "#tdA", "#tdB", "#tlA", "#tlB"], { opacity: 0 }, q(41.6));
    pipSet(41.6, 21); pipSet(42.267, 22);
    pop("#warn", 41.62, 0.35);
    cut("#sc6", 43.7, 0);
    // 43.7-51.37 TH: bukan berarti dihentikan (B&W + coret), lalu inti
    full(43.7, 23, 1.38, 1.44); bw(45.78, 47.1);
    tl.set("#strike", { top: 1060 + 400 / 2 + 50 }, 0);
    tl.fromTo("#strike", { opacity: 1, scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out" }, q(46.6));
    hide("#strike", 46.98, 0.12);
    full(47.1, 24, 1.04, 1.08, 49.7); punch(49.74, 1.16);
    // 51.37-53.87 CUT 3: besok
    cutout(51.367, "#sc7");
    pop("#ev", 52.64, 0.32); pop("#gd", 52.9, 0.32);
    // 53.87-56.7 PIP: AI melemahkan pengawasnya
    pipIn(53.867, 26, 1.05); pipSet(55.167, 27);
    tl.to(["#ev", "#evl", "#gd", "#gdl"], { y: "+=300", duration: 0.45, ease: "power3.inOut" }, q(53.867));
    tl.to("#ev", { x: 520, duration: 0.4, ease: "power3.in" }, q(55.32));
    tl.to("#gd", { background: "#3a3d44", color: "#FF3B4E", boxShadow: "0 0 0 rgba(0,0,0,0)", rotation: -12, y: 330, duration: 0.25, ease: "power2.out" }, q(55.7));
    tl.to("#gdl", { color: "#FF3B4E", duration: 0.2 }, q(55.86));
    cut("#sc7", 56.7, 0);
    // 56.7-59.1 TH: save + follow
    full(56.7, 27, 1.08, 1.04, 57.2); tl.to("#vw", { scale: 1.08, duration: 1.9, ease: "none" }, q(57.2));
"""

def main():
    pub = HERE / "public"
    (pub / "fonts").mkdir(parents=True, exist_ok=True)
    (pub / "vendor").mkdir(exist_ok=True)
    for f in FONTS.values():
        shutil.copy(SK / "assets/fonts" / f, pub / "fonts" / f)
    shutil.copy(MONO, pub / "fonts/Mono.ttf")
    shutil.copy(HERE / "uji-gaya/A/public/vendor/gsap.min.js", pub / "vendor/gsap.min.js")
    shutil.copy(HERE / "uji-gaya/A/public/hyperframes.json", pub / "hyperframes.json")
    shutil.copy(LOGO, pub / "openai.png")
    if not (pub / "plate.mp4").exists():
        shutil.copy(TAKE, pub / "plate.mp4")
    html = U.page("Full", CSS, BODY, JS, {"locks": [d for _, d in LOCKS], "pip": PIP})
    (pub / "index.html").write_text(html, encoding="utf-8")
    print("ok", len(LOCKS), "lockups")

main()
