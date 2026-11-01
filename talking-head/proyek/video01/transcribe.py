import json, sys
from faster_whisper import WhisperModel
import wave, numpy as np
audio, out = sys.argv[1], sys.argv[2]
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
w_=wave.open(audio,"rb"); arr=np.frombuffer(w_.readframes(w_.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
segs, info = model.transcribe(arr, language="id", word_timestamps=True, beam_size=5,
    vad_filter=True, initial_prompt="EndrichTech, ChatGPT, OpenAI, Claude, AI agent.", hotwords="EndrichTech ChatGPT OpenAI Claude")
words, segments = [], []
for s in segs:
    segments.append({"start": round(s.start,2), "end": round(s.end,2), "text": s.text.strip()})
    for w in s.words:
        words.append({"word": w.word.strip(), "start": round(w.start,2), "end": round(w.end,2), "probability": round(w.probability,3)})
json.dump({"language": info.language, "model": "large-v3-turbo (faster-whisper)", "segments": segments, "words": words},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for s in segments: print(f"[{s['start']:6.2f}-{s['end']:6.2f}] {s['text']}")
