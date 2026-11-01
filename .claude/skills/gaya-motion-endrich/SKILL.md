---
name: gaya-motion-endrich
description: Spesifikasi motion graphic reel Endrich Tech, yaitu menu 10 gaya, safe area IG, teks kata kunci, ritme, karakter chibi, label, dan cover. Pakai di Tahap 3 saat membangun atau merevisi visual reel (HyperFrames build.py).
---

# Gaya motion Endrich Tech

Baca `CLAUDE.md` bagian 6 dan `motion/panduan-gaya/PANDUAN_GAYA.md`.

## Mulai
- Salin template gaya yang dipilih ke `motion/proyek/<slug>/` (daftar template di CLAUDE.md bagian 6), bersama `public/fonts`, `public/vendor`, dan `hyperframes.json`.
- Helper bersama ada di `motion/gaya/gaya_common.py`: `words()`, `page()`, dan helper JS cut/rise/pop/hide/count/type.
- Timing dari timestamp kata VO aktual (`scene_NN.json`), bukan estimasi.

## Spesifikasi
- 1080x1920, 30 fps. Hook bergerak sejak frame pertama. Perubahan visual tiap 2-3 detik.
- **Safe area:**
  - atas 250 px dan bawah 350 px (y > 1570) bebas dari teks penting;
  - kanan ~150 px untuk tombol IG;
  - **watermark "EndrichTech" di y ≈ 1525**.
- Teks maksimal ~6-8 kata per layar.
- **Teks kata kunci** (2-6 kata per beat) sinkron VO. Bukan subtitle penuh kata per kata, karena itu sudah ditolak Endrich.
- Label kecil "Ilustrasi AI" untuk visual AI dan "SIMULASI" untuk mockup.
- Label seri + progres bagian (HUD/stepper) bila gaya mendukung.

## Standar gerak (semua gaya)
Diadopsi 2026-11-01 dari `motion/panduan-gaya/ACUAN_SHAAN_28_GAYA.md`. Berlaku di atas gaya mana pun, kecuali gaya itu punya pengecualian di bawah.
- **Tanpa fade/crossfade sebagai cara masuk/keluar.** Elemen masuk lewat spring, slide, rise dari mask (`overflow:hidden` + `yPercent`), stroke (SVG dashoffset), stamp, atau morph. Opacity hanya pelengkap, bukan satu-satunya gerak.
- **Spring overshoot ~10%** untuk masuk (`back.out(1.4)` atau setara), ~5% untuk perubahan bentuk besar. **Bounce dipakai untuk momen penting saja**, jangan semua elemen.
- **Satu warna aksen** per gaya. Sisanya netral.
- **Angka menghitung pakai `font-variant-numeric: tabular-nums`** supaya lebar digit tidak goyang; mendarat tepat di angka akhir, tanpa overshoot melewati nilai asli.
- **Satu kejadian = satu beat** dengan jeda jelas (titik SFX). Ritme lambat-cepat-lambat lebih enak daripada kecepatan konstan; tidak ada gerak linear.
- **Gradien halus/gelap diberi grain atau dither** supaya tidak banding setelah encode; cek di `final.mp4`, bukan di snapshot.
- Motion blur hanya saat bergerak cepat; saat diam semua tajam.
- Frame pertama sudah terbaca (tidak mulai dari layar kosong).
- Ujung beat boleh diam sebentar (~0,5-1 dtk) supaya terbaca, tetap patuhi "tidak ada layar diam > 3 dtk".

### Larangan (cek saat review frame)
- Neon glow, partikel/sparkle, lens flare, lantai grid menyala.
- Camera shake.
- Teks dekoratif di pojok frame.
- Apa pun yang terlihat seperti template.
- Brand, logo, atau orang asli tanpa izin; untuk berita pakai sumber asli yang disitasi (CLAUDE.md bagian 6).

### Pengecualian yang sudah disetujui
- **EMBER** dan **TERMINAL**: glow/bloom dan kedip CRT memang bagian gayanya. Glow tetap di sekitar elemen, inti tetap terang, jangan membanjiri layar.
- **PULSE**: hard cut tiap ketukan dan kamera bergetar tetap dipakai.
- **Elemen pojok wajib** tetap ada: watermark, label "Ilustrasi AI"/"SIMULASI", HUD/label seri. Yang dilarang hanya teks dekoratif di pojok.

## Personality
- Karakter chibi Endrich `karakter/pose_fix/pose_{0..7}_*.png` (netral, lambai, tunjuk, mikir, kaget, keren, bicara, kedip) tampil minimal di bagian CTA (detik 20-30 dan penutup).
- Lip-flap, kedip, dan squash-pose: salin dari `motion/gaya/gaya-avatar/build.py`.
- Jangan membuat sosok baru tanpa izin.

## Aturan GSAP/HyperFrames (pernah bikin bug)
- `immediateRender:false` untuk flash/kamera fromTo.
- Animasikan x/y, jangan top/left.
- Jangan pakai CSS transform di elemen yang di-scale GSAP.
- Hindari `tl.call`; pakai `tl.set`.
- Repeat yoyo harus genap/terhitung supaya status akhirnya benar.

## QA
- `hf.sh lint public`, lalu `hf.sh snapshot public --at ... --no-end --describe false`, lalu cek frame dengan garis safe area.
- Render: `hf.sh render public -o renders/visual.mp4 --low-memory-mode`. Jangan menjalankan snapshot bersamaan dengan render (timeout).

## Cover
- `cover.png` 1080x1920 berisi judul hook + label seri + nomor part, terbaca sebagai thumbnail grid (judul besar di sepertiga atas).
