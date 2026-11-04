# Cover/thumbnail per reel (CLAUDE.md §6): 1080x1920, series label + hook title inside the 3:4 centre crop the IG grid
# shows (y 240-1680), chibi Endrich at the bottom, watermark. Writes output/motion/<slug>/cover.png.
#   python tools/make_covers.py [slug ...]
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "motion" / "gaya" / "gaya-terminal" / "public" / "fonts"
POSE = ROOT / "karakter" / "pose_fix"
COVERS = {
    "2026-10-26-ai-pemburu-celah": dict(bg=(10, 9, 7), glow=(255, 74, 74), label="INTERNET JEBOL #2", lc=(245, 196, 82),
                                        title=["AI PENJAGA", "JAGO NYERANG?"], tc=[(255, 243, 214), (255, 90, 90)], pose="pose_4_kaget"),
    "2026-10-27-chatgpt-intelligent-ui": dict(bg=(18, 19, 20), glow=(198, 244, 50), label="UPDATE AI MINGGU INI #1", lc=(198, 244, 50),
                                              title=["JAWABAN CHATGPT", "BISA DIKLIK"], tc=[(242, 238, 227), (198, 244, 50)], pose="pose_2_tunjuk"),
    "2026-10-28-penipuan-suara-ai": dict(bg=(5, 8, 7), glow=(255, 176, 0), label="INTERNET JEBOL", lc=(57, 255, 136),
                                         title=["Rp80 JUTA HILANG", "SUARA 'TEMAN' PALSU"], tc=[(255, 176, 0), (216, 255, 232)], pose="pose_4_kaget"),
    "2026-11-04-ai-ngelawan-balik": dict(bg=(5, 8, 7), glow=(57, 255, 136), label="AI PENGAWAS #4", lc=(57, 255, 136),
                                         title=["AI NEMU 129.000 CELAH", "SIAPA YANG NAMBAL?"], tc=[(57, 255, 136), (255, 176, 0)], pose="pose_2_tunjuk"),
}


def font(px, name="InterDisplay-Black.ttf"):
    return ImageFont.truetype(str(FONTS / name), px)


def fit(text, px, maxw):
    while font(px).getlength(text) > maxw:
        px -= 2
    return px


for slug, c in COVERS.items():
    if len(sys.argv) > 1 and slug not in sys.argv[1:]:
        continue
    im = Image.new("RGB", (1080, 1920), c["bg"])
    glow = Image.new("RGB", (1080, 1920), c["bg"])
    ImageDraw.Draw(glow).ellipse((140, 700, 940, 1500), fill=tuple(int(v * 0.35) for v in c["glow"]))
    im = Image.blend(im, glow.filter(ImageFilter.GaussianBlur(160)), 0.9)
    d = ImageDraw.Draw(im)
    lf = font(36, "InterDisplay-Bold.ttf")
    lw = d.textlength(c["label"], font=lf)
    d.rounded_rectangle((540 - lw / 2 - 24, 330, 540 + lw / 2 + 24, 390), radius=12, outline=c["lc"], width=3)
    d.text((540, 360), c["label"], font=lf, fill=c["lc"], anchor="mm")
    y = 430
    for line, col in zip(c["title"], c["tc"]):
        f = font(fit(line, 128, 900))
        shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(shadow).text((540, y), line, font=f, fill=col + (200,), anchor="mt")
        im.paste(shadow.filter(ImageFilter.GaussianBlur(18)), (0, 0), shadow.filter(ImageFilter.GaussianBlur(18)))
        d = ImageDraw.Draw(im)
        d.text((540, y), line, font=f, fill=col, anchor="mt")
        y += int(f.size * 1.1)
    ch = Image.open(POSE / f"{c['pose']}.png").convert("RGBA")
    ch = ch.resize((int(ch.width * 0.62), int(ch.height * 0.62)), Image.LANCZOS)
    im.paste(ch, (540 - ch.width // 2 - 20, 1660 - int(ch.height * 0.95)), ch)
    d = ImageDraw.Draw(im)
    bf = font(36)
    d.text((540, 262), "EndrichTech", font=bf, fill=(255, 243, 214), anchor="mt")
    out = ROOT / "output" / "motion" / slug / "cover.png"
    im.save(out)
    print(out)
