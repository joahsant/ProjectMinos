package com.joaquim.minos.model

data class MarketSnapshot(
    val symbol: String,
    val lastPrice: String,
    val priceChangePercent24h: String,
    val highPrice24h: String,
    val lowPrice24h: String,
    val updatedAtMillis: Long,
)

