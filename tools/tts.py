"""Voiceover ElevenLabs pakai clone suara Endrich, + timestamp per kata untuk motion graphic.

Pakai:
  python tools/tts.py naskah.txt                 -> output di folder naskah_vo/
  python tools/tts.py naskah.txt --out D:/proyek/vo --model eleven_v4 --stability 0.35

Model ekspresif (eleven_v4 / eleven_v3) memahami audio tag di naskah, misalnya [curious], [laughs], [sighs].
Tag tidak ikut ke JSON timestamp; untuk model lain tag otomatis dibuang sebelum dikirim.

Naskah: satu scene per paragraf (pisahkan dengan baris kosong).
Per scene keluar scene_01.mp3 + scene_01.json (kata asli + start/end detik).
Kata di tools/pelafalan.json diganti cara bacanya sebelum dikirim (AI -> Ei-ai, 3D -> tridi),
tapi JSON timestamp tetap memakai kata asli dari naskah.
"""
import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

ROOT = Path(__file__).resolve().parent.parent
VOICE_ID = "xV29wBiBgOzpCgTwBbDC"  # Endrich - VO (Instant Voice Clone)
TAGGED_MODELS = ("eleven_v4", "eleven_v3")  # model yang membaca [audio tag]; v4 tidak punya slider style/speed
TAG = re.compile(r"\[[^\]]*\]\s*")


def strip_tags(text):
    return re.sub(r"\s{2,}", " ", TAG.sub("", text)).strip()


def voice_settings(model, stability, similarity, style, speed=None):
    if model in TAGGED_MODELS:
        extra = {"speed": speed} if speed else {}
        return VoiceSettings(stability=stability, similarity_boost=similarity, use_speaker_boost=True, **extra)
    return VoiceSettings(stability=stability, similarity_boost=similarity, style=style, use_speaker_boost=True, speed=1.0)


def load_lexicon():
    data = json.loads((ROOT / "tools" / "pelafalan.json").read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


def to_spoken(text, lexicon):
    """Ganti kata utuh sesuai kamus. Tidak menyentuh 'ai' di dalam kata seperti 'pakai'."""
    for word, spoken in lexicon.items():
        text = re.sub(rf"(?<![\w]){re.escape(word)}(?![\w])", spoken, text)
    return text


def word_timings(alignment, original_text):
    """Kelompokkan timestamp per karakter jadi per kata, lalu pasangkan ke kata naskah asli."""
    words, cur, start, end, in_tag = [], "", None, None, False
    for ch, s, e in zip(alignment.characters, alignment.character_start_times_seconds,
                        alignment.character_end_times_seconds):
        if ch == "[":
            in_tag = True
        if in_tag:  # audio tag tidak diucapkan -> bukan kata
            in_tag = ch != "]"
            continue
        if ch.isspace():
            if cur:
                words.append((cur, start, end))
            cur, start = "", None
            continue
        if start is None:
            start = s
        cur, end = cur + ch, e
    if cur:
        words.append((cur, start, end))

    original = strip_tags(original_text).split()
    if len(original) != len(words):  # jaga-jaga; seharusnya selalu sama karena kamus tanpa spasi
        print(f"  ! jumlah kata beda ({len(original)} vs {len(words)}), pakai teks yang diucapkan")
        original = [w for w, _, _ in words]
    return [{"word": o, "spoken": w, "start": round(s, 3), "end": round(e, 3)}
            for o, (w, s, e) in zip(original, words)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("naskah")
    ap.add_argument("--out")
    ap.add_argument("--model", default="eleven_multilingual_v2")
    ap.add_argument("--seed", type=int, default=42)
    # default = setelan yang disetujui di tes web (m2, stability 50, similarity 75, style 0)
    ap.add_argument("--stability", type=float, default=0.5)
    ap.add_argument("--similarity", type=float, default=0.75)
    ap.add_argument("--style", type=float, default=0.0)
    ap.add_argument("--speed", type=float, help="tempo bicara, mis. 1.15 (gaya mentor cepat seperti ref-intonasi)")
    args = ap.parse_args()

    load_dotenv(ROOT / ".env")
    if not os.getenv("ELEVENLABS_API_KEY"):
        sys.exit("ELEVENLABS_API_KEY belum ada di .env")
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    src = Path(args.naskah)
    scenes = [p.strip() for p in re.split(r"\n\s*\n", src.read_text(encoding="utf-8")) if p.strip()]
    out = Path(args.out) if args.out else src.with_name(src.stem + "_vo")
    out.mkdir(parents=True, exist_ok=True)
    lexicon = load_lexicon()

    spoken_all = [to_spoken(s, lexicon) for s in scenes]
    if args.model not in TAGGED_MODELS:
        spoken_all = [strip_tags(s) for s in spoken_all]
    settings = voice_settings(args.model, args.stability, args.similarity, args.style, args.speed)
    total_chars = sum(len(s) for s in spoken_all)
    print(f"{len(scenes)} scene, {total_chars} karakter, model {args.model}")

    for i, (scene, spoken) in enumerate(zip(scenes, spoken_all), 1):
        # previous/next_text menjaga intonasi tetap nyambung antar scene
        context = {}
        if i > 1:
            context["previous_text"] = spoken_all[i - 2]
        if i < len(spoken_all):
            context["next_text"] = spoken_all[i]
        request = dict(text=spoken, model_id=args.model, voice_settings=settings,
                       output_format="mp3_44100_192", seed=args.seed)
        try:
            res = client.text_to_speech.convert_with_timestamps(VOICE_ID, **request, **context)
        except Exception as err:  # beberapa model menolak previous/next_text
            if not context:
                raise
            print(f"  ! konteks antar scene ditolak ({str(err)[:80]}), ulang tanpa konteks")
            res = client.text_to_speech.convert_with_timestamps(VOICE_ID, **request)
        name = f"scene_{i:02d}"
        (out / f"{name}.mp3").write_bytes(base64.b64decode(res.audio_base_64))
        words = word_timings(res.alignment, scene)
        (out / f"{name}.json").write_text(json.dumps(
            {"text": scene, "spoken": spoken, "duration": words[-1]["end"] if words else 0, "words": words},
            ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  {name}.mp3  {words[-1]['end'] if words else 0:.2f}s  | {spoken[:60]}")

    print(f"Selesai -> {out}")


if __name__ == "__main__":
    main()
