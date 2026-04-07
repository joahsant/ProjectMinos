package com.joaquim.minos.data

import com.joaquim.minos.model.MarketSnapshot

class CoinGeckoMarketRepository(
    private val apiClient: CoinGeckoApiClient,
) {
    suspend fun fetchTopCoins(): List<MarketSnapshot> {
        val updatedAtMillis = System.currentTimeMillis()

        return apiClient.fetchTopCoins().map { coin ->
            MarketSnapshot(
                id = coin.id,
                symbol = coin.symbol.uppercase(),
                name = coin.name,
                imageUrl = coin.image,
                lastPrice = coin.currentPrice,
                priceChangePercent24h = coin.priceChangePercentage24h,
                highPrice24h = coin.high24h,
                lowPrice24h = coin.low24h,
                marketCapRank = coin.marketCapRank,
                updatedAtMillis = updatedAtMillis,
            )
        }
    }

    suspend fun fetchCoinSummary(coinId: String): String {
        val detail = apiClient.fetchCoinDetail(coinId)
        return detail.description.english.orEmpty()
    }
}
