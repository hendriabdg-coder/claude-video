# Music bed for the reel (STORY MOTION, from motion/gaya/gaya-story/music.py) via Eleven Music: one chunk per story act, so the bed follows the arc
# (storybook intro -> curious tension -> uplifting reveal -> warm confident CTA).   python music.py
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

HERE = Path(__file__).resolve().parent
load_dotenv(HERE.parents[2] / ".env")
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

CHUNKS = [(6660, ["gentle storybook intro", "soft plucked pizzicato and felt piano", "light, curious, a small doubt"], ["drums", "epic"]),
          (3830, ["slight melancholy", "muted plucks, soft low pad", "a problem appears"], ["happy", "aggressive"]),
          (13620, ["curious light tension", "ticking percussion and soft muted plucks", "thoughtful discovery, slowly building"], ["dark", "aggressive"]),
          (8010, ["uplifting reveal", "punchy clean drums enter with finger snaps", "bright plucky synth, premium product commercial, 108 bpm"], ["sad", "lo-fi"]),
          (14390, ["warm confident tech ad groove", "clean drums, soft bass, plucks", "friendly, optimistic, inviting, 108 bpm"], ["dark", "aggressive"]),
          (3000, ["soft final hit and gentle sparkle tail"], ["abrupt cut"])]
NEG = ["vocals", "singing", "spoken words"]

out = HERE / "public" / "music.mp3"
plan = {"chunks": [{"text": "", "duration_ms": d, "positive_styles": ["instrumental", "background music for a short story video"] + p,
                    "negative_styles": NEG + n, "context_adherence": "high"} for d, p, n in CHUNKS]}
try:
    audio = client.music.compose(composition_plan=plan, model_id="music_v2_5", respect_sections_durations=True, output_format="mp3_44100_192")
    out.write_bytes(b"".join(audio))
except Exception as err:
    sys.exit(f"Eleven Music gagal: {getattr(err, 'status_code', '')} {getattr(err, 'body', err)}")
print("saved", out)
