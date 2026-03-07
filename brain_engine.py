# SAFE BRAIN ENGINE (NO EXTERNAL DEPENDENCY)

from step2_full_data_engine import fetch_price
from datetime import datetime

SYMBOLS = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS"]

def run():
    for s in SYMBOLS:
        price = fetch_price(s)
        print("INGESTION:", {
            "symbol": s,
            "price": price,
            "timestamp": str(datetime.utcnow())
        })

# disabled_entry_point


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
