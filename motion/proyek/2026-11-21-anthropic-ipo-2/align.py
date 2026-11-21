# Timing kata untuk VO manual Endrich (Anthropic IPO part 2): segmen jeda dari silencedetect, teks Whisper-small dikoreksi telinga,
# kata disebar per segmen berdasarkan jumlah vokal. Tulis output/motion/<slug>/vo/vo-full.json (format tools/tts.py).
import json, re, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = HERE.name
SEGS = [
 (0.00, 1.57, "Kamu pakai Claude buat kerja?"),
 (1.92, 4.29, "Nah, perusahaan di balik AI andalan kamu itu"),
 (4.39, 7.00, "sekarang udah resmi masuk bursa saham Amerika."),
 (7.29, 8.79, "Anthropic, pembuat Claude."),
 (9.03, 12.81, "IPO di Nasdaq tanggal 19 November dengan kode ANT."),
 (13.05, 14.65, "Dan ini bukan IPO biasa."),
 (14.90, 17.24, "Ini IPO terbesar sepanjang sejarah."),
 (17.43, 20.06, "Dana yang masuk 81 miliar dolar."),
 (20.30, 22.97, "Valuasinya sekitar 1,5 triliun dolar."),
 (23.22, 26.40, "Di hari pertama sahamnya sempat lompat 34%."),
 (26.67, 28.95, "Terus, apa artinya buat kita yang bukan investor?"),
 (29.22, 29.84, "Ada 3 hal."),
 (30.11, 35.11, "Pertama, AI udah bukan tren lagi, tapi industri raksasa yang dipercaya pasar global."),
 (35.35, 39.48, "Kedua, persaingannya makin ketat, jadi fitur AI bakal berkembang makin cepat."),
 (39.77, 45.55, "Ketiga, di dokumen IPO-nya Anthropic sendiri bilang batas pemakaian dan fitur bisa berubah sewaktu-waktu."),
 (45.75, 47.87, "Jadi jangan cuma bergantung ke satu tools."),
 (48.06, 50.56, "Pelajari cara kerjanya, bukan cuma tombolnya."),
 (50.79, 55.08, "Yang paham AI dari sekarang bakal paling siap waktu semua bisnis mulai pakai AI."),
 (55.36, 57.45, "Follow EndrichTech biar kamu nggak ketinggalan."),
]
NUM = {"15": 5, "81": 4, "3": 2, "34": 5, "19": 3, "ant": 2, "ipo": 3, "ipomnya": 4, "ipohnya": 4, "19": 3, "83": 4, "70": 3, "78": 5, "81": 4, "rp1300": 9, "111": 6, "34": 5, "97": 5, "17": 4, "ant": 2, "ipo": 3, "ipohnya": 4}
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
