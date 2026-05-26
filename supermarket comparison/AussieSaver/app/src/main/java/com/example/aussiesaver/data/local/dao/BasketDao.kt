package com.example.aussiesaver.data.local.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.example.aussiesaver.data.local.entity.BasketItemEntity
import com.example.aussiesaver.data.local.entity.ShoppingBasketEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface BasketDao {
    @Query("SELECT * FROM shopping_baskets")
    fun getAllBaskets(): Flow<List<ShoppingBasketEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertBasket(basket: ShoppingBasketEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertBasketItems(items: List<BasketItemEntity>)

    @Query("SELECT * FROM basket_items WHERE basketId = :basketId")
    fun getItemsInBasket(basketId: String): Flow<List<BasketItemEntity>>

    @Delete
    suspend fun deleteBasketItem(item: BasketItemEntity)
}
