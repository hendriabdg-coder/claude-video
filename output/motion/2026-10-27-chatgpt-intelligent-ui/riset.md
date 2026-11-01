# Lembar Riset: ChatGPT GPT-6 "Intelligent UI"
Seri Update AI Minggu Ini #1 | Riset tanggal 2026-10-25

CATATAN METODE: halaman primer OpenAI (help.openai.com, openai.com, release notes) memberi HTTP 403 saat dibuka langsung. Kutipan "OpenAI" di bawah diambil dari (a) posting pengumuman OpenAI di OpenAI Developer Community (terbaca penuh), (b) cuplikan hasil pencarian atas Release Notes resmi, (c) media yang mengutip OpenAI. Kutipan hasil pencarian ditandai "[via cuplikan]". Sebelum produksi, Endrich/agent utama sebaiknya buka sendiri help.openai.com/en/articles/20001598-intelligent-ui-in-chatgpt dan memverifikasi.

## 1. Ringkasan fakta
1. Intelligent UI diluncurkan bersama GPT-6 di ChatGPT pada 7 Okt 2026.
2. Bentuk jawaban dipilih model sesuai pertanyaan: teks, grafik, tombol, formulir, grafik/chart. Pertanyaan sederhana tetap teks biasa.
3. Rollout: Plus, Pro, Business, Enterprise mulai 7 Okt (model GPT-6 Sol); Free dan Go mulai 8 Okt (model GPT-6 Luna). Itu tanggal mulai, bukan jaminan semua akun langsung dapat.
4. Awal rilis terbatas di tab Chat, bukan Work/Voice. Opsi Astra Pro tidak mendukung Intelligent UI (sumber sekunder).
5. Contoh: kalkulator, pembagi tagihan (bill splitter), perbandingan berdampingan, peta road trip, diagram sepeda, game kecil.
6. Indonesia: Liputan6 (12 Okt) menulis pengguna Indonesia sudah bisa memakai sesuai paket. Dukungan Bahasa Indonesia khusus: tidak ditemukan.
7. OpenAI sendiri mengakui "design judgment" dan ragam antarmuka masih perlu ditingkatkan.
8. GPT-6.1 Astra dibatalkan (dilaporkan WSJ, dikonfirmasi pejabat OpenAI lewat Al Jazeera, 29 Sep). GPT-6.1 Sol benar dirilis 29 Sep, tetapi belum di chat standar.

## 2. Tabel klaim | status | sumber

| Klaim | Status | Sumber (tanggal) |
|---|---|---|
| Rollout global dimulai 7 Okt untuk Plus, Pro, Business, Enterprise; Free dan Go mulai 8 Okt. Kutipan: "The global rollout began on October 7 for Plus, Pro, Business, and Enterprise, expanding to Free and Go starting October 8." | FAKTA | OpenAI Developer Community, "GPT-6 and Intelligent UI in ChatGPT" (pengumuman resmi), https://community.openai.com/t/gpt-6-and-intelligent-ui-in-chatgpt/1404139 (7 Okt 2026) |
| Paket berbayar pakai GPT-6 Sol, Free/Go pakai GPT-6 Luna | FAKTA (tabel rollout posting resmi) | sumber sama (7 Okt 2026) |
| Rilis Release Notes: "launched in ChatGPT ... starts globally today for Plus, Pro, Business, and Enterprise in the Chat tab, and expands to Free and Go starting tomorrow" | FAKTA [via cuplikan, halaman 403] | OpenAI ChatGPT release notes, https://help.openai.com/en/articles/6825453-chatgpt-release-notes (7 Okt 2026) |
| Tiga lapis: teks + visual + elemen interaktif; format "depends on the question"; teks biasa bila paling pas | FAKTA | Community post (7 Okt); Gizmologi (8 Okt) |
| Contoh resmi: "Ask for a game, calculator or bill splitter you can use in the conversation"; ide belajar dengan visual yang bisa diatur | FAKTA | Community post (7 Okt 2026) |
| Contoh lain: kalkulator tabungan pensiun, perbandingan berdampingan, diagram sepeda, peta road trip | FAKTA (dilaporkan media, mengacu pengumuman) | The AI Innovator https://theaiinnovator.com/openai-gpt-6-chatgpt-intelligent-ui-interactive-interfaces/ (8 Okt); Liputan6 https://www.liputan6.com/tekno/read/8311510/gpt-6-resmi-meluncur (12 Okt) |
| Contoh hands-on WIRED: kalkulator keterjangkauan apartemen, ilustrasi anatomi, penjelajah kursi pesawat | FAKTA sekunder (dari rangkuman, WIRED tidak dibuka langsung) | AI IDE List https://aiidelist.com/blog/openai-intelligent-ui-gpt-6 (8 Okt 2026) |
| Contoh "hitung cicilan" / "bandingkan harga" / "jadwal" | TIDAK DISEBUT sebagai contoh resmi. Terdekat: bill splitter, kalkulator tabungan, perbandingan berdampingan, kalkulator keterjangkauan apartemen | - |
| Launch hanya di Chat, bukan Work/Voice; opsi GPT-6 Astra Pro tidak mendukung | FAKTA sekunder | AI IDE List (8 Okt); The AI Innovator (8 Okt) |
| Kuota/batas pemakaian untuk Free/Go | TIDAK DISEBUT/tidak terkuantifikasi. Community post: "Limits: Not stated". AI IDE List: batas disebut tapi tanpa angka | Community post; AI IDE List |
| Platform web vs app | TIDAK DISEBUT jelas. Web dirujuk lewat pengaturan layout; app mobile tidak dijelaskan. Notebookcheck (September, soal GPT-6 Luna gratis) menulis hanya di desktop app: BERTENTANGAN/belum tersinkron dengan rollout 8 Okt | AI IDE List; Notebookcheck https://www.notebookcheck.net/ChatGPT-Free-gets-GPT-6-Luna-but-only-in-the-desktop-app.1407282.0.html (tanggal tidak terverifikasi, kira-kira September) |
| Free/Go dapat "Intelligent UI dasar" (Luna) | FAKTA sekunder, 1 sumber | Liputan6 (12 Okt) |
| Tersedia di Indonesia: "Pengguna di Indonesia sudah bisa menggunakannya sesuai dengan ketersediaan paket masing-masing." Rollout disebut "global" oleh OpenAI | FAKTA (Liputan6) + TERSIRAT (dari "global") | Liputan6 (12 Okt 2026); Community post (7 Okt) |
| Dukungan Bahasa Indonesia untuk Intelligent UI | TIDAK DISEBUT. Halaman help center versi id-id hanya menampilkan teks Inggris. Jangan tulis "pasti bisa" atau "pasti tidak" | Hasil pencarian help.openai.com/id-id (tidak terbuka) |
| Harga rupiah paket Plus/Go | tidak ditemukan (tidak diriset) | - |
| Antarmuka tampil progresif saat model masih menjawab | FAKTA | Gizmologi https://gizmologi.id/news/openai-ubah-cara-chatgpt-menjawab/amp/ (8 Okt 2026) |
| GPT-6 Instant mulai menjawab pertanyaan web search "44% sooner on average" dibanding GPT-5.6 Instant (uji internal OpenAI, ukur waktu mulai menjawab, bukan total) | FAKTA | Community post (7 Okt) |
| GPT-6.1 Sol dirilis 29 Sep di DevDay; API $2/$10 per juta token; ada di ChatGPT Work dan Codex untuk berbayar, "not yet available in ChatGPT's standard chat mode" | FAKTA sekunder | The Batch, deeplearning.ai https://www.deeplearning.ai/the-batch/sol-nearly-eclipses-astra (9 Okt 2026); ProPakistani https://propakistani.pk/2026/09/30/gpt-6-1-sol-brings-astra-level-performance-at-5x-lower-cost/ (30 Sep) |
| GPT-6.1 Astra dibatalkan, gagal "scope and authorization" (kata Saachi Jain): "didn't quite meet the bar in terms of staying within scope and authorisation, and how it communicates back to the user about the type of work it's done" | FAKTA (dikutip pejabat OpenAI, pertama dilaporkan WSJ) | Al Jazeera https://aljazeera.com/economy/2026/9/29/openai-scraps-release-of-latest-ai-model-over-safety-concerns (29 Sep 2026); Computing https://www.computing.co.uk/news/2026/ai/openai-cancels-astra-launch-safety-test-fail |
| Jabatan Jain | BERTENTANGAN: "head of safety systems" (Al Jazeera) vs "safety training team" (Bernama/Sputnik) | Al Jazeera; Bernama https://bernama.com/en/news.php?id=2613183 |
| Pembatalan 6.1 Astra ada hubungannya dengan Intelligent UI | TIDAK DISEBUT (modelnya terpisah) | - |
| Tampilan rapi tak menjamin isi benar; galat hitung/asumsi tidak realistis tersembunyi di UI cantik | TERSIRAT/opini penulis (bukan temuan uji independen) | Gizmologi (8 Okt); AI IDE List (8 Okt) |
| Belum dijelaskan cara menampilkan sumber pada jawaban berbentuk grafik/alat | FAKTA (catatan Search Engine Journal, via Gizmologi, SEJ tidak dibuka langsung) | Gizmologi (8 Okt 2026) |
| Interface tidak menjamin data live; state mungkin tidak bertahan antar thread | FAKTA sekunder, 1 sumber | AI IDE List (8 Okt) |
| Kritik privasi spesifik Intelligent UI | tidak ditemukan | - |
| Google lebih dulu dengan generative UI di Gemini 3 pada 18 Nov 2025 | FAKTA sekunder | Gizmologi (8 Okt 2026) |

## 3. Belum pasti / diperdebatkan
- Penamaan membingungkan: "GPT-6 Sol" (model chat berbayar, rilis 22 Sep menurut Liputan6, rollout 7 Okt) vs "GPT-6.1 Sol" (DevDay 29 Sep, belum di chat standar). Jangan campur dua nama ini di naskah. Tulis "GPT-6" saja.
- Tanggal rilis Sol: Liputan6 menyebut 22 Sep, The Batch menyebut GPT-6.1 Sol 29 Sep. Itu dua model berbeda menurut The Batch.
- Free/Go: pengumuman bilang 8 Okt, tetapi Notebookcheck (September) menulis GPT-6 Luna gratis hanya di desktop app. Belum jelas mana yang berlaku untuk Intelligent UI di HP Indonesia.
- Kuota Free/Go, ketersediaan web vs app, dan bahasa: tidak ditemukan angka/pernyataan resmi.
- Sumber "ringkasan" awal (local-ai-zone.github.io, hellogrowth.ai, dev.to) tidak dipakai. Semua klaim di atas dicek ke community post OpenAI atau media.
- Fakta "GPT-6.1 Sol 2.8% vs 2.1%" (angka kegagalan melaporkan tool rusak) beda antar sumber, tidak relevan reel, jangan dipakai.
- Kritik akurasi/privasi spesifik Intelligent UI hanya dari opini media, bukan pengujian independen.

## 4. Sudut lokal Indonesia
- Tersedia: ya menurut Liputan6, sesuai paket. Free/Go dapat belakangan (8 Okt).
- Harga rupiah: tidak ditemukan.
- Dampak kerja: tersirat, kalkulator/pembanding instan berguna untuk pekerja muda (cicilan, patungan). Ini kesimpulan, bukan klaim sumber. Contoh cicilan harus ditulis sebagai "ide yang bisa kamu minta", bukan contoh resmi.

## 5. Tiga usulan sudut hook
A. "ChatGPT sekarang bisa jawab pakai kalkulator dan grafik yang bisa kamu klik, bukan cuma teks."
B. "Mau patungan makan? Minta saja ChatGPT bikinin pembagi tagihannya langsung di chat." (contoh resmi: bill splitter)
C. "Tampilannya rapi, tapi jangan langsung percaya: angka di grafik ChatGPT tetap perlu kamu cek."

## Sumber utama
- https://community.openai.com/t/gpt-6-and-intelligent-ui-in-chatgpt/1404139 (7 Okt 2026)
- https://help.openai.com/en/articles/6825453-chatgpt-release-notes (cuplikan, 403)
- https://theaiinnovator.com/openai-gpt-6-chatgpt-intelligent-ui-interactive-interfaces/ (8 Okt 2026)
- https://aiidelist.com/blog/openai-intelligent-ui-gpt-6 (8 Okt 2026)
- https://gizmologi.id/news/openai-ubah-cara-chatgpt-menjawab/amp/ (8 Okt 2026)
- https://www.liputan6.com/tekno/read/8311510/gpt-6-resmi-meluncur (12 Okt 2026)
- https://www.deeplearning.ai/the-batch/sol-nearly-eclipses-astra (9 Okt 2026)
- https://aljazeera.com/economy/2026/9/29/openai-scraps-release-of-latest-ai-model-over-safety-concerns (29 Sep 2026)
- https://propakistani.pk/2026/09/30/gpt-6-1-sol-brings-astra-level-performance-at-5x-lower-cost/ (30 Sep 2026)
- https://www.notebookcheck.net/ChatGPT-Free-gets-GPT-6-Luna-but-only-in-the-desktop-app.1407282.0.html (tanggal tidak terverifikasi)
