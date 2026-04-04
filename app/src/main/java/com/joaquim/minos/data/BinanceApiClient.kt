package com.joaquim.minos.data

import java.net.HttpURLConnection
import java.net.URL
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json

class BinanceApiClient(
    private val json: Json = Json { ignoreUnknownKeys = true },
) {
    suspend fun fetchTicker24h(symbol: String): BinanceTicker24hrDto = withContext(Dispatchers.IO) {
        val url = URL("https://api.binance.com/api/v3/ticker/24hr?symbol=$symbol")
        val connection = (url.openConnection() as HttpURLConnection).apply {
            requestMethod = "GET"
            connectTimeout = 15_000
            readTimeout = 15_000
            doInput = true
        }

        try {
            val statusCode = connection.responseCode
            if (statusCode !in 200..299) {
                throw IllegalStateException("Binance request failed with HTTP $statusCode")
            }

            val payload = connection.inputStream.bufferedReader().use { it.readText() }
            json.decodeFromString<BinanceTicker24hrDto>(payload)
        } finally {
            connection.disconnect()
        }
    }
}

