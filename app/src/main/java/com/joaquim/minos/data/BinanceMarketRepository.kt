package com.joaquim.minos.data

import com.joaquim.minos.model.MarketSnapshot

class BinanceMarketRepository(
    private val apiClient: BinanceApiClient,
) {
    suspend fun fetchBtcUsdtSnapshot(): MarketSnapshot {
        val ticker = apiClient.fetchTicker24h(symbol = BTC_USDT_SYMBOL)

        return MarketSnapshot(
            symbol = ticker.symbol,
            lastPrice = ticker.lastPrice,
            priceChangePercent24h = ticker.priceChangePercent,
            highPrice24h = ticker.highPrice,
            lowPrice24h = ticker.lowPrice,
            updatedAtMillis = System.currentTimeMillis(),
        )
    }

    companion object {
        const val BTC_USDT_SYMBOL = "BTCUSDT"
    }
}

