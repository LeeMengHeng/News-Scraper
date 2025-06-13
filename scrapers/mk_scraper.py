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

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        paragraphs = soup.select("div.news_cnt_detail_wrap p")
        # If no article found, we return None
        if not paragraphs:
            return None

        content = "\n".join(
            p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20
        )
        return content or "[Paragraphs found but content empty]"
    
    except Exception as e:
        return f"[Error fetching article: {e}]"

# Main scraper
def run():
    try:
        driver.get("https://www.mk.co.kr/")
        WebDriverWait(driver, 10)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        divs = []
        for a in soup.select('ul.top_news_list a'):
            if a.find("span"):
                continue
            else:
                divs.append(a)

        articles = []   
        seen_url = []
        counter = 0
        for div in divs:
            # Limit to 10 articles
            if counter == 10:
                break

            href = div.get("href")
            full_url = href if href.startswith("http") else "https://www.mk.co.kr/" + href
            # If URL already visited, we skip
            if full_url in seen_url:
                continue

            # title = divs[counter].get_text(strip=True)

            seen_url.append(full_url)
            content = extract_article_content(full_url)
            if content != None:
                articles.append({
                    "爬蟲日期時間": datetime.now(),
                    "新聞網站名稱": "MK",
                    "新聞來源國家": "KOR",
                    "新聞內容": content,
                    "該新聞原始連結": full_url
                })
            else:
                continue

            counter += 1

        insert_articles(articles)
        # df = pd.DataFrame(articles)
        # df.to_excel("MK_Scraped.xlsx", index=False)
        print("✅ MK Scraper Done")

    finally:
        driver.quit()
