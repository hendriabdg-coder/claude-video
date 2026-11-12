# Rakit audio lagu pop jazz "Kopi, Laptop, dan Kamu" ±60 dtk (opsi A):
#   intro percakapan (Endrich = clone "Endrich - VO", AI = "Velora" perempuan) + ketikan/notif chat,
#   lalu lagu Eleven Music take A; break "Kamu belajar di mana? / Di kolom chat… tiap malam." diganti TTS di atas instrumental.
# Keluaran: audio/preview.wav (vokal panduan AI), audio/karaoke.wav (instrumental + semua dialog, untuk rekaman Endrich),
#           audio/panduan_vokal.wav (vokal panduan sejajar timeline final). Timeline lagu dicatat di audio/timeline.json.
import json, subprocess
from pathlib import Path
import numpy as np

A = Path(__file__).resolve().parent / "audio"
SR = 48000


def load(p, ch=2, af=None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(p)] + (["-af", af] if af else []) + ["-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.check_output(cmd), np.float32).reshape(-1, ch).copy()


TRIM = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
lines = [("d1_endrich", 0.35), ("d2_ai", None), ("d3_endrich", None), ("d4_ai", None), ("d5_endrich", None), ("d6_ai", None)]
GAP = 0.14
dlg, t, marks = [], 0.0, []
for name, at in lines:
    x = load(A / f"{name}.mp3", af=TRIM + ",atempo=1.06")
    t = at if at is not None else t + GAP
    dlg.append((t, x)); marks.append([name, round(t, 2), round(t + len(x) / SR, 2)]); t += len(x) / SR
SONG0 = round(t - 0.35, 3)                    # Rhodes masuk menimpa ujung tawa "Mulai, ya"
song, inst, voc = load(A / "songA.mp3"), load(A / "instrumental.wav"), load(A / "vocal_iso.mp3")
END_SONG = 47.7                                # lagu selesai setelah "mulai malam ini", fade 1,2 dtk
n_song = int(END_SONG * SR)
song, inst, voc = song[:n_song], inst[:n_song], voc[:n_song]
fade = np.ones(n_song, np.float32); f = int(1.2 * SR); fade[-f:] = np.linspace(1, 0, f)
song *= fade[:, None]; inst *= fade[:, None]; voc *= fade[:, None]
# break dialog replaces 30.0-33.6 of the song
BR = (38.2, 42.8)
b1, b2 = load(A / "b1_ai.mp3", af=TRIM), load(A / "b2_endrich.mp3", af=TRIM + ",atempo=1.08")
w = np.zeros(n_song, np.float32); i0, i1, ff = int(BR[0] * SR), int(BR[1] * SR), int(0.05 * SR)
w[i0:i1] = 1; w[i0 - ff:i0] = np.linspace(0, 1, ff); w[i1:i1 + ff] = np.linspace(1, 0, ff)
total = int((SONG0 + END_SONG + 0.6) * SR)


def place(buf, x, at, g=1.0):
    s = int(at * SR); e = min(len(buf), s + len(x)); buf[s:e] += x[:e - s] * g


def build(with_guide):
    out = np.zeros((total, 2), np.float32)
    for at, x in dlg:
        place(out, x, at, 1.0)
    # intro foley: typing under Endrich lines, chat pop under AI lines
    ty, po = load(A / "typing.mp3"), load(A / "pop.mp3")[: int(0.35 * SR)]
    for (name, s, e) in marks:
        if "endrich" in name: place(out, ty[: int(min(e - s, 1.0) * SR)], s - 0.9 if s > 1 else 0.0, 0.18)
        else: place(out, po, s - 0.15, 0.35)
    body = (song if with_guide else inst) * (1 - w[:, None]) + inst * w[:, None]
    if not with_guide:
        body = inst.copy()
    place(out, body, SONG0, 1.0)
    place(out, b1, SONG0 + 38.3, 1.1); place(out, b2, SONG0 + 40.1, 1.1)
    return out


def save(x, name, norm=True):
    af = "alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000" if norm else "aresample=48000"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af", af, str(A / name)],
                   input=x.astype(np.float32).tobytes(), check=True)


save(build(True), "preview.wav"); save(build(False), "karaoke.wav")
ven = A / "vocal_endrich.mp3"
if ven.exists():   # opsi 2: nyanyian panduan diubah ke clone Endrich (Voice Changer), diproses lalu ditaruh di atas instrumental
    ve = load(ven, af="highpass=f=90,acompressor=threshold=0.12:ratio=3:attack=8:release=120:makeup=1.5,aecho=0.8:0.5:60:0.10")[:n_song]
    ve = np.pad(ve, ((0, max(0, n_song - len(ve))), (0, 0)))[:n_song] * fade[:, None]
    out = build(False); place(out, ve * (1 - w[:, None]) * 1.05, SONG0); save(out, "lagu_endrich.wav")
g = np.zeros((total, 2), np.float32); place(g, voc * (1 - w[:, None]), SONG0); save(g, "panduan_vokal.wav", norm=False)
json.dump({"song0": SONG0, "end": round(SONG0 + END_SONG + 0.6, 2), "intro": marks, "break": [SONG0 + 38.3, SONG0 + 40.1]},
          open(A / "timeline.json", "w"), indent=1)
print("song0", SONG0, "total", round(total / SR, 2), marks)
