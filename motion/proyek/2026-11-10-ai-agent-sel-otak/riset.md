# Lembar Riset: Ribuan AI Agent Meneliti Sel Otak (Hari 10, tayang 2026-11-10)

Tanggal riset: 2026-11-07. Peneliti: peneliti-konten.

## Status akses sumber (PENTING)
- WebFetch ke openai.com, biorxiv.org, tomsguide, unite.ai, genengnews, xenospectrum GAGAL (host tidak bisa diakses dari sesi ini). Hanya github.com yang terbuka.
- Semua isi di bawah berasal dari RINGKASAN hasil pencarian web (halaman OpenAI, bioRxiv, dan media muncul di hasil, tetapi teks aslinya TIDAK dibaca langsung). Jadi kalimat dalam tanda kutip BELUM terverifikasi kata per kata. Agent utama/Endrich perlu membuka halaman OpenAI dan preprint bioRxiv lewat browser dan mencocokkan angka sebelum jadi teks layar.
- Halaman primer yang ditemukan (belum dibuka): OpenAI https://openai.com/index/scaling-ai-research-for-complex-biological-data/ (21 Okt 2026); bioRxiv https://www.biorxiv.org/content/10.64898/2026.10.15.759436v1 (diposting 16 Okt 2026 menurut ringkasan; satu sumber menyebut 15 Okt dari DOI "2026.10.15", belum pasti).
- Press release PR Newswire (via Morningstar), 21 Okt 2026: https://www.morningstar.com/news/pr-newswire/20261021sf77380/perturbai-and-openai-unveil-first-of-its-kind-ai-reasoning-agents-to-scale-biomedical-discovery (belum dibuka).

## Koreksi untuk draf hook
Draf: "Ribuan AI Agent membantu analisis jutaan sel otak hanya dalam 32 menit."
1. "Ribuan agent": angka persis dilaporkan 1.946 (R&D World) atau "hampir 2.000" (banyak media). OpenAI sendiri menurut satu ringkasan hanya menulis "thousands". Aman: "hampir 2.000 agent" atau "ribuan" (dua-duanya benar secara kasar; 1.946 < 2.000, jadi "ribuan" agak longgar; lebih aman "hampir 2.000").
2. "Jutaan sel": angka dataset berbeda antar sumber, 7,7 juta inti sel (OpenAI/TechRepublic/Tech Times) vs 8 juta (beberapa media, AI Weekly, TNW). Aman: "jutaan" atau "sekitar 7,7 juta".
3. "Sel otak" harus ditambah "tikus" (mouse). Ini bukan sel otak manusia. Datanya sudah ada (data eksperimen lama), bukan eksperimen baru.
4. "32 menit" = waktu agent menganalisis data yang sudah ada, bukan waktu menemukan sesuatu atau menyelesaikan penelitian. Pembanding "berbulan-bulan sampai setahun" adalah ESTIMASI peneliti, bukan uji waktu nyata.
5. "membantu analisis" sudah tepat. Jangan "menemukan obat/penyebab penyakit". Hasilnya hipotesis yang belum divalidasi di lab.

## Ringkasan fakta (5-8 poin)
1. OpenAI, PerturbAI, dan Scripps Research mengumumkan riset ini 21 Okt 2026. Preprint di bioRxiv "Distributed AI agents enable comprehensive discovery of biological insights at scale" (penulis utama Alexander Sun dkk.), BELUM peer review.
2. Metode "distributed biological reasoning": satu agent per gangguan gen (perturbation); tiap agent menelaah perubahan aktivitas sel dan mencari literatur untuk penjelasan; laporan digabung jadi "reasoning atlas".
3. Skala: 1.946 agent GPT-Rosalind paralel (R&D World; media lain "hampir 2.000"), data atlas CRISPR (Perturb-seq) seluruh otak tikus, sekitar 7,7 juta sel (sumber lain 8 juta), selesai dalam 32 menit.
4. Hasil berupa hipotesis: Tsc2 vs Tsc1 berbeda dampaknya di cerebellum (Tsc2 mengubah puluhan gen komunikasi saraf, Tsc1 hampir tidak); gangguan Dctn1 menaikkan gen pembuat kolesterol sehingga muncul pertanyaan baru soal distribusi kolesterol di neuron. Mekanisme belum diuji eksperimen.
5. Uji internal: tanpa akses ke naskah studi aslinya, sistem memulihkan temuan studi atlas asli (angka konflik: 52 dari 55 vs 48 dari 55, lihat tabel); pakar buta lebih memilih laporan multi-agent 75% (45 dari 60) vs agent tunggal; sitasi literatur 700+ vs 11 pada beban terbesar.
6. Konflik kepentingan: enam penulis karyawan OpenAI, dua karyawan PerturbAI, Grace Zheng dan Xin Jin salah satu pendiri PerturbAI (pernyataan competing-interest preprint, via ringkasan Blockchain.News/Tech Times). Xin Jin penulis korespondensi.
7. Kode (MIT) di GitHub dan atlas di Hugging Face terbuka; README GitHub: memakai Codex CLI secara default, data 10,8 GB.
8. Biaya komputasi/token: tidak ditemukan di sumber yang terbaca.

## Tabel klaim | status | sumber
| Klaim | Status | Sumber |
|---|---|---|
| Diumumkan 21 Okt 2026 oleh OpenAI, PerturbAI, Scripps | FAKTA (via ringkasan; halaman OpenAI belum dibuka) | OpenAI, "Scaling AI research for complex biological data", https://openai.com/index/scaling-ai-research-for-complex-biological-data/ , 21 Okt 2026; TNW https://thenextweb.com/news/openai-ai-agents-mouse-brain-crispr-atlas |
| Satu outlet menulis tanggal 1 Okt 2026 | Konflik, kemungkinan salah ketik; pakai 21 Okt | via ringkasan pencarian (outlet tidak teridentifikasi) |
| Preprint bioRxiv, belum peer review | FAKTA | bioRxiv, "Distributed AI agents enable comprehensive discovery of biological insights at scale", https://www.biorxiv.org/content/10.64898/2026.10.15.759436v1 , posting 15/16 Okt 2026 (tanggal konflik antar ringkasan); TNW |
| 1.946 agent | FAKTA (satu outlet) | R&D World, https://www.rdworldonline.com/openai-deploys-nearly-2000-gpt-rosalind-agents-to-generate-biological-research-leads-in-32-minutes/ , Okt 2026 |
| "Hampir 2.000" agent | FAKTA | TNW; TechRepublic https://www.techrepublic.com/article/news-openai-ai-agents-brain-research/ ; AllSci https://allsci.com/news/research/ai-agents-brain-disease-openai-and-partners-use/ |
| OpenAI sendiri hanya menulis "thousands" | TERSIRAT/belum dicek di halaman asli | ringkasan pencarian, ai-daily.news |
| ~7,7 juta sel (inti sel) | FAKTA (satu kelompok sumber) | Tech Times https://www.techtimes.com/articles/329363/20261022/openai-drug-discovery-swarm-decoded-77-million-brain-cells-32-minutes.htm , 22 Okt 2026 |
| 8 juta sel | Konflik dengan 7,7 juta | AI Weekly https://aiweekly.co/alerts/openai-perturbai-and-scripps-run-2000-gpt-rosalind-agents-on-8m-cell-brain ; Digg |
| Rangkaian ringkasan: "1,946 GPT-Rosalind agents, running in parallel, analyzing existing data from millions of mouse brain cells in 32 minutes" | FAKTA (parafrase ringkasan, belum diverifikasi sebagai kutipan resmi) | R&D World (di atas) |
| 32 menit = waktu analisis data yang sudah ada | FAKTA | OpenAI; R&D World |
| Pembanding manual "beberapa bulan sampai setahun" | FAKTA bahwa itu ESTIMASI peneliti, bukan pengukuran | R&D World; satu outlet: asumsi 15 menit per gangguan gen dan 10 menit per makalah |
| Model: GPT-Rosalind (model OpenAI khusus biologi, diumumkan 16 Apr 2026, akses terbatas) | FAKTA | OpenAI "Introducing GPT-Rosalind" https://openai.com/index/introducing-gpt-rosalind/ ; Axios 16 Apr 2026 https://axios.com/2026/04/16/openai-models-life-sciences-drugs |
| Framework: Codex CLI default, MIT license, data 10,8 GB Parquet | FAKTA | GitHub README https://github.com/jinlabneurogenomics/distributed_agent (dibuka langsung 2026-11-07) |
| Jumlah agent/sel/runtime di README | TIDAK DISEBUT | GitHub README (sama) |
| Tiap agent menangani satu gangguan gen, baca data ekspresi per tipe sel + literatur | FAKTA | GitHub README; R&D World |
| Dataset asli: in vivo Perturb-seq otak utuh tikus | FAKTA | GitHub README; "Genome-scale functional mapping of the mammalian whole brain with in vivo Perturb-seq" https://www.genomicmedicine.ac.uk/node/170 (belum dibaca detail) |
| Tsc2 vs Tsc1 berbeda di cerebellum | FAKTA sebagai temuan hipotesis | ringkasan pencarian atas preprint/OpenAI; TNW |
| Dctn1 -> gen kolesterol naik; mekanisme belum diuji | FAKTA (hipotesis) | OpenAI (via ringkasan); AllSci |
| Dctn1 dikaitkan Perry syndrome | FAKTA (satu ringkasan, bukan dari OpenAI) | ringkasan pencarian |
| Temuan tervalidasi di lab basah | TIDAK ditemukan; sumber: "still awaiting experimental validation", butuh uji di sel manusia | AllSci; TechRepublic; ringkasan Tom's Guide |
| 52 dari 55 temuan studi asli pulih (94,5%) | Konflik | Tech Times / ai-daily.news (via ringkasan) |
| 48 dari 55 cocok/disempurnakan; 52 dari 55 minimal sebagian pulih | Menjelaskan konflik: dua definisi berbeda | aiwiki.ai/wiki/distributed_biological_reasoning (wiki pihak ketiga); AllSci menulis "48 of 55" |
| Pakar buta pilih multi-agent 75% (45 dari 60 yang bisa dinilai) vs 17% agent tunggal | FAKTA klaim penulis (tidak ada konfirmasi independen) | AllSci; ai-daily.news; ringkasan pencarian |
| Sitasi 700+ vs 11 (agent tunggal) | FAKTA klaim penulis | GIGAZINE https://gigazine.net/gsc_news/en/20261022-openai-research-complex-biological-data/ ; Tech Times |
| Keterbatasan: akurasi turun bila perturbation berkerabat tidak ada di data latih; butuh uji dataset independen dan eksperimen prospektif | FAKTA (via ringkasan AllSci) | AllSci |
| Konflik kepentingan: 6 penulis OpenAI, 2 PerturbAI, Zheng dan Jin pendiri PerturbAI | FAKTA | Blockchain.News / Tech Times ringkasan; TNW untuk peran Jin |
| Biaya komputasi/token | TIDAK DISEBUT / tidak ditemukan | R&D World search ("no token counts or cost") |
| Kritik ilmuwan independen | TIDAK ditemukan | pencarian 2026-11-07 |
| Peran Scripps secara rinci | TIDAK ditemukan jelas (Jin Lab, Scripps; repo "jinlabneurogenomics") | GitHub |
| AI "menemukan obat" / "AGI" | TIDAK DISEBUT. Jangan dipakai | - |

## Penjelasan awam (untuk naskah)
- Data: peneliti sebelumnya mematikan satu gen per kelompok sel otak tikus (CRISPR) lalu membaca aktivitas gen tiap sel (single-cell, Perturb-seq). Hasilnya tumpukan data raksasa.
- Kerja agent: tiap agent "kebagian" satu gen yang dimatikan, melihat apa yang berubah, membaca makalah ilmiah, lalu menulis laporan dan tebakan penjelasan. Laporan ribuan agent digabung.
- Hasil: daftar petunjuk (hipotesis) untuk dites ilmuwan, bukan jawaban.

## Konteks tren AI scientist (pembanding, singkat)
- Google DeepMind Co-Scientist dan FutureHouse Robin terbit di Nature, Mei 2026 (Robin 19 Mei 2026). Robin: 30 kandidat, 5 divalidasi eksperimen, 2 menjanjikan (ripasudil, KL001) untuk age-related macular degeneration; Co-Scientist menurut ringkasan butuh pakar manusia memilih kandidat. Sumber: Resultsense https://www.resultsense.com/news/2026-05-20-ai-scientists-nature-papers-limits/ , 20 Mei 2026; GEN https://www.genengnews.com/topics/artificial-intelligence/google-deepmind-and-edison-are-building-the-ai-scientist/ (sekunder, belum dibuka; cek makalah Nature). Beda: pembanding ini sudah ada validasi lab; riset OpenAI ini belum.
- Kosmos (Edison/FutureHouse), preprint arXiv, belum peer review: https://arxiv.org/html/2511.02824v2

## Sudut lokal Indonesia
- Tidak ditemukan sumber tentang dampak langsung ke Indonesia. Ketersediaan GPT-Rosalind: satu ringkasan menyebut terbatas (pelanggan korporasi AS); akses Indonesia dan harga rupiah TIDAK DISEBUT. Kode dan atlas terbuka (MIT, Hugging Face), jadi secara prinsip bisa dipelajari siapa saja, tapi menjalankan ulang butuh akses model/biaya (tidak disebut).
- OPINI (tandai sebagai analisis): pola "banyak agent dipecah per tugas" relevan untuk pekerja data/analis; pengecekan manusia tetap perlu.

## Angka aman untuk layar
- 21 Okt 2026 (diumumkan); 32 menit (waktu analisis); "hampir 2.000" agent (atau 1.946 dengan sumber R&D World); "jutaan sel otak tikus" (aman) atau "7,7 juta" (sumber Tech Times, ada versi 8 juta); 0 temuan tervalidasi di lab (dari "still awaiting validation", tulis "belum divalidasi lab").
- Hindari tanpa cek preprint: 52/55, 48/55, 94,5%, 75%, 45/60, 700 vs 11.
- Jangan pakai: "berbulan-bulan jadi 32 menit" sebagai fakta; harus "estimasi peneliti".

## Belum pasti / diperdebatkan
- 7,7 juta vs 8 juta sel; 1.946 vs "hampir 2.000" vs "thousands".
- 52/55 (94,5%) vs 48/55: kemungkinan beda definisi (sebagian pulih vs cocok/disempurnakan); cek preprint.
- Tanggal preprint 15 vs 16 Okt; satu outlet 1 Okt.
- Pembanding manual hanya estimasi dengan asumsi (15 menit per gen, 10 menit per paper); tidak ada uji waktu nyata.
- Evaluasi dilakukan penulis yang terkait perusahaan; pakar penilai dan kriterianya belum dicek; tidak ada konfirmasi independen.
- Risiko halusinasi agent/sitasi keliru: tidak ditemukan analisis spesifik; yang disebut hanya keterbatasan akurasi dan perlunya uji dataset independen.
- Peran manusia dalam pengecekan: pakar buta menilai laporan; detail tidak terbaca.
- Kritik independen: tidak ditemukan per 2026-11-07.
- Tinjau sendiri: apakah "Scripps" ikut menulis atau sebagai institusi afiliasi Jin Lab.

## Jangan dikatakan
- "AI menemukan obat/penyebab Parkinson/Alzheimer" (liputan Tom's Guide menyebut "Parkinson-like disease" dan media lain Alzheimer/Parkinson sebagai konteks; OpenAI memakai kata "leads/hypotheses").
- "AGI" atau "AI menggantikan ilmuwan".
- "Dalam 32 menit menyelesaikan riset setahun."
- Sel otak manusia.

## 3 usulan sudut hook
1. Hampir 2.000 AI agent membaca data jutaan sel otak tikus dalam 32 menit, tapi hasilnya baru petunjuk yang belum dites di lab.
2. 32 menit itu bukan menemukan obat: itu waktu AI membuat daftar tebakan untuk dicek ilmuwan.
3. Satu agent kebagian satu gen: begini cara ribuan AI memecah data otak raksasa (dan kenapa manusia tetap harus mengecek).

## Daftar sumber (tanggal)
- OpenAI, 21 Okt 2026: https://openai.com/index/scaling-ai-research-for-complex-biological-data/
- bioRxiv preprint, 15/16 Okt 2026: https://www.biorxiv.org/content/10.64898/2026.10.15.759436v1
- GitHub (dibuka): https://github.com/jinlabneurogenomics/distributed_agent
- R&D World, Okt 2026: https://www.rdworldonline.com/openai-deploys-nearly-2000-gpt-rosalind-agents-to-generate-biological-research-leads-in-32-minutes/
- TNW, Okt 2026: https://thenextweb.com/news/openai-ai-agents-mouse-brain-crispr-atlas
- TechRepublic: https://www.techrepublic.com/article/news-openai-ai-agents-brain-research/
- AllSci: https://allsci.com/news/research/ai-agents-brain-disease-openai-and-partners-use/
- Tech Times, 22 Okt 2026: https://www.techtimes.com/articles/329363/20261022/openai-drug-discovery-swarm-decoded-77-million-brain-cells-32-minutes.htm
- GIGAZINE, 22 Okt 2026: https://gigazine.net/gsc_news/en/20261022-openai-research-complex-biological-data/
- PR Newswire/Morningstar, 21 Okt 2026 (belum dibuka)
- GPT-Rosalind: https://openai.com/index/introducing-gpt-rosalind/ ; Axios 16 Apr 2026
- Pembanding: Resultsense 20 Mei 2026; GEN; arXiv Kosmos

## Tambahan 2026-11-07 (QC final, via web search; halaman tidak dibuka langsung)
| Klaim | Status | Sumber |
|---|---|---|
| OpenAI menyebut "thousands of AI agents powered by GPT-Rosalind" menganalisis data dari "millions of mouse brain cells" dalam 32 menit; metodenya disebut "distributed biological reasoning" | FAKTA (ringkasan hasil pencarian atas halaman resmi) | OpenAI, "Scaling AI research for complex biological data", https://openai.com/index/scaling-ai-research-for-complex-biological-data/ , 21 Okt 2026 |
| Preprint "Distributed AI agents enable comprehensive discovery of biological insights at scale" diunggah ke bioRxiv 16 Okt 2026, belum peer review | FAKTA | ringkasan pencarian (OpenAI + media) |
| Angka 1.946 agent hanya ada di satu blog; media lain menulis "nearly 2,000" | Tetap satu sumber, jadi **di layar dipakai "±2.000"** | unite.ai; cryptobriefing.com; aiweekly.co |
| TSC1 (hamartin) dan TSC2 (tuberin) membentuk satu kompleks protein (kompleks TSC) yang mengatur pertumbuhan sel lewat mTORC1. Ini mendukung VO "keduanya punya hubungan yang cukup erat" | FAKTA (pengetahuan biologi mapan) | NCBI Gene TSC2 (ID 7249), https://www.ncbi.nlm.nih.gov/gene/7249 ; NCBI Gene TSC1 (ID 7248), https://www.ncbi.nlm.nih.gov/gene/7248 |
