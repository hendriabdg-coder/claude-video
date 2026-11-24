# cover.png: foto Jensen (aset Endrich) digelapkan + judul pergi/kembali + chibi kaget.
# Judul di dalam crop grid IG 3:4 (y 240-1680).  python cover.py
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FONTS = ROOT / "motion" / "gaya" / "gaya-terminal" / "public" / "fonts"
frame = None
bg = Image.open(HERE / "aset" / "jensen.webp").convert("RGB").resize((1080, 1080), Image.LANCZOS)
im = Image.new("RGB", (1080, 1920), (7, 9, 10))
im.paste(ImageEnhance.Brightness(bg).enhance(0.5), (0, 700))
fadeg = Image.new("L", (1, 300)); fadeg.putdata([int(255 * (1 - i / 299)) for i in range(300)])
im.paste(Image.new("RGB", (1080, 300), (7, 9, 10)), (0, 700), fadeg.resize((1080, 300)))


def font(px, name="InterDisplay-Black.ttf"):
    return ImageFont.truetype(str(FONTS / name), px)


def fit(text, px, maxw):
    while font(px).getlength(text) > maxw:
        px -= 2
    return px


d = ImageDraw.Draw(im)
d.text((540, 262), "EndrichTech", font=font(36), fill=(244, 241, 234), anchor="mt")
lab = "BERITA AI · NVIDIA"
lf = font(36, "InterDisplay-Bold.ttf")
lw = d.textlength(lab, font=lf)
d.rounded_rectangle((540 - lw / 2 - 24, 340, 540 + lw / 2 + 24, 400), radius=12, fill=(118, 185, 0))
d.text((540, 370), lab, font=lf, fill=(244, 241, 234), anchor="mm")
y = 440
for line, col in (("1 ORANG PERGI,", (244, 241, 234)), ("SAHAM ANJLOK", (255, 79, 58)), ("KEMBALI: +31%", (155, 226, 45))):
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
d.text((365, y + 80), "JENSEN HUANG", font=pf, fill=(7, 9, 10), anchor="mm")
ch = Image.open(ROOT / "karakter" / "pose_fix" / "pose_4_kaget.png").convert("RGBA")
ch = ch.resize((int(ch.width * 0.55), int(ch.height * 0.55)), Image.LANCZOS)
im.paste(ch, (540 - ch.width // 2 + 230, 1680 - int(ch.height * 0.95)), ch)
out = ROOT / "output" / "motion" / HERE.name / "cover.png"
im.save(out)
print(out)
