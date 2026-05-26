package com.example.aussiesaver.data.local.db

import androidx.room.Database
import androidx.room.RoomDatabase
import com.example.aussiesaver.data.local.dao.BasketDao
import com.example.aussiesaver.data.local.dao.ProductDao
import com.example.aussiesaver.data.local.dao.StoreDao
import com.example.aussiesaver.data.local.entity.BasketItemEntity
import com.example.aussiesaver.data.local.entity.PriceHistoryEntity
import com.example.aussiesaver.data.local.entity.ProductEntity
import com.example.aussiesaver.data.local.entity.ShoppingBasketEntity
import com.example.aussiesaver.data.local.entity.StorePriceEntity
import com.example.aussiesaver.data.local.entity.SupermarketEntity

@Database(
    entities = [
        ProductEntity::class,
        SupermarketEntity::class,
        StorePriceEntity::class,
        PriceHistoryEntity::class,
        ShoppingBasketEntity::class,
        BasketItemEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class AussieSaverDatabase : RoomDatabase() {
    abstract fun productDao(): ProductDao
    abstract fun storeDao(): StoreDao
    abstract fun basketDao(): BasketDao
}
