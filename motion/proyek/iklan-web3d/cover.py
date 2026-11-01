# cover.png (1080x1920): hook title in the top third, three demo stills, chibi (kaget), label.  python cover.py
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
PUB = HERE / "public"
W, H = 1080, 1920
img = Image.new("RGB", (W, H), "#F4EBE1")
blob = Image.new("RGBA", (W, H), (244, 235, 225, 0))
bd = ImageDraw.Draw(blob)
for c, x, y, s in [("#FFB48A", 120, 260, 620), ("#FF8C6B", 620, 900, 560), ("#D5B8FF", 160, 1300, 640)]:
    bd.ellipse([x, y, x + s, y + s], fill=c + "C0")
img = Image.alpha_composite(img.convert("RGBA"), blob.filter(ImageFilter.GaussianBlur(110))).convert("RGB")
d = ImageDraw.Draw(img)
black = ImageFont.truetype(str(PUB / "fonts" / "InterDisplay-Black.ttf"), 92)
serif = ImageFont.truetype(str(PUB / "fonts" / "SerifBI.ttf"), 112)
semi = ImageFont.truetype(str(PUB / "fonts" / "InterDisplay-SemiBold.ttf"), 30)


def center(text, y, font, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)


label = "IKLAN · JASA WEBSITE 3D"
lw = d.textlength(label, font=semi)
d.rounded_rectangle([(W - lw) / 2 - 22, 268, (W + lw) / 2 + 22, 320], 12, fill="#E2582B")
center(label, 276, semi, "#FFF6EE")
center("Website kamu", 350, black, "#1E1B18")
center("cuma jadi", 452, black, "#1E1B18")
center("brosur online?", 552, serif, "#E2582B")

for k, (name, x, y, rot) in enumerate([("watch", 40, 760, 7), ("log", 320, 720, 0), ("int", 600, 760, -7)]):
    s = Image.open(PUB / "assets" / f"still_{name}.jpg").convert("RGBA").resize((440, 248))
    card = Image.new("RGBA", (440, 278), "#FFFDFB")
    card.paste(s, (0, 30))
    mask = Image.new("L", card.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 439, 277], 20, fill=255)
    card.putalpha(mask)
    card = card.rotate(rot, expand=True, resample=Image.BICUBIC)
    img.paste(card, (x, y), card)

chibi = Image.open(PUB / "pose" / "pose_4_kaget.png").convert("RGBA")
ch = chibi.resize((int(chibi.width * 560 / chibi.height), 560))
img.paste(ch, ((W - ch.width) // 2, 925), ch)
wm1 = ImageFont.truetype(str(PUB / "fonts" / "InterDisplay-Black.ttf"), 30)
wm2 = ImageFont.truetype(str(PUB / "fonts" / "SerifBI.ttf"), 30)
a, b = d.textlength("Endrich", font=wm1), d.textlength("Tech", font=wm2)
d.text(((W - a - b) / 2, 1508), "Endrich", font=wm1, fill="#1E1B18")
d.text(((W - a - b) / 2 + a, 1508), "Tech", font=wm2, fill="#E2582B")
img.save(HERE / "cover.png")
print("ok")
