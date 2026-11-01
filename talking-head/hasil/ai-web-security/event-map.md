# Event map — EndrichTech_AI_Web_Security_Final

Sumber: `Editing Video Motion/Video Mentah.mp4` (1080×1920, 30 fps, 29,733 dtk). Tidak ada potongan; audio & sinkron bibir asli.
Timing ucapan = `words.json` (faster-whisper large-v3-turbo, timestamp per kata). Komposisi: `public/index.html` (HyperFrames + GSAP).

| Beat | Ucapan (waktu audio) | Shot sumber | Event motion | Posisi |
|---|---|---|---|---|
| 1 | "Bikin website pakai AI memang cepat" 0,00–2,04 | 0–2,10 meja laptop | `BIKIN`(0,00) `WEBSITE`(0,36) serif putih; label cyan `PAKAI AI` 0,70; garis cyan menyapu di "cepat" 1,60; keluar 2,62 | dada, y≈900–1100; laptop kiri bawah bebas |
| 2 | "tapi jangan … aman … tampilannya sudah rapi" 2,22–6,16 | 2,10 samping / 4,27 buku | `RAPI` 2,80, `≠` amber 3,44, `AMAN` 3,76; jendela website mini di "tampilannya" 4,94; penanda amber `!` di "rapi" 5,70; keluar 6,20 | headline dada; jendela kanan bawah (x 600–910), buku & tangan bebas |
| 3 | "kunci API bisa bocor di kode publik" 7,30–9,66 | 6,37 laptop | chip 01-02-03 + kartu `KUNCI API` 7,30; sublabel `Bocor di kode publik` 8,46; strip `API_KEY = "DEMO_ONLY"` 9,02, sorot amber 9,22 | kanan bawah x 380–930, y 1120–1450 |
| 4 | "akses admin nggak dibatasi" 10,60–12,10 | 9,97 meja+gelas | kartu 1 keluar → `HAK AKSES` 10,60; sublabel `Admin tidak dibatasi` 11,36; chip 02 aktif | sama; gelas kiri bebas |
| 5 | "input pengguna nggak divalidasi" 12,56–14,04 | 12,37 menuang air | `VALIDASI INPUT` 12,56; field netral "ketik nama kamu..." 12,86; sublabel 13,24; segitiga peringatan 13,50 | sama; teko, aliran air, gelas di kiri tidak tertutup |
| 6 | "itu celah keamanan" 14,24–15,30 | 12,37 / 15,13 close | tiga label bertumpuk 14,10–14,26; pill amber `= CELAH KEAMANAN` 14,50; keluar 15,36 | kanan bawah |
| 7 | "save dulu biar nggak lupa" 15,80 / "follow buat tips keamanan AI lainnya" 17,40 | 15,13 close / 17,07 lebar | bookmark outline + `SIMPAN DULU` 15,80–17,22; `FOLLOW untuk tips keamanan AI` 17,40–19,62 | pill kecil y≈1240, tengah; tangan & gelas bebas |
| 8 | "Sebelum website dirilis, cek lagi tiga hal tadi, kunci API, hak akses, dan validasi input" 19,84–25,32 | 19,93 teras / 22,93 gestur jari | panel `CEK SEBELUM RILIS` 20,66; tiga baris 21,84; sorot baris di 22,98 / 23,80 / 24,58 (kotak kosong berisi titik cyan, **bukan centang hijau**); keluar 25,40 | bawah x 240–900, y 1330–1560; jari & gelas bebas |
| 9 | "Jangan cuma percaya AI bilang beres" 25,50–27,52 | 25,37 teras | `JANGAN CUMA` 25,50, `PERCAYA` 26,06 + garis amber 26,30; bubble `Beres!` + label `JAWABAN AI` 26,48 (pop di "beres" 27,06); keluar 27,80 | headline dada; bubble kanan kepala (x 690–930, y 430–600) |
| 10 | "harus tetap diuji sendiri" 28,00–29,42 | 27,37 penutup | `TETAP` 28,30, `DIUJI` cyan 28,66, `SENDIRI` 29,06; wordmark `EndrichTech` 28,30; tahan sampai akhir | dada; wordmark y≈1505 |

## SFX (Epidemic, `new sfx/`, level −20 s/d −26 dB relatif, dialog tetap dominan)
0,00 whoosh soft · 3,44 pop UI (≠) · 7,30 whoosh soft · 10,60 & 12,56 klik UI · 14,50 pop UI · 15,80 notif soft (simpan) · 20,66 whoosh soft · 22,98 / 23,80 / 24,58 marker highlight · 27,06 notif bubble.
Tanpa musik (sumber juga tidak mengandung musik; jeda ucapan −45 s/d −59 dB).

## Aset dipakai
| Aset | Sumber |
|---|---|
| Video + dialog | `Video Mentah.mp4` (pengguna) |
| Font headline | Georgia Bold (font bawaan Windows, dipakai juga di project sebelumnya) |
| Font label/kartu | Inter Display (SIL OFL, `.claude/skills/endrichtech-edit/assets/fonts/`) |
| Ikon kunci, user+perisai, field, bookmark, peringatan, jendela website, checklist, bubble | dibuat sebagai SVG/HTML di `public/index.html` |
| Wordmark | teks "EndrichTech" (bukan file logo) |
| SFX | Epidemic Sound (langganan aktif): Whoosh Softs; UI Click Pop Up Notification; UI Double Click Phone Tap; Text Message Confirm Round Soft; Highlight Drag Marker Highlighter; Text Message Round Tone Clicky |
| GSAP | `public/vendor/gsap.min.js` |
