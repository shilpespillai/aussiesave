package com.example.aussiesaver.domain.usecase

import com.example.aussiesaver.data.local.entity.ProductEntity
import com.example.aussiesaver.data.local.entity.StorePriceEntity
import com.example.aussiesaver.domain.repository.ProductRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.flow
import javax.inject.Inject

data class ProductSearchResult(
    val product: ProductEntity,
    val prices: List<StorePriceEntity>,
    val cheapestPrice: Double?,
    val cheapestStoreName: String?
)

class SearchProductsUseCase @Inject constructor(
    private val repository: ProductRepository
) {
    operator fun invoke(query: String): Flow<List<ProductSearchResult>> = flow {
        repository.searchProducts(query).collect { products ->
            val results = products.map { product ->
                val prices = repository.getPricesForProduct(product.id).first()
                val cheapestPrice = prices.minOfOrNull { it.currentPrice }
                val cheapestStore = prices.find { it.currentPrice == cheapestPrice }?.let { priceEntity ->
                    val stores = repository.getAllStores().first()
                    stores.find { it.id == priceEntity.storeId }?.brandName
                }
                ProductSearchResult(product, prices, cheapestPrice, cheapestStore)
            }
            emit(results)
        }
    }
}
