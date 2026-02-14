# ============================================================
# ULTIMATE BRAIN — STEP 2 FINAL DATA INGESTION ENGINE
# ============================================================

import sqlite3
import datetime
import time
import requests
from threading import Thread

DB_NAME = "ultimate_brain_data.db"

# ---------------- DATABASE ----------------
def init_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS market_prices(
        symbol TEXT,
        price REAL,
        timestamp TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS news_feed(
        headline TEXT,
        source TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized")


# ---------------- SAFE FETCH ----------------
def safe_fetch(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200 and r.text.strip():
            return r.json()
    except Exception as e:
        print("Fetch error:", e)
    return None


# ---------------- PRICE INGESTION ----------------
def ingest_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    data = safe_fetch(url)

    if data:
        price = float(data["bpi"]["USD"]["rate"].replace(",", ""))
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO market_prices VALUES (?, ?, ?)",
            ("TEST", price, str(datetime.datetime.now()))
        )
        conn.commit()
        conn.close()
        print("Price stored:", price)


# ---------------- NEWS INGESTION ----------------
def ingest_news():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO news_feed VALUES (?, ?, ?)",
        ("Sample market update", "system", str(datetime.datetime.now()))
    )
    conn.commit()
    conn.close()
    print("News stored")


# ---------------- LOOP ----------------
def ingestion_loop():
    while True:
        print("Step-2 ingestion running...")
        ingest_price()
        ingest_news()
        time.sleep(3600)


def start_step2_engine():
    init_database()
    Thread(target=ingestion_loop, daemon=True).start()
    print("STEP-2 ENGINE ACTIVE")


if __name__ == "__main__":
    start_step2_engine()
