package com.joaquim.minos.xr

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.xr.glimmer.Button
import androidx.xr.glimmer.Card
import androidx.xr.glimmer.Text
import androidx.xr.glimmer.surface
import com.joaquim.minos.ui.MarketUiState
import com.joaquim.minos.ui.MarketViewModel
import com.joaquim.minos.ui.toPercentDisplay
import com.joaquim.minos.ui.toUsdtDisplay

@Composable
fun GlassesHomeScreen(
    viewModel: MarketViewModel,
    onClose: () -> Unit,
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Box(
        modifier = Modifier
            .surface(focusable = false)
            .fillMaxSize(),
        contentAlignment = Alignment.Center,
    ) {
        Card(
            title = { Text("Project Minos") },
            action = {
                Button(onClick = onClose) {
                    Text("Close")
                }
            },
        ) {
            when (val state = uiState) {
                is MarketUiState.Loading -> {
                    Text(
                        if (state.recoveryMode) {
                            "Reconnecting to Binance..."
                        } else {
                            "Loading BTC/USDT..."
                        },
                    )
                }

                is MarketUiState.Loaded -> {
                    Text("BTC/USDT ${state.snapshot.lastPrice.toUsdtDisplay()}")
                    Text("24h ${state.snapshot.priceChangePercent24h.toPercentDisplay()}")
                    Text("High ${state.snapshot.highPrice24h.toUsdtDisplay()}")
                    Text("Low ${state.snapshot.lowPrice24h.toUsdtDisplay()}")
                }
            }
        }
    }
}
