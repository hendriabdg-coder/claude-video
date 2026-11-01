package com.endrich.asistenhp

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.IBinder
import android.os.PowerManager
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch
import org.json.JSONObject

/**
 * Service latar depan (notifikasi tetap) yang memegang sesi suara dan agen.
 * Tetap hidup saat aplikasi lain sedang dibuka oleh agen.
 */
class AssistantService : Service(), ToolHandler {

    companion object {
        private const val CHANNEL = "asisten"
        private const val NOTIF_ID = 1
        private const val ACTION_STOP = "com.endrich.asistenhp.STOP"

        @Volatile
        var instance: AssistantService? = null
            private set

        fun start(context: Context) {
            context.startForegroundService(Intent(context, AssistantService::class.java))
        }

        fun stop(context: Context) {
            context.startService(Intent(context, AssistantService::class.java).setAction(ACTION_STOP))
        }
    }

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
    private lateinit var settings: Settings
    private lateinit var chat: OpenAiChat
    private lateinit var agent: PhoneAgent
    private var voice: RealtimeVoice? = null
    private var audio: AudioIO? = null
    private var agentJob: Job? = null
    private var currentGoal: String? = null
    private var wakeLock: PowerManager.WakeLock? = null

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        settings = Settings(this)
        chat = OpenAiChat { settings.apiKey }
        agent = PhoneAgent(settings, chat, packageName)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (intent?.action == ACTION_STOP) {
            stopSelf()
            return START_NOT_STICKY
        }
        if (voice != null) return START_NOT_STICKY // sudah berjalan

        startForeground(NOTIF_ID, buildNotification("Mendengarkan…"), ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE)
        instance = this
        AppBus.running.value = true

        val pm = getSystemService(Context.POWER_SERVICE) as PowerManager
        wakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "AsistenHP:sesi").apply {
            setReferenceCounted(false)
            acquire(2 * 60 * 60 * 1000L) // pengaman: maksimal 2 jam
        }

        val io = AudioIO(this).also { it.micEnabled = AppBus.micOn.value }
        audio = io
        voice = RealtimeVoice(chat.http, VoiceConfig(settings.apiKey, settings.realtimeModel, settings.voice), io, this)
            .also { it.start() }
        return START_NOT_STICKY
    }

    override fun onDestroy() {
        agentJob?.cancel()
        voice?.stop()
        voice = null
        audio = null
        scope.cancel()
        wakeLock?.let { if (it.isHeld) it.release() }
        instance = null
        AppBus.running.value = false
        AppBus.task.value = null
        AppBus.status.value = "Belum aktif"
        super.onDestroy()
    }

    // ------------------------------------------------------------------ dipanggil dari layar

    fun sendText(text: String) {
        voice?.sendText(text)
    }

    fun setMic(on: Boolean) {
        voice?.setMic(on)
    }

    fun stopTask(): Boolean {
        val job = agentJob ?: return false
        if (!job.isActive) return false
        job.cancel()
        return true
    }

    // ------------------------------------------------------------------ tool dari model suara

    override suspend fun call(name: String, args: JSONObject): JSONObject = when (name) {
        "jalankan_tugas" -> startTask(args.optString("tugas").trim())
        "cek_tugas" -> {
            if (agentJob?.isActive == true) {
                JSONObject().put("ok", true).put("tugas", currentGoal).put("langkah_terakhir", agent.lastStep)
            } else {
                JSONObject().put("ok", true).put("pesan", "Tidak ada tugas yang sedang berjalan.")
            }
        }
        "hentikan_tugas" -> JSONObject().put("ok", true)
            .put("pesan", if (stopTask()) "Tugas dihentikan." else "Tidak ada tugas yang sedang berjalan.")
        else -> JSONObject().put("ok", false).put("pesan", "Tool tidak dikenal: $name")
    }

    private fun startTask(goal: String): JSONObject {
        if (goal.isEmpty()) return JSONObject().put("ok", false).put("pesan", "Deskripsi tugas kosong.")
        if (agentJob?.isActive == true) {
            return JSONObject().put("ok", false)
                .put("pesan", "Masih ada tugas berjalan. Hentikan dulu dengan hentikan_tugas.")
                .put("tugas_berjalan", currentGoal)
        }
        if (AgentAccessibilityService.instance == null) {
            return JSONObject().put("ok", false)
                .put("pesan", "Layanan aksesibilitas Asisten HP belum aktif. Minta pengguna menyalakannya di Pengaturan > Aksesibilitas.")
        }

        currentGoal = goal
        AppBus.task.value = goal
        updateNotification("Mengerjakan: $goal")
        agentJob = scope.launch {
            val result = try {
                agent.run(goal) { step -> AppBus.log(Who.SYS, step) }
            } catch (e: CancellationException) {
                AgentResult(false, "Tugas dihentikan pengguna.", 0)
            } catch (e: Exception) {
                AgentResult(false, "Error: ${e.message}", 0)
            }
            AppBus.log(if (result.success) Who.SYS else Who.ERR, "${if (result.success) "✅" else "⚠️"} ${result.summary}")
            AppBus.task.value = null
            updateNotification("Mendengarkan…")
            voice?.notify(
                "[NOTIFIKASI SISTEM] Tugas di HP ${if (result.success) "selesai" else "tidak berhasil"}.\n" +
                    "Tugas: $goal\nLangkah: ${result.steps}\nHasil: ${result.summary}\n" +
                    "Sampaikan hasilnya ke pengguna secara singkat.",
            )
        }
        return JSONObject().put("ok", true).put("pesan", "Tugas diterima dan sedang dikerjakan di HP.")
    }

    // ------------------------------------------------------------------ notifikasi

    private fun buildNotification(text: String): Notification {
        val nm = (getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager)
        if (nm.getNotificationChannel(CHANNEL) == null) {
            nm.createNotificationChannel(NotificationChannel(CHANNEL, "Asisten HP", NotificationManager.IMPORTANCE_LOW))
        }
        val open = PendingIntent.getActivity(
            this, 0, Intent(this, MainActivity::class.java), PendingIntent.FLAG_IMMUTABLE,
        )
        val stop = PendingIntent.getService(
            this, 1, Intent(this, AssistantService::class.java).setAction(ACTION_STOP), PendingIntent.FLAG_IMMUTABLE,
        )
        return Notification.Builder(this, CHANNEL)
            .setSmallIcon(android.R.drawable.ic_btn_speak_now)
            .setContentTitle("Asisten HP aktif")
            .setContentText(text)
            .setContentIntent(open)
            .setOngoing(true)
            .addAction(Notification.Action.Builder(null, "Matikan", stop).build())
            .build()
    }

    private fun updateNotification(text: String) {
        (getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager).notify(NOTIF_ID, buildNotification(text))
    }
}
