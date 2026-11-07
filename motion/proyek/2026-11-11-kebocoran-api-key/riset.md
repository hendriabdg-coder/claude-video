# Lembar Riset (Cek Fakta VO): Kebocoran API Key (tayang 2026-11-11)

Tanggal riset: 2026-11-07. Peneliti: peneliti-konten. Tugas: verifikasi klaim VO yang sudah jadi, bukan menulis naskah.

## Status akses sumber (PENTING)
- WebFetch GAGAL untuk blog.gitguardian.com, help.openai.com, docs.github.com (host tidak resolve; di luar domain yang diizinkan sesi ini). Semua isi di bawah berasal dari RINGKASAN hasil pencarian web. Kalimat dalam kutipan di bawah adalah kutipan/parafrase dari ringkasan pencarian, BELUM dicocokkan kata per kata dengan halaman asli. Buka halaman primer di browser sebelum jadi teks layar.
- Halaman primer yang muncul di hasil (belum dibuka): GitGuardian https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/ ; OpenAI https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety ; GitHub https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

## Verdict klaim VO
| Klaim VO | Verdict |
|---|---|
| "sekitar 28,6 juta secret baru ... commit GitHub publik sepanjang 2025" | BENAR. Angka persis 28,65 juta; "sekitar 28,6 juta" kurang pas pembulatan (28,65 dibulatkan jadi 28,7 atau "sekitar 29 juta"). Aman: "sekitar 29 juta" / "28,65 juta". |
| "laporan GitGuardian tahun 2026" | BENAR sebagai nama laporan (rilis 17 Mar 2026), tapi datanya tahun 2025. VO sudah menyebut "sepanjang tahun 2025", jadi OK. |
| Secret tetap ada walau dihapus dari kode terbaru | BENAR (riwayat git/fork/clone). |
| Key di front-end bisa terbaca lewat browser | BENAR (OpenAI melarang di client-side). |
| "Yang ketiga": bocor lewat screenshot, log error, atau minta bantuan AI coding | SEBAGIAN. Bagian AI coding punya data GitGuardian. Screenshot dan log: TIDAK ditemukan data di GitGuardian. Jangan sebut "sering banget nggak disadari" sebagai fakta; itu opini. |
| Dampak: penyalahgunaan, saldo habis, akses data tergantung izin | BENAR (OpenAI: "unexpected charges or compromised account data"), "tergantung izin" TERSIRAT. |
| Rekomendasi: back-end, batasi akses, jangan bagikan | BENAR, plus rotasi key dan batas pengeluaran (belum ada di VO). |
| "pernah ikut terkirim" ke AI | AMAN sebagai ajakan cek; jangan dibaca sebagai "pasti terkirim ke AI". |

## Ringkasan fakta
1. GitGuardian State of Secrets Sprawl 2026 (edisi kelima) dirilis 17 Mar 2026: 28,65 juta secret hardcoded baru di commit GitHub publik sepanjang 2025, naik 34% dari tahun sebelumnya.
2. Commit publik sekitar 1,94 miliar (naik 43%).
3. Kebocoran terkait layanan AI naik 81% (81,5% di satu sumber).
4. Commit yang ditulis bersama Claude Code: tingkat bocor secret 3,2% vs baseline 1,5% (sekitar 2x). Ini hanya untuk Claude Code, bukan semua asisten AI.
5. GitHub docs: menulis ulang riwayat tidak menghapus data sepenuhnya; langkah pertama untuk secret adalah cabut/rotasi.
6. OpenAI: jangan taruh key di lingkungan client-side (browser/mobile app); arahkan lewat backend sendiri.
7. OpenAI: key yang terekspos bisa dipakai pihak lain dan menyebabkan tagihan tak terduga atau data akun terbuka.
8. Sudut lokal Indonesia: TIDAK ditemukan data kebocoran khusus Indonesia dan harga rupiah.

## Tabel klaim | status | sumber
| Klaim | Status | Sumber |
|---|---|---|
| "28.65 million new hardcoded secrets were added to public GitHub commits in 2025 alone, a 34% increase" (kalimat dari ringkasan pencarian, belum dicek kata per kata) | FAKTA (via ringkasan) | GitGuardian, "The State of Secrets Sprawl 2026", https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/ , 17 Mar 2026 |
| Media membulatkan ke "29 juta" | FAKTA (beda pembulatan, bukan konflik) | CPO Magazine https://www.cpomagazine.com/?p=41171 ; DEV Community (GitGuardian) https://dev.to/gitguardian/the-state-of-secrets-sprawl-2026-ai-service-leaks-surge-81-and-29m-secrets-hit-public-github-2bgj ; Mar 2026 |
| Tanggal rilis 17 Mar 2026 | FAKTA (via ringkasan) | The Hacker News https://thehackernews.com/2026/03/the-state-of-secrets-sprawl-2026-9.html ; SC World https://www.scworld.com/news/ai-coding-assistants-twice-as-likely-to-leak-secrets-as-overall-leaks-rise-34 |
| Commit publik ~1,94 miliar, +43% | FAKTA (via ringkasan) | ringkasan pencarian atas laporan GitGuardian, Mar 2026 |
| Kebocoran layanan AI +81% | FAKTA (via ringkasan) | CPO Magazine (judul "81% Surge of AI-Service Leaks"), Mar 2026 |
| Claude Code co-authored commits: 3,2% vs 1,5% baseline; puncak Agustus ~2,4x; Desember turun ke 13 per 1.000 commit, mendekati baseline | FAKTA (via ringkasan; angka baseline 1,6% di satu outlet) | SecurityBrief https://securitybrief.co.uk/story/ai-surge-drives-record-secrets-sprawl-across-github ; SC World (link di atas), Mar 2026 |
| GitGuardian sendiri: selisih jangan dibaca sebagai kegagalan alat semata | FAKTA (parafrase ringkasan) | ringkasan pencarian |
| Laporan menyebut "AI coding assistant" secara umum (semua alat) dengan angka | TIDAK DISEBUT jelas di ringkasan; yang terlihat hanya Claude Code. Judul SC World: "AI coding assistants twice as likely to leak secrets" (judul media, bukan angka per alat) | SC World |
| Secret di config MCP: 24.008 unik, 2.117 terverifikasi valid | FAKTA (via ringkasan) | ringkasan pencarian |
| ~28% insiden berasal dari alat kolaborasi/produktivitas (bukan repo) | FAKTA (via ringkasan press release); tidak ada rincian Slack/Jira/log | ringkasan pencarian |
| Screenshot atau log error sebagai jalur bocor menurut GitGuardian | TIDAK DITEMUKAN | - |
| Prompt ke asisten AI mengirim key ke penyedia AI | TIDAK DITEMUKAN sumber di riset ini | - |
| 64% secret valid dari 2022 belum dicabut di 2026 | FAKTA (via ringkasan) | ringkasan pencarian |
| Menulis ulang riwayat tidak menghapus semua salinan: tidak bisa hapus dari clone orang lain; "If the commit that introduced the sensitive data exists in any forks, it will continue to be accessible there"; cached views dan referensi PR bisa tetap ada (parafrase ringkasan) | FAKTA (via ringkasan) | GitHub Docs, "Removing sensitive data from a repository", https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository , tanpa tanggal terbaca |
| Docs GitHub: untuk secret, langkah pertama "revoke and/or rotate" | FAKTA (via ringkasan) | GitHub Docs (sama) |
| Klaim VO "orang lain bisa menemukannya" setelah dihapus dari kode terbaru | TERSIRAT dari docs (data bisa tetap di fork/clone/cache); docs tidak menulis "pasti ditemukan siapa saja" | GitHub Docs |
| "Never deploy your key in client-side environments like browsers or mobile apps." | FAKTA (via ringkasan) | OpenAI Help, "Best practices for API key safety", https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety , tanggal tidak terbaca |
| Kunci dari front-end bisa "dibaca lewat browser" (DevTools) | TERSIRAT (OpenAI melarang karena bisa dipakai ulang; kata "DevTools" tidak ditemukan) | OpenAI Help (sama) |
| "Exposing the key in browsers or mobile apps lets bad actors reuse it, which may lead to surprise charges or compromised account data." | FAKTA (parafrase ringkasan) | OpenAI Help (sama) |
| Terekspos: "unauthorized API usage through your account, which can result in charges or activity that violates our terms of service"; OpenAI menonaktifkan key yang terdeteksi di internet publik | FAKTA (via ringkasan) | OpenAI Help, "How to secure your OpenAI account if you suspect unauthorized access", https://help.openai.com/en/articles/8304786-how-to-secure-your-openai-account-if-you-suspect-unauthorized-access |
| Akses data "tergantung izin key" | TERSIRAT (OpenAI hanya menyebut "compromised account data"); prinsip least privilege dari GitGuardian remediation, https://www.gitguardian.com/remediation/openai-api-key. Fitur key terbatas OpenAI: tidak terkonfirmasi | - |
| Rekomendasi: lewat backend sendiri; jangan commit key; env variable/key management; expiry dan rotasi rutin; batas pengeluaran bulanan (alert saja tidak memblokir); IP allowlist; satu key per fitur/proyek | FAKTA (via ringkasan) | OpenAI Help (best practices, di atas) |
| Penyedia lain (Anthropic, Google, dll.) sama | TIDAK DISEBUT (hanya OpenAI dicek) | - |

## Angka aman untuk layar
- "28,65 juta secret baru di GitHub publik, 2025" (atau "sekitar 29 juta"); sumber GitGuardian, Mar 2026.
- "+34% dibanding tahun sebelumnya".
- "Commit bantuan Claude Code: 3,2% bocor vs 1,5% rata-rata" HANYA kalau jelas ditulis Claude Code, bukan "AI coding".
- Hindari: "screenshot/log paling sering" (tidak ada data); "semua AI 2x lebih bocor".

## Belum pasti / diperdebatkan
- 28,65 juta vs "29 juta": beda pembulatan, bukan konflik. VO "28,6" tidak tepat bulat.
- Baseline 1,5% vs 1,6% antar outlet.
- GitGuardian menghitung secret hardcoded di commit publik (termasuk yang belum tentu valid/aktif); angka 28,65 juta bukan "key yang disalahgunakan".
- Semua teks kutipan belum dicek langsung ke halaman primer.
- Konteks lokal Indonesia, harga rupiah, kasus tagihan nyata: tidak ditemukan.

## Saran koreksi VO (untuk Endrich putuskan)
1. "sekitar 28,6 juta" -> "sekitar 29 juta" atau "28,65 juta".
2. Kalimat "yang ketiga sering banget nggak disadari" dan jalur screenshot/log: tandai sebagai opini/peringatan umum, bukan temuan GitGuardian. Data GitGuardian relevan hanya soal AI coding (Claude Code 3,2% vs 1,5%).
3. Tambahkan "rotasi/ganti key" bila VO masih bisa direvisi; ini langkah pertama versi GitHub docs.
4. "orang lain bisa menemukannya" aman; jangan ditulis "pasti".

## 3 usulan sudut hook
1. Dalam setahun, sekitar 29 juta secret baru nongol di GitHub publik, dan sebagian bisa jadi API key seperti punyamu.
2. Menghapus API key dari kode belum tentu menghapusnya dari riwayat; cabut dan ganti dulu.
3. Satu aturan dari OpenAI: jangan taruh API key di browser atau aplikasi, lewatkan lewat backend.
