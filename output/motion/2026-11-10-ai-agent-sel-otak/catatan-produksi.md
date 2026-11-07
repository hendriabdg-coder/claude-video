# Catatan produksi · Hari 10 · Hampir 2.000 AI Agent Analisis Sel Otak Tikus

## Ringkas
- Jenis MOTION, Seri AI Agent #2, tayang 2026-11-10 (Notion ENTE-10).
- Gaya dasar PULSE (hitam / biru elektrik #3A5BFF / coral #FF4F3A / krem). Gaya per beat: PULSE (hook, "cepat banget", "jadi gini", "satu hal penting"), SIGNAL (DNA + alur DATA → JURNAL → LAPORAN, peta laporan), TERMINAL (log agent, SIMULASI), PAPER (kartu preprint + stempel), AVATAR (chibi lip-flap di CTA).
- Animasi 3D (Three.js), semua deterministik per frame:
  1. otak tikus berupa awan ±6.300 titik sel, dengan 1.946 kubus agent terbang masuk dan mengorbit (hook);
  2. pil yang terbelah saat "bukan obat baru";
  3. heliks DNA: satu segmen gen menyala biru dan satu agent menempel;
  4. 144 kartu laporan terbang dan menyusun satu peta, lalu pola tersembunyi menyala;
  5. otak kecil (cerebellum) menyala coral;
  6. dua gen Tsc1/Tsc2 yang terhubung rantai;
  7. labu lab dengan gelembung dan tanda X "belum diuji lab".

## Asumsi / hal yang perlu dicek Endrich
1. **Durasi 72,4 dtk.** Ini lewat batas CLAUDE.md (target 25-35 dtk, maksimal 45), karena VO final dari Endrich menambah beberapa kalimat. Acuan akun: rata-rata nonton 18 dtk. Kalau mau dipendekkan, kandidat potongan: "Cepat banget kan?", "Jadi gini.", "Padahal keduanya...", "Tapi ada satu hal penting...", "Jadi, bukan berarti hasilnya salah...". Potongan ini bisa menghemat ±12 dtk, dan Claude bisa render ulang.
2. **Timing kata adalah estimasi.** VO di-generate manual, jadi tidak ada timestamp ElevenLabs. Timing berasal dari Whisper-small per jeda dan dibagi per suku kata (`motion/proyek/<slug>/align.py`). Teks layar sinkron per frasa; cek sekilas apakah ada yang muncul terlalu cepat atau lambat.
3. **Angka belum dicek ke halaman asli** (1.946 agent, jutaan/7,7 juta sel, 32 menit). Sesi ini tidak bisa membuka openai.com dan bioRxiv; lihat riset.md.
4. **Klaim baru di VO** "keduanya punya hubungan yang cukup erat" (Tsc1/Tsc2) belum punya sumber di riset.md. Ini fakta biologi umum (keduanya membentuk satu kompleks protein TSC), tapi tetap tambahkan sumbernya.
5. **Musik + SFX belum ada.** Library Epidemic dan Eleven Music tidak terjangkau dari sesi cloud ini. `final.mp4` berisi VO saja (loudnorm -14 LUFS). Tambahkan di CapCut dengan cue di bawah, atau jalankan mixer `motion/gaya/reel_sfx.py` di PC (perlu fungsi `cues_` untuk slug ini).
6. **Teks layar.** Nama "OpenAI" muncul sebagai teks biasa (bukan logo) di kartu preprint.
7. Saran profil: pin seri AI Agent #1-#3 setelah Hari 11 tayang (tayangan dari Profil cuma 0,4%).

## Cue SFX / musik (untuk CapCut; detik di final.mp4)
Musik: electronic energik ±120 BPM (PULSE), gelap tapi penasaran. Mulai dengan hentakan di 0 dtk, turun lebih ringan di bagian PAPER (42,8-58 dtk), lalu hangat di CTA. Taruh 12-15 dB di bawah VO.

| Detik | Kejadian layar | SFX usulan |
|---|---|---|
| 0,0 | hook, otak 3D + agent masuk | hit gelap + whoosh panjang |
| 0,8-2,5 | counter 0 → 1.946 | tick cepat, berhenti di 2,5 |
| 5,4 | timer "32:00" dibanting | hit + kick |
| 6,8 / 7,1 | "CEPAT" / "BANGET?" (blok biru) | dua hentakan pendek |
| 7,8 | pil 3D | whoosh lembut |
| 11,8 | pil terbelah + coret "OBAT BARU" | crack/snap + swish |
| 12,8 | "JADI GINI." (blok coral) | hentakan |
| 13,7 / 16,5 | DNA, gen menyala biru | whoosh + shimmer kecil |
| 17,6 / 18,5 / 20,6 | DATA → JURNAL → LAPORAN | pop ×3 |
| 22,3 / 25,2 | kartu terbang jadi peta, pola menyala | whoosh banyak kertas + ding |
| 28,3 | terminal | ketikan |
| 32,0 / 33,0 | bar Tsc1 / Tsc2 | pop kecil / pop besar |
| 34,9 / 36,1 | otak kecil menyala coral | whoosh + hit |
| 37,7 / 38,8 | dua gen terhubung | klik rantai |
| 40,4 / 41,3 | "!" + "SATU HAL PENTING" | dua hentakan |
| 43,5 | kartu preprint | kertas slide |
| 46,9 | X merah di labu | negatif/buzz pendek |
| 48,1 / 51,4 | baris checklist 2 & 3 | tap |
| 56,9 | stempel "PERLU DIUJI" | stamp keras |
| 58,2 | CTA biru, chibi masuk | whoosh |
| 63,0-63,7 | tombol Follow diklik | pop + klik + konfirmasi |
| 65,0 | "MENURUT KAMU?" | whoosh lembut |
| 67,9 / 69,4 | kartu A / B | pop / pop |

## Review
- Naskah: reviewer-konten 1 putaran (0 BLOKIR, 5 PERBAIKI diterapkan).
- QC final: lihat bagian di bawah (diisi setelah reviewer).

## Evaluasi setup
- Jumlah temuan reviewer naskah: 5 PERBAIKI + 4 SARAN; berapa yang valid menurut Endrich: (isi).
