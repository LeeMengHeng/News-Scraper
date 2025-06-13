from scrapers import bbc_scraper, bitcoin_scraper, cnn_scraper, digitimes_scraper, techcrunch_scraper, qz_scraper, handelsblatt_scraper, mk_scraper

def run_all():
    bbc_scraper.run()
    bitcoin_scraper.run()
    techcrunch_scraper.run()
    cnn_scraper.run()
    qz_scraper.run()
    handelsblatt_scraper.run()
    mk_scraper.run()

if __name__ == "__main__":
    run_all()
