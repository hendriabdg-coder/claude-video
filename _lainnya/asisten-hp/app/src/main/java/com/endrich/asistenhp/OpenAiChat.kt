package com.endrich.asistenhp

import kotlinx.coroutines.delay
import kotlinx.coroutines.suspendCancellableCoroutine
import okhttp3.Call
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import org.json.JSONObject
import java.io.IOException
import java.util.concurrent.TimeUnit
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException

class OpenAiException(val code: Int, message: String) : IOException(message)

/** Klien kecil untuk OpenAI Chat Completions (dipakai agen penyetir HP). */
class OpenAiChat(private val apiKey: () -> String) {

    val http: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(20, TimeUnit.SECONDS)
        .readTimeout(120, TimeUnit.SECONDS)
        .writeTimeout(60, TimeUnit.SECONDS)
        .pingInterval(20, TimeUnit.SECONDS) // juga menjaga WebSocket Realtime tetap hidup
        .build()

    /** Kirim body Chat Completions, coba ulang sekali untuk 429/5xx. */
    suspend fun complete(body: JSONObject): JSONObject {
        var lastError: Exception? = null
        repeat(3) { attempt ->
            try {
                return post("https://api.openai.com/v1/chat/completions", body)
            } catch (e: OpenAiException) {
                lastError = e
                if (e.code != 429 && e.code < 500) throw e
            } catch (e: IOException) {
                lastError = e
            }
            delay(1500L * (attempt + 1))
        }
        throw lastError ?: IOException("Gagal menghubungi OpenAI")
    }

    private suspend fun post(url: String, body: JSONObject): JSONObject {
        val request = Request.Builder()
            .url(url)
            .header("Authorization", "Bearer ${apiKey()}")
            .post(body.toString().toRequestBody(JSON))
            .build()
        val text = http.newCall(request).await().use { resp ->
            val raw = resp.body?.string().orEmpty()
            if (!resp.isSuccessful) {
                val msg = runCatching { JSONObject(raw).getJSONObject("error").getString("message") }
                    .getOrDefault(raw.take(300))
                throw OpenAiException(resp.code, "OpenAI ${resp.code}: $msg")
            }
            raw
        }
        return JSONObject(text)
    }

    companion object {
        private val JSON = "application/json".toMediaType()
    }
}

/** Jalankan Call OkHttp sebagai suspend function; dibatalkan kalau coroutine dibatalkan. */
suspend fun Call.await(): Response = suspendCancellableCoroutine { cont ->
    cont.invokeOnCancellation { runCatching { cancel() } }
    enqueue(object : Callback {
        override fun onFailure(call: Call, e: IOException) {
            if (cont.isActive) cont.resumeWithException(e)
        }

        override fun onResponse(call: Call, response: Response) {
            if (cont.isActive) cont.resume(response) else response.close()
        }
    })
}
