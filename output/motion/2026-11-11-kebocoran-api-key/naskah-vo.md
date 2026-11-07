# Naskah VO: 3 Kesalahan yang Bikin API Key Kamu Bocor

JENIS: MOTION · SERI: (usul) Keamanan AI · GAYA: sama dengan Hari 10 (dasar PULSE + SIGNAL/TERMINAL/PAPER/AVATAR + 3D), tempo dipercepat
CATATAN GATE: VO di-generate manual oleh Endrich **tanpa melewati gate 1-2** (riset dan naskah tidak direview sebelum VO). Fakta dicek setelahnya oleh peneliti-konten (riset.md).

## VO final (transkrip Whisper + dicek), 66,7 dtk
> Kamu punya website atau aplikasi yang terhubung ke AI? Hati-hati, ada 3 kesalahan yang bisa bikin API key kamu bocor, dan yang ketiga sering banget nggak disadari. Pertama, mengunggah kode ke GitHub. Kalau API key kamu ikut tersimpan di dalamnya, orang lain bisa menemukannya, bahkan setelah kamu hapus dari kode terbaru. Kedua, menyimpan API key rahasia di front-end website. Meskipun nggak kelihatan di halaman, kunci tersebut bisa saja terbaca lewat browser. Nah, yang ketiga, ini yang menarik: tanpa sadar kamu membagikan API key lewat screenshot, log error, atau bahkan saat meminta bantuan AI coding. Menurut laporan GitGuardian tahun 2026, sekitar 28,6 juta secret baru terdeteksi dalam commit GitHub publik sepanjang tahun 2025. Dan kalau API key rahasia kamu bocor, orang lain bisa menyalahgunakan layanan, menghabiskan saldo API, bahkan mengakses data, tergantung izin yang dimiliki. Jadi, simpan secret key di back-end, batasi aksesnya, dan jangan pernah membagikannya sembarangan. Kalau kamu pernah pakai AI buat coding, coba cek lagi. Jangan-jangan API key kamu pernah ikut terkirim.

## Status fakta (detail di riset.md)
- GitGuardian State of Secrets Sprawl 2026 (17 Mar 2026): 28,65 juta secret baru di commit GitHub publik 2025. VO "sekitar 28,6 juta" masih wajar; di layar ditulis **28,65 JUTA**.
- Secret tetap ada di riwayat setelah dihapus dari kode terbaru: benar (docs GitHub).
- Key di front-end terbaca lewat browser: benar (OpenAI: jangan pasang key di client-side). Panel "DevTools" di layar = SIMULASI.
- Jalur screenshot / log error / chat AI coding: **tidak bersumber GitGuardian**. Ini peringatan umum; di layar diberi label SIMULASI dan tidak dikaitkan ke angka GitGuardian. "Sering banget nggak disadari" = opini.
- Dampak (penyalahgunaan, tagihan, data akun): sesuai OpenAI; "tergantung izin" = TERSIRAT.
- Ditambahkan di layar (tidak ada di VO): "Sudah bocor? Ganti (rotasi) key" (rekomendasi GitHub/OpenAI).

## Struktur & gaya per beat
| Waktu | Blok | Gaya | Visual |
|---|---|---|---|
| 0-3,3 | HOOK | PULSE + 3D | kunci API 3D berputar, "WEBSITE / APLIKASI + AI?" |
| 3,3-4,1 | HOOK 2 | PULSE | blok coral "HATI-HATI!" |
| 4,1-10 | LEAD + loop | PULSE + 3D | angka "3" raksasa, kunci memerah dan bocor jadi partikel, "YANG KE-3?" |
| 10-19 | BODY 1 | SIGNAL + 3D | grafik commit git 3D, commit lama menyimpan key, "MASIH ADA DI RIWAYAT" |
| 19-27 | BODY 2 | SIGNAL/TERMINAL | jendela website + DevTools (SIMULASI) menyorot key |
| 27-29 | LOOP | PULSE | blok biru "YANG KETIGA / INI MENARIK" |
| 29-36 | BODY 3 | TERMINAL | kartu screenshot / log error / chat AI coding (SIMULASI) |
| 36-46 | DATA | PULSE + 3D | counter 28,65 JUTA + hujan "secret" 3D, sumber GitGuardian |
| 46-55 | DAMPAK | PAPER | 3 kartu dampak + saldo terkuras + "TERGANTUNG IZIN KEY" |
| 55-61 | SOLUSI | PAPER + 3D | checklist + brankas 3D menutup, "SUDAH BOCOR? GANTI (ROTASI) KEY" |
| 61-69,7 | PENUTUP + CTA | AVATAR | chibi (mikir/tunjuk/kaget/lambai), "CEK LAGI", CTA layar Follow + A/B |
