# SFX + musik untuk reel "CEO Nvidia pergi & kembali". SFX ElevenLabs dipakai ulang dari reel kebocoran API key + chime/papers
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


# visual dari Remotion: talking-head/remotion (komposisi CeoNvidia) -> renders/visual.mp4
C = [(0.0, "hit_hook", -5, 1.0), (0.05, "whoosh", -15, 0.9), (0.6, "buzz", -12, 0.6), (T[5] - 0.15, "whoosh", -12, 0.7), (T[5] + 0.3, "shimmer", -11, 1.0),
     (T[11] - 0.1, "whoosh", -15, 0.8), (T[15], "slam", -9, 0.6), (T[20], "crack", -10, 0.7), (T[20], "papers", -14, 0.6),
     (T[22], "papers", -14, 0.6), (T[26] + 0.2, "papers", -14, 0.6), (T[32], "buzz", -14, 0.5),
     (T[34] - 0.08, "slam", -8, 0.7), (T[35], "drain", -11, 1.3), (T[37], "whoosh", -14, 0.8), (T[48], "crack", -8, 0.8), (T[48], "buzz", -11, 0.5),
     (T[50] - 0.08, "whoosh", -15, 0.8), (T[53] - 0.1, "whoosh", -14, 0.6), (T[59], "stamp", -6, 0.8),
     (T[65] - 0.08, "whoosh", -15, 0.8), (T[66], "tick", -16, 0.9), (T[66] + 0.1, "tick", -16, 0.6), (T[71], "pop", -12, 0.35),
     (T[74] - 0.1, "whoosh", -13, 0.8), (T[74], "shimmer", -11, 1.2),
     (T[76] - 0.08, "whoosh", -15, 0.8), (T[78], "tick", -15, 1.2), (T[79] + 0.5, "hit_hook", -8, 0.9), (T[83], "pop", -11, 0.35),
     (T[91] - 0.08, "whoosh", -14, 0.8), (T[97], "pop", -14, 0.3), (T[97] + 0.3, "pop", -14, 0.3), (T[97] + 0.6, "pop", -14, 0.3), (T[101], "slam", -11, 0.5),
     (T[105], "confirm", -12, 0.7), (T[106], "crack", -13, 0.6), (T[107], "buzz", -12, 0.5),
     (T[109] - 0.1, "whoosh", -14, 0.8), (T[116], "whoosh", -16, 0.6), (T[123], "pop", -10, 0.35), (T[123] + 0.1, "confirm", -11, 0.9)]


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
