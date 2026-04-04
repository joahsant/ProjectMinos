package com.joaquim.minos

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.remember
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.xr.projected.experimental.ExperimentalProjectedApi
import com.joaquim.minos.data.BinanceApiClient
import com.joaquim.minos.data.BinanceMarketRepository
import com.joaquim.minos.ui.MarketViewModel
import com.joaquim.minos.ui.MarketViewModelFactory
import com.joaquim.minos.ui.MinosApp
import com.joaquim.minos.ui.theme.ProjectMinosTheme
import com.joaquim.minos.xr.GlassesMainActivity
import com.joaquim.minos.xr.GlassesCoreDebugLauncher
import androidx.xr.projected.ProjectedContext
import com.joaquim.minos.xr.XrRuntime

@OptIn(ExperimentalProjectedApi::class)
class MainActivity : ComponentActivity() {
    private val logTag = "MinosMainActivity"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d(logTag, "onCreate: starting host activity")
        enableEdgeToEdge()

        setContent {
            val xrRuntime = remember { XrRuntime() }
            val repository = remember {
                BinanceMarketRepository(
                    apiClient = BinanceApiClient(),
                )
            }
            val factory = remember { MarketViewModelFactory(repository) }
            val viewModel: MarketViewModel = viewModel(factory = factory)

            ProjectMinosTheme {
                MinosApp(
                    viewModel = viewModel,
                    xrExperienceMode = xrRuntime.resolveExperienceMode(),
                    onLaunchProjectedGlasses = { launchProjectedGlassesSafely() },
                )
            }
        }
    }

    private fun launchProjectedGlassesSafely() {
        try {
            Log.d(logTag, "onLaunchProjectedGlasses: creating projected options")
            val intent = Intent(this, GlassesMainActivity::class.java)
            val options = ProjectedContext.createProjectedActivityOptions(this)
            Log.d(logTag, "onLaunchProjectedGlasses: starting GlassesMainActivity")
            startActivity(intent, options.toBundle())
        } catch (error: IllegalStateException) {
            Log.e(logTag, "onLaunchProjectedGlasses: projected device unavailable", error)
            launchThroughGlassesCoreFallback(error)
        }
    }

    private fun launchThroughGlassesCoreFallback(originalError: IllegalStateException) {
        Log.w(logTag, "launchThroughGlassesCoreFallback: trying glasses core binder route", originalError)
        GlassesCoreDebugLauncher.launch(
            context = this,
            targetActivity = GlassesMainActivity::class.java,
        ) { result ->
            result.onSuccess {
                Log.d(logTag, "launchThroughGlassesCoreFallback: launch request sent")
                runOnUiThread {
                    Toast.makeText(
                        this,
                        "Projected launch sent through glasses core.",
                        Toast.LENGTH_SHORT,
                    ).show()
                }
            }.onFailure { error ->
                Log.e(logTag, "launchThroughGlassesCoreFallback: failed", error)
                runOnUiThread {
                    Toast.makeText(
                        this,
                        "AI glasses not connected yet. Finish pairing and try again.",
                        Toast.LENGTH_LONG,
                    ).show()
                }
            }
        }
    }
}
