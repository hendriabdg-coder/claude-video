# Remotion 16:9 · template edit EndrichTech (50% hybrid / 50% full motion)

Struktur edit (permintaan Endrich 2026-11-12):
- **50% hybrid**: talking head + motion graphic. Variant:
  - `split`: video di kiri dalam kartu, judul kata per kata + poin bernomor di kanan;
  - `pip`: video dalam lingkaran di atas latar motion biru;
  - `lower`: video penuh + kata kunci besar di bawah.
- **50% full Remotion dinamis**. Variant:
  - `kinetic`: kata raksasa, hard cut warna;
  - `stat`: angka menghitung + sumber + bar opsional;
  - `list`: langkah bernomor;
  - `quote`: kartu kutipan.
- Audio talking head jalan terus dari awal sampai akhir; segmen full hanya mengganti gambarnya. Tiap segmen masuk dengan wipe diagonal (bukan fade). Ada progress bar dan watermark EndrichTech.

## Pakai
1. Taruh video 16:9 di `public/th.mp4` (sekarang berisi placeholder 30 dtk).
2. Isi `src/timeline.ts`: `SEGMENTS` (detik mulai/selesai + teks per segmen). Claude yang mengisinya dari transkrip video.
3. Preview: `npm run studio` (port 3000) · Render: `npm run render` → `out/final.mp4`.

`remotion.config.ts` memakai Chromium container cloud di Linux; di PC Windows Remotion memakai Chrome bawaannya sendiri.
Angka/klaim di segmen `stat`/`quote` wajib bersumber (aturan CLAUDE.md); contoh di timeline memakai angka GitGuardian 2026 yang sudah diriset.
