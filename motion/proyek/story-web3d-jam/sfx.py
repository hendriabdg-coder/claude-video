# SFX + music for the reel with the reel mixer (motion/gaya/reel_sfx.py): Epidemic cues on the VO word timeline, music gain
# measured so the ducked bed sits ~13.5 dB under the voice, -14 LUFS / TP -1.5.
#   python sfx.py   (renders/visual.mp4 + public/music.mp3 -> renders/final.mp4)
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
from reel_sfx import mix  # noqa: E402

VO = json.loads((HERE / "vo" / "vo-full.json").read_text(encoding="utf-8"))
T = {i: w["start"] + 0.3 for i, w in enumerate(VO["words"])}
A = [0, T[19] - 0.12, T[28] - 0.12, T[63] - 0.12, T[79] - 0.12]
A2b, B5, B6 = T[54] - 0.12, T[98] - 0.12, T[110] - 0.12

C = [(0.0, "hit_thump", -10, 1.0, "onset"), (0.05, "wh_fly", -13, 1.0, "peak"), (0.4, "tap", -15, None, "onset"),
     (T[6], "hit_washed", -11, 1.0, "onset"), (T[6] + 0.05, "neg", -14, 0.8, "onset"), (T[12], "pop", -12, 0.25, "onset"),
     # bab 2: chats come in
     (A[1], "wh_soft", -14, 0.9, "peak")]
C += [(T[20] + 0.55 * k, "msg", -15, 0.6, "onset") for k in range(3)]
C += [(T[27] - 0.1, "pop", -12, 0.25, "onset"),
      # bab 3: the fact
      (A[2], "wh_swish", -13, 0.5, "peak"), (T[40], "wh_swish", -15, 0.5, "peak"), (T[43] - 0.1, "click_dbl", -14, None, "onset"),
      (T[48], "tick", -16, T[53] - T[48] + 0.2, "onset"), (T[53] + 0.2, "hit_deep", -10, 1.2, "onset"),
      (A2b, "wh_soft", -14, 0.9, "peak"), (T[61], "bubble", -13, 0.6, "onset"),
      # turning point: halftone wipe -> real demo
      (A[3] - 0.35, "wh_cine", -11, 1.2, "peak"), (A[3] + 0.2, "hit_thump", -11, 1.0, "onset"), (A[3] + 0.3, "shimmer", -15, 1.4, "onset"),
      (T[72], "pop", -12, 0.25, "onset"), (T[73] - 0.1, "wh_swish", -14, 0.6, "peak"), (T[75] - 0.1, "wh_fast", -13, 0.4, "peak"),
      (T[75], "glitch_tr", -17, 0.4, "peak"),
      # bab 5: next video + follow, offer + comment, A/B
      (A[4], "wh_fast", -12, 0.4, "peak"), (T[83], "ui_popup", -14, 0.6, "onset"), (T[95] + 0.3, "click_metal", -11, None, "onset"),
      (T[95] + 0.32, "ui_confirm", -13, None, "onset"), (B5, "wh_soft", -14, 0.9, "peak"), (T[104], "bubble", -13, 0.6, "onset"),
      (B6, "wh_swish", -14, 0.5, "peak"), (T[115] - 0.1, "pop", -12, 0.25, "onset"), (T[118], "bubble", -14, 0.6, "onset"),
      (T[119] - 0.1, "pop", -12, 0.25, "onset"), (T[119] + 0.3, "shimmer", -16, 1.4, "onset")]

mix("story-web3d-jam", C)
