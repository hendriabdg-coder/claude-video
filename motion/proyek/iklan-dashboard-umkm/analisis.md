# Analisis aset · Iklan "Dashboard Kuliner UMKM" (templat Google Sheets)

Produk: templat dashboard UMKM kuliner (produk digital Endrich). Demo: "Dashboard Kuliner - DEMO Kopi Senja", periode Sep–Nov 2026.
Format: 2 video iklan 9:16 · gaya premium Apple + Google · VO clone Endrich (2 take).

## 1. VO (transkrip, dicek telinga lewat Whisper)
Naskah sama, dua take. vo1 = 26,3 dtk · vo2 = 26,8 dtk.
> Udah jam 11 malam, masih ngitung nota sama buku kas. | Padahal cukup catat penjualan per hari per menu. | 5 menit beres. | Harga, modal, sama laba keisi sendiri. | Dashboard langsung kasih omzet, laba kotor, laba bersih, | dibandingin sama periode yang sama bulan lalu. | Mau lihat bulan lain? Tinggal pilih, | semua angka sama grafik ikut ganti. | Bahan yang hampir habis juga langsung muncul di daftar belanja. | Mau templatenya? Comment SHEET, nanti aku kirim linknya.

Perbedaan take: vo1 "Comment SHEET" lebih tegas dan cepat; vo2 sedikit lebih santai, ada jeda "Comments!… Comment sheet".

## 2. Analisis 11 gambar

| # | Tab | Isi penting | Kualitas & catatan | Dipakai untuk kalimat VO |
|---|---|---|---|---|
| 01 | Dashboard | 2 kartu insight ("Perlu diperhatikan · penjualan ojol Rp12,4 jt (19,9%)", "Kabar baik · Es Kopi Susu Aren 852 porsi (30,0%) · paling untung Nasi Goreng Spesial Rp20.480/porsi"), 4 KPI (Omzet Rp62.250.000 · Laba kotor Rp40.283.050, margin 64,7% · Laba bersih Rp21.817.050, margin 35,0% · Food cost 35,3%), grafik omzet harian, donut metode bayar, Top 5 menu, "Perlu dibeli (3 bahan)" | Aset terkuat. Ada bar rumus panjang + sel terseleksi (biru) di atas, jadi perlu di-crop. Teks KPI cukup besar untuk zoom. ⚠️ KPI menulis **"Belum ada data pembanding"** | omzet/laba kotor/laba bersih; bahan habis ("Perlu dibeli") |
| 02 | Rincian (crop) | Dropdown "Mau lihat apa? → Omzet per hari", tabel harian + bar | Duplikat #03 (lebih sempit, tanpa toolbar). Pilih salah satu | "tinggal pilih" |
| 03 | Rincian (penuh) | Sama dengan #02 + toolbar & tab bawah | Lebih lengkap untuk mockup layar | "tinggal pilih, grafik ikut ganti" |
| 04 | Penjualan | Input: tanggal, menu, jumlah, metode bayar (sel kuning). Otomatis: harga satuan, total, HPP, laba kotor (sel abu) | Bukti utama "catat 1 baris, sisanya otomatis" | "catat penjualan per hari per menu", "harga, modal, laba keisi sendiri" |
| 05 | Kas | Biaya operasional: gaji 9 jt, sewa 4 jt, listrik, gas, komisi ojol 20%, iklan IG | Bagus untuk "semua tercatat", tapi tidak disebut VO | montase "lengkap" |
| 06 | Belanja & Mutasi Stok | Belanja mingguan per bahan (kode BB01–BB15) | Tidak disebut VO | montase / pendukung stok |
| 07 | Stok Bahan Baku | Status **RESTOK** merah: Susu UHT (59%), Cup Plastik (46%), Telur Ayam (33%) | Visual kuat dan jelas | "bahan yang hampir habis langsung muncul" |
| 08 | Menu & HPP | HPP, food cost per menu; Matcha Latte 43,7% (merah) | Bagus untuk "modal keisi sendiri" | "harga, modal…" |
| 09 | Resep | Takaran per porsi → biaya per porsi | Sumber hitungan HPP otomatis | "modal keisi sendiri" (detail) |
| 10 | Laba Rugi Bulanan | Sep Rp62,25 jt · Okt Rp64,01 jt · Nov Rp30,19 jt (bulan berjalan); laba bersih Sep 21,8 jt · Okt 22,9 jt · simulasi PPh Final UMKM | Satu-satunya aset yang menunjukkan **perbandingan antar-bulan**. ⚠️ Nov baru separuh bulan, jadi jangan dibandingkan langsung (terkesan turun) | "dibandingin sama bulan lalu", "lihat bulan lain" |
| 11 | Pengaturan | Nama usaha, tarif PPh, tabel bantu otomatis | ⚠️ Ada **foto profil Endrich + tombol Bagikan** di pojok kanan atas, perlu di-crop. Isinya teknis, kurang menjual | montase singkat (opsional) |

**Konsistensi data (aku cek silang):**
- Omzet Rp62.250.000 = Laba Rugi Sep.
- Food cost 21.966.950 ÷ 62.250.000 = 35,3%.
- Margin kotor 64,7% dan margin bersih 35,0%.
- Ojol GoFood 6.027.000 + GrabFood 6.354.000 = 12.381.000 (19,9%); komisi 20% = Rp2.476.000 di Kas.
- Es Kopi Susu Aren 18.662.000 = 30,0% omzet.

Semua cocok, jadi angka demo aman ditampilkan sebagai **contoh** (diberi label "DATA DEMO").

## 3. Temuan yang perlu diputuskan Endrich
1. **VO bilang "dibandingin sama periode yang sama bulan lalu", tapi screenshot Dashboard (#01) menulis "Belum ada data pembanding"** karena periode Sep adalah bulan pertama. Agar iklan tidak menjanjikan sesuatu yang tidak terlihat:
   - **Terbaik:** kirim 1 screenshot Dashboard dengan Periode = **Oktober**, supaya kartu KPI menampilkan pembanding Sep.
   - **Sementara:** bagian itu memakai Laba Rugi (#10), kolom Sep vs Okt yang disorot. Ini perbandingan asli dari data.
2. **"Mau lihat bulan lain? Tinggal pilih":** pemilih Periode ada di tab Dashboard tapi tidak terlihat di screenshot. Yang terlihat hanya dropdown "Mau lihat apa?" (#03). Kalau ada, kirim screenshot kotak Periode / dropdown bulan; kalau tidak, dropdown #03 yang dianimasikan.
3. **Tab "Dashboard HP"** ada tapi tidak ada screenshot-nya. Untuk gaya Apple, mockup iPhone dengan dashboard versi HP akan sangat kuat. Kirim kalau ada.
4. **CTA "Comment SHEET".** Di aturan repo, CTA "komen KATA" dilarang untuk reel organik (dianggap engagement bait). Untuk **iklan berbayar / comment-to-DM** ini wajar. Aku ikuti VO, tapi pastikan otomatis DM-nya siap.
5. Resolusi screenshot ±1350 px, jadi zoom maksimal ±1,6x supaya tidak pecah. Angka penting (KPI, RESTOK) aku **gambar ulang sebagai motion graphic tajam**, bukan zoom raster.

## 4. Arah visual "Apple + Google"
- **Apple:** latar putih/abu sangat terang, tipografi besar tebal (Inter Display), banyak ruang kosong, mockup MacBook/iPhone mengambang dengan bayangan lembut, kamera dolly halus, satu pesan per layar.
- **Google:** kartu Material bersudut bulat, chip, ripple saat klik, kursor, aksen 4 warna (biru #4285F4, merah #EA4335, kuning #FBBC04, hijau #34A853) dipakai hemat, gerak "bouncy" yang ramah.
- Warna produk (coklat kopi #5B3A1E / oranye #C0661F) dipakai sebagai warna merek templat.

## 5. Pembagian 2 video
- **Video 1 · "Keynote" (vo1, gaya Apple dominan):** gelap → terang, dashboard di MacBook 3D, KPI menghitung naik, montase semua tab di akhir. Aset: 01, 04, 08, 09, 10, 07, 05.
- **Video 2 · "Material" (vo2, gaya Google dominan):** putih, kartu-kartu, kursor mengetik baris penjualan, ripple klik dropdown, chip RESTOK. Aset: 04, 03, 01, 10, 07, 06, 11 (crop).

Peta adegan (dua video mengikuti timing VO masing-masing):

| VO | V1 Keynote | V2 Material |
|---|---|---|
| "jam 11 malam, ngitung nota…" | gelap, jam 23:00, tumpukan nota 3D berantakan | kartu "23:00" + nota kusut, kalkulator; mood abu |
| "cukup catat penjualan per hari per menu" | lampu menyala → MacBook muncul, layar Penjualan (#04) | kursor mengetik 1 baris (tanggal, menu, jumlah) di kartu Penjualan (#04) |
| "5 menit beres" | angka besar "5 menit" | chip timer "5:00 ✓" bouncy |
| "harga, modal, laba keisi sendiri" | sorot kolom auto (harga/HPP/laba) + Menu&HPP (#08), Resep (#09) | 3 chip warna (Harga / Modal / Laba) terisi otomatis |
| "dashboard kasih omzet, laba kotor, laba bersih" | 3 KPI raksasa menghitung (Rp62,25 jt / 40,28 jt / 21,82 jt) + #01 | 3 kartu KPI Material + #01 |
| "dibandingin bulan lalu" | Laba Rugi #10, Sep vs Okt disorot | kartu Sep ↔ Okt + panah |
| "lihat bulan lain? tinggal pilih, grafik ikut ganti" | dropdown + grafik batang 3D berubah | ripple klik dropdown #03, grafik ikut ganti |
| "bahan hampir habis → daftar belanja" | Stok #07, label RESTOK berdenyut | chip merah RESTOK masuk ke kartu "Perlu dibeli" |
| "Mau templatenya? Comment SHEET" | layar akhir putih: "Comment **SHEET**" + montase cepat semua tab | kolom komentar mengetik "SHEET" → balasan "link terkirim ✓" |

Label: "DATA DEMO" kecil di setiap screenshot. Watermark EndrichTech. Musik: Eleven Music (V1 minimal piano/electronic keynote, V2 upbeat ukulele/pluck ala Google). SFX ElevenLabs.
