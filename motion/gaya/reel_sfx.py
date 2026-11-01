# SFX + music mix for full reels (CLAUDE.md §7): Epidemic SFX cues aligned to the VO word timeline, Eleven Music bed
# 12-15 dB under the VO (gain measured per song so the ducked bed sits ~13.5 dB under speech), hit in 0-1 s,
# alimiter + loudnorm -14 LUFS / TP -1.5.
# Writes motion/proyek/<slug>/renders/final.mp4.   python reel_sfx.py <slug> [<slug> ...]
import subprocess
import sys
from pathlib import Path

import numpy as np

from gaya_sfx import LIB, P, analyse
from reel_common import words

HERE = Path(__file__).resolve().parent
P.update({
    "riser": "riser/ES_Bass, Sharp Detail Riser - Epidemic Sound.mp3",
    "msg": "message/ES_Communications, Cellphone, Smartphone, Send, Receive Message 01 - Epidemic Sound.mp3",
    "static": "drones/ES_Designed, Drone, Void, Static 01 - Epidemic Sound.mp3",
    "heart": "heartbeats/ES_Cinematic, 45 BPM - Epidemic Sound.mp3",
    # QC 2026-10-25: the non-ES whooshes in gaya_sfx (cinematic/fast/impact/fly through) have no clear license -> ES only
    "wh_cine": "whosh/ES_Swooshes, Whoosh, Classic, Hollow, Low, Long - Epidemic Sound.mp3",
    "wh_fast": "whosh/ES_Swooshes, Whoosh, Organic, Wind, Muffled, Fast - Epidemic Sound.mp3",
    "wh_impact": "ES_Swoosh, Reverse, Bassy Fire - Epidemic Sound.mp3",
    "wh_fly": "whosh/ES_Swooshes, Whoosh, Generic Long Whooshes, Fast Attack, Release - Epidemic Sound.mp3",
})


def cues_celah(T):        # Senin · EMBER
    C = [(0.0, "hit_dark1", -8, 1.6, "onset"), (0.15, "shimmer", -17, 1.2, "onset"),
         (T[6] + 0.3, "glitch_tr", -15, 0.5, "peak"), (T[9] - 0.05, "hit_deep", -8, 1.4, "onset"), (T[9] - 0.05, "wh_impact", -12, 1.0, "peak"),
         (T[11], "wh_cine", -13, 1.2, "peak"), (T[12] - 0.05, "wh_swish", -15, 0.6, "peak")]
    C += [(t + 0.22, "hit_thump", -10, 0.8, "onset") for t in (T[19], T[21], T[23])]
    C += [(T[25], "wh_soft", -14, 1.0, "peak"), (T[32] - 0.05, "st_metal", -8, 1.4, "onset"),
          (T[37], "wh_fast", -15, 0.4, "peak"), (T[39], "tick", -16, 0.8, "onset"), (T[40] + 0.3, "hit_washed", -10, 1.0, "onset"),
          (T[41], "wh_swish", -15, 0.6, "peak"), (T[50] - 0.6, "tick", -17, 1.2, "onset"), (T[52] + 0.22, "hit_dark1", -9, 1.4, "onset"),
          (T[54], "wh_cine", -14, 1.2, "peak"), (T[65], "pop", -12, 0.25, "onset"), (T[65] + 0.5, "click_dbl", -11, None, "onset"),
          (T[65] + 0.58, "ui_confirm", -13, None, "onset"), (T[71], "wh_soft", -15, 1.0, "peak"),
          (T[80] - 0.05, "ui_popup", -13, 0.6, "onset"), (T[82] - 0.05, "ui_popup", -13, 0.6, "onset")]
    return C


def cues_intelligent(T):  # Selasa · SIGNAL
    C = [(0.0, "hit_thump", -9, 1.0, "onset"), (0.35, "msg", -14, 0.8, "onset"), (0.8, "typing", -18, 1.0, "onset"),
         (T[6], "wh_fast", -12, 0.4, "peak"), (T[6] + 0.2, "hit_washed", -9, 1.0, "onset"),
         (T[8] - 0.1, "wh_cine", -13, 1.2, "peak"), (T[12], "pop", -12, 0.25, "onset"), (T[15], "pop", -12, 0.25, "onset"),
         (T[20] - 0.05, "ui_open", -13, None, "onset"), (T[21] - 0.05, "ui_open", -13, None, "onset"), (T[22], "tap", -13, None, "onset"),
         (T[23] - 0.05, "ui_open", -13, None, "onset"), (T[23] + 0.1, "tick", -17, 0.7, "onset"),
         (T[24] - 0.1, "wh_soft", -14, 1.0, "peak"), (T[26], "tap", -14, None, "onset"), (T[27], "tap", -14, None, "onset"),
         (T[28] + 0.2, "ui_confirm", -12, None, "onset"), (T[29], "wh_swish", -14, 0.6, "peak"), (T[30], "hit_thump", -11, 0.8, "onset"),
         (T[40] - 0.3, "wh_fly", -14, 1.2, "peak"), (T[46], "neg", -13, 0.9, "onset"),
         (T[52], "wh_swish", -14, 0.6, "peak"), (T[53] + 0.2, "pop", -12, 0.25, "onset"),
         (T[59], "pop", -12, 0.25, "onset"), (T[61] + 0.5, "click_dbl", -11, None, "onset"), (T[61] + 0.58, "ui_confirm", -13, None, "onset"),
         (T[70], "wh_soft", -15, 1.0, "peak"), (T[72], "ui_popup", -13, 0.6, "onset"), (T[76], "ui_popup", -13, 0.6, "onset")]
    return C


def cues_suara(T):        # Rabu · TERMINAL
    C = [(0.0, "hit_dark1", -8, 1.6, "onset"), (0.15, "msg", -12, 0.8, "onset"), (0.9, "msg", -15, 0.8, "onset"),
         (T[3], "tick", -15, 0.9, "onset"), (T[3] + 0.9, "neg", -10, 0.9, "onset"), (T[3] + 0.9, "hit_deep", -9, 1.4, "onset"),
         (T[6], "glitch_tr", -15, 0.4, "peak"), (T[10] - 0.15, "wh_swish", -15, 0.6, "peak"), (T[11], "typing", -17, 0.6, "onset"),
         (T[14], "static", -22, 2.2, "onset"), (T[17] + 0.22, "hit_washed", -9, 1.0, "onset"), (T[17] + 0.22, "glitch_tr", -14, 0.5, "peak"),
         (T[19] - 0.15, "wh_fast", -14, 0.4, "peak"), (T[20], "tick", -16, 1.6, "onset"), (T[20] + 1.6, "ui_confirm", -13, None, "onset"),
         (T[28], "ui_open", -13, None, "onset"), (T[31], "tick", -15, 1.2, "onset"), (T[35], "neg", -12, 0.9, "onset")]
    C += [(t, "typing", -15, 0.5, "onset") for t in (T[38], T[44], T[49])]
    C += [(T[52] + 0.55, "neg", -11, 0.9, "onset"), (T[52] + 0.55, "glitch_tr", -15, 0.4, "peak"),
          (T[58] - 0.2, "wh_cine", -14, 1.2, "peak"), (T[65] - 0.1, "hit_thump", -11, 0.8, "onset"),
          (T[69], "pop", -12, 0.25, "onset"), (T[69] + 0.5, "click_dbl", -11, None, "onset"), (T[69] + 0.58, "ui_confirm", -13, None, "onset"),
          (T[74], "wh_soft", -15, 1.0, "peak"), (T[78] - 0.05, "ui_popup", -13, 0.6, "onset"), (T[81] - 0.05, "ui_popup", -13, 0.6, "onset")]
    return C


CUES = {"2026-10-26-ai-pemburu-celah": cues_celah, "2026-10-27-chatgpt-intelligent-ui": cues_intelligent,
        "2026-10-28-penipuan-suara-ai": cues_suara}


GAP_DB = 13.5


def music_gain(d, probe=-7.5):
    """Gain for the music bed so that, after VO ducking, it sits GAP_DB under the voice while the voice speaks.
    Eleven Music beds differ a lot in loudness, so a fixed volume is not enough."""
    fx = (f"[0:a]aformat=sample_rates=48000:channel_layouts=mono,asplit=2[v][k];[1:a]aformat=sample_rates=48000:channel_layouts=mono,"
          f"volume={probe}dB[m0];[m0][k]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=350[m]")
    tmp = {k: d / "renders" / f"_{k}.raw" for k in ("v", "m")}
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(d / "public" / "vo.mp3"), "-i", str(d / "public" / "music.mp3"),
                    "-filter_complex", fx, "-map", "[v]", "-f", "s16le", str(tmp["v"]), "-map", "[m]", "-f", "s16le", str(tmp["m"])], check=True)
    v, m = (np.fromfile(tmp[k], np.int16).astype(np.float32) / 32768 for k in ("v", "m"))
    for f in tmp.values():
        f.unlink()
    n = min(len(v), len(m)) // 4800 * 4800
    rv, rm = (20 * np.log10(np.sqrt((x[:n].reshape(-1, 4800) ** 2).mean(1)) + 1e-9) for x in (v, m))
    act = rv > rv.max() - 20
    return round(probe - (GAP_DB - float(np.median(rv[act] - rm[act]))), 1)


def mix(slug, cues):
    d = HERE / slug if (HERE / slug).exists() else HERE.parent / "proyek" / slug
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
    gain = music_gain(d)
    fx += f";[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{dur:.3f},volume={gain}dB,afade=t=out:st={dur - 1.2:.3f}:d=1.2[mus0]"
    fx += ";[mus0][k2]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=350[mus]"
    fx += ";[voice][sfx][mus]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.84,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]"
    subprocess.run(args + ["-filter_complex", fx, "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                           "-movflags", "+faststart", str(out)], check=True)
    print(slug, n, "cues, music", gain, "dB ->", out)


if __name__ == "__main__":
    for slug in sys.argv[1:]:
        mix(slug, CUES[slug](words(slug)))
