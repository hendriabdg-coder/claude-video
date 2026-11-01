# ATURAN KONTEN REEL MOTION GRAPHIC: ENDRICH TECH

Instruksi kerja untuk Claude Code di project ini. Baca seluruhnya sebelum mengerjakan konten reel apa pun.
Sumber: `aturan-konten-motion-graphic.md` dari Endrich (2026-10-25), sudah disesuaikan dengan keputusan Endrich:
musik 12-15 dB di bawah VO, teks kata kunci (bukan subtitle penuh), **intonasi VO lama tetap dipakai**, dan menu 10 gaya.
Bagian 1-12 berlaku untuk konten **MOTION** (full motion graphic). Konten **TH** (talking head + motion) punya alur sendiri di bagian 13.

Balas user dalam Bahasa Indonesia santai.

---

## Struktur folder

Ada dua jenis konten, masing-masing punya "rumah" sendiri. Aset bersama tetap di root.

```
D:\Claude Video\
├─ CLAUDE.md · AGENTS.md · PANDUAN-VO.md · .env · .claude\   aturan, skill, agent
├─ tools\  karakter\  new sfx\  library\logos\               aset & tool bersama (dua jenis konten)
├─ kalender\            kalender-30hari.md (status semua konten, diupdate tiap gate)
├─ referensi\           video/audio referensi, clone-samples, audio-vo (intonasi)
├─ motion\              KONTEN MOTION (bagian 1-12)
│   ├─ aset\ui\ ikon\   aset visual yang dipakai ulang (screenshot UI, rekaman layar, ikon)
│   ├─ gaya\            10 template gaya + helper bersama (reel_*.py, gaya_*.py, chibi_track.py)
│   ├─ panduan-gaya\    PANDUAN_GAYA.md, preview tiap gaya, _vo preview
│   ├─ proyek\<slug>\   folder kerja tiap reel (aset khusus reel di sumber\)
│   └─ arsip\           eksperimen lama
├─ talking-head\        KONTEN TH: TALKING HEAD + MOTION (bagian 13, skill endrichtech-edit)
│   ├─ aset\broll\      B-roll yang dipakai ulang
│   ├─ mentah\<slug>\   klip\ (dari Flow) + urutan.txt + gabungan.mp4 + _assets\ (b-roll khusus video ini)
│   ├─ proyek\<slug>\   folder kerja
│   └─ hasil\<slug>\    _motion.mp4 + CATATAN_CAPCUT
├─ output\
│   ├─ motion\YYYY-MM-DD-slug\        serah terima reel motion (bagian 8)
│   ├─ talking-head\YYYY-MM-DD-slug\  serah terima talking head (bila perlu)
│   └─ log-performa.md
└─ _lainnya\            hal di luar konten reel (PPT, demo produk, eksperimen)
```

- Helper motion selalu diimpor dari `motion/gaya/` (`sys.path.insert(0, str(HERE.parents[1] / "gaya"))` dari `motion/proyek/<slug>/`). Root project = `HERE.parents[2]`.
- Jangan menaruh file kerja lepas di root.

---

## 1. Konteks & tujuan

- Akun: Instagram @end.rich9 (Endrich Tech). Niche edukasi AI/tech untuk audiens umum Indonesia.
- Format: Reel 9:16 (1080x1920, 30 fps), faceless motion graphic, watermark "EndrichTech".
- Tujuan: **jangkauan DAN konversi follow**. Jangkauan sudah terbukti; yang diperbaiki adalah konversi view ke follow.

### Acuan wajib: reel "Jebol Massal?" (gaya EMBER, durasi 1:03)

| Temuan | Data | Implikasi |
|---|---|---|
| Jangkauan | 1.918 tayangan (sekitar 4x reel talking-head), 97,4% bukan pengikut | Format faceless motion kuat menarik orang baru |
| Sumber | Tab Reels 74,8%, Jelajahi 20,4%, Profil 0,4% | Hampir tidak ada yang mampir ke profil |
| Skip rate | 46% (lebih rendah dari biasanya) | Hook sudah menahan |
| Save / share | 24 / 16 (di atas biasanya) | Topik dianggap berguna |
| Follow | 4 dari 1.628 pemirsa (~0,25%) | **Kebocoran utama: tidak ada alasan untuk follow** |
| Komentar | 0 | Tidak ada pemicu interaksi |
| Retention | Turun ke ~40% di 5 detik pertama, lalu datar ~20-25% | Yang lolos hook cenderung bertahan |
| Rata-rata nonton | 18 detik dari 1:03 | Durasi terlalu panjang |
| Audiens | 25-34 (48,4%), 18-24 (29,1%), 35-44 (14,2%) | Pekerja muda, calon pembeli produk digital |

**Target per reel:** konversi follow di atas 1%, komentar lebih dari 0, retention rata-rata di atas 40%.
Ini baru 1 data; tinjau ulang pola setelah 3-5 reel (lihat bagian 10).

---

## 2. Pembagian peran & gate persetujuan

**Endrich:** topik/materi umum dan keputusan akhir.
**Claude Code:** riset, naskah, VO (suara clone), motion graphic, SFX, musik, render final, cover, dan caption. Semua di Claude Code. Flow AI hanya dipakai Endrich sendiri untuk klip talking head dirinya (konten TH, bagian 13).

**Gate (WAJIB, Claude berhenti dan menunggu):**
1. Setelah **Lembar Riset + outline**.
2. Setelah **naskah VO** (3 alternatif hook).
3. Setelah **VO digenerate**: Endrich mendengar intonasinya dulu (reviewer tidak bisa menilai intonasi).

Dilarang lanjut ke motion sebelum gate 3 lolos. Preview visual sebelum SFX/musik boleh dikirim kalau perubahannya besar.
**Dilarang mengunggah/posting apa pun.** Output berhenti di file final.

---

## 3. Alur kerja (urut, jangan lompat)

Tahap 1 dijalankan subagent `peneliti-konten`; review naskah dan QC final oleh subagent `reviewer-konten` (bagian 12).

- **Tahap 0, brief.** Minimal topik. Kalau kurang, tanya maksimal 3 pertanyaan singkat. **Tanyakan gaya** dari menu 10 gaya (bagian 6) bila belum disebut.
  ```
  Jenis (MOTION / TH):
  Topik/materi:
  Sudut pandang (opsional):
  Gaya dasar (SIGNAL/PAPER/PULSE/TERMINAL/EMBER/AVATAR/SETUP/SHOWCASE/GUIDE/STORY MOTION; per beat digabung, bagian 6):
  Target durasi (default 25-35 detik):
  Seri / part ke- (opsional):
  Catatan khusus:
  ```
- **Tahap 1, riset.** Lembar Riset: 5-8 poin fakta, tiap poin dengan sumber (judul + URL + tanggal); bagian "belum pasti / diperdebatkan"; 3 usulan sudut hook.
  - Jangan menulis angka, nama, atau klaim tanpa sumber. Sumber bertentangan ditulis keduanya.
  - Clickbait boleh tajam, tidak boleh bohong; isi harus meluruskan judulnya.
  - **STOP (gate 1).**
- **Tahap 2, naskah VO** (bagian 5). **STOP (gate 2).**
- **Tahap 3, VO**, lalu **STOP (gate 3)**, lalu motion yang disinkronkan ke durasi VO aktual (bagian 6).
- **Tahap 4, SFX + musik** (bagian 7).
- **Tahap 5, render, QC, dan serah terima** (bagian 8-9).

---

## 4. Struktur reel

Durasi **25-35 detik** (maksimal 45). Naskah memakai **kerangka 8 blok** (skill `naskah-reel`, diadopsi 2026-11-01):
`HOOK → LEAD → BODY 1 → LOOP → BODY 2 → LOOP → BODY 3 → CTA`. Varian pendek 25-30 dtk: 1 loop, 2 body.

| Waktu (±30 dtk) | Bagian | Aturan |
|---|---|---|
| 0-3 dtk | **HOOK** | Satu kalimat tajam + teks besar, bergerak sejak frame pertama. Topik disebut di 3 detik pertama. Tanpa intro, salam, atau logo. |
| 3-8 dtk | **LEAD** | Janji isi + alasan bertahan sampai akhir (menahan sampai ~detik 10; retention akun jatuh di 5 detik pertama). |
| 8-25 dtk | **BODY + OPEN LOOP** | 2-3 poin, satu ide per body; di antara body satu kalimat penasaran (1-2 loop per video, wajib terbayar). Poin terkuat di body terakhir. Visual berganti tiap 2-3 detik. |
| 25-30 dtk | **CTA SERI** | Janji spesifik ke part berikutnya + alasan follow yang konkret. |
| Penutup | **CTA KOMENTAR** | Satu pertanyaan, diutamakan pilihan A/B yang gampang dijawab. Untuk konten tips/daftar boleh ditambah CTA save. |

### Aturan CTA
1. **CTA seri, bukan generik.** Dilarang "jangan lupa follow". Contoh: "Besok aku bahas [part berikutnya]. Follow biar nggak ketinggalan."
2. **Label seri** di cover dan caption (misalnya "Seri Internet Jebol #1").
3. **CTA komentar:** pertanyaan sungguhan ("Kamu lebih takut A atau B?"). Hindari pola "komen MAU" karena bisa dianggap engagement bait oleh Meta.
4. Alasan follow konkret: seri lanjutan, ringkasan berita AI, tips yang bisa dipakai.
5. **Personality Endrich:**
   - suara clone sebagai VO dari awal sampai akhir;
   - **karakter chibi Endrich** (`karakter/pose_fix/*.png`, 8 pose, sudah disetujui) tampil minimal di bagian CTA (detik 20-30 dan penutup), memakai cara lip-flap di `motion/gaya/gaya-avatar/build.py`.
     Khusus gaya GUIDE: pakai klip animasi chibi (`karakter/Animasi Karakter/*.mp4`, green screen) lewat `motion/gaya/chibi_track.py`; tanpa lip-flap.
   - Jangan membuat sosok/wajah baru tanpa izin.
6. Kalimat CTA bernada Endrich bicara langsung ("aku", "kamu"), bukan narator berita.
7. Profil adalah corong follow (tayangan dari Profil cuma 0,4%). Di catatan serah terima, sarankan pin/sorotan seri bila relevan.

---

## 5. Naskah & VO

- Bahasa Indonesia santai, kalimat pendek, satu kalimat = satu ide. Istilah teknis dijelaskan dalam satu klausa.
- Tidak ada pembuka basa-basi. Hook ditulis dulu, **wajib 3 alternatif hook**.
- **Tempo: pakai intonasi lama yang sudah disetujui** (eleven_v4, stability 0.35, natural, tidak dipercepat). Endrich menolak versi cepat ("mentor"). Durasi dipadatkan lewat **naskah yang ringkas** dan pemotongan hening di awal/akhir, bukan dengan bicara cepat. Patokan kasar sekitar 2,2-2,5 kata/detik, jadi 30 detik ≈ 65-75 kata.
- Tandai fakta berbasis sumber vs opini/analisis. Jangan menyimpulkan lebih dari riset.
- Format naskah (MOTION dan TH per klip) dan aturan tiap blok: lihat skill `naskah-reel`. Blok wajib di naskah: HOOK (3 alternatif), LEAD, BODY + LOOP, CTA SERI, CTA KOMENTAR, lalu CAPTION, HASHTAG (5-8), SUMBER.

### Pembuatan suara (setelah gate 2)
- Tool: `python tools/tts.py naskah.txt --out DIR --model eleven_v4 --stability 0.35`
  - Satu paragraf = satu segmen. Hasilnya `scene_NN.mp3` + `scene_NN.json` berisi timestamp per kata.
  - Voice clone Endrich: `voice_id xV29wBiBgOzpCgTwBbDC`. **Jangan membuat clone baru atau mengganti voice_id.**
- Kamus pelafalan: `tools/pelafalan.json` (misalnya AI → Ei-ai, siber → saiber, 3D → tridi). Tambahkan kata yang salah ucap ke sini dan catat di `catatan-produksi.md`.
- Generate hanya dari naskah yang sudah disetujui. Ulangi hanya segmen yang bermasalah.
- Simpan per segmen + `vo-full.mp3`; animasi mengikuti durasi aktual.
- VO yang jelas cacat (salah baca, tidak natural) tidak diserahkan. Jelaskan masalahnya dan tawarkan perbaikan.
- API key ada di `.env`. **Jangan pernah dibaca, dicetak, atau ditulis ke file mana pun.**

---

## 6. Motion graphic

- 1080x1920, 30 fps. Dibangun dengan HyperFrames (HTML + GSAP), dirender lewat `.claude/skills/endrichtech-edit/scripts/hf.sh` (lint, snapshot, render `--low-memory-mode`), lalu di-merge dengan ffmpeg.
- **Menu gaya (10):** lihat `motion/panduan-gaya/PANDUAN_GAYA.md`.
- **Gabungkan gaya dalam satu video** (aturan Endrich 2026-11-01, berlaku untuk MOTION dan TH/Hybrid): jangan berpatokan pada satu template gaya. Gaya di brief = gaya **dasar** (palet + font + watermark); per beat pilih gaya yang paling relevan dengan isi (mis. kronologi/log → TERMINAL, alur/proses → SIGNAL, kutipan/berita → PAPER, peringatan → EMBER, angka → PULSE) supaya bervariasi tapi tetap satu kesatuan. Tulis pilihan gaya per beat di naskah dan `plan.md`.

  | Gaya | Template |
  |---|---|
  | SIGNAL | `motion/gaya/claude-duet/build.py` |
  | PAPER | `motion/gaya/gaya-paper/build.py` |
  | PULSE | `motion/gaya/gaya-pulse/build.py` |
  | TERMINAL | `motion/gaya/gaya-terminal/build.py` |
  | EMBER | `motion/gaya/black-october/build.py` |
  | AVATAR | `motion/gaya/gaya-avatar/build.py` |
  | SETUP | `motion/gaya/gaya-setup/build.py` |
  | SHOWCASE | `motion/gaya/gaya-showcase/build.py` |
  | GUIDE | `motion/gaya/gaya-guide/build.py` + `motion/gaya/chibi_track.py` (chibi animasi di-overlay setelah render) |
  | STORY MOTION | `motion/gaya/gaya-story/build.py` + `compose.py` (chibi animasi multi-posisi) + `sfx.py`; untuk storytelling edukasi + iklan |

  Jangan membuat gaya baru tanpa persetujuan.
- **Safe area IG:**
  - atas 250 px dan bawah 350 px (y > 1570) bebas dari teks penting;
  - sisi kanan ~150 px untuk tombol;
  - watermark di **y ≈ 1525** (di atas zona caption).
- **Teks layar:** maksimal ~6-8 kata per layar, terbaca di HP.
- **Teks kata kunci, bukan subtitle penuh.** Tampilkan 2-6 kata kunci per beat yang sinkron VO supaya bisa dipahami tanpa suara. Subtitle kata-per-kata sudah ditolak Endrich.
- **Ritme:** perubahan visual tiap 2-3 detik; tidak ada layar diam lebih dari 3 detik.
- **Label:** "Ilustrasi AI" kecil di pojok untuk visual AI; "SIMULASI" untuk mockup.
- Jangan memakai logo/karakter/aset berhak cipta pihak lain tanpa izin. Untuk berita, pakai grafis sendiri atau tangkapan layar yang disitasi.
- Buat **cover.png** terpisah (judul + label seri + nomor part).

---

## 7. SFX & musik

- **SFX:** library Epidemic di `new sfx/` (langganan aktif). Pastikan akun Instagram @end.rich9 terdaftar di akun Epidemic, karena lisensi terikat channel.
- **Musik:** Eleven Music (`client.music.compose`, model music_v2_5, chunks ≥ 3000 ms), instrumental, mood ikut topik.
- **Level:**
  - musik **12-15 dB di bawah VO**. Mixer reel `motion/gaya/reel_sfx.py` mengukur gain per lagu supaya musik ~13,5 dB di bawah VO saat bicara (setelah sidechain ducking), karena tiap lagu Eleven Music beda kerasnya. `volume=-7.5dB` tetap hanya untuk preview gaya;
  - ada hentakan audio di 0-1 detik;
  - SFX hemat dan tepat sasaran;
  - akhir: alimiter + loudnorm **-14 LUFS**, true peak di bawah -1 dBFS.
- Catat semua aset di `credits.md`.
- Jangan memakai lagu dari folder "Viral Songs" (hak cipta komersial).

---

## 8. Output per konten

- Folder kerja: `motion/proyek/<slug>/`.
- Serahkan ke `output/motion/[YYYY-MM-DD]-[slug]/`:
  1. `riset.md`
  2. `naskah-vo.md`
  3. `vo/` (per segmen + `vo-full.mp3`)
  4. `final.mp4`
  5. `cover.png`
  6. `caption.md` (caption + hashtag + CTA komentar)
  7. `credits.md`
  8. `catatan-produksi.md` (asumsi, kredit ElevenLabs terpakai bila terbaca, hal yang perlu dicek, temuan reviewer)
- Salin `final.mp4` juga ke OneDrive `Videos/EndrichTech/`.
- Laporan ke Endrich maksimal 5 baris: apa yang dihasilkan, durasi, dan satu saran (misalnya ide part 2).

---

## 9. Checklist QC

- [ ] Hook bergerak di 3 detik pertama, topik disebut
- [ ] Durasi 25-35 detik (maksimal 45)
- [ ] Setiap fakta/angka punya sumber di `riset.md`
- [ ] CTA seri spesifik di detik 20-30 + label seri
- [ ] CTA komentar (pertanyaan sungguhan)
- [ ] Suara clone Endrich dengan intonasi lama yang sudah disetujui
- [ ] Karakter chibi Endrich tampil minimal di bagian CTA
- [ ] Teks aman dari UI IG (atas 250, bawah 350, kanan 150); watermark y ≈ 1525
- [ ] Teks kata kunci sinkron VO
- [ ] Musik 12-15 dB di bawah VO, -14 LUFS, TP < -1 dBFS, tanpa clipping
- [ ] Label "Ilustrasi AI" / "SIMULASI" bila perlu
- [ ] Aset tercatat di `credits.md`
- [ ] Ketiga gate sudah lolos
- [ ] Reviewer QC final tanpa temuan BLOKIR

---

## 10. Evaluasi setelah tayang (screenshot insight 24-48 jam)

- Bandingkan dengan acuan bagian 1 untuk:
  - skip rate, retention, dan durasi nonton rata-rata;
  - pengikut vs bukan pengikut;
  - sumber tayangan;
  - follow / pemirsa;
  - komentar, save, dan share.
- Hasilkan **3 temuan utama, 1 yang dipertahankan, 1 yang diubah**, lalu catat di `output/log-performa.md`.
- Rilis part berikutnya dalam 24-48 jam bila save/share tinggi.

---

## 11. Larangan

- Memposting, mengirim pesan, atau mengubah akun apa pun atas nama Endrich.
- Mengarang data, kutipan, atau sumber.
- Memakai audio/visual yang lisensinya tidak jelas.
- Melewati gate di bagian 2, atau mengubah gaya visual inti tanpa persetujuan.
- Flow AI atau tool video generatif lain untuk menampilkan orang berbicara, **kecuali** klip talking head Endrich sendiri yang Endrich generate untuk konten TH (bagian 13). Claude tidak membuat sosok/wajah orang lain.
- Clone suara baru, mengganti voice_id, atau generate VO sebelum naskah disetujui.
- Menulis API key/kredensial ke file, log, atau `CLAUDE.md`.
- Suara clone hanya untuk naskah Endrich Tech yang disetujui.

---

## 12. Pembagian agent

- **Agent utama:** memegang seluruh alur dan satu-satunya yang bicara dengan Endrich.
  - Mengerjakan naskah, VO, motion, SFX, dan musik, karena keempatnya saling terikat timing.
  - Memakai skill `naskah-reel`, `gaya-motion-endrich`, dan `spek-audio-vo` (di `.claude/skills/`).
- **`peneliti-konten`** (`.claude/agents/`): dipanggil di Tahap 1.
  - Input: topik, sudut pandang, dan pertanyaan riset spesifik.
  - Output: ringkasan maksimal 400 kata + tabel klaim-sumber; detail ditulis ke `riset.md`.
  - Maksimal 3 peneliti paralel, hanya untuk topik kompleks.
- **`reviewer-konten`** (`.claude/agents/`): dipanggil dua kali, yaitu (a) review naskah sebelum dikirim ke Endrich dan (b) QC final sebelum serah terima.
  - Hanya melapor, dalam kategori BLOKIR / PERBAIKI / SARAN.
  - Agent utama yang memperbaiki, lalu reviewer cek ulang bagian itu saja.
  - Maksimal 2 putaran; kalau masih BLOKIR, lapor ke Endrich.
- **Subagent** tidak menghubungi Endrich, tidak generate VO, tidak menyentuh kredensial, tidak posting, dan tidak membuka gate.
- **Kontrol biaya:** satu peneliti dan satu reviewer naskah + satu QC per konten. Iterasi render adalah pemborosan terbesar, karena itu review naskah dilakukan sebelum motion.
- **Evaluasi setup:** di `catatan-produksi.md`, catat jumlah temuan reviewer dan berapa yang valid menurut Endrich. Setelah 5 konten, tinjau apakah setup ini perlu disederhanakan.

---

## 13. Konten TH: talking head + motion

Alur (urut, jangan lompat): `ide → riset ✋ → naskah ✋ → video mentah ✋ → visual → final → diposting` (✋ = gate, Claude berhenti dan menunggu).

- **Riset & naskah:** sama seperti bagian 3-5 (sumber wajib, 3 alternatif hook, CTA seri + CTA komentar, Endrich bicara "aku/kamu"). Gate 1 dan 2 tetap berlaku.
  - Naskah TH ditulis **per klip**, karena Endrich generate klipnya di Flow dengan durasi 4, 6, 8, atau 10 detik.
    Patokan ~2,5 kata/detik: 4 dtk ≈ 8-10 kata, 6 dtk ≈ 13-15, 8 dtk ≈ 18-20, 10 dtk ≈ 23-25. Kalimat jangan terpotong di tengah klip.
    Format: `Klip 01 (6 dtk) | HOOK | ucapan: ... | ekspresi/gestur: ... | teks motion: ...` (kerangka 8 blok, skill `naskah-reel`).
  - Target durasi default 30-60 detik (tetap padat; acuan bagian 1: rata-rata nonton 18 detik).
- **Video mentah (gate 3 TH):**
  1. Endrich menaruh klip Flow di `talking-head/mentah/<slug>/klip/` (nama `klip_01.mp4`, `klip_02.mp4`, ...).
  2. Claude menggabungkan: `python tools/gabung_klip.py talking-head/mentah/<slug>`. Hasilnya `gabungan.mp4` (1080x1920, 30 fps, volume tiap klip disamakan), `gabungan_cek.jpg` (frame awal/akhir tiap klip), `gabungan.txt` (titik potong). Urutan dan potongan diatur di `urutan.txt` (`klip_03.mp4 0.4 7.8`).
  3. Claude cek sambungan (lompatan posisi/ekspresi, jeda hening, klip salah urut), lalu kirim `gabungan.mp4` ke Endrich.
  4. **STOP sampai Endrich approve.** Revisi (ganti/potong/urut ulang klip) diulang dari langkah 2.
- **Visual (motion):** skill `endrichtech-edit` dengan input `talking-head/mentah/<slug>/gabungan.mp4`; folder kerja `talking-head/proyek/<slug>/`, hasil `talking-head/hasil/<slug>/`.
  - **Struktur motion TH = "HYBRID 50/50"** (dipilih Endrich 2026-11-01 dari uji 4 varian; contoh `talking-head/proyek/2026-11-01-ai-mengawasi-ai-lain/`):
    - kira-kira separuh durasi TH full (lockup kata kunci di dada, punch-in, B&W untuk momen "serius"), separuh scene motion; di scene motion wajah Endrich tampil di **frame bulat** atau **latar dihapus**;
    - logo merek asli hanya dari `talking-head/aset/Image & Logo/` (aset Endrich); ikon buatan sendiri.
  - **Jangan terpaku pada satu gaya visual** (keputusan Endrich 2026-11-01): HYBRID 50/50 adalah kerangka pembagian TH/motion, bukan satu template. Tiap video, pilih dan **gabungkan 2-3 gaya yang relevan** per beat dari `motion/panduan-gaya/PANDUAN_GAYA.md` (10 gaya) dan `ACUAN_SHAAN_28_GAYA.md`. Contoh: data/angka → Stat Chart/PULSE, alur/proses → SIGNAL/Isometric flow, peringatan → EMBER, berita/kutipan → PAPER/Headline Highlight. Tetap satu palet + satu keluarga font per video supaya kombinasinya terasa satu kesatuan. Tulis pilihan gaya per beat di `plan.md`.
  - **Latar dihapus:** hasil 2026-11-01 terlihat aneh (lihat temuan reviewer di catatan proyek). Pakai hanya kalau orangnya menyatu dengan latar barunya (warna/cahaya disamakan, ada bayangan/rim light, transisi masuk-keluar halus); kalau ragu, pakai frame bulat atau split.
  - Chibi Endrich tidak wajib di TH (wajah Endrich sudah tampil).
- **Final:** SFX/musik di CapCut oleh Endrich (CATATAN_CAPCUT berisi daftar cue), kecuali Endrich minta Claude yang mixing.
- **Label:** klip dari Flow adalah video AI yang realistis. Sarankan Endrich mengaktifkan label "Info AI" saat posting di Instagram.
- Status tiap konten dicatat di `kalender/kalender-30hari.md` (kolom Jenis = TH).
