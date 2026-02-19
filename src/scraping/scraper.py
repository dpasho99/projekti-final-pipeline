import os
import re
import logging
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

log = logging.getLogger(__name__)

BASE_URL = "https://books.toscrape.com/"


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": os.getenv("USER_AGENT", "ProjektiFinal/1.0"),
            "Accept-Language": "en-US,en;q=0.9",
        }
    )
    return s


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type((requests.Timeout, requests.ConnectionError)),
)
def fetch_html(url: str) -> str:
    timeout = int(os.getenv("HTTP_TIMEOUT", "15"))
    resp = _session().get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def _parse_price_to_float(price_text: str) -> float | None:
    """
    Robust parsing to handle encoding issues (e.g., 'Â£51.77') and extract the numeric value.
    Returns None if no number is found.
    """
    if not price_text:
        return None
    m = re.search(r"(\d+(\.\d+)?)", price_text)
    return float(m.group(1)) if m else None


def scrape_books(pages: int = 3) -> list[dict]:
    """
    Scrape N pages from books.toscrape.com and return a list of dict records.
    Fields:
      - title
      - price_gbp
      - rating
      - in_stock
      - source_url
    """
    results: list[dict] = []
    next_url = BASE_URL + "catalogue/page-1.html"

    for page in range(1, pages + 1):
        log.info("Scraping page %s: %s", page, next_url)
        html = fetch_html(next_url)
        soup = BeautifulSoup(html, "html.parser")

        for article in soup.select("article.product_pod"):
            title = article.h3.a.get("title", "").strip()

            price_text = article.select_one(".price_color").get_text(strip=True)
            price_val = _parse_price_to_float(price_text)

            rating_classes = article.select_one("p.star-rating").get("class", [])
            rating = (
                [c for c in rating_classes if c != "star-rating"][0]
                if len(rating_classes) > 1
                else "Unknown"
            )

            availability_text = article.select_one(".availability").get_text(" ", strip=True)
            in_stock = "In stock" in availability_text

            rel_url = article.h3.a.get("href", "")
            product_url = BASE_URL + "catalogue/" + rel_url.replace("../", "")

            results.append(
                {
                    "title": title,
                    "price_gbp": price_val,
                    "rating": rating,
                    "in_stock": in_stock,
                    "source_url": product_url,
                }
            )

        next_link = soup.select_one("li.next a")
        if not next_link:
            break

        next_url = BASE_URL + "catalogue/" + next_link.get("href")

    return results