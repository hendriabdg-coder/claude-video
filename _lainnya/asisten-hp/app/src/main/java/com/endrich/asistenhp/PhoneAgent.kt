package com.endrich.asistenhp

import kotlinx.coroutines.delay
import kotlinx.coroutines.ensureActive
import org.json.JSONArray
import org.json.JSONObject
import kotlin.coroutines.coroutineContext

data class AgentResult(val success: Boolean, val summary: String, val steps: Int)

/**
 * Agen penyetir HP: setiap langkah mengambil screenshot + daftar elemen layar,
 * menanyakan langkah berikutnya ke model vision OpenAI, lalu menjalankannya.
 * Riwayat dikirim sebagai teks ringkas sehingga biaya per langkah tetap kecil.
 */
class PhoneAgent(
    private val settings: Settings,
    private val chat: OpenAiChat,
    private val ownPackage: String,
) {
    @Volatile
    var lastStep: String = ""
        private set

    suspend fun run(goal: String, onStep: (String) -> Unit): AgentResult {
        val svc = AgentAccessibilityService.instance
            ?: return AgentResult(false, "Layanan aksesibilitas Asisten HP belum aktif. Nyalakan di Pengaturan > Aksesibilitas.", 0)

        // Jangan mulai dari layar aplikasi ini sendiri.
        if (svc.currentPackage() == ownPackage) {
            svc.global("home")
            delay(700)
        }

        val history = mutableListOf<String>()
        val maxSteps = settings.maxSteps
        for (step in 1..maxSteps) {
            coroutineContext.ensureActive()

            val shot = svc.screenshot()
            val scale = shot?.scale ?: 1f
            val elements = svc.snapshotUi(scale)
            val body = buildRequest(goal, step, maxSteps, history, svc.currentPackage(), shot, elements)

            val response = chat.complete(body)
            val call = response.getJSONArray("choices").getJSONObject(0).getJSONObject("message")
                .optJSONArray("tool_calls")?.optJSONObject(0)?.getJSONObject("function")
            if (call == null) {
                history.add("$step. (model tidak memilih aksi)")
                continue
            }
            val name = call.getString("name")
            val args = runCatching { JSONObject(call.getString("arguments")) }.getOrDefault(JSONObject())
            val reason = args.optString("alasan")

            if (name == "finish") {
                val ok = args.optBoolean("success", false)
                val result = args.optString("result").ifBlank { if (ok) "Selesai." else "Gagal." }
                lastStep = "selesai"
                return AgentResult(ok, result, step)
            }

            val outcome = try {
                execute(svc, name, args, elements, scale)
            } catch (e: Exception) {
                "error: ${e.message}"
            }
            val line = "$step. $name(${describeArgs(args)}) -> $outcome" + if (reason.isNotBlank()) "  | $reason" else ""
            history.add(line)
            lastStep = line
            onStep(line)

            delay(if (name == "wait") 0 else 900) // beri waktu UI berubah
        }
        return AgentResult(false, "Batas $maxSteps langkah habis sebelum tugas selesai.", maxSteps)
    }

    private suspend fun execute(
        svc: AgentAccessibilityService,
        name: String,
        args: JSONObject,
        elements: List<UiElement>,
        scale: Float,
    ): String {
        fun element(): UiElement? {
            if (!args.has("index")) return null
            return elements.getOrNull(args.optInt("index", -1))
        }
        fun need(): UiElement = element() ?: throw IllegalArgumentException("index ${args.opt("index")} tidak ada di layar")

        return when (name) {
            "tap" -> ok(svc.click(need()))
            "long_press" -> ok(svc.longPress(need()))
            "tap_xy" -> ok(svc.tap(args.getDouble("x").toFloat() / scale, args.getDouble("y").toFloat() / scale))
            "type_text" -> {
                val target = element()
                if (target != null) svc.click(target)
                delay(300)
                val typed = svc.setText(target, args.getString("text"))
                if (typed && args.optBoolean("submit", false)) {
                    delay(300)
                    "ok, enter=" + ok(svc.pressEnter())
                } else {
                    ok(typed)
                }
            }
            "scroll" -> ok(svc.scroll(args.optString("direction", "down"), element()))
            "press" -> ok(svc.global(args.optString("key")))
            "open_app" -> svc.openApp(args.optString("name"))?.let { "membuka $it" }
                ?: "aplikasi '${args.optString("name")}' tidak ditemukan"
            "wait" -> {
                delay((args.optDouble("seconds", 2.0).coerceIn(0.5, 10.0) * 1000).toLong())
                "ok"
            }
            else -> "aksi tidak dikenal"
        }
    }

    private fun ok(b: Boolean) = if (b) "ok" else "gagal"

    private fun describeArgs(args: JSONObject): String =
        args.keys().asSequence().filter { it != "alasan" }.joinToString(", ") { k ->
            val v = args.opt(k).toString()
            "$k=${if (v.length > 40) v.take(40) + "…" else v}"
        }

    private fun buildRequest(
        goal: String,
        step: Int,
        maxSteps: Int,
        history: List<String>,
        pkg: String?,
        shot: Screenshot?,
        elements: List<UiElement>,
    ): JSONObject {
        val text = buildString {
            appendLine("TUJUAN: $goal")
            appendLine("Langkah $step dari maksimal $maxSteps.")
            appendLine("Aplikasi di depan: ${pkg ?: "tidak diketahui"}")
            appendLine()
            appendLine("RIWAYAT AKSI:")
            if (history.isEmpty()) appendLine("(belum ada)") else history.takeLast(15).forEach { appendLine(it) }
            appendLine()
            if (shot != null) {
                appendLine("Screenshot terlampir, ukuran ${shot.width}x${shot.height} px. Koordinat @(x,y) di bawah memakai skala yang sama.")
            } else {
                appendLine("Screenshot tidak tersedia (mungkin layar dilindungi aplikasi). Andalkan daftar elemen.")
            }
            appendLine("ELEMEN LAYAR:")
            if (elements.isEmpty()) appendLine("(tidak terbaca)") else elements.forEach { appendLine(it.description) }
        }
        val content = JSONArray().put(JSONObject().put("type", "text").put("text", text))
        if (shot != null) {
            content.put(
                JSONObject().put("type", "image_url").put(
                    "image_url",
                    JSONObject().put("url", "data:image/jpeg;base64,${shot.base64Jpeg}").put("detail", "high"),
                ),
            )
        }
        val messages = JSONArray()
            .put(JSONObject().put("role", "system").put("content", Prompts.agentSystem(ownPackage)))
            .put(JSONObject().put("role", "user").put("content", content))
        return JSONObject()
            .put("model", settings.agentModel)
            .put("messages", messages)
            .put("tools", Prompts.agentTools())
            .put("tool_choice", "required")
            .put("parallel_tool_calls", false)
    }
}
