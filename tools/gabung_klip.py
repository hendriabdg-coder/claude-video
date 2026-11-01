# Gabung klip talking head (Flow, 4-10 dtk) jadi satu video mentah utuh untuk review Endrich.
#   python tools/gabung_klip.py talking-head/mentah/<slug> [--fade 0]
# Input : <folder>/klip/*.mp4 (urut nama: klip_01.mp4, klip_02.mp4, ...).
#         <folder>/urutan.txt (opsional, dibuat otomatis saat pertama jalan): satu baris per klip,
#         "nama_file [mulai] [akhir]" dalam detik untuk memotong; baris diawali # dilewati; urutan baris = urutan video.
# Output: <folder>/gabungan.mp4 (1080x1920, 30 fps, AAC 48 kHz, tiap klip loudnorm -16 LUFS supaya volumenya rata)
#         <folder>/gabungan_cek.jpg (frame awal + akhir tiap klip, untuk cek sambungan)
#         <folder>/gabungan.txt (titik potong tiap klip di timeline gabungan)
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

W, H, FPS = 1080, 1920, 30


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height",
                        "-of", "json", str(p)], capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    return float(j["format"]["duration"]), v["width"], v["height"], any(s["codec_type"] == "audio" for s in j["streams"])


def natural(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]


def read_order(folder, clips):
    f = folder / "urutan.txt"
    if not f.exists():
        f.write_text("# urutan klip (atur ulang baris / tambah detik mulai & akhir untuk memotong), contoh: klip_03.mp4 0.4 7.8\n"
                     + "".join(f"{c.name}\n" for c in clips), encoding="utf-8")
    order = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"(.+?\.(?:mp4|mov|m4v|webm))\s*([\d.]+)?\s*([\d.]+)?$", line, re.I)
        if not m:
            sys.exit(f"urutan.txt: baris tidak terbaca: {line}")
        order.append((folder / "klip" / m[1], float(m[2]) if m[2] else None, float(m[3]) if m[3] else None))
    return order


def main():
    folder = Path(sys.argv[1]).resolve()
    fade = float(sys.argv[sys.argv.index("--fade") + 1]) if "--fade" in sys.argv else 0.0
    clips = sorted((p for p in (folder / "klip").glob("*") if p.suffix.lower() in (".mp4", ".mov", ".m4v", ".webm")), key=natural)
    if not clips:
        sys.exit(f"Tidak ada klip di {folder / 'klip'}")
    tmp = folder / "_norm"
    tmp.mkdir(exist_ok=True)
    parts, rows, t = [], [], 0.0
    for k, (src, a, b) in enumerate(read_order(folder, clips)):
        dur, w, h, has_audio = probe(src)
        a, b = a or 0.0, min(b or dur, dur)
        n = b - a
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,format=yuv420p")
        af = "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo"
        if fade:
            vf += f",fade=t=in:st=0:d={fade},fade=t=out:st={n - fade:.3f}:d={fade}"
            af += f",afade=t=in:st=0:d={fade},afade=t=out:st={n - fade:.3f}:d={fade}"
        out = tmp / f"{k:02d}.mp4"
        args = ["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{n:.3f}", "-i", str(src)]
        if not has_audio:
            args += ["-f", "lavfi", "-t", f"{n:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
        args += ["-map", "0:v:0", "-map", "0:a:0" if has_audio else "1:a:0", "-vf", vf, "-af", af,
                 "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)]
        subprocess.run(args, check=True)
        real = probe(out)[0]
        parts.append(out)
        rows.append((k + 1, src.name, w, h, has_audio, t, t + real))
        t += real
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    final = folder / "gabungan.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    "-movflags", "+faststart", str(final)], check=True)

    tw, th = 135, 240
    sheet = Image.new("RGB", (tw * 2 * 4, (th + 22) * ((len(rows) + 3) // 4)), "black")
    d = ImageDraw.Draw(sheet)
    for k, (i, name, *_ , s, e) in enumerate(rows):
        x0, y0 = (k % 4) * tw * 2, (k // 4) * (th + 22)
        for j, at in enumerate((s + 0.05, e - 0.1)):
            fp = tmp / f"_f{k}_{j}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at:.2f}", "-i", str(final), "-frames:v", "1",
                            "-vf", f"scale={tw}:{th}", str(fp)], check=True)
            sheet.paste(Image.open(fp), (x0 + j * tw, y0 + 22))
        d.text((x0 + 4, y0 + 4), f"#{i} | {name[:20]} | {s:.1f}-{e:.1f}s", fill="yellow")
    sheet.save(folder / "gabungan_cek.jpg", quality=85)

    lines = [f"#{i:<2} {s:6.2f} - {e:6.2f}  ({e - s:4.1f} dtk)  {name}  {w}x{h}{'' if au else '  TANPA AUDIO'}"
             for i, name, w, h, au, s, e in rows]
    (folder / "gabungan.txt").write_text("\n".join(lines) + f"\nTotal: {t:.2f} dtk\n", encoding="utf-8")
    shutil.rmtree(tmp)
    print("\n".join(lines), f"\nTotal: {t:.2f} dtk -> {final}", sep="")


if __name__ == "__main__":
    main()
