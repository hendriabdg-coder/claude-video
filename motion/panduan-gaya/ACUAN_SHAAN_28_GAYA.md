# Acuan: 28 Kartu Gaya Animasi (Shaan Johari)

Sumber: Notion "Animation styles you can build with Claude" oleh Shaan Johari (@viashaan),
https://ruby-cotija-fb5.notion.site/Animation-styles-you-can-build-with-Claude-3fa28691eca3814ebb34c73a7cc261bf
(dibaca 2026-11-01; halaman terus bertambah, part baru muncul paling atas).

**Status: acuan, bukan gaya resmi.** Menu gaya tetap 10 gaya di `PANDUAN_GAYA.md`.
Memakai kartu di sini sebagai gaya baru, atau sebagai beat di dalam gaya yang ada, **butuh persetujuan Endrich dulu** (CLAUDE.md bagian 6 dan 11).
Isi di bawah adalah ringkasan kita sendiri, bukan salinan prompt aslinya. Buka link-nya untuk teks lengkap.

---

## 1. Cara pakai di project ini

- Kartu aslinya ditulis untuk **Remotion** dan berdurasi **5 detik**. Kita memakai **HyperFrames + GSAP**, jadi:
  - "spring dengan overshoot ~10%": `ease: "back.out(1.4)"` atau `elastic.out(1, 0.6)` yang dijinakkan;
  - "rise out of a mask": wrapper `overflow:hidden` + `yPercent: 100 → 0`;
  - "drawn on as a stroke": SVG `stroke-dasharray/dashoffset`;
  - "tabular figures": `font-variant-numeric: tabular-nums`;
  - "real 3D scene": Three.js di HyperFrames (skill `hyperframes-animation` → adapter Three.js), atau CSS 3D kalau cukup.
- Karena hanya 5 detik, satu kartu paling pas dipakai sebagai **satu beat (2-5 dtk) di dalam reel 25-35 dtk**, bukan sebagai video penuh.
- Format kartu bagus untuk ditiru di `PANDUAN_GAYA.md`: **Tampilan** (palet hex, font, layout, tekstur) → **Gerak** → **Larangan** → **Prompt siap tempel**.
  Bagian "Larangan" adalah kata-kata yang paling ampuh untuk revisi ("cards jangan fade, harus spring").

---

## 2. Aturan yang berulang di hampir semua kartu

| Aturan | Sejalan dengan aturan kita? |
|---|---|
| Frame pertama sudah terbaca, tidak mulai dari layar kosong | Ya: hook bergerak sejak frame pertama |
| **Tanpa fade/crossfade.** Elemen masuk lewat spring, slide, mask, stroke, stamp, atau morph | Baru, layak diadopsi |
| Spring dengan overshoot ~10%, perubahan bentuk besar ~5% | Baru |
| **Satu warna aksen**, sisanya netral | Kebanyakan gaya kita sudah begini |
| Angka menghitung dengan digit lebar sama (tabular), tidak goyang | Penting untuk PAPER / angka |
| Gradien gelap/halus diberi **dither/grain** supaya tidak banding saat encode | Baru, cek di render final |
| **Seperlima bawah layar kosong** | Ya: safe area bawah 350 px |
| Satu kejadian = satu beat yang jelas, ada jeda di antaranya | Ya: titik SFX klik |
| Motion blur hanya saat bergerak cepat, tajam saat diam | Baru |
| 1 detik terakhir diam total | Hati-hati: aturan kita "tidak ada layar diam > 3 dtk". 1 dtk aman |
| Brand, orang, dan data karangan; tanpa logo asli | Sejalan; **tapi** untuk berita kita wajib sumber asli yang disitasi |

### Daftar larangan "biar tidak kelihatan bikinan AI" (tempel di akhir prompt/brief motion)
- Tanpa neon glow, kecuali gayanya memang berbasis glow (EMBER, TERMINAL).
- Tanpa ledakan partikel atau sparkle.
- Tanpa crossfade. Elemen berubah bentuk atau cut, bukan larut.
- Bounce jangan di semua elemen. Pilih satu momen untuk memantul.
- Tanpa camera shake dan lens flare. (Catatan: PULSE memakai kamera bergetar; itu pengecualian yang sudah disetujui.)
- Tanpa lantai grid yang menyala.
- Tanpa teks di pojok frame.
- Tidak ada yang terlihat seperti template.

---

## 3. Kartu yang paling relevan untuk Endrich Tech

| Kartu | Inti visual | Pakai untuk | Dekat dengan gaya kita |
|---|---|---|---|
| **Day counter** | "DAY" merah raksasa + angka odometer, kalender terisi centang tangan; lambat-cepat-lambat | Seri "30 hari belajar AI", streak, build in public. **Langsung membantu CTA seri / konversi follow** | AVATAR, PAPER |
| **Headline Highlight** | Artikel melayang 3D di atas dinding artikel blur, kamera dolly ke paragraf, stabilo lime menyapu kalimat kunci, kartu post muncul | Berita AI, "bukti" klaim. **Wajib** sumber asli + sitasi, bukan koran karangan | EMBER, SIGNAL |
| **Social post receipt** | Kartu post putih, angka like/view naik cepat, 2 balasan menumpuk, garis spidol merah | "Lihat apa kata X", komentar berita | SIGNAL |
| **Versus** | Layar terbelah miring, nama besar kiri-kanan, 4 baris statistik dengan bar tumbuh dari tengah, centang pemenang | "ChatGPT vs Claude", paket harga, A vs B. Nama boleh, logo tidak | PULSE |
| **Screen-Recording Zoom** | Jendela app gelap di latar mint, kursor melengkung ke tombol, kamera zoom 2x dengan blur, klik + ring | Tutorial tools AI | GUIDE, SETUP |
| **Stat Chart** | Latar hitam, angka raksasa = nilai di ujung garis, garis jadi oranye tepat di momen "event" | Pertumbuhan, data AI, hasil klien | PAPER, TERMINAL |
| **Ranking bars** | Bar chart race 6 bar, satu bar hero oranye-merah naik ke #1 | Ranking model/tools AI, pangsa pasar | PAPER |
| **Isometric flow** | Diorama isometrik: bangunan per langkah muncul, van mengantar sepanjang jalan, label bernomor | "Cara kerja X" 3 langkah | SIGNAL, STORY MOTION |
| **Timeline** | Garis waktu di lantai perspektif, kartu milestone muncul seperti pop-up book, kartu NOW biru | Sejarah AI, "perjalanan" | STORY MOTION |
| **Before/after slider** | Jendela browser, situs lama vs baru, pembatas putih menyapu lalu parkir di tengah | **Iklan jasa web 3D**, makeover | SHOWCASE |
| **Laptop reveal** | Laptop silver 3D terbuka, layar menyala ke landing page, kursor klik, nama produk naik | Iklan jasa web, portofolio | SHOWCASE |
| **App Mockup** | HP 3/4 dengan UI asli (bukan screenshot), 3 kartu UI melayang muncul dari pill/chip | Demo aplikasi/produk digital | SHOWCASE |
| **Notification stack** | Lock screen, notifikasi order berjatuhan makin cepat, total naik | **Hanya dengan label SIMULASI.** "Bukti" penjualan palsu menyesatkan; pakai hanya untuk data asli atau ilustrasi yang jelas | SHOWCASE |
| **Paper Desk** | Top-down di cutting mat hijau, kertas jatuh dengan bobot, selotip, lingkaran spidol merah, stabilo kuning | Explainer "barang bukti" | PAPER |

### Kartu lain (kurang mendesak, catat saja)
- **Retro CRT, Oscilloscope**: dekat TERMINAL. CRT bagus untuk "coming up next" / pembuka seri.
- **Apple One-Take**: satu objek terus berubah bentuk tanpa cut; bagus untuk pembuka produk.
- **Glow Orb, Frosted Glass**: tenang/minimalis; Frosted Glass cocok untuk "aku tanya AI ..." (bar pencarian diketik).
- **Magazine + Note, Blue Editorial, Swiss Grid, Risograph**: tipografi editorial; bisa untuk kutipan/pernyataan satu kalimat.
- **3D Map Route, Globe arcs**: peta/jangkauan global.
- **Exploded Teardown**: produk dibongkar per lapis (review gadget).
- **Ink Wash, Pencil to Blueprint**: kartu judul artistik / "dari ide ke produk".

---

## 4. Ringkasan per kartu (palet + font)

Dipakai saat membangun beat agar tidak menebak warna. Semua font gratis (Google Fonts).

| Kartu | Palet utama | Font |
|---|---|---|
| Globe arcs | navy `#0E1830`→`#05070C`, titik daratan `#C9D6EE`, rute oranye `#FF8A3D` | Inter Tight, JetBrains Mono |
| Laptop reveal | studio `#F5F5F7`→`#E4E6EA`, tinta `#0F1115`, tombol `#2F6BFF` | Inter Tight |
| Isometric flow | latar `#EEF2F7`, jalan `#3A4458`, mint `#36C39A`, biru `#3B6CF6`, coral `#FF6A4D` | Inter Tight |
| Notification stack | biru `#0E2A5A` + teal `#0F4C5C` di atas `#070A12`, aksen hijau `#1FB872` | Inter |
| Before/after | latar `#EEF1F6`, tinta `#121418`, aksen tomat `#E4572E` | Inter Tight, Manrope |
| Ranking bars | putih→`#F4F6F9`, hero `#FF5A36`, bar lain kalem | Inter Tight |
| Social post receipt | `#F1F3F6`, kartu putih, merah `#F4385E`, centang `#2B7BF2` | Inter |
| Day counter | putih→`#F3F3F1`, merah `#E5383B`, hitam `#111111` | Anton, Inter |
| Versus | `#0B0D12`, biru `#3D7BFF` kiri, oranye `#FF7A30` kanan | Anton, Barlow Condensed |
| 3D Map Route | kota abu pucat, rute `#1A73E8`, pin `#EA4335` | Inter |
| Exploded Teardown | grafit `#2A2D33`→`#0A0A0C`, aksen `#FF5A2A` | IBM Plex Sans/Mono |
| Ink Wash | kertas `#EEEAE0`, tinta `#1B1A18`, segel `#B8352A` | Cormorant SC/Garamond |
| Paper Desk | mat `#2D684C`, kertas `#F4F2EC`, merah `#D4231B`, stabilo `#FFE024` | Libre Caslon Text, IBM Plex Mono, Inter Tight, Permanent Marker |
| Headline Highlight | `#15181C`, kertas `#FCFCFA`, stabilo lime `#C9F52A` | Newsreader, Inter |
| Stat Chart | `#0A0B0D`, putih `#F4F5F6`, oranye `#FF5B1F` | Inter Tight, IBM Plex Mono |
| App Mockup | `#DFE6EE`→`#CFD8E2`, tinta `#0E1116`, hijau `#0E9F6E` | Plus Jakarta Sans |
| Screen-Recording Zoom | mint `#E3EFE9`→`#9CC4BD`, app `#1B1C20`, tombol `#3D7BFA` | Inter, JetBrains Mono |
| Timeline | lantai `#F5F6F8`, tinta `#0E1116`, biru `#2442F5` | Schibsted Grotesk, JetBrains Mono |
| Glow Orb | `#070304`, halo `#531829`, orb `#F696DE` | Outfit |
| Frosted Glass | teal `#1F5A6E`, navy `#0E2A3D`, coral `#FF8A5C` | Plus Jakarta Sans |
| Apple One-Take | `#EEEEEC`, tinta `#111113`, titik merah `#FF3B30` | Inter Tight |
| Retro CRT | `#07090F`, inti `#FCFBF8`, bloom `#FF9A90` | Syncopate, Share Tech Mono |
| Oscilloscope | `#030805`, fosfor `#46FF8C` | Share Tech Mono |
| Magazine + Note | kertas `#EAEDED`, tinta `#1B1E25`, pena `#C42E26` | Bodoni Moda, Newsreader, La Belle Aurore |
| Blue Editorial | biru `#2433F0`, putih `#F4F5FA` | Instrument Serif Italic, Schibsted Grotesk Black |
| Risograph | kertas `#EDEFEE`, pink `#FF48B0`, biru `#3255A4` | Bricolage Grotesque |
| Swiss Grid | kertas `#F0F0E8`, tinta `#101010`, merah `#F03820` | Public Sans |
| Pencil to Blueprint | kertas `#ECECE6`, biru `#1C4C8F`, putih `#EEF4FB` | Barlow Semi Condensed |

---

## 5. Usulan langkah berikutnya (perlu keputusan Endrich)

1. ~~**Adopsi aturan, bukan gaya:**~~ **Sudah (2026-11-01)**, masuk bagian "Standar gerak" di `.claude/skills/gaya-motion-endrich/SKILL.md`. Rencana awal: tambahkan "tanpa fade, spring ~10%, satu aksen, tabular digits, dither" dan daftar larangan di bagian 2 ke skill `gaya-motion-endrich` sebagai standar semua gaya.
2. **Uji coba 1 beat:** coba **Day counter** sebagai beat CTA seri di reel berikutnya (mendukung target konversi follow), di dalam gaya yang dipilih.
3. **Untuk iklan web 3D:** pertimbangkan Before/after slider atau Laptop reveal sebagai beat di gaya SHOWCASE.
