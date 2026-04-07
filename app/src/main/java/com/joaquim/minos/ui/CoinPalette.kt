package com.joaquim.minos.ui

import androidx.compose.ui.graphics.Color

data class CoinPalette(
    val card: Color,
    val text: Color,
    val pill: Color,
    val pillText: Color,
)

fun coinPaletteFor(coinId: String): CoinPalette {
    return when (coinId) {
        "bitcoin" -> CoinPalette(
            card = Color(0xFFF4F3EE),
            text = Color(0xFF1C1A16),
            pill = Color(0xFFFFC681),
            pillText = Color(0xFF6A3B00),
        )
        "ethereum" -> CoinPalette(
            card = Color(0xFFDCCBFF),
            text = Color(0xFF24173F),
            pill = Color(0xFFF3EBFF),
            pillText = Color(0xFF5A418E),
        )
        "solana" -> CoinPalette(
            card = Color(0xFFDBFFF2),
            text = Color(0xFF073B2C),
            pill = Color(0xFFA7F1D1),
            pillText = Color(0xFF0C5A41),
        )
        "binancecoin" -> CoinPalette(
            card = Color(0xFFFFF0A6),
            text = Color(0xFF423400),
            pill = Color(0xFFFFD65A),
            pillText = Color(0xFF5D4400),
        )
        "ripple" -> CoinPalette(
            card = Color(0xFFDDEBFF),
            text = Color(0xFF10233F),
            pill = Color(0xFFBDD5FF),
            pillText = Color(0xFF2A4A80),
        )
        "cardano" -> CoinPalette(
            card = Color(0xFFFFD5E8),
            text = Color(0xFF4D1731),
            pill = Color(0xFFFFB5D4),
            pillText = Color(0xFF7A3054),
        )
        "dogecoin" -> CoinPalette(
            card = Color(0xFFFFE2B8),
            text = Color(0xFF4D2A00),
            pill = Color(0xFFFFC86E),
            pillText = Color(0xFF6A3E00),
        )
        "tron" -> CoinPalette(
            card = Color(0xFFFFD2CC),
            text = Color(0xFF4B1711),
            pill = Color(0xFFFFA79A),
            pillText = Color(0xFF7D2E21),
        )
        else -> FALLBACK_PALETTES[(coinId.hashCode().safeAbsoluteValue) % FALLBACK_PALETTES.size]
    }
}

private val FALLBACK_PALETTES = listOf(
    CoinPalette(Color(0xFFC8CCFF), Color(0xFF1D225C), Color(0xFFE7E9FF), Color(0xFF404A9A)),
    CoinPalette(Color(0xFFFFCCF4), Color(0xFF531B4A), Color(0xFFFFE2FA), Color(0xFF8A447C)),
    CoinPalette(Color(0xFFD0FFD8), Color(0xFF124B21), Color(0xFFE9FFED), Color(0xFF2B8242)),
    CoinPalette(Color(0xFFFFDEC6), Color(0xFF5A2A0A), Color(0xFFFFF0E2), Color(0xFF9B5A22)),
)

private val Int.safeAbsoluteValue: Int
    get() = if (this == Int.MIN_VALUE) 0 else if (this < 0) -this else this
