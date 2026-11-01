# Panduan Gaya Konten Motion: EndrichTech

Cara pakai: saat punya ide video, cukup bilang **"pakai gaya PAPER"** (atau SIGNAL / PULSE / TERMINAL / EMBER / AVATAR / SETUP / SHOWCASE / GUIDE / STORY MOTION).
Kalau tidak disebut, Claude akan menanyakan gaya mana yang mau dipakai. Workflow tetap sama:
riset, cek fakta, 3 skrip, VO (kamu review), visual (kamu review), lalu SFX dan musik.

Semua gaya memakai **suara clone Endrich (Eleven v4, stability 0.35)**, **tanpa subtitle**,
**SFX dari library Epidemic**, dan **musik Eleven Music sekitar 9–10 dB di bawah suara**.

| No | Gaya | Preview | Cocok untuk |
|---|---|---|---|
| 01 | **SIGNAL** | `01_SIGNAL_preview.mp4` | Explainer produk/fitur AI, tools, "apa itu X" |
| 02 | **PAPER** | `02_PAPER_preview.mp4` | Uang, biaya, data, simulasi, hitung-hitungan |
| 03 | **PULSE** | `03_PULSE_preview.mp4` | Opini, hot take, tips "3 hal", hook motivasi |
| 04 | **TERMINAL** | `04_TERMINAL_preview.mp4` | Keamanan siber, tutorial perintah, dev tips |
| bonus | **EMBER** | `05_EMBER_bonus_preview.mp4` | Cek fakta dramatis, berita besar (gaya Black October) |
| 06 | **AVATAR** | `06_AVATAR_preview.mp4` | Konten "ngobrol" dengan karakter kartun kamu: edukasi AI, sapaan, seri belajar |
| 07 | **SETUP** | `07_SETUP_preview.mp4` | Workflow, produktivitas, tools di layar, "cara aku bikin X" |
| 09 | **GUIDE** | `09_GUIDE_preview.mp4` | Tutorial langkah-langkah, "cara aku bikin X pakai AI", workflow 3-4 langkah, review tools |
| 08 | **SHOWCASE** | `08_SHOWCASE_preview.mp4` | **Iklan** jasa/produk, demo hasil kerja (website 3D, aplikasi, tools), "cara kerjanya 1-2-3" |
| 10 | **STORY MOTION** | `10_STORY_MOTION_preview.mp4` | **Storytelling** edukasi + iklan halus: cerita tokoh → masalah → fakta bersumber → perubahan (produk) → CTA seri + pertanyaan A/B |

---

## 01 · SIGNAL (sudah dipakai: Claude Duet)
- **Rasa:** rapi, techy, "dashboard produk".
- **Warna:** charcoal `#121314` + **lime** `#C6F432` + kartu krem `#F2EEE3`.
- **Ciri khas:** HUD seri "CEK AI · Nº", counter FRAME, progress bar, stepper bab; HP dan notifikasi; kartu izin dengan klik kursor; struk/receipt; kartu komentar diketik + tombol Follow.
- **Musik:** lo-fi electronic minimal. **SFX:** dominan UI (notifikasi, klik, ketik).

## 02 · PAPER (baru)
- **Rasa:** tenang, ramah, seperti infografis majalah; paling mudah dicerna.
- **Warna:** kanvas krem `#F1ECE2` + tinta `#1E1B18` + **oranye** `#D9622B`, ditambah lingkaran dekorasi samar.
- **Ciri khas:** objek flat (kartu, kalender, dompet) yang muncul dan menyusut; **angka menghitung naik**; kalender terisi titik; pill "ASUMSI ..." untuk kejujuran data.
- **Musik:** akustik lo-fi (petikan gitar/ukulele, perkusi lembut). **SFX:** pop, tap, tick saat menghitung, satu hentakan rendah untuk angka akhir.
- **Referensi:** ref-motion-3.

## 03 · PULSE (baru)
- **Rasa:** keras, cepat, percaya diri, cocok untuk hook dan opini.
- **Warna:** blok penuh layar bergantian: hitam `#0E0E0E`, **biru elektrik** `#3A5BFF`, **coral** `#FF4F3A`, krem `#F4F1EA`.
- **Ciri khas:** satu kata/frasa **raksasa** per potongan, hard cut tiap ketukan, huruf "dibanting" masuk, kamera bergetar, angka outline besar (1/2/3), teks berulang di latar.
- **Musik:** electronic energik four-on-the-floor sekitar 124 BPM. **SFX:** hentakan di setiap potongan, whoosh cepat, stinger di akhir.
- **Referensi:** ref-motion-4 (TEXT KINETIK / TRANSISI CEPAT) dan ref-motion-2.

## 04 · TERMINAL (baru)
- **Rasa:** dunia developer/hacker yang serius tapi keren; cocok untuk keamanan siber.
- **Warna:** hitam CRT `#050807` + **hijau fosfor** `#39FF88` + **amber** `#FFB000` untuk peringatan.
- **Ciri khas:** font monospace, garis scanline dan kedip CRT, jendela terminal dengan perintah **diketik sinkron dengan VO**, output contoh (label CONTOH OUTPUT), kotak peringatan amber yang berkedip, progress bar ASCII `[####----]`.
- **Musik:** synthwave gelap minimal dengan arpeggio bass dan tick digital. **SFX:** mengetik, enter, glitch, notifikasi negatif untuk peringatan.

## Bonus · EMBER (sudah dipakai: Black October, Gemini v2)
- **Rasa:** sinematik dan dramatis.
- **Warna:** warm black + glow emas, merah/amber untuk verdict, cyan untuk twist.
- **Ciri khas:** teks lebar bersinar yang muncul huruf per huruf, angka bab outline (01–04), panel UI miring 3D, kartu flash dengan teks berulang, debu emas, stempel verdict.

## 06 · AVATAR (baru, gabungan ref-moti0n-6/7/8)
- **Rasa:** ramah, personal, seperti punya presenter sendiri.
- **Karakter:** chibi kamu (kemeja hitam "EndrichTech", cargo krem) di bawah tengah. Ada 8 pose: netral, lambai, tunjuk, mikir, kaget, keren (kacamata), bicara, kedip. **Gerak bibir otomatis** mengikuti suara VO, kedip mata, goyang idle, dan ganti pose di kata kunci.
- **Warna:** satu mood per bab: oranye, merah, biru blueprint, lalu ungu-oranye neon.
- **Ciri khas:** judul sans tebal + **kata aksen serif miring**, label bab "01 SAPA", kartu UI gelap melayang, trik **coretan sketsa jadi neon**.
- **Musik:** pop ceria bouncy (pluck, clap, marimba). **SFX:** pop, bubble, whoosh, kilau (shimmer) saat neon.
- **File karakter:** `karakter/pose_fix/` (PNG transparan, tulisan baju sudah dibetulkan).

## 07 · SETUP (baru, gabungan ref-moti0n-9/10/11)
- **Rasa:** cozy "meja kerja malam", techy tapi hangat.
- **Warna:** ruangan gelap hangat + lampu amber, layar **biru blueprint** + aksen cyan.
- **Ciri khas:** judul overlay besar di atas; kamera **masuk ke layar monitor**; grid blueprint dan UI beranimasi di layar; objek **terbang keluar dari layar** ke arah penonton; penutup **keypad 3D** yang ditekan satu per satu (F-O-L-L-O-W).
- **Catatan:** meja dibuat dari grafis (tanpa footage). Kalau nanti kamu rekam meja kerjamu sendiri, layar monitornya bisa diganti dengan rekaman asli.
- **Musik:** chill lo-fi house (electric piano, kick lembut). **SFX:** whoosh masuk layar, glitch, klik keyboard mekanik untuk CTA.

## 08 · SHOWCASE (baru, gabungan ref-moti0n-12/13/14 + Refrensi Iklan + AVATAR)
- **Rasa:** iklan premium yang ramah: produk dibuktikan, bukan cuma diceritakan.
- **Karakter:** chibi kamu tampil **besar saat hook**, lalu **mengecil ke pojok kanan bawah** sebagai maskot yang bereaksi (pose tunjuk/mikir/keren + gerak bibir), dan sedikit membesar lagi saat twist.
- **Warna:** kanvas krem `#F4EBE1` + tinta `#1E1B18` + **oranye** `#E2582B`; blob warna lembut di latar yang **ganti tint per bab** (peach, biru langit, lilac).
- **Ciri khas:** judul sans tebal + kata aksen serif miring oranye; **langkah bernomor** dalam bulatan oranye (1 Versi 3D, 2 Bisa diputar, 3 Scroll sinematik); **jendela browser melayang** berisi **website 3D sungguhan (Three.js)**: produk berputar 360°, kamera dolly saat "scroll"; website lama dicoret merah lalu dibalik jadi versi 3D; kursor drag/klik, pil "360°", "LIVE", toast "Pesanan masuk"; **twist** "Yang barusan kamu lihat? Itu website."
- **Caption:** pengecualian khusus gaya ini: hanya **kata kunci** (2–4 kata) per kalimat, kata utama di kotak oranye; hook dan twist tanpa caption (judul yang bicara). Bisa dimatikan kalau mau tetap tanpa subtitle.
- **CTA (video penuh):** gelembung "Komen "3D"" dipegang chibi + tulisan tangan "nanti aku kirim detailnya".
- **Musik:** upbeat product commercial (snap, pluck synth, sekitar 112 BPM). **SFX:** whoosh flip kartu, klik kursor, pop kata kunci, hentakan di twist, shimmer.
- **Produk 3D:** dibuat di Three.js (`public/vendor/three.module.min.js`, lokal). Model detail bisa dibuat di Blender lalu diekspor `.glb`.

## 09 · GUIDE (baru, ATM dari ref-moti0n-15, plus sedikit 16/17/18)
- **Rasa:** tutorial yang rapi dan personal: kamu yang memandu, langkahnya jelas bernomor.
- **Karakter:** **chibi animasi** kamu (klip green screen di `karakter/Animasi Karakter/`) berdiri setengah badan di bawah tengah. Klipnya ganti tiap beat sesuai makna: lambai (hook), hitung jari, ngetik, tunjuk ke atas, jempol. Semua klip mulai dan berakhir di pose netral, jadi potongannya mulus. Klip animasi tidak punya gerak bibir; ekspresinya lewat gestur.
- **Warna:** kanvas krem `#EEEBE4` dengan bintik halus + tinta `#151515` + **lime** `#C6F432` sebagai stabilo di bawah kata aksen; merah `#E8392B` hanya untuk stempel/tombol.
- **Ciri khas:** HUD mono di atas (`// 03 · tulis ide` + counter yang ikut berubah: VIEWS, LANGKAH 1/3); headline **kata kunci** yang muncul kata per kata dengan satu kata **serif miring** berstabilo lime; props bernomor dengan **badge hitam** di pojok (HP, podium 1-2-3, jendela app yang diketik + ENTER, checklist dengan progress, tombol Bagikan + stempel "SIAP TAYANG"); **transisi titik halftone** ke bagian bukti/penutup.
- **Struktur (video penuh):** hasil dulu (hook) → "cuma N langkah" → 3-4 langkah → **bukti** (angka/hasil nyata, bersumber) → twist jujur "video ini dibuat pakai AI, suaranya clone suara aku" → CTA seri + pertanyaan A/B.
- **Musik:** lo-fi pop bersih (snap, rhodes, sekitar 104 BPM). **SFX:** whoosh tiap ganti langkah, pop angka, ketikan, klik ENTER, centang, tap, hentakan saat stempel.
- **Analisis referensi:** `ANALISIS_REF_15-18.md`.

## 10 · STORY MOTION (baru 2026-10-26, gabungan 08 SHOWCASE + 09 GUIDE)
- **Rasa:** cerita pendek yang hangat: penonton ikut "kisah" satu tokoh, belajar satu fakta, lalu melihat solusinya (produk/jasa) tanpa terasa jualan keras.
- **Struktur 5 bab** (HUD mono atas `// bab 02 · masalah` + **progress bar 5 titik** "BAB 2/5"): **01 kenalan** (tokoh) → **02 masalah** → **03 kenapa?** (fakta bersumber) → **04 berubah** (produk/solusi) → **05 kamu** (tawaran + CTA seri + pertanyaan A/B).
- **Tokoh tanpa wajah:** tokoh cerita (mis. "Raka") ditampilkan lewat **benda** (name tag, cangkir, toko onlinenya), bukan wajah baru; label kecil "CERITA ILUSTRASI".
- **Narator:** **chibi animasi** kamu (dari GUIDE) tampil **besar saat hook**, lalu **turun ke pojok kanan bawah** sebagai narator yang bereaksi (tunjuk, menghela napas, mikir, tepuk jidat, jentik jari, putar objek), lalu **naik lagi di CTA** (ajak mendekat, semangat, presentasi kiri-kanan untuk A/B). Ganti posisi = turun lalu muncul dari bawah (dari SHOWCASE).
- **Warna:** kanvas krem `#F2ECE3` berbintik + tinta `#18161A`; **lime** `#C6F432` stabilo di bawah satu kata aksen serif miring (GUIDE); **oranye** `#E2582B` untuk nomor langkah/produk/tombol (SHOWCASE). **Blob latar ganti tint mengikuti mood cerita:** hangat (kenalan) → abu-abu (masalah) → biru (fakta) → peach (berubah) → lilac (CTA).
- **Ciri khas:** headline kata kunci muncul kata per kata; toko "datar" jadi abu-abu, kursor pengunjung masuk lalu keluar; **kartu fakta** (stopwatch + angka menghitung + chip sumber) dan stempel merah; **transisi titik halftone tepat di titik balik cerita**; **jendela browser 3D (Three.js)** dengan langkah bernomor oranye, pil 360°/LIVE, kursor; kartu tawaran gelap, kartu seri "PART 1 → besok PART 2" dengan tombol Follow yang diklik; **kartu A vs B** untuk pertanyaan komentar.
- **VO:** gaya bercerita ("Ini Raka. Kopinya enak banget... tapi"), tag [soft] → [curious] → [excited] → [warm]; tetap intonasi lama (eleven_v4, stability 0.35).
- **Musik:** satu chunk Eleven Music per bab: storybook pizzicato/piano → ketukan penasaran → reveal upbeat (drum masuk) → groove iklan hangat. **SFX:** tap pengunjung, notif negatif, tick stopwatch, hentakan stempel, whoosh + shimmer di titik balik, klik Follow, pop A/B.

---

### File kerja (untuk Claude)
- Template build: `motion/gaya/gaya-paper/build.py`, `motion/gaya/gaya-pulse/build.py`, `motion/gaya/gaya-terminal/build.py` (+ `motion/gaya/gaya_common.py`)
- SIGNAL: `motion/gaya/claude-duet/build.py` · EMBER: `motion/gaya/black-october/build.py`
- AVATAR: `motion/gaya/gaya-avatar/build.py` · SETUP: `motion/gaya/gaya-setup/build.py` · SHOWCASE: `motion/gaya/gaya-showcase/build.py`
- GUIDE: `motion/gaya/gaya-guide/build.py` (grafis) + `motion/gaya/chibi_track.py` (key green screen chibi + watermark di atas, jalankan setelah render: `python chibi_track.py gaya-guide`)
- SFX/musik preview: `motion/gaya/gaya_sfx.py`, `motion/gaya/gaya_music.py`
- Perbaikan tulisan baju karakter: `karakter/tools/fix_shirt.py`
- STORY MOTION: `motion/gaya/gaya-story/build.py` (grafis) → render → `compose.py` (chibi animasi multi-posisi + watermark) → `sfx.py` (SFX + musik, mixer reel). Musik: `music.py`.
