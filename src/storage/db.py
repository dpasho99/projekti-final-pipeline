import sqlite3
from pathlib import Path

DB_PATH = Path("data/processed/books.sqlite")

def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price_gbp REAL,
                rating TEXT,
                in_stock INTEGER,
                source_url_enc TEXT,
                source_url_hash TEXT,
                country_input TEXT,
                region TEXT,
                population INTEGER,
                currencies TEXT
            )
        """)
        con.commit()

def insert_books(rows: list[dict]) -> None:
    with sqlite3.connect(DB_PATH) as con:
        con.executemany("""
            INSERT INTO books (
                title, price_gbp, rating, in_stock,
                source_url_enc, source_url_hash,
                country_input, region, population, currencies
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                r.get("title"),
                r.get("price_gbp"),
                r.get("rating"),
                1 if r.get("in_stock") else 0,
                r.get("source_url_enc"),
                r.get("source_url_hash"),
                r.get("country_input"),
                r.get("region"),
                r.get("population"),
                r.get("currencies"),
            )
            for r in rows
        ])
        con.commit()