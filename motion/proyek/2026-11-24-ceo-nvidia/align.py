# Timing kata untuk VO manual Endrich (CEO Nvidia): segmen jeda dari silencedetect, teks Whisper-small dikoreksi telinga,
# kata disebar per segmen berdasarkan jumlah vokal. Tulis output/motion/<slug>/vo/vo-full.json (format tools/tts.py).
import json, re, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = HERE.name
SEGS = [
 (0.00, 2.20, "Satu orang pergi, saham anjlok."),
 (2.62, 5.68, "Satu orang kembali, saham melonjak 30%."),
 (5.97, 7.54, "Inilah kekuatan Jensen Huang."),
 (8.01, 12.14, "12 November, CEO Nvidia itu mundur setelah mengakui perselingkuhan,"),
 (12.37, 16.17, "di tengah penyelidikan soal laporan bahwa dia jadi sasaran intelijen."),
 (16.44, 17.55, "Pasar langsung panik."),
 (17.89, 23.08, "Nvidia adalah tulang punggung industri AI dunia, dan sosok di puncaknya tiba-tiba hilang."),
 (23.38, 29.44, "Dewan menunjuk CFO Colette Kress sebagai CEO sementara, dan menegaskan tidak akan mengangkat Jensen lagi."),
 (29.71, 32.89, "Tapi 11 hari setelah dia mundur, dewan berbalik arah."),
 (33.17, 34.00, "Jensen kembali."),
 (34.25, 37.29, "Investor lega, saham pulih hampir semua kerugiannya."),
 (37.56, 39.91, "Trump juga mengaku ikut berperan dalam keputusan ini."),
 (40.28, 42.34, "Pelajarannya buat kita yang menjalankan bisnis:"),
 (42.61, 47.46, "kalau perusahaan terlalu bergantung pada satu orang, itu kekuatan sekaligus risiko besar."),
 (47.73, 49.26, "Apa yang terjadi kalau orang itu pergi?"),
 (49.55, 51.35, "Bisnis kamu sudah siap jalan tanpa kamu?"),
 (51.60, 52.41, "Jawab di komentar."),
]
NUM = {"30": 5, "12": 4, "11": 4, "cfo": 3, "ceo": 3, "19": 3, "83": 4, "70": 3, "78": 5, "81": 4, "rp1300": 9, "111": 6, "34": 5, "97": 5, "17": 4, "ant": 2, "ipo": 3, "ipohnya": 4}
def weight(w):
    w = w.lower()
    if w == "ai": return 2
    if w in NUM: return NUM[w]
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
out.write_text(json.dumps({"duration": round(dur, 3), "source": "VO manual ElevenLabs dari Endrich; timing diperkirakan", "words": words},
                          ensure_ascii=False, indent=1), encoding="utf-8")
for i, w in enumerate(words): print(i, w["word"], w["start"], end=" | ")
