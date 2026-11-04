# Lembar Riset: AI yang Ngelawan Balik (Seri AI Pengawas #4)

Tanggal riset: 2026-11-04. Slug usulan: `2026-11-04-ai-ngelawan-balik`. Status: menunggu gate 1.
Sambungan: CTA hari 3 menjanjikan "AI yang justru dipakai buat ngelawan serangan ini".
Beda dengan reel 2026-10-26 "AI pemburu celah" (Gemini 4 Argon, Seri Internet Jebol #2): reel itu soal satu produk dan sisi dual-use-nya. Hari 4 fokus ke **balapan**: AI penjaga nemu celah lebih cepat dari manusia sempat nambal, dan ujungnya ada di tombol update penonton.

## 1. Status akses sumber

| Sumber | Akses |
|---|---|
| Google Cloud blog, Sandra Joyce (17 Jul 2025), Big Sleep | Terbaca langsung (primer) |
| Anthropic, "Project Glasswing: An initial update" (22 Mei 2026) | Terbaca langsung (primer) |
| Anthropic, "Expanding the Cyber Verification Program" (6 Okt 2026) | Terbaca langsung (primer) |
| Microsoft Security Blog, "Insights from the 2026 Microsoft Digital Defense Report" (1 Okt 2026) | Terbaca langsung (primer, ringkasan) |
| Laporan penuh Microsoft MDDR 2026 | TIDAK dibuka; angka "<24 jam" dan "30-60 hari" hanya dari ringkasan media (Byte Journal) |
| CrowdStrike AI kill switch (3 Nov 2026), OpenAI Daybreak (Mei 2026) | Hanya dari hasil pencarian/media; halaman CNBC & ir.crowdstrike.com diblokir jaringan sesi cloud |
| BSSN soal AI untuk pertahanan | Hanya judul/ringkasan hasil pencarian (Bisnis.com 13 Okt 2026, GovInsider) |

## 2. Ringkasan fakta

1. **Google Big Sleep (Juli 2025):** agen AI Google (DeepMind + Project Zero) bersama tim intel ancaman Google menemukan celah kritis SQLite (CVE-2025-6965) yang "known only to threat actors" dan "imminently going to be used", lalu dilaporkan dan ditambal sebelum dipakai. Google: "We believe this is the first time an AI agent has been used to directly foil efforts to exploit a vulnerability in the wild."
2. **Anthropic Project Glasswing, update 22 Mei 2026:** Claude Mythos Preview + ~50 mitra. Di 1.000+ proyek open-source, Mythos memperkirakan 6.202 celah high/critical; dari 1.752 yang dinilai, 90,6% (1.587) valid. **Dari 530 celah high/critical yang sudah dilaporkan, baru 75 yang ditambal.** Rata-rata satu celah high/critical butuh dua minggu untuk ditambal.
3. **Anthropic, 6 Okt 2026:** mitra Glasswing menemukan "at least 129,000 verified software vulnerabilities between April and July 2026" (batas bawah, data parsial), plus 5.500 dari pemindaian Anthropic sendiri (Apr-Okt 2026). Lebih dari 33.000 dinilai critical/high. Anthropic: angkanya "likely an undercount".
4. **Microsoft Digital Defense Report 2026 (1 Okt 2026):** "AI is giving defenders new ways to find and address weaknesses while giving cyberattackers new ways to look for them." Media (bukan teks primer yang terbaca) menyimpulkan AI memberi penyerang keunggulan jangka pendek.
5. **Kecepatan penyerang (sekunder):** ringkasan media atas MDDR 2026: median dari celah ditemukan sampai dijadikan senjata < 24 jam; perusahaan butuh 30-60 hari menambal celah kritis. BELUM dicek ke laporan asli, jangan dipakai di VO tanpa "menurut ringkasan".
6. **Produk pertahanan baru (konteks):** OpenAI Daybreak (diluncurkan Mei 2026, review kode & deteksi); CrowdStrike "AI kill switch" (3 Nov 2026) untuk mematikan agen AI yang lepas kendali, keputusan tetap di manusia. Keduanya dari media, belum primer.
7. **Hari 3 nyambung:** VAPOR PANDA ketahuan oleh tim threat hunting CrowdStrike OverWatch (manusia + tools), bukan dikonfirmasi oleh "AI CrowdStrike" (IT Brief, 30 Okt 2026). Kasus Cairn ketahuan karena peneliti memindai internet (lihat riset hari 3). Jadi: jangan bilang "AI yang nangkep hacker hari 3".
8. **Indonesia:** BSSN mendorong antisipasi serangan berbasis AI dan bekerja sama dengan Google Cloud soal AI untuk keamanan (sejak Mar 2024). Tidak ditemukan data resmi BSSN soal hasil pertahanan berbasis AI.

## 3. Tabel klaim

| No | Klaim | Status | Sumber |
|---|---|---|---|
| 1 | Big Sleep + GTIG menemukan celah SQLite yang hanya diketahui penyerang dan akan segera dipakai, lalu "cut it off beforehand" | FAKTA (klaim Google) | Google Cloud blog, "Cloud CISO Perspectives: Our Big Sleep agent makes a big leap", https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-our-big-sleep-agent-makes-big-leap, 17 Jul 2025 |
| 2 | "first time an AI agent has been used to directly foil efforts to exploit a vulnerability in the wild" | FAKTA (klaim "pertama" milik Google, bukan fakta independen) | sama |
| 3 | Nomor celah CVE-2025-6965 | FAKTA | sama; The Record/The Register (Jul 2025) |
| 4 | Mythos Preview: 6.202 perkiraan celah high/critical di 1.000+ proyek open-source; 90,6% dari 1.752 yang dinilai valid | FAKTA (klaim Anthropic) | Anthropic, "Project Glasswing: An initial update", https://www.anthropic.com/news/glasswing-initial-update, 22 Mei 2026 |
| 5 | 75 dari 530 celah high/critical yang dilaporkan sudah ditambal | FAKTA (per 22 Mei 2026; angka sekarang pasti berubah) | sama |
| 6 | Rata-rata dua minggu menambal satu celah high/critical temuan Mythos | FAKTA | sama |
| 7 | Mitra menemukan ≥129.000 celah terverifikasi Apr-Jul 2026; Anthropic +5.500 Apr-Okt 2026; >33.000 critical/high | FAKTA (klaim Anthropic, batas bawah) | Anthropic, "Expanding the Cyber Verification Program", https://www.anthropic.com/news/cyber-verification-program, 6 Okt 2026 |
| 8 | "Cybersecurity is inherently dual use"; tujuan "give defenders a permanent advantage" | FAKTA (kutipan) | sama |
| 9 | Microsoft: AI memberi pembela cara baru menemukan & menutup celah, sekaligus memberi penyerang cara baru mencarinya | FAKTA (kutipan) | Microsoft Security Blog, Terrell Cox, https://www.microsoft.com/en-us/security/blog/2026/10/01/insights-from-the-2026-microsoft-digital-defense-report/, 1 Okt 2026 |
| 10 | "AI sudah memberi penyerang keunggulan jangka pendek" | TERSIRAT/versi media (Byte Journal, aiweekly); blog Microsoft sendiri lebih netral | Byte Journal, https://bytejournal.org/news/2026-10-01-microsoft-digital-defense-report-attackers-reach-ai-advantages-first/, 1 Okt 2026 |
| 11 | Celah jadi senjata < 24 jam (median); tambal 30-60 hari | BELUM DIVERIFIKASI ke primer | Byte Journal 1 Okt 2026 (sekunder) |
| 12 | OpenAI Daybreak diluncurkan Mei 2026 untuk pertahanan siber | FAKTA (media) | Technology Magazine / Decrypt, Mei 2026; halaman resmi https://openai.com/cyber |
| 13 | CrowdStrike AI kill switch, 3 Nov 2026; manusia yang memutuskan memutus agen | FAKTA (media, belum primer) | CNBC, https://cnbc.com/2026/11/03/crowdstrike-ai-kill-switch-rogue-agents.html, 3 Nov 2026 (via hasil pencarian) |
| 14 | VAPOR PANDA dideteksi tim OverWatch CrowdStrike | FAKTA | IT Brief, https://itbrief.com.au/story/crowdstrike-uncovers-china-linked-ai-cyber-campaign, 30 Okt 2026 |
| 15 | Google Scam Detection (Messages/telepon, Gemini Nano on-device) | FAKTA, tapi ketersediaan resmi dalam Bahasa Indonesia TIDAK DITEMUKAN | detik/CNBC Indonesia, Mar 2025; Selular.ID Agt 2026 |
| 16 | Data BSSN soal hasil pertahanan berbasis AI | TIDAK DITEMUKAN | pencarian 4 Nov 2026 |

## 4. Belum pasti / diperdebatkan

- Semua angka Glasswing adalah klaim Anthropic sendiri (vendor), belum audit independen. Angka 129.000 adalah gabungan laporan mitra, "batas bawah".
- Klaim "pertama kali" Big Sleep milik Google. Peristiwanya Juli 2025, jadi sebut tahunnya; jangan disajikan sebagai berita minggu ini.
- Siapa yang unggul, penyerang atau pembela? Media membaca MDDR 2026 sebagai "penyerang duluan"; blog Microsoft lebih seimbang; Anthropic bilang tujuannya keunggulan permanen buat pembela. Ini opini yang diperdebatkan, cocok jadi bahan komentar, bukan disimpulkan.
- Rasio 75/530 adalah foto per 22 Mei 2026 (di awal masa embargo 90 hari), jadi bukan bukti "pengembang malas". Anthropic sendiri menyebut maintainer kewalahan.

## 5. Sudut lokal Indonesia

- Tidak ada data Indonesia soal AI penjaga. Relevansi ke penonton: tambalan dari temuan AI baru melindungi kalau perangkat/aplikasi di-update. (Inferensi logis, tidak butuh angka.) Riset hari 3: Kaspersky, eksploit celah software = serangan terbanyak ke UMKM Indonesia (20%), Bisnis.com 14 Sep 2026.

## 6. Batas klaim (JANGAN di naskah)

- Jangan bilang "AI sudah menang" atau "hacker AI pasti kalah".
- Jangan bilang AI yang menangkap pelaku hari 3 (VAPOR PANDA/Cairn ketahuan oleh tim manusia/peneliti).
- Jangan sebut "<24 jam" / "30-60 hari" tanpa cek primer.
- Jangan bilang 129.000 celah "sudah ditambal"; itu jumlah yang ditemukan.
- Jangan menyiratkan Scam Detection Google sudah ada di semua HP Indonesia.
- Jangan promosi produk (Mythos tidak tersedia untuk umum).

## 7. Tiga usulan sudut hook

1. **"AI nemuin 129 ribu celah keamanan dalam empat bulan. Masalahnya, yang nambal masih manusia."** (rekomendasi: angka besar + open loop langsung; sumber Anthropic 6 Okt 2026)
2. "Kemarin hacker pakai AI buat nyerang. Hari ini, AI yang ngelawan balik." (paling nyambung seri, tapi kurang tajam)
3. "Tahun lalu, untuk pertama kalinya, AI ngegagalin serangan hacker sebelum serangannya dimulai, kata Google." (cerita kuat, tapi peristiwanya 2025)

## 8. Saran kerangka

Body 1 = kemenangan (Big Sleep potong serangan duluan). Loop = "tapi ada masalah". Body 2 = AI nemu jauh lebih cepat dari manusia nambal (530 → 75, dua minggu). Body 3 / payoff (terkuat) = tambalannya baru sampai ke kamu kalau kamu klik update. CTA komentar A/B soal kebiasaan update.
