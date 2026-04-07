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
import com.joaquim.minos.ui.MarketViewModel
import com.joaquim.minos.ui.QuoteUiState
import com.joaquim.minos.ui.toPercentDisplay
import com.joaquim.minos.ui.toUsdDisplay
import com.joaquim.minos.ui.toUsdDisplayOrDash

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
            when (val state = uiState.quoteState) {
                is QuoteUiState.Loading -> {
                    Text(
                        if (state.recoveryMode) {
                            "Reconnecting to CoinGecko..."
                        } else {
                            "Loading selected coin..."
                        },
                    )
                }

                is QuoteUiState.Loaded -> {
                    Text("${state.snapshot.symbol} ${state.snapshot.lastPrice.toUsdDisplay()}")
                    Text("24h ${state.snapshot.priceChangePercent24h.toPercentDisplay()}")
                    Text("High ${state.snapshot.highPrice24h.toUsdDisplayOrDash()}")
                    Text("Low ${state.snapshot.lowPrice24h.toUsdDisplayOrDash()}")
                }
            }
        }
    }
}
