# STORY MOTION compositor: keys the animated chibi clips (chibi_track.make_track) and lays them over the HyperFrames
# render with SEVERAL placement windows (big at the hook -> narrator in the corner -> CTA size). Each window has its
# own copy of the track: the narrator rises in from below at t0 and drops out at t1, so a size change reads as a pop
# to a new spot instead of a jump. Watermark (chibi_track.watermark) goes on top until wm_until.
#   python compose.py   (uses public/char_track.json + renders/graphics.mp4 -> renders/visual.mp4)
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from chibi_track import make_track, run, watermark  # noqa: E402

spec = json.loads((HERE / "public" / "char_track.json").read_text(encoding="utf-8"))
trk = make_track([tuple(s) for s in spec["segments"]], spec["dur"], HERE / "renders" / "char_track.mov")
wm = watermark(HERE / "renders" / "wm.png")
places = spec["places"]
n = len(places)
fx = f"[1:v]setpts=PTS-STARTPTS,split={n}" + "".join(f"[t{k}]" for k in range(n)) + ";"
prev = "0:v"
for k, p in enumerate(places):
    w, h = round(720 * p["scale"]), round(1280 * p["scale"])
    t0, t1 = p["t0"], p["t1"]
    rise = f"1000*pow(max(0\\,1-(t-{t0})/0.45)\\,3)"
    drop = f"1100*pow(max(0\\,(t-{t1 - 0.28})/0.28)\\,2)" if t1 < spec["dur"] - 0.01 else "0"
    fx += (f"[t{k}]scale={w}:{h}:flags=lanczos[c{k}];"
           f"[{prev}][c{k}]overlay=x={p['cx'] - w // 2}:y='{p['top']}+{rise}+{drop}':eval=frame:"
           f"enable='between(t\\,{t0}\\,{t1})'[v{k}];")
    prev = f"v{k}"
fx += f"[{prev}][2:v]overlay=0:0:enable='lt(t\\,{spec['wm_until']})',format=yuv420p[v]"
out = HERE / "renders" / "visual.mp4"
run(["-i", str(HERE / "renders" / "graphics.mp4"), "-i", str(trk), "-loop", "1", "-i", str(wm), "-filter_complex", fx,
     "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "copy", "-shortest",
     "-movflags", "+faststart", str(out)])
print("ok ->", out)
