# Timing kata untuk VO manual Endrich (Anthropic IPO): segmen jeda dari silencedetect, teks Whisper-small dikoreksi telinga,
# kata disebar per segmen berdasarkan jumlah vokal. Tulis output/motion/<slug>/vo/vo-full.json (format tools/tts.py).
import json, re, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = HERE.name
SEGS = [
 (0.00, 3.33, "Rekor IPO terbesar sepanjang sejarah baru aja pecah."),
 (3.59, 5.23, "Dan pemecahnya bukan Elon Musk."),
 (5.53, 6.63, "Pemecahnya Anthropic."),
 (7.00, 8.19, "Perusahaan di balik"),
 (8.48, 10.33, "AI yang mungkin kamu pakai tiap hari."),
 (10.63, 12.22, "Tanggal 19 November kemarin,"),
 (12.39, 15.61, "Anthropic resmi masuk Nasdaq dengan kode saham ANT."),
 (15.89, 18.48, "Harga IPO-nya 83 dolar per lembar."),
 (18.70, 22.22, "Padahal awalnya cuma ditarget 70 sampai 78 dolar."),
 (22.50, 25.35, "Dana yang terkumpul, 81 miliar dolar,"),
 (25.61, 28.29, "atau lebih dari Rp1.300 triliun,"),
 (28.53, 30.93, "dan itu ngalahin rekor SpaceX bulan Juni lalu."),
 (31.18, 32.41, "Begitu bel dibunyikan,"),
 (32.48, 36.64, "sahamnya langsung dibuka di 111 dolar, naik 34 persen."),
 (36.87, 38.46, "Tapi pasar tetap pasar."),
 (38.72, 40.82, "Sorenya ditutup di 97 dolar,"),
 (41.06, 43.24, "masih naik 17% dari harga IPO."),
 (43.50, 44.23, "Yang bikin menarik,"),
 (44.47, 48.66, "Anthropic masih rugi besar karena biaya komputasi AI super mahal."),
 (48.90, 53.14, "Artinya, investor lagi bertaruh di masa depan AI, bukan di untung hari ini."),
 (53.39, 56.74, "Menurut kamu, ini awal era baru atau tanda gelembung AI?"),
 (56.96, 60.51, "Tulis di komentar dan follow EndrichTech buat update AI tiap hari."),
]
NUM = {"19": 3, "83": 4, "70": 3, "78": 5, "81": 4, "rp1300": 9, "111": 6, "34": 5, "97": 5, "17": 4, "ant": 2, "ipo": 3, "ipohnya": 4}
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
