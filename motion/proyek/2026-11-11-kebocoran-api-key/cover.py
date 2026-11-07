# cover.png: frame 3D kunci API dari render (detik 1.4, area tanpa teks layar) digelapkan, label seri, judul 3 baris, chibi kaget.
# Judul di dalam crop grid IG 3:4 (y 240-1680).  python cover.py
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FONTS = ROOT / "motion" / "gaya" / "gaya-terminal" / "public" / "fonts"
frame = HERE / "renders" / "_cover_bg.png"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1.4", "-i", str(HERE / "renders" / "visual.mp4"), "-frames:v", "1", str(frame)], check=True)
bg = Image.open(frame).convert("RGB")
# hide the in-video counter: crop the swarm region and scale it up as the backdrop
bg = bg.crop((0, 600, 1080, 1440)).resize((1250, 972), Image.LANCZOS)
im = Image.new("RGB", (1080, 1920), (14, 14, 14))
im.paste(ImageEnhance.Brightness(bg).enhance(0.55), (-85, 640))


def font(px, name="InterDisplay-Black.ttf"):
    return ImageFont.truetype(str(FONTS / name), px)


def fit(text, px, maxw):
    while font(px).getlength(text) > maxw:
        px -= 2
    return px


d = ImageDraw.Draw(im)
d.text((540, 262), "EndrichTech", font=font(36), fill=(244, 241, 234), anchor="mt")
lab = "KEAMANAN AI"
lf = font(36, "InterDisplay-Bold.ttf")
lw = d.textlength(lab, font=lf)
d.rounded_rectangle((540 - lw / 2 - 24, 340, 540 + lw / 2 + 24, 400), radius=12, fill=(255, 79, 58))
d.text((540, 370), lab, font=lf, fill=(244, 241, 234), anchor="mm")
y = 440
for line, col in (("3 KESALAHAN", (244, 241, 234)), ("BIKIN API KEY", (255, 79, 58)), ("KAMU BOCOR", (255, 79, 58))):
    f = font(fit(line, 140, 940))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((540, y + 6), line, font=f, fill=(0, 0, 0, 230), anchor="mt")
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    im.paste(sh, (0, 0), sh)
    d = ImageDraw.Draw(im)
    d.text((540, y), line, font=f, fill=col, anchor="mt")
    y += int(f.size * 1.08)
ch = Image.open(ROOT / "karakter" / "pose_fix" / "pose_4_kaget.png").convert("RGBA")
ch = ch.resize((int(ch.width * 0.55), int(ch.height * 0.55)), Image.LANCZOS)
im.paste(ch, (540 - ch.width // 2 + 220, 1680 - int(ch.height * 0.95)), ch)
out = ROOT / "output" / "motion" / HERE.name / "cover.png"
im.save(out)
frame.unlink()
print(out)
