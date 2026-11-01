# Plate renderer: smooth sub-pixel digital zooms anchored on the eyes, punch-ins, B&W beats, light grade.
#   python plate.py plate.json
# plate.json (all times in seconds; use frame/30 for frame-exact camera cuts):
# {
#   "src": "../../video 02.mp4", "out": "public/plate.mp4",
#   "cuts":  [0, 3.6667, 9.1, 99],                 # shot boundaries (first 0, last 99)
#   "eyes":  [[0.465,0.374],[0.49,0.36],[0.47,0.37]],  # eye anchor per shot, as fraction of SOURCE width/height
#   "seg":   [[0,1,1.14,1.04],[1,3.6667,1.04,1.07]],   # [start,end,zoom_from,zoom_to], smoothstep inside, hard cut between
#   "bw":    [[7.78,9.1]],                           # black & white windows (optional)
#   "grade": {"contrast":1.05,"saturation":1.06},    # optional
#   "broll": [                                       # optional cutaways; the take's audio keeps playing underneath
#     {"start":12.4,"end":14.9,"file":"D:/Claude Video/talking-head/aset/broll/broll_ketik-laptop.mp4",
#      "in":1.0, "anchor":[0.5,0.5], "push":[1.00,1.06]}   # in-point s, crop anchor (fraction), slow push zoom
#   ]
# }
# Output: 1080x1920, 30 fps, dense keyframes (-g 30), source audio copied. Zoom 1.00 = the largest 9:16 window
# that fits the source (a 16:9 source is cropped around the eyes, never letterboxed).
import json, os, subprocess, sys
from PIL import Image

P = json.load(open(sys.argv[1], encoding="utf-8"))
OW, OH, FPS = 1080, 1920, 30
r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", P["src"]],
                   capture_output=True, text=True, check=True)
SW, SH = map(int, r.stdout.strip().split(",")[:2])
NATIVE = abs(SW / SH - 9 / 16) < 0.01
BW_, BH_ = (SW, SH) if NATIVE else (min(SW, SH * 9 / 16), min(SW, SH * 9 / 16) * 16 / 9)
CUTS, EYES, SEG = P["cuts"], P["eyes"], P["seg"]
BW = P.get("bw", [])
G = P.get("grade", {})

def zoom(t):
    for a, b, z0, z1 in SEG:
        if a <= t < b:
            p = (t - a) / (b - a)
            return z0 + (z1 - z0) * p * p * (3 - 2 * p)
    return SEG[-1][3]

def eyes(t):
    for k in range(len(CUTS) - 1):
        if CUTS[k] <= t < CUTS[k + 1]:
            return EYES[min(k, len(EYES) - 1)]
    return EYES[-1]

def box(t):
    z = zoom(t)
    ax, ay = eyes(t)
    w, h = BW_ / z, BH_ / z
    if NATIVE:   # keep the eyes where they are on screen while zooming (proven on take / video01)
        cx = SW * ax + (SW / 2 - SW * ax) / z
        cy = SH * ay + (SH / 2 - SH * ay) / z
    else:        # wide source: centre horizontally on the eyes, eyes at ~37% of frame height
        cx = SW * ax
        cy = SH * ay + h * (0.5 - 0.37)
    cx = min(max(cx, w / 2), SW - w / 2)
    cy = min(max(cy, h / 2), SH - h / 2)
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", P["src"], "-vf",
                        f"fps={FPS},eq=contrast={G.get('contrast', 1.05)}:saturation={G.get('saturation', 1.06)}",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
vf = "vignette=angle=PI/5"
if BW:
    bw = "+".join(f"between(t,{a:.4f},{b:.4f})" for a, b in BW)
    vf = f"hue=s=0:enable='{bw}',eq=contrast=1.12:enable='{bw}'," + vf
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
                        "-i", P["src"], "-map", "0:v", "-map", "1:a?", "-vf", vf,
                        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-g", str(FPS), "-keyint_min", str(FPS),
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", P["out"]],
                       stdin=subprocess.PIPE)
BROLL = sorted(P.get("broll", []), key=lambda b: b["start"])
_bdec = {}       # index -> [decoder process, last frame]
def broll_frame(k, t):
    b = BROLL[k]
    if k not in _bdec:
        ax, ay = b.get("anchor", [0.5, 0.5])
        vf = (f"fps={FPS},scale={OW}:{OH}:force_original_aspect_ratio=increase,"
              f"crop={OW}:{OH}:(iw-{OW})*{ax}:(ih-{OH})*{ay},"
              f"eq=contrast={G.get('contrast', 1.05)}:saturation={G.get('saturation', 1.06)}")
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(b.get("in", 0)), "-i", b["file"], "-an", "-vf", vf,
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        _bdec[k] = [p, None]
    p, last = _bdec[k]
    buf = p.stdout.read(OW * OH * 3)
    if len(buf) == OW * OH * 3:
        last = Image.frombuffer("RGB", (OW, OH), buf, "raw", "RGB", 0, 1).copy()
        _bdec[k][1] = last
    elif last is None:
        sys.exit(f"b-roll {b['file']} gave no frames")
    elif not b.get("_warned"):
        print(f"warning: {os.path.basename(b['file'])} shorter than its slot, holding last frame"); b["_warned"] = True
    z0, z1 = b.get("push", [1.0, 1.06])
    q = (t - b["start"]) / max(b["end"] - b["start"], 1e-6)
    z = z0 + (z1 - z0) * q
    w, h = OW / z, OH / z
    return last.resize((OW, OH), Image.LANCZOS, box=((OW - w) / 2, (OH - h) / 2, (OW + w) / 2, (OH + h) / 2))

fsize = SW * SH * 3
i = 0
while True:
    buf = dec.stdout.read(fsize)
    if len(buf) < fsize:
        break
    t = i / FPS
    k = next((n for n, b in enumerate(BROLL) if b["start"] <= t < b["end"]), None)
    if k is not None:
        enc.stdin.write(broll_frame(k, t).tobytes())
    else:
        img = Image.frombuffer("RGB", (SW, SH), buf, "raw", "RGB", 0, 1)
        enc.stdin.write(img.resize((OW, OH), Image.LANCZOS, box=box(t)).tobytes())
    i += 1
for p, _ in _bdec.values():
    p.kill()
enc.stdin.close()
enc.wait()
print("plate done:", i, "frames ->", P["out"], "| source", f"{SW}x{SH}", "native 9:16" if NATIVE else "cropped to 9:16")
