package com.example.aussiesaver.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "normalized_products")
data class ProductEntity(
    @PrimaryKey val id: String,
    val barcode: String,
    val name: String,
    val category: String,
    val brand: String,
    val imageUrl: String,
    val standardSize: Double,
    val unitType: String
)
