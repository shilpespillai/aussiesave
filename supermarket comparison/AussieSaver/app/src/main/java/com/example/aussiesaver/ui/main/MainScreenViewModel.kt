package com.example.aussiesaver.ui.main

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.aussiesaver.data.local.entity.BasketItemEntity
import com.example.aussiesaver.data.local.entity.ProductEntity
import com.example.aussiesaver.data.local.entity.StorePriceEntity
import com.example.aussiesaver.data.local.entity.SupermarketEntity
import com.example.aussiesaver.domain.repository.ProductRepository
import com.example.aussiesaver.domain.usecase.BasketOptimizationResult
import com.example.aussiesaver.domain.usecase.GetBasketOptimizationUseCase
import com.example.aussiesaver.domain.usecase.ProductSearchResult
import com.example.aussiesaver.domain.usecase.SearchProductsUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

data class Message(val content: String, val isFromUser: Boolean)

data class MainScreenUiState(
    val products: List<ProductSearchResult> = emptyList(),
    val stores: List<SupermarketEntity> = emptyList(),
    val basketOptimization: BasketOptimizationResult? = null,
    val basketItems: List<BasketItemEntity> = emptyList(),
    val chatMessages: List<Message> = listOf(
        Message("G'day! I'm your AussieSaver assistant. Ask me to find the cheapest ingredients or compare local store specials!", false)
    ),
    val isLoading: Boolean = false,
    val searchResults: List<ProductSearchResult> = emptyList()
)

@HiltViewModel
class MainScreenViewModel @Inject constructor(
    private val repository: ProductRepository,
    private val searchProductsUseCase: SearchProductsUseCase,
    private val getBasketOptimizationUseCase: GetBasketOptimizationUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow(MainScreenUiState())
    val uiState: StateFlow<MainScreenUiState> = _uiState.asStateFlow()

    private val searchQuery = MutableStateFlow("")

    init {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            repository.syncRemoteData() // Seed local DB with Australian supermarket feeds
            
            // Fetch stores
            repository.getAllStores().collect { stores ->
                _uiState.value = _uiState.value.copy(stores = stores, isLoading = false)
            }
        }

        // Setup dynamic search results Flow
        viewModelScope.launch {
            searchQuery.flatMapLatest { query ->
                if (query.isBlank()) {
                    flowOf(emptyList())
                } else {
                    searchProductsUseCase(query)
                }
            }.collect { results ->
                _uiState.value = _uiState.value.copy(searchResults = results)
            }
        }

        // Keep basket items updated and re-run basket optimizer on change
        viewModelScope.launch {
            repository.getAllBaskets().collect { baskets ->
                val activeBasket = baskets.firstOrNull()
                if (activeBasket == null) {
                    repository.createBasket("My Shopping List")
                } else {
                    repository.getItemsInBasket(activeBasket.id).collect { items ->
                        val optimization = getBasketOptimizationUseCase.invoke(activeBasket.id)
                        _uiState.value = _uiState.value.copy(
                            basketItems = items,
                            basketOptimization = optimization
                        )
                    }
                }
            }
        }
    }

    fun onSearchQueryChanged(query: String) {
        searchQuery.value = query
    }

    fun addProductToBasket(productId: String) {
        viewModelScope.launch {
            repository.getAllBaskets().collect { baskets ->
                baskets.firstOrNull()?.let { basket ->
                    repository.addProductToBasket(basket.id, productId, 1)
                }
            }
        }
    }

    fun sendChatMessage(content: String) {
        val currentMessages = _uiState.value.chatMessages.toMutableList()
        currentMessages.add(Message(content, true))
        _uiState.value = _uiState.value.copy(chatMessages = currentMessages)

        viewModelScope.launch {
            val response = generateAiResponse(content)
            val updatedMessages = _uiState.value.chatMessages.toMutableList()
            updatedMessages.add(Message(response, false))
            _uiState.value = _uiState.value.copy(chatMessages = updatedMessages)
        }
    }

    private fun generateAiResponse(query: String): String {
        val q = query.lowercase()
        return when {
            q.contains("breakfast") || q.contains("brekkie") -> {
                "For a budget-friendly Aussie breakfast, go for Devondale Milk ($1.60 at ALDI) and Sunny Queen Free Range Eggs ($4.60 at ALDI). Total cost is only $6.20!"
            }
            q.contains("milk") -> {
                "Devondale Long Life Milk is cheapest at Costco ($1.45) and ALDI ($1.60). Woolies and Coles are selling it for $1.85."
            }
            q.contains("laundry") -> {
                "Dynamo Professional Laundry Liquid 1.8L is currently a hot special! Woolworths has it for $13.50 (down from $27.00 - Save $13.50). Coles is selling it for $20.00, while ALDI's equivalent laundry liquid is $12.00."
            }
            q.contains("bread") -> {
                "Wonder White Bread is on special at Woolies for $3.40 (down from $4.20). Coles is $3.90, and ALDI has their house brand bread from $2.80."
            }
            q.contains("family") || q.contains("feed") -> {
                "A weekly shopping run of milk, bread, and eggs for a family of 4 totals: ALDI ($9.00), Coles ($10.65), and Woolworths ($10.45). ALDI is your best bet this week!"
            }
            else -> "I recommend comparing home brand options at ALDI and looking out for half-price specials at Woolies and Coles for maximum savings."
        }
    }
}
