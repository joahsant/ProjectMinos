package com.joaquim.minos.ui

import com.joaquim.minos.model.MarketSnapshot

sealed interface MarketUiState {
    data class Loading(
        val recoveryMode: Boolean,
    ) : MarketUiState

    data class Loaded(
        val snapshot: MarketSnapshot,
    ) : MarketUiState
}

