
# 📰 News Scraper System

This project is a Python-based web scraper that collects the latest news articles from multiple international news websites, parses the article content, and exports the results into both Excel files and an optional MongoDB collection.

---

## 📌 Features

- Supports 20+ global news websites (BBC, Bloomberg, Bitcoin.com, etc.)
- Automatically extracts:
  - Article title
  - Full content
  - Original URL
  - Scrape timestamp
  - News source site and country
- Export to Excel for human-readable backup
- (Optional) Automatically store into MongoDB

---

## 🗃️ Output Schema

Each scraped article contains the following fields:

| Field             | Description                                      |
|------------------|--------------------------------------------------|
| `爬蟲日期時間`      | Timestamp of when the article was scraped        |
| `新聞網站名稱`      | Name of the news site (e.g., "BBC")             |
| `新聞來源國家`      | Country of origin (e.g., "UK", "USA", "Taiwan") |
| `新聞內容`         | Full article body text                           |
| `該新聞原始連結`    | Direct link to the original article              |

---

## 📂 Project Structure

```
news_scraper_project/
├── scrapers/              # Scrapers for individual news sites
│   ├── bbc_scraper.py
│   ├── bloomberg_scraper.py
│   ├── bitcoin_scraper.py
│   └── ...
├── utils.py               # Shared helper functions (e.g., DB insert)
├── main.py                # Main runner that calls all scrapers
├── .env.example           # Example environment file for MongoDB URI
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## ⚙️ Setup Instructions

### 1. Clone or unzip the project
```bash
unzip news_scraper_project.zip
cd news_scraper_project
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. (If using Playwright) Install browser engine
```bash
playwright install
```

---

## 🔐 MongoDB Setup (Optional)

1. Copy the example environment config:
```bash
cp .env.example .env
```

2. Edit `.env` and insert your MongoDB connection URI:
```
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
```

> If you’re not using MongoDB, you can ignore this step. The scraper will still export Excel files.

---

## ▶️ How to Run

Run all scrapers at once:
```bash
python main.py
```

You’ll find Excel files like:
```
BBC_News_Scraped.xlsx
Bitcoin_News_Scraped.xlsx
CTEE_News_Scraped.xlsx
```

If MongoDB is enabled, articles will also be inserted into the specified collection.

---

## 🧼 Clear Data from MongoDB (optional)

To remove all previously inserted articles:

```python
from pymongo import MongoClient

client = MongoClient("your_mongo_uri")
collection = client["webNews"]["webNews"]
collection.delete_many({})
```

---

## 🧠 Notes

- Some websites use JavaScript rendering or anti-bot protections. The project uses **Playwright** or **Selenium** when necessary.
- Slow sites may require adjusting `time.sleep()` or timeout settings in each scraper.

---

## 👤 Contact

This project was delivered by Meng-Heng Lee.  
If you need help running or deploying the scraper, feel free to contact me.
