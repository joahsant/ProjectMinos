package com.joaquim.minos.xr

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.remember
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.xr.glimmer.GlimmerTheme
import com.joaquim.minos.data.CoinGeckoApiClient
import com.joaquim.minos.data.CoinGeckoMarketRepository
import com.joaquim.minos.data.HostCollectionPreferences
import com.joaquim.minos.ui.MarketViewModel
import com.joaquim.minos.ui.MarketViewModelFactory

class GlassesMainActivity : ComponentActivity() {
    private val logTag = "MinosGlassesActivity"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d(logTag, "onCreate: projected glasses activity created")

        setContent {
            val repository = remember {
                CoinGeckoMarketRepository(
                    apiClient = CoinGeckoApiClient(),
                )
            }
            val preferences = remember { HostCollectionPreferences(applicationContext) }
            val factory = remember { MarketViewModelFactory(repository, preferences) }
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
