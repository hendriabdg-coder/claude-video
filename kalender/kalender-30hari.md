# Kalender Konten 30 Hari — Endrich Tech

Mulai: (isi tanggal hari 1)  ·  Diupdate Claude tiap kali satu tahap/gate selesai.

## Cara isi
- **Slug** = `YYYY-MM-DD-topik` (tanggal tayang). Slug yang sama dipakai di semua folder konten itu.
- **Jenis** = `MOTION` (full motion graphic) atau `TH` (talking head + motion).
- **Gaya** = salah satu dari 10 gaya (MOTION), atau gaya motion TH (HYBRID 50/50, dipilih 2026-11-01).
- **Status** = tahap terakhir yang **sudah selesai**. ✋ = menunggu review/approve Endrich.

### Alur MOTION
`ide → riset ✋ → naskah ✋ → VO ✋ → visual → final → diposting`
Folder: `motion/proyek/<slug>/` · serah terima `output/motion/<slug>/`

### Alur TH (talking head + motion)
`ide → riset ✋ → naskah ✋ → video mentah ✋ → visual → final → diposting`
- Video mentah: Endrich generate klip di Flow (4/6/8/10 dtk) sesuai naskah → taruh di `talking-head/mentah/<slug>/klip/`
  → Claude gabung jadi satu (`python tools/gabung_klip.py talking-head/mentah/<slug>`) → **Endrich review `gabungan.mp4`** → baru tambah motion.
Folder: `talking-head/mentah/<slug>/` → `talking-head/proyek/<slug>/` → `talking-head/hasil/<slug>/`

## Kalender

| Hari | Tanggal | Slug | Jenis | Gaya | Seri / part | Status | Catatan |
|---|---|---|---|---|---|---|---|
| 1 | 2026-11-01 | 2026-11-01-ai-mengawasi-ai-lain | TH | HYBRID 50/50 | (usul: Seri AI Pengawas #1) | final ✋ | v2 + SFX + musik oleh Claude (_final.mp4); tinggal posting |
| 2 | 2026-11-02 | 2026-11-02-ai-melemahkan-pengawas | MOTION | EMBER | Seri AI Pengawas #2 | naskah ✋ | riset disetujui; naskah lolos review (2 putaran) menunggu Endrich; gaya dasar EMBER + TERMINAL/PAPER/AVATAR; Notion ENTE-2 |
| 3 | 2026-11-03 | 2026-11-03-hacker-pakai-agen-ai | MOTION | TERMINAL | Seri AI Pengawas #3 | final | selesai menurut Endrich 2026-11-04; file kerja di folder bersama hari-03/ |
| 4 | 2026-11-04 | 2026-11-04-ai-ngelawan-balik | MOTION | TERMINAL (usul) | Seri AI Pengawas #4 | naskah ✋ | naskah v2 (CTA ke hari 5 library AI) menunggu VO dari Endrich; Genie 4 dipindah ke hari 13 di Notion |
| 5 | | | | | | ide | |
| 6 | | | | | | ide | |
| 7 | | | | | | ide | |
| 8 | | | | | | ide | |
| 9 | | | | | | ide | |
| 10 | | | | | | ide | |
| 11 | | | | | | ide | |
| 12 | | | | | | ide | |
| 13 | | | | | | ide | |
| 14 | | | | | | ide | |
| 15 | | | | | | ide | |
| 16 | | | | | | ide | |
| 17 | | | | | | ide | |
| 18 | | | | | | ide | |
| 19 | | | | | | ide | |
| 20 | | | | | | ide | |
| 21 | | | | | | ide | |
| 22 | | | | | | ide | |
| 23 | | | | | | ide | |
| 24 | | | | | | ide | |
| 25 | | | | | | ide | |
| 26 | | | | | | ide | |
| 27 | | | | | | ide | |
| 28 | | | | | | ide | |
| 29 | | | | | | ide | |
| 30 | | | | | | ide | |

## Ringkasan minggu ini
- Siap review Endrich (✋):
- Jadwal batch berikutnya:
