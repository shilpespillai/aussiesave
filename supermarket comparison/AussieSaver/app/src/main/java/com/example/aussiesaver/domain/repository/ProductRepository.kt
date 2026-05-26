package com.example.aussiesaver.domain.repository

import com.example.aussiesaver.data.local.entity.BasketItemEntity
import com.example.aussiesaver.data.local.entity.ProductEntity
import com.example.aussiesaver.data.local.entity.ShoppingBasketEntity
import com.example.aussiesaver.data.local.entity.StorePriceEntity
import com.example.aussiesaver.data.local.entity.SupermarketEntity
import kotlinx.coroutines.flow.Flow

interface ProductRepository {
    fun searchProducts(query: String): Flow<List<ProductEntity>>
    suspend fun getProductById(productId: String): ProductEntity?
    fun getPricesForProduct(productId: String): Flow<List<StorePriceEntity>>
    fun getAllStores(): Flow<List<SupermarketEntity>>
    fun getAllBaskets(): Flow<List<ShoppingBasketEntity>>
    suspend fun createBasket(basketName: String)
    suspend fun addProductToBasket(basketId: String, productId: String, quantity: Int)
    fun getItemsInBasket(basketId: String): Flow<List<BasketItemEntity>>
    suspend fun syncRemoteData()
}
