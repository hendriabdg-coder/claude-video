# Eleven Music beds for full reels (CLAUDE.md §7): one instrumental bed per reel, chunked to the reel's structure
# (hook / body / CTA / tail), length = composition duration.  python reel_music.py <slug> [<slug> ...]
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

HERE = Path(__file__).resolve().parent
load_dotenv(HERE.parents[1] / ".env")
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
GLOBAL_NEG = ["vocals", "singing", "spoken words"]
MOOD = {
    "2026-10-26-ai-pemburu-celah": (["dark cinematic tension", "deep pulsing sub bass", "ticking hi-hat", "warm analog synth pads",
                                     "cyber security news, serious, 90 bpm"], ["happy", "acoustic", "lo-fi"]),
    "2026-10-27-chatgpt-intelligent-ui": (["minimal clean electronic", "bright plucky synths", "soft punchy kick and claps",
                                           "modern tech product update, curious, upbeat, 108 bpm"], ["dark", "orchestral", "aggressive"]),
    "2026-10-28-penipuan-suara-ai": (["dark minimal synthwave", "suspenseful analog bass arpeggio", "glitchy digital ticks",
                                      "scam warning, tense but not horror, 95 bpm"], ["happy", "acoustic", "epic"]),
}


def work(slug):
    # style previews live next to this file, reels in motion/proyek/
    return HERE / slug if (HERE / slug).exists() else HERE.parent / "proyek" / slug


def duration(slug):
    html = (work(slug) / "public" / "index.html").read_text(encoding="utf-8")
    return float(re.search(r'data-composition-id="[^"]+" data-start="0" data-duration="([\d.]+)"', html).group(1))


for slug in sys.argv[1:]:
    out = work(slug) / "public" / "music.mp3"
    if out.exists():
        print("exists", out)
        continue
    pos, neg = MOOD[slug]
    total = int(duration(slug) * 1000) + 500
    plan = [(4000, ["sparse intro hit, immediate start"] + pos, []),
            (total - 4000 - 9000 - 3500, ["main groove"] + pos, []),
            (9000, ["lighter, warmer, slightly hopeful variation", "room for voice"] + pos[1:], []),
            (3500, ["clean resolve, final hit and short tail"], ["abrupt cut"])]
    body = {"chunks": [{"text": "", "duration_ms": d, "positive_styles": ["instrumental", "background music for a short video"] + p,
                        "negative_styles": GLOBAL_NEG + neg + n, "context_adherence": "high"} for d, p, n in plan]}
    try:
        audio = client.music.compose(composition_plan=body, model_id="music_v2_5", respect_sections_durations=True,
                                     output_format="mp3_44100_192")
        out.write_bytes(b"".join(audio))
    except Exception as err:
        sys.exit(f"{slug}: Eleven Music gagal: {getattr(err, 'status_code', '')} {getattr(err, 'body', err)}")
    print("saved", out)
