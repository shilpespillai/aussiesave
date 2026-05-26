package com.example.aussiesaver.data.local.entity

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "basket_items",
    foreignKeys = [
        ForeignKey(
            entity = ShoppingBasketEntity::class,
            parentColumns = ["id"],
            childColumns = ["basketId"],
            onDelete = ForeignKey.CASCADE
        ),
        ForeignKey(
            entity = ProductEntity::class,
            parentColumns = ["id"],
            childColumns = ["productId"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [
        Index(value = ["basketId"]),
        Index(value = ["productId"])
    ]
)
data class BasketItemEntity(
    @PrimaryKey val id: String,
    val basketId: String,
    val productId: String,
    val quantity: Int
)
