# SFX + musik untuk reel Hari 10 (CLAUDE.md §7). Library Epidemic tidak ada di sesi cloud, jadi SFX dan musik
# dibuat dengan ElevenLabs (Sound Effects eleven_text_to_sound_v2 + Eleven Music v2.5, instrumental) dari akun Endrich,
# file di audio/ (tidak masuk git). Cue mengikuti kejadian layar di build.py (timeline kata VO).
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


# (time, sfx, peak dB, max length s)
C = [(0.0, "hit_hook", -5, 1.0), (0.1, "whoosh", -15, 1.6), (0.8, "tick", -17, 1.0), (1.8, "tick", -19, 0.9),
     (T[14] - 0.1, "slam", -8, 0.8),
     (T[16] - 0.12, "slam", -7, 0.8), (T[17], "slam", -8, 0.8), (T[19] - 0.1, "whoosh", -15, 1.2),
     (T[31] + 0.05, "crack", -8, 1.0), (T[33] - 0.1, "slam", -7, 0.8),
     (T[35] - 0.1, "whoosh", -15, 1.2), (T[42] - 0.2, "shimmer", -14, 1.6),
     (T[45], "pop", -12, 0.4), (T[47], "pop", -12, 0.4), (T[52], "pop", -11, 0.4),
     (T[55] - 0.1, "paper", -11, 2.0), (T[63] - 0.1, "shimmer", -13, 1.6),
     (T[70] - 0.12, "whoosh", -16, 1.0), (T[71], "typing", -15, 1.0), (T[77] + 0.1, "typing", -17, 1.0),
     (T[80] + 0.15, "pop", -13, 0.4), (T[82] + 0.15, "pop", -11, 0.4),
     (T[86] - 0.1, "whoosh", -15, 1.2), (T[89] - 0.05, "slam", -10, 0.8),
     (T[92] - 0.12, "whoosh", -16, 1.0), (T[95] - 0.1, "chain", -10, 1.0),
     (T[99] - 0.12, "slam", -7, 0.8), (T[101] - 0.05, "slam", -9, 0.8), (T[103] - 0.05, "slam", -8, 0.8),
     (T[108] - 0.12, "whoosh", -15, 1.2), (T[110], "paper", -18, 1.2),
     (T[115], "pop", -13, 0.4), (T[118] + 0.1, "buzz", -12, 0.8), (T[121], "pop", -13, 0.4), (T[127], "pop", -13, 0.4),
     (T[140] + 0.12, "stamp", -7, 1.0),
     (T[143] - 0.12, "whoosh", -14, 1.2), (T[157] - 0.1, "pop", -12, 0.4), (T[159], "confirm", -10, 1.0),
     (T[162] - 0.12, "whoosh", -15, 1.2), (T[170] - 0.05, "pop", -12, 0.4), (T[174] - 0.05, "pop", -12, 0.4)]


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
