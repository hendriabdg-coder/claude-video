# SFX + musik untuk reel "Rekor IPO Anthropic". SFX ElevenLabs dipakai ulang dari reel kebocoran API key + chime/papers
# (iklan dashboard); musik Eleven Music dari reel kebocoran API key (instrumental, tegang-tech, 71 dtk), jadi tanpa kredit baru.
# Musik di-duck oleh VO, gain diukur ~13,5 dB di bawah VO saat bicara; akhir alimiter + loudnorm -14 LUFS.
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
    x = pcm(A / f"{name}.mp3")
    pk = float(np.abs(x).max()) + 1e-9
    on = int(np.argmax(np.abs(x) > pk * 10 ** (-30 / 20)))
    return 20 * np.log10(pk), on / 48000


W = {k: T[i] - 0.08 for k, i in dict(B=8, C=15, D=25, E=37, F=51, G=70, I=97, J=110, K=123).items()}
# (waktu, sfx, puncak dB, panjang maks dtk)
C = [(0.0, "hit_hook", -5, 1.0), (0.05, "whoosh", -15, 0.9), (T[2] - 0.05, "slam", -9, 0.6),
     (T[7] - 0.05, "crack", -6, 0.9), (T[7], "slam", -7, 0.7),
     (W["B"], "papers", -12, 1.0), (T[11] - 0.1, "typing", -16, 0.6), (T[12] + 0.25, "buzz", -12, 0.6), (T[14] - 0.1, "stamp", -7, 0.8),
     (W["C"], "whoosh", -15, 0.8), (T[16], "pop", -12, 0.35), (T[18] + 0.2, "pop", -12, 0.35), (T[23], "tick", -18, 0.6),
     (W["D"], "whoosh", -15, 0.8), (W["D"] + 0.15, "pop", -12, 0.35), (T[30], "typing", -16, 0.5), (T[32], "typing", -16, 0.5),
     (T[34], "typing", -16, 0.5), (T[36] - 0.1, "slam", -9, 0.6),
     (W["E"], "whoosh", -15, 0.8), (T[38], "tick", -16, 0.9), (T[39] + 0.3, "hit_hook", -9, 0.8), (T[47], "whoosh", -17, 0.6),
     (T[50], "pop", -11, 0.35), (T[50] + 0.1, "confirm", -12, 0.8),
     (W["F"], "whoosh", -15, 0.8), (T[53], "tick", -16, 1.1), (T[55], "hit_hook", -9, 0.8), (T[59], "pop", -12, 0.35),
     (T[66], "whoosh", -17, 0.6), (T[67], "whoosh", -17, 0.8), (T[68] + 0.2, "shimmer", -12, 1.2),
     (W["G"], "chime", -8, 1.4), (T[71] + 0.2, "chime", -11, 1.0), (T[75], "whoosh", -14, 0.7), (T[75], "tick", -17, 0.6),
     (T[79], "confirm", -11, 0.8), (T[82], "slam", -12, 0.6), (T[86], "tick", -18, 1.2), (T[91], "pop", -12, 0.35),
     (W["I"], "whoosh", -15, 0.8), (T[101], "slam", -7, 0.7), (T[104], "buzz", -12, 0.7), (T[105], "drain", -10, 1.3),
     (T[106], "pop", -13, 0.35), (T[108] - 0.2, "stamp", -10, 0.7),
     (W["J"], "whoosh", -15, 0.8), (T[113], "pop", -13, 0.3), (T[113] + 0.18, "pop", -13, 0.3), (T[113] + 0.36, "pop", -13, 0.3),
     (T[113] + 0.54, "pop", -13, 0.3), (T[115], "vault", -11, 1.0),
     (W["K"], "whoosh", -14, 0.8), (T[126], "pop", -11, 0.35), (T[130], "pop", -11, 0.35), (T[133], "whoosh", -16, 0.6),
     (T[138], "pop", -10, 0.35), (T[138] + 0.1, "confirm", -10, 0.9)]


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
