# Background music for "Claude Duet" (SIGNAL style) via Eleven Music (music_v2_5 chunk plan): one chunk per video chapter so the
# mood turns exactly at the cuts.  python music.py
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

HERE = Path(__file__).resolve().parent
load_dotenv(HERE.parents[2] / ".env")
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# scene cuts from build.py: s1 0-11.53, s2 11.53-22.31, s3 22.31-36.18, s4 36.18-46.11, s5 46.11-53.4
CHUNKS = [
    (11530, ["bright morning wake-up feel", "soft plucked synth motif", "light shaker", "curious and optimistic"],
     ["dark", "heavy drums"]),
    (10780, ["clean minimal tech groove", "warm sub bass", "crisp light drums", "smooth and confident"], ["dark"]),
    (13870, ["focused careful mood", "muted groove", "ticking hi-hat", "subtle tension then release"],
     ["aggressive", "big drums"]),
    (9930, ["slightly bittersweet", "drums thin out", "soft pads", "honest calm"], ["happy", "aggressive"]),
    (7290, ["warm hopeful outro", "plucks return", "gentle lift", "clean ending"], ["dark", "abrupt cut"]),
]
GLOBAL_POS = ["instrumental", "minimal modern lo-fi electronic background music for a tech explainer short", "100 bpm",
              "leaves space for a voiceover"]
GLOBAL_NEG = ["vocals", "singing", "spoken words", "lo-fi vinyl crackle"]
plan = {"chunks": [{"text": "", "duration_ms": d, "positive_styles": GLOBAL_POS + p, "negative_styles": GLOBAL_NEG + n,
                    "context_adherence": "high"} for d, p, n in CHUNKS]}

out = HERE / "public" / "music.mp3"
try:
    audio = client.music.compose(composition_plan=plan, model_id="music_v2_5", respect_sections_durations=True,
                                 output_format="mp3_44100_192")
    out.write_bytes(b"".join(audio))
except Exception as err:
    sys.exit(f"Eleven Music gagal: {getattr(err, 'status_code', '')} {getattr(err, 'body', err)}")
print("saved", out, out.stat().st_size, "bytes")
