# Asisten HP: ngobrol atau ketik, HP jalan sendiri (tanpa PC)

Aplikasi Android yang berjalan **sepenuhnya di HP**:
- **Suara real-time dua arah** (OpenAI Realtime, `gpt-realtime`). Kamu boleh memotong AI saat ia bicara.
- **Ketik** di kolom bawah. Masuk ke percakapan yang sama.
- Kalau kamu minta sesuatu dikerjakan, asisten **menyetir HP-mu sendiri**: membaca layar, mengetuk, menggeser,
  mengetik, dan membuka aplikasi, lalu melaporkan hasilnya dengan suara.

Semua memakai **API key OpenAI milikmu**. Tidak ada server perantara: HP bicara langsung ke `api.openai.com`.

```
 Kamu ──suara/ketik──► Asisten HP (aplikasi)
                         ├─ RealtimeVoice ──WebSocket──► OpenAI Realtime (ngobrol, memutuskan kapan menjalankan tugas)
                         └─ PhoneAgent ──► OpenAI gpt-4o (melihat screenshot, memilih aksi)
                               └─ AgentAccessibilityService ──► tap / geser / ketik / buka aplikasi di HP
```

## Pasang APK (tanpa PC)

1. Di HP, buka **GitHub → repo `claude-video` → tab Actions → "Build Asisten HP (APK)"**, pilih run terbaru yang hijau,
   lalu unduh artifact **`asisten-hp-apk`** (file zip, isinya `app-debug.apk`).
2. Ekstrak zip-nya, lalu buka `app-debug.apk`. Izinkan "Instal aplikasi tak dikenal" untuk browser/file manager.
3. Buka **Asisten HP** → tombol ⚙ → isi **API key OpenAI** → **Simpan**.
4. Tekan **Aktifkan aksesibilitas** → cari **Asisten HP** → nyalakan.
   - **Android 13 ke atas:** kalau tombolnya abu-abu atau muncul "Setelan terbatas", buka
     **Pengaturan → Aplikasi → Asisten HP → menu ⋮ (kanan atas) → Izinkan setelan terbatas**, lalu ulangi.
5. Tekan **Mulai**, izinkan mikrofon dan notifikasi. Selesai, silakan bicara.

Untuk update: unduh APK baru dan pasang menimpa yang lama. Pengaturan tetap tersimpan.

## Contoh perintah

- "Buka YouTube, cari lagu Coldplay Yellow, terus putar."
- "Berapa persen baterai HP aku?"
- "Cek notifikasi WhatsApp terbaru dari siapa aja."
- Ketik: "nyalakan mode pesawat"

Tombol: **🎤** menyalakan/mematikan mikrofon (mode ketik saja), **■** menghentikan tugas yang sedang berjalan,
dan **Matikan** di notifikasi menghentikan semuanya.

## Pengaman bawaan

- Sebelum mengirim pesan, posting, membayar/membeli, menghapus, atau mengubah akun, asisten **meminta konfirmasi "ya"** dulu.
  Kalau belum dikonfirmasi, agen berhenti tepat sebelum langkah terakhir.
- Asisten **tidak pernah** mengetik password, PIN, OTP, atau nomor kartu, dan tidak menyelesaikan CAPTCHA. Bagian itu kamu isi sendiri.
- API key disimpan di penyimpanan privat aplikasi dan hanya dikirim ke OpenAI.
- Satu tugas berjalan pada satu waktu, maksimal 30 langkah (bisa diubah di ⚙).

## Batasan

- **Aplikasi bank/pembayaran** biasanya memblokir screenshot. Agen tetap membaca daftar elemen, tapi bisa kurang akurat.
- **Biaya:** setiap langkah mengirim satu screenshot ke `gpt-4o`; suara real-time ditagih per token audio.
  Pantau di dashboard OpenAI. Untuk lebih hemat, ganti model penyetir di ⚙ (mis. `gpt-4o-mini`), dengan risiko akurasi turun.
- Tanpa earphone, asisten mengandalkan peredam gema HP. Kalau AI sering "memotong dirinya sendiri", pakai earphone
  atau matikan 🎤 saat AI bicara.
- Beberapa HP (Xiaomi, Oppo, Vivo, dll.) agresif mematikan aplikasi latar belakang. Kalau sesi sering putus,
  set **Baterai → Tanpa batasan** untuk Asisten HP.
- Ini APK debug untuk pemakaian pribadi, bukan rilis Play Store.

## Untuk pengembang

- Kode: `app/src/main/java/com/endrich/asistenhp/`
  - `AgentAccessibilityService.kt`: membaca layar, screenshot (Android 11+), aksi
  - `PhoneAgent.kt` + `Prompts.kt`: loop agen dan definisi tool
  - `RealtimeVoice.kt` + `AudioIO.kt`: suara Realtime (PCM16 24 kHz) dan antrean response
  - `AssistantService.kt`: foreground service (mikrofon) yang memegang sesi dan tugas
  - `MainActivity.kt`: layar (dibangun dari kode, tanpa layout XML)
- Build lokal (butuh Android SDK): `gradle assembleDebug` di folder ini. Build CI: `.github/workflows/asisten-hp.yml`.
- minSdk 30 (Android 11), targetSdk 35.

## Status pengujian (2026-11-01)

- Seluruh kode Kotlin lolos kompilasi terhadap framework Android 15; APK dibangun oleh GitHub Actions.
- Skema tool untuk OpenAI dicek valid.
- Logika suara diuji terhadap server WebSocket tiruan yang meniru alur event OpenAI Realtime: ketik, panggilan tool,
  notifikasi saat tool berjalan, pengguna memotong AI, dan ketikan di tengah jawaban. Tidak ada tabrakan `response.create`.
- **Belum diuji di HP sungguhan dan dengan API OpenAI asli.** Uji pertama yang disarankan: "Berapa persen baterai HP aku?".
