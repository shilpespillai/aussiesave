package com.example.aussiesaver.data.local.entity

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index

@Entity(
    tableName = "store_product_prices",
    primaryKeys = ["productId", "storeId"],
    foreignKeys = [
        ForeignKey(
            entity = ProductEntity::class,
            parentColumns = ["id"],
            childColumns = ["productId"],
            onDelete = ForeignKey.CASCADE
        ),
        ForeignKey(
            entity = SupermarketEntity::class,
            parentColumns = ["id"],
            childColumns = ["storeId"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [
        Index(value = ["productId"]),
        Index(value = ["storeId"])
    ]
)
data class StorePriceEntity(
    val productId: String,
    val storeId: String,
    val currentPrice: Double,
    val normalPrice: Double,
    val unitPrice: Double,
    val isPromo: Boolean,
    val promoDesc: String,
    val lastUpdated: Long
)
