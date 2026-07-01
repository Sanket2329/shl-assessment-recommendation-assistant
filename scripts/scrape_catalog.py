import json
import requests
from bs4 import BeautifulSoup


class SHLCatalogScraper:

    BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"

    def __init__(self):
        self.assessments = []

    def scrape(self):

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(
            self.BASE_URL,
            headers=headers,
            timeout=30
        )

        print(response.status_code)
        print("Length:", len(response.text))

        with open("page.html", "w", encoding="utf-8") as f:
         f.write(response.text)

         print("Saved page.html")


if __name__ == "__main__":
    scraper = SHLCatalogScraper()
    scraper.scrape()