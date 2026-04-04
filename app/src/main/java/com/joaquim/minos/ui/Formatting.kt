package com.joaquim.minos.ui

import java.text.NumberFormat
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

fun Long.toDisplayTime(): String {
    val formatter = SimpleDateFormat("HH:mm:ss", Locale.getDefault())
    return formatter.format(Date(this))
}

fun String.toUsdtDisplay(): String {
    val value = toDoubleOrNull() ?: return this
    val formatter = NumberFormat.getNumberInstance(Locale.US).apply {
        minimumFractionDigits = 2
        maximumFractionDigits = 2
    }
    return "$${formatter.format(value)}"
}

fun String.toPercentDisplay(): String {
    val value = toDoubleOrNull() ?: return this
    return String.format(Locale.US, "%+.2f%%", value)
}
