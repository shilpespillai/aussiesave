package com.example.aussiesaver.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "supermarkets")
data class SupermarketEntity(
    @PrimaryKey val id: String,
    val brandName: String,
    val branchName: String,
    val latitude: Double,
    val longitude: Double,
    val openingHours: String
)
