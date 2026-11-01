# SFX + music for the STORY MOTION preview, with the reel mixer (motion/gaya/reel_sfx.py): Epidemic cues on the VO word
# timeline, music gain measured so the ducked bed sits ~13.5 dB under the voice, -14 LUFS / TP -1.5.
#   python sfx.py   (renders/visual.mp4 + public/music.mp3 -> renders/final.mp4)
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from reel_sfx import mix  # noqa: E402

VO = json.loads((HERE.parents[2] / "motion" / "panduan-gaya" / "_vo" / "story" / "scene_01.json").read_text(encoding="utf-8"))
T = {i: w["start"] + 0.3 for i, w in enumerate(VO["words"])}
A = [0, T[5] - 0.12, T[13] - 0.12, T[29] - 0.12, T[42] - 0.12]
B5, B6 = T[51] - 0.12, T[57] - 0.12
END = max(VO["words"][-1]["end"] + 0.3 + 0.5, B6 + 3.2)

C = [(0.0, "hit_thump", -10, 1.0, "onset"), (0.1, "wh_fly", -13, 1.0, "peak"), (T[1], "pop", -12, 0.25, "onset"),
     (T[1] + 0.05, "wh_swish", -15, 0.5, "peak"),
     # bab 2: the shop goes grey, visitors leave
     (A[1], "wh_soft", -14, 0.9, "peak"), (T[8], "neg", -14, 0.8, "onset")]
C += [(T[10] + 0.2 * k, "tap", -15, None, "onset") for k in range(3)]
C += [(T[12], "wh_fast", -15, 0.4, "peak"),
      # bab 3: the fact
      (A[2], "wh_swish", -13, 0.5, "peak"), (T[14], "ui_popup", -14, 0.6, "onset"), (T[20], "tick", -15, T[24] - T[20], "onset"),
      (T[24], "pop", -11, 0.25, "onset"), (T[27], "hit_deep", -9, 1.2, "onset"),
      # turning point: halftone wipe -> 3D site
      (A[3] - 0.35, "wh_cine", -11, 1.2, "peak"), (A[3] + 0.2, "hit_thump", -11, 1.0, "onset"), (A[3] + 0.3, "shimmer", -15, 1.4, "onset"),
      (T[36], "click_dbl", -13, None, "onset"), (T[36] + 0.1, "wh_swish", -14, 0.9, "peak"), (T[37], "ui_popup", -14, 0.6, "onset"),
      (T[38], "wh_soft", -13, 1.0, "peak"),
      # bab 5: offer, follow, A/B
      (A[4], "wh_fast", -12, 0.4, "peak"), (T[48], "hit_washed", -11, 1.0, "onset"), (B5, "wh_swish", -14, 0.5, "peak"),
      (T[52] + 0.6, "click_metal", -11, None, "onset"), (T[52] + 0.62, "ui_confirm", -13, None, "onset"),
      (B6, "wh_soft", -14, 0.9, "peak"), (T[63] - 0.1, "pop", -12, 0.25, "onset"), (T[64], "bubble", -14, 0.6, "onset"),
      (T[65] - 0.1, "pop", -12, 0.25, "onset"),
      (END, "wh_cine", -11, 1.2, "peak"), (END + 0.3, "shimmer", -15, 1.6, "onset")]

mix("gaya-story", C)
