package com.example.aussiesaver.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Transaction
import com.example.aussiesaver.data.local.entity.ProductEntity
import com.example.aussiesaver.data.local.entity.StorePriceEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ProductDao {
    @Query("SELECT * FROM normalized_products WHERE name LIKE :query OR brand LIKE :query")
    fun searchProducts(query: String): Flow<List<ProductEntity>>

    @Query("SELECT * FROM normalized_products WHERE id = :productId")
    suspend fun getProductById(productId: String): ProductEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertProducts(products: List<ProductEntity>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPrices(prices: List<StorePriceEntity>)

    @Query("SELECT * FROM store_product_prices WHERE productId = :productId")
    fun getPricesForProduct(productId: String): Flow<List<StorePriceEntity>>
}
