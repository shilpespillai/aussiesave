package com.example.aussiesaver.domain.usecase

import com.example.aussiesaver.data.local.entity.BasketItemEntity
import com.example.aussiesaver.data.local.entity.StorePriceEntity
import com.example.aussiesaver.domain.repository.ProductRepository
import kotlinx.coroutines.flow.first
import javax.inject.Inject

data class StoreTotal(
    val storeId: String,
    val storeName: String,
    val totalCost: Double,
    val missingItemsCount: Int
)

data class SplitShopItem(
    val productId: String,
    val productName: String,
    val storeId: String,
    val storeName: String,
    val price: Double,
    val quantity: Int
)

data class BasketOptimizationResult(
    val singleStoreTotals: List<StoreTotal>,
    val splitShopItems: List<SplitShopItem>,
    val splitShopTotal: Double,
    val potentialSavings: Double
)

class GetBasketOptimizationUseCase @Inject constructor(
    private val repository: ProductRepository
) {
    suspend fun invoke(basketId: String): BasketOptimizationResult {
        val items = repository.getItemsInBasket(basketId).first()
        val stores = repository.getAllStores().first()
        
        // Calculate costs per store
        val storeTotals = stores.map { store ->
            var total = 0.0
            var missing = 0
            for (item in items) {
                val prices = repository.getPricesForProduct(item.productId).first()
                val price = prices.find { it.storeId == store.id }
                if (price != null) {
                    total += price.currentPrice * item.quantity
                } else {
                    missing++
                }
            }
            StoreTotal(store.id, store.brandName + " (" + store.branchName + ")", total, missing)
        }.sortedBy { it.totalCost }

        // Calculate split shop configuration (choose absolute cheapest for each item)
        val splitShopItems = mutableListOf<SplitShopItem>()
        var splitTotal = 0.0

        for (item in items) {
            val product = repository.getProductById(item.productId) ?: continue
            val prices = repository.getPricesForProduct(item.productId).first()
            val cheapestPriceEntity = prices.minByOrNull { it.currentPrice }
            
            if (cheapestPriceEntity != null) {
                val store = stores.find { it.id == cheapestPriceEntity.storeId }
                val storeName = store?.let { "${it.brandName} (${it.branchName})" } ?: "Unknown"
                
                splitShopItems.add(
                    SplitShopItem(
                        productId = item.productId,
                        productName = product.name,
                        storeId = cheapestPriceEntity.storeId,
                        storeName = storeName,
                        price = cheapestPriceEntity.currentPrice,
                        quantity = item.quantity
                    )
                )
                splitTotal += cheapestPriceEntity.currentPrice * item.quantity
            }
        }

        val cheapestSingleStore = storeTotals.filter { it.missingItemsCount == 0 }.minOfOrNull { it.totalCost }
        val savings = if (cheapestSingleStore != null) cheapestSingleStore - splitTotal else 0.0

        return BasketOptimizationResult(
            singleStoreTotals = storeTotals,
            splitShopItems = splitShopItems,
            splitShopTotal = splitTotal,
            potentialSavings = if (savings > 0) savings else 0.0
        )
    }
}
