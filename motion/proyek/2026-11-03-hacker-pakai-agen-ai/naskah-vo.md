# Naskah VO v1: Hacker Pakai Agen AI

```
JUDUL REEL: Satu Orang, 1.200 Situs: Hacker Pakai Agen AI
JENIS: MOTION
SERI / PART: Seri AI Pengawas #3 (label final menunggu Endrich)
GAYA: dasar TERMINAL (hitam + hijau fosfor, font mono) + PULSE / SIGNAL / EMBER / AVATAR per beat,
      semuanya dalam palet TERMINAL supaya satu kesatuan
VARIAN: ringkas (2 kasus + payoff, 1 loop)
DURASI TOTAL (estimasi): 35-38 dtk      KATA: ±91 (hook B)
NADA: cerita ke teman, "aku/kamu"
```

Status: draf untuk direvisi Endrich. Belum lewat reviewer-konten (dijalankan setelah revisi kamu).

## HOOK (pilih 1)
- **A) Pertanyaan tegang:** "Seribu dua ratus situs belanja diserang satu orang?"
- **B) Angka mengejutkan (rekomendasi):** "Satu orang pakai agen AI, nyasar seribu dua ratus situs belanja online."
- **C) Kontras:** "Kamu kira hacker butuh satu tim? Sekarang cukup satu orang plus agen AI."

## Naskah per blok

| Waktu | Blok | VO | Teks layar (kata kunci) | Gaya + visual | Fakta/opini |
|---|---|---|---|---|---|
| 0-5 | HOOK | (hook B) Satu orang pakai agen AI, nyasar seribu dua ratus situs belanja online. | "1 ORANG" · "1.200+ SITUS" | **TERMINAL**: counter target berputar cepat ke 1.200+, ikon orang tunggal di tengah grid situs; hentakan audio frame 0 | FAKTA (Reuters/NorForge, 19-20 Okt 2026; riset no. 2; sumber: "1.200+") |
| 5-9 | LEAD | Perintahnya nggak sampai seratus karakter. Dan itu baru kasus pertama. | "< 100 KARAKTER" · "KASUS #1" | **PULSE (palet TERMINAL)**: kotak prompt pendek, kursor berkedip, angka dibanting masuk | FAKTA (instruksi operator < 100 karakter) |
| 9-17 | BODY 1 + LOOP | Kata peneliti, seratus lebih perusahaan dilaporkan tembus. Ongkos AI-nya cuma sekitar lima ribu dolar. Yang kedua lebih ngeri. | "100+ DILAPORKAN TEMBUS" · "±US$5.000" | **TERMINAL**: log scan berjalan (label SIMULASI), daftar situs berubah merah satu per satu; loop: glitch → "KASUS #2" | FAKTA dengan atribusi (no. 2); "dilaporkan" wajib karena data yang diambil tidak diketahui |
| 17-26 | BODY 2 | Menurut CrowdStrike, satu kelompok nyerang dua ratus organisasi dalam sebelas hari. Dari empat puluh perintah sejam, jadi seribu lima ratus. | "200+ ORGANISASI · 11 HARI" · "40/JAM → 1.500+/JAM" | **PULSE (palet TERMINAL)**: kalender 11 hari dicoret cepat, bar chart 40 vs 1.500 tumbuh | FAKTA (CrowdStrike 29 Okt 2026; sumber: "200+" dan "exceed 1,500 commands an hour" vs maks ~40 manual; no. 1) |
| 26-31 | BODY 3 (payoff) | Tapi manusianya tetap yang milih target. Penangkalnya masih dasar: update, batasi akses, backup. | "MANUSIA TETAP PILIH TARGET" · checklist "UPDATE · AKSES · BACKUP" | **SIGNAL → EMBER**: alur "manusia → agen AI → target", lalu checklist 3 tips menyala satu per satu | FAKTA (operator tetap campur tangan; tips Kaspersky/CrowdStrike, no. 6) |
| 31-35 | CTA SERI | Besok aku bahas AI yang ngelawan balik. Follow biar nggak kelewat. | "PART 4 BESOK" · "AI NGELAWAN BALIK" | **AVATAR**: chibi Endrich pose tunjuk → lambai, lip-flap | Janji part berikut (butuh riset terpisah) |
| 35-38 | CTA KOMENTAR | Kamu lebih takut data dicuri, atau usaha lumpuh? | "A: DATA DICURI" · "B: USAHA LUMPUH" | **AVATAR**: chibi pose mikir, dua tombol A/B | Opini penonton |

Watermark "EndrichTech" y ≈ 1525 sepanjang video. Label "SIMULASI" di log scan.

## Teks untuk tools/tts.py (satu paragraf = satu segmen)

```
Satu orang pakai agen AI, nyasar seribu dua ratus situs belanja online.

Perintahnya nggak sampai seratus karakter. Dan itu baru kasus pertama.

Kata peneliti, seratus lebih perusahaan dilaporkan tembus. Ongkos AI-nya cuma sekitar lima ribu dolar. Yang kedua lebih ngeri.

Menurut CrowdStrike, satu kelompok nyerang dua ratus organisasi dalam sebelas hari. Dari empat puluh perintah sejam, jadi seribu lima ratus.

Tapi manusianya tetap yang milih target. Penangkalnya masih dasar: update, batasi akses, backup.

Besok aku bahas AI yang ngelawan balik. Follow biar nggak kelewat.

Kamu lebih takut data dicuri, atau usaha lumpuh?
```

## CAPTION (draf)
Seri AI Pengawas #3 🛡️

Kemarin kita bahas AI yang ngelemahin pengawasnya. Sekarang sisi gelapnya: agen AI dipakai buat nyerang.

Kasus 1 (Okt 2026): menurut peneliti yang dikutip Reuters, satu penyerang pakai alat AI open-source buat nyasar 1.200+ situs e-commerce. 100+ perusahaan dilaporkan tembus, ongkos token AI sekitar US$5.000. Beberapa korban bilang data sensitifnya nggak terbukti diakses. Kasus ini ketahuan karena peneliti nemu panel kendali penyerangnya kebuka di internet.

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
- Durasi ±35-38 dtk (setara hari 2), sedikit di atas target 35, di bawah batas 45. Kalau mau lebih pendek, buang "Dan itu baru kasus pertama" (−5 kata).
- Fakta "ketahuan karena panel kendalinya kebuka di internet" dipindah ke caption supaya VO ringkas.

---

# v2 (2026-11-03): versi Endrich

## Versi Endrich + 2 koreksi fakta (±160 kata, estimasi ±68-72 dtk; batas CLAUDE.md 45 dtk)
Koreksi: (1) "berhasil nyerang seribu dua ratus" → "nyerang lebih dari seribu dua ratus" (1.200+ itu sasaran; yang dilaporkan tembus 100+, sukses ~10%). (2) "Di kasus lain" → "Dari situ": 100+ perusahaan dan US$5.000 itu kasus yang SAMA (Cairn), jadi kalimat "itu baru kasus pertama" dipindah sesudahnya.

```
Ada satu orang yang pakai agen AI, buat nyerang lebih dari seribu dua ratus situs belanja online.

Padahal, perintah yang dia kasih ke AI itu... nggak sampai seratus karakter.

Dari situ, lebih dari seratus perusahaan dilaporkan berhasil ditembus. Biaya AI yang dipakai cuma sekitar lima ribu dolar. Dan ternyata, itu baru kasus pertama.

Dan, ini yang lebih gila, menurut CrowdStrike, ada satu kelompok yang menyerang dua ratus organisasi, cuma dalam sebelas hari. Kecepatan serangannya juga melonjak. Dari empat puluh perintah per jam, jadi seribu lima ratus.

Tapi ada satu hal yang perlu kamu tahu. AI-nya memang membantu mempercepat serangan, tapi manusia tetap yang menentukan targetnya. Makanya, keamanan dasar itu masih penting banget. Rutin update sistem, batasi akses, dan jangan lupa backup data.

Besok, aku mau bahas AI yang justru dipakai buat melawan serangan seperti ini. Follow dulu, biar nggak ketinggalan.

Kalau kamu punya bisnis, kamu lebih khawatir data pelanggan dicuri... atau bisnis kamu tiba-tiba nggak bisa beroperasi?
```

## Versi ringkas gaya Endrich (±107 kata, estimasi ±45 dtk)

```
Satu orang pakai agen AI buat nyerang seribu dua ratus lebih situs belanja online.

Padahal perintahnya ke AI... nggak sampai seratus karakter.

Lebih dari seratus perusahaan dilaporkan berhasil ditembus. Biaya AI-nya cuma sekitar lima ribu dolar. Dan itu baru kasus pertama.

Yang lebih gila, menurut CrowdStrike, satu kelompok nyerang dua ratus organisasi cuma dalam sebelas hari. Dari empat puluh perintah per jam, jadi seribu lima ratus.

Tapi manusia tetap yang nentuin target. Makanya keamanan dasar masih penting: update sistem, batasi akses, backup data.

Besok aku bahas AI yang justru dipakai buat ngelawan serangan ini. Follow biar nggak ketinggalan.

Kamu lebih khawatir data pelanggan dicuri... atau bisnis tiba-tiba lumpuh?
```
Estimasi pakai tempo VO lama yang terukur: 2,37 kata/dtk (VO 2026-10-28-penipuan-suara-ai).
