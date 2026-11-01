---
name: spek-audio-vo
description: Spesifikasi audio reel Endrich Tech, yaitu VO suara clone (tools/tts.py, intonasi lama), SFX Epidemic, musik Eleven Music, level, ducking, dan loudness. Pakai di Tahap 3-4 saat generate VO, memilih SFX/musik, dan mixing.
---

# Spek audio & VO Endrich Tech

Baca `CLAUDE.md` bagian 5 dan 7.

## VO
- `python tools/tts.py naskah.txt --out DIR --model eleven_v4 --stability 0.35`
  - voice_id clone Endrich: `xV29wBiBgOzpCgTwBbDC`. Jangan mengubah voice_id atau membuat clone baru.
  - Dikunci **intonasi lama** yang disetujui: natural dan ekspresif, tidak dipercepat. Parameter speed diabaikan oleh v4, dan versi cepat sudah ditolak.
- Kata yang salah ucap ditambahkan ke `tools/pelafalan.json`.
- Potong hening berlebih di awal/akhir file dengan ffmpeg. Gabungkan segmen ke `vo-full.mp3`.
- Setelah generate: **STOP, Endrich dengar dulu (gate 3).**
- API key hanya di `.env`; jangan dibaca atau dicetak.

## SFX
- Library Epidemic `new sfx/`. Palet alias dan cara align onset/peak ada di `motion/gaya/gaya_sfx.py` (`P`, `analyse()`, `mix()`).
- Hentakan di 0-1 detik (hook). Selebihnya hemat: transisi, angka, kata kunci.
- Pastikan akun IG terdaftar di Epidemic. Catat file yang dipakai di `credits.md`.

## Musik
- Eleven Music: `client.music.compose(composition_plan={"chunks":[...]}, model_id="music_v2_5")`, tiap chunk ≥ 3000 ms, instrumental (negatif: vocals, singing, spoken words). Contoh di `motion/gaya/gaya_music.py`.
- Mood ikut topik: berita tegang = gelap/tegas, edukasi ringan = lebih terang.
- Jangan memakai lagu dari folder "Viral Songs".

## Mix (reel: `python motion/gaya/reel_sfx.py <slug>`; cue per reel di fungsi `cues_*`)
- `music_gain()` mengukur musik setelah ducking vs VO saat bicara dan mengatur gain supaya **~13,5 dB di bawah VO** (target 12-15). Volume tetap -7.5 dB terbukti tidak cukup untuk lagu Eleven Music yang keras (hasilnya cuma 10,5 dB).
- SFX di-duck ringan oleh VO.
- Bagian VO berbisik/pelan butuh dip musik tambahan.
- Akhir: `alimiter=limit=0.84` + `loudnorm=I=-14:TP=-1.5:LRA=11`. Cek dengan `ffmpeg -af ebur128`: sekitar -14 LUFS, true peak di bawah -1 dBFS.
