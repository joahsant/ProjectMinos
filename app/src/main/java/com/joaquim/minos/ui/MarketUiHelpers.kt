package com.joaquim.minos.ui

import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable

@Composable
fun marketChangeColor(
    rawValue: Double?,
) = (rawValue ?: 0.0).let { change ->
    when {
        change > 0.0 -> MaterialTheme.colorScheme.primary
        change < 0.0 -> MaterialTheme.colorScheme.error
        else -> MaterialTheme.colorScheme.onSurface
    }
}
