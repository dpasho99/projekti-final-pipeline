import logging
from dotenv import load_dotenv
import pandas as pd

from src.utils.logging_config import setup_logging
from src.scraping.scraper import scrape_books
from src.processing.transform import clean, enrich_with_country, compute_metrics
from src.security.crypto import encrypt_text, hash_text
from src.storage.db import init_db, insert_books

log = logging.getLogger(__name__)

def run(pages: int = 3) -> None:
    load_dotenv()
    setup_logging()

    log.info("Starting pipeline...")

    # 1) Scraping
    raw_data = scrape_books(pages=pages)
    df = pd.DataFrame(raw_data)
    log.info("Scraped %s records", len(df))
    # 2) Clean
    df = clean(df)

    # 3) API Enrichment
    df = enrich_with_country(df)

    # 4) Security (Encryption + Hashing)
    df["source_url_enc"] = df["source_url"].apply(
        lambda x: encrypt_text(x) if isinstance(x, str) else None
    )
    df["source_url_hash"] = df["source_url"].apply(
        lambda x: hash_text(x) if isinstance(x, str) else None
    )

    # 5) Storage (SQLite)
    init_db()
    insert_books(df.to_dict(orient="records"))
    log.info("Inserted %s rows into SQLite", len(df))

    # 6) Export processed data
    df.to_csv("data/processed/books_enriched.csv", index=False)

    # 7) Metrics export
    metrics = compute_metrics(df)
    metrics.to_csv("data/processed/metrics.csv", index=False)

    log.info("Pipeline finished successfully!")
    log.info("Outputs saved in data/processed/")

if __name__ == "__main__":
    run(pages=3)