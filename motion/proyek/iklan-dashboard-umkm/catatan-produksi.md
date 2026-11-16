# Catatan produksi · iklan-dashboard-umkm (2026-11-16)

- 2 video iklan 9:16: **V1 Keynote** (gaya Apple, vo1) dan **V2 Material** (gaya Google, vo2). Detail analisis aset: `analisis.md`.
- Kejujuran visual:
  - VO bilang "dibandingin sama periode yang sama bulan lalu", tapi Dashboard demo menulis "Belum ada data pembanding". Adegan itu memakai **Laba Rugi Sep vs Okt** (data asli templat).
  - Adegan "pilih bulan" hanya menampilkan angka asli (omzet Sep 62.250.000 → Okt 64.011.000). Nov ditandai * karena bulan berjalan.
  - Label "DATA DEMO · KOPI SENJA" tampil terus.
- Screenshot Pengaturan (#11) tidak dipakai di layar karena ada foto profil.
- Perbaikan saat QC: kotak sorot RESTOK di adegan Stok sempat meleset satu baris (sudah digeser); kursor Material tidak lagi menutupi KPI.
- Kredit ElevenLabs terpakai (perkiraan): musik 2 × ±900, SFX 3 × ±17, total ±1.850 kredit.
- CTA "Comment SHEET": untuk iklan berbayar / comment-to-DM. Untuk reel organik, aturan repo melarang pola "komen KATA" (risiko engagement bait).
- Rekomendasi aset tambahan (opsional, untuk versi berikutnya): screenshot Dashboard periode Oktober (agar pembanding tampil di KPI), kotak pemilih Periode, dan tab Dashboard HP (mockup iPhone).

## V3 Meta (2026-11-16)
- VO baru `vo3.mp3` (24,5 dtk). Isinya: tanpa "per menu" dan tanpa bagian stok; ada kalimat baru "pembukuan kuliner yang beres tanpa begadang"; CTA "Cek templatenya lewat link di bawah".
- Gaya Apple (sama dengan V1). Adegan baru: kipas 5 tab templat + "tanpa begadang", serta CTA tombol "Link di bawah ↓" (diarahkan ke tombol CTA iklan Meta).
- Musik memakai ulang `music_keynote.mp3`, jadi tidak ada kredit ElevenLabs tambahan.
- Bug yang ikut terperbaiki: `META` belum dideklarasikan di JS (frame hitam saat snapshot pertama).
