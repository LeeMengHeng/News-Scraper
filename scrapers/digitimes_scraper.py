from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time
import requests
from utils import insert_articles

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

def extract_article_content(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10)
        time.sleep(2)

        # res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        paragraphs = soup.select("div.article__body p")
        return "\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20)
    except Exception as e:
        return f"[Error fetching article: {e}]"

# Main scraper
def run():
    try:
        driver.get("https://www.digitimes.com.tw/")
        WebDriverWait(driver, 10)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        divs = soup.select('#Realtime a')
        print(divs)
        articles = []
        for a in divs[:10]:  # limit to first 10
            href = a.get("href")
            full_url = href if href.startswith("http") else "https://www.digitimes.com.tw/" + href
            title = a.get_text(strip=True)
            content = extract_article_content(full_url)

            articles.append({
                "爬蟲日期時間": datetime.now(),
                "新聞網站名稱": "DigiTimes",
                "新聞來源國家": "Global",
                "新聞內容": content,
                "該新聞原始連結": full_url
            })

        # insert_articles(articles)
        df = pd.DataFrame(articles)
        df.to_excel("Digitimes_News_Scraped.xlsx", index=False)
        print("✅ Digitimes Scraper Done")

    finally:
        driver.quit()
