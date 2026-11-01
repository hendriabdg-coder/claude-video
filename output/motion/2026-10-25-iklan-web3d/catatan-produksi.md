# Catatan produksi: iklan-web3d (2026-10-25)

- Jenis: iklan jasa website 3D (bukan reel edukasi/seri), gaya 08 SHOWCASE, 25 detik, 1080x1920/30fps.
- Naskah: Skrip 1 hard selling pilihan Endrich, CTA "DM aku, ketik 3D. Kita bahas website kamu hari ini." Tidak ada riset.md karena tidak ada klaim fakta eksternal.
- Gate: naskah dipilih Endrich (gate 2), VO disetujui Endrich (gate 3).
- VO: 20,6 detik, mulai di 0,3 detik. Pelafalan baru: DM → di-em (tools/pelafalan.json).
- Visual: rekaman layar 3 situs demo dipotong ke area monitor (prep_clips.py) dan diputar dalam kartu browser; mockup "brosur" diberi label SIMULASI; kartu demo diberi label DEMO KARYA.
- Audio: Eleven Music 25 detik (-7.5 dB + ducking), 22 SFX Epidemic, -14,2 LUFS, peak -1,1 dBFS.
- Review naskah (reviewer-konten): 0 BLOKIR, 4 PERBAIKI (durasi, lisensi model 3D, label SIMULASI, safe area), semua ditangani kecuali lisensi model 3D yang perlu dikonfirmasi Endrich.
- QC final (reviewer-konten): 1 BLOKIR (asal aset 3D vs klaim "aku yang bikin", menunggu konfirmasi Endrich), 2 PERBAIKI (chip "pengunjung cepat pergi" tertutup chibi, chip "pembeli" mepet chibi) sudah diperbaiki dan dirender ulang; waktu ganti URL disamakan dengan potongan klip.
- Perlu dicek Endrich: asal model/foto 3D di ketiga situs (VO bilang "aku yang bikin"); CTA 17-25 dtk cukup statis (hanya pil berdenyut + chibi melambai).
- Sumber kerja: videos/iklan-web3d/ (build.py, prep_clips.py, audio.py, cover.py).
