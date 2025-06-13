from pymongo import MongoClient
from datetime import datetime
from datetime import datetime, timedelta

# 用戶提供的 MongoDB URI
MONGO_URI = "mongodb+srv://bing:eTRUKG4ihehqVX5Y@webnews.d8cuzzn.mongodb.net/?retryWrites=true&w=majority&appName=webNews"
DB_NAME = "webNews"
COLLECTION_NAME = "webNews"

def test_connection():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        test_doc = {
            "爬蟲日期時間": datetime.now(),
            "新聞網站名稱": "TestSite",
            "新聞來源國家": "TestLand",
            "新聞內容": "這是新的 schema 格式測試資料。",
            "該新聞原始連結": "https://example.com/new-schema-test"
        }

        result = collection.insert_one(test_doc)
        print("✅ 成功插入測試資料，ID:", result.inserted_id)

        # 驗證寫入資料
        fetched = collection.find_one({"_id": result.inserted_id})
        print("🔎 成功讀取資料:", fetched)

        # 清除測試資料（可選）
        collection.delete_one({"_id": result.inserted_id})
        print("🧹 測試資料已刪除")

    except Exception as e:
        print("❌ 連線或寫入失敗:", e)

def check_history():   
    MONGO_URI = "mongodb+srv://bing:eTRUKG4ihehqVX5Y@webnews.d8cuzzn.mongodb.net/?retryWrites=true&w=majority&appName=webNews"
    client = MongoClient(MONGO_URI)
    collection = client["webNews"]["webNews"]

    today = datetime.now()
    yesterday = today - timedelta(days=1)

    count = collection.count_documents({
        "爬蟲日期時間": {"$gte": yesterday}
    })
    print(f"🧾 Documents added in last 24h: {count}")
    # Delete documents by website name
    result = collection.delete_many({})
    print(f"✅ Deleted {result.deleted_count} documents.")


if __name__ == "__main__":
    # test_connection()
    check_history()
