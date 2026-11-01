# SFX + music pass for "Claude Duet" (SIGNAL) — same recipe as gemini-cek-fakta/sfx_v3.py (the creator's Epidemic Sound
# library + an Eleven Music bed, levels measured from Ref-video-motion). Cue times follow build.py.   python sfx.py
# cue(t, alias, peak dB, max len, align): align "onset" = sound starts at t, "peak" = its loudest moment lands on t.
import json
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LIB = ROOT / "new sfx"
VO = HERE / "vo-sumber" / "vo_final"
SRC = HERE / "renders" / "claude_duet_visual.mp4"
MUSIC = HERE / "public" / "music.mp3"
OUT = ROOT / "output" / "motion" / "_lama" / "claude-duet" / "claude-duet_motion.mp4"
STEMS = HERE / "renders"
GAP = 0.3

P = {  # alias -> file in the Epidemic library
    "wh_fast": "whosh/fast whoosh.mp3",
    "wh_fly": "whosh/fly through whoosh.mp3",
    "wh_fly2": "whosh/fly through whoosh 2.mp3",
    "wh_cine": "whosh/cinematic whoosh.mp3",
    "wh_impact": "whosh/impact whoosh.mp3",
    "wh_soft": "whosh/ES_Swooshes, Whoosh, Softs - Epidemic Sound.mp3",
    "wh_swish": "whosh/ES_Swooshes, Swish, Short, Wind Gusts, Dry - Epidemic Sound.mp3",
    "wh_rev": "ES_Swoosh, Reverse, Bassy Fire - Epidemic Sound.mp3",
    "wh_roll": "rolling/ES_Futuristic, Whoosh, Bass Rolling 02 - Epidemic Sound.mp3",
    "wh_metal": "sound effects 2/random metalic whoosh.mp3",
    "hit_dark1": "ES_Impact, Dark, Cinematic, Hard Hit 01 - Epidemic Sound.mp3",
    "hit_dark2": "ES_Impact, Dark, Cinematic, Hard Hit 02 - Epidemic Sound.mp3",
    "hit_final": "ES_Impact, Final Hit - Epidemic Sound.mp3",
    "hit_deep": "ES_Short, Deep, Dry - Epidemic Sound.mp3",
    "hit_washed": "ES_Short, Washed Mids, Low End, Dry - Epidemic Sound.mp3",
    "hit_thump": "wood hit/ES_Thump, Hit, Hollow 02 - Epidemic Sound.mp3",
    "st_metal": "new Epic Trailer/ES_Designed, Stinger, Impact, Metal Detail - Epidemic Sound.mp3",
    "st_brass": "new Epic Trailer/ES_Designed, Stinger, Brassy, Big Shock Hit - Epidemic Sound.mp3",
    "st_dark": "new Epic Trailer/ES_Designed, Stinger, Hit, Metallic, Tonal, Dark - Epidemic Sound.mp3",
    "st_orch": "new Epic Trailer/ES_Designed, Stinger, Hit, Orchestral Elements, Big - Epidemic Sound.mp3",
    "riser_bass": "riser/ES_Bass, Sharp Detail Riser - Epidemic Sound.mp3",
    "riser_suck": "riser/ES_Designed, Riser, Suckback, Reverse Transition, Build Up Effect 01 - Epidemic Sound.mp3",
    "click_dbl": "ui/ES_User Interface, Click, Button, Double Click, Fast, Phone Tap - Epidemic Sound.mp3",
    "click_metal": "click/ES_Mechanical, Click, Metal Click, Close, Variations 01 - Epidemic Sound.mp3",
    "click_btn": "click/ES_User Interface, Click, Button Press Click, Tap, Video Game, Back, Return, Negative - Epidemic Sound.mp3",
    "ui_open": "ui/ES_Sci Fi Games, UI Menu, Very Short, Open 10 - Epidemic Sound.mp3",
    "ui_confirm": "ui/ES_User Interface, Beep, Notification, Confirm, Positive - Epidemic Sound.mp3",
    "ui_popup": "ui/ES_User Interface, Click, Software, Interface, Pop Up, Notification - Epidemic Sound.mp3",
    "ui_glitch": "ui/ES_Chimes, UI Glitch - Epidemic Sound.mp3",
    "glitch_tr": "glitch/ES_User Interface, Glitch, Medium, Video Transition, Motion 01 - Epidemic Sound.mp3",
    "pop": "pop/ES_Cartoon, Pop, Pops x6 - Epidemic Sound.mp3",
    "bubble": "ES_Bubble Effect 03 - Epidemic Sound.mp3",
    "gear": "gear/ES_Complex Mechanism, Gizmo, Gears 01 - Epidemic Sound.mp3",
    "marker": "hight light/ES_Objects, Writing, Text, Highlight Drag, Marker Highlighter - Epidemic Sound.mp3",
    "typing": "typing/ES_Computers, Keyboard & Mouse, Keyboard, Macbook Pro 2015, Typing, Moderate - Epidemic Sound.mp3",
    "tick": "click/ES_Mechanical, Click, Tick, Medium, Loopable, Clocks 02 - Epidemic Sound.mp3",
    "neg": "message/ES_User Interface, Alert, Notification, Message Recieved, Negative, Flute, Short - Epidemic Sound.mp3",
    "notif": "ES_Notifications 20 - Epidemic Sound.mp3",
    "shimmer": "ES_Christmas, Chimes, Sparkle, Magic, Shimmer Dust 03 - Epidemic Sound.mp3",
    "heart": "heartbeats/ES_Cinematic, 45 BPM - Epidemic Sound.mp3",
    "drone": "drones/ES_Designed, Drone, Space, Weird Tonal 01 - Epidemic Sound.mp3",
    "victory": "ES_Victory, Achievement, Positive, Calm, Drums, Video Game - Epidemic Sound.mp3",
    "audience": "ES_Audience, Interior, Ohhh - Epidemic Sound.mp3",
}

WORDS, off = [], 0.0
for n in range(1, 6):
    d = json.loads((VO / f"scene_{n:02d}.json").read_text(encoding="utf-8"))
    WORDS += [w["start"] + off for w in d["words"]]
    off += float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                          "csv=p=0", str(VO / f"scene_{n:02d}.mp3")])) + GAP
T = lambda i: WORDS[i]
S = {"s5": T(114) - 0.05}

_cache = {}
def analyse(alias):
    """peak dBFS, time of the loudest 20 ms, onset (first moment within 24 dB of that peak, up to 1.5 s before it)."""
    if alias not in _cache:
        raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(LIB / P[alias]), "-ac", "1", "-ar", "16000",
                                       "-f", "s16le", "-"])
        x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
        h = 320
        env = np.array([np.sqrt((x[i:i + h] ** 2).mean()) + 1e-9 for i in range(0, len(x) - h, h)])
        db = 20 * np.log10(env)
        k = int(db.argmax())
        j = k
        while j > 0 and k - j < 75 and db[j - 1] > db[k] - 24:
            j -= 1
        _cache[alias] = (20 * np.log10(np.abs(x).max() + 1e-9), k * 0.02, j * 0.02)
    return _cache[alias]

C = []
def cue(t, alias, db, maxlen=None, align="onset"):
    pk, tpeak, tonset = analyse(alias)
    start = tonset if align == "onset" else max(tpeak - 0.6, 0)   # peak-aligned sounds keep 0.6 s of build-up
    at = t if align == "onset" else t - (tpeak - start)
    C.append((round(max(at, 0), 3), alias, db, maxlen, round(start, 3), pk))

# variety: each event family cycles through several sounds
def cycler(*names):
    state = {"i": 0}
    def nxt():
        state["i"] += 1
        return names[(state["i"] - 1) % len(names)]
    return nxt
WH_HEAD = cycler("wh_soft", "wh_swish", "wh_fast", "wh_fly2", "wh_soft", "wh_metal")
WH_PANEL = cycler("wh_fly", "wh_roll", "wh_fly2", "wh_impact")
HIT_STAMP = cycler("hit_dark1", "hit_final", "hit_dark2")
CLICKS = cycler("click_dbl", "click_metal", "click_btn")
POPS = cycler("pop", "bubble", "ui_popup")

def headline(t): cue(t, WH_HEAD(), -14, 1.2, "peak")
def panel(t): cue(t + 0.15, WH_PANEL(), -9, 1.6, "peak")
def stamp(t):
    cue(t + 0.24, HIT_STAMP(), -5, 2.0)
    cue(t + 0.24, "click_metal", -12)
def chapter(t):
    cue(t, "wh_cine", -9, 1.6, "peak")
    cue(t, "hit_deep", -7, 1.6)
def card(t, sting, tail=2.5):
    cue(t, "riser_suck", -10, 1.6, "peak")
    cue(t, sting, -4, tail)
    cue(t, "glitch_tr", -15, 0.5, "peak")

# SIGNAL leans on UI sounds (phone notifications, clicks, typing, pops); impacts only on the title card and stamps
P.update({
    "msg1": "message/ES_Communications, Cellphone, Smartphone, Send, Receive Message 01 - Epidemic Sound.mp3",
    "msg2": "message/ES_Communications, Cellphone, Smartphone, Send, Receive Message 02 - Epidemic Sound.mp3",
    "msg_pos": "message/ES_User Interface, Alert, Notification, Message Recieved, Positive, Calm 04 - Epidemic Sound.mp3",
    "msg_txt": "message/ES_User Interface, Alert, Notification, Message, Text - Epidemic Sound.mp3",
    "tap": "message/ES_User Interface, Click, Select, Smartphone, Short 03 - Epidemic Sound.mp3",
})

# ---------- 1. APA ----------
cue(0.0, "ui_open", -13)
headline(T(0))
cue(T(2) - 0.1, "wh_fly", -12, 1.4, "peak")                             # phone rises
cue(T(3), "notif", -11)                                                 # alarm bell
cue(T(9), "msg1", -10); cue(T(12), "msg2", -10); cue(T(18), "msg_txt", -10)          # 3 notifications
cue(T(22) - 0.05, "wh_impact", -9, 1.4, "peak"); cue(T(22), "hit_deep", -10, 1.4)     # CLAUDE DUET card
for i in (24, 26, 28):
    cue(T(i), "tap", -13)                                               # date / preview / model chips

# ---------- 2. CARA KERJA ----------
cue(T(32), "wh_swish", -12, 0.8, "peak")                                # chatbot card
cue(T(32) + 0.4, "tick", -17, 1.0)                                      # waiting dots
cue(T(34), "wh_fast", -11, 0.6, "peak"); cue(T(34) + 0.1, "ui_confirm", -11)          # Duet card
headline(T(35))
cue(T(39), "wh_roll", -11, 1.4, "peak"); cue(T(39), "ui_open", -12)     # cloud hub
for i in (43, 44, 45, 47):
    cue(T(i), POPS(), -12, 0.3)                                         # connector chips
cue(T(48), "tick", -15, 1.2)                                            # "secara berkala"
cue(T(51), "msg_pos", -9)                                               # invoice alert

# ---------- 3. ATURAN ----------
headline(T(59))
for i in (63, 65, 66, 69):
    cue(T(i), CLICKS(), -12); cue(T(i) + 0.25, "gear", -15)             # action + lock
cue(T(71), "wh_soft", -12, 1.0, "peak")                                 # approval card
cue(T(73), "wh_swish", -17, 0.5, "peak")                                # cursor glides
cue(T(75), "click_dbl", -8); cue(T(75) + 0.12, "ui_confirm", -11)       # IZINKAN
cue(T(77), "wh_soft", -16, 0.8, "peak")                                 # faint deny rows
cue(T(85), "tap", -12); cue(T(88), "tap", -12)
cue(T(86) + 0.2, "wh_fast", -11, 0.4, "peak"); cue(T(86) + 0.4, "neg", -12, 0.9)
cue(T(90) + 0.1, "wh_fast", -11, 0.4, "peak"); cue(T(90) + 0.3, "neg", -12, 0.9)
stamp(T(90) + 0.45)                                                     # DITOLAK MESKI DIIZINKAN

# ---------- 4. BATASAN ----------
headline(T(91)); cue(T(91) + 0.1, "hit_washed", -11, 1.4)
cue(T(92), "wh_soft", -12, 1.0, "peak")                                 # receipt slides up
for i in (94, 99, 103, 105, 107):
    cue(T(i), "click_metal", -14)                                       # receipt lines print
cue(T(103) + 0.4, "click_metal", -14); cue(T(103) + 0.6, "neg", -11, 0.9)            # Indonesia: Belum
cue(T(110), "tap", -13)
cue(T(111), "tick", -15, 1.0); cue(T(111) + 0.9, "riser_bass", -11, None, "peak")     # limit bar climbs
stamp(T(113))                                                           # TETAP MAKAN LIMIT

# ---------- 5. PENUTUP ----------
cue(S["s5"], "wh_cine", -12, 1.2, "peak")
headline(T(120)); cue(T(120) + 0.2, "bubble", -10)                      # pin bounce
cue(T(121) - 0.1, "wh_soft", -13, 1.0, "peak")                          # comment card
cue(T(121) + 0.2, "typing", -15, T(131) - T(121) - 0.2)                 # comment typed
cue(T(131), "pop", -9, 0.25)                                            # Follow button
cue(T(132), "wh_swish", -17, 0.5, "peak")                               # cursor
cue(T(133) + 0.3, "click_dbl", -8); cue(T(133) + 0.4, "ui_confirm", -11); cue(T(133) + 0.45, "shimmer", -15, 1.2)

# ---------- mix ----------
# no whispered line in this VO: dip disabled
W0, W1 = -2.0, -1.0
DIP = f"pow(10,-14*max(0,min(1,min((t-{W0:.2f})/0.3,({W1:.2f}-t)/0.4)))/20)"
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(SRC)]))
args = ["ffmpeg", "-v", "error", "-y", "-i", str(SRC), "-i", str(MUSIC)]
chains = []
for k, (t, alias, db, maxlen, start, pk) in enumerate(sorted(C), start=2):
    args += ["-ss", f"{start:.3f}", "-i", str(LIB / P[alias])]
    trim = f"atrim=0:{maxlen:.3f},afade=t=out:st={max(maxlen - 0.2, 0):.3f}:d=0.2," if maxlen else ""
    chains.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,{trim}volume={db - pk:.2f}dB,"
                  f"adelay={int(round(t * 1000))}:all=1[s{k}]")
n = len(C)
fx = ";".join(chains)
fx += f";{''.join(f'[s{k}]' for k in range(2, n + 2))}amix=inputs={n}:normalize=0:duration=longest,atrim=0:{dur:.3f}[bed]"
fx += ";[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=3[voice][k1][k2]"
# SFX: light duck (about -3 dB while talking); music: ~6 dB under speech, ducks ~4 dB more under the voice
fx += ";[bed][k1]sidechaincompress=threshold=0.06:ratio=2:attack=10:release=180,asplit=2[sfx][sfxstem]"
fx += (f";[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{dur:.3f},volume=-7.5dB,"
       f"afade=t=out:st={dur - 1.2:.3f}:d=1.2[mus0]")
# the whisper dip comes after the ducker, otherwise the compressor gives most of it back
fx += (";[mus0][k2]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=350,"
       f"volume='{DIP}':eval=frame,asplit=2[mus][musstem]")
fx += (";[voice][sfx][mus]amix=inputs=3:normalize=0:duration=first,"
       "alimiter=limit=0.84,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]")
subprocess.run(args + ["-filter_complex", fx,
                       "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUT),
                       "-map", "[sfxstem]", "-c:a", "pcm_s16le", str(STEMS / "sfx_only.wav"),
                       "-map", "[musstem]", "-c:a", "pcm_s16le", str(STEMS / "music_only.wav")], check=True)
print(f"{n} cues ({n / dur * 60:.0f}/min), {len(set(c[1] for c in C))} different sounds -> {OUT}")
