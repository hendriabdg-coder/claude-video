# Crop screenshot sheet: buang toolbar/bar rumus/sel terseleksi & foto profil (img11), upscale 1.5x (Lanczos) supaya tidak pecah di 9:16.
from pathlib import Path
from PIL import Image, ImageFilter
HERE = Path(__file__).resolve().parent
C = {  # nama: (file, (x0, y0, x1, y1))
    "dash": ("img01.jpg", (52, 212, 1112, 900)),
    "dash_kpi": ("img01.jpg", (52, 330, 1112, 470)),
    "dash_beli": ("img01.jpg", (770, 810, 1112, 900)),
    "rincian": ("img03.jpg", (52, 165, 960, 900)),
    "jual": ("img04.jpg", (40, 160, 1055, 900)),
    "kas": ("img05.jpg", (40, 170, 910, 780)),
    "belanja": ("img06.jpg", (40, 160, 1010, 900)),
    "stok": ("img07.jpg", (40, 160, 1360, 600)),
    "menu": ("img08.jpg", (40, 165, 1155, 450)),
    "resep": ("img09.jpg", (40, 165, 950, 860)),
    "labarugi": ("img10.jpg", (40, 160, 1600, 705)),
    "atur": ("img11.jpg", (0, 100, 700, 760)),
}
for name, (f, box) in C.items():
    im = Image.open(HERE / "aset" / f).convert("RGB").crop(box)
    im = im.resize((round(im.width * 1.5), round(im.height * 1.5)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
    im.save(HERE / "shots" / f"{name}.png")
    print(name, im.size)

# komposit agar kolom penting terbaca di 9:16: label + kolom Sep/Okt/Nov (Laba Rugi), nama bahan + stok akhir/status (Stok)
def comp(f, y, cols, scale, out):
    src = Image.open(HERE / "aset" / f).convert("RGB")
    parts = [src.crop((x0, y[0], x1, y[1])) for x0, x1 in cols]
    w = sum(p.width for p in parts); im = Image.new("RGB", (w, parts[0].height), "white"); x = 0
    for p in parts: im.paste(p, (x, 0)); x += p.width
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
    im.save(HERE / "shots" / out); print(out, im.size)
comp("img10.jpg", (236, 700), [(44, 312), (1093, 1385)], 1.7, "labarugi2.png")
comp("img07.jpg", (240, 588), [(44, 292), (893, 1055)], 2.0, "stok2.png")
