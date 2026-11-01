# Cut the creator's three phone recordings of the web-3D demos into the one 8 s "screen" clip shown inside the
# browser card (comp 4.86 -> 12.94), cropped to the monitor and scaled to 1280x720, plus three stills for the
# "aku yang bikin" beat.  python prep_clips.py
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "sumber"
OUT = HERE / "public" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

# monitor area inside each 848x478 recording (x, y, w, h), inset a little from the bezel
CROP = {"watch": ("Web-3D-Sinematik02.mp4", (168, 112, 572, 316)),
        "log": ("Web-3D-sinematik01.mp4", (130, 90, 630, 348)),
        "int": ("Web-3D-Interaktif.mp4", (128, 62, 584, 324))}
# (source, src_in, src_out, speed): watch 3.24 s, logistics 0.96+0.72+0.72, interaktif 0.8+1.68  -> 8.12 s
SEGS = [("watch", 1.0, 4.24, 1.0), ("log", 2.3, 3.26, 1.0), ("log", 6.8, 7.52, 1.0), ("log", 10.6, 11.32, 1.0),
        ("int", 1.0, 1.8, 1.0), ("int", 10.0, 12.52, 1.5)]

args, chains = ["ffmpeg", "-v", "error", "-y"], []
for k, (name, a, b, sp) in enumerate(SEGS):
    f, (x, y, w, h) = CROP[name]
    args += ["-i", str(SRC / f)]
    chains.append(f"[{k}:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{sp},crop={w}:{h}:{x}:{y},scale=1280:720,setsar=1,fps=30,"
                  f"eq=contrast=1.06:saturation=1.08[v{k}]")
fx = ";".join(chains) + ";" + "".join(f"[v{k}]" for k in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
subprocess.run(args + ["-filter_complex", fx, "-map", "[out]", "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                       "-pix_fmt", "yuv420p", str(OUT / "screen.mp4")], check=True)

for name, t in (("watch", 9.6), ("log", 0.6), ("int", 2.0)):
    f, (x, y, w, h) = CROP[name]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(SRC / f), "-frames:v", "1", "-vf",
                    f"crop={w}:{h}:{x}:{y},scale=640:360,eq=contrast=1.06:saturation=1.08", "-q:v", "3",
                    str(OUT / f"still_{name}.jpg")], check=True)
print("ok")
