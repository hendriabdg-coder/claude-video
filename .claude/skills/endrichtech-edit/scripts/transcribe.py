# Word-level transcript for an EndrichTech take.
#   python transcribe.py "<video>" <out.words.json> [extra hotwords...]
# faster-whisper large-v3-turbo, CPU int8, Indonesian. Audio is decoded with ffmpeg to a 16 kHz WAV and read
# with numpy (faster-whisper's own decoder crashes on this machine: av.open(... metadata_errors) bug).
import json, os, subprocess, sys, tempfile, wave
import numpy as np

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")      # Xet downloads stall on this connection
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
from faster_whisper import WhisperModel

video, out = sys.argv[1], sys.argv[2]
extra = sys.argv[3:]
BASE_HOT = ["EndrichTech", "AI", "ChatGPT", "OpenAI", "Claude", "Gemini"]
hot = BASE_HOT + [h for h in extra if h not in BASE_HOT]

wav = os.path.join(tempfile.gettempdir(), "edt_audio16k.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav], check=True)
w_ = wave.open(wav, "rb")
arr = np.frombuffer(w_.readframes(w_.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0

model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
segs, info = model.transcribe(arr, language="id", word_timestamps=True, beam_size=5, vad_filter=True,
                              initial_prompt=", ".join(hot) + ".", hotwords=" ".join(hot))
words, segments = [], []
for s in segs:
    segments.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()})
    for w in s.words:
        words.append({"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2), "probability": round(w.probability, 3)})
json.dump({"language": info.language, "duration": round(len(arr) / 16000, 3), "model": "large-v3-turbo (faster-whisper)",
           "segments": segments, "words": words}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

for s in segments:
    print(f"[{s['start']:6.2f}-{s['end']:6.2f}] {s['text']}")
low = [f"{i}:{w['word']}({w['probability']})" for i, w in enumerate(words) if w["probability"] < 0.6]
print("\nLOW-CONFIDENCE WORDS (<0.6):", ", ".join(low) if low else "none")
