# Build the "plate": source video at 1080x1920/30fps with smooth sub-pixel zooms
# (anchored on the eyes so the face stays put), punch-ins, B&W beats and a light grade.
import subprocess, sys, numpy as np
from PIL import Image

SRC = "../../mentah/take/take.mp4"
OUT = "public/plate.mp4"
SW, SH = 1440, 2560          # source size
OW, OH = 1080, 1920          # output size
FPS = 30
AX, AY = 0.523, 0.357        # zoom anchor = between the eyes (fraction of frame)

# (start, end, zoom_from, zoom_to) — smoothstep inside each segment, hard cut between
SEG = [
    (0.00, 1.20, 1.14, 1.03),   # hook: pull back
    (1.20, 3.85, 1.03, 1.06),
    (3.85, 6.10, 1.10, 1.13),   # "Dots" punch-in (text behind head)
    (6.10, 9.60, 1.00, 1.04),   # split scene
    (9.60, 10.95, 1.24, 1.27),  # "tapi coba dengerin ini" punch (B&W)
    (10.95, 17.40, 1.02, 1.06),
    (17.40, 20.30, 1.06, 1.09),
    (20.30, 22.88, 1.00, 1.00), # red card covers
    (22.88, 27.06, 1.00, 1.10), # slow push while "ditunda" builds
    (27.06, 31.00, 1.04, 1.06), # relief pull-back
    (31.00, 33.05, 1.08, 1.10),
    (33.05, 34.95, 1.22, 1.25), # "risikonya tetap ada" punch (B&W)
    (34.95, 41.00, 1.02, 1.05), # split scene
    (41.00, 42.55, 1.08, 1.12),
    (42.55, 45.25, 1.03, 1.06),
    (45.25, 46.70, 1.12, 1.14), # "1 hari?" punch (text behind head)
    (46.70, 51.65, 1.00, 1.00), # black card covers
    (51.65, 60.00, 1.06, 1.14), # slow push to the end
]
BW = [(9.60, 10.95), (33.05, 34.95)]

def zoom(t):
    for a, b, z0, z1 in SEG:
        if a <= t < b:
            p = (t - a) / (b - a)
            s = p * p * (3 - 2 * p)
            return z0 + (z1 - z0) * s
    return SEG[-1][3]

dec = subprocess.Popen(
    ["ffmpeg", "-v", "error", "-i", SRC, "-vf", f"fps={FPS},eq=contrast=1.05:saturation=1.07",
     "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
bw = "+".join(f"between(t,{a},{b})" for a, b in BW)
enc = subprocess.Popen(
    ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}",
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
    w, h = SW / z, SH / z
    cx = SW * AX + (SW / 2 - SW * AX) / z
    cy = SH * AY + (SH / 2 - SH * AY) / z
    box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    img = Image.frombuffer("RGB", (SW, SH), buf, "raw", "RGB", 0, 1)
    enc.stdin.write(img.resize((OW, OH), Image.LANCZOS, box=box).tobytes())
    i += 1
    if i % 150 == 0:
        print(f"{i} frames ({t:.1f}s)", flush=True)
enc.stdin.close()
enc.wait()
print("done", i, "frames")
