package com.joaquim.minos.ui

import android.text.Html
import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.joaquim.minos.data.CoinGeckoMarketRepository
import com.joaquim.minos.data.HostCollectionPreferences
import com.joaquim.minos.model.MarketSnapshot
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class MarketViewModel(
    private val repository: CoinGeckoMarketRepository,
    private val preferences: HostCollectionPreferences,
) : ViewModel() {
    private val logTag = "MinosMarketViewModel"
    private val summaryCache = mutableMapOf<String, String>()

    private val _uiState = MutableStateFlow(
        MarketUiState(
            collectionIds = preferences.loadCollectionIds(),
            selectedCoinId = preferences.loadSelectedCoinId(),
            isCatalogVisible = false,
            quoteState = QuoteUiState.Loading(recoveryMode = false),
        ),
    )
    val uiState: StateFlow<MarketUiState> = _uiState.asStateFlow()

    init {
        observeMarket()
    }

    fun showCatalog() {
        _uiState.update { it.copy(isCatalogVisible = true) }
    }

    fun hideCatalog() {
        _uiState.update { it.copy(isCatalogVisible = false, searchQuery = "") }
    }

    fun updateSearchQuery(query: String) {
        _uiState.update {
            it.copy(
                searchQuery = query,
                isCatalogVisible = query.isNotBlank() || it.isCatalogVisible,
            )
        }
    }

    fun selectCoinFromCollection(coinId: String) {
        preferences.saveSelectedCoinId(coinId)
        _uiState.update { state ->
            state.copy(
                selectedCoinId = coinId,
                quoteState = state.catalog.firstOrNull { it.id == coinId }?.let(QuoteUiState::Loaded)
                    ?: QuoteUiState.Loading(recoveryMode = state.catalog.isNotEmpty()),
            )
        }
    }

    fun previewCoin(coin: MarketSnapshot) {
        _uiState.update { it.copy(previewState = CoinPreviewState.Loading(coin)) }

        val cachedSummary = summaryCache[coin.id]
        if (cachedSummary != null) {
            _uiState.update { it.copy(previewState = CoinPreviewState.Loaded(coin, cachedSummary)) }
            return
        }

        viewModelScope.launch {
            try {
                val summary = repository.fetchCoinSummary(coin.id).toPlainSummary()
                summaryCache[coin.id] = summary
                _uiState.update { current ->
                    if (current.previewState?.coin?.id == coin.id) {
                        current.copy(previewState = CoinPreviewState.Loaded(coin, summary))
                    } else {
                        current
                    }
                }
            } catch (error: Exception) {
                Log.w(logTag, "previewCoin: summary load failed for ${coin.id}", error)
                _uiState.update { current ->
                    if (current.previewState?.coin?.id == coin.id) {
                        current.copy(
                            previewState = CoinPreviewState.Error(
                                coin = coin,
                                message = "Summary unavailable right now.",
                            ),
                        )
                    } else {
                        current
                    }
                }
            }
        }
    }

    fun dismissPreview() {
        _uiState.update { it.copy(previewState = null) }
    }

    fun addPreviewCoin() {
        val previewCoin = _uiState.value.previewState?.coin ?: return
        val nextCollection = (_uiState.value.collectionIds + previewCoin.id).distinct()
        preferences.saveCollectionIds(nextCollection)
        preferences.saveSelectedCoinId(previewCoin.id)
        _uiState.update {
            it.copy(
                collectionIds = nextCollection,
                selectedCoinId = previewCoin.id,
                previewState = null,
                isCatalogVisible = false,
                searchQuery = "",
                quoteState = QuoteUiState.Loaded(previewCoin),
            )
        }
    }

    private fun observeMarket() {
        viewModelScope.launch {
            var hasLoadedSuccessfully = false

            while (true) {
                try {
                    val catalog = repository.fetchTopCoins()
                    val selectedCoin = resolveSelectedCoin(catalog)

                    Log.d(logTag, "observeMarket: catalog loaded at ${selectedCoin.updatedAtMillis}")
                    _uiState.update { state ->
                        state.copy(
                            catalog = catalog,
                            collectionIds = normalizeCollectionIds(state.collectionIds, catalog),
                            selectedCoinId = selectedCoin.id,
                            quoteState = QuoteUiState.Loaded(selectedCoin),
                        )
                    }
                    hasLoadedSuccessfully = true
                    delay(STEADY_STATE_REFRESH_MILLIS)
                } catch (error: Exception) {
                    Log.w(logTag, "observeMarket: market load failed", error)
                    _uiState.update { state ->
                        state.copy(
                            quoteState = QuoteUiState.Loading(recoveryMode = hasLoadedSuccessfully),
                        )
                    }
                    delay(RETRY_REFRESH_MILLIS)
                }
            }
        }
    }

    private fun resolveSelectedCoin(catalog: List<MarketSnapshot>): MarketSnapshot {
        val normalizedCollection = normalizeCollectionIds(_uiState.value.collectionIds, catalog)
        if (normalizedCollection != _uiState.value.collectionIds) {
            preferences.saveCollectionIds(normalizedCollection)
        }

        val requestedSelection = _uiState.value.selectedCoinId
        val resolvedSelection = normalizedCollection.firstOrNull { it == requestedSelection }
            ?: normalizedCollection.firstOrNull()
            ?: catalog.first().id

        preferences.saveSelectedCoinId(resolvedSelection)
        return catalog.firstOrNull { it.id == resolvedSelection } ?: catalog.first()
    }

    private fun normalizeCollectionIds(
        collectionIds: List<String>,
        catalog: List<MarketSnapshot>,
    ): List<String> {
        val availableIds = catalog.mapTo(linkedSetOf()) { it.id }
        val normalized = collectionIds.filter(availableIds::contains).ifEmpty {
            listOf(MarketUiState.DEFAULT_COLLECTION_ID)
        }.filter(availableIds::contains)

        return if (normalized.isEmpty()) {
            listOf(catalog.first().id)
        } else {
            normalized
        }
    }

    private fun String.toPlainSummary(): String {
        val plainText = Html.fromHtml(this, Html.FROM_HTML_MODE_LEGACY)
            .toString()
            .replace(Regex("\\s+"), " ")
            .trim()

        return when {
            plainText.isBlank() -> "Summary unavailable right now."
            plainText.length <= MAX_SUMMARY_LENGTH -> plainText
            else -> plainText.take(MAX_SUMMARY_LENGTH).trimEnd() + "..."
        }
    }

    companion object {
        private const val RETRY_REFRESH_MILLIS = 5_000L
        private const val STEADY_STATE_REFRESH_MILLIS = 60_000L
        private const val MAX_SUMMARY_LENGTH = 220
    }
}

class MarketViewModelFactory(
    private val repository: CoinGeckoMarketRepository,
    private val preferences: HostCollectionPreferences,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        require(modelClass.isAssignableFrom(MarketViewModel::class.java)) {
            "Unknown ViewModel class: ${modelClass.name}"
        }
        return MarketViewModel(repository, preferences) as T
    }
}
