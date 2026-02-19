import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

log = logging.getLogger(__name__)

@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type((requests.Timeout, requests.ConnectionError)),
)
def get_country_info(country_name: str) -> dict | None:
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    resp = requests.get(url, timeout=15, params={"fullText": "true"})
    if resp.status_code == 404:
        log.warning("Country not found: %s", country_name)
        return None
    resp.raise_for_status()

    data = resp.json()
    if not data:
        return None

    c = data[0]
    currencies = list((c.get("currencies") or {}).keys())
    return {
        "country": c.get("name", {}).get("common"),
        "region": c.get("region"),
        "subregion": c.get("subregion"),
        "population": c.get("population"),
        "currencies": ",".join(currencies) if currencies else None,
    }