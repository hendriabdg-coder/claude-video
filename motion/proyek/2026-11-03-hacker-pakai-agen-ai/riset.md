# Lembar Riset: Hacker Pakai Agen AI (Seri AI Pengawas #3)

Tanggal riset: 2026-11-03. Peneliti: peneliti-konten. Status: menunggu gate 1.

## 1. Status akses sumber

| Sumber | Akses | Catatan |
|---|---|---|
| Anthropic, "Disrupting the first reported AI-orchestrated cyber espionage campaign" (anthropic.com/news/disrupting-AI-espionage) | Terbaca langsung (primer) | Bagian ringkas; PDF lengkap tidak dibuka |
| Anthropic, "Detecting and countering misuse of AI: August 2025" | Terbaca langsung (primer) | |
| Google GTIG AI Threat Tracker (cloud.google.com) | TIDAK dibuka langsung; dibaca lewat The Register (5 Nov 2025) | Sekunder |
| NorForge/Reuters (kasus Cairn, Okt 2026) | Laporan asli Reuters dan NorForge TIDAK dibuka; dibaca lewat The Hacker News, TNW, Fortune, SafeBreach | Sekunder semua |
| CrowdStrike VAPOR PANDA/ARTEX (29 Okt 2026) | Laporan asli TIDAK dibuka; dibaca lewat CyberScoop, IT Brief, Tech Times | Sekunder semua |
| BSSN | Dibaca lewat Bisnis.com (14 Okt 2026) | Siaran resmi BSSN tidak dibuka |
| OJK "70.000 kasus penipuan berbasis AI" | Gagal dibuka (client_error); hanya judul hasil pencarian | Jangan dipakai sebagai angka |

Semua angka kasus 2026 berasal dari media/vendor, bukan audit independen. Itu wajib tercermin di naskah ("menurut peneliti", "menurut CrowdStrike").

## 2. Ringkasan fakta (urut dari yang paling baru)

1. **CrowdStrike, 29 Okt 2026 (paling baru):** kelompok VAPOR PANDA (dituduh China, atribusi CrowdStrike) memakai ARTEX, framework pentest AI open-source, dipadu DeepSeek, menyasar 200+ organisasi di 14+ negara dalam 11 hari. CrowdStrike: kecepatan perintah bisa lebih dari 1.500/jam (versus maks ~40/jam secara manual). Kampanye mulai 17 Okt 2026 dan masih aktif. Manusia tetap ada: operator memberi instruksi dan campur tangan di keputusan penting.
2. **Reuters/NorForge, 19-20 Okt 2026:** satu penyerang berbahasa Mandarin memakai Cairn (alat pentest AI open-source) untuk mengarahkan DeepSeek dan Claude Code. Sasaran 1.200+ situs e-commerce, 100+ perusahaan dilaporkan tembus, biaya sekitar US$5.000 token (sekitar US$50 per peretasan sukses), rata-rata sedikit di bawah 23 jam per peretasan sukses. Instruksi operator kurang dari 100 karakter. Ketahuan karena peneliti memindai internet dan menemukan panel Cairn terbuka, bukan dari laporan korban.
3. **Korban bilang dampak terbatas:** Deere "found no evidence sensitive data was accessed"; SharkNinja bilang hanya situs dukungan produk terpisah; Cummins masih menyelidiki situs milik vendor. Reuters tidak bisa memastikan berapa data yang diambil.
4. **Okt 2026, bank Korea Selatan:** Fortune (mengutip Reuters/WSJ) melaporkan penyerang yang kemungkinan berbasis China memakai Artex + Claude Code; estimasi data 68.000 orang dicuri. CrowdStrike juga mengaitkan kasus ARTEX dengan penangkapan mantan pentester Korea pada 26 Okt (8,2 juta rekaman) menurut Tech Times (sekunder, hati-hati).
5. **Anthropic, 13 Nov 2025 (GTG-1002):** kampanye spionase yang menyalahgunakan Claude Code; target sekitar 30 organisasi global, "a small number of cases" berhasil. Anthropic: AI melakukan "80-90% of the campaign", manusia di "perhaps 4-6 critical decision points per hacking campaign". Ketahuan "mid-September 2025", akun diblokir, pihak terdampak diberi tahu "as appropriate". Claude "occasionally hallucinated credentials".
6. **Anthropic, 27 Agt 2025 ("vibe hacking"):** satu pelaku memakai Claude Code untuk "at least 17 distinct organizations" (kesehatan, layanan darurat, pemerintah, lembaga keagamaan), tuntutan tebusan kadang lebih dari US$500.000. Anthropic memblokir akun, membuat classifier khusus, dan membagikan indikator ke otoritas.
7. **Google GTIG, 5 Nov 2025:** PROMPTFLUX (malware yang memanggil Gemini untuk menulis ulang dirinya) masih "experimental"; PROMPTSTEAL dipakai APT28 terhadap Ukraina, disebut Google "malware querying an LLM deployed in a live operation". Google menonaktifkan akun terkait.
8. **Indonesia:** BSSN (14 Okt 2026): 3,1 miliar anomali trafik hingga Okt 2026, lebih dari 85% terkait malware; Deputi Bondan Widiawan memperingatkan AI membuat malware/ransomware lebih adaptif. Tidak ada angka BSSN khusus serangan "agen AI" (lihat bagian 3 poin 20).

## 3. Tabel klaim

| No | Klaim | Status | Sumber (judul, URL, tanggal) |
|---|---|---|---|
| 1 | VAPOR PANDA memakai ARTEX + DeepSeek terhadap 200+ organisasi di 14+ negara | FAKTA (klaim CrowdStrike) | CyberScoop, laporan CrowdStrike, https://cyberscoop.com/?p=91390, 30 Okt 2026; Tech Times, https://www.techtimes.com/articles/329874/20261102/china-hacked-200-organizations-11-days-one-human-ai-agents-command.htm, 2 Nov 2026 |
| 2 | Kampanye 11 hari; mulai 17 Okt 2026; masih aktif | FAKTA | CyberScoop 30 Okt 2026; IT Brief https://itbrief.com.au/story/crowdstrike-uncovers-china-linked-ai-cyber-campaign, 30 Okt 2026 |
| 3 | Kecepatan: "Now, with ARTEX, we could see it exceed 1,500 commands an hour" (Adam Meyers, CrowdStrike); manual historis sampai 40 perintah/jam | FAKTA (kutipan) | CyberScoop 30 Okt 2026 |
| 4 | "This is the first time that we're seeing an agentic adversary nation-state threat actor at this scale" | FAKTA (kutipan Meyers; klaim "pertama" milik CrowdStrike) | CyberScoop 30 Okt 2026 |
| 5 | Sekitar 140 target sensitif dikompromikan, ~70% | FAKTA bersyarat: 70% termasuk "moderate-confidence", CyberScoop tidak menyatakan 140 = 70% dari 200 | CyberScoop 30 Okt 2026 |
| 6 | Tech Times: hanya 9 organisasi terkonfirmasi post-exploitation, 12+ lagi password spraying | FAKTA menurut Tech Times; BERTENTANGAN dengan angka ~140 di CyberScoop | Tech Times 2 Nov 2026 (sumber sekunder, kurang kuat) |
| 7 | Operator manusia tetap ada: "did not operate entirely independently"; transkrip menunjukkan operator memberi instruksi berbahasa Mandarin dan campur tangan di keputusan kunci | FAKTA | IT Brief 30 Okt 2026 |
| 8 | Seorang penyerang berbahasa Mandarin, Cairn, DeepSeek + Claude Code, 1.200+ situs ditarget | FAKTA (laporan NorForge via Reuters) | The Hacker News, https://thehackernews.com/2026/10/hackers-use-autonomous-ai-agents-to.html, 20 Okt 2026; TNW, https://thenextweb.com/news/ai-agents-hacker-cairn-100-sites-deere-norforge, 19 Okt 2026 |
| 9 | 100+ perusahaan dilaporkan tembus; mis. Deere, SharkNinja, Cummins | FAKTA bersyarat ("reportedly"); jumlah data yang diambil tidak diketahui | Fortune, https://fortune.com/2026/10/21/powerful-new-ai-models-are-powering-a-growing-wave-of-cyber-attacks-experts-say/, 21 Okt 2026; TNW 19 Okt 2026 |
| 10 | Biaya sekitar US$5.000 token, ~US$50 per peretasan sukses; NorForge juga menulis rata-rata ~US$5 per tugas termasuk yang gagal | FAKTA (estimasi satu peneliti, Snorre Fagerland) | The Hacker News 20 Okt 2026; TNW 19 Okt 2026 |
| 11 | Rata-rata sukses "a little under 23 hours"; tingkat sukses sekitar 10% | FAKTA (estimasi NorForge; klaster tidak sebanding langsung) | The Hacker News 20 Okt 2026; TNW 19 Okt 2026 |
| 12 | Instruksi operator kurang dari 100 karakter Mandarin | FAKTA (via Reuters/The Hacker News). SafeBreach tidak konsisten soal satuannya | The Hacker News 20 Okt 2026; Security Boulevard/SafeBreach, https://securityboulevard.com/2026/10/one-hacker-5000-100-breaches-the-autonomous-ai-attack-cisos-cant-ignore/, 22 Okt 2026 |
| 13 | Ketahuan karena peneliti memindai internet cari panel Cairn terbuka; aktivitas terlihat sejak sekitar 2 Okt | FAKTA | The Hacker News 20 Okt 2026 |
| 14 | Model "claudecode_deepseek-v4.1-flash" mungkin Claude Code menjalankan DeepSeek; "tidak dikonfirmasi" NorForge/Reuters | TERSIRAT (inferensi peneliti). Fortune/SafeBreach menulis "DeepSeek dan Claude Code" lebih tegas | TNW 19 Okt 2026; The Hacker News 20 Okt 2026 |
| 15 | Respons Anthropic/DeepSeek terhadap kasus Cairn (blokir akun, pernyataan) | TIDAK DISEBUT / tidak ditemukan | TNW 19 Okt 2026: "includes no statement from either company" |
| 16 | Pembuat Cairn ("le1xia0"): alatnya "not designed for hacking attacks" | FAKTA (kutipan ke Reuters) | The Hacker News 20 Okt 2026; TNW 19 Okt 2026 |
| 17 | Fagerland: "It's not script kiddie stuff." | FAKTA (kutipan Reuters) | TNW 19 Okt 2026 |
| 18 | Korea Selatan: Artex + Claude Code, ~68.000 orang datanya dicuri | FAKTA bersyarat ("likely based in China", angka estimasi) | Fortune 21 Okt 2026 |
| 19 | Ahli: "These AI systems are now both more capable of hacking and are able to act more autonomously" (Jessica Ji, Georgetown CSET) | FAKTA (kutipan) | Fortune 21 Okt 2026 |
| 20 | Data BSSN khusus serangan "agen AI" otonom di Indonesia | TIDAK DITEMUKAN | Pencarian BSSN/Bisnis.com, 3 Nov 2026 |
| 21 | BSSN: 3,1 miliar anomali trafik hingga Okt 2026, >85% terkait malware; Bondan Widiawan: AI bisa membuat malware/ransomware "lebih adaptif dan mampu menghindari mekanisme pertahanan" | FAKTA (angka umum, bukan khusus AI agen) | Bisnis.com, https://teknologi.bisnis.com/read/20261014/84/2012594/bssn-catat-anomali-trafik-31-miliar-hingga-oktober-2026-didominasi-malware, 14 Okt 2026 |
| 22 | Kaspersky: 92% UMKM Indonesia mengalami insiden siber setahun terakhir; terbanyak eksploitasi celah software 20%, phishing 19%, malware massal 18%; survei 18 negara | FAKTA (survei vendor; bukan khusus AI) | Bisnis.com, https://teknologi.bisnis.com/read/20260914/84/2003898/kaspersky-92-umkm-indonesia-alami-insiden-siber-phishing-malware-paling-sering, 14 Sep 2026 |
| 23 | GTG-1002: AI melakukan "80-90% of the campaign"; sekitar 30 target; "small number of cases" berhasil | FAKTA (klaim Anthropic) | Anthropic, "Disrupting the first reported AI-orchestrated cyber espionage campaign", https://www.anthropic.com/news/disrupting-AI-espionage, 13 Nov 2025 (update 14 Nov) |
| 24 | Manusia di "perhaps 4-6 critical decision points per hacking campaign" | FAKTA | Anthropic, sama, 13 Nov 2025 |
| 25 | Koreksi Anthropic: "thousands of requests, often multiple per second" (bukan "per detik" ribuan) | FAKTA (pembetulan di halaman Anthropic) | Anthropic, sama |
| 26 | Anthropic menemukan aktivitas "mid-September 2025", blokir akun "as they were identified", memberi tahu pihak terdampak "as appropriate" | FAKTA | Anthropic, sama |
| 27 | Claude "occasionally hallucinated credentials" | FAKTA | Anthropic, sama; The Hacker News, https://thehackernews.com/2025/11/chinese-hackers-use-anthropics-ai-to.html, 14 Nov 2025 |
| 28 | GTG-1002: Anthropic menyebut pelaku didukung negara China | TERSIRAT/tidak diverifikasi di halaman yang dibaca (halaman yang terbaca tidak mengutip kalimat atribusi). Cek ulang sebelum dipakai | The Hacker News 14 Nov 2025 (judul "Chinese hackers") |
| 29 | Agustus 2025: pelaku memakai Claude Code untuk "at least 17 distinct organizations"; tebusan kadang >US$500.000 | FAKTA | Anthropic, "Detecting and countering misuse of AI: August 2025", https://www.anthropic.com/news/detecting-countering-misuse-aug-2025, 27 Agt 2025 |
| 30 | Respons Agt 2025: akun diblokir, classifier khusus, indikator dibagi ke otoritas | FAKTA | Anthropic, sama |
| 31 | PROMPTFLUX masih "experimental", belum bisa menembus jaringan korban | FAKTA | The Register, https://www.theregister.com/2025/11/05/attackers_experiment_with_gemini_ai/, 5 Nov 2025 |
| 32 | PROMPTSTEAL dipakai APT28 vs Ukraina, "malware querying an LLM deployed in a live operation"; atribusi APT28 berasal dari pernyataan pemerintah AS/Inggris | FAKTA | The Register 5 Nov 2025 |
| 33 | Hugging Face (Juli 2026) pindah ke model terbuka GLM 5.2 karena model tertutup menolak permintaan pertahanan; OpenCode 18 Okt 2026 ~1,4% pengguna terdampak | FAKTA menurut Fortune (belum dicek silang; bukan inti topik) | Fortune 21 Okt 2026 |
| 34 | Tips CrowdStrike: "patching internet-facing systems and deploying endpoint detection and response agents" | FAKTA (rekomendasi untuk organisasi) | IT Brief 30 Okt 2026 |
| 35 | Tips Kaspersky untuk UMKM: batasi akses, cabut akses karyawan yang keluar, backup otomatis, persetujuan IT untuk software baru, latih staf kenali deepfake/vishing | FAKTA (rekomendasi vendor) | Bisnis.com 14 Sep 2026 (URL di no. 22) |

## 4. Belum pasti / diperdebatkan

- **Seberapa "otonom":** Anthropic bilang 80-90%, tetapi BleepingComputer (14 Nov 2025) mencatat keraguan. Kevin Beaumont: "The operational impact should likely be zero - existing detections will work for open source tooling, most likely"; ia juga menyoroti tidak adanya IoC. Daniel Card: "This Anthropic thing is marketing guff." Beberapa peneliti tak bernama menyebutnya dibesar-besarkan. Anthropic tidak membalas langsung di artikel itu, dan meminta detail teknis tidak dijawab.
- Anthropic sendiri mengakui Claude kadang berhalusinasi dan melebih-lebihkan temuan, yang menghambat otonomi penuh.
- **Kasus Cairn:** "otonom" berarti agen mengerjakan hampir semua, tetapi manusia menentukan target dan tujuan serta bisa menambah petunjuk (TNW). Tingkat sukses ~10%. Angka US$50 per peretasan adalah perkiraan kasar satu peneliti dan NorForge sendiri menyebut ketidakpastiannya "considerable". Korban membantah dampak besar.
- **VAPOR PANDA:** semua angka dari CrowdStrike (vendor); atribusi China milik CrowdStrike. Angka ~140 (CyberScoop) bertentangan dengan 9 terkonfirmasi (Tech Times). Meyers sendiri bilang tekniknya tidak baru; yang berubah kecepatan dan skala.
- Peran Claude Code di kasus Cairn dan Korea hanya "dilaporkan" / inferensi; respons Anthropic tidak ditemukan.
- Debat model terbuka vs tertutup (Fortune): Amodei memperingatkan risiko model terbuka; pihak lain bilang model terbuka lebih menguntungkan pembela.
- Laporan asli Reuters, NorForge, dan CrowdStrike belum dibaca langsung. Sebelum naskah final, sebaiknya angka ditandai "menurut".

## 5. Sudut lokal Indonesia

- **Data khusus agen AI di Indonesia: tidak ditemukan.** Tidak ada laporan BSSN/resmi yang menghitung serangan oleh agen AI otonom di Indonesia.
- Konteks umum yang ada: BSSN 3,1 miliar anomali trafik hingga Okt 2026 (>85% malware) dan peringatan Bondan Widiawan soal AI (Bisnis.com, 14 Okt 2026). Kaspersky: 92% UMKM Indonesia mengalami insiden siber setahun terakhir; kendala utama: kesadaran staf non-IT rendah (26%), software/hardware usang (23%) (Bisnis.com, 14 Sep 2026).
- Hubungan ke Indonesia adalah inferensi: korban kasus Cairn adalah situs e-commerce AS/Kanada/Australia/Jepang (SafeBreach), bukan Indonesia. Jangan menyiratkan pelaku sudah menyerang Indonesia. Kasus ini relevan sebagai "arah tren", bukan bukti serangan lokal.

## 6. Tips praktis (bersumber)

1. Perbarui (patch) software dan sistem yang terhubung internet. Alasan: exploit celah software adalah serangan terbanyak pada UMKM Indonesia (20%, Kaspersky) dan CrowdStrike menyarankan "patching internet-facing systems". Sumber di tabel no. 22, 34.
2. Batasi akses dan cabut akun karyawan yang sudah keluar; aktifkan backup otomatis (Kaspersky, no. 35). Catatan: sumber yang dibaca tidak menyebut MFA, jadi jangan mengutip MFA sebagai rekomendasi sumber ini. Kalau mau menyebut MFA, perlu sumber tambahan.

## 7. Batas klaim (JANGAN dikatakan di naskah)

- Jangan bilang "AI menyerang sendiri tanpa manusia" / "100% otomatis". Manusia menentukan target dan tujuan di semua kasus.
- Jangan tulis "100 perusahaan dibobol dan datanya dicuri": sumber bilang "reportedly" dan data yang diambil tidak diketahui; Deere tidak menemukan bukti data sensitif diakses.
- Jangan sebut "Claude/Anthropic menyerang" atau mengesankan Anthropic bersalah. Di kasus Cairn peran Claude Code hanya dilaporkan dan tak dikonfirmasi; respons Anthropic tidak ditemukan. Di kasus 2025, Anthropic yang mendeteksi dan menghentikan.
- Jangan sebut China sebagai fakta mutlak: atribusi milik CrowdStrike / "kemungkinan".
- Jangan tulis US$50 per peretasan sebagai harga pasti; "perkiraan peneliti".
- Jangan sebut kasus ini terjadi di Indonesia atau menimpa UMKM Indonesia.
- Jangan bilang "serangan AI pertama di dunia" tanpa atribusi; "pertama" adalah klaim Anthropic (2025) dan CrowdStrike (2026).
- Jangan pakai angka 70.000 penipuan AI (OJK): tidak terverifikasi.
- Jangan sebut angka 9 organisasi atau 140 target tanpa menyebut sumbernya bertentangan; lebih aman pakai "200+ organisasi dalam 11 hari, menurut CrowdStrike".
- Jangan menyatakan hacker bisa dihentikan hanya dengan satu tips; tips hanyalah mengurangi risiko.
- Jangan memberi detail teknis yang bisa meniru serangan (nama alat boleh sebagai fakta berita; tanpa cara pakai).

## 8. Tiga usulan sudut hook

1. "Satu orang, 1.200 situs jadi sasaran, biayanya sekitar 5 ribu dolar token AI, kata peneliti." (konversi rupiah butuh kurs bersumber sebelum dipakai.)
2. "Dulu hacker butuh tim. Sekarang, menurut peneliti, cukup satu orang dan perintah di bawah 100 karakter."
3. "Anthropic bilang AI menjalankan 80-90% serangan. Peneliti keamanan bilang itu dibesar-besarkan. Siapa yang benar?" (cocok dengan tema seri AI Pengawas dan debat "otonom").

## 9. Saran kerangka (bukan naskah)

Sambungan ke Hari 2: ini jawaban "agen AI yang dipakai buat nyerang". Poin terkuat untuk body terakhir: kasus terbaru (CrowdStrike, 29 Okt 2026) atau kecepatan 1.500 perintah/jam vs 40. Open loop yang bisa dibayar: "manusianya masih ada, tapi apa tugasnya?" Sambungan CTA seri: Part 4 tentang bagaimana AI dipakai untuk bertahan (konteks Hugging Face/OpenAI Daybreak di Fortune, perlu riset terpisah).
