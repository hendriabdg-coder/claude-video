# cover.png (1080x1920) in STORY MOTION look: cream + mood blobs, mono kicker, hook title with a lime-highlighted serif
# accent, the demo watch in a browser card, chibi (mikir), watermark. No series label (creator's decision).
#   python cover.py
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
PUB = HERE / "public"
POSE = HERE.parents[2] / "karakter" / "pose_fix"
W, H = 1080, 1920
img = Image.new("RGB", (W, H), "#F2ECE3")
blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(blob)
for c, x, y, s in [("#FFC9A0", 100, 240, 640), ("#A9CFFF", 600, 760, 560), ("#D5B8FF", 160, 1300, 640)]:
    bd.ellipse([x, y, x + s, y + s], fill=c + "B0")
img = Image.alpha_composite(img.convert("RGBA"), blob.filter(ImageFilter.GaussianBlur(110))).convert("RGB")
d = ImageDraw.Draw(img)
F = PUB / "fonts"
black = ImageFont.truetype(str(F / "InterDisplay-Black.ttf"), 100)
serif = ImageFont.truetype(str(F / "SerifBI.ttf"), 116)
mono = ImageFont.truetype(str(F / "Mono.ttf"), 30)


def center(text, y, font, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)
    return (W - w) / 2, w


center("// edukasi + website 3D", 280, mono, (24, 22, 26, 160))
center("Kenapa pembeli", 340, black, "#18161A")
x, w = (W - d.textlength("batal checkout?", font=serif)) / 2, d.textlength("batal checkout?", font=serif)
d.rounded_rectangle([x - 10, 505, x + w + 10, 560], 10, fill="#C6F432")
d.text((x, 440), "batal checkout?", font=serif, fill="#18161A")

shot = Image.open(PUB / "assets" / "still_watch.jpg").convert("RGBA").resize((800, 450))
card = Image.new("RGBA", (800, 500), "#FFFDFB")
cd = ImageDraw.Draw(card)
cd.rectangle([0, 0, 800, 50], fill="#ECE6DE")
for k in range(3):
    cd.ellipse([22 + 28 * k, 17, 38 + 28 * k, 33], fill="#D5CCC2")
card.paste(shot, (0, 50))
mask = Image.new("L", card.size, 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, 799, 499], 26, fill=255)
card.putalpha(mask)
card = card.rotate(-3, expand=True, resample=Image.BICUBIC)
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle([150, 700, 930, 1200], 30, fill=(60, 40, 30, 70))
img = Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(30)))
img.paste(card, (130, 640), card)
d = ImageDraw.Draw(img)
b3 = ImageFont.truetype(str(F / "InterDisplay-Black.ttf"), 52)
tg = ImageFont.truetype(str(F / "Mono.ttf"), 20)
d.rounded_rectangle([150, 1150, 470, 1186], 16, fill=(255, 255, 255, 230))
d.text((166, 1155), "DEMO KARYA · MEREK FIKTIF", font=tg, fill="#18161A")
d.rounded_rectangle([860, 600, 960, 700], 18, fill="#18161A")
d.text((910 - d.textlength("3D", font=b3) / 2, 618), "3D", font=b3, fill="#FFFFFF")

chibi = Image.open(POSE / "pose_3_mikir.png").convert("RGBA")
ch = chibi.resize((int(chibi.width * 600 / chibi.height), 600))
img.paste(ch, ((W - ch.width) // 2, 1190), ch)
wm1 = ImageFont.truetype(str(F / "InterDisplay-Black.ttf"), 30)
wm2 = ImageFont.truetype(str(F / "SerifBI.ttf"), 30)
a, b = d.textlength("Endrich", font=wm1), d.textlength("Tech", font=wm2)
d.rounded_rectangle([(W - a - b) / 2 - 16, 1500, (W + a + b) / 2 + 16, 1552], 22, fill=(238, 235, 228))
d.text(((W - a - b) / 2, 1508), "Endrich", font=wm1, fill="#18161A")
d.text(((W - a - b) / 2 + a, 1508), "Tech", font=wm2, fill="#18161A")
img.convert("RGB").save(HERE / "cover.png")
print("ok", HERE / "cover.png")
