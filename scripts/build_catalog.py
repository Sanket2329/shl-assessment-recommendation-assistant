import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.shl.com/products/product-catalog/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}

response = requests.get(URL, headers=HEADERS, timeout=30)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.title.text)