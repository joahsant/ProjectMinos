package com.joaquim.minos.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class BinanceTicker24hrDto(
    @SerialName("symbol") val symbol: String,
    @SerialName("lastPrice") val lastPrice: String,
    @SerialName("priceChangePercent") val priceChangePercent: String,
    @SerialName("highPrice") val highPrice: String,
    @SerialName("lowPrice") val lowPrice: String,
)

