"""Bedah video referensi jadi data yang bisa dibaca reviewer.

Pakai:  python tools/bedah_referensi.py referensi/viral [--visual-only | --transcript-only]

Untuk tiap video di <folder>/motion dan <folder>/hybrid, tulis ke <folder>/kartu/_data/<nama>/:
  sheet.jpg    contact sheet (maks ~60 frame, tiap 1 dtk untuk video <= 60 dtk)
  awal3.jpg    6 frame di 0-2,5 dtk (bedah hook)
  data.json    durasi, titik potong scene, rata-rata panjang shot, transkrip + kata/detik
"""
import json
import os
import re
import subprocess
import sys
import wave
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

EXT = {".mp4", ".mov", ".m4v", ".webm"}


def slug(name):
    s = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()
    return s[:60] or "video"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def durasi(f):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]).stdout
    return float(out.strip() or 0)


def visual(f, out, dur):
    step = max(1.0, dur / 60)
    n = int(dur / step) + 1
    cols = 8
    rows = (n + cols - 1) // cols
    run(["ffmpeg", "-y", "-v", "error", "-i", str(f), "-vf",
         f"fps=1/{step},scale=200:-2,tile={cols}x{rows}:padding=4:color=white", "-frames:v", "1",
         str(out / "sheet.jpg")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(f), "-t", "3", "-vf",
         "fps=2,scale=270:-2,tile=6x1:padding=4:color=white", "-frames:v", "1", str(out / "awal3.jpg")])
    # titik potong scene
    r = run(["ffmpeg", "-v", "info", "-i", str(f), "-vf", "select='gt(scene,0.3)',showinfo", "-an", "-f", "null", "-"])
    cuts = [round(float(m), 2) for m in re.findall(r"pts_time:([\d.]+)", r.stderr)]
    shots = len(cuts) + 1
    return {"durasi": round(dur, 2), "langkah_sheet_dtk": round(step, 2), "potongan": cuts,
            "jumlah_shot": shots, "rata_panjang_shot_dtk": round(dur / shots, 2)}


_model = None


def transkrip(f, out):
    global _model
    import numpy as np
    from faster_whisper import WhisperModel
    if _model is None:
        _model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
    wav = out / "_audio.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(f), "-ac", "1", "-ar", "16000", str(wav)])
    with wave.open(str(wav)) as w:
        audio = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype("float32") / 32768
    segs, info = _model.transcribe(audio, word_timestamps=True, vad_filter=True)
    seg_out, words = [], []
    for s in segs:
        seg_out.append({"mulai": round(s.start, 2), "selesai": round(s.end, 2), "teks": s.text.strip()})
        words += [(w.start, w.end) for w in (s.words or [])]
    wav.unlink(missing_ok=True)
    bicara = sum(e - s for s, e in words) or 1
    awal3 = " ".join(x["teks"] for x in seg_out if x["mulai"] < 3)
    return {"bahasa": info.language, "segmen": seg_out, "jumlah_kata": len(words),
            "kata_per_dtk_bicara": round(len(words) / bicara, 2),
            "kata_per_dtk_total": round(len(words) / max(durasi(f), 1), 2),
            "kata_pertama_dtk": round(words[0][0], 2) if words else None, "ucapan_3dtk_awal": awal3}


def main():
    root = Path(sys.argv[1])
    mode = sys.argv[2] if len(sys.argv) > 2 else ""
    for jenis in ("motion", "hybrid"):
        for f in sorted((root / jenis).glob("*")):
            if f.suffix.lower() not in EXT:
                continue
            out = root / "kartu" / "_data" / f"{jenis}-{slug(f.stem)}"
            out.mkdir(parents=True, exist_ok=True)
            dj = out / "data.json"
            data = json.loads(dj.read_text(encoding="utf-8")) if dj.exists() else {}
            data.update({"file": str(f.relative_to(root)), "jenis": jenis})
            if mode != "--transcript-only":
                data.update(visual(f, out, durasi(f)))
            if mode != "--visual-only":
                data["transkrip"] = transkrip(f, out)
            dj.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            print("ok", out.name, flush=True)


if __name__ == "__main__":
    main()
