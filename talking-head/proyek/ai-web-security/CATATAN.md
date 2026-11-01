# Catatan edit — Keamanan website buatan AI

## Hasil
- `EndrichTech_AI_Web_Security_Final.mp4` — 1080×1920, 30 fps, 29,73 dtk, H.264 High + AAC 192k, faststart. Dialog asli + SFX tipis, −14,0 LUFS, true peak −1,5 dBFS.
- `EndrichTech_AI_Web_Security_VoiceOnly.mp4` — visual sama, audio dialog saja (kalau mau isi SFX/musik sendiri di CapCut).
- `EndrichTech_AI_Web_Security_Final.srt` — subtitle frasa (maks. 2 baris) sesuai ucapan aktual. **Tidak di-burn** ke video (aturan kanal: teks kata kunci, bukan subtitle penuh). Import ke CapCut kalau mau dipakai.
- `event-map.md` — peta ucapan → waktu → shot → event motion, daftar SFX & aset.
- Source yang bisa direvisi: `videos/ai-web-security/public/index.html` (HyperFrames + GSAP), `mix.py` (audio), `words.json` (transkrip per kata).

## Apa yang diubah
- Video tidak dipotong: durasi, cut, angle, dan sinkron bibir sama persis dengan sumber.
- Overlay grafis 10 beat sesuai storyboard (headline serif putih, aksen cyan, amber hanya untuk risiko). Semua elemen dibuat dengan kode/SVG; tanpa gambar AI, logo produk, atau kredensial nyata (`API_KEY = "DEMO_ONLY"`).
- Mockup (jendela website, kartu kode, field input, bubble "Beres!") diberi label kecil `ILUSTRASI`. Checklist memakai kotak + titik sorot, bukan centang hijau.
- Audio: tidak ada noise reduction karena sumber sudah bersih (jeda −45 s/d −59 dB, tanpa musik bawaan). Hanya normalisasi + limiter.

## Selisih naskah tertulis vs ucapan aktual
| Naskah tertulis | Yang diucapkan | Penanganan |
|---|---|---|
| "Kunci API bisa bocor…" | "**Contohnya,** kunci API…" | ikut audio |
| "akses admin nggak dibatasi, atau input…" | "**belum lagi** akses admin…, **dan** input…" | ikut audio |
| "Tiga hal ini bisa jadi celah keamanan." | "**itu** celah keamanan." | label `= CELAH KEAMANAN` (bukan "3 RISIKO") |
| "save dulu **video ini** biar nggak lupa. Follow juga biar nggak ketinggalan tips keamanan AI lainnya." | "save dulu biar nggak lupa, dan follow buat tips keamanan AI lainnya." | label `FOLLOW untuk tips keamanan AI` |
| "Haru Tetap di uji sendiri!" | "harus tetap diuji sendiri" | SRT dinormalisasi: "Harus tetap diuji sendiri!" |
Tidak ada kalimat yang hilang dari audio; tidak ada TTS tambahan.

## Pengecekan
- Contact sheet 2 fps seluruh video: wajah tidak tertutup; buku, aliran air, gelas, dan gestur jari bebas; tidak ada teks bertumpuk atau nyangkut; 0 frame hitam.
- Durasi video 29,733 dtk = sumber, audio tidak drift (dialog di-mux langsung dari file mentah).
- Safe area: semua teks penting di y 880–1565, x ≥ 240 dan ≤ 930 (tidak menabrak tombol kanan IG).
- Temuan saat QC: render pertama menampilkan headline dengan font sans (nama font "Serif" bentrok dengan nama generik). Sudah diganti jadi "GeorgiaHL" dan dirender ulang; sudah dicek.

## Keterbatasan
- Font headline Georgia Bold adalah font bawaan Windows (sudah dipakai di video EndrichTech sebelumnya). Kalau mau 100% open-license, bisa diganti serif OFL (mis. Playfair/Fraunces) tanpa mengubah layout.
- Belum dicek di HP asli; cek sekali di preview IG sebelum posting.
- SFX Epidemic: pastikan @end.rich9 terdaftar di akun Epidemic (lisensi terikat channel).
