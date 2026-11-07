# Word timeline for Endrich's manually generated VO (no ElevenLabs timestamps): Whisper-small (sherpa-onnx) per pause
# segment, corrected text below, words spread inside each segment by vowel count (syllable proxy).
# Writes output/motion/<slug>/vo/vo-full.json in the tts.py format ({"duration", "words":[{word,start,end}]}).
import json, re, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = HERE.name
SEGS = [  # (start, end) from silencedetect -38 dB / 0.28 s; text checked by ear against the ASR draft
 (0.00, 6.25, "Ada hampir 2000 agent AI berhasil menganalisis data sel otak tikus, cuma dalam waktu 32 menit."),
 (6.60, 7.33, "Cepat banget kan?"),
 (7.64, 12.33, "Tapi jangan salah paham dulu, ini bukan berarti AI udah berhasil nemuin obat baru."),
 (12.63, 13.12, "Jadi gini."),
 (13.47, 21.77, "Masing-masing agent AI dikasih tugas buat meneliti satu gen. Mereka membaca data, mencari informasi dari jurnal ilmiah, lalu menyusun laporan."),
 (22.06, 27.85, "Nah, semua laporan itu kemudian digabung, buat melihat pola yang sebelumnya mungkin sulit ditemukan manusia."),
 (28.14, 37.17, "Dan ternyata ada temuan yang cukup menarik. Dua gen namanya Tsc1 dan Tsc2 menunjukkan efek yang berbeda banget di bagian otak kecil."),
 (37.46, 39.86, "Padahal keduanya punya hubungan yang cukup erat."),
 (40.20, 42.42, "Tapi ada satu hal penting yang perlu kamu tahu."),
 (42.72, 57.75, "Hasil ini masih berupa temuan awal. Belum dibuktikan lewat eksperimen laboratorium dan belum melewati peninjauan ilmiah independen. Apalagi, sebagian penelitinya juga berasal dari OpenAI sendiri. Jadi, bukan berarti hasilnya salah. Tapi tetap perlu diuji dulu."),
 (58.04, 62.52, "Dan besok, kita akan bahas bahaya tersembunyi di balik alat yang digunakan agent AI."),
 (62.84, 64.48, "Follow dulu biar nggak ketinggalan."),
 (64.76, 71.20, "Kalau menurut kamu, hasil penelitian AI seperti ini langsung bisa dipercaya, atau harus dibuktikan di laboratorium dulu?"),
]
def weight(w):
    w = w.lower()
    if w == "ai": return 2
    if re.fullmatch(r"\d+", w): return {"2000": 4, "32": 4}.get(w, 2)
    if w.startswith("tsc"): return 4
    return max(1, len(re.findall(r"[aiueo]+", w)))
words = []
for s, e, text in SEGS:
    toks = text.split()
    ws = [weight(re.sub(r"[^\w]", "", t)) + (0.6 if re.search(r"[.,?]$", t) else 0) for t in toks]
    tot, acc = sum(ws), 0.0
    for t, w in zip(toks, ws):
        a = s + (e - s) * acc / tot; acc += w; b = s + (e - s) * acc / tot
        words.append({"word": t, "start": round(a, 3), "end": round(b, 3)})
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                     str(ROOT / "output/motion" / SLUG / "vo/vo-full.mp3")]))
out = ROOT / "output/motion" / SLUG / "vo/vo-full.json"
out.write_text(json.dumps({"duration": round(dur, 3), "source": "manual ElevenLabs VO by Endrich; timings estimated", "words": words}, ensure_ascii=False, indent=1), encoding="utf-8")
for i, w in enumerate(words): print(i, w["word"], w["start"], end=" | ")
