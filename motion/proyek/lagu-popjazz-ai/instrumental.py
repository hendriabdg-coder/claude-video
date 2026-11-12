# Instrumental "kasar" dari lagu Eleven Music: lagu - vokal hasil Voice Isolator (disejajarkan + gain least-squares per band
# waktu). Eleven Music tidak memberi stem, jadi ini cara mendapatkan bed musik di bawah vokal suara Endrich.
#   python instrumental.py audio/takeB.mp3 audio/vocal_iso.mp3 audio/instrumental.wav
import subprocess, sys
import numpy as np
from scipy.signal import correlate, stft, istft

def load(p, sr=48000):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"])
    return np.frombuffer(raw, np.float32).copy()

mix, voc = load(sys.argv[1]), load(sys.argv[2])
n = min(len(mix), len(voc)); mix, voc = mix[:n], voc[:n]
seg = slice(48000 * 5, 48000 * 25)
c = correlate(mix[seg], voc[seg], mode="full", method="fft"); lag = int(np.argmax(c)) - (len(mix[seg]) - 1)
voc = np.roll(voc, lag)
# spectral subtraction: per time-frequency bin remove the vocal's magnitude estimate (soft mask)
f, t, M = stft(mix, 48000, nperseg=2048); _, _, V = stft(voc, 48000, nperseg=2048)
g = np.sum(np.abs(M) * np.abs(V)) / (np.sum(np.abs(V) ** 2) + 1e-9)
A = float(sys.argv[4]) if len(sys.argv) > 4 else 2.5   # over-subtraction: residual vocal ends up under Endrich's vocal
mask = np.clip(1 - A * g * np.abs(V) / (np.abs(M) + 1e-9), 0.02, 1)
_, inst = istft(M * mask, 48000, nperseg=2048)
inst = inst[:n] / (np.abs(inst).max() + 1e-9) * 0.9
raw = (inst * 32767).astype(np.int16).tobytes()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "48000", "-ac", "1", "-i", "-", "-ac", "2", sys.argv[3]], input=raw, check=True)
print("lag", lag, "gain", round(float(g), 3))
