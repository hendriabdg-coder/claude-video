package com.endrich.asistenhp

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Path
import android.graphics.Rect
import android.os.Bundle
import android.util.Base64
import android.view.Display
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import android.view.accessibility.AccessibilityWindowInfo
import kotlinx.coroutines.suspendCancellableCoroutine
import java.io.ByteArrayOutputStream
import kotlin.coroutines.resume

/** Satu elemen layar yang bisa dirujuk agen lewat nomor indeks. */
data class UiElement(
    val index: Int,
    val node: AccessibilityNodeInfo,
    val bounds: Rect,
    val description: String,
)

/** Screenshot yang sudah diperkecil; [scale] = lebar gambar / lebar layar asli. */
class Screenshot(val base64Jpeg: String, val width: Int, val height: Int, val scale: Float)

/**
 * "Tangan dan mata" agen: membaca struktur layar, mengambil screenshot, dan
 * mengetuk / menggeser / mengetik. Aktif setelah pengguna menyalakannya di
 * Pengaturan > Aksesibilitas.
 */
class AgentAccessibilityService : AccessibilityService() {

    companion object {
        @Volatile
        var instance: AgentAccessibilityService? = null
            private set

        private const val MAX_ELEMENTS = 150
    }

    override fun onServiceConnected() {
        super.onServiceConnected()
        instance = this
        AppBus.log(Who.SYS, "Layanan aksesibilitas aktif.")
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) = Unit

    override fun onInterrupt() = Unit

    override fun onUnbind(intent: Intent?): Boolean {
        instance = null
        return super.onUnbind(intent)
    }

    override fun onDestroy() {
        instance = null
        super.onDestroy()
    }

    // ------------------------------------------------------------------ membaca layar

    fun currentPackage(): String? = rootInActiveWindow?.packageName?.toString()

    /** Daftar elemen penting di layar. Koordinat dikalikan [scale] supaya sama dengan screenshot. */
    fun snapshotUi(scale: Float): List<UiElement> {
        val roots = mutableListOf<AccessibilityNodeInfo>()
        try {
            for (w in windows) {
                if (w.type == AccessibilityWindowInfo.TYPE_APPLICATION ||
                    w.type == AccessibilityWindowInfo.TYPE_SYSTEM
                ) {
                    val root = w.root ?: continue
                    if (root.packageName?.toString() == packageName) continue // jangan baca aplikasi sendiri
                    roots.add(root)
                }
            }
        } catch (_: Exception) {
            // abaikan, pakai jendela aktif saja
        }
        if (roots.isEmpty()) rootInActiveWindow?.let { roots.add(it) }

        val out = mutableListOf<UiElement>()
        for (root in roots) walk(root, out, scale)
        return out
    }

    private fun walk(node: AccessibilityNodeInfo, out: MutableList<UiElement>, scale: Float) {
        if (out.size >= MAX_ELEMENTS) return
        if (!node.isVisibleToUser) return

        val label = listOfNotNull(
            node.text?.toString(),
            node.contentDescription?.toString(),
            node.hintText?.toString(),
        ).map { it.trim().replace('\n', ' ') }.firstOrNull { it.isNotEmpty() }

        val interactive = node.isClickable || node.isLongClickable || node.isEditable ||
            node.isScrollable || node.isCheckable
        if (interactive || label != null) {
            val r = Rect()
            node.getBoundsInScreen(r)
            if (r.width() > 0 && r.height() > 0) {
                val idx = out.size
                val cls = node.className?.toString()?.substringAfterLast('.') ?: "View"
                val id = node.viewIdResourceName?.substringAfterLast('/')
                val cx = (r.exactCenterX() * scale).toInt()
                val cy = (r.exactCenterY() * scale).toInt()
                val flags = buildList {
                    if (node.isClickable) add("klik")
                    if (node.isEditable) add("ketik")
                    if (node.isScrollable) add("scroll")
                    if (node.isCheckable) add(if (node.isChecked) "dicentang" else "tidak-dicentang")
                    if (!node.isEnabled) add("nonaktif")
                    if (node.isFocused) add("fokus")
                }.joinToString(",")
                val desc = buildString {
                    append("[$idx] $cls")
                    if (label != null) append(" \"${label.take(80)}\"")
                    if (id != null) append(" id=$id")
                    append(" @($cx,$cy)")
                    if (flags.isNotEmpty()) append(" $flags")
                }
                out.add(UiElement(idx, node, r, desc))
            }
        }
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            walk(child, out, scale)
        }
    }

    /** Screenshot layar sekarang (Android 11+), diperkecil ke lebar [maxWidth]. */
    suspend fun screenshot(maxWidth: Int = 720): Screenshot? = suspendCancellableCoroutine { cont ->
        try {
            takeScreenshot(
                Display.DEFAULT_DISPLAY,
                mainExecutor,
                object : TakeScreenshotCallback {
                    override fun onSuccess(result: ScreenshotResult) {
                        val shot = try {
                            val hw = Bitmap.wrapHardwareBuffer(result.hardwareBuffer, result.colorSpace)
                            val soft = hw?.copy(Bitmap.Config.ARGB_8888, false)
                            result.hardwareBuffer.close()
                            soft?.let { encode(it, maxWidth) }
                        } catch (e: Exception) {
                            null
                        }
                        if (cont.isActive) cont.resume(shot)
                    }

                    override fun onFailure(errorCode: Int) {
                        if (cont.isActive) cont.resume(null)
                    }
                },
            )
        } catch (e: Exception) {
            if (cont.isActive) cont.resume(null)
        }
    }

    private fun encode(full: Bitmap, maxWidth: Int): Screenshot {
        val scale = if (full.width > maxWidth) maxWidth.toFloat() / full.width else 1f
        val bmp = if (scale < 1f) {
            Bitmap.createScaledBitmap(full, (full.width * scale).toInt(), (full.height * scale).toInt(), true)
        } else {
            full
        }
        val bytes = ByteArrayOutputStream().use { stream ->
            bmp.compress(Bitmap.CompressFormat.JPEG, 70, stream)
            stream.toByteArray()
        }
        return Screenshot(Base64.encodeToString(bytes, Base64.NO_WRAP), bmp.width, bmp.height, scale)
    }

    // ------------------------------------------------------------------ aksi

    suspend fun click(el: UiElement): Boolean {
        var n: AccessibilityNodeInfo? = el.node
        while (n != null && !n.isClickable) n = n.parent
        if (n != null && n.performAction(AccessibilityNodeInfo.ACTION_CLICK)) return true
        return tap(el.bounds.exactCenterX(), el.bounds.exactCenterY())
    }

    suspend fun longPress(el: UiElement): Boolean {
        var n: AccessibilityNodeInfo? = el.node
        while (n != null && !n.isLongClickable) n = n.parent
        if (n != null && n.performAction(AccessibilityNodeInfo.ACTION_LONG_CLICK)) return true
        return gesture(pointPath(el.bounds.exactCenterX(), el.bounds.exactCenterY()), 800)
    }

    suspend fun tap(x: Float, y: Float): Boolean = gesture(pointPath(x, y), 60)

    suspend fun swipe(x1: Float, y1: Float, x2: Float, y2: Float, durationMs: Long = 400): Boolean {
        val path = Path().apply {
            moveTo(x1, y1)
            lineTo(x2, y2)
        }
        return gesture(path, durationMs)
    }

    /** Scroll konten. direction = arah konten bergerak dilihat pengguna: down = lihat yang di bawah. */
    suspend fun scroll(direction: String, el: UiElement?): Boolean {
        if (el != null) {
            var n: AccessibilityNodeInfo? = el.node
            while (n != null && !n.isScrollable) n = n.parent
            val action = if (direction == "down" || direction == "right") {
                AccessibilityNodeInfo.ACTION_SCROLL_FORWARD
            } else {
                AccessibilityNodeInfo.ACTION_SCROLL_BACKWARD
            }
            if (n != null && n.performAction(action)) return true
        }
        val dm = resources.displayMetrics
        val w = dm.widthPixels.toFloat()
        val h = dm.heightPixels.toFloat()
        return when (direction) {
            "down" -> swipe(w / 2, h * 0.70f, w / 2, h * 0.30f)
            "up" -> swipe(w / 2, h * 0.30f, w / 2, h * 0.70f)
            "right" -> swipe(w * 0.80f, h / 2, w * 0.20f, h / 2)
            "left" -> swipe(w * 0.20f, h / 2, w * 0.80f, h / 2)
            else -> false
        }
    }

    fun setText(el: UiElement?, text: String): Boolean {
        val node = el?.node ?: findFocus(AccessibilityNodeInfo.FOCUS_INPUT) ?: return false
        node.performAction(AccessibilityNodeInfo.ACTION_FOCUS)
        val args = Bundle().apply {
            putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, text)
        }
        return node.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, args)
    }

    /** Tekan Enter / kirim pada kolom yang sedang fokus. */
    fun pressEnter(): Boolean {
        val node = findFocus(AccessibilityNodeInfo.FOCUS_INPUT) ?: return false
        return node.performAction(AccessibilityNodeInfo.AccessibilityAction.ACTION_IME_ENTER.id)
    }

    fun global(action: String): Boolean = when (action) {
        "back" -> performGlobalAction(GLOBAL_ACTION_BACK)
        "home" -> performGlobalAction(GLOBAL_ACTION_HOME)
        "recents" -> performGlobalAction(GLOBAL_ACTION_RECENTS)
        "notifications" -> performGlobalAction(GLOBAL_ACTION_NOTIFICATIONS)
        "quick_settings" -> performGlobalAction(GLOBAL_ACTION_QUICK_SETTINGS)
        "enter" -> pressEnter()
        else -> false
    }

    /** Buka aplikasi berdasarkan nama (label di launcher) atau nama paket. Kembali: label yang dibuka. */
    fun openApp(query: String): String? {
        val q = query.lowercase().trim()
        if (q.isEmpty()) return null
        val pm = packageManager
        val launcher = Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER)
        val apps = if (android.os.Build.VERSION.SDK_INT >= 33) {
            pm.queryIntentActivities(launcher, PackageManager.ResolveInfoFlags.of(0L))
        } else {
            @Suppress("DEPRECATION")
            pm.queryIntentActivities(launcher, 0) // Android 11-12: ResolveInfoFlags belum ada
        }
        val best = apps.mapNotNull { ri ->
            val label = ri.loadLabel(pm).toString()
            val l = label.lowercase()
            val pkg = ri.activityInfo.packageName
            val score = when {
                l == q || pkg == q -> 0
                l.startsWith(q) -> 1
                l.contains(q) -> 2
                q.contains(l) && l.length >= 3 -> 3
                pkg.lowercase().contains(q.replace(" ", "")) -> 4
                else -> return@mapNotNull null
            }
            Triple(score, label, pkg)
        }.filter { it.third != packageName }.minByOrNull { it.first } ?: return null

        val intent = pm.getLaunchIntentForPackage(best.third) ?: return null
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_RESET_TASK_IF_NEEDED)
        startActivity(intent)
        return best.second
    }

    // ------------------------------------------------------------------ util

    private fun pointPath(x: Float, y: Float) = Path().apply { moveTo(x, y) }

    private suspend fun gesture(path: Path, durationMs: Long): Boolean = suspendCancellableCoroutine { cont ->
        val g = GestureDescription.Builder()
            .addStroke(GestureDescription.StrokeDescription(path, 0, durationMs))
            .build()
        val dispatched = dispatchGesture(
            g,
            object : GestureResultCallback() {
                override fun onCompleted(gestureDescription: GestureDescription?) {
                    if (cont.isActive) cont.resume(true)
                }

                override fun onCancelled(gestureDescription: GestureDescription?) {
                    if (cont.isActive) cont.resume(false)
                }
            },
            null,
        )
        if (!dispatched && cont.isActive) cont.resume(false)
    }
}
