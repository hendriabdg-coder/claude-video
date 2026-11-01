package com.endrich.asistenhp

import android.annotation.SuppressLint
import android.content.Context
import android.media.AudioAttributes
import android.media.AudioDeviceInfo
import android.media.AudioFormat
import android.media.AudioManager
import android.media.AudioRecord
import android.media.AudioTrack
import android.media.MediaRecorder
import android.media.audiofx.AcousticEchoCanceler
import android.media.audiofx.NoiseSuppressor
import android.os.Build
import java.util.concurrent.LinkedBlockingQueue
import java.util.concurrent.TimeUnit

/** Audio dua arah yang dipakai [RealtimeVoice] (dipisah supaya bisa diuji tanpa HP). */
interface VoiceAudio {
    var micEnabled: Boolean
    fun start(onChunk: (ByteArray) -> Unit)
    fun play(pcm: ByteArray)
    fun flushPlayback()
    fun stop()
}

/**
 * Mikrofon + speaker untuk OpenAI Realtime: PCM16 mono 24 kHz.
 * Memakai mode "komunikasi" Android supaya peredam gema (AEC) aktif,
 * jadi suara AI dari speaker tidak terdengar balik sebagai ucapan pengguna.
 */
class AudioIO(context: Context) : VoiceAudio {

    private val audioManager = context.getSystemService(Context.AUDIO_SERVICE) as AudioManager
    private var record: AudioRecord? = null
    private var track: AudioTrack? = null
    private var aec: AcousticEchoCanceler? = null
    private var ns: NoiseSuppressor? = null
    private var captureThread: Thread? = null
    private var playThread: Thread? = null
    private val playQueue = LinkedBlockingQueue<ByteArray>()
    private var previousMode = AudioManager.MODE_NORMAL

    @Volatile
    private var running = false

    @Volatile
    override var micEnabled = true

    @SuppressLint("MissingPermission") // izin RECORD_AUDIO dicek di MainActivity sebelum service dimulai
    override fun start(onChunk: (ByteArray) -> Unit) {
        if (running) return
        running = true

        previousMode = audioManager.mode
        audioManager.mode = AudioManager.MODE_IN_COMMUNICATION
        routeOutput()

        val minIn = AudioRecord.getMinBufferSize(RATE, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT)
        val rec = AudioRecord(
            MediaRecorder.AudioSource.VOICE_COMMUNICATION,
            RATE,
            AudioFormat.CHANNEL_IN_MONO,
            AudioFormat.ENCODING_PCM_16BIT,
            maxOf(minIn, CHUNK_BYTES * 4),
        )
        record = rec
        if (AcousticEchoCanceler.isAvailable()) aec = AcousticEchoCanceler.create(rec.audioSessionId)?.apply { enabled = true }
        if (NoiseSuppressor.isAvailable()) ns = NoiseSuppressor.create(rec.audioSessionId)?.apply { enabled = true }

        val minOut = AudioTrack.getMinBufferSize(RATE, AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT)
        val out = AudioTrack.Builder()
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_VOICE_COMMUNICATION)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build(),
            )
            .setAudioFormat(
                AudioFormat.Builder()
                    .setSampleRate(RATE)
                    .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                    .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                    .build(),
            )
            .setTransferMode(AudioTrack.MODE_STREAM)
            .setBufferSizeInBytes(maxOf(minOut, CHUNK_BYTES * 8))
            .build()
        track = out
        out.play()

        rec.startRecording()
        captureThread = Thread({
            val buf = ByteArray(CHUNK_BYTES)
            while (running) {
                val n = rec.read(buf, 0, buf.size)
                if (n > 0 && micEnabled) onChunk(buf.copyOf(n))
            }
        }, "asisten-mic").apply { start() }

        playThread = Thread({
            while (running) {
                val chunk = try {
                    playQueue.poll(200, TimeUnit.MILLISECONDS)
                } catch (_: InterruptedException) {
                    null
                } ?: continue
                out.write(chunk, 0, chunk.size) // blocking: menjaga tempo pemutaran
            }
        }, "asisten-speaker").apply { start() }
    }

    override fun play(pcm: ByteArray) {
        if (running) playQueue.offer(pcm)
    }

    /** Hentikan suara AI seketika (dipakai saat pengguna memotong bicara). */
    override fun flushPlayback() {
        playQueue.clear()
        track?.let {
            runCatching {
                it.pause()
                it.flush()
                it.play()
            }
        }
    }

    override fun stop() {
        if (!running) return
        running = false
        playQueue.clear()
        captureThread?.join(500)
        playThread?.interrupt()
        playThread?.join(500)
        runCatching { record?.stop() }
        record?.release()
        record = null
        runCatching { track?.stop() }
        track?.release()
        track = null
        aec?.release()
        ns?.release()
        aec = null
        ns = null
        if (Build.VERSION.SDK_INT >= 31) audioManager.clearCommunicationDevice()
        @Suppress("DEPRECATION")
        if (Build.VERSION.SDK_INT < 31) audioManager.isSpeakerphoneOn = false
        audioManager.mode = previousMode
    }

    /** Pakai headset/earphone kalau ada, kalau tidak pakai speaker HP (bukan speaker telinga). */
    private fun routeOutput() {
        if (Build.VERSION.SDK_INT >= 31) {
            val devices = audioManager.availableCommunicationDevices
            val headset = devices.firstOrNull { it.type in HEADSET_TYPES }
            val target = headset ?: devices.firstOrNull { it.type == AudioDeviceInfo.TYPE_BUILTIN_SPEAKER }
            if (target != null) audioManager.setCommunicationDevice(target)
        } else {
            @Suppress("DEPRECATION")
            audioManager.isSpeakerphoneOn = true
        }
    }

    companion object {
        const val RATE = 24_000
        private const val CHUNK_BYTES = RATE / 1000 * 40 * 2 // 40 ms PCM16 mono
        private val HEADSET_TYPES = setOf(
            AudioDeviceInfo.TYPE_WIRED_HEADSET,
            AudioDeviceInfo.TYPE_WIRED_HEADPHONES,
            AudioDeviceInfo.TYPE_BLUETOOTH_SCO,
            AudioDeviceInfo.TYPE_BLE_HEADSET,
            AudioDeviceInfo.TYPE_USB_HEADSET,
        )
    }
}
