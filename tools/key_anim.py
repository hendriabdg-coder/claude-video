# Character animation clips (karakter/Animasi Karakter/*.mp4, green screen, 720x1280, 24 fps, 4 s) -> transparent
# VP9 WebM for HyperFrames: key out the green, and fix the shirt print typo "EndichTech" -> "EndrichTech" on every
# frame (word blob found per frame, box smoothed over neighbours so the redrawn text doesn't jitter).
#   python tools/key_anim.py Berfikir Terkejut ...      -> karakter/anim_alpha/<name>.webm (+ <name>_check.png)
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "karakter" / "Animasi Karakter"
OUT = ROOT / "karakter" / "anim_alpha"
FONT = ROOT / "motion" / "gaya" / "gaya-terminal" / "public" / "fonts" / "InterDisplay-SemiBold.ttf"
W, H = 720, 1280
OUT.mkdir(exist_ok=True)


def key(rgb):
    r, g, b = (rgb[..., i].astype(int) for i in range(3))
    dom = g - np.maximum(r, b)
    alpha = np.clip(1.0 - (dom - 30) / 60.0, 0, 1)
    g2 = np.where(dom > 0, np.maximum(r, b) + np.clip(dom, 0, 10), g)
    out = np.dstack([r, g2, b]).clip(0, 255).astype(np.uint8)
    return out, (alpha * 255).astype(np.uint8)


def find_word(rgb, a):
    lo, hi = rgb.min(-1).astype(int), rgb.max(-1).astype(int)
    m = ((lo > 150) & (hi - lo < 50) & (a > 250)).astype(np.uint8)
    m[:int(H * 0.30)] = 0; m[int(H * 0.55):] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(m, np.ones((3, 7), np.uint8)))
    best = None
    for k in range(1, n):
        if st[k, 4] < 150 or st[k, 2] > 130:
            continue
        ys, xs = np.nonzero((lab == k) & (m > 0))
        (cx, cy), (w, h), ang = cv2.minAreaRect(np.column_stack([xs, ys]).astype(np.float32))
        if w < h:
            w, h, ang = h, w, ang - 90
        # rotated-rect aspect: the print tilts with the body, so the axis-aligned bbox gets too tall
        if not (35 <= w <= 120 and w > 2.5 * max(h, 1) and abs((ang + 90) % 180 - 90) < 35):
            continue
        if best is None or len(xs) > best[5]:
            best = [cx, cy, w, (ang + 90) % 180 - 90, (lab == k).astype(np.uint8), len(xs)]
    return best[:5] if best else None


def word_img(w, ang):
    font = ImageFont.truetype(str(FONT), 200)
    x0, y0, x1, y1 = font.getbbox("EndrichTech")
    t = Image.new("L", (x1 - x0 + 40, y1 - y0 + 40), 0)
    ImageDraw.Draw(t).text((20 - x0, 20 - y0), "EndrichTech", font=font, fill=255)
    tw = max(int(w * 1.06), 4); th = max(int(t.height * tw / t.width), 1)
    return t.resize((tw, th), Image.LANCZOS).rotate(-ang, expand=True, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.4))


def process(name):
    src = SRC / f"{name}.mp4"
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(src), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    keyed = [key(f) for f in frames]
    found = [find_word(rgb, a) for rgb, a in keyed]
    # smooth the word box (median of neighbours) so the redrawn print stays steady
    idx = [i for i, f in enumerate(found) if f]
    out_dir = OUT / f"_{name}"; out_dir.mkdir(exist_ok=True)
    for i, (rgb, a) in enumerate(keyed):
        img = rgb.copy()
        if idx:
            near = [found[j] for j in idx if abs(j - i) <= 2] or [found[min(idx, key=lambda j: abs(j - i))]]
            cx, cy, w, ang = (float(np.median([f[k] for f in near])) for k in range(4))
            if found[i]:
                hole = cv2.dilate(found[i][4] * 255, np.ones((5, 5), np.uint8))
                img = cv2.inpaint(np.ascontiguousarray(img), hole, 4, cv2.INPAINT_TELEA)
                pil = Image.fromarray(np.dstack([img, a]))
                t = word_img(w, ang)
                col = Image.new("RGBA", t.size, (232, 232, 230, 255)); col.putalpha(t)
                pil.alpha_composite(col, (int(cx - t.width / 2), int(cy - t.height / 2)))
                Image.fromarray(np.array(pil)).save(out_dir / f"{i:03d}.png")
                continue
        Image.fromarray(np.dstack([img, a])).save(out_dir / f"{i:03d}.png")
    webm = OUT / f"{name}.webm"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "24", "-i", str(out_dir / "%03d.png"), "-c:v", "libvpx-vp9",
                    "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "28", "-auto-alt-ref", "0", "-an", str(webm)], check=True)
    # check sheet: 4 frames on dark bg + shirt zoom
    sheet = Image.new("RGB", (4 * 240 + 400, 427), (24, 20, 30))
    for k, i in enumerate((0, 30, 60, 90)):
        fr = Image.open(out_dir / f"{min(i, len(frames) - 1):03d}.png"); im = fr.copy(); im.thumbnail((240, 427))
        sheet.paste(im, (k * 240, 0), im)
    if idx:
        f = found[idx[len(idx) // 2]]; fr = Image.open(out_dir / f"{idx[len(idx) // 2]:03d}.png")
        c = fr.crop((int(f[0]) - 60, int(f[1]) - 25, int(f[0]) + 60, int(f[1]) + 25)).resize((400, 166))
        sheet.paste(c, (960, 120), c)
    sheet.save(OUT / f"{name}_check.png")
    print(name, len(frames), "frames, word found in", len(idx), "->", webm)


for n in sys.argv[1:]:
    process(n)
