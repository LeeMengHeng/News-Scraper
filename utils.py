# utils.py
from pymongo import MongoClient

MONGO_URI = ""
DB_NAME = "webNews"
COLLECTION_NAME = "webNews"

def get_mongo_collection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

def insert_articles(article_list):
    if not article_list:
        print("⚠️ No articles to insert.")
        return
    collection = get_mongo_collection()
    result = collection.insert_many(article_list)
    print(f"✅ Inserted {len(result.inserted_ids)} documents into MongoDB.")
