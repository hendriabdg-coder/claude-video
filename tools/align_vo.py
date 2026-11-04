"""Perkiraan timestamp per kata untuk VO yang dibuat manual (tanpa scene_NN.json dari tools/tts.py).

Dipakai di sesi cloud: VO dibuat Endrich di ElevenLabs lalu diunggah, jadi tidak ada timestamp kata.
Cara kerja: deteksi jeda (ffmpeg silencedetect) -> potongan bicara; naskah dipecah per frasa (tanda baca);
frasa dibagi ke potongan bicara lewat DP (durasi ~ jumlah suku kata); dalam satu potongan, kata dibagi
proporsional suku kata. Akurasi kira-kira 0,1-0,3 dtk, cukup untuk teks kata kunci (bukan subtitle).

  python tools/align_vo.py VO.mp3 naskah.txt OUT.json [--noise -38] [--min-sil 0.12]
naskah.txt = teks persis yang dibacakan (pakai angka dalam huruf). Hasil OUT.json mengikuti format
scene_NN.json: {"duration": .., "words": [{"word", "start", "end"}]}.
"""
import argparse
import json
import re
import subprocess


def speech_chunks(path, noise, min_sil):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"silencedetect=noise={noise}dB:d={min_sil}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    chunks, t = [], 0.0
    for s, e in zip(starts, ends + [dur] * (len(starts) - len(ends))):
        if s - t > 0.08:
            chunks.append((t, s))
        t = e
    if dur - t > 0.08:
        chunks.append((t, dur))
    return chunks, dur


def syl(w):
    return max(1, len(re.findall(r"[aiueo]+", w.lower())))


def phrases(text):
    out = []
    for p in re.split(r"(?<=[,.?!…])\s+|\.\.\.\s*", text.replace("\n", " ")):
        ws = p.split()
        if ws:
            out.append(ws)
    return out


def align(chunks, phr):
    n, m = len(phr), len(chunks)
    s = [sum(syl(w) for w in p) for p in phr]
    k = sum(b - a for a, b in chunks) / sum(s)
    INF = float("inf")
    # dp[i][j]: best cost putting first i phrases into first j chunks (each chunk >= 1 phrase, or merged chunks)
    # allow a phrase group to span several chunks too (speaker paused mid-phrase): groups map to chunk ranges.
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    bk = [[None] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            if dp[i][j] == INF:
                continue
            for i2 in range(i + 1, min(n, i + 4) + 1):
                for j2 in range(j + 1, min(m, j + 4) + 1):
                    if i2 - i > 1 and j2 - j > 1:
                        continue
                    d = chunks[j2 - 1][1] - chunks[j][0]
                    c = dp[i][j] + (d - k * sum(s[i:i2])) ** 2
                    if c < dp[i2][j2]:
                        dp[i2][j2], bk[i2][j2] = c, (i, j)
    groups, i, j = [], n, m
    while (i, j) != (0, 0):
        pi, pj = bk[i][j]
        groups.append((pi, i, pj, j))
        i, j = pi, pj
    words = []
    for pi, i, pj, j in reversed(groups):
        ws = [w for p in phr[pi:i] for w in p]
        segs = chunks[pj:j]
        tot = sum(b - a for a, b in segs)
        sy = [syl(w) for w in ws]
        tsum, acc = sum(sy), 0.0

        def at(x):  # x = speaking-time offset inside this group -> absolute time
            for a, b in segs:
                if x <= b - a + 1e-9:
                    return a + x
                x -= b - a
            return segs[-1][1]
        for w, v in zip(ws, sy):
            st, acc = at(acc), acc + tot * v / tsum
            words.append({"word": w, "start": round(st, 3), "end": round(at(acc), 3)})
    return words, groups


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("vo"); ap.add_argument("text"); ap.add_argument("out")
    ap.add_argument("--noise", type=float, default=-38); ap.add_argument("--min-sil", type=float, default=0.12)
    a = ap.parse_args()
    chunks, dur = speech_chunks(a.vo, a.noise, a.min_sil)
    phr = phrases(open(a.text, encoding="utf-8").read())
    words, groups = align(chunks, phr)
    json.dump({"duration": round(dur, 3), "words": words, "source": "align_vo.py (perkiraan dari jeda)"},
              open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for pi, i, pj, j in reversed(groups):
        print(f"{chunks[pj][0]:6.2f}-{chunks[j - 1][1]:6.2f}  {' '.join(w for p in phr[pi:i] for w in p)}")
