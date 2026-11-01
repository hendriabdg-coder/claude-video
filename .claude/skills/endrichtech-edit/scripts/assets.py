# Inventory of the creator's B-roll and logos for one job.
#   python assets.py "<take.mp4>" <outdir>
# Scans D:/Claude Video/talking-head/aset/broll/ + library/logos/ and the per-video folder (recursively):
# "_assets/" next to the take (talking-head/mentah/<slug>/_assets/), else the old "<take name>_assets/".
# Writes <outdir>/assets.json and <outdir>/broll_sheet.jpg (3 frames per clip at 15/50/85%, labelled with the index),
# so clips can be chosen from file name + what they actually show.
import json, os, subprocess, sys
from PIL import Image, ImageDraw

take, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
LIB = os.path.join(ROOT, "library")
BROLL = os.path.join(ROOT, "talking-head", "aset", "broll")
PER = os.path.join(os.path.dirname(os.path.abspath(take)), "_assets")
if not os.path.isdir(PER):
    PER = os.path.splitext(os.path.abspath(take))[0] + "_assets"
VID = (".mp4", ".mov", ".m4v", ".mkv", ".webm")
IMG = (".png", ".svg", ".webp", ".jpg", ".jpeg")

def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                        "-of", "json", p], capture_output=True, text=True)
    try:
        j = json.loads(r.stdout)
        return j["streams"][0]["width"], j["streams"][0]["height"], float(j["format"].get("duration", 0))
    except Exception:
        return None, None, 0.0

def walk(base, exts):
    if not os.path.isdir(base):
        return []
    return sorted(os.path.join(d, f) for d, _, fs in os.walk(base) for f in fs if f.lower().endswith(exts))

broll = []
for scope, base in (("video", PER), ("library", BROLL)):
    for p in walk(base, VID):
        w, h, d = probe(p)
        if not w:
            continue
        broll.append({"id": len(broll), "scope": scope, "file": p.replace("\\", "/"), "name": os.path.basename(p),
                      "w": w, "h": h, "dur": round(d, 2), "orient": "vertical" if h > w else "horizontal",
                      "crop_ok": (h >= 1920 or w >= 3240) if w > h else h >= 1600})
logos = []
for p in walk(os.path.join(LIB, "logos"), IMG) + walk(PER, IMG):
    info = {"file": p.replace("\\", "/"), "name": os.path.basename(p)}
    if not p.lower().endswith(".svg"):
        im = Image.open(p)
        info.update({"w": im.width, "h": im.height, "alpha": im.mode in ("RGBA", "LA") or "transparency" in im.info})
    logos.append(info)

if broll:
    tw, th = 180, 320
    sheet = Image.new("RGB", (tw * 3 * 2, (th + 24) * ((len(broll) + 1) // 2)), "black")
    d = ImageDraw.Draw(sheet)
    for k, c in enumerate(broll):
        x0, y0 = (k % 2) * tw * 3, (k // 2) * (th + 24)
        for j, frac in enumerate((0.15, 0.5, 0.85)):
            fp = os.path.join(out, f"_b{k}_{j}.jpg")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['dur'] * frac:.2f}", "-i", c["file"], "-frames:v", "1",
                            "-vf", f"scale={tw}:{th}:force_original_aspect_ratio=increase,crop={tw}:{th}", fp])
            if os.path.exists(fp):
                sheet.paste(Image.open(fp), (x0 + j * tw, y0 + 24))
        d.text((x0 + 4, y0 + 5), f"#{c['id']} {c['name'][:48]} ({c['dur']}s)", fill="yellow")
    sheet.save(os.path.join(out, "broll_sheet.jpg"), quality=85)

json.dump({"broll": broll, "logos": logos, "per_video_folder": PER.replace("\\", "/")}, open(os.path.join(out, "assets.json"), "w"), indent=1)
print(f"B-roll: {len(broll)} clip(s)  |  logos: {len(logos)}")
for c in broll:
    print(f"  #{c['id']} [{c['scope']}] {c['name']}  {c['w']}x{c['h']} {c['dur']}s {'' if c['crop_ok'] else '(low-res for 9:16 crop)'}")
for l in logos:
    print(f"  logo {l['name']} {l.get('w', '')}x{l.get('h', '')} alpha={l.get('alpha', 'svg')}")
if not broll and not logos:
    print("  (no assets — edit uses graphics + typography + crop variation only, per guidebook §70)")
