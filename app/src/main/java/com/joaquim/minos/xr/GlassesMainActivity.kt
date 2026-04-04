package com.joaquim.minos.xr

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.remember
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.xr.glimmer.GlimmerTheme
import com.joaquim.minos.data.BinanceApiClient
import com.joaquim.minos.data.BinanceMarketRepository
import com.joaquim.minos.ui.MarketViewModel
import com.joaquim.minos.ui.MarketViewModelFactory

class GlassesMainActivity : ComponentActivity() {
    private val logTag = "MinosGlassesActivity"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d(logTag, "onCreate: projected glasses activity created")

        setContent {
            val repository = remember {
                BinanceMarketRepository(
                    apiClient = BinanceApiClient(),
                )
            }
            val factory = remember { MarketViewModelFactory(repository) }
            val viewModel: MarketViewModel = viewModel(factory = factory)

            GlimmerTheme {
                GlassesHomeScreen(
                    viewModel = viewModel,
                    onClose = {
                        Log.d(logTag, "onClose: finishing projected glasses activity")
                        finish()
                    },
                )
            }
        }
    }
}
