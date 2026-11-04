# Cover gaya editorial (gaya hari 3/4): latar krem, label mono, judul Inter + kata aksen Fraunces miring merah,
# chibi setengah badan kanan bawah, kartu watermark @end.rich9. 1080x1920, judul di sepertiga atas (aman crop grid 3:4).
#   python tools/cover_editorial.py <slug>   (isi COVERS di bawah)
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
COVERS = {
    "2026-11-04-ai-ngelawan-balik": dict(label="// seri ai pengawas", part="#4",
                                         lines=[[("AI nemu", 0)], [("129.000 celah", 1)], [("Siapa yang", 0)], [("nambal?", 1)]],
                                         pose="pose_2_tunjuk"),
}
CREAM, INK, RED, GREY, PAPER = (236, 234, 228), (21, 21, 21), (224, 70, 31), (138, 135, 127), (246, 244, 239)


def fonts(slug):
    fd = ROOT / "motion" / "proyek" / slug / "public" / "fonts"
    return (lambda px: ImageFont.truetype(str(fd / "Inter-500.woff2"), px), lambda px: ImageFont.truetype(str(fd / "Fraunces-800-italic.woff2"), px),
            lambda px: ImageFont.truetype(str(fd / "JBMono-400.woff2"), px), lambda px: ImageFont.truetype(str(ROOT / "motion/gaya/gaya-terminal/public/fonts/InterDisplay-Black.ttf"), px))


for slug in sys.argv[1:] or COVERS:
    c = COVERS[slug]
    inter, fra, mono, black = fonts(slug)
    im = Image.new("RGB", (1080, 1920), CREAM)
    d = ImageDraw.Draw(im)
    for y in range(1100, 1920, 14):
        for x in range(500, 1080, 14):
            if (x - 500) + (y - 1100) > 300:
                d.ellipse((x - 1.6, y - 1.6, x + 1.6, y + 1.6), fill=(205, 202, 194))
    d.text((70, 300), c["label"], font=mono(30), fill=GREY)
    d.text((1010, 300), c["part"], font=mono(30), fill=RED, anchor="ra")
    y = 370
    for line in c["lines"]:
        x = 70
        for txt, ac in line:
            f = fra(122) if ac else inter(116)
            d.text((x, y), txt, font=f, fill=RED if ac else INK)
            x += d.textlength(txt + " ", font=f)
        y += 136
    ch = Image.open(ROOT / "karakter" / "pose_fix" / f"{c['pose']}.png").convert("RGBA")
    im.paste(ch, (380, 1180), ch)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((78, 1450, 408, 1562), radius=16, fill=INK)
    d.rounded_rectangle((70, 1442, 400, 1554), radius=16, fill=PAPER, outline=INK, width=3)
    d.rounded_rectangle((88, 1456, 230, 1490), radius=8, fill=RED)
    d.text((159, 1473), "@end.rich9", font=mono(20), fill="white", anchor="mm")
    d.text((88, 1500), "Endrich", font=black(40), fill=INK)
    d.text((88 + d.textlength("Endrich", font=black(40)), 1500), "Tech", font=black(40), fill=RED)
    out = ROOT / "output" / "motion" / slug / "cover.png"
    im.save(out)
    print(out)
