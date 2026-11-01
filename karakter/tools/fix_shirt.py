# Replace the shirt print typo "EndichTech" with "EndrichTech" on every keyed pose (pose_png -> pose_fix):
# find the white word blob on the chest, inpaint it with the shirt, draw the corrected word at the same angle/size.
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT.parent / "videos" / "gaya-terminal" / "public" / "fonts" / "InterDisplay-SemiBold.ttf"
(ROOT / "pose_fix").mkdir(exist_ok=True)
crops = []
for f in sorted((ROOT / "pose_png").glob("pose_*.png")):
    im = np.array(Image.open(f).convert("RGBA"))
    rgb = im[..., :3].astype(int)
    lo, hi = rgb.min(-1), rgb.max(-1)
    m = ((lo > 165) & (hi - lo < 45) & (im[..., 3] > 250)).astype(np.uint8)
    m[:540] = 0; m[920:] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(m, np.ones((5, 9), np.uint8)))
    best = max((k for k in range(1, n) if 60 <= st[k, 2] <= 160 and st[k, 2] > 2.5 * st[k, 3]),
               key=lambda k: (m[lab == k]).sum())
    word = (lab == best) & (m > 0)
    ys, xs = np.nonzero(word)
    (cx, cy), (w, h), ang = cv2.minAreaRect(np.column_stack([xs, ys]).astype(np.float32))
    if w < h:
        w, h, ang = h, w, ang - 90
    ang = (ang + 90) % 180 - 90
    hole = cv2.dilate((lab == best).astype(np.uint8) * 255, np.ones((5, 5), np.uint8))
    rgb8 = cv2.inpaint(np.ascontiguousarray(im[..., :3]), hole, 6, cv2.INPAINT_TELEA)
    out = Image.fromarray(np.dstack([rgb8, im[..., 3]]))
    # draw corrected word big, then scale/rotate onto the shirt
    font = ImageFont.truetype(str(FONT), 200)
    x0, y0, x1, y1 = font.getbbox("EndrichTech")
    t = Image.new("L", (x1 - x0 + 40, y1 - y0 + 40), 0)
    ImageDraw.Draw(t).text((20 - x0, 20 - y0), "EndrichTech", font=font, fill=255)
    tw = int(w * 1.06); th = max(int(t.height * tw / t.width), 1)
    t = t.resize((tw, th), Image.LANCZOS).rotate(-ang, expand=True, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.5))
    col = Image.new("RGBA", t.size, (232, 232, 230, 255)); col.putalpha(t)
    out.alpha_composite(col, (int(cx - t.width / 2), int(cy - t.height / 2)))
    out.save(ROOT / "pose_fix" / f.name)
    print(f.name, round(cx), round(cy), round(w), round(h), round(ang, 1))
    c = out.crop((int(cx) - 110, int(cy) - 45, int(cx) + 110, int(cy) + 45)); bg = Image.new("RGB", c.size, (40, 40, 40)); bg.paste(c, (0, 0), c)
    crops.append(bg.resize((440, 180)))
sheet = Image.new("RGB", (880, 180 * 4))
for i, c in enumerate(crops):
    sheet.paste(c, ((i % 2) * 440, (i // 2) * 180))
sheet.save(ROOT / "shirt_check.png")
