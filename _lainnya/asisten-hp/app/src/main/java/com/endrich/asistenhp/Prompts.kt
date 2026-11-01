package com.endrich.asistenhp

import org.json.JSONArray
import org.json.JSONObject

object Prompts {

    // ------------------------------------------------------------------ asisten suara (Realtime)

    val VOICE_INSTRUCTIONS = """
        Kamu "Asisten HP", asisten suara pribadi yang berjalan di HP Android pengguna dan bisa mengoperasikan HP itu.
        Bicara Bahasa Indonesia santai, singkat, dan jelas. Pengguna bisa bicara atau mengetik; tanggapi keduanya sama.

        Cara kerja:
        - Kalau pengguna minta sesuatu dikerjakan di HP, panggil `jalankan_tugas`. Tulis tugasnya lengkap dan eksplisit:
          nama aplikasi, langkah penting, dan kapan dianggap selesai
          (mis. "Buka WhatsApp, buka chat Budi, baca 3 pesan terakhir lalu laporkan isinya").
        - Tugas di HP butuh waktu (beberapa detik per langkah). Setelah memanggil tool, bilang singkat bahwa sedang dikerjakan.
          Jangan mengarang hasil. Hasil datang lewat pesan "[NOTIFIKASI SISTEM]"; ringkas hasil itu untuk pengguna.
        - Hanya satu tugas berjalan pada satu waktu. Kalau pengguna mengganti perintah saat tugas berjalan, panggil
          `hentikan_tugas` dulu lalu `jalankan_tugas` dengan perintah baru. Pakai `cek_tugas` kalau pengguna menanyakan progres.
        - Pertanyaan biasa (bukan tugas di HP) jawab langsung tanpa tool.

        Keamanan (wajib):
        - Sebelum tindakan yang sulit dibatalkan atau berisiko, ulangi rinciannya dan minta konfirmasi "ya" dulu:
          mengirim pesan/email/komentar/posting, menelepon, transaksi/pembayaran/pembelian, menghapus data,
          mengubah pengaturan akun/keamanan, menginstal/menghapus aplikasi.
          Setelah pengguna setuju, tulis di tugas: "Pengguna SUDAH mengonfirmasi tindakan ini."
        - Jangan pernah meminta, mengetikkan, atau mengucapkan password, PIN, OTP, atau data kartu.
          Kalau tugas butuh itu, minta pengguna mengisinya sendiri.
    """.trimIndent()

    fun voiceTools(): JSONArray = JSONArray()
        .put(
            realtimeTool(
                "jalankan_tugas",
                "Menjalankan satu tugas di HP pengguna. Kembali segera; hasil datang belakangan sebagai notifikasi.",
                JSONObject()
                    .put("type", "object")
                    .put("properties", JSONObject().put("tugas", str("Deskripsi tugas lengkap dan eksplisit.")))
                    .put("required", JSONArray().put("tugas")),
            ),
        )
        .put(realtimeTool("cek_tugas", "Melihat status dan langkah terakhir tugas yang sedang berjalan.", emptyParams()))
        .put(realtimeTool("hentikan_tugas", "Menghentikan tugas yang sedang berjalan di HP.", emptyParams()))

    private fun realtimeTool(name: String, description: String, params: JSONObject) = JSONObject()
        .put("type", "function")
        .put("name", name)
        .put("description", description)
        .put("parameters", params)

    // ------------------------------------------------------------------ agen penyetir HP (Chat Completions)

    fun agentSystem(ownPackage: String) = """
        You are an Android phone-operating agent. Each turn you receive the user's goal, the history of your previous
        actions, the foreground app, a screenshot, and a numbered list of on-screen elements. Choose exactly ONE action
        by calling one tool. After each action you will see the new screen, so verify the effect before moving on.

        Rules:
        - Prefer `tap` with an element index. Use `tap_xy` only when the target is not in the element list
          (coordinates use the screenshot's pixel scale).
        - To launch an app use `open_app` instead of hunting for icons.
        - If the screen did not change after an action, try a different approach instead of repeating it.
        - Dismiss irrelevant popups (ads, rating prompts) when they block progress.
        - Never interact with the app with package "$ownPackage" (that is you, the assistant).
        - Never type passwords, PINs, OTP codes or card numbers, and never solve CAPTCHAs. If the goal needs them,
          call `finish` with success=false and explain that the user must do that part.
        - Do NOT perform irreversible actions (sending messages, posting, paying/buying, deleting, changing account or
          security settings, installing/uninstalling) unless the goal explicitly says the user has already confirmed it.
          Otherwise stop right before that final action and call `finish`, describing what is ready to be confirmed.
        - When the goal is achieved, or it is impossible, call `finish`. Put the information the user asked for
          (in Indonesian, concise) in `result`.
        - Always fill `alasan` with a very short reason (Indonesian).
    """.trimIndent()

    fun agentTools(): JSONArray = JSONArray()
        .put(chatTool("tap", "Tap an element by its index.", props("index" to int("Element index."))))
        .put(chatTool("long_press", "Long-press an element by its index.", props("index" to int("Element index."))))
        .put(
            chatTool(
                "tap_xy",
                "Tap at screenshot pixel coordinates.",
                props("x" to num("X in screenshot pixels."), "y" to num("Y in screenshot pixels.")),
            ),
        )
        .put(
            chatTool(
                "type_text",
                "Replace the text of an input field. If index is omitted the currently focused field is used.",
                props(
                    "text" to str("Text to type."),
                    "index" to int("Optional element index of the input field."),
                    "submit" to JSONObject().put("type", "boolean").put("description", "Press enter/search after typing."),
                ),
                required = listOf("text"),
            ),
        )
        .put(
            chatTool(
                "scroll",
                "Scroll content. 'down' reveals content below. Optional index of a scrollable element.",
                props("direction" to enumStr("up", "down", "left", "right"), "index" to int("Optional scrollable element index.")),
                required = listOf("direction"),
            ),
        )
        .put(
            chatTool(
                "press",
                "Press a system key.",
                props("key" to enumStr("back", "home", "recents", "notifications", "quick_settings", "enter")),
            ),
        )
        .put(chatTool("open_app", "Open an installed app by its name (e.g. 'YouTube', 'WhatsApp').", props("name" to str("App name."))))
        .put(chatTool("wait", "Wait for loading.", props("seconds" to num("Seconds to wait (0.5-10)."))))
        .put(
            chatTool(
                "finish",
                "End the task.",
                props(
                    "success" to JSONObject().put("type", "boolean"),
                    "result" to str("Answer / summary for the user, in Indonesian."),
                ),
            ),
        )

    private fun chatTool(name: String, description: String, properties: JSONObject, required: List<String>? = null): JSONObject {
        // Default: semua properti wajib; isi `required` kalau ada properti opsional.
        val req = JSONArray((required ?: properties.keys().asSequence().toList()) + "alasan")
        properties.put("alasan", str("Very short reason, Indonesian."))
        return JSONObject()
            .put("type", "function")
            .put(
                "function",
                JSONObject()
                    .put("name", name)
                    .put("description", description)
                    .put("parameters", JSONObject().put("type", "object").put("properties", properties).put("required", req)),
            )
    }

    private fun props(vararg pairs: Pair<String, JSONObject>): JSONObject {
        val o = JSONObject()
        pairs.forEach { (k, v) -> o.put(k, v) }
        return o
    }

    private fun str(desc: String) = JSONObject().put("type", "string").put("description", desc)
    private fun int(desc: String) = JSONObject().put("type", "integer").put("description", desc)
    private fun num(desc: String) = JSONObject().put("type", "number").put("description", desc)
    private fun enumStr(vararg values: String) = JSONObject().put("type", "string").put("enum", JSONArray(values.toList()))
    private fun emptyParams() = JSONObject().put("type", "object").put("properties", JSONObject())
}
