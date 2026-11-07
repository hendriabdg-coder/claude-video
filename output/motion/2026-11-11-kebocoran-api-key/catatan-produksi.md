# Catatan produksi · 3 Kesalahan yang Bikin API Key Kamu Bocor

## Ringkas
- MOTION, 69,7 dtk (VO 66,7 dtk + CTA layar 2,8 dtk). Slug sementara `2026-11-11-kebocoran-api-key`, mengisi slot Hari 11. Topik Hari 11 di Notion sebenarnya "Server MCP Berbahaya", jadi tolong konfirmasi tanggal tayangnya.
- Gaya sama dengan Hari 10: dasar PULSE, plus SIGNAL / TERMINAL / PAPER / AVATAR, plus Three.js. **Tempo dipercepat:** elemen masuk dalam 0,16-0,22 dtk (Hari 10: 0,26-0,4), visual berganti tiap ±1,5-2 dtk, rotasi 3D ±1,6x lebih cepat, flash tipis di tiap pergantian bab, dan teks berulang di latar bergerak lebih cepat.
- Animasi 3D:
  1. kunci API yang memerah lalu bocor jadi partikel;
  2. grafik commit git (commit lama menyimpan key, commit baru tidak menghapusnya);
  3. hujan ±1.400 "secret" saat angka 28,65 juta;
  4. brankas yang menutup setelah kunci masuk (back-end).

## Perlu dicek / diputuskan Endrich
1. **Gate dilewati:** VO dibuat sebelum riset dan naskah direview (gate 1-2). Fakta dicek setelahnya (riset.md). Tidak ada klaim yang salah; dua hal dilunakkan di layar:
   - angka di layar memakai **28,65 juta** (sumber), sedangkan VO menyebut "sekitar 28,6 juta" (masih wajar);
   - jalur bocor lewat screenshot / log / chat AI **tidak bersumber GitGuardian**, jadi di layar berlabel SIMULASI dan tidak dikaitkan ke angka itu.
2. **VO tidak punya CTA seri dan CTA komentar.** Keduanya ditambahkan di layar saja (tombol Follow + "SERI KEAMANAN AI", pertanyaan A/B "Udah aku cek / Belum pernah") selama 2,8 dtk di ujung, dan di caption. Kalau mau lebih kuat, tambah 1 kalimat VO di akhir.
3. **Durasi 69,7 dtk**, lewat batas 45 dtk.
4. **Label seri** "Keamanan AI" masih usulan; HUD menulis "KEAMANAN AI · API KEY".
5. Halaman primer (GitGuardian, docs GitHub, OpenAI) belum dibuka langsung; isi riset dari ringkasan hasil pencarian.
6. Ditambahkan di layar: "SUDAH BOCOR? GANTI (ROTASI) KEY" (rekomendasi GitHub/OpenAI), karena VO tidak menyebut rotasi.

## Audio
- `mix.py`: 51 cue SFX (ElevenLabs), musik Eleven Music di -14,0 dB (diukur supaya ±13,5 dB di bawah VO setelah ducking), hentakan di 0 dtk. Hasil -14,4 LUFS, TP -1,3 dBFS.
- Biaya ElevenLabs reel ini: ±950 kredit (musik 900, 3 SFX baru × 17). 11 SFX lain dipakai ulang dari Hari 10.

## Timing
- Timing kata adalah estimasi (Whisper-small per jeda, dibagi per suku kata; `align.py`), jadi sinkronnya per frasa.

## QC
- Frame dicek di `motion/proyek/<slug>/qa/grid.jpg`. Jeda statis "KALAU BOCOR:" dipendekkan dari 3,1 jadi 2,3 dtk.
- QC final reviewer-konten (1 putaran): 0 BLOKIR.
  - PERBAIKI diterapkan: "API KEY-MU AMAN?" muncul di 0,5 dtk (topik di 3 dtk pertama); cover diberi label "SERI KEAMANAN AI #1".
  - SARAN diterapkan: caption diperjelas ("terdeteksi di commit", "key di front-end bisa terbaca lewat browser"); janji "tips tiap minggu" dihapus dari layar.
  - Masih terbuka (keputusan Endrich): gate dilewati, durasi 69,7 dtk, CTA hanya di layar, cek halaman GitGuardian asli.
- Final: -14,4 LUFS, TP -1,3 dBFS.
