"""Jembatan suara + ketik untuk ARTEMIS (google/artemis) memakai OpenAI Realtime API.

Alur:
  Browser (HP/PC)  --WebRTC audio duplex-->  OpenAI Realtime (gpt-realtime)
        |  data channel: teks, transkrip, function call
        v
  server.py (ini, 127.0.0.1)  --HTTP-->  ARTEMIS daemon (localhost:8000)  --ADB-->  HP Android

server.py hanya:
  1. menyajikan halaman web (static/index.html);
  2. membuat kunci sementara (ephemeral) Realtime, sehingga API key OpenAI tidak pernah sampai ke browser;
  3. meneruskan panggilan tool dari model ke ARTEMIS (jalankan / cek / hentikan tugas);
  4. memantau tugas yang berjalan dan mengabari browser lewat SSE saat selesai.

Jalankan dengan environment ARTEMIS (sudah berisi fastapi, uvicorn, httpx, python-dotenv, artemis_client):
    uv run --project <folder-artemis> python server.py
"""

from __future__ import annotations

import asyncio
import json
import os
import uuid
from time import monotonic as loop_time
from pathlib import Path
from typing import Any

import httpx
import uvicorn
from artemis_client import ArtemisClient
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse

HERE = Path(__file__).resolve().parent
load_dotenv(HERE / ".env")

ARTEMIS_URL = os.environ.get("ARTEMIS_URL", "http://127.0.0.1:8000")
ARTEMIS_PROFILE = os.environ.get("ARTEMIS_PROFILE", "flash")
DEVICE_SERIAL = os.environ.get("DEVICE_SERIAL") or None
REALTIME_MODEL = os.environ.get("REALTIME_MODEL", "gpt-realtime")
REALTIME_VOICE = os.environ.get("REALTIME_VOICE", "marin")
TRANSCRIBE_MODEL = os.environ.get("TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe")
HOST = "127.0.0.1"  # sengaja hanya localhost: orang lain di Wi-Fi tidak bisa memakai kredit/HP kamu
PORT = int(os.environ.get("PORT", "8765"))
LAUNCH_TIMEOUT_S = float(os.environ.get("LAUNCH_TIMEOUT_S", "60"))

OPENAI_API = "https://api.openai.com/v1"

INSTRUCTIONS = """\
Kamu asisten suara pribadi yang bisa mengoperasikan HP Android pengguna lewat sistem ARTEMIS.
Bicara Bahasa Indonesia santai, singkat, dan jelas. Pengguna bisa bicara atau mengetik; tanggapi keduanya sama.

Cara kerja:
- Kalau pengguna minta sesuatu dikerjakan di HP, panggil `jalankan_tugas`. Tulis tugasnya lengkap dan eksplisit:
  nama aplikasi, langkah penting, dan kapan dianggap selesai (mis. "Buka WhatsApp, buka chat Budi, baca 3 pesan terakhir lalu laporkan isinya").
- Tugas di HP butuh waktu (beberapa detik per langkah). Setelah memanggil tool, bilang singkat bahwa sedang dikerjakan.
  Jangan mengarang hasil. Hasil datang lewat pesan "[NOTIFIKASI SISTEM]"; ringkas hasil itu untuk pengguna.
- Hanya satu tugas berjalan pada satu waktu. Kalau pengguna mengganti perintah saat tugas berjalan, panggil
  `hentikan_tugas` dulu lalu `jalankan_tugas` dengan perintah baru. Pakai `cek_tugas` kalau pengguna menanyakan progres.
- Mode "pro" hanya untuk tugas panjang/rumit yang butuh rencana dan verifikasi; selain itu biarkan default.
- Pertanyaan biasa (bukan tugas di HP) jawab langsung tanpa tool.

Keamanan (wajib):
- Sebelum tindakan yang sulit dibatalkan atau berisiko, ulangi rinciannya dan minta konfirmasi "ya" dulu:
  mengirim pesan/email/komentar/posting, menelepon, transaksi/pembayaran/pembelian, menghapus data,
  mengubah pengaturan akun/keamanan, menginstal/menghapus aplikasi.
- Jangan pernah meminta, mengetikkan, atau mengucapkan password, PIN, OTP, atau data kartu.
  Kalau tugas butuh itu, minta pengguna mengisinya sendiri langsung di HP.
"""

TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "name": "jalankan_tugas",
        "description": "Menjalankan satu tugas di HP Android pengguna lewat ARTEMIS. Kembali segera; hasil datang belakangan sebagai notifikasi.",
        "parameters": {
            "type": "object",
            "properties": {
                "tugas": {"type": "string", "description": "Deskripsi tugas lengkap dan eksplisit."},
                "mode": {
                    "type": "string",
                    "enum": ["flash", "pro"],
                    "description": "flash = cepat (default); pro = tugas panjang/rumit dengan rencana dan verifikasi.",
                },
            },
            "required": ["tugas"],
        },
    },
    {
        "type": "function",
        "name": "cek_tugas",
        "description": "Melihat status dan hasil sementara tugas yang sedang/terakhir berjalan.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "hentikan_tugas",
        "description": "Menghentikan tugas yang sedang berjalan di HP.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "daftar_perangkat",
        "description": "Melihat HP/emulator yang terhubung ke ARTEMIS.",
        "parameters": {"type": "object", "properties": {}},
    },
]

app = FastAPI(title="ARTEMIS Suara")
artemis = ArtemisClient(ARTEMIS_URL, device_serial=DEVICE_SERIAL, default_profile=ARTEMIS_PROFILE)

_state: dict[str, Any] = {"task_id": None, "goal": None}
_subscribers: set[asyncio.Queue] = set()


def _openai_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise HTTPException(500, "OPENAI_API_KEY belum diisi di file .env (lihat README).")
    return key


def _short(value: Any, limit: int = 1500) -> str:
    if value is None:
        return ""
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
    return text if len(text) <= limit else text[:limit] + " …(dipotong)"


async def _broadcast(event: dict[str, Any]) -> None:
    for queue in list(_subscribers):
        queue.put_nowait(event)


async def _watch(task_id: str, goal: str) -> None:
    """Pantau satu tugas sampai selesai lalu kabari semua browser."""
    last_status = None
    started = loop_time()
    while True:
        await asyncio.sleep(2.0)
        try:
            result = await artemis.get_task(task_id)
        except Exception as exc:  # daemon mati / jaringan putus
            if _state["task_id"] == task_id:
                _state["task_id"] = None
            await _broadcast({"type": "task_error", "task_id": task_id, "error": f"Gagal cek ARTEMIS: {exc}"})
            return
        # "launching" = ARTEMIS belum/tidak pernah memulai tugas ini (mis. HP lepas). Jangan menunggu selamanya.
        if result.status == "launching" and loop_time() - started > LAUNCH_TIMEOUT_S:
            if _state["task_id"] == task_id:
                _state["task_id"] = None
            await _broadcast(
                {
                    "type": "task_done",
                    "task_id": task_id,
                    "goal": goal,
                    "status": "failed",
                    "succeeded": False,
                    "output": "",
                    "error": "ARTEMIS tidak memulai tugas. Cek HP masih terhubung (adb devices) atau jalankan 'artemis doctor'.",
                }
            )
            return
        if result.status != last_status:
            last_status = result.status
            await _broadcast({"type": "task_status", "task_id": task_id, "status": result.status})
        if result.done:
            if _state["task_id"] == task_id:
                _state["task_id"] = None
            await _broadcast(
                {
                    "type": "task_done",
                    "task_id": task_id,
                    "goal": goal,
                    "status": result.status,
                    "succeeded": result.succeeded,
                    "output": _short(result.output),
                    "error": _short(result.error, 500),
                }
            )
            return


# ---------------------------------------------------------------- routes


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(HERE / "static" / "index.html")


@app.post("/session")
async def create_session() -> dict[str, Any]:
    """Buat client secret sementara untuk satu sesi Realtime (WebRTC)."""
    session = {
        "type": "realtime",
        "model": REALTIME_MODEL,
        "instructions": INSTRUCTIONS,
        "audio": {
            "input": {
                "transcription": {"model": TRANSCRIBE_MODEL, "language": "id"},
                "turn_detection": {"type": "server_vad", "silence_duration_ms": 600},
            },
            "output": {"voice": REALTIME_VOICE},
        },
        "tools": TOOLS,
        "tool_choice": "auto",
    }
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(
            f"{OPENAI_API}/realtime/client_secrets",
            headers={"Authorization": f"Bearer {_openai_key()}"},
            json={"session": session},
        )
    if resp.status_code >= 400:
        # Teruskan pesan error OpenAI (tidak berisi API key) supaya mudah didiagnosa.
        raise HTTPException(resp.status_code, f"OpenAI menolak membuat sesi: {resp.text[:500]}")
    data = resp.json()
    return {"client_secret": data.get("value"), "model": REALTIME_MODEL}


@app.post("/tool/{name}")
async def run_tool(name: str, request: Request) -> dict[str, Any]:
    try:
        args = await request.json()
    except Exception:
        args = {}
    if not isinstance(args, dict):
        args = {}
    try:
        return await _dispatch(name, args)
    except Exception as exc:
        return {"ok": False, "pesan": f"Gagal menghubungi ARTEMIS di {ARTEMIS_URL}: {exc}"}


async def _dispatch(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "jalankan_tugas":
        goal = str(args.get("tugas") or "").strip()
        if not goal:
            return {"ok": False, "pesan": "Deskripsi tugas kosong."}
        if _state["task_id"]:
            current = await artemis.get_task(_state["task_id"])
            if not current.done:
                return {
                    "ok": False,
                    "pesan": "Masih ada tugas berjalan. Hentikan dulu dengan hentikan_tugas.",
                    "tugas_berjalan": _state["goal"],
                }
        devices = [d for d in await artemis.list_devices() if d.state == "device"]
        if not devices:
            return {"ok": False, "pesan": "Tidak ada HP yang terhubung/terotorisasi ke ARTEMIS. Cek kabel/USB debugging."}
        mode = args.get("mode") if args.get("mode") in ("flash", "pro") else None
        task_id = str(uuid.uuid4())
        handle = await artemis.submit(goal, profile=mode, task_id=task_id)
        _state.update(task_id=handle.task_id, goal=goal)
        asyncio.create_task(_watch(handle.task_id, goal))
        return {"ok": True, "status": handle.status, "pesan": "Tugas diterima dan sedang dikerjakan di HP."}

    if name == "cek_tugas":
        if not _state["task_id"]:
            return {"ok": True, "pesan": "Tidak ada tugas yang sedang berjalan."}
        result = await artemis.get_task(_state["task_id"])
        return {
            "ok": True,
            "tugas": _state["goal"],
            "status": result.status,
            "langkah": result.turns,
            "hasil": _short(result.output),
            "error": _short(result.error, 500),
        }

    if name == "hentikan_tugas":
        if not _state["task_id"]:
            return {"ok": True, "pesan": "Tidak ada tugas yang sedang berjalan."}
        stopped = await artemis.stop(_state["task_id"])
        return {"ok": stopped, "pesan": "Tugas dihentikan." if stopped else "Permintaan stop dikirim, tunggu sebentar."}

    if name == "daftar_perangkat":
        devices = await artemis.list_devices()
        return {
            "ok": True,
            "perangkat": [
                {"serial": d.serial, "status": d.state, "model": d.model, "sibuk": d.busy} for d in devices
            ],
        }

    return {"ok": False, "pesan": f"Tool tidak dikenal: {name}"}


@app.get("/events")
async def events(request: Request) -> StreamingResponse:
    """Server-Sent Events: kabar status/selesainya tugas ke browser."""
    queue: asyncio.Queue = asyncio.Queue()
    _subscribers.add(queue)

    async def stream():
        try:
            yield "retry: 3000\n\n"
            while not await request.is_disconnected():
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=15)
                    yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
                except asyncio.TimeoutError:
                    yield ": ping\n\n"
        finally:
            _subscribers.discard(queue)

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.get("/health")
async def health() -> dict[str, Any]:
    info: dict[str, Any] = {"openai_key": bool(os.environ.get("OPENAI_API_KEY")), "artemis_url": ARTEMIS_URL}
    try:
        await artemis.health()
        info["artemis"] = "ok"
    except Exception as exc:
        info["artemis"] = f"tidak terhubung: {exc}"
    return info


if __name__ == "__main__":
    print(f"ARTEMIS Suara jalan di http://localhost:{PORT}  (ARTEMIS: {ARTEMIS_URL})")
    uvicorn.run(app, host=HOST, port=PORT, log_level="warning")
