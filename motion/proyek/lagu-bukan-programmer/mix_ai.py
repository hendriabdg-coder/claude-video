# Audio final opsi A (dipilih Endrich 2026-11-12): vokal penyanyi AI Eleven Music (take B) apa adanya; hanya 3 baris
# "lawan bicara AI" diganti stem: instrumental + vokal terisolasi berfilter telepon, crossfade 40 ms.
#   python mix_ai.py  ->  audio/lagu_final.wav
import subprocess
from pathlib import Path
import numpy as np

A = Path(__file__).resolve().parent / "audio"
SR = 48000
AI = [(3.18, 3.72), (6.42, 7.80), (32.82, 33.90)]


def load(p, ch=2):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(p), "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"])
    return np.frombuffer(raw, np.float32).reshape(-1, ch).copy()


mix, inst = load(A / "takeB.mp3"), load(A / "inst_2.5.wav")
phone = load_phone = None
raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(A / "vocal_iso.mp3"), "-af",
                               "highpass=f=450,lowpass=f=3200,acrusher=bits=10:mix=0.25,volume=1.25",
                               "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"])
phone = np.frombuffer(raw, np.float32).reshape(-1, 2)
n = min(len(mix), len(inst), len(phone))
mix, alt = mix[:n], inst[:n] * 0.92 + phone[:n]
w = np.zeros(n, np.float32)
for a, b in AI:
    i0, i1, f = int(a * SR), int(b * SR), int(0.04 * SR)
    w[i0:i1] = 1
    w[i0 - f:i0] = np.linspace(0, 1, f); w[i1:i1 + f] = np.linspace(1, 0, f)
out = mix * (1 - w[:, None]) + alt * w[:, None]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af",
                "alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000", str(A / "lagu_final.wav")],
               input=out.astype(np.float32).tobytes(), check=True)
print("ok", n / SR)
