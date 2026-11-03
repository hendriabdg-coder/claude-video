# Naskah VO v1: Hacker Pakai Agen AI

```
JUDUL REEL: Satu Orang, 1.200 Situs: Hacker Pakai Agen AI
JENIS: MOTION
SERI / PART: Seri AI Pengawas #3 (label final menunggu Endrich)
GAYA: dasar TERMINAL (hitam + hijau fosfor, font mono) + PULSE / SIGNAL / EMBER / AVATAR per beat,
      semuanya dalam palet TERMINAL supaya satu kesatuan
VARIAN: standar (2 kasus + payoff, 2 loop)
DURASI TOTAL (estimasi): 33-36 dtk      KATA: ±82 (hook B)
NADA: cerita ke teman, "aku/kamu"
```

Status: draf untuk direvisi Endrich. Belum lewat reviewer-konten (dijalankan setelah revisi kamu).

## HOOK (pilih 1)
- **A) Pertanyaan tegang:** "Seribu dua ratus situs belanja diserang satu orang?"
- **B) Angka mengejutkan (rekomendasi):** "Satu orang, pakai agen AI, nyasar lebih dari seribu dua ratus situs belanja online."
- **C) Kontras:** "Kamu kira hacker butuh satu tim? Sekarang cukup satu orang plus agen AI."

## Naskah per blok

| Waktu | Blok | VO | Teks layar (kata kunci) | Gaya + visual | Fakta/opini |
|---|---|---|---|---|---|
| 0-4 | HOOK | (hook B) Satu orang, pakai agen AI, nyasar lebih dari seribu dua ratus situs belanja online. | "1 ORANG" · "1.200+ SITUS" | **TERMINAL**: counter target berputar cepat ke 1.200+, ikon orang tunggal di tengah grid situs; hentakan audio frame 0 | FAKTA (Reuters/NorForge, 19-20 Okt 2026; riset no. 2) |
| 4-8 | LEAD | Perintahnya nggak sampai seratus karakter. Dan ini baru kasus pertama dari dua. | "< 100 KARAKTER" · "KASUS 1 DARI 2" | **PULSE (palet TERMINAL)**: kotak prompt pendek, kursor berkedip, angka dibanting masuk | FAKTA (instruksi operator < 100 karakter) |
| 8-16 | BODY 1 + LOOP 1 | Kata peneliti, lebih dari seratus perusahaan dilaporkan tembus. Ongkos AI-nya cuma sekitar lima ribu dolar. Ketahuannya pun gara-gara panel kendalinya kebuka di internet. Tapi kasus kedua lebih ngeri. | "100+ DILAPORKAN TEMBUS" · "±US$5.000" · "PANEL KEBUKA" | **TERMINAL**: log scan berjalan (label SIMULASI), dashboard panel dengan gembok terbuka; loop: glitch → "KASUS #2" | FAKTA dengan atribusi "kata peneliti" (no. 2); "dilaporkan" wajib karena data yang diambil tidak diketahui |
| 16-24 | BODY 2 + LOOP 2 | Menurut CrowdStrike, satu kelompok nyerang dua ratus lebih organisasi, cuma dalam sebelas hari. Dulu, hacker paling banter empat puluh perintah sejam. Sekarang bisa seribu lima ratus lebih. Terus, manusianya ngapain? | "200+ ORGANISASI · 11 HARI" · "40/JAM → 1.500+/JAM" · "MANUSIANYA?" | **PULSE (palet TERMINAL)**: bar chart 40 vs 1.500 tumbuh, kalender 11 hari dicoret cepat | FAKTA (CrowdStrike 29 Okt 2026, kutipan Adam Meyers; no. 1) |
| 24-30 | BODY 3 (payoff) | Manusianya masih nentuin target dan keputusan penting. Bedanya, satu orang sekarang kerjanya kayak satu tim. Penangkalnya masih dasar: rajin update, batasi akses, dan backup. | "BUKAN 100% OTOMATIS" · "1 ORANG = 1 TIM" · checklist "UPDATE · AKSES · BACKUP" | **SIGNAL → EMBER**: alur "manusia → agen AI → target" lalu checklist 3 tips menyala satu per satu | FAKTA (operator tetap campur tangan; tips Kaspersky/CrowdStrike, no. 6). "Kerjanya kayak satu tim" = OPINI/analisis |
| 30-33 | CTA SERI | Besok aku bahas gimana AI dipakai buat ngelawan balik. Follow biar nggak kelewat. | "PART 4 BESOK" · "AI NGELAWAN BALIK" | **AVATAR**: chibi Endrich pose tunjuk → lambai, lip-flap | Janji part berikut (butuh riset terpisah) |
| 33-36 | CTA KOMENTAR | Kamu lebih takut datanya dicuri, atau usahanya lumpuh? | "A: DATA DICURI" · "B: USAHA LUMPUH" | **AVATAR**: chibi pose mikir, dua tombol A/B | Opini penonton |

Watermark "EndrichTech" y ≈ 1525 sepanjang video. Label "SIMULASI" di log scan dan dashboard panel.

## Teks untuk tools/tts.py (satu paragraf = satu segmen)

```
Satu orang, pakai agen AI, nyasar lebih dari seribu dua ratus situs belanja online.

Perintahnya nggak sampai seratus karakter. Dan ini baru kasus pertama dari dua.

Kata peneliti, lebih dari seratus perusahaan dilaporkan tembus. Ongkos AI-nya cuma sekitar lima ribu dolar. Ketahuannya pun gara-gara panel kendalinya kebuka di internet. Tapi kasus kedua lebih ngeri.

Menurut CrowdStrike, satu kelompok nyerang dua ratus lebih organisasi, cuma dalam sebelas hari. Dulu, hacker paling banter empat puluh perintah sejam. Sekarang bisa seribu lima ratus lebih. Terus, manusianya ngapain?

Manusianya masih nentuin target dan keputusan penting. Bedanya, satu orang sekarang kerjanya kayak satu tim. Penangkalnya masih dasar: rajin update, batasi akses, dan backup.

Besok aku bahas gimana AI dipakai buat ngelawan balik. Follow biar nggak kelewat.

Kamu lebih takut datanya dicuri, atau usahanya lumpuh?
```

## CAPTION (draf)
Seri AI Pengawas #3 🛡️

Kemarin kita bahas AI yang ngelemahin pengawasnya. Sekarang sisi gelapnya: agen AI dipakai buat nyerang.

Kasus 1 (Okt 2026): menurut peneliti yang dikutip Reuters, satu penyerang pakai alat AI open-source buat nyasar 1.200+ situs e-commerce. 100+ perusahaan dilaporkan tembus, ongkos token AI sekitar US$5.000. Beberapa korban bilang data sensitifnya nggak terbukti diakses.

Kasus 2 (29 Okt 2026): CrowdStrike melaporkan satu kelompok menyasar 200+ organisasi di 14+ negara dalam 11 hari, dengan kecepatan bisa lebih dari 1.500 perintah per jam (manual sekitar 40).

Manusia masih pegang kendali: milih target dan keputusan penting. Yang berubah, satu orang bisa kerja kayak satu tim.

Penangkal dasarnya: update sistem yang terhubung internet, batasi akses (cabut akun karyawan yang udah keluar), dan backup otomatis.

Kamu lebih takut A) data dicuri atau B) usaha lumpuh?
Part 4 besok: gimana AI dipakai buat ngelawan balik.

## HASHTAG (7)
#AI #AIAgent #KeamananSiber #CyberSecurity #Hacker #BeritaAI #EndrichTech

## SUMBER
Detail lengkap + URL di riset.md (tabel klaim).
1. Reuters via media (CyberScoop, The Hacker News, TNW), laporan NorForge soal Cairn, 19-20 Okt 2026.
2. CrowdStrike, laporan VAPOR PANDA / ARTEX, 29 Okt 2026 (via CyberScoop, IT Brief).
3. Kaspersky, survei keamanan UMKM Indonesia (via Bisnis.com, 14 Sep 2026), untuk tips.

## Catatan
- Angka ditulis dalam kata di teks TTS supaya dibaca benar ("seribu dua ratus", "lima ribu dolar").
- Pelafalan: "AI" → Ei-ai (sudah di pelafalan.json). Perlu dicek di sampel: "CrowdStrike" (mungkin perlu "Kraud-straik"), "update", "backup".
- Nama alat (Cairn, ARTEX) dan atribusi negara sengaja tidak diucapkan: tidak menambah nilai buat penonton awam dan atribusinya masih versi vendor.
- Part 4 ("AI ngelawan balik") butuh riset sendiri sebelum dijanjikan; kalau mau topik lain, ganti CTA seri.
- Durasi ±35 dtk, di batas atas target. Kalau mau dipendekkan: buang kalimat "Ketahuannya pun..." (−9 kata).
