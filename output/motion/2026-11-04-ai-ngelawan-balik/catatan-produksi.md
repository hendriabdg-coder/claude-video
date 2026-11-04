# Catatan produksi: hari 4 · AI Ngelawan Balik

- Topik: diambil dari CTA hari 3, bukan Notion (Notion hari 4 = Genie 4). Endrich memutuskan tetap pakai topik ini (2026-11-04); Genie 4 dipindah ke hari 13, "AI Agent sebagai Karyawan Digital" ke hari 7. Hari 7 di Notion sekarang dobel dengan "Gemini 4 Carbon" (menunggu Endrich).
- Naskah: v1 (Claude) → versi Endrich (55,9 dtk, terlalu panjang) → v2 dipadatkan + CTA ke hari 5 Notion → Endrich menambah kata penghubung saat generate.
- VO: dibuat Endrich di ElevenLabs (sesi cloud tidak punya kunci). Durasi 41,3 dtk (di atas target 25-35, di bawah batas 45).
- Timestamp kata: `tools/align_vo.py` dengan teks persis dari Endrich (perkiraan dari jeda, ±0,1-0,3 dtk).
- Reviewer: review naskah oleh reviewer-konten tidak dijalankan (naskah direvisi langsung oleh Endrich). QC final belum.
- Gaya: SAMA DENGAN HARI 3 (permintaan Endrich): editorial neo-brutal krem/arang/oranye, judul Inter + aksen Fraunces miring, kartu ber-shadow, chibi setengah badan sepanjang video. Versi TERMINAL (preview v1) dibuang, kodenya di build_terminal_v1.py.
- Label SIMULASI di notif update.
- Audio (2026-11-04): SFX + musik disintesis sendiri (synth_audio.py), 24 cue (mix.py), musik ~13,5 dB di bawah VO dengan sidechain ducking, hentakan di 0 dtk, alimiter + loudnorm: -14,4 LUFS, TP -1,5 dBFS. final.mp4 42,5 dtk.
- Aset ElevenLabs (musik + 6 SFX, ±1.000 kredit) sudah digenerate tapi tidak terpakai: domain file ElevenLabs diblokir dari sesi cloud dan Endrich tidak bisa unduh dari HP. Lain kali di cloud langsung sintesis saja, jangan generate di ElevenLabs.
- Saran: pin/sorotan "Seri AI Pengawas" di profil (part 1-4 sudah ada).
