# Timing kata untuk VO manual Endrich (AI dilarang negara): segmen jeda dari silencedetect, teks Whisper-small dikoreksi telinga,
# kata disebar per segmen berdasarkan jumlah vokal. Tulis output/motion/<slug>/vo/vo-full.json (format tools/tts.py).
import json, re, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = HERE.name
SEGS = [
 (0.00, 3.60, "Kenapa sebuah negara sampai melarang AI buatan perusahaannya sendiri?"),
 (3.94, 7.25, "Itu yang terjadi pada Claude Fable 5 dan Claude Mythos 5."),
 (7.72, 9.04, "Juni 2026."),
 (9.28, 14.58, "Belum seminggu setelah Fable 5 rilis, Departemen Perdagangan Amerika memberlakukan kontrol ekspor."),
 (14.83, 17.11, "Warga asing tidak boleh mengakses keduanya."),
 (17.38, 22.57, "Akibatnya, dua model AI tercanggih saat itu mati total untuk semua pengguna di dunia."),
 (22.84, 23.56, "Ketakutannya:"),
 (23.78, 27.72, "kemampuan AI ini bisa dipakai untuk mencari celah keamanan perangkat lunak."),
 (27.95, 31.74, "Artinya, Amerika menilai model AI sama strategisnya dengan chip."),
 (32.16, 33.85, "Akhir Juni, larangan itu dicabut,"),
 (34.11, 36.52, "setelah Anthropic sepakat memperketat pengamanan."),
 (36.83, 37.73, "Tapi coba pikir."),
 (38.04, 40.93, "Kalau negara maju saja seserius itu menjaga AI,"),
 (41.16, 42.33, "kenapa kita masih santai?"),
 (42.66, 44.58, "Indonesia tidak boleh cuma jadi pasar."),
 (44.85, 48.78, "Pelajar, pekerja, pelaku usaha, semua perlu melek AI."),
 (49.00, 54.15, "Bukan untuk ikut-ikutan tren, tapi supaya kita tidak tertinggal saat dunia bergerak secepat ini."),
 (54.43, 55.41, "Pertanyaannya sekarang:"),
 (55.64, 57.02, "kamu sudah mulai belajar,"),
 (57.22, 58.30, "atau masih menunggu?"),
]
NUM = {"5": 2, "2026": 6, "19": 3, "83": 4, "70": 3, "78": 5, "81": 4, "rp1300": 9, "111": 6, "34": 5, "97": 5, "17": 4, "ant": 2, "ipo": 3, "ipohnya": 4}
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
