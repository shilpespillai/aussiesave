package com.example.aussiesaver.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "shopping_baskets")
data class ShoppingBasketEntity(
    @PrimaryKey val id: String,
    val name: String,
    val createdAt: Long
)
