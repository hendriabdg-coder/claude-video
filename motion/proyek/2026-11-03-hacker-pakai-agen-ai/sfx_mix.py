# SFX sintetis (dibuat sendiri dengan numpy, bebas lisensi) + musik latar + VO -> audio final.
# Library Epidemic ("new sfx/") tidak ada di sesi cloud, jadi SFX dibuat di sini; di laptop bisa diganti library asli.
# Level: musik ~13,5 dB di bawah VO saat bicara (sidechain ducking), akhir loudnorm -14 LUFS, TP <= -1,5 dBFS.
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.argv = [sys.argv[0]]
ns = {"__file__": str(HERE / "build2.py"), "__name__": "build2"}
exec((HERE / "build2.py").read_text(encoding="utf-8"), ns)          # B, K, HITS, DUR
B, K, HITS, DUR = ns["B"], ns["K"], ns["HITS"], ns["DUR"]
SR = 48000
rng = np.random.default_rng(7)
OUT = HERE / "audio"
OUT.mkdir(exist_ok=True)


def env(n, a=0.003, r=None):
    e = np.ones(n)
    na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    if r:
        e *= np.exp(-np.arange(n) / (r * SR))
    return e


def lp(x, k):  # crude one-pole low-pass, k in (0,1)
    y = np.zeros_like(x); s = 0.0
    for i, v in enumerate(x):
        s += k * (v - s); y[i] = s
    return y


def whoosh(d=0.35, up=False):
    n = int(d * SR); x = rng.standard_normal(n)
    sweep = np.linspace(0.02, 0.35, n) if up else np.concatenate([np.linspace(0.03, 0.3, n // 2), np.linspace(0.3, 0.03, n - n // 2)])
    y = np.zeros(n); s = 0.0
    for i in range(n):
        s += sweep[i] * (x[i] - s); y[i] = s
    e = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return y * e * 0.9


def pop(f=900, d=0.09):
    n = int(d * SR); t = np.arange(n) / SR
    fr = f * (1 + 1.5 * np.exp(-t * 60))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(n, 0.001, 0.025) * 0.7


def click():
    n = int(0.025 * SR)
    return (rng.standard_normal(n) * env(n, 0.0005, 0.004) + 0.4 * np.sin(2 * np.pi * 2400 * np.arange(n) / SR) * env(n, 0.0005, 0.003)) * 0.35


def thud(d=0.3):
    n = int(d * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * np.cumsum(110 * (1 + 2 * np.exp(-t * 30))) / SR) * env(n, 0.001, 0.08)
    noise = lp(rng.standard_normal(n), 0.15) * env(n, 0.0005, 0.02)
    return (body + noise * 0.8) * 0.8


def impact():
    n = int(1.2 * SR); t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(55 * (1 + 3 * np.exp(-t * 18))) / SR) * env(n, 0.001, 0.35)
    crack = lp(rng.standard_normal(n), 0.4) * env(n, 0.0005, 0.05)
    return (sub + 0.6 * crack) * 0.95


def ding(f=1320):
    n = int(0.6 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t)) * env(n, 0.001, 0.15) * 0.35


def tick():
    n = int(0.03 * SR)
    return np.sin(2 * np.pi * 3000 * np.arange(n) / SR) * env(n, 0.0005, 0.006) * 0.3


cues = [(0.0, impact(), 0)]
for k in ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9", "b10", "b11"]:
    cues.append((B[k] - 0.12, whoosh(0.32), -6))
for k in range(5):
    cues.append((max(0.0, K["agen"] - 0.6) + k * 0.12 + 0.15, pop(700 + 90 * k), -9))
cues.append((K["seribu"], pop(1100), -8))
cues += [(K["seribu"] + i * 0.09, tick(), -12) for i in range(int((K["situs"] - K["seribu"] + 0.3) / 0.09))]
cues.append((K["situs"] + 0.3, ding(1480), -6))
t = K["perintah"]
while t < K["nggak1"] - 0.2:
    cues.append((t, click(), -6)); t += 0.075 + 0.03 * rng.random()
cues.append((K["seratus1"] - 0.15, pop(1000), -6))
cues.append((B["b2"] + 0.05, whoosh(0.28), -9)); cues.append((K["pertama"] - 0.2, whoosh(0.28), -9))
cues.append((K["pertama"] + 0.05, thud(), -7))
for n_, _ in enumerate(HITS):
    cues.append((K["seratus2"] + 0.2 + n_ * 0.14 + 0.16, thud(0.22), -8))
cues.append((K["biaya"], whoosh(0.3), -8)); cues.append((K["biaya"] + 0.35, thud(0.25), -9))
cues += [(K["biaya"] + 0.2 + i * 0.1, tick(), -13) for i in range(int((K["lima"] - K["biaya"] + 0.5) / 0.1))]
cues.append((K["dua2"] - 0.1, pop(1000), -7))
for k in range(11):
    cues.append((K["dua2"] + 0.6 + k * ((K["sebelas"] - K["dua2"]) / 11), tick(), -9))
cues.append((K["jadi"], whoosh(1.0, up=True), -4))
cues.append((K["jadi"] + 1.0, ding(1760), -7))
cues.append((B["b6"] + 0.3, pop(600), -7))
cues.append((K["manusia"] - 0.2, whoosh(0.28), -9)); cues.append((K["target"] - 0.1, pop(1200), -7))
for k in ["update", "batasi", "backup"]:
    cues.append((K[k] + 0.35, ding(1320 if k != "backup" else 1760), -5))
cues.append((K["melawan"], pop(800), -6)); cues.append((B["b10"] + 0.7, click(), 0)); cues.append((B["b10"] + 0.9, ding(1568), -7))
cues.append((K["data"] - 0.2, pop(900), -7)); cues.append((K["atau"] + 0.2, pop(1100), -7))

n = int((DUR + 0.5) * SR)
sfx = np.zeros(n)
for t0, s, g in cues:
    i = int(max(0, t0) * SR); j = min(n, i + len(s))
    sfx[i:j] += s[: j - i] * 10 ** (g / 20)
sfx = np.clip(sfx, -0.98, 0.98)
import wave
with wave.open(str(OUT / "sfx.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((sfx * 32767).astype(np.int16).tobytes())
(OUT / "sfx_cues.json").write_text(json.dumps([[round(t0, 3), g] for t0, _, g in cues]))
print("sfx cues:", len(cues))


def lufs(path, extra=""):
    o = subprocess.run(["ffmpeg", "-i", str(path), "-af", (extra + "," if extra else "") + "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return float(o.rsplit("I:", 1)[1].split("LUFS")[0])


music = OUT / "music.mp3"
vo = HERE / "vo" / "vo-full.mp3"
# music gain: aim music (before ducking) ~ 9 dB below VO; ducking adds ~4.5 dB more while speaking => ~13.5 dB
if not music.exists():
    fc = (f"[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0[vo];[2:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=-3dB[fx];"
          f"[vo][fx]amix=inputs=2:normalize=0:duration=longest,atrim=0:{DUR},alimiter=limit=0.84:level=false,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vo), "-i", str(vo), "-i", str(OUT / "sfx.wav"), "-filter_complex", fc,
                    "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s16le", str(OUT / "mix.wav")], check=True)
    print("TANPA musik (audio/music.mp3 belum ada); mix -> audio/mix.wav"); sys.exit(0)
mg = lufs(vo) - lufs(music) - 9.0
fc = (f"[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=2[vo][sc];"
      f"[1:a]aresample=48000,volume={mg:.2f}dB,afade=t=in:d=0.3,afade=t=out:st={DUR - 1.8:.2f}:d=1.8[mu];"
      f"[mu][sc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=350[duck];"
      f"[2:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=-3dB[fx];"
      f"[vo][duck][fx]amix=inputs=3:normalize=0:duration=longest,atrim=0:{DUR},"
      f"alimiter=limit=0.84:level=false,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vo), "-i", str(music), "-i", str(OUT / "sfx.wav"),
                "-filter_complex", fc, "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s16le", str(OUT / "mix.wav")], check=True)
print(f"music gain {mg:.1f} dB; mix -> audio/mix.wav")
