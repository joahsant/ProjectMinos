package com.joaquim.minos.ui

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.joaquim.minos.data.BinanceMarketRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class MarketViewModel(
    private val repository: BinanceMarketRepository,
) : ViewModel() {
    private val logTag = "MinosMarketViewModel"
    private val _uiState = MutableStateFlow<MarketUiState>(MarketUiState.Loading(recoveryMode = false))
    val uiState: StateFlow<MarketUiState> = _uiState.asStateFlow()

    init {
        observeMarket()
    }

    private fun observeMarket() {
        viewModelScope.launch {
            var hasLoadedSuccessfully = false

            while (true) {
                try {
                    val snapshot = repository.fetchBtcUsdtSnapshot()
                    Log.d(logTag, "observeMarket: snapshot loaded at ${snapshot.updatedAtMillis}")
                    _uiState.value = MarketUiState.Loaded(snapshot)
                    hasLoadedSuccessfully = true
                    delay(STEADY_STATE_REFRESH_MILLIS)
                } catch (error: Exception) {
                    Log.w(logTag, "observeMarket: snapshot load failed", error)
                    _uiState.value = MarketUiState.Loading(recoveryMode = hasLoadedSuccessfully)
                    delay(RETRY_REFRESH_MILLIS)
                }
            }
        }
    }

    companion object {
        private const val RETRY_REFRESH_MILLIS = 5_000L
        private const val STEADY_STATE_REFRESH_MILLIS = 60_000L
    }
}

class MarketViewModelFactory(
    private val repository: BinanceMarketRepository,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        require(modelClass.isAssignableFrom(MarketViewModel::class.java)) {
            "Unknown ViewModel class: ${modelClass.name}"
        }
        return MarketViewModel(repository) as T
    }
}
