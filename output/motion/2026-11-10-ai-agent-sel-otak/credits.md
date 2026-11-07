# Credits

## Audio
- **VO:** suara clone Endrich (ElevenLabs, voice clone milik Endrich), di-generate manual oleh Endrich dari naskah yang disetujui. File: `vo/vo-full.mp3`.
- **Musik:** Eleven Music v2.5 (akun ElevenLabs Endrich, flow "Reel Hari 10 · musik + SFX"), 74 dtk, instrumental (dicek dengan Whisper: tanpa vokal). Prompt: electronic sains-tech minimal ±118 BPM, bagian tengah lebih ringan. Hak komersial mengikuti paket ElevenLabs Endrich.
- **SFX:** ElevenLabs Sound Effects (eleven_text_to_sound_v2), 12 file buatan sendiri dari prompt teks: hit_hook, tick, slam, whoosh, crack (pil), pop, shimmer, paper, typing, chain, buzz, stamp, confirm. Library Epidemic tidak dipakai di reel ini karena tidak tersedia di sesi cloud.
- File audio ada di `motion/proyek/2026-11-10-ai-agent-sel-otak/audio/` (tidak masuk git). Mixer: `mix.py` (42 cue).

## Visual
- Semua grafis dan objek 3D dibuat sendiri: HyperFrames (HTML + GSAP) dan Three.js r181 (otak tikus sebagai awan titik, 1.946 kubus agent, pil, heliks DNA, kartu laporan, dua gen, labu lab). Tidak ada logo atau tangkapan layar pihak lain. Nama OpenAI, PerturbAI, dan Scripps hanya ditulis sebagai teks sumber.
- Karakter chibi Endrich: `karakter/pose_fix` (aset Endrich), lip-flap dari level VO.
- Font: Inter Display.
- Label "SIMULASI" ada di log terminal agent. Label "ILUSTRASI 3D" ada di visual labu lab; di hook, chip sumber "PREPRINT · OPENAI, PERTURBAI, SCRIPPS · OKT 2026" menandai bahwa visual itu ilustrasi riset.
