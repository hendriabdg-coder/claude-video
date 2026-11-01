# Background music for "Black October" via Eleven Music (music_v2_5 chunk plan): one chunk per video chapter so the
# mood turns exactly at the cuts.  python music.py
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

HERE = Path(__file__).resolve().parent
load_dotenv(HERE.parents[2] / ".env")
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# scene cuts from build.py: hook 0-11.85, PHP 11.85-23.75, Plex 23.75-33.81, GitLab 33.81-42.03,
# eMudhra 42.03-52.89, outro 52.89-63.3
CHUNKS = [
    (11850, ["dark cyber-thriller intro", "low ominous sub drone", "ticking clock pulse", "sparse glitchy plucks",
             "building dread"], ["drums", "happy"]),
    (11900, ["urgent cyber-thriller groove", "driving distorted bass pulse", "tight electronic percussion",
             "alarm-like synth stabs", "red alert tension"], ["happy", "major key"]),
    (10060, ["continue urgent groove", "gritty arpeggiated synth", "heavier drums", "relentless"], ["happy"]),
    (8220, ["suspense break", "drums drop out", "filtered bass", "uncertain hanging chords", "investigative"],
     ["big drums"]),
    (10860, ["mysterious suspense", "glassy synth arpeggio", "soft heartbeat kick", "amber warm tone",
             "curious tension"], ["happy", "aggressive"]),
    (10410, ["resolution", "confident warm synth chords", "steady beat", "clear ending, final hit"],
     ["dark", "abrupt cut"]),
]
GLOBAL_POS = ["instrumental", "cinematic electronic background music for a tech news short", "110 bpm",
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
