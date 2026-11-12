# Mix lagu "Aku Bukan Programmer": vokal suara clone Endrich (Voice Changer dari vokal Eleven Music) + instrumental
# (lagu dikurangi vokal hasil isolasi, instrumental.py A=2.5). Baris "AI" (Terus? / Ya udah, ketik aja / Ijazahmu apa?)
# diberi filter telepon supaya terdengar sebagai lawan bicara. Vokal ±5 dB di atas musik (lagu, bukan VO+bed).
#   python mix_lagu.py  ->  audio/lagu_endrich.mp3
import subprocess
from pathlib import Path

A = Path(__file__).resolve().parent / "audio"
AI = [(3.18, 3.72), (6.42, 7.80), (32.82, 33.90)]          # detik, dari silencedetect + Whisper
en = "+".join(f"between(t,{a},{b})" for a, b in AI)
fx = (f"[0:a]aformat=sample_rates=48000:channel_layouts=mono,highpass=f=90,"
      f"acompressor=threshold=0.12:ratio=3:attack=8:release=120:makeup=1.6,asplit=2[v1][v2];"
      f"[v1]volume='if({en},0,1)':eval=frame[lead];"
      f"[v2]volume='if({en},1,0)':eval=frame,highpass=f=450,lowpass=f=3200,acrusher=bits=10:mix=0.25,volume=1.3[ai];"
      f"[lead][ai]amix=inputs=2:normalize=0,aecho=0.8:0.6:45:0.12,pan=stereo|c0=c0|c1=c0[voc];"
      f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=-5dB[mus];"
      f"[voc][mus]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(A / "vocal_endrich.mp3"), "-i", str(A / "inst_2.5.wav"),
                "-filter_complex", fx, "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "192k", str(A / "lagu_endrich.mp3")], check=True)
print("ok", A / "lagu_endrich.mp3")
