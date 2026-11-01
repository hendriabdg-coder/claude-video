# SFX + musik untuk v2 (Endrich minta Claude yang mixing, CLAUDE.md bagian 7 + 13).
#   python th_audio.py music   -> musik.mp3 (Eleven Music, music_v2_5, instrumental, chunk >= 3000 ms)
#   python th_audio.py mix     -> hasil/<slug>/<slug>_final.mp4 (SFX Epidemic, musik ~13,5 dB di bawah suara, -14 LUFS, TP -1.5)
import os, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "motion/gaya"))
import reel_sfx                        # mengganti whoosh non-ES dengan ES (QC 2026-10-25)
from gaya_sfx import LIB, P, analyse

SLUG = HERE.name
SRC = ROOT / f"talking-head/hasil/{SLUG}/{SLUG}_motion_v2.mp4"
OUT = ROOT / f"talking-head/hasil/{SLUG}/{SLUG}_final.mp4"
MUSIC = HERE / "musik.mp3"
P["crack"] = "ES_Impact, Crack 05 - Epidemic Sound.mp3"
GAP_DB = 13.5
BOOST_DB = 2.6   # Endrich 2026-11-01: SFX + musik dinaikkan ~35% (20*log10(1.35))

def compose():
    from dotenv import load_dotenv
    from elevenlabs.client import ElevenLabs
    load_dotenv(ROOT / ".env")
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    pos = ["tech thriller", "clean pulsing analog synth bass", "tight electronic drums, ticking hi-hats", "subtle glitch textures",
           "AI security news, tense but not horror, 104 bpm"]
    neg = ["vocals", "singing", "spoken words", "happy", "acoustic", "orchestral epic", "lo-fi"]
    plan = [(4000, ["immediate start, sparse intro hit"] + pos),
            (47400, ["main groove, steady, leaves room for voice"] + pos),
            (5000, ["rising tension, building toward a reveal"] + pos),
            (3200, ["clean resolve, final hit and short tail"])]
    body = {"chunks": [{"text": "", "duration_ms": d, "positive_styles": ["instrumental", "background music for a short video"] + p,
                        "negative_styles": neg, "context_adherence": "high"} for d, p in plan]}
    audio = client.music.compose(composition_plan=body, model_id="music_v2_5", respect_sections_durations=True, output_format="mp3_44100_192")
    MUSIC.write_bytes(b"".join(audio))
    print("saved", MUSIC)

# (detik, sfx, dB, panjang maks, align) — onset = awal bunyi di t, peak = puncak bunyi di t
CUES = [
    (0.0, "hit_dark1", -8, 1.6, "onset"),
    (1.4, "wh_soft", -14, 1.0, "peak"), (1.5, "typing", -17, 0.6, "onset"), (2.84, "typing", -18, 0.4, "onset"),
    (3.6, "wh_swish", -15, 0.6, "peak"), (3.85, "wh_fast", -16, 0.4, "peak"), (4.38, "shimmer", -18, 0.8, "onset"), (5.24, "pop", -13, 0.25, "onset"),
    (7.52, "hit_deep", -9, 1.4, "onset"),
    (8.9, "wh_swish", -15, 0.6, "peak"), (9.0, "typing", -17, 0.5, "onset"), (10.62, "click_metal", -12, None, "onset"),
    (11.1, "glitch_tr", -12, 0.5, "peak"), (11.1, "neg", -13, 0.9, "onset"),
    (11.8, "wh_soft", -16, 1.0, "peak"), (13.14, "hit_thump", -12, 0.8, "onset"),
    (17.633, "wh_soft", -14, 1.0, "peak"), (18.933, "wh_swish", -15, 0.6, "peak"),
    (19.42, "hit_thump", -13, 0.6, "onset"), (19.74, "hit_thump", -12, 0.6, "onset"), (19.96, "hit_thump", -11, 0.6, "onset"),
    (20.72, "ui_open", -13, None, "onset"), (23.44, "ui_popup", -13, 0.6, "onset"),
    (25.2, "wh_soft", -16, 1.0, "peak"), (27.66, "ui_open", -13, None, "onset"), (29.44, "msg", -13, 0.8, "onset"),
    (32.7, "wh_fast", -15, 0.4, "peak"),
    (34.133, "wh_swish", -15, 0.6, "peak"), (35.5, "pop", -13, 0.25, "onset"),
    (38.3, "tick", -16, 1.0, "onset"), (39.3, "riser", -16, 2.5, "peak"), (39.3, "ui_confirm", -13, None, "onset"),
    (41.6, "hit_washed", -12, 1.0, "onset"),
    (45.78, "hit_deep", -11, 1.2, "onset"), (46.6, "wh_swish", -14, 0.5, "peak"),
    (51.367, "wh_cine", -14, 1.2, "peak"), (52.64, "pop", -12, 0.25, "onset"), (52.9, "pop", -12, 0.25, "onset"),
    (54.06, "hit_dark1", -10, 1.2, "onset"), (55.32, "wh_impact", -12, 1.0, "peak"), (55.77, "crack", -10, 1.0, "onset"),
    (56.75, "ui_popup", -12, 0.6, "onset"), (57.48, "ui_confirm", -13, None, "onset"),
]

def music_gain(probe=-7.5):
    fx = (f"[0:a]aformat=sample_rates=48000:channel_layouts=mono,asplit=2[v][k];[1:a]aformat=sample_rates=48000:channel_layouts=mono,"
          f"volume={probe}dB[m0];[m0][k]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=350[m]")
    tmp = {k: HERE / f"_{k}.raw" for k in ("v", "m")}
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SRC), "-i", str(MUSIC), "-filter_complex", fx,
                    "-map", "[v]", "-f", "s16le", str(tmp["v"]), "-map", "[m]", "-f", "s16le", str(tmp["m"])], check=True)
    v, m = (np.fromfile(tmp[k], np.int16).astype(np.float32) / 32768 for k in ("v", "m"))
    for f in tmp.values():
        f.unlink()
    n = min(len(v), len(m)) // 4800 * 4800
    rv, rm = (20 * np.log10(np.sqrt((x[:n].reshape(-1, 4800) ** 2).mean(1)) + 1e-9) for x in (v, m))
    act = rv > rv.max() - 20
    return round(probe - (GAP_DB - float(np.median(rv[act] - rm[act]))), 1)

def mix():
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(SRC)]))
    args, chains = ["ffmpeg", "-v", "error", "-y", "-i", str(SRC), "-i", str(MUSIC)], []
    for k, (t, alias, db, maxlen, align) in enumerate(sorted(CUES, key=lambda c: c[0]), start=2):
        pk, tpeak, tonset = analyse(alias)
        start = tonset if align == "onset" else max(tpeak - 0.6, 0)
        at = t if align == "onset" else t - (tpeak - start)
        args += ["-ss", f"{start:.3f}", "-i", str(LIB / P[alias])]
        trim = f"atrim=0:{maxlen:.3f},afade=t=out:st={max(maxlen - 0.2, 0):.3f}:d=0.2," if maxlen else ""
        chains.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,{trim}volume={db - pk + BOOST_DB:.2f}dB,"
                      f"adelay={int(round(max(at, 0) * 1000))}:all=1[s{k}]")
    n = len(CUES)
    fx = ";".join(chains)
    fx += f";{''.join(f'[s{k}]' for k in range(2, n + 2))}amix=inputs={n}:normalize=0:duration=longest,atrim=0:{dur:.3f}[bed]"
    fx += ";[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=3[voice][k1][k2]"
    fx += ";[bed][k1]sidechaincompress=threshold=0.06:ratio=2:attack=10:release=180[sfx]"
    gain = round(music_gain() + BOOST_DB, 1)
    fx += f";[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{dur:.3f},volume={gain}dB,afade=t=out:st={dur - 1.2:.3f}:d=1.2[mus0]"
    fx += ";[mus0][k2]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=350[mus]"
    fx += ";[voice][sfx][mus]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.84,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]"
    subprocess.run(args + ["-filter_complex", fx, "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                           "-movflags", "+faststart", str(OUT)], check=True)
    print(n, "cues, musik", gain, "dB ->", OUT)

if __name__ == "__main__":
    {"music": compose, "mix": mix}[sys.argv[1]]()
