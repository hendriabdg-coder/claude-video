# cover.png: frame teks partikel "AKU BUKAN PROGRAMMER" (detik 21,8) + label lagu + chip vokal AI.  python cover.py
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
F = ROOT / "motion" / "gaya" / "gaya-terminal" / "public" / "fonts"
tmp = HERE / "renders" / "_c.png"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "21.8", "-i", str(HERE / "renders" / "visual.mp4"), "-frames:v", "1", str(tmp)], check=True)
im = Image.open(tmp).convert("RGB"); d = ImageDraw.Draw(im)
f = lambda px, n="InterDisplay-Black.ttf": ImageFont.truetype(str(F / n), px)
d.rectangle((0, 1440, 1080, 1520), fill=(11, 11, 12))
lab = "♪ LAGU · ENDRICHTECH"
w = d.textlength(lab, font=f(40, "InterDisplay-Bold.ttf"))
d.rounded_rectangle((540 - w / 2 - 26, 420, 540 + w / 2 + 26, 490), radius=14, fill=(242, 153, 74))
d.text((540, 455), lab, font=f(40, "InterDisplay-Bold.ttf"), fill=(11, 11, 12), anchor="mm")
d.text((540, 1180), "tapi lihat yang aku bikin", font=f(64, "InterDisplay-SemiBoldItalic.ttf"), fill=(242, 153, 74), anchor="mm")
d.text((540, 1290), "vokal: AI (Eleven Music)", font=f(32, "InterDisplay-Bold.ttf"), fill=(107, 111, 120), anchor="mm")
out = ROOT / "output" / "motion" / HERE.name / "cover.png"; im.save(out); tmp.unlink(); print(out)
