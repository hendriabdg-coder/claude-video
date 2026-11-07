# Word timeline for Endrich's manually generated VO (kebocoran API key) (no ElevenLabs timestamps): Whisper-small (sherpa-onnx) per pause
# segment, corrected text below, words spread inside each segment by vowel count (syllable proxy).
# Writes output/motion/<slug>/vo/vo-full.json in the tts.py format ({"duration", "words":[{word,start,end}]}).
import json, re, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = HERE.name
SEGS = [  # (start, end) from silencedetect -32 dB / 0.15 s; text from Whisper-small on longer windows, corrected by ear
 (0.00, 2.78, "Kamu punya website atau aplikasi yang terhubung ke AI?"),
 (3.14, 3.76, "Hati-hati,"),
 (4.00, 7.11, "ada 3 kesalahan yang bisa bikin API key kamu bocor,"),
 (7.32, 9.60, "dan yang ketiga sering banget nggak disadari."),
 (9.88, 10.36, "Pertama,"),
 (10.57, 12.00, "mengunggah kode ke GitHub."),
 (12.28, 14.64, "Kalau API key kamu ikut tersimpan di dalamnya,"),
 (14.80, 16.25, "orang lain bisa menemukannya,"),
 (16.43, 18.71, "bahkan setelah kamu hapus dari kode terbaru."),
 (18.99, 19.41, "Kedua,"),
 (19.65, 22.24, "menyimpan API key rahasia di front-end website."),
 (22.52, 24.07, "Meskipun nggak kelihatan di halaman,"),
 (24.23, 26.56, "kunci tersebut bisa saja terbaca lewat browser."),
 (26.87, 27.88, "Nah, yang ketiga,"),
 (28.06, 28.72, "ini yang menarik."),
 (28.99, 32.20, "Tanpa sadar, kamu membagikan API key lewat screenshot,"),
 (32.38, 35.61, "log error, atau bahkan saat meminta bantuan AI coding."),
 (35.87, 45.54, "Menurut laporan GitGuardian tahun 2026, sekitar 28,6 juta secret baru terdeteksi dalam commit GitHub publik sepanjang tahun 2025."),
 (45.78, 47.92, "Dan kalau API key rahasia kamu bocor,"),
 (48.09, 53.09, "orang lain bisa menyalahgunakan layanan, menghabiskan saldo API, bahkan mengakses data,"),
 (53.26, 54.65, "tergantung izin yang dimiliki."),
 (54.89, 60.56, "Jadi, simpan secret key di back-end, batasi aksesnya, dan jangan pernah membagikannya sembarangan."),
 (60.80, 62.72, "Kalau kamu pernah pakai AI buat coding,"),
 (62.89, 63.56, "coba cek lagi."),
 (63.74, 66.49, "Jangan-jangan API key kamu pernah ikut terkirim."),
]
def weight(w):
    w = w.lower()
    if w == "ai": return 2
    if re.fullmatch(r"[\d,]+", w): return {"2026": 4, "2025": 4, "286": 5}.get(w.replace(",", ""), 2)
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
