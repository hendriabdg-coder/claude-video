# Lembar Riset: AI Pemburu Celah Keamanan (Seri Internet Jebol #2)

Tanggal riset: 2026-10-25. Disusun oleh peneliti-konten. Status: menunggu gate 1.
Legenda: FAKTA = disebut sumber; TERSIRAT = kesimpulan dari sumber; TIDAK DISEBUT = sumber diam.
Tanda [P] = sumber primer dibuka langsung. [S] = sekunder. [R] = hanya dari ringkasan hasil pencarian, halaman belum dibuka langsung.

## Ringkasan fakta

1. Google mengumumkan Gemini 4 Argon pada 30 Sep 2026. Google menulis: "Argon can autonomously find, validate, and patch critical software vulnerabilities." Awalnya hanya untuk "trusted cyber defenders" lewat Fairwind Program. [P]
2. Rilis luas 13 Okt 2026: "Gemini 4 Argon is now globally available today for developers and enterprises via the API", dan untuk "Google AI Ultra and Pro subscribers in the Gemini app and AI Mode in Search". [P]
3. Di Indonesia: KompasTekno (14 Okt 2026) menulis Argon "belum bisa dicoba secara gratis"; Google AI Pro Rp 309.000/bulan, Ultra Rp 1,58 juta/bulan. [S]
4. Versi "tanpa cyber guardrails" hanya untuk pelamar Fairwind yang lolos vetting; Google melarang pembuatan malware. [P]
5. Anthropic (29 Sep 2026): GLM-5.3 (open-weight, Zhipu/Z.ai) membuat eksploit end-to-end 50 dari 410 percobaan di ExploitBench; Claude Mythos Preview 56 dari 410. [P]
6. Anthropic: safeguard GLM-5.3 bisa ditembus 64%-100% dengan teknik sederhana; biaya "abliteration" sekitar $4.400. [P]
7. Angka AI pemburu celah: mitra Project Glasswing Anthropic melaporkan "at least 129,000 verified software vulnerabilities" (Apr-Jul 2026), tapi data survei sebagian mitra dan tingkat patch tidak lengkap. [P]
8. Pedang bermata dua diakui sumber resmi sendiri: Anthropic dan Google sama-sama menyebut kemampuan yang sama dipakai bertahan dan menyerang.

## Tabel klaim

| Klaim | Status | Sumber (judul, URL, tanggal) |
|---|---|---|
| Argon diumumkan 30 Sep 2026; "can autonomously find, validate, and patch critical software vulnerabilities" | FAKTA | Google, "Gemini 4 Argon: our next era of frontier intelligence", https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/, 30 Sep 2026 [P] |
| Awal: "rolling out to a set of trusted cyber defenders through our Fairwind Program"; belum publik | FAKTA | Sama seperti di atas, 30 Sep 2026 [P] |
| Argon "uncovered a critical vulnerability exposing sensitive personal information across healthcare software"; Wiz memakainya lewat "Scan for Good" | FAKTA (klaim Google sendiri) | Sama, 30 Sep 2026. Software tidak disebut nama, status perbaikan tidak jelas (SecurityWeek, https://www.securityweek.com/google-launches-gemini-4-argon-with-guardrail-free-access-for-vetted-defenders/, 1 Okt 2026) [P/S] |
| 13 Okt: Argon "now globally available today for developers and enterprises via the API"; Pro dan Ultra di app Gemini dan AI Mode | FAKTA | Google, "Gemini 4 Argon: Built to solve your hardest problems", https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/, 13 Okt 2026 [P] |
| Daftar negara tersedia | TIDAK DISEBUT | Halaman Google di atas hanya bilang global, tanpa daftar negara |
| Bisa dipakai di Indonesia, berbayar | FAKTA (sekunder) | KompasTekno, "Gemini 4 Argon Sudah Bisa Dicoba di Indonesia...", https://tekno.kompas.com/read/2026/10/14/09270027/gemini-4-argon-sudah-bisa-dicoba-di-indonesia-model-ai-google-untuk-tugas?page=all, 14 Okt 2026 [S] |
| Harga: "Google AI Pro dibanderol Rp 309.000 per bulan, sementara Google AI Ultra Rp 1,58 juta per bulan" | FAKTA (sekunder) | KompasTekno, tautan sama, 14 Okt 2026 |
| Fairwind: akses hanya tim keamanan internal, wajib MFA tahan phishing; "Malicious tasks such as creating malware are not permitted"; "over 650 partners globally" | FAKTA | Google DeepMind, "Fairwind Program", https://deepmind.google/fairwind-program/, tanpa tanggal [P] |
| Versi tanpa guardrail untuk pelamar Fairwind "on a rolling basis"; ada "hundreds of additional" mitra | FAKTA | Google 13 Okt 2026 (tautan "Built to solve") [P] |
| Argon tidak tersedia di Indonesia lewat Fairwind (apakah ada mitra Indonesia) | TIDAK DISEBUT | Daftar mitra tidak dipublikasikan |
| Argon seri 68% CWE-bench v1, imbang dengan GPT-6 Astra dan Grok 4.7 | FAKTA (angka Google, belum diverifikasi independen) | SecurityWeek, 1 Okt 2026 [S] |
| Google: peningkatan kemampuan cari celah juga menaikkan skor tes serangan, dari 5 ke 12 dari 12 skenario serangan simulasi; maksud desain "to give defenders an advantage over attackers" | FAKTA | Google, "Developing Gemini 4 Argon responsibly and safely", https://blog.google/innovation-and-ai/technology/safety-security/gemini-4-model-safety-security/, 13 Okt 2026 [P] |
| Google memasang 3 lapis safeguard real-time (screening input, probe internal, monitoring) | FAKTA | Sama, 13 Okt 2026 [P] |
| Anthropic: GLM-5.3 "develops end-to-end exploits in 50 of 410 attempts"; Mythos Preview "56 of 410" | FAKTA | Anthropic, "GLM-5.3 and the spread of advanced cyber capabilities", https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities, 29 Sep 2026 [P] |
| GLM-5.3 membajak alur kontrol penuh di 4% percobaan vs Mythos 6% (100 tugas); model lama (Opus 4.6, GLM-5.2) 0 | FAKTA | Sama, 29 Sep 2026 [P] |
| "attackers can bypass GLM-5.3's safeguards between 64% and 100% of the time with simple techniques in our simulated tests"; Claude yang ber-safeguard tidak tertembus teknik yang sama | FAKTA | Sama [P] |
| Abliteration GLM-5.3 sekitar 2.200 jam GPU, sekitar $4.400; penolakan turun dari >90% ke sekitar 3% dan 2% | FAKTA | Sama [P] |
| "GLM-5.3 is unlike other frontier models in that it has been released without meaningful safeguards"; "a critical threshold in freely accessible capabilities has now been crossed" | FAKTA | Sama [P] |
| CAISI (NIST) menyebut GLM-5.3 "the most cyber-capable open-weight model released to date" | FAKTA (dikutip Anthropic) | Sama [P] |
| Kata "mendekati kemampuan Claude" | TERSIRAT, perlu presisi | Pembandingnya Claude Mythos Preview (model terbatas), bukan semua Claude |
| Mythos Preview menemukan bug OpenBSD 27 tahun dan FFmpeg 16 tahun; tidak dirilis umum | FAKTA | Help Net Security, https://www.helpnetsecurity.com/2026/04/08/anthropic-claude-mythos-preview-identify-vulnerabilities/, 8 Apr 2026 [S]; primer: https://red.anthropic.com/2026/mythos-preview/ [R] |
| Mitra Glasswing menemukan ">10 ribu" celah high/critical; "75 of the 530 high- or critical-severity bugs we've reported have now been patched" | FAKTA | Anthropic, "Project Glasswing: An initial update", https://www.anthropic.com/news/glasswing-initial-update, 22 Mei 2026 [P] |
| "at least 129,000 verified software vulnerabilities between April and July 2026"; "likely an undercount" (survei sebagian mitra); tidak ada total patch | FAKTA | Anthropic, "Expanding the Cyber Verification Program", https://www.anthropic.com/news/cyber-verification-program, 6 Okt 2026 [P] |
| "The same improvements that make the model substantially more effective at patching" juga membuatnya lebih baik mengeksploitasi; Mythos-class model akan membuat eksploitasi "dramatically cheaper and easier" | FAKTA | Help Net Security (8 Apr 2026) [S]; Anthropic Glasswing update (22 Mei 2026) [P] |
| Dari 1.061 celah temuan AI, 14 (1,3%) terkonfirmasi dieksploitasi di dunia nyata | FAKTA (dari ringkasan, belum dibuka) | VulnCheck, https://www.vulncheck.com/blog/ai-assisted-vulnerability-discovery, H1 2026 [R] |
| Maintainer curl: dari 5 laporan "terkonfirmasi" Mythos, hanya 1 valid sebagai CVE | FAKTA (belum dibuka langsung) | Ringkasan Sonatype, https://www.sonatype.com/resources/research/ai-vulnerability-storm [R] |
| BSSN: sekitar 3,1 miliar anomali trafik hingga Okt 2026, lebih dari 85% terkait malware | FAKTA (hanya dari ringkasan, halaman 403) | Bisnis.com, https://teknologi.bisnis.com/read/20261014/84/2012594/bssn-catat-anomali-trafik-31-miliar-hingga-oktober-2026-didominasi-malware, 14 Okt 2026 [R] |
| BSSN: 1,5 miliar anomali trafik 1 Jan-15 Apr 2026; anomali belum tentu serangan berhasil | FAKTA (ringkasan) | detikInet, https://inet.detik.com/security/d-8458200/duh-ri-dihantam-1-5-miliar-anomali-trafik-dalam-4-bulan, Apr 2026 [R] |
| Ada serangan Indonesia yang dilakukan oleh AI pemburu celah | TIDAK DISEBUT | Tidak ditemukan |
| Kerugian perbankan Rp 8 triliun (JawaPos, 30 Apr 2026) | Belum diverifikasi, hanya judul | https://www.jawapos.com/teknologi/2604300241/serangan-siber-menggila-perbankan-jadi-target-utama-kerugian-tembus-rp-8-triliun [R]; jangan dipakai tanpa dibuka |

## Belum pasti / diperdebatkan

- Status Argon bertentangan antar sumber: Google 30 Sep menulis belum publik (Ultra dan API berbayar lebih dulu, Pro tidak disebut); Google 13 Okt menulis global untuk API dan Pro/Ultra. Artikel JournalArta 4 Okt masih menyebut terbatas. Pakai tanggal 13 Okt. Versi tanpa guardrail tetap hanya untuk Fairwind (vetting), bukan untuk pelanggan Pro/Ultra.
- Klaim "dikabarkan tersedia untuk Pro/Ultra" benar menurut Google 13 Okt, tapi daftar negara TIDAK DISEBUT. Konfirmasi Indonesia hanya dari KompasTekno (sekunder). Cek langsung di akun Indonesia sebelum menyebut "bisa dipakai sekarang".
- Semua angka performa Argon (68% CWE-bench, 2x temuan Wiz) adalah klaim Google, tanpa verifikasi independen. Celah layanan kesehatan tidak disebut namanya dan status perbaikannya tidak jelas.
- Harga rupiah API berbeda antar artikel Kompas (Rp 35.000 vs Rp 35.800 per 1 juta token input); itu konversi media, bukan dari Google.
- Angka "129.000" adalah laporan mitra, batas bawah, belum tentu semua dipatch. Sonatype menyebut sekitar 60 CVE temuan AI yang sudah publik; sebagian besar masih embargo. Ada kasus klaim AI yang gugur (curl). Jangan tulis "AI sudah menemukan 129 ribu celah yang diperbaiki".
- "Mendekati Claude" harus ditulis "mendekati Claude Mythos Preview", model terbatas yang tidak dirilis umum. Tes Anthropic adalah simulasi; belum ada bukti GLM-5.3 dipakai dalam serangan nyata (TIDAK DISEBUT di laporan yang dibuka).
- Data BSSN: halaman utama 403, angka hanya dari ringkasan. "Anomali" bukan "serangan". Satu pejabat BSSN menyebut kapasitas monitoring belum 10% trafik (ringkasan, 2025/2026 tidak pasti).

## 3 usulan sudut hook

1. "AI yang sama bisa menambal celah di rumah sakit atau membobolnya; Google sendiri bilang peningkatannya naik di dua arah."
2. "Model AI gratis bisa membuat eksploit di 50 dari 410 percobaan, dan pengamannya bisa dilepas dengan biaya sekitar Rp 70 jutaan." (hitung konversi sendiri dari $4.400; tulis dalam dolar jika ragu kurs)
3. "Google bilang AI barunya bisa temukan, validasi, dan tambal celah sendiri; kamu bisa pakai di Indonesia mulai Rp 309 ribu per bulan, tapi versi tanpa pengaman cuma untuk yang lolos seleksi."

## Catatan untuk naskah

- Aman ditulis: Argon dan GLM-5.3 sebagai "klaim Google" dan "laporan Anthropic". Hindari "AI jebol sistem Indonesia".
- Sudut Indonesia: harga langganan (Rp 309.000 dan Rp 1,58 juta), data BSSN (anomali, bukan serangan berhasil), dampak ke pekerja IT/pemilik usaha: tidak ditemukan sumber spesifik.
- Saran serah terima: pin/sorotan Seri Internet Jebol di profil.
