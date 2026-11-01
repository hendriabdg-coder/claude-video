# SFX + music for the style-template previews (paper / pulse / terminal / avatar / setup / showcase / guide). Same recipe as the full
# videos: Epidemic SFX library, Eleven Music bed at the creator's preferred level (volume -7.5 dB = ~12-15 dB under the voice, ducked),
# loudnorm -14 LUFS.  python gaya_sfx.py [style ...]   (no args = all styles)
import subprocess
from pathlib import Path

import numpy as np

from gaya_common import words

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LIB = ROOT / "new sfx"
P = {
    "wh_fast": "whosh/fast whoosh.mp3", "wh_fly": "whosh/fly through whoosh.mp3", "wh_cine": "whosh/cinematic whoosh.mp3",
    "wh_impact": "whosh/impact whoosh.mp3", "wh_soft": "whosh/ES_Swooshes, Whoosh, Softs - Epidemic Sound.mp3",
    "wh_swish": "whosh/ES_Swooshes, Swish, Short, Wind Gusts, Dry - Epidemic Sound.mp3",
    "hit_deep": "ES_Short, Deep, Dry - Epidemic Sound.mp3", "hit_washed": "ES_Short, Washed Mids, Low End, Dry - Epidemic Sound.mp3",
    "hit_thump": "wood hit/ES_Thump, Hit, Hollow 02 - Epidemic Sound.mp3", "hit_final": "ES_Impact, Final Hit - Epidemic Sound.mp3",
    "hit_dark1": "ES_Impact, Dark, Cinematic, Hard Hit 01 - Epidemic Sound.mp3",
    "st_metal": "new Epic Trailer/ES_Designed, Stinger, Impact, Metal Detail - Epidemic Sound.mp3",
    "st_brass": "new Epic Trailer/ES_Designed, Stinger, Brassy, Big Shock Hit - Epidemic Sound.mp3",
    "click_dbl": "ui/ES_User Interface, Click, Button, Double Click, Fast, Phone Tap - Epidemic Sound.mp3",
    "click_metal": "click/ES_Mechanical, Click, Metal Click, Close, Variations 01 - Epidemic Sound.mp3",
    "ui_open": "ui/ES_Sci Fi Games, UI Menu, Very Short, Open 10 - Epidemic Sound.mp3",
    "ui_confirm": "ui/ES_User Interface, Beep, Notification, Confirm, Positive - Epidemic Sound.mp3",
    "ui_popup": "ui/ES_User Interface, Click, Software, Interface, Pop Up, Notification - Epidemic Sound.mp3",
    "ui_glitch": "ui/ES_Chimes, UI Glitch - Epidemic Sound.mp3",
    "glitch_tr": "glitch/ES_User Interface, Glitch, Medium, Video Transition, Motion 01 - Epidemic Sound.mp3",
    "pop": "pop/ES_Cartoon, Pop, Pops x6 - Epidemic Sound.mp3", "bubble": "ES_Bubble Effect 03 - Epidemic Sound.mp3",
    "tick": "click/ES_Mechanical, Click, Tick, Medium, Loopable, Clocks 02 - Epidemic Sound.mp3",
    "typing": "typing/ES_Computers, Keyboard & Mouse, Keyboard, Macbook Pro 2015, Typing, Moderate - Epidemic Sound.mp3",
    "neg": "message/ES_User Interface, Alert, Notification, Message Recieved, Negative, Flute, Short - Epidemic Sound.mp3",
    "tap": "message/ES_User Interface, Click, Select, Smartphone, Short 03 - Epidemic Sound.mp3",
    "shimmer": "ES_Christmas, Chimes, Sparkle, Magic, Shimmer Dust 03 - Epidemic Sound.mp3",
}

_cache = {}
def analyse(alias):
    if alias not in _cache:
        raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(LIB / P[alias]), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"])
        x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
        env = np.array([np.sqrt((x[i:i + 320] ** 2).mean()) + 1e-9 for i in range(0, len(x) - 320, 320)])
        db = 20 * np.log10(env); k = int(db.argmax()); j = k
        while j > 0 and k - j < 75 and db[j - 1] > db[k] - 24:
            j -= 1
        _cache[alias] = (20 * np.log10(np.abs(x).max() + 1e-9), k * 0.02, j * 0.02)
    return _cache[alias]


def cues_paper(T):
    C = [(0.25, "wh_soft", -12, 1.0, "peak")]
    C += [(T[2] + 0.18 * k, "pop", -11, 0.25, "onset") for k in range(3)]
    C += [(T[6] + 0.12 * k, "tap", -12, None, "onset") for k in range(3)]
    C += [(T[10], "wh_swish", -14, 0.6, "peak"), (T[11], "ui_popup", -13, 0.6, "onset"), (T[12], "wh_soft", -12, 1.0, "peak"),
          (T[13], "wh_fly", -12, 1.2, "peak"), (T[13], "tick", -15, 1.0, "onset"), (T[15], "tick", -14, T[19] - T[15] + 0.3, "onset"),
          (T[19] + 0.35, "hit_deep", -9, 1.4, "onset"), (T[20], "wh_impact", -11, 1.2, "peak"), (T[23], "ui_confirm", -12, None, "onset"),
          (T[24], "tap", -14, None, "onset"), (12.4, "wh_cine", -11, 1.2, "peak"), (12.6, "shimmer", -15, 1.6, "onset")]
    return C


def cues_pulse(T):
    hits = ["hit_thump", "hit_deep", "hit_washed", "hit_thump", "st_metal", "hit_dark1", "hit_dark1", "hit_dark1", "hit_deep", "hit_final"]
    starts = [0.0, T[0], T[3], T[7], T[12], T[13], T[14], T[15], T[17], T[21]]
    C = [(t, h, -7 if h in ("hit_final", "st_metal") else -9, 1.2, "onset") for t, h in zip(starts, hits)]
    C += [(t - 0.02, "wh_fast", -14, 0.4, "peak") for t in starts[1:]]
    C += [(T[5], "wh_fast", -10, 0.4, "peak"), (T[5] + 0.1, "neg", -12, 0.9, "onset"), (12.3, "st_brass", -7, 1.8, "onset")]
    return C


def cues_terminal(T):
    C = [(0.1 + 0.25 * k, "click_metal", -16, None, "onset") for k in range(3)]
    C += [(T[0], "typing", -15, 2.6, "onset"), (T[9] - 0.2, "ui_open", -12, None, "onset"), (T[9] - 0.2, "glitch_tr", -16, 0.4, "peak")]
    C += [(T[i], "typing", -13, 0.3, "onset") for i in (10, 11, 12)]
    C += [(T[14] - 0.1, "click_dbl", -10, None, "onset"), (T[14], "ui_glitch", -15, 0.8, "onset"), (T[18], "neg", -10, 0.9, "onset"),
          (T[18], "glitch_tr", -14, 0.5, "peak"), (T[20], "typing", -15, 0.6, "onset"), (T[21], "tick", -14, T[25] - T[21] + 0.5, "onset"),
          (T[25] + 0.5, "ui_confirm", -11, None, "onset"), (12.4, "glitch_tr", -12, 0.6, "peak"), (12.45, "hit_deep", -11, 1.4, "onset")]
    return C


def cues_avatar(T):
    C = [(0.45, "wh_fly", -12, 1.0, "peak"), (T[0], "bubble", -13, 0.6, "onset"), (T[2], "pop", -12, 0.25, "onset"),
         (T[4], "pop", -11, 0.25, "onset"), (T[4] + 0.45, "tap", -14, None, "onset"), (T[5] - 0.1, "wh_swish", -13, 0.6, "peak"),
         (T[5], "click_dbl", -13, None, "onset"), (T[9], "ui_popup", -13, 0.6, "onset"), (T[11] + 0.15, "ui_confirm", -13, None, "onset"),
         (T[13] - 0.1, "wh_soft", -13, 1.0, "peak")]
    C += [(T[14] + 0.3 * k + 0.25, "wh_swish", -19, 0.4, "peak") for k in range(4)]
    C += [(T[18] - 0.05, "hit_deep", -9, 1.4, "onset"), (T[18], "shimmer", -13, 1.4, "onset"), (T[18] + 0.4, "glitch_tr", -17, 0.4, "peak"),
          (T[21], "hit_thump", -11, 1.0, "onset"), (T[21] + 0.05, "shimmer", -12, 1.6, "onset"),
          (12.4, "wh_cine", -11, 1.2, "peak"), (12.5, "bubble", -13, 0.6, "onset")]
    return C


def cues_setup(T):
    C = [(0.6, "wh_soft", -15, 1.0, "peak"), (T[6] + 0.6, "wh_cine", -11, 1.2, "peak"), (T[7], "glitch_tr", -16, 0.4, "peak"),
         (T[9], "click_metal", -14, None, "onset"), (T[11] - 0.05, "pop", -11, 0.25, "onset")]
    C += [(T[15] + 0.1 * k + 0.2, "wh_fast", -13, 0.4, "peak") for k in range(3)]
    C += [(T[15] + 0.5, "hit_thump", -11, 1.0, "onset"), (T[17], "tick", -15, 0.7, "onset"), (T[19] - 0.1, "wh_soft", -13, 1.0, "peak"),
          (T[22] - 0.25, "hit_washed", -11, 1.2, "onset")]
    C += [(T[23] + 0.12 * k, "click_metal", -10, None, "onset") for k in range(6)]
    C += [(T[23] + 0.7, "ui_confirm", -10, None, "onset"), (T[23] + 0.7, "hit_deep", -10, 1.4, "onset"),
          (12.4, "wh_cine", -11, 1.2, "peak"), (12.5, "shimmer", -15, 1.6, "onset")]
    return C


def cues_showcase(T):
    C = [(0.15, "wh_fly", -12, 1.0, "peak"), (0.4, "wh_soft", -15, 1.0, "peak"), (T[2], "pop", -12, 0.25, "onset"),
         (T[3], "wh_swish", -12, 0.5, "peak"), (T[3] + 0.3, "neg", -14, 0.8, "onset"),
         (T[4] - 0.1, "wh_fast", -11, 0.4, "peak"), (T[4] + 0.1, "hit_thump", -11, 1.0, "onset"), (T[7], "pop", -11, 0.25, "onset"),
         (T[8], "click_dbl", -13, None, "onset"), (T[8] + 0.2, "wh_swish", -13, 0.9, "peak"), (T[10], "ui_popup", -13, 0.6, "onset"),
         (T[11], "wh_cine", -12, 1.4, "peak"), (T[14], "pop", -12, 0.25, "onset"), (T[15], "wh_soft", -13, 1.0, "peak"),
         (T[19], "ui_confirm", -14, None, "onset"), (T[20], "hit_deep", -9, 1.4, "onset"), (T[20] + 0.9, "click_metal", -11, None, "onset"),
         (T[20] + 1.0, "ui_confirm", -12, None, "onset"), (T[21], "shimmer", -13, 1.6, "onset"), (T[21] + 0.6, "bubble", -14, 0.6, "onset"),
         (12.3, "wh_cine", -11, 1.2, "peak"), (12.45, "bubble", -13, 0.6, "onset")]
    return C


def cues_guide(T):
    b1, b2, b3, b4 = T[6] - 0.12, T[9] - 0.12, T[14] - 0.12, T[20] - 0.12
    end = min(max(T[23] + 1.1, 12.3), 13.0)
    C = [(0.05, "hit_thump", -10, 1.0, "onset"), (0.15, "wh_fly", -13, 1.0, "peak"), (0.5, "pop", -12, 0.25, "onset"),
         (T[3] + 0.15, "bubble", -15, 0.6, "onset"), (b1, "wh_swish", -13, 0.5, "peak")]
    C += [(T[7] - 0.1 + 0.16 * k, "pop", -12, 0.25, "onset") for k in range(3)]
    C += [(b2, "wh_soft", -14, 0.9, "peak"), (b2 + 0.25, "ui_popup", -15, 0.6, "onset"), (T[10], "typing", -16, T[13] - T[10] + 0.2, "onset"),
          (T[13] + 0.5, "click_dbl", -11, None, "onset"), (b3, "wh_swish", -13, 0.5, "peak")]
    C += [(t, "ui_confirm", -15, None, "onset") for t in (T[17], T[19], min(T[19] + 0.6, b4 - 0.3))]
    C += [(b4, "wh_fast", -12, 0.4, "peak"), (b4 + 0.3, "pop", -13, 0.25, "onset"), (T[23], "tap", -12, None, "onset"),
          (T[23] + 0.55, "hit_deep", -9, 1.2, "onset"), (end, "wh_cine", -11, 1.2, "peak"), (end + 0.3, "shimmer", -15, 1.6, "onset")]
    return C


def mix(style, cues):
    d = HERE / f"gaya-{style}"
    src, music, out = d / "renders" / "visual.mp4", d / "public" / "music.mp3", d / "renders" / "final.mp4"
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)]))
    args, chains = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-i", str(music)], []
    for k, (t, alias, db, maxlen, align) in enumerate(sorted(cues), start=2):
        pk, tpeak, tonset = analyse(alias)
        start = tonset if align == "onset" else max(tpeak - 0.6, 0)
        at = t if align == "onset" else t - (tpeak - start)
        args += ["-ss", f"{start:.3f}", "-i", str(LIB / P[alias])]
        trim = f"atrim=0:{maxlen:.3f},afade=t=out:st={max(maxlen - 0.2, 0):.3f}:d=0.2," if maxlen else ""
        chains.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,{trim}volume={db - pk:.2f}dB,"
                      f"adelay={int(round(max(at, 0) * 1000))}:all=1[s{k}]")
    n = len(cues)
    fx = ";".join(chains)
    fx += f";{''.join(f'[s{k}]' for k in range(2, n + 2))}amix=inputs={n}:normalize=0:duration=longest,atrim=0:{dur:.3f}[bed]"
    fx += ";[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=3[voice][k1][k2]"
    fx += ";[bed][k1]sidechaincompress=threshold=0.06:ratio=2:attack=10:release=180[sfx]"
    fx += f";[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{dur:.3f},volume=-7.5dB,afade=t=out:st={dur - 1.0:.3f}:d=1.0[mus0]"
    fx += ";[mus0][k2]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=350[mus]"
    fx += ";[voice][sfx][mus]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.84,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]"
    subprocess.run(args + ["-filter_complex", fx, "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                           "-movflags", "+faststart", str(out)], check=True)
    print(style, n, "cues ->", out)


if __name__ == "__main__":
    import sys
    ALL = {"paper": cues_paper, "pulse": cues_pulse, "terminal": cues_terminal, "avatar": cues_avatar, "setup": cues_setup,
           "showcase": cues_showcase, "guide": cues_guide}
    for style in sys.argv[1:] or ALL:
        mix(style, ALL[style](words(style)))
