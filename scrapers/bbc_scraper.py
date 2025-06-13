import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from utils import insert_articles

# Function for article content extraction
def extract_article_content(article_url):
    headers = {
    "User-Agent": "Mozilla/5.0"
    }
    try:
        res = requests.get(article_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        article_tag = soup.find("article")

        # If no article found, we return None
        if not article_tag:
            return None
        
        paragraphs = article_tag.find_all("p")
        content = "\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20)
        return content or "[Article found, but empty]"
    
    except Exception as e:
        return f"[Error fetching article: {e}]"
    
def run():
    # Target URL
    url = "https://www.bbc.com/business"

    # Custom headers to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Send request
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.select('div[data-testid$="-card"]')

    articles = []
    seen_url = []
    counter = 0
    for div in divs:

        # Limit to 10 articles
        if counter == 10:
            break

        a_tag = div.select_one('a[data-testid="internal-link"]')
        if not a_tag:
            continue

        href = a_tag.get("href")
        full_url = "https://www.bbc.com" + href if href.startswith("/") else href

        # If URL already visited, we skip
        if full_url in seen_url:
            continue
        
        seen_url.append(full_url)

        # title = divs[counter].select_one('h2[data-testid="card-headline"]')
        # summary = divs[counter].select_one('p[data-testid="card-description"]')

        content = extract_article_content(full_url)

        # Check if content is None
        if content != None:
            articles.append({
                "爬蟲日期時間": datetime.now(),
                "新聞網站名稱": "BBC",
                "新聞來源國家": "UK",
                "新聞內容": content,
                "該新聞原始連結": full_url
            })
        else:
            continue

        counter += 1

    insert_articles(articles)
    # df = pd.DataFrame(articles)
    # df.to_excel("BBC_News_Scraped.xlsx", index=False)
    print("✅ BBC Scraper Done")