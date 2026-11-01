# Fast DRAFT subject matte for the BEHIND device: MediaPipe Selfie Segmenter on CPU (~10 fps on this laptop vs
# ~0.5 fps for `hf.sh remove-background`). Writes the same kind of file (ProRes 4444 with alpha), so composite.sh works
# unchanged. Hair/ear edges are softer than remove-background: use it to check placement, then make the final matte
# with remove-background.
#   python matte_fast.py matte/seg1.mp4 matte/m1.mov [--mask-width 540]
# Mask method (guided filter, contrast, temporal blend) after github.com/Vibha-Ramprakash/claude-video-effects (MIT).
import argparse, json, os, subprocess
import numpy as np
import cv2

MODEL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "models", "selfie_segmenter.tflite")

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("dst")
ap.add_argument("--mask-width", type=int, default=540, help="width the segmenter runs at (1080 is 5x slower, no better)")
a = ap.parse_args()

j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                               "-of", "json", a.src], capture_output=True, text=True, check=True).stdout)["streams"][0]
W, H, fr = j["width"], j["height"], j["r_frame_rate"]
num, den = fr.split("/"); fps = float(num) / float(den or 1)
aw = a.mask_width; ah = int(round(aw * H / W / 2)) * 2


def frames(path):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, bufsize=10 ** 8)
    n = W * H * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)
    p.wait()


def guided(I, p, r=8, eps=2e-3):
    box = lambda x: cv2.boxFilter(x, -1, (2 * r + 1, 2 * r + 1))
    mI, mp_ = box(I), box(p)
    A = (box(I * p) - mI * mp_) / (box(I * I) - mI * mI + eps)
    return np.clip(box(A) * I + box(mp_ - A * mI), 0, 1)


import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=MODEL), running_mode=vision.RunningMode.VIDEO,
    output_confidence_masks=True, output_category_mask=False))

enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", fr, "-i", "-",
                        "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", a.dst], stdin=subprocess.PIPE)
prev = None
for i, rgb in enumerate(frames(a.src)):
    small = cv2.resize(rgb, (aw, ah), interpolation=cv2.INTER_AREA)
    m = seg.segment_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(small)), int(i * 1000 / fps))
    m = m.confidence_masks[-1].numpy_view().astype(np.float32).reshape(ah, aw)
    m = guided(cv2.cvtColor(small, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255, m)
    m = np.clip((m - 0.5) * 1.6 + 0.5, 0, 1)
    if prev is not None: m = 0.65 * m + 0.35 * prev  # damp flicker between frames
    prev = m
    alpha = (cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR) * 255 + 0.5).astype(np.uint8)
    enc.stdin.write(np.dstack([rgb, alpha]).tobytes())
enc.stdin.close(); enc.wait()
print(f"wrote {a.dst} ({i + 1} frames, draft matte)")
