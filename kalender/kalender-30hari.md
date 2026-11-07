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
| 3 | | | | | | ide | |
| 4 | | | | | | ide | |
| 5 | | | | | | ide | |
| 6 | | | | | | ide | |
| 7 | | | | | | ide | |
| 8 | | | | | | ide | |
| 9 | | | | | | ide | |
| 10 | 2026-11-10 | 2026-11-10-ai-agent-sel-otak | MOTION | PULSE | Seri AI Agent #2 | naskah ✋ | riset disetujui; naskah lolos review (1 putaran), VO 1 paragraf di-generate manual oleh Endrich; gaya per beat PULSE/SIGNAL/TERMINAL/PAPER/AVATAR; angka perlu cek halaman asli (fetch gagal); Notion ENTE-10 |
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
