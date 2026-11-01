# Music beds for the style-template previews (15 s each) via Eleven Music. One mood per style: the bed is part of
# each style's identity.  python gaya_music.py
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

HERE = Path(__file__).resolve().parent
load_dotenv(HERE.parents[1] / ".env")
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

STYLES = {
    "paper": [(12000, ["soft acoustic lo-fi", "light ukulele or plucked guitar", "gentle brushed percussion",
                       "calm, friendly, curious, like an explainer about money"], ["dark", "heavy drums"]),
              (3000, ["soft resolve", "warm final chord"], ["abrupt cut"])],
    "pulse": [(12000, ["punchy energetic electronic", "hard four-on-the-floor kick", "stabby synth hits on the beat",
                       "hype, motivational, fast cuts, 124 bpm"], ["calm", "lo-fi"]),
              (3000, ["big final hit then short tail"], ["fade-in"])],
    "terminal": [(12000, ["dark minimal synthwave", "pulsing analog bass arpeggio", "glitchy digital ticks",
                          "hacker / cyber security mood, 100 bpm"], ["happy", "acoustic"]),
                 (3000, ["low drone resolve", "digital glitch ending"], ["abrupt cut"])],
    "avatar": [(12000, ["playful bouncy pop", "warm plucky synths and claps", "light marimba accents",
                        "friendly cartoon presenter, optimistic, 110 bpm"], ["dark", "aggressive"]),
               (3000, ["cheerful final hit and sparkle tail"], ["abrupt cut"])],
    "setup": [(12000, ["chill lo-fi house", "soft deep kick and shaker", "warm electric piano chords",
                       "cozy late-night desk setup, focused, 105 bpm"], ["epic", "orchestral"]),
              (3000, ["filtered resolve", "warm final chord"], ["abrupt cut"])],
    "guide": [(12000, ["modern clean lo-fi pop", "soft punchy kick and finger snaps", "warm rhodes chords and light plucks",
                       "friendly how-to tutorial, confident and light, 104 bpm"], ["dark", "epic", "aggressive"]),
              (3000, ["light final hit and soft sparkle tail"], ["abrupt cut"])],
    "showcase": [(12000, ["modern upbeat product commercial", "punchy clean drums and finger snaps", "warm plucky synth and soft bass",
                          "premium, confident, playful tech ad, 112 bpm"], ["dark", "lo-fi", "aggressive"]),
                 (3000, ["bright final hit and sparkle tail"], ["abrupt cut"])],
}
GLOBAL_NEG = ["vocals", "singing", "spoken words"]

for name, chunks in STYLES.items():
    out = HERE / f"gaya-{name}" / "public" / "music.mp3"
    if out.exists():
        continue
    plan = {"chunks": [{"text": "", "duration_ms": d, "positive_styles": ["instrumental", "background music for a short video"] + p,
                        "negative_styles": GLOBAL_NEG + n, "context_adherence": "high"} for d, p, n in chunks]}
    try:
        audio = client.music.compose(composition_plan=plan, model_id="music_v2_5", respect_sections_durations=True,
                                     output_format="mp3_44100_192")
        out.write_bytes(b"".join(audio))
    except Exception as err:
        sys.exit(f"{name}: Eleven Music gagal: {getattr(err, 'status_code', '')} {getattr(err, 'body', err)}")
    print("saved", out)
