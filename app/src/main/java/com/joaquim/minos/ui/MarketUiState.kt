package com.joaquim.minos.ui

import com.joaquim.minos.model.MarketSnapshot

data class MarketUiState(
    val catalog: List<MarketSnapshot> = emptyList(),
    val collectionIds: List<String> = listOf(DEFAULT_COLLECTION_ID),
    val selectedCoinId: String = DEFAULT_COLLECTION_ID,
    val searchQuery: String = "",
    val isCatalogVisible: Boolean = false,
    val quoteState: QuoteUiState = QuoteUiState.Loading(recoveryMode = false),
    val previewState: CoinPreviewState? = null,
) {
    val selectedCoin: MarketSnapshot?
        get() = catalog.firstOrNull { it.id == selectedCoinId }

    val collectionCoins: List<MarketSnapshot>
        get() = collectionIds.mapNotNull { coinId -> catalog.firstOrNull { it.id == coinId } }

    val filteredCatalog: List<MarketSnapshot>
        get() {
            if (searchQuery.isBlank()) {
                return catalog
            }

            val normalizedQuery = searchQuery.trim().lowercase()
            return catalog.filter { coin ->
                coin.name.lowercase().contains(normalizedQuery) ||
                    coin.symbol.lowercase().contains(normalizedQuery)
            }
        }

    companion object {
        const val DEFAULT_COLLECTION_ID = "bitcoin"
    }
}

sealed interface QuoteUiState {
    data class Loading(
        val recoveryMode: Boolean,
    ) : QuoteUiState

    data class Loaded(
        val snapshot: MarketSnapshot,
    ) : QuoteUiState
}

sealed interface CoinPreviewState {
    val coin: MarketSnapshot

    data class Loading(
        override val coin: MarketSnapshot,
    ) : CoinPreviewState

    data class Loaded(
        override val coin: MarketSnapshot,
        val summary: String,
    ) : CoinPreviewState

    data class Error(
        override val coin: MarketSnapshot,
        val message: String,
    ) : CoinPreviewState
}
