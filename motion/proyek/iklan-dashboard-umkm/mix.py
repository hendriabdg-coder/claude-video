# Mix iklan dashboard: VO (sudah di visual.mp4) + musik Eleven Music (±13,5 dB di bawah VO setelah ducking) + SFX ElevenLabs.
#   python mix.py keynote|material|meta  ->  renders/final_<v>.mp4
import json, re, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
A = HERE / "audio"
V = sys.argv[1]
html = (HERE / f"build_{V}" / "public" / "index.html").read_text()
K = json.loads(re.search(r"var K = (\{.*?\})", html).group(1))
GAP_DB = 13.5


def pcm(p, sr=48000):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"])
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def analyse(name):
    x = pcm(A / f"{name}.mp3"); pk = float(np.abs(x).max()) + 1e-9
    return 20 * np.log10(pk), int(np.argmax(np.abs(x) > pk * 10 ** (-30 / 20))) / 48000


C = [(0.0, "papers", -10, 1.5), (K["nota"] + 0.35, "pop", -14, 0.35), (K["nota"] + 0.65, "pop", -14, 0.35), (K["nota"] + 0.95, "pop", -14, 0.35),
     (K["catat"] - 0.2, "wake", -9, 1.2), (K["menit"], "chime", -11, 0.7), (K["harga"], "pop", -13, 0.35), (K["harga"] + 0.45, "pop", -13, 0.35),
     (K["harga"] + 0.9, "pop", -13, 0.35), (K["dash"] - 0.1, "whoosh", -15, 0.8), (K["dash"], "tick", -18, 0.9), (K["kotor"], "tick", -19, 0.9),
     (K["bersih"], "tick", -19, 0.9), (K["bersih"] + 0.9, "chime", -12, 0.7), (K["banding"], "whoosh", -16, 0.8), (K["banding"] + 1.1, "confirm", -12, 0.8),
     (K["bulan"], "whoosh", -16, 0.8), (K["pilih"], "pop", -11, 0.35), (K["grafik"], "shimmer", -15, 1.0)]
if V == "meta":
    C += [(K["beres"], "whoosh", -16, 0.8), (K["beres"] + 0.3, "papers", -16, 1.0), (K["begadang"], "chime", -12, 0.7),
          (K["link"], "whoosh", -15, 0.8), (K["bawah"] - 0.1, "hit_hook", -10, 1.0), (K["bawah"] + 0.5, "confirm", -13, 0.9)]
else:
    C += [(K["bahan"], "whoosh", -16, 0.8), (K["bahan"] + 0.8, "buzz", -16, 0.6), (K["daftar"], "chime", -12, 0.7), (K["mau"], "whoosh", -15, 0.8),
          (K["comment"] + 0.2, "hit_hook", -9, 1.0), (K["link"], "confirm", -11, 0.9)]
if V == "material":
    C += [(K["catat"] + 0.7, "typing", -17, 1.0), (K["catat"] + 1.3, "typing", -18, 1.0), (K["comment"] + 0.1, "typing", -16, 0.5), (K["comment"] + 0.7, "pop", -11, 0.35)]


def music_gain(vo, music, probe=-10.0):
    fx = (f"[0:a]aformat=sample_rates=48000:channel_layouts=mono,asplit=2[v][k];[1:a]aformat=sample_rates=48000:channel_layouts=mono,"
          f"volume={probe}dB[m0];[m0][k]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=350[m]")
    tmp = {k: HERE / "renders" / f"_{k}.raw" for k in ("v", "m")}
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vo), "-i", str(music), "-filter_complex", fx,
                    "-map", "[v]", "-f", "s16le", str(tmp["v"]), "-map", "[m]", "-f", "s16le", str(tmp["m"])], check=True)
    v, m = (np.fromfile(tmp[k], np.int16).astype(np.float32) / 32768 for k in ("v", "m"))
    for f in tmp.values(): f.unlink()
    n = min(len(v), len(m)) // 4800 * 4800
    rv, rm = (20 * np.log10(np.sqrt((x[:n].reshape(-1, 4800) ** 2).mean(1)) + 1e-9) for x in (v, m))
    act = rv > rv.max() - 20
    return round(probe - (GAP_DB - float(np.median(rv[act] - rm[act]))), 1)


src, out, mus = HERE / "renders" / f"visual_{V}.mp4", HERE / "renders" / f"final_{V}.mp4", A / f"music_{V}.mp3"
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)]))
args, chains = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-i", str(mus)], []
for k, (t, name, db, mx) in enumerate(sorted(C), start=2):
    pk, on = analyse(name)
    args += ["-ss", f"{on:.3f}", "-i", str(A / f"{name}.mp3")]
    chains.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{mx:.3f},afade=t=out:st={max(mx - 0.15, 0):.3f}:d=0.15,"
                  f"volume={db - pk:.2f}dB,adelay={int(round(max(t, 0) * 1000))}:all=1[s{k}]")
n = len(C)
gain = music_gain(HERE / f"build_{V}" / "public" / "vo.mp3", mus)
fx = ";".join(chains)
fx += f";{''.join(f'[s{k}]' for k in range(2, n + 2))}amix=inputs={n}:normalize=0:duration=longest,atrim=0:{dur:.3f}[bed]"
fx += ";[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=3[voice][k1][k2]"
fx += ";[bed][k1]sidechaincompress=threshold=0.06:ratio=2:attack=10:release=180[sfx]"
fx += (f";[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{dur:.3f},volume={gain}dB,afade=t=out:st={dur - 1.3:.3f}:d=1.3[mus0];"
       f"[mus0][k2]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=350[mus]")
fx += ";[voice][sfx][mus]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.84,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]"
subprocess.run(args + ["-filter_complex", fx, "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                       "-movflags", "+faststart", str(out)], check=True)
print(V, n, "cues, music", gain, "dB ->", out)
