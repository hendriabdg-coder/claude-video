# Look at a take before planning: probe, camera-cut detection, 1 fps contact sheets and a gridded frame per shot.
#   python look.py "<video>" <outdir>
# Writes <outdir>/sheet_N.jpg (1 fps, timestamped), <outdir>/grid_shotK.jpg (1080x1920 with a 60 px grid and
# y labels every 120 px, used to measure eyes-y / head-top-y / chest band) and <outdir>/look.json:
# {width, height, fps, duration, cuts:[frame,...], shots:[{start_s, end_s, grid}]}.
import json, os, subprocess, sys
from PIL import Image, ImageDraw

video, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)

def probe():
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate:format=duration", "-of", "json", video], capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    st = j["streams"][0]
    num, den = st["r_frame_rate"].split("/")
    return st["width"], st["height"], float(num) / float(den), float(j["format"]["duration"])

W, H, FPS, DUR = probe()

# camera cuts / framing changes: 0.08 catches jump-cut reframes that 0.3 misses
r = subprocess.run(["ffmpeg", "-v", "info", "-i", video, "-vf", "fps=30,select='gt(scene,0.08)',showinfo", "-an", "-f", "null", "-"],
                   capture_output=True, text=True)
cuts = sorted({round(float(l.split("pts_time:")[1].split()[0]) * 30) for l in r.stderr.splitlines() if "pts_time:" in l})
cuts = [c for c in cuts if c > 3]

# 1 fps contact sheets, 24 frames per sheet
tmp = os.path.join(out, "_frames")
os.makedirs(tmp, exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", "fps=1,scale=270:-2", os.path.join(tmp, "f%04d.jpg")], check=True)
frames = sorted(os.listdir(tmp))
per = 24
for s in range(0, len(frames), per):
    chunk = frames[s:s + per]
    im0 = Image.open(os.path.join(tmp, chunk[0]))
    fw, fh = im0.size
    sheet = Image.new("RGB", (fw * 6, fh * ((len(chunk) + 5) // 6)), "black")
    d = ImageDraw.Draw(sheet)
    for k, f in enumerate(chunk):
        x, y = (k % 6) * fw, (k // 6) * fh
        sheet.paste(Image.open(os.path.join(tmp, f)), (x, y))
        d.rectangle([x, y, x + 46, y + 22], fill="black")
        d.text((x + 4, y + 4), f"{s + k}s", fill="yellow")
    sheet.save(os.path.join(out, f"sheet_{s // per + 1}.jpg"), quality=85)

# gridded mid-frame per shot (scaled to a 1080x1920 canvas when the source is 9:16)
bounds = [0] + cuts + [int(DUR * 30)]
shots = []
for k in range(len(bounds) - 1):
    a, b = bounds[k] / 30, bounds[k + 1] / 30
    t = (a + b) / 2
    g = os.path.join(out, f"grid_shot{k}.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2", g], check=True)
    im = Image.open(g).convert("RGB")
    d = ImageDraw.Draw(im)
    for y in range(0, 1920, 60):
        d.line([(0, y), (1080, y)], fill=(255, 255, 0) if y % 120 == 0 else (90, 90, 0), width=1)
        if y % 120 == 0:
            d.text((6, y + 2), str(y), fill="yellow")
    for x in range(0, 1080, 60):
        d.line([(x, 0), (x, 1920)], fill=(90, 90, 0), width=1)
    im.save(g, quality=85)
    shots.append({"start_s": round(a, 3), "end_s": round(b, 3), "grid": g})

json.dump({"width": W, "height": H, "fps": FPS, "duration": DUR, "cuts": cuts, "shots": shots},
          open(os.path.join(out, "look.json"), "w"), indent=1)
print(f"{W}x{H} @ {FPS:.2f} fps, {DUR:.2f}s, aspect {'9:16' if abs(W / H - 9 / 16) < 0.01 else f'{W / H:.3f}'}")
print("cuts (frames @30fps):", cuts)
for s in shots:
    print(f"shot {s['start_s']:6.2f}-{s['end_s']:6.2f}  {s['grid']}")
