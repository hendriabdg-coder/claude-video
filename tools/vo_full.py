# Join tts.py segments into one vo-full.mp3: trim each scene to its spoken words (from scene_NN.json timestamps),
# put a short fixed gap between scenes, and write vo-full.json with the joined word timeline for the build.
#   python tools/vo_full.py output/motion/<slug>/vo [--gap 0.25]
import argparse
import json
import subprocess
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("dir")
ap.add_argument("--gap", type=float, default=0.25)
a = ap.parse_args()
d = Path(a.dir)
scenes = sorted(d.glob("scene_*.json"))
words, parts, lens, t = [], [], [], 0.0
for k, js in enumerate(scenes):
    w = json.loads(js.read_text(encoding="utf-8"))["words"]
    s0, s1 = max(w[0]["start"] - 0.06, 0), w[-1]["end"] + 0.18
    cut = d / f"_cut_{k:02d}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(js.with_suffix(".mp3")), "-ss", f"{s0:.3f}", "-to", f"{s1:.3f}",
                    "-ar", "44100", "-ac", "1", str(cut)], check=True)
    parts.append(cut)
    # use the measured length of the cut (ffmpeg rounds the cut), so the joined word timeline doesn't drift
    n = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(cut)]))
    lens.append(n)
    words += [dict(x, start=round(x["start"] - s0 + t, 3), end=round(x["end"] - s0 + t, 3), scene=k + 1) for x in w]
    t += n + (a.gap if k < len(scenes) - 1 else 0)
inputs, fx = [], []
for k, p in enumerate(parts):
    inputs += ["-i", str(p)]
    # pad by target total length (apad pad_dur is ignored before concat on this ffmpeg build)
    pad = f",apad=whole_dur={lens[k] + a.gap:.3f}" if k < len(parts) - 1 else ""
    fx.append(f"[{k}:a]anull{pad}[a{k}]")
fx.append("".join(f"[a{k}]" for k in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fx), "-map", "[out]",
                "-b:a", "192k", str(d / "vo-full.mp3")], check=True)
for p in parts:
    p.unlink()
(d / "vo-full.json").write_text(json.dumps({"duration": round(t, 3), "words": words}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{d} -> vo-full.mp3 {t:.2f}s, {len(words)} kata")
