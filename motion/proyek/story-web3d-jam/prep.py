# Media for the reel: VO (0.3 s lead + tail pad), the creator's Aset-iklan.mp4 screen recording cropped to the monitor
# and cut to the VO ("berputar" -> rotating watch, "dibongkar" -> exploded view), a second clip for the offer card and
# a still of the watch for the hook's "foto" card.   python prep.py
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "sumber" / "Aset-iklan.mp4"
OUT = HERE / "public" / "assets"
VS, TAIL = 0.3, 1.2
VO = json.loads((HERE / "vo" / "vo-full.json").read_text(encoding="utf-8"))
T = {i: w["start"] + VS for i, w in enumerate(VO["words"])}
DUR = round(VO["words"][-1]["end"] + VS + TAIL, 2)
CROP = "crop=600:338:124:80"   # monitor area (the phone drifts a little, so inset from the bezel)


def run(a):
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + a, check=True)


run(["-i", str(HERE / "vo" / "vo-full.mp3"), "-af", f"adelay={int(VS * 1000)}:all=1,apad=whole_dur={DUR}", "-t", str(DUR),
     "-ar", "44100", str(HERE / "public" / "vo.mp3")])

v0 = T[63] - 0.12 + 0.15                      # browser card with footage appears
c1, c2, c3 = T[73] - 0.25, T[75] - 0.1, T[79] - 0.05   # cut to rotation, cut to exploded view, card leaves
SEGS = [(0.3, c1 - v0), (3.0, c2 - c1), (8.0, c3 - c2)]   # (source in, length)
args, ch = [], []
for k, (a, n) in enumerate(SEGS):
    args += ["-ss", f"{a:.2f}", "-t", f"{n:.3f}", "-i", str(SRC)]
    ch.append(f"[{k}:v]{CROP},scale=1280:720:flags=lanczos,setsar=1,fps=30,eq=contrast=1.08:saturation=1.1,setpts=PTS-STARTPTS[v{k}]")
fx = ";".join(ch) + ";" + "".join(f"[v{k}]" for k in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[o]"
run(args + ["-filter_complex", fx, "-map", "[o]", "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", str(OUT / "screen.mp4")])
# offer card: Calibre + "detak yang bisa dilihat"
run(["-ss", "10.5", "-t", "6", "-i", str(SRC), "-vf", f"{CROP},scale=960:540:flags=lanczos,setsar=1,fps=30,eq=contrast=1.08:saturation=1.1",
     "-an", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(OUT / "offer.mp4")])
run(["-ss", "1.0", "-i", str(SRC), "-frames:v", "1", "-vf", f"{CROP},scale=960:540:flags=lanczos,eq=contrast=1.08:saturation=1.1",
     "-q:v", "3", str(OUT / "still_watch.jpg")])
print("ok DUR", DUR, "screen", round(c3 - v0, 2), "s")
