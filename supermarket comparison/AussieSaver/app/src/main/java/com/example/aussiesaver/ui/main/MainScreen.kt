package com.example.aussiesaver.ui.main

import androidx.compose.animation.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation3.runtime.NavKey
import com.example.aussiesaver.data.local.entity.SupermarketEntity
import com.example.aussiesaver.domain.usecase.ProductSearchResult
import com.example.aussiesaver.theme.FreshMintGreen
import com.example.aussiesaver.theme.SoftMintContainer
import com.example.aussiesaver.theme.DuskNavy
import com.example.aussiesaver.theme.SoftNavyContainer
import com.example.aussiesaver.theme.GoldenWattle

// Premium Light-Green Theme Palette
private val BackgroundLight = Color(0xFFF6F8FA)
private val CardSurface = Color(0xFFFFFFFF)
private val BorderColor = Color(0xFFE2E8F0)
private val PrimaryMint = Color(0xFF00C853)
private val LightMintContainer = Color(0xFFE8F7F0)
private val NavyAccent = Color(0xFF0A1931)
private val WattleYellow = Color(0xFFFFD700)
private val TextDark = Color(0xFF1A202C)
private val TextMuted = Color(0xFF718096)
private val HeaderMint = Color(0xFF7BE3B6)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(
    onItemClick: (NavKey) -> Unit,
    modifier: Modifier = Modifier,
    viewModel: MainScreenViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var selectedTab by remember { mutableIntStateOf(0) }
    var activeDomain by remember { mutableStateOf("grocery") }

    Scaffold(
        bottomBar = {
            NavigationBar(
                containerColor = Color.White,
                tonalElevation = 8.dp,
                modifier = Modifier.height(72.dp)
            ) {
                NavigationBarItem(
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 },
                    icon = { Icon(Icons.Default.Home, contentDescription = "Home") },
                    label = { Text("Home", fontWeight = FontWeight.Bold, fontSize = 11.sp) },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color(0xFF0E5E3A),
                        selectedTextColor = Color(0xFF0E5E3A),
                        unselectedIconColor = TextMuted,
                        unselectedTextColor = TextMuted,
                        indicatorColor = Color(0xFFC8F2DD)
                    )
                )
                NavigationBarItem(
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 },
                    icon = { Icon(Icons.Default.Search, contentDescription = "Search") },
                    label = { Text("Search", fontWeight = FontWeight.Bold, fontSize = 11.sp) },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color(0xFF0E5E3A),
                        selectedTextColor = Color(0xFF0E5E3A),
                        unselectedIconColor = TextMuted,
                        unselectedTextColor = TextMuted,
                        indicatorColor = Color(0xFFC8F2DD)
                    )
                )
                NavigationBarItem(
                    selected = selectedTab == 2,
                    onClick = { selectedTab = 2 },
                    icon = { Icon(Icons.Default.ShoppingCart, contentDescription = "Basket") },
                    label = { Text("Basket", fontWeight = FontWeight.Bold, fontSize = 11.sp) },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color(0xFF0E5E3A),
                        selectedTextColor = Color(0xFF0E5E3A),
                        unselectedIconColor = TextMuted,
                        unselectedTextColor = TextMuted,
                        indicatorColor = Color(0xFFC8F2DD)
                    )
                )
                NavigationBarItem(
                    selected = selectedTab == 3,
                    onClick = { selectedTab = 3 },
                    icon = { Icon(Icons.Default.Face, contentDescription = "AI Assistant") },
                    label = { Text("AI Helper", fontWeight = FontWeight.Bold, fontSize = 11.sp) },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = Color(0xFF0E5E3A),
                        selectedTextColor = Color(0xFF0E5E3A),
                        unselectedIconColor = TextMuted,
                        unselectedTextColor = TextMuted,
                        indicatorColor = Color(0xFFC8F2DD)
                    )
                )
            }
        }
    ) { paddingValues ->
        Box(
            modifier = modifier
                .fillMaxSize()
                .padding(paddingValues)
                .background(BackgroundLight)
        ) {
            when (selectedTab) {
                0 -> DashboardTab(
                    state = uiState,
                    activeDomain = activeDomain,
                    onDomainChange = { activeDomain = it },
                    onSearchClick = { selectedTab = 1 },
                    viewModel = viewModel
                )
                1 -> SearchTab(uiState, viewModel)
                2 -> BasketTab(uiState, viewModel)
                3 -> ChatTab(uiState, viewModel)
            }
        }
    }
}

@Composable
fun DashboardTab(
    state: MainScreenUiState,
    activeDomain: String,
    onDomainChange: (String) -> Unit,
    onSearchClick: () -> Unit,
    viewModel: MainScreenViewModel
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Curvy Mint Green Header
        item {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(155.dp)
                    .background(
                        color = HeaderMint,
                        shape = RoundedCornerShape(bottomStart = 40.dp, bottomEnd = 40.dp)
                    )
                    .padding(horizontal = 20.dp, vertical = 16.dp)
            ) {
                Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = "Aussie",
                                color = Color(0xFF0E5E3A),
                                fontSize = 22.sp,
                                fontWeight = FontWeight.Black
                            )
                            Text(
                                text = "Saver",
                                color = NavyAccent,
                                fontSize = 22.sp,
                                fontWeight = FontWeight.Black
                            )
                        }
                        Box(
                            modifier = Modifier
                                .background(Color(0x33FFFFFF), RoundedCornerShape(10.dp))
                                .padding(horizontal = 10.dp, vertical = 5.dp)
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    imageVector = Icons.Default.LocationOn,
                                    contentDescription = null,
                                    tint = Color(0xFF0E5E3A),
                                    modifier = Modifier.size(13.dp)
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Text("Richmond Plaza", color = Color(0xFF0E5E3A), fontSize = 11.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }

                    // Domain selector
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color(0x1F0E5E3A), RoundedCornerShape(20.dp))
                            .padding(3.dp)
                    ) {
                        listOf(
                            Triple("grocery", "Grocery", Icons.Default.ShoppingCart),
                            Triple("utility", "Utilities", Icons.Default.Build),
                            Triple("insurance", "Insurance", Icons.Default.Lock)
                        ).forEach { (domainId, label, icon) ->
                            val isActive = activeDomain == domainId
                            Row(
                                modifier = Modifier
                                    .weight(1f)
                                    .clip(RoundedCornerShape(18.dp))
                                    .background(if (isActive) NavyAccent else Color.Transparent)
                                    .clickable { onDomainChange(domainId) }
                                    .padding(vertical = 6.dp),
                                horizontalArrangement = Arrangement.Center,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    imageVector = icon,
                                    contentDescription = label,
                                    tint = if (isActive) Color.White else Color(0xFF0E5E3A),
                                    modifier = Modifier.size(13.dp)
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(
                                    text = label,
                                    color = if (isActive) Color.White else Color(0xFF0E5E3A),
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    }
                }
            }
        }

        // Overlapping Savings Card Wrapper
        item {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 20.dp)
                    .offset(y = (-30).dp)
            ) {
                Column {
                    // Navy Card
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(24.dp),
                        colors = CardDefaults.cardColors(containerColor = NavyAccent)
                    ) {
                        Column(
                            modifier = Modifier
                                .padding(horizontal = 20.dp, vertical = 16.dp)
                                .padding(bottom = 36.dp)
                        ) {
                            Text(
                                text = "Hi, Liam!",
                                color = Color.White,
                                fontSize = 16.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Text(
                                text = if (activeDomain == "grocery") "Optimize your groceries today" else if (activeDomain == "utility") "Minimize your annual utility bills" else "Maximize your insurance discounts",
                                color = Color.White.copy(alpha = 0.75f),
                                fontSize = 12.sp
                            )
                        }
                    }

                    // Floating Overlapping Mint Savings Card
                    val savingsText = when(activeDomain) {
                        "grocery" -> "$142.50 Saved"
                        "utility" -> "$185.00 Saved"
                        else -> "$240.00 Saved"
                    }
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 12.dp)
                            .offset(y = (-24).dp),
                        shape = RoundedCornerShape(20.dp),
                        colors = CardDefaults.cardColors(containerColor = LightMintContainer),
                        border = androidx.compose.foundation.BorderStroke(1.dp, Color(0x3300C853))
                    ) {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(16.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                text = savingsText,
                                color = PrimaryMint,
                                fontSize = 28.sp,
                                fontWeight = FontWeight.ExtraBold
                            )
                            Text(
                                text = "Your savings this month",
                                color = Color(0xFF1A3E2B),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Box(
                                modifier = Modifier
                                    .width(180.dp)
                                    .height(6.dp)
                                    .background(Color(0x1F00C853), RoundedCornerShape(10.dp))
                            ) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxHeight()
                                        .fillMaxWidth(0.68f)
                                        .background(PrimaryMint, RoundedCornerShape(10.dp))
                                )
                            }
                        }
                    }
                }
            }
        }

        // Section Title: Deals
        item {
            Text(
                text = "Today's Biggest Deals",
                color = TextDark,
                fontSize = 16.sp,
                fontWeight = FontWeight.ExtraBold,
                modifier = Modifier
                    .padding(horizontal = 20.dp)
                    .offset(y = (-20).dp)
            )
        }

        // Populate deal comparison list card based on domain selection
        item {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 20.dp)
                    .offset(y = (-20).dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                if (activeDomain == "grocery") {
                    PremiumDealComparisonCard(
                        title = "Wonder White Sliced Bread 700g",
                        brand = "Wonder White",
                        badge = "Save 80c",
                        stores = listOf(
                            StoreRowData("Woolworths Richmond", 3.40, 4.20, true, "W", Color(0xFF377B2B)),
                            StoreRowData("Coles Richmond", 3.90, null, false, "C", Color(0xFFE01A22))
                        )
                    )
                    PremiumDealComparisonCard(
                        title = "Cadbury Dairy Milk Chocolate 180g",
                        brand = "Cadbury",
                        badge = "Half Price",
                        stores = listOf(
                            StoreRowData("Woolworths Richmond", 4.00, 8.00, true, "W", Color(0xFF377B2B)),
                            StoreRowData("Coles Richmond", 4.50, null, false, "C", Color(0xFFE01A22)),
                            StoreRowData("ALDI Richmond", 4.80, null, false, "A", Color(0xFF002C6C))
                        )
                    )
                } else if (activeDomain == "utility") {
                    PremiumDealComparisonCard(
                        title = "Standard Electricity Plan (Flat Rate)",
                        brand = "AGL Energy vs Origin",
                        badge = "Save $65/yr",
                        stores = listOf(
                            StoreRowData("AGL Energy Plan", 1420.00, 1485.00, true, "A", Color(0xFF6C5CE7)),
                            StoreRowData("Origin Basic Tariff", 1485.00, null, false, "O", Color(0xFF6C5CE7))
                        )
                    )
                } else {
                    PremiumDealComparisonCard(
                        title = "Comprehensive Car Insurance Policy",
                        brand = "NRMA vs Bupa",
                        badge = "Save $70/yr",
                        stores = listOf(
                            StoreRowData("NRMA Comprehensive", 850.00, 920.00, true, "N", Color(0xFFFD9644)),
                            StoreRowData("Bupa Standard Cover", 920.00, null, false, "B", Color(0xFFFD9644))
                        )
                    )
                }
            }
        }
    }
}

data class StoreRowData(
    val storeName: String,
    val price: Double,
    val originalPrice: Double?,
    val isBest: Boolean,
    val logoChar: String,
    val logoColor: Color
)

@Composable
fun PremiumDealComparisonCard(
    title: String,
    brand: String,
    badge: String,
    stores: List<StoreRowData>
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .border(1.dp, BorderColor, RoundedCornerShape(24.dp)),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = CardSurface)
    ) {
        Column(modifier = Modifier.padding(18.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Top
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = title,
                        color = TextDark,
                        fontSize = 15.sp,
                        fontWeight = FontWeight.ExtraBold,
                        lineHeight = 20.sp,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                    Text(
                        text = brand,
                        color = TextMuted,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(top = 2.dp)
                    )
                }
                Box(
                    modifier = Modifier
                        .background(Color(0xFFFFF9C4), RoundedCornerShape(10.dp))
                        .border(1.dp, Color(0x33F5B041), RoundedCornerShape(10.dp))
                        .padding(horizontal = 8.dp, vertical = 3.dp)
                ) {
                    Text(
                        text = badge,
                        color = Color(0xFF7E5109),
                        fontSize = 9.sp,
                        fontWeight = FontWeight.Black
                    )
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                stores.forEach { store ->
                    val borderModifier = if (store.isBest) {
                        Modifier.border(1.dp, Color(0x3300C853), RoundedCornerShape(12.dp))
                    } else Modifier

                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(if (store.isBest) LightMintContainer else Color(0xFFF8FAFC))
                            .then(borderModifier)
                            .padding(horizontal = 12.dp, vertical = 8.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(20.dp)
                                    .background(store.logoColor, CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = store.logoChar,
                                    color = Color.White,
                                    fontSize = 9.sp,
                                    fontWeight = FontWeight.Black
                                )
                            }
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = store.storeName,
                                color = TextDark,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            if (store.originalPrice != null) {
                                Text(
                                    text = "$${"%.2f".format(store.originalPrice)}",
                                    color = TextMuted,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Medium,
                                    style = LocalTextStyle.current.copy(textDecoration = androidx.compose.ui.text.style.TextDecoration.LineThrough),
                                    modifier = Modifier.padding(end = 6.dp)
                                )
                            }
                            Text(
                                text = "$${"%.2f".format(store.price)}",
                                color = if (store.isBest) Color(0xFF0E5E3A) else TextDark,
                                fontSize = 14.sp,
                                fontWeight = FontWeight.ExtraBold
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ChatTab(state: MainScreenUiState, viewModel: MainScreenViewModel) {
    var messageText by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text("AI Savings Assistant", fontWeight = FontWeight.Bold, fontSize = 22.sp, color = TextDark)
        Text("Compare catalogs and optimize recipes dynamically", fontSize = 13.sp, color = TextMuted)
        Spacer(modifier = Modifier.height(16.dp))

        LazyColumn(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            items(state.chatMessages) { message ->
                Box(
                    modifier = Modifier.fillMaxWidth(),
                    contentAlignment = if (message.isFromUser) Alignment.CenterEnd else Alignment.CenterStart
                ) {
                    Card(
                        shape = RoundedCornerShape(
                            topStart = 16.dp,
                            topEnd = 16.dp,
                            bottomStart = if (message.isFromUser) 16.dp else 4.dp,
                            bottomEnd = if (message.isFromUser) 4.dp else 16.dp
                        ),
                        colors = CardDefaults.cardColors(
                            containerColor = if (message.isFromUser) NavyAccent else CardSurface
                        ),
                        border = androidx.compose.foundation.BorderStroke(1.dp, BorderColor),
                        modifier = Modifier.widthIn(max = 280.dp)
                    ) {
                        Text(
                            text = message.content,
                            color = if (message.isFromUser) Color.White else TextDark,
                            modifier = Modifier.padding(12.dp),
                            fontSize = 14.sp
                        )
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(12.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = messageText,
                onValueChange = { messageText = it },
                placeholder = { Text("Ask about milk, specials, recipes...", color = TextMuted) },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = PrimaryMint,
                    unfocusedBorderColor = BorderColor,
                    focusedTextColor = TextDark,
                    unfocusedTextColor = TextDark,
                    focusedContainerColor = CardSurface,
                    unfocusedContainerColor = CardSurface
                ),
                shape = RoundedCornerShape(20.dp),
                modifier = Modifier.weight(1f)
            )
            Spacer(modifier = Modifier.width(8.dp))
            IconButton(
                onClick = {
                    if (messageText.isNotBlank()) {
                        viewModel.sendChatMessage(messageText)
                        messageText = ""
                    }
                },
                modifier = Modifier
                    .background(PrimaryMint, CircleShape)
                    .size(48.dp)
            ) {
                Icon(Icons.Default.Send, contentDescription = "Send", tint = Color.White)
            }
        }
    }
}

@Composable
fun SearchTab(state: MainScreenUiState, viewModel: MainScreenViewModel) {
    var query by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text("Product Search", fontWeight = FontWeight.Bold, fontSize = 22.sp, color = TextDark)
        Text("Compare supermarket prices side-by-side", fontSize = 13.sp, color = TextMuted)
        Spacer(modifier = Modifier.height(16.dp))

        OutlinedTextField(
            value = query,
            onValueChange = {
                query = it
                viewModel.onSearchQueryChanged(it)
            },
            modifier = Modifier.fillMaxWidth(),
            placeholder = { Text("Search milk, bread, eggs...", color = TextMuted) },
            leadingIcon = { Icon(Icons.Default.Search, contentDescription = null, tint = TextMuted) },
            singleLine = true,
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = PrimaryMint,
                unfocusedBorderColor = BorderColor,
                focusedTextColor = TextDark,
                unfocusedTextColor = TextDark,
                focusedContainerColor = CardSurface,
                unfocusedContainerColor = CardSurface
            ),
            shape = RoundedCornerShape(16.dp)
        )

        Spacer(modifier = Modifier.height(16.dp))

        if (state.searchResults.isEmpty() && query.isNotEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("No items found", color = TextMuted)
            }
        } else {
            LazyColumn(
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(state.searchResults) { result ->
                    ProductCompareRowCard(result) {
                        viewModel.addProductToBasket(result.product.id)
                    }
                }
            }
        }
    }
}

@Composable
fun ProductCompareRowCard(result: ProductSearchResult, onAddClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .border(1.dp, BorderColor, RoundedCornerShape(24.dp)),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = CardSurface)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Top
            ) {
                Column {
                    Text(
                        text = result.product.name,
                        fontWeight = FontWeight.Bold,
                        color = TextDark,
                        fontSize = 14.sp
                    )
                    Text(
                        text = "${result.product.brand} | ${result.product.standardSize} ${result.product.unitType}",
                        color = TextMuted,
                        fontSize = 12.sp
                    )
                }
                Box(
                    modifier = Modifier
                        .size(32.dp)
                        .background(Color(0x1A00C853), RoundedCornerShape(16.dp))
                        .clickable(onClick = onAddClick),
                    contentAlignment = Alignment.Center
                ) {
                    Text("+", color = PrimaryMint, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
            HorizontalDivider(color = BorderColor)
            Spacer(modifier = Modifier.height(12.dp))

            result.prices.sortedBy { it.currentPrice }.forEachIndexed { idx, price ->
                val isCheapest = idx == 0
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(
                            color = if (isCheapest) LightMintContainer else Color.Transparent,
                            shape = RoundedCornerShape(8.dp)
                        )
                        .padding(horizontal = 10.dp, vertical = 6.dp),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = if (price.storeId.contains("wool")) "Woolworths" else if (price.storeId.contains("coles")) "Coles" else if (price.storeId.contains("aldi")) "ALDI" else "Costco",
                        fontWeight = if (isCheapest) FontWeight.Bold else FontWeight.Medium,
                        color = if (isCheapest) Color(0xFF0E5E3A) else TextDark,
                        fontSize = 12.sp
                    )
                    Text(
                        text = "$${"%.2f".format(price.currentPrice)}",
                        fontWeight = FontWeight.Bold,
                        color = if (isCheapest) Color(0xFF0E5E3A) else TextDark,
                        fontSize = 12.sp
                    )
                }
            }
        }
    }
}

@Composable
fun BasketTab(state: MainScreenUiState, viewModel: MainScreenViewModel) {
    val opt = state.basketOptimization

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
        contentPadding = PaddingValues(bottom = 24.dp)
    ) {
        item {
            Text("Basket Optimizer", fontWeight = FontWeight.Bold, fontSize = 22.sp, color = TextDark)
            Text("Cheapest checkout builder", fontSize = 13.sp, color = TextMuted)
        }

        if (opt != null && opt.splitShopItems.isNotEmpty()) {
            item {
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .border(1.dp, Color(0x3300C853), RoundedCornerShape(24.dp)),
                    shape = RoundedCornerShape(24.dp),
                    colors = CardDefaults.cardColors(containerColor = LightMintContainer)
                ) {
                    Column(modifier = Modifier.padding(20.dp)) {
                        Text(
                            text = "Split Shop Recommendation",
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF0E5E3A),
                            fontSize = 15.sp
                        )
                        Text(
                            text = "Split your basket to unlock maximum savings:",
                            fontSize = 13.sp,
                            color = Color(0xFF1C3F2F),
                            modifier = Modifier.padding(bottom = 12.dp)
                        )
                        opt.splitShopItems.forEach { item ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 4.dp),
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Text(item.productName, fontSize = 13.sp, color = TextDark, maxLines = 1)
                                Text(
                                    text = "${item.storeName.substringBefore(" ")} - $${"%.2f".format(item.price)}",
                                    fontSize = 13.sp,
                                    color = Color(0xFF0E5E3A),
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                        HorizontalDivider(color = Color(0x3300C853))
                        Spacer(modifier = Modifier.height(10.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text("Total optimized cost:", color = TextDark, fontWeight = FontWeight.Bold)
                            Text(
                                text = "$${"%.2f".format(opt.splitShopTotal)}",
                                color = Color(0xFF0E5E3A),
                                fontWeight = FontWeight.Black,
                                fontSize = 16.sp
                            )
                        }
                    }
                }
            }

            item {
                Text("Single Store Totals", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = TextDark)
            }

            items(opt.singleStoreTotals) { total ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(CardSurface, RoundedCornerShape(14.dp))
                        .border(1.dp, BorderColor, RoundedCornerShape(14.dp))
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(total.storeName, fontSize = 14.sp, color = TextDark, fontWeight = FontWeight.Bold)
                    Text(
                        text = "$${"%.2f".format(total.totalCost)}",
                        fontWeight = FontWeight.Bold,
                        fontSize = 14.sp,
                        color = TextDark
                    )
                }
            }
        } else {
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 40.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text("Your basket is empty. Search items to begin saving!", color = TextMuted, fontSize = 14.sp)
                }
            }
        }
    }
}
