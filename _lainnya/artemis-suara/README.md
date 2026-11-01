# ARTEMIS Suara: kendalikan HP Android lewat suara atau ketikan (OpenAI Realtime)

Dengan alat ini kamu bisa ngobrol dengan asisten (suara real-time dua arah, boleh memotong AI saat bicara) atau mengetik.
Kalau kamu minta sesuatu dikerjakan di HP, asisten menyerahkannya ke **ARTEMIS** (google/artemis), yang lalu menjalankan HP-nya.
Semua model memakai **API OpenAI** dari akunmu.

```
 Kamu (bicara / ketik)
   │  browser di PC atau Chrome di HP: http://localhost:8765
   │
   ├── audio + teks (WebRTC, duplex) ──► OpenAI Realtime (gpt-realtime)
   │                                        │  memanggil tool: jalankan_tugas / cek_tugas / hentikan_tugas
   ▼                                        ▼
 server.py (PC, 127.0.0.1:8765) ──HTTP──► ARTEMIS daemon (PC, :8000, otak: OpenAI gpt-4o)
                                             │  ADB (USB / Wi-Fi)
                                             ▼
                                          HP Android
```

- API key OpenAI **hanya ada di PC** (file `.env`). Browser cuma menerima kunci sementara yang berlaku sebentar.
- Server hanya mendengarkan `127.0.0.1`, jadi orang lain di Wi-Fi yang sama tidak bisa memakai kreditmu atau HP-mu.

## Isi folder

| File | Fungsi |
|---|---|
| `server.py` | Jembatan: halaman web, kunci sementara Realtime, meneruskan tool ke ARTEMIS, notifikasi tugas selesai |
| `static/index.html` | Aplikasi web: tombol mic, kolom ketik, transkrip, tombol stop |
| `artemis-openai.jsonc` | Override config supaya ARTEMIS memakai OpenAI (bukan Gemini) |
| `pasang_config_openai.py` | Memasang override itu ke ARTEMIS (file lama di-backup) |
| `contoh-env.txt` | Contoh isi `.env` |
| `mulai.bat` | Start cepat di Windows |

## Syarat

- PC Windows/macOS/Linux dan **HP Android** (ARTEMIS belum mendukung iPhone).
- USB debugging aktif di HP (Opsi Pengembang → USB debugging), kabel USB.
- API key OpenAI dengan saldo. Realtime (audio) ditagih per token audio, jadi pantau pemakaian di dashboard OpenAI.

## Pasang (sekali saja)

**1. Pasang ARTEMIS** di luar folder project ini, misalnya `C:\artemis`:

```powershell
git clone https://github.com/google/artemis.git C:\artemis
```

```powershell
cd C:\artemis
.\start.bat
```

`start.bat` memasang ADB, scrcpy, FFmpeg, dan `uv`. Tutup UI yang terbuka setelah selesai.

**2. Isi API key untuk ARTEMIS.** Buat file `C:\artemis\.env` berisi satu baris:

```
OPENAI_API_KEY=sk-...isi-punyamu...
```

**3. Ubah otak ARTEMIS ke OpenAI** (dijalankan dari folder `artemis-suara` ini):

```powershell
uv run --project C:\artemis python pasang_config_openai.py C:\artemis
```

**4. Cek dan coba ARTEMIS sendirian dulu** (HP tersambung, layar tidak terkunci):

```powershell
cd C:\artemis
uv run artemis doctor
```

```powershell
uv run artemis run "Buka Settings, cari Battery, lalu sebutkan persentase baterai" --profile flash
```

Saat pertama, ARTEMIS memasang "Artemis Accessibility Helper" di HP (muncul notifikasi dan entri di Aksesibilitas).

**5. Siapkan jembatan suara.** Di folder `artemis-suara`, salin `contoh-env.txt` menjadi `.env` lalu isi `OPENAI_API_KEY`.
Kalau folder ARTEMIS bukan `C:\artemis`, ubah `ARTEMIS_DIR` di `mulai.bat`.

## Pakai (setiap kali)

1. Jalankan daemon ARTEMIS dan biarkan terbuka:
   ```powershell
   cd C:\artemis
   uv run artemis ui
   ```
2. Jalankan jembatan: klik dua kali `mulai.bat`.
3. Buka antarmukanya:
   - **Di PC (paling stabil):** buka `http://localhost:8765` di Chrome/Edge.
   - **Di HP:** buka Chrome di HP lalu ketik `http://localhost:8765`. `mulai.bat` sudah menjalankan `adb reverse`,
     jadi alamat localhost di HP diteruskan ke PC (mikrofon browser hanya diizinkan di localhost/HTTPS).
4. Tekan **Mulai**, izinkan mikrofon, lalu bicara atau ketik. Contoh:
   - "Tolong buka YouTube dan putar lagu Coldplay Yellow."
   - "Berapa baterai HP aku sekarang?"
   - Ketik: "cek ada notifikasi WhatsApp apa aja"

Tombol 🎤 menyalakan/mematikan mikrofon (mode ketik saja). Tombol ■ menghentikan tugas yang sedang berjalan di HP.

## Cara asisten bekerja

- Pertanyaan biasa langsung dijawab. Tugas di HP dikirim ke ARTEMIS (default mode **flash**, ~3-5 detik per langkah).
  Untuk tugas panjang, minta saja "pakai mode pro".
- Saat tugas selesai, hasilnya otomatis dibacakan.
- Hanya satu tugas berjalan pada satu waktu. Kalau kamu ganti perintah, asisten menghentikan tugas lama dulu.
- Asisten **minta konfirmasi** sebelum mengirim pesan, posting, transaksi, menghapus, atau mengubah akun,
  dan **tidak pernah** mengetik password, PIN, atau OTP (isi sendiri di HP).

## Batasan yang perlu kamu tahu

1. **Antarmuka di HP yang sama dengan yang dikendalikan.** Saat ARTEMIS berpindah aplikasi, Chrome masuk ke latar belakang.
   Biasanya suara tetap jalan, tapi Android bisa menghentikannya. Paling nyaman: antarmuka di PC atau HP/tablet kedua.
   Kalau di HP yang sama, pakai earphone supaya suara AI tidak tertangkap mikrofon.
2. **Beberapa bagian ARTEMIS terkunci ke Gemini di kodenya.** Override ini mematikan atau mengganti bagian tersebut:
   - pendeteksi koordinat "Robotics-ER" diganti explorer mode `pro` (lebih lambat per langkah, tapi jalan dengan OpenAI);
   - ringkasan langkah di latar belakang dimatikan, jadi tugas yang sangat panjang memakai konteks lebih banyak;
   - kompresi riwayat ("chunking") tetap mencoba Gemini. Tanpa kunci Gemini, bagian ini gagal diam-diam (degradasi, tidak mati);
   - di mode **pro**, "pixel safety net" dan validasi rencana selalu memakai Gemini (bug ARTEMIS: blok `nodes` tidak dibaca).
     Validasi rencana sudah dimatikan; safety net berbasis XML tetap jalan.
   Kalau mau semua fitur penuh, tambahkan `GEMINI_API_KEY=...` di `C:\artemis\.env` (ada kuota gratis). Otak utamanya tetap OpenAI.
3. Tidak bisa menyisipkan instruksi di tengah tugas. Perintah baru = hentikan lalu jalankan tugas baru.
4. Model OpenAI di `artemis-openai.jsonc` adalah `gpt-4o` dan `gpt-4o-mini` (preset bawaan ARTEMIS). Ganti saja kalau mau model vision lain,
   lalu jalankan ulang langkah 3.
5. **Keamanan:** ARTEMIS bisa melakukan apa saja di HP, termasuk ADB shell di mode pro. Disarankan pakai HP cadangan/emulator,
   dan jangan biarkan layar berisi data sensitif karena screenshot dikirim ke OpenAI.

## Kalau ada masalah

| Gejala | Coba |
|---|---|
| "OPENAI_API_KEY belum diisi" | Buat `.env` di folder `artemis-suara` |
| "Tidak ada HP yang terhubung" | `adb devices` harus menampilkan `device`; buka kunci HP dan setujui dialog USB debugging |
| "Gagal menghubungi ARTEMIS" | Pastikan `uv run artemis ui` masih jalan; buka `http://localhost:8765/health` |
| Tugas gagal "ARTEMIS tidak memulai tugas" | `uv run artemis doctor` di folder ARTEMIS |
| Mikrofon tidak diizinkan di HP | Buka lewat `http://localhost:8765` (bukan IP PC) dan pastikan `adb reverse tcp:8765 tcp:8765` sudah jalan |
| Kembali ke Gemini | Kembalikan `C:\artemis\config\artemis.jsonc.bak-...` menjadi `artemis.jsonc` |

## Status pengujian (2026-11-01)

Diuji di sandbox **tanpa HP dan tanpa API key asli**:
- config OpenAI terbaca ARTEMIS: semua node utama `openai/gpt-4o(-mini)`, validasi kredensial lolos, daemon melaporkan `openai/gpt-4o`;
- semua endpoint `server.py` diuji terhadap daemon ARTEMIS sungguhan (cek HP, satu-tugas, stop, SSE, batas waktu tugas "hilang");
- logika halaman web diuji di Chromium headless dengan WebRTC tiruan (ketik, transkrip suara, panggilan tool, memotong jawaban AI).

**Belum diuji:** koneksi nyata ke OpenAI Realtime dan HP sungguhan. Uji pertama yang disarankan: langkah 4 di atas,
lalu satu perintah sederhana lewat suara.
