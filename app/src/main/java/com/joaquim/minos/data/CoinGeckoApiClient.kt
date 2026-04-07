package com.joaquim.minos.data

import java.net.HttpURLConnection
import java.net.URLEncoder
import java.net.URL
import kotlin.text.Charsets.UTF_8
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json

class CoinGeckoApiClient(
    private val json: Json = Json { ignoreUnknownKeys = true },
) {
    suspend fun fetchTopCoins(): List<CoinGeckoCoinMarketDto> = withContext(Dispatchers.IO) {
        val endpoint =
            "$BASE_URL/coins/markets" +
                "?vs_currency=usd" +
                "&order=market_cap_desc" +
                "&per_page=50" +
                "&page=1" +
                "&sparkline=false" +
                "&price_change_percentage=24h"

        performRequest(endpoint) { payload ->
            json.decodeFromString<List<CoinGeckoCoinMarketDto>>(payload)
        }
    }

    suspend fun fetchCoinDetail(coinId: String): CoinGeckoCoinDetailDto = withContext(Dispatchers.IO) {
        val encodedId = URLEncoder.encode(coinId, UTF_8.name())
        val endpoint =
            "$BASE_URL/coins/$encodedId" +
                "?localization=false" +
                "&tickers=false" +
                "&market_data=false" +
                "&community_data=false" +
                "&developer_data=false" +
                "&sparkline=false"

        performRequest(endpoint) { payload ->
            json.decodeFromString<CoinGeckoCoinDetailDto>(payload)
        }
    }

    private fun <T> performRequest(
        endpoint: String,
        transform: (String) -> T,
    ): T {
        val connection = (URL(endpoint).openConnection() as HttpURLConnection).apply {
            requestMethod = "GET"
            connectTimeout = 15_000
            readTimeout = 15_000
            doInput = true
            setRequestProperty("Accept", "application/json")
        }

        try {
            val statusCode = connection.responseCode
            if (statusCode !in 200..299) {
                throw IllegalStateException("CoinGecko request failed with HTTP $statusCode")
            }

            val payload = connection.inputStream.bufferedReader().use { it.readText() }
            return transform(payload)
        } finally {
            connection.disconnect()
        }
    }

    private companion object {
        const val BASE_URL = "https://api.coingecko.com/api/v3"
    }
}
