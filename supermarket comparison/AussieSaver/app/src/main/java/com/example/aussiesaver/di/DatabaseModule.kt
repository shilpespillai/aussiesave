package com.example.aussiesaver.di

import android.content.Context
import androidx.room.Room
import com.example.aussiesaver.data.local.dao.BasketDao
import com.example.aussiesaver.data.local.dao.ProductDao
import com.example.aussiesaver.data.local.dao.StoreDao
import com.example.aussiesaver.data.local.db.AussieSaverDatabase
import com.example.aussiesaver.data.repository.ProductRepositoryImpl
import com.example.aussiesaver.domain.repository.ProductRepository
import dagger.Binds
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
abstract class DatabaseModule {

    @Binds
    @Singleton
    abstract fun bindProductRepository(
        productRepositoryImpl: ProductRepositoryImpl
    ): ProductRepository

    companion object {
        @Provides
        @Singleton
        fun provideDatabase(
            @ApplicationContext context: Context
        ): AussieSaverDatabase {
            return Room.databaseBuilder(
                context,
                AussieSaverDatabase::class.java,
                "aussiesaver_db"
            ).build()
        }

        @Provides
        fun provideProductDao(db: AussieSaverDatabase): ProductDao = db.productDao()

        @Provides
        fun provideStoreDao(db: AussieSaverDatabase): StoreDao = db.storeDao()

        @Provides
        fun provideBasketDao(db: AussieSaverDatabase): BasketDao = db.basketDao()
    }
}
