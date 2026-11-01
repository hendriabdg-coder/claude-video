"""Cek API key ElevenLabs + tampilkan sisa kredit dan daftar voice (termasuk clone kamu).

Pakai:  python tools/elevenlabs_check.py
Key dibaca dari file .env di folder D:\\Claude Video (ELEVENLABS_API_KEY=...).
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
key = os.getenv("ELEVENLABS_API_KEY")
if not key:
    sys.exit("ELEVENLABS_API_KEY belum ada. Buat file .env di D:\\Claude Video dulu.")

client = ElevenLabs(api_key=key)

sub = client.user.subscription.get()
print(f"Paket : {sub.tier}")
print(f"Kredit: {sub.character_count:,} terpakai dari {sub.character_limit:,}")
print()

voices = client.voices.get_all().voices
mine = [v for v in voices if v.is_owner]
print("Voice clone milik kamu:" if mine else "Belum ada voice clone milik kamu.")
for v in mine:
    print(f"  {v.name:<30} voice_id={v.voice_id}  ({v.category})")

library = [v for v in voices if not v.is_owner and v.category == "professional"]
if library:
    print(f"\n{len(library)} voice dari Voice Library tersimpan di My Voices (bukan clone kamu).")
