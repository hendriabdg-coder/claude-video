# Timing kata untuk VO manual Endrich (Peris.ai): segmen jeda dari silencedetect, teks Whisper-small dikoreksi telinga,
# kata disebar per segmen berdasarkan jumlah vokal. Tulis output/motion/<slug>/vo/vo-full.json (format tools/tts.py).
import json, re, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = HERE.name
SEGS = [
 (0.00, 4.35, "Kenapa yang juara satu kompetisi AI se-ASEAN justru startup keamanan siber?"),
 (4.76, 7.19, "Karena ancaman hacker sekarang makin gila."),
 (7.53, 11.30, "Minggu ini, Peris.ai dari Indonesia menang di"),
 (11.36, 13.30, "Korea-ASEAN AI Youth Festa 2026,"),
 (13.46, 16.31, "ngalahin 23 startup dari 12 negara."),
 (16.61, 18.49, "Produk mereka pakai agentic AI,"),
 (18.69, 21.56, "yaitu AI yang bisa kerja sendiri,"),
 (21.62, 25.32, "berjaga 24 jam mendeteksi serangan, terus langsung bertindak tanpa nunggu manusia."),
 (25.64, 26.83, "Pelajarannya buat kita gini."),
 (27.16, 33.16, "Kalau perusahaan besar aja butuh AI buat jaga datanya, gimana dengan bisnis kecil yang sama sekali nggak punya pengamanan?"),
 (33.45, 34.93, "Akun WhatsApp bisnis dibajak,"),
 (35.06, 36.26, "data pelanggan bocor,"),
 (36.40, 38.99, "website disusupi judi online,"),
 (39.10, 41.41, "semua itu nyata dan sering banget kejadian ke UMKM."),
 (41.67, 42.83, "Mulai dari yang paling dasar."),
 (43.07, 44.81, "Aktifkan verifikasi dua langkah,"),
 (45.00, 46.56, "jangan pakai password yang sama,"),
 (46.63, 48.13, "dan jangan asal klik link."),
 (48.43, 50.46, "Menurut kamu, bisnis kamu udah aman belum?"),
 (50.72, 53.13, "Dan follow buat tips keamanan digital berikutnya."),
]
NUM = {"2026": 6, "23": 4, "12": 3, "24": 4, "umkm": 4, "se-asean": 4, "19": 3, "83": 4, "70": 3, "78": 5, "81": 4, "rp1300": 9, "111": 6, "34": 5, "97": 5, "17": 4, "ant": 2, "ipo": 3, "ipohnya": 4}
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
