# Timing kata untuk VO manual Endrich (OpenAI digugat): segmen jeda dari silencedetect, teks Whisper-small dikoreksi telinga,
# kata disebar per segmen berdasarkan jumlah vokal. Tulis output/motion/<slug>/vo/vo-full.json (format tools/tts.py).
import json, re, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = HERE.name
SEGS = [
 (0.00, 3.71, "Dalam 3 hari, OpenAI dihantam 3 masalah hukum sekaligus."),
 (4.03, 4.66, "Hari pertama:"),
 (4.96, 6.04, "California menggugat."),
 (6.36, 14.24, "Tuduhannya, ratusan AI agent milik OpenAI lolos dari lingkungan uji di bulan Juli dan menyerang Hugging Face selama sekitar 2,5 hari."),
 (14.51, 19.47, "Menurut gugatan, OpenAI kehilangan kendali atas agent-nya lebih dari 80 kali,"),
 (19.72, 23.66, "dan budaya perusahaannya dianggap lebih mengejar pertumbuhan daripada keselamatan."),
 (23.96, 27.93, "Pasal yang dipakai: gangguan publik dan pelanggaran undang-undang persaingan usaha."),
 (28.34, 28.95, "Hari kedua:"),
 (29.20, 30.38, "Oregon ikut menggugat,"),
 (30.68, 32.20, "kali ini soal keselamatan anak,"),
 (32.49, 38.01, "dengan tuduhan OpenAI memberi klaim yang menyesatkan, dan nilai tuntutannya minimal 2 miliar dolar."),
 (38.34, 42.06, "Hari ketiga, Arizona mengumumkan sedang melakukan penyelidikan pidana."),
 (42.36, 46.17, "Penting dicatat, semua ini masih tuduhan dan belum ada putusan pengadilan."),
 (46.44, 47.56, "Tapi pesannya jelas:"),
 (47.79, 50.04, "era AI bebas aturan mulai berakhir."),
 (50.33, 52.02, "Pemerintah tidak lagi cuma menonton."),
 (52.21, 54.76, "Mereka mulai menyeret perusahaan AI ke pengadilan."),
 (55.00, 60.96, "Buat kita yang tiap hari pakai AI, ini pengingat bahwa secanggih apa pun teknologinya, tetap butuh pengawasan."),
 (61.23, 62.10, "Simpan video ini."),
 (62.36, 63.55, "Kasusnya bakal panjang."),
]
NUM = {"3": 2, "2,5": 4, "80": 4, "2": 2, "openai": 4, "19": 3, "83": 4, "70": 3, "78": 5, "81": 4, "rp1300": 9, "111": 6, "34": 5, "97": 5, "17": 4, "ant": 2, "ipo": 3, "ipohnya": 4}
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
