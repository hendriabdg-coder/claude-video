package com.endrich.asistenhp

import android.util.Base64
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import org.json.JSONArray
import org.json.JSONObject

/** Konfigurasi sesi suara (diambil dari [Settings] saat sesi dimulai). */
data class VoiceConfig(val apiKey: String, val model: String, val voice: String)

/** Dipanggil saat model suara memanggil tool. */
fun interface ToolHandler {
    suspend fun call(name: String, args: JSONObject): JSONObject
}

/**
 * Sesi OpenAI Realtime (suara dua arah + teks) lewat WebSocket.
 * Semua event diproses berurutan di satu "jalur" coroutine supaya status
 * (response aktif, tool berjalan, antrean) tidak balapan.
 */
@OptIn(ExperimentalCoroutinesApi::class)
class RealtimeVoice(
    private val http: OkHttpClient,
    private val config: VoiceConfig,
    private val audio: VoiceAudio,
    private val tools: ToolHandler,
) {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default.limitedParallelism(1))
    private var ws: WebSocket? = null

    private var connected = false
    private var responseActive = false // model sedang menjawab
    private var toolsRunning = false // menunggu hasil tool
    private var wantResponse = false // ada input yang menunggu dijawab
    private val pendingNotices = mutableListOf<String>()
    private val handledCalls = HashSet<String>()

    fun start(baseUrl: String = "wss://api.openai.com/v1/realtime") {
        val request = Request.Builder()
            .url("$baseUrl?model=${config.model}")
            .header("Authorization", "Bearer ${config.apiKey}")
            .build()
        AppBus.status.value = "Menghubungkan…"
        ws = http.newWebSocket(request, Listener())
    }

    fun stop() {
        audio.stop()
        ws?.close(1000, "selesai")
        ws = null
        scope.cancel()
        AppBus.status.value = "Belum aktif"
    }

    fun setMic(on: Boolean) {
        audio.micEnabled = on
    }

    fun sendText(text: String) = scope.launch {
        if (!connected) {
            AppBus.log(Who.ERR, "Belum tersambung.")
            return@launch
        }
        if (responseActive) {
            send(JSONObject().put("type", "response.cancel")) // ketikan baru memotong jawaban AI
            audio.flushPlayback()
        }
        send(userMessage(text))
        requestResponse()
    }

    /** Kabar dari agen (tugas selesai) yang harus disampaikan ke pengguna. */
    fun notify(text: String) = scope.launch {
        pendingNotices.add(text)
        flushNotices()
    }

    // ------------------------------------------------------------------ alur response

    private fun requestResponse() {
        if (responseActive || toolsRunning) {
            wantResponse = true
            return
        }
        wantResponse = false
        responseActive = true
        send(JSONObject().put("type", "response.create"))
    }

    private fun afterIdle() {
        if (responseActive || toolsRunning) return
        flushNotices()
        if (wantResponse) requestResponse()
    }

    private fun flushNotices() {
        if (!connected || responseActive || toolsRunning || pendingNotices.isEmpty()) return
        val text = pendingNotices.joinToString("\n\n")
        pendingNotices.clear()
        send(userMessage(text))
        requestResponse()
    }

    private suspend fun handleFunctionCalls(response: JSONObject?) {
        val output = response?.optJSONArray("output") ?: return
        val calls = (0 until output.length()).map { output.getJSONObject(it) }
            .filter { it.optString("type") == "function_call" && handledCalls.add(it.optString("call_id")) }
        if (calls.isEmpty()) return

        toolsRunning = true
        for (call in calls) {
            val name = call.optString("name")
            val args = runCatching { JSONObject(call.optString("arguments", "{}")) }.getOrDefault(JSONObject())
            AppBus.log(Who.SYS, "⚙️ $name" + (args.optString("tugas").takeIf { it.isNotBlank() }?.let { ": $it" } ?: ""))
            val result = try {
                tools.call(name, args)
            } catch (e: Exception) {
                JSONObject().put("ok", false).put("pesan", "Error: ${e.message}")
            }
            send(
                JSONObject().put("type", "conversation.item.create").put(
                    "item",
                    JSONObject()
                        .put("type", "function_call_output")
                        .put("call_id", call.optString("call_id"))
                        .put("output", result.toString()),
                ),
            )
        }
        toolsRunning = false
        requestResponse()
    }

    // ------------------------------------------------------------------ event server

    private suspend fun onEvent(ev: JSONObject) {
        when (ev.optString("type")) {
            "session.created" -> send(sessionUpdate())
            "session.updated" -> {
                if (!connected) {
                    connected = true
                    AppBus.status.value = "Tersambung — silakan bicara atau ketik"
                    AppBus.log(Who.SYS, "Tersambung. Bicara langsung (boleh memotong AI) atau ketik.")
                    audio.start { pcm -> appendAudio(pcm) }
                }
            }
            "input_audio_buffer.speech_started" -> {
                audio.flushPlayback() // pengguna memotong: diamkan AI seketika
                AppBus.status.value = "Mendengarkan…"
            }
            "conversation.item.input_audio_transcription.completed" -> {
                val t = ev.optString("transcript").trim()
                if (t.isNotEmpty()) AppBus.log(Who.USER, "🎤 $t")
            }
            "response.created" -> {
                responseActive = true
                AppBus.status.value = "AI menjawab…"
            }
            "response.output_audio.delta", "response.audio.delta" -> {
                val b64 = ev.optString("delta")
                if (b64.isNotEmpty()) audio.play(Base64.decode(b64, Base64.DEFAULT))
            }
            "response.output_audio_transcript.done", "response.audio_transcript.done" -> {
                val t = ev.optString("transcript").trim()
                if (t.isNotEmpty()) AppBus.log(Who.AI, t)
            }
            "response.output_text.done", "response.text.done" -> {
                val t = ev.optString("text").trim()
                if (t.isNotEmpty()) AppBus.log(Who.AI, t)
            }
            "response.done" -> {
                responseActive = false
                AppBus.status.value = "Tersambung"
                handleFunctionCalls(ev.optJSONObject("response"))
                afterIdle()
            }
            "error" -> {
                val err = ev.optJSONObject("error")
                AppBus.log(Who.ERR, "Error: ${err?.optString("message") ?: ev}")
                if (err?.optString("code") != "conversation_already_has_active_response") {
                    responseActive = false
                    afterIdle()
                }
            }
        }
    }

    private fun appendAudio(pcm: ByteArray) {
        // Dipanggil dari thread mikrofon; WebSocket.send aman dipanggil dari thread mana pun.
        ws?.send(
            JSONObject()
                .put("type", "input_audio_buffer.append")
                .put("audio", Base64.encodeToString(pcm, Base64.NO_WRAP))
                .toString(),
        )
    }

    private fun send(obj: JSONObject) {
        ws?.send(obj.toString())
    }

    private fun userMessage(text: String) = JSONObject()
        .put("type", "conversation.item.create")
        .put(
            "item",
            JSONObject()
                .put("type", "message")
                .put("role", "user")
                .put("content", JSONArray().put(JSONObject().put("type", "input_text").put("text", text))),
        )

    private fun sessionUpdate(): JSONObject {
        val pcm = JSONObject().put("type", "audio/pcm").put("rate", AudioIO.RATE)
        val session = JSONObject()
            .put("type", "realtime")
            .put("instructions", Prompts.VOICE_INSTRUCTIONS)
            .put("output_modalities", JSONArray().put("audio"))
            .put(
                "audio",
                JSONObject()
                    .put(
                        "input",
                        JSONObject()
                            .put("format", pcm)
                            .put("transcription", JSONObject().put("model", "gpt-4o-mini-transcribe").put("language", "id"))
                            .put("turn_detection", JSONObject().put("type", "server_vad").put("silence_duration_ms", 600)),
                    )
                    .put("output", JSONObject().put("format", JSONObject(pcm.toString())).put("voice", config.voice)),
            )
            .put("tools", Prompts.voiceTools())
            .put("tool_choice", "auto")
        return JSONObject().put("type", "session.update").put("session", session)
    }

    private inner class Listener : WebSocketListener() {
        override fun onMessage(webSocket: WebSocket, text: String) {
            val ev = runCatching { JSONObject(text) }.getOrNull() ?: return
            scope.launch { onEvent(ev) }
        }

        override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
            scope.launch {
                connected = false
                val detail = response?.let { " (HTTP ${it.code})" } ?: ""
                AppBus.log(Who.ERR, "Koneksi suara putus: ${t.message}$detail")
                AppBus.status.value = "Terputus"
                audio.stop()
            }
        }

        override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
            scope.launch {
                connected = false
                AppBus.status.value = "Terputus"
            }
        }
    }
}
