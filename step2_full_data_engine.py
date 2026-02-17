# PRODUCTION NSE LIVE DATA INGESTION ENGINE
# Stable, retry-enabled, continuous ingestion

from nsepython import nse_eq
from datetime import datetime
import time
import logging

# ---------------- CONFIG ----------------
SYMBOLS = ["RELIANCE", "TCS", "HDFCBANK"]
FETCH_INTERVAL = 60          # seconds
MAX_RETRY = 3                # retry attempts
# ----------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def fetch_price(symbol):
    """
    Fetch NSE price with retry logic
    """
    for attempt in range(MAX_RETRY):
        try:
            data = nse_eq(symbol)

            price = float(data["priceInfo"]["lastPrice"])
            volume = int(data["securityWiseDP"]["quantityTraded"])

            return price, volume

        except Exception as e:
            logging.warning(f"{symbol} retry {attempt+1}: {e}")
            time.sleep(2)

    logging.error(f"{symbol} failed after retries")
    return 0, 0


def ingestion_cycle():
    """
    Continuous ingestion loop
    """
    logging.info("NSE ingestion engine started")

    while True:
        timestamp = datetime.now()

        for symbol in SYMBOLS:
            price, volume = fetch_price(symbol)

            record = {
                "symbol": f"{symbol}.NS",
                "price": price,
                "volume": volume,
                "timestamp": str(timestamp)
            }

            logging.info(f"INGESTION {record}")

        time.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    ingestion_cycle()
