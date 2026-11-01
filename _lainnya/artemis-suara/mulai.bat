@echo off
REM Menjalankan jembatan suara ARTEMIS. Ubah ARTEMIS_DIR kalau folder ARTEMIS kamu di tempat lain.
set ARTEMIS_DIR=C:\artemis
cd /d "%~dp0"

if not exist ".env" (
  echo File .env belum ada. Salin contoh-env.txt menjadi .env lalu isi OPENAI_API_KEY.
  pause
  exit /b 1
)

REM Supaya Chrome di HP bisa membuka http://localhost:8765 (mikrofon hanya diizinkan di localhost/HTTPS)
adb reverse tcp:8765 tcp:8765 >nul 2>&1

uv run --project "%ARTEMIS_DIR%" python server.py
pause
