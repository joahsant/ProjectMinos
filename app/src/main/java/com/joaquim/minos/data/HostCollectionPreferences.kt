package com.joaquim.minos.data

import android.content.Context
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

class HostCollectionPreferences(
    context: Context,
    private val json: Json = Json,
) {
    private val preferences = context.getSharedPreferences(PREFERENCES_NAME, Context.MODE_PRIVATE)

    fun loadCollectionIds(): List<String> {
        val rawValue = preferences.getString(KEY_COLLECTION_IDS, null) ?: return listOf(DEFAULT_COLLECTION_ID)
        return runCatching { json.decodeFromString<List<String>>(rawValue) }
            .getOrElse { listOf(DEFAULT_COLLECTION_ID) }
            .ifEmpty { listOf(DEFAULT_COLLECTION_ID) }
    }

    fun saveCollectionIds(collectionIds: List<String>) {
        preferences.edit()
            .putString(KEY_COLLECTION_IDS, json.encodeToString(collectionIds.distinct()))
            .apply()
    }

    fun loadSelectedCoinId(): String {
        return preferences.getString(KEY_SELECTED_COIN_ID, DEFAULT_COLLECTION_ID) ?: DEFAULT_COLLECTION_ID
    }

    fun saveSelectedCoinId(coinId: String) {
        preferences.edit()
            .putString(KEY_SELECTED_COIN_ID, coinId)
            .apply()
    }

    private companion object {
        const val PREFERENCES_NAME = "minos_host_collection"
        const val KEY_COLLECTION_IDS = "collection_ids"
        const val KEY_SELECTED_COIN_ID = "selected_coin_id"
        const val DEFAULT_COLLECTION_ID = "bitcoin"
    }
}
