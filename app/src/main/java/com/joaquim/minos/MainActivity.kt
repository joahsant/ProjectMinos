package com.joaquim.minos

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.xr.projected.experimental.ExperimentalProjectedApi
import com.joaquim.minos.data.CoinGeckoApiClient
import com.joaquim.minos.data.CoinGeckoMarketRepository
import com.joaquim.minos.data.HostCollectionPreferences
import com.joaquim.minos.ui.MarketViewModel
import com.joaquim.minos.ui.MarketViewModelFactory
import com.joaquim.minos.ui.MinosApp
import com.joaquim.minos.ui.XrLaunchStatus
import com.joaquim.minos.ui.theme.ProjectMinosTheme
import com.joaquim.minos.xr.GlassesMainActivity
import com.joaquim.minos.xr.GlassesCoreDebugLauncher
import androidx.xr.projected.ProjectedContext
import com.joaquim.minos.xr.XrRuntime

@OptIn(ExperimentalProjectedApi::class)
class MainActivity : ComponentActivity() {
    private val logTag = "MinosMainActivity"
    private val xrLaunchStatus = mutableStateOf<XrLaunchStatus>(XrLaunchStatus.Ready)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d(logTag, "onCreate: starting host activity")
        enableEdgeToEdge()

        setContent {
            val xrRuntime = remember { XrRuntime() }
            val repository = remember {
                CoinGeckoMarketRepository(
                    apiClient = CoinGeckoApiClient(),
                )
            }
            val preferences = remember { HostCollectionPreferences(applicationContext) }
            val factory = remember { MarketViewModelFactory(repository, preferences) }
            val viewModel: MarketViewModel = viewModel(factory = factory)

            ProjectMinosTheme {
                MinosApp(
                    viewModel = viewModel,
                    xrExperienceMode = xrRuntime.resolveExperienceMode(),
                    xrLaunchStatus = xrLaunchStatus.value,
                    onLaunchProjectedGlasses = { launchProjectedGlassesSafely() },
                )
            }
        }
    }

    private fun launchProjectedGlassesSafely() {
        xrLaunchStatus.value = XrLaunchStatus.Launching
        try {
            Log.d(logTag, "onLaunchProjectedGlasses: creating projected options")
            val intent = Intent(this, GlassesMainActivity::class.java)
            val options = ProjectedContext.createProjectedActivityOptions(this)
            Log.d(logTag, "onLaunchProjectedGlasses: starting GlassesMainActivity")
            startActivity(intent, options.toBundle())
            xrLaunchStatus.value = XrLaunchStatus.Requested(
                "Projected launch requested. If nothing appears, the XR runtime is still blocked.",
            )
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
                xrLaunchStatus.value = XrLaunchStatus.Requested(
                    "Launch request sent through Glasses Core. Pairing may still be incomplete.",
                )
                runOnUiThread {
                    Toast.makeText(
                        this,
                        "Projected launch sent through glasses core.",
                        Toast.LENGTH_SHORT,
                    ).show()
                }
            }.onFailure { error ->
                Log.e(logTag, "launchThroughGlassesCoreFallback: failed", error)
                xrLaunchStatus.value = XrLaunchStatus.Blocked(
                    "Pairing incomplete. The host app is ready, but the projected device is unavailable.",
                )
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
