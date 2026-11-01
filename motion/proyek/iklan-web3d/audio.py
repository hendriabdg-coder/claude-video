# Music bed (Eleven Music, 25 s) + Epidemic SFX + final mix for the web-3D ad, same recipe as motion/gaya/gaya_sfx.py
# (music -7.5 dB and ducked by the voice, SFX ducked lightly, loudnorm -14 LUFS / TP -1.5).
#   python audio.py music   -> public/music.mp3 (skips if it exists)
#   python audio.py mix     -> renders/final.mp4
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gaya"))
from gaya_sfx import LIB, P, analyse  # noqa: E402

VO_START = 0.3
d = json.loads((HERE / "vo" / "scene_01.json").read_text(encoding="utf-8"))
T = {i: round(w["start"] + VO_START, 3) for i, w in enumerate(d["words"])}


def music():
    out = HERE / "public" / "music.mp3"
    if out.exists():
        return
    from dotenv import load_dotenv
    from elevenlabs.client import ElevenLabs
    load_dotenv(HERE.parents[2] / ".env")
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    chunks = [(22000, ["modern upbeat product commercial", "punchy clean drums and finger snaps", "warm plucky synth and soft bass",
                       "premium, confident, persuasive tech ad, 112 bpm"], ["dark", "lo-fi", "aggressive"]),
              (3000, ["bright final hit and sparkle tail"], ["abrupt cut"])]
    plan = {"chunks": [{"text": "", "duration_ms": ms, "positive_styles": ["instrumental", "background music for a short video ad"] + p,
                        "negative_styles": ["vocals", "singing", "spoken words"] + n, "context_adherence": "high"} for ms, p, n in chunks]}
    audio = client.music.compose(composition_plan=plan, model_id="music_v2_5", respect_sections_durations=True,
                                 output_format="mp3_44100_192")
    out.write_bytes(b"".join(audio))
    print("saved", out)


def cues():
    C1 = T[10] + 3.267
    C2 = T[10] + 5.667
    return [(0.0, "hit_washed", -9, 1.2, "onset"), (0.05, "wh_fly", -13, 1.0, "peak"), (T[4], "pop", -12, 0.25, "onset"),
            (T[6], "wh_swish", -12, 0.6, "peak"), (T[8], "neg", -13, 0.8, "onset"),
            (T[10] - 0.15, "wh_fast", -11, 0.4, "peak"), (T[10] + 0.05, "hit_thump", -11, 1.0, "onset"),
            (T[16], "pop", -12, 0.25, "onset"), (T[16] + 0.1, "wh_soft", -16, 0.9, "peak"),
            (C1, "wh_cine", -12, 1.2, "peak"), (T[24], "pop", -12, 0.25, "onset"), (C2, "wh_swish", -12, 0.6, "peak"),
            (T[28] + 0.35, "click_dbl", -12, None, "onset"), (T[28], "pop", -12, 0.25, "onset"),
            (T[31] - 0.1, "wh_impact", -11, 1.2, "peak"), (T[32], "ui_popup", -14, 0.6, "onset"), (T[35], "pop", -12, 0.25, "onset"),
            (T[38] - 0.1, "wh_soft", -13, 1.0, "peak"), (T[44] - 0.1, "bubble", -12, 0.6, "onset"),
            (T[47], "hit_deep", -10, 1.4, "onset"), (T[47] + 0.05, "shimmer", -13, 1.6, "onset"), (T[48], "ui_confirm", -15, None, "onset")]


def mix():
    src, mus, out = HERE / "renders" / "visual.mp4", HERE / "public" / "music.mp3", HERE / "renders" / "final.mp4"
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)]))
    cs = sorted(cues())
    args, chains = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-i", str(mus)], []
    for k, (t, alias, db, maxlen, align) in enumerate(cs, start=2):
        pk, tpeak, tonset = analyse(alias)
        start = tonset if align == "onset" else max(tpeak - 0.6, 0)
        at = t if align == "onset" else t - (tpeak - start)
        args += ["-ss", f"{start:.3f}", "-i", str(LIB / P[alias])]
        trim = f"atrim=0:{maxlen:.3f},afade=t=out:st={max(maxlen - 0.2, 0):.3f}:d=0.2," if maxlen else ""
        chains.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,{trim}volume={db - pk:.2f}dB,"
                      f"adelay={int(round(max(at, 0) * 1000))}:all=1[s{k}]")
    n = len(cs)
    fx = ";".join(chains)
    fx += f";{''.join(f'[s{k}]' for k in range(2, n + 2))}amix=inputs={n}:normalize=0:duration=longest,atrim=0:{dur:.3f}[bed]"
    fx += ";[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=3[voice][k1][k2]"
    fx += ";[bed][k1]sidechaincompress=threshold=0.06:ratio=2:attack=10:release=180[sfx]"
    fx += f";[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{dur:.3f},volume=-7.5dB,afade=t=out:st={dur - 1.2:.3f}:d=1.2[mus0]"
    fx += ";[mus0][k2]sidechaincompress=threshold=0.05:ratio=2.5:attack=20:release=350[mus]"
    fx += ";[voice][sfx][mus]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.84,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[mix]"
    subprocess.run(args + ["-filter_complex", fx, "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                           "-movflags", "+faststart", str(out)], check=True)
    print(n, "cues ->", out)


if __name__ == "__main__":
    {"music": music, "mix": mix}[sys.argv[1]]()
