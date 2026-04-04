package com.joaquim.minos.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable

private val MinosColorScheme = darkColorScheme(
    background = MinosBackground,
    surface = MinosSurface,
    surfaceContainerHighest = MinosSurfaceHigh,
    primary = MinosPrimary,
    onPrimary = MinosOnPrimary,
    onSurface = MinosOnSurface,
    onSurfaceVariant = MinosOnSurfaceVariant,
    error = MinosError,
)

@Composable
fun ProjectMinosTheme(
    content: @Composable () -> Unit,
) {
    MaterialTheme(
        colorScheme = MinosColorScheme,
        typography = AppTypography,
        content = content,
    )
}

