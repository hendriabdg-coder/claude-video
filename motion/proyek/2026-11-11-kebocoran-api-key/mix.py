# SFX + musik untuk reel kebocoran API key (CLAUDE.md §7). Library Epidemic tidak ada di sesi cloud, jadi SFX dan musik
# dibuat dengan ElevenLabs (Sound Effects eleven_text_to_sound_v2 + Eleven Music v2.5, instrumental) dari akun Endrich,
# file di audio/ (tidak masuk git; 11 SFX dipakai ulang dari Hari 10 + shutter, drain, vault). Cue mengikuti build.py.
# Musik di-duck oleh VO dan gain-nya diukur supaya ~13,5 dB di bawah VO saat bicara; akhir alimiter + loudnorm -14 LUFS.
#   python mix.py   ->  renders/final.mp4
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
from reel_common import words  # noqa: E402

A = HERE / "audio"
T = words(HERE.name)
GAP_DB = 13.5


def pcm(path, sr=48000):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def analyse(name):
    """peak dBFS and onset (first sample within 30 dB of the peak) of an SFX file."""
    x = pcm(A / f"{name}.mp3")
    pk = float(np.abs(x).max()) + 1e-9
    on = int(np.argmax(np.abs(x) > pk * 10 ** (-30 / 20)))
    return 20 * np.log10(pk), on / 48000


# window starts (sama dengan build.py)
W = {"B": T[9] - 0.08, "D": T[27] - 0.08, "E": T[51] - 0.08, "F": T[71] - 0.08, "G": T[77] - 0.08, "H": T[94] - 0.08,
     "I": T[112] - 0.08, "J": T[134] - 0.08, "K": T[147] - 0.08}
E = T[163]
# (time, sfx, peak dB, max length s) — tempo cepat: lebih banyak hit pendek, whoosh dipotong pendek
C = [(0.0, "hit_hook", -5, 1.0), (0.1, "whoosh", -15, 1.0), (T[7] - 0.05, "slam", -9, 0.6),
     (W["B"], "slam", -7, 0.7), (T[11] - 0.05, "slam", -6, 0.8), (T[16] - 0.05, "whoosh", -15, 0.8), (T[19], "crack", -9, 0.9),
     (T[19] + 0.1, "tick", -18, 1.0), (T[22] - 0.05, "pop", -12, 0.35), (T[25] - 0.1, "pop", -13, 0.35),
     (W["D"], "whoosh", -14, 0.8), (W["D"] + 0.1, "tick", -18, 0.7), (T[33] - 0.2, "shimmer", -13, 1.2), (T[40] - 0.1, "pop", -12, 0.35),
     (T[44], "pop", -12, 0.35), (T[47] - 0.05, "buzz", -11, 0.7),
     (W["E"], "whoosh", -14, 0.8), (T[56] - 0.1, "pop", -12, 0.35), (T[64] - 0.05, "typing", -15, 0.9), (T[67], "buzz", -11, 0.7),
     (T[68], "slam", -11, 0.6),
     (W["F"], "slam", -7, 0.7), (T[74] - 0.05, "slam", -8, 0.7),
     (W["G"], "whoosh", -15, 0.8), (T[84] - 0.1, "shutter", -8, 0.6), (T[85] - 0.05, "typing", -14, 0.8), (T[90] - 0.05, "pop", -11, 0.35),
     (T[92], "buzz", -14, 0.7),
     (W["H"], "whoosh", -14, 0.8), (T[100] - 0.3, "tick", -15, 1.0), (T[100] + 0.75, "hit_hook", -7, 1.0), (T[102] - 0.05, "slam", -10, 0.6),
     (T[106], "pop", -13, 0.35),
     (W["I"], "whoosh", -15, 0.8), (T[119] - 0.1, "pop", -12, 0.35), (T[124] - 0.05, "drain", -10, 1.2), (T[128] - 0.05, "pop", -12, 0.35),
     (T[130], "stamp", -9, 0.8),
     (W["J"], "whoosh", -15, 0.8), (T[135], "whoosh", -17, 1.0), (T[138], "vault", -8, 1.2), (T[140] - 0.05, "pop", -12, 0.35),
     (T[143] - 0.05, "pop", -12, 0.35), (T[145], "pop", -13, 0.35),
     (W["K"], "whoosh", -14, 0.8), (T[154] - 0.05, "slam", -9, 0.6), (T[161], "slam", -12, 0.6),
     (E + 0.8, "pop", -12, 0.35), (E + 1.3, "confirm", -10, 0.9), (E + 1.8, "pop", -12, 0.35), (E + 1.95, "pop", -12, 0.35)]


def music_gain(vo, music, probe=-10.0):
    """Gain so the ducked music sits GAP_DB under the voice while the voice speaks (Eleven Music beds vary in level)."""
    fx = (f"[0:a]aformat=sample_rates=48000:channel_layouts=mono,asplit=2[v][k];[1:a]aformat=sample_rates=48000:channel_layouts=mono,"
          f"volume={probe}dB[m0];[m0][k]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=350[m]")
    tmp = {k: HERE / "renders" / f"_{k}.raw" for k in ("v", "m")}
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vo), "-i", str(music), "-filter_complex", fx,
                    "-map", "[v]", "-f", "s16le", str(tmp["v"]), "-map", "[m]", "-f", "s16le", str(tmp["m"])], check=True)
    v, m = (np.fromfile(tmp[k], np.int16).astype(np.float32) / 32768 for k in ("v", "m"))
    for f in tmp.values():
        f.unlink()
    n = min(len(v), len(m)) // 4800 * 4800
    rv, rm = (20 * np.log10(np.sqrt((x[:n].reshape(-1, 4800) ** 2).mean(1)) + 1e-9) for x in (v, m))
    act = rv > rv.max() - 20
    return round(probe - (GAP_DB - float(np.median(rv[act] - rm[act]))), 1)


src, out = HERE / "renders" / "visual.mp4", HERE / "renders" / "final.mp4"
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)]))
args, chains = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-i", str(A / "music.mp3")], []
for k, (t, name, db, maxlen) in enumerate(sorted(C), start=2):
    pk, on = analyse(name)
    args += ["-ss", f"{on:.3f}", "-i", str(A / f"{name}.mp3")]
    chains.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{maxlen:.3f},"
                  f"afade=t=out:st={max(maxlen - 0.15, 0):.3f}:d=0.15,volume={db - pk:.2f}dB,adelay={int(round(max(t, 0) * 1000))}:all=1[s{k}]")
n = len(C)
gain = music_gain(HERE / "public" / "vo.mp3", A / "music.mp3")
fx = ";".join(chains)
fx += f";{''.join(f'[s{k}]' for k in range(2, n + 2))}amix=inputs={n}:normalize=0:duration=longest,atrim=0:{dur:.3f}[bed]"
fx += ";[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=3[voice][k1][k2]"
fx += ";[bed][k1]sidechaincompress=threshold=0.06:ratio=2:attack=10:release=180[sfx]"
fx += (f";[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{dur:.3f},volume={gain}dB,"
       f"afade=t=out:st={dur - 1.5:.3f}:d=1.5[mus0];[mus0][k2]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=350[mus]")
fx += ";[voice][sfx][mus]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.84,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]"
subprocess.run(args + ["-filter_complex", fx, "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                       "-movflags", "+faststart", str(out)], check=True)
print(n, "cues, music", gain, "dB ->", out)
