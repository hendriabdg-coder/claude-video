"""Cover 1080x1920 untuk kedua iklan: python cover.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = Path(__file__).parent
FD = HERE / "build_keynote" / "public" / "fonts"
F = lambda n, s: ImageFont.truetype(str(FD / f"InterDisplay-{n}.ttf"), s)
V = {"keynote": dict(bg="#F5F5F7", ink="#1D1D1F", sub="#6E6E73", acc="#0071E3"),
     "material": dict(bg="#FFFFFF", ink="#202124", sub="#5F6368", acc="#1A73E8"),
     "meta": dict(bg="#F5F5F7", ink="#1D1D1F", sub="#6E6E73", acc="#0071E3", sub2="Pembukuan beres, tanpa begadang.")}
BRAND = "#B8611D"

def ctext(d, y, t, f, fill):
    w = d.textlength(t, font=f); d.text(((1080 - w) / 2, y), t, font=f, fill=fill)

for v, P in V.items():
    im = Image.new("RGB", (1080, 1920), P["bg"]); d = ImageDraw.Draw(im)
    # chip label
    f = F("Bold", 30); t = "TEMPLAT DASHBOARD UMKM"; w = d.textlength(t, font=f)
    d.rounded_rectangle(((1080 - w) / 2 - 26, 300, (1080 + w) / 2 + 26, 360), 30, fill=BRAND)
    ctext(d, 311, t, f, "#FFFFFF")
    ctext(d, 410, "Masih ngitung nota", F("Black", 92), P["ink"])
    ctext(d, 520, "jam 11 malam?", F("Black", 92), P["acc"])
    ctext(d, 650, P.get("sub2", "Catat 5 menit, laba keisi sendiri."), F("SemiBold", 46), P["sub"])
    # dashboard card with shadow
    sh = Image.open(HERE / "shots" / "dash.png").convert("RGB")
    W = 940; sh = sh.resize((W, int(sh.height * W / sh.width)), Image.LANCZOS)
    H = min(sh.height, 640); sh = sh.crop((0, 0, W, H))
    x, y = 70, 780
    shadow = Image.new("L", (1080, 1920), 0); ImageDraw.Draw(shadow).rounded_rectangle((x, y + 24, x + W, y + H + 24), 28, fill=90)
    shadow = shadow.filter(ImageFilter.GaussianBlur(30))
    im.paste(Image.new("RGB", im.size, "#000000"), (0, 0), shadow)
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, W, H), 24, fill=255)
    im.paste(sh, (x, y), m); d = ImageDraw.Draw(im)
    # KPI pill
    f = F("Black", 54); t = "Rp62.250.000"; w = d.textlength(t, font=f)
    d.rounded_rectangle((540 - w / 2 - 40, 1370, 540 + w / 2 + 40, 1460), 45, fill=P["acc"])
    ctext(d, 1379, t, f, "#FFFFFF")
    f = F("Bold", 20); d.text((60, 1475), "DATA DEMO · KOPI SENJA", font=f, fill=P["sub"])
    f = F("SemiBold", 34); a = "Endrich"; b = "Tech"; wa = d.textlength(a, font=f); wt = wa + d.textlength(b, font=f)
    d.text(((1080 - wt) / 2, 1525), a, font=f, fill=P["ink"]); d.text(((1080 - wt) / 2 + wa, 1525), b, font=f, fill=BRAND)
    im.save(HERE / "renders" / f"cover_{v}.png")
    print("ok", v)
