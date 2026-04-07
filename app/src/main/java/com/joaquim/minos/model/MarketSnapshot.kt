package com.joaquim.minos.model

data class MarketSnapshot(
    val id: String,
    val symbol: String,
    val name: String,
    val imageUrl: String,
    val lastPrice: Double,
    val priceChangePercent24h: Double?,
    val highPrice24h: Double?,
    val lowPrice24h: Double?,
    val marketCapRank: Int?,
    val updatedAtMillis: Long,
)
