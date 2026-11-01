---
name: naskah-reel
description: Menulis atau merevisi naskah reel Endrich Tech (konten MOTION maupun TH talking head) dengan kerangka 8 blok, yaitu hook, lead, body, open loop, dan CTA, termasuk 3 alternatif hook, CTA seri, CTA komentar, dan format per klip Flow untuk TH. Pakai di Tahap 2 setiap kali menulis naskah, mengubah ide jadi naskah, atau merevisi naskah reel.
---

# Naskah reel: kerangka 8 blok, Endrich Tech

Baca `CLAUDE.md` bagian 4, 5, dan (untuk TH) 13 dulu. Naskah ditulis dari `riset.md` yang sudah lolos gate 1.

## Kerangka 8 blok

Nilai dan rasa penasaran diselang-seling: setiap poin selesai, langsung dibuka pertanyaan baru, jadi tidak ada momen "oke, cukup, scroll".

| # | Blok | Tugas | Panjang |
|---|---|---|---|
| 1 | **HOOK** | Memutus pola scroll. Topik disebut. | 1 kalimat, 0-3/4 dtk |
| 2 | **LEAD** | Menahan sampai ~detik 10: janji isi + alasan bertahan sampai akhir. | 1-2 kalimat, 3-5 dtk |
| 3 | **BODY 1** | Poin nilai pertama. | 5-7 dtk |
| 4 | **LOOP 1** | Satu kalimat penasaran ke poin berikutnya. | 1 kalimat, 1-2 dtk |
| 5 | **BODY 2** | Poin kedua. | 5-7 dtk |
| 6 | **LOOP 2** | Penasaran ke poin terakhir (yang paling kuat). | 1 kalimat, 1-2 dtk |
| 7 | **BODY 3** | Poin terkuat / twist / "tapi sayangnya". Membayar semua loop. | 5-7 dtk |
| 8 | **CTA** | CTA seri (+ alasan follow konkret), lalu CTA komentar. CTA save opsional. | 6-8 dtk |

Sumber kerangka: video referensi @robin_linkerpro (dibedah 2026-11-01), disesuaikan ke aturan akun ini (dua CTA, VO natural).

### Varian sesuai durasi
- **Pendek, 25-30 dtk (default MOTION):** HOOK → LEAD → BODY 1 → LOOP → BODY 2 → CTA (1 loop, 2 poin).
- **Standar, 30-40 dtk:** 8 blok penuh (2 loop, 3 poin).
- **TH 45-60 dtk:** 8 blok penuh; body boleh 8-10 dtk. Jangan menambah body ke-4. Kalau materinya lebih banyak, pecah jadi part berikutnya (seri).
- Konten satu cerita (bukan daftar poin): body = babak cerita (masalah → kenapa → berubah), loop = "terus apa yang terjadi?".

### Aturan per blok

**HOOK**
- Wajib **3 alternatif**, masing-masing dari pola berbeda: pertanyaan tegang ("Jebol Massal?", terbukti 4x jangkauan), klaim berani yang **benar**, angka mengejutkan dari riset, atau kontras "kamu kira A, ternyata B".
- Topik disebut dalam 3 detik. Tanpa salam, intro, atau logo. Jangan buka dengan "bayangin deh", "halo guys", atau kata "jangan".

**LEAD**
- Menjawab "kenapa aku harus nonton sampai habis?". Sebut berapa poin atau apa yang didapat, dan tanam janji untuk bagian akhir.
- Contoh pola: "Ada 3 tanda kamu kena, dan yang terakhir paling sering nggak disadari." / "Aku jelasin caranya, plus satu hal yang bikin ini berbahaya."
- Data akun: retention jatuh ke ~40% di 5 detik pertama. Lead adalah obatnya, jadi jangan dilewati.

**BODY**
- Satu body = satu ide. Satu kalimat = satu ide. Istilah teknis dijelaskan dalam satu klausa.
- Sudut lokal bila relevan: tersedia di Indonesia, harga dalam rupiah, dampak ke kerja/usaha.
- Taruh poin **terkuat di BODY 3**, karena di situlah loop dibayar.
- Tandai fakta (bersumber di `riset.md`) vs opini/analisis.

**OPEN LOOP**
- Satu kalimat pendek, 1-2 per video (tidak lebih, supaya tidak terasa formulaik). Tidak dipakai setelah body terakhir.
- **Wajib dibayar.** Kalau dijanjikan "paling bahaya", body berikutnya memang harus yang paling bahaya. Loop yang tidak terbayar = clickbait bohong (dilarang CLAUDE.md).
- Variasikan antar video. Bank frasa: "Tapi itu belum seberapa." · "Nah, yang kedua ini lebih licik." · "Dan ini bagian yang jarang dibahas." · "Masalahnya, ada satu celah lagi." · "Tapi tunggu, yang terakhir ini yang bikin aku kaget." · "Terus, kenapa ini bisa kejadian?"

**CTA**
- **CTA seri:** "Besok aku bahas [part berikutnya yang spesifik]. Follow biar nggak ketinggalan." Dilarang "jangan lupa follow". Alasan follow konkret (seri lanjutan, ringkasan berita AI, tips).
- **CTA komentar:** satu pertanyaan sungguhan, diutamakan A/B ("Kamu tim A atau B?"). Hindari "komen MAU" (engagement bait).
- **CTA save (opsional):** untuk konten tips/daftar/cara ("Simpan dulu, biar nggak lupa pas butuh."). Maksimal 2 CTA diucapkan; kalau ada save, CTA komentar boleh pindah ke teks layar + caption.
- **Label seri** di cover dan caption. Nada Endrich bicara langsung ("aku", "kamu"), bukan narator berita.

## Format naskah

### MOTION (VO suara clone)
Satu paragraf VO = satu segmen `tools/tts.py`. Biasanya satu blok = satu paragraf; LOOP digabung ke akhir paragraf body sebelumnya.

```
JUDUL REEL:
JENIS: MOTION
SERI / PART:
GAYA:
VARIAN: pendek / standar
DURASI TOTAL (estimasi):      KATA: (±2,2-2,5 kata/dtk)

HOOK (pilih 1): A) ... B) ... C) ...

[0-3 dtk] HOOK
VO: ...
Teks layar: (2-6 kata kunci)

[3-8 dtk] LEAD
VO: ...
Teks layar: ...

[8-15 dtk] BODY 1  (+ LOOP 1 di kalimat terakhir)
VO: ...
Teks layar: ...
Visual: ...
Fakta/opini: (sumber no. x di riset.md)

... BODY 2, LOOP 2, BODY 3 ...

[CTA]
VO seri: ...
VO komentar: ...

CAPTION (draf):
HASHTAG (5-8):
SUMBER:
```

### TH (klip Flow, talking head)
Endrich generate tiap klip di Flow dengan durasi 4, 6, 8, atau 10 detik, jadi naskah ditulis **per klip**.
- Jumlah kata per klip (~2,5 kata/dtk): 4 dtk ≈ 8-10 · 6 dtk ≈ 13-15 · 8 dtk ≈ 18-20 · 10 dtk ≈ 23-25. Lebih baik kurang dari lebih (ucapan Flow sering lebih lambat).
- Kalimat tidak boleh terpotong di tengah klip; blok boleh terdiri dari beberapa klip. LOOP ditaruh di akhir klip body.
- Nomor klip = nama file (`klip_01.mp4`, ...), supaya `tools/gabung_klip.py` langsung mengurutkannya.

```
JUDUL REEL:
JENIS: TH
SERI / PART:
DURASI TOTAL (estimasi):      JUMLAH KLIP:

HOOK (pilih 1): A) ... B) ... C) ...

Klip 01 (4 dtk) | HOOK   | ucapan: "..." | ekspresi/gestur: ... | teks motion: ...
Klip 02 (6 dtk) | LEAD   | ucapan: "..." | ekspresi/gestur: ... | teks motion: ...
Klip 03 (8 dtk) | BODY 1 + LOOP | ucapan: "..." | ...
...
Klip 0N (8 dtk) | CTA    | ucapan: "..." | ...

CAPTION (draf):
HASHTAG (5-8):
SUMBER:
```

## Penulisan untuk suara clone (MOTION)
- Ejaan ramah mesin; cek `tools/pelafalan.json` (AI → Ei-ai, dan lainnya).
- Tag emosi eleven_v4 di awal paragraf bila perlu, misalnya `[curious]`, `[cheerful]`.
- VO memakai intonasi lama (natural, tidak dipercepat). Padatkan naskahnya, jangan tempo bicaranya.

## Kejujuran
- Judul/hook boleh tajam, isi tidak boleh melebihi sumber.
- Klaim yang sumbernya diam ditulis "belum diumumkan", bukan "pasti tidak/ya".

## Cek sendiri sebelum dikirim ke reviewer
- [ ] 3 hook dari pola berbeda; topik disebut ≤ 3 dtk
- [ ] Ada LEAD dengan janji isi; tidak langsung loncat ke body
- [ ] Loop 1-2 kali, semuanya terbayar; poin terkuat di body terakhir
- [ ] CTA seri spesifik + CTA komentar A/B (+ save bila konten tips)
- [ ] Jumlah kata sesuai durasi (MOTION total; TH per klip)
- [ ] Setiap angka/nama/klaim ada di `riset.md`
