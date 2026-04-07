package com.joaquim.minos.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.requiredHeightIn
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowForward
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Home
import androidx.compose.material.icons.rounded.Search
import androidx.compose.material.icons.rounded.Tune
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.BasicAlertDialog
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.joaquim.minos.model.MarketSnapshot
import com.joaquim.minos.xr.XrExperienceMode

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MinosApp(
    viewModel: MarketViewModel,
    xrExperienceMode: XrExperienceMode,
    xrLaunchStatus: XrLaunchStatus,
    onLaunchProjectedGlasses: () -> Unit,
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val previewState = uiState.previewState

    if (previewState != null) {
        CoinPreviewBottomSheet(
            previewState = previewState,
            pricesVisible = uiState.quoteState is QuoteUiState.Loaded,
            onAddCoin = viewModel::addPreviewCoin,
            onDismiss = viewModel::dismissPreview,
        )
    }

    Scaffold(
        containerColor = Color(0xFFF7F4F1),
        contentWindowInsets = WindowInsets.safeDrawing,
    ) { innerPadding ->
        Surface(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .windowInsetsPadding(WindowInsets.safeDrawing),
            color = Color(0xFFF7F4F1),
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 20.dp, vertical = 16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                HomeHeader(
                    onShowCatalog = viewModel::showCatalog,
                )
                SearchField(
                    query = uiState.searchQuery,
                    onQueryChange = viewModel::updateSearchQuery,
                    onOpenCatalog = viewModel::showCatalog,
                    onCloseCatalog = viewModel::hideCatalog,
                    isCatalogVisible = uiState.isCatalogVisible,
                )

                if (uiState.isCatalogVisible || uiState.searchQuery.isNotBlank()) {
                    CoinCatalogList(
                        uiState = uiState,
                        onCoinClick = viewModel::previewCoin,
                    )
                } else {
                    CollectionStack(
                        uiState = uiState,
                        onCoinClick = { coin -> viewModel.selectCoinFromCollection(coin.id) },
                    )
                }

                CompactXrLaunch(
                    xrExperienceMode = xrExperienceMode,
                    xrLaunchStatus = xrLaunchStatus,
                    onLaunchProjectedGlasses = onLaunchProjectedGlasses,
                )

                BottomNavigationMock()
            }
        }
    }
}

@Composable
private fun HomeHeader(
    onShowCatalog: () -> Unit,
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(
            text = "My collections",
            style = MaterialTheme.typography.headlineLarge,
            fontWeight = FontWeight.Medium,
            color = Color(0xFF1A1815),
        )
        IconButton(
            onClick = onShowCatalog,
            modifier = Modifier
                .size(44.dp)
                .background(Color.White, CircleShape),
        ) {
            Icon(
                imageVector = Icons.Rounded.Add,
                contentDescription = "Add coin",
                tint = Color(0xFF1A1815),
            )
        }
    }
}

@Composable
private fun SearchField(
    query: String,
    onQueryChange: (String) -> Unit,
    onOpenCatalog: () -> Unit,
    onCloseCatalog: () -> Unit,
    isCatalogVisible: Boolean,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color(0xFFEDEAE5), RoundedCornerShape(28.dp))
            .padding(horizontal = 14.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Row(
            modifier = Modifier
                .weight(1f)
                .clickable {
                    if (!isCatalogVisible) {
                        onOpenCatalog()
                    }
                }
                .padding(vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Icon(
                imageVector = Icons.Rounded.Search,
                contentDescription = null,
                tint = Color(0xFF8A847B),
            )
            androidx.compose.foundation.text.BasicTextField(
                value = query,
                onValueChange = {
                    if (!isCatalogVisible) {
                        onOpenCatalog()
                    }
                    onQueryChange(it)
                },
                singleLine = true,
                textStyle = MaterialTheme.typography.bodyLarge.copy(color = Color(0xFF1A1815)),
                modifier = Modifier.fillMaxWidth(),
                decorationBox = { innerTextField ->
                    if (query.isBlank()) {
                        Text(
                            text = "Search",
                            style = MaterialTheme.typography.bodyLarge,
                            color = Color(0xFF8A847B),
                        )
                    }
                    innerTextField()
                },
            )
        }

        if (isCatalogVisible) {
            IconButton(onClick = onCloseCatalog) {
                Icon(Icons.Rounded.Close, contentDescription = "Close list", tint = Color(0xFF534F49))
            }
        }
        Icon(
            imageVector = Icons.Rounded.Tune,
            contentDescription = null,
            tint = Color(0xFF534F49),
        )
    }
}

@Composable
private fun CoinCatalogList(
    uiState: MarketUiState,
    onCoinClick: (MarketSnapshot) -> Unit,
) {
    val pricesVisible = uiState.quoteState is QuoteUiState.Loaded

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .requiredHeightIn(max = 560.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(28.dp),
    ) {
        LazyColumn(
            modifier = Modifier.fillMaxWidth(),
            contentPadding = PaddingValues(vertical = 8.dp),
        ) {
            itemsIndexed(uiState.filteredCatalog, key = { _, coin -> coin.id }) { index, coin ->
                CoinCatalogRow(
                    coin = coin,
                    pricesVisible = pricesVisible,
                    onClick = { onCoinClick(coin) },
                )
                if (index < uiState.filteredCatalog.lastIndex) {
                    HorizontalDivider(
                        modifier = Modifier.padding(horizontal = 18.dp),
                        color = Color(0xFFF0ECE6),
                    )
                }
            }
        }
    }
}

@Composable
private fun CoinCatalogRow(
    coin: MarketSnapshot,
    pricesVisible: Boolean,
    onClick: () -> Unit,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(horizontal = 18.dp, vertical = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(14.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        AsyncImage(
            model = coin.imageUrl,
            contentDescription = coin.name,
            modifier = Modifier
                .size(42.dp)
                .clip(CircleShape),
        )
        Column(
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(2.dp),
        ) {
            Text(
                text = coin.name,
                style = MaterialTheme.typography.titleMedium,
                color = Color(0xFF191714),
            )
            Text(
                text = coin.symbol,
                style = MaterialTheme.typography.bodySmall,
                color = Color(0xFF79736A),
            )
        }
        if (pricesVisible) {
            Text(
                text = coin.lastPrice.toUsdDisplay(),
                style = MaterialTheme.typography.titleSmall,
                color = Color(0xFF191714),
                fontWeight = FontWeight.SemiBold,
            )
        } else {
            CircularProgressIndicator(
                modifier = Modifier.size(18.dp),
                strokeWidth = 2.dp,
            )
        }
    }
}

@Composable
private fun CollectionStack(
    uiState: MarketUiState,
    onCoinClick: (MarketSnapshot) -> Unit,
) {
    val collectionCoins = uiState.collectionCoins
    val pricesVisible = uiState.quoteState is QuoteUiState.Loaded

    if (collectionCoins.isEmpty()) {
        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(34.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
        ) {
            Column(
                modifier = Modifier.padding(24.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                Text(
                    text = "Start your collection",
                    style = MaterialTheme.typography.headlineSmall,
                    color = Color(0xFF1A1815),
                )
                Text(
                    text = "Search the top market-cap coins, preview the summary, and add the ones you want on glasses.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = Color(0xFF726C63),
                )
            }
        }
        return
    }

    LazyColumn(
        modifier = Modifier
            .fillMaxWidth()
            .requiredHeightIn(max = 610.dp),
        contentPadding = PaddingValues(bottom = 18.dp),
        verticalArrangement = Arrangement.spacedBy((-32).dp),
    ) {
        itemsIndexed(collectionCoins, key = { _, coin -> coin.id }) { _, coin ->
            CollectionCard(
                coin = coin,
                selected = coin.id == uiState.selectedCoinId,
                pricesVisible = pricesVisible,
                onClick = { onCoinClick(coin) },
            )
        }
    }
}

@Composable
private fun CollectionCard(
    coin: MarketSnapshot,
    selected: Boolean,
    pricesVisible: Boolean,
    onClick: () -> Unit,
) {
    val palette = coinPaletteFor(coin.id)
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(30.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = if (selected) 6.dp else 0.dp),
        colors = CardDefaults.cardColors(containerColor = palette.card),
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp, vertical = 22.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.Top,
                ) {
                    Text(
                        text = coin.name,
                        style = MaterialTheme.typography.headlineMedium,
                        color = palette.text,
                        fontWeight = FontWeight.Medium,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                    )
                    Text(
                        text = coin.priceChangePercent24h.toPercentDisplay(),
                        style = MaterialTheme.typography.bodyMedium,
                        color = palette.text.copy(alpha = 0.72f),
                        fontWeight = FontWeight.SemiBold,
                    )
                }

                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    CardPill(
                        text = coin.symbol,
                        background = palette.pill,
                        contentColor = palette.pillText,
                    )
                    if (pricesVisible) {
                        CardPill(
                            text = coin.lastPrice.toUsdDisplay(),
                            background = palette.pill,
                            contentColor = palette.pillText,
                        )
                    } else {
                        LoadingPill(
                            background = palette.pill,
                            contentColor = palette.pillText,
                        )
                    }
                }
            }

            Box(
                modifier = Modifier
                    .padding(start = 14.dp)
                    .size(42.dp)
                    .background(Color(0xFF32302D), CircleShape),
                contentAlignment = Alignment.Center,
            ) {
                Icon(
                    imageVector = Icons.AutoMirrored.Rounded.ArrowForward,
                    contentDescription = null,
                    tint = Color.White,
                )
            }
        }
    }
}

@Composable
private fun CardPill(
    text: String,
    background: Color,
    contentColor: Color,
) {
    Box(
        modifier = Modifier
            .background(background, RoundedCornerShape(999.dp))
            .padding(horizontal = 12.dp, vertical = 7.dp),
    ) {
        Text(
            text = text,
            color = contentColor,
            style = MaterialTheme.typography.labelLarge,
        )
    }
}

@Composable
private fun LoadingPill(
    background: Color,
    contentColor: Color,
) {
    Row(
        modifier = Modifier
            .background(background, RoundedCornerShape(999.dp))
            .padding(horizontal = 12.dp, vertical = 7.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        CircularProgressIndicator(
            modifier = Modifier.size(14.dp),
            strokeWidth = 2.dp,
            color = contentColor,
        )
        Text(
            text = "Loading",
            color = contentColor,
            style = MaterialTheme.typography.labelLarge,
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun CoinPreviewBottomSheet(
    previewState: CoinPreviewState,
    pricesVisible: Boolean,
    onAddCoin: () -> Unit,
    onDismiss: () -> Unit,
) {
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        containerColor = Color(0xFFFFFCF8),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 22.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(14.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                AsyncImage(
                    model = previewState.coin.imageUrl,
                    contentDescription = previewState.coin.name,
                    modifier = Modifier
                        .size(50.dp)
                        .clip(CircleShape),
                )
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = previewState.coin.name,
                        style = MaterialTheme.typography.headlineSmall,
                        color = Color(0xFF191714),
                    )
                    Text(
                        text = previewState.coin.symbol,
                        style = MaterialTheme.typography.bodyMedium,
                        color = Color(0xFF726C63),
                    )
                }
                if (pricesVisible) {
                    Text(
                        text = previewState.coin.lastPrice.toUsdDisplay(),
                        style = MaterialTheme.typography.titleLarge,
                        color = Color(0xFF191714),
                        fontWeight = FontWeight.SemiBold,
                    )
                } else {
                    CircularProgressIndicator(
                        modifier = Modifier.size(22.dp),
                        strokeWidth = 2.dp,
                    )
                }
            }

            Text(
                text = when (previewState) {
                    is CoinPreviewState.Loading -> "Loading summary..."
                    is CoinPreviewState.Loaded -> previewState.summary
                    is CoinPreviewState.Error -> previewState.message
                },
                style = MaterialTheme.typography.bodyLarge,
                color = Color(0xFF4B463F),
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                TextButton(
                    onClick = onDismiss,
                    modifier = Modifier.weight(1f),
                ) {
                    Text("Close")
                }
                Button(
                    onClick = onAddCoin,
                    modifier = Modifier.weight(1f),
                ) {
                    Text("Add coin")
                }
            }

            Spacer(modifier = Modifier.height(20.dp))
        }
    }
}

@Composable
private fun CompactXrLaunch(
    xrExperienceMode: XrExperienceMode,
    xrLaunchStatus: XrLaunchStatus,
    onLaunchProjectedGlasses: () -> Unit,
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(
            text = when (xrExperienceMode) {
                XrExperienceMode.StandardAndroid -> "Android host"
                XrExperienceMode.ProjectedAiGlasses -> "AI glasses"
            },
            style = MaterialTheme.typography.bodyMedium,
            color = if (xrLaunchStatus is XrLaunchStatus.Blocked) Color(0xFFBF4B4B) else Color(0xFF726C63),
        )
        TextButton(onClick = onLaunchProjectedGlasses) {
            Text(
                text = "Launch",
                color = Color(0xFF1A1815),
            )
        }
    }
}

@Composable
private fun BottomNavigationMock() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color.White, RoundedCornerShape(26.dp))
            .padding(horizontal = 18.dp, vertical = 10.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        BottomNavItem(icon = Icons.Rounded.Search, label = "Search", selected = false)
        BottomNavItem(icon = Icons.Rounded.Add, label = "Library", selected = false)
        BottomNavItem(icon = Icons.Rounded.Home, label = "Home", selected = true)
        BottomNavItem(icon = Icons.Rounded.Tune, label = "Chat", selected = false)
        BottomNavItem(icon = Icons.Rounded.Close, label = "Profile", selected = false)
    }
}

@Composable
private fun BottomNavItem(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    label: String,
    selected: Boolean,
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = if (selected) Color(0xFF1A1815) else Color(0xFF8A847B),
            modifier = Modifier.size(20.dp),
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall,
            color = if (selected) Color(0xFF1A1815) else Color(0xFF8A847B),
        )
    }
}

private fun xrLaunchStatusMessage(xrLaunchStatus: XrLaunchStatus): String {
    return when (xrLaunchStatus) {
        XrLaunchStatus.Ready -> "Host path ready. If projection fails, the current blocker is XR pairing/runtime."
        XrLaunchStatus.Launching -> "Requesting projected launch..."
        is XrLaunchStatus.Blocked -> xrLaunchStatus.message
        is XrLaunchStatus.Requested -> xrLaunchStatus.message
    }
}
