package com.example.aussiesaver.data.repository

import com.example.aussiesaver.data.local.dao.BasketDao
import com.example.aussiesaver.data.local.dao.ProductDao
import com.example.aussiesaver.data.local.dao.StoreDao
import com.example.aussiesaver.data.local.entity.BasketItemEntity
import com.example.aussiesaver.data.local.entity.ProductEntity
import com.example.aussiesaver.data.local.entity.ShoppingBasketEntity
import com.example.aussiesaver.data.local.entity.StorePriceEntity
import com.example.aussiesaver.data.local.entity.SupermarketEntity
import com.example.aussiesaver.domain.repository.ProductRepository
import kotlinx.coroutines.flow.Flow
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ProductRepositoryImpl @Inject constructor(
    private val productDao: ProductDao,
    private val storeDao: StoreDao,
    private val basketDao: BasketDao
) : ProductRepository {

    override fun searchProducts(query: String): Flow<List<ProductEntity>> {
        return productDao.searchProducts("%$query%")
    }

    override suspend fun getProductById(productId: String): ProductEntity? {
        return productDao.getProductById(productId)
    }

    override fun getPricesForProduct(productId: String): Flow<List<StorePriceEntity>> {
        return productDao.getPricesForProduct(productId)
    }

    override fun getAllStores(): Flow<List<SupermarketEntity>> {
        return storeDao.getAllStores()
    }

    override fun getAllBaskets(): Flow<List<ShoppingBasketEntity>> {
        return basketDao.getAllBaskets()
    }

    override suspend fun createBasket(basketName: String) {
        val basket = ShoppingBasketEntity(
            id = UUID.randomUUID().toString(),
            name = basketName,
            createdAt = System.currentTimeMillis()
        )
        basketDao.insertBasket(basket)
    }

    override suspend fun addProductToBasket(basketId: String, productId: String, quantity: Int) {
        val item = BasketItemEntity(
            id = UUID.randomUUID().toString(),
            basketId = basketId,
            productId = productId,
            quantity = quantity
        )
        basketDao.insertBasketItems(listOf(item))
    }

    override fun getItemsInBasket(basketId: String): Flow<List<BasketItemEntity>> {
        return basketDao.getItemsInBasket(basketId)
    }

    override suspend fun syncRemoteData() {
        // Baseline remote data ingestion representing the Australian supermarkets price feed ingestion
        val baselineStores = listOf(
            SupermarketEntity("woolworths_richmond", "Woolworths", "Richmond Plaza", -37.8183, 144.9984, "7am - 10pm"),
            SupermarketEntity("coles_richmond", "Coles", "Richmond Central", -37.8190, 144.9960, "6am - midnight"),
            SupermarketEntity("aldi_richmond", "ALDI", "Richmond", -37.8175, 144.9972, "8:30am - 8pm"),
            SupermarketEntity("iga_richmond", "IGA", "Richmond Local", -37.8210, 145.0020, "7am - 9pm"),
            SupermarketEntity("costco_docklands", "Costco", "Docklands", -37.8120, 144.9370, "10am - 8:30pm")
        )
        storeDao.insertStores(baselineStores)

        val baselineProducts = listOf(
            ProductEntity("prod_milk_devondale", "9310072001222", "Devondale Long Life Full Cream Milk", "Dairy", "Devondale", "", 1.0, "L"),
            ProductEntity("prod_bread_wonder", "9310072002345", "Wonder White Sliced Bread", "Bakery", "Wonder", "", 700.0, "g"),
            ProductEntity("prod_eggs_sunny", "9310072003456", "Sunny Queen Free Range Eggs 12pk", "Dairy", "Sunny Queen", "", 700.0, "g"),
            ProductEntity("prod_rice_sunwhite", "9310072004567", "Sunwhite Jasmine Rice 5kg", "Pantry", "Sunwhite", "", 5.0, "kg"),
            ProductEntity("prod_pasta_sanremo", "9310072005678", "San Remo Spaghetti No 5", "Pantry", "San Remo", "", 500.0, "g"),
            ProductEntity("prod_laundry_dynamo", "9310072006789", "Dynamo Professional Laundry Liquid 1.8L", "Household", "Dynamo", "", 1.8, "L"),
            ProductEntity("prod_laundry_omo", "9310072006790", "Omo Active Clean Laundry Liquid 2L", "Household", "Omo", "", 2.0, "L"),
            ProductEntity("prod_laundry_coldpower", "9310072006791", "Cold Power Regular Laundry Liquid 2L", "Household", "Cold Power", "", 2.0, "L"),
            ProductEntity("prod_laundry_biozet", "9310072006792", "Biozet Attack Regular Laundry Powder 2kg", "Household", "Biozet Attack", "", 2.0, "kg"),
            ProductEntity("prod_laundry_radiant", "9310072006793", "Radiant Mixed Colour Laundry Liquid 2L", "Household", "Radiant", "", 2.0, "L"),
            ProductEntity("prod_laundry_fab", "9310072006794", "Fab Essential Laundry Liquid 2L", "Household", "Fab", "", 2.0, "L"),
            ProductEntity("prod_laundry_surf", "9310072006795", "Surf Tropical Fresh Laundry Powder 2kg", "Household", "Surf", "", 2.0, "kg"),
            ProductEntity("prod_laundry_house", "9310072006796", "Everyday Clean Laundry Liquid 2L", "Household", "Supermarket Brand", "", 2.0, "L")
        )
        productDao.insertProducts(baselineProducts)

        val baselinePrices = listOf(
            // Milk
            StorePriceEntity("prod_milk_devondale", "woolworths_richmond", 1.85, 2.20, 1.85, true, "Save 35c", System.currentTimeMillis()),
            StorePriceEntity("prod_milk_devondale", "coles_richmond", 1.85, 1.85, 1.85, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_milk_devondale", "aldi_richmond", 1.60, 1.60, 1.60, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_milk_devondale", "iga_richmond", 2.15, 2.15, 2.15, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_milk_devondale", "costco_docklands", 1.45, 1.45, 1.45, false, "", System.currentTimeMillis()),
            // Bread
            StorePriceEntity("prod_bread_wonder", "woolworths_richmond", 3.40, 4.20, 0.49, true, "Save 80c", System.currentTimeMillis()),
            StorePriceEntity("prod_bread_wonder", "coles_richmond", 3.90, 3.90, 0.56, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_bread_wonder", "aldi_richmond", 2.80, 2.80, 0.40, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_bread_wonder", "iga_richmond", 4.10, 4.10, 0.59, false, "", System.currentTimeMillis()),
            // Eggs
            StorePriceEntity("prod_eggs_sunny", "woolworths_richmond", 5.20, 5.20, 0.43, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_eggs_sunny", "coles_richmond", 4.90, 5.80, 0.41, true, "Save 90c", System.currentTimeMillis()),
            StorePriceEntity("prod_eggs_sunny", "aldi_richmond", 4.60, 4.60, 0.38, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_eggs_sunny", "iga_richmond", 5.90, 5.90, 0.49, false, "", System.currentTimeMillis()),
            // Laundry - Dynamo
            StorePriceEntity("prod_laundry_dynamo", "woolworths_richmond", 13.50, 27.00, 7.50, false, "Save $13.50", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_dynamo", "coles_richmond", 20.00, 20.00, 11.11, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_dynamo", "aldi_richmond", 12.00, 12.00, 6.67, true, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_dynamo", "iga_richmond", 22.00, 22.00, 12.22, false, "", System.currentTimeMillis()),
            // Laundry - Omo
            StorePriceEntity("prod_laundry_omo", "woolworths_richmond", 24.00, 24.00, 12.00, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_omo", "coles_richmond", 12.00, 24.00, 6.00, true, "Save $12.00", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_omo", "aldi_richmond", 14.00, 14.00, 7.00, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_omo", "iga_richmond", 26.00, 26.00, 13.00, false, "", System.currentTimeMillis()),
            // Laundry - Cold Power
            StorePriceEntity("prod_laundry_coldpower", "woolworths_richmond", 11.00, 22.00, 5.50, true, "Save $11.00", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_coldpower", "coles_richmond", 22.00, 22.00, 11.00, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_coldpower", "aldi_richmond", 11.50, 11.50, 5.75, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_coldpower", "iga_richmond", 23.00, 23.00, 11.50, false, "", System.currentTimeMillis()),
            // Laundry - Biozet
            StorePriceEntity("prod_laundry_biozet", "woolworths_richmond", 22.00, 22.00, 11.00, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_biozet", "coles_richmond", 24.00, 24.00, 12.00, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_biozet", "aldi_richmond", 18.00, 24.00, 9.00, true, "Save $6.00", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_biozet", "iga_richmond", 26.00, 26.00, 13.00, false, "", System.currentTimeMillis()),
            // Laundry - Radiant
            StorePriceEntity("prod_laundry_radiant", "woolworths_richmond", 10.00, 20.00, 5.00, true, "Save $10.00", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_radiant", "coles_richmond", 20.00, 20.00, 10.00, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_radiant", "aldi_richmond", 11.00, 11.00, 5.50, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_radiant", "iga_richmond", 22.00, 22.00, 11.00, false, "", System.currentTimeMillis()),
            // Laundry - Fab
            StorePriceEntity("prod_laundry_fab", "woolworths_richmond", 6.00, 12.00, 3.00, true, "Save $6.00", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_fab", "coles_richmond", 12.00, 12.00, 6.00, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_fab", "aldi_richmond", 8.00, 8.00, 4.00, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_fab", "iga_richmond", 13.00, 13.00, 6.50, false, "", System.currentTimeMillis()),
            // Laundry - Surf
            StorePriceEntity("prod_laundry_surf", "woolworths_richmond", 8.50, 8.50, 4.25, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_surf", "coles_richmond", 8.50, 8.50, 4.25, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_surf", "aldi_richmond", 7.00, 7.00, 3.50, true, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_surf", "iga_richmond", 9.50, 9.50, 4.75, false, "", System.currentTimeMillis()),
            // Laundry - House brand
            StorePriceEntity("prod_laundry_house", "woolworths_richmond", 3.50, 3.50, 1.75, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_house", "coles_richmond", 3.50, 3.50, 1.75, false, "", System.currentTimeMillis()),
            StorePriceEntity("prod_laundry_house", "aldi_richmond", 3.49, 3.49, 1.75, true, "", System.currentTimeMillis())
        )
        productDao.insertPrices(baselinePrices)
    }
}
