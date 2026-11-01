# QA sheets for a finished edit.
#   python qa.py "<final.mp4>" <outdir> [band_top band_height]
# Writes final_sheet_N.jpg (1 fps, timestamped, 24 per sheet) and band_sheet.jpg (the caption band of every second
# stacked, to spot text that stays on screen too long or overlaps). Default band = 1000..1500 px.
import os, subprocess, sys
from PIL import Image, ImageDraw

video, out = sys.argv[1], sys.argv[2]
top = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
bh = int(sys.argv[4]) if len(sys.argv) > 4 else 500
os.makedirs(out, exist_ok=True)
tmp = os.path.join(out, "_qa")
os.makedirs(tmp, exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", "fps=1", os.path.join(tmp, "q%04d.png")], check=True)
fr = sorted(f for f in os.listdir(tmp) if f.startswith("q"))
per = 24
for s in range(0, len(fr), per):
    chunk = fr[s:s + per]
    sheet = Image.new("RGB", (270 * 6, 480 * ((len(chunk) + 5) // 6)), "black")
    d = ImageDraw.Draw(sheet)
    for k, f in enumerate(chunk):
        x, y = (k % 6) * 270, (k // 6) * 480
        sheet.paste(Image.open(os.path.join(tmp, f)).resize((270, 480)), (x, y))
        d.rectangle([x, y, x + 46, y + 22], fill="black")
        d.text((x + 4, y + 4), f"{s + k}s", fill="yellow")
    sheet.save(os.path.join(out, f"final_sheet_{s // per + 1}.jpg"), quality=85)
cols = 3
rows = (len(fr) + cols - 1) // cols
bw, bhs = 540, bh // 2
band = Image.new("RGB", (bw * cols, bhs * rows), "black")
d = ImageDraw.Draw(band)
for k, f in enumerate(fr):
    im = Image.open(os.path.join(tmp, f)).crop((0, top, 1080, top + bh)).resize((bw, bhs))
    x, y = (k % cols) * bw, (k // cols) * bhs
    band.paste(im, (x, y))
    d.text((x + 4, y + 4), f"{k}s", fill="yellow")
band.save(os.path.join(out, "band_sheet.jpg"), quality=85)
print("sheets in", out, "|", len(fr), "seconds")
