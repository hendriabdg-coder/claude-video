# Mix SFX + musik reel hari 4 (CLAUDE.md §7). Sesi cloud tidak punya library Epidemic `new sfx/`, jadi SFX + musik
# dibuat lewat ElevenLabs (flow "Reel Hari 4 - AI Ngelawan Balik (audio)") dan disimpan di audio/:
#   musik.mp3 (Eleven Music v2.5) · hit, whoosh, pop, glitch, ding, tick .mp3 (Sound Effects v2)
# Logika sama dengan motion/gaya/reel_sfx.py: gain musik diukur per lagu supaya ~13,5 dB di bawah VO saat bicara
# (setelah sidechain ducking), hentakan di 0 dtk, alimiter + loudnorm -14 LUFS / TP -1.5.
#   python mix.py            -> renders/final.mp4
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
import gaya_sfx  # noqa: E402
from reel_common import ROOT, VO_START  # noqa: E402
from reel_sfx import music_gain  # noqa: E402

SLUG = "2026-11-04-ai-ngelawan-balik"
AUD = HERE / "audio"
for k in ("hit", "whoosh", "pop", "glitch", "ding", "tick"):
    gaya_sfx.P["d4_" + k] = str(AUD / f"{k}.mp3")   # absolute path: LIB / abs == abs
WD = json.loads((ROOT / "output" / "motion" / SLUG / "vo" / "vo-full.json").read_text(encoding="utf-8"))["words"]


def at(word, n=1):
    k = 0
    for w in WD:
        if w["word"].lower().strip(",.?!").startswith(word.lower()):
            k += 1
            if k == n:
                return round(w["start"] + VO_START, 3)
    raise KeyError(f"{word} #{n}")


def cues():
    A = {k: at(*v) for k, v in {
        "dalam": ("dalam",), "celah1": ("celah",), "masalah": ("masalahnya",), "setengah": ("setengah",), "dan0": ("dan",),
        "disiapin": ("disiapin",), "untung": ("untungnya",), "ditambal1": ("ditambal",), "tapi": ("tapi",), "mei": ("mei",),
        "lima": ("lima",), "tujuh": ("tujuh",), "dan": ("dan", 2), "kalau1": ("kalau",), "pasang1": ("pasang",),
        "besok": ("besok",), "alat": ("alat",), "follow": ("follow",), "kalau2": ("kalau", 2),
        "langsung": ("langsung",), "nunggu": ("nunggu",)}.items()}
    SC = [A["masalah"] - 0.1, A["dan0"] - 0.1, A["tapi"] - 0.08, A["mei"] - 0.1, A["dan"] - 0.1, A["besok"] - 0.1, A["kalau2"] - 0.1]
    C = [(0.0, "d4_hit", -8, 1.6, "onset"),                                   # hentakan 0-1 dtk
         (A["dalam"] + 0.2, "d4_tick", -19, A["celah1"] - A["dalam"] + 0.2, "onset"),   # counter 129.000
         (A["celah1"] + 0.2, "d4_pop", -12, 0.3, "onset")]
    C += [(t, "d4_whoosh", -15, 0.8, "peak") for i, t in enumerate(SC) if i != 2]       # pergantian scene
    C += [(SC[2], "d4_glitch", -13, 0.8, "onset"), (SC[2] + 0.02, "d4_hit", -11, 1.2, "onset")]  # "Tapi lihat ini."
    C += [(A["setengah"], "d4_pop", -13, 0.3, "onset"),
          (A["disiapin"] - 0.3, "d4_pop", -14, 0.3, "onset"), (A["untung"] - 0.2, "d4_pop", -14, 0.3, "onset"),
          (A["ditambal1"], "d4_pop", -13, 0.3, "onset"),
          (A["lima"], "d4_tick", -19, 0.9, "onset"), (A["tujuh"], "d4_tick", -19, 0.6, "onset"),
          (SC[4] + 0.15, "d4_ding", -13, 1.2, "onset"),                      # notifikasi update muncul
          (A["pasang1"], "d4_pop", -11, 0.3, "onset"),
          (A["alat"] - 0.1, "d4_pop", -14, 0.3, "onset"),
          (A["follow"] + 0.75, "d4_ding", -14, 1.0, "onset"),                # Follow -> Following
          (SC[6] + 0.02, "d4_hit", -12, 1.2, "onset"),
          (A["langsung"], "d4_pop", -13, 0.3, "onset"), (A["nunggu"], "d4_pop", -13, 0.3, "onset")]
    return C


def mix():
    src, out = HERE / "renders" / "visual_v2.mp4", HERE / "renders" / "final.mp4"
    music = HERE / "public" / "music.mp3"
    subprocess.run(["cp", str(AUD / "musik.mp3"), str(music)], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)]))
    C = sorted(cues())
    args, chains = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-i", str(music)], []
    for k, (t, alias, db, maxlen, align) in enumerate(C, start=2):
        pk, tpeak, tonset = gaya_sfx.analyse(alias)
        start = tonset if align == "onset" else max(tpeak - 0.6, 0)
        t_at = t if align == "onset" else t - (tpeak - start)
        args += ["-ss", f"{start:.3f}", "-i", gaya_sfx.P[alias]]
        trim = f"atrim=0:{maxlen:.3f},afade=t=out:st={max(maxlen - 0.2, 0):.3f}:d=0.2," if maxlen else ""
        chains.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,{trim}volume={db - pk:.2f}dB,"
                      f"adelay={int(round(max(t_at, 0) * 1000))}:all=1[s{k}]")
    n = len(C)
    fx = ";".join(chains)
    fx += f";{''.join(f'[s{k}]' for k in range(2, n + 2))}amix=inputs={n}:normalize=0:duration=longest,atrim=0:{dur:.3f}[bed]"
    fx += ";[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=3[voice][k1][k2]"
    fx += ";[bed][k1]sidechaincompress=threshold=0.06:ratio=2:attack=10:release=180[sfx]"
    gain = music_gain(HERE)
    fx += f";[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{dur:.3f},volume={gain}dB,afade=t=out:st={dur - 1.2:.3f}:d=1.2[mus0]"
    fx += ";[mus0][k2]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=350[mus]"
    fx += ";[voice][sfx][mus]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.84,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]"
    subprocess.run(args + ["-filter_complex", fx, "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                           "-movflags", "+faststart", str(out)], check=True)
    print(n, "cues, musik", gain, "dB ->", out)


if __name__ == "__main__":
    if "--cues" in sys.argv:
        for c in sorted(cues()):
            print(c)
    else:
        mix()
