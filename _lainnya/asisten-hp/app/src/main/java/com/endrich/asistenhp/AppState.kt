package com.endrich.asistenhp

import android.content.Context
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow

enum class Who { USER, AI, SYS, ERR }

data class LogEntry(val who: Who, val text: String)

/** Saluran bersama antara service (suara + agen) dan layar aplikasi. */
object AppBus {
    val log = MutableSharedFlow<LogEntry>(replay = 200, extraBufferCapacity = 200)
    val status = MutableStateFlow("Belum aktif")
    val running = MutableStateFlow(false)
    val micOn = MutableStateFlow(true)
    val task = MutableStateFlow<String?>(null)

    fun log(who: Who, text: String) {
        log.tryEmit(LogEntry(who, text))
    }
}

/** Pengaturan disimpan di penyimpanan privat aplikasi (tidak bisa dibaca aplikasi lain). */
class Settings(context: Context) {
    private val prefs = context.getSharedPreferences("asisten", Context.MODE_PRIVATE)

    var apiKey: String
        get() = prefs.getString("api_key", "") ?: ""
        set(v) = prefs.edit().putString("api_key", v.trim()).apply()

    /** Model vision yang menyetir HP (Chat Completions). */
    var agentModel: String
        get() = prefs.getString("agent_model", DEFAULT_AGENT_MODEL) ?: DEFAULT_AGENT_MODEL
        set(v) = prefs.edit().putString("agent_model", v.trim().ifEmpty { DEFAULT_AGENT_MODEL }).apply()

    var realtimeModel: String
        get() = prefs.getString("realtime_model", DEFAULT_REALTIME_MODEL) ?: DEFAULT_REALTIME_MODEL
        set(v) = prefs.edit().putString("realtime_model", v.trim().ifEmpty { DEFAULT_REALTIME_MODEL }).apply()

    var voice: String
        get() = prefs.getString("voice", DEFAULT_VOICE) ?: DEFAULT_VOICE
        set(v) = prefs.edit().putString("voice", v.trim().ifEmpty { DEFAULT_VOICE }).apply()

    var maxSteps: Int
        get() = prefs.getInt("max_steps", DEFAULT_MAX_STEPS)
        set(v) = prefs.edit().putInt("max_steps", v.coerceIn(5, 100)).apply()

    companion object {
        const val DEFAULT_AGENT_MODEL = "gpt-4o"
        const val DEFAULT_REALTIME_MODEL = "gpt-realtime"
        const val DEFAULT_VOICE = "marin"
        const val DEFAULT_MAX_STEPS = 30
    }
}
