# Plate for "video 01": 1080x1920/30fps, smooth sub-pixel zooms anchored on the eyes of
# each camera shot (the take is jump-cut into 6 shots), punch-ins, one B&W beat, light grade.
import subprocess, numpy as np
from PIL import Image

SRC = "../../mentah/video01/video 01.mp4"
OUT = "public/plate.mp4"
SW, SH = 1440, 2560
OW, OH = 1080, 1920
FPS = 30
F = lambda n: n / FPS            # frame index -> seconds (cuts are frame-exact)
CUTS = [0, F(110), F(273), F(546), F(710), F(928), 99]
EYES = [(0.465, 0.374), (0.492, 0.358), (0.468, 0.374), (0.468, 0.371), (0.495, 0.368), (0.450, 0.385)]

# (start, end, zoom_from, zoom_to) — smoothstep inside each segment, hard cut between
SEG = [
    (0.00, 1.00, 1.14, 1.04),      # hook pull-back ("JANGAN" behind head)
    (1.00, F(110), 1.04, 1.07),
    (F(110), 7.78, 1.00, 1.04),    # split: chat mock
    (7.78, F(273), 1.22, 1.26),    # B&W punch "tapi angkanya dari mana?"
    (F(273), F(546), 1.00, 1.05),  # split: what AI doesn't know
    (F(546), 21.26, 1.04, 1.12),   # slow push "tebakan rata-rata"
    (21.26, 23.36, 1.00, 1.00),    # red card covers
    (23.36, F(710), 1.16, 1.17),   # punch "terus AI gunanya apa?"
    (F(710), 25.10, 1.17, 1.20),
    (25.10, F(928), 1.00, 1.04),   # split: let AI do the math
    (F(928), 32.85, 1.03, 1.07),
    (32.85, 34.72, 1.12, 1.15),    # punch "keputusan harganya tetap di kamu" ("KAMU" behind head)
    (34.72, 99.0, 1.05, 1.00),     # CTA pull-back
]
BW = [(7.78, F(273))]

def zoom(t):
    for a, b, z0, z1 in SEG:
        if a <= t < b:
            p = (t - a) / (b - a)
            return z0 + (z1 - z0) * p * p * (3 - 2 * p)
    return SEG[-1][3]

def eyes(t):
    for k in range(6):
        if CUTS[k] <= t < CUTS[k + 1]:
            return EYES[k]
    return EYES[-1]

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", f"fps={FPS},eq=contrast=1.05:saturation=1.08",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
bw = "+".join(f"between(t,{a:.4f},{b:.4f})" for a, b in BW)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}",
                        "-r", str(FPS), "-i", "-", "-i", SRC, "-map", "0:v", "-map", "1:a",
                        "-vf", f"hue=s=0:enable='{bw}',eq=contrast=1.12:enable='{bw}',vignette=angle=PI/5",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-g", str(FPS), "-keyint_min", str(FPS),
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT],
                       stdin=subprocess.PIPE)
fsize = SW * SH * 3
i = 0
while True:
    buf = dec.stdout.read(fsize)
    if len(buf) < fsize:
        break
    t = i / FPS
    z = zoom(t)
    ax, ay = eyes(t)
    w, h = SW / z, SH / z
    cx = SW * ax + (SW / 2 - SW * ax) / z
    cy = SH * ay + (SH / 2 - SH * ay) / z
    img = Image.frombuffer("RGB", (SW, SH), buf, "raw", "RGB", 0, 1)
    enc.stdin.write(img.resize((OW, OH), Image.LANCZOS, box=(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)).tobytes())
    i += 1
enc.stdin.close()
enc.wait()
print("done", i, "frames")
