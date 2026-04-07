package com.joaquim.minos.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class CoinGeckoCoinDetailDto(
    @SerialName("id") val id: String,
    @SerialName("description") val description: DescriptionDto = DescriptionDto(),
) {
    @Serializable
    data class DescriptionDto(
        @SerialName("en") val english: String? = null,
    )
}
