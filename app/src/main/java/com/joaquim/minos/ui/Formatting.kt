package com.joaquim.minos.ui

import java.text.NumberFormat
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

fun Long.toDisplayTime(): String {
    val formatter = SimpleDateFormat("HH:mm:ss", Locale.getDefault())
    return formatter.format(Date(this))
}

fun Double.toUsdDisplay(): String {
    val formatter = NumberFormat.getNumberInstance(Locale.US).apply {
        minimumFractionDigits = if (this@toUsdDisplay >= 1.0) 2 else 4
        maximumFractionDigits = if (this@toUsdDisplay >= 1.0) 2 else 4
    }
    return "$${formatter.format(this)}"
}

fun Double?.toUsdDisplayOrDash(): String {
    return this?.toUsdDisplay() ?: "—"
}

fun Double?.toPercentDisplay(): String {
    val value = this ?: return "—"
    return String.format(Locale.US, "%+.2f%%", value)
}
