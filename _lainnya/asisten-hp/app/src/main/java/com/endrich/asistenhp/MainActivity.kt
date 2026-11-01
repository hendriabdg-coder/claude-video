package com.endrich.asistenhp

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.provider.Settings as AndroidSettings
import android.text.InputType
import android.view.Gravity
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import kotlinx.coroutines.MainScope
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch

/** Layar utama: tombol mulai, mic, kolom ketik, transkrip, dan pengaturan. */
class MainActivity : Activity() {

    private val ui = MainScope()
    private lateinit var settings: Settings

    private lateinit var statusText: TextView
    private lateinit var a11yButton: Button
    private lateinit var startButton: Button
    private lateinit var micButton: Button
    private lateinit var taskText: TextView
    private lateinit var logBox: LinearLayout
    private lateinit var logScroll: ScrollView
    private lateinit var input: EditText
    private lateinit var settingsPanel: LinearLayout

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        settings = Settings(this)
        setContentView(buildUi())
        observe()
        if (settings.apiKey.isBlank()) settingsPanel.visibility = View.VISIBLE
    }

    override fun onResume() {
        super.onResume()
        refreshA11y()
    }

    override fun onDestroy() {
        ui.cancel()
        super.onDestroy()
    }

    // ------------------------------------------------------------------ aksi

    private fun toggleSession() {
        if (AppBus.running.value) {
            AssistantService.stop(this)
            return
        }
        if (settings.apiKey.isBlank()) {
            toast("Isi API key OpenAI dulu di Pengaturan.")
            settingsPanel.visibility = View.VISIBLE
            return
        }
        val missing = buildList {
            if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                add(Manifest.permission.RECORD_AUDIO)
            }
            if (android.os.Build.VERSION.SDK_INT >= 33 &&
                checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
            ) {
                add(Manifest.permission.POST_NOTIFICATIONS)
            }
        }
        if (missing.isNotEmpty()) {
            requestPermissions(missing.toTypedArray(), REQ_PERMS)
            return
        }
        if (AgentAccessibilityService.instance == null) {
            toast("Ngobrol bisa, tapi untuk menjalankan HP aktifkan dulu layanan aksesibilitas.")
        }
        AssistantService.start(this)
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode != REQ_PERMS) return
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
            toggleSession()
        } else {
            toast("Izin mikrofon diperlukan untuk mode suara.")
        }
    }

    private fun sendText() {
        val text = input.text.toString().trim()
        if (text.isEmpty()) return
        val svc = AssistantService.instance
        if (svc == null) {
            toast("Tekan Mulai dulu.")
            return
        }
        input.setText("")
        AppBus.log(Who.USER, text)
        svc.sendText(text)
    }

    private fun toggleMic() {
        val on = !AppBus.micOn.value
        AppBus.micOn.value = on
        AssistantService.instance?.setMic(on)
    }

    private fun refreshA11y() {
        val active = AgentAccessibilityService.instance != null
        a11yButton.text = if (active) "Aksesibilitas: aktif" else "Aktifkan aksesibilitas"
        a11yButton.background = pill(if (active) GREEN else RED)
    }

    // ------------------------------------------------------------------ data → layar

    private fun observe() {
        ui.launch { AppBus.status.collect { statusText.text = it } }
        ui.launch {
            AppBus.running.collect { running ->
                startButton.text = if (running) "Matikan" else "Mulai"
                startButton.background = pill(if (running) RED else ACCENT)
            }
        }
        ui.launch {
            AppBus.micOn.collect { on ->
                micButton.text = if (on) "🎤 on" else "🎤 off"
                micButton.background = pill(if (on) GREEN else PANEL)
            }
        }
        ui.launch {
            AppBus.task.collect { t ->
                taskText.visibility = if (t == null) View.GONE else View.VISIBLE
                taskText.text = "⏳ Sedang dikerjakan: ${t ?: ""}"
            }
        }
        ui.launch { AppBus.log.collect { addBubble(it) } }
    }

    private fun addBubble(entry: LogEntry) {
        val tv = TextView(this).apply {
            text = entry.text
            textSize = if (entry.who == Who.SYS || entry.who == Who.ERR) 12f else 15f
            setPadding(dp(11), dp(8), dp(11), dp(8))
            setTextColor(
                when (entry.who) {
                    Who.USER -> Color.WHITE
                    Who.AI -> TEXT
                    Who.SYS -> MUTED
                    Who.ERR -> RED
                },
            )
            when (entry.who) {
                Who.USER -> background = rounded(ACCENT)
                Who.AI -> background = rounded(PANEL)
                else -> Unit
            }
        }
        val lp = LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT).apply {
            topMargin = dp(6)
            gravity = when (entry.who) {
                Who.USER -> Gravity.END
                Who.AI -> Gravity.START
                else -> Gravity.CENTER_HORIZONTAL
            }
        }
        tv.maxWidth = (resources.displayMetrics.widthPixels * 0.85).toInt()
        logBox.addView(tv, lp)
        if (logBox.childCount > 300) logBox.removeViewAt(0)
        logScroll.post { logScroll.fullScroll(View.FOCUS_DOWN) }
    }

    // ------------------------------------------------------------------ tampilan

    private fun buildUi(): View {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(BG)
            fitsSystemWindows = true
        }

        // Header
        val header = row().apply { setPadding(dp(14), dp(12), dp(14), dp(8)) }
        header.addView(
            TextView(this).apply {
                text = "Asisten HP"
                textSize = 18f
                setTypeface(typeface, Typeface.BOLD)
                setTextColor(TEXT)
            },
            LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f),
        )
        header.addView(smallButton("⚙") { settingsPanel.visibility = if (settingsPanel.visibility == View.VISIBLE) View.GONE else View.VISIBLE })
        startButton = smallButton("Mulai") { toggleSession() }
        header.addView(startButton)
        root.addView(header)

        statusText = TextView(this).apply {
            textSize = 12f
            setTextColor(MUTED)
            setPadding(dp(14), 0, dp(14), dp(6))
        }
        root.addView(statusText)

        a11yButton = smallButton("") { startActivity(Intent(AndroidSettings.ACTION_ACCESSIBILITY_SETTINGS)) }
        root.addView(a11yButton, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, dp(40)).apply { setMargins(dp(14), 0, dp(14), dp(6)) })

        settingsPanel = buildSettings()
        root.addView(settingsPanel)

        taskText = TextView(this).apply {
            textSize = 13f
            setTextColor(TEXT)
            background = rounded(PANEL)
            setPadding(dp(10), dp(8), dp(10), dp(8))
            visibility = View.GONE
        }
        root.addView(taskText, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT).apply { setMargins(dp(14), 0, dp(14), dp(6)) })

        logBox = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(14), dp(4), dp(14), dp(12))
        }
        logScroll = ScrollView(this).apply { addView(logBox) }
        root.addView(logScroll, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f))

        // Bawah: mic, ketik, kirim, stop
        val bottom = row().apply { setPadding(dp(10), dp(8), dp(10), dp(10)) }
        micButton = smallButton("🎤") { toggleMic() }
        bottom.addView(micButton)
        input = EditText(this).apply {
            hint = "Ketik perintah atau pertanyaan…"
            setHintTextColor(MUTED)
            setTextColor(TEXT)
            textSize = 15f
            background = rounded(PANEL)
            setPadding(dp(12), dp(8), dp(12), dp(8))
            imeOptions = EditorInfo.IME_ACTION_SEND
            inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_CAP_SENTENCES
            setOnEditorActionListener { _, actionId, _ ->
                if (actionId == EditorInfo.IME_ACTION_SEND) {
                    sendText()
                    true
                } else {
                    false
                }
            }
        }
        bottom.addView(input, LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f).apply { setMargins(dp(6), 0, dp(6), 0) })
        bottom.addView(smallButton("Kirim") { sendText() })
        bottom.addView(
            smallButton("■") {
                val stopped = AssistantService.instance?.stopTask() ?: false
                toast(if (stopped) "Tugas dihentikan." else "Tidak ada tugas berjalan.")
            },
        )
        root.addView(bottom)
        return root
    }

    private fun buildSettings(): LinearLayout {
        val panel = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(14), dp(6), dp(14), dp(10))
            visibility = View.GONE
        }
        fun field(label: String, value: String, secret: Boolean = false): EditText {
            panel.addView(TextView(this).apply { text = label; textSize = 12f; setTextColor(MUTED) })
            val et = EditText(this).apply {
                setText(value)
                setTextColor(TEXT)
                textSize = 14f
                inputType = if (secret) {
                    InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
                } else {
                    InputType.TYPE_CLASS_TEXT
                }
            }
            panel.addView(et)
            return et
        }
        val key = field("API key OpenAI", settings.apiKey, secret = true)
        val agentModel = field("Model penyetir HP (vision)", settings.agentModel)
        val rtModel = field("Model suara real-time", settings.realtimeModel)
        val voice = field("Suara (mis. marin, cedar, alloy)", settings.voice)
        val steps = field("Maksimal langkah per tugas", settings.maxSteps.toString())
        panel.addView(
            smallButton("Simpan") {
                settings.apiKey = key.text.toString()
                settings.agentModel = agentModel.text.toString()
                settings.realtimeModel = rtModel.text.toString()
                settings.voice = voice.text.toString()
                settings.maxSteps = steps.text.toString().toIntOrNull() ?: Settings.DEFAULT_MAX_STEPS
                toast("Tersimpan. Matikan lalu Mulai lagi kalau sesi sedang berjalan.")
                panel.visibility = View.GONE
            },
        )
        return panel
    }

    private fun row() = LinearLayout(this).apply {
        orientation = LinearLayout.HORIZONTAL
        gravity = Gravity.CENTER_VERTICAL
    }

    private fun smallButton(label: String, onClick: () -> Unit) = Button(this).apply {
        text = label
        isAllCaps = false
        setTextColor(Color.WHITE)
        background = pill(PANEL)
        minWidth = dp(44)
        minimumWidth = dp(44)
        setPadding(dp(12), 0, dp(12), 0)
        setOnClickListener { onClick() }
    }

    private fun rounded(color: Int) = GradientDrawable().apply {
        setColor(color)
        cornerRadius = dp(12).toFloat()
    }

    private fun pill(color: Int) = GradientDrawable().apply {
        setColor(color)
        cornerRadius = dp(22).toFloat()
    }

    private fun dp(v: Int) = (v * resources.displayMetrics.density).toInt()

    private fun toast(msg: String) = Toast.makeText(this, msg, Toast.LENGTH_LONG).show()

    companion object {
        private const val REQ_PERMS = 7
        private val BG = Color.parseColor("#0E1116")
        private val PANEL = Color.parseColor("#232A35")
        private val TEXT = Color.parseColor("#E8EBF0")
        private val MUTED = Color.parseColor("#8B94A3")
        private val ACCENT = Color.parseColor("#4F8CFF")
        private val GREEN = Color.parseColor("#2FBF71")
        private val RED = Color.parseColor("#EF5350")
    }
}
