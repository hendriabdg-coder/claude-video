# Panduan VO Endrich Tech (untuk agent mana pun: Claude Code, Codex, dll.)

Dokumen ini berisi **semua** setelan yang dipakai untuk menghasilkan VO suara clone Endrich dengan intonasi yang sudah disetujui.
Ikuti persis. Jangan mengarang setelan sendiri.

**Cara paling aman:** jangan menulis kode TTS baru. Pakai tool yang sudah ada:

```bash
python tools/tts.py output/motion/<slug>/vo/naskah.txt --out output/motion/<slug>/vo --model eleven_v4 --stability 0.35
python tools/vo_full.py output/motion/<slug>/vo
```

Kalau ada agent yang menulis panggilan API sendiri, intonasi dan pelafalannya hampir pasti meleset, karena kamus pelafalan,
konteks antar segmen, seed, dan audio tag ikut tertinggal. Masalah itulah yang muncul waktu Codex mencoba.

---

## 1. Setelan suara (WAJIB)

| Setelan | Nilai | Catatan |
|---|---|---|
| Provider | ElevenLabs, SDK Python `elevenlabs` 2.74.1 | |
| Endpoint | `client.text_to_speech.convert_with_timestamps(...)` | butuh timestamp per kata untuk motion |
| `voice_id` | `xV29wBiBgOzpCgTwBbDC` | clone "Endrich - VO". **Jangan membuat clone baru atau mengganti ID ini.** |
| `model_id` | `eleven_v4` | wajib eksplisit, karena default tool `eleven_multilingual_v2` |
| `stability` | `0.35` | wajib eksplisit, karena default tool 0.5 |
| `similarity_boost` | `0.75` | |
| `use_speaker_boost` | `True` | |
| `style` | **tidak dikirim** | v4 tidak punya slider style |
| `speed` | **tidak dikirim** (tempo normal 1.0) | Endrich **menolak** versi cepat ("mentor", speed 1.15). Jangan mempercepat. |
| `seed` | `42` | supaya hasilnya konsisten |
| `output_format` | `mp3_44100_192` | |
| `previous_text` / `next_text` | teks paragraf sebelum/sesudah (versi yang sudah diganti kamus) | menjaga intonasi tetap nyambung antar segmen. Kalau ditolak API, ulang tanpa konteks. |
| API key | `ELEVENLABS_API_KEY` di `.env`, dimuat dengan `python-dotenv` | **jangan dibaca, dicetak, atau ditulis ke file mana pun** |

Bentuk panggilannya (persis yang dilakukan `tools/tts.py`):

```python
VoiceSettings(stability=0.35, similarity_boost=0.75, use_speaker_boost=True)

client.text_to_speech.convert_with_timestamps(
    "xV29wBiBgOzpCgTwBbDC",
    text=spoken,                     # teks segmen SETELAH diganti kamus pelafalan
    model_id="eleven_v4",
    voice_settings=settings,
    output_format="mp3_44100_192",
    seed=42,
    previous_text=prev_spoken,       # tidak dikirim untuk segmen pertama
    next_text=next_spoken,           # tidak dikirim untuk segmen terakhir
)
```

---

## 2. Format naskah (`naskah.txt`)

- **Satu paragraf = satu segmen**, dipisahkan baris kosong. Satu segmen biasanya satu beat (hook, isi 1, isi 2, CTA, penutup).
- **Audio tag** (dibaca oleh eleven_v4, tidak diucapkan):
  - `[serious]` di awal paragraf hook;
  - `[warm]` di awal paragraf CTA/penutup (bagian Endrich bicara langsung ke penonton);
  - paragraf isi **tanpa tag**.
  Jangan menumpuk tag lain tanpa tes.
- Bahasa Indonesia santai, kalimat pendek. Patokan 2,2-2,5 kata/detik (30 detik ≈ 65-75 kata).
  Durasi dipadatkan lewat naskah yang ringkas, **bukan** dengan menaikkan speed.

Contoh (reel prompt injection, 2026-10-29):

```
[serious] AI kamu bisa dibajak tanpa kamu sadar. Bukan lewat hack, tapi cukup lewat satu dokumen biasa.

Bayangkan kamu minta AI ngeringkas sebuah file. Tapi di dalam file-nya ada kalimat selipan yang nyuruh AI ngelakuin hal lain. Kalau AI-nya nurut, kerjaanmu langsung berantakan.

Namanya indirect prompt injection. Perintah jahatnya nyamar jadi isi bacaan, bisa di dokumen, email, atau web.

Kalau AI-nya bisa kirim data atau ngubah file, dampaknya jauh lebih serius. Jadi cukup kasih akses seperlunya saja, dan untuk aksi penting, harus minta konfirmasi dulu.

[warm] Ingat, boleh dibaca bukan berarti boleh dituruti. Pertanyaannya, kamu sekarang pakai AI buat ngobrol doang, atau udah buat kerja?
```

---

## 3. Pelafalan (penyebab utama salah ucap)

### 3a. Kamus `tools/pelafalan.json`
Sebelum teks dikirim ke API, setiap **kata utuh** (case-sensitive) diganti cara bacanya:

| Tulisan | Dibaca |
|---|---|
| AI | Ei-ai |
| 3D | tridi |
| 2D | tudi |
| cyber / Cyber / siber | saiber / Saiber / saiber |
| PHP | pe-ha-pe |
| PHP2Shell | pe-ha-pe-tu-syel |
| eMudhra | i-mudra |
| DM | di-em |

Aturan penggantian: regex `(?<![\w])KATA(?![\w])`, jadi "AI-nya" menjadi "Ei-ai-nya", tetapi "pakai" **tidak** tersentuh.
Cara baca **tidak boleh mengandung spasi** (pakai tanda hubung), supaya jumlah kata tetap sama dan timestamp cocok dengan naskah asli.
JSON timestamp tetap memakai kata asli dari naskah (field `word`), sedangkan versi ucapannya ada di field `spoken`.
Kata baru yang salah ucap ditambahkan ke kamus ini dan dicatat di `catatan-produksi.md`.

### 3b. Normalisasi teks sebelum generate
- **Jangan menulis kata dengan huruf kapital semua** ("HARUS", "INDIRECT PROMPT INJECTION"), karena bisa dieja huruf per huruf.
  Tulis huruf kecil di naskah VO; kapital cukup di teks layar.
- **Tanda kutip dan apostrof di tengah kata dibuang:** "file'nya" ditulis "file-nya", sedangkan `"INDIRECT..."` ditulis tanpa kutip.
- **Angka ditulis sebagai kata:** "80 juta" ditulis "Delapan puluh juta", "1.300-an" ditulis "seribu tiga ratusan".
- **Singkatan yang dieja ditulis fonetik:** "OTP" ditulis "o-te-pe". Singkatan yang dibaca seperti kata, misalnya "OJK", biasanya aman, tetapi tetap dicek saat didengar.
- Jeda dramatis cukup memakai `...` (contoh: "hilang... cuma karena").
- Istilah Inggris umum (file, email, web, hack, prompt injection) dibiarkan apa adanya; v4 membacanya dengan wajar.

---

## 4. Output dan penggabungan

`tools/tts.py` menghasilkan per segmen:
- `scene_NN.mp3`
- `scene_NN.json`, berisi `{text, spoken, duration, words:[{word, spoken, start, end}]}`; timestamp per karakter dari API dikelompokkan per kata, dan audio tag tidak dihitung sebagai kata.

`tools/vo_full.py` menggabungkan semuanya:
- setiap segmen dipotong dari (kata pertama − 0,06 dtk) sampai (kata terakhir + 0,18 dtk), supaya hening di awal/akhir hilang;
- hasil potongan dikonversi ke 44,1 kHz mono;
- antar segmen diberi jeda tetap **0,25 detik** (`--gap 0.25`);
- hasilnya `vo-full.mp3` (192k) dan `vo-full.json` (timeline kata gabungan + nomor scene), yang dibaca oleh build motion (`motion/gaya/reel_common.py`).

Lokasi: `output/motion/<YYYY-MM-DD>-<slug>/vo/` (naskah.txt, scene_*, vo-full.*).

---

## 5. Aturan proses

1. Generate hanya dari naskah yang **sudah disetujui** Endrich.
2. Setelah generate, **STOP**: Endrich harus mendengar intonasinya dulu sebelum lanjut ke motion.
3. Kalau ada yang salah ucap, perbaiki kamus atau naskah, lalu ulang **hanya segmen yang bermasalah**. Ingat: seed sama + teks sama = hasil sama, jadi ubah teksnya.
4. Jangan mempercepat VO, jangan mengganti model/voice, dan jangan menulis API key ke file atau log.
