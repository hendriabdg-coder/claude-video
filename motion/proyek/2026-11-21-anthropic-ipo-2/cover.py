# cover.png: latar gelap + grafik hari pertama (dari render, detik 43) digelapkan, label, judul 3 baris, chibi kaget.
# Judul di dalam crop grid IG 3:4 (y 240-1680).  python cover.py
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FONTS = ROOT / "motion" / "gaya" / "gaya-terminal" / "public" / "fonts"
frame = HERE / "renders" / "_cover_bg.png"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "26", "-i", str(HERE / "renders" / "visual.mp4"), "-frames:v", "1", str(frame)], check=True)
bg = Image.open(frame).convert("RGB").crop((60, 560, 1060, 1250)).resize((1180, 814), Image.LANCZOS)
im = Image.new("RGB", (1080, 1920), (11, 11, 13))
im.paste(ImageEnhance.Brightness(bg).enhance(0.35), (-60, 830))


def font(px, name="InterDisplay-Black.ttf"):
    return ImageFont.truetype(str(FONTS / name), px)


def fit(text, px, maxw):
    while font(px).getlength(text) > maxw:
        px -= 2
    return px


d = ImageDraw.Draw(im)
d.text((540, 262), "EndrichTech", font=font(36), fill=(244, 241, 234), anchor="mt")
lab = "BERITA AI · IPO #2"
lf = font(36, "InterDisplay-Bold.ttf")
lw = d.textlength(lab, font=lf)
d.rounded_rectangle((540 - lw / 2 - 24, 340, 540 + lw / 2 + 24, 400), radius=12, fill=(255, 79, 58))
d.text((540, 370), lab, font=lf, fill=(244, 241, 234), anchor="mm")
y = 440
for line, col in (("ANTHROPIC IPO:", (244, 241, 234)), ("APA ARTINYA", (244, 241, 234)), ("BUAT KITA?", (255, 106, 61))):
    f = font(fit(line, 150, 940))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((540, y + 6), line, font=f, fill=(0, 0, 0, 230), anchor="mt")
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    im.paste(sh, (0, 0), sh)
    d = ImageDraw.Draw(im)
    d.text((540, y), line, font=f, fill=col, anchor="mt")
    y += int(f.size * 1.08)
pf = font(64)
d.rounded_rectangle((90, y + 30, 640, y + 130), radius=20, fill=(244, 241, 234))
d.text((365, y + 80), "3 HAL PENTING", font=pf, fill=(11, 11, 13), anchor="mm")
ch = Image.open(ROOT / "karakter" / "pose_fix" / "pose_3_mikir.png").convert("RGBA")
ch = ch.resize((int(ch.width * 0.55), int(ch.height * 0.55)), Image.LANCZOS)
im.paste(ch, (540 - ch.width // 2 + 230, 1680 - int(ch.height * 0.95)), ch)
out = ROOT / "output" / "motion" / HERE.name / "cover.png"
im.save(out)
frame.unlink()
print(out)
