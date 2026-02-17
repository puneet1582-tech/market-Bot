# =====================================================
# INSTITUTIONAL-GRADE NSE INGESTION ENGINE (SCALABLE)
# Reliable, Retry Logic, Validation, Logging
# =====================================================

from nsepython import nse_eq
from datetime import datetime
import logging
import time
import sys

# ---------------- CONFIG ----------------
SYMBOLS = ["RELIANCE", "TCS", "HDFCBANK"]
FETCH_INTERVAL = 60
MAX_RETRY = 3
RETRY_DELAY = 2
# ----------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("ingestion.log")
    ]
)

def fetch_price(symbol):
    """
    Fetch live NSE price safely with retries
    """
    for attempt in range(MAX_RETRY):
        try:
            data = nse_eq(symbol)

            if "priceInfo" not in data:
                raise Exception("priceInfo missing")

            price = float(data["priceInfo"]["lastPrice"])

            volume = 0
            if "securityWiseDP" in data and "quantityTraded" in data["securityWiseDP"]:
                volume = int(data["securityWiseDP"]["quantityTraded"])

            return price, volume

        except Exception as e:
            logging.warning(f"{symbol} retry {attempt+1}/{MAX_RETRY}: {e}")
            time.sleep(RETRY_DELAY)

    logging.error(f"{symbol} failed after retries")
    return 0, 0


def ingestion_cycle():
    """
    Continuous ingestion loop
    """
    logging.info("NSE Institutional Ingestion Engine Started")

    while True:
        cycle_time = datetime.now()

        for symbol in SYMBOLS:
            price, volume = fetch_price(symbol)

            record = {
                "symbol": f"{symbol}.NS",
                "price": price,
                "volume": volume,
                "timestamp": str(cycle_time)
            }

            logging.info(f"INGESTION {record}")

        time.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    try:
        ingestion_cycle()
    except KeyboardInterrupt:
        logging.info("Engine stopped manually")
