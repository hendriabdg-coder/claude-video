# Perkiraan timestamp per kata untuk vo/vo-full.mp3 (VO clone yang digenerate manual, tanpa JSON timestamp).
# Teks diasumsikan = vo/naskah_vo_aktual.txt (urutan kalimat cocok dengan jeda di audio). Kalimat di-anchor ke jeda
# (silencedetect) yang terdekat, lalu kata diinterpolasi menurut panjang huruf. Hasil: vo/align.json
import json, re, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
txt = " ".join((HERE / "vo" / "naskah_vo_aktual.txt").read_text(encoding="utf-8").split())
out = subprocess.run(["ffmpeg", "-i", str(HERE / "vo" / "vo-full.mp3"), "-af", "silencedetect=n=-40dB:d=0.2", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
pauses = [(a, b) for a, b in zip(ss, se) if a > 0.3]
speech_end = ss[-1] if len(ss) > len(se) else float(subprocess.check_output(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(HERE / "vo" / "vo-full.mp3")]))
words = txt.split()
cum, c = [], 0
for w in words:
    cum.append(c); c += len(w) + 1
L = c
# sentence/clause ends (char positions) as candidate anchors
cand = [cum[i] + len(w) + 1 for i, w in enumerate(words) if w[-1] in ".?!," or w.endswith("...")]
anchors = [(0, 0.05), (L, speech_end)]
for a, b in pauses:
    est = lambda p: p / L * speech_end
    best = min(cand, key=lambda p: abs(est(p) - (a + b) / 2))
    if abs(est(best) - (a + b) / 2) < 1.6:
        anchors.append((best, b))       # next word starts at pause end
anchors = sorted(set(anchors))
def tmap(p):
    for (p0, t0), (p1, t1) in zip(anchors, anchors[1:]):
        if p0 <= p <= p1:
            return t0 + (p - p0) / max(1, p1 - p0) * (t1 - t0)
    return speech_end
res = [{"word": w, "start": round(tmap(cum[i]), 3), "end": round(tmap(cum[i] + len(w)), 3)} for i, w in enumerate(words)]
(HERE / "vo" / "align.json").write_text(json.dumps({"words": res, "pauses": pauses, "anchors": anchors}, indent=0))
print(len(words), "kata; anchors:", [(round(t, 2)) for _, t in anchors])
for i in range(0, len(res), 12):
    print(" ".join(f"{r['word']}@{r['start']}" for r in res[i:i + 4]))
